# XIAO ESP32S3 Sense — gaps, conflicts and unresolved questions

> Every place where sources disagree, where vendor data is wrong, or where I could not establish a fact.
> Research snapshot **2026-08-24**. Nothing here is smoothed over — where I could not resolve a conflict, it stays open.

---

## 1. Seeed serves the wrong file under the "XIAO ESP32S3 v1.4" schematic URL

**Severity: high — you cannot currently obtain the non-Sense schematic at all.**

| URL (advertised as) | Actually contains |
|---|---|
| `…/new-res/202003751_XIAO%20ESP32S3_v1.4_SCH_260226.pdf.pdf` — *plain XIAO ESP32S3 v1.4 schematic* | The **Sense v1.5** schematic |
| `…/new-res/202003753_XIAO%20ESP32S3%20Sense_v1.5_SCH_260226.pdf.pdf` — *Sense v1.5 schematic* | The Sense v1.5 schematic ✔ |

Both PDFs are **byte-identical**: SHA-256 `15993097cd695d17…`, 666,348 bytes. The two `SCH&PCB` ZIPs are byte-identical too, and unzipping the "v1.4" archive produces a directory literally named `202003753_XIAO ESP32S3 Sense_v1.5_SCH&PCB_260226`.

Verified by download and hash comparison on 2026-08-24 (see [`acquisition/manifest.json`](acquisition/manifest.json)). The duplicate is recorded at [`artifacts/schematics/xiao-esp32s3-v1.4-sch.pdf.DUPLICATE.md`](artifacts/schematics/xiao-esp32s3-v1.4-sch.pdf.DUPLICATE.md).

**Consequence:** there is no published schematic for the current non-Sense XIAO ESP32S3 revision. The closest available is the **v1.2** EAGLE PDF (`XIAO_ESP32S3_SCH_v1.2.pdf`, retained) and the **v1.1** EAGLE source. For Sense work this does not matter — the Sense schematic is the superset — but if you are designing against the bare board, be aware you are working from a 2023 document.

**Status: unresolved.** Not reported to Seeed as part of this research pass.

---

## 2. The schematic's own revision number contradicts its filename

The Sense schematic package is published as **v1.5**, but internally:

| Location | Says |
|---|---|
| Download filename | `..._Sense_v1.5_SCH_260226` |
| KiCad project / PCB / sch filenames | `XIAO ESP32S3_V1.5.kicad_*` |
| **PDF title-block `Rev:` field** | **`V1.3`** |
| **Footprint library nickname** | **`XIAO ESP32S3_V1.3`** |
| Revision-history sheet, latest entry | **`v1.3`**, 2025/10/21 |
| PDF creation date | `2026-02-26`, sheet date `2026-02-10` |

The revision-history sheet lists exactly four revisions — v1.0 (2023-01-04), v1.1 (2023-03-27), v1.2 (2023-07-25), v1.3 (2025-10-21) — and **no v1.4 or v1.5 entry exists**.

Most likely reading: **the electrical design is v1.3**; "v1.4"/"v1.5" are Seeed's document/release numbering, not board revisions. That would also explain item 1 — `202003751` and `202003753` are internal document IDs that got crossed.

**Consequence for you:** if you need to know which board is in your hand, **the silkscreen and the revision-history sheet are the authority, not the filename.** A board marked v1.3 is the current design.

**Status: unresolved.** No Seeed document explains the numbering.

---

## 3. Battery charge current: 110 mA (schematic) vs 100 mA (wiki)

| Source | Claim |
|---|---|
| Schematic annotation, v1.5 sheet | `ICharge = 24000/220K = 110mA`, with R10 = 220 kΩ confirmed in the BOM |
| `XIAO_ESP32S3_Getting_Started.md` | "Charging current: **100mA** (Fast) / 0.9mA (Trickle)" |

The schematic's arithmetic is self-consistent (24000 / 220000 = 109 mA). The wiki figure is probably a rounded marketing number, but it could equally be a measured value or reflect a different R10 on some revision.

**Status: unresolved.** Treat ~100–110 mA as the range; do not design a charge-time budget that depends on the difference. Nothing here was measured on hardware.

---

## 4. Seeed's own spec table gives two different deep-sleep figures for the Sense

Within a single table in `XIAO_ESP32S3_Getting_Started.md`:

- one row: Sense deep sleep = **3 mA**
- another row: Sense deep sleep = **3.8 V / 33.51 µA**

These differ by ~90×. 33.51 µA is plausible for an ESP32-S3 in deep sleep with a camera left powered; 3 mA is not obviously attributable to anything, though it could be a figure measured with the camera in an un-idled state.

**Update 2026-08-24:** the product page's spec table adds a third datapoint — Sense
deep sleep = **3 mA** again (while the non-Sense XIAO ESP32S3 column on the same page
says **14 µA**). The suspicious 3 mA figure is therefore repeated across two vendor
surfaces. Recorded in [`camera-sensors.md`](camera-sensors.md#power-vendor-published-product-page-2026-08-24).

**Status: unresolved.** I would plan around **~34 µA** and verify on your own hardware before committing to a battery-life claim. Neither number was measured here.

---

## 5. The camera sensor fitted has changed, and the product page is stale

Seeed's wiki states plainly:

> "The **OV2640 camera has been discontinued**, and the subsequent XIAO ESP32-S3 Sense uses the **OV3660** camera model. However, the Wiki example code for the camera still applies."

Meanwhile the same wiki's feature bullets still advertise "Detachable **OV2640** camera sensor for 1600×1200", and the product page continues to headline the OV2640.

So a unit bought today most likely carries an **OV3660 (2048×1536)**, not the advertised OV2640 (1600×1200). An **OV5640** is also sold as a separate upgrade and is compatible.

**Practical impact is small but real:** the sensor is auto-detected by `esp32-camera` (the factory binary contains driver strings for all three), so code generally does not care. But:
- maximum resolution differs (UXGA vs QXGA vs 2592×1944);
- OV3660 and OV5640 have different register sets, so any code that pokes sensor registers directly will not port;
- the OV5640 upgrade is sold **with a heat sink** because it runs hot.

**Status: partially resolved.** Which sensor ships is *not* determinable from the SKU — you must read it back at runtime (`esp_camera_sensor_get()->id.PID`). Document your unit.

> **Update 2026-08-24:** the product page has since been amended. It now carries a
> banner ("devices with either OV2640 or OV3660 sensors may be shipped") and a change
> record entry ("2025/6/30, Upgrade camera sensor from OV2640 to OV3660"), and links a
> *PCN XIAO ESP32-S3 Sense Series Camera Upgrade* PDF. The wiki feature bullets still
> advertise the OV2640, so "stale" now applies to the wiki rather than the product page.
> Sensor details, detection code and per-part comparison: [`camera-sensors.md`](camera-sensors.md).

---

## 6. ~~J3 board-to-board pinout is undocumented~~ — **RESOLVED 2026-08-24**

Seeed publishes no pinout for the 30-pin `DF40C-30DP-0.4V(51)` connector. The XIAO side was reconstructed from the KiCad PCB netlist ([`pinouts-and-buses.md` §2](pinouts-and-buses.md#2-the-j3-board-to-board-connector-sense-daughterboard-interface)).

**The daughterboard side is now also resolved.** The file Seeed distributes as *"XIAO ESP32S3 Exp. Board v1.0"* **is the Sense sensor board**, not the unrelated OLED/RTC expansion accessory its name implies. Its EAGLE `.sch` is XML with an explicit netlist. See [`sense-daughterboard.md`](sense-daughterboard.md).

Each previously-unknown item:

| Was unknown | Now established |
|---|---|
| microSD pull-up / termination | 22 Ω series (R1–R3), 4.7 kΩ pull-ups, ESD arrays D1–D4, ferrite-filtered supply |
| Microphone part number | **MSM261D3526H1CPM** — see item 7 |
| Whether J3.2 (GPIO3) is used | **Yes** — `D2/SD_CS`, an alternate SD chip-select via **DNP R11** |
| Camera FPC pinout | Full 24-pin map recovered; `PWDN`/`RESET` are **strapped off** by R9/R10 |

**Residual unknown:** the camera *module's* internal schematic (sensor, crystal, decoupling on its own FPC) — JA1 is only the connector.

---

## 7. ~~Microphone part number not established~~ — **RESOLVED 2026-08-24**

The Sense microphone is a **MEMSensing `MSM261D3526H1CPM`**, confirmed from **primary evidence**: reference designator `MIC1` in the daughterboard EAGLE BOM, library part `MIC-MSM261D3526H1CPM`.

This confirms the part number that had circulated online for years without a citable source. Component record: [`components/memsensing/msm261d3526h1cpm`](../../../components/memsensing/msm261d3526h1cpm/README.md).

Additionally established: the **`L/R` pin is tied to GND**, selecting the left channel — the hardware reason the device is mono and why right-channel configurations return silence. `CLK` and `DATA` pass through **solder jumpers JP1/JP2**, so the microphone can be disconnected to free GPIO41/42 (`MTDI`/`MTMS`).

**Two failed routes worth recording**, since both looked promising:
- **FCC internal photos** ([`regulatory-and-certification.md`](regulatory-and-certification.md)) — the exhibits show the mainboard, antenna and camera module, but no daughterboard component markings at legible resolution.
- Searching for a Seeed BOM release — none exists.

The answer was in a file already downloaded on day one, behind a misleading filename.

**Still unknown:** the microphone's acoustic specifications (sensitivity, SNR, AOP, frequency response). No MEMSensing datasheet was obtained.

---

## 8. EAGLE-era schematic PDFs have no extractable text

`XIAO_ESP32S3_SCH_v1.2.pdf`, `XIAO ESP32S3_v1.1_SCH_230327.pdf` and `XIAO_ESP32S3_ExpBoard_v1.0_SCH.pdf` were exported from **EAGLE 9.6.2 via Qt 5.9.4**, which renders all text as vector paths. Text extraction returns essentially nothing (a stray full-width colon).

This is why all netlist work here uses the **v1.5 KiCad** package instead. The EAGLE `.sch` files *are* XML and are parseable — they are retained in [`artifacts/extracted/`](artifacts/extracted/) — but they were not fully mined in this pass.

**Consequence:** the **expansion-board accessory** (OLED / RTC / buzzer / SD add-on) is documented here only from its PDF and wiki prose, not from a parsed netlist. Its EAGLE XML is present if someone wants to finish the job.

**Status: known limitation, tractable.**

---

## 9. Factory firmware ships with unusable hardcoded Wi-Fi credentials

The shipped `CameraWebServer.bin` embeds the strings `seeedstudio` and `XIAO_ESP32S3_Sense` adjacent to the connection logic, in a station-mode build with no SoftAP fallback. It therefore attempts to join Seeed's internal network and fails everywhere else. Full analysis in [`factory-firmware.md` §5](factory-firmware.md#5-the-factory-demo-cannot-connect-to-your-network).

**What is confirmed:** the strings are in the binary; the build is station-mode; the demo cannot be configured at runtime.
**What is inferred:** which of the two strings is the SSID and which is the password. Not verified on hardware.

This is the most likely explanation for the recurring "my new board does nothing" reports, but I have not confirmed the causal link with a physical unit.

**Status: high confidence, not hardware-verified.**

---

## 10. The "20240814" firmware release contains 2023 binaries

Every binary in `XIAO-ESP32S3-Sense-firmware-20240814.zip` is byte-identical to the one in the older `XIAOESP32S3-Sense-firmware.zip`. The application was built **2023-02-08**; only the flashing wrapper changed. The date in the filename is a repackaging date.

**Status: resolved (by hash comparison), but undocumented by the vendor.** Do not assume the newer download fixes anything.

---

## 11. Vendored `WifiLocation` library carries an expired root CA

The `XIAO-ESP32S3-Geolocation` example bundles a `WifiLocation` snapshot pinned to the **Baltimore CyberTrust Root**, which expired **2025-05-12**. Upstream has migrated to DigiCert Global Root G2. The bundled copy's HTTPS geolocation call should therefore fail certificate validation today.

Full analysis and patch: [`examples/vendored-lib-deltas/README.md`](examples/vendored-lib-deltas/README.md).

**Status: established by inspection of the embedded PEM; not reproduced on hardware.**

---

## 12. Smaller open questions

| Question | What is known | What would resolve it |
|---|---|---|
| What are C1, C2, C17, C20, L3 (all **DNP**) for? | C1/C2 sit on the USB D± lines; C17/L3 sit in the antenna matching network; C20 is adjacent to L3. Reasonable reading: optional USB EMI caps and an alternate antenna match. **This is inference from placement, not documented.** | A Seeed design note, or a variant build that populates them |
| Is `TP1` connected to anything? | The netlist shows it in a single-pad net (no other member) | Physical probing |
| ~~Does the daughterboard load `VIN` or `VCC_3V3`?~~ | ✅ **RESOLVED** — **both, for different loads.** The camera runs from local LDOs (U1 2.8 V, U2 1.3 V); the microphone and microSD run from `VCC_3V3`. See [`sense-daughterboard.md` §3](sense-daughterboard.md#3-power--the-camera-needs-three-rails) | — |
| Real usable microSD throughput | Wired 1-bit SPI only; no SDIO lines cross J3. Vendor quotes no figure | Benchmark on hardware |
| Does the OV5640 upgrade need the heat sink, or is it optional? | Seeed sells them together and cites 53.5 °C with dual heat sinks vs ~10 °C higher without | Thermal measurement under sustained streaming |
| ~~**Why LoRa and the camera cannot coexist**~~ **RESOLVED** | **Pin conflict, not connector incompatibility.** The Wio-SX1262 needs GPIO14–18, 21, 47, 48 — **all eight are camera/SD pins** on the Sense daughterboard. From [Seeed's published Wio-SX1262 schematic](comparisons-and-recommendations.md#why-lora-and-the-camera-are-mutually-exclusive--resolved-from-the-schematic) | — |
| **Why the Plus B2B is "incompatible" with the camera board** | The Plus's J3 has the **same footprint, same 34 pads and the same pin assignment** as the Sense mainboard, but uses a **different connector part** (`LBF11-G30P-BOR` vs Hirose `DF40C-30DP-0.4V(51)`). The daughterboard socket is a Hirose `DF40HC(3.0)`. Most likely a mating/stack-height incompatibility rather than an electrical one — but Seeed's claim stands until tested | Physically attempting the mate, or the `LBF11-G30P-BOR` datasheet |
| What `J1` and `J2` (both **DNP**) in v1.1 were for | Present as do-not-populate positions in the v1.1 EAGLE schematic, **absent from v1.5**, and **not mentioned in Seeed's revision history**. Likely factory test/programming points | A Seeed design note, or a populated variant |
| Exact ESP32-S3R8 date-code / silicon revision fitted | Not marked in any published document | Reading `esp_chip_info()` / eFuse on a physical unit |
| Which daughterboard revision ships today | The only published schematic is **v1.0, dated 2023-03-24**. The OV2640→OV3660 sensor change happened later, so a revised board may exist | A newer Seeed release, or markings on a current unit |
| Camera module internal schematic | JA1 is only the 24-pin FPC connector; the sensor, its crystal and decoupling sit on a separate module | Module teardown or an OmniVision reference design |
| Microphone acoustic specs (sensitivity, SNR, AOP) | Part identified as MSM261D3526H1CPM, but **no MEMSensing datasheet was obtained** | The MEMSensing datasheet |
| What `model-differences.pdf` (FCC) says | Scanned image, **no text layer, unread**. Would state how the Sense differs from the plain board for certification | OCR the exhibit |

---

## 13. What this research pass did *not* cover

Stated explicitly so the boundary is clear:

- **No hardware was available.** Nothing here is a firsthand electrical, thermal, throughput or power measurement. Every number is either vendor-published, extracted from a binary, or computed from design files.
- **No example was built or flashed.** Selected examples were inspected and their dependency pinning audited, but no compile was attempted.
- **The Sense daughterboard was not torn down.** Items 6 and 7 depend on this.
- **Regulatory filings (FCC/CE) were not mined.** FCC internal-photos exhibits would likely resolve item 7 and much of item 6.
- **Non-English community sources were only lightly sampled**, although the wiki snapshot includes the `zh-CN`, `ja` and `pt-BR` translations.

## Related

- [`pinouts-and-buses.md`](pinouts-and-buses.md) — the wiring facts that *are* established
- [`factory-firmware.md`](factory-firmware.md) — firmware analysis
- [`examples/vendored-lib-deltas/README.md`](examples/vendored-lib-deltas/README.md) — dependency audit
- [`sources.md`](sources.md) — full source table with evidence classes
