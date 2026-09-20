# Xteink X4 — sources

Retrieved **2026-09-04** unless stated.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published | Establishes | Limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| **X401** | `freeink-sdk` `BoardConfig.h` `XTEINK_X4` L844–874 | Free-Ink | community | source (commit-pinned) | <https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/libs/hardware/BoardConfig/include/BoardConfig.h#L844-L874> | 2026-09-04 | commit 2026-09-01 | **Every pin.** SPI clock policy, the GPIO13 latch and the two board revisions | Third-party RE; not vendor documentation | `scratch/eink-software/repos/freeink-sdk/` |
| **X402** | `InputManager.cpp` L29–45, `InputManager.h` L73–74 | Free-Ink | community | source | <https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/libs/hardware/InputManager/src/InputManager.cpp> | 2026-09-04 | same | **ADC ladder pins and raw readings from three physical devices** | — | same |
| **X403** | `XteinkDetect.cpp` | Free-Ink | community | source | <https://github.com/Free-Ink/freeink-sdk/blob/24003795381a6c23630a26472ae3b06550333e71/libs/hardware/XteinkDetect/src/XteinkDetect.cpp> | 2026-09-04 | same | X3-vs-X4 I²C fingerprint; controller probe | — | same |
| **X404** | **OEM full-flash dump, 16 MB** | re-uploaded by `abhishek-nerella` | community | firmware binary | <https://raw.githubusercontent.com/abhishek-nerella/XTEINK-OEM-BIN-/main/flash.bin> | 2026-09-04 | unknown | **Partition table, chip-id 5 = C3, app descriptor, OTA + web-manager endpoints** | **Provenance of the dump is undocumented.** Licence none declared | [archived](artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin.ARCHIVED.md) |
| **X405** | `zocs/eink-quick-flasher` firmware README | community dev | community | repository doc | <https://github.com/zocs/eink-quick-flasher/blob/main/firmware/README.md> | 2026-09-04 | — | Stock versions **V5.1.6 (EN)** and **V5.2.13 (CN)**; that **CN/EN differ only by default UI language** | The .bin files are Git LFS pointers; blobs **not fetched** | `scratch/xteink/firmware/zocs-firmware-README.md` |
| **X406** | "The Xteink X4 - A Pocket-Sized E-Reader Gem" | r/Ultralight | community | forum, owner report | <https://old.reddit.com/r/Ultralight/comments/1r1jfny/> | 2026-09-04 | 2026-02-11, 51 pts | **114×70×7 mm, 80 g, 220 PPI, 4 front + 3 side buttons** | **Single source** for the physical dimensions | `scratch/xteink/reddit/_merged-posts.json` |
| **X407** | "Hi everyone, I'm Crusoe from Xteink" | Xteink founder | **primary** (self-published) | forum post | <https://old.reddit.com/r/ereader/comments/1o2203h/> | 2026-09-04 | 2025-10-09, **1,477 pts** | Company is *"a small team based in Shenzhen"*; the X4 is their *"4.3-inch model"* | Founder marketing statement | same |
| **X408** | "Xteink Star Pupil X4 (星瞳X4) first impressions" | r/ereader | community | forum, owner report | <https://old.reddit.com/r/ereader/comments/1n5kmpc/> | 2026-09-04 | 2025-09-01, 191 pts | **Chinese product name 星瞳 = "Star Pupil"**; earliest English owner report found | — | same |
| **X409** | "X3 vs X4 - actual experience comparison" | r/xteinkereader | community | forum, comparative ownership | <https://old.reddit.com/r/xteinkereader/comments/1syav96/> | 2026-09-04 | 2026-04-28, **412 pts** | Button feel: X4 *"clickier and louder"*, X3 *"mushy and quieter"* | Subjective, firsthand | same |
| **X410** | X4 accessory collection | Xteink | **primary** | store API | <https://www.xteink.com/collections/x4-series/products.json?limit=250> | 2026-09-04 | — | **The X4 device is absent; all 4 accessory SKUs sold out** → delisted | Snapshot | `scratch/xteink/vendor/coll-x4-series.json` |
| **X411** | `togotago/xteink-x4-escape` | community dev | community | repository | <https://github.com/togotago/xteink-x4-escape> | 2026-09-04 | pushed 2026-05-10 | A named, reproducible brick (CrossPoint 1.2.0, OTA fails at `esp_ota_end()`) and its escape recipe | Not tested here | — |
| **X412** | `adafruit/Adafruit_CircuitPython_Xteink_X4` | **Adafruit** | credible mirror | repository | <https://github.com/adafruit/Adafruit_CircuitPython_Xteink_X4> | 2026-09-04 | pushed 2026-04-23 | A major vendor published a CircuitPython helper for this device | Not inspected | — |

## Corroboration map

| Claim | Independent sources |
|---|---|
| SoC is ESP32-C3 | **[SDK]** profile · **[DUMP]** bootloader chip-id 5 · **[TD]** X3 photo caption · **[CN-TD]** Chinese BOM |
| 16 MB flash | **[SDK]** · **[DUMP]** image length · **[TD]** *"128 MBit (16 MB) flash"* |
| ~220 PPI | **[COMM]** owner report (220) · **arithmetic** from 800×480 / 4.26″ = 219 |
| Delisted | **[VENDOR]** absent from catalogue · accessories sold out |

## Not used as evidence

`xteink.com` product prose (AI/SEO-generated); `aimindseye/xteink-x4` wiki
(self-labelled AI-generated, no primary measurement).
