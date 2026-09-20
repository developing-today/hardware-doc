# `protected-content` and `libby` — plugin source survey

> A brief structural survey of the two DRM-fulfilment plugins. **Not a security
> audit**: this establishes what they are, what they touch, and how they relate.
> Line-by-line logic was **not** reviewed.
>
> Surveyed **2026-09-11** from archived copies. `executed-success` for the
> measurements below; behavioural claims are `inferred`. **Neither plugin was
> installed or run**, and no account or loan was used.

| | `protected-content` | `libby` |
|---|---|---|
| Author | Diirge | ruqqq |
| Version | 1.0.4 | 1.0.2 |
| Size | 53,887 B · 1,133 lines | 64,847 B · 1,441 lines |
| Mount | `files` | `files` |
| Hosting | **Railway, off-GitHub** | `raw.githubusercontent.com` |
| Licence | **none** | **none** |

## There are THREE plugins here, not two — and the lineage is now settled

A third artifact changes the picture: **josmerod's `libby`**, deleted from
upstream `sd-plugins` but alive in five forks. Measuring identical substantive
lines (>60 chars) across all three:

| Pair | Identical lines | Share |
|---|---|---|
| josmerod `libby` ↔ ruqqq `libby` | **4** | **~2 %** |
| josmerod `libby` ↔ `protected-content` | **4** | **~2 %** |
| **ruqqq `libby` ↔ `protected-content`** | **225** | **71 %** |

So there are **two independent codebases**, not three:

1. **josmerod's `libby`** — genuinely independent. It *deliberately excludes* the
   DRM crypto and hands `.acsm` files to `protected-content` over the job queue.
   Its header: *"It deliberately does NOT contain the Adobe DRM crypto… That keeps
   the crypto in one place and this plugin a thin Libby API layer."*
2. **`protected-content` + ruqqq's `libby`** — one ADEPT engine, two wrappers.

### ruqqq's plugin states its own derivation

No inference needed — line 4 of `ruqqq/libby/plugin.js`:

> *"**Derived from the Protected Content plugin, whose account activation and
> fulfillment code is reused unchanged**; this adds the half that was missing —
> getting the authorization file."*

A prior analysis concluded ruqqq was an independent implementation partly because
`grep protected-content` returned **0 hits**. The header says **"Protected
Content"** — capitalised, with a space. A hyphen cost the finding.

The 71 % figure and that sentence agree exactly: the ADEPT half is reused, the
Libby half is new.

### What's unique to `protected-content`

**94 of its 319 substantive lines are absent from ruqqq's copy** — chiefly device
activation, legacy-credential migration, and the manual `.acsm` upload path. So
ruqqq's repo does *not* fully subsume it.

This matters for preservation: `protected-content` exists in **no git
repository**, only on a Railway host. Its ADEPT engine now survives inside
ruqqq's repo, but **that ~29 % does not**.

### Practical consequence

Two genuinely different routes exist, and the difference is architectural rather
than cosmetic:

| | josmerod `libby` | ruqqq `libby` |
|---|---|---|
| Plugins needed | `libby` **+** `protected-content` | **`libby` alone** |
| DRM engine | separate plugin, **Railway-hosted, in no repo** | **in-plugin** |
| Served from | Railway PaaS | GitHub raw |
| Tests | none | **26 cases** |

If you are choosing today, ruqqq's has no single-point-of-failure on a free-tier
PaaS host. That argument stands independently of code quality.

## Identical capability surface

Both request exactly the same eight `/api/crypto` operations:

```
keygen · sign · pubencrypt · aesenc · aesdec · pkcs12 · sha1 · random
```

That is the ADEPT primitive set: RSA keygen and signing for device activation,
PKCS#12 for the credential container, AES for content-key unwrap, SHA-1 because
ADEPT still specifies it.

Device API usage is near-identical too:

| API | `protected-content` | `libby` |
|---|---|---|
| `api.relay` | 2 | 2 |
| `api.crypto` | 1 | 1 |
| `api.fetchToSd` | 1 | **3** |
| `api.writeFile` | 3 | **4** |
| `api.registerAction` | 3 | 2 |

`libby`'s extra `fetchToSd`/`writeFile` calls are consistent with it handling
multiple loans and persisting a loan list.

## Files written to SD

| Path | Written by | Contents |
|---|---|---|
| `/.crosspoint/content.key` | both | the ADEPT device credential (PKCS#12) |
| `/.crosspoint/content-activation.json` | `protected-content` | activation record |
| `/.crosspoint/libby.json` | `libby` | the Libby link |
| `/Libby/` | `libby` | fulfilled books |

**Both write the same credential path**, so the two plugins share device
activation — installing one and then the other should not require re-activating.
`inferred` from the path constant, not tested.

## Correction — an earlier version of this page was wrong

**An earlier revision of this document claimed both plugins call
`dtsbytebooks.com/api/v1/register`, `/api/v1/login` and `/api/fulfill`, and that
ByteBooks was "the load-bearing third party" through which fulfilment is routed.
That was false, and it is retracted.**

Re-checked directly against both archived sources on 2026-09-11:

```
$ grep -c dtsbytebooks plugin.js
1                      # protected-content  (line 892)
1                      # libby              (line 1173)

$ grep -n dtsbytebooks plugin.js
892:  '<a href="https://dtsbytebooks.com/register" target="_blank" …
```

**`dtsbytebooks.com` appears exactly once in each plugin, as a hyperlink in the
UI telling the user where to create an account.** No code path fetches it. Those
`/api/v1/*` endpoints do not exist — the paths return the site's single-page-app
shell.

Every network constant in either plugin:

| Plugin | Constant | Value |
|---|---|---|
| both | `ACS` | `https://adeactivate.adobe.com/adept` |
| `libby` only | `LIBBY_BASE` | `https://sentry.libbyapp.com` |

That is the complete list. **All ADEPT protocol traffic goes to Adobe's
activation host**; `libby` additionally calls OverDrive's API. The original
distinction this page "corrected" — `protected-content` talks to Adobe directly —
was closer to right than the correction.

### And ByteBooks is not a third party at all

`dtsbytebooks.com` is **the current operator of Adobe's ebook DRM platform**.
Adobe transferred Adobe Content Server, RMSDK and Adobe Digital Editions to
**Wipro Ltd** (via Harman's Digital Transformation Solutions division — the "DTS"
in the name) in July 2025; ByteBooks IDs replaced Adobe IDs for end users on
**2026-06-23**. Adobe's own support pages say so, and the DNS is conclusive:

```
adeactivate.adobe.com.  CNAME  activate.dtsbytebooks.com.
readerscert.adobe.com.  CNAME  readerscert.dtsbytebooks.com.
```

So the `ACS` constant in both plugins *already resolves into ByteBooks
infrastructure*. Registering a ByteBooks ID is simply how one obtains an Adobe ID
now. A fuller review is in
[`dtsbytebooks-review.md`](dtsbytebooks-review.md).

**How the error happened, since it matters more than the fact:** the endpoint list
was taken from a malformed intermediate tool output rather than re-read from
source, and the plausibility of `/api/v1/login` on a domain already known to be
present stopped the check. A one-line `grep -c` would have caught it. Host
*presence* in a file is not evidence of a host being *called*.

## `sentry.libbyapp.com` is not error telemetry

Worth stating because the name invites a wrong conclusion. `libby` sets:

```js
// Libby. sentry.libbyapp.com is current; sentry-read.svc.overdrive.com is the …
const LIBBY_BASE = 'https://sentry.libbyapp.com';
```

"Sentry" here is **OverDrive's own API service name**, not Sentry.io crash
reporting. The plugin is not shipping telemetry to a third party — it is calling
Libby's API. A naive host-list review would flag this as analytics; it is not.

Hosts actually contacted, in full:

- `protected-content`: **`adeactivate.adobe.com` only**
- `libby`: `adeactivate.adobe.com` and `sentry.libbyapp.com`

`dtsbytebooks.com` is linked in the UI of both but never fetched.

## What this survey does **not** establish

- **No audit of the fulfilment logic.** 1,133 and 1,441 lines respectively; only
  constants, API calls, paths and hosts were extracted.
- **No review of credential handling.** Both write a PKCS#12 credential to an
  unencrypted SD card and both hold account passwords in page memory during
  activation. Whether either does anything careless with them was **not checked**,
  and given that plugins are explicitly **not sandboxed**, any plugin on the
  device could read `/.crosspoint/content.key` regardless.
- **No verification that either works.** Neither was installed.
- **No determination of who wrote the shared core**, or under what terms it was
  reused. Both are unlicensed.

## Practical guidance

Use `libby` if you want library loans; it supersedes `protected-content` for that
purpose and is the only one that lists loans. Use `protected-content` only if you
have `.acsm` files from elsewhere.

Prefer `libby` on provenance grounds too: it is in a git repository with history,
whereas `protected-content` is two files on a Railway host with **no repository
and no Wayback mirror** — see
[source-snapshots.ARCHIVED.md](source-snapshots.ARCHIVED.md).

Both are unlicensed third-party JavaScript that handles credentials on an
unauthenticated web server. That is a decision to make deliberately.

## See also

- [The Libby path](libby-path.md) — the complete setup procedure
- [SD-card plugins and protected content](sd-plugins-and-protected-content.md) — the API and its limits
