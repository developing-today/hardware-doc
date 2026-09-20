# CrossPoint plugin systems — and whether NFC/LoRa could ever be a plugin

> There is no single "CrossPoint plugin system". There are **two, of completely
> different kinds**, built by different people, and confusing them produces wrong
> answers to the question that matters: *can a plugin reach hardware?*
>
> Snapshot **2026-09-04**. Repository facts `executed-success` (GitHub API);
> design descriptions read from the projects' own documentation, `inferred` for
> behaviour. **Nothing was built or run.**

## The short answer

**No — not as a plugin alone, in either system. But the gap is much smaller than
"fork the firmware".**

| System | Where code runs | Can it reach GPIO / I²C / SPI? |
|---|---|---|
| Upstream CrossPoint (roadmap, unmerged) | **Browser only** — JavaScript + JSON manifests | **No.** No code executes on the MCU at all |
| `mekhontsev` fork — native SD plugins | **On the MCU** — native C++ ELF modules | **No**, but only because the host ABI allow-list omits them — and it is extensible |

The second is the interesting one, and it changes the answer from "impossible" to
"requires a small, well-defined firmware change".

## System 1 — upstream's JavaScript plugins

Per a prior analysis in this project (`reported-working`, **not re-verified
here**):

- The plugin work lives on **two unmerged feature branches**, not `develop`, and
  is a Phase 2 roadmap item.

> **CORRECTION 2026-09-11.** The "unmerged branches" framing above understates
> the state of this work. Measured against `develop`:
>
> | Branch | vs `develop` | Tip | Reading |
> |---|---|---|---|
> | **`feat-sd-plugins`** | **66 ahead, 0 behind** | **2026-09-10** | Contains all of `develop` plus 66 commits — **a clean merge**, actively developed, and it carries **`[env:papermono]`** |
> | `feat-sd-web-plugins` | 64 ahead, 58 behind | — | genuinely divergent |
>
> There is also a **live plugin ecosystem** — `itsthisjustin/sd-plugins` (★36,
> 10 forks, pushed 2026-09-10) with a store protocol, eight plugins and
> independent third-party catalogues. See
> [sd-plugins and protected content](sd-plugins-and-protected-content.md) and
> [the Libby path](libby-path.md).
- Plugins are **browser JavaScript plus declarative JSON manifests**. No
  interpreter (Lua, WASM, QuickJS, Duktape) is vendored anywhere in the firmware.
- The injected API is roughly five functions — relay, crypto, writeFile,
  fetchToSd, registerAction.
- Upstream's own docs state the on-device plane works *"without any code running
  on the device."*

**So the boundary is not "curated hardware access" — it is "no execution".** A
plugin in this model is a web page talking to the firmware's HTTP server. It
could no more toggle a GPIO than a browser tab could.

The **plugin store** for this system is
[`ruqqq/crosspoint-plugins`](https://github.com/ruqqq/crosspoint-plugins) —
JavaScript, HEAD `8aa65e18`, last push 2026-08-18, ★0, **no licence file**. It
describes itself as "a plugin-store catalog and the plugins it ships". At zero
stars and no licence it is very early work, and its all-rights-reserved default
matters if anyone intends to redistribute from it.

A related first-party-adjacent example:
[`samfoy/crosspoint-bookorbit-plugin`](https://github.com/samfoy/crosspoint-bookorbit-plugin)
(JavaScript, HEAD `d5957f13`, no licence) — a reading-session sync plugin, which
is exactly the shape this system is good at: **network and data, not hardware**.

## System 2 — the `mekhontsev` native plugin host

[`mekhontsev/crosspoint-plugins`](https://github.com/mekhontsev/crosspoint-plugins)
— C/C++, **MIT**, HEAD `b503aaa7`, last push 2026-09-01.

This is a genuinely different architecture and it invalidates any blanket claim
that "CrossPoint plugins can't run on the device". It is **native C++ ELF modules
loaded from the SD card at runtime**, against a versioned host ABI (**currently
version 3**).

```
upstream CrossPoint Reader
      │  small, mergeable fork delta
      ▼
firmware fork: Plugins entry + loader + host ABI + BLE transport
      │  lazy native loading from /plugins
      ▼
manager.so ──discovers child metadata──► terminal.so, further .so modules
      ▲
      │  authenticated PageWire protocol (BLE)
PageWire client (Android/Termux)
```

Design points worth recording:

- **Lazy.** No plugin code runs at boot. `manager.so` loads only when the user
  opens the Plugins menu.
- **No firmware-side catalog.** The firmware knows one path,
  `/plugins/manager.so`, and an ABI version. Child modules are discovered from
  metadata embedded in their own ELF images (`.crosspoint.plugin` section).
- **Independently updatable** — plugins rebuild and reinstall without reflashing
  the reader.
- **Explicitly not a sandbox.** The docs say so directly: *"This is an
  experimental native extension mechanism, not a security sandbox. A bad plugin
  can crash and restart the reader."* Containment is that a crashed activity
  doesn't enter the boot path — remove the `.so` and the reader is fine.
- **Small upstream delta** — the firmware fork is deliberately kept mergeable,
  matching the ecosystem's general fork discipline.

It is a three-repository system: the firmware fork
(`mekhontsev/crosspoint-reader`), the plugins, and `mekhontsev/pagewire` (the
Android/Termux client and protocol spec). **Xteink X4 Pro only**, and
self-described as experimental.

### The ABI allow-list — the actual boundary

This is the load-bearing detail. The host exposes a deliberately small symbol
allow-list, and **the plugin build fails if a module references anything outside
it**:

| Exposed | |
|---|---|
| Activity lifecycle | `onEnter`, `loop`, `onExit`, redraw, child activities |
| Display and UI | screen size, text measurement/drawing, lines, rects, framebuffer, theme metrics, plugin-registered fonts |
| Input | mapped hardware buttons, touch rectangles, long presses |
| Text input | the firmware-owned keyboard (`crosspoint_plugin_*_keyboard_v2`) |
| Localization | `I18n` lookup |
| BLE | the shared authenticated PageWire GATT transport |
| Plugin management | child discovery, streamed install, update status |
| Diagnostics/runtime | logging, time, heap/PSRAM queries, allocation, a limited C/C++ runtime, a small FreeRTOS subset |

**Explicitly *not* exported:** *"general storage, Wi-Fi, networking, and arbitrary
NimBLE APIs"*. And notably **no GPIO, no I²C, no SPI** appears anywhere in the
list.

`PluginHostSymbols.inc` in the firmware fork is the authoritative allow-list, and
the docs are precise that *"a declaration being present in a firmware header does
not make its implementation part of the plugin ABI."*

## What this means for NFC and LoRa on the PaperMono

The [PaperMono](../../../../devices/m5stack/papermono/README.md) has an ST25R3916
NFC reader on I²C and an SX1262 LoRa module on SPI, both behind an I/O expander
that also gates their power rails.

Working through it:

1. **Upstream JS plugins — impossible.** No MCU-side execution. Not a limitation
   to work around; there is nothing to work with.
2. **Native ELF plugins — blocked by the allow-list, not by the architecture.**
   Native code does run on the MCU. But NFC needs I²C, LoRa needs SPI, and both
   need expander-controlled enables — none exported. The build would **fail at
   link time** on the unresolved symbols, by design.
3. **The documented escape hatch is small.** The plugin docs say: *"When a
   genuinely reusable host service is missing, add the smallest stable entry point
   to the firmware ABI, add it to the allow-list, and increment the ABI if the
   change is incompatible."*

**So the honest answer is a firmware change is required — but a small, structured
one**, not a fork of the reader. Something like an `i2cTransfer` / `spiTransfer`
host service plus expander-pin control, added to `PluginHostSymbols.inc` with an
ABI bump. The radio driver itself (RadioLib, an ST25R3916 stack) could then live
entirely in the plugin.

Two caveats before anyone treats that as a plan:

- **The ABI is X4 Pro-only today.** The PaperMono is not a target of this fork,
  so the port work comes first — and the PaperMono's peripherals sit behind an
  M5IOE1 expander and M5PM1 power manager that this fork has never seen.
- **Exporting raw bus access weakens the containment story.** A plugin that can
  drive I²C can also wedge the shared bus that the RTC, touch, IMU, expander and
  power manager all sit on — see the PaperMono's
  [resources-and-conflicts](../../../../devices/m5stack/papermono/resources-and-conflicts.md).
  The charger already has a documented bus-stability hazard on that bus.

**A cleaner design would export *capability* services** — "read an NFC tag",
"send a LoRa packet" — rather than raw buses, keeping bus arbitration in the
firmware where it belongs. That is a firmware feature with a plugin-facing API,
which is arguably the right answer anyway.

## Correction to this knowledge base

An earlier pass recorded, flatly, that CrossPoint plugins *"cannot reach GPIO,
I²C, SPI or any peripheral — the injected API is five functions"*, and that
therefore NFC/LoRa *"would require a fork."*

That was **true of upstream's system and wrong as a general claim.** A
third-party fork has built a native ELF plugin host where plugin code genuinely
executes on the MCU. The correct statement is:

> Hardware access is gated by a **firmware-side ABI allow-list**, not by the
> absence of on-device execution. Extending it is a documented, bounded
> firmware change rather than a fork of the reader.

Recorded here rather than silently edited, per the method's treatment of refuted
claims. Date 2026-09-04; refuting artifacts `ARCHITECTURE.md` and
`PLUGIN_DEVELOPMENT.md` in `mekhontsev/crosspoint-plugins` at HEAD `b503aaa7`.


### Verified at source, not just documentation (2026-09-04)

The previous section reported the allow-list from `PLUGIN_DEVELOPMENT.md`. The
authoritative file has now been **read directly** —
`mekhontsev/crosspoint-reader:main/src/plugins/PluginHostSymbols.inc`, 81 lines,
5,201 bytes, retrieved 2026-09-04 (`executed-success`).

It is a flat list of `PLUGIN_HOST_SYMBOL(n, "<mangled name>")` entries. Census by
category:

| Category | Present in the allow-list? |
|---|---|
| **I²C** | **absent** |
| **SPI** | **absent** |
| **GPIO** (`pinMode`, `digitalWrite`) | **absent** |
| **ADC / PWM / LEDC** | **absent** |
| **Wi-Fi** | **absent** |
| **Storage / file** | **absent** |
| BLE (`ble_terminal::*`) | **present, 15 symbols** |

What *is* exported, from the demangled names: `logPrintf`; `GfxRenderer`
(`insertFont`, `clearScreen`, `getTextWidth`, `displayBuffer`); `UITheme`
(`drawCenteredText`, `drawCenteredWrappedText`, `instance`); `Activity`
(`onEnter`, `onExit`, `onGoHome`, `requestUpdate`, `requestUpdateAndWait`,
`startActivityForResult`); `I18n::getInstance`; `EspClass::getFreeHeap` and
`getFreePsram`; and the `ble_terminal` transport surface.

**The documentation was accurate.** A plugin gets UI, input, BLE, i18n and heap
introspection — and nothing that touches a bus, a pin or a filesystem. The
peripheral gap is not an oversight in the docs; it is the actual contract, in the
actual file, and the build enforces it.

## Sources

| ID | What | Retrieved |
|---|---|---|
| PL01 | `ruqqq/crosspoint-plugins` metadata, HEAD `8aa65e18` | 2026-09-04 |
| PL02 | `mekhontsev/crosspoint-plugins` metadata, HEAD `b503aaa7`, MIT | 2026-09-04 |
| PL03 | `mekhontsev/crosspoint-plugins/ARCHITECTURE.md` | 2026-09-04 |
| PL04 | `mekhontsev/crosspoint-plugins/PLUGIN_DEVELOPMENT.md` — the ABI allow-list | 2026-09-04 |
| PL05 | `samfoy/crosspoint-bookorbit-plugin` metadata, HEAD `d5957f13` | 2026-09-04 |

## Open questions

- **Upstream's JS plugin system was not re-verified in this pass.** Its
  description is carried over from an earlier analysis.
- `PluginHostSymbols.inc` was **not read directly** — the allow-list above is
  from the documentation that describes it. Read the file before designing
  against it.
- Whether upstream intends to adopt anything like the native ABI is unknown.
- No plugin was built; the ABI-v3 contract is untested here.

## See also

- [CrossPoint Reader](../README.md) — the firmware
- [Fork network](../../../ecosystems/crosspoint-freeink/fork-network.md) — how forks like `mekhontsev`'s relate to upstream
- [PaperMono NFC](../../../../devices/m5stack/papermono/features/nfc.md) · [LoRa](../../../../devices/m5stack/papermono/features/lora.md)
