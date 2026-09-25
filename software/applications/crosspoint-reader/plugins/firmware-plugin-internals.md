# CrossPoint Reader — the SD plugin system

**Research date:** 2026-09-02. Evidence labels: `executed-success` (I ran it), `inferred`
(read from source), `not-tested` (documented, not verified). Nothing here is
hardware-verified.

---

## Headline: two corrections to the premise, then the answer

**1. The plugin system is not "in beta" — it is not in the shipping firmware at all.**
It exists only on **two unmerged feature branches**. `develop` (the default branch, HEAD
`e6139861`) contains **zero** plugin implementation files.

**2. The hardware-reach answer: a plugin can reach *no* hardware.** There is no GPIO, no
I²C, no SPI, no peripheral access of any kind — not curated, not sandboxed, simply absent.
Plugins are **JavaScript executing in the user's browser** plus **declarative JSON
manifests** interpreted by a fixed C++ activity. No plugin code ever executes on the MCU.

**But** the boundary that *does* exist is weaker than the design implies: the plugin
filesystem endpoints are **not confined to the plugin's own directory**, and the web server
that hosts them has **no authentication**. Details in §5.

---

## 1. Where the code actually lives

`develop` has no plugin files. Verified (`executed-success`):

```
$ find . -iname '*plugin*' -not -path './.git/*'    # in crosspoint-reader @ develop
(no results)
```

The only `plugin` strings on `develop` refer to the **Calibre** desktop plugin, an
unrelated third-party thing:

- `src/activities/network/CalibreConnectActivity.cpp:80` — "mDNS is optional for the
  Calibre plugin"
- `lib/I18n/translations/english.yaml:86` — `"1) Install CrossPoint Reader plugin"`
- `docs/webserver.md:29,72`, `docs/contributing/architecture.md:171`

The implementation is on two branches:

| Branch | HEAD | Date | Ahead / behind `develop` | Author of tip |
|---|---|---|---|---|
| `origin/feat-sd-plugins` | `a7844957` | 2026-08-30 | +18 / −26 | Lindsey Bligh |
| `origin/feat-sd-web-plugins` | `bdbbbef7` | 2026-08-17 | +58 / −64 | Justin Mitchell |

`feat-sd-plugins` is the newer and more complete of the two (it adds `PluginEvents` and
`PluginHttp`, which `feat-sd-web-plugins` lacks). All source citations below are from
**`origin/feat-sd-plugins`** unless stated.

**Corroborating status from the project's own roadmap** — `ROADMAP.md:66-69` lists
"SD-loaded plugins" as a **Phase 2** item:

> **SD-loaded plugins.** Extend the device from the SD card without growing the firmware:
> plugin packages that add integrations and connectors, running through the web server and
> a whitelisted job queue instead of compiled-in code.

and `ROADMAP.md:28` marks **Phase 1 as still IN PROGRESS**, with `ROADMAP.md:76` stating
"This phase depends on Phase 1 cleanup landing first."

**Conflict recorded:** the premise "currently in beta" is not supported by the repository.
There is no beta release, no `develop` merge, and no release artifact containing plugin
code. The most defensible description is **"implemented on feature branches, awaiting a
phase gate."**

Implementation size (`feat-sd-plugins`, `executed-success` via `wc -l`):

```
1684  src/activities/plugins/PluginCatalogActivity.cpp
 297  src/activities/plugins/PluginCatalogActivity.h
 385  src/util/PluginEvents.cpp
 258  src/util/PluginHttp.cpp
  83  src/util/PluginEvents.h
  94  src/util/PluginHttp.h
  46  src/util/PluginLocations.cpp
  30  src/util/PluginLocations.h
 172  src/network/html/shared/PluginHost.js.inc
────
3049  total
```

Docs: `docs/sd-plugins.md` (389 lines), `docs/plugin-events.md` (171 lines).

---

## 2. What a plugin *is*

A folder on the SD card. `docs/sd-plugins.md:10-17`:

```
<root>/<name>/
    manifest.json     web UI card metadata (optional)
    plugin.js         browser-side plugin (optional)
    device.json       on-device catalog screen (optional)
    README.md         usage instructions, shown on-device (optional)
    ...assets
```

Discovery roots — `src/util/PluginLocations.h:10`:

```cpp
inline constexpr const char* kRoots[] = {"/.crosspoint/plugins", "/plugins", "/.plugins"};
```

"This is the single definition of 'what is a plugin'" (`PluginLocations.h:25`). A folder
qualifies if it holds any of `manifest.json`, `plugin.js`, or `device.json`
(`PluginLocations.h:17-19`). Earliest root wins on name collision (`:22-24`).

**Installation is: copy a folder onto the SD card.** No signing, no packaging format, no
verification, no manifest hash. (`inferred` — no signature/verification code exists in
`PluginLocations.cpp` or `PluginCatalogActivity.cpp`.)

---

## 3. Compilation and loading model — there is no VM

This is the crux. There are **three** execution planes, and none of them runs plugin-authored
native code on the device:

| Surface | Where the plugin's logic runs | Language | Loaded how |
|---|---|---|---|
| `plugin.js` | **The user's web browser** | JavaScript | `<script>` injected into the reader's served web page |
| `device.json` | **Nowhere** — it is data | JSON | Parsed by a fixed C++ activity |
| Job queue | The browser again (`/plugins-run`) | JavaScript | Same as `plugin.js` |

**No native code. No bytecode. No Lua, no WASM, no QuickJS, no Duktape, no Berry, no
mruby.** Verified tree-wide (`executed-success`): grep for `lua.h|wasm3|quickjs|duk_config|
berry|mruby` across `*.h/*.cpp/*.c/*.ini` matched only
`freeink-sdk/libs/book/FreeInkBook/third_party/expat/internal.h` — a substring false
positive. No interpreter is vendored in `lib/` or `freeink-sdk/libs/`.

`docs/sd-plugins.md:100-102` states the on-device plane explicitly:

> It expresses "authenticated JSON catalog: sign in, browse, download, sidecar" — enough
> for most book services — **without any code running on the device**.

And `docs/sd-plugins.md:352-354`:

> **On-device (`device.json`)** — standalone on the reader, but only the declarative
> vocabulary above … **No arbitrary logic.**

### ABI / stability story

Because nothing is compiled against firmware headers, **there is no ABI**. Compatibility is
a *schema* contract, and it is explicitly forward-tolerant. `src/util/PluginEvents.h:36-38`:

```
// Whitelist only: unknown names in a manifest are ignored with a log line, so
// manifests written against newer firmware degrade gracefully. Event names are
// a compatibility promise (semantic, not activity class names).
```

That is the only stability commitment I found. There is no versioned API surface, no
`api_version` field in the manifest schema (`docs/sd-plugins.md:139-232`), and no
deprecation policy.

---

## 4. The complete API surface

### 4a. Browser-side (`plugin.js`)

Handed to each plugin by `src/network/html/shared/PluginHost.js.inc:154-159`:

```js
relay:         (m, u, h, b)   => CrossPoint.relay(p.name, m, u, h, b),
crypto:        (op, f)        => CrossPoint.crypto(op, f),
writeFile:     (path, d)      => CrossPoint.writeFile(p.name, path, d),
fetchToSd:     (u, dest, h)   => CrossPoint.fetchToSd(p.name, u, dest, h),
registerAction:(a, fn)        => CrossPoint.registerAction(p.name, a, fn),
```

**That is the entire injected API — five functions.** Each maps to one HTTP endpoint
(`PluginHost.js.inc:69-111`). Everything else a plugin does, it does with ordinary browser
APIs against same-origin file endpoints (`/api/files`, `/mkdir`, `/move`, `/delete`),
per `docs/sd-plugins.md:379-387`.

### 4b. The device endpoints behind them

Registered in `src/network/CrossPointWebServer.cpp:219-229`, declared with intent comments
at `src/network/CrossPointWebServer.h:161-195`:

| Endpoint | Handler | Purpose |
|---|---|---|
| `POST /api/relay` | `handleRelay()` :1769 | Device performs an outbound HTTP(S) call the browser can't (CORS). 32 KB response cap (`:1823`). |
| `POST /api/crypto` | `handleCrypto()` :1959 | "Generic wolfSSL primitives (hash, random, AES, RSA, PKCS#12)" (`:1957`). Stateless, base64 I/O, 64 KB field cap (`:1971`). |
| `POST /api/fetch` | `handleFetch()` :2089 | Device streams a URL straight to SD. 4 MB per segment (`:2096`). |
| `POST /api/plugin-fs` | `handlePluginFs()` :2345 | Plugin writes a small file to SD. 256 KB cap (`:2376`). |
| `POST /api/plugin-jobs` | `handlePluginJobSubmit()` | Enqueue `{plugin, action, args}` → `{id}` |
| `GET /api/plugin-jobs/claim` | `handlePluginJobClaim()` | Executor claims next job |
| `POST /api/plugin-jobs/complete` | `handlePluginJobComplete()` | Executor posts outcome |
| `GET /api/plugin-jobs/status` | `handlePluginJobStatus()` | Caller polls |
| `GET /plugins-run` | `handlePluginRunnerPage()` :2405 | Headless executor page |
| `GET /api/plugins`, `GET /plugin` | `handlePluginList()`, `handlePluginFile()` | List / serve plugin files |

### 4c. The job queue (external automation)

A **fixed 6-slot pool** of opaque blobs the firmware never interprets
(`docs/sd-plugins.md:52-55`). Allocation is slot-recycling, oldest-finished-first —
`src/network/CrossPointWebServer.cpp:2409-2417` (`allocPluginJob`). Limits
(`docs/sd-plugins.md:88-91`): names < 24 chars, args and result < 192 bytes of JSON each,
10-minute lease reclaim. Jobs only run **while a hosting browser page is open**.

### 4d. Firmware events (`feat-sd-plugins` only)

A **closed whitelist of four events** — `src/util/PluginEvents.h:41-47`:

```cpp
enum class Event : uint8_t {
  ReaderOpen,      // "reader.open"      vars: book
  ReaderExit,      // "reader.exit"      vars: book, percent
  BookDownloaded,  // "book.downloaded"  vars: path, title, plugin
  SleepEnter,      // "sleep.enter"      vars: book, percent …
  COUNT
};
```

Delivery is deferred to an SD outbox (`<plugin dir>/events.jsonl`) and replayed as
declarative HTTPS requests when online (`PluginEvents.h:29-34`). A handler may opt into
bounded Wi-Fi bring-up at sleep (`wantsConnect()`, `:67`). Drain is bounded to
`maxEvents = 4` per call (`:81`).

---

## 5. Sandboxing and permissions — the honest assessment

### What a plugin *cannot* do

- **Touch any hardware.** No GPIO, I²C, SPI, ADC, PWM, display, or peripheral API is
  exposed. Verified (`executed-success`): grep for
  `digitalWrite|pinMode|Wire\.|SPI\.|ledcWrite|analogRead` across
  `src/network/CrossPointWebServer.cpp`, `src/util/Plugin*.cpp` and
  `src/activities/plugins/*.cpp` returns **zero matches**. The reachable device surface is
  exactly the ten endpoints in §4b.
- **Execute native code on the MCU.** No loader, no interpreter (§3).
- **Persist resident state on device.** `docs/sd-plugins.md:107-109`: "`discoverPlugins()`
  rescans the plugin folders each time the picker opens; nothing stays resident."
- **Subscribe to arbitrary firmware events.** Whitelist of four (§4d).
- **Exceed the memory caps.** Manifest ≤ 8 KB, token ≤ 2 KB, small API responses ≤ 48 KB,
  browse bodies streamed to an SD temp file with a 1 MB cap, XML parsing stops after 200
  entries per feed (`docs/sd-plugins.md:270-286`).

### What a plugin *can* do — and this is the weak spot

**Plugin file writes are not confined to the plugin's directory.** The entire path check is
one line — `src/network/CrossPointWebServer.cpp:1953`:

```cpp
bool safeWritePath(const std::string& p) { return p.size() > 1 && p[0] == '/' && p.find("..") == std::string::npos; }
```

It checks only: non-empty, absolute, no `..`. **It does not scope the path to
`<root>/<name>/`.** The `plugin` parameter *is* validated — but only as a name, by
`safeComponent()` (`:1687-1689`), which rejects `/`, `\` and `..` — and it is **never used to
derive or constrain the write path**. In `handlePluginFs()` (`:2345`) the `path` argument is
used verbatim (`:2352`, then `:2385-2396`).

Consequences (`inferred` from source; not exercised on hardware):

- Any plugin can write **anywhere on the SD card** via `POST /api/plugin-fs` — including
  another plugin's `token.file`, `/.crosspoint/settings.json`, `/.crosspoint/state.json`, or
  `/.crosspoint/content.key`. The code comment at `:2364-2366` confirms credential files are
  an intended target: *"A plugin file (config, token, rights, credential) is never
  legitimately empty."*
- `POST /api/fetch` uses the **same** check on its `dest` (`:2098`), so a plugin can
  download an arbitrary URL to an arbitrary SD path, up to 4 MB per segment.

**There is no authentication on the web server.** I searched
`CrossPointWebServer.cpp` for `authenticate|requireAuth|checkAuth|basic_auth|BasicAuth`
(`executed-success`) — every `password` hit is about *storing* OPDS or Wi-Fi credentials
(`:1440-1496`, `:1556-1618`), never about gating a request. No handler in the
`server->on(...)` table at `:179-234` performs an auth check.

So the practical trust boundary is not plugin-vs-firmware; it is **network-vs-device**:
while the web server is running, *any host on the same network* can call
`/api/plugin-fs`, `/api/fetch`, `/api/relay` and `/api/crypto` — no plugin required. The
`plugin` field is **attribution, not authorisation**.

Two mitigations, both by construction rather than by policy (`inferred`):

- The web server runs only inside an explicitly-entered activity
  (`src/activities/network/CrossPointWebServerActivity.h`, per
  `docs/contributing/architecture.md:165`), not continuously.
- `handleRelay()` calls `http.setInsecure()` (`:1792`) — TLS peer verification is
  **disabled**, because "The SecureNet transport ships no CA bundle, so peer verification
  always fails (wolfSSL -188)" (`:1789-1791`). Relayed HTTPS is therefore not
  authenticated either. This is a documented, deliberate trade-off, not an oversight — but
  it means plugin traffic is MITM-able.

### Summary table — plugin hardware reach

| Resource | Reachable? | Evidence |
|---|---|---|
| GPIO / I²C / SPI / ADC / PWM | **No** | no peripheral call in any plugin-path file (grep, `executed-success`) |
| Display / framebuffer | **No** — rendering is done by `PluginCatalogActivity`, not the plugin | `docs/sd-plugins.md:104-106` |
| Arbitrary native code on MCU | **No** | no interpreter/loader anywhere (§3) |
| Network (outbound HTTP/S) | **Yes**, via `/api/relay`, `/api/fetch` — TLS unverified | `CrossPointWebServer.cpp:1769, 2089, 1792` |
| Crypto primitives | **Yes**, wolfSSL hash/AES/RSA/PKCS#12 | `:1956-1959` |
| SD filesystem | **Yes — unconfined**, any absolute path without `..` | `:1953`, `:2352`, `:2098` |
| Firmware events | **Yes**, whitelist of 4 | `PluginEvents.h:41-47` |
| Wi-Fi bring-up | **Indirectly**, opt-in bounded, at sleep entry only | `PluginEvents.h:63-67` |
| OTA / firmware flashing | **No plugin endpoint** — OTA is a separate activity | not in `server->on()` table `:179-234` |

---

## 6. Risks worth recording

1. **Unconfined plugin filesystem writes** (`:1953`) — a malicious or buggy plugin can
   overwrite any SD file including other plugins' credentials and the reader's settings.
   Because there is no auth, so can any LAN host.
2. **TLS peer verification disabled on the relay path** (`:1792`) — no CA bundle ships.
3. **No plugin signing or integrity check** — installation is a folder copy.
4. **Unmerged and divergent** — the two branches are 26 and 64 commits behind `develop`
   respectively. Whatever lands may differ substantially from what is documented here.
5. **Not a bricking risk.** Plugins cannot write flash or trigger OTA. Bricking exposure
   sits in the separate firmware-update path (`src/network/OtaUpdater.cpp`,
   `FirmwareFlasher.cpp`), which is guarded by a board tag —
   `src/network/FirmwareBoardTag.{h,cpp}`, added in `bbca4886`, with a
   `WRONG_DEVICE_ERROR` code in `OtaUpdater.h:30`. The dual-OTA partition layout
   (`partitions.csv`: `app0`/`app1` at 0x640000 each + `otadata`) means a failed OTA can
   fall back.

---

## 7. Design intent vs. implementation — one recorded conflict

`ROADMAP.md:66-69` describes plugins as running "through the web server and a whitelisted
job queue". The implementation delivers that, **plus** a third plane the roadmap does not
mention: the declarative on-device `device.json` catalog
(`PluginCatalogActivity`, 1,684 lines) that runs authenticated HTTPS browse/download
**directly from the firmware with no browser present**. That is a materially larger
device-side surface than "a whitelisted job queue" implies — though still entirely
declarative, with no plugin-authored code executing.
