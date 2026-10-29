# machines/ — hardware inventory records

One record per inventoried machine: `<hostname>.json` (canonical,
machine-readable) plus a generated `<hostname>.md` summary for humans.

Why a new top-level tree: the existing layout has no home for whole-machine
records — `devices/` and `components/` are per-device/per-component
research dossiers, and the root `VERIFICATION-*.md` files verify individual
devices. A cluster machine is none of those; it is an inventory subject
(schema + template + one record per machine), so it gets its own tree.
Filed under developing-today/code#1094 (basement-cluster program).

## Files

- `inventory-record.schema.json` — JSON Schema (2020-12) for a record.
- `inventory-record-template.md` — the field checklist and JSON skeleton.
- `collect-inventory.py` — the collector. Stdlib-only Python; run it **on
  the machine being inventoried**. It reads DMI sysfs, `lscpu`, `/proc/meminfo`,
  `lsblk`, `ip link`, `lspci`, and (via `sudo -n`, never prompting) `dmidecode`
  and `smartctl`, then writes `<hostname>.json` + `<hostname>.md`. Anything it
  cannot read becomes `null` plus an entry in the record's `unknowns` array
  with the reason — values are never invented.
- `<hostname>.json` / `<hostname>.md` — one pair per machine.

## Validate a record

```bash
npx --yes ajv-cli validate --spec=draft2020 -s machines/inventory-record.schema.json -d machines/<hostname>.json
```

## Collect a new machine

```bash
# on the machine itself, from a hardware-doc checkout:
python3 machines/collect-inventory.py
# then re-run it under sudo if you want the privileged fields
# (dmidecode memory detail, SMART, DMI serial) filled in the same pass:
sudo python3 machines/collect-inventory.py
git -C <checkout> add machines/<hostname>.json machines/<hostname>.md
```

Collecting the basement core machines themselves is tracked separately
(developing-today/code#1096/#1099 — physical/KVM access); this tree is the
record shape they will land in.
