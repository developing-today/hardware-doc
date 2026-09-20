# NixOS as an embedded development host

Cross-cutting notes on running embedded toolchains — ESP-IDF, Arduino, PlatformIO, mesh/LoRa/SDR tooling and proprietary UI editors — on NixOS, where the usual "download the installer and run it" instructions do not apply.

**Compiled:** 2026-08-30 · **Host repository:** this flake (`nixos/environment/default.nix`, `nixos/hardware/default.nix`) · **Locked nixpkgs:** `developing-today-forks/nixpkgs` rev `9b9332edb9cf9682eea4484a611e2ab3ffe3d38b`.

> **Read this first.** Every package name below was checked for **existence** by Nix evaluation. **Nothing in this guide has been built, and no configuration here has been rebuilt or activated.** Treat build success, runtime behaviour and hardware access as *unverified*. See the [evidence boundary](#8-evidence-boundary).

This guide exists as its own `guides/` domain because it is host-platform knowledge: it belongs to no chip, board or manufacturer, yet it gates all firmware work done from this machine.

---

## 1. ESP-IDF: three routes, and why the obvious one fails

| Route | Verdict |
|---|---|
| Espressif's `install.sh` / `export.sh` | Works only inside an FHS environment; mutable, unpinned, fights the store. Fallback only. |
| **`nixpkgs-esp-dev` flake** | **The NixOS-native answer.** Pinned, reproducible, ships the Xtensa/RISC-V toolchains, OpenOCD and the full Python environment. |
| PlatformIO | Fine for Arduino-framework and multi-board projects; lags ESP-IDF releases and hides native configuration. |

### The trap: the package alone does nothing

`nixpkgs-esp-dev` exposes `packages.<system>.esp-idf-full` **and** `devShells.<system>.esp-idf-full`. Putting the *package* in `environment.systemPackages` type-checks and installs files — and still leaves you with **no `idf.py`, no `IDF_PATH`, no toolchain on `PATH`**.

The reason: the package's usability comes from a **stdenv setup hook** (`setup-hook.sh`), which only runs for downstream derivations and `nix develop` shells. NixOS builds `/run/current-system/sw` by symlinking store paths; it never executes setup hooks in a login shell. The upstream binary is at `$out/tools/idf.py`, not `$out/bin/idf.py`, so nothing lands on `PATH` either.

### What this repository does instead

`nixos/environment/default.nix` reimplements the setup hook as an ordinary wrapper so ESP-IDF is genuinely system-wide, per the requirement that these tools not live in a dev shell. Each wrapper exports the complete, version-scoped environment and then execs the real entry point:

```text
IDF_PATH, IDF_TOOLS_PATH, IDF_PYTHON_CHECK_CONSTRAINTS, IDF_PYTHON_ENV_PATH,
GIT_CONFIG_SYSTEM, plus every tool's exportVars, then PATH
```

`GIT_CONFIG_SYSTEM` matters: the package ships `etc/gitconfig` marking its own store path a `safe.directory`, because ESP-IDF's CMake runs `git describe` against a tree owned by the build user.

### Running 5.5 and 6.x side by side

Two ESP-IDF versions **cannot** share one global environment — `IDF_PATH`, `IDF_TOOLS_PATH`, `IDF_PYTHON_ENV_PATH`, `OPENOCD_SCRIPTS` and `ESP_ROM_ELF_DIR` each hold exactly one value, and `idf.py`, `esptool`, `openocd` and the toolchain binaries all collide by name. Whichever initialised last would silently win.

The resolution is namespaced entry points, each carrying its own complete environment:

| Command | Version | Notes |
|---|---|---|
| `idf.py`, `idf5.py` | **5.5.2** | Default. From maintained upstream `mirrexagon/nixpkgs-esp-dev` |
| `esp-idf-5` | 5.5.2 | Interactive shell with the 5.5 environment |
| `idf6.py` | **6.0.1** | Deliberately *not* the default — see below |
| `esp-idf-6` | 6.0.1 | Interactive shell with the 6.0 environment |

`idf-component-manager` is inside each version's bundled Python environment, so ESP-IDF component fetching works with no extra packages.

### Status of the 6.x packaging, stated honestly

ESP-IDF 6.x is **not** in upstream `nixpkgs-esp-dev`. This repository pins the open PR #125 fork (`dvdvgt/nixpkgs-esp-dev`, ESP-IDF v6.0.1).

| Evidence | Finding |
|---|---|
| Upstream merge status | **Open, unmerged, no approving review** |
| CI | **None** — zero checks, zero commit statuses; no workflows exist at that revision |
| Author's own assessment | "I have not tested it too thoroughly… More testing is thus advisable." |
| Independent user report | One: "This works for me", from a user who pins this exact commit for an ESP32-C6 project |
| Known broken | The upstream `blink` example — `led_strip.h` is now a separate component |
| Naive version override | **Unsafe.** The Python dependency set is hand-maintained per IDF release; bumping `rev`/`sha256` yields 6.x sources with a 5.5-era Python environment |

Current upstream stable is 6.0.2, so even the fork is one patch release behind.

## 2. Package availability in the locked nixpkgs

Checked 2026-08-30 by attribute-existence evaluation ([method](#7-checking-whether-a-package-exists-without-building)). Existence ≠ builds ≠ works.

**Present:** `esptool` · `esptool-ck` · `espflash` · `espup` · `esp-generate` · `platformio` · `gcc-arm-embedded` · `pkgsCross.{arm-embedded,riscv32-embedded,riscv64-embedded,avr}` · `avrdude` · `simavr` · `openocd` · `probe-rs-tools` · `pyocd` · `stlink` · `dfu-util` · `flashrom` · `picotool` · `pico-sdk` · `micropython` · `mpremote` · `thonny` · `rshell` · `adafruit-ampy` · `circup` · `meshtastic` · `meshtasticd` · `meshcore-cli` · `rns` · `nomadnet` · `sideband` · `chirpstack-*` · `qFlipper` · `esphome` · `zigbee2mqtt` · `bluez` · `nrfutil` · `nanopb` · `flatbuffers` · `cbor-diag` · `home-assistant` · `home-assistant-cli` · `node-red` · `nanomq` · `flashmq` · `rabbitmq-server` · `mosquitto` · `sigrok-cli` · `pulseview` · `gnuradio` · `rtl-sdr` · `hackrf` · `urh` · `yosys` · `kicad` · `librepcb` · `horizon-eda` · `geda` · `gerbv` · `gpsd` · `rtklib-ex`

**Absent — do not plan around these:**

| Attribute | Consequence |
|---|---|
| `matter-sdk`, `chip-tool` | Matter development needs its own upstream build system |
| `openthread`, `otbr` | No packaged Thread border-router tooling |
| `west`, `zephyr` | Zephyr must come from its own `west` workspace, typically in a dev shell |
| `lvgl` | See [§3](#3-lvgl-and-sensor-libraries-are-project-dependencies) — this is expected, not a gap |
| `emqx`, `vernemq` | Use `mosquitto`, `nanomq` or `flashmq` |

Renames observed in this nixpkgs revision, both of which break older configurations: **`cargo-espflash` → `espflash`**, and top-level **`avrlibc` → `pkgsCross.avr.libc`** (the top-level attribute now refuses to evaluate on `x86_64-linux`).

## 3. LVGL and sensor libraries are project dependencies

A recurring wrong question is "which nixpkgs package provides LVGL / the BME280 driver?" There is none, and there should not be:

- **LVGL** arrives through `idf-component-manager` (ESP-IDF), the PlatformIO library manager, or vendored CMake/`FetchContent` — per project, pinned per project.
- **Sensor libraries** (Bosch, Adafruit, SparkFun, SHT…) work the same way.
- **SquareLine Studio bundles its own LVGL** — four complete trees in v1.6.1: **v8.3.11, v9.1.0, v9.2.2, v9.3**. Exported code targets whichever the project selects, which is a far more common source of version mismatch than anything nixpkgs does.

The system-wide packages that *are* useful here are the format converters: `lv_font_conv`, plus the image/SVG optimisers.

## 4. Device access

Flashing and debugging need more than binaries. This repository sets, system-wide:

- **udev rules** via `services.udev.packages`: `platformio-core.udev`, `meshtasticd`, `openocd`, `probe-rs-tools`, `stlink`, `picotool`, `picoprobe-udev-rules`, `teensy-udev-rules`, `usb-blaster-udev-rules`, `qFlipper`, `hackrf`, `rtl-sdr`.
- **Groups**: `dialout` (serial/programmers), `plugdev` (SDR and vendor debug hardware), `wireshark`.
- `programs.wireshark.usbmon.enable` for USB capture.

`plugdev` does not exist by default on NixOS and is created explicitly; rules referencing it are inert without it.

## 5. SquareLine Studio

Proprietary, and **not** an AppImage on Linux — it is a ZIP. `appimage-run` is therefore irrelevant to it (it remains installed for other tools). Sourcing details, URL patterns and the soft-404 trap: [`vendors/squareline/README.md`](../../vendors/squareline/README.md).

It is packaged declaratively here: `fetchurl` the pinned ZIP → unpack into the store → run under `buildFHSEnv` (a Unity application; it wants the X11 GDK backend, GTK/NSS/ALSA/GL and friends).

**The defect worth recording.** Upstream's `setup.sh` marks **six** files executable, not one:

```text
SquareLine_Studio.x86_64
lvgl/lv_font_conv-linux
lvgl/lvgl_v{8_3_11,9_1_0,9_2_2,9_3}/server/micropython
```

A packaging that chmods only `*.x86_64` and `*.so` — as this repository's first attempt did — produces an editor that **launches fine and then fails later** at font conversion and LVGL live preview. The fix mirrors upstream's exact set. This was caught by reading the archive, not by running the program.

Two further packaging notes, both taken from the shipped `.desktop` template: upstream forces `GDK_BACKEND=x11`, and the template's `__folder__` placeholders assume an extracted-in-place install, so a store-based package must generate its own desktop entry.

## 6. What is not solved here

- **Zephyr, Matter and Thread** have no packaged path; they need project-level `west`/upstream builds, which is exactly the dev-shell pattern this system-wide configuration avoids elsewhere.
- **TouchGFX** is STM32-only and Windows/STM32Cube-centric.
- **Nextion Editor** is Windows-only; WINE is the only route.
- **EAGLE** is no longer meaningfully free — Autodesk folded it into paid Fusion 360; KiCad supersedes it.

## 7. Checking whether a package exists without building

Useful when adding many packages at once, since a single bad attribute fails the whole rebuild:

```sh
nix eval --impure --raw --expr 'let f = builtins.getFlake "github:OWNER/nixpkgs/BRANCH";
  in builtins.toString (f.legacyPackages.x86_64-linux ? PACKAGE_ATTR)'
# -> "1" when present, empty when absent
```

Two cautions learned the hard way:

- `builtins.getFlake` on an **unlocked** reference needs `--impure`, otherwise it errors out.
- A batched `listToAttrs` probe over many names **returned `false` for everything**, including `hello` and `mosquitto`. Re-probing one attribute at a time gave correct results. **Sanity-check any bulk probe against an attribute you know exists**, and distrust an all-negative result.

## 8. Evidence boundary

- **Verified by evaluation (2026-08-30):** every attribute-existence claim in [§2](#2-package-availability-in-the-locked-nixpkgs); the two renames.
- **Verified by reading upstream source:** the ESP-IDF setup-hook mechanism, the `$out/tools/idf.py` layout, the environment variables, `idf-component-manager`'s presence, and the executable set in SquareLine's `setup.sh`.
- **Verified by live probe:** SquareLine host/URL behaviour ([vendor guide](../../vendors/squareline/README.md)).
- **Reported, not reproduced:** the single "works for me" report for ESP-IDF 6.0.1.
- **Not tested at all:** every build, the ESP-IDF wrappers, the SquareLine package, udev rules and group membership. **No `nixos-rebuild`, no `nix build`, no `nix flake check` has been run**, at the user's instruction. The first rebuild is the real test; renamed attributes and the SquareLine FHS wrapper are the most likely failure points.
- **Snapshot-bound:** package availability is true for one nixpkgs revision on `x86_64-linux` and will drift.
