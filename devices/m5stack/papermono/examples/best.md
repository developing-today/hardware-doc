# PaperMono — selected examples

> Portfolio selected 2026-09-01 from the 43-entry population in
> [`catalog.json`](catalog.json). Population research is in
> [`../projects-and-community.md`](../projects-and-community.md); feature-to-evidence
> mapping is in [`../coverage.md`](../coverage.md).

> **Nothing here was built, flashed or run.** There is no PaperMono in this
> project. Every selection is a judgement from reading source and repository
> metadata — `inferred`, never `executed-success`. Build status for every entry
> in the catalogue is `not-built`.

**No example source is vendored.** The catalogue records canonical URLs, pinned
commit SHAs and immutable tree URLs instead. All 43 repositories resolved and
were pinned; none were gone or private.

## The portfolio

| # | Project | Commit | Licence | Why it is here |
|---|---|---|---|---|
| 1 | [`m5stack/M5PaperMono-UserDemo`](https://github.com/m5stack/M5PaperMono-UserDemo) | `c1099107` | MIT | The only artifact exercising **NFC, LoRa, IMU, RTC, PDM, buzzer, RGB and the M5PM1/M5IOE1 power path together** |
| 2 | [`m5stack/M5PaperMono-OTP-Demo`](https://github.com/m5stack/M5PaperMono-OTP-Demo) | `c7c02554` | MIT | Best e-paper diagnostic — drives the panel from built-in OTP waveforms |
| 3 | [`m5stack/M5PM1`](https://github.com/m5stack/M5PM1) | `be9a5456` | MIT | The register documentation for a custom chip that has none |
| 4 | [`m5stack/M5IOE1`](https://github.com/m5stack/M5IOE1) | `846eec7d` | MIT | Same; also the source of the `PIN_n` off-by-one trap |
| 5 | [`m5stack/M5GFX`](https://github.com/m5stack/M5GFX) | `d91077b9` | MIT | The shipped display path, board probe and OPI-PSRAM abort |
| 6 | [`m5stack/M5Unified`](https://github.com/m5stack/M5Unified) | `8530f537` | MIT | Defines `board_M5PaperMono`; cheapest route to a working build |
| 7 | [`crosspoint-reader/crosspoint-reader`](https://github.com/crosspoint-reader/crosspoint-reader) | `e6139861` | MIT | Best integrated third-party application shipping PaperMono support |
| 8 | [`Free-Ink/freeink-sdk`](https://github.com/Free-Ink/freeink-sdk) | `24003795` | MIT | Cleanest illustration of how a PaperMono port is structured |
| 9 | [`MagicCube/free-ink-on-paper-mono`](https://github.com/MagicCube/free-ink-on-paper-mono) | `34cc8794` | **none** | **Negative example — see below** |

Nine selected, plus one deliberate negative. Ten of 43.

## Why the negative example is here

`free-ink-on-paper-mono` demonstrates FreeInk running on this exact board and
carries an unmerged partial-refresh patch that is directly relevant to the
device's known refresh problems. It is also the single most tempting thing in
the population to copy from.

**It has no `LICENSE` file.** Absent an explicit grant, the code is
all-rights-reserved by default. Read it for technique; do not copy it. It is
selected precisely so that this is recorded rather than discovered later by
someone who has already pasted from it.

Nine other repositories in the catalogue likewise carry no detected licence —
`escape-hatch`, `m5stack-board-id`, `PaperMonoCalendar`, `learning-paper-mono`,
`buddy-watch`, `M5PaperMono-HomeAssistant-ESPHome`, `PaperMono`,
`claude-desktop-buddy`. One apparent case is **not** real: `esphome/esphome`
reports `NOASSERTION` because GitHub's detector cannot classify its split
GPLv3/custom licence. That distinction is recorded per-entry.

## Feature coverage, and what is not covered

| Feature | Covered by | Confidence |
|---|---|---|
| E-paper, waveforms, refresh | #2, #5, #9 | good — three independent implementations |
| Touch | #1, #5 | adequate |
| Power states, M5PM1 | #1, #3 | good |
| I/O expander | #1, #4 | good |
| NFC | **#1 only** | thin |
| LoRa | **#1 only** | thin |
| IMU, RTC, microSD, PDM, buzzer, RGB | #1, #6 | adequate |
| Wi-Fi / BLE | #7 | generic ESP32-S3, nothing board-specific |
| Frontlight | #1, #5 | adequate |

**NFC and LoRa rest on a single artifact each — the vendor's own demo.** There
is no independent implementation of either on this board. If that demo is wrong,
nothing in the population contradicts it, and this record inherits the error.
That is the most important limitation of the whole example survey.

## Slots the method asks for that could not be filled

Stated rather than padded:

- **No integrated application demonstrated on PaperMono hardware by an
  independent author.** `crosspoint-reader` ships support; whether it has been
  run on this board is not established here.
- **No performance or resource-limit example.** Nothing in the population
  measures refresh timing, current draw, memory pressure or concurrency.
- **No negative example of a *failure mode*** — the one negative entry is a
  licensing hazard, not a demonstrated technical failure.
- **No example exercising realistic feature combinations** (e-paper + microSD +
  Wi-Fi concurrently, or LoRa + Wi-Fi). See
  [`../resources-and-conflicts.md`](../resources-and-conflicts.md).

The population is days old — the device shipped 2026-08-21 and this snapshot is
2026-09-01 — so these gaps reflect the world, not the search.

## Reacquisition

```bash
# pinned clone of any selected example
git clone https://github.com/<owner>/<repo> && git -C <repo> checkout <commit>
```

Commits are in the table above and in every catalogue entry as `commit` /
`immutable_url`. See [`search-log.md`](search-log.md) for how the population was
found.
