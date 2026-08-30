# Archived image and data payloads — reacquisition record

**55 files, 26,570,069 bytes (25.3 MiB)** moved out of the repository on **2026-08-30**. Not
deleted. 
This took the vendored library from **28 MiB to 8.3 MiB while removing no code at all.**

> **These files are absent from the repository.** They are not symlinks and not placeholders-in-place —
> the paths simply do not exist here any more. This record is the only thing standing in for them,
> which is why it carries a SHA-256, a byte count and a pinned reacquisition URL for every file.
>
> The archive copy is a **convenience for whoever holds it, not part of the contract**: it lives
> outside the repository at a machine-local path, so nothing here may depend on it.

## What was archived, and what deliberately was not

Every file here is **embedded image data** — either a `.bmp`/`.jpg` asset or a `.h` file that is a
generated C array of pixel data (all `.h` files over 100 KB in this tree are exactly that; none is
a real header). They are demo artwork for the example sketches.

| Kept | Archived |
|---|---|
| Every `.ino`, `.cpp` and real `.h` | `.bmp` / `.jpg` assets |
| `src/boards/Inkplate5*`, `src/features/`, `src/graphics/`, `src/system/` | `.h` files over 100 KB — generated pixel arrays |
| `Fonts/`, `licenses/`, `LICENSE`, `library.properties` | |
| Every example **directory** and its source | |

**No example directory was removed and no path stopped resolving.** The sketches still sit where
they always did; only the artwork they display moved. That matters because authored documentation
cites example *directories* — `examples/Inkplate5/Diagnostics/Inkplate5_Peripheral_Mode/`,
`examples/Inkplate5V2/Diagnostics/Inkplate5V2_SetVCOM/` and others — and those citations are
unaffected.

**Checked before archiving:** every one of the 55 files was tested by full relative path, as a
fixed string, against all authored Markdown outside this tree. **Zero were cited.**

> An earlier check appeared to show five citations of `image.h`. That was a false positive — the
> `.` in `image.h` was being read as a regex wildcard. Verified again with fixed-string matching on
> the full relative path.

## Reacquisition

| | |
|---|---|
| Repository | `SolderedElectronics/Inkplate-Arduino-library` |
| URL | <https://github.com/SolderedElectronics/Inkplate-Arduino-library> |
| Commit | **`1751cbe578522e5ea9ef713f32980186bde38077`** (2026-08-20) |
| Licence | **LGPL-3.0** |
| Also on | Arduino Library Manager |
| Source ID | **IP5-12** in [`sources.md`](../../../sources.md) |

```bash
git clone https://github.com/SolderedElectronics/Inkplate-Arduino-library
git -C Inkplate-Arduino-library checkout 1751cbe578522e5ea9ef713f32980186bde38077
```

Single file at the pinned commit:

```bash
curl -fsSL "https://raw.githubusercontent.com/SolderedElectronics/Inkplate-Arduino-library/1751cbe578522e5ea9ef713f32980186bde38077/<path-from-table>"
```

A **306-star public GitHub repository at a pinned commit, also distributed through the Arduino
Library Manager** — among the lowest reacquisition risks in this repository, which is what makes
archiving safe here.

Archive root:
`archive/hardware-doc/devices/soldered-electronics/inkplate-5/artifacts/source-snapshots/Inkplate-Arduino-library/`

## Restoring a file

Re-fetch it from the pinned upstream in the Reacquisition section above and verify against the
SHA-256 in the table. If you happen to hold the local archive, copying from the archive root shown
above is faster and gives the identical bytes.

## Note on modifying a vendored snapshot

Removing files is a **local modification**: a fresh upstream clone at the pinned commit has these
files present. Reconcile against the table above before concluding that a diff means something.

## Contents

| File | Bytes | SHA-256 |
|---|---:|---|
| `examples/Inkplate5V2/Advanced/DeepSleep/Inkplate5V2_Simple_Deep_Sleep/picture3.h` | 2,304,607 | `41dabecac977d273e4ce834aeb8458785a34134fdac418d04d7c2424646d25f6` |
| `examples/Inkplate5V2/Advanced/DeepSleep/Inkplate5V2_Simple_Deep_Sleep/picture2.h` | 2,303,987 | `09a1512a8eefef26c35c1ae52c718746982a34069484099b8a15e6f8cfababc8` |
| `examples/Inkplate5V2/Diagnostics/Inkplate5V2_Factory_Programming_VCOM/image.h` | 2,283,125 | `b98b2de763c104886ba86aae1378bae913cfed89f55a5231a52417e246eab075` |
| `examples/Inkplate5/Advanced/microSD/Inkplate5_microSD_Pictures/image1.bmp` | 1,555,254 | `2ec575f26cabdb53ff81fd62d489b10769cda8745b7d89bc4b01c8bab9a4c023` |
| `examples/Inkplate5/Advanced/microSD/Inkplate5_microSD_Pictures/image2.bmp` | 1,555,254 | `3d4f40a229837f2f90b14892b4bd1e1d7f464dd105b7822f4eeb8986a121c7d6` |
| `examples/Inkplate5V2/Advanced/WEB_WiFi/Inkplate5V2_Show_Pictures_From_Web/neowise.bmp` | 1,440,056 | `0efa1c9e55d904f3cfa87f2f0f018cb5fb1e1535a8363706ebf9c18aca640ae2` |
| `examples/Inkplate5/Advanced/WEB_WiFi/Inkplate5_Show_Pictures_From_Web/neowise.bmp` | 1,440,056 | `0efa1c9e55d904f3cfa87f2f0f018cb5fb1e1535a8363706ebf9c18aca640ae2` |
| `examples/Inkplate5/Advanced/DeepSleep/Inkplate5_Simple_Deep_Sleep/picture2.h` | 1,291,723 | `cd425f4c833ff7b8eb57497dbecdda85b995c334d056147dff9e09ea22ae9127` |
| `examples/Inkplate5/Diagnostics/Inkplate5_Factory_Programming_VCOM/image.h` | 1,286,148 | `6bbcbf95c7f3f735385b777eb80f425006725c704b4b3b215f8498778c018063` |
| `examples/Inkplate5/Advanced/DeepSleep/Inkplate5_Simple_Deep_Sleep/picture3.h` | 1,257,059 | `3bbcfa1a47cb30d83e7d5a282b74f4d2b1199258187d80ddc766d87dd2a58c7a` |
| `examples/Inkplate5/Advanced/DeepSleep/Inkplate5_Simple_Deep_Sleep/picture1.h` | 1,251,576 | `d30631061b9c4bb156176f4343ac2e5a48aedc5f8e546c0a191ba1f9b4a5b383` |
| `examples/Inkplate5V2/Advanced/DeepSleep/Inkplate5V2_Simple_Deep_Sleep/picture1.h` | 800,377 | `0c2f3456540f90d9886122861762dd8701157080b3fa965fd32ddc7d3b6d54cb` |
| `examples/Inkplate5V2/Basic/Inkplate5V2_Image_Converter/image.h` | 705,799 | `ed209990f39d3be75d2737acf4340a4d50eb3e2134e5c6c19bad827e1a785955` |
| `src/features/BME680/libs/BME680/Images/Feather_SD_BME680.jpg` | 692,332 | `62b87a9dd5d67a6e828d53e54dbc8d0736b2fc437f5acc9f90e31b0dfeaad2ff` |
| `examples/Inkplate5V2/Diagnostics/Inkplate5V2_Factory_Programming_VCOM/demo_image.jpg` | 570,111 | `2094160486d84f7b162092c12a65b28734b52526b90afa8bf7b4e2e514511318` |
| `examples/Inkplate5/Diagnostics/Inkplate5_Factory_Programming_VCOM/demo_image.jpg` | 570,111 | `2094160486d84f7b162092c12a65b28734b52526b90afa8bf7b4e2e514511318` |
| `src/features/BME680/libs/BME680/Images/TwoBME680.jpg` | 514,974 | `ff90c91f995aee51912e2c9a074f6efb44376975e53000f0da95a763be22dfd4` |
| `examples/Inkplate5V2/Basic/Inkplate5V2_Grayscale/image.h` | 498,881 | `6be585b2c6711033696b5575b183ad223750a15a7587401d8586c83ba37520dc` |
| `examples/Inkplate5/Basic/Inkplate5_Grayscale/image.h` | 498,881 | `6be585b2c6711033696b5575b183ad223750a15a7587401d8586c83ba37520dc` |
| `src/features/BME680/libs/BME680/Images/SDLoggerSPIDemo.jpg` | 489,462 | `0e30c12c7a2e9158c991cd8a2f229e52f155fdef2fb27981c11bf61ee4c3b049` |
| `extras/InkplateImage.jpg` | 415,557 | `8c64fd310d6470783735a4d69ba4b1d3328290ca6c0afc7eabfb21b002a05e76` |
| `src/features/BME680/libs/BME680/Images/adafruit-bme680.jpg` | 209,154 | `05e65f31603cd21301ce4559752b2a80a9863fb480e9e87f50c4b42336318d02` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_Google_Calendar/src/fonts/FreeSansBold48pt7b.h` | 207,871 | `ec5bc46ab9d32726832e40fc52965cb8684ea93ef26c4eb72f91470e423bf51b` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/fonts/FreeSansBold48pt7b.h` | 207,871 | `ec5bc46ab9d32726832e40fc52965cb8684ea93ef26c4eb72f91470e423bf51b` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_Google_Calendar/src/fonts/FreeSans48pt7b.h` | 192,343 | `28c1f378bf314271b58ad801a3d2180f0df4014ccbf628dc03ea10531f44b774` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/fonts/FreeSans48pt7b.h` | 192,343 | `28c1f378bf314271b58ad801a3d2180f0df4014ccbf628dc03ea10531f44b774` |
| `examples/Inkplate5V2/Advanced/WEB_WiFi/Inkplate5V2_Show_Pictures_From_Web/destination.jpg` | 178,510 | `3c704f0524f25374d78c4aab4a39429843c698d843c699c965a1cab91623873c` |
| `examples/Inkplate5/Advanced/WEB_WiFi/Inkplate5_Show_Pictures_From_Web/destination.jpg` | 178,510 | `3c704f0524f25374d78c4aab4a39429843c698d843c699c965a1cab91623873c` |
| `src/features/BME680/libs/BME680/Images/Micro_BME280_bb.png` | 169,471 | `3fb61cf2eb3fe30529961ca78f2dcbc13581923b4e92c76ba3954d08f5eb006b` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_Quotables/Fonts/exmouth_40pt7b.h` | 157,778 | `bad59d18a440163c6f41bbc3f15b7a204598430512435c828d3c2c58ce327b92` |
| `examples/Inkplate5/Projects/Inkplate5_Quotables/Fonts/exmouth_40pt7b.h` | 157,778 | `bad59d18a440163c6f41bbc3f15b7a204598430512435c828d3c2c58ce327b92` |
| `src/features/BME680/libs/BME680/Images/Mega_SW_SPI_BME280_bb.png` | 146,394 | `a932c7573b6166e2057be038227e6ed06bc6ebf49cd5f65750657f6a22df9bbc` |
| `src/features/BME680/libs/BME680/Images/Mega_HW_SPI_BME280_bb.png` | 143,553 | `f5f3bd73c1e901890d5e43e2a408cee7a877b00b545f3f0bed61a1987417533a` |
| `examples/Inkplate5/Advanced/microSD/Inkplate5_microSD_Pictures/pyramid.jpg` | 105,552 | `7a457a1d54d7079ca29a575f099bc331941b391631e0cb70458d845dbd3db4c7` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_Quotables/Fonts/exmouth_32pt7b.h` | 103,208 | `102bc2d4309de048fc6619851af3293670c74bf81e682b6060b649baf44befd4` |
| `examples/Inkplate5/Projects/Inkplate5_Quotables/Fonts/exmouth_32pt7b.h` | 103,208 | `102bc2d4309de048fc6619851af3293670c74bf81e682b6060b649baf44befd4` |
| `src/features/BME680/libs/BME680/Images/BlueDotBME680.jpg` | 98,316 | `fdc69ba61527859678d03a7ed1d81a214f6420251f3173ef303ef9e57f7d5017` |
| `examples/Inkplate5V2/Advanced/WEB_WiFi/Inkplate5V2_Show_Pictures_From_Web/neowise_Mono.bmp` | 60,064 | `1f84ec0ad898bc12637cd12c629e8ea1e66cd5951ccae3b17d769fdbab6318a1` |
| `examples/Inkplate5/Advanced/WEB_WiFi/Inkplate5_Show_Pictures_From_Web/neowise_Mono.bmp` | 60,064 | `1f84ec0ad898bc12637cd12c629e8ea1e66cd5951ccae3b17d769fdbab6318a1` |
| `examples/Inkplate5V2/Advanced/microSD/Inkplate5V2_GIF_From_SD/cat_gif.gif` | 22,489 | `10d4d75f1db65c8e2002dc92f29b7c8a0f3a474539da7c57af5c9929fec19958` |
| `examples/Inkplate5/Advanced/microSD/Inkplate5_GIF_From_SD/cat_gif.gif` | 22,489 | `10d4d75f1db65c8e2002dc92f29b7c8a0f3a474539da7c57af5c9929fec19958` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/icons/clear_sky.png` | 17,659 | `2086b3fb3957ae1134b281518a62c5f6273a8917551a797298a7caec50563c41` |
| `src/features/BME680/libs/BME680/Images/bosch-bme680.jpg` | 14,578 | `fbb51fb1fcf06fb68b957a258c808a44e669324c5a4a1b5b5907ae20a43e9acc` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/icons/moon.png` | 14,280 | `c847aa2c5964df894cb1afeb68e7f3affbf55401b3107dea41dbe8baa308faf6` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/icons/storm.png` | 12,517 | `e4fb126408df7dcaa2b08dfbba13b5625313aa10c502b17f67677b29f58bea36` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/icons/snow.png` | 12,436 | `0454d497e1c786cec4caa53fb4b45fbf2420e7c51ef7546cd539ec029e727d7d` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/icons/rain.png` | 11,881 | `1fbfbd559832ca5c721c9975ee823237e098841aea2f8ca8668e6aa54da3d31a` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/icons/fog.png` | 11,526 | `f498ca90c775e095db9585673ce1fe46290df57d0e50204bb74e3fe4c979312a` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/icons/thermometer.png` | 7,745 | `fa5ff2969a9e603e37af91c4502e19a045e2a8c758e5709a36f5e30fa29942d4` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/icons/partly_cloudy.png` | 6,321 | `231f207c4345a0d53cf195c0f275c6a401eb0d27224f36744adafbc0fee000c6` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/icons/high_battery.png` | 4,395 | `d0af972311f9007ec3606ce9651eb783951526c0bdbed9ff32bad09a3d107399` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/icons/full_battery.png` | 4,319 | `41ac10e84ee2327f528266bf25d1452806a4a47359de205632dda00c3a1bbe85` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/icons/low_battery.png` | 4,316 | `12ae61e74223df03e1a3a1c2db3b084ed1d6a175647ab5f42fbfc02f6a06c0ea` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/icons/half_battery.png` | 3,446 | `48af64925c6fd00127ce78ad0cc309d488d3bbdab2d8104db660f9bda0724a17` |
| `examples/Inkplate5V2/Projects/Inkplate5V2_OpenMeteo_Weather_Station/src/icons/gray.png` | 2,354 | `953e43086af841474b0cbf162c4c65c3aabfe17d0dd918f5807b6d56f862a9db` |
