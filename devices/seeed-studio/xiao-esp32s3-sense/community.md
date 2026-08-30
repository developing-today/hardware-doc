# Community — XIAO ESP32S3 Sense

> Firsthand owner reports, gathered by searching directly rather than via the vendor's curated showcase.
> Snapshot **2026-08-24**. Raw data: [`artifacts/reddit-index.json`](artifacts/reddit-index.json) (115 posts), [`artifacts/reddit-threads.json`](artifacts/reddit-threads.json) (6 threads with comments).

## 1. How this differs from `projects-and-community.md`

[`projects-and-community.md`](projects-and-community.md) is built from Seeed's own showcase catalogue — **vendor-curated, promotional, and demonstrably containing at least one copy-paste error**. This page is direct community search: unfiltered, including complaints and failures.

The two give noticeably different pictures, which is the point.

### Retrieval note

`www.reddit.com/search.json` returns **HTTP 403** to every user agent tried (browser Chrome UA, WhatsApp, ChatGPT-User, ClaudeBot, curl). **`old.reddit.com/search.json` with the `WhatsApp/2.23.20.0` UA returns 200.** That fallback is what produced this data and is worth remembering.

## 2. Where the conversation happens

115 unique posts across three queries:

| Subreddit | Posts | Character |
|---|---:|---|
| **r/esp32** | 54 | General projects, build showcases, troubleshooting |
| **r/meshtastic** | 17 | **LoRa mesh nodes** |
| r/arduino | 6 | Beginner projects |
| r/Esphome | 4 | Home Assistant integration |
| r/homeassistant | 4 | idem |
| r/meshcore | 3 | LoRa mesh (alternative firmware) |
| r/Seeed_Studio | 3 | Vendor subreddit — notably quiet |
| r/PrintedCircuitBoard | 2 | Carrier-board design reviews |

## 3. The use case the vendor catalogue understates: LoRa mesh

**20 of 115 posts (r/meshtastic + r/meshcore) are about LoRa mesh networking** — pairing a XIAO ESP32S3 with the **Wio-SX1262** board to build Meshtastic/MeshCore nodes. Titles include *"My 1st Node — Seeed Xiao ESP32S3 Wio SX1262"*, *"Ordered a $10 XIAO ESP32S3 for Meshtastic & LoRa"*, *"Brass with XIAO ESP32S3 & Wio-SX1262 Kit"*.

This is the **second-largest application cluster after cameras**.

> **Correction to an earlier draft of this page.** I initially wrote that Seeed "barely documents" this. That is wrong, and the error came from searching only the *reference-design showcase PDF*. Seeed maintains **15 wiki pages** on XIAO + LoRa under `docs/Network/Meshtastic_Network/` and `docs/Network/LoRa_Wio_Series/`, covering Meshtastic, MeshCore, LoRaWAN gateways, a node-map application, MQTT bridging and a 3D-printed enclosure guide — plus a published [Wio-SX1262 schematic](https://files.seeedstudio.com/products/SenseCAP/Wio_SX1262/Schematic_Diagram_Wio-SX1262_for_XIAO.pdf) and module datasheet.
>
> The real gap is narrower: LoRa is under-represented in the **showcase catalogue** that [`projects-and-community.md`](projects-and-community.md) is built from, not in the wiki. A lesson about trusting one vendor document as a proxy for vendor coverage.

⚠ **Important for Sense owners: you cannot have both a camera and LoRa on one XIAO — and now we know exactly why.**

Seeed publishes the [Wio-SX1262 schematic](artifacts/accessories/wio-sx1262-for-xiao-v1.0-sch.pdf) (KiCad 8, dated 2024-09-19, retained locally). Parsing its net labels against the Sense daughterboard's B2B usage gives a complete collision:

| GPIO | Wio-SX1262 needs it for | Sense daughterboard already uses it for |
|---:|---|---|
| 14 | LoRa SPI / control | `DVP_Y6` |
| 15 | LoRa | `DVP_Y2` |
| 16 | LoRa | `DVP_Y5` |
| 17 | LoRa | `DVP_Y3` |
| 18 | LoRa | `DVP_Y4` |
| **21** | LoRa | **`USER_LED` / SD `CS`** |
| 47 | LoRa | `DVP_HREF` |
| 48 | LoRa | `DVP_Y9` |

**All 8 of the GPIOs the LoRa board requires are consumed by the camera board.** The two accessories are mutually exclusive by pin assignment, not by connector geometry — they both plug into the same 30-pin B2B and both claim the same signals.

That also clarifies the [Plus connector question](comparisons-and-recommendations.md#6-versus-the-xiao-esp32s3-plus--examined-from-the-schematics): the Wio-SX1262 works on the Plus because the Plus's J3 carries the same pins, and Seeed supports that combination. The camera board is a different matter.

**If LoRa is your goal, buy the plain XIAO ESP32S3 or the Plus and save the $6.50.**

## 4. Firsthand technical findings

These are **owner reports with reproduction detail** — stronger evidence than the showcase summaries, weaker than instrumented measurement.

### 4.1 The OV5640 upgrade has a fixed-pattern noise problem

Thread: [*"Noise and consistent lines on OV5640 camera with Seeed Studio ESP32S3 Sense"*](https://reddit.com/r/esp32/comments/1v3ctcx/noise_and_consistent_lines_on_ov5640_camera_with/) (r/esp32, 13 pts, 12 comments).

Original report: vertical lines that "sit in the same place shot to shot", worst in dark scenes, on an OV5640 powered from a 2000 mAh LiPo. Crucially:

> "**Did not experience the issue with the OV3660 the board came with by default.**"

A second owner independently confirmed the same symptom. Reported mitigations, in order of reported effectiveness:

| Mitigation | Reported effect | Evidence |
|---|---|---|
| **Lower `XCLK` from 20 MHz → 6 MHz** | "still present but **much less noticeable**" | firsthand, one reporter |
| Add 100 nF ceramics as close to the camera as possible | suggested | interpretation, untested |
| Heat sink and/or small fan | suggested; sensor believed to be overheating | firsthand thermal claim below |

**This materially supports the recommendation in [`market-and-pricing.md` §3](market-and-pricing.md#3-upgrading-to-the-ov5640) to skip the OV5640 upgrade** unless you specifically need autofocus. You pay 86 % of the board's price for a sensor with a reported dark-frame noise problem that the stock OV3660 does not exhibit.

Note the OV5640 datasheet's 6–27 MHz input clock range means 6 MHz is legal, not a hack — but it will cap frame rate.

### 4.2 A hard thermal datum

From the same thread:

> "Esp32s3 sense I have will run at **180 °F streaming video** out of it and that's in **open air**, not in a box. Highly recommend heat sink and tiny fan if you're putting in a box."

**180 °F ≈ 82 °C**, in open air, streaming video.

This is the only temperature figure located from an owner rather than the vendor. Compare Seeed's claim of **53.5 °C with dual heat sinks**. The two are not directly comparable (different sensor, cooling, workload, and an unstated measurement method), but 82 °C bare is consistent with Seeed selling heat sinks and with the OV5640's 140 mA draw.

> Evidence status: **single firsthand report, no stated instrument or measurement point.** Treat as an order-of-magnitude warning, not a specification. It is nonetheless the most useful thermal data point found, because [`performance.md`](performance.md) has nothing better.

**Practical consequence:** if you enclose this board — which most wearable and camera projects do — thermal design is a real requirement, not an optional extra.

### 4.3 There are no mounting holes

Thread: [*"Mounting Seeed Studio XIAO ESP32S3?"*](https://reddit.com/r/esp32/comments/1fztq73/mounting_seeed_studio_xiao_esp32s3/) (r/esp32, 23 pts, **39 comments** — the highest comment count on a purely practical question).

The board has **no screw holes, no clips, no mounting provision of any kind**. This surprises people and is a real design constraint that no spec sheet mentions.

Community solutions, in rough order of endorsement:

1. **Solder it directly to a custom carrier PCB** — the castellated pads run to the board edge specifically for this. Most endorsed by experienced posters; PCB MOQ is ~5 and cheap.
2. **Solder headers, plug into a XIAO-specific breakout/breadboard.**
3. **Hot glue** — endorsed unironically: "waterproof and nonconductive, and you'd be surprised how many low cost electronics use a dab of hot glue".
4. **3D-printed mounts** — e.g. [Thingiverse 5196253](https://www.thingiverse.com/thing:5196253), [5508504](https://www.thingiverse.com/thing:5508504).

This is by design: the XIAO is marketed as a **module** intended to be soldered into a larger board, not as a standalone dev board. Seeed publishes [KiCad footprints and symbols](artifacts/kicad/) for exactly this purpose.

### 4.4 A correction worth reading

Thread: *"How I revived a completely dead/bricked SenseCAP Solar Node (XIAO ESP32S3)"* (r/meshtastic, 118 pts).

The OP described reviving a dead node by **shorting the `RST` and `GND` solder pads with a paperclip** while USB was connected. Commenters corrected two factual errors — the node is **nRF52-based, not ESP32-S3**, and the cells are spring-loaded, not welded — and the OP acknowledged both.

Two lessons: the **reset-pad short is a real recovery technique** that the OP says works on these XIAO boards; and **a high-scoring post is not evidence** — this one was substantially wrong about the hardware and only the comments fixed it. Score correlates with presentation, not accuracy.

---

## 4A. Seeed's own forum — measured data the wiki does not have

Searched **2026-08-24** via the Discourse JSON API (`forum.seeedstudio.com/search.json?q=...`, plain browser UA, HTTP 200). 50 topics matched "XIAO ESP32S3 Sense". Three were read in full and retained at [`artifacts/seeed-forum-threads.json`](artifacts/seeed-forum-threads.json) — **118 posts**.

The forum turns out to be the **single most technically valuable community source for this board**, well above Reddit, because Seeed staff answer and owners post instrumented measurements.

### 4A.1 A vendor-confirmed schematic error

Thread [*"Error in XIAO ESP32S3 Sense Schematic?"*](https://forum.seeedstudio.com/t/273213) (7 posts).

`StuartsProjects` observed that the daughterboard schematic labels the camera `DVDD` rail on connector JA1 as **`VCC_1V8`**, while the regulator fitted is an **`SGM2036S-1.3`** — a **1.3 V** part. **Seeed staff confirmed the error:**

> "We are using SGM2036S-1.3XXDH4G/TR at U2, which outputs **1.3V**. The network label (**VCC_1V8**) on the schematic is **incorrect and should be changed to 1V3**. We will update the schematic as soon as possible."
> — `Seeed_Seraphina`, Seeed Studio

**The net name `VCC_1V8` in the schematic is wrong. The actual rail is 1.3 V.** The reporter also gives the camera's stated limits for that pin: min 1.24 V, typ 1.3 V, max 1.36 V — consistent with 1.3 V and *not* with 1.8 V.

This directly corrects [`sense-daughterboard.md`](sense-daughterboard.md), which reproduced the erroneous label from the netlist. Evidence: **vendor-confirmed**.

### 4A.2 Deep-sleep current — the vendor figures are unachievable, and here is why

Thread [*"Xiao esp32s3 sense camera sleep current"*](https://forum.seeedstudio.com/t/271258) — **74 posts**, running over years, with multiple owners using proper instrumentation (a Nordic PPK2 is mentioned).

This resolves the [three-way vendor contradiction](performance.md#the-deep-sleep-figures-are-not-achievable-once-the-camera-is-used--measured) in the most useful possible way: **none of Seeed's published figures are reachable once the camera has been used.**

Measured deep-sleep current after taking a picture, by sensor (`StuartsProjects`, same sketch, same board):

| Sensor | No register shutdown | **With register shutdown** |
|---|---:|---:|
| OV2640 | 22.3 mA | **22.3 mA** (no effect) |
| **OV3660** | 37.8 mA | **1.45 mA** |
| OV5640 | 104 mA | *(reported, value truncated in thread)* |

Other firsthand measurements from the thread:

| Condition | Current | Reporter |
|---|---:|---|
| Deep sleep, camera + SD fitted but **never initialised** | **~2.8 mA** | `StuartsProjects` |
| Deep sleep **after taking a picture and saving to SD** | **~90 mA** | `StuartsProjects`, `JaBa` |
| Deep sleep, ESPHome, **camera not configured** | **~140 µA** | `JaBa` |
| Deep sleep, ESPHome, **camera configured** | **~90 mA** | `JaBa` |
| **Light sleep**, board + camera + SD | **~4 mA** | `StuartsProjects` |
| Light sleep, bare XIAO ESP32S3 (no Sense board) | ~3 mA | `StuartsProjects` |
| Best achieved deep sleep, OV3660 + standby trick | **~1 mA / "just less than 1 mA"** | `jksemple` |
| CPU idle, camera active | ~34.7 mA (both `GRAB_LATEST` and `GRAB_WHEN_EMPTY`) | `StuartsProjects` |

**The gap between ~34 µA (wiki) and 1–90 mA (measured) is three orders of magnitude.** The mechanism is exactly the one documented in [`features/camera.md` §3.1](pinouts-and-buses.md#31-there-is-no-camera-power-down-or-reset-line--and-that-has-consequences): the camera cannot be powered down, so once initialised it keeps drawing current through deep sleep.

`jksemple` diagnosed it precisely, and independently reached the same conclusion as this research tree's schematic analysis:

> "The ESP32Cam provided hardware support to cut power to the OV2640 during deep sleep... **Seeedstudio did not provide any means in the Sense design to cut power nor to drive the POWERDWN pin** so there are no hardware [options]."

And on the residual draw even with the sensor in standby:

> "Looking at the datasheet for OV3660 the standby current is apparently **20 µA – 40 µA**, so I guess most of the additional power consumption in light sleep when using the Sense board is due to the **regulators, SD card and microphone**."

Seeed staff (`Seeed_Seraphina`) responded that the wiki figures are intended to "illustrate how much the actual impact on low power consumption can [be]" for different peripheral combinations — i.e. they are not a promise for a camera-initialised board.

### 4A.3 The workaround: software standby via a sensor register

The thread's most actionable output. `jksemple` and `StuartsProjects` independently confirm that writing an OV3660/OV5640 standby register before sleeping recovers most of the current:

```cpp
sensor_t *sensor = esp_camera_sensor_get();
sensor->set_reg(sensor, 0x3008, 0x40, 0x40);   // enter software standby
```

Reported effects:
- **OV3660 deep sleep: 37.8 mA → 1.45 mA** — a ~26× improvement.
- Active-mode draw drops from ~135 mA to ~50 mA when standby is asserted.
- **Confirmed working on OV3660**; the OV5640 register map appears the same, so it is expected to work there too.
- **No effect on OV2640** — its standby is a different mechanism (`set_reg_bits(sensor, BANK_SENSOR, COM2, 4, 1, enable)`), and multiple people report `SCCB_Write Failed addr:0x30` when trying it.

⚠ **Known defect:** `StuartsProjects` reports that **cancelling standby leaves the camera non-functional** — "if you then attempt to cancel standby mode the camera appears to stop wo[rking]". Since there is no `RESET` line, recovery needs a full power cycle. So this is usable for *wake → capture → standby → deep sleep → reset* cycles, but not for resuming a live camera.

Evidence: **firsthand measurement, two independent reporters, one hardware configuration.** Not reproduced here.

**This makes the OV3660 the correct sensor choice for battery projects by a wide margin** — the OV2640 cannot be put into standby at all, and the OV5640 draws the most. It reinforces the [OV5640 recommendation](market-and-pricing.md#3-upgrading-to-the-ov5640) from a second, independent direction.

### 4A.4 Other recurring forum themes

| Theme | Finding |
|---|---|
| **`while(!Serial);` bricks battery operation** | Extremely common. Sketches copied from tutorials block forever when USB is absent, so the board appears dead on battery. Remove the line |
| Camera + SD + TFT simultaneously | Multiple reports of conflicts — consistent with the [GPIO21 CS collision](features/microsd.md#4-the-chip-select-collision) |
| OV5640 autofocus | 35-post thread; AF firmware must be uploaded at runtime |
| `D2`/GPIO3 and R11 | `jksemple` independently spotted that `D2/SD_CS` is grouped with the SD signals but connected through **DNP R11** — corroborating [`sense-daughterboard.md` §5](sense-daughterboard.md#the-gpio3-vs-gpio21-contradiction-is-now-explained) |
| Custom I/O expander daughterboards | Users building sandwich boards that intercept B2B signals — the B2B pinout in this tree is exactly what that needs |

`while(!Serial);` deserves emphasis: it is probably the most common single cause of "my battery-powered XIAO does nothing", and it is a copied-tutorial artefact rather than a hardware fault.

## 5. Representative projects from direct search

Not in Seeed's catalogue:

| Project | Sub | Score |
|---|---|---:|
| Passwordless fingerprint unlocker | r/esp32 | 713 |
| ESP32-S3 selfie camera with round display, syncs to iPhone | r/esp32 | 295 |
| Autonomous rover controlled from a browser | r/esp32 | 254 |
| ePaper digital frame | r/esp32 | 148 |
| IMU + altimeter + SD custom carrier board | r/esp32 | 118 |
| XIAO ESP32S3 HaLow→WiFi bridge | r/esp32 | 31 |
| Working ESPHome camera YAML | r/Esphome | 12 |
| Retro camera recording AVI to SD | r/esp32 | 11 |

The **custom carrier board** and **HaLow bridge** posts reinforce §4.3: serious users treat this as a module to design around.

## 6. What the community complains about

Ranked by how often it appeared:

1. **Mounting** — no holes, no provision (39 comments on one thread).
2. **Camera image quality**, especially after the OV5640 upgrade.
3. **Thermals** under sustained streaming.
4. **Camera init failures** — consistently traced to PSRAM/partition settings, matching [`features/camera.md` §4](features/camera.md#4-why-esp_camera_init-fails).

Notably **absent** from complaints: the GPIO21 LED/SD collision and the JTAG conflict. That is not evidence they are unimportant — more likely that people hit them, fail to diagnose the cause, and post something vaguer. Both are documented here precisely because they are hard to self-diagnose.

## 7. Evidence limitations

- **Reddit and the Seeed forum** were searched (50 forum topics matched; 3 read in full). **Not** searched: Discord, Chinese-language platforms (Bilibili, Zhihu, Gitee), and the 210 references to `wiki-documents/discussions/69` in the wiki corpus.
- **115 posts is a sample, not a census.** Subreddit proportions describe *this sample*, not the community.
- Scores and comment counts measure engagement, not correctness — see §4.4.
- No claim here was reproduced on hardware.
- Prevalence language is avoided deliberately: "two independent reports among 115 posts reviewed" is what the OV5640 noise finding actually rests on.

## 8. Related
- [`projects-and-community.md`](projects-and-community.md) — the vendor-curated view
- [`performance.md`](performance.md) — where the 82 °C figure is carried forward
- [`compatibility-and-status.md`](compatibility-and-status.md) — working/failing reports by feature
- [`market-and-pricing.md`](market-and-pricing.md) — the OV5640 value question
