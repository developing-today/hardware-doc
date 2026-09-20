# The CrossPoint SD-card plugin system — and the Libby/ADEPT path

> Everything needed to approach this confidently: the firmware branch, the API
> surface, the hard limits, the store protocol, every shipped plugin, and how
> protected library loans actually reach the device.
>
> Researched **2026-09-11**. Repository, branch and source facts are
> `executed-success` (repos cloned, `git grep` against the actual branch, live
> HTTP fetches). Behaviour is `inferred` — **nothing was built, flashed or run**,
> and no device or library account was used.

## Two corrections to this knowledge base

This research overturns two things recorded earlier. Both are stated here first
because they change what a reader should believe.

**1. The plugin system is not a stale roadmap item.** An earlier pass recorded
that "`develop` contains zero plugin files" and the work was a Phase 2 item on
unmerged branches. The first half is still true. The second is misleading:

| Branch | vs `develop` | Tip | State |
|---|---|---|---|
| **`feat-sd-plugins`** | **66 ahead, 0 behind** | **2026-09-10** | Strictly ahead — **a clean merge**, actively developed |
| `feat-sd-web-plugins` | 64 ahead, 58 behind | — | Genuinely divergent |

`feat-sd-plugins` contains everything in `develop` plus 66 commits. It is not
drifting; it was touched the day before this snapshot. **And it carries
`[env:papermono]`.**

**2. CrossPoint *can* read Adobe-DRM'd EPUBs.** The Calibre record in this
knowledge base states that "no CrossPoint-family firmware has a DRM client" and
that protected loans "do not open". **That is wrong.**
`lib/Epub/ContentProtection.cpp` exists on `feat-sd-plugins` and reads a
`<book>.epub.rights` sidecar — deliberately keeping the EPUB *"byte-identical"*
on disk — against a device credential at `/.crosspoint/content.key`.

## Architecture

```
 Browser (reader's web UI, same-origin)          Device firmware            SD card
 ┌──────────────────────────────┐        ┌──────────────────────┐     ┌──────────────┐
 │ plugin.js                    │──────▶ │ /api/relay   32 KB   │────▶│              │
 │  CrossPoint.registerPlugin() │        │ /api/crypto  wolfSSL │     │ /.crosspoint │
 │  mounted on Files or Settings│        │ /api/fetch   →SD     │────▶│  /plugins/   │
 └──────────────────────────────┘        │ /api/plugin-fs       │     │  content.key │
            ▲                            │ /api/plugins         │     │  *.epub      │
            │ injected by PluginHost.js  └──────────────────────┘     │  *.epub.rights│
            │                                       │                 └──────────────┘
      device.json → an on-device UI under Settings ▸ System ▸ Plugins
```

**Plugins are browser JavaScript.** No code runs on the MCU. The firmware
provides four capabilities a browser cannot do itself, and that is the whole
boundary.

## The API surface

From `src/network/html/shared/PluginHost.js.inc` on `feat-sd-plugins`. A plugin
calls `CrossPoint.registerPlugin(async (container, api) => { … })` and receives:

| Call | Backing endpoint | Purpose |
|---|---|---|
| `api.relay(method, url, headers, body)` | `POST /api/relay` | Outbound HTTP(S) — browsers can't, due to CORS |
| `api.crypto(op, fields)` | `POST /api/crypto` | wolfSSL primitives |
| `api.writeFile(path, dataB64)` | `POST /api/plugin-fs` | Write a small file to SD |
| `api.fetchToSd(url, dest, headers)` | `POST /api/fetch` | Stream a URL straight to SD — **bytes never touch the page** |
| `api.registerAction(action, fn)` | — | Expose an action to the host page |

Discovery is `GET /api/plugins` → `[{name, title, mount}]`; files are served from
`GET /plugin?name=<p>&file=<f>`, reading `/.crosspoint/plugins/<p>/<f>`.

### `/api/crypto` operations

Enumerated from the source: `keygen`, `sign`, `pubencrypt`, `aesenc`, `aesdec`,
`pkcs12`, `cert`, `hash`, `sha1`, `random`.

**That set is not incidental — it is precisely an Adobe ADEPT toolkit**: RSA
keygen and signing for device activation, PKCS#12 for the credential container,
AES for content-key unwrap, SHA-1 because ADEPT still uses it.

### Hard limits — design around these

| Limit | Value | Source |
|---|---|---|
| `/api/relay` response cap | **32 KB** (`RELAY_BODY_LIMIT`) | HTTP **413**, *"response too large, use /api/fetch"* |
| `/api/fetch` segment cap | **4 MB** (`FETCH_MAX_SEGMENT_SIZE`) | supports `offset`/`maxBytes` for chunking |
| Stalled-fetch retries | 3 (`FETCH_MAX_STALLED_ATTEMPTS`) | |
| Manifest cap | **8 KB** | per the repo's plugin-authoring skill |
| Redirects on `/api/fetch` | **not followed** | resolve them yourself via `relay` |
| Archive extraction | **none on-device** | ship unpacked files |

The 32 KB relay cap is the one that shapes plugin design: **metadata and API
calls go through `relay`, book bytes go through `fetchToSd`.**

## Installing

Three roots are scanned, first match wins:

```
/.crosspoint/plugins/<name>/      ← where the store installs
/plugins/<name>/                  ← easier to reach from a computer
/.plugins/<name>/
      manifest.json   plugin.js   device.json   …assets
```

`manifest.json` `mount` is `files` or `settings` — which page the plugin extends.
A `device.json` additionally gives it an **on-device** UI under
Settings ▸ System ▸ Plugins, so a plugin can be driven without a browser.

**Fastest path:** download `plugin-store.zip` from the sd-plugins releases, unzip
at the SD root, then install everything else from the store itself.

## `itsthisjustin/sd-plugins`

★36 · 10 forks · JavaScript · **no licence file** · HEAD `dfc0a888` · pushed **2026-09-10**

| Plugin | v | What it does |
|---|---|---|
| `plugin-store` | 1.1.2 | Installs plugins from one or more hosted catalogs |
| `bookfusion` | 1.2.0 | BookFusion library; device-code + QR sign-in; writes `<book>.meta.json` that rides KOSync progress uploads |
| `webdav` | 1.0.0 | Nextcloud/ownCloud/Seafile/Koofr; creds in `/.crosspoint/webdav.json` |
| `wallabag` | 1.2.0 | Read-it-later articles as EPUB (OAuth2 password grant) |
| `dictionaries` | 1.0.0 | ~20 offline StarDict dictionaries from Wiktionary + Webster's 1913 |
| `organize-by-author` | 1.0.0 | Files EPUBs into per-author folders; moves progress, cache and `.epub.rights` sidecars with the book |
| `hello` | 1.0.0 | Minimal loader example |
| **`protected-content`** | **1.0.4** | **See below** |

Catalog format is documented in `CATALOG.md`: a JSON doc with `plugins[]`, each
carrying `name`, `base` URL and a `files[]` list. **Anyone can host a catalog**
— a static file or raw Git URLs — and users add multiple stores.

## The Libby path: `protected-content`

This is the plugin the question was really about. It is **not named Libby**, and
it is **not in the repository**.

```jsonc
{
  "name": "protected-content",
  "title": "Protected Content",
  "description": "Fulfill protected content from an online provider.",
  "author": "Diirge",
  "version": "1.0.4",
  "base": "https://protected-content-host-production.up.railway.app/",
  "files": ["manifest.json", "plugin.js"]
}
```

**It is hosted off-GitHub on Railway** — no git history, no licence, no code
review, no tags. Every other plugin's `base` is `raw.githubusercontent.com`. Only
this one is elsewhere, and only this one ships no `README.md`. A grep of the
sd-plugins repo for "libby" returns **zero hits**.

Draw your own conclusion about why; the observable fact is that the DRM
fulfilment code is deliberately kept outside the repository.

### What it actually is

`plugin.js` is **53,887 bytes** and its own header comment is explicit:

> *Browser-side account activation and fulfillment using generic device APIs:*
> `/api/relay` *outbound HTTP(S) (browsers can't, due to CORS)*
> `/api/crypto` *wolfSSL primitives (keygen, sign, AES, PKCS#12, hash, random)*
> `/api/fetch` *download a URL straight to SD (book bytes never touch the page)*
> `/api/plugin-fs` *write a small file to SD (the credential + rights sidecar)*

Constants confirm it is a full **Adobe ADEPT** client:

```js
const ADEPT_NS = 'http://ns.adobe.com/adept';
const ACS      = 'https://adeactivate.adobe.com/adept';   // Adobe's activation server
const ADEPT_CT = 'application/vnd.adobe.adept+xml';
const CREDENTIAL_PATH = '/.crosspoint/content.key';
const ACTIVATION_PATH = '/.crosspoint/content-activation.json';
const HOBBES = '10.0.4';                                   // the ADE version it presents as
```

`mount: "files"` — it appears in the File Manager.

### The end-to-end chain

1. **Activate** — the plugin generates an RSA keypair via `/api/crypto keygen`,
   signs an activation request, talks to `adeactivate.adobe.com` through
   `/api/relay`, and stores the resulting credential at
   `/.crosspoint/content.key` (PKCS#12) plus
   `/.crosspoint/content-activation.json`.
2. **Fulfil** — given an `.acsm` (what Libby/OverDrive hand you for a loan), it
   performs the ADEPT fulfilment exchange and uses `/api/fetch` to stream the
   EPUB **straight to SD**, then writes a `<book>.epub.rights` sidecar.
3. **Read** — `lib/Epub/ContentProtection.cpp` in the firmware reads that sidecar
   against the device credential. The source notes the design keeps the EPUB
   *"byte-identical"* on disk — so the file is **not** decrypted in place; it is
   decrypted at read time.

**So the device is an ADEPT-activated reader.** It is not removing DRM — it is
acting as a licensed endpoint, the same role Adobe Digital Editions or a Kobo
plays.

### What you need

| Requirement | Detail |
|---|---|
| Firmware | A build from **`feat-sd-plugins`** (or `feat-sd-web-plugins`). **Not `develop`** — it has no plugin API |
| Adobe ID | Activation consumes one of the account's device slots |
| The plugin | Installed via the store, or by hand from the Railway URL |
| Source | Libby/OverDrive — export the loan as an **ACSM** (the "Adobe" / EPUB download option, not "read in browser") |

**Constraints worth knowing up front:** Adobe IDs have a limited number of
activations, and deactivating requires ADE or Adobe's site. The 32 KB relay cap
means the fulfilment negotiation is chunked while the book itself goes via
`fetch`. And **nothing here removes DRM** — the loan still expires, and the file
is unreadable on an unactivated device.

### Legal framing

This documents what exists and how it works. **Using a licensed ADEPT client to
read a legitimately borrowed loan is the intended use of that content** — it is
what ADE does. That is different in kind from DRM *removal* (DeDRM and friends,
covered in the [Calibre record](../../../tooling/calibre/README.md)), which is
restricted in many jurisdictions.

None of this is legal advice, and the plugin's unlicensed, off-repository hosting
is a fact a reader should weigh for themselves.

## Security model — stated plainly by upstream

The sd-plugins README does not oversell it:

> *"Plugins are JavaScript loaded into the File Manager or Settings page, **not an
> isolated iframe**. They can call the same-origin web API and any generic device
> capability."*

So a plugin has the **full authority of the web UI**, including other plugins'
credentials on SD. Combined with the web server having **no authentication**, the
real boundary is *network-vs-device*, not *plugin-vs-firmware*. Install plugins
you trust, and treat the reader's Wi-Fi exposure accordingly.

This is a different and weaker boundary than the
[native ELF plugin system](README.md),
which enforces an 81-symbol allow-list at link time — but that one cannot reach
the network at all.

## Confidence checklist

To approach this with confidence, in order:

1. **Build from `feat-sd-plugins`**, confirm `[env:papermono]`, flash.
2. **Verify the API is live** — `GET /api/plugins` on the device web UI.
3. **Install `plugin-store`** from the release zip at the SD root.
4. **Prove the loader** with `hello` before anything else.
5. **Try a non-DRM plugin next** — `webdav` or `wallabag` — to validate relay,
   fetch and credentials end to end.
6. **Only then `protected-content`**, knowing it is unlicensed, off-repo, and
   consumes an Adobe activation slot.

## Open questions

- **Nothing was built, flashed or run.** No device, no Adobe ID, no loan.
- `protected-content`'s `plugin.js` was fetched and its header and constants read;
  **the fulfilment logic was not audited line by line.**
- Whether `ContentProtection.cpp` covers all ADEPT variants (and what it does with
  expired loans) was **not examined**.
- The relationship between `feat-sd-plugins` and `feat-sd-web-plugins`, and which
  upstream intends to merge, is unknown.
- `itsthisjustin/sd-plugins` has **no licence** — as does the Railway-hosted
  plugin. Redistribution status of both is therefore all-rights-reserved.
- Ten forks exist; none was examined.

## Sources

All 2026-09-11, `executed-success`:
`itsthisjustin/sd-plugins` @ `dfc0a888` (README, CATALOG.md, catalog.json) ·
`crosspoint-reader` branches `feat-sd-plugins` @ `3657026e` and
`feat-sd-web-plugins` @ `bdbbbef7` (`git grep`/`git show` against
`CrossPointWebServer.cpp`, `PluginHost.js.inc`, `ContentProtection.cpp`,
`platformio.ini`) ·
`https://protected-content-host-production.up.railway.app/{manifest.json,plugin.js}`
(HTTP 200, 170 B and 53,887 B).
