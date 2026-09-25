# XUNPU TYPEC-302-BRP16SC08

> **USB Type-C 3.1 receptacle**, 16 contacts, female, surface-mount, rated **5 A / 5 V**, 10 000 mating cycles.
> Research snapshot **2026-09-01**. Fitted with the reference designator **`USB`, on sheet 2** of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) — the board's only external electrical interface besides the battery.
> **No hardware was available.** Every claim traces to the schematic PDF, the LCSC catalogue entry or the vendor drawing held in `artifacts/`.

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DWG]** | XUNPU drawing for `TYPEC-302-BRP16SC08`, local copy `artifacts/typec-302-brp16sc08-xunpu-lcsc-mirror.pdf` | `not-tested` |
| **[CAT]** | LCSC / JLCPCB catalogue entry `C2835312`, retrieved 2026-09-01 | `not-tested` |
| **[SCH-V]** | Read off sheet 2 of `PaperMono_SCH_V0.6.2_20260522.pdf` rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **`TYPEC-302-BRP16SC08`** | **[SCH-V]**, **[CAT]** |
| Manufacturer | **XUNPU** (深圳市讯普电子有限公司) | **[CAT]** |
| LCSC part | **`C2835312`** | **[CAT]** |
| Function | USB Type-C **receptacle** (female), USB 3.1 body, 16 contacts | **[CAT]** |
| Mounting | **SMD**, "laminated board" (板上贴片) style | **[CAT]** |
| Contacts | **16** — 12 signal + **4 shell/shield legs** | **[SCH-V]** |
| Current rating | **5 A** | **[CAT]** |
| Voltage rating | **5 V** | **[CAT]** |
| Durability | **10 000 insertion cycles** | **[CAT]** |
| Operating temperature | **−45 °C to +85 °C** | **[CAT]** |
| Body length | 6.5 mm | **[CAT]** |
| Colour | black insulator | **[CAT]** |
| RoHS | yes | **[CAT]** |

> ⚠ **The `5 V` voltage rating is the connector's own specification**, and it is
> the number a designer should notice: this is a receptacle sold for 5 V
> applications, not one qualified for the 20 V a full USB-PD contract can carry.
> On this board that is consistent — there is no PD (§3) — but it is a hard
> constraint on anyone thinking of retrofitting one. **[CAT]** + **[INF]**

---

## 2. ⚠ The datasheet is a single-page mechanical drawing with **no text layer**

`artifacts/typec-302-brp16sc08-xunpu-lcsc-mirror.pdf` is **1 page, 115 078 bytes**,
and `pdftotext` extracts **one byte** from it. Every glyph is a vector outline or
a raster.

Consequences, stated plainly:

- **There is no electrical specification in the document.** The ratings in §1
  come from LCSC's parametric fields, **not** from the manufacturer's own text.
  They should be treated as a distributor's transcription.
- No contact-resistance, insulation-resistance, dielectric-withstand or
  solder-profile figures were obtained for this part from any source.
- The drawing does carry the footprint and outline dimensions, but they must be
  read as an image. That was **not** done here — the PaperMono's PCB layout is
  not published, so the footprint could not be cross-checked against anything.

This is a normal state of affairs for Chinese connector vendors and is not a
defect in the acquisition; it is a limit on what can be asserted.

---

## 3. Used By

### `devices/m5stack/papermono` — **`USB`**, sheet 2

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).
**The [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md) uses
the same connector**: the Lite differs only in dropping NFC and LoRa, and its USB
path is unchanged. Its schematic is published as a 4-sheet `PRJ` PDF rather than
a 6-sheet `SCH`, so this is `inferred` from the product pages rather than read
from the Lite's own drawing.

> ⚠ **This connector's reference designator is the bare string `USB`** — letters
> only, no number. Its symbol carries `TYPEC-302-BRP16SC08` above and `USB`
> below; the [IP2315 charger](../../injoinic/ip2315/README.md) on the same sheet
> is `U1`. **[SCH-V]**
>
> **An earlier reading of the PaperMono census recorded this part as a second
> `U1` on sheet 2. That was wrong and is refuted here:** the Altium marker layer
> contains one `CO` marker with body `U1` and one with body `USB`, and the latter
> is accompanied by **16 `PIUSB01`…`PIUSB016` pin markers** — exactly a 16-contact
> receptacle. Sheet 2 has one `U1`.
>
> The digit-less designator has a practical consequence: **a census that filters
> designators with a `[A-Z]+[0-9]+` pattern drops this component silently.** That
> is how it went missing in the first place. See the
> [BOM §2.1](../../../devices/m5stack/papermono/bill-of-materials.md#21--two-parser-artefacts-had-to-be-repaired--and-one-of-them-refutes-a-claim).
> ⚠ [`pinouts-and-buses.md`](../../../devices/m5stack/papermono/pinouts-and-buses.md)
> still lists it as "`U1` (sheet 2)". Not corrected there by this pass.

### 3.1 Pinout as wired **[SCH-V]**

Read from sheet 2 rendered at 200 dpi. Pin names are the connector symbol's own.

| Pin | Name | Net on the PaperMono | Notes |
|---:|---|---|---|
| 1 | `GND` | `GND` | trace annotated **`20mil min`** |
| 2 | `VBUS` | **`VUSB_IN`** | to the [AW32901FCR](../../awinic/aw32901/README.md) OVP switch |
| 3 | `SBU2` | *(stub, unconnected)* | see §3.3 |
| 4 | **`CC1`** | `CC1` → **`R4` = 5.1 kΩ** → `GND` | §3.2 |
| 5 | `DN2` | `USB_N` | tied to pin 7 |
| 6 | `DP1` | `USB_P` | tied to pin 8 |
| 7 | `DN1` | `USB_N` | tied to pin 5 |
| 8 | `DP2` | `USB_P` | tied to pin 6 |
| 9 | `SBU1` | *(stub, unconnected)* | see §3.3 |
| 10 | **`CC2`** | `CC2` → **`R14` = 5.1 kΩ** → `GND` | §3.2 |
| 11 | `VBUS` | **`VUSB_IN`** | paralleled with pin 2 |
| 12 | `GND` | `GND` | paralleled with pin 1 |
| 13–16 | `SHELL` ×4 | shell / shield | |

`USB_N` and `USB_P` continue to `TVS1` and `TVS2`
([ESD5311](../../generic/esd5311/README.md)), then through the
`ICMF062P900MFR` common-mode choke `FT1` and the 22 Ω series resistors `R40`/`R41`
on sheet 3, to ESP32-S3 GPIO19/GPIO20.

### 3.2 ⚠ The CC arrangement: a plain sink, and no USB-PD — twice over

This is the single most important thing about how this connector is wired.

**Both CC lines carry a 5.1 kΩ pulldown to ground:**

| Resistor | On | Value | Function |
|---|---|---|---|
| **`R4`** | `CC1` (pin 4) | **5.1 kΩ ±1 %** | R<sub>d</sub> |
| **`R14`** | `CC2` (pin 10) | **5.1 kΩ ±1 %** | R<sub>d</sub> |

5.1 kΩ on both CC pins is the USB Type-C specification's **R<sub>d</sub>** — the
advertisement *"I am a sink (UFP); give me default USB current"*. Putting it on
both lines is what makes the cable orientation-independent: whichever CC the
plug lands on, the source sees R<sub>d</sub> and applies V<sub>BUS</sub>.

> The [device record's earlier note](../../../devices/m5stack/papermono/pinouts-and-buses.md)
> mentions only one CC resistor. **There are two**, `R4` on `CC1` and `R14` on
> `CC2`, both 5.1 kΩ/1 %. Confirmed by rendering the block at 200 dpi.
> Date 2026-09-01. **[SCH-V]**

**Meanwhile the charger's own CC pins are depopulated.** The
[IP2315](../../injoinic/ip2315/README.md) can negotiate USB-PD, FCP, AFC and
PE+ by itself, and its `CC1`/`CC2` (pins 2 and 3) reach the connector through
`R1` and `R2` — both of which carry the value **`NC/1%`**, i.e. **not fitted**.

So there are two independent reasons this is a 5 V-only port:

1. **Passive R<sub>d</sub> only.** With plain 5.1 kΩ pulldowns and nothing driving
   or listening on CC, the port cannot send or receive a PD message. A PD source
   will see a legacy sink and hold V<sub>BUS</sub> at 5 V.
2. **The one chip that could negotiate is disconnected from CC.** Even if a
   controller wanted to talk, `R1`/`R2` are open.

And a third, upstream: the [AW32901FCR](../../awinic/aw32901/README.md) OVP
switch is configured with a **5.95 V** over-voltage threshold, so a higher
negotiated voltage would be cut off rather than merely unused. **[SCH-V]**

**Practical consequence.** Charge current is limited by what the IP2315 draws
from a 5 V supply. Nothing a user plugs in — PD brick, PPS supply, laptop port —
changes that. Anyone reading the IP2315 datasheet and expecting 9 V fast charge
on a PaperMono will be disappointed, and the reason is here, not in the charger.

### 3.3 `SBU1`/`SBU2` are unconnected — but that is an *omission*, not an assertion

Pins 3 and 9 terminate in short stubs with nothing attached and **no drawn
no-connect marker**. That distinction matters: elsewhere on this schematic the
designer *does* place explicit red ✗ markers (on the buzzer symbol on sheet 4,
on the `PYB_NFC_EN` stub at `J3`). Here they did not.

So the correct reading is **"unknown/unused"**, not "the designer asserted these
must not be connected". In practice SBU is used only for alternate modes
(DisplayPort, debug accessory), none of which this board supports. **[INF]**

---

## 4. Equivalents and substitution

The pin *function* order of a USB-C receptacle is fixed by the USB Type-C
specification, so any 16-pin mid-mount/SMT receptacle is functionally a
candidate. What is **not** interchangeable is the mechanical part: shell height,
leg pattern, board cut-out and retention geometry differ between vendors and
between "laminated board"/sinking depths within one vendor.

| Alternative | vs. this part | When |
|---|---|---|
| XUNPU `TYPEC-304-BCP16` and siblings | Same vendor, different mount style | Same ecosystem, different board thickness |
| Korean Hroparts / Jing Extension 16-pin USB-C | Widely stocked at LCSC | Cost |
| Amphenol, Molex, JAE 16-pin USB-C | Documented, qualified, far more expensive | When the 5 V rating or the 10 000-cycle figure is not enough |

> **Do not substitute by pin count alone.** 16-pin USB-C receptacles exist in at
> least four incompatible footprints. Without the PaperMono's PCB layout — which
> M5Stack does not publish — the footprint cannot be matched from this record.

---

## 5. Integration pitfalls

1. **This is a 5 V-rated connector on a 5 V-only port.** Correct as built, but
   it forecloses retrofitting PD without changing the connector *and* `R1`/`R2`
   *and* the AW32901's OVP threshold (§3.2).
2. **The datasheet has no electrical section** (§2). Do not quote a
   contact-resistance or dielectric figure for this part; none was obtained.
3. **Two `U1`s on sheet 2** (§3). A designator-based search will find the wrong
   one half the time.
4. **`SBU1`/`SBU2` are open with no ERC marker** (§3.3) — do not read that as a
   designed no-connect.
5. **The shell is four separate contacts (13–16)**, not one. Whether they are
   commoned inside the connector is not shown by the drawing's text and was not
   verified.

---

## 6. Open questions

- The drawing's mechanical dimensions and footprint (§2) — readable only as an
  image, and with no published PCB layout to check them against.
- Whether the four shell legs are internally commoned.
- Contact resistance, insulation resistance and the reflow profile — absent from
  every source found.
- Whether the PaperMono-Lite fits the identical part number (`inferred`, §3).

---

## Manufacturer

**XUNPU** (深圳市讯普电子有限公司) is a Shenzhen connector maker whose catalogue
is distributed almost entirely through LCSC. It has no vendor sourcing guide in
this repository yet. The same vendor supplies this board's
[`BTB0.408-10PLBDR-G41`](../../generic/btb0.408-10plbdr-g41/README.md)
board-to-board connector, for which **no datasheet exists at all**.

**⚠ Retrieval finding — the LCSC PDF host trap, confirmed again.** For this part
the working URL is on **`wmsc.lcsc.com`**:

| URL | Result |
|---|---|
| `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2105281102_XUNPU-TYPEC-302-BRP16SC08_C2835312.pdf` | **200, `%PDF` ✓** |
| `https://www.lcsc.com/datasheet/…` (the form LCSC's own product page links) | **HTTP 200 with `text/html`** — an interstitial page, not the document |

`www.lcsc.com/datasheet/*.pdf` returns **HTTP 200 and a `.pdf` URL while serving
HTML**. The status code is worthless; only the `%PDF` magic at byte 0 decides.
The mechanical rewrite that works is
`www.lcsc.com/datasheet/lcsc_datasheet_<stamp>_<name>_<code>.pdf` →
`wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/<stamp>_<name>_<code>.pdf`.
This matches the finding already recorded in the
[IP2315 record](../../injoinic/ip2315/README.md#manufacturer) and belongs in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

Part discovery itself was done through **JLCPCB's SMT parts API**, which answers
with compact JSON including manufacturer, package and datasheet URL, and which —
unlike DuckDuckGo-lite, Mojeek and searx.be, all of which blocked or captcha'd
`curl` on 2026-09-01 — is not bot-filtered:

```bash
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"keyword":"TYPEC-302-BRP16SC08","currentPage":1,"pageSize":3}' \
  https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList
```

`executed-success`, 2026-09-01. Helper:
[`archive/devices/m5stack/papermono/artifacts/research-scratch/tools/lcsc_lookup.sh`](../../../archive/devices/m5stack/papermono/artifacts/research-scratch/tools/lcsc_lookup.sh).

## Related pages

- [Awinic AW32901FCR](../../awinic/aw32901/README.md) — `U2`, the OVP switch `VUSB_IN` feeds
- [Injoinic IP2315](../../injoinic/ip2315/README.md) — `U1` sheet 2, whose CC pins are depopulated
- [ESD5311](../../generic/esd5311/README.md) — `TVS1`/`TVS2` on `USB_N`/`USB_P`
- [USB-C target-selection interface](../usb-c-interface/README.md) — the generic interface record
- [PaperMono bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)
- [PaperMono USB and serial feature guide](../../../devices/m5stack/papermono/features/usb-and-serial.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| D1 | `TYPEC-302-BRP16SC08` drawing | XUNPU (via LCSC CDN) | primary, via distributor mirror | <https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2105281102_XUNPU-TYPEC-302-BRP16SC08_C2835312.pdf> | 2026-09-01 | undated, 1 p | mechanical outline only — **no text layer**, §2 | `artifacts/typec-302-brp16sc08-xunpu-lcsc-mirror.pdf` |
| C1 | LCSC catalogue entry `C2835312` | LCSC / JLCPCB | distributor | <https://www.lcsc.com/product-detail/usb-connectors_xunpu-typec-302-brp16sc08_C2835312.html> | 2026-09-01 | — | manufacturer, 16P, 5 A, 5 V, 10 000 cycles, −45…+85 °C, 6.5 mm | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | the §3.1 pinout, `R4`/`R14` = 5.1 kΩ, `R1`/`R2` = `NC`, **the designator `USB` and its 16 pin markers** | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/typec-302-brp16sc08-xunpu-lcsc-mirror.pdf` | 115 078 | `99d0419afa7fb46d18ad9b441fef7c327482305ed9dd6a26013c40f4631df7ed` | 1 |

**Method note.** D1 was fetched with `curl`, validated as `%PDF` (`executed-success`),
and found to carry no text layer (`pdftotext` yields 1 byte). The pinout in §3.1
was read from a 200 dpi PNG render of schematic sheet 2, not from the text layer —
which for this block interleaves the connector's pin names with the neighbouring
charger's and cannot be separated reliably.
