# CrossInk + PaperMono + plugins + radios — a feasibility assessment

> Four questions, answered against the source rather than the marketing:
> can CrossInk run on a PaperMono, can it take the plugin store and Libby, what
> does updating the fork cost, and what would basic LoRa/NFC take?
>
> Measured **2026-09-04**. Repository and source facts are `executed-success`
> (repos cloned, files read, GitHub compare API). Effort estimates are
> `inferred`. **No hardware, and nothing was built for CrossInk.**

## Short answers

| Question | Answer |
|---|---|
| Does CrossInk support the PaperMono? | **No — and it structurally cannot today.** Its pinned SDK predates PaperMono support entirely |
| Can it take the plugin store? | **No.** CrossInk has no on-device plugin system, and neither does upstream on `develop` |
| Can it take Libby? | **Yes, already — and no firmware change is needed.** Libby is host-side Calibre tooling |
| What does updating the fork cost? | **High.** 294 commits behind, with divergence concentrated in `lib/` (224 files) — the opposite of a clean additive fork |
| What would LoRa/NFC take? | **A new capability class in the SDK.** Neither radio has *any* abstraction today |

## 1. PaperMono on CrossInk

**CrossInk has no PaperMono support of any kind.** Grepping the whole repository
for `papermono`, `paper_mono` or `C153` across `.ini`, `.h`, `.cpp` and `.md`
returns **zero matches**.

Its build environments (`platformio.ini`, HEAD `cab4f249`, branch `main`):

```
default · debug · simulator · simulator-X3 · sticky-simulator
x4-pro-simulator · sticky · sticky-debug
```

So: the C3 devices (`default`), the Seeed reTerminal Sticky, and simulator
variants. No PaperMono, and notably no non-simulator X4 Pro env either.

### The blocker is the SDK pin, not the build config

This is the part that makes it more than a missing `[env:]` block.

| | freeink-sdk commit | PaperMono refs in `BoardConfig.h` |
|---|---|---|
| **CrossInk** | `1ff020263cd2202ea79ce3eb811f5ac8489b8cde` | **0** |
| **CrossPoint** | `68425f8eec1246a0be0c0f311540f60ad733fa76` | **37** |

`GET /compare/1ff02026...68425f8e` → **ahead 136, behind 0, 103 files changed.**

**PaperMono board support was added to the FreeInk SDK in those 136 commits.**
CrossInk's pin predates it. There is nothing to switch on.

In the newer SDK the support is real and structural — `FREEINK_DEVICE_PAPERMONO`,
`BoardProfile PAPER_MONO`, `FREEINK_DRIVER_PAPER_MONO`, a `Board::PaperMono`
case, and the device appears in the capability groupings for touch, frontlight,
USB-MSC, **MIC** and **LED**.

### So the work is, in order

1. **Bump the submodule 136 commits** — 103 files of SDK change landing under a
   fork that has diverged from upstream. This is the real cost, not the envs.
2. Add `[env:papermono]` (and release variants), mirroring CrossPoint's.
3. Reconcile CrossInk's own `lib/` changes against SDK API drift across 136
   commits.

Step 3 is unbounded from here — it depends on which SDK APIs CrossInk touches,
which was not audited. **Do not read "add an env" as the estimate.**

## 2. The plugin store

**Not available on CrossInk, and not because of CrossInk.**

CrossInk contains no on-device plugin system. Every `plugin` match in the
repository is documentation about the **Calibre** device plugin
(`docs/user-guide.md`, `docs/webserver.md`) — host-side, unrelated.

Upstream is the same: the JavaScript plugin work lives on two unmerged branches,
never on `develop`. The store (`ruqqq/crosspoint-plugins`, ★0, no licence)
catalogues plugins for a system that has not shipped in either firmware.

The **native** plugin host — `mekhontsev`'s ELF-module system with a versioned
ABI — is a *different fork's* invention and is **X4 Pro only**. It is not in
CrossInk and not in upstream.

So "incorporating the plugin store into CrossInk" means first importing a plugin
system that does not exist in either parent. See
[plugin systems](../../applications/crosspoint-reader/plugins/README.md).

## 3. Libby — already solved, at the wrong layer to worry about

Libby is **not device software.** `ping/libby-calibre-plugin` runs inside Calibre
on a computer; it fetches OverDrive loans into a Calibre library. The device
never speaks to OverDrive.

CrossInk's own `docs/user-guide.md` already documents receiving books via the
**CrossPoint Calibre device plugin**, and its web server implements the Calibre
Wireless path (`src/network/CrossPointWebServer.cpp`, `docs/webserver.md`).

**So the Libby → Calibre → CrossInk chain works today with no firmware change.**

Two caveats carried from the [Calibre record](../../tooling/calibre/README.md),
and they are the real risks:

- `libby-calibre-plugin` was **last pushed 2023-12-01** — nearly three years
  stale against a vendor-controlled API. Whether it still works is untested here.
- **DRM is the actual barrier.** Most commercial library loans are Adobe
  ADEPT-protected, and no CrossPoint-family firmware has a DRM client. Unprotected
  loans pass through; protected ones do not open, and no firmware work changes
  that.

## 4. Updating the fork — the expensive part

CrossInk vs upstream `develop`, 2026-09-04:

```
ahead 616 · behind 294 · 300+ files changed (API caps the list at 300)
top directories: lib/ 224 · docs/ 45 · .github/ 11 · include/ 5
```

**224 of the changed files are in `lib/`** — the shared library layer, not
quarantined new directories.

Contrast [CrossPlay](../../applications/crossplay/README.md), which is 2,610
commits ahead but only **2 behind**, with its additions confined to
`src/apps_local/` and ~15 documented seams. CrossInk is the opposite pattern:
fewer commits, far more entanglement with code upstream is actively changing.

**Consequences:**

- Merging 294 upstream commits into 224 modified shared files is a genuinely hard
  merge, not a routine sync.
- The SDK bump in §1 (136 commits, 103 files) lands *on top of* that.
- Prior research recorded that in this ecosystem **"commits behind" is a
  brick-risk signal**, because vendors revise hardware silently and upstream
  carries the fixes. 294 behind is a lot of unabsorbed hardware fixes.

CrossInk is actively maintained (pushed 2026-09-03), so this is deliberate
divergence rather than abandonment — but it is divergence that compounds.

## 5. LoRa and NFC — the decisive finding

**The FreeInk SDK has no radio abstraction whatsoever.** This is the answer that
governs the whole question, for CrossInk *and* CrossPoint *and* CrossPlay.

The SDK's complete capability set:

```
AUDIO · BLE_HID_HOST · BLE_KEYBOARD · BUZZER · COLOR · FRONTLIGHT
IMU · LED · MIC · NET_TLS · RTC · TEMP_HUMIDITY · TOUCH · USB_MSC · WARMLIGHT
```

**No `FREEINK_CAP_LORA`. No `FREEINK_CAP_NFC`. No RFID.**

What the greps actually found, and why neither counts:

| Match | Reality |
|---|---|
| `T5S3_LORA_CS/IRQ/RST/BUSY` in `BoardT5S3Pins.h` | Pin *numbers* for the LilyGo T5S3 |
| `pinMode(T5S3_LORA_CS, OUTPUT)` in `BoardT5S3.cpp` | **Deasserting chip-select** so the LoRa chip does not corrupt the shared SPI bus. Housekeeping, not a driver |
| `0x50 (NFC on Pro)` in `InputManager.cpp` | A **comment** in an I²C-address list, so the bus scanner knows what it may see |

That is the entirety of radio awareness in the SDK: know the pins exist, keep
them quiet, and don't be surprised by an I²C address.

### What adding basic LoRa/NFC actually requires

Not a plugin, and not a build flag. The pattern the SDK already uses for `Rtc`
and `Imu` would have to be repeated:

1. **New capability flags** — `FREEINK_CAP_LORA`, `FREEINK_CAP_NFC` — gated per
   board profile.
2. **New board-profile fields** — SPI pins, NSS, BUSY, DIO/IRQ, reset, antenna
   switch for LoRa; I²C address and IRQ for NFC. On the PaperMono these are not
   direct GPIO: reset and antenna switch run through the **M5IOE1 expander** and
   the LoRa rail is enabled by the **M5PM1** power manager
   ([pinouts](../../../devices/m5stack/papermono/pinouts-and-buses.md)).
3. **New device managers** — `LoRaManager`, `NfcManager` — alongside the existing
   `Rtc`/`Imu`/`FrontlightManager`, wrapping **RadioLib** (MIT at the pinned
   7.2.1) and an ST25R3916 stack such as ST's RFAL.
4. **Application surface** — some UI, since a reader firmware has no concept of a
   radio today.
5. **Regional band configuration for LoRa**, which is a legal constraint the
   firmware would then own — see [`guides/lora`](../../../guides/lora/README.md).

**And a plugin cannot do this.** The native plugin ABI's authoritative allow-list
(`PluginHostSymbols.inc`, 81 symbols, read directly) exports **no I²C, SPI, GPIO,
ADC or PWM** — the link fails if a module references them. Radios need a firmware
change first, exposing either raw bus access or, better, capability-level
services.

### Ordering, if someone actually wants this on a PaperMono

The dependency chain is strict and worth stating plainly:

```
1. SDK gains LoRa/NFC capability + managers        (largest piece, benefits everyone)
2. PaperMono board profile gains the radio fields   (expander + PMIC aware)
3. CrossInk bumps its SDK pin 136+ commits          (§1)
4. CrossInk adds a papermono env                    (small)
5. Application UI                                   (fork's own choice)
```

**Steps 1–2 belong upstream in the SDK**, not in a fork — which is also where
they would benefit CrossPoint, CrossPlay and every other consumer. Doing them in
CrossInk would deepen exactly the divergence that already makes §4 expensive.

## What was not checked

- **CrossInk was not built.** No compile, no simulator run — unlike upstream,
  which was [built and run successfully](../../tooling/crosspoint-simulator-build-notes.md).
  CrossInk ships its own simulator envs, so this is doable and was simply not done.
- **Which SDK APIs CrossInk's 224 modified `lib/` files touch** — the number that
  would turn §1 step 3 from "unbounded" into an estimate.
- Whether upstream or the SDK have any *stated intent* to add radio support; no
  roadmap or issue search was done.
- CrossInk's own release/versioning practice.
- No commit SHA was pinned for CrossInk's `main` beyond `cab4f249` at fetch time.

## Sources

All 2026-09-04, `executed-success`:

| What | Detail |
|---|---|
| `uxjulia/CrossInk` @ `cab4f2492` | cloned; `platformio.ini`, `.gitmodules`, `docs/`, `src/network/` read |
| `crosspoint-reader/crosspoint-reader` @ `e6139861` | cloned with submodule |
| `Free-Ink/freeink-sdk` @ `68425f8e` and `1ff02026` | `BoardConfig.h` compared; capability flags enumerated from source |
| SDK compare | `GET /compare/1ff02026...68425f8e` → ahead 136, 103 files |
| CrossInk compare | `GET /compare/develop...uxjulia:CrossInk:main` → ahead 616, behind 294 |
| `PluginHostSymbols.inc` | 81 symbols, no bus access — read directly |
