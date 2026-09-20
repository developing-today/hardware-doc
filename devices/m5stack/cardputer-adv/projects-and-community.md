# Cardputer ADV — projects, firmware and community

> Snapshot **2026-09-04**. Discovery: `gh search repos cardputer --limit 100` (returned 100,
> the API cap — the true count is higher), targeted `gh search code` inside five named
> upstreams, and `old.reddit.com/search.json` with `User-Agent: WhatsApp/2.23.20.0`
> (`www.reddit.com` returns 403 to plain clients; `old.reddit.com` with that UA returns 200).
>
> **Evidence classes** are stated per project. "Supports ADV" means the repository contains a
> build target, a documented ADV path, or an explicit statement — not that this session flashed
> it. **No firmware was built or run by this session.** Everything below is
> `reported-working`, `documented` or `inferred`.

## 1. Why the ecosystem matters here

The Cardputer has an unusually large third-party firmware scene for a $30 board — larger than
its own vendor's software effort. `terremoth/awesome-m5stack-cardputer` (★734, GPL-3.0) and
`ru84r8/Cardputer-firmware-list` (★105) exist purely to index it, and there are at least three
dedicated subreddits (**r/CardPuter**, **r/CardPuterZero**, plus heavy traffic in r/M5Stack).

The 2026 pattern is stark: **new work targets the ADV.** Of the 100 repositories GitHub
returned, the ones created or renamed in 2026 overwhelmingly carry "ADV" in the name or
description. The v1.x is where the ecosystem grew up; the ADV is where it lives now.

## 2. The major firmwares

### 2.1 Bruce — `BruceDevices/firmware`

| | |
|---|---|
| URL | `https://github.com/BruceDevices/firmware` (**formerly `pr3y/Bruce`** — the old URL redirects) |
| HEAD at snapshot | **`1d555e0d5b201cc91ad201ac40c2482ec00d1ac1`**, 2026-08-28 |
| Stars / licence | ★6 642 · **AGPL-3.0** |
| Cardputer support | **v1.0, v1.1 and ADV from one build target** |
| Evidence | build config read at HEAD; `reported-working` by the wider community |

Bruce is the most important firmware on this platform and the cleanest demonstration that
one binary can serve both generations. `boards/m5stack-cardputer/m5stack-cardputer.ini`:

```ini
board = m5stack-cardputer
board_build.partitions = custom_8Mb.csv
-DTCA8418_INT_PIN=11  -DTCA8418_I2C_ADDR=0x34  -DTCA8418_SDA_PIN=8  -DTCA8418_SCL_PIN=9
-D ES8311_CODEC=1     -D ES8311_ADDR=0x18
-DMIC_SPM1423=1  -DPIN_CLK=43  -DPIN_DATA=46          ; the v1.x mic
-D SYS_I2C_SDA=-1 #8 on ADV Only
-D SYS_I2C_SCL=-1 #9 on ADV Only
lib_deps = adafruit/Adafruit TCA8418 @ ^1.0.2
```

Runtime detection, `boards/m5stack-cardputer/interface.cpp`:

```cpp
bool UseTCA8418 = false;              // line 12
Wire1.begin(TCA8418_SDA_PIN, TCA8418_SCL_PIN);
UseTCA8418 = tca.begin(TCA8418_I2C_ADDR, &Wire1);
if (!UseTCA8418) {
    Serial.println("ADV  : Failed to initialize TCA8418!");
    Serial.println("Probable standard Cardputer detected, switching to Keyboard library");
}
```

**Known issues, from reading the source:**

* Keyboard is **polled, not interrupt-driven** (`TCA8418_REPEAT_START_MS 350`,
  `TCA8418_REPEAT_MS 150`, ~100 ms poll). Perceptibly less responsive than the vendor library's
  interrupt path on held keys.
* Its ES8311 sequences at `interface.cpp:491-527` are copied verbatim from M5Unified,
  **including the register-`0x01` divergence** between the speaker (`0xB5`) and microphone
  (`0xBA`) paths. See [`features/audio.md`](features/audio.md) §6.1 — the defect has propagated.
* `-DLITE_VERSION=1` exists specifically "to limit some features to save space for M5Launcher
  Compatibility" — the 8 MB flash is a real constraint when chain-loading.
* Its build config declares CC1101, NRF24, W5500 and LoRa on the shared SPI bus with
  `SPI_SS_PIN = GROVE_SCL` (G1) for the v1.x path and dedicated ADV pins otherwise.

Build: `pio run -e m5stack-cardputer` — `not-tested` here.

### 2.2 Launcher — `bmorcelli/Launcher`

| | |
|---|---|
| URL | `https://github.com/bmorcelli/Launcher` (**formerly `bmorcelli/M5Stick-Launcher`**) |
| HEAD | **`3b91484efc5f1a392fac2c4d6066d8306409c688`**, 2026-09-04 |
| Stars / licence | ★2 054 · **MIT** |
| Cardputer support | v1.x and **ADV**, with a dedicated `boards/m5stack-cardputer/CardputerADV.md` |

Widely called **"M5Launcher"** by users; the repository name changed. It is a multi-firmware
boot menu — you keep several `.bin` images on the SD card and pick one at boot. That makes it
the de-facto entry point for people who want Bruce *and* Marauder *and* a game.

Its `CardputerADV.md` is a good short account of the port and states plainly:

> | Component | Original Cardputer | Cardputer ADV |
> | Keyboard Controller | Direct GPIO matrix | TCA8418 I2C controller |
> | I2C Address | N/A | 0x34 |
> | SDA/SCL/Interrupt | GPIO13 / GPIO15 / N/A | GPIO8 / GPIO9 / GPIO11 |
> **Matrix Size**: 7 rows × 8 columns · **Communication**: I2C polling only · 100 ms interval

That confirms the 7 × 8 matrix independently of M5Stack.

> ⚠ **Documentation error in that file, recorded:** it lists "**0x18**: Likely
> accelerometer/IMU" and "**0x69**: Likely additional sensor". They are inverted —
> `0x18` is the ES8311 codec, `0x69` is the BMI270 (the ADV schematic prints
> *"7-bit Address 69H"* beside the BMI270).

Companion: `CCP101/cardputer-recoverable-multiboot` (MIT) — "M5Launcher as factory entry,
combined with OTA application partitions", i.e. a partition scheme that keeps a recovery path.

### 2.3 Meshtastic — `meshtastic/firmware`

| | |
|---|---|
| HEAD | **`be2f68b5af806332c9d877d1643007771bd10c36`**, 2026-09-03 |
| Stars / licence | ★8 250 · **GPL-3.0** |
| Cardputer support | **ADV only** — env `m5stack-cardputer-adv`, `board_level = release` |

`variants/esp32s3/m5stack_cardputer_adv/` is a first-class upstream variant, not a fork. It
targets `board = m5stack-stamps3` with `default_8MB.csv`, `-DOLEDDISPLAY_REDUCE_MEMORY`, and
pins `meshtastic/st7789@92bae2e4`, `pschatzmann/arduino-audio-driver@v0.3.0`,
`meshtastic/ESP8266Audio@34302463`, `earlephilhower/ESP8266SAM@1.1.0`.

Its `variant.h` is an excellent independent pin reference and is quoted throughout this record —
notably `GPS_RX_PIN 15` / `GPS_TX_PIN 13`, `LORA_CS 5`, `LORA_RESET 3`, `LORA_DIO1 4`,
`SX126X_BUSY ← 6`, `KB_INT 11`, `I2C_SDA 8`/`I2C_SCL 9`, `I2C_SDA1 2`/`I2C_SCL1 1`, and
`#define I2C_NO_RESCAN`.

**There is no `m5stack_cardputer` (non-ADV) variant.** Meshtastic on a v1.x means a third-party
client, not upstream.

The **Cardputer Mesh Kit (K152)** is an *officially licensed* Meshtastic device with a
registration flow at `meshtastic-reg.m5stack.com`, and M5Stack states: *"Only devices in the
Cardputer Mesh Kit set can be registered. Other Cardputer/-Adv devices are not eligible."*
So an ADV + separately-bought Cap LoRa-1262 runs the firmware but cannot claim the badge.

### 2.4 Meshtastic clients and alternatives

| Project | Stars | Licence | Notes |
|---|---|---|---|
| `d4rkmen/plai` | ★175 | GPL-3.0 | *"Standalone Meshtastic node for CardPuter ADV"*. Announced r/CardPuter 2026-02-27 (↑153, 139 comments). u/Big-Bunch2804 (2026-08-05, firsthand): *"tested this on my cardputer adv … it works great! I also ran it yesterday with the lora cap and it automatically detected the lora cap and switched configurations. Did a couple test on LongFast and got acknowledged. Allows use of arrow keys unlike many other meshtastic firmware."* Same user, **2026-08-29**: *"The update today won't allow me to use directional arrows on adv anymore. Still won't save configurations when switching firmware."* |
| `Stachugit/MeshCore-Cardputer-ADV` | ★134 | MIT | MeshCore, not Meshtastic |
| `sosprz/meshcore-cardputer-adv` | ★69 | — | MeshCore client |
| `MultiMote/meshcore-cardputer-adv` | ★18 | MIT | *"Still in development 🚧"* |
| `ratspeak/rsCardputer` | ★53 | AGPL-3.0 | Reticulum/LXMF for ADV |
| `nonik0/CardputerLoRaChat` | ★121 | — | |

The unnamed r/CardPuter post of **2026-08-01** — *"Meshtastic client firmware for the Cardputer
ADV — full Unicode on 240x135 with no PSRAM, and no phone in the loop"* (↑47, 38 comments) —
contains the best single engineering account of the platform's memory constraint. Quoted in
[`resources-and-conflicts.md`](resources-and-conflicts.md) §4.

### 2.5 Evil-M5Project ("EvilCardputer") — `7h30th3r0n3/Evil-M5Project`

★2 570, **no licence file** (redistribution status `unknown`), last push 2026-08-20.
Wi-Fi auditing suite; the long-running community favourite on v1.x. Its description lists
"Cardputer, Atoms3, Fire, core2" and does **not** mention the ADV. Version 1.4.3 was announced
on r/CardPuter 2025-08-17 (↑330, 91 comments). **ADV support: not established.** A companion
content repo, `uagainshadow/Tons-of-LIVE-Public-CCTV-Cameras-for-the-Cardputer`, describes
adding an `evil/cctv` folder on the SD card.

### 2.6 ESP32Marauder — `justcallmekoko/ESP32Marauder`

★12 212, **no licence field returned by the API** (`none`), HEAD `91724fd8`, 2026-08-24.
`gh search code` finds **both** `User_Setup_marauder_m5cardputer.h` **and**
`User_Setup_marauder_m5cardputer_adv.h`, plus `installer/targets.json` and
`esp32_marauder/Keyboard.cpp` / `Keyboard_def.h`. So **ADV is a distinct supported target**.
It is an Arduino-IDE project, not PlatformIO — `platformio.ini` contains only `[env:native]`.

### 2.7 NEMO — `n0xa/m5stick-nemo`

★1 300, licence `NOASSERTION`, HEAD `0b8c5c73`, 2026-07-15. `configs/` contains exactly four
`.env` files: `M5Cardputer`, `M5StickC`, `M5StickCPlus`, `M5StickCPlus2`. The Cardputer one is:

```sh
export FQBN="m5stack:esp32:m5stack_cardputer"
export EXTRA_FLAGS="-DCARDPUTER"
export LIBRARIES="M5Cardputer IRRemoteESP8266 M5Stack-SD-Updater M5Unified"
```

**There is no ADV config.** However, because it builds against the `M5Cardputer` library, a
build using **library ≥ 1.1.1** would pick up board autodetect and the TCA8418 reader for free.
**Status: plausible but unverified.** Recorded as `inferred`, not `working`.

### 2.8 MicroHydra — `echo-lalia/MicroHydra`

★314, **GPL-3.0**, last push 2026-08-21. *"a simple, 'OS-like', MicroPython based app
switcher"*. The principal MicroPython route onto the platform; companion
`echo-lalia/Cardputer-Micropython-Examples` (★49, MIT). ADV support **not confirmed** from the
metadata available in this pass.

### 2.9 Picoware — `jblanked/Picoware`

★320, **GPL-3.0**, 2026-09-03. Description names **"PicoCalc, Cardputer ADV, Flipper Zero"** —
explicit ADV support, cross-device.

## 3. Emulators, games and "tiny OS"

| Project | Stars | Licence | Target |
|---|---|---|---|
| `geo-tp/Cardputer-Game-Station-Emulators` | ★240 | MIT | NES, SNES, GameBoy, GameGear, Master System, Megadrive, NeoGeo |
| `romalik/m5cardputer_doom` | ★82 | MIT | Doom |
| `matteofo/gb_cardputer` | ★71 | — | Peanut-GB port |
| `AndyAiCardputer/zx-spectrum-cardputer-external` / `-ili9341` | ★48 / ★26 | other | ZX Spectrum 48K on **external** ILI9488/ILI9341 via the CAP header |
| `question-and-answer/cave-mine-cardputer-alpha1` | ★22 | MIT | "true 3D voxel sandbox" for the ADV |
| `mindovermiles262/tamaputer` | ★25 | — | Tamagotchi, v1.x **and** ADV |
| `acpayers-alt/raising-hell-cardputer` | ★98 | MIT | virtual pet |
| `bomberman30/AdvanceOS-for-cardputer` | ★90 | MIT | ADV media playback OS |
| `engneer-hamachan/area512` | ★50 | MIT | **"Ruby & Python development environment for the 512KB M5Stack Cardputer"** — announced r/CardPuter 2026-07-03 (↑120) |
| `bryant24hao/ClawPuter` | ★149 | MIT | pixel desktop companion |
| `technoblogy/ulisp-cardputer` | ★27 | — | uLisp — a self-contained Lisp machine |
| `Kezii/Rust-M5Stack-Cardputer` | ★69 | GPL-3.0 | **Rust** HAL and examples |
| `shikarunochi/CardputerSimpleLaucher` | ★61 | MIT | simple launcher |
| `d4rkmen/M5Apps` | ★90 | MIT | *"Multi-app installer for M5 CardPuter v1.0, v1.1 and ADV"* — explicitly all three |

"Cardputer-Mario"-class platformers were **not** found under that name; the emulator collections
above are what the community actually uses to run 8/16-bit titles.

## 4. Audio and music — the 2026 surprise

A whole music scene appeared on the ADV in mid-2026, entirely because of the ES8311 and the jack.

| Project | Stars | Notes |
|---|---|---|
| `urtubia/miniacid` | ★105, MIT | *"An Acid style mini groovebox for the M5Stack Cardputer ADV"*. r/CardPuter 2026-07-13 (↑515, 44 comments) and r/synthdiy the same day (↑226): *"A $30 4-track acid groovebox … 303 voices, 808/909"* |
| `CHARL3X/GLIDE-Synth-Cardputer-ADV` | ★83 | *"a playable instrument with fretless-style glide"*. r/CardPuter 2026-06-28, ↑301 |
| "BKLVA Pocket DAW" | — | 0.2.20 announced 2026-07-30 (↑135), 0.3.4 on 2026-08-20 (↑100): *"Scenes, song chaining, Drum16, sampling and USB MIDI"*. Repository not located in this pass — **gap** |
| `AndyAiCardputer/mp3-player-winamp-cardputer-adv` | ★47 | *"with ES8311 audio codec support"* |
| `halbeshuhn/Cardputer-WebRadio`, `wusiu/WebRadio_WuSiU_Cardputer_Adv`, `cyberwisk/M5Cardputer_WebRadio` | ★16 / ★21 / ★129 | streaming |
| `sanchitminda/MP3PlayerForM5Cardputer` | ★47, GPL-3.0 | |
| "EMBER" MP3/FLAC/WAV player | — | r/CardPuter 2026-08-05, ↑47 |
| `wcheng95/Mini-FT8` | ★76, MIT | **FT8** digital-mode ham radio |

## 5. AI and LLM

| Project | Notes |
|---|---|
| `therezor/cardputer-ai` (★79) | *"Fully offline tiny LLM chatbot on the ESP32-S3 Cardputer ADV — 8M params, Q4"*. r/CardPuter 2026-06-12, ↑165. A genuine curiosity: an 8-million-parameter model on a no-PSRAM part. |
| `d4rkmen/M5Gemini` (★71), `shaahin/CardputerGPT` (★8), `FelipeLima2/M5CardputerAI` (★29), `vanshksingh/M5Cardputer-Chat-with-Gemini-API` (★58) | cloud-API clients |
| `dakshaymehta/cardputer-claude-os` (★202, Apache-2.0), `moremas/build-with-claude` (★196) | agent front-ends |
| `GOROman/LLMCardputer` (★63), `fwz233-RE/M5Claw` (★51) | |

## 6. Sensing, radio and instruments

`skizzophrenic/Cardputer-CSI-Human-Detector` (★207, MIT) and
`Zeloksa/Cardputer-ADV-CSI-Radar` (★100) do **Wi-Fi CSI** human/motion sensing — a research
technique running on a $30 handheld. `Jay-Jayismyname1/Cardputer-ABS-B-Radar` tracks aircraft;
`adammelancon/cardputer-satellite-tracker` (★58) and `wisnc/stellar-map` (★68, Stellarium-like)
and `nongxl/SkyCompass_CardputerADV` (celestial navigation off the Cap LoRa GNSS) point at the
sky. `lunarc3/CardputerGPSMap` (★27) and `geo-tp/M5Cardputer-GPS-Logger` (★37) use the GNSS.
`MatthewKuKanich/ChimeraBLE` (★220) does BLE reverse engineering. `geo-tp/MicroCOM` (★44) is a
serial terminal; `geo-tp/M5-Card-Computer-I2C-Scanner` (★23) an I²C scanner; several SSH clients
exist (`aat440hz/SSHClient-M5Cardputer` ★62, `MangoX0567/M5Stack-Cardputer-SSH` ★58 "for
Cardputer ADV", plus the vendor's own `examples/Advanced/SSHClient`).
`baget/esphome-m5cardputer` (★31, Apache-2.0) brings it into Home Assistant.
`nishad2m8/WLED-Cardputer` (★12, EUPL-1.2) drives WLED.

## 7. Hardware mods and CAP boards

* `Prokuon/CardputerADV_Cap_TFT-2.8` (★63) and `CardputerADV_Cap_TFT_V2` (★35) — community CAP
  display boards. The announcement (r/CardPuter, **2026-06-22**) hit **↑989 with 75 comments**,
  the highest-scoring Cardputer hardware post found.
* `guicmg/cardputer_adv_external_screen` (★71, MIT) — dual-screen guide.
* `JosephCGS/Cardputer-ADV-CC1101-NRF24L01-LoRa` (★39) — a DIY multi-radio CAP.
* `henriquesebastiao/external-cardputer-antenna` (★55, MIT).
* r/cyberDeck **2026-06-22**: *"Turning my Cardputer ADV into a mini Cyberdeck"* — ↑710.
* r/CardPuter **2026-07-09**: *"My first cardputer adv mod!"* — ↑213.
* "Cardputer XL mod with Schematik" — r/M5Stack 2026-08-07.

## 8. Forum and community evidence

**Subreddits.** r/CardPuter is the centre of gravity; r/CardPuterZero exists for the Linux
sibling; r/M5Stack carries vendor announcements and support traffic. Cross-posting to
r/cyberDeck, r/synthdiy, r/meshtastic and r/flipperzero is common.

Selected dated posts, with evidence type:

| Date | Sub | Post | Type |
|---|---|---|---|
| 2025-08-17 | r/CardPuter | Evil-Cardputer v1.4.3 release, ↑330/91 | project announcement |
| 2026-02-27 | r/CardPuter | Plai first beta, ↑153/**139 comments** | project announcement |
| 2026-03-11 | r/meshtastic | *"Any reason not to just get a Cardputer with lora cap for 55 bucks total even after ship?"*, 19 comments | purchase-decision thread |
| 2026-04-13 | r/CardPuter | *"What are some cool things you do with your Cardputer, specifically the ADV one?"* | owner discussion |
| 2026-05-31 | r/CardPuter | *"Guys I messed up big time"*, ↑39/**74 comments** — buyer torn between ADV and Zero. u/G33K_FISH: *"the ADV and the Zero are different. The Zero will be linux based. You can do things on the Zero you can not do on the ADV and vise versa."* u/Fluid-Fortune-432 (owns two ADVs): *"unless you're good with firmwares or coding your own stuff I'd cancel and wait for the zero."* | firsthand ownership opinion |
| 2026-06-22 | r/CardPuter | Cap TFT-2.8, **↑989/75** | hardware project |
| 2026-07-13 | r/CardPuter + r/synthdiy | miniacid groovebox, ↑515 + ↑226 | demonstrated project |
| 2026-08-01 | r/CardPuter | Meshtastic client, no-PSRAM Unicode font | **engineering account** |
| 2026-08-05 | r/M5Stack | *"Search for screws and buttons for the Cardputer ADV for repair"* — spares are hard to get; M5Stack sells a mixed M3 pack, buttons are 3D-printed | firsthand ownership problem |
| 2026-08-09 | r/CardPuter | *"What sd card does everybody use with their cardputer Adv?"* | open question, no vendor guidance |
| 2026-08-22 | r/M5Stack | *"Cardputer adv black screen only when turning it on"* — two replies, unresolved | **unresolved fault report** |
| 2026-08-29 | r/CardPuter | Plai regression: arrow keys stopped working on ADV | firsthand regression report |
| 2026-09-04 | r/M5Stack | *"which one should i get? m5stack cardputer adv or t embed c1101 plus?"* | active comparison shopping |

**Prevalence caveat.** These are individual reports from a reviewed sample of ~75 threads
returned by three Reddit searches on one day. They establish that an experience occurred. They
do **not** establish how common it is, and no claim in this record depends on frequency.

**M5Stack's own forum (`community.m5stack.com`) could not be searched.** Per
[`vendors/m5stack`](../../../vendors/m5stack/README.md) §5.3 its search API returns
`401 not-authorised` and `/search` redirects to login; only `/api/recent` is open. **A negative
result from the vendor forum is "no determination possible", not "nothing exists."**

Other channels: an official **Discord** (`discord.gg/ysQAWBUE9Q`), M5Stack's Hackster profile,
and `cardputer-dev/cardputer-site` (★16). No Hackaday article specific to the ADV was located in
this pass — recorded as a gap.

## 9. Compatibility summary for the ADV

| Firmware | ADV | v1.1 | v1.0 | Basis |
|---|---|---|---|---|
| M5Stack `M5Cardputer` ≥ 1.1.1 | ✅ | ✅ | ✅ | autodetect + reader injection |
| M5Stack factory UserDemo | ✅ (`CardputerADV` branch) | ✅ (`main`) | ✅ | separate branches |
| Bruce | ✅ runtime-detected | ✅ | ✅ | one build target |
| Launcher / "M5Launcher" | ✅ documented | ✅ | ✅ | `CardputerADV.md` |
| Meshtastic upstream | ✅ `m5stack-cardputer-adv` | ❌ no variant | ❌ | variants dir |
| Plai | ✅ ADV-only | ❌ | ❌ | description |
| MeshCore ports | ✅ ADV-only | ❌ | ❌ | descriptions |
| ESP32Marauder | ✅ `_adv` user setup | ✅ | ✅ | code search |
| Evil-M5Project | ❓ **not established** | ✅ | ✅ | description omits ADV |
| NEMO | ❓ **inferred only** | ✅ | ✅ | no ADV config; may work via library autodetect |
| MicroHydra | ❓ not confirmed | ✅ | ✅ | metadata only |
| Picoware | ✅ named | ❓ | ❓ | description |
| UiFlow2 | ✅ `/en/uiflow2/cardputer-adv/program` | ✅ `/en/uiflow2/cardputer/program` | ✅ | separate doc paths |

Full status matrix with caveats: [`compatibility-and-status.md`](compatibility-and-status.md).
