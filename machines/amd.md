# Inventory record — amd

- Collected: 2026-10-29T15:48:31Z by machines/collect-inventory.py
- Machine-readable record: `amd.json` (schema: `inventory-record.schema.json`)

## System
- Vendor: Framework
- Product: Laptop 13 (AMD Ryzen 7040Series) (A7)
- Board: Framework FRANMDCP07 (A7)
- BIOS: INSYDE Corp. 03.18 (01/08/2026)
- Serial: unknown — see JSON record

## CPU
- AMD Ryzen 7 7840U w/ Radeon  780M Graphics — 8 cores / 16 threads

## Memory
- Total: 132752572416 bytes (slots/ECC detail: see JSON record unknowns if absent)

## Drives
- /dev/nvme0n1: Samsung SSD 990 PRO 4TB (4000787030016 bytes, nvme), serial S7KGNU0X603846F

## Network
- wlp1s0: MEDIATEK Corp. MT7922 802.11ax PCI Express Wireless Network Adapter (wireless), MAC 44:fa:66:08:b6:5d

## GPU
- Advanced Micro Devices, Inc. [AMD/ATI] Phoenix1 (rev c4)

## Unknowns (unreadable on this run)
- `nics[wlp1s0].speed_mbps` — link speed not exposed via sysfs for this interface (wireless or driver does not report it)
- `gpus[].integrated` — integration (discrete vs APU/iGPU) is not reported by lspci; confirm manually if it matters
- `system.serial_number` — /sys/class/dmi/id/product_serial is not readable by an unprivileged user on this machine
- `system.bmc` — no BMC present or discoverable from the OS on this machine; record the KVM address manually for managed servers
- `memory.slots_total/memory.slots_used/memory.ecc/memory.modules` — dmidecode requires root on this machine and passwordless sudo is not available; only the total from /proc/meminfo could be read
- `drives[/dev/nvme0n1].firmware_version/smart` — smartctl requires root on this machine and passwordless sudo is not available
