# Projects and community — Cap LoRa-1262 (U214)

Sample: **217 unique Reddit posts** across r/CardPuter, r/M5Stack, r/meshtastic, r/Lora,
r/meshcore and adjacent subs, dated **2025-09-04 → 2026-09-04**, plus 13 GitHub repositories.
Prevalence statements below are scoped to that sample and no wider.

## 1. Firmware projects that use this Cap

| Project | Author | Stars | Last push | What it is |
|---|---|---|---|---|
| [`meshtastic/firmware`](https://github.com/meshtastic/firmware) | Meshtastic | — | current | **Upstream official support**, board `m5stack-cardputer-adv` |
| [`d4rkmen/plai`](https://github.com/d4rkmen/plai) | d4rkmen | **175** | 2026-07-27 | *"Standalone Meshtastic node for CardPuter ADV"* — written because *"the MT firmware is a disaster: on esp32 wifi is unusable … on esp32-s3 same story with bluetooth"* ([2026-02-15](https://old.reddit.com/r/CardPuter/comments/1r4waav/)) |
| [`anton-vinogradov/meshtastic-adv`](https://github.com/anton-vinogradov/meshtastic-adv) | anton-vinogradov | 24 | 2026-08-30 | *"Keyboard-first Meshtastic client for the M5Stack Cardputer ADV — own Cap LoRa-1262 or any…"*. Full Unicode on 240×135 with no PSRAM; companion mode drives any stock Meshtastic node over BLE |
| [`RaymiiOrg/MeshCompromise`](https://github.com/RaymiiOrg/MeshCompromise) | RaymiiOrg | 3 | 2026-08-19 | **Meshtastic + MeshCore in one firmware** on Cardputer-Adv |
| [`TenoTrash/PoisonMesh`](https://github.com/TenoTrash/PoisonMesh) | TenoTrash | 7 | 2026-06-23 | Meshtastic-network pentesting tool for Cardputer-Adv |
| [`baltamir1978/fantashtic`](https://github.com/baltamir1978/fantashtic) | baltamir1978 | 0 | 2026-08-15 | *"Firmware de mensajeria LoRa privada para M5Stack Cardputer Adv + Cap LoRa-1262"* — private (non-Meshtastic) LoRa messaging |
| [`yuiseki/m5-cardputer-meshtastic-map`](https://github.com/yuiseki/m5-cardputer-meshtastic-map) | yuiseki | 0 | 2026-08-23 | Meshtastic **plus an offline planet-scale vector map** on one Cardputer-Adv |
| [`SweetSourFox/meshtastic-meteo`](https://github.com/SweetSourFox/meshtastic-meteo) | SweetSourFox | 1 | 2026-08-17 | Meshtastic 2.7.22 + weather sensors (BME688/SCD41) |
| [`hansgao0422/Meshtastic-CardputerADV-CN`](https://github.com/hansgao0422/Meshtastic-CardputerADV-CN), [`ce021711/cardputer-adv-meshtastic-cn`](https://github.com/ce021711/cardputer-adv-meshtastic-cn) | — | 8 / 0 | 2026-07/08 | Chinese localisation + IME |
| [`MrOlim7/Meshtastic-CZ`](https://github.com/MrOlim7/Meshtastic-CZ) | MrOlim7 | 1 | 2026-05-25 | *"Meshtastic for Cardputer **Zero**"* — evidence the Zero path is real |
| **MeshCore-Cardputer-ADV** | truthfly et al. | — | v1.1.0, 2026-01-27 | Announced across three subs; **104 upvotes / 42 comments** in r/CardPuter, 44/22 in r/meshcore |
| **Bruce**, **M5Launcher**, **WhisperOS**, **Porkchop** | community | — | — | General-purpose Cardputer firmwares that expose the Cap |

### For the *original* Cardputer, not this Cap

| Project | Note |
|---|---|
| [`sigil-03/cardputer-meshtastic-client`](https://github.com/sigil-03/cardputer-meshtastic-client) | *"cursed meshtastic client for the M5 Cardputer"*, 5 stars, last push **2025-02-05** — a BLE **client** for an external node, not an on-board radio |
| [`reydeargentina/cardtastic`](https://github.com/reydeargentina/cardtastic) | *"simple, fast UI for Meshtastic nodes running on the M5Stack Cardputer v1.1"*, 2026-02-09 |
| [`jeroavf/Cardkb_emulator`](https://github.com/jeroavf/Cardkb_emulator) | Turns a Cardputer into an I²C CardKB keyboard **for** a Heltec/other Meshtastic node — the honest workaround for a host with no LoRa |
| **MeshClient** | *"MeshClient Firmware for CardPuter & CardPuter ADV"*, [2025-11-11](https://old.reddit.com/r/CardPuter/comments/1ouceka/); later *"MeshClient supports on MeshCore & Meshtastic"* [2025-12-16](https://old.reddit.com/r/CardPuter/comments/1pogcwg/) |

## 2. Community timeline

| Date | Event |
|---|---|
| **2025-09-04** | *"Cardputer adv and lora module info sheet"* (66 pts) — first sighting, sourced from `x.com/M5Stack/status/1963562345785098345`. In the comments: *"Can other versions of Cardputers make use of the Caplora?"* → **"No, not enough gpio pins"** |
| 2025-09-06 | M5Stack's own Cardputer-Adv announcement (45 pts); *"CardPuter free text to New CardPuter ADV by Meshtastic?"* (91 pts, 16 comments) |
| **2025-09-08** | *"Cardputer ADV Hacker cap (CC1101 SubGHz & ST25R3916 RFID) expected release"* — an owner emailed M5Stack and was told **"3–4 months, either December or January"**. It actually shipped **2026-08-28**, ~11 months later |
| 2025-09-09 | *"is it possible to port meshtastic firmware for cardputer adv to cardputer 1.0?"* — answered no: the ADV moved the keyboard to I²C, freeing the GPIO |
| **2025-09-15** | *"Got my Cardputer ADV and Lora Cap"* — **156 pts**, the U201 arrival wave |
| 2025-09-19 | *"Cardputer adv up and running with Lora cap on US915"* — first documented US915 use, via SMA adapters |
| 2025-11-11 → 12-16 | MeshClient firmware releases |
| **2025-12-30** | **U214 launch**, announced in r/M5Stack (56 pts) and r/CardPuter (40 pts) |
| 2026-01-13 | **MeshCore-Cardputer-ADV** lands (82/33/44 pts across three subs) |
| 2026-01-27 | MeshCore v1.1.0 (104 pts, 42 comments) — the single biggest Cardputer-mesh thread in the sample |
| 2026-02-11/12 | *"I turned my M5Cardputer into a standalone LoRa & GPS Field Tester"* + open-source release |
| 2026-02-15 | u/thetestbug points at **PR #9540** as the coming official support |
| **2026-03-11** | Meshtastic **2.7.20** ships the variant |
| 2026-04-30 | **Cardputer Mesh Kit** launches |
| **2026-05-23** | Meshtastic **2.7.24** — antenna-switch fix |
| 2026-07-05 → 08-01 | anton-vinogradov's keyboard-first client (15/54/44 pts across three posts) |
| 2026-07-18 | *"Case for Cardputer+LoRa Cap (WiP)"* — **139 pts**; released on Printables 2026-07-18 (69 pts). 3D-printed cases are the most-upvoted Cap content in the sample |
| **2026-08-28** | **Cap CC1101 & NFC** launches (41 pts, 16 comments) |

## 3. What owners actually build

Demonstrated (code or photos exist): Meshtastic/MeshCore nodes; a **standalone LoRa & GPS
field tester**; **offline vector maps** driven by the Cap's GNSS; a private LoRa messaging
firmware; mesh pentesting; weather telemetry over mesh; several 3D-printed cases.

Proposed but not demonstrated in the sample: LoRaWAN of any kind; a **LoRa + GPS game**
([r/CardPuter 2026-07-20](https://old.reddit.com/r/CardPuter/comments/1v1u7ce/), 10 pts —
ideas only).

## 4. The recurring complaints, in order of frequency in the sample

1. **Antenna band/connector.** 868 whip shipped worldwide; adapters needed. §Market.
2. **Battery reporting.** Voltage-only, no BMS, unreliable with a Cap fitted
   ([2026-06-12](https://old.reddit.com/r/CardPuter/comments/1u3qeez/), 9 comments;
   [2026-08-21 "Problems charging the Cardputer ADV"](https://old.reddit.com/r/CardPuter/comments/1vu5kya/), 17 comments).
3. **GNSS "not working"** — RX/TX pins, launcher state, or Meshtastic precision settings.
   Never yet actually a dead receiver in any thread that reached a resolution.
4. **Meshtastic BLE/Wi-Fi instability on ESP32-S3** — the stated motivation for at least
   two independent alternative firmwares.
5. **Only one Cap slot.** *"Cardputer ADV + LoRa cap, only one module…any project ideas?"*
   ([2026-08-12](https://old.reddit.com/r/CardPuter/comments/1vmd55m/)). The wish is
   explicit: *"Would love to have a CC1101/GPS/NRF24/RFID/LoRa all in one"* —
   u/heytheremonkeyboy, [2025-09-08](https://old.reddit.com/r/CardPuter/comments/1nbe134/).

## 5. Evidence discipline

Everything in §2–§4 is **firsthand owner report, demonstrable project, or informed
interpretation** — none of it is measurement. The counts in §4 are orderings within the
217-post sample, not population statistics. Where a thread reached a resolution, the
resolution is quoted rather than the complaint.
