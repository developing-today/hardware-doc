# ARCHIVED: `CASIC_Multi-mode_Satellite_Navigation_Receiver_Protocol_Specification.pdf`

> This file was **moved out of the repository**, not deleted. Archived **2026-09-04**.

**What it was:** the **CASIC binary protocol specification** for multi-mode satellite
navigation receivers — the document that defines the configuration and query messages used
by ZhongKeWei GNSS chipsets including the **AT6668** inside the
[ATGM336H-6N](../../atgm336h-6n/README.md).

**What it is for:** everything beyond reading NMEA. Constellation selection, boot mode
(cold/warm/hot/factory), update rate, baud rate and firmware-version query are all CASIC
messages, not NMEA sentences. M5Stack's `MultipleSatellite` API
(`setSatelliteMode()`, `setSystemBootMode()`, `getGNSSVersion()`) is a thin wrapper over
this protocol.

**Why it was moved:** 2.9 MB, and it is a **protocol manual rather than a part datasheet** —
the least central of the four PDFs this research pass retained. It is re-fetchable from a
stable vendor CDN.

## Identity

| Field | Value |
|---|---|
| Original repository path | `components/zhongkewei/at6668/artifacts/CASIC_Multi-mode_Satellite_Navigation_Receiver_Protocol_Specification.pdf` |
| Archived to | `archive/components/zhongkewei/at6668/artifacts/CASIC_Multi-mode_Satellite_Navigation_Receiver_Protocol_Specification.pdf` |
| Type | file, PDF (`%PDF-1.7`, magic verified) |
| Size | **2 899 191 B (2.76 MiB)** |
| SHA-256 | `61e2567dcf04b0d8e4d5ec6c9c841f8ac0caa846f5b54645a64b7704d800fe04` |
| Retrieved | **2026-09-04**, HTTP 200 |
| Document version / date | **unknown** — no version string in the filename, and the file's contents were **not read** by the pass that fetched it |
| Language | **unknown** (CASIC material commonly circulates in Chinese; an English rendering of the title is used by M5Stack) |
| Publisher | CASIC (China Aerospace Science and Industry Corporation), mirrored by M5Stack |
| Licence | **unknown.** No licence statement accompanies M5Stack's document mirrors |
| Redistribution status | **unknown** |
| Disposition | **archived** (local-cache equivalent); not tracked in this repository |

## How to get it back

Verified **2026-09-04**.

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

# Source 1 — M5Stack documentation CDN (the copy that was archived)
curl -sSL -A "$UA" -o CASIC_Multi-mode_Satellite_Navigation_Receiver_Protocol_Specification.pdf \
  https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1173/CASIC_Multi-mode_Satellite_Navigation_Receiver_Protocol_Specification.pdf

# Source 2 — the same file is linked from two M5Stack product pages, in case the
# direct CDN path changes. Re-scrape the "Datasheets" section of either:
#   https://docs.m5stack.com/en/cap/Cap_LoRa-1262
#   https://docs.m5stack.com/en/core/Cardputer_Mesh_Kit

# Verify
sha256sum CASIC_Multi-mode_Satellite_Navigation_Receiver_Protocol_Specification.pdf
#   61e2567dcf04b0d8e4d5ec6c9c841f8ac0caa846f5b54645a64b7704d800fe04
stat -c%s CASIC_Multi-mode_Satellite_Navigation_Receiver_Protocol_Specification.pdf
#   2899191
head -c 8 CASIC_Multi-mode_Satellite_Navigation_Receiver_Protocol_Specification.pdf
#   %PDF-1.7
```

Reacquisition status: **automatic** (both routes are unauthenticated HTTP GET).

**Not submitted to the Wayback Machine.** It is a vendor-CDN mirror of a widely-circulated
Chinese-industry protocol document, not a scarce one-off — the criteria in `AGENTS.md` for
`web.archive.org/save/` are not met. If a future pass finds the CDN path dead and no
alternative, that judgement should be revisited.

## Restore from the local archive

```bash
mv archive/components/zhongkewei/at6668/artifacts/CASIC_Multi-mode_Satellite_Navigation_Receiver_Protocol_Specification.pdf \
   components/zhongkewei/at6668/artifacts/
```

## Cited by

- [`components/zhongkewei/at6668/README.md`](../README.md) §5
- [`components/zhongkewei/atgm336h-6n/README.md`](../../atgm336h-6n/README.md) §6
- [`devices/m5stack/cap-lora-1262/sources.md`](../../../../devices/m5stack/cap-lora-1262/sources.md) — S-20
- [`devices/m5stack/cap-lora-1262/features/gnss.md`](../../../../devices/m5stack/cap-lora-1262/features/gnss.md) §3
- [`devices/m5stack/cardputer-mesh-kit/README.md`](../../../../devices/m5stack/cardputer-mesh-kit/README.md) §7
