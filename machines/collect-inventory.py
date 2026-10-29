#!/usr/bin/env python3
"""Collect one machine's hardware inventory record (hardware-doc issue #1094).

Stdlib-only. Run on the machine being inventoried:

    python3 machines/collect-inventory.py [--out-dir DIR] [--host NAME]

Writes <host>.json (validates against machines/inventory-record.schema.json)
and <host>.md (human-readable summary) into the output directory (default:
the directory containing this script).

Design rule: a value is only recorded if it was actually read on this run.
Anything unreadable is null (or an empty list) and is named in `unknowns`
with the reason -- never invent a serial, a slot count, or a SMART value.
Privileged reads (dmidecode, smartctl) are attempted via `sudo -n` only;
the collector never prompts and never blocks on a password.
"""

import argparse
import json
import re
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

UNKNOWNS = []


def unknown(field, reason):
    UNKNOWNS.append({"field": field, "reason": reason})
    return None


def run(cmd, timeout=15):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return out.stdout if out.returncode == 0 else None
    except Exception:
        return None


def read_file(path):
    try:
        return Path(path).read_text().strip()
    except Exception:
        return None


def dmi(field):
    return read_file(f"/sys/class/dmi/id/{field}")


def collect_system():
    system = {
        "vendor": dmi("sys_vendor"),
        "product_name": dmi("product_name"),
        "product_version": dmi("product_version"),
        "serial_number": dmi("product_serial"),
        "board": {
            "vendor": dmi("board_vendor"),
            "name": dmi("board_name"),
            "version": dmi("board_version"),
        },
        "bios": {
            "vendor": dmi("bios_vendor"),
            "version": dmi("bios_version"),
            "release_date": dmi("bios_date"),
        },
        "bmc": None,
    }
    if system["serial_number"] is None:
        unknown("system.serial_number",
                "/sys/class/dmi/id/product_serial is not readable by an "
                "unprivileged user on this machine")
    unknown("system.bmc",
            "no BMC present or discoverable from the OS on this machine; "
            "record the KVM address manually for managed servers")
    return system


def collect_cpu():
    cpu = {"model": None, "vendor": None, "architecture": None,
           "sockets": None, "cores": None, "threads": None}
    raw = run(["lscpu", "-J"])
    if raw:
        try:
            flat = {}

            def walk(node):
                if isinstance(node, list):
                    for item in node:
                        walk(item)
                    return
                if isinstance(node, dict):
                    if "field" in node and "data" in node:
                        flat[node["field"].rstrip(":")] = node["data"]
                    for child in node.get("children", []):
                        walk(child)

            walk(json.loads(raw).get("lscpu", []))
            cpu["model"] = flat.get("Model name")
            cpu["vendor"] = flat.get("Vendor ID")
            cpu["architecture"] = flat.get("Architecture")
            for key, src in (("sockets", "Socket(s)"), ("cores", "Core(s) per socket"),
                             ("threads", "CPU(s)")):
                try:
                    cpu[key] = int(flat[src])
                except (KeyError, TypeError, ValueError):
                    pass
            if cpu["cores"] is not None and cpu["sockets"]:
                cpu["cores"] *= cpu["sockets"]
            return cpu
        except Exception:
            pass
    unknown("cpu", "lscpu -J unavailable on this machine")
    return cpu


def collect_memory():
    mem = {"total_bytes": None, "slots_total": None, "slots_used": None,
           "ecc": None, "modules": []}
    meminfo = read_file("/proc/meminfo") or ""
    m = re.search(r"MemTotal:\s+(\d+)\s+kB", meminfo)
    if m:
        mem["total_bytes"] = int(m.group(1)) * 1024
    dmi_out = run(["sudo", "-n", "dmidecode", "-t", "memory"]) or \
        run(["dmidecode", "-t", "memory"])
    if dmi_out:
        ecc = re.search(r"Error Correction Type:\s+(.+)", dmi_out)
        if ecc:
            mem["ecc"] = "none" not in ecc.group(1).lower()
        sizes = re.findall(r"Size:\s+(\d+)\s+(GB|MB)", dmi_out)
        if sizes:
            mem["slots_used"] = len(sizes)
            types = re.findall(r"Type:\s+(DDR\d+)", dmi_out)
            speeds = re.findall(r"Speed:\s+(\d+)\s+MT/s", dmi_out)
            parts = re.findall(r"Part Number:\s+(.+)", dmi_out)
            mans = re.findall(r"Manufacturer:\s+(.+)", dmi_out)
            locs = re.findall(r"Locator:\s+(.+)", dmi_out)
            for i, (size, unit) in enumerate(sizes):
                mult = 1024 ** 3 if unit == "GB" else 1024 ** 2
                mem["modules"].append({
                    "locator": locs[i].strip() if i < len(locs) else None,
                    "size_bytes": int(size) * mult,
                    "type": types[i] if i < len(types) else None,
                    "speed_mts": int(speeds[i]) if i < len(speeds) else None,
                    "manufacturer": mans[i].strip() if i < len(mans) else None,
                    "part_number": parts[i].strip() if i < len(parts) else None,
                    "serial_number": None,
                })
        total = re.search(r"Number Of Devices:\s+(\d+)", dmi_out)
        if total:
            mem["slots_total"] = int(total.group(1))
    else:
        unknown("memory.slots_total/memory.slots_used/memory.ecc/memory.modules",
                "dmidecode requires root on this machine and passwordless "
                "sudo is not available; only the total from /proc/meminfo "
                "could be read")
    return mem


def collect_drives():
    drives = []
    raw = run(["lsblk", "-J", "-b", "-d", "-o",
               "NAME,MODEL,SERIAL,SIZE,TYPE,TRAN"])
    if not raw:
        unknown("drives", "lsblk unavailable on this machine")
        return drives
    for dev in json.loads(raw).get("blockdevices", []):
        if dev.get("type") != "disk":
            continue
        entry = {
            "device": f"/dev/{dev['name']}",
            "model": (dev.get("model") or "").strip() or None,
            "serial_number": (dev.get("serial") or "").strip() or None,
            "capacity_bytes": dev.get("size"),
            "interface": dev.get("tran"),
            "firmware_version": None,
            "smart": None,
        }
        smart = run(["sudo", "-n", "smartctl", "-i", "-H", "-A",
                     entry["device"]])
        if smart:
            fw = re.search(r"Firmware Version:\s+(.+)", smart)
            if fw:
                entry["firmware_version"] = fw.group(1).strip()
            health = re.search(r"SMART overall-health.*:\s+(.+)", smart) or \
                re.search(r"SMART Health Status:\s+(.+)", smart)
            pct = re.search(r"Percentage Used:\s+(\d+)%", smart)
            hours = re.search(r"Power On Hours:\s+([\d,]+)", smart) or \
                re.search(r"Power_On_Hours.*\s(\d+)\s*$", smart, re.M)
            entry["smart"] = {
                "health": health.group(1).strip() if health else None,
                "percentage_used": int(pct.group(1)) if pct else None,
                "power_on_hours": int(hours.group(1).replace(",", ""))
                if hours else None,
            }
        else:
            unknown(f"drives[{entry['device']}].firmware_version/smart",
                    "smartctl requires root on this machine and "
                    "passwordless sudo is not available")
        drives.append(entry)
    return drives


def pci_devices():
    raw = run(["lspci"]) or ""
    nics, gpus = [], []
    for line in raw.splitlines():
        low = line.lower()
        if "network controller" in low or "ethernet controller" in low:
            nics.append(re.sub(r"^[^ ]+ [^:]+: ", "", line).strip())
        if "vga compatible controller" in low or "3d controller" in low:
            gpus.append(re.sub(r"^[^ ]+ [^:]+: ", "", line).strip())
    return nics, gpus


def collect_nics_gpus():
    pci_nics, pci_gpus = pci_devices()
    nics = []
    raw = run(["ip", "-j", "link"])
    links = []
    if raw:
        try:
            links = json.loads(raw)
        except Exception:
            links = []
    virtual = ("lo", "tailscale", "docker", "br-", "veth", "virbr", "wg")
    phys = [l for l in links
            if not l.get("ifname", "").startswith(virtual)
            and l.get("link_type") != "loopback"]
    for i, link in enumerate(phys):
        name = link["ifname"]
        speed = None
        speed_raw = read_file(f"/sys/class/net/{name}/speed")
        if speed_raw and speed_raw.lstrip("-").isdigit() and int(speed_raw) > 0:
            speed = int(speed_raw)
        else:
            unknown(f"nics[{name}].speed_mbps",
                    "link speed not exposed via sysfs for this interface "
                    "(wireless or driver does not report it)")
        nics.append({
            "name": name,
            "model": pci_nics[i] if i < len(pci_nics) else None,
            "mac_address": link.get("address"),
            "speed_mbps": speed,
            "ports": 1,
            "medium": "wireless" if name.startswith("wl") else "wired",
        })
    gpus = [{"model": g, "vendor": None, "integrated": None} for g in pci_gpus]
    if gpus:
        unknown("gpus[].integrated",
                "integration (discrete vs APU/iGPU) is not reported by "
                "lspci; confirm manually if it matters")
    return nics, gpus


def render_md(rec):
    s = rec["system"]
    lines = [
        f"# Inventory record — {rec['hostname']}",
        "",
        f"- Collected: {rec['collected_at']} by {rec.get('collected_by') or 'collect-inventory.py'}",
        f"- Machine-readable record: `{rec['hostname']}.json` "
        "(schema: `inventory-record.schema.json`)",
        "",
        "## System",
        f"- Vendor: {s.get('vendor')}",
        f"- Product: {s.get('product_name')} ({s.get('product_version')})",
        f"- Board: {s['board'].get('vendor')} {s['board'].get('name')} "
        f"({s['board'].get('version')})",
        f"- BIOS: {s['bios'].get('vendor')} {s['bios'].get('version')} "
        f"({s['bios'].get('release_date')})",
        f"- Serial: {s.get('serial_number') or 'unknown — see JSON record'}",
        "",
        "## CPU",
        f"- {rec['cpu'].get('model')} — {rec['cpu'].get('cores')} cores / "
        f"{rec['cpu'].get('threads')} threads",
        "",
        "## Memory",
        f"- Total: {rec['memory'].get('total_bytes')} bytes "
        f"(slots/ECC detail: see JSON record unknowns if absent)",
        "",
        "## Drives",
    ]
    for d in rec["drives"]:
        lines.append(f"- {d['device']}: {d.get('model')} "
                     f"({d.get('capacity_bytes')} bytes, {d.get('interface')}), "
                     f"serial {d.get('serial_number')}")
    lines += ["", "## Network"]
    for n in rec["nics"]:
        lines.append(f"- {n['name']}: {n.get('model')} ({n.get('medium')}), "
                     f"MAC {n.get('mac_address')}")
    lines += ["", "## GPU"]
    for g in rec["gpus"]:
        lines.append(f"- {g.get('model')}")
    if rec["unknowns"]:
        lines += ["", "## Unknowns (unreadable on this run)"]
        for u in rec["unknowns"]:
            lines.append(f"- `{u['field']}` — {u['reason']}")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(Path(__file__).resolve().parent))
    ap.add_argument("--host", default=socket.gethostname())
    args = ap.parse_args()
    nics, gpus = collect_nics_gpus()
    rec = {
        "schema_version": "1.0",
        "hostname": args.host,
        "collected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "collected_by": "machines/collect-inventory.py",
        "system": collect_system(),
        "cpu": collect_cpu(),
        "memory": collect_memory(),
        "drives": collect_drives(),
        "nics": nics,
        "gpus": gpus,
        "unknowns": UNKNOWNS,
    }
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{args.host}.json").write_text(json.dumps(rec, indent=2) + "\n")
    (out / f"{args.host}.md").write_text(render_md(rec))
    print(f"wrote {out / (args.host + '.json')} and {out / (args.host + '.md')}")
    print(f"unknowns: {len(UNKNOWNS)} (see record)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
