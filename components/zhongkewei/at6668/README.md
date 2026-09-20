# ZhongKeWei AT6668

- **Category:** **multi-mode GNSS baseband/RF chipset** — the silicon inside the
  [ATGM336H-6N](../atgm336h-6n/README.md) module
- **Research status:** **no chip datasheet located.** What *is* held is the **CASIC
  Multi-mode Satellite Navigation Receiver Protocol Specification**, which is the document
  that actually matters for firmware, because everything beyond "read NMEA" goes through it.
- **Retrieved:** 2026-09-04

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **ZhongKeWei / 中科微电子** (Zhongke Microelectronics) | `inferred` from the module lineage |
| Part | **`AT6668`** | M5Stack writes the module/chip pairing as **`ATGM336H-6N@AT6668`** on three separate product pages |
| Role | Multi-constellation GNSS receiver SoC | vendor |
| Constellations | GPS, QZSS, BDS (B1I + B1C), GALILEO E1, GLONASS R1, SBAS | vendor |
| Channels | 50 | vendor |
| Host protocol | **NMEA 0183 4.1** output; **CASIC binary** for configuration and status | vendor + the protocol specification |

The chip is not sold as a bare part in the channels this pass searched; it is encountered
only inside modules. That is why the module record carries the electrical detail and this
record carries the protocol.

## 2. Why the CASIC protocol matters

Reading a position is easy — the receiver emits standard NMEA sentences and any parser will
do. **Everything else requires CASIC binary messages:**

| Task | Mechanism |
|---|---|
| Select which constellations are used | CASIC config message |
| Cold / warm / hot / factory start | CASIC command |
| Change update rate | CASIC config |
| Change UART baud rate | CASIC config |
| Query firmware version | CASIC query |
| Power/standby modes | CASIC command |

M5Stack's `MultipleSatellite` class (in their `TinyGPSPlus` fork) exposes exactly this
surface — `setSystemBootMode(BOOT_FACTORY_START)`, `setSatelliteMode(SATELLITE_MODE_GLONASS)`,
`getGNSSVersion()` — and those calls are CASIC frames underneath, not NMEA.

**Practical consequence for a port:** if you drop a generic NMEA library onto an
ATGM336H/AT6668 and then find you cannot change the constellation set or the update rate,
this is why. The protocol specification is the reference; it is archived below.

## 3. Used By

### [ATGM336H-6N module](../atgm336h-6n/README.md)

The only route by which this chipset appears in this repository. Through that module it
reaches:

- [M5Stack Cap LoRa-1262 (U214)](../../../devices/m5stack/cap-lora-1262/README.md) — designator `M2`, UART only
- [M5Stack Cap LoRa868 (U201)](../../../devices/m5stack/cap-lora868/README.md) — same
- [M5Stack Cardputer Mesh Kit (K152)](../../../devices/m5stack/cardputer-mesh-kit/README.md) — via the bundled Cap

On all three the chipset speaks **UART at 115200 8N1** and nothing else is exposed.

## 4. Caveats

| # | Issue |
|---|---|
| 1 | **No AT6668 chip datasheet located.** Constellation, channel and sensitivity figures here are *module-level* claims from M5Stack |
| 2 | The CASIC specification is a **multi-vendor** document covering a family of receivers — not every message it defines is necessarily implemented by the AT6668 |
| 3 | The archived specification's **language and revision were not checked** (see the placeholder). CASIC documentation commonly circulates in Chinese with partial English translations |
| 4 | Whether the AT6668 differs materially from the AT6558 / AT6558R used in older ATGM336H variants was **not investigated** |

## 5. Local artifacts

| File | Status |
|---|---|
| [`artifacts/CASIC_Multi-mode_Satellite_Navigation_Receiver_Protocol_Specification.ARCHIVED.md`](artifacts/CASIC_Multi-mode_Satellite_Navigation_Receiver_Protocol_Specification.ARCHIVED.md) | **Archived** 2026-09-04 — 2 899 191 B. The placeholder carries the hash and two reacquisition URLs |

Cited from the device records that caused the fetch:
[Cap LoRa-1262 `sources.md` S-20](../../../devices/m5stack/cap-lora-1262/sources.md) and
[Cardputer Mesh Kit §7](../../../devices/m5stack/cardputer-mesh-kit/README.md).

## 6. Sources

| ID | Title | Publisher | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|
| Z-1 | CASIC Multi-mode Satellite Navigation Receiver Protocol Specification | CASIC, mirrored by M5Stack | authorized mirror | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1173/CASIC_Multi-mode_Satellite_Navigation_Receiver_Protocol_Specification.pdf` | 2026-09-04 | The binary configuration protocol — **archived** |
| Z-2 | Cap LoRa-1262 documentation | M5Stack | primary | `https://docs.m5stack.com/en/cap/Cap_LoRa-1262` | 2026-09-04 | `ATGM336H-6N@AT6668` pairing; constellation and band list |
| Z-3 | `m5stack/TinyGPSPlus` (`MultipleSatellite`) | M5Stack | primary | `https://github.com/m5stack/TinyGPSPlus` @ `254a10041ac38d17d98dab24c0ae4d2a8d19a677` | 2026-09-04 | The CASIC-backed API surface named in §2 |
