# The factory "comprehensive example" apps

Retrieved **2026-08-21**. Source: Waveshare wiki [ESP32-S3-Knob-Touch-LCD-1.8](https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8), section 4 *"Comprehensive Example Usage Instructions"*, pinned at **revision 111069** (raw wikitext retained at `artifacts/source-snapshots/waveshare-wiki-wikitext-oldid-111069.txt`, lines 114-196). Re-fetched live 2026-08-23: the page is still revision 111069 and the body is byte-identical, so nothing below is stale.

Evidence markers used throughout this folder: **[SRC]** = stated by the vendor or present in shipped source; **[INF]** = inference from hardware ownership, not a vendor statement.

---

## 1. What the "comprehensive example" is

The board ships with a single large application already flashed — Waveshare calls it the *comprehensive example* (综合例程). It is **not** one of the eight numbered `01_ADC_Test` … `08_LVGL_Test` demos in the demo archive, and **Waveshare publishes no source for it.** Only the prebuilt binaries exist, in `ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip` and duplicated inside the demo ZIP under `Firmware/`.

> **[SRC]** "The product defaults to flashing a comprehensive example. If you accidentally erase the comprehensive example, you can refer to BIN File Flashing to restore it."

Restoring it is covered in [factory-firmware.md](factory-firmware.md). Because there is no source, **back the images up before overwriting either chip** — see [dual-MCU architecture](dual-mcu-architecture.md).

The comprehensive example spans **both MCUs**. The S3 image drives the launcher, the screen and everything file- or network-backed; the ESP32-U4WDH image provides the two Bluetooth Classic personalities. Which chip owns which app matters enormously if you intend to keep one app and replace the rest — see the ownership column in §3.

### Navigating the launcher

> **[SRC]** "Slide up from the bottom to bring up the control selection interface […] In Figure 1, you need to pay attention to the Type-C direction, and then slide up from the bottom to bring up the control selection interface. In Figure 2, click the red circle to close the control selection interface."

Two things are worth unpacking:

- **"Pay attention to the Type-C direction"** is not about flashing here — it is about *which way up the board is*. The stock UI is drawn in one fixed rotation, so "slide up from the bottom" only means anything once you know where the bottom is, and the USB-C port is the landmark. (Independently, `joshuacant/BlueKnob` rotates its whole UI 180° specifically so the USB-C port ends up at the *rear* while charging — see [examples/catalog.md](examples/catalog.md).)
- The gesture is a **bottom-edge swipe-up**, i.e. an Android-style app drawer. Individual apps then use left/right swipes and the knob.

---

## 2. Global setup you will need before most apps work

| Prerequisite | Detail | Which apps need it |
|---|---|---|
| **Wi-Fi provisioning** | The board raises an AP: **SSID `My Ap`, password `12345678`**. Join it, browse to **`192.168.4.1`**, and enter your real network's credentials. **[SRC]** | AIDA64 screen, Theme Clock (NTP) |
| **TF card** | A microSD is fitted from the factory and read over 4-bit SDMMC. Content lives in **fixed lower-case directory names** at the card root. | Music, MJPEG, Album, Text Reader |
| **3.5 mm output** | There is **no onboard speaker or amplifier.** Headphones or powered speakers must be plugged into the 3.5 mm jack. **[SRC]**, repeated by the wiki for three separate apps | Music, Bluetooth Music |

### TF card directory layout

The wiki documents **four** directories. An as-shipped card image published by a community member (see below) shows **nine**.

**Documented by Waveshare [SRC]:**

| Directory | Format the wiki demands | App |
|---|---|---|
| `music/` | MP3 | Music Player |
| `mjpeg/` | MJPEG, **360×360, 25 fps, quality 7** | MJPEG Player |
| `pic/` | JPEG, **360×360** | Picture Album |
| `txt/` | Plain text, **UTF-8 encoding mandatory** | Text Reader |

**Undocumented, present on the shipped card [SRC]** — from `nkinnan/manufacturer-firmware-and-sd-card-contents_Guition-K5-Knob-Series-JC3636K518` @ `cee5b94c63`, an as-shipped dump from the **Guition JC3636K518**, a near-identical clone whose firmware the author reports is the same application. Enumerated 2026-08-23 via the GitHub tree API. Full context in [examples/catalog.md §1.1](examples/catalog.md).

| Directory | Files | What it is |
|---|---:|---|
| **`weather/`** | 19 | `clear`, `sunny`, `partly_cloud[_night]`, `cloudy_day/night`, `rain[_night]`, `snow_day/night`, `thunderstorm_day/night`, `windy_day/night`, `fog_day/night`, `hot`, **`nowifi`** — all `.mjpeg`. **Evidence of a tenth app** — see §3.10 |
| **`aida64/`** | 18 | `001`–`017` plus `00_ff0000` — selectable backgrounds for the AIDA64 screen |
| **`clockbg/`** | 14 | Theme Clock backgrounds — this is where "**Theme** Clock" gets its name. Includes `ring_mask.bin`, `star_bg_360.bin`, `Oronys_ring_mask_360.bin` as raw pre-rendered blobs |
| **`night7/`** | 4 | `boot.mjpeg`, **`rhythmbg.mjpeg`**, `red_disk.bin`, `disk_mask_240.bin` |
| **`fonts/`** | 5 | `SYHT_16`, `SYHT_BOLD_16`, `SYST_BOLD_16`, `UI_FONT_16`, `EX_FONT_16` — **binary bitmap fonts** (SYHT = Source Han Sans, SYST = Source Han Serif) |

Three details from that dump worth carrying forward:

- **`txt/` holds a `.sav` alongside every `.txt`** (three of each). The Text Reader **persists reading position per file** — undocumented, and it means the card is written to, not just read.
- **`music/` contains a `.pcm`** alongside the MP3s. The player evidently also accepts raw PCM, which the wiki never mentions. (The official `07_Audio_Test` demo has a `PlaybackMusicmode` that "can directly play PCM-format audio", so the codepath exists.)
- **The fonts are off-chip binary assets.** This matters for §3.6: the UI's text is rendered from these blobs, not from ASCII string tables compiled into the firmware.

> ⚠️ **Provenance caveat.** This is a dump from the **Guition clone**, not from a Waveshare unit. The author's claim that the two run the same application is credible and matches the app set, but it is his assertion, not a verified equivalence. Treat the directory *names and roles* as strong evidence and the *exact file lists* as indicative. **[INF]**

These constraints are not cosmetic. The panel is 360×360, and the S3 has no video scaler — a differently-sized MJPEG or JPEG has to be resampled in software on a chip that is already spending most of its time pushing pixels over QSPI. Waveshare's answer is to require you to pre-size everything on the PC. Likewise the UTF-8 requirement means the text reader carries **one** decoder, not an encoding sniffer; a Windows-default CP1252 or GB2312 `.txt` will render as mojibake rather than fail loudly.

---

## 3. The apps

**Nine documented by the wiki, plus a tenth found on the shipped SD card.**

| # | App | Runs on | Primary hardware | Needs network | Needs TF card |
|---|---|---|---|:--:|:--:|
| 1 | AIDA64 Secondary Screen | **ESP32-S3** | Wi-Fi STA, LCD | yes | backgrounds only |
| 2 | Music Player | **ESP32-S3** | SDMMC, I2S→PCM5100A, knob 1, touch | no | yes |
| 3 | MJPEG Player | **ESP32-S3** | SDMMC, LCD, touch | no | yes |
| 4 | Picture Album | **ESP32-S3** | SDMMC, LCD, touch | no | yes |
| 5 | Theme Clock | **ESP32-S3** | Wi-Fi/NTP, knob 1, DRV2605L haptics | yes (for auto-set) | backgrounds only |
| 6 | **Spectrum Analyzer** | **ESP32-S3** | **PDM microphone**, LCD | no | background only |
| 7 | Bluetooth Music Player | **ESP32-U4WDH** (UI on S3) | BT Classic A2DP/AVRCP, I2S→DAC | no | no |
| 8 | Text Reader | **ESP32-S3** | SDMMC, LCD, knob 1 | no | yes |
| 9 | HID Volume Control | **ESP32-U4WDH** | BT Classic HID, knob | no | no |
| **10** | **Weather** — *undocumented, see §3.10* | **ESP32-S3** **[INF]** | Wi-Fi, LCD | yes | assets only |

MCU assignment is **[INF]** from the hardware-ownership table in [dual-mcu-architecture.md](dual-mcu-architecture.md), except where the app name itself gives it away: the two Bluetooth apps advertise **`TAIJI_KNOB_AUDIO`** and **`TAIJI_KNOB_HID`**, and `TAIJI_KNOB_32` is the ESP-IDF project name embedded in the ESP32-U4WDH factory image. That is direct corroboration that the secondary chip runs both.

---

### 3.1 AIDA64 Secondary Screen

Turns the knob into a desktop PC telemetry display. This is the most setup-heavy app on the board.

**What it does.** AIDA64 (commercial Windows system-monitoring software) has a "RemoteSensor" LCD backend that serves sensor values over HTTP. The knob joins your LAN, polls the PC, and renders the values.

**Setup, as the wiki gives it [SRC]:**

1. Download Waveshare's AIDA64 configuration file (see [wiki-resource-links.md](wiki-resource-links.md)) and install AIDA64 itself from [aida64.com](https://www.aida64.com/).
2. **File → Preferences → LCD → select `RemoteSensor`.**
3. **LCD Items → Import** the supplied configuration file.
   - > "There are 8 parameters in total. Everyone's computer configuration is different, so this needs to be configured according to actual conditions. Double-click to edit."
   - > "Show label cannot be modified, **Show unit must be filled with `^`**, otherwise the system will not recognize it."
4. Minimise AIDA64 (or set it to start on boot), then provision the knob's Wi-Fi via the `My Ap` / `12345678` → `192.168.4.1` flow. **"The AP must be on the same LAN as the computer."**
5. Browse to the knob's newly-acquired IP, scroll to **PC Monitor**, and enter the IP of the machine running AIDA64. **"If port 80 of the computer is already occupied, you need to add the port number."** Click Save.
6. > "If the display fails, it's worth checking if the computer firewall is restricting it. If it's due to the firewall, the simplest way is to disable the firewall for testing purposes."

**Commentary.** The `^` in "Show unit" is a delimiter, not a unit — it is how the firmware's parser finds field boundaries in AIDA64's flat text response. Get it wrong and the knob shows nothing with no diagnostic. Disabling your firewall wholesale (step 6) is poor advice for a device that then listens on your LAN; add a scoped inbound rule for the AIDA64 port instead.

**What is actually in the config file.** We extracted `Aida_remote_1.85.zip` (a valid 475-byte ZIP containing one CRLF text file, `aida_remote_1.85/aida_remote_1.85.rslcd`, declaring `<LCDVER>200</LCDVER><SWVER>6.33.5741 Beta</SWVER>`). The eight sensor IDs are **[SRC]**:

| Slot | AIDA64 sensor ID | Meaning |
|---|---|---|
| 1 | `SCPUUTI` | CPU utilisation |
| 2 | `SCPUCLK` | CPU clock |
| 3 | `TCPUPKG` | CPU package temperature |
| 4 | `FCPU` | CPU fan |
| 5 | `SGPU1UTI` | GPU utilisation |
| 6 | `SGPU1CLK` | GPU clock |
| 7 | `TGPU1DIO` | GPU diode temperature |
| 8 | `FGPU1` | GPU fan |

So the eight fields are a fixed CPU/GPU quad each. This also tells you what "configure according to actual conditions" means in practice: if your machine reports no CPU fan tacho, or you have no discrete GPU, slots 4/5/6/7/8 will be empty and you should re-point them at sensors you actually have.

---

### 3.2 Music Player

Local MP3 playback from the TF card.

> **[SRC]** "Turn the knob left first, and then you can play the music, in the process of playing music, you can turn the knob left or right to adjust the volume. External speakers or headphones are required to 3.5 mm headphone jack. Swipe left or right to switch songs. If you need to play your own songs, you can put the MP3 file into the `music` directory of the TF card."

| Control | Action |
|---|---|
| Knob left (initially) | Start playback |
| Knob left / right (during playback) | Volume down / up |
| Swipe left / right | Previous / next track |

**Commentary.** The "turn the knob left first" start gesture is genuinely unintuitive and is the single most common "my board is broken" report for this app. Note also that this app plays *local* files decoded **on the S3** and pushed out over the S3's I2S — a different audio path from app 7, which never touches the S3 at all. Both paths converge at the CH445P analog mux, and the DAC's `XSMT` mute line is owned by the *other* MCU (GPIO32, high = un-muted). If you reflash the ESP32-U4WDH with firmware that never raises `XSMT`, **this S3-side app goes silent too** and the cause is not on the chip you were working on. See [gaps-and-conflicts.md](gaps-and-conflicts.md).

---

### 3.3 MJPEG Player

> **[SRC]** "You can convert the video to a **360×360 MJPEG file with an FPS of 25 and a video quality of 7** through FFmpeg, and then put it into the `mjpeg` directory of the TF card. Swipe left or right to switch videos."

Waveshare ships a bundled converter rather than expecting you to drive FFmpeg yourself — see [§4](#4-the-mjpeg-conversion-tool) below.

**Commentary.** MJPEG (every frame an independent JPEG, no inter-frame prediction) is the pragmatic choice here: the S3 has JPEG decode capability and no H.264 block whatsoever, and seeking/frame-dropping is trivial when frames are independent. The cost is bitrate — "quality 7" in FFmpeg's `-q:v` scale is mid-range, and 25 fps of 360×360 JPEG is roughly 0.5–1.5 MB/s off the SD card, which is why this app wants the 4-bit SDMMC bus rather than SPI.

---

### 3.4 Picture Album

> **[SRC]** "You can put files in **360×360 JPEG** format into the `pic` directory of your TF card. Swipe left or right to switch pictures."

The simplest app on the board. Same sizing discipline as the MJPEG player and for the same reason.

---

### 3.5 Theme Clock

Clock plus a knob-set countdown timer with haptic completion.

> **[SRC]** "Rotate the knob to set the timer. Click on the screen to start timing, and **it will vibrate to indicate when it ends**."
>
> "Click **Offset** to set the time zone, set it by turning the knob, such as `+08:00` in China. After successfully connecting to the network, time will be automatically calibrated."

**Commentary.** This is the only stock app that uses the **DRV2605L haptic driver and LRA** for anything user-visible, which makes it the fastest way to confirm your haptics work without writing code. Time zone is a **raw UTC offset**, not an IANA zone name — so there is no DST database on board and you will have to re-set the offset twice a year if your locale observes it. "Automatically calibrated" means SNTP, which requires the Wi-Fi provisioning in §2.

---

### 3.6 Spectrum Analyzer — and the reconciliation

> **[SRC]** "Enter the **pickup spectrum analyzer** interface […] You can **capture the sounds around you** and display them on the screen in a spectral manner."

**This resolves an open question recorded in [dual-mcu-architecture.md](dual-mcu-architecture.md) §3.2 and its question 8.**

The prior finding was: *"Not confirmed to exist as a distinct app — no app URI or label string matching `spectrum`/`fft`/`vu` was found in the S3 image. It may be a display mode inside the music or Bluetooth app rather than a separate app. Cannot confirm from the evidence held."* A follow-on worry was recorded too: *if* it visualised Bluetooth audio, the S3 never sees those samples (they go through the analog mux), so amplitude data would have to be shipped over the inter-MCU UART.

The wiki settles both halves:

1. **The app exists**, as a distinct entry in the launcher with its own wiki subsection (4.2.6) and its own screenshot (`ESP32-S3-Knob-Touch-LCD-1.8-8.png`).
2. **It is fed by the microphone, not by Bluetooth audio.** The wiki's word is *"pickup"* (拾音, i.e. sound pickup) and the described behaviour is "capture the sounds around you". The PDM microphone is wired to the **ESP32-S3** (GPIO45/46).

**Therefore the inter-MCU-UART concern is void.** The Spectrum Analyzer is a purely S3-local app: PDM mic → I2S RX → FFT → LVGL. It requires nothing from the ESP32-U4WDH, sends nothing over the UART link, and does not visualise the Bluetooth audio stream. The "does it use the link?" answer for question 8 is **no**.

**Why the string search missed it.** The negative result was real and remains correctly reported — but it was evidence about *string tables*, not about *app existence*. **The as-shipped SD card supplies the mechanism:** the card carries a `fonts/` directory of **binary bitmap font blobs** (`SYHT_16`, `SYHT_BOLD_16`, `SYST_BOLD_16`, `UI_FONT_16`, `EX_FONT_16` — Source Han Sans/Serif, and the shipped `txt/` files are Chinese). **The UI renders its text from off-chip binary font assets, not from ASCII string tables compiled into the firmware image.** A scan of the S3 binary for `spectrum`/`fft`/`vu` was therefore looking in the wrong place entirely — for this UI, that search would fail for *every* app name, including ones we know exist. **[INF]**

**Independent corroboration that it is a first-class app.** The shipped card has a `night7/` directory containing **`rhythmbg.mjpeg`** — a "rhythm background" — alongside `boot.mjpeg`, `red_disk.bin` and `disk_mask_240.bin`. Every other app on the board with a visual theme has its own asset directory (`aida64/`, `clockbg/`, `weather/`). A dedicated rhythm/spectrum backdrop is what a distinct launcher entry looks like, not what a hidden display mode inside another app looks like. **[INF]**

**The lesson worth keeping:** absence of a string in a firmware image is weak evidence of absence of a feature, and it is *near-zero* evidence when the application renders text from external font assets — which is the normal LVGL pattern and demonstrably the case here. Vendor documentation outranks a negative string search. This entry should be treated as a **correction** to the earlier analysis, not as new information layered on top of it.

---

### 3.7 Bluetooth Music Player

Board acts as a Bluetooth **speaker** (A2DP sink) with metadata display.

> **[SRC]** "Connect your phone to the **`TAIJI_KNOB_AUDIO`** Bluetooth device. If your phone cannot scan or connect successfully, you can clear the recorded device […] and then try to reconnect. After pairing is successful, you can play songs using any music player software. **The interface can display song covers and lyrics**, and you can set this up through the music player software. The speaker or headphone need to be connected to the 3.5 mm headphone jack."

**Runs on the ESP32-U4WDH.** The ESP32-S3 has no Bluetooth Classic radio at all — this is a silicon omission, not a software gap — so A2DP cannot come from it. See [classic-bluetooth.md](classic-bluetooth.md).

**Commentary.** This is the one stock app that *demonstrably* exercises the inter-MCU UART. The audio itself does not cross the link (the U4WDH feeds the PCM5100A over its own I2S), but the **cover art and lyrics do**: they arrive at the U4WDH over AVRCP metadata, and the screen belongs to the S3. Album-art JPEGs and lyric text are small enough for a control-rate serial link — a few kB per track change — which is exactly the bandwidth envelope described in [dual-mcu-architecture.md §2](dual-mcu-architecture.md). Audio samples would not be; the arithmetic there rules that out even at the ESP32's 5 Mbaud ceiling.

The "clear the recorded device" advice is standard BR/EDR link-key hygiene: if the board's NVS and the phone's pairing store disagree about the link key, re-pairing fails silently until one side forgets.

---

### 3.8 Text Reader

> **[SRC]** "Open the txt file in Notepad and check the file encoding in the lower right corner. **If it is not UTF-8 encoding, you need to change it to UTF-8** encoding before placing it in the TF card `txt` directory. […] you can switch the text using the knob."

Knob scrolls/pages. See the encoding note in §2.

---

### 3.9 HID Volume Control

> **[SRC]** "Open Bluetooth on your computer or phone and click to pair with **`TAIJI_KNOB_HID`**. After successful pairing, you can control the volume of your computer or phone by rotating the knob. If pairing fails or if you cannot scan the HID Bluetooth, refer to the first point in the explanation for the Bluetooth Music Player."

**Runs on the ESP32-U4WDH** — same reasoning as 3.7, and the `TAIJI_KNOB_*` naming corroborates it. **[INF]**

**An unresolved detail:** *which* knob. The board has two, and each is readable only by its own MCU — knob 1 (`SW2`, GPIO8/7) by the S3, knob 2 (`SW1`, GPIO19/22) by the U4WDH. If the app reads knob 2 it is entirely self-contained on the secondary chip; if it reads knob 1 then rotation events must cross the UART from the S3. The wiki says only "the knob". **We cannot resolve this from the evidence held.** Worth noting that a self-contained implementation on knob 2 is the simpler design and the one the hardware seems laid out for. **[INF]**

Note that `TAIJI_KNOB_AUDIO` and `TAIJI_KNOB_HID` are advertised as **separate device names**, implying the secondary firmware presents a different profile set depending on which app the launcher has selected — another thing the S3 must be telling it over the UART.

---

### 3.10 Weather — an app the wiki never documents

**Absent from the wiki entirely**, but attested by *two independent lines of evidence*.

**Evidence 1 — firmware strings [FW].** The S3 factory image contains the HTTP endpoint **`/saveweather`** and the configuration fields **`CityCode`** and **`apikey`**, already recorded in [dual-mcu-architecture.md §3.2](dual-mcu-architecture.md). An API key plus a city code is the configuration surface of a **weather-service client**, and `/saveweather` is a settings-persistence route in the same web portal that provisions Wi-Fi.

**Evidence 2 — the shipped SD card [SRC].** A **`weather/`** directory of 19 MJPEG condition graphics:

`clear` · `sunny` · `partly_sunny` · `partly_cloud` · `partly_cloud_night` · `cloudy_day` · `cloudy_night` · `rain` · `rain_night` · `snow_day` · `snow_night` · `thunderstorm_day` · `thunderstorm_night` · `windy_day` · `windy_night` · `fog_day` · `fog_night` · `hot` · **`nowifi`**

**Why the assets settle it [INF]:**

- The set is a **complete weather-condition taxonomy** with systematic **day/night variants** — a lookup table keyed on a weather API's condition codes, not artwork.
- **`nowifi.mjpeg` is an error state.** Assets only ship an offline-fallback graphic for something that fetches over the network and can fail — exactly what `apikey` + `CityCode` imply.
- It sits at the same level as `aida64/` and `clockbg/`, both of which back confirmed launcher entries.

The two lines agree and neither depends on the other: the strings came from the **Waveshare** S3 binary, the assets from a **Guition clone's** card. **The comprehensive example includes a network weather display**, running on the **ESP32-S3** (the only chip with both Wi-Fi provisioning and the screen), reusing the same credentials as the AIDA64 screen and Theme Clock.

**What is still unknown:** which weather service (the `apikey` field implies a keyed API the user must supply — plausibly a Chinese provider, but no string identifies it), whether `CityCode` is set through the same `192.168.4.1` portal, and whether this is a standalone launcher entry or a face of the Theme Clock. The firmware groups the two together — `/clockbg` and `/saveweather` belong to one app in the string analysis — which mildly favours the latter. Recorded as open in [gaps-and-conflicts.md](gaps-and-conflicts.md).

**Practical note:** if you restore the factory firmware but reformat or replace the TF card using only the four directories the wiki documents, this app — along with the AIDA64, clock and spectrum backgrounds **and the UI fonts** — will be missing its assets. **Back up the shipped card before touching it.** The wiki never suggests the card is anything but user media storage. It is not: it is part of the application.

---

## 4. The MJPEG conversion tool

Waveshare distributes a wrapper GUI bundled with FFmpeg rather than documenting raw FFmpeg flags.

- **URL:** `https://files.waveshare.com/wiki/common/mjpeg%20Conversion%20tool%20V2.1.zip`
- **Local artifact:** `artifacts/tools/mjpeg_Conversion_tool_V2.1.zip` (81,719,210 bytes, validated ZIP)

Contents (verified 2026-08-23):

| File | Size | Note |
|---|---:|---|
| `ffmpeg.exe` | 60,993,536 | dated 2024-09-14 |
| `ffprobe.exe` | 45,051,904 | dated 2024-09-14 |
| `mjpeg…exe` + `.dll` + `.pdb` + `.deps.json` + `.runtimeconfig.json` | 106 MB dll | .NET wrapper GUI, dated 2024-07-29 |

**Windows-only**, and the wrapper's filenames are GB2312-encoded Chinese that renders as `mjpeg?++????.exe` under a UTF-8 locale. A `.pdb` (debug symbols) shipped in a release archive is sloppy but harmless.

**You do not need it.** The wiki states the target parameters explicitly, so plain FFmpeg on any platform does the same job:

~~~sh
ffmpeg -i input.mp4 \
       -vf "scale=360:360:force_original_aspect_ratio=increase,crop=360:360" \
       -c:v mjpeg -q:v 7 -r 25 -an \
       output.mjpeg
~~~

`-an` drops audio (the MJPEG player is video-only); the `scale`+`crop` pair centre-crops to square rather than distorting, which the vendor tool's behaviour is not documented well enough to confirm either way.

For the picture album, the equivalent is:

~~~sh
ffmpeg -i input.jpg -vf "scale=360:360:force_original_aspect_ratio=increase,crop=360:360" -q:v 3 out.jpg
~~~

---

## 5. What none of this tells you

Worth stating plainly, because the wiki's tone implies more openness than exists:

- **There is no source for any of these apps.** The wiki documents them as a *user manual*, not as example code. The eight numbered demos in the archive are unrelated peripheral tests.
- **The launcher's app-switching protocol over the inter-MCU UART is undocumented**, including its baud rate. See [dual-mcu-architecture.md §2.4](dual-mcu-architecture.md#24-the-protocol--what-is-known-and-what-is-not).
- A community mirror of the **clone board's** vendor source may be the closest thing to source for this UI that exists publicly — see the Guition JC3636K518 note in [examples/catalog.md](examples/catalog.md). We were unable to retrieve it; the reacquisition command is recorded there.

---

## Cross-references

- [dual-mcu-architecture.md](dual-mcu-architecture.md) — ownership, the UART link, the Spectrum Analyzer question this page closes
- [factory-firmware.md](factory-firmware.md) — restoring the comprehensive example
- [classic-bluetooth.md](classic-bluetooth.md) — why apps 7 and 9 need the secondary MCU
- [faq-and-troubleshooting.md](faq-and-troubleshooting.md) — vendor FAQ, including the USB-C orientation answer
- [wiki-resource-links.md](wiki-resource-links.md) — every downloadable the wiki references
- [examples/catalog.md](examples/catalog.md) — community projects
