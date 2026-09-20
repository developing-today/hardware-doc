# New PaperMono projects — 2026-09-07 sweep

> The PaperMono shipped **2026-08-21**. An earlier survey on 2026-09-01
> catalogued 43 repositories. This is a re-sweep two weeks post-launch, and it
> found **five projects that did not exist or were not visible before** —
> including two in **Rust**, a language the earlier catalogue contained none of,
> and one that **implements NFC on this board**.
>
> Retrieved **2026-09-07**, `executed-success` (GitHub API + raw file reads).
> Nothing was built or run.

## What is new since 2026-09-01

| Repository | Lang | Licence | Created | Pushed | What |
|---|---|---|---|---|---|
| **[`ciniml/paper_name_plate`](https://github.com/ciniml/paper_name_plate)** | **Rust** | none | 2026-09-05 | 2026-09-06 | **Bare-metal `no_std` firmware with a full NFC stack** |
| [`canardleteer/papermono-rs`](https://github.com/canardleteer/papermono-rs) | **Rust** | MIT | 2026-09-01 | 2026-09-06 | Embedded Rust workspace — `crates/`, `firmware/`, `host/`, `xtask/` |
| [`CitizenRacer/M5PaperMonoLite`](https://github.com/CitizenRacer/M5PaperMonoLite) | C++ | MIT | 2026-09-04 | 2026-09-04 | ESPHome support — **targets the Lite**, self-described *"I have no idea what I'm doing"* |
| [`atreyap31-cell/mono-note-mini`](https://github.com/atreyap31-cell/mono-note-mini) | C | none | 2026-08-24 | 2026-09-06 | Voice-only note companion; ships a case, emulator and server |
| [`hectorzin/M5PaperMono-HomeAssistant-ESPHome`](https://github.com/hectorzin/M5PaperMono-HomeAssistant-ESPHome) | C | none | 2026-08-27 | **2026-09-07** | In the earlier catalogue; **still actively pushed** |

**Rust is the notable shift.** The 2026-09-01 catalogue was entirely C/C++ plus a
few TypeScript host tools. Two independent embedded-Rust efforts appeared within
a fortnight of launch, one of them from **ciniml (Kenta Ida)**, a well-known
Japanese embedded engineer.

## `ciniml/paper_name_plate` — the important one

**Bare-metal `no_std` Rust on `esp-hal`, and it implements NFC on this board.**
This is the first third-party artifact found anywhere that drives the PaperMono's
radios.

```
src/st25r3916.rs        28,899 B   ST25R3916 NFC driver
src/t2t_emu.rs          19,784 B   NFC Forum Type 2 Tag emulation
src/board.rs            14,579 B   PaperMono board init
src/pm1.rs               8,397 B   M5PM1 PMIC driver
src/ioe1.rs              6,291 B   M5IOE1 expander driver
src/ndef.rs              5,389 B   NDEF encoding
src/isodep.rs            5,343 B   ISO-DEP
src/ssd1677/             —         panel driver, 4-gray LUTs, framebuffer
src/ft6336.rs            3,233 B   touch
```

Toolchain: `espup`/`esp` Xtensa channel, `xtensa-esp32s3-none-elf`, **esp-hal
1.1.x**, `embedded-graphics 0.8`, `espflash`. Blocking rather than `embassy`, by
choice, with a stated intent to reconsider when NFC/touch/button events need it.

Its `DESIGN.md` explains why it writes its own drivers rather than using existing
crates: *"4-gray, OTP waveforms, reset via IOE1 — existing crates do not
anticipate the 800×480 4-gray + external-reset combination."*

> ⚠ **No `LICENSE` file.** All-rights-reserved by default. Read it for technique;
> do not copy code without asking.

## It independently confirms this knowledge base's pin map

`DESIGN.md` was written from the author's own reading of the hardware, and it
agrees with the PaperMono device record on essentially every contested point.
That is unusually strong corroboration — two independent derivations converging.

| Finding | This knowledge base | `paper_name_plate` `DESIGN.md` |
|---|---|---|
| **`PYGn` is 1-based** | recorded, with the `M5IOE1_PIN_3 = 2` off-by-one warning | *"P1..P8 → L register bit0..7, P9..P14 → H register bit0..5 (**docs' `PYGn` = 1-based**)"* |
| **Frontlight is M5PM1 GPIO3** | recorded; an earlier pass wrongly called the vendor page defective | *"Frontlight: **GPIO3** … FUNC0 → `11` (PWM0), `PWM_FREQ = 5000 Hz`"* |
| **EPD reset = M5IOE1 IO5** | recorded | *"RST = M5IOE1 **IO5 (0-based index 4)**"* — states the off-by-one explicitly |
| **NFC enable = M5IOE1 IO4** | identified as **missing from the FreeInk SDK** | *"NFC … power enable via **M5IOE1 IO4**"* |
| **LoRa reset = IO10, ant switch = IO2** | identified as missing from the SDK | *"**IO10 = LoRa RST, IO2 = LoRa ANT SW**"* |
| **LoRa SPI pins** | MOSI 38 / MISO 40 / CLK 39 / NSS 41, BUSY 21, IRQ 5 | identical |
| **IP2315 bus hazard** | recorded from the vendor warning | *"IP2315 (0x75). **Do not keep it on the bus for long** (doc warning). Don't touch it."* |
| **SSD1677 4-gray via OTP** | `0x1A=0x5A` + `0x22=0xD7` | identical |
| **Deep-sleep recovery** | — | *"**hardware reset (IOE1 IO5) is required** to wake"* — new |
| **Bus speeds** | 100 kHz for PM1/IOE1 | *"PM1/IOE1 default 100 kHz (400 selectable); **touch/NFC at 400 kHz**"* — new |

**On the 20 vs 40 MHz panel-clock conflict** this record has tracked: `DESIGN.md`
says *"reference implementations are 20–40 MHz"* — acknowledging both without
resolving it. So the conflict is real and visible to third parties, not an
artifact of this project's reading.

## New findings from it

**M5GFX's waveform LUTs are FreeBSD-licensed and reusable.** `DESIGN.md` states
*"M5GFX's quality/text/fast/fastest LUTs are FreeBSD-licensed, so they can be
reused"*, and `src/ssd1677/lut.rs` is annotated as being taken from M5GFX under
that licence. That materially changes the
[libraries licensing picture](../../libraries/README.md): the e-paper
*driver* libraries skew copyleft, but **M5Stack's own waveform tables are
permissive**.

**A booster-parameter discrepancy.** `DESIGN.md` gives the SSD1677 init as
`0x0C AE C7 C3 C0 40`. This project's
[OTP-demo analysis](../../../devices/m5stack/papermono/features/epaper-display.md)
recorded `0x0C = {0xAE, 0xC7, 0xC3, 0xC0, 0x80}` — **the fifth byte differs,
`0x40` vs `0x80`**. One of the two is wrong, or they are from different sources.
**Unresolved**; worth checking against the OTP demo directly before either is
relied on.

**An internal contradiction in their own doc.** The IO list reads
*"… IO4 = NFC_EN … IO0(= P1?) = RTC INT, **IO4 = IMU INT**"* — assigning IO4
twice. This knowledge base's schematic extraction puts **RTC INT on M5PM1 G0 and
IMU INT on M5PM1 G4**, not on the expander. Their `IO4 = IMU INT` line is
probably an M5PM1/M5IOE1 mix-up — the exact `PYGn` ambiguity documented in
[`pin-naming-and-the-pyg-ambiguity.md`](../../../devices/m5stack/papermono/pin-naming-and-the-pyg-ambiguity.md),
appearing in the wild.

## What this changes

**NFC on the PaperMono is proven, not theoretical.** A working third-party
ST25R3916 driver with tag emulation exists. The
[radios assessment](radios-on-papermono.md) argued the hardware was reachable
from firmware source; this is the demonstration.

**Two independent implementations now confirm the expander/PMIC approach.**
`paper_name_plate` wrote its own `pm1.rs`/`ioe1.rs` rather than using the FreeInk
SDK — the same conclusion that assessment reached: the abstraction is optional.

**Rust is a viable path**, with `esp-hal 1.1.x` and `embedded-graphics 0.8`
handling this board.

**LoRa remains undemonstrated.** `paper_name_plate` lists the SX1262 pins and
explicitly scopes it out (*"out of scope for this project for now"*). No project
found anywhere drives LoRa on this board.


## Second sweep — 2026-09-11

Four days on, **two more projects**, one created the same day.

| Repository | Lang | Licence | Created | Pushed | What |
|---|---|---|---|---|---|
| **[`fperuzzo72/crossplay-papermono`](https://github.com/fperuzzo72/crossplay-papermono)** | C | MIT | **2026-09-11** | **2026-09-11** | **CrossPlay ported to the PaperMono** |
| [`Corvelis/m5-touch-card`](https://github.com/Corvelis/m5-touch-card) | C++ | MIT | 2026-09-07 | 2026-09-08 | **Second independent NFC project** — tap-to-exchange business cards |

### `crossplay-papermono` — the port is happening

Branch `papermono-bringup`, ~430 MB (a full CrossPlay tree), described as
*"CrossPlay no M5Stack Paper Mono: bring-up a partir de `ma-r-s/crossplay`"*.
Commits from 2026-09-11 are real bring-up, not scaffolding:

- *"papermono: give the render task the same 16384 stack the x4pro render task uses"*
- *"papermono: carry the stack flag into the release envs and build"*
- *"papermono: publish the release asset its updater asks for"*
- *"papermono: offer it on the Install button and in the install doc"*
- *"Point the update check at this fork's releases, not upstream's"*

That last commit is **exactly the seam CrossPlay's own `LOCAL_SCOPE.md` documents
as unavoidably fork-local** — the OTA URL, which if left pointing upstream would
flash a C3 image onto an S3. An independent porter hit it and fixed it the same
way, which is a small validation of that fork-portability analysis.

It is `fork: false`, `parent: null` — **detached**, the pattern that makes 9 of 14
named forks invisible to GitHub's `/forks` endpoint.

**This retires the "Class P" classification** applied to CrossPlay-on-PaperMono in
the earlier catalogue: support is no longer merely present in a build config,
someone is actively bringing it up.

### `m5-touch-card` — NFC, independently, again

*"PaperMonoとスタックチャンで、タッチして名刺交換。NFC対応ファームウェアとスマホ編集アプリ。"*
— tap-to-exchange business cards using the PaperMono and Stack-chan, with NFC
firmware **and a companion smartphone editing app**. Root layout (`firmware/`,
`mobile/`, `protocol/`, `migration/`, `release/`, `docs/`) is a finished product
rather than a demo, and it ships four embedded hardware demo videos. Recent work
includes *"Improve PaperMono idle sleep and minute/hourly display refresh"*.

### What the two sweeps together show

**NFC is the emergent killer application.** Three independent implementations now
exist — the vendor demo, `ciniml/paper_name_plate` (Rust) and
`Corvelis/m5-touch-card` (C++) — and the latter two converged, without contact,
on the same use case: *tap to exchange contact details*. For a device that is a
screen plus a tag emulator, that is the obvious product, and the market found it
within three weeks of launch.

**LoRa remains at zero.** Across three sweeps no project drives it. Every one
either scopes it out explicitly (`paper_name_plate`) or ignores it.

**Growth rate:** 43 repositories on 2026-09-01 → 5 new by 09-07 → 2 more by
09-11. Three weeks post-launch and still compounding.

## Method and limits

Searched the GitHub repository API for `papermono`, `paper+mono+esp32`,
`C153+m5stack`, `m5papermono`, sorted by `updated desc`. **Code search was not
used** and does not index forks, so quiet forks carrying real work remain
invisible. Chinese-language platforms (Gitee, Bilibili, CSDN) were **again not
searched** — still the largest known hole.

Nothing here was built, flashed or run. All source claims are `inferred` from
reading; the repository metadata is `executed-success`.

Commit SHAs at retrieval: `paper_name_plate` `7eac75dfc9`, `papermono-rs`
`67ee512024`, `M5PaperMonoLite` `dd97e91048`, `mono-note-mini` `ae84a34da7`.
