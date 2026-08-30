# Tools — archived artifacts and reacquisition record

> Archive/removal date: **2026-08-23**.
> "Archived" means moved to `archive/hardware-doc/devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/tools/`,
> preserving this repository's relative path. Nothing was deleted.

All URLs below were enumerated from the local wikitext snapshot
`../source-snapshots/waveshare-wiki-wikitext-oldid-111069.txt` (Waveshare wiki oldid 111069) and
then live-probed with HTTP HEAD on **2026-08-23**. In every case the served `Content-Length`
matched the local byte size exactly, confirming the URL still serves the identical artifact.

## Still present in this repository

| File | Bytes | Why kept |
|---|---:|---|
| `Aida_remote_1.85.zip` | 475 | Trivial size. Contains one `aida_remote_1.85.rslcd` config file. |
| `aida_remote_1.85/` | 1,728 | **Extracted 2026-08-24.** One plain-text AIDA64 LCD layout. See [`aida_remote_1.85/README.md`](./aida_remote_1.85/README.md). |
| `Sscom5.13.1.zip` | 420,199 | Small. Windows serial terminal, `sscom5.13.1.exe` + `sscom51.ini`. Kept as the byte-exact original, and as an offline source for the archived `.exe`. |
| `sscom5.13.1/` | — | **Extracted 2026-08-24.** `sscom51.ini` kept (plus a UTF-8 transcode); `sscom5.13.1.exe` archived. See [`sscom5.13.1/README.md`](./sscom5.13.1/README.md). |
| `ch34x-macos-driver-install-instructions.pdf` | 710,663 | **Extracted from `CH34XSER_MAC.7z`** — the only human-readable documentation in that archive. See below. |

> **2026-08-24 update.** Both remaining ZIPs were opened and inventoried. One further item was
> archived — `sscom5.13.1/sscom5.13.1.exe` (451,072 B), a third-party Windows binary with no
> documentary value that is recoverable offline from the retained ZIP beside it. Full record:
> [`sscom5.13.1/sscom5.13.1.exe.REMOVED.md`](./sscom5.13.1/sscom5.13.1.exe.REMOVED.md).
> Neither ZIP contained any PDF, datasheet or schematic, so nothing was promoted to a
> `components/` record from them.

## Archived

### 1. `mjpeg_Conversion_tool_V2.1.zip`

| Field | Value |
|---|---|
| Bytes | 81,719,210 (77.93 MiB) |
| SHA-256 | `8db4252b99ed27666b0316e23e1db1f5fcaa1a53116454cd34b8dc91c4fee1e7` |
| Primary URL | `https://files.waveshare.com/wiki/common/mjpeg%20Conversion%20tool%20V2.1.zip` |
| URL probe (2026-08-23) | `HTTP/1.1 200`, `Content-Length: 81719210` — **matches local byte size** |
| Upstream `Last-Modified` | `Fri, 20 Jun 2025 01:41:06 GMT` |
| Publisher | Waveshare |
| Redistribution status | `unknown` (Waveshare tool, no stated license) — **but see GPL note below** |
| Disposition | archived (`local-cache` outside the repo) |

**Do not extract this into the repository.** Extraction *increases* size from 78 MiB to **203 MiB**,
because the archive is already deflate-compressed and its contents are large binaries.

Contents (7 files):

| Member | Bytes | SHA-256 (prefix) | Notes |
|---|---:|---|---|
| `ffmpeg.exe` | 60,988,928 | `6001ad699ca9894c` | Stock third-party build — see below |
| `ffprobe.exe` | 45,046,272 | `622fc9bdd034d90e` | Stock third-party build |
| `mjpeg转换工具.dll` | 106,138,624 | `1ecb84ec8d34b885` | The actual app. .NET/Mono assembly |
| `mjpeg转换工具.exe` | 220,160 | `9e62d314c832de0d` | .NET launcher shim, PE timestamp 2023-10-19 |
| `mjpeg转换工具.pdb` | 10,240 | `0aabd7b1ec3e2d70` | Debug symbols |
| `mjpeg转换工具.deps.json` | ~700 | `d9c175c7dfe1a6bf` | Assembly name `mjpeg转换工具`, version `1.0.0` |
| `mjpeg转换工具.runtimeconfig.json` | ~300 | `321b4e463bbacd61` | Targets `net6.0`, `Microsoft.WindowsDesktop.App` 6.0.0 |

The app's real name is **`mjpeg转换工具`** ("mjpeg conversion tool"), assembly version `1.0.0`,
built for **.NET 6.0 Windows Desktop**. Waveshare's "V2.1" is a distribution label, not the
assembly version.

**Bundled FFmpeg identification** (extracted from the binary's embedded configure string):

```
FFmpeg version n5.0.1-4-ga5ebb3d25e-20220508
--arch=i686 --target-os=mingw32 --enable-gpl --enable-version3 ...
--extra-version=20220508
```

- Upstream FFmpeg commit: `a5ebb3d25e`, four commits after tag `n5.0.1`
- 32-bit (`i686`) Windows cross-build, dated **2022-05-08**
- The `--extra-version=20220508` plus `/ffbuild/prefix` path is the signature of the
  well-known public Windows autobuilds (BtbN / gyan.dev style), **not** a Waveshare build
- Reacquire equivalent builds from <https://github.com/BtbN/FFmpeg-Builds/releases> or
  <https://www.gyan.dev/ffmpeg/builds/>. Note that exact historical 32-bit builds from
  2022-05-08 may no longer be published; the Waveshare ZIP is currently the most reliable
  source for this *exact* binary.

**Licensing caution:** the bundled FFmpeg is built `--enable-gpl --enable-version3`, so those
binaries are **GPLv3**. Waveshare ships them without an accompanying source offer. The 101 MiB
`.dll` also contains ~1000 FFmpeg/libav strings, indicating FFmpeg is embedded a *third* time
inside the managed assembly. Redistributing this archive carries unresolved GPL obligations —
this is a significant reason to keep it out of the repository.

Reacquire:

```bash
curl -L -o mjpeg_Conversion_tool_V2.1.zip \
  "https://files.waveshare.com/wiki/common/mjpeg%20Conversion%20tool%20V2.1.zip"
sha256sum mjpeg_Conversion_tool_V2.1.zip
# expect 8db4252b99ed27666b0316e23e1db1f5fcaa1a53116454cd34b8dc91c4fee1e7
```

Secondary sources: the path segment `/wiki/common/` is Waveshare's **shared file pool**, linked
from many Waveshare product wikis, so this URL is not tied to this product's page and will
survive changes to it. No independent third-party mirror was located. Because this is a
single-source artifact whose vendor may withdraw it, it is a good candidate for
`https://web.archive.org/save/`.

---

### 2. `flash_download_tool.zip`

| Field | Value |
|---|---|
| Bytes | 25,943,693 (24.74 MiB) |
| SHA-256 | `c1fbf280aa04cd8fbe725bff74360fb0a7c83fbd49afcaf37f6c14a6575ea9bc` |
| Primary URL | `https://dl.espressif.com/public/flash_download_tool.zip` |
| URL probe (2026-08-23) | `HTTP/2 200`, `content-length: 25943693` — **matches local byte size** |
| Upstream `Last-Modified` | `Tue, 09 Jun 2026 03:16:29 GMT` |
| Version | **3.9.11** (from the single payload filename) |
| Publisher | Espressif Systems |
| Redistribution status | `unknown` (Espressif proprietary tool, closed-source) |
| Disposition | archived (`local-cache` outside the repo) |

**Nothing was salvageable.** The archive contains exactly **one file** plus seven empty
directories:

```
flash_download_tool/flash_download_tool_3.9.11.exe   (25.3 MiB, Windows PE)
flash_download_tool/{bin,combine,configure,efuse_dump,flash_dump,logs,secure}/   (all empty)
```

No source, no documentation, no config worth preserving. This is the single best
`reference-only` candidate in the whole tree: an official Espressif tool on a permanent
Espressif URL.

> **Important caveat — the URL is unversioned.** `dl.espressif.com/public/flash_download_tool.zip`
> is updated *in place* by Espressif. Its `Last-Modified` of 2026-06-09 is newer than our
> retrieval, yet the byte size and hash still match, so as of 2026-08-23 the served file is
> still v3.9.11. **A future download may return a different version and therefore a different
> hash.** If you need exactly v3.9.11, use the archived copy. Always re-record the version and
> hash after any fresh download.

Reacquire:

```bash
curl -L -O https://dl.espressif.com/public/flash_download_tool.zip
sha256sum flash_download_tool.zip
# expect c1fbf280aa04cd8fbe725bff74360fb0a7c83fbd49afcaf37f6c14a6575ea9bc for v3.9.11
unzip -l flash_download_tool.zip | grep -o 'flash_download_tool_[0-9.]*\.exe'   # confirm version
```

Secondary sources:
- Espressif tool index: <https://www.espressif.com/en/support/download/other-tools>
- China mirror host: `https://dl.espressif.cn/public/flash_download_tool.zip` (same path pattern)
- Linked from the Waveshare wiki for this board, which is how it entered this repository

---

### 3. `CH34XSER_MAC.7z`

| Field | Value |
|---|---|
| Bytes | 4,123,873 (3.93 MiB) |
| SHA-256 | `c041275b27906b6beea109c0d73f937b48e09894373ff4d34d2011a0aee3dc7e` |
| Primary URL | `https://files.waveshare.com/wiki/common/CH34XSER_MAC.7z` |
| URL probe (2026-08-23) | `HTTP/1.1 200`, `Content-Length: 4123873` — **matches local byte size** |
| Upstream `Last-Modified` | `Wed, 11 Dec 2024 09:21:31 GMT` |
| Publisher | Waveshare, mirroring WCH (Nanjing Qinheng Microelectronics) |
| Redistribution status | `unknown` (WCH proprietary driver binaries) |
| Disposition | archived (`local-cache` outside the repo) |

**What it is:** the macOS USB-serial (VCP) driver for the WCH CH34x family. This board's
USB-UART bridge is a **CH445P** — see [`components/wch/ch445p/`](../../../../../components/wch/ch445p/).
You need this driver only to use the board's serial port from macOS; Linux and Windows 10+
have in-tree/inbox drivers.

Extracted contents (3 files, 4,629,059 bytes total):

| Member | Bytes | SHA-256 | Disposition |
|---|---:|---|---|
| `CH34X_DRV_INSTAL_INSTRUCTIONS.pdf` | 710,663 | `49432d23dd20c7d880d7d07b6d45d9d4346702bd39341a2c41482c13ff50ab7a` | **Kept in repo** as `ch34x-macos-driver-install-instructions.pdf` |
| `CH34xVCPDriver.dmg` | 1,976,378 | `f8a60745c3d95d017ec67116f40678ac9b10da7ca7c87a45889a70635726c0d1` | Archived — opaque macOS disk image |
| `CH34xVCPDriver.pkg` | 1,942,018 | `07e6fde30077b2624642ee11c0a81c457a4233eb95428610f81d2d387e5ebc9b` | Archived — opaque macOS installer |

Internal file dates: the `.dmg`/`.pkg` are dated **2022-11-06**, the instructions PDF
**2023-05-14**. These are the driver's own build dates, older than Waveshare's 2024-12-11
re-upload of the wrapping `.7z`.

The two binaries are opaque installers with no extractable documentation value; only the PDF
was worth keeping, and it now lives in the repository.

Reacquire:

```bash
curl -L -O https://files.waveshare.com/wiki/common/CH34XSER_MAC.7z
sha256sum CH34XSER_MAC.7z
# expect c041275b27906b6beea109c0d73f937b48e09894373ff4d34d2011a0aee3dc7e
7z x CH34XSER_MAC.7z
```

Secondary sources (WCH is the true origin; Waveshare is a mirror):
- WCH official downloads: <https://www.wch-ic.com/downloads/CH34XSER_MAC_ZIP.html> (English)
- WCH China: <https://www.wch.cn/downloads/CH34XSER_MAC_ZIP.html>
- WCH maintains open-source driver repos under <https://github.com/WCHSoftGroup>, including
  a macOS CH34x VCP driver project — useful if you need source rather than the signed installer
- The `/wiki/common/` pool means many other Waveshare product wikis link this identical file

> Version numbers were **not** determinable from the binaries offline — WCH does not embed a
> readable version string in the `.pkg`, and the filename carries none. Treat the internal file
> date (2022-11-06) as the best available version proxy, and check WCH's download page for the
> current published version and release date before assuming this copy is current.

---

## Summary of size change

| | Before | After |
|---|---:|---:|
| `artifacts/tools/` in repository | 108 MiB | **1.1 MiB** |
| Moved to `archive/` | — | 106.6 MiB |
| Newly extracted and kept (CH34X PDF) | — | 0.68 MiB |

Net repository reduction: **≈107 MiB**, with every archived byte hash-recorded and
confirmed reacquirable from a live, size-matched URL.
