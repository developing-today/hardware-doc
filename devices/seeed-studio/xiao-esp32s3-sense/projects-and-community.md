# Projects and community — XIAO ESP32S3 Sense

> What people actually build with this board, aggregated from primary sources.
> Snapshot **2026-08-24**.

## Where this data comes from

The bulk of this page is **extracted from Seeed's own 129-page XIAO Reference Design catalogue** ([`xiao-reference-design.pdf`](artifacts/datasheets/xiao-reference-design.pdf.ARCHIVED.md) *(archived — placeholder)*, 49.9 MB, published 2025-11-15). That document is easy to overlook — the filename suggests a hardware design guide, but pages 14–129 are a curated **project showcase**, one project per page, each with an author byline, a description, keywords and a "Read more details" hyperlink.

Those hyperlinks are **link annotations, not text**, so they are invisible to ordinary text extraction and to search engines indexing the PDF's text layer. [`tools/extract_showcase.py`](../../../tools/extract_showcase.py) pulls them out of the PDF's `/Annots` structures. It also has to undo Adobe InDesign's kerning export, which scatters spaces inside words (`W e ar ables`), by building a vocabulary from the non-kerned pages and greedily re-merging token runs.

Result: **117 project entries, 116 with working external URLs**, of which **28 use the XIAO ESP32-S3 or S3 Sense**. Machine-readable output: [`artifacts/showcase-projects.json`](artifacts/showcase-projects.json).

This matters for durability. The PDF is a single 50 MB file on Seeed's CDN; the projects live across five other platforms. Both are fragile. The table below is the flattened, greppable version.

### Where the community actually publishes

| Platform | S3/Sense projects |
|---|---:|
| hackster.io | 10 |
| youtube.com | 7 |
| instructables.com | 4 |
| hackaday.io | 2 |
| github.com | 1 |

**Only one of the 28 showcased projects links to a Git repository.** The rest are write-ups or videos. This is the defining characteristic of this board's community: it is a *maker* community, not a software-engineering one. Reproducible, licensed, version-controlled source is scarce — which is exactly what [`examples/best.md`](examples/best.md) had to work around, and why so many candidate projects there carry no licence.

## Showcased projects (Seeed catalogue, S3 / S3 Sense only)

### Wearables

| Project | Board | Author | Source |
|---|---|---|---|
| **TPGmini v2 Tiny AR Wearable Companion** | Sense | Nguyễn Minh HIỂN | [hackaday.io](https://hackaday.io/project/202281-tpgmini-the-customizable-ar-smart-glasses-v1) |
| **WatchThis Wearable Point-and-Ask Assistant** | Sense | Cathy Mengying Fang, Patrick Chwal | — |
| **LED Choker** | S3 | Ted | [hackaday.io](https://hackaday.io/project/195078-led-choker) |
| **uPhone AI Wearable for Social Interaction** | S3 | Cayden Pierce | — |
| **OpenGlass $20 AI-Powered Smart Glasses** | Sense | Nik Shevchenko | — |

### Robotics

| Project | Board | Author | Source |
|---|---|---|---|
| **ARMOR: Egocentric Perception for Humanoid Robots** | S3 | Daehwa Kim , Mario Srouji, Chen Ch | — |
| **ESP-ROLL: Self-Balancing Spherical Ball Robot** | Sense | Max Imagination | [youtube.com](https://www.youtube.com/watch?v=VuBfRYNQgw0) |
| **FPV Robot Car with XIAO ESP32-S3 Sense By Nickson Kiprotich ** | Sense | Nickson Kiprotich | [hackster.io](https://www.hackster.io/tech_nickk/fpv-robot-car-with-xiao-esp32s3-sense-a3dd8a) |
| **Small Robot Car with Camera** | Sense | Just Do Electronics | [youtube.com](https://www.youtube.com/watch?v=XsVgyg9ZOLs) |
| **Gus: A Smart Robot Whose Eyes Indicate Your Room's Health** | Sense | Makestreme | [hackster.io](https://www.hackster.io/makestreme/gus-a-smart-robot-whose-eyes-indicate-your-room-s-health-2ee50c) |
| **DIY Mini FPV Tank** | S3 | techiesms | [youtube.com](https://www.youtube.com/watch?v=tOGO_k2xXh0) |
| **TN-24 V2.0: Emotionally Intelligent Desktop Robot** | Sense | Nickson Kiprotich | [hackster.io](https://www.hackster.io/tech_nickk/tn-24-v2-0-cute-desktop-companion-robot-44a472#toc-upcoming-updates-2) |
| **XIAO Camera NanoTank** | S3 | moononournation | [instructables.com](https://www.instructables.com/Camera-NanoTank/) |
| **3D-Printed Screw-Propelled Robot with Video Feed** | Sense | Gokul KB | [instructables.com](https://www.instructables.com/3D-Printed-Screw-propelled-Robot-With-Video-Feed/) |
| **ESP-DIVE — DIY RC Submarine with FPV Camera** | Sense | Max Imagination | [youtube.com](https://www.youtube.com/watch?v=d-2uSKn9rYs) |

### Smart Home

| Project | Board | Author | Source |
|---|---|---|---|
| **Static IP Address** | Sense | Pradeep | [hackster.io](https://www.hackster.io/pradeeplogu0/static-ip-address-on-xiao-esp32-s3-sense-4b4bdb) |
| **Sensing Environmental Conditions in My Garden** | S3 | Spencer and Yvonne | [hackster.io](https://www.hackster.io/spenyan/sensing-environmental-conditions-in-my-garden-with-xiao-1fe6c7) |
| **Temperature Prediction using a TinyML LSTM model** | Sense | MJRoBot (Marcelo Rovai) | [hackster.io](https://www.hackster.io/mjrobot/temperature-prediction-using-a-tinyml-lstm-model-264029) |
| **Home Automation Shield** | S3 | Arnov Sharma | [hackster.io](https://www.hackster.io/Arnov_Sharma_makes/xiao-esp32-home-automation-shield-7c568e) |

### Health

| Project | Board | Author | Source |
|---|---|---|---|
| **AI Microscope for Real-Time Sample Analysis** | Sense | techiesms | [youtube.com](https://www.youtube.com/watch?v=HbGUlDN49r8&ab_channel=techiesms) |

### AI

| Project | Board | Author | Source |
|---|---|---|---|
| **Real-Life Pokédex with AI Voice & Vision Recognition** | Sense | abe's projects | [youtube.com](https://www.youtube.com/watch?v=wVcerPofkE0) |
| **AI Study Lamp That Helps You Reduce Distractions** | S3 | Arpan Mondal | [instructables.com](https://www.instructables.com/AI-Study-Lamp-Helps-Reduce-Distractions/) |
| **AI Candy Dispenser** | Sense | Bruno Santos | [github.com](https://github.com/feiticeir0/ai-candy-dispenser) |
| **Dual AI Camera Hummingbird Detection and Capture** | Sense | Ralph Yamamoto | [hackster.io](https://www.hackster.io/Ralphjy/dual-ai-camera-e04757) |
| **AI Scarecrow Makes Noise When It Sees Birds** | S3 | Makestreme | [hackster.io](https://www.hackster.io/makestreme/ai-scarecrow-makes-noise-when-it-sees-birds-1b5dd3) |
| **Miniature ChatGPT Voice Assistant** | Sense | SeeedStudio | [youtube.com](https://www.youtube.com/watch?v=wPi-XjeJPNw) |

### Tools

| Project | Board | Author | Source |
|---|---|---|---|
| **XIAO ESP32 S3 Handheld Camera Pocket Edition** | S3 | Arnov Sharma | [hackster.io](https://www.hackster.io/Arnov_Sharma_makes/xiao-esp32-s3-handheld-camera-pocket-edition-9325f6) |

### Uncategorised

| Project | Board | Author | Source |
|---|---|---|---|
| **Li-ion Cell Charger** | S3 | Arnov Sharma | [instructables.com](https://www.instructables.com/Li-ion-Cell-Charger-With-TP4056-and-XIAO-ESP32S3/) |

---

## What the project mix tells you

Counting the 28 showcased S3/Sense projects by what they actually do:

| Application pattern | Count | Notes |
|---|---:|---|
| **Camera streaming / FPV** (robots, vehicles, drones) | 9 | The single largest cluster. Sense + motor driver + Wi-Fi |
| **AI vision + LLM** (glasses, assistants, recognition) | 7 | Almost all offload inference to a cloud LLM, not on-device |
| **Wearables** | 5 | Driven entirely by the 17.8 × 21.1 mm footprint |
| **TinyML on-device** | 3 | Edge Impulse / SSCMA |
| **Environmental / smart home sensing** | 3 | Often uses the plain S3, not the Sense |
| **Power / charging utility** | 1 | |

Three observations worth acting on:

**The board is bought for the camera.** Roughly two-thirds of showcased projects use the camera; the microphone appears in a handful; the microSD slot is almost never the reason someone picked it. If you are evaluating the Sense for an audio-first product, you are going against the grain of the community's experience — expect less prior art and fewer answers (this matches the coverage gaps found in [`examples/best.md`](examples/best.md)).

**"AI" almost always means a cloud round-trip.** OpenGlass, WatchThis, uPhone, the Pokédex and the ChatGPT assistant all capture on-device and send the image to GPT-4o or similar. Genuine on-device inference is confined to the TinyML cluster and is much more constrained. Do not read "AI wearable powered by XIAO ESP32-S3 Sense" as evidence that the board runs the model.

**Battery-powered wearables are common despite the board's power weaknesses.** Five wearables ship despite there being [no battery voltage sense](pinouts-and-buses.md#82-there-is-no-battery-voltage-sense--confirmed-by-the-vendor) and a camera that [cannot be powered down](pinouts-and-buses.md#31-there-is-no-camera-power-down-or-reset-line--and-that-has-consequences). The showcase entries do not report runtime figures, so this should not be read as evidence that battery life is good — only that people accept it.

## Notable individual projects

- **OpenGlass** (Nik Shevchenko) — "$20 AI-powered smart glasses". The most-referenced XIAO ESP32S3 Sense project on the internet, and largely responsible for the board's visibility in the AI-wearable scene.
- **WatchThis** (Cathy Mengying Fang, Patrick Chwalek, Quincy Kuang, Pattie Maes — **MIT Media Lab**) — a wrist-mounted point-and-ask assistant using GPT-4o. Notable as an academic-lab use of the board.
- **ARMOR** (Daehwa Kim, Mario Srouji, Chen Chen, Jian Zhang — **Apple**-affiliated) — egocentric perception for humanoid robots, using multiple XIAO ESP32-S3 units with SparkFun VL53L5CX ToF sensors. The most technically serious entry in the catalogue.
- **AI Candy Dispenser** (Bruno Santos / `feiticeir0`) — the **only** showcased project with a GitHub repository: <https://github.com/feiticeir0/ai-candy-dispenser>.
- **Temperature Prediction using a TinyML LSTM** (Marcelo Rovai) — Rovai is the author of the largest teaching repository for this board (see [`examples/best.md`](examples/best.md)) and of the *TinyML Made Easy: XIAO ESP32S3* ebook.

## Data-quality warning about the catalogue itself

Seeed's showcase PDF contains at least one **copy-paste error**: page 20, "Environment Audio Monitoring Wearable" by *Solomon Muhunyo Githu*, carries a description that is **verbatim identical** to page 16's "Vibe AI Wearable Nutrition Tracker" by *Jacob Trebil* — text about passively tracking meals with computer vision, which has nothing to do with audio monitoring.

Treat the catalogue's descriptions as marketing copy of uncertain accuracy. The **titles, authors and hyperlinks** appear reliable; the prose does not. Where a project matters to you, follow the link rather than trusting the summary.

## Evidence status

Everything on this page is **reproduced documentation** — Seeed's editorial claims about third-party projects. It is *not*:

- evidence that any project works as described (none were built or tested here);
- a measurement of prevalence (a vendor showcase selects for promotable projects, and Seeed sponsors or solicits many of them);
- a complete census (this is one catalogue; GitHub search alone returned 142 repositories matching "xiao esp32s3 sense" — see [`examples/catalog.json`](examples/catalog.json)).

Individual project pages on Hackster/Hackaday/Instructables are **firsthand build reports** by their authors, which is stronger evidence than the catalogue summary but still uncorroborated and rarely includes measurements.

## Related

- [`examples/best.md`](examples/best.md) — code you can actually build from, with licences checked
- [`examples/catalog.json`](examples/catalog.json) — 18 GitHub projects with pinned commits
- [`README.md`](README.md) — device overview
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — vendor documentation errors, including this one
