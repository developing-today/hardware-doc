# Portability — where AppFS and the launcher actually run

> Is this P4-specific? Does it need the dual-chip setup? Short answers: **no** and **no**.
> Snapshot **2026-08-24**, launcher @ `20022fce`. Read from build configuration; **nothing was compiled**.

---

## 1. Supported targets

The launcher ships eight build configurations in [`sdkconfigs/`](https://github.com/Nicolai-Electronics/tanmatsu-launcher/tree/main/sdkconfigs), spanning **four different ESP32 chips plus a host build**:

| Config | `CONFIG_IDF_TARGET` | BSP target | Device |
|---|---|---|---|
| `tanmatsu` | **`esp32p4`** | `TANMATSU` | Tanmatsu / Konsool |
| `esp32-p4-function-ev-board` | `esp32p4` | `ESP32_P4_FUNCTION_EV_BOARD` | Espressif P4 devkit |
| `esp32-s31-korvo-1` | **`esp32s31`** | `ESP32_S31_KORVO_1` | Espressif S31 Korvo-1 |
| `hackaday2025` | **`esp32s3`** | `HACKADAY2025` | Hackaday 2025 Communicator badge |
| `mch2022` | **`esp32`** | `MCH2022` | MCH2022 badge |
| `kami` | **`esp32`** | `KAMI` | Nicolai Electronics Kami |
| `linux` | **`linux`** | — | **Host build** |
| `general` | — | — | Shared defaults |

So the launcher runs on **ESP32 (original), ESP32-S3, ESP32-P4 and ESP32-S31** — and there is a **`linux`** target for building the thing on a PC, presumably for UI work and testing without hardware.

### AppFS is likewise not P4-specific

Partition tables exist for six flash layouts:

```
esp32p4-16mb.csv   esp32s3-16mb.csv   esp32s3-8mb.csv
esp32s3-8mb-noappfs.csv   mch2022.csv   hackerhotel2024.csv   esp32s31-16mb.csv
```

The MCH2022 table (plain ESP32) includes an `appfs` partition, so **AppFS works on the original ESP32**. Note also **`esp32s3-8mb-noappfs.csv`** — a build without AppFS at all, for flash-constrained boards.

**Resolved from the component itself.** [`badgeteam/esp32-component-appfs`](https://github.com/badgeteam/esp32-component-appfs) @ `eee29be` (2026-08-25, Apache-2.0) declares **ten targets**:

```yaml
targets: [esp32, esp32s3, esp32c6, esp32p4, esp32c5, esp32c3, esp32c61, esp32h2, esp32s31, esp32c2]
```

That is nearly the entire current ESP32 line-up. The older documentation claim — *"bootloader
modifications for the ESP32, ESP32-C6 and ESP32-P4 included. Other ESP32 variants are not supported
yet"* — is **stale**. AppFS also requires **ESP-IDF ≥ 6.0.2**, consistent with the launcher.

## 2. No dual-chip requirement

**MCH2022 and Kami are single-chip ESP32 devices** with the radio built into the SoC. They run the same launcher and the same AppFS.

The P4 + C6 split on Tanmatsu exists for one reason: **the ESP32-P4 has no radio**. It is a *hardware* consequence of choosing the P4, not an architectural requirement of the software. On an ESP32 or S3 target the Wi-Fi stack is local and `tanmatsu-wifi`/`esp-hosted` is simply not used.

Evidence in the dependency rules — the companion-chip and P4-specific components are conditionally included:

```yaml
nicolaielectronics/rvswd:      { rules: [if: target == esp32p4] }   # CH32V203 flashing
badgeteam/esptool:             { rules: [if: target == esp32p4] }
espressif/esp_tinyusb:         { rules: [if: target == esp32p4 || target == esp32s3] }
badgeteam/badge-elf:           { rules: [if: "target == esp32p4 && ENABLE_LAUNCHERPLUGINS"] }
```

### Two boot-selection backends

AppFS stores the "which app next" record in one of two places, selected by `CONFIG_APPFS_USE_RTC_REG`:

| Mode | Storage | Argument support |
|---|---|---|
| Default | **RTC retained memory** (`rtc_retain_mem_t.custom`), 64-bit magic + fd + valid flag + 128-byte arg | ✅ up to 127 chars |
| `CONFIG_APPFS_USE_RTC_REG=y` | **A single RTC register** (`RTC_CNTL_STORE0_REG` / `LP_AON_STORE0_REG`), `0xA5000000 \| fd` | ❌ warns and discards |

The register mode exists for parts without usable retained memory. **It cannot support
interpreter/script apps**, which pass the script path as the argument
([`apps-vs-plugins.md` §8](apps-vs-plugins.md)). Full mechanism in
[`badgelink-and-appfs.md` §12](badgelink-and-appfs.md).

## 3. What *is* P4-only

| Feature | Restriction | Why |
|---|---|---|
| **Plugins (ELF)** | `depends on IDF_TARGET_ESP32P4`, `default n` | Needs `badge-elf`/kbelf and PSRAM headroom |
| `rvswd` coprocessor flashing | P4 only | Tanmatsu-specific hardware |
| `badgeteam/esptool` | P4 only | Flashing companion chips |
| USB device stack | P4 **or** S3 | Only these have native USB-OTG |

So: **apps are portable across every target; plugins are Tanmatsu/P4 only.**

## 4. Practical consequences

**If you are writing an app**, targeting the launcher's app model does not tie you to the P4. The same `metadata.json` + AppFS binary model works on a plain ESP32 badge. Your *binary* is still per-chip — that is why `metadata.json` has a `targets` array.

**If you are writing a plugin**, you are committed to the ESP32-P4 *and* to the user running a launcher built with `CONFIG_ENABLE_LAUNCHERPLUGINS=y`, which is **not the default**.

**If you want AppFS in your own project**, it is an independent Espressif-registry component (`badgeteam/appfs`) usable on ESP32/C6/P4 without any of the rest of this. You need the component plus the bootloader symlinks — see [`badgelink-and-appfs.md` §7](badgelink-and-appfs.md).

## 5. Reusing the launcher on your own board

The launcher is **MIT** and explicitly presents itself as reusable:

> *"A launcher firmware for **ESP32 based devices** which allows users to configure WiFi, browse apps
> from an online repository and download and run apps on their devices."*
>
> Supported boards: **Tanmatsu · MCH2022 badge · Kami e-paper badge · ESP32-P4 function EV board**

### Building for an existing board

```bash
git clone https://github.com/Nicolai-Electronics/tanmatsu-launcher.git
cd tanmatsu-launcher
make prepare
make build
make flashmonitor
```

Board selection is a single `DEVICE` variable in the `Makefile`, which drives everything else:

```make
SDKCONFIG_DEFAULTS ?= sdkconfigs/general;sdkconfigs/$(DEVICE)
SDKCONFIG          ?= sdkconfig_$(DEVICE)
IDF_TARGET         ?= esp32p4   # per-DEVICE override
IDF_PARAMS := -B $(BUILD) -DDEVICE=$(DEVICE) -DIDF_TARGET=$(IDF_TARGET) -DFAT=$(FAT) ...
```

So `make DEVICE=mch2022 build` picks `sdkconfigs/general` + `sdkconfigs/mch2022`, sets
`IDF_TARGET=esp32` and uses `partition_tables/mch2022.csv`.

Other Makefile targets: `menuconfig`, `defconfig`, `appfs` / `prepappfs`, `erase`, `efuse`,
`openocd` / `gdb` / `gdbgui`, `size` / `size-components` / `size-files`, `icons`,
`compile-protobuf`, `mode_badgelink` / `mode_debug`, `buildall`.

### Porting to a new board

There is **no written porting guide**, but the required pieces are visible:

1. **A BSP target** in [`badgeteam/esp32-component-badge-bsp`](https://github.com/badgeteam/esp32-component-badge-bsp) —
   a `targets/<board>/` directory implementing `badge_bsp_display.c`, `_input.c`, `_i2c.c`,
   `_device.c` and friends, plus a `<board>_hardware.h` of pin definitions and a `Kconfig` entry.
2. **A partition table** at `partition_tables/<board>.csv` including an `appfs` partition
   (type `0x43`, subtype `3`) — or follow the `-noappfs` pattern if flash is tight.
3. **An sdkconfig** at `sdkconfigs/<board>` setting `CONFIG_IDF_TARGET` and `CONFIG_BSP_TARGET_<BOARD>=y`.
4. **A `DEVICE` → `IDF_TARGET` mapping** in the `Makefile`.
5. **AppFS bootloader symlinks** — see [`badgelink-and-appfs.md` §7](badgelink-and-appfs.md).

The existing `mch2022` target is the best worked example of a **non-Tanmatsu, single-chip, plain
ESP32** board: 16 MB flash, PSRAM at 80 MHz, its own partition table, big-endian colour flag. The
`linux` target shows the minimum — a one-line sdkconfig.

> Status: **`inferred`** from the build system and existing targets. No port was attempted; upstream
> publishes no porting documentation.

## 6. Gaps

| Question | Status |
|---|---|
| Does the S3 AppFS path use the bootloader patch? | **RESOLVED** — S3 is one of ten declared targets in the component itself |
| What is **ESP32-S31**? | A target string in current ESP-IDF; **not researched** |
| Does the `linux` target run the full UI? | **Untested** — its sdkconfig is a single line |
| Is there a written porting guide? | **No.** §5 is reconstructed from the build system |
| Is Kami single- or dual-chip? | Target is `esp32`, so radio is on-die; board **not researched** |

## Related

- [`software-architecture.md`](software-architecture.md) — launcher internals
- [`apps-vs-plugins.md`](apps-vs-plugins.md) — build systems
- [`badgelink-and-appfs.md`](badgelink-and-appfs.md) — AppFS integration
