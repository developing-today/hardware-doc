# Hangzhou Zhongke Microelectronics (杭州中科微电子有限公司)

> Documentation-sourcing knowledge for the GNSS vendor behind the **ATGM336H** module family
> and the **AT6668** / **AT6558** receiver SoCs. Created **2026-09-20**.

## 1. Identity — get this right first

| Property | Value | Evidence |
|---|---|---|
| Legal name (zh) | **杭州中科微电子有限公司** | ATGM336H-6N user manual V1.1, cover + all 17 page footers |
| English rendering | *Hangzhou Zhongke Microelectronics Co., Ltd.* | translation of the above; the company does not publish a canonical English name in this document |
| City | **Hangzhou** (杭州), Binjiang District | manual p. 1 address |
| Address | 杭州市滨江区江南大道 3850 号创新大厦 10 楼 | manual p. 1 |
| Phone / fax | 0571-28918100 / 0571-28918122 — **0571 is the Hangzhou area code** | manual p. 1 |
| Site | **`http://www.hzzkw.com`** — **hz** = Hangzhou, **zkw** = ZhongKeWei | manual p. 1 |
| Repository slug | **`zhongkewei`** | pre-existing; retained |

⚠ **Known trap: "Chengdu".** This repository previously recorded the company as
Chengdu-based. That was unsourced and is **refuted** — four independent signals in the
vendor's own document (address, area code, footer, domain) all say Hangzhou. Distributor
listings and parts aggregators attribute ZhongKeWei inconsistently; **trust the document
footer, not a listing.**

⚠ **Naming is genuinely ambiguous in the wild.** The company is variously written
ZhongKeWei, Zhongke Micro, Zhongke Microelectronics, CASIC Microelectronics and 中科微.
"中科" (Zhongke) is also a common prefix for Chinese Academy of Sciences spinoffs generally,
so a bare "Zhongke" match is **not** identification. Confirm against `hzzkw.com` or a
document footer.

### Relationship to "CASIC"

The binary configuration protocol these receivers speak is published as the **CASIC
Multi-mode Satellite Navigation Receiver Protocol Specification**. Whether "CASIC" here
denotes China Aerospace Science and Industry Corp., a product-line brand, or simply the
protocol's name as used across several Chinese GNSS vendors **was not established**. Treat
the protocol name and the company name as separate facts until evidence links them. See
[`components/zhongkewei/at6668`](../../components/zhongkewei/at6668/README.md).

## 2. Document-class checklist for a Zhongke GNSS part

The module manual is a thin entry point that **defers almost everything**. Expect to need
all of these; the manual names them on p. 17 and in §1.6/§1.8/§1.10/§1.12:

| # | Document (zh) | English | Covers | Held? |
|---|---|---|---|---|
| 1 | 《中科微 AGNSS 解决方案》 | Zhongke AGNSS Solution | assisted-GNSS injection | ❌ |
| 2 | **《中科微多模卫星导航接收机协议规范》** | **Multi-mode Satellite Navigation Receiver Protocol Specification** | **NMEA sentence set + all CASIC binary configuration** | ✅ archived — [`at6668/artifacts/`](../../components/zhongkewei/at6668/artifacts/) |
| 3 | 《ATGM 模块在线升级协议》 | ATGM Module Online Upgrade Protocol | field firmware update, incl. remote trigger | ❌ |
| 4 | **《AT6668 芯片数据手册》** | **AT6668 Chip Datasheet** | the silicon itself | ❌ **known to exist; no URL found** |
| 5 | 《GNSSToolKit 工具使用说明》 | GNSSToolKit manual | PC parsing/configuration tool | ❌ |
| 6 | 《UBF 串口升级工具使用说明》 | UBF serial upgrade tool manual | PC flashing tool | ❌ |

**The lesson:** a Zhongke *module user manual* will not tell you the NMEA sentences, the
baud-change command, the update-rate command or whether settings persist. Budget for
document 2 from the start — it is the one that matters.

## 3. Where documents were actually obtained

| Host | What it served | Notes |
|---|---|---|
| `m5stack.oss-cn-shenzhen.aliyuncs.com` | ATGM336H-6N user manual V1.1 (zh) | ⚠ served under a **different product's** path (`.../unit/Unit-GPS%20v1.1/ATGM336H-6N.pdf`). M5Stack reuses one upload across products — **a CDN path is not a fitment claim** |
| `m5stack-doc.oss-cn-shenzhen.aliyuncs.com` | CASIC protocol specification | numeric product-ID path prefix (`/1173/`), same reuse caveat |
| `www.hzzkw.com` | — | **never attempted.** The obvious primary route; untested |

**Both Zhongke documents this repository holds came from a customer's CDN, not the
manufacturer.** No document has been cross-checked against `hzzkw.com`, so whether newer
revisions exist is unknown for every one of them.

## 4. Version and naming conventions

**Model decomposition** (ATGM336H-6N manual §5.2) — this is a reusable three-field pattern:

```
ATGM336H  -  6N  -  32
└ product   └ type  └ hardware code
  (module     (silicon  (satellite-system set)
   size/      platform)
   series)
```

- `ATGM336H` → the 10.1 × 9.7 mm module series
- `6N` → built on the **AT6668** platform. **Not a firmware grade.** An older `-5N`-style
  code would imply different silicon (the AT6558 family) — *inferred from the pattern, not
  stated*
- `-32` / `-74` → the constellation set. **Vendors routinely drop this field**, as M5Stack
  does, leaving the actual variant unidentifiable from the part number alone

**Document versioning:** a 版本更新历史 (revision-history) table is on the **last page**, and
the PDF `CreationDate` has matched the stated revision date in the one case checked. Read
the last page first.

## 5. Document traps observed

- **Chinese-only.** No English version of the ATGM336H-6N manual was located. Under this
  repository's multi-language policy the Chinese document is therefore the **primary
  source** and belongs in the repo on its own merit.
- **Text layer is clean.** `pdftotext -layout` on the Word-2021-produced manual yields
  correct Chinese and correct numerals; values were cross-checked against a raw (non-layout)
  re-extraction and the rendered heading before transcription. No glyph-offset corruption
  observed — but check again per document.
- **Schematic symbols drawn by customers disagree with the vendor pin table.** Seen on the
  ATGM336H-6N: a customer symbol labelled pads 16/17 as I²C where the vendor defines a second
  UART, and drew a vendor-defined power *output* as an input. **Prefer the vendor's pin table
  and record the conflict.**
- **`Author` metadata is worthless** — `微软用户` ("Microsoft User"), a Word default.

## 6. Products in this repository

| Record | Part |
|---|---|
| [`components/zhongkewei/atgm336h-6n`](../../components/zhongkewei/atgm336h-6n/README.md) | ATGM336H-6N GNSS module — **manual mined 2026-09-20** |
| [`components/zhongkewei/at6668`](../../components/zhongkewei/at6668/README.md) | AT6668 GNSS SoC + CASIC protocol |

Reached via [M5Stack Cap LoRa-1262](../../devices/m5stack/cap-lora-1262/README.md),
[Cap LoRa868](../../devices/m5stack/cap-lora868/README.md) and the
[Cardputer Mesh Kit](../../devices/m5stack/cardputer-mesh-kit/README.md).

## 7. Open sourcing questions

1. Does `hzzkw.com` publish the manual directly, and at what revision? **Untested.**
2. Is the **AT6668 chip datasheet** publicly available anywhere? **Not found.**
3. What changed between manual **V1.0 (2022-08-26)** and **V1.1 (2023-01-11)**? The revision
   table says "修改定位性能技术参数" — *revised positioning-performance specifications* — so
   third-party sites quoting older sensitivity/TTFF figures may be quoting V1.0. **V1.0 not
   held.**
