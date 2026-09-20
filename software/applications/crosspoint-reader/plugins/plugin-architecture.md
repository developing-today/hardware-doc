# CrossPoint plugin architecture — how it actually works

> What the plugin system is, whether it really works, what it can and cannot do,
> and — the practical question — **what you can add without touching firmware and
> what forces a fork.**
>
> Read from the plugin host source, the store, and five shipped plugins on
> **2026-09-11**. Source reads are `executed-success`. **Nothing was installed,
> flashed or run**; behaviour is `inferred` from source and from plugin authors'
> reports, which are attributed where they matter.
>
> This is a design review, **not a security audit**.

## There are two plugin systems, and confusing them wastes days

| | **Browser plugin** (`plugin.js`) | **On-device UI** (`device.json`) |
|---|---|---|
| Runs where | In a page in **your browser**, talking to the device | On the **device**, rendered on e-paper |
| Language | JavaScript, arbitrary | **JSON only** — no code |
| Interpreted by | The page's plugin host | The **firmware** |
| Needs a browser? | **Yes, always** | **No** |
| Can do crypto? | Yes, via `/api/crypto` | No |
| Typical use | Account linking, DRM fulfilment, anything complex | Browse a feed, download a file |

A plugin folder can ship **both**, and the good ones do: `readeck` uses
`plugin.js` for setup and `device.json` for day-to-day browsing on the device.
They are complementary, not alternatives.

**Both live on the SD card. Adding either needs no firmware change** — that is
the entire point of the design.

## Part 1 — the browser plugin host

### Discovery and loading

```js
// 1. host asks the device what's installed
list = await (await fetch('/api/plugins')).json();     // [{name, mount, title}, …]

// 2. for each plugin matching this page's mount, inject its script
s.src = '/plugin?name=' + encodeURIComponent(p.name) + '&file=plugin.js';

// 3. the script calls registerPlugin(fn); the host then invokes it
CrossPoint._pending(container, { name, relay, crypto, writeFile,
                                 fetchToSd, registerAction, pluginFile });
```

A plugin is a single file that calls `CrossPoint.registerPlugin(fn)`. The host
hands it a DOM container and an API object **pre-bound to that plugin's name** —
so the device knows which plugin made each call.

### `mount` decides which page loads it

| `mount` | Loaded by |
|---|---|
| `settings` (default) | the Settings page |
| `files` | the File Manager |
| *(null filter)* | the **headless `/plugins-run` page**, which loads **everything** |

### The API surface — six functions, and that's all

| Function | Endpoint | What it's for |
|---|---|---|
| `relay(method, url, headers, body)` | `/api/relay` | Outbound HTTP the browser can't make (CORS) |
| `crypto(op, fields)` | `/api/crypto` | wolfSSL primitives |
| `writeFile(path, dataB64)` | `/api/plugin-fs` | Write a small file to SD |
| `fetchToSd(url, dest, headers)` | `/api/fetch` | Stream a URL **straight to SD** |
| `registerAction(action, fn)` | job queue | Expose a callable action to other plugins |
| `pluginFile(f)` | — | URL for another file in your own plugin folder |

Two details that matter when writing one:

**`relay` preserves duplicate headers.** It resolves to
`{status, body, headers}` where headers is an **ordered list of `[name, value]`
pairs** — so every `Set-Cookie` survives. Most naive relay designs lose these.

**`writeFile` decodes base64 in the browser** and posts binary
(`application/octet-stream`), specifically so embedded NULs survive. You pass
base64; the wire carries bytes.

### The job queue is the most interesting part

This is how one plugin calls another, and it explains an otherwise baffling
design choice.

```js
registerAction(pluginName, action, fn) {
  (this._actions[pluginName] = this._actions[pluginName] || {})[action] = fn;
  if (!this._actionTimer) this._actionTimer = setInterval(() => this._pollJobs(), 2500);
}
```

Registering an action starts a **2.5-second poll**. Jobs are enqueued externally
via `POST /api/plugin-jobs`, then:

1. `GET /api/plugin-jobs/claim?plugin=X` — any page hosting that plugin claims it
2. the registered `fn(job.args)` runs
3. `POST /api/plugin-jobs/complete {id, ok, result}` — the caller polls for this

**Completion is retried before new work is claimed** (`_pendingCompletion` is
posted first on the next tick if it failed), so a dropped result isn't silently
lost.

**Why it exists:** it lets `libby` hand a fulfilment token to `protected-content`
without either plugin importing the other. The DRM engine stays in one plugin;
the Libby API layer stays thin. `libby`'s own header says exactly that.

**Why it constrains you:** a job only runs **while some page hosting that plugin
is open in a browser.** The `/plugins-run` page exists to be that page — but it
is still a browser page on a computer. **There is no background execution on the
device.**

### `fetchToSd` segments at 2 MB — client-side

```js
const maxBytes = 2 * 1024 * 1024;
let offset = 0;
for (;;) {
  const result = await this._post('/api/fetch', { plugin, url, dest, headers, offset, maxBytes });
  if (result.complete !== false) return result;
  if (!Number.isFinite(result.bytes) || result.bytes <= offset) throw new Error('/api/fetch made no progress');
  offset = result.bytes;
}
```

The comment gives the reason, and it is not what you'd guess: *"Mobile browsers
may terminate a request after a few minutes even when response heartbeats are
flowing, while the device itself is still downloading successfully."*

**This resolves a discrepancy in prior research.** A firmware constant
`FETCH_MAX_SEGMENT_SIZE = 4 MB` was recorded alongside observed 2 MB segments and
marked unresolved. They are different things: **2 MB is what the browser
requests; 4 MB is the firmware's ceiling on that request.** Not a contradiction.

**The consequence is real though:** any file over 2 MB **always** needs a second,
offset-based call. If the firmware issues a `Range` request for that and the
server doesn't support ranges, the download fails deterministically — and
retrying cannot help, because every attempt crosses the same point. Plugin
authors have described this as a "numbers game" mitigation with retry counts;
**if the mechanism is as described, retries are futile for that case.** The
`/api/fetch` handler was not captured, so whether it sends `Range` on `offset > 0`
is **unverified**.

## Part 2 — `device.json`, the declarative on-device UI

No JavaScript. The firmware reads this and renders a browsable list on the
e-paper. Real example, shipped:

```json
{
  "token":  { "file": "/.crosspoint/readeck.json", "path": "token" },
  "config": { "file": "/.crosspoint/readeck.json" },
  "browse": {
    "format": "json",
    "url": "{cfg.url}/api/bookmarks?is_archived=false&sort=-created&limit=16",
    "headers": { "Authorization": "Bearer {token}" },
    "items": "",
    "fields": { "title": "title", "id": "id" },
    "page_size": 16,
    "lists":  [ { "title": "Unread" },
                { "title": "Favorites", "url": "…is_marked=true…" } ],
    "search": { "url": "…search={query}…" }
  },
  "download": {
    "url": "{cfg.url}/api/bookmarks/{id}/article.epub",
    "dest_dir": "/Readeck",
    "filename": "{title}.epub"
  }
}
```

Template variables: `{cfg.*}` from the config file, `{token}`, `{id}`, `{title}`,
`{query}`, `{page}`.

### The template engine does substitution, not arithmetic

`{page}` is a **counter**, and there is no way to compute `offset = page × size`.
That single limitation shapes every `device.json` you will write.

Readeck's workaround is instructive: it **hardcodes `limit=16`** rather than
using a `{limit}` template, so the firmware's "+1 lookahead" probe never returns
an extra row and the device concludes there is no next page. Pagination is
effectively disabled in exchange for a list that works. That is the level of
cleverness the engine currently demands.

## The known plugin population — 11, across three stores

Merged from the captured catalogs on 2026-09-11. **None of these were installed
or run**; this is a roster from `catalog.json` plus source headers.

### `itsthisjustin/sd-plugins` — 8 plugins (★36, 10 forks, pushed 2026-09-10)

| Plugin | v | Mount | What it does |
|---|---|---|---|
| `plugin-store` | 1.1.2 | settings | **Installs other plugins from hosted catalogs** — the bootstrap |
| `bookfusion` | 1.2.0 | settings | BookFusion library; device-code + QR sign-in; writes `<book>.meta.json` that rides KOSync progress uploads |
| `webdav` | 1.0.0 | settings | Nextcloud / ownCloud / Seafile / Koofr; credentials in `/.crosspoint/webdav.json` |
| `wallabag` | 1.2.0 | settings | Read-it-later articles as EPUB, OAuth2 password grant; self-hosted or `app.wallabag.it` |
| `dictionaries` | 1.0.0 | settings | ~20 offline StarDict dictionaries (Wiktionary + Webster's 1913); sets `dictionaryName` |
| `organize-by-author` | 1.0.0 | **files** | Sorts EPUBs into per-author folders; EPUB 2 + 3 creator sort-names; **moves progress, cache and sidecars with the book** |
| `hello` | 1.0.0 | files | Minimal loader example — **start here** |
| `protected-content` | 1.0.4 | files | ADEPT fulfilment |

### `ruqqq/crosspoint-plugins` — a second store, 2 plugins

| Plugin | v | Mount | What it does |
|---|---|---|---|
| `libby` | 1.0.2 | files | Libby loans, self-contained ADEPT |
| `kopi` | 1.2.0 | **settings** | **OPDS** feed reader — lists issues newest-first, downloads to SD |

### Off-catalog

| Plugin | Where | Note |
|---|---|---|
| `readeck` | never upstream | `plugin.js` **+ `device.json` v1.4.0** — the reference for on-device UI |
| `libby` (josmerod) | **deleted upstream**, alive in 5 forks | The independent implementation; hands `.acsm` to `protected-content` |

### What the roster tells you

- **`hello` is the actual starting point** for a new plugin — a minimal loader
  example, MIT-adjacent in spirit but see the licence caveat below.
- **`kopi` proves the OPDS path.** It is a template for Calibre-Web, Kavita or
  Komga, not a single-vendor integration.
- **`organize-by-author` is the only plugin that mutates the library**, and
  notably it moves progress/cache sidecars with the book — worth reading before
  writing anything that touches user files.
- **A store is just a repo with a `catalog.json`.** Three exist, all on the same
  schema, two of them built independently — which is the strongest evidence that
  the store protocol is genuinely reusable.

> ⚠ **Licensing.** `itsthisjustin/sd-plugins` has **no licence**;
> `ruqqq/crosspoint-plugins` has **no licence**; `protected-content` has no
> licence and lives in **no git repository**. All-rights-reserved by default.
> Read for technique; do not copy.

## Does it really work?

**Yes — with the caveat that I verified none of it on hardware.** The evidence is
that multiple independent authors have shipped non-trivial things on it:

| Plugin | Author | What it proves |
|---|---|---|
| `protected-content` | Diirge | A **full Adobe ADEPT client** runs in this model — RSA keygen, signing, PKCS#12, AES unwrap |
| `readeck` | Diirge | `device.json` browse+download **shipped in v1.4.0**, with on-device UI |
| `libby` (josmerod) | — | **Cross-plugin RPC** via the job queue works as designed |
| `libby` (ruqqq) | ruqqq | Same flow, self-contained — **and the only tested code, 26 cases** |
| `kopi` | ruqqq | **OPDS** — so any OPDS server (Calibre-Web, Kavita, Komga) is reachable |

Three plugin **stores** exist (`itsthisjustin/sd-plugins`, `ruqqq`'s, and the
bundled one), all using the same catalog schema. A store is just a repo with a
`catalog.json`.

**The honest counterweight:** the firmware branch is `feat-sd-plugins`, which is
**66 commits ahead of `develop` and 0 behind** as of 2026-09-10 — a clean
fast-forward, actively developed, but **not merged**. This is not a dormant
roadmap item; neither is it shipped to everyone.

## What it can't do

| Limit | Value | Notes |
|---|---|---|
| Relay response | **32 KB** | **Behaviour on overflow is disputed — see below** |
| Fetch segment | 2 MB client / 4 MB firmware ceiling | Files >2 MB always need a second call |
| Manifest | 8 KB | |
| Redirects | **not followed** | Resolve them yourself, or relay each hop |
| Archives | **no extraction** | No unzip on device |
| Background work | **none** | A browser page must be open for actions to run |
| Sandbox | **none** | Plugins share the page's full authority |

### The 32 KB relay cap: four sources, four different behaviours

This matters because it decides how you write every plugin, and **there is no
captured firmware evidence for any of it**:

| Source | Claimed behaviour | Basis |
|---|---|---|
| Prior firmware read | HTTP **413** *"response too large, use /api/fetch"* | Read of `RELAY_BODY_LIMIT` — **handler not captured** |
| `readeck/IDEAS.md` | **`abort()`s the device** | Real-device crash; author hedges *"appears to"*; dump not captured |
| `libby` (josmerod) | **silently truncates** | Header comment |
| `libby` (ruqqq) | returns a **200 with an `error` body** | What their code handles |

ruqqq's case deserves a note, because prior research cited it as corroboration
for the 413: it isn't. Their only evidence is **a mock in their own test suite**,
and the shape they handle — `if (!r.error) return r;` — can only fire on a
resolved 2xx whose body carries `error`. A real HTTP 413 would **throw** in
`_readResponse` before reaching it. Their code encodes a *third* belief, not
support for the first.

**Practical guidance regardless:** keep relayed responses small, page
aggressively (`readeck` ships `PAGE_SIZE = 5`), and use `fetchToSd` for anything
large — it has no cap.

## What's easy to add, and what needs a fork

This is the question worth answering, so it is worth being specific.

### Easy — no firmware change, hours not weeks

| You want | How |
|---|---|
| **Any HTTP+JSON catalogue on the device** | `device.json` alone. No JS |
| **Any OPDS server** — Calibre-Web, Kavita, Komga | `kopi` is a working template; change the base URL |
| **A new content source with login** | `plugin.js` for auth + `writeFile` the token; `device.json` reads it back via `token.file`/`token.path` |
| **Serious crypto** | `/api/crypto` already exposes keygen, sign, pubencrypt, AES, PKCS#12, SHA-1/256, random — enough for a full ADEPT client, as proven |
| **Your own plugin store** | A GitHub repo with a `catalog.json`. Two independent people have done it |
| **Cross-plugin calls** | `registerAction` + the job queue |

The gating skill is **JavaScript and an API you can reach over HTTP**, not
embedded development. That is a genuinely low bar and it is the design's main
achievement.

### Requires a firmware fork

| You want | Why it's blocked |
|---|---|
| **A crypto op that isn't in the list** | The op set is firmware-side |
| **Relay responses over 32 KB** | `RELAY_BODY_LIMIT` is a firmware constant |
| **Redirect following** | Not implemented in the relay |
| **Unzip / archive extraction** | No extractor on device |
| **Arithmetic in `device.json`** (real pagination) | The template engine substitutes only |
| **Anything running with no browser open** | There is no on-device JS engine — the host *is* the browser |
| **A new mount point** | The pages that load plugins are firmware |
| **Sandboxing plugins from each other** | Would require an isolation model that doesn't exist |

**The sharpest line:** anything expressible as *"make HTTP calls, do crypto, write
files, render a list"* is a config or a small JS file. Anything requiring the
**device to act on its own**, or requiring a **new capability from the firmware**,
is a fork.

### The architectural ceiling

The system deliberately puts **no scheme-specific knowledge in the firmware**.
The firmware's DRM glue comment says it outright: *"Generic path — the reader
carries no scheme name."* All Adobe-specific logic lives in an off-repo plugin.

That is a clean, consistent decision with an obvious consequence: **the device
can only do what a browser page, connected to it, tells it to do right now.**
Everything else is a fork.

## Practical notes for writing one

- **Page small.** The relay cap is the most common failure and the least
  gracefully handled.
- **Use `fetchToSd` for content**, always — no cap, and book bytes never pass
  through the page.
- **Expect files >2 MB to need a Range-capable server.**
- **`device.json` first** if your source is a plain JSON API — it gets you an
  on-device UI for free, and no JS to maintain.
- **Ship both**: `plugin.js` for setup, `device.json` for daily use.
- **Copy ruqqq's error handling.** Catching the relay error and telling the user
  *what to do about it* is the only example of that discipline in the ecosystem.

## What was not established

- **No plugin was installed or run.** Every behavioural claim is from source or
  from an author's report.
- **The firmware handlers for `/api/relay`, `/api/fetch` and `/api/plugin-fs` were
  not captured** — so all limits, the 413 path, and Range behaviour are
  second-hand.
- **Which branch upstream intends to merge is unknown.**
- Plugin **licensing is largely absent** across the ecosystem — see the
  [plugin source survey](plugin-source-survey.md).

## See also

- [Plugin source survey](plugin-source-survey.md) — what the DRM plugins are, and their shared lineage
- [The ContentProtection library](../../../frameworks/freeink-sdk/contentprotection-library.md) — the firmware half of the DRM chain
- [`dtsbytebooks.com` review](dtsbytebooks-review.md) — who operates ADEPT now
- [SD plugins and protected content](sd-plugins-and-protected-content.md) — the store protocol and plugin roster
