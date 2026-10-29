# Inventory record template — one machine

Copy this shape into `machines/<hostname>.json`, or better: run
`machines/collect-inventory.py` on the machine and edit only what it could
not read. The JSON record is the canonical form and must validate against
`machines/inventory-record.schema.json`:

```bash
npx --yes ajv-cli validate --spec=draft2020 -s machines/inventory-record.schema.json -d machines/<hostname>.json
```

**The one hard rule: never invent a value.** A field you cannot read is
`null` (or an empty list), and the record's `unknowns` array names the
field path and why it could not be read (needs root, no such hardware,
tool missing, …). An honest `unknown` is data; a guessed serial is a lie
that will be trusted later.

## Fields (issue #1094 checklist)

| Section | Fields | Read from |
|---|---|---|
| `system` | vendor, product name/version, machine serial | `/sys/class/dmi/id/*` |
| `system.board` | motherboard vendor / name / version | `/sys/class/dmi/id/board_*` |
| `system.bios` | BIOS vendor / version / release date | `/sys/class/dmi/id/bios_*` |
| `system.bmc` | BMC/KVM address, BMC firmware version | out-of-band config; `null` + unknown entry on machines without a BMC |
| `cpu` | model, vendor, architecture, sockets, cores, threads | `lscpu -J` |
| `memory` | total bytes; slots total/used; ECC yes/no; per-module locator, size, type, speed, manufacturer, part number, serial | `/proc/meminfo` for the total; `dmidecode -t memory` (root) for slots/modules/ECC |
| `drives[]` | device, model, serial, capacity bytes, interface (NVMe/SATA/…), firmware version, SMART summary (health, % used, power-on hours) | `lsblk -J -b -d`; `smartctl -i -H -A` (root) for firmware/SMART |
| `nics[]` | interface name, model, MAC, speed Mb/s, port count, medium (wired/wireless) | `ip -j link`, `lspci`, `/sys/class/net/<if>/speed` |
| `gpus[]` | model, vendor, integrated? | `lspci` (integration is not reported by lspci — confirm manually) |
| `unknowns[]` | `{field, reason}` for every null/empty value above | you, honestly |

## Skeleton

```json
{
  "schema_version": "1.0",
  "hostname": "<hostname>",
  "collected_at": "<UTC ISO-8601>",
  "collected_by": "machines/collect-inventory.py",
  "system": {
    "vendor": null, "product_name": null, "product_version": null,
    "serial_number": null,
    "board": {"vendor": null, "name": null, "version": null},
    "bios": {"vendor": null, "version": null, "release_date": null},
    "bmc": {"kvm_address": null, "firmware_version": null}
  },
  "cpu": {"model": null, "vendor": null, "architecture": null,
          "sockets": null, "cores": null, "threads": null},
  "memory": {"total_bytes": null, "slots_total": null, "slots_used": null,
             "ecc": null, "modules": []},
  "drives": [{"device": "/dev/<name>", "model": null, "serial_number": null,
              "capacity_bytes": null, "interface": null,
              "firmware_version": null,
              "smart": {"health": null, "percentage_used": null,
                        "power_on_hours": null}}],
  "nics": [{"name": "<ifname>", "model": null, "mac_address": null,
            "speed_mbps": null, "ports": null, "medium": null}],
  "gpus": [{"model": null, "vendor": null, "integrated": null}],
  "unknowns": [{"field": "<dotted.path>", "reason": "<why unreadable>"}]
}
```

A worked, real example lives beside this file: `amd.json` / `amd.md`
(the laptop the collector was first run on, 2026-10-29).
