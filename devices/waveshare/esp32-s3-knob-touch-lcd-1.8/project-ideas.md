# Project ideas — what this board can, can't, and shouldn't do

A realistic feasibility map for the Waveshare ESP32-S3-Knob-Touch-LCD-1.8.

Every entry names **the constraint that drives the verdict** and links to where that constraint is documented. The point is not to be discouraging — it is that this board has an unusual dual-MCU architecture whose limits are non-obvious, and knowing them up front is the difference between a weekend project and a month of fighting the hardware.

Implementation patterns for everything below live in [techniques.md](techniques.md).

---

## The five constraints that decide almost everything

Read these first. Nearly every verdict on this page reduces to one of them.

| # | Constraint | Consequence | Documented in |
|---|---|---|---|
| **C1** | **Inter-MCU UART bandwidth.** Two wires, no flow control, baud *unknown* and capped by the ESP32's ~5 Mbaud ceiling | Nothing resembling bulk data — least of all video — crosses between the two chips | [dual-mcu-architecture.md §2.3](dual-mcu-architecture.md#23-bandwidth--what-this-link-can-and-cannot-carry) |
| **C2** | **The S3 has no Classic Bluetooth.** Wi-Fi + BLE only; Classic BT lives on the U4WDH | Any A2DP/HFP/Classic-BT feature requires the second MCU and the link in C1 | [classic-bluetooth.md](classic-bluetooth.md) |
| **C3** | **The U4WDH has no OTA partition layout.** It updates only over USB-C serial | No field updates for the secondary MCU. A shipped product needs physical access | [dual-mcu-architecture.md §5](dual-mcu-architecture.md#5-ota-the-s3-can-the-u4wdh-cannot) |
| **C4** | **The secondary MCU idles at ~50 mA** and cannot be powered down by the S3 | It dominates battery life. Unused, it is pure drain | [examples/catalog.md §1.2](examples/catalog.md) |
| **C5** | **The display is S3-exclusive.** The U4WDH has no path to the panel | The chip that owns Classic BT cannot draw anything | [pinouts-and-buses.md](pinouts-and-buses.md#L147) |

Two lesser constraints recur often enough to name: **C6 — 8.3 filenames only** (`CONFIG_FATFS_LFN_NONE`) and **C7 — no card-detect line**. Both in [techniques.md §6.2](techniques.md#62-the-three-constraints-that-shape-sd-code-on-this-board).

### The arithmetic behind C1, because it settles a lot of arguments

```
One 360x360 frame, RGB565:   360 x 360 x 2 B  =  259,200 B  ≈  259 KB
30 fps:                      259,200 x 30     =  7.78 MB/s
UART 8N1 -> 10 bits/byte:    7.78 MB/s        =  77.8 Mbaud required

ESP32 practical UART ceiling:                    ~5 Mbaud  =  ~500 KB/s
Shortfall:                                       ~15x
```

Even **1 fps** of uncompressed full-screen video needs 259 KB/s — ~2.6 Mbaud — which is at best marginal on an unbuffered, flow-control-free link whose actual baud we have not yet measured. **Streaming video across the inter-MCU link is not a tuning problem; it is off by more than an order of magnitude.**

The corollary is the useful part: **the link is a control channel, not a data channel.** Design for it to carry track titles, volume levels, button events and state changes — tens of bytes — and put everything bulky on whichever side already has it.

---

## 1. Realistic — build these

### 1.1 Wi-Fi/BLE smart-home dial

A rotary controller for Home Assistant, Zigbee2MQTT, Hue, etc. The knob adjusts, the screen confirms, Wi-Fi carries the command.

**Why it fits:** entirely S3-side. No inter-MCU traffic (C1 irrelevant), no Classic BT (C2 irrelevant), display is S3-owned (C5 satisfied). Mains-powered, so C4 does not bite.

**Prior art:** ESPHome configurations already exist for this board and its Guition clone — see [examples/catalog.md §1.1](examples/catalog.md). `chris023/orion-waveshare-rotary-dial` and `muness/roon-knob` are working instances of exactly this shape.

**Watch:** knob spin rate — the vendor encoder driver tops out at ~30 events/sec ([techniques.md §3.1](techniques.md#31-it-is-not-a-quadrature-encoder)). Fine for volume, poor for fast scrolling until you move to hardware PCNT.

### 1.2 Local media/animation player from SD

MJPEG playback, slideshows, animated faces. The factory firmware does this already, from `mjpeg/` and `pic/`.

**Why it fits:** SD and display are both on the S3 — data never crosses the link, so C1 never applies. This is the key insight: **local** media is easy; **relayed** media is impossible.

**Watch:** C6 (8.3 names — `CLIP0001.MJP`, not `my-holiday-video.mjpeg`) and C7 (no card-detect, so poll-to-mount and never `format_if_mount_failed = true`). `0015/lvgl_kawaii_face` (MIT) is a clean starting point.

### 1.3 Standalone instrument / meter / dashboard

Gauges fed by Wi-Fi APIs or onboard ADC. `VolosR/Knob18Meters` is precisely this.

**Why it fits:** S3-only, low data rate, and the 360x360 round panel genuinely suits radial gauges. LVGL 8.4.0 arc widgets do most of the work.

### 1.4 Game / counter / timer devices

MTG life counters, pomodoro timers, dice. Two independent community implementations exist (`knobby-mtg`, `juggernautwins608` — the latter MIT-licensed).

**Why it fits:** no networking requirement at all, low frame rates, haptics available for tactile feedback.

**Watch:** fix the haptics first — stock code drives the LRA from an ERM waveform library and never calibrates ([techniques.md §4.1](techniques.md#41-two-separate-defects-in-the-vendor-path)).

### 1.5 Long-life battery device — *if* you sleep the secondary MCU

Any of the above, on battery, becomes viable once you flash the U4WDH a deep-sleep image: **~50 mA → ~10 µA**, a 5,000x cut ([C4](examples/catalog.md)).

**Why it fits:** the technique is proven independently by two projects (`svwhisper/lyngdorf-secondary-sleep`, `joshuacant/BlueKnob`).

**Watch:** this trades away Classic Bluetooth permanently-ish, and reflashing needs USB-C ([C3](dual-mcu-architecture.md#5-ota-the-s3-can-the-u4wdh-cannot)). **Back up the factory image first** — [dual-mcu-architecture.md §6.2](dual-mcu-architecture.md#62--back-up-the-factory-esp32-image-before-you-touch-it).

### 1.6 BLE peripheral — HID knob, media remote, custom GATT

A BLE volume knob, presenter clicker or macro dial.

**Why it fits:** BLE *is* on the S3, alongside the display. No link traffic, no C2 problem.

**Watch:** BLE HID is not the same as Classic BT HID. Some older hosts (and many car heads) accept only Classic — that lands you in §2.1.

---

## 2. Hard — possible, but budget real time for it

### 2.1 Classic-Bluetooth audio with on-screen metadata (the "Bluetooth speaker" project)

The obvious flagship project, and the one the board's own factory firmware implements. It is hard for a compounding set of reasons.

**The constraint stack:** Classic BT is U4WDH-only (C2), the display is S3-only (C5), so **every piece of now-playing metadata must cross the link** (C1) — and the audio path additionally requires *both* chips to cooperate, since the S3 owns the mux select and the U4WDH owns `XSMT` mute ([techniques.md §5.1](techniques.md#51-the-arbitration-you-cannot-avoid)).

**What makes it tractable:** metadata is small. Track title, artist, elapsed seconds and volume are tens of bytes at a few Hz — comfortably within C1. The factory firmware's pull-based `"Need packet:%d"` framing exists to do exactly this ([dual-mcu-architecture.md §2.4](dual-mcu-architecture.md#24-the-protocol--what-is-known-and-what-is-not)).

**What makes it hard:**
- **The link baud is unknown.** Measure it with a logic analyser before writing a line of protocol code. Do not assume 115200 ([techniques.md §7.2](techniques.md#72-the-link-itself)).
- **The protocol is only partly reverse-engineered.**
- **You likely need custom firmware on both chips**, and the U4WDH side has no public source and no OTA (C3).
- **Audio handover requires coordination** across the very link you are still characterising.

**Verdict:** very doable if you keep the stock U4WDH firmware and only speak its existing protocol. A large project if you replace both sides.

### 2.2 Fast, high-resolution knob input

Scrubbing a timeline, tuning a radio dial, anything wanting hundreds of counts/sec.

**Constraint:** the vendor's software polling ceiling of ~30 events/sec, and the fact that this is **not a quadrature encoder** — two independent switches, so every off-the-shelf quadrature decoder is useless ([techniques.md §3.1](techniques.md#31-it-is-not-a-quadrature-encoder)).

**Why it's merely hard, not impossible:** hardware PCNT is present and unused on both MCUs. Because the channels are independent closures, each can drive its own PCNT unit or GPIO ISR. Nobody appears to have published this yet — it is the most valuable unclaimed contribution on this board.

### 2.3 High-framerate full-screen animation

**Constraint:** not the link (all local) but memory and bus. QSPI at 40 MHz, two 25.9 KB DMA buffers in *internal* RAM, and the mandatory 2-pixel area rounding ([techniques.md §1.2](techniques.md#12-the-2-pixel-rounding-constraint--the-non-obvious-one)).

**Why it's hard:** a full 259 KB frame over 40 MHz QSPI has a hard floor around 52 ms of pure bus time before any rendering — so full-screen redraw caps out near 19 fps. Partial redraws are much faster; design the UI so most frames touch a small dirty region.

### 2.4 Shipping a product with field-updatable firmware

**Constraint:** C3. The S3 can OTA; the U4WDH cannot, having no OTA partition layout.

**Why it's hard:** if a bug lands in your U4WDH image, every unit needs physical USB-C access. The escape hatch — an S3-mediated serial bootloader for the secondary chip over the inter-MCU link — is sketched but **does not exist today** ([dual-mcu-architecture.md §5.5](dual-mcu-architecture.md#55-the-escape-hatch-you-could-build-does-not-exist-today)). Building it is a real project in itself.

**Mitigation:** design so the U4WDH runs stock or near-stock firmware and all your logic lives on the OTA-capable S3.

### 2.5 Reliable removable-media UX

**Constraint:** C7, no card-detect. You cannot know a card arrived or left.

**Why it's hard:** you must poll mounts and infer removal from I/O errors, and hot-removal during a write can corrupt the filesystem with no way to warn the user in advance. Combined with C6, user-supplied files also need 8.3-safe names.

---

## 3. Impossible — do not start these

### 3.1 Streaming video from the U4WDH to the display

**Constraint:** C1. ~7.78 MB/s needed at 30 fps against a ~500 KB/s ceiling — **~15x short**, and that is the theoretical maximum, not the measured link. Even 1 fps uncompressed is marginal.

**Documented:** [dual-mcu-architecture.md §2.3](dual-mcu-architecture.md#23-bandwidth--what-this-link-can-and-cannot-carry).

> No compression scheme rescues this. If the U4WDH is your video source, the architecture is wrong — put the source on the S3.

### 3.2 Classic Bluetooth on the ESP32-S3

**Constraint:** C2. The S3 silicon has no Classic BT radio. This is not a configuration option, a library gap, or something a future IDF release fixes.

**Documented:** [classic-bluetooth.md](classic-bluetooth.md).

> If you flash your own firmware to the S3 and expect A2DP, you will not get it. The board has Classic BT only because a second, older chip is on it.

### 3.3 Anything on the display driven by the U4WDH

**Constraint:** C5. There is no wire from the U4WDH to the panel. A "let the Bluetooth chip own the UI" design is unbuildable.

**Documented:** [pinouts-and-buses.md](pinouts-and-buses.md#L147), [dual-mcu-architecture.md §4](dual-mcu-architecture.md#4-who-owns-what--the-definitive-table).

### 3.4 Audio from one MCU acting alone

**Constraint:** split ownership — S3 owns the CH445P mux select (GPIO 0), U4WDH owns `XSMT` mute (its GPIO 32, wired directly to the DAC, no pull fitted).

**Documented:** [pinouts-and-buses.md §Audio arbitration](pinouts-and-buses.md#L125-L155).

> If you sleep the U4WDH for battery life (§1.5), check what it leaves `XSMT` at. Deep-sleeping the chip that owns your un-mute line can silence the DAC permanently. **This interaction is untested by us and is the sharpest trap on the board.**

### 3.5 Powering down the secondary MCU from the S3

**Constraint:** C4. It is permanently powered from `3V3` with no GPIO-controllable enable.

> The *only* lever is firmware — flash it a deep-sleep image (§1.5). There is no hardware kill switch, and no amount of S3-side code will find one.

### 3.6 True AMOLED per-pixel-brightness effects

**Constraint:** the panel has a **backlight** (PWM on GPIO 47), so it is not an AMOLED — which is also a principal argument that the controller is ST77916 rather than the AMOLED-driver SH8601 the code names.

**Documented:** [gaps-and-conflicts.md](gaps-and-conflicts.md#L29).

> "Black pixels cost no power" does not hold here. Budget backlight current as a constant.

---

## 4. Choosing an architecture — a short decision guide

```
Do you need Classic Bluetooth (A2DP / HFP / Classic HID)?
├─ NO  ──> Sleep the U4WDH (~50 mA -> ~10 uA). Build entirely on the S3.
│          This is the happy path. Sections 1.1-1.4, 1.6.
└─ YES ──> The U4WDH must stay awake and you inherit C1, C3 and C4.
           ├─ Metadata/control only across the link?  -> Hard but proven (§2.1)
           └─ Bulk data across the link?              -> Redesign. (§3.1)
```

**The one-sentence version:** *keep data on the chip that owns the peripheral, and let the inter-MCU link carry only control.*

---

## 5. Deliberately unassessed

Honesty about the edges of this map:

- **Concurrent Wi-Fi + BLE + heavy LVGL** on the S3 — plausible on paper, but we have not measured RAM headroom with the two 25.9 KB DMA buffers plus a Wi-Fi stack in place.
- **Actual sustained frame rates.** The ~19 fps figure in §2.3 is bus arithmetic, not a measurement.
- **Sleep-mode interaction with `XSMT`** (§3.4) — flagged as a risk, not tested.
- **Battery runtime figures.** The ~50 mA / ~10 µA numbers are community-reported ([C4](examples/catalog.md)); we have not reproduced them or characterised the S3's own draw.

---

## Related

- [techniques.md](techniques.md) — how to implement everything judged realistic here
- [dual-mcu-architecture.md](dual-mcu-architecture.md) — the constraint source for C1-C5
- [examples/catalog.md](examples/catalog.md) — 28 community projects; prior art for most of §1
- [gaps-and-conflicts.md](gaps-and-conflicts.md) — open questions that could move items between sections
- [getting-started.md](getting-started.md) — first build and flash
