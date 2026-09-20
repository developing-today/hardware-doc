# `ciniml/paper_name_plate` — code review

> A bare-metal Rust firmware for the M5Stack PaperMono, reviewed to the same
> standard applied to `M5Unit-NFC` — including looking for the *same class* of
> bug.
>
> Reviewed **2026-09-11** at HEAD `7eac75dfc9`, 29 commits, sole author
> **Kenta IDA (ciniml)**. Source-level review only: **nothing was built, flashed
> or run.** Findings are `inferred`.

## What it is

A digital name badge. It shows your contact details on the e-paper, **emulates an
NFC tag** so a phone tap retrieves them, and is configured over **BLE** from a Web
Bluetooth page served via GitHub Pages.

Notable as the only PaperMono firmware written in Rust, and one of only two
third-party projects driving the board's NFC.

```
src/st25r3916.rs   28.9 KB   NFC transceiver driver, from scratch
src/t2t_emu.rs     19.8 KB   NFC Forum Type 2 Tag emulation
src/board.rs       14.6 KB   board bring-up: pins, PMIC, expander, EPD power
src/pm1.rs          8.4 KB   M5PM1 PMIC
src/ioe1.rs         6.3 KB   M5IOE1 I/O expander
src/ndef.rs         5.4 KB   NDEF encoding
src/isodep.rs       5.3 KB   ISO-DEP
src/config_store.rs 4.4 KB   persistence
src/ft6336.rs       3.2 KB   touch
src/ssd1677/        —        panel driver, 4-gray LUTs, 2-plane framebuffer
```

Toolchain: `esp-hal 1.1.x`, `xtensa-esp32s3-none-elf`, `embedded-graphics 0.8`,
`espflash`. Blocking, no `embassy` — a stated choice to revisit when event
handling demands it.

## The headline: it contains the *same logic error* as `M5Unit-NFC`, with a different outcome

This is the most instructive thing in the review, and it is a genuinely
apples-to-apples comparison.

**`src/t2t_emu.rs:397–399`:**

```rust
let mut rx = [0u8; 64];
let n = bytes as usize - 2;     // strip CRC — NOT clamped to rx.len()
nfc.read_fifo(&mut rx[..n])?;
```

`bytes` is the FIFO length, read from the chip, derived from an RF frame — up to
**512**. `rx` is **64 bytes**. This is precisely the mistake at
`emulation_layer_a_ST25R3916.cpp:444`.

**The consequence is not the same:**

| | `M5Unit-NFC` (C++) | `paper_name_plate` (Rust) |
|---|---|---|
| `n > 64` | `readRegister` writes past `rx` — **stack overflow**, RF-controlled data | `&mut rx[..n]` **panics** — bounds-checked slice |
| `bytes < 2` | n/a | `bytes - 2` **underflows**; debug panics, release wraps to `usize::MAX-1` → the slice index then panics anyway |
| Class | **memory corruption** | **denial of service** |

Both are bugs and both are reachable from RF. Only one is a memory-safety
failure. The device reboots instead of having its stack rewritten — which is
exactly the tradeoff the language is for, and it is nice to see it demonstrated
on the same chip, the same protocol, and the same mistake.

**Recommended fix**, matching the file's own idiom elsewhere:

```rust
let n = (bytes as usize).saturating_sub(2).min(rx.len());
```

## The API shape is why the C++ bug was possible and this one is bounded

```rust
pub fn read_fifo(&mut self, buf: &mut [u8]) -> Result<(), I2C::Error>
```

versus

```cpp
uint32_t readFIFO(uint16_t& actual, uint8_t* buf, const uint16_t buf_size);
```

The Rust signature **cannot be lied to**: the slice carries its own length, so
"capacity" and "requested length" are the same value. The C++ signature separates
pointer from size, which is the shape that invites passing the FIFO length where
the buffer capacity belongs — and that is exactly what happened.

Worth stating plainly because it is a design lesson, not a language-war point:
**the defect was in the interface, and the caller was merely where it surfaced.**

## The other three FIFO call sites are correct

```rust
// st25r3916.rs:697-699
let (bytes, _) = self.fifo_status()?;
let n = (bytes as usize).min(rx.len());      // clamped
self.read_fifo(&mut rx[..n])?;

// t2t_emu.rs:350, :386
let n = (bytes as usize).min(4);             // clamped
nfc.read_fifo(&mut peek[..n])?;
```

And the anticollision path bounds both ends of the range:

```rust
// st25r3916.rs:615-618
let want = 5 - rbuf_offset;
let actual = (bytes as usize).min(want);
if actual == 0 { return Err(Error::Protocol); }
self.read_fifo(&mut rbuf[rbuf_offset..rbuf_offset + actual])?;
```

So three of four sites are right. The defective one is an outlier — the same
profile as the C++ library, where one of two sites was wrong.

## Safety posture

| Metric | Count | Assessment |
|---|---|---|
| `unsafe` blocks | 7 | Low for bare-metal; **not individually audited** |
| `panic!`/`unwrap`/`expect` | **3** | All init-time invariants, all legitimate |
| Unchecked slice ranges | 12 | One is the defect above |
| Checked `.get()`/`.get_mut()` | 20 | Checked access outnumbers raw indexing |

The three panic sites are `board.rs:143` `.expect("i2c config")`, `board.rs:203`
`.expect("spi config")`, and `app/mod.rs:754`
`.expect("poll_nfc only runs with NFC")`. All are boot-time configuration or
documented preconditions — the right places to panic. **There is no
`unwrap()` in the RF data path**, which is the discipline that matters.


## The seven `unsafe` blocks — audited

Previously counted but unread. All seven examined 2026-09-11:

| # | Site | Purpose | Assessment |
|---|---|---|---|
| 1 | `ssd1677/framebuffer.rs:133` | In-place `MaybeUninit` init of the two-plane framebuffer via `addr_of_mut!` + `write_bytes` | **Sound.** Correct idiom — no reference to uninitialised memory is created. Avoids a large stack copy |
| 2 | `bin/main.rs:39` | Registers a second heap region from `static mut MaybeUninit<[u8; N]>` | **Sound.** Standard `esp_alloc` pattern, one-shot at boot, `#[allow(static_mut_refs)]` acknowledged |
| 3 | `app/mod.rs:80` | `doze_diag_set` writes a `static mut` diagnostic array | **Sound-ish.** Uses `addr_of_mut!`; `d[idx]` is a *bounds-checked* array index, so a bad index panics rather than corrupting. No synchronisation, but the path is single-threaded |
| 4 | `app/mod.rs:92` | Reads the USB SOF frame counter via `esp32s3::USB_DEVICE::ptr()` | **Sound.** Ordinary PAC register read, used to detect a live USB host so the console stays usable |
| 5 | `app/mod.rs:101` | Reads the diagnostic array (`addr_of!`) | **Sound** |
| 6 | `app/mod.rs:108` | Zeroes the diagnostic array | **Sound** |
| 7 | `board.rs:227` | **`clone_unchecked()` on four GPIOs** — all four also get live `Input` drivers | **Permanent duplicate ownership**, sound only by temporal discipline — see below |

### The one worth scrutiny

```rust
// SAFETY: the clones are only used to program RTC-IO wake-up right
// before deep sleep, when the `Input` drivers are no longer used.
let wake_pins: [AnyPin<'static>; 4] = unsafe {
    [ p.GPIO6.clone_unchecked().into(),   // NFC IRQ
      p.GPIO4.clone_unchecked().into(),   // touch INT
      p.GPIO2.clone_unchecked().into(),   // button A
      p.GPIO3.clone_unchecked().into() ]  // button B
};
let tp_int   = Input::new(p.GPIO4, /* … */);   // line 235
let nfc_irq  = Input::new(p.GPIO6, /* … */);   // line 236
let button_a = Input::new(p.GPIO2, /* … */);   // line 270
let button_b = Input::new(p.GPIO3, /* … */);   // line 271
```

`clone_unchecked()` deliberately duplicates pin ownership — precisely what
esp-hal's type system exists to prevent. **All four cloned pins then receive live
`Input` drivers within the next 45 lines**, and `Board` (`board.rs:294`) stores
*both* sets:

```rust
Board { … tp_int, nfc_irq, button_a, button_b, …, wake_pins, … }
```

So the duplicate ownership is **structural and lasts the entire life of the
program**, not a brief window — an earlier draft of this review said the window
was small, which was wrong. What is small is the *use* of the clones: they are
touched only at `app/mod.rs:376`, destructured as `[nfc, tp, btn_a, btn_b]`
immediately before deep sleep.

The soundness argument is therefore **purely temporal** — two owners of each pin
coexist permanently, and correctness depends on never using them at overlapping
times. This is a recognised embedded pattern (RTC wake-up needs the pin identity
while a driver still holds it, and esp-hal offers no safe way to express that),
and the author both documented it and named the invariant. But it is enforced by
discipline alone, and a refactor that touched `wake_pins` outside the sleep path
would break it silently.

**Overall:** all seven are recognised embedded-Rust idioms, **none is in the RF
data path**, and the riskiest is documented. This is careful code.

## Engineering quality

**Hardware bring-up is defensive.** A commit titled *"Recover from a flaky I2C bus
at boot: retry IOE1 EPD power-on"* — independent corroboration that this board's
shared I²C bus needs retry logic, matching what the device record says about bus
contention.

**The `DESIGN.md` is the best third-party PaperMono hardware document that
exists.** It independently confirms this knowledge base's pin map on every
contested point, states the `PYGn` 1-based/0-based trap explicitly, and records
bus speeds (PM1/IOE1 100 kHz, touch/NFC 400 kHz) that no vendor document gives.

**Driver decisions are justified in writing.** On writing its own drivers:
*"existing crates do not anticipate the 800×480 4-gray + external-reset
combination."* On licences, it notes M5GFX's LUTs are FreeBSD and reusable —
attribution done properly.

**Commit messages are precise** — *"Clear the display image over BLE (CTRL 06)"*,
*"Report rejected plate text as STATUS state 5"*. This reads as careful work.

## Risks

- **No `LICENSE` file.** All-rights-reserved by default. Read for technique; do
  not copy. This is the single biggest practical barrier to the project being
  useful to others.
- **Bus factor 1.** 29 commits, one author, ★0.
- **The `t2t_emu.rs` defect is live** at HEAD.
- ~~`unsafe` blocks not audited~~ — **all seven audited**; see above. One (`board.rs:227`, `clone_unchecked`) carries an unenforced invariant.
- **BLE control surface not reviewed.** It accepts plate text and display
  commands over BLE; input validation was not examined. There is a hint of
  validation (*"Report rejected plate text"*), but it was not verified.
- Release-mode integer overflow behaviour was not confirmed against the project's
  `Cargo.toml` profile settings.

## What was not done

- **Nothing built or run.** No device, no toolchain invocation, no tag read.
- Only the NFC and FIFO paths were reviewed closely; `ndef.rs`, `isodep.rs`,
  `config_store.rs` and `ssd1677/` were **not** reviewed.

- No fuzzing, no static analysis, no `cargo clippy` run.
- The defect was **not reported to the author.**

## See also

- [The `M5Unit-NFC` overflow](m5unit-nfc-overflow.md) — the C++ counterpart
- [NFC implementation comparison](nfc-implementation-comparison.md)
- Archived at `archive/software/ecosystems/crosspoint-freeink/nfc-source-snapshots/ciniml_paper_name_plate/`
