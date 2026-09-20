# `aida_remote_1.85/` — extracted contents of `../Aida_remote_1.85.zip`

Extracted **2026-08-24**. The ZIP (`../Aida_remote_1.85.zip`, 475 bytes) is also retained —
at that size the duplication is meaningless and the ZIP is the byte-exact original.

| Field | Value |
|---|---|
| Archive | `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/tools/Aida_remote_1.85.zip` |
| Archive SHA-256 | `81f6d7c78f89fb4834cb7c0381baf5644bdb5e35888fba172e439f59053cbdc5` |
| Archive size (pre-extract) | **475 bytes** |
| Extracted size (post-extract) | **1,728 bytes** |
| File count when extracted | **1** |
| Extracted file SHA-256 | `f396b4c8f8352bce1fa21e75a336ec96e4c9098d5a9842bbb2a9ea90e56773c3` |
| Version | **1.85** (Waveshare's layout version, from the filename) |
| Release date | Member mtime **2024-06-25 15:54**; server `Last-Modified` **Thu, 19 Jun 2025 12:58:26 GMT** |
| Author / vendor | Waveshare Electronics — this is a Waveshare-authored layout, not an AIDA64 product file |
| License | **None stated.** Redistribution status `unknown` |
| Upstream repo / commit | Not applicable |
| Disposition | `repository` — kept, both forms |

## Contents

```
aida_remote_1.85/
└── aida_remote_1.85.rslcd    1,728 bytes, ASCII text, CRLF
```

**No PDFs, no datasheets, no binaries.** One plain-text file.

## What a `.rslcd` file is

`.rslcd` is the **AIDA64 "RemoteSensor / LCD" layout format**. [AIDA64](https://www.aida64.com/)
is a commercial Windows system-monitoring application; its *SensorPanel / LCD* feature pushes
live host telemetry (CPU load, clocks, temperatures, fan speeds) to an external display. This
file is the **screen layout** that makes AIDA64 render correctly on this board's 360×360 round
panel — it is the missing piece for the board's `aida64` demo app.

It is a tag-delimited text format, trivially readable and editable:

```
<LCDVER>200</LCDVER><SWVER>6.33.5741 Beta</SWVER>
<LCDBGCOLOR>16777215</LCDBGCOLOR>
<LCDPAGE1>
  <ID>[SIMPLE]SCPUUTI</ID><TXTSIZ>8</TXTSIZ><FNTNAM>Tahoma</FNTNAM>
  <TXTCOL>0</TXTCOL><TXTBIR>000</TXTBIR><SHWLBL>1</SHWLBL><LBL>CPU usage</LBL>
  <SHWUNT>1</SHWUNT><UNT>^</UNT><ITMX>0</ITMX><ITMY>0</ITMY>
  <ID>[SIMPLE]SCPUCLK</ID>…
```

Fields decode as: `ID` = AIDA64 sensor identifier (`SCPUUTI` = CPU utilisation, `SCPUCLK` = CPU
clock), `LBL`/`SHWLBL` = label text and whether to draw it, `UNT`/`SHWUNT` = unit suffix,
`TXTSIZ`/`FNTNAM`/`TXTCOL` = typography, `ITMX`/`ITMY` = pixel position on the page.

Two version numbers are embedded and they mean different things:

- `LCDVER 200` — the layout **file-format** version.
- `SWVER 6.33.5741 Beta` — the **AIDA64 build that authored it**. AIDA64 6.33 dates to
  2021. Waveshare's "1.85" in the filename matches neither; it is a distribution label.

## Why it is kept as-is

It is 1.7 KB of plain text, it is Waveshare-authored (so not reacquirable from AIDA64), it is
directly readable, and it documents the sensor set the board's AIDA64 demo expects. There is
nothing to extract from it and nothing to archive. Both the ZIP and the extraction stay.

Note the connection to [`../../examples/catalog.md` §2](../../../examples/catalog.md): the
as-shipped SD card contains an undocumented `aida64/` directory of 18 selectable backgrounds
(`001`–`017` plus `00_ff0000`). This layout file and those assets are two halves of the same
feature.

## Reacquire

```bash
# Source 1 — Waveshare shared file pool (primary)
curl -L -O https://files.waveshare.com/wiki/common/Aida_remote_1.85.zip

# Source 2 — Internet Archive, 2025-08-22 capture
curl -L -o Aida_remote_1.85.zip \
  "https://web.archive.org/web/20250822191132id_/https://files.waveshare.com/wiki/common/Aida_remote_1.85.zip"

# Source 3 — Internet Archive, 2026-01-01 capture
curl -L -o Aida_remote_1.85.zip \
  "https://web.archive.org/web/20260101172223id_/https://files.waveshare.com/wiki/common/Aida_remote_1.85.zip"
```

## Verify

```bash
sha256sum Aida_remote_1.85.zip
# expect 81f6d7c78f89fb4834cb7c0381baf5644bdb5e35888fba172e439f59053cbdc5
unzip -p Aida_remote_1.85.zip aida_remote_1.85/aida_remote_1.85.rslcd | sha256sum
# expect f396b4c8f8352bce1fa21e75a336ec96e4c9098d5a9842bbb2a9ea90e56773c3
```

## URL probe results (2026-08-24)

| URL | HTTP | Content-Length | Last-Modified |
|---|---|---:|---|
| `https://files.waveshare.com/wiki/common/Aida_remote_1.85.zip` | `200 OK` | 475 — **matches** | `Thu, 19 Jun 2025 12:58:26 GMT` |
| `https://web.archive.org/web/20250822191132id_/…` | `200 OK` (CDX) | — | capture 2025-08-22 |
| `https://web.archive.org/web/20260101172223id_/…` | `200 OK` (CDX) | — | capture 2026-01-01 |

Both Internet Archive captures share CDX content digest `ZJYNK4KPEL3EIELWUTO3EDJUEUEMXBET`.

> Direct download of the Wayback copies was attempted on 2026-08-24 but the Internet Archive was
> intermittently returning its "Temporarily Offline" page. The CDX index confirms both captures
> exist with a stable content digest; the payload bytes were **not** independently hash-verified
> for this file, unlike the schematic and BIN archives. Recorded as-is rather than overstated.
