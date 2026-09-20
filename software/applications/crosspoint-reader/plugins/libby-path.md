# Reading Libby loans on a CrossPoint device — the complete path

> Every step, every account, every failure mode, and which of the competing
> implementations actually works.
>
> Researched **2026-09-11**. Repository facts, HTTP probes and source reads are
> `executed-success`. **Nothing was installed, activated or run** — no device, no
> library card, no content account. Procedures are `reported-working` from the
> plugins' own documentation.

## The answer in one table

There are **three** Libby plugins in circulation. Only one of them works.

| Plugin | Version | Source | Status |
|---|---|---|---|
| **`ruqqq/crosspoint-plugins` → `libby`** | **1.0.2** | `raw.githubusercontent.com/ruqqq/crosspoint-plugins/main/libby/` | ✅ **Live** — all three files fetch (HTTP 200, `plugin.js` 64,847 B) |
| `itsthisjustin/sd-plugins` → `libby` | 0.2.0 | `raw.githubusercontent.com/itsthisjustin/sd-plugins/main/libby/` | ❌ **Gone — HTTP 404.** Directory removed; not in upstream's catalogue |
| Four fork catalogues listing `libby` 0.2.0 | 0.2.0 | point at the dead URL above | ❌ **Broken** — install will fail |

`pagdot`, `marczykm`, `dezren39` and `josmerod` all carry a `libby` entry in
their forked `catalog.json` whose `base` is the deleted upstream path. Their
descriptions differ (*"Fetch Libby books via the web interface"* vs *"Link Libby,
view your loans, and fulfill them"*) but the URL is identical and dead.

**Use `ruqqq`'s.** It is a separate, self-contained implementation — it does
**not** require the `protected-content` plugin, unlike the removed one.

## Prerequisites

| Requirement | Detail |
|---|---|
| **Firmware** | A build from **`feat-sd-plugins`** (66 commits ahead of `develop`, 0 behind, tip 2026-09-10). `develop` has **no plugin API at all** |
| **Plugin Store** | Unzip `plugin-store.zip` at the SD root, then add `https://raw.githubusercontent.com/ruqqq/crosspoint-plugins/main/catalog.json` as a store |
| **Network mode** | **File Transfer → Join Network** (*not* Hotspot) — the reader must actually be online |
| **Library card** | A normal Libby/OverDrive account |
| **Content account** | A **DTS ByteBooks** account — `dtsbytebooks.com/register`. **Separate from your library card** |

That last row is the one people miss. The ByteBooks account is what authorises
*this device* to open protected books; the library card is what lends them.

## Setup, once

1. Device web page → **File Manager** → the **Libby** card.
2. Enter the **content account** email and password → **Activate device**.
   Writes a credential to `/.crosspoint/content.key`.
3. Tap **Link Libby** — the card shows an **8-digit code**.
4. In the Libby app: **menu → Copy To Another Device**, enter that code.
   The card picks it up within a minute and lists your library.

## Borrowing, each time

1. Borrow the title in Libby as normal.
2. On the Libby card: **Refresh loans**, pick the title.
3. **Send to device.** It lands in `/Libby/` and opens.

## Fallback when Libby changes something

The plugin's README is refreshingly direct about the risk:

> *"Libby has no public API, so this can break when they change things."*

Manual route, which does not depend on Libby's internals: in Libby choose
**Read With… → Other Options → EPUB** to download an `.acsm`, upload it with the
File Manager, then use **Fetch selected book** at the bottom of the card.

## What it talks to

Hosts extracted from `plugin.js`:

```
libbyapp.com · sentry.libbyapp.com · dtsbytebooks.com
adeactivate.adobe.com · ns.adobe.com
```

Device APIs used: `api.relay` ×2, `api.crypto` ×1, `api.fetchToSd` ×3,
`api.writeFile` ×4, `api.registerAction` ×2.

So it is an **Adobe ADEPT flow brokered through ByteBooks**: ByteBooks supplies
the account, `adeactivate.adobe.com` does the device activation, Libby supplies
the loan, and the book streams to SD via `fetchToSd` — **book bytes never pass
through the browser page**.

## The eight-step procedure

> ⚠ **This is a map, not a tested recipe.** It is reconstructed from source,
> READMEs and catalog metadata. **Nobody in this project has a PaperMono, an
> Adobe ID, or a library loan** — no step below has been executed. Expect to
> debug.

### 1 — build and flash the plugin branch

```bash
git clone --recurse-submodules https://github.com/crosspoint-reader/crosspoint-reader
cd crosspoint-reader
git checkout feat-sd-plugins          # 66 commits ahead of develop, 0 behind
pio run -e papermono -t upload        # or x4pro / x4c / sticky / default
```

`feat-sd-plugins` @ `3657026e` (tip 2026-09-10) contains **all** of `develop`
plus 66 commits — a clean fast-forward, not a divergent branch.

**Verify before continuing:** request `GET /api/plugins` from the device web UI.
It should return a JSON array. A 404 means you are on the wrong firmware.

### 2 — install the plugin store

Download `plugin-store.zip` from the `itsthisjustin/sd-plugins` releases and
**unzip at the root of the SD card**. By hand instead, copy the folder to any of
these — **first match wins**:

```
/.crosspoint/plugins/plugin-store/
/plugins/plugin-store/
/.plugins/plugin-store/
```

each containing `manifest.json`, `plugin.js`, `device.json`.

The store appears under **Settings** in the web UI, and on the reader itself at
**Settings ▸ System ▸ Plugins**. Its default catalog is preconfigured to
`raw.githubusercontent.com/itsthisjustin/sd-plugins/refs/heads/main/catalog.json`;
your catalog list persists at `/.crosspoint/plugin-store.json`.

### 3 — prove the plumbing *before* touching DRM

**Skipping this is how people end up debugging three things at once.**

1. Install **`hello`** — proves the loader works end to end, no network.
2. Install **`webdav`** or **`wallabag`** — proves `relay`, `fetchToSd` and
   credential storage all work.

Only once a non-DRM plugin has downloaded a real book should you continue.

### 4 — install `protected-content`

Listed as *"Protected Content — Fulfill protected content from an online
provider"*, v1.0.4, by `Diirge`. It mounts on **`files`**, so it appears in the
**File Manager**, not Settings.

> ⚠ **Know what you are installing.** Unlike every other plugin in the catalog,
> its files are not served from GitHub — `base` is
> `https://protected-content-host-production.up.railway.app/`. **No git history,
> no licence, no README, no review.** Two files: `manifest.json` (170 B) and
> `plugin.js` (53,887 B).
>
> The sd-plugins repo never mentions "libby" — this plugin is generic ADEPT.

**Alternative worth considering:** `ruqqq/crosspoint-plugins`' `libby` bundles
the same ADEPT engine (71 % identical code, by its own admission) and needs
**neither** `protected-content` **nor** the Railway host. See the
[plugin source survey](plugin-source-survey.md).

### 5 — activate against Adobe

Standard ADEPT device activation, entirely in the browser:

| Phase | What happens | Device API |
|---|---|---|
| Keypair | RSA keypair generated | `crypto keygen` |
| Sign | Activation request signed | `crypto sign` |
| Exchange | Talks to `adeactivate.adobe.com/adept` | `relay` (CORS) |
| Store | PKCS#12 credential written | `plugin-fs` → `/.crosspoint/content.key` |
| State | Activation record written | `plugin-fs` → `/.crosspoint/content-activation.json` |

It presents as Adobe Digital Editions **`10.0.4`** (the `HOBBES` constant).

**This consumes one of your account's activation slots** — the limit is 10.
Deactivate an old device via ADE or the vendor's site if you run out. Note the
account is now a **ByteBooks ID**, not an Adobe ID; see the
[ByteBooks review](dtsbytebooks-review.md).

### 6 — get an ACSM out of Libby

**The step most people get wrong.** When borrowing, choose the **EPUB download
for Adobe Digital Editions** — *not* "Read in browser", "Read with Kindle" or
"Listen". You should get a small **`.acsm`** file: a few KB of XML, a fulfilment
*token*, not the book.

**Not every title offers this.** Publishers choose formats; some are Kindle-only
or browser-only. If there is no Adobe/EPUB option, **this path cannot work for
that title** — and no amount of debugging will change that.

### 7 — fulfil

Put the `.acsm` where the plugin can reach it (the File Manager is its mount, so
the current folder is natural) and run the fulfil action.

1. ADEPT fulfilment exchange with the content server, via `relay`
2. The real EPUB streams **straight to SD** via `fetchToSd` — the browser never
   holds book bytes, which is also how it avoids the 32 KB relay cap
3. A **`<book>.epub.rights`** sidecar is written beside it

### 8 — read it

The EPUB on disk stays **byte-identical to what the server sent**. Decryption
happens per zip entry at read time, against `/.crosspoint/content.key`. If the
book refuses to open, the firmware's error strings are specific and worth
knowing: **`"loan date unverified"`** means no trustworthy clock, and
**`"access expired"`** means the loan is over. See
[the ContentProtection library](../../../frameworks/freeink-sdk/contentprotection-library.md).

## Limits, stated by the plugin itself

- **Ebooks only.** Audiobooks and magazines are unsupported. Titles Libby only
  offers in its own web reader *"can't be sent to a device by any app"*.
- **The book stays protected on the SD card.** It is unlocked in memory only
  while being read, and **stops opening when the loan ends**. Returning or
  deleting it is your job.
- A few titles are publisher-DRM-free; those download directly with no expiry
  beyond the loan.
- **Both the Libby link and the content credential live on the SD card** — treat
  the card as sensitive.

**Unlink:** tap **Unlink**, or delete `/.crosspoint/libby.json`. To drop the
content account too, delete `/.crosspoint/content.key`.

## How this differs from `protected-content`

Both end in an ADEPT-fulfilled book, by different routes:

| | `protected-content` (Diirge) | `libby` (ruqqq) |
|---|---|---|
| Account | Adobe ID, direct | **DTS ByteBooks** |
| Input | an `.acsm` you supply | **your live Libby loan list** |
| Hosting | **off-GitHub**, Railway, unlicensed | GitHub, in-repo |
| Scope | any ADEPT provider | Libby specifically |
| Dependency | standalone | standalone |

The removed `libby` 0.2.0 *required* `protected-content`; ruqqq's 1.0.2 does not.

## Legal framing

This is a **licensed ADEPT client reading a legitimately borrowed loan** — the
role Adobe Digital Editions or a Kobo plays. The DRM is honoured, not removed:
the file stays encrypted on disk and stops opening at loan end. That is
categorically different from DRM *stripping* (DeDRM and similar), which is
restricted in many jurisdictions.

The plugin states it is *"not affiliated with or endorsed by Libby, OverDrive,
Adobe, or ByteBooks."* Using an unofficial client against an API with no public
contract may breach those services' terms — a separate question from copyright,
and one this record does not answer.

## Trust and provenance — read before installing

- **`ruqqq/crosspoint-plugins` has no `LICENSE` file.** ★0, created 2026-08-17,
  last pushed **2026-08-18** — so the working Libby plugin sits in a
  three-week-untouched, unlicensed repository.
- **`itsthisjustin/sd-plugins` also has no licence**, and its
  `protected-content` is hosted **off-GitHub on Railway** with no source history.
- **Plugins are not sandboxed.** Upstream says so plainly: they load into the
  page, *"not an isolated iframe"*, with the full authority of the web UI — which
  has **no authentication**. A plugin can read other plugins' credentials on SD.

You are entering library-card-adjacent and Adobe-account credentials into
unlicensed third-party JavaScript. That may well be fine; it should be a decision,
not an accident.

## Checklist

1. Build and flash from **`feat-sd-plugins`** (confirm `[env:papermono]` if relevant).
2. Verify the API is live: `GET /api/plugins` on the device web UI.
3. Install `plugin-store` from the release zip at the SD root.
4. Prove the loader with `hello`.
5. Add ruqqq's catalogue URL as a store; install `libby` **1.0.2**.
6. Register at `dtsbytebooks.com`, activate the device, link Libby.
7. **Do not** install `libby` from `pagdot`/`marczykm`/`dezren39`/`josmerod` — dead URL.

## Open questions

- **Nothing was installed or run.** No device, no ByteBooks account, no loan.
- `plugin.js` (64,847 B) was fetched; **hosts and API calls were extracted, but
  the fulfilment logic was not audited line by line.**
- **Why `libby` was removed from `itsthisjustin/sd-plugins` is unknown** — no
  commit history is returned for the path. Whether it was withdrawn, rewritten
  out, or never on `main` is unestablished.
- What DTS ByteBooks actually is — an Adobe-licensed fulfilment reseller is the
  obvious reading, **not verified**.
- Whether `ContentProtection.cpp` handles loan expiry gracefully was not examined.

## Sources

All 2026-09-11, `executed-success`: catalogue JSON from `itsthisjustin`,
`ruqqq`, and eight forks; HTTP probes of `itsthisjustin/.../libby/*` (404) and
`ruqqq/.../libby/*` (200); `manifest.json`, `README.md` and `plugin.js` of
ruqqq's libby 1.0.2; `git grep` of `feat-sd-plugins` for the API surface.
