# DinMeter v1.1 — development

**The toolchain, board target, libraries, build/flash/monitor procedure and download-mode
sequence are identical to the DinMeter v1.0's.**
→ **[`../dinmeter/development.md`](../dinmeter/development.md)** is the full guide.

This page states only the v1.1 deltas, and the evidence that the rest is genuinely the same.

---

## 1. Do existing DinMeter builds run on v1.1? — **Yes, except one thing**

| Aspect | v1.1 | Basis |
|---|---|---|
| Target / toolchain | `esp32s3`, 8 MB flash, **no PSRAM** — unchanged | vendor spec; Bruce/Launcher `build_unflags = -DBOARD_HAS_PSRAM` |
| M5Unified board enum | `board_M5DinMeter` — **unchanged**; there is no v1.1 enum and no `board_M5StampS3A` at master `8530f5377d782e4a25a6c482de2e71c3f75ca8eb` | grep of `src/`, `executed-success` |
| `M5DinMeter` library | **1.0.0**, unchanged; no v1.1 release, no v1.1 code path | GitHub API, HEAD `8ccbad72…` |
| Display / encoder / button / buzzer / RTC / Grove / power hold | all unchanged | PinMap comparison + M5Unified source |
| Download mode | hold `G0` on the module while applying power — **identical wording on both Stamp pages** | vendor docs |
| Partition layout | unchanged (none published for either) | — |
| **RGB LED** | **needs `GPIO38 = HIGH` first, or it stays dark** | §2 |

**A binary built for v1.0 boots and runs on v1.1.** No recompilation is required. Nothing in the
build system needs to change.

## 2. The one change you must make — only if you use the RGB LED

```cpp
// Portable across v1.0 and v1.1. On v1.0 GPIO38 is unconnected on the carrier,
// so driving it is harmless.
pinMode(38, OUTPUT);
digitalWrite(38, HIGH);
delay(1);              // AW35122 typical rise 165 us
// ... then drive GPIO21 with your WS2812 library of choice
```
`not-tested`. Evidence chain:
[`stamp-s3-to-s3a-delta.md` §3](stamp-s3-to-s3a-delta.md#3-change-1--the-rgb-led-is-no-longer-always-powered-the-only-source-compatibility-break).

**Nothing else in any framework needs a change**, and no framework currently *makes* this change
for you.

## 3. Still true, and still the first thing to get right

Raise **GPIO46** in `setup()` or the board switches itself off on battery power the moment you
release the knob. `M5.begin()` does it via M5Unified's power-hold table
(`M5Unified.cpp:282`, `board_M5DinMeter → GPIO_NUM_46`). Bare ESP-IDF or bare Arduino: do it
yourself, first thing.

→ [`../dinmeter/development.md` §0](../dinmeter/development.md#0-the-one-thing-to-do-first)

## 4. Framework support status for v1.1 specifically

| Framework | v1.1 status | Note |
|---|---|---|
| Arduino + `M5DinMeter` 1.0.0 + M5Unified | **works**, except the RGB LED | no v1.1-specific release exists |
| ESP-IDF + `espressif/esp-board-manager` | `board_info.yaml` declares `version: 1.0.0` and was written against the v1.0 page; **nothing in it is wrong for v1.1** — every pin it models is unchanged | untested on v1.1 hardware |
| UiFlow2 | supported; the DinMeter target in `m5stack/uiflow-micropython` is not versioned by board revision | — |
| `bmorcelli/Launcher` | its `m5stack-dinmeter` target makes no revision distinction | ships as `Launcher-m5stack-dinmeter.bin` |
| PlatformIO | M5Stack's own factory project uses generic `esp32-s3-devkitc-1`; nothing revision-specific | — |

**No framework distinguishes v1.0 from v1.1 anywhere.** That is convenient and it is also
exactly why the RGB-LED change is a silent failure rather than a compile error.

## 5. Everything else

Versions, install commands, the Arduino FQBN caveat, the ESP-IDF route, the UiFlow2 relationship,
serial/USB/download-mode detail, and the bricking-and-power risk table are all in
**[`../dinmeter/development.md`](../dinmeter/development.md)** and apply verbatim.
