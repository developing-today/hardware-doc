# FAQ and troubleshooting

Retrieved **2026-08-21**; re-verified against the live page **2026-08-23** (still revision 111069, content unchanged).

Source: Waveshare wiki [ESP32-S3-Knob-Touch-LCD-1.8](https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8) **section 9, "FAQ"**, plus the `{{Note}}` advisories scattered through sections 3, 5 and 6. Wikitext retained at `artifacts/source-snapshots/waveshare-wiki-wikitext-oldid-111069.txt`, lines 945-996.

**All eleven vendor FAQ entries are reproduced below**, quoted closely enough to be usable as attribution, each followed by our own commentary. Where the vendor's advice is incomplete or actively unwise, we say so — the quoted block is the vendor's position, the prose after it is ours.

---

## 1. "Why can't the program be flashed?" — the definitive orientation statement

This is the most important entry on the page, and it is worth quoting in full because it is **Waveshare's own statement of the USB-C orientation behaviour**. Elsewhere in this folder the orientation quirk is described from schematic reading and from user reports; this is the vendor asserting it directly.

> **Q: Why can't the program be flashed?**
>
> This product features two onboard chips, ESP32-S3 and ESP32. **The two insertion orientations of the Type-C plug connect to different download channels.**
>
> If programming fails, the serial port is not found, or the connection cannot be established, please perform the following steps first:
>
> 1. Disconnect the Type-C cable;
> 2. **Flip the Type-C plug 180°;**
> 3. Re-insert the cable and attempt programming again.
>
> — Waveshare wiki, ESP32-S3-Knob-Touch-LCD-1.8, §9 FAQ, revision 111069, retrieved 2026-08-21

The wikitext also preserves an **earlier, commented-out version** of the same answer, which is worth recording because it is blunter about the mechanism:

> `<!--*Plug the Type-C into the port in a different direction and try`
> `*Switch between ESP32 or ESP32S3 through Type-C access in different directions-->`

### Commentary

This confirms, from the vendor, the single most consequential fact about developing on this board. Some further points the FAQ does not make:

- **It is not a fault. It is the design.** USB-C has two sets of high-speed pins (one per rotation) so that the connector is reversible. Waveshare wired *different destinations* to each set: one orientation reaches the **ESP32-S3's native USB** (GPIO19/20), the other reaches the **`U10` USB-UART bridge** feeding the **ESP32-U4WDH**. A normal cable therefore selects a chip by how you hold it.
- **Confirm rather than guess.** Before flashing anything:

  ~~~sh
  esptool --port PORT chip_id
  ~~~

  If it names the wrong chip, unplug, rotate 180°, reconnect. `esptool` refusing with *"This chip is ESP32, not ESP32-S3"* is not an error to work around — it is the orientation indicator working correctly.
- **C-to-C cables make this non-deterministic.** With a Type-A-to-C cable the orientation is fixed by how you insert the C end. With a **C-to-C** cable, which pair is used is negotiated by the host-side mux, so flipping either end may or may not change anything. `nkinnan` documents exactly this on the clone board: *"If using a C-C cable, which ESP you're talking to will depend on which signal line pair the host-side mux selects."* **Use an A-to-C cable for development.** Waveshare's own "Components Preparation" list specifies *"USB cable (Type-A male to Type-C male) x1"* — now you know why.
- **A subtlety the FAQ omits:** the bridge `U10` drives the ESP32's `EN` from `RTS#` and `IO0` from `DTR#`. Serial terminals that assert DTR/RTS on port open will reset the secondary chip or drop it into the bootloader unexpectedly. If a monitor session dies the instant you connect, disable DTR/RTS assertion in your terminal program. This is a *different* failure from the orientation one and flipping the cable will not fix it.

See [dual-mcu-architecture.md](dual-mcu-architecture.md) and [development.md](development.md).

---

## 2. "How to use this product?"

> **Q: How to use this product?**
>
> Volos has released a video demonstrating the use of this product. Click the [link](https://www.youtube.com/watch?v=5G4W3irHkks) to watch the video.

### Commentary

The vendor's answer to "how do I use the thing I bought" is *a link to a third party's YouTube video*. The same link also appears at the top of section 4.

For a written equivalent covering all the preinstalled apps (nine documented, plus a tenth found on the shipped SD card), see **[factory-demo-apps.md](factory-demo-apps.md)** in this folder. Note this is a **different** Volos video from the one in the wiki's Project Resources list (`8pHF0OAG2TI`); both are catalogued in [wiki-resource-links.md](wiki-resource-links.md).

---

## 3. "Failed to set up the VSCode environment?"

> **Q: Failed to set up the VSCode environment?**
>
> First consider the network issue, try switching to another network.

### Commentary

Thin, but not wrong for the intended audience — and it is aimed at a real problem. The Espressif IDF VS Code extension bootstraps by downloading the ESP-IDF tree plus a toolchain bundle (several GB) from `github.com` and `dl.espressif.com`. In mainland China both are slow or intermittently blocked, which is the failure mode Waveshare is actually describing.

Practical additions:

- Espressif mirrors the tooling. Set `IDF_GITHUB_ASSETS=dl.espressif.cn` and use `https://mirrors.tuna.tsinghua.edu.cn/git/esp-idf.git` as the clone source, or select the mirror in the extension's setup wizard.
- Failures are frequently **partial downloads** rather than outright refusals. Clear `~/.espressif/dist/` before retrying, or the installer will keep validating the same truncated archive.
- **Path length and spaces break the Windows toolchain.** Install to a short ASCII path such as `C:\esp\`, not under a profile directory containing spaces or non-ASCII characters.
- If you only need to flash the prebuilt factory images, you do not need any of this — `esptool` alone suffices. See [factory-firmware.md](factory-firmware.md).

The wiki links its own generic tutorial: [Install Espressif IDF Plugin](https://www.waveshare.com/wiki/Install_Espressif_IDF_Plugin_Tutorial).

---

## 4. "Error when compiling an Arduino program?"

> **Q: Error when compiling an Arduino program?**
>
> - Check if the Arduino IDE → Tools is correctly configured
> - Is the ESP32 version in Arduino consistent with the demo requirement?

### Commentary

"Consistent with the demo requirement" means the board package table in wiki §5.1.2: **`esp32 by Espressif Systems` ≥ 3.2.0**. Version skew here is a genuinely common cause of failure, because the 2.x → 3.x transition changed the ESP-IDF version underneath the Arduino core and broke a large amount of peripheral API surface. A 2.x core will not build these examples.

"Tools is correctly configured" is doing a lot of unexplained work. The settings that matter, corroborated by community projects (see [examples/catalog.md](examples/catalog.md)):

| Setting | Value |
|---|---|
| Board | **ESP32S3 Dev Module** (not "ESP32 Dev Module" — that is the *other* chip) |
| Flash Size | **16 MB (128 Mb)** |
| PSRAM | **OPI PSRAM** — omitting this is the classic cause of allocation failures in the LVGL demo |
| Flash Mode | QIO 80 MHz |
| USB CDC On Boot | **Enabled** if using the S3's native USB for the serial monitor |
| Partition Scheme | one with ≥ 4 MB app if the sketch is large |

Also install the bundled libraries **offline** where the wiki demands it — LVGL **8.4.0** in particular. LVGL 9.x is not API-compatible and the Library Manager will happily give it to you.

---

## 5. "How to deal with the first compilation of the program being extremely slow?"

> **Q: How to deal with the first compilation of the program being extremely slow?**
>
> It's normal for the first compilation to be slow, just be patient.

### Commentary

Correct. The first build compiles the entire ESP-IDF/Arduino core and LVGL from source; subsequent builds reuse the cache. Ten to thirty minutes is normal, and the LVGL demo is the slowest.

If the *second* build is also slow, that is a real problem — usually antivirus scanning every object file as it is written. Exclude the build directory and `~/.espressif` / `%USERPROFILE%\AppData\Local\Arduino15`.

---

## 6. "How to handle the display 'waiting for download...' on the serial port after successfully ESP-IDF flashing?"

> **Q:** …
>
> If there is a reset button on the development board, press the reset button; if there is no reset button, please power it on again.

### Commentary

The chip is sitting in the ROM serial bootloader waiting for another download instead of running the image you just flashed — a normal post-flash state when the tool did not (or could not) trigger an automatic reset.

**This board has no reset button**, so the second clause applies: use the **power switch**. The wiki's own BIN-flashing procedure ends with the same instruction — *"After flashing is complete, toggle the switch to reboot the device."*

The board *does* have an **ESP32-S3 BOOT button**, described as *"Press and hold the button, power on again to enter download mode."* Do not confuse the two: BOOT gets you *into* the bootloader, the power switch gets you *out*.

---

## 7. "What should I do if I can't find the AppData folder?"

> **Q: What should I do if I can't find the AppData folder?**
>
> - Some AppData folders are hidden by default and can be set to show.
> - English system: Explorer → View → Check "Hidden items"
> - Chinese system: File Explorer → View → Display → Check "Hidden Items"

### Commentary

Generic Windows advice, relevant because Arduino's ESP32 package and board definitions live under `%USERPROFILE%\AppData\Local\Arduino15\`. You can also type `%LOCALAPPDATA%` directly into the Explorer address bar without changing any settings.

---

## 8. "How do I check the COM port I use?"

> **Q: How do I check the COM port I use?**
>
> **Windows system:**
> ① View through Device Manager: Press Windows + R to open the "Run" dialog; input `devmgmt.msc` and press Enter to open the Device Manager; expand the "Ports (COM and LPT)" section, where all COM ports and their current statuses will be listed.
> ② Use the command prompt to view: Open the Command Prompt (CMD), enter the `mode` command, which will display status information for all COM ports.
> ③ Check hardware connections: If you have already connected external devices to the COM port, the device usually occupies a port number, which can be determined by checking the connected hardware.
>
> **Linux system:**
> ① Use the `dmesg` command to view: Open the terminal.
> ① Use the `ls` command to view: Enter `ls /dev/ttyS*` or `ls /dev/ttyUSB*` to list all serial port devices.
> ③ Use the `setserial` command to view: Enter `setserial -g /dev/ttyS*` to view the configuration information of all serial port devices.

*(The duplicated "①" numbering in the Linux list is verbatim from the source.)*

### Commentary

Two omissions matter **specifically on this board**:

- **`ls /dev/ttyUSB*` will not find the ESP32-S3.** In the S3 orientation the board enumerates as a native **USB Serial/JTAG** device — `/dev/ttyACM*` on Linux, `/dev/cu.usbmodem*` on macOS. Only the *other* orientation, going through the `U10` bridge, produces `/dev/ttyUSB*` (`/dev/cu.usbserial-*` on macOS). **The device node name tells you which MCU you are about to flash** — a far more reliable indicator than remembering which way up the plug was.
- On Linux you likely need group membership: `sudo usermod -aG dialout $USER`, then log out and back in. Permission errors here look exactly like "no port found".

Best single command regardless of platform:

~~~sh
esptool --port PORT chip_id
~~~

---

## 9. "Why does the program flashing fail when using a MAC device?"

> **Q: Why does the program flashing fail when using a MAC device?**
>
> Install [MAC Driver](https://files.waveshare.com/wiki/common/CH34XSER_MAC.7z) and flash again.

### Commentary

This is a **CH34x** USB-UART driver, which tells us something the schematic annotation left open: the unidentified `U10` bridge is a **WCH CH34x-family part**. It also tells you this FAQ entry only applies to **one of the two orientations** — the ESP32-U4WDH path. The ESP32-S3's native USB needs no driver on any modern OS.

The driver is retained locally at `artifacts/tools/CH34XSER_MAC.7z` (4,123,873 bytes).

On recent macOS, WCH's kernel extension is largely superseded: macOS 11+ ships a built-in `AppleUSBCHCOM` driver that handles most CH34x devices, and installing WCH's kext can *conflict* with it. Try the board **without** any driver first and look for `/dev/cu.usbserial-*` or `/dev/cu.wchusbserial*`. Only install WCH's package if nothing enumerates. Note that `svwhisper`'s flashing instructions (see [examples/catalog.md](examples/catalog.md)) use plain `/dev/cu.usbserial-*` on macOS with no mention of installing anything.

---

## 10. "How to choose lithium batteries?"

> **Q: How to choose lithium batteries?**
>
> Normal 3.7 V–4.2 V lithium battery, and exposed PH1.25 battery holder on the development board.

### Commentary

3.7 V nominal / 4.2 V fully charged is an ordinary single-cell LiPo. The product page specifies a **102035** cell for the bundled option.

Note the **connector-designation conflict**: this FAQ says **PH1.25**, while the wiki's own Onboard Resources list calls the same part an **"MX1.25 Lithium battery socket"**. 1.25 mm pitch is consistent across both names, so a standard 1.25 mm 2-pin JST-compatible LiPo connector is what you want — but **polarity is not standardised across vendors on these connectors.** Verify with a meter before plugging in an unknown battery; reversed polarity on a LiPo input is not a recoverable mistake. This conflict is tracked in [gaps-and-conflicts.md](gaps-and-conflicts.md).

The wiki has a separate **section 2, "Lithium Battery Installation"**, whose entire content is an embedded video: <https://www.youtube.com/watch?v=RUIXx_-BYDg>. There is no written installation procedure.

---

## 11. "How to use SquareLine Studio to design interfaces?"

> **Q: How to use SquareLine Studio to design interfaces?**
>
> Please refer to [SquareLine Studio tutorial](https://www.waveshare.com/wiki/Waveshare_SquareLine_Studio).

### Commentary

SquareLine Studio is a commercial WYSIWYG designer that exports C source against LVGL. It is the practical way to build a UI for this panel without hand-writing widget trees. Waveshare links only its own generic tutorial page — nothing board-specific, and in particular **no ready-made 360×360 round board profile** for this product.

Points that matter for this board:

- **Match the LVGL version.** The bundled library is **8.4.0**; SquareLine must be set to an 8.x export target. An LVGL 9 export will not compile against this project.
- Create a **360×360** project. The panel is round, so keep interactive elements inside the inscribed circle — roughly a 255 px square is fully safe, or design radially.
- **A working reference exists.** `joshuacant/BlueKnob` ships its complete SquareLine project as `BlueKnob-UI` and documents the one real gotcha: *"Squareline Studio unfortunately stores paths in a non-relative format so you will need to set the 'Project Export Root' and 'UI Files Export Path' manually."* That project is retained locally under [`examples/selected/`](examples/) — it is a far more useful starting point than the vendor tutorial.

---

## Additional vendor advisories (not in the FAQ section)

Ten `{{Note}}` boxes appear in the body of the wiki. The ones with real content:

| Where | Advisory |
|---|---|
| §3.3 Components Preparation | > "Before operating, it is recommended to browse the table of contents to quickly understand the document structure. For smooth operation, **please read the FAQ carefully to understand possible problems in advance.** All resources in the document are provided with hyperlinks for easy download." — flagged `warn`, the strongest severity used on the page |
| §5.1.1 Arduino install | > "The environment setup is carried out on the **Windows 10** system, Linux and Mac users can access [Arduino-esp32 environment setup](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html) for reference" |
| §6.1.1 VS Code install | > "The environment setup is carried out on the Windows 10 system, Linux and Mac users can access [ESP-IDF environment setup](https://docs.espressif.com/projects/esp-idf/en/v5.1.4/esp32s3/get-started/windows-setup.html) for reference" — **note the pinned `v5.1.4`** |
| §5.2 / §6.2, SD card demos | > "How to know more about the Arduino ESP32 libraries which explain the use of TF card? Please refer to [Arduino ESP32 library TF card use](https://github.com/espressif/arduino-esp32/tree/master/libraries/SD)" |
| §5.2 / §6.2, LVGL demos | > "For more learning and use of LVGL, please refer to [LVGL official documentation](https://docs.lvgl.io/master/intro/introduction/index.html)" — links `master`, though the board ships **8.4.0**; use <https://docs.lvgl.io/8.4/> instead |

That the vendor explicitly tells you to read the FAQ **before** starting, at `warn` severity, is a reasonable signal that the orientation problem in entry 1 generates most of their support load.

---

## Problems the vendor FAQ does not cover

Recorded here because they are well-attested elsewhere in this folder or in community projects, and a reader arriving at a troubleshooting page will want them.

| Symptom | Cause | Where it is treated |
|---|---|---|
| **No audio at all**, from any app, including S3-side local playback | The PCM5100A `XSMT` mute is on **ESP32-U4WDH GPIO32** (high = un-muted). Reflashing the secondary with firmware that never raises it silences the board globally — including audio originating on the S3, which cannot reach that pin. | [gaps-and-conflicts.md](gaps-and-conflicts.md), [classic-bluetooth.md](classic-bluetooth.md) |
| **Battery drains fast when idle** | The secondary ESP32 is permanently powered with no S3-controllable enable and draws **~50 mA** running stock firmware. Two independent community projects exist solely to deep-sleep it. | [examples/catalog.md](examples/catalog.md) — `svwhisper/lyngdorf-secondary-sleep`, `joshuacant/BlueKnob` |
| **Display shows garbage or stays blank** with a "standard SPI" driver | The panel needs **QSPI with 32-bit command frames at 40 MHz**, not 8-bit SPI at 20 MHz. Driver identity is disputed (marketed ST77916, code says SH8601). | [examples/catalog.md](examples/catalog.md), [gaps-and-conflicts.md](gaps-and-conflicts.md) |
| **Serial monitor disconnects on open** (secondary MCU only) | `U10` drives `EN` from `RTS#` and `IO0` from `DTR#`. Disable DTR/RTS assertion. | [development.md](development.md) |
| **Large `read-flash` operations fail** when backing up firmware | Reported on the clone board; the workaround is chunked 4 KB reads with retry, in boot mode. | [examples/catalog.md](examples/catalog.md) — `nkinnan` |
| **No Bluetooth Classic from your S3 sketch** | Silicon limitation. No library can add it. | [classic-bluetooth.md](classic-bluetooth.md) |

---

## Section 10, "Support"

The wiki's final section is the MediaWiki template `{{Servicebox1}}` — Waveshare's standard boilerplate service block (working hours, ticket/email contact). It carries **no board-specific content**, which is why it is not reproduced here.

---

## Cross-references

- [development.md](development.md) — toolchain versions and setup
- [dual-mcu-architecture.md](dual-mcu-architecture.md) — why entry 1 exists
- [factory-demo-apps.md](factory-demo-apps.md) — the preinstalled apps
- [factory-firmware.md](factory-firmware.md) — restoring the shipped image
- [gaps-and-conflicts.md](gaps-and-conflicts.md) — unresolved contradictions
- [wiki-resource-links.md](wiki-resource-links.md) — every URL the wiki offers
