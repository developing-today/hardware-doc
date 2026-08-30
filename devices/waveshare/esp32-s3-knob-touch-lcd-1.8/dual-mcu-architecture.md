# Dual-MCU architecture: how the ESP32-S3 and the ESP32-U4WDH work together

> Device: [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](README.md) (product 31623).
> Analysis date **2026-08-22**. All findings below were re-derived from the artifacts in `artifacts/` for this document; nothing is carried over on trust.

This board is not "an MCU with a helper chip". It is **two complete, independent ESP32-family SoCs** on one PCB — separate crystals, separate antennas, separate flash, separate reset circuits, separate firmware images, separate USB paths. They share exactly three things: a 3.3 V rail, one analog audio DAC, and **one two-wire UART**.

Almost every surprising thing about this product — why your serial port disappears, why the SD card is invisible to the Bluetooth stack, why audio goes silent after you reflash "the board", why one chip can be updated over the air and the other cannot — is a direct consequence of that split. This page is the full treatment.

## Evidence labels

| Label | Meaning |
|---|---|
| **[SCH]** | Read off the official schematic PNGs in `artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/` (5 sheets) |
| **[FW]** | Extracted from the factory binaries in `artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/` — image headers, partition tables, app descriptors, embedded strings |
| **[SRC]** | Read in the official demo source tree `artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/{Arduino,ESP-IDF}/` |
| **[DOC]** | Vendor datasheet or Espressif document held in `artifacts/datasheets/` |
| **[WEB]** | Waveshare's own wiki or product page, from the HTML snapshots in `artifacts/source-snapshots/` |
| **[INF]** | Inference, arithmetic, or convention. **Not** established by any of the above. Treat as a hypothesis |

Where the record is thin, this document says so rather than filling the gap.

---

## 1. The USB-C orientation flip

### 1.1 What Waveshare actually says

Two independent vendor statements, quoted verbatim.

Product page, in the hardware-callout table **[WEB]** (`waveshare-product-31623-2026-08-21.html`):

> **Type-C connector** — Switching ESP32-S3 USB or ESP32 UART based on Type-C plug orientation

Wiki FAQ, under *"Why can't the program be flashed?"* **[WEB]** (`waveshare-wiki-wikitext-oldid-111069.txt`, lines 946–953):

> This product features two onboard chips, ESP32-S3 and ESP32. The two insertion orientations of the Type-C plug connect to different download channels.
>
> - If programming fails, the serial port is not found, or the connection cannot be established, please perform the following steps first:
>   - 1. Disconnect the Type-C cable;
>   - 2. Flip the Type-C plug 180°;
>   - 3. Re-insert the cable and attempt programming again.

And in the BIN-flashing walkthrough **[WEB]** (line 824 ff.), Waveshare's own instruction is to *probe* rather than assume:

> 5. The board has two MCUs, ESP32 and ESP32-S3. We first identify which board the COMx connected to the computer is […]
>    1. Enter the command: `esptool.exe --port COMx --baud 115200 chip_id`
>    3. Confirm that it is ESP32 or ESP32S3, you can check the chip type

That is the whole of the vendor documentation on the subject. There is no description of the mechanism.

### 1.2 ⚠ Evidence boundary — the schematic does not show this

**The five published schematic sheets contain no USB Type-C receptacle symbol at all.** Verified across all five PNGs. Both USB differential pairs appear only as nets, and their only drawn endpoints are:

| Net | Drawn endpoint | Sheet |
|---|---|---|
| `USB_DP` / `USB_DN` | ESP32-S3 GPIO20 / GPIO19 (native USB-OTG), and connector `CN1` | `2_ESP32S3-R8.png`, `1_LCD&POWER.png` **[SCH]** |
| `USB_ESP32_DP` / `USB_ESP32_DN` | USB-UART bridge `U10` pins 1/2, and connector `CN1` | `3_ESP32-CHIP.png`, `1_LCD&POWER.png` **[SCH]** |

So the *two endpoints* are firmly established **[SCH]**, but **the orientation-selection topology is not**. It could be a passive arrangement that simply wires one pair to the receptacle's A-side D+/D− pins and the other to the B-side pins (the simplest and most likely explanation, since a Type-C plug only ever mates one of the two D+/D− pin pairs); it could be a CC-sensing mux IC; it could be something else. **This document does not guess.** Tracked in [gaps and conflicts](gaps-and-conflicts.md) and the [USB-C interface record](../../../components/generic/usb-c-interface/README.md).

Everything in §1.1 is therefore **[WEB]-only**: vendor-asserted product behaviour, corroborated by community reports, not confirmed by any schematic we hold.

### 1.3 What each orientation gives you

| | Orientation A | Orientation B |
|---|---|---|
| Reaches | **ESP32-S3R8** (`U2`) | **ESP32-U4WDH** (`U14`) |
| Path | S3's **native USB-OTG** peripheral, GPIO19/GPIO20, straight into the chip **[SCH]** | External **USB-UART bridge `U10`** → the U4WDH's **UART0** (GPIO1/GPIO3) **[SCH]** |
| Host sees | A USB device implemented *by the S3's firmware* — USB-CDC-ACM if the app enables it, or USB-Serial-JTAG, or nothing at all if the app disables USB | A **fixed USB-serial bridge chip**, enumerating whether or not the ESP32 is even running |
| `esptool … chip_id` reports | `ESP32-S3` | `ESP32-U4WDH` |
| Download-mode entry | S3 `BOOT` button + power cycle **[WEB]**, or USB-Serial-JTAG auto-reset | Automatic: `U10` `RTS#` → `ESP32_EN`, `U10` `TNOW/DTR#` → `ESP32_IO0` **[SCH]** |
| Present when firmware is crashed/erased | Depends — a bricked or USB-disabled S3 app may not enumerate; the S3 ROM download stub does | **Always** — the bridge is a separate chip on the 3V3 rail |

**Which orientation is "A" is not labelled on the product and cannot be predicted.** There is no marking, no LED, no silkscreen arrow. You determine it by plugging in and looking.

### 1.4 How to tell which mode you are in

Three tells, in order of reliability:

**1. Ask esptool.** Waveshare's own recommendation **[WEB]**:

```sh
esptool --port /dev/ttyUSB0 chip_id     # or COMx on Windows
# "Chip is ESP32-S3 (QFN56) …"        -> you are on the S3, native USB
# "Chip is ESP32-U4WDH (revision …)"  -> you are on the secondary MCU, via the bridge
```

**2. Look at what enumerated.** The two paths look completely different to the host:

| Symptom | Meaning |
|---|---|
| A **USB CDC** / composite device attributed to Espressif (VID `0x303A`), device node appearing and disappearing when the S3 resets | **S3 native USB.** The port is created by S3 firmware, so it vanishes on every reset and reappears when the app re-enumerates |
| A **WCH USB-serial bridge**, VID:PID **`1A86:7523`**, node stable across target resets, present even with the target held in reset | **The `U10` bridge → ESP32-U4WDH** |

✅ **Update 2026-08-21 — the bridge is identified and you *can* name the driver.** `U10` is a **WCH CH340X** (MSOP-10). The schematic symbol carries no part number, but the pin order, the compound `TNOW/DTR#` pin name and `R14` 5.1 kΩ wired **between pin 6 and pin 5** are, together, WCH CH340 datasheet §5.3 option ② and nothing else. Enumerates as **`1A86:7523`** — WCH's own driver personality table is the source. Full evidence chain, candidate elimination and confirmation procedure in the [USB-UART bridge record](../../../components/wch/ch340x/README.md).

Drivers: **Linux** — nothing, `ch341` is in-tree. **macOS** — WCH `CH34xVCPDriver` (Waveshare mirrors it in this board's `artifacts/tools/CH34XSER_MAC.7z`); macOS 11+ may handle it in-box. **Windows** — `CH341SER` (*not* `CH343SER`), usually resolved by Windows Update. This supersedes the earlier "do not tell users to install a specific driver" caution.

**3. Look at the boot log.** If you get a serial port and it prints an ESP-IDF banner naming the chip, that settles it. Note the S3's UART0 console is **not** routed to the bridge **[SCH]** — S3 console output goes over its native USB, not over `U10`.

### 1.5 Flashing each MCU

Both images are **merged images written at offset `0x0`** — they contain bootloader, partition table and app. Do not flash them at `0x1000` or `0x10000`. Verified: both binaries carry an ESP32 image magic `0xE9` at file offset 0 and a valid partition table at `0x8000` **[FW]**.

```sh
# --- Orientation giving the ESP32-U4WDH -------------------------------
esptool --chip esp32   --port PORT chip_id          # confirm ESP32-U4WDH first
esptool --chip esp32   --port PORT --baud 921600 \
        read_flash 0x0 0x400000 esp32-u4wdh-backup.bin      # 4 MB, BACK UP FIRST — see §6.2
esptool --chip esp32   --port PORT --baud 921600 \
        write_flash -z 0x0 ESP32-KNOB_ESP32_0.bin

# --- Flip the plug 180°, re-enumerate ---------------------------------

# --- Orientation giving the ESP32-S3R8 --------------------------------
esptool --chip esp32s3 --port PORT chip_id          # confirm ESP32-S3
esptool --chip esp32s3 --port PORT --baud 921600 \
        write_flash -z 0x0 WX-ESP32S3-KNOB_V1.2.bin
```

Waveshare's wiki gives the same two-step sequence and is explicit that it is two separate operations on two separate COM ports **[WEB]**: *"The board has two MCUs onboard, namely ESP32 and ESP32S3. First, flash the bin file to the ESP32 […] Next, flash the ESP32-S3 bin file […] Note that it needs to be changed to ESP32S3."*

### 1.6 Risks and gotchas

| Gotcha | Why | Mitigation |
|---|---|---|
| **`--chip` forcing defeats the safety net** | `esptool` normally refuses a mismatched image on the chip-ID check — but only if you let it autodetect. Forcing `--chip esp32` while physically connected to the S3 bypasses that | Always run `chip_id` **first**, with no `--chip`, and read the answer |
| **Flashing an `esp32s3` image into the U4WDH (or vice versa)** | Produces a chip that boot-loops. It is recoverable — ROM download mode still works — but you will think you bricked it | See above. Also note the U4WDH has only **4 MB** of flash **[FW]**; the S3 image is 2.04 MB of a 16 MB layout and its partition table declares partitions past 4 MB, so it cannot work |
| **A serial terminal resets the ESP32 on open** | On this board `U10` `RTS#` drives `EN` and `DTR#` drives `IO0` **directly**, not through the usual two-transistor cross-coupled network **[SCH]**. Any terminal that asserts DTR/RTS on port open can reset the chip or drop it into the bootloader | Disable DTR/RTS assertion in your terminal (`picocom --lower-dtr --lower-rts`, or uncheck the boxes in your IDE monitor) |
| **The S3 port disappears mid-session** | Native USB is implemented in S3 *firmware*. Reset, crash, or reflash and the device node goes away | Expected. Use `--before default-reset` and let esptool handle it; re-open the port after reset |
| **Flipping the plug does not seem to change anything** | Some Type-C cables, hubs and captive-cable adapters are electrically symmetric or re-orient internally | Try a different cable, and try a direct port rather than a hub |
| **Flashing one MCU does not touch the other** | They have entirely separate flash | A half-updated board misbehaves *subtly* rather than failing cleanly — see §6.3 |
| **You cannot talk to both MCUs at once over USB** | One receptacle, one orientation at a time | To debug the inter-MCU link live you need a logic analyser on the two GPIOs, or a wire to the second PH1.27 header |

---

## 2. The inter-MCU link: a two-wire UART

### 2.1 Physical layer — fully established **[SCH]**

| Direction | Source pin | Net | Destination pin |
|---|---|---|---|
| ESP32-U4WDH → ESP32-S3 | U4WDH **GPIO23** (package pin 36) | `ESP32S3_RX` | S3 **GPIO48** |
| ESP32-S3 → ESP32-U4WDH | S3 **GPIO38** | `ESP32S3_TX` | U4WDH **GPIO18** (package pin 35) |

Cross-referenced against [pinouts and buses](pinouts-and-buses.md) §S3 pin table (rows 38 and 48) and §U4WDH package-pin table (pins 35 and 36); both derive from sheets `2_ESP32S3-R8.png` and `3_ESP32-CHIP.png` **[SCH]**.

Note the net *names* are written from the **S3's** point of view — `ESP32S3_RX` is the wire the S3 receives on, driven by the ESP32. Do not read them as "the ESP32's RX".

**Two wires. That is the entire interface.** There is:

- **no third or fourth wire** — no RTS, no CTS, no DTR, no DSR;
- **no reset line** — neither chip can reset the other;
- **no interrupt / attention line** — neither chip can signal "wake up, I have something" out of band;
- **no shared clock**, no SPI, no I2C, no shared memory, no shared GPIO handshake;
- **no other channel of any kind.** Verified by walking all five schematic sheets for nets touching both `U2` and `U14`: the only ones are `3V3`, `GND`, the two UART wires, and the audio path through the CH445P mux (which is analog switching, not communication) **[SCH]**.

Series/damping resistors on these two nets are **not established** — the U4WDH README's pin table and the schematic transcription do not record any, but absence in a raster-PNG transcription is weak evidence. **[INF]**: assume direct 3.3 V CMOS.

### 2.2 Full duplex, no flow control — and why that matters

Because TX and RX are **separate, cross-connected wires**, this is a **full-duplex** link. Both chips can transmit simultaneously and neither transmission interferes with the other. This is not a shared bus; there is no arbitration, no collision, no turnaround delay, no half-duplex direction-switch dead time. Each direction is an independent 3.3 V CMOS point-to-point signal.

That is the good news. The bad news:

**There is no hardware flow control.** RTS/CTS would require two more wires and those wires do not exist **[SCH]**. Consequently:

- A transmitter has **no way to know** whether the receiver's FIFO is full. It will happily keep shifting bytes onto the wire.
- The ESP32 UART RX FIFO is **128 bytes** deep on both chips **[DOC]** (ESP32 and ESP32-S3 technical reference manuals, UART chapter). ESP-IDF's `uart_driver_install()` adds a software ring buffer on top, drained by an ISR — but if the ISR is starved (a long critical section, a flash write with the cache disabled, a `WiFi`/`BT` stack burst, an LVGL frame flush), the *hardware* FIFO overruns first and bytes are lost silently.
- **Flow control on this link must therefore be implemented in software**, in the protocol itself. And it is: the factory protocol is **pull-based** for bulk data — the receiver asks for each packet by number (`[I] [UART] Need packet:%d` **[FW]**) rather than the sender pushing. That is exactly the design you arrive at when you have no RTS/CTS. See §2.4.
- Software flow control using XON/XOFF is **not** an option for this link, because the payload is binary (JPEG data) and would collide with the `0x11`/`0x13` control bytes.

If you write your own firmware for both ends, **do the same thing**: acknowledge-and-request, or a windowed protocol, or a strict request/response discipline where neither side ever sends unsolicited bulk. Do not open a raw byte pipe at 2 Mbaud and hope.

### 2.3 Bandwidth — what this link can and cannot carry

#### 2.3.1 The configured baud rate is **UNKNOWN**

This must be stated plainly, because it is the single most-wanted number on this page and we do not have it.

**Searched and found nothing:**

- **The demo tree**: every occurrence of a baud rate in `Arduino/examples/` and `ESP-IDF/` is a *console* baud — `CONFIG_ESP_CONSOLE_UART_BAUDRATE=115200`, `CONFIG_ESPTOOLPY_MONITOR_BAUD=115200`, `CONFIG_MONITOR_BAUD=115200` — in `sdkconfig` files only. **No `.c`, `.h`, `.cpp` or `.ino` file in the entire demo tree contains `uart_driver_install`, `uart_param_config`, `uart_set_pin`, `UART_NUM_1`, `UART_NUM_2`, `Serial1` or `Serial2`.** **[SRC]** (verified 2026-08-22 by exhaustive search excluding the vendored LVGL copy).
- **Both firmware binaries**: no baud-rate literal is recoverable from strings. ESP-IDF does not log the configured baud, and the value reaches the hardware as a computed clock divider written to `UART_CLKDIV_REG` at runtime. It is present only as an immediate operand inside compiled code. **[FW]**

**How to obtain it** (in ascending order of effort):

1. **Auto-baud with a logic analyser** on S3 GPIO48/GPIO38 (or U4WDH pins 36/35) while the stock firmware is running and you tap a track-change on a paired phone. Sigrok/PulseView and Saleae Logic both auto-detect. This takes minutes and is the recommended route.
2. **Disassemble.** Both images are present locally with known hashes (§5.3). The translation units are named in the debug strings — `../main/uart1.c` on the ESP32 and `src/driver/uart1.cpp` on the S3 **[FW]** — so the relevant code is small and identifiable. Look for the `uart_param_config` call site and read the `.baud_rate` initialiser.
3. **Instrument.** Flash your own S3 firmware that configures UART1 on GPIO38/48 and sweeps candidate bauds while looking for framing errors against the still-stock ESP32.

Until one of those is done, **treat the baud rate as unknown.** Do not assume 115200 because the console is 115200 — that is a different UART on a different peripheral instance.

#### 2.3.2 Throughput arithmetic

With the near-universal **8N1** framing (1 start bit + 8 data bits + 1 stop bit, no parity), each byte occupies **10 bit-times**. So:

```
bytes_per_second = baud / 10
```

**[INF]** on the 8N1 assumption for this specific link — 8N1 is the ESP-IDF default (`UART_DATA_8_BITS`, `UART_PARITY_DISABLE`, `UART_STOP_BITS_1`) and overwhelmingly the convention, but it is not confirmed for the factory firmware. If parity were enabled it would be 11 bit-times/byte and every figure below drops ~9%.

| Baud | Bytes/s | KB/s (×1000) | KiB/s (×1024) | Mbit/s on the wire |
|---:|---:|---:|---:|---:|
| 115 200 | 11 520 | 11.5 | 11.25 | 0.115 |
| 230 400 | 23 040 | 23.0 | 22.5 | 0.230 |
| 460 800 | 46 080 | 46.1 | 45.0 | 0.461 |
| 921 600 | 92 160 | 92.2 | 90.0 | 0.922 |
| 1 500 000 | 150 000 | 150.0 | 146.5 | 1.500 |
| 2 000 000 | 200 000 | 200.0 | 195.3 | 2.000 |
| 3 000 000 | 300 000 | 300.0 | 292.9 | 3.000 |
| **5 000 000** | 500 000 | 500.0 | 488.3 | 5.000 |

**5 Mbaud is the ceiling.** The ESP32 and ESP32-S3 UART peripherals are specified to **5 Mbps** **[DOC]** (ESP32 datasheet §UART; ESP32-S3 datasheet §UART — "up to 5 Mbps"). That is a silicon maximum under ideal conditions, not a number you should design to. Practically:

- Above roughly **1–2 Mbaud**, with no flow control and both chips running RTOS workloads (Bluetooth stack on one side, LVGL + Wi-Fi + SD on the other), **RX FIFO overruns become the dominant failure mode**. A 128-byte FIFO at 2 Mbaud drains in **640 µs**. Any ISR-blocking event longer than that loses data.
- These are unshielded PCB traces of unknown length with no termination and unknown (probably absent) series damping **[SCH]/[INF]**. Signal integrity at 5 Mbaud is not something to assume.
- Both chips must agree on the divider. The ESP32's UART clock source and any APB frequency scaling (dynamic frequency scaling, light sleep) affect the achieved baud unless `UART_SCLK_REF_TICK`/`UART_SCLK_XTAL` is selected. **If you enable DFS or light sleep on either side, pin the UART clock source**, or your baud will drift.

**Recommendation [INF]:** if you are writing both ends, **921600 is the sensible default** — ~90 KiB/s, comfortably reliable, and standard enough that every tool auto-detects it. Go higher only with a real ack/window protocol and measured error rates.

#### 2.3.3 What that means in practice

Worked figures. All **[INF]** arithmetic on top of the table above; payload sizes are typical, not measured on this device.

**Album cover art — the thing the link is actually for.** AVRCP Cover Art (BIP) thumbnails are small; a 200×200 JPEG is commonly 8–20 KB, and full-size images 30–80 KB.

| Payload | @115 200 | @460 800 | @921 600 | @2 000 000 |
|---|---:|---:|---:|---:|
| 8 KB thumbnail | 0.71 s | 0.18 s | 0.09 s | 0.04 s |
| 20 KB thumbnail | 1.78 s | 0.44 s | 0.22 s | 0.10 s |
| 50 KB cover | 4.44 s | 1.11 s | 0.56 s | 0.26 s |
| 100 KB cover | 8.9 s | 2.2 s | 1.1 s | 0.51 s |

Add protocol overhead (a ≥7-byte header per packet, §2.4) and the round-trip latency of the pull-based request/response cycle — at 115200 a realistic multi-packet transfer runs perhaps 1.3–1.5× the raw figure. **The observable behaviour on the stock firmware — album art visibly popping in a beat after the track changes — is consistent with a sub-second to low-single-digit-seconds transfer, which brackets the plausible baud somewhere in the 115200–921600 range. That is a soft inference from UI feel, not evidence. [INF]**

**Track metadata.** Artist/title/album strings are a few hundred bytes. Even at 115200 that is **tens of milliseconds** — completely free. This is the ideal traffic for the link.

**Control and status frames.** Play/pause/next/volume commands, `Report status` heartbeats **[FW]** — single-digit to low-tens of bytes. Free at any baud.

**❌ What this link absolutely cannot do:**

| Workload | Required rate | Verdict |
|---|---:|---|
| **Raw video to the 360×360 panel**, RGB565 | 259 200 B/frame → **7.78 MB/s at 30 fps** | **Impossible.** 15× over the 5 Mbaud silicon ceiling *for a single frame per second*. At 2 Mbaud you get **0.77 fps**. This is why the LCD hangs off the S3's QSPI bus, not off the UART |
| **One full framebuffer, one-shot** | 259 200 B | 22.5 s @115200; 2.8 s @921600; 0.53 s @5 Mbaud. Even best case, a slideshow at ~2 fps |
| **Uncompressed CD audio**, 44.1 kHz/16-bit/stereo | **176 400 B/s** = 1.764 Mbaud *with zero overhead and zero framing* | Not viable. Needs >2 Mbaud with no margin, no headroom for the protocol, and no tolerance for a single dropped byte |
| **A2DP SBC stream**, ~328 kbps | ~41 000 B/s = ~410 kbaud minimum | Theoretically possible above ~600 kbaud, but pointless — **and this is exactly why the board has a CH445P analog mux instead.** The audio path is hardware-switched I2S, not tunnelled over the UART. See §4.3 |
| **Bulk SD-card file transfer** to the ESP32 | arbitrary | A 4 MB MP3 takes **6 minutes** @115200, **45 s** @921600. Not a design you should build |

**The one-line rule: this link is a control and metadata channel with an occasional small-image bulk mode. It is not a data bus.** Anything larger than "a JPEG thumbnail" belongs somewhere else.

### 2.4 The protocol — what is known and what is not

The wire format is **not documented by Waveshare anywhere**, and — importantly — **no official example uses it** (§3). The only evidence is log and assert strings compiled into the two factory images. Everything below is **[FW]**.

Both sides use **UART1** — not UART0, which is each chip's own console:

| Side | Evidence |
|---|---|
| ESP32-U4WDH | source path string `../main/uart1.c`; task name `task_uart1`; log tags `uart1`, `UART1`; symbol `uart1_task` |
| ESP32-S3 | source path string `src/driver/uart1.cpp`; symbol `void task_uart1(void*)`; boot line `[I] UART1 task started.`; log tag `[UART]` |

#### 2.4.1 What the strings establish

| Established fact | Evidence string | Emitting side |
|---|---|---|
| Frames carry a **command/opcode** field; unknown values are rejected | `[E] [UART] Wrong cmd:%d` | S3 |
| Frames carry a **transfer id**, validated against an expected value | `[E] [UART] Wrong transfer id:%d` | S3 |
| Frames carry an **explicit length**, which is validated | `[E] [UART] Data len wrong:%d` | S3 |
| Cover-art transfers are **multi-packet with a known total announced up front** | `[I] [UART] Recv cover art begin , total packet:%d` | S3 |
| The receiver **requests packets by number** — pull-based flow control / retransmission | `[I] [UART] Need packet:%d` | S3 |
| Transfers complete with a **byte count** | `[I] [UART] Recv cover art ok, size:%u` | S3 |
| Transfers can be **aborted with a reason code** | `[I] [UART] Recv cover stoped,reason:%u` | S3 |
| The S3 **pushes status** to the ESP32 | `[I] [UART] Report status` | S3 |
| The ESP32 sends **AVRCP metadata** over the link | `W (%lu) %s: Uart send meta data error` | ESP32 |
| Cover-art request frames have a **minimum length of 7 bytes** | `W (%lu) %s: Uart send cover art error, rcv data length < 7` | ESP32 |
| The ESP32 tracks a **send id** and a **packet id** as *separate* fields, and validates both | `… bad send id:%u,%u`, `… bad packet id` | ESP32 |
| Transfers are **stateful** — packets outside an active transfer are rejected | `… not in sending` | ESP32 |
| The transmit path can **fail and report it** | `… send failed` | ESP32 |
| Cover art is **JPEG**, decoded from RAM on the S3 | `[I] [IO] Decode jpeg from ram,size :%u`, `[I] [IO] Skip decode cover jpeg` | S3 |
| The S3 can command the ESP32 to **forget the A2DP pairing** | `Clear BT A2DP pair` (S3 UI), `Clearing pair info...` (S3); `PEERADDR` NVS key + `Clear peer addr err,code: %d` (ESP32) | both |

Corroborating context on the ESP32 side **[FW]**: `btc_avrc_ct_cover_art_connect`, `btc_avrc_ct_cover_art_get_image`, `btc_avrc_ct_cover_art_get_linked_thumbnail`, `Peer support Cover Art feature, start connection...`, `Cover Art Client connected`, `obex_main.c`. The ESP32 fetches artwork over Bluetooth OBEX/BIP and then relays it across the UART.

#### 2.4.2 The shape of the protocol

Putting that together, the design is:

> **A length-prefixed, command-coded frame carrying a transfer id, used bidirectionally over a full-duplex link, with a pull-based multi-packet bulk mode for JPEG album art flowing ESP32 → S3, and status/control frames flowing S3 → ESP32.**

The pull-based design is the giveaway that the authors were working around the missing hardware flow control (§2.2): the S3 never gets flooded because nothing arrives that it did not ask for.

The 7-byte minimum on a cover-art *request* frame is consistent with a header along the lines of `{cmd, send/transfer id, packet id (16-bit?), length (16-bit?)}` — but note that **the string only tells us the minimum length the ESP32 will accept, not the field layout.**

#### 2.4.3 ⚠ What is NOT known — do not guess these

- **The byte order** of multi-byte fields.
- **The width** of every field — `cmd`, `transfer id`, `send id`, `packet id`, `length` are all `%d`/`%u` in the format strings, which tells you nothing about the on-wire size.
- **The field order** within the header.
- Whether there is a **sync/preamble byte or magic**, and what it is.
- Whether there is a **checksum or CRC**, and if so which polynomial and over what span. (Neither image contains a UART-specific checksum error string, which is weak evidence *against* one — but the S3 image does contain generic `Checksum failed. Calculated 0x%x read 0x%x` from the bootloader, so absence of a dedicated string proves nothing.)
- Whether payloads are **escaped or byte-stuffed** (they must handle arbitrary JPEG bytes somehow — either explicit length framing with no delimiters, which the `Data len wrong` string suggests, or stuffing).
- The **maximum packet size** and hence the packet count for a given image.
- The **numeric values** of any `cmd` opcode.
- The **timeout and retry policy**.
- The **baud rate** (§2.3.1).
- Whether there is a **handshake/version exchange at boot** — `[I] UART1 task started.` is the only boot-time UART string on the S3.

**No byte layout is reconstructed in this document, and none should be reconstructed from these strings alone.** Anything that claims a specific frame diagram for this board without a logic-analyser capture or a disassembly is fabricated.

#### 2.4.4 If you need the protocol

1. **Don't.** Reflash *both* MCUs with your own firmware and define your own protocol. The link is just two GPIOs; you own both ends. This is by far the sanest path and it is what community projects do. (Back up the factory ESP32 image first — §6.2.)
2. **Sniff it.** Logic analyser on S3 GPIO48 and GPIO38, auto-baud, trigger on a track change. Minutes of work, gives you the real baud and real frames.
3. **Disassemble.** Both images are local with known hashes; `../main/uart1.c` and `src/driver/uart1.cpp` are small, named, identifiable translation units.

---

## 3. Do the demos and preinstalled apps actually use the link?

Two very different answers, and the difference matters a lot to users.

### 3.1 The official demo archive: **no — and there is no ESP32 source at all**

**This is the single most important practical finding in this document, and it is easy to miss.**

`artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/` contains eight Arduino examples and eight ESP-IDF examples. Verified **[SRC]**:

| Check | Result |
|---|---|
| ESP-IDF projects, `CONFIG_IDF_TARGET` | **8 of 8 = `"esp32s3"`.** Zero projects target `esp32` |
| ESP-IDF projects, `CONFIG_ESPTOOLPY_FLASHSIZE` | 8 of 8 = `"16MB"` — the S3's external W25Q128, not the U4WDH's 4 MB |
| `uart_driver_install`, `uart_param_config`, `uart_set_pin`, `UART_NUM_1`, `UART_NUM_2`, `Serial1`, `Serial2` in any `.c`/`.h`/`.cpp`/`.ino` | **zero hits** across the whole tree |
| References to GPIO 38 or GPIO 48 in any example | **zero hits.** (The only `43`/`44` hits are `SENSOR_IRQ`/`SENSOR_RST` in a vendored third-party `SensorLib` example for an unrelated part) |
| Any Bluetooth Classic / A2DP / AVRCP code | **none** |
| Any ESP32-U4WDH source, project, sdkconfig or build file | **none** |

The eight examples are: `01_ADC_Test`, `02_SD_Card`, `03_DRV2605_Test`, `04_Encoder_Test`, `05_WIFI_AP`, `06_WIFI_STA`, `07_Audio_Test`, `08_LVGL_Test`. Every one is a **single-chip S3 peripheral test**. `04_Encoder_Test` reads only **knob 1** (`SW2`, S3 GPIO7/8) — the second knob is physically wired to the U4WDH **[SCH]** and no example can read it. `07_Audio_Test` drives the DAC from the S3 via the mux, without any coordination with the chip that owns the mute line.

**Say this plainly to users:**

> **Waveshare ships no source code whatsoever for the ESP32-U4WDH.** The secondary MCU exists in the published materials only as a **prebuilt binary blob**, `ESP32-KNOB_ESP32_0.bin`. There is no project, no `main/`, no `sdkconfig`, no build instructions, no protocol specification, and no example that talks to it. If you want Classic Bluetooth on this board you are either running Waveshare's opaque blob, or writing that firmware from scratch yourself.

That is not a documentation oversight to be worked around; it is a hard boundary on what you can do with the product out of the box.

### 3.2 The preinstalled factory firmware: **yes, extensively — but only some apps**

The shipped S3 application is **not** built from the demo tree. It is a third-party-authored application (build paths point at `C:/Users/Fei/.platformio/…`, PlatformIO with Arduino-ESP32 3.x **[FW]**) with its own app framework. Its app set, from URI and label strings **[FW]**: `music`, `mjpeg`, `aida64`, a clock/weather app (`/clockbg`, `/saveweather`), a Bluetooth mode, plus a Wi-Fi config portal (`/configwifi`, `/wifilist`) and a web control panel (`/getstatus`, `/docmd`, `/save`).

| Preinstalled app | Uses the inter-MCU UART? | What crosses the link | Evidence |
|---|---|---|---|
| **Bluetooth Music Player** | **Yes — heavily. This is the link's whole reason to exist** | ESP32 → S3: AVRCP **track metadata** (`Uart send meta data error`), multi-packet **JPEG album cover art** (`Recv cover art begin , total packet:%d`). S3 → ESP32: **status/control** (`Report status`), **playback control** (S3 UI shows play/pause/volume; ESP32 holds the AVRCP CT that issues `esp_avrc_ct_send_passthrough_cmd`), **clear pairing** (`Clear BT A2DP pair` → ESP32 `PEERADDR`/`Clear peer addr err`) | **[FW]** both images |
| **AIDA64 secondary screen** | **No** | Pure S3 Wi-Fi feature. The S3 polls the PC over HTTP: `[I] [APP] Get aida64 info err:%d, retry after:%u ms`, URI `/aida64`, config field `HostIP`. Wiki confirms the workflow is entirely Wi-Fi/LAN **[WEB]** | **[FW]**, **[WEB]** |
| **MJPEG video player** | **No** | Reads `.mjpeg` files from the microSD (`Please copy MJPEG files`, `No MJPEG files`, `%s/boot.mjpeg`, `default_timer_bg.mjpeg`) and decodes them on the S3's JPEG decoder. Both the storage and the display are S3-side. Also §2.3.3: streaming video over this link is arithmetically impossible | **[FW]** |
| **Local music player (SD)** | **No** for the audio; **possibly** for mux/mute arbitration | Decoders are all S3-side (`Failed to decode mp3/flac/alac frame`, M4A parser, `44.1k/48k Hz music`). Files come off the S3's SD card. But the **`XSMT` mute pin belongs to the ESP32** (§4.3), so *something* has to un-mute — **[INF]**, mechanism not established | **[FW]** |
| **Spectrum analyser** | **No** — *resolved 2026-08-23, supersedes the earlier "not confirmed" finding* | **The app exists, and it is microphone-driven.** The wiki documents it as a distinct launcher entry, §4.2.6 "pickup spectrum analyzer": *"You can capture the sounds around you and display them on the screen in a spectral manner"* **[WEB]**. The source is the **S3's own PDM microphone** (GPIO45/46), so the whole path is S3-local — PDM → I2S RX → FFT → LVGL. It does **not** visualise Bluetooth audio, so the UART-relay concern raised in the earlier analysis **does not arise**. Corroborated by the as-shipped SD card, which carries a dedicated `night7/rhythmbg.mjpeg` backdrop, as every other themed app has one. See [factory-demo-apps.md §3.6](factory-demo-apps.md) | **[WEB]**, **[SRC]** SD card |
| **Clock / weather** | **No** | S3 Wi-Fi + `/saveweather`, `CityCode`, `apikey`. **The weather half is a real app**, confirmed 2026-08-23: the shipped SD card carries a `weather/` directory of 19 condition graphics with day/night variants and a `nowifi` offline-fallback. **The wiki never documents it** — §4 lists nine apps and this is not among them | **[FW]**, **[SRC]** SD card |
| **Wi-Fi config portal / web control panel** | **Partly** | Runs entirely on the S3, but exposes `Clear BT A2DP pair` and music play-mode controls (`[I] [WEB] Change music play mode to: %d`) which for the Bluetooth app must be relayed to the ESP32 | **[FW]** **[INF]** on the relay |

Note also that the S3 image contains `Clear BLE HID pair` alongside `Clear BT A2DP pair` **[FW]** — the S3 runs **its own BLE HID** (so the knob can act as a BLE media-key device without the ESP32 at all), while Classic BT A2DP pairing lives on the ESP32 and is cleared by proxy over the UART. Two distinct Bluetooth identities on one product.

**Summary:** the link is real, it is load-bearing, and it carries exactly one thing of any size — album art. Everything else on it is small control and metadata traffic. Four of the six user-visible apps never touch it.

---

## 4. Who owns what — the definitive table

Compiled from the schematic **[SCH]**, cross-checked against the demo source **[SRC]** and the factory firmware strings **[FW]**. Full pin-level detail in [pinouts and buses](pinouts-and-buses.md).

| Resource | ESP32-S3R8 (`U2`) | ESP32-U4WDH (`U14`) | Evidence |
|---|:--:|:--:|---|
| **1.8" 360×360 LCD** (QSPI, GPIO13–18 + RST 21) | **YES — exclusively** | no connection | **[SCH]** **[SRC]** `08_LVGL_Test` |
| LCD backlight PWM (GPIO47 → AO3400A) | **YES** | — | **[SCH]** |
| **CST816D capacitive touch** (I2C0, GPIO11/12, addr 0x15) | **YES — exclusively** | no connection | **[SCH]** **[SRC]** |
| **microSD / TF card** (4-bit SDMMC, GPIO2–6 + 42) | **YES — exclusively** | no connection | **[SCH]** **[SRC]** `02_SD_Card` |
| **MSM261 PDM microphone** (GPIO45/46) | **YES — exclusively** | no connection | **[SCH]** |
| **DRV2605L haptics + LRA** (I2C0, addr 0x5A) | **YES — exclusively** | no connection | **[SCH]** **[SRC]** `03_DRV2605_Test` |
| **Knob 1** (`SW2`, EC1_A/EC1_B, GPIO8/GPIO7) | **YES** | — | **[SCH]** **[SRC]** `04_Encoder_Test` |
| **Knob 2** (`SW1`, EC2_A/EC2_B, GPIO19/GPIO22) | — | **YES** | **[SCH]** **[FW]** (`iot_knob` in the ESP32 image) |
| 16 MB external flash (W25Q128JVPIQ) | **YES** | — | **[SCH]** |
| 8 MB PSRAM (in-package) | **YES** | none, and none possible | **[SCH]** **[DOC]** |
| 4 MB flash (in-package) | — | **YES** | **[DOC]** **[FW]** |
| Battery ADC divider | **YES** | — | **[SCH]** **[SRC]** `01_ADC_Test` |
| **I2S audio out → PCM5100A** | via CH445P **`S2`** bank (GPIO39/40/41) | via CH445P **`S1`** bank (GPIO25/26/27) | **[SCH]** sheet `5_DAC.png` |
| **CH445P mux SELECT** (`I2S_SWITCH_IN`) | **YES — GPIO0, sole owner** | — | **[SCH]** |
| **PCM5100A MUTE** (`XSMT`) | — | **YES — GPIO32, sole owner** | **[SCH]** |
| 3.5 mm line output | — (via the mux) | — (via the mux) | **[SCH]** |
| **Native USB device** | **YES** — USB-OTG, GPIO19/20 | **no** — silicon has none; needs bridge `U10` | **[SCH]** **[DOC]** |
| USB-UART bridge `U10` | — | **YES** — to its UART0 (GPIO1/3) | **[SCH]** |
| **Wi-Fi 802.11 b/g/n** | **YES — and actually used** (AP portal, STA, AIDA64 client, web panel) | present in silicon, **unused by the factory image** — no Wi-Fi provisioning or HTTP strings in it | **[DOC]** **[FW]** |
| **Bluetooth LE** | **YES — BLE 5**, and used (`Clear BLE HID pair`) | present — **BLE 4.2** | **[DOC]** **[FW]** |
| **Bluetooth Classic (BR/EDR)** | **NO — not possible in silicon** | **YES — the only source on the board** | **[DOC]** **[FW]** |
| A2DP sink + source, AVRCP CT + TG, Cover Art, SPP, BT-HID | — | **YES** | **[FW]** |
| Own crystal | `X1` 40 MHz | `X2` 40 MHz | **[SCH]** |
| Own antenna | `ANT1` | `ANT2` | **[SCH]** |
| Own firmware image | `WX-ESP32S3-KNOB_V1.2.bin` | `ESP32-KNOB_ESP32_0.bin` | **[FW]** |
| **OTA-capable partition layout** | **YES** (`app0`/`app1` + `otadata`) | **NO** (`factory` only) | **[FW]** — see §5 |

### 4.1 Direct answers

> **Q: The SD card is on which MCU?**
> **The ESP32-S3.** microSD via 4-bit SDMMC on S3 GPIO2, 3, 4, 5, 6 and 42 **[SCH]**, confirmed by the `02_SD_Card` example which is an `esp32s3`-target project **[SRC]**. **The ESP32-U4WDH has no connection to the card socket whatsoever.** It physically cannot — its GPIO6–11 (the pins that would form an SD interface) are bonded to its in-package flash die and are drawn on the schematic with **no net attached at all** **[SCH]** **[DOC]**. If the Bluetooth MCU ever needs a file, it has to ask the S3 over the UART.

> **Q: The screen is on which MCU?**
> **The ESP32-S3.** The 360×360 panel hangs off the S3's QSPI bus (GPIO13–18, reset on GPIO21, backlight PWM on GPIO47) **[SCH]**, and every graphics example targets `esp32s3` **[SRC]**. **The ESP32-U4WDH cannot draw a single pixel.** Everything the Bluetooth MCU wants shown — track title, artist, album art, connection state — must be serialised across the two-wire UART and rendered by the S3. That is the entire architectural point of §2.

> **Q: Can the S3 be OTA'd but not the U4WDH?**
> **Yes. See §5 for the full answer.**

### 4.2 The pattern

Read the table and one design emerges: **the S3 is the computer; the U4WDH is a Bluetooth radio peripheral with two extra pins of its own.** The S3 has every input device except knob 2, every output device except the mute line, all the storage, all the compute headroom, and a native USB. The U4WDH has a Bluetooth Classic radio, an I2S output, a knob, and a mute pin.

### 4.3 The awkward exception: split audio control

The one place the clean split breaks down, and it breaks down badly.

Both MCUs want the single [PCM5100A](../../../components/texas-instruments/pcm5100a/README.md) DAC. A [CH445P](../../../components/wch/ch445p/README.md) four-channel 2:1 analog switch (`U18`, sheet `5_DAC.png`) selects whose I2S reaches it **[SCH]**. But the two control pins are on **different chips**:

- **The S3 owns the mux select.** `I2S_SWITCH_IN` (CH445P pin 15) is **S3 GPIO0**. The ESP32 cannot route itself to the DAC.
- **The ESP32 owns the mute.** `XSMT` (PCM5100A pin 17) is driven by **ESP32 GPIO32** and by nothing else. It is not routed through the mux and no S3 pin touches it. The S3 cannot un-mute the DAC.

**Neither chip can make a sound alone.** Every source handover — "stop playing the SD-card MP3, the phone just connected over Bluetooth" — must be negotiated over the inter-MCU UART. This is a hard functional dependency, not an optimisation.

Live caveats, tracked in [gaps and conflicts](gaps-and-conflicts.md):

- **The CH445P truth table is unverified** — no datasheet obtained — so *which* logic level selects *which* bank is unknown.
- **S3 GPIO0 is also the S3's BOOT strapping pin** with an external 10 k pull-up, so the mux sits in an unverified state from reset and during S3 download mode.
- **CH445P channel D is unconnected**, so **no MCLK reaches the DAC from either MCU** — the PCM5100A must run in BCK-derived clocking mode **[SCH]**.
- **Open question:** how does the S3-only `07_Audio_Test` example produce sound at all, given it never drives a mute line it cannot reach? Either `XSMT` floats or is pulled high by something not transcribed, or the stock ESP32 firmware leaves it un-muted and the example silently depends on that. **Unresolved.**

---

## 5. OTA: the S3 can, the U4WDH cannot

### 5.1 The partition tables, read directly from the images

Parsed from the `0xAA50`-magic entries at offset `0x8000` in each merged image **[FW]**:

**`WX-ESP32S3-KNOB_V1.2.bin` — ESP32-S3R8, 2 138 224 bytes, 16 MB layout**

| Name | Type | SubType | Offset | Size |
|---|---|---|---:|---:|
| `nvs` | data (0x01) | nvs (0x02) | `0x009000` | 20 KB |
| **`otadata`** | data (0x01) | **ota (0x00)** | `0x00e000` | 8 KB |
| **`app0`** | app (0x00) | **ota_0 (0x10)** | `0x010000` | 3072 KB |
| **`app1`** | app (0x00) | **ota_1 (0x11)** | `0x310000` | 3072 KB |
| `spiffs` | data (0x01) | spiffs (0x82) | `0x610000` | 10 112 KB |
| `coredump` | data (0x01) | coredump (0x03) | `0xff0000` | 64 KB |

**`ESP32-KNOB_ESP32_0.bin` — ESP32-U4WDH, 1 130 672 bytes, 4 MB layout**

| Name | Type | SubType | Offset | Size |
|---|---|---|---:|---:|
| `nvs` | data (0x01) | nvs (0x02) | `0x009000` | 24 KB |
| `phy_init` | data (0x01) | phy (0x01) | `0x00f000` | 4 KB |
| **`factory`** | app (0x00) | **factory (0x00)** | `0x010000` | 1600 KB |
| `storage` | data (0x01) | spiffs (0x82) | `0x1a0000` | 1408 KB |

### 5.2 What that means

| | ESP32-S3R8 | ESP32-U4WDH |
|---|---|---|
| App slots | **two** (`app0` 3 MB, `app1` 3 MB) | **one** (`factory` 1.56 MB) |
| `otadata` boot-selector partition | **present** | **absent** |
| Rollback possible | yes (two slots + otadata) | no |
| **OTA-capable layout** | **YES** | **NO** |
| Free flash for a second slot | — | **No.** 4 MB total, `factory` is 1.56 MB and `storage` is 1.38 MB. A second 1.56 MB slot does not fit without repartitioning and shrinking or dropping `storage` |

**Answer to the question as asked: yes — the ESP32-S3 has an OTA-capable partition layout and the ESP32-U4WDH does not.** This is not a nuance; it is a structural difference between the two images.

### 5.3 An important qualification: capable ≠ implemented

The S3's *layout* supports OTA. Whether the *factory application* actually performs OTA is a separate question, and the evidence says **no**:

- The S3 image contains **`esp_ota_ops.c`** and generic app-update symbols (`esp_ota_get_running_partition`, `esp_ota_get_app_partition_count`, `not found otadata`, `Rollback is not possible, do not have any suitable apps in slots`) **[FW]** — but these are pulled in by the standard Arduino-ESP32 / ESP-IDF `app_update` component on **any** build with an OTA layout. Their presence is not evidence of an OTA client.
- **No `esp_https_ota` strings. No `ArduinoOTA` strings. No `Update.h` strings.** **[FW]**
- The embedded HTTP server's complete URI set is `/aida64`, `/clockbg`, `/configwifi`, `/docmd`, `/getstatus`, `/mjpeg`, `/music`, `/pic`, `/root`, `/save`, `/saveweather`, `/spiffs`, `/txt`, `/wifilist` **[FW]**. **There is no `/update`, `/ota`, or firmware-upload endpoint**, and the web control panel's JavaScript (fully recoverable from the image) exposes only brightness, volume, app selection, boot app, timezone, weather and AIDA64 host settings — **no firmware field**.

Interestingly, the U4WDH image *also* contains `esp_ota_ops.c` and `Error in write_otadata operation` **[FW]** — but with no `otadata` partition and only a `factory` slot, that code can never succeed. It is dead weight linked in by the IDF.

So the accurate statement is:

> **The S3 is OTA-*capable* by partition layout, with 3 MB of headroom in each slot and full rollback support — but the shipped factory application does not implement an OTA update path. Your own S3 firmware can trivially add one. The U4WDH is not OTA-capable at all, at any layer.**

### 5.4 Practical consequences

| Scenario | S3 | U4WDH |
|---|---|---|
| Ship a field update over Wi-Fi | **Yes** — write your own app using the existing `app0`/`app1`/`otadata` layout. `esp_https_ota` or `ArduinoOTA` both drop straight in. 3 MB per slot is generous | **No** |
| Recover from a bad update | **Yes** — automatic rollback to the other slot via `otadata` | **No** — a bad flash means a bricked chip until you get a cable to it |
| Update in the field with no physical access | **Yes** | **No** |
| Update method that always works | Serial over USB-C in the S3 orientation | **Serial over USB-C in the ESP32 orientation — flip the plug.** This is the only method that exists |

**In practice, updating the Bluetooth MCU means physically handling the device: plug in USB-C, flip the plug if you land on the S3, run `esptool write_flash 0x0`.** For a consumer product that would be a serious limitation. For a dev board it is merely tedious.

### 5.5 The escape hatch you could build (does not exist today)

Because the S3 *can* be OTA'd and the two chips *are* connected, you could build **OTA-over-UART-bridge**: OTA a new S3 image that contains an embedded ESP32 firmware payload, then have the S3 push that payload across the inter-MCU UART into a custom U4WDH bootloader/updater that writes it to flash.

**⚠ This does not exist. Nothing in either factory image implements it, no Waveshare document mentions it, and no community project is known to have done it on this board. It is offered only as a design you could construct.** To build it you would need:

1. Custom U4WDH firmware, since Waveshare ships **no ESP32 source** (§3.1) — you are writing the receiving end from scratch anyway.
2. A repartition of the 4 MB flash to create a second app slot plus `otadata`. **The `storage` SPIFFS partition (1408 KB) is the only place the space can come from** — and its contents are unknown and unrecoverable if you drop it (see §6.2, back the flash up first).
3. Transfer-time budget: a ~1.1 MB image at 115200 takes **~96 seconds**; at 921600, **~12 seconds** (§2.3.2). Tolerable either way.
4. Robust framing with retry, since there is no hardware flow control (§2.2).
5. Careful failure handling — **neither chip can reset the other** (§2.1), so a U4WDH that hangs mid-update cannot be recovered by the S3. You would want the update logic in a minimal, never-overwritten bootloader region.

Point 5 is the real risk. Without a reset line, a botched UART update leaves you with a chip only a USB cable can save.

---

## 6. Practical guidance

### 6.1 Developing for both chips

| | ESP32-S3R8 | ESP32-U4WDH |
|---|---|---|
| ESP-IDF target | `idf.py set-target esp32s3` | `idf.py set-target esp32` |
| Arduino board | ESP32S3 Dev Module | ESP32 Dev Module |
| Flash size to configure | 16 MB | **4 MB** |
| PSRAM | 8 MB, enable Octal PSRAM | **none — do not enable** |
| Official example code | 8 examples, all `esp32s3` **[SRC]** | **none exists** |
| USB path | native USB (one plug orientation) | bridge `U10` (the other orientation) |
| Console | native USB CDC / USB-Serial-JTAG; UART0 is **not** routed to the bridge **[SCH]** | UART0 (GPIO1/3) → bridge → host |
| Inter-MCU UART | **UART1** on GPIO38 (TX) / GPIO48 (RX) | **UART1** on GPIO23 (TX) / GPIO18 (RX) |
| Reserved / dangerous pins | GPIO0 is BOOT **and** the audio mux select — driving it at the wrong moment affects boot straps and audio routing | GPIO0 boot strap (driven by the bridge); GPIO6–11 bonded to internal flash, unusable |

⚠ **Before writing any U4WDH code, check the core count.** ESP32-U4WDH was originally a **single-core, 160 MHz** part and was upgraded to dual-core effective 2021-12-02 (Espressif PCN-2021-021). Nothing in Waveshare's materials says which is fitted. Run `esp_chip_info()` on boot and branch. Full treatment in [ESP32-U4WDH §2](../../../components/espressif/esp32-u4wdh/README.md#2--the-core-count-and-clock-speed-caveat-unresolved).

Skeleton for your own end of the link (both sides symmetrical apart from pins and target):

```c
// ESP32-S3 side. Mirror on the ESP32 with tx=23, rx=18.
#define LINK_UART   UART_NUM_1
#define LINK_TX_PIN 38      // -> U4WDH GPIO18
#define LINK_RX_PIN 48      // <- U4WDH GPIO23

uart_config_t cfg = {
    .baud_rate  = 921600,               // pick one; BOTH SIDES MUST MATCH
    .data_bits  = UART_DATA_8_BITS,
    .parity     = UART_PARITY_DISABLE,
    .stop_bits  = UART_STOP_BITS_1,
    .flow_ctrl  = UART_HW_FLOWCTRL_DISABLE,   // no RTS/CTS wires exist
    .source_clk = UART_SCLK_XTAL,             // immune to APB/DFS changes
};
ESP_ERROR_CHECK(uart_param_config(LINK_UART, &cfg));
ESP_ERROR_CHECK(uart_set_pin(LINK_UART, LINK_TX_PIN, LINK_RX_PIN,
                             UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));
ESP_ERROR_CHECK(uart_driver_install(LINK_UART, 4096, 4096, 20, &q, 0));
```

Three things that will bite you:

1. **`source_clk = UART_SCLK_XTAL`.** If either side enables dynamic frequency scaling or light sleep with the default APB clock source, its baud drifts and the link dies intermittently.
2. **Generous RX ring buffer.** The 128-byte hardware FIFO is your real deadline; a large software buffer plus a high-priority drain task buys you slack, but only if the ISR runs.
3. **Design your own flow control.** Request/response or windowed-ack. Never unsolicited bulk. See §2.2.

More setup detail in [development](development.md); Bluetooth specifics in [classic Bluetooth](classic-bluetooth.md).

### 6.2 ⚠ Back up the factory ESP32 image before you touch it

**`ESP32-KNOB_ESP32_0.bin` is the only copy of the Classic Bluetooth application that exists. There is no source. If you lose it, you cannot rebuild it.**

Waveshare publishes it, so it is re-downloadable *today* — but vendor download links rot, and the local copy is your insurance either way. More to the point, **a `read_flash` backup captures things the published image does not**: your `nvs` partition (pairing records under the `PEERADDR` key, settings) and the 1408 KB `storage` SPIFFS partition, whose contents are undocumented and are **not** in the published binary.

```sh
# Connect in the orientation that gives you the ESP32-U4WDH, then:
esptool --port PORT chip_id            # MUST say ESP32-U4WDH
esptool --chip esp32 --port PORT --baud 921600 \
        read_flash 0x0 0x400000 esp32-u4wdh-full-backup.bin
sha256sum esp32-u4wdh-full-backup.bin  # record it somewhere durable

# Do the same for the S3 while you are here (16 MB, slower):
esptool --chip esp32s3 --port PORT --baud 921600 \
        read_flash 0x0 0x1000000 esp32s3-full-backup.bin
```

Known-good hashes of the **published** images, for verifying a fresh download **[FW]**:

| File | Size | SHA-256 | MD5 |
|---|---:|---|---|
| `ESP32-KNOB_ESP32_0.bin` | 1 130 672 | `0c1c21b9822d4c2d80d58534b33eb0083880de4ed7354a38b4c78ba51757349d` | `3af00b75ca143a3cf8449a98610bca3b` |
| `WX-ESP32S3-KNOB_V1.2.bin` | 2 138 224 | `f7c1cc18b687559f3bd69e5c9ab526bc61c2b2d9c502f38367f7f2bfe4ff8e87` | `fa3e025c88d8304da24e0af91aacffeb` |

Image provenance **[FW]** (from the `esp_app_desc_t` structures at `0x10020`):

| Image | Project name | Version | Built | ESP-IDF |
|---|---|---|---|---|
| `ESP32-KNOB_ESP32_0.bin` | `TAIJI_KNOB_32` | `1` | 2025-04-18 09:24:52 | `v5.4-727-g5cbd2a3877` |
| `WX-ESP32S3-KNOB_V1.2.bin` | `arduino-lib-builder` | `599b76d` | 2025-02-28 12:10:29 | `v5.1.4-972-g632e0c2a9f-dirty` |

(The S3 image's project name is the Arduino-ESP32 libs-builder placeholder, not the application's real name — this is a PlatformIO Arduino build. Its actual origin is a third party, from the `C:/Users/Fei/…` build paths **[FW]**, not Waveshare's own demo tree.)

Full restore procedure and archive URLs in [factory firmware](factory-firmware.md).

### 6.3 Does replacing the S3 firmware break Bluetooth?

**It breaks the Bluetooth *experience*, not the Bluetooth *radio*.** Precisely:

| What happens | Why |
|---|---|
| The ESP32 keeps working as a Bluetooth speaker/AVRCP device | It is a wholly separate chip with its own untouched firmware. Your phone will still see and pair with it |
| Existing pairings survive | They live in the ESP32's `nvs` (`PEERADDR`), which S3 flashing never touches |
| **The screen goes blank / shows your app instead** | The ESP32 cannot draw anything (§4.1). It will keep sending metadata and cover-art frames into a UART nobody is parsing |
| **Track title, artist and album art disappear** | Same reason. The data is still on the wire; nothing renders it |
| **Playback control from the knob and touchscreen stops** | Both input devices are S3-side; the commands crossed the UART, and your firmware does not speak the (undocumented, §2.4.3) protocol |
| **"Clear Bluetooth pairing" from the UI stops working** | Same |
| **⚠ Audio may go completely silent** | This is the nasty one. The S3 owns the CH445P **mux select** (GPIO0) and the ESP32 owns the **`XSMT` mute** (§4.3). If your S3 firmware leaves GPIO0 in a state that routes the *S3's* silent I2S bank to the DAC, the ESP32's audio never reaches the PCM5100A — even though the ESP32 thinks it is playing. **And you cannot fix it from the ESP32 side.** |

**Mitigation:** if you replace the S3 firmware and want to keep Bluetooth audio working, your very first job is to determine and hold the correct GPIO0 level for the ESP32's `S1` bank. The CH445P truth table is **unverified** (no datasheet obtained), so this is empirical: set GPIO0 low, play from a paired phone, listen; if silent, set it high. Record which one worked. Note GPIO0 is also the S3's BOOT strap with a 10 k pull-up — drive it *after* boot, never during.

Conversely, replacing the **ESP32** firmware while keeping the stock S3 firmware breaks it the other way: the S3 UI will sit waiting for metadata that never arrives, and — worse — **nothing will ever un-mute the DAC**, so the local SD-card music player may go silent too. See [classic Bluetooth §"If you reflash the U4WDH and lose all audio"](classic-bluetooth.md).

### 6.4 How to restore

Full factory state = **both** images, flashed in **both** orientations:

```sh
# 1. Verify your downloads against the hashes in §6.2.

# 2. Plug in. Identify what you are on. Do NOT force --chip for this step.
esptool --port PORT chip_id

# 3. Flash whichever chip that is, at offset 0x0.
esptool --chip esp32   --port PORT --baud 921600 write_flash -z 0x0 ESP32-KNOB_ESP32_0.bin
#   ...or...
esptool --chip esp32s3 --port PORT --baud 921600 write_flash -z 0x0 WX-ESP32S3-KNOB_V1.2.bin

# 4. Unplug. FLIP THE PLUG 180°. Plug back in.
# 5. Repeat steps 2-3 for the other chip.
# 6. Power-cycle with the physical switch (the wiki's step 8).
```

Notes:

- **`write_flash 0x0` overwrites `nvs`**, so Wi-Fi credentials and Bluetooth pairings are erased. That is usually what you want when restoring, but it means you re-pair afterwards.
- To reset pairing *without* a full reflash, the stock UI's `Clear BT A2DP pair` does it over the inter-MCU link — see [factory firmware](factory-firmware.md#resetting-bluetooth-pairing-without-a-full-reflash).
- If a flash fails or the port vanishes: unplug, flip, re-plug, re-run `chip_id`. Per Waveshare's FAQ **[WEB]**, that is the first thing to try for essentially every symptom.
- If you took a full `read_flash` backup (§6.2), restore *that* instead of the published image — it brings back your `nvs` and `storage` contents too.

---

## 7. Open questions

Carried into [gaps and conflicts](gaps-and-conflicts.md).

| # | Question | Status |
|---|---|---|
| 1 | **What baud rate does the inter-MCU link run at?** | **Unknown.** Not in the demo tree, not recoverable from strings. Needs a logic analyser or a disassembly (§2.3.1) |
| 2 | What is the byte-level frame layout — field widths, order, endianness, sync, checksum? | **Unknown.** Only field *names* are known, from log strings (§2.4.3) |
| 3 | What are the numeric `cmd` opcode values? | Unknown |
| 4 | How does the USB-C receptacle select between the two USB endpoints? | **Not shown on any schematic sheet.** Vendor-asserted behaviour only (§1.2) |
| 5 | What part is the USB-UART bridge `U10`? | Unidentified — unnamed symbol, no legible silkscreen (§1.4) |
| 6 | Which CH445P `IN` level selects which I2S bank? | Unknown — no datasheet obtained (§4.3) |
| 7 | How does the S3-only `07_Audio_Test` example get sound past a mute line it cannot drive? | Unresolved (§4.3) |
| 8 | Is there a distinct "spectrum analyser" app, and does it use the link? | **RESOLVED 2026-08-23. Yes it exists; no it does not use the link.** Wiki §4.2.6 documents it as a launcher entry fed by the **PDM microphone**, so it is entirely S3-local. The earlier negative string search was sound but misread — the UI renders text from **binary font blobs on the SD card**, not firmware string tables, so a string scan would fail for every app name (§3.2, [factory-demo-apps.md §3.6](factory-demo-apps.md)) |
| 9 | What is in the U4WDH's 1408 KB `storage` SPIFFS partition? | Unknown — not present in the published image; only a `read_flash` backup would capture it (§6.2) |
| 10 | Is the U4WDH on this board single-core or dual-core? | Unresolved per board; determinable per unit at runtime (§6.1) |
| 11 | Are there series resistors on the two inter-MCU UART nets? | Not recorded in the schematic transcription; weak evidence (§2.1) |

---

## Related

- [Device README](README.md) — overview and specifications
- [Pinouts and buses](pinouts-and-buses.md) — pin-by-pin for both chips
- [Classic Bluetooth](classic-bluetooth.md) — what the secondary MCU provides and how to build for it
- [Factory firmware and restore](factory-firmware.md) — images, hashes, provenance, restore procedure
- [Development and examples](development.md) — toolchain setup for both targets
- [Gaps and conflicts](gaps-and-conflicts.md) — the open-questions register
- [ESP32-U4WDH component page](../../../components/espressif/esp32-u4wdh/README.md) — the deep treatment of the secondary MCU
- [ESP32-S3R8 component page](../../../components/espressif/esp32-s3r8/README.md)
- [USB-C orientation-select interface](../../../components/generic/usb-c-interface/README.md)
- [USB-UART bridge `U10`](../../../components/wch/ch340x/README.md)
- [CH445P audio mux](../../../components/wch/ch445p/README.md)
