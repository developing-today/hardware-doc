# SquareLine — Documentation and Download Sourcing Guide

SquareLine Kft. publishes **SquareLine Studio**, a proprietary drag-and-drop UI editor that generates [LVGL](https://lvgl.io) C code. It is not a hardware manufacturer, but it is a vendor whose tooling is used to build firmware UIs for the ESP32/display boards documented elsewhere in this tree, so its sourcing knowledge lives here.

**Researched:** 2026-08-30 · **Version observed:** 1.6.1 · **Evidence class:** live probes from this host, plus third-party distribution packaging.

> **Headline finding.** The Linux build is **a plain ZIP, not an AppImage**, and the download host **returns HTTP 206 for every path that is syntactically valid** — including files that do not exist. `Content-Type` is the only reliable existence signal. See [§3](#3-the-soft-404-trap-content-type-is-the-only-existence-signal).

---

## 1. Hosts

| Host | Resolves | Role | Evidence |
|---|---|---|---|
| `squareline.io` | yes | Marketing site and downloads **page** | [S1] |
| `static.squareline.io` | yes → `34.120.198.143` (Google Cloud) | **Actual file host** for all installers | [S2] |
| `download.squareline.io` | **NXDOMAIN** | Does not exist — a plausible-looking guess that fails | [S2] |

`download.squareline.io` is recorded because it is the obvious first guess and it costs a DNS lookup to disprove. It has never resolved from this host.

## 2. URL pattern

```sh
# Linux (ZIP; extract-and-run, no installer)
https://static.squareline.io/downloads/SquareLine_Studio_Linux_v<MAJOR>_<MINOR>_<PATCH>.zip

# Windows (ZIP)
https://static.squareline.io/downloads/SquareLine_Studio_Windows_v<MAJOR>_<MINOR>_<PATCH>.zip
```

**Version separators are underscores, not dots.** `v1_6_1`, never `v1.6.1`. The AUR PKGBUILD performs exactly this substitution (`${pkgver//./_}`) [S4].

No login, account, licence key or referer is required to download. Licence enforcement happens at first launch inside the application, not at the CDN.

## 3. The soft-404 trap: `Content-Type` is the only existence signal

A range request against this host returns **HTTP 206 whether or not the file exists**. Probing status codes alone will report every guessed URL as a success.

Probed 2026-08-30 with `curl -r 0-0` and a browser User-Agent:

| URL suffix | Status | `Content-Type` | Exists? |
|---|---|---|---|
| `SquareLine_Studio_Linux_v1_6_1.zip` | 206 | `application/x-zip-compressed` | **yes** |
| `SquareLine_Studio_Linux_v1_6_0.zip` | 206 | `application/x-zip-compressed` | **yes** |
| `SquareLine_Studio_Windows_v1_6_1.zip` | 206 | `application/x-zip-compressed` | **yes** |
| `SquareLine_Studio_Linux_v9_9_9.zip` — *negative control* | 206 | `text/html` | **no** |
| `SquareLine_Studio_Setup_v1_6_1.exe` — *negative control* | 206 | `text/html` | **no** |
| `SquareLine_Studio_macOS_v1_6_1.dmg` — *negative control* | 206 | `text/html` | **no** |

Validation rule:

```sh
# Treat only application/x-zip-compressed as a hit; text/html is a soft 404.
curl -s -o /dev/null -w '%{http_code} %{content_type}\n' -r 0-0 \
  -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36' \
  "https://static.squareline.io/downloads/SquareLine_Studio_Linux_v1_6_1.zip"
```

The macOS and `Setup*.exe` rows say only that **those two names** are wrong; they do not prove macOS builds are unavailable. The naming for macOS was not determined.

## 4. The downloads page is a JavaScript shell — do not scrape it

`https://squareline.io/downloads` is a Next.js application. A plain fetch returns an **11,103-byte HTML shell containing no download links whatsoever**; `grep` for `.AppImage`, `.zip` or `href=".*download"` returns nothing [S1].

Consequences:

- Version enumeration must come from rendered search-engine snapshots, the third-party packaging below, or probing [§2](#2-url-pattern) with the [§3](#3-the-soft-404-trap-content-type-is-the-only-existence-signal) validation rule.
- Versions visible in the rendered archive as of 2026-08-30: **1.6.1** (current), 1.6.0, 1.5.4, 1.5.3, 1.5.2, 1.5.1, 1.5.0, 1.4.2, 1.4.1, 1.4.0, 1.3.4, 1.3.3, 1.3.2, 1.3.1, 1.3.0 [S1].
- Attempting `/_next/data/…` JSON extraction was **not** performed; it remains the most likely route to a machine-readable version list.

## 5. Third-party packaging as a sourcing oracle

Two independent distributions package SquareLine Studio from the same host, and both are more informative than the vendor's own page:

| Source | Value | Ref |
|---|---|---|
| **AUR** `squareline-studio` | Confirms the `static.squareline.io` URL and the dot→underscore version rule; a 2024 comment records that **1.4.2 shipped with an extra directory level inside the ZIP**, which broke packaging | [S4] |
| **Gentoo / liguros ebuild** | Confirms the same `SRC_URI`, records `LICENSE="all-rights-reserved"`, and installs to `/opt` with `SquareLine_Studio.x86_64` as the entry point | [S5] |

The 1.4.2 nesting note matters: **ZIP internal layout is not stable across releases.** Verify the top level after any version bump rather than assuming a flat tree.

## 6. What is inside the Linux ZIP (v1.6.1)

Verified by reading the archive directly, 2026-08-30. See the [archived-artifact record](artifacts/ARCHIVED-SQUARELINE-STUDIO-LINUX.md) for hashes.

- **1,711 members, flat top level** (no wrapper directory in this release, unlike 1.4.2).
- `SquareLine_Studio.x86_64` — **ELF, only 4,472 bytes**: the Unity player stub. The real engine is `UnityPlayer.so`, with assets in `SquareLine_Studio_Data/`.
- `setup.sh` — the documented install step. It **only** `chmod +x`es files and writes a `.desktop` entry; it compiles and installs nothing.
- `squareline_studio.desktop.template` — placeholders `__folder__`; notably `Exec=env GDK_BACKEND=x11 …`, i.e. **upstream forces the X11 GDK backend**, so the app is expected to run under XWayland rather than native Wayland.
- Bundled `libdecor-0.so.0` / `libdecor-cairo.so` despite the X11 default.
- **`lvgl/` — four complete bundled LVGL trees: `lvgl_v8_3_11`, `lvgl_v9_1_0`, `lvgl_v9_2_2`, `lvgl_v9_3`**, each with its own `server/micropython` binary used for live preview, plus `lv_font_conv-linux`.
- **No licence, EULA, or copyright file is included in the archive at all.** Licence terms exist only on the website.

### The executables `setup.sh` chmods

Any repackaging must reproduce this exact set, not just the `.x86_64`:

```text
SquareLine_Studio.x86_64
lvgl/lv_font_conv-linux
lvgl/lvgl_v8_3_11/server/micropython
lvgl/lvgl_v9_1_0/server/micropython
lvgl/lvgl_v9_2_2/server/micropython
lvgl/lvgl_v9_3/server/micropython
```

Missing the `micropython` servers or `lv_font_conv-linux` yields an application that starts normally and then fails at font conversion and live preview — a silent, late failure. This exact defect was found and fixed in this repository's Nix packaging; see [`guides/nixos/README.md`](../../guides/nixos/README.md#5-squareline-studio).

## 7. Licensing

| Field | Value |
|---|---|
| **Licence** | Proprietary, all rights reserved [S5] |
| **Tiers** | Free tier with limits; 30-day full-featured trial requiring no account [S1] |
| **Account required to download** | No |
| **Account/internet required to activate** | Yes, at first launch [S6] |
| **Redistribution status** | **restricted** — no evidence of any redistribution grant, and no licence file ships in the archive |
| **Disposition** | **local-cache** — archived outside the repository; never staged |

## 8. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | SquareLine Studio downloads | SquareLine Kft. | primary | official page | `https://squareline.io/downloads` | 2026-08-30 | JS-shell behaviour; version archive list; free-trial terms |
| S2 | DNS + range probes from this host | — | primary | live probe | `static.squareline.io`, `download.squareline.io` | 2026-08-30 | Host resolution; the 206 soft-404 behaviour |
| S3 | `SquareLine_Studio_Linux_v1_6_1.zip` contents | SquareLine Kft. | primary | archive | see [§2](#2-url-pattern) | 2026-08-30 | Layout, bundled LVGL versions, `setup.sh` behaviour |
| S4 | AUR `squareline-studio` PKGBUILD + comments | AUR contributors | community | repository | `https://aur.archlinux.org/packages/squareline-studio` | 2026-08-30 | URL pattern; version separator rule; 1.4.2 ZIP nesting |
| S5 | `squareline-studio-1.6.0.ebuild` | liguros / GURU overlay | community | repository | `https://data.gpo.zugaina.org/guru/dev-embedded/squareline-studio/squareline-studio-1.6.0.ebuild` | 2026-08-30 | Same `SRC_URI`; `LICENSE="all-rights-reserved"`; `/opt` entry point |
| S6 | Waveshare SquareLine Studio wiki | Waveshare | community | wiki | `https://www.waveshare.com/wiki/Waveshare_SquareLine_Studio` | 2026-08-30 | Activation requires internet; 30-day trial without purchase |

## 9. Evidence boundary

- **Directly verified from this host (2026-08-30):** DNS results, all six URL probes and their content types, the JS-shell response size, and every statement in [§6](#6-what-is-inside-the-linux-zip-v161) — those were read out of the downloaded archive.
- **Third-party but consistent:** the version-separator rule and the 1.4.2 nesting anomaly [S4], the licence expression [S5].
- **From rendered search snapshots, not fetched directly:** the version archive list in [§4](#4-the-downloads-page-is-a-javascript-shell--do-not-scrape-it).
- **Not established:** macOS download naming; whether `/_next/data/…` exposes a version index; whether the free tier's export limits differ from the trial's; SquareLine's licence position on running the tool from an immutable store path.
- **Not tested:** the application has never been launched on this machine. No claim here describes runtime behaviour beyond what the shipped files and vendor scripts state.
