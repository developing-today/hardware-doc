# ZhongKeWei ATGM336H-6N

- **Category:** **GNSS receiver module** — a 10.1 × 9.7 × 2.4 mm, 18-pad SMD carrier for an
  **AT6668** multi-mode satellite-navigation SoC
- **Scope:** module level. The configuration protocol (CASIC binary) belongs to
  [`components/zhongkewei/at6668`](../at6668/README.md)
- **Research status:** **datasheet mined 2026-09-20.** The 2026-09-04 pass held the PDF but
  explicitly had not read it; every figure below now comes from the manufacturer's own
  document unless marked otherwise. **Mining refuted two caveats the previous pass
  recorded** — see §9.
- **Retrieved:** 2026-09-04 · **mined:** 2026-09-20

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **杭州中科微电子有限公司** — *Hangzhou Zhongke Microelectronics Co., Ltd.* | **manual cover page and every page footer** (p. 1–17) |
| Address | 杭州市滨江区江南大道 3850 号创新大厦 10 楼 — Innovation Building 10F, 3850 Jiangnan Avenue, Binjiang District, **Hangzhou** | manual p. 1 |
| Contact | tel 0571-28918100 · fax 0571-28918122 · **`http://www.hzzkw.com`** | manual p. 1 |
| Part | **`ATGM336H-6N`** (series) | manual title p. 1 |
| Chipset inside | **`AT6668`** — "中科微第六代多系统 GNSS SOC 单芯片" (Zhongke **6th-generation** multi-system GNSS SoC) | manual §1.1 p. 2 |
| Pads | **18** | manual §2.3 p. 8 |
| Document | **用户手册 (User Manual) V1.1, 2023-01-11** | manual version-history table p. 17 |

> ⚠ **Manufacturer corrected.** The 2026-09-04 record said *"ZhongKeWei / 中科微电子
> (Zhongke Microelectronics), **Chengdu**"*. The document itself says **Hangzhou**, on the
> cover and in all seventeen page footers, with a Hangzhou address, a Hangzhou area code
> (0571) and the domain `hzzkw.com` (**hz** = Hangzhou). The "Chengdu" attribution was
> unsourced and is **refuted**. `components/zhongkewei/` is the correct, consistent vendor
> slug and no near-duplicate was created.

### 1.1 What `-6N` means — the manufacturer spells it out

Manual **§5.2 型号命名规则 (model naming rules)**, p. 16, decomposes `ATGM336H-6N-32`:

| Field | Example | Manufacturer's gloss |
|---|---|---|
| Product code 产品名 | `ATGM336H` | the **10.1 mm × 9.7 mm module series** |
| Type code 类型名 | **`6N`** | **"采用 AT6668 硬件平台的导航模块"** — a navigation module built on the **AT6668 hardware platform** |
| Hardware code 硬件功能名 | `32` | the **satellite-system set** supported |

So **`-6N` is not a firmware grade or a revision — it designates the AT6668 silicon
platform.** The 2026-09-04 record's "the `-6N` suffix denotes the variant/firmware grade"
was a guess and is superseded.

### 1.2 The trailing hardware code is the part that actually varies

Manual **§1.2 产品选购 (product selection)**, p. 2 — the full published variant list:

| Ordering part | Satellite systems | Bands | Baud |
|---|---|---|---|
| `ATGM336H-6N-32` | GPS + QZSS + BD2 + BD3 | L1 + B1I + B1C | 115200 bps |
| `ATGM336H-6N-74` | GPS + QZSS + BD2 + BD3 + **GAL + GLO** | L1 + B1I + B1C + **E1 + R1** | 115200 bps |

⚠ **M5Stack writes only `ATGM336H-6N`, with no hardware code**, so which of the two is
fitted is **not established by naming**. M5Stack's published constellation list includes
GALILEO and GLONASS, which matches **`-74`** and not `-32`. That is consistent but
**`inferred`** — the schematic comment is `GP-02` and the specification table is prose, so
no document in this repository states the hardware code directly. A `$GPTXT` version query
on real hardware would settle it; `not-tested`.

## 2. Technical specification — manufacturer's figures

Manual **§2.6 技术规范**, p. 11. Text layer cross-checked against the rendered page heading
and re-extracted without `-layout` before transcription — `executed-success`, 2026-09-20.

| Item | Value |
|---|---|
| Signal reception | **BDS** B1I + B1C · **GPS/QZSS/SBAS** L1 · **GALILEO** E1 · **GLONASS** R1 |
| Channels | **50** (§1.3) |
| **TTFF cold** | **≤ 23 s** |
| **TTFF hot** | **≤ 1 s** |
| **TTFF reacquisition** | **≤ 1 s** |
| Cold-start acquisition sensitivity | **−148 dBm** |
| **Hot-start acquisition sensitivity** | **−156 dBm** |
| **Reacquisition sensitivity** | **−160 dBm** |
| **Tracking sensitivity** | **−162 dBm** |
| Position accuracy | **< 1.5 m (CEP50)** |
| **Velocity accuracy** | **< 0.1 m/s (1σ)** |
| Update rate | **1 Hz default, 10 Hz maximum** |
| UART | **115200 bps default, 8 data bits, no parity, 1 stop bit** |
| Protocol | **NMEA 0183 4.1** |
| Dimensions | 10.1 × 9.7 × 2.4 mm |
| Weight | **0.6 g** |

**Four sensitivity numbers, not three.** The previous record carried only three and
mislabelled them. The manufacturer distinguishes **cold-start acquisition (−148)**,
**hot-start acquisition (−156)**, **reacquisition (−160)** and **tracking (−162)** — these
are four different measurements and quoting "acquisition −160 dBm" (as the previous record
did) conflates reacquisition with acquisition. Tracking is always the most optimistic
figure; it is the threshold for *keeping* a lock already held, not for getting one.

**The default update rate is 1 Hz, not 10 Hz.** 10 Hz is the ceiling and must be commanded.
A record that lists only "up to 10 Hz" invites firmware authors to assume they get 10 Hz out
of the box; they do not.

## 3. Pinout — as the manufacturer defines it

Manual **§2.3 PIN 排列图** (p. 8) and **§2.4 管脚定义** (p. 9):

| # | Name | I/O | Function | Electrical |
|---:|---|---|---|---|
| 1 | `GND` | — | Ground | — |
| 2 | **`TXD0`** | O | **Main** UART data out | — |
| 3 | **`RXD0`** | I | **Main** UART data in | — |
| 4 | `1PPS` | O | Pulse-per-second output | — |
| 5 | `ON/OFF` | I | Module shutdown control, **active low** | — |
| 6 | `VBAT` | I | RTC + SRAM backup supply | **1.5–3.6 V**, required for hot start |
| 7 | `Reserved` | — | Reserved | **leave floating** |
| 8 | `VCC` | I | Module supply | **2.7–3.6 V** |
| 9 | `nRESET` | I | Module reset, **active low** | **leave floating if unused** |
| 10 | `GND` | — | Ground | — |
| 11 | `RF_IN` | I | Antenna signal input | — |
| 12 | `GND` | — | Ground | — |
| 13 | `Reserved` | — | Reserved | leave floating |
| 14 | **`VCC_RF`** | **O** | **Power *output*** | **+3.3 V, can supply the antenna** |
| 15 | `Reserved` | — | Reserved | leave floating |
| 16 | **`RXD1`** | I | **Auxiliary** serial data in | — |
| 17 | **`TXD1`** | O | **Auxiliary** serial data out | — |
| 18 | `Reserved` | — | Reserved | leave floating |

### 3.1 ⚠ Three conflicts with M5Stack's schematic symbol — unresolved

The symbol M5Stack draws on the Cap LoRa-1262 (designator `M2`, comment `GP-02`) **does not
match the manufacturer's pin table in three places.** Both readings are recorded; neither is
discarded.

| Pin | Manufacturer's manual (§2.4) | M5Stack schematic symbol | Status |
|---:|---|---|---|
| 2 / 3 | **`TXD0` / `RXD0`** — the *main* port | `TXD1` / `RXD1` | **Naming conflict only.** The host is wired to the module's main UART, which is correct behaviour; M5Stack's "1" suffix is misleading but harmless |
| **16 / 17** | **`RXD1` / `TXD1`** — an *auxiliary UART* | **`SDA` / `SCL`** — I²C | **Substantive conflict, unresolved** |
| **14** | **`VCC_RF` is an OUTPUT** (+3.3 V, supplies the antenna) | drawn as a **supply input** fed from `+3.3V` via ferrite `FB2` | **Substantive conflict, unresolved** |

**On pins 16/17.** The module block diagram (§1.4, p. 4) *does* list `SPI、UART、I2C、GPIO`
among the AT6668's peripheral interfaces, so the silicon certainly has I²C. But the module's
own pin-definition table assigns pads 16/17 to a **second UART**, not to I²C. Possible
readings: the pads are multiplexed and the manual documents only the default; M5Stack's
symbol is inherited from a different module; or one of the two is simply wrong. **None is
established.** On the two Cap boards these pins are not routed to the host anyway (§5), so
nothing in this repository depends on the answer — but a design that *does* route them must
not assume I²C on the strength of M5Stack's symbol alone.

**On pin 14.** This matters more. If `VCC_RF` is an output, as the manufacturer states, then
a board driving `+3.3V` *into* it is back-feeding a regulated output. Note that this
repository already contains both readings of the same board:
[`features/gnss.md` §1](../../../devices/m5stack/cap-lora-1262/features/gnss.md) says the
MAX2659 LNA is *"powered **from** `VCC_RF` through a ferrite"* — which is **consistent** with
the manufacturer — while the pin table in the same file and the previous version of this
record describe `VCC_RF` as being **fed from** `VDD_3V3`. These cannot both be right.
**The schematic has not been re-traced to settle it** — `not-tested`. Until it is, do not
cite either direction as established.

**Separately, the manual is explicit that `RF_IN` is internally biased:** *"模块内部 RF_IN
已通过电感和 VCC_RF 相连进行供电"* — **`RF_IN` is connected to `VCC_RF` through an internal
inductor** (§2.7.1, p. 12). The module therefore feeds an active antenna through the RF pin
itself; no external bias tee is required.

## 4. Antenna — active and passive both supported, with built-in protection

Manual §1.11, §2.7 and §2.8.

| Property | Value |
|---|---|
| Antenna types | **both active and passive** (§1.11, p. 6) |
| Active-antenna bias | via **`RF_IN`**, internally inductor-coupled to `VCC_RF` (+3.3 V) |
| **Recommended active-antenna gain** | **15–30 dB** (§2.7.1) |
| Passive-antenna guidance | *"建议在模块前端增加一级 LNA 保证性能"* — **add an LNA stage ahead of the module**; the manual's own reference circuit uses an **`AT2659`** with a 6.8 nH series inductor and 100 pF coupling cap (§2.7.2) |
| **Short-circuit protection** | antenna supply **current-limited to 50 mA** |
| **Open-circuit detection threshold** | **2.5 mA** (min) drawn from `VCC_RF` |
| Supply-ripple requirement | **low-ripple LDO, ≤ 50 mVpp** (§2.8) |
| RF layout | antenna connector close to `RF_IN`, **50 Ω** matched (§2.8) |

### 4.1 The antenna-status NMEA sentences — the only sentences this manual publishes

The module reports antenna-port state changes **as `$GPTXT` sentences on the UART** (§2.8,
p. 13). These are quoted verbatim from the manual, checksums included:

```
$GPTXT,01,01,01,ANTENNA SHORT*63
$GPTXT,01,01,01,ANTENNA OPEN*25
$GPTXT,01,01,01,ANTENNA OK*35
```

⚠ **With a passive antenna the module reports `ANTENNA OPEN` permanently.** The manual says
so outright: *"模块使用无源天线时，串口输出语句均为开路"* — *"when the module uses a passive
antenna, the serial output is always open-circuit."*

**Do not treat `ANTENNA OPEN` as a fault condition without knowing the antenna topology.** A
firmware health check that alarms on this string will alarm forever on any passive-antenna
design.

**Open question for the Cap LoRa-1262 and Cap LoRa868.** Both fit a *passive* patch with an
external MAX2659 LNA powered from the module's own `VCC_RF`. Whether the LNA's quiescent
draw exceeds the **2.5 mA** open-detection threshold — and therefore whether those boards
report `ANTENNA OK` or `ANTENNA OPEN` — **cannot be determined here**: no MAX2659 datasheet
is held in this repository (see
[`components/analog-devices/max2659`](../../analog-devices/max2659/README.md) §"Local
artifacts"), so its supply current is unknown. `not-tested`, and deliberately **not**
inferred.

## 5. Power

Manual §1.3 (p. 3) and §2.5 (p. 10).

| Parameter | Symbol | Min | Typ | Max | Unit |
|---|---|---:|---:|---:|---|
| Supply voltage | `Vcc` | 2.7 | 3.3 | 3.6 | V |
| **Operating current @ 3.3 V** | `Icc` | — | **42** | — | mA |
| Backup supply | `Vbat` | 1.5 | 3.0 | 3.6 | V |
| **Backup current** | `Ibat` | — | **10** | — | µA |
| Active-antenna output | `VCC_RF` | — | 3.3 | — | V |
| Antenna short-protection current | — | — | 50 | — | mA |
| Antenna open-detection current | — | 2.5 | — | — | mA |

§1.3 states the headline figures as **continuous multi-mode operation < 42 mA @ 3.3 V** and
**standby < 10 µA @ 3.3 V**.

**Logic levels** (§2.5): `Vil` ≤ 0.2 × `Vcc`; `Vih` ≥ 0.7 × `Vcc`; `Vol` ≤ 0.4 V at
`Io = −12 mA`; `Voh` ≥ `Vcc` − 0.4 V at `Io = 12 mA`. **Drive strength is a usable ±12 mA**,
which is unusually strong for a GNSS module and means `1PPS` can drive a load directly.

**Absolute maximums** (§2.5): `Vcc` and `Vbat` −0.3 to **3.6 V**; digital input −0.3 to
`Vcc` + 0.2 V; **ESD (HBM) 2000 V**; storage −40 to **125 °C**; operating −40 to **85 °C**.

⚠ **3.6 V is the absolute maximum, not a headroom figure** — it is the same number as the
recommended maximum. There is no margin above 3.6 V at all. A nominally-4.2 V LiPo must not
reach this part unregulated.

### 5.1 Power modes — what the manual does and does not say

| Mode | Mechanism | Evidence |
|---|---|---|
| Shutdown | **`ON/OFF` pin 5, active low** | §2.4 |
| Reset | **`nRESET` pin 9, active low**; float if unused | §2.4 |
| Backup / hot-start retention | **`VBAT` pin 6** keeps RTC + SRAM alive, 1.5–3.6 V, ~10 µA | §2.4, §2.5 |
| Standby | **< 10 µA @ 3.3 V** | §1.3 |

⚠ **The manual does not document a software standby command, nor how `ON/OFF` relates to the
< 10 µA standby figure.** Whether standby is entered by the pin, by a CASIC command, or
both, is **not stated in this document**. Do not assume.

## 6. 1PPS

§1.7, p. 5, in full: *"ATGM336H-6N 系列模块支持精确秒脉冲输出，脉冲上升沿与 UTC 时间对齐"* —
the module supports a precise pulse-per-second output whose **rising edge is aligned to UTC**.

**That is the entirety of the PPS specification in this document.** No pulse width, no
accuracy/jitter figure, no statement of behaviour before first fix, no indication whether the
output is disabled or free-running without satellites. Those are **unknown** — the manual
does not contain them and nothing here should be read as implying otherwise.

## 7. Configuration, upgrade and tooling — this manual defers

**The manual does not document any configuration command, and it does not list the NMEA
sentence set.** This is an important negative result, because the assignment of a GNSS record
normally expects both. Instead §1.8 points elsewhere:

| Topic | §  | The manual's referenced document |
|---|---|---|
| Output protocol / NMEA sentences | 1.8 | **《中科微多模卫星导航接收机协议规范》** — *Zhongke Multi-mode Satellite Navigation Receiver Protocol Specification* |
| A-GNSS | 1.6 | 《中科微 AGNSS 解决方案》 — *Zhongke AGNSS Solution* |
| Firmware over-the-air upgrade | 1.10 | 《ATGM 模块在线升级协议》 — *ATGM Module Online Upgrade Protocol* |
| Chip-level detail | p. 17 | **《AT6668 芯片数据手册》** — *AT6668 Chip Datasheet* |
| PC tooling | 1.12 | 《GNSSToolKit 工具使用说明》, 《UBF 串口升级工具使用说明》 |

So: **update rate, baud rate and constellation selection all go through the CASIC binary
protocol**, which is the archived document under
[`components/zhongkewei/at6668`](../at6668/README.md). The sentence set likewise lives
there, not here.

⚠ **Persistence of changed settings is therefore not answerable from this document.** What
the manual *does* establish (§1.9, p. 5) is that the module **carries a Flash** and that the
vendor's stated purpose for it includes *"让客户自主配置定位更新率"* — letting the customer
configure the update rate themselves — which implies a persistent store exists. **Whether a
given CASIC config message writes to it or only to RAM is not stated here.** `inferred` at
best; do not rely on it.

**On-line upgrade** (§1.10): the module accepts field firmware updates over the vendor's
upgrade protocol, including **remotely triggered** updates. The PC-side tool is the *UBF
serial upgrade tool*; a device-side updater is explicitly the customer's job to write.

## 8. Manufacturing

| Property | Value | §  |
|---|---|---|
| **Moisture sensitivity** | **MSL 3** (IPC/JEDEC J-STD-020) | 4.2.1 |
| Packaging | vacuum tape-and-reel, moisture- and ESD-protective, **1000 pcs/reel** | 4.1 |
| RoHS | compliant | 3.1 |
| Reflow ramp-up | **1–4 °C/s**, 25 → 150 °C average | 4.2.2 |
| Reflow preheat | **140–150 °C for 60–90 s** | 4.2.2 |
| Reflow peak | **225–250 °C for ≈ 30 s** | 4.2.2 |
| Reflow ramp-down | **2–6 °C/s** to 183 °C, ≈ 15 s | 4.2.2 |
| Total reflow time | **≈ 300 s** | 4.2.2 |

**ESD handling** (§4.2.3): the module is ESD-sensitive. Touch PCB GND first unless the board
is already well grounded; **connect antenna GND before the signal line**; keep away from
charged dielectric antennas, coax and soldering irons; do not touch exposed antenna
dielectric; use an ESD-safe iron on RF-input connectors.

**Mechanical** (§2.1, p. 7): body **A** 10.0/10.1/10.7 mm, **B** 9.6/9.7/9.8 mm,
**C** (height) 2.2/2.4/2.6 mm, pad pitch **F** 0.8 mm typ, pad **G** 0.4/0.5/0.6 mm,
**H** 0.8/0.9/1.0 mm, **K** 0.7/0.8/0.9 mm, **D** 0.55/0.65/0.95 mm, **E** 1.0/1.1/1.2 mm.
A PCB land-pattern drawing is given in §2.2 (0.9 / 0.65 / 0.80 / 1.1 mm on a 10.1 × 9.7
outline).

## 9. Refuted — claims the previous pass recorded that the datasheet contradicts

Recorded explicitly so they are not re-investigated. All refutations dated **2026-09-20**,
evidence = the manufacturer's manual V1.1.

| # | Previous claim | Status | Evidence |
|---|---|---|---|
| 1 | *"115200 bps is not the ATGM336H's usual factory default (9600 is common elsewhere) … Autobaud should include 9600"* | **REFUTED** | **115200 bps is the factory default**, stated twice: §1.2 variant table (both parts) and §2.6 *"波特率默认 115200bps"*. M5Stack is shipping the part at its own default, not reconfiguring it |
| 2 | *"The −162 dBm tracking figure quoted by M5Stack is for a board carrying an external MAX2659 LNA, not for the bare module. Attributing it to the module alone would be wrong."* | **REFUTED** | **−162 dBm tracking is the module's own published specification** (§2.6), with no external LNA. M5Stack is quoting the manufacturer's module figure verbatim. The repository's [`features/gnss.md`](../../../devices/m5stack/cap-lora-1262/features/gnss.md) claim that the LNA *"is what buys the −162 dBm tracking figure"* is **unsupported** |
| 3 | Manufacturer located in **Chengdu** | **REFUTED** | **Hangzhou** — cover, all 17 footers, address, 0571 area code, `hzzkw.com` (§1) |
| 4 | *"the `-6N` suffix denotes the variant/firmware grade"* | **SUPERSEDED** | `-6N` = **AT6668 hardware platform** (§5.2). The *hardware code* that follows (`-32` / `-74`) is what denotes the variant (§1.2) |

**Confirmed correct, and left alone:** the module's constellation/band list, the 50-channel
count, < 1.5 m CEP50, cold 23 s / hot 1 s TTFF, 10 Hz maximum update rate, NMEA 0183 4.1, and
the `AT6668` pairing all match the manufacturer's document exactly as M5Stack published them.

## 10. Used By

Fitment evidence is unchanged by this pass — it rests on M5Stack's schematics and
specification tables, not on the manufacturer's manual, which names no customer.

### [M5Stack Cap LoRa-1262 (U214)](../../../devices/m5stack/cap-lora-1262/README.md) — designator `M2`, symbol comment `GP-02`

**Evidence:** schematic V1.1 (designator + symbol) **plus** the product page specification
table giving `ATGM336H-6N@AT6668`. Direct, two independent sources.

| Function | Module pin | Board / host |
|---|---:|---|
| UART TX (module → host RX) | **2** (`TXD0`) | Cap-Bus 1 → host **G15** |
| UART RX (module ← host TX) | **3** (`RXD0`) | Cap-Bus 2 → host **G13** |
| `VCC` | 8 | `+3.3V` via `FB3` 120 Ω/MB |
| `VCC_RF` | 14 | ⚠ direction disputed — see §3.1 |
| `RF_IN` | **11** | ← `U1` **MAX2659** LNA `RFOUT` via `C5` 470 pF ← `J1` `ANT1818-04` patch |
| `VBAT` | 6 | `BT1` backup cell |
| `1PPS` (4), `ON/OFF` (5), `nRESET` (9), pads 16/17 | — | **not routed to the Cap-Bus** |

**So on this board it is a UART-only device with no host reset, no hardware standby and no
pulse-per-second.** Everything configurable must go over the serial link, via CASIC. Full
detail: [`devices/m5stack/cap-lora-1262/features/gnss.md`](../../../devices/m5stack/cap-lora-1262/features/gnss.md).

⚠ **The symbol comment reads `GP-02`, not `ATGM336H-6N`.** Still **unresolved**; the
manufacturer's manual contains no occurrence of `GP-02`, so it is not a vendor designation
from this document. Most likely an M5Stack internal library name, but that is `inferred`.

### [M5Stack Cap LoRa868 (U201)](../../../devices/m5stack/cap-lora868/README.md) — same part

Specification table gives the identical `ATGM336H-6N@AT6668` pairing and identical GNSS
figures; same two Cap-Bus lines (`GPS_TX` → G15, `GPS_RX` → G13). The U201 page additionally
publishes **state-resolved current** — GPS on / LoRa standby **29.24 mA** vs **GPS sleep /
LoRa standby 3.16 mA**.

> Worth noting against §5: the manufacturer's typical operating current is **42 mA @ 3.3 V**,
> while M5Stack's board-level figure is **29.24 mA at 5 V** for GPS-on. These are measured at
> different points on different rails and are **not directly comparable**; no conclusion is
> drawn.

### [M5Stack Cardputer Mesh Kit (K152)](../../../devices/m5stack/cardputer-mesh-kit/README.md)

Via the bundled Cap LoRa-1262. Indirect fitment — the kit contains the Cap; the module is not
separately on the kit's own board.

### Elsewhere in M5Stack's catalogue — **not** a fitment claim

The mirror this repository holds is served from M5Stack's **`Unit-GPS v1.1`** documentation
path. That establishes **only that M5Stack published this document under that product's
path** — M5Stack demonstrably reuses one upload across products (the same is true of its
CC1101 mirror, served from the `/1188/` CC1101-Module path). **It is not evidence that
Unit-GPS v1.1 fits an ATGM336H-6N.** No Unit-GPS record exists in this repository and the
product was not researched. `not-tested`.

## 11. Caveats

| # | Issue |
|---|---|
| 1 | **Pads 16/17: manufacturer says auxiliary UART, M5Stack's symbol says I²C.** Unresolved (§3.1) |
| 2 | **Pin 14 `VCC_RF` direction disputed** — manufacturer says output; the board records in this repository disagree with each other (§3.1) |
| 3 | **Which hardware code (`-32` or `-74`) M5Stack fits is not established** (§1.2) |
| 4 | **No NMEA sentence list and no configuration commands in this document** — both deferred to the CASIC specification (§7) |
| 5 | **Whether configuration changes persist across power cycles is not stated** (§7) |
| 6 | **1PPS has no pulse width, jitter or pre-fix behaviour specified** (§6) |
| 7 | **`ANTENNA OPEN` is the permanent normal state on passive-antenna boards** — and whether the two Caps report it is undetermined (§4.1) |
| 8 | `GP-02` remains unexplained (§10) |
| 9 | **This is a Chinese-language document with no English version located.** It is therefore the **primary source** for this part (§12) |
| 10 | No independent measurement of TTFF, accuracy, sensitivity or current. All figures are manufacturer claims, `not-tested` |
| 11 | **The AT6668 chip datasheet is referenced by this manual (p. 17) but is not held.** A known gap — see the [AT6668 record](../at6668/README.md) |

## 12. Related components

- [`components/zhongkewei/at6668`](../at6668/README.md) — the chipset inside, and the CASIC protocol
- [`components/analog-devices/max2659`](../../analog-devices/max2659/README.md) — the LNA in front of it on both Caps
- [`components/generic/gnss-ceramic-patch-antenna`](../../generic/gnss-ceramic-patch-antenna/README.md)

Note the manufacturer's own passive-antenna reference design (§2.7.2) specifies an **`AT2659`**
LNA — a Zhongke part whose number deliberately echoes the Maxim **`MAX2659`** that M5Stack
actually fits. **No record exists for the `AT2659` and the two were not compared**; do not
assume they are interchangeable on the strength of the number alone.

## 13. Local artifacts

| File | Bytes | SHA-256 | Provenance |
|---|---:|---|---|
| [`artifacts/atgm336h-6n-user-manual-v1.1-zh-m5stack-mirror.pdf`](artifacts/atgm336h-6n-user-manual-v1.1-zh-m5stack-mirror.pdf) | 752 259 | `7b1c10193709d7600e0234445a1c15603bf3443e14780ecde4818091ec2eda32` | `https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/unit/Unit-GPS%20v1.1/ATGM336H-6N.pdf`, retrieved 2026-09-04, HTTP 200, `%PDF-1.7`, 17 pp, A4 |

**Renamed 2026-09-20** from `atgm336h-6n-datasheet-m5stack-mirror.pdf` to house style with
the version now established from the document's own revision table. It is a **用户手册 (user
manual)**, not a datasheet — the name was corrected to say so.

**Document identity** (from the PDF's own metadata and revision history):

| Field | Value |
|---|---|
| Version | **V1.1** |
| Version date | **2023-01-11** |
| Revision history | V1.0 2022-08-26 初稿 (first draft) · **V1.1 2023-01-11 修改定位性能技术参数** ("revised positioning-performance specifications") |
| PDF `CreationDate` / `ModDate` | 2023-01-11 04:05:59 CST — **matches the stated revision date** |
| `Creator` / `Producer` | Microsoft® Word 2021 |
| `Author` | `微软用户` ("Microsoft User") — default, carries no information |
| Pages | 17 |

⚠ **V1.1's stated change is precisely "revised positioning-performance specifications."** So
the §2 sensitivity/TTFF/accuracy figures are **the ones that changed between V1.0 and V1.1**.
Any third-party source quoting ATGM336H-6N performance numbers may be quoting V1.0. **V1.0 is
not held** and was not located; the delta is therefore unknown.

⚠ **Vendor mirror, served from a different product's documentation path** (`Unit-GPS v1.1`).
Revision not cross-checked against ZhongKeWei's own publication at `hzzkw.com` — **no attempt
was made this pass** to fetch from the manufacturer, so whether a V1.2+ exists is unknown.

**Language:** Chinese only. **No English version was located**, and per the repository's
multi-language policy this Chinese document is accordingly the **primary source** for the
part and is retained in the repository on its own merit.

**Duplicate copy, retained, not deleted.** A byte-identical copy (same SHA-256
`7b1c1019…`, same 752 259 bytes) remains in the archive at
`archive/devices/m5stack/shared-artifacts/lora-expansions/research-scratch/artifacts/ATGM336H-6N-m5stack-mirror.pdf`,
left behind by the 2026-09-20 scratch drain. It is scratch residue, not a second source.

Licence/redistribution: **unknown** — the document states no terms. Disposition:
**repository, unstaged** pending review.

## 14. Sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| A-1 | **ATGM336H-6N 模块用户手册** | **Hangzhou Zhongke Microelectronics (杭州中科微电子)**, mirrored by M5Stack | authorized mirror | user manual (zh) | see §13 | 2026-09-04, **mined 2026-09-20** | **V1.1, 2023-01-11** | **§1–§9 in their entirety** — manufacturer identity, `-6N` meaning, variants, full specification, pinout, antenna behaviour, power, 1PPS, manufacturing |
| A-2 | Cap LoRa-1262 documentation | M5Stack | primary | official page | `https://docs.m5stack.com/en/cap/Cap_LoRa-1262` | 2026-09-04 | — | `ATGM336H-6N@AT6668`; fitment |
| A-3 | Cap LoRa868 documentation | M5Stack | primary | official page | `https://docs.m5stack.com/en/cap/Cap_LoRa868` | 2026-09-04 | — | Same module on the predecessor; state-resolved current |
| A-4 | Cardputer Mesh Kit documentation | M5Stack | primary | official page | `https://docs.m5stack.com/en/core/Cardputer_Mesh_Kit` | 2026-09-04 | — | Third citation of the pairing |
| A-5 | Cap LoRa-1262 schematic V1.1 | M5Stack | primary | schematic | [`devices/m5stack/cap-lora-1262/artifacts/schematic/`](../../../devices/m5stack/cap-lora-1262/artifacts/schematic/) | 2026-09-04 | V1.1 | The 18-pad symbol, designator `M2`, what is/is not routed |
| A-6 | `m5stack/TinyGPSPlus` | M5Stack | primary | repository | `https://github.com/m5stack/TinyGPSPlus` @ `254a10041ac38d17d98dab24c0ae4d2a8d19a677` | 2026-09-04 | 2025-01-02 | `MultipleSatellite`; **no LICENSE file** |
| A-7 | ZhongKeWei corporate site | Hangzhou Zhongke Microelectronics | primary | vendor site | `http://www.hzzkw.com` | — | — | ⚠ **not retrieved** — named in the manual (§1); a reacquisition route for newer revisions |
| A-8 | 《AT6668 芯片数据手册》 (AT6668 Chip Datasheet) | Hangzhou Zhongke Microelectronics | primary | datasheet | — | — | — | ⚠ **not retrieved, no URL known.** Referenced by the manual p. 17; a known gap |

## 15. Software

| Library | Notes |
|---|---|
| **`m5stack/TinyGPSPlus`** — class **`MultipleSatellite`** | M5Stack's fork, head `254a10041ac38d17d98dab24c0ae4d2a8d19a677` (2025-01-02). ⚠ Vendor documentation says explicitly: *"needs to be downloaded from the GitHub version adapted for M5Stack devices… **Do not download it from the Arduino Library Manager**"*. **No LICENSE file is present in the fork**; upstream TinyGPSPlus is LGPL-2.1 — flagged, unresolved |
| Meshtastic | built-in GPS subsystem; `GPS_BAUDRATE 115200` |
| Any NMEA parser | sufficient for position/time at the **default 1 Hz**; **not** sufficient for configuration |
| **`GNSSToolKit`** (vendor PC tool) | Named in manual §1.12 for output parsing and operating-mode configuration. **Not retrieved** |
| **`UBF 串口升级工具`** (vendor PC tool) | Serial firmware-upgrade tool, manual §1.12. **Not retrieved** |

`MultipleSatellite` adds M5Stack-specific calls — `setSystemBootMode(BOOT_FACTORY_START)`,
`setSatelliteMode(...)`, `getGNSSVersion()` — which are **CASIC binary commands**, not NMEA.
See the [AT6668 record](../at6668/README.md).
