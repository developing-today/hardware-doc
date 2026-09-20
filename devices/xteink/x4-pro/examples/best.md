# Xteink X4 Pro — selected examples

Snapshot **2026-09-04**. **None was built, flashed or run.** Statuses are
`inferred` from source and repository metadata unless marked otherwise.

## Why this portfolio looks unusual

There is **no vendor SDK and no vendor sample code** for any Xteink device. The
corpus is complete e-reader applications rather than per-feature demos, so this
selection covers each **hardware path** by naming the project that best exercises
it — plus the one project that is genuinely a minimal starting point, and two
**negative examples** that document real failures.

## The portfolio

### 1. Best starting point — [`Free-Ink/freeink-sdk`](https://github.com/Free-Ink/freeink-sdk) @ `2400379`

**Not an application — the HAL.** It is the correct first read for any X4 Pro work
and the source of every hardware fact in this device record.

Covers: display + three-controller auto-detect · GT911 touch · frontlight ·
SDMMC · CW2017 · BM8563 · buttons · power rails · sleep.

Why selected: `[env:x4pro]` exists and is maintained; `docs/xteink-x4pro-support.md`
distinguishes **Confirmed on hardware / Corrected / Pending** per claim, which is
rarer and more valuable than the code itself.

Pitfall: it is a **submodule**, not a package. Consumers must also define
`USE_BLOCK_DEVICE_INTERFACE=1` for SD.

### 2. Best minimal consumer — [`Free-Ink/freeink-reader`](https://github.com/Free-Ink/freeink-reader)

MIT · *"Minimal e-reader using the FreeInk SDK"* · last push 2026-07-08.

The smallest thing that is a real application. Use it to see the SDK's
initialisation contract without CrossPoint's 3,000-commit surface area.

Caveat: **less actively maintained** than the mainlines, and no X4 Pro-specific
claim is made.

### 3. Best integrated application — [`crosspoint-reader/crosspoint-reader`](https://github.com/crosspoint-reader/crosspoint-reader)

MIT · the reference implementation · `ROADMAP.md:40` lists X4 Pro among
*"ESP32-S3 class hardware"* targets.

Exercises every fitted capability in one program. Its **1.5 release notes** are
also the best statement of the ecosystem's brick risks.

### 4. Best distinct approach — [`uxjulia/CrossInk`](https://github.com/uxjulia/CrossInk)

MIT · added an `x4pro` device type to its bug-report template on 2026-08-18 ·
ships an **SDL simulator** ([`crossink-simulator`](https://github.com/uxjulia/crossink-simulator)).

An independent lineage rather than a CrossPoint fork. **The simulator is the only
way to exercise UI code in this ecosystem without hardware** — directly relevant
here, where no hardware was available.

### 5. Best X4 Pro-specific work — [`goodyttoor/inkback-freeink-sdk`](https://github.com/goodyttoor/inkback-freeink-sdk)

MIT · *"InkMotion (PSRAM multi-buffer, damage windows, ghost budget) and **X4 Pro
display work**"* · push 2026-08-18.

The only project found that targets what actually distinguishes this device from
the C3 models: **8 MB PSRAM**. Multi-buffering, damage windows and ghost budgeting
are impossible on an X4/X3.

### 6. Best fork-maintenance study — [`ma-r-s/crossplay`](https://github.com/ma-r-s/crossplay)

MIT · [full record in this knowledge base](../../../../software/applications/crossplay/README.md).

Selected for its `LOCAL_SCOPE.md`: an explicit, maintained accounting of every
upstream file it touches and why. It names the **X4 Pro as the design floor**
("two side keys plus touch") and documents the
**C3-image-onto-S3 OTA hazard**.

### 7. Non-reader use — [`vjFaLk/esphome-xteink`](https://github.com/vjFaLk/esphome-xteink)

MIT · wraps the whole FreeInk SDK as an **ESPHome external component** under
`components/xteink/sdk/`, for X4 / X3 / **X4 Pro**.

The clearest demonstration that this is a general ESP32-S3 e-paper platform, not
only a reader.

### 8. From-scratch alternative — [`thepropm/proink-os`](https://github.com/thepropm/proink-os)

*"a from-scratch e-reader firmware for the Xteink X4 Pro, built on the FreeInk
SDK"* · push **2026-09-04** — the most recently active X4 Pro-specific project.

Also relevant: [`MrStu82/crosspoint-llama-pro`](https://github.com/MrStu82/crosspoint-llama-pro),
whose description independently corroborates the hardware profile —
*"ESP32-S3, GT911 touch, dual warm/cold frontlight"*.

### 9. **Negative example** — [`togotago/xteink-x4-escape`](https://github.com/togotago/xteink-x4-escape)

MIT · *"Escape recipe for Xteink X4 e-readers stuck on CrossPoint Reader 1.2.0
with OTA failing at `esp_ota_end()`"*.

**A named, reproducible brick and its cure.** For the X4, not the Pro — but the
OTA path is shared, and it is the only documented recovery recipe in the ecosystem.

### 10. **Negative example** — [`lvturner/x4-dual-boot`](https://github.com/lvturner/x4-dual-boot)

*"MicroSlate + CrossInk dual-boot for a **USB-locked** Xteink X4 (SD-card
install)"*.

Documents working around the factory USB lock — the constraint that shapes every
first-time flashing experience in this family.

### 11. Backup tooling — [`HomeAssistantPi/xteink-backup-utility`](https://github.com/HomeAssistantPi/xteink-backup-utility)

MIT · *"Flash and Storage Utility for XTEINK / ESP32-S3. **Built for my XTEINK 4
PRO**."* — the only X4 Pro-specific flash tool located. **Not inspected in depth.**

## Feature coverage of the portfolio

| Capability | Covered by | Gap |
|---|---|---|
| Display + 3-controller detect | 1, 3, 5 | — |
| GT911 touch + Home key | 1, 3, 4 | — |
| Frontlight warm/cool | 1, 3 | — |
| Buttons | 1, 3 | — |
| SDMMC | 1, 3 | — |
| CW2017 battery | 1, 3 | — |
| BM8563 RTC | 1, 3 | — |
| Wi-Fi / BLE | 3, 7 | — |
| **PSRAM multi-buffering** | **5 only** | — |
| **USB-MSC** | **none** | **Uncovered.** In stock firmware, not ported to the SDK |
| Deep-sleep power | 1 (implemented, unmeasured) | **No power figure exists** |
| Flash / recovery | 9, 10, 11 | — |

**Two genuine gaps: USB-MSC has no example anywhere, and no example demonstrates
or measures sleep power.**

## Nothing was vendored

No example source is copied into this repository. Reasons: none is small enough to
be a snippet; all are actively developed and a stale copy would mislead; and all
are one `git clone` away at a pinned commit. Only the FreeInk SDK is held locally,
in `scratch/eink-software/repos/freeink-sdk` at commit
`24003795381a6c23630a26472ae3b06550333e71`, fetched by an earlier session.

## Not validated

**No example was built or statically validated.** No toolchain was installed. The
honest status of every entry is `inferred`.
