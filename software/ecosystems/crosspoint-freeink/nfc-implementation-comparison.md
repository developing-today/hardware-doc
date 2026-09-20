# Three NFC implementations on the PaperMono — a technique comparison

> The same chip, the same board, three independent approaches — and one of them
> found a remotely-reachable stack overflow in M5Stack's own NFC library.
>
> Researched **2026-09-11**. Repository, build-config and patch-source facts are
> `executed-success` (files fetched and read). Behavioural claims are `inferred`;
> **nothing was built, flashed or tested against a tag.**

## The three

| | **Vendor UserDemo** | **`ciniml/paper_name_plate`** | **`Corvelis/m5-touch-card`** |
|---|---|---|---|
| Language | C++ / Arduino | **Rust, `no_std`** | C++ / Arduino |
| Framework | ESP-IDF 5.5.1 + arduino-esp32 3.3.10 | **esp-hal 1.1.x** | PlatformIO, espressif32 6.12.0, `-std=gnu++17` |
| NFC driver | `M5Unit-NFC`, as shipped | **written from scratch** (28.9 KB) | `M5Unit-NFC` **pinned + patched** |
| NFC role | reader — identity probe | **tag emulation** (T2T, ISO-DEP, NDEF) | **tag emulation** (NFC-A) |
| Graphics | M5GFX | own SSD1677 + `embedded-graphics 0.8` | M5GFX 0.2.27 |
| Storage | — | `config_store.rs` | **LittleFS**, 16 MB OTA partition table |
| Companion | — | Web Bluetooth page (GitHub Pages) | **smartphone app** (`mobile/`) |
| Licence | MIT | **none** | MIT |

Three positions on the same axis: **use the vendor library**, **fix the vendor
library**, **replace it entirely**.

## The headline: `M5Unit-NFC` 0.1.0 has an RF-reachable stack overflow

`Corvelis` ships `firmware/scripts/patch_m5unit_nfc.py` — a 374-line PlatformIO
**pre-build script that patches the vendor library in place** before compiling.
Its docstring states the problem plainly:

> *"M5Unit-NFC 0.1.0 uses 64-byte stack buffers in the NFC-A emulation listener.
> PaperMono's tested transport uses a 253-byte command (240-byte DATA payload),
> so both listener buffers are expanded to 256 bytes. The explicit length guard
> also makes malformed RF frames fail closed before the FIFO read."*

The original code reads a length from the chip's FIFO and then reads that many
bytes into a **64-byte stack buffer with no bounds check**:

```cpp
_u.readFIFOSize(bytes, bits);
rx_len = bytes;
if (irq32 & (I_par32 | I_crc32 | I_err132 | I_err232) || rx_len <= 2) {
```

The patch inserts the guard the original lacks:

```cpp
if (rx_len > sizeof(rx)) {
    M5_LIB_LOGE("A RX oversized %u", rx_len);
    _u.writeDirectCommand(CMD_CLEAR_FIFO);
    _u.writeDirectCommand(CMD_UNMASK_RECEIVE_DATA);
    return EmulationLayerA::State::Active;
}
```

**Severity.** In emulation mode the length is attacker-controlled — it comes from
an RF frame sent by whatever is holding a reader near the device. An oversized
frame smashes a 64-byte stack buffer. No authentication is involved because none
exists at that layer; proximity is the only precondition.

**Status: `inferred`, not demonstrated.** The missing bound is visible in the
source and the patch author describes it as a real transport problem they hit.
Whether it is practically exploitable versus merely a crash was **not tested**,
and nothing was run. Recorded because the method calls for auditing vendor driver
source, and this is exactly what that is for.

Note the vendor's own UserDemo uses `M5Unit-NFC` **unpatched** — but in *reader*
mode, where the emulation listener is not the active path.

## Six more defects the same patch fixes

`patch_m5unit_nfc.py` is a small vendor-library audit in its own right:

| # | Fix | What it says about the library |
|---|---|---|
| 1 | `uint8_t rx[64]` → `rx[256]` (both listener buffers) | Sized for a protocol smaller than the one in use |
| 2 | Length guard before `readFIFO` | **The overflow above** |
| 3 | IRQ poll: also check `gpio_get_level(irq)` | *"The ST25R3916 IRQ output stays high until its interrupt registers are read. If the GPIO rising edge is missed, checking only the ISR flag **deadlocks NFC-A emulation in Ready forever**."* A missed edge is unrecoverable |
| 4 | `gpio_isr_handler_remove()` before `add` | *"A failed `begin()` can leave this instance's IRQ handler installed"* — retry path leaks a handler |
| 5 | `picc.isMifareUltralight()` instead of an explicit type pair | Library had responses for the whole Ultralight family but gated emulation to two types |
| 6 | Field-off detect adds `is_extra_field()`; `begin()` reports *why* it failed | Field detection and diagnostics |

Fix 3 is the one most likely to be mistaken for a hardware fault: emulation
silently wedges in `Ready` and never recovers. The patch notes the library's own
blocking `wait_for_interrupt()` already polls the pin level *for the same reason*
— so the fix pattern was present elsewhere in the same driver and simply not
applied here.

## Why the Rust project wrote its own driver

`ciniml/paper_name_plate` states its reasoning in `DESIGN.md`:

> *"We implement drivers ourselves rather than relying on external crates
> (`ssd1677` etc.). PaperMono has many device-specific circumstances — 4-gray,
> OTP waveforms, reset via IOE1 — and existing crates do not anticipate the
> 800×480 4-gray + external-reset combination."*

That reasoning is about the **display**, but the same logic produced a
from-scratch `st25r3916.rs` (28.9 KB) plus `t2t_emu.rs` (19.8 KB), `isodep.rs`
and `ndef.rs`. There is no Rust ST25R3916 crate to lean on, so "write it" was the
only option rather than a preference.

**Consequence:** it is the only one of the three that owns its full NFC stack, so
none of the `M5Unit-NFC` defects above apply to it — and any equivalent bugs it
has are its own and undocumented.

## Architecture contrasts worth noting

**Peripheral access.** All three drive the M5IOE1 expander and M5PM1 PMIC
directly rather than through an abstraction — the vendor demo via its own HAL,
`paper_name_plate` via hand-written `ioe1.rs`/`pm1.rs`, `Corvelis` via
`M5UnitUnified`/`M5HAL`. **None uses the FreeInk SDK**, which independently
supports the conclusion in
[radios-on-papermono](../../ecosystems/crosspoint-freeink/radios-on-papermono.md)
that the SDK abstraction is optional for radio work.

**Partitioning.** Only `Corvelis` ships an OTA-capable table
(`partitions_16mb_ota_4m_littlefs_7m.csv` — 4 MB app slots, 7 MB LittleFS). The
vendor image is a single `factory` app with **no OTA**. That is the difference
between a demo and something intended to be updated in the field.

**Configuration UX.** Three different answers to "how does a user set this up":
vendor — none; `paper_name_plate` — **Web Bluetooth page** served from GitHub
Pages; `Corvelis` — a **native smartphone app** with its own `protocol/`
directory. For a device with no keyboard, this is the real design problem, and
nobody chose the device's own web server.

**Build-time patching as a technique.** `Corvelis`'s approach — pin the dependency
to an exact commit, then patch it in a `pre:` script — is worth calling out. It
keeps the fix reproducible and visible in-tree without forking the library, at
the cost of breaking silently if upstream changes the matched text. The script
carries both `_ORIGINAL` and `_LEGACY_PATCHED` variants, so the author has
already hit that.

## What this says about the ecosystem

**The vendor library is the weak link and two of three projects routed around
it.** One patched it, one replaced it. Only the vendor's own demo uses it as
shipped, and only in the mode that avoids the defective path.

**Nobody has upstreamed the fixes.** The patch lives in one project's build
scripts. `M5Unit-NFC` at the pinned commit `93745b54` presumably still has the
missing bound.

**Two independent projects converged on tag emulation**, not tag reading — the
PaperMono's natural NFC product is *being* a tag, not reading one.

## Open questions

- **Nothing was built, flashed or tested.** No tag was read, no emulation
  exercised, no overflow attempted.
- **The overflow is `inferred` from source.** Exploitability versus
  crash-only was not assessed, and no responsible-disclosure step was taken from
  here.
- Whether `M5Unit-NFC` has since fixed any of this upstream was **not checked** —
  `Corvelis` pins `93745b54`, and current `main` was not compared.
- `paper_name_plate`'s own NFC stack was **not audited** for equivalent defects.
- The vendor UserDemo's NFC path was inferred from earlier research, not re-read
  for this comparison.

## Sources

All 2026-09-11: `Corvelis/m5-touch-card` `firmware/platformio.ini`,
`firmware/src/`, `firmware/lib/`, and `firmware/scripts/patch_m5unit_nfc.py`
(374 lines, read in full); `ciniml/paper_name_plate` `README.md`, `DESIGN.md`,
`src/` listing; `m5stack/M5PaperMono-UserDemo` from prior research.
Archived copies of the plugin-ecosystem repos are listed in
[source-snapshots.ARCHIVED.md](../../applications/crosspoint-reader/plugins/source-snapshots.ARCHIVED.md);
the NFC projects are archived at
`archive/software/ecosystems/crosspoint-freeink/nfc-source-snapshots/`:
`ciniml/paper_name_plate` @ `7eac75d`, `Corvelis/m5-touch-card` @ `fc20a44`,
`m5stack/M5PaperMono-UserDemo` @ `c109910`, and **`m5stack/M5Unit-NFC` @ `93745b5`**
— the last so the unpatched defective source is preserved alongside the patch
that fixes it.
