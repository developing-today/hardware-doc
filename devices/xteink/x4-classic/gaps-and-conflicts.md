# Xteink X4 Classic — gaps and conflicts

Snapshot **2026-09-04**. **The defining characteristic of this record is an
inversion: the hardware is better documented than the product.**

## The inversion, stated plainly

| Well established | Completely unknown |
|---|---|
| Every GPIO, with per-pin confidence levels | **Price** |
| All three I²C peripherals and addresses | **Where or whether you can buy it** |
| Display pinout, SPI clock, controller-selection mechanism | **Dimensions, mass, battery capacity** |
| Button map, corrected by hardware testing | **Any photograph of the device** |
| Partition layout, board tag, revision string, stock version | **Whether it is sold under another name in China** |
| Build configuration | **Whether anyone outside China owns one** |

This happens because the **only** source is a firmware dump. A dump tells you
everything about the board and nothing about the product.

## Open technical questions

### 1. GPIO4 — configured, never used

The stock board-init registers GPIO4 as a **plain input, mode 0, not
interrupt-attached**. It is therefore not a button. The SDK does not read it.

**Nobody knows what it is.** Candidates, none supported: a hall/lid sensor, a
hardware-variant strap, a second charge/fault line, or a depopulated feature. The
fact that stock configures it at all argues it is connected to something.

**What would resolve it:** read it on hardware under varied conditions
(lid/case on and off, charger in and out, magnet nearby), or a teardown.

### 2. Charge-STAT polarity

`batteryChargeStatus = 21`, `batteryChargeStatusActiveHigh = true` — **carried over
from the X4 Pro** rather than independently confirmed. The SDK marks it `PENDING`.

### 3. Panel orientation

Ships `NO_FLIP`. Pending hardware.

### 4. `ESP32S3_X4R2_CLA` — does an R1 exist?

The board revision string contains `R2`. **No R1 has been observed.** It may be an
internal iteration, or the shipping X4C may already be a revision-2 board. Nothing
distinguishes them externally because nothing external has been seen at all.

### 5. Bezel insets are inherited, not measured

`viewableInsets = {9, 7, 3, 7}` are the X4 Pro's values, adopted on the grounds of
identical glass and explicitly *"pending measurement"*.

## A community claim that does not match the firmware

[r/XTEINK `1ud0d9c`](https://old.reddit.com/r/XTEINK/comments/1ud0d9c/) (2026-06-22,
**300 points**) is the post that first identified this device in a vendor video:

> "Did we just spot a new X4 model? **Physical buttons + frontlight** but no
> touchscreen in the latest video?"

The community was **right about the buttons and the absence of touch, and wrong
about the frontlight**. The X4C's `BoardProfile` sets `NO_FRONTLIGHT`, and the
stock firmware itself reports *"Frontlight hardware is disabled on this board"*.
Firmware evidence beats video interpretation.

**But there is a live complication.** A separate 2026-08-25 thread about a coming
"X4 version 2" contains this claim:

> "Leaked versions shows the X4 v2 with pogos and **another X4 with pogos,
> backlight and no touch**."
> — [r/xteinkereader `1vxsr0x`](https://old.reddit.com/r/xteinkereader/comments/1vxsr0x/) · **hearsay, unverified**

If a buttons-plus-frontlight-no-touch device genuinely exists, it is **not** the
X4 Classic documented here — the dump is unambiguous. It would be a *further*
model. Recorded so that a future pass does not merge them.

## Gaps — commercial

- **No price has ever been published**, in any currency, on any channel.
- The vendor's own `x4-classic` Shopify collection **exists and contains no
  device** — only four generic accessories. That is a strong signal the SKU was
  provisioned for an international launch that has not happened.
- **No listing was found** on AliExpress, Amazon or Xianyu in this session's
  searches — though Chinese marketplaces were **not searched directly**, so this
  is a weak negative.

## Gaps — physical

No teardown, no photograph, no PCB image, no dimensions, no mass, no battery
capacity, no connector identification, **no evidence of what its charging
connector even is** (USB-C like the X4, or pogo like the X3 and X4 Pro — the dump
does not say, and this is a first-order question for a buyer).

## Gaps — regulatory

None read. See the family finding in
[`../x4-pro/gaps-and-conflicts.md`](../x4-pro/gaps-and-conflicts.md) and the
X3 record: Xteink devices generally **carry no external CE/FCC marking**, with
regulatory text placed in software instead.

## Gaps — community

**Zero.** No X4C owner report, bug report, firmware fork, flashing guide, review or
photograph was found in a corpus of **2,136 Reddit posts** and a
**~200-repository GitHub census**. This device has no community footprint at all
outside the FreeInk SDK.

That is itself the finding: **the X4 Classic is documented but not distributed.**

---

# Round 2 — 2026-09-11. Gaps closed, gaps opened, conflicts recorded.

**No line above this rule was altered.** Several items above are now answered;
they are answered *here* rather than edited in place.

## A. Closed

| Was open | Now | Evidence |
|---|---|---|
| No price, no listing, no availability | **US$79.00, listed 2026-09-06, in stock** | vendor API `published_at` |
| No dimensions, mass, battery capacity | **114 × 69 × 4.9 mm · 68 g · 920 mAh** | vendor spec block |
| Charging connector unknown | **Pogo pin, 4 contacts, magnetic. No USB-C** | vendor spec block; confirmed by the label exhibit's rear photograph |
| No regional name | **`XTEINK X4 Classic (X4 V2)`** — both names, one product | vendor title, vendor announcement, FCC description |
| Whether it is sold internationally | **Yes** | — |
| No photograph of any kind | **One public regulatory photograph** (rear, with label) | `artifacts/certification/2BTR9-X4C-label.pdf` |
| No regulatory filing found | **FCC ID `2BTR9-X4C`, granted 2026-07-20** | fccid.io |
| Manufacturer's legal identity unknown | **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**, Longhua District, Shenzhen, FRN `0037772233` | FCC grantee record |
| `xteink.cn` unreachable, ownership unproven | **The FCC filing lists `xteink.cn` as the applicant's domain** and the responsible party's e-mail is `chuchen@xteink.cn` | FCC |

## B. `R2` — narrowed, not closed

Detailed in [`README.md`](README.md) §`R2`. In short: the same X4 Pro stock binary
carries **all four** S3 board tags, so the tags are a shared-codebase enum rather
than a per-unit revision stamp; `"X4R1_CLA"` returns **zero** results on GitHub
code search; there is **no earlier X4C FCC grant**; and both the vendor ("X4 V2")
and owners ("the V1") treat the plain X4 as version 1.

**Most economical reading: `X4R2` = "X4, revision 2", and revision 1 is the C3
X4.** Not proven. An unreleased engineering-sample X4C R1 cannot be excluded from
public sources and never will be.

**What would settle it:** the `SCH`/`BLOCK` exhibits (**permanently
confidential** — never), a silkscreened revision in the internal photographs
(**2027-01-16**), or a second stock dump from a *known* X4 Classic showing a
different revision string.

## C. Still open

| # | Gap | What would settle it |
|---|---|---|
| R2-1 | **GPIO4's role.** Neither FreeInk nor Draftling uses it; FreeInk calls it *"a plain input (not a button, not used by the SDK)"* | Internal photographs (2027-01-16), or a continuity measurement |
| R2-2 | **Charge-`STAT` polarity on GPIO21** is `inferred` from a profile field, never observed | A multimeter on a charging unit |
| R2-3 | **Panel orientation** — no `DisplayOrientation` has been verified on hardware | One photograph of a booted X4C running a known image |
| R2-4 | **BM8563 `CLKOUT` → ESP32-S3 `XTAL_32K_P`/GPIO15?** Asked publicly 2026-09-10, unanswered. Would enable low-power always-on BLE | Internal photographs, or continuity |
| R2-5 | **Which panel controller ships in retail units.** `hw_calib/screenType` is set per unit at the factory; the retail distribution is unknown. A physical X4 **Pro** read `screenType = 2` (**UC8279**) on 2026-09-06 — that is one unit of a *different* model | `[XTDET]` console lines from several X4C units |
| R2-6 | **Chinese-market launch date and price.** JD, Taobao, Xianyu and Xiaohongshu were **not searched** this pass | Those marketplaces |
| R2-7 | **No X4C-specific stock-firmware version is corroborated.** FreeInk analysed `xteink_app` v7.0.11; a physical X4 **Pro** shipped **7.2.4** (ESP-IDF v6.0.1, built 2026-08-14) and a **7.5.4** analysis exists. The X4C's shipping version is unknown | Any X4C `esptool read-flash` |
| R2-8 | **Nothing measured.** No refresh time, no deep-sleep current, no page-turn latency, no contrast measurement | See [`performance.md`](performance.md) §4 |

## D. New conflicts, recorded rather than resolved

### R2-C1 — the product page contradicts itself about file formats

| Source | Claim |
|---|---|
| Spec block, same page | *"Document: **EPUB, TXT** / Image: BMP / Fonts: BIN, XTF"* |
| FAQ, same page | *"XTEINK supports **TXT, EPUB, MOBI, PDF, XTCH, XTC, and XTCZ** formats"* |

Both were retrieved from one HTML document on 2026-09-11. The FAQ text is
brand-wide boilerplate ("XTEINK supports…"), the spec block is device-specific.
**Neither is treated as authoritative.** This is consistent with the family's
established finding that `xteink.com` prose is SEO-generated and unreliable — the
X3 listing still advertises a frontlight the X3 does not have.

### R2-C2 — "4.3 inch" vs 4.26″

The vendor's spec block says **4.3 inch**; the firmware, the FreeInk docs and
every other record in this tree say **4.26″**. 800×480 at 219 PPI computes to
4.26″. **Vendor rounding**, recorded for completeness.

### R2-C3 — an "E-ink secondary screen on the back"

The product-page FAQ asks *"How do I customize the E-ink secondary screen on the
back?"* and answers with instructions for setting a **power-off / sleep
wallpaper**. There is **no second display**: the answer describes the main panel
retaining an image when off, which is what e-paper does. The question is
mis-worded marketing copy. **No evidence of a second panel exists in the board
profile, the FCC filing, any review or any photograph.** Recorded so it is not
re-investigated.

### R2-C4 — "better screen" vs unchanged pixel density

Two launch reviewers describe improved contrast; one of them calls it *"a slight
improvement in the screen resolution"*. **The density is unchanged at 219 PPI**,
corrected inside the same thread by u/scamper_ (*"It does not, it's still 219"*)
and independently by u/ajcabrera (*"Both use the same 219 PPI screen"*).

Whether *contrast* improved is **unresolved**: it could be a panel-controller
batch difference (SSD1677 vs UC8179 vs UC8279 drive the same glass differently),
a waveform change, the absence of the Pro's touch and frontlight layers — one
commenter, u/quangvu1991, offers exactly that mechanism — or observer bias on
vendor-supplied units. **No photometry exists.**

### R2-C5 — EU price vs store price

US$79.00 (vendor API, 2026-09-11) against **€89** reported by an EU buyer the
same week ([r/XTEINK `1w9jzpn`](https://old.reddit.com/r/XTEINK/comments/1w9jzpn/),
2026-09-07). Almost certainly VAT and regional pricing, **but it was not
normalised** and no EU store page was retrieved. Do not quote a single "price"
for this device without a region.

### R2-C6 — X4 Pro touch orientation: a new disagreement, inherited here

Not an X4C conflict — the X4C has no touch — but it bears on how much to trust
the shared profile, so it is flagged:

| Source | Claim |
|---|---|
| FreeInk `BoardConfig.h` | `swapXY=true, flipX=false, flipY=true` — *"confirmed by corner-tap"* |
| `kycube/x4pro-emu` `docs/hardware.md` | repeats FreeInk's values and notes the support **doc's** I²C paragraph has INT/RST swapped and is *"stale"* |
| **`clackups/draftling` `HARDWARE.md`** | *"the FreeInk SDK's starting values (`swapXY=true, flipY=true`) had touches landing **180 degrees opposite** of where the finger was"* — corrected against a physical unit to `MIRROR_X`/`MIRROR_Y` = 1/0 |

Draftling's is the only **on-hardware** claim of the three, but it is made inside
a different rendering stack with its own orientation convention, so the two are
not necessarily contradictory. **Recorded as unresolved**, and carried to
[`../x4-pro/gaps-and-conflicts.md`](../x4-pro/gaps-and-conflicts.md).

## E. A pre-existing statement confirmed correct

The 2026-09-04 record's claim that **the X4 Classic has no frontlight** was
challenged by the community from June to September and was **right**. The
vendor's own spec block now reads `Front light: No` and the FAQ says so in
prose. The conflict listed above as item 8 of `VERIFICATION-xteink.md`
("X4 Classic reported with a frontlight by the community; firmware says none")
is **resolved in favour of the firmware**.
