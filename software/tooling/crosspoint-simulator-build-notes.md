# Building and running the CrossPoint simulator on NixOS

> **Result: `[SUCCESS]`.** CrossPoint Reader firmware compiled natively and ran
> on an x86-64 NixOS host with no e-reader hardware, 2026-09-04.
>
> Evidence status **`executed-success`** — every command below was run and the
> stated outcome observed. This is the first hardware-free execution of this
> firmware recorded in this knowledge base, and it converts a set of previously
> `inferred` claims into observed fact.

Related: [`crosspoint-simulator` in the tooling record](README.md) ·
[CrossPoint Reader](../applications/crosspoint-reader/README.md) ·
[FreeInk SDK](../frameworks/freeink-sdk/README.md)

## What was built

| Item | Value |
|---|---|
| Firmware | `crosspoint-reader/crosspoint-reader` @ **`e6139861a2a8c634aa18c333b7e214ee51a9965c`** |
| Submodule | `Free-Ink/freeink-sdk` @ **`68425f8eec1246a0be0c0f311540f60ad733fa76`** |
| Simulator | `crosspoint-reader/crosspoint-simulator` @ **`c55f168bc0e677fdb32312c8be4b5874469465e6`** |
| Host | NixOS, x86-64, **GCC 15.3.0**, PlatformIO Core 6.1.19, SDL2 2.32.70 (sdl2-compat) |
| Output | `.pio/build/simulator/program`, **6,649,712 bytes** |
| Build time | ~51 s cold, ~8 s incremental |
| Run | Executes; with `SDL_VIDEODRIVER=dummy` it runs to the timeout with **no errors** once its virtual SD card exists |

## Seven portability problems, and their fixes

The simulator README warns that platforms other than macOS and Ubuntu-under-WSL
"may need additional libraries or platform-specific stubs". This is what that
meant in practice. **None of these are in the sample config.**

### 1. The simulator must *not* inherit the SDK's hardware libraries

The single most important finding, and the one that costs the most time.

The firmware's `[base]` env declares `lib_deps` pulling in fourteen `freeink-sdk`
libraries. **The simulator provides its own stubs for those** — it ships
`Arduino.h`, `BoardConfig.h`, `EInkDisplay.h`, `BatteryMonitor.h`, `ESP.cpp` and
more. Inheriting `${base.lib_deps}` compiles the *real* hardware libraries, which
then fail on `pinMode`, `digitalWrite`, `HIGH`, `LOW`, `SPISettings` — Arduino
symbols that do not exist natively.

**But two of the fourteen are not hardware and must be kept:** `FreeInkUI`
(provides `FreeInkApp.h`) and `Icons`. Ignoring those fails with
`fatal error: FreeInkApp.h: No such file or directory`.

So the correct split is: **ignore the hardware libs, keep the UI/asset libs.**

### 2. GCC 15 defaults to C23, which breaks the QRCode library

`qrcode.h` contains the AVR-era idiom:

```c
#ifndef __cplusplus
typedef unsigned char bool;
static const bool false = 0;
static const bool true  = 1;
#endif
```

In **C23**, `bool`, `true` and `false` are keywords, so this is now a syntax
error: `'bool' cannot be defined via 'typedef'`. GCC 15 defaults to `gnu23`.

This will affect **anyone building this on a current toolchain**, not just NixOS.
Passing `-std=gnu17` does not help — PlatformIO deduplicates `-std=` flags and
the C++ standard wins. The fix used here was a local patch to the vendored
header, guarding on `__STDC_VERSION__ < 202311L`.

### 3. `char` signedness differs from the target

The firmware embeds generated data tables (e.g.
`src/network/html/js/jszip_minJs.generated.h`) containing bytes above 127. On
ESP32 (Xtensa and RISC-V) `char` is **unsigned**; on x86-64 Linux it is
**signed**, so those initialisers become narrowing conversions and the build
fails with dozens of `-Wnarrowing` errors.

**Fix:** `-funsigned-char`, which matches the target's convention rather than
suppressing the diagnostic.

### 4. PNGdec and JPEGDEC need `memcpy_P`

Both call the AVR/ESP `pgmspace` API, which does not exist on a native host.
Supplying it as a **`-D` macro breaks compilation** — `memcpy_P` also appears in
function signatures, so the macro corrupts them. A forced-include header with a
real inline function works:

```c
/* sim-compat.h */
#pragma once
#include <string.h>
#include <stdint.h>
#ifndef PROGMEM
#define PROGMEM
#endif
static inline void *memcpy_P(void *d, const void *s, size_t n) { return memcpy(d, s, n); }
#ifndef pgm_read_byte
static inline uint8_t pgm_read_byte(const void *p) { return *(const uint8_t *)p; }
#endif
```

added with `-include sim-compat.h`.

### 5. The documented "native decoders" mode did not work

The sample config offers `-DCROSSPOINT_SIM_USE_NATIVE_DECODERS`. The simulator's
`PNGdec.h` / `JPEGDEC.h` shims implement it with **`#include_next`**, which
requires the simulator's include directory to precede the real library's on the
command line. PlatformIO's dependency-graph ordering puts
`.pio/libdeps/simulator/JPEGDEC/src` **first**, so `__has_include_next` finds
nothing and the shim raises
`#error "CROSSPOINT_SIM_USE_NATIVE_DECODERS requires JPEGDEC in this PlatformIO environment"`.

**Not used.** The ordinary Arduino PNGdec/JPEGDEC path plus the compat header
above works instead. This looks like a genuine latent bug in the simulator for
any environment where PlatformIO orders includes this way, rather than anything
NixOS-specific — `inferred`, not reported upstream.

### 6. Three defines the sample config omits

Inherited from `[base]` on real builds and silently required:

- `-DCROSSPOINT_VERSION=\"…\"` — otherwise `BootActivity.cpp` fails
- `-DXML_CONTEXT_BYTES=1024` — expat refuses to build without it
- `-DPNG_MAX_BUFFERED_PIXELS=16416` — `PngToFramebufferConverter.cpp` fails

### 7. `-lcrypto` for MD5

`KOReaderDocumentId.cpp` uses OpenSSL's `MD5_Init` / `MD5_Update` / `MD5_Final`.
The README mentions needing OpenSSL headers but the sample config does not link
the library, so the build compiles fully and then fails at **link** time.

## The working configuration

Appended to the firmware's `platformio.ini`. **Local build experiment, not
upstream** — do not send this as a patch without cleaning it up.

```ini
[env:simulator]
platform = native
lib_ldf_mode = deep+
lib_compat_mode = off
lib_deps =
  symlink://../crosspoint-simulator
  bblanchon/ArduinoJson @ 7.4.2
  ricmoo/QRCode @ 0.0.1
  bitbank2/PNGdec @ 1.1.6
  https://github.com/bitbank2/JPEGDEC.git#86282979224c8a32fd51e091ed5a35b0c699a52b
  FreeInkUI=symlink://freeink-sdk/libs/ui/FreeInkUI
  Icons=symlink://freeink-sdk/libs/assets/Icons
lib_ignore =
  hal
  WebSockets
  BoardConfig
  EInkDisplay
  BatteryMonitor
  InputManager
  SDCardManager
  UsbMassStorage
  XteinkDetect
  PowerManager
  FrontlightManager
  Rtc
  Imu
  SecureNet
build_src_filter =
  +<*>
  -<network/FirmwareFlasher.cpp>
  -<network/OtaBootSwitch.cpp>
  -<network/OtaUpdater.cpp>
  -<platform/skip_efuse_blk_check.c>
build_flags =
  -std=gnu++2a
  -funsigned-char
  -I src
  -include sim-compat.h
  -DCROSSPOINT_VERSION=\"sim-local\"
  -DEINK_DISPLAY_SINGLE_BUFFER_MODE=1
  -DDISABLE_FS_H_WARNING=1
  -DXML_GE=0
  -DXML_CONTEXT_BYTES=1024
  -DPNG_MAX_BUFFERED_PIXELS=16416
  -DUSE_UTF8_LONG_NAMES=1
  !sdl2-config --cflags --libs
  -lcrypto
```

Plus the local `qrcode.h` C23 patch (§2) and `sim-compat.h` (§4).

## Commands

```bash
git clone --depth 1 --recurse-submodules --shallow-submodules \
  https://github.com/crosspoint-reader/crosspoint-reader
git clone --depth 1 https://github.com/crosspoint-reader/crosspoint-simulator
cd crosspoint-reader

nix-shell -p SDL2 SDL2.dev pkg-config openssl openssl.dev curl gcc gnumake python3 \
  --run 'export PLATFORMIO_CORE_DIR="$PWD/.cache/platformio"; pio run -e simulator'
# => [SUCCESS] Took 51.03 seconds

mkdir -p fs_/fonts fs_/books           # the simulator's virtual SD card
SDL_VIDEODRIVER=dummy ./.pio/build/simulator/program
```

All `executed-success`. The clone is ~533 MB with the submodule.

## What running it establishes

Modest but real, and previously unavailable:

- **The firmware builds and executes without an e-reader.** Every prior claim in
  this knowledge base about CrossPoint's runtime behaviour was `inferred` from
  source; this is the first observation.
- **It mounts a virtual SD card at `./fs_/`.** Before that directory exists it
  reports `[SIM] open failed: ./fs_/.fonts` and `./fs_/fonts`; afterwards it runs
  silently. So the SD layout is inspectable and modifiable on a desktop, which is
  the practical route to understanding the on-card format.
- **It runs headless** under `SDL_VIDEODRIVER=dummy` — so it is usable in CI or
  a container, not only on a desktop with a display.

## Limits — what this does *not* establish

- **No frame was captured.** Under the dummy video driver nothing renders to a
  file, and no screenshot mechanism was found. Display output is unverified.
- **Nothing about the PaperMono.** This build targets the simulator's own board
  stubs. Whether the simulator can model the
  [PaperMono](../../devices/m5stack/papermono/README.md)'s M5IOE1 expander and
  M5PM1 power manager is **still unknown** — the original open question stands.
- **No book was loaded**, no UI interaction driven, no reading path exercised.
- The build required a **local patch to a vendored library** and a compat header;
  it is not a clean upstream configuration.

## Suggested upstream contributions

Three of these are general, not NixOS-specific, and would help anyone on a
current toolchain:

1. The **C23/`bool`** breakage in QRCode (§2) — affects every GCC ≥ 14 host.
2. The **`#include_next` ordering** assumption in the native-decoder shims (§5).
3. The sample config's **missing defines and `-lcrypto`** (§6, §7).

None has been reported upstream from here.
