# T-Display K230 — competitors, equivalents and recommendations

Comparisons are scoped to a stated workload. Nothing here is called "equivalent" unless the
interfaces, performance and software requirements actually align — and in this comparison set,
almost nothing does.

## 1. Direct comparison

Prices are the dated observations from [`market-and-pricing.md`](market-and-pricing.md);
everything else is vendor specification. **No cross-device benchmark exists**, so no performance
ranking is offered.

| | **T-Display K230 Kit** | **LilyGO T-Deck Plus** | **LilyGO T-Display P4** | **M5Stack Cardputer** | **CanMV-K230** | **BPI-CanMV-K230D-Zero** |
|---|---|---|---|---|---|---|
| SoC | K230, 2 × RV64 @ 1.6 + 0.8 GHz | ESP32-S3 | ESP32-P4 | ESP32-S3 | K230 | K230D |
| Class | **application processor, Linux** | MCU | MCU | MCU | application processor | application processor |
| RAM | **1 GB LPDDR4** | 8 MB PSRAM | 16/32 MB PSRAM | 8 MB PSRAM | 512 MB | 128 MB (SiP) |
| NPU | **yes (KPU)** | no | **no** | no | yes | yes |
| Vector | **RVV 1.0 on CPU1** | no | Espressif PIE | no | RVV 1.0 | RVV 1.0 |
| Display | **4.1″ AMOLED 568×1232** | 2.8″ IPS 320×240 | — (kit) | 1.14″ 240×135 | none | none |
| Keyboard | **full QWERTY, backlit** | small QWERTY + trackball | separate, incompatible | QWERTY | none | none |
| Camera | **2 MP MIPI CSI** (3 CSI available) | no | MIPI CSI capable | optional unit | 3 × CSI | CSI |
| Video codec | **H.264+H.265 enc *and* dec** | none | H.264 **enc only** | none | same as K230 | same |
| Wi-Fi | 2.4 GHz 802.11n (external) | 2.4 GHz (integrated) | **none on SoC** | 2.4 GHz | — | — |
| Bluetooth | **USB dongle only** | integrated BLE | **none on SoC** | integrated BLE | — | — |
| LoRa | **SX1262 or LR2021** | SX1262 | no | via unit | no | no |
| Cellular / GNSS | **nRF9151 option** | GPS option | no | no | no | no |
| Ethernet | **100 Mbit USB** | no | **MAC on SoC** | no | no | yes |
| OS | **Linux** | Arduino / ESP-IDF | ESP-IDF | Arduino / M5 | Linux | Linux |
| Toolchain maturity | **poor** | **excellent** | good | excellent | poor | poor |
| Price, 2026-09-04 | **$263.56** full | ~$60–70 (not re-verified) | not observed | ~$30 (not re-verified) | not established | **$29** (2024) |

⚠ **The T-Deck Plus and Cardputer prices are from memory of the general market, not from a dated
observation made in this pass.** They are marked as such and must not be quoted as findings.

## 2. What each comparison actually tells you

**vs T-Deck Plus** — the closest thing in spirit, and the wrong comparison technically. The
T-Deck Plus is an ESP32-S3 handheld: cheaper, mature, with an enormous community and a working
Meshtastic firmware today. The K230 kit costs roughly four times as much and gives you Linux, a
much better screen, a camera and an NPU. **If your project is "a Meshtastic node with a keyboard",
buy the T-Deck Plus.** If it is "a Linux computer that happens to have LoRa", the T-Deck cannot
do it at all. One user made the trade explicitly: *"If the WiFi is any better than the t-deck plus
I might end up with one."*

**vs T-Display P4** — the interesting one, because it is the same vendor, the same product line
and the same idea one class down. The P4 is a *microcontroller* with MIPI DSI and CSI; it runs
ESP-IDF, which is a genuinely good SDK with reproducible NixOS packaging. The K230 runs Linux with
1 GB of RAM and an NPU, and its build system wants Ubuntu and a hard-coded `/opt/toolchain`.
**The K230 is more capable and much harder to work with.** The keyboards are mutually incompatible
(LilyGO, 2026-07-28). See [`components/espressif/esp32-p4`](../../../components/espressif/esp32-p4/README.md)
and the [K230 record §11](../../../components/canaan/k230/README.md#11-competing-and-substitute-parts).

**vs M5Stack Cardputer** — not a competitor. An order of magnitude cheaper, an order of magnitude
less capable. It came up in this research only because a user asked whether to buy one instead.
One K230 kit buyer said: *"I'll stick with the cardputer zero I ordered but I'm going to be
watching this."*

**vs CanMV-K230 / BPI-CanMV-K230D-Zero** — same silicon, no display, no keyboard, no radio, and
**half or an eighth of the memory**. If you want to develop for the K230 chip and do not need a
handheld, the $29 Zero is the rational purchase. The LilyGO board is the only K230 board with
1 GB and the only one with a screen attached.

**vs a de-Googled phone** — raised by the community, and it is a fair challenge for the
Meshtastic use case specifically. A phone has better radios, a better screen, a much better
battery and a real OS. It does not have a 40-pin header, three MIPI CSI inputs, an LR2021, or a
Linux userspace you control.

## 3. Alternatives by tier — for a *LoRa-mesh handheld*, dated 2026-09-04

| Tier | Choice | Why |
|---|---|---|
| **Budget** | A dedicated Meshtastic node (~$30) + your phone | Best battery life, best software maturity, lowest cost |
| **Mainstream** | **LilyGO T-Deck Plus** | Integrated keyboard handheld, mature Meshtastic support, no build system required |
| **Capability** | **T-Display K230 Kit, `K277` + `K256-04`** | The only option with mesh **voice and photo** transfer, plus Linux, a camera and cellular |
| **Experimentation / RISC-V** | **T-Display K230 bare board `K256`** | Cheapest route to 1 GB of K230 with a screen |
| **Chip development only** | **BPI-CanMV-K230D-Zero** ($29) | Cheapest K230; accept 128 MB |
| **Professional / product** | **None of the above** | No certification data, no errata, no published schematic, no recovery procedure, no licence on the vendor firmware |

## 4. Alternatives by tier — for an *on-device vision/AI* project

| Tier | Choice | Why |
|---|---|---|
| Cheapest working NPU | Sophgo CV1800B boards (Milk-V Duo) | ~0.5 TOPS, 64 MB, tiny, cheap |
| Balanced | **T-Display K230** | 1 GB, real ISP, 3 CSI, H.265, integrated screen |
| Mature ecosystem | Rockchip RV1106 boards | The IP-camera default; large community; single Cortex-A7 |
| Arm alternative | Allwinner V853 | Mature Tina Linux BSP |
| **MCU-class** | ESP32-P4 | If 32 MB of PSRAM is enough and you want ESP-IDF |

## 5. Clones and used market

**No clone of the T-Display K230 was found** in any search performed. **No used listings** were
found either — the kit is fifteen days old at the research date. Both are negative results from a
search that did not include AliExpress or Taobao ([`research-log.md`](research-log.md)), so they
are weaker than they look.

## 6. Comparison traps specific to this device

1. **"Two RISC-V cores" ≠ a dual-core SMP system.** Two independent subsystems, one with a vector
   unit and one without, historically running two different operating systems.
2. **"Ethernet" ≠ an Ethernet MAC.** 100 Mbit over USB.
3. **"Wi-Fi + Bluetooth" ≠ integrated.** SDIO Wi-Fi and a Bluetooth *dongle*.
4. **"1.6 TOPS" is not a datasheet figure.** Canaan publishes none.
5. **"Kit" is two purchases**, and no single SKU is the complete handheld.
6. **A 2025 review describes a different product** — the software arrived in August 2026.
7. **`K230` as a SKU means a T-Embed CC1101.** Never infer silicon from a LilyGO stock code.

---

## Cross-references added 2026-09-07

Append-only, from a cross-cutting synthesis pass. Nothing above was changed and no
new evidence was gathered.

- [**Handheld and e-ink device landscape, 2026-09**](../../../guides/markets/handheld-and-eink-device-landscape-2026-09.md)
  — the K230 Kit placed against the Cardputer ADV ($29.90), the Cardputer v1.1 and
  the Tanmatsu (~€120) in a keyboard-handheld group, with the **$263.56 complete
  price** stated up front and the comparisons that are not supportable — notably
  that **no independent benchmark of this board exists**, even though its own BSP
  builds CoreMark into the shipped image.
- [**SoC choice for battery e-ink devices**](../../../guides/hardware/soc-choice-for-battery-eink-devices.md)
  — the K230 against ESP32-C3/S3/P4 and the nRF parts on memory, radio integration,
  toolchain maturity and price. Two figures from this record do heavy lifting there:
  the **≤ 20 µW SoC standby** claim and the board's **2.5 W idle**, which together
  are the whole Linux-versus-MCU trade. It also uses the **$42.31 nRF9151 delta**
  between `K256-04` and `K256-04-A` as the only clean per-chip price signal in this
  repository.
- [**Adding LoRa, NFC and an RGB sidelight to e-ink firmware**](../../../guides/hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md)
  — for the LR2021-versus-SX1262 purchase decision in a wider radio context.
