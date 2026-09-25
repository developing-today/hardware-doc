# Recovering dead technical sites — archives, mirrors and the order to try them

- **Compiled:** 2026-09-02. Every figure below was measured on that date unless stated otherwise.
- **Re-verified independently 2026-09-04** by a second pass that re-ran the load-bearing probes. Most
  values reproduced **byte-for-byte** (see §12 S25); three findings were **corrected** and are marked
  inline: the Wayback throttle ceiling and failure mode (§2.2), the CDX-vs-availability host split
  (§2.3, strengthened), and archive.today's `/timemap/` endpoint (§7.4, previously recorded as
  CAPTCHA-walled — it is not).
- **The question:** *the datasheet / manual / tech report / forum thread I need is gone. Where is
  the copy, and how do I get at it without being blocked?*
- **Why this file is here.** The rest of this directory is about *preprint servers* — places that
  are alive and want to be read. This file is about the opposite case, which is the more common one
  in hardware work: `hpl.hp.com` is TCP-dead, `datasheetcatalog.com` is NXDOMAIN, Espressif has
  silently withdrawn a datasheet, `parc.com/publications/` now redirects to a corporate division
  page. Those are all *measured* facts from this repository, not hypotheticals — see
  [`government-and-institutional-technical-reports.md` §4](government-and-institutional-technical-reports.md)
  and the repository's [crawler access table](../../ai-crawler-site-access-table.md)
  (§ Vendor documentation portals, § Electronics distributors).
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).
- **Raw probe output:** [`../../archive/research/preprint-repositories/bulk-archives/probe-log-2026-09-02.txt`](../../archive/research/preprint-repositories/bulk-archives/probe-log-2026-09-02.txt)
  and `waybackratelimit.txt` in the same directory; re-verification logs in
  [`../../archive/research/preprint-repositories/dead-sites/`](../../archive/research/preprint-repositories/dead-sites/)
  (`VERIFY-SUMMARY.md` plus `verify-01`…`verify-13`).

> **Two corrections to this repository's own guidance are recorded here.** The
> [crawler access table](../../ai-crawler-site-access-table.md#general-retrieval-tips) currently
> recommends the **Memento Aggregator** (`timetravel.mementoweb.org`) — that host is **NXDOMAIN as
> of 2026-09-02** and the service was shut down at the end of 2025 (§7.2). And
> [`retrieval-notes.md`](retrieval-notes.md#6-rate-limits-and-terms) records "`web.archive.org/web/`
> 429-blocks while the CDX API stays open"; that is **wrong in the way that costs you data**. The CDX
> API is on the *same host* as replay and degrades with it — confirmed on two independent runs, in
> both failure modes (§2.3). What stays open is `archive.org` (availability, metadata,
> `advancedsearch.php`), which is a **different host**.

---

## 1. The decision tree — the page is gone, do this in this order

Run top to bottom. Stop when you have bytes with the right magic number.

| # | Step | Cost | Catches |
|---|---|---|---|
| **0** | **Confirm it is actually gone.** Probe a deliberately bogus sibling path. A 200 with an SPA shell, a soft-404, or a UA-inverted block all look like "deleted" | one request | Most false alarms. See the three failure classes in the [crawler table](../../ai-crawler-site-access-table.md#vendor-documentation-portals) |
| **1** | **`archive.org/wayback/available?url=<url>`** | one request, ~0.7–2.5 s | Is there *any* IA snapshot? Fast, on a **different host** to the replay service, and it survived every rate-limit window measured here (§2.2) |
| **2** | **Wayback CDX** — `web.archive.org/cdx/search/cdx?url=…&output=json` | one request | The full capture list with status codes; `matchType=prefix` enumerates a whole dead directory (§2.3) |
| **3** | **Replay with `id_`** — `web.archive.org/web/<ts>id_/<url>` | one request, **paced ≥1.5 s** | The original unmodified bytes. Mandatory for PDFs and binaries (§2.4) |
| **4** | **Is it a *vendor manual or historical computing document*? → bitsavers** (§4) | grep one text file | DEC, IBM, HP, CDC, Data General, Xerox, plus 8,297 component datasheets. Wayback will not have these; bitsavers will |
| **5** | **Is it an *archive.org item* rather than a web page?** `advancedsearch.php` + `metadata/<id>` (§3) | two requests | Scanned manuals, ROM dumps, CD-ROMs, magazines — 3.04 M items in `collection:"manuals"` alone |
| **6** | **Is it *source code*? → Software Heritage** (§6) | one request | Whole repositories, including deleted GitHub/GitLab/Gitorious origins. 439 M origins |
| **7** | **A different web archive** — Arquivo.pt first, then archive.today (§7) | one request | Arquivo.pt has captures IA lacks and a working CDX API. It replayed the dead HP Labs Compaq/DEC index for us |
| **8** | **Common Crawl** — index + WARC byte-range (§7.5) | two requests | Machine-friendly, no rate limit hit here, and it holds **PDFs** — we pulled a 722 KB TI datasheet out of a WARC |
| **9** | **Exact-string search** — a unique phrase, error message or part number, quoted | manual | Forks, mirrors, course pages, GitHub copies. Still the highest-yield manual step |
| **10** | **A mirror of the *whole site*** — vendors' downstream partners, university mirrors, `mirrorservice.org`, `ftpmirror.your.org` | manual | Frequently the only route once the origin starts blocking bots (§4.4) |

**Not on this list, deliberately:** Google cache and Bing cache. Both are dead as recovery routes
in 2026 and §8 shows the measurements.

---

## 2. The Internet Archive Wayback Machine

### 2.1 The four endpoints, and which host each lives on

This distinction is the single most operationally useful thing in this file, because the two hosts
fail independently.

| Endpoint | Host | Purpose |
|---|---|---|
| `archive.org/wayback/available?url=<url>` | **`archive.org`** | "Is there a snapshot, and which is closest?" JSON, tiny |
| `web.archive.org/cdx/search/cdx?url=…` | `web.archive.org` | Enumerate **every** capture, with status codes |
| `web.archive.org/web/<timestamp>/<url>` | `web.archive.org` | Replay, **rewritten** for browser display |
| `web.archive.org/web/<timestamp>id_/<url>` | `web.archive.org` | Replay, **original bytes**, no rewriting |
| `web.archive.org/save/<url>` | `web.archive.org` | Submit a capture (unauthenticated, heavily throttled) |

Measured 2026-09-02 [API]:

```
archive.org/wayback/available?url=hpl.hp.com/techreports/Compaq-DEC/
  -> 200, 246 B  {"archived_snapshots":{"closest":{"status":"200","available":true,
                   "url":"http://web.archive.org/web/20190213111131/http://hpl.hp.com:80/techreports/Compaq-DEC/",
                   "timestamp":"20190213111131"}}}

archive.org/wayback/available?url=this-domain-does-not-exist-zzq9.example/
  -> 200,  77 B  {"url":"...","archived_snapshots":{}}          <- clean negative control
```

**The availability API is scheme- and path-literal.** `roa.rutgers.edu/info.html` returns
`{}` while `roa.rutgers.edu/` returns a 2026-07-11 snapshot. Query the exact URL you want, and if
that is empty, fall back to a CDX prefix query before concluding anything.

### 2.2 Rate limits, measured honestly

This was probed deliberately because a sibling record left it half-documented, and **re-probed
independently on 2026-09-04**, which changed the conclusion in three ways. All figures Chrome-131 UA,
sequential `curl`, single IP [WEB]:

| Pattern | 2026-09-02 run | 2026-09-04 re-probe |
|---|---|---|
| Rapid `/web/` replay GETs before the first failure | #1–3 → 200, then blocked | **#1–16 → 200**, blocked from #17 |
| Mode of the block | **HTTP 429**, 620-byte body, `server: nginx`, `x-rl: 0`, `x-na: 0` — *"Your request is being blocked because our system has flagged it as suspected abusive bot traffic that is degrading the performance of the Wayback Machine."* | **TCP connection refused** (`curl` exit 7, `http_code` 000) in ~80–480 ms. **No 429 was seen once in ~60 requests** |
| Recovery | still 000 at **+20 s**; 200 at **+60 s** | requests **flap** 200/000 within seconds (below) |
| **6 GETs paced 1.5 s apart** | **6/6 → 200** | not re-run |
| UA rotation during a block | Useless | Useless — and demonstrably so (below) |

**Three corrections, and the third is the one that will corrupt a harvest:**

1. **There is no fixed low quota.** "About three requests" was measured *inside an
   already-throttled window* and is too pessimistic; the re-probe got **16 consecutive 200s** before
   the block engaged. **Do not calibrate a scraper against either number** — the ceiling is a moving
   server-side judgement, not a published quota.
2. **429 and TCP-refusal are alternative modes, not an ordered escalation.** The first run saw only
   429s then refusal; the second saw only refusal, never a 429. Handle both, and treat
   `http_code == 000` on `web.archive.org` as *throttling*, not as *the Internet Archive is down*.
3. **⚠ The throttled state flaps, so a partial success does not mean you are clear.** Identical
   Chrome-131 requests, 1 s apart, on 2026-09-04:

   ```
   200 200 000 000 000 200 200 000 000 000
   ```

   **A bulk fetch running through a throttle window therefore yields a silent mixture of retrieved
   and missing files, with no error that distinguishes "not archived" from "refused".** Verify every
   file by magic bytes and re-drive the whole list until it is clean; never treat one 000 as a final
   answer about a URL.

**On UA rotation — the 2026-09-04 data settles it.** While blocked, `curl/8.5.0` and `ClaudeBot`
returned 200 in the same second that `Googlebot/2.1`, `WhatsApp/2.23.20.0` and *no UA header at all*
returned 000. That is not a UA policy, it is the flapping above sampled by different requests.
**The Wayback throttle is not UA-gated — do not waste the `AGENTS.md` UA ladder on it.** (A UA table
built from a single pass through a flapping service is exactly how a spurious "working user agent"
gets recorded; this one nearly was.)

> **Byte sizes on IA drift between days and are not stable fingerprints.** The same replay capture
> measured **16,004 B** on 2026-09-02 and **16,006 B** on 2026-09-04; `metadata/tektronix_465` went
> 4,438 → 4,437 B. Sizes quoted in this file are good for recognising a *class* of response (the
> 620-byte 429, the 11,832-byte 503, the 283-byte bitsavers 403), not for equality tests.

**Where `retrieval-notes.md` goes wrong:** it records that "`/web/` 429-blocks while the CDX API
stays open." The CDX API lives on `web.archive.org` — the *same host as replay* — so when the replay
service is throttled the CDX API degrades **with it**. This is why it is worth knowing which endpoint
sits on which host, and it was confirmed on two independent runs, in both failure modes [WEB]:

```
                                              2026-09-02 (429 mode)   2026-09-04 (TCP-refusal mode)
web.archive.org/cdx/search/cdx?url=bitsavers.org   000 (refused)          503, 11,832 B
archive.org/wayback/available?url=hpl.hp.com/...   200,  246 B            200,    246 B
archive.org/metadata/tektronix_465                 —                      200,  4,437 B
archive.org/advancedsearch.php?q=…&rows=0          —                      200,    227 B
```

**Rule, now confirmed on two independent runs: everything on `web.archive.org` fails together, and
everything on `archive.org` keeps working.** The availability API, the item metadata API and
`advancedsearch.php` all survived a block that had `web.archive.org` refusing TCP connections.
**Make `archive.org/wayback/available` your first call** — it answers in ~0.5 s, it is a clean
existence oracle, and it is on the host that stays up.

**A separate, unrelated failure to know about:** the CDX API intermittently returns
**HTTP 503 with an 11,832-byte "Internet Archive: Temporarily Offline" page**. Frequency is high and
variable — **1 of 3** identical requests on 2026-09-02, **2 of 3** on a cold 2026-09-04 run (the
third succeeded in 16.7 s). It is a service-wide condition, **not** a statement about your URL.
**Always retry a CDX 503 at least twice before concluding a URL has no captures**, or you will
record "never archived" for a page that is archived. Response times for CDX were poor throughout:
**5.2–16.7 s** for a 20-row query.

### 2.3 The CDX API — the enumeration tool

Base form, plus the parameters that actually earn their keep:

```
https://web.archive.org/cdx/search/cdx?url=<url>
    &output=json                       # otherwise you get whitespace-separated text
    &matchType=exact|prefix|host|domain
    &filter=statuscode:200             # skip the 301/302/404 captures
    &collapse=urlkey                   # one row per distinct URL, not per capture
    &from=2004&to=2008                 # YYYY[MM[DD[hh[mm[ss]]]]]
    &limit=500                         # and paginate; do not ask for everything
    &fl=timestamp,original,statuscode,digest,length
```

Rows are `[urlkey, timestamp, original, mimetype, statuscode, digest, length]`. Worked example, the
DEC/Compaq technical report index that this repository already established is dead at source [API]:

```
url=hpl.hp.com/techreports/Compaq-DEC/&output=json&limit=20   -> 200, 3,444 B
  earliest  20021214042738  200  text/html  19,816 B
  ...       20040102135157  301                406 B   <- note the 301s interleaved throughout
  latest measured by the sibling record: 2022-05-17 (302), 2022-05-17 (301), 2022-12-22 (301)
```

Three things that CDX gives you and nothing else does:

1. **`digest` is a SHA-1 of the payload.** Identical digests across timestamps mean the page did not
   change — pick any one of them, and you can prove a capture is byte-identical to another without
   downloading both. Five consecutive 2005 captures of the DEC index share digest
   `YHLG3MDTKGZWUXHEZJZZUY3JOOTGORHI`.
2. **`statuscode` lets you skip the redirect era.** The DEC index above was *already only a
   redirect* by 2022. Without `filter=statuscode:200` you will happily replay a 301 and report the
   collection as recovered.
3. **`matchType=prefix` enumerates a directory you can no longer list.** This is how you rebuild a
   dead vendor's `/docs/` tree: query the prefix, collapse on urlkey, and you get every path IA ever
   saw — including ones you did not know existed.

**Negative control:** `url=this-domain-does-not-exist-zzq9.example/` → **HTTP 200 with body `[]`
(3 bytes)**. Clean. Status code is *not* the signal here; body length is.

### 2.4 `id_` — the suffix you need for anything that is not HTML

Wayback rewrites replayed HTML: it injects its own JavaScript, a toolbar, and rewrites every link to
point back into the archive. For reading, that is fine. For **recovering a file**, it corrupts the
bytes.

| Suffix | Meaning | Measured on the same capture |
|---|---|---|
| *(none)* | Rewritten for display | 200, **16,004 B** |
| `id_` | **`id`entity — original bytes, no rewriting** | 200, **13,237 B** |
| `if_` | Framed replay (toolbar in an iframe) | — |

The 2,767-byte difference is the injected `web-static.archive.org/_static/js/bundle-playback.js`
machinery [WEB]. **For a PDF, a firmware image, a `.zip`, a CSV or a datasheet, always use `id_`,
then check the magic bytes.** This repository has already been burnt by `.pdf` URLs returning HTML
(LCSC, `documentation.espressif.com`) — a rewritten Wayback replay is the same hazard with a
friendlier face.

The existing note in the crawler table uses `if_` and it worked (a 470,491-byte ESP32-WROVER
datasheet). `id_` is the stricter choice; prefer it.

**Caveat measured here:** `id_` and `if_` are rate-limited exactly like plain replay. Our first two
`id_` attempts returned the 620-byte 429 page *while a plain replay of the same capture succeeded*,
purely because the plain one was requested first. From a cold start, `id_` returned 200 immediately.
**Do not conclude that `id_` is blocked; conclude that you are throttled.**

### 2.5 `web.archive.org/save/`

Unauthenticated, works, and is the mechanism `AGENTS.md` rule 9 refers to. Known behaviour, carried
forward from this repository's existing measurement rather than re-probed here [WEB]:

- It has **timed out at 120 s and then returned HTTP 503** on retry — which reads as failure but may
  not be. (Recorded in the crawler table, 2026-08-24.)
- Anonymous submissions are throttled to roughly a few per minute.
- **Query `archive.org/wayback/available` first.** In this pass, *every* archival candidate that was
  still live turned out to be captured already (§10) — four checks, zero saves needed.

---

## 3. archive.org at item level — a different archive that shares a domain

The Wayback Machine and the archive.org *item* store are separate systems. Wayback holds web
captures; the item store holds uploaded, catalogued objects: scanned manuals, magazines, ROM images,
CD-ROMs, software. For hardware documentation the item store is frequently the better hit.

### 3.1 Sizes, measured [API]

`https://archive.org/advancedsearch.php?q=<query>&rows=0&output=json` → `response.numFound`:

| Query | numFound |
|---|---|
| `mediatype:texts` | **52,096,704** |
| `collection:"manuals"` | **3,040,530** |
| `collection:"vintagesoftware"` | 335,219 |
| `collection:"softwarelibrary"` | 273,718 |
| `collection:"bitsavers"` | **91,398** |
| `collection:"cd-roms"` | 86,584 |
| `collection:"texts"` | **39,535** |
| `collection:"folkscanomy_computer"` | 23,940 |
| `collection:"computermanuals"` | 18,255 |
| `title:(datasheet)` | 12,636 |
| `collection:"bitsavers" AND subject:"DEC"` | 487 |

> **Probing trap — `collection:"texts"` is not `mediatype:texts`.** They differ by a factor of
> **~1,317** (39,535 vs 52,096,704). `texts` is a *mediatype*; there also happens to be a small
> collection with the same name. Getting this wrong understates the archive by three orders of
> magnitude.
>
> **Probing trap — silent zeros.** `collection:"zzq9nosuchcollection"` returns **HTTP 200 with
> `numFound: 0`**, indistinguishable from a genuinely empty real collection. Same class as the
> Zenodo facet trap in [`README.md §4`](README.md#6-probing-traps). Always run a known-good query
> alongside.

### 3.2 The `metadata/<id>` endpoint

`https://archive.org/metadata/<identifier>` returns the complete file manifest with no
authentication. Worked example [API]:

```
archive.org/metadata/tektronix_465    -> 200, 4,438 B
  metadata.title      "Tektronix Manual: 465"
  metadata.mediatype  texts
  metadata.collection ["manuals_tektronix", "manuals"]
  metadata.addeddate  2016-01-02
  metadata.uploader   sketch@cow.net          <- note: a private individual, not Tektronix
  files (14):  465.pdf                31,597,373 B   Image Container PDF
               465_text.pdf           87,710,344 B   Additional Text PDF
               465_djvu.txt              695,458 B   <- the OCR layer, as plain text
               465_jp2.zip           392,156,276 B   page images
               tektronix_465_archive.torrent  24,994 B
```

**Negative control:** `archive.org/metadata/zzq9-no-such-item-exists-here` → **HTTP 200 with body
`{}` (2 bytes)**. Status code carries no information; test for the empty object.

Files come from `https://archive.org/download/<id>/<file>` (302s to a regional node such as
`dn760005.eu.archive.org`). A missing filename returns a **real 404** (548 B) — that endpoint at
least is honest.

### 3.3 Worked example: finding a vendor manual, and why you must read the metadata

`advancedsearch.php?q=title:(tektronix 465)&fl[]=identifier&fl[]=title&fl[]=collection&rows=8&output=json`
→ 14 hits [API]. Four of the eight returned rows are 3D-printer models from `thingiverse`. Two more:

```
manualsonline-id-3d483d5c-…   "Tektronix Fish Finder 465 AND DM44 User Guide"
manualsbase-id-660252          "Tektronix Hunting Equipment TAS 465 user manual"
```

Those are the **Tektronix 465 oscilloscope** and the **TAS455/465**, bulk-imported from
manuals-aggregator sites that guessed the product category. The documents are real; the metadata is
fiction. This is the single most important thing to understand about bulk manual collections:
**the scan is usually trustworthy, the catalogue record often is not.**

The OCR is worse. The first 400 characters of `465_djvu.txt`, a real Tektronix service manual:

```
BEFORE READING  PLEASE CHECK FOR CHANGE INFORMATION AT THE REAR OF THIS MANUAL.
THIS MANUAL REPRINTED JULY 1975
:: V [-vlj.ln r L -  i"a K x-;-.-  r'|'“ , p ■ '"I E. : . J" 51  1!7 ‘■vi:
```

Headings survive; body text collapses into noise wherever the scan hit a schematic or a halftone.
**Never quote a figure from an archive.org OCR layer without opening the page image.**

---

## 4. bitsavers.org — the one that matters most

- **URL:** `https://www.bitsavers.org/` (apex `bitsavers.org` serves identically, 9,377 B)
- **Operator:** **Al Kossow**, personally. Not an institution, not a foundation, not a company.
- **Status:** active, continuously updated — most recent file in the PDF tree on the probe date was
  **2026-08-27** [WEB]
- **Self-declared size (home page, dated 2026-05-10):** *"There are over 188000 files including over
  8.86 million text pages in the 1.86tb archive."* [DOC]

If you work on hardware older than about fifteen years, bitsavers is not *an* archive, it is *the*
archive. DEC, IBM, HP, CDC, Data General, Burroughs, Univac, Honeywell, Xerox, Apple, Tektronix,
Intel, National Semiconductor, Motorola — manuals, schematics, field-service documentation, ISA
references, component data books, program listings. This repository has already had one case where
bitsavers was **the only surviving copy** of a corporate research collection (§4.5).

### 4.1 Layout

Six top-level trees, each independently indexed:

| Tree | `IndexByDate.txt` | Files listed | What it is |
|---|---|---|---|
| `/pdf/` | 8,578,234 B | **93,668** | Manuals, tech reports, schematics — the main archive |
| `/bits/` | 4,978,120 B | **70,762** | Software: tape images, disk images, source listings, OS distributions |
| `/components/` | 620,925 B | **8,297** | **Semiconductor data books and datasheets** |
| `/test_equipment/` | 243,303 B | 3,210 | Instrument service manuals |
| `/magazines/` | 195,210 B | 2,996 | Trade press |
| `/communications/` | 141,265 B | 1,808 | Telecom / networking |
| | | **180,741** | total lines across the six indexes [API] |

`/pdf/` alone contains **1,132 vendor directories** (`3M/` … `zilog/`), served as plain Apache
directory indexes. File-type mix in the PDF tree: 68,941 `.pdf`, 13,532 `.jpg`, 3,041 `.tif`,
2,378 `.bin` (ROM dumps), 1,734 `.dat`, 969 `.txt`, 469 `.zip`. The date range in
`pdf/IndexByDate.txt` runs **1997-05-14 → 2026-08-27** — twenty-nine years of continuous scanning.

Largest vendor directories in `/pdf/`, by file count [API]:

| dec | ibm | mit | hp | cdc | xerox | stanford | apple | burroughs | datapro | univac | honeywell |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 22,089 | 15,860 | 3,622 | 2,473 | 2,291 | 1,998 | 1,822 | 1,802 | 1,658 | 1,476 | 1,362 | 965 |

And in `/components/` — this is the part people miss:

| national | motorola | ti | intel | amd | xilinx | westernDigital | nec | fairchild | signetics |
|---|---|---|---|---|---|---|---|---|---|
| 909 | 751 | 658 | 460 | 236 | 179 | 172 | 147 | 141 | 127 |

**If you need a 1980s National Semiconductor or Signetics part, look here before you look anywhere
else.** The commercial datasheet aggregators (§5) have largely dropped pre-1995 parts.

### 4.2 How to search it — there is no search box

Kossow says so himself on the home page: *"I have been disappointed in how poorly bitsavers is
indexed in the modern web. So it goes."* [DOC] There is no search form, no database, no JavaScript.
The site is deliberately a static tree so that it can be mirrored byte-for-byte.

**The technique is to download the index and grep it locally.** This is the single most useful
practical fact in this file:

```bash
# One 8.5 MB download gives you the complete manifest of the PDF tree.
curl -A "$BROWSER_UA" -o idx-pdf.txt        https://www.bitsavers.org/pdf/IndexByDate.txt
curl -A "$BROWSER_UA" -o idx-components.txt https://www.bitsavers.org/components/IndexByDate.txt

# Format: "YYYY-MM-DD HH:MM:SS <path-relative-to-tree-root>"
grep -i 'signetics.*8x30' idx-components.txt
grep -i 'dec/tech_reports/SRC-RR' idx-pdf.txt | wc -l      # 170

# Path -> URL is a straight concatenation:
#   https://www.bitsavers.org/pdf/<path>
```

`IndexByDate.txt` is regenerated on every addition and is what drives the RSS feeds
(`bitsavers.org/rss/{pdf,bits,comp,mags,comms,te}.xml`; the PDF feed was 185,936 B, `pubDate`
2026-08-27) [WEB]. Sorting by date also means the *top* of the file is the newest material, which is
how you monitor the archive without polling directory listings.

Two supplementary techniques:

- **`rsync --list-only`** gives a directory listing with sizes and mtimes without transferring
  anything: `rsync --list-only rsync://bitsavers.org/bitsavers/pdf/dec/tech_reports/` returned
  **522 entries** [API]. Cheaper and more informative than scraping the Apache index.
- **Some directories carry embedded Adobe Acrobat index files** for full-text search across their
  OCR layers — Kossow mentions this for "directories with large numbers of OCRed pdf files" [DOC].
  Not machine-probed here: **[NOT-VERIFIED]** which directories have them.

### 4.3 The retrieval trap: bitsavers 403s `curl` and `Wget`

Measured 2026-09-02, and it is an inverted ladder [WEB]:

| User-Agent | `/pdf/dec/tech_reports/` |
|---|---|
| `Wget/1.21.4` | **403**, 283-byte Apache "Forbidden" |
| `curl/8.21.0` (default) | **403**, 283 B |
| Chrome 131 | **200** |

`robots.txt` is **HTTP 200 with a zero-byte body** — it expresses no restriction at all, so a naive
crawler sees an open invitation and then gets a 403 on the first fetch.

**This is not a bot-wall to be routed around; it is a stated policy.** The home page, dated
2026-05-10 [DOC]:

> *"As of April, 2026 due to the level of web traffic, Wget is no longer permitted here. […] People
> are downloading the ENTIRE site through the web interface. The situation has gotten much worse
> since the LLM web scrapers have appeared. USE ANONYMOUS RSYNC.. That's what it's there for!"*

`AGENTS.md` rule 7 forbids UA substitution to bypass access controls, and rule 5 warns against
masking genuine behaviour. **The correct reading here: a browser UA is fine for fetching the handful
of documents a human would fetch; it is not a licence to bulk-download.** For anything at volume,
the operator has provided two better routes and asks you to use them.

### 4.4 Mirrors and rsync — the sanctioned bulk routes

`rsync://bitsavers.org/` advertises six modules [API]:

```
bitsavers    The bitsavers.org archive
vtda-bits    The vtda.org software archive     vtda-books   The vtda.org book archive
vtda-docs    The vtda.org document archive     vtda-pics    The vtda.org image archive
vtda-pubs    The vtda.org publications archive
```

Full clone, as documented by the operator: `rsync -av --delete rsync://bitsavers.org:/bitsavers/ bitsavers/`.
`--delete` is required because, in Kossow's words, *"file names, dates and their location in the
hierarchy change (these aren't permalinks)"* [DOC]. **Treat every bitsavers URL you cite as
potentially unstable** and record the file name and size, not just the path.

All seven advertised web mirrors were reachable on the probe date [WEB]:

| Mirror | Root page |
|---|---|
| `bitsavers.computerhistory.org` (Computer History Museum) | 200, 9,377 B |
| `bitsavers.informatik.uni-stuttgart.de` | 200, 9,377 B |
| `bitsavers.trailing-edge.com` | 200, 9,377 B |
| `www.mirrorservice.org/sites/www.bitsavers.org/` (University of Kent) | 200, 9,377 B |
| `www.bighole.nl/pub/mirror/www.bitsavers.org/` | 200, 9,377 B |
| `archive.decromancer.ca/bitsavers.org/` | 200, 9,377 B |
| `ftpmirror.your.org/pub/misc/bitsavers/` | 200, **7,584 B** (different index page, not the origin's) |

Plus rsync mirrors at `eldanna.ocaml.nl`, `ftpmirror.your.org` and `ftpmirror.infania.net`, and FTP
at Stuttgart, Kent and your.org.

**The finding that matters:** the mirrors do **not** apply the origin's `curl`/`Wget` 403.
`mirrorservice.org`, `trailing-edge.com` and `uni-stuttgart.de` all returned **200 to the default
`curl` UA** on `/pdf/dec/tech_reports/` [WEB]. And `ftpmirror.your.org`'s `pdf/IndexByDate.txt` was
**byte-identical to the origin's** (8,578,234 B, 93,668 lines, same first line). **So the answer to
the bitsavers bot-block is a mirror, not a user-agent — and that is also what the operator wants.**

### 4.5 Case study: the DEC SRC/WRL/CRL series exists only here

The companion record
[`government-and-institutional-technical-reports.md` §4.2](government-and-institutional-technical-reports.md)
established that DEC's research-lab report series — SRC (Systems Research Center), WRL (Western
Research Lab), CRL (Cambridge), PRL (Paris), NSL (Network Systems Lab) — lost its host when
`hpl.hp.com/techreports/Compaq-DEC/` went TCP-dead, and that the directory was **already only a
redirect by 2022**. That is confirmed independently above (§2.3): every CDX capture from 2004 onward
includes 301s, and the last three captures are 302/301/301.

**This pass re-derived the bitsavers holdings by a different method** — counting prefixes in
`pdf/IndexByDate.txt` rather than parsing the Apache directory listing — and got the same numbers
[API]:

| Prefix | This pass (index) | Sibling record (dir listing) | Series |
|---|---|---|---|
| `SRC-RR-` | **170** | 170 | SRC Research Reports |
| `SRC-TN-` | **67** | 67 | SRC Technical Notes |
| `WRL-` (excl. TN) | **108** | 108 | Western Research Lab |
| `WRL-TN-` | **42** | 42 | WRL Technical Notes |
| `CRL-` | **91** | 91 | Cambridge Research Lab |
| `PRL-RR-` | **35** | 35 | Paris Research Lab |
| `NSL-*` | **7** | 7 (4+2+1) | Network Systems Lab |
| | 521 lines total in `dec/tech_reports/` | | |

Two independent methods agreeing is worth more than either alone; **treat these counts as
confirmed.**

And the object that makes the whole thing safe:

```
dec/tech_reports/Compaq-DEC_TRs_HPL_mirror_2007.zip     236,085,636 B   indexed 2023-09-04
```

**Somebody took a copy of HP Labs' hosted collection in 2007. That ZIP is now the reason the
collection exists.** HP never announced the removal; the directory quietly degraded to a redirect
some time before 2022 and then the host stopped answering entirely.

Spot check, with a negative control [WEB]:

```
/pdf/dec/tech_reports/SRC-RR-1.pdf       -> 200, 2,239,056 B, magic "%PDF-1.2"
/pdf/dec/tech_reports/SRC-RR-99999.pdf   -> 404, 280 B
```

bitsavers returns **honest 404s** — class (a) in the crawler table's three-class taxonomy. A 200
from this host really does mean the file exists. That is rarer than it should be.

### 4.6 Bitsavers on archive.org, and what it is not

`collection:"bitsavers"` on archive.org holds **91,398 items** (§3.1) — a partial, item-ised mirror,
useful because it is full-text searchable and IA-hosted, but **it is not the same corpus** as the
188,000-file live tree and there is no guarantee of currency. Use it for discovery; fetch from
bitsavers or a mirror.

Two limitations to state plainly:

- **Scans, not text.** Kossow's format is *"a minimal subset of PDF […] just using it as a container
  for lossless Group 4 fax compression (ITU-T T.6) images"*, scanned at 400 dpi (600 dpi since the
  2010s), with OCR *"slowly being applied to older pdf files […] it will take many years to
  complete"* [DOC]. **Many bitsavers PDFs have no text layer at all.** Grep will not find them.
- **The originals are destroyed.** *"The scanning process I use is destructive. Bindings are removed
  and paper is recycled."* Documents in good condition may go to the Computer History Museum (lot
  `X6512.2012`) [DOC]. This is a one-shot archive: what was scanned is what survives.

---

## 5. Component and datasheet archives — reliability assessment

Measured 2026-09-02, Chrome-131 UA [WEB]:

| Site | Result | Verdict |
|---|---|---|
| **`bitsavers.org/components/`** | 200 (browser UA), **8,297 files** | **First choice for pre-1995 parts.** Provenance is a named archivist and a scan; the vendor is the directory name |
| **`datasheetarchive.com`** | 200, 41,998 B; `/?q=lm317` → 200, 239,746 B of real results | Open to scripts. Results carry manufacturer + description + ECAD model. **Zero direct `.pdf` hrefs in the HTML** — downloads are JS-driven, so you cannot enumerate PDFs by scraping |
| **`alldatasheet.com`** | **403**, 5,603 B (search page 5,714 B) | Cloudflare. The **~5.6 kB 403 fingerprint** documented in [`retrieval-notes.md §1`](retrieval-notes.md) — alive, refusing robots. UA rotation did not defeat it there and there is no reason to expect it to here |
| **`datasheets.com`** | **403**, 5,601 B | Same fingerprint |
| **`datasheets360.com`** | **403**, 5,625 B | Same fingerprint |
| **`octopart.com`** | **403**, 51,989 B | Already recorded in the crawler table: *"a 52 KB 403 body that superficially looks like content"* |
| **`datasheetcatalog.com`** | **NXDOMAIN** (apex and `www`) | **Dead.** A widely-cited datasheet host that no longer resolves at all |
| **`chipdb.org`** | 200, 71,622 B | **Not a datasheet site.** A die/package *photograph* database — *"6392 images in 1222 categories"* — attached to the cpu-world.com forum. Excellent for identifying an unmarked or remarked chip; useless for electrical specifications |

### 5.1 Why an aggregator datasheet is weaker evidence than it looks

Four failure modes, all of which this repository has hit:

1. **Mis-OCR.** §3.3 shows what an OCR layer does to a scanned instrument manual. A single-character
   error in a scanned datasheet turns 3.3 V into 8.3 V and nothing flags it.
2. **Mislabelling.** archive.org's own catalogue calls a Tektronix oscilloscope manual a *"Fish
   Finder"* user guide (§3.3). Aggregators that bulk-import from other aggregators inherit and
   compound this.
3. **Wrong revision, silently.** A part is documented across revisions A/B/C with different absolute
   maximum ratings; the aggregator keeps whichever it scraped and rarely says which.
4. **AI-generated prose presented as specification.** Already recorded in the crawler table:
   `digi-electronics.com` *"misstated a chip's operating temperature by 20 °C against the
   manufacturer datasheet."* Use the tables, discard the paragraphs.

**Rule for this knowledge base:** an aggregator datasheet is a *lead*, not a source. Resolve it to
(a) the manufacturer's own file, (b) a distributor mirror with a traceable part code — the crawler
table's LCSC finding, `datasheet.lcsc.com/lcsc/<id>_<Manufacturer>-<Part>_C<NNNNN>.pdf`, is
unusually good on this because the filename carries the provenance — or (c) bitsavers, where the
directory *is* the vendor attribution. Record the byte size and the revision string from the cover
page.

---

## 6. Software Heritage — the archive of source code

- **URL:** `https://archive.softwareheritage.org/` · API base `/api/1/`
- **Operator:** Inria, with UNESCO under a formal agreement; a public-interest, non-profit archive
- **What it archives:** *source code with its full development history* — not web pages, not
  binaries, not releases-as-tarballs. Git, Mercurial, SVN, Debian source packages, and more.

### 6.1 Scale, measured [API]

`GET /api/1/stat/counters/`, 2026-09-02:

| Counter | Value |
|---|---|
| `origin` (distinct repository URLs ever ingested) | **439,088,634** |
| `origin_visit` | 2,002,159,594 |
| `content` (unique file blobs) | **29,475,358,773** |
| `directory` | 22,958,659,572 |
| `revision` (commits) | **6,103,072,139** |
| `release` | 183,390,908 |
| `snapshot` | 402,766,238 |
| `skipped_content` | 637,206 |

It is actively crawling: `https://github.com/torvalds/linux` was on **visit #478, 2026-09-02
03:44:11 UTC, status `full`** — a few hours before this probe [API].

### 6.2 SWHIDs

A **SWHID** (SoftWare Heritage persistent IDentifier) is an intrinsic, content-addressed
identifier: `swh:1:<type>:<hex>` where type is `cnt` (file), `dir`, `rev`, `rel`, `snp` or `ori`.
Because the hash is computed *from the content*, a SWHID does not depend on the archive continuing
to exist — anyone with the bytes can recompute it. That is a categorically stronger citation than a
DOI, which is a promise by a registry. `swhid.org` records the identifier as **standardised as
ISO/IEC 18670**, on top of two earlier Publicly Available Specifications [DOC] (S24).

```
GET /api/1/resolve/swh:1:cnt:94a9ed024d3859793618152ea559a168bbcbb5e2/
  -> 200  {"object_type":"content", "browse_url":".../browse/content/sha1_git:94a9ed…/"}
GET /api/1/resolve/swh:1:cnt:0000000000000000000000000000000000000000/
  -> 404, 131 B  {"exception":"NotFoundExc","reason":"Content with sha1_git … not found!"}
```

The negative control 404s properly, so `/resolve/` **is** an existence oracle [API]. Other useful
endpoints: `/api/1/origin/search/<query>/`, `/api/1/origin/<url>/get/`, `/api/1/origin/<url>/visits/`,
`/api/1/snapshot/<id>/`, and `/api/1/vault/` for reconstructing a whole directory as a tarball.

**Trap:** `origin/search/torvalds%2Flinux/?limit=5` did **not** return `github.com/torvalds/linux`
in its top five — it returned two dead Gitorious mirrors and three unrelated forks [API]. The search
ranking is poor. If you know the URL, use `origin/<url>/get/`, which resolved instantly. A bogus
search returns `[]` (2 bytes) with HTTP 200.

### 6.3 The access trap — the UA ladder runs backwards here

Software Heritage sits behind **Anubis**, a JavaScript proof-of-work wall (the same class of
obstacle recorded for EconStor and hprints in
[`retrieval-notes.md §3`](retrieval-notes.md#3-proof-of-work-walls-defeat-the-ua-ladder-entirely)).
Measured against `/api/1/origin/search/torvalds%2Flinux/?limit=3` [WEB]:

| User-Agent | Result |
|---|---|
| Chrome 131 | **200, 4,667 B — Anubis challenge page** (`<title>Making sure you're not a bot!</title>`) |
| Firefox 128 | 200, 4,626 B — Anubis challenge |
| ClaudeBot | **403**, 508 B |
| `curl/8.21.0` (default) | **200, 1,643 B — real JSON** |
| `WhatsApp/2.23.20.0` | **200 — real JSON** |
| `Googlebot/2.1` | **200 — real JSON** |
| *(no `User-Agent` header at all)* | **200 — real JSON** |

**Escalating to a browser UA breaks the SWH API.** This is the second confirmed inversion in this
repository after `nxp.com`, and it is worth a line in the crawler table: *when a site serves a
proof-of-work interstitial, the browser UA is what triggers it.* Send nothing, or send `curl`.

Note also that the challenge arrives with **HTTP 200**, so a status-code check reports success. Test
for the string `not a bot` or parse the JSON and fail loudly.

*(`www.softwareheritage.org` — the organisation's marketing site, distinct from the archive — failed
TLS verification in this environment: "unable to get local issuer certificate". The same happened on
`webarchive.org.uk`, whose certificate is a valid DigiCert chain expiring 2027-02-24. **That is a
gap in this machine's CA store, not a site fault.** Recorded so nobody repeats the misdiagnosis.)*

### 6.4 Relationship to Zenodo

Zenodo pushes eligible software deposits into Software Heritage — see
[`zenodo.md` § Software Heritage](zenodo.md). The division of labour is worth stating because people
routinely pick the wrong one:

| You want | Use |
|---|---|
| A **citable DOI** for a release of your firmware, with a version and authors | **Zenodo** |
| The **complete history** of a repository, including the commits nobody released | **Software Heritage** |
| Proof that a specific *file* existed with specific *content* | **SWHID** — intrinsic, verifiable offline |
| A repository that has been **deleted from GitHub** | **Software Heritage** (Zenodo only has what was deposited) |

For hardware work the last row is the important one: firmware, board-support packages and vendor SDKs
disappear from GitHub constantly, and SWH is usually the only place the history survives.

---

## 7. Other web archives

### 7.1 Summary, measured 2026-09-02

| Archive | Reachable? | API | Accepts save requests? |
|---|---|---|---|
| **Internet Archive** | ✅ (throttled, §2.2) | CDX + availability + item APIs | **Yes** — `web.archive.org/save/<url>`, unauthenticated |
| **Arquivo.pt** (Portuguese Web Archive) | ✅ **best-behaved of the lot** | Memento TimeMap, CDX (`/wayback/cdx`), `/textsearch` | **Yes** — `arquivo.pt/services/savepagenow` **302s to `/services/archivepagenow`**, a working "ArchivePage Now" form (200, 18,183 B). Verified as *present*; not exercised |
| **archive.today** (`.ph` / `.is`) | ⚠️ partial | **`/timemap/` works** (Memento, 5/5); `/newest/` is CAPTCHA-walled (§7.4) | Yes, but interactively only |
| **Common Crawl** | ✅ | CDX index + WARC byte-range on S3 | **No.** Crawl-only, no submission |
| **UK Web Archive** (British Library) | ❌ **service down** | — | No |
| **Library of Congress web archives** | ❌ 403 Cloudflare | — | **[NOT-VERIFIED]** |
| **Bibliotheca Alexandrina IA mirror** | ❌ TCP timeout | — | No |
| **Memento Aggregator** (`timetravel.mementoweb.org`) | ❌ **NXDOMAIN — service shut down 2025** | — | — |

### 7.2 The Memento Aggregator is gone — correct your notes

`timetravel.mementoweb.org` is **NXDOMAIN**, as are `www.`, `labs.` and `aggregator.mementoweb.org`
[WEB]. The apex `mementoweb.org` resolves and serves a 2,826-byte static stub. Its `/about/` page
(8,269 B) says why [DOC]:

> *"This website launched in 2009 and was operated and funded by the Research Library of the Los
> Alamos National Laboratory. As a result of a managerial decision, the site was taken down towards
> the end of 2025. The current static site, brought online in 2026, contains resources resurrected
> from the original site […] It is operated on a volunteer basis and is hosted as Github Pages. The
> site used to provide two services that were necessarily discontinued as a result of the forced
> migration: The **Time Travel** service was a Memento aggregator that allowed searching across a
> wide range of public web archives, providing both a user interface and an API. It operated between
> 2015 and 2025 […] The **Robust Links** service […]"*

**Consequences:**

- The recommendation in
  [`ai-crawler-site-access-table.md` § General retrieval tips](../../ai-crawler-site-access-table.md#general-retrieval-tips)
  to use `http://timetravel.mementoweb.org/api/json/<timestamp>/<url>` **no longer works and should
  be removed or annotated.** It is staged for that in §10.
- **The Memento *protocol* is unaffected.** RFC 7089 datetime negotiation is implemented by the
  individual archives, and per-archive TimeMaps still work — Arquivo.pt's did, below. What is gone
  is the one service that queried them all at once. Until something replaces it, **cross-archive
  search is a manual loop over a list of archives.**
- This is itself a textbook instance of what this file is about: a decade-old piece of public
  research infrastructure removed by an internal management decision, with no successor and no
  notice.

### 7.3 Arquivo.pt — the underrated one

The Portuguese national web archive. Nominally national in scope, in practice it crawled a great deal
of the international web and it holds captures the Internet Archive's replay throttle makes awkward
to reach. It also has **the most script-friendly interface of any archive probed here** — no UA
games, no CAPTCHA, fast.

Worked example, on the exact resource this repository lost [API]:

```
GET /wayback/cdx?url=hpl.hp.com/techreports/Compaq-DEC/&output=json&limit=5   -> 200, 1,590 B
  {"urlkey":"com,hp,hpl)/techreports/compaq-dec","timestamp":"20081022115306",
   "status":"200","length":"24883","filename":"IAH-20081022114828-07684-T1.arc.gz",
   "collection":"AWP3", ...}

GET /wayback/20081022115306mp_/http://www.hpl.hp.com/techreports/Compaq-DEC/  -> 200, 97,670 B
  "HP Labs : Compaq & DEC … Compaq & DEC Technical Reports » 2008 » 2007 » … » 1990 - 1999
   Heritage Technical Reports » Compaq & DEC Technical Reports » Tandem Technical Reports
   The Technical Reports appearing on this page were published by Compaq & DEC from 1981-2002."
```

**That is the dead HP Labs index, recovered from a Portuguese archive.** Note the replay suffix is
`mp_`, not `id_`. Negative control: a TimeMap for a nonexistent domain → **HTTP 404, 0 bytes** —
clean. There is also `/textsearch?q=<query>&maxItems=N`, a JSON full-text search over archived
content with an `estimated_nr_results` field.

**Also note:** Arquivo.pt holds captures of `hpl.hp.com` from **2008 and 2009**, when the collection
was live and complete. IA's captures of the same path degrade to redirects from 2004 onward. For a
resource that died slowly, *a second archive is not redundancy — it is a different point in time.*

### 7.4 archive.today

Reachable at `archive.today`, `archive.ph` and `archive.is` — all three returned an identical
16,590-byte root page [WEB]. It is genuinely valuable for JavaScript-heavy pages, which the Wayback
Machine captures poorly, because it stores a rendered snapshot.

**Correction (re-probed 2026-09-04): it *does* have a machine-usable discovery endpoint.** The
2026-09-02 pass recorded "every lookup path CAPTCHA-walled / no API". That is wrong for
`/timemap/`, which is a standard RFC 7089 Memento TimeMap and answered cleanly **5 times out of 5**,
no CAPTCHA, plain Chrome UA [API]:

```
GET https://archive.ph/timemap/https://www.bitsavers.org/     -> 200, 1,497 B, 5/5 attempts
  <https://www.bitsavers.org/>; rel="original",
  <http://archive.md/timegate/https://www.bitsavers.org/>; rel="timegate",
  <http://archive.md/20120731064623/http://www.bitsavers.org/>; rel="first memento";
      datetime="Tue, 31 Jul 2012 06:46:23 GMT",
  <http://archive.md/20180514014300/…>; rel="memento"; …   (and so on)
```

**So the split is discovery vs retrieval:**

| Path | Result 2026-09-04 | Usable from a script? |
|---|---|---|
| `/timemap/<url>` | **200, 1,497 B, real Memento TimeMap** | **Yes** |
| `/newest/<url>` | **429 + 63,290-byte CAPTCHA** (*"One more step — Please complete the security check"*; 55,512 B on 2026-09-02) | No |

**This matters more than it looks.** With the Memento Aggregator dead (§7.2), `/timemap/` is the one
remaining way to ask archive.today *"do you have this, and from when?"* without a browser — which is
exactly the question you need answered before deciding whether it is worth opening one. Enumerate
with `/timemap/`, then fetch the specific memento by hand. Operator identity and funding remain
undisclosed, there is still no documented API, and the endpoint is undocumented and could go at any
time — **do not build an unattended pipeline on it**, but do use it interactively.

### 7.5 Common Crawl — the one that holds PDFs

Not a web archive in the preservation sense — a crawl corpus published for research — but it is
**the best machine-accessible route to a recently-dead URL**, and unlike the Wayback Machine it did
not throttle at all here.

`https://index.commoncrawl.org/collinfo.json` → 200, 34,947 B, **127 collections** from
**CC-MAIN-2026-34 (August 2026)** back to **CC-MAIN-2008-2009** [API].

The full recovery, end to end, verified on a TI datasheet [API]:

```bash
# 1. Query the index for the crawl you want.
curl "https://index.commoncrawl.org/CC-MAIN-2026-34-index?url=www.ti.com%2Flit%2Fds%2F*&output=json&limit=3"
# -> {"url":"https://www.ti.com/lit/ds/sbos264a/sbos264a.pdf","mime":"application/pdf",
#     "status":"200","length":"660220","offset":"905907244",
#     "filename":"crawl-data/CC-MAIN-2026-34/segments/…/CC-MAIN-…-00755.warc.gz"}

# 2. Range-GET exactly that record out of the WARC. No S3 credentials needed.
curl -r 905907244-906567463 -o rec.warc.gz "https://data.commoncrawl.org/crawl-data/…-00755.warc.gz"
# -> HTTP 206, 660,220 bytes

# 3. Decompress: WARC header, then the HTTP response, then the payload.
python3 -c "import gzip; d=gzip.open('rec.warc.gz','rb').read(); i=d.find(b'%PDF'); \
            print(len(d), i, len(d)-i)"
# -> 724237  2285  721952        <- a real 722 KB PDF
```

`mime-detected` is more trustworthy than `mime` (one row showed `"mime":"unk"` with
`"mime-detected":"application/pdf"`). A URL with no captures returns **HTTP 404 with JSON
`{"message": "No Captures found for: …"}`** — honest, for both a real domain and a bogus one.

**Limitation:** Common Crawl obeys `robots.txt` and gets blocked like any other crawler. A query for
`bitsavers.org/pdf/dec/tech_reports/*` returned no captures — consistent with bitsavers' 403 to
non-browser agents. **Absence from Common Crawl is evidence about the crawler, not about the site.**

### 7.6 UK Web Archive, Library of Congress, Bibliotheca Alexandrina

- **UK Web Archive** (`webarchive.org.uk`): the certificate is valid (British Library / DigiCert,
  expires 2027-02-24); the failure in this environment was a local CA-store gap. Fetched with
  verification relaxed, it returns a 5,611-byte page titled **"UK Web Archive currently
  unavailable"**: *"The British Library is continuing to experience disruption following a
  cyber-attack and are working hard to restore services."* [WEB] **They are still crawling under UK
  legal deposit; access is what is down.** Do not record it as defunct.
- **`webarchive.loc.gov`**: **HTTP 403** with a 5,740-byte Cloudflare "Just a moment…" interstitial
  to a Chrome 131 UA [WEB]. Alive, closed to scripts. Its collections (e.g. legislative and
  government-agency web captures) are reachable through a browser. Whether an API exists is
  **[NOT-VERIFIED]**.
- **Bibliotheca Alexandrina's Internet Archive mirror** (`web.archive.bibalex.org`): DNS resolves to
  `196.204.180.101` but **TCP times out on both :80 and :443** after 25 s [WEB]. This was the
  celebrated 2002 full mirror of the Internet Archive; it appears no longer to serve. Recorded as
  **unreachable on one day from one host**, not as defunct — the discipline this repository applied
  to Synthical applies here too.

---

## 8. Search-engine caches — dead, in both directions

Both were probed because people still reach for them first [WEB]:

| Route | Result 2026-09-02 |
|---|---|
| `webcache.googleusercontent.com/search?q=cache:<url>` | **HTTP 200, ~92 KB** — but the body is a generic *"Google Search — If you're having trouble accessing Google Search, please click here"* page. **No cached content, for any URL tried.** The host still resolves; the service does not exist |
| `cc.bingj.com/cache.aspx?…` | **HTTP 400**, 194-byte Edge error: *"Our services aren't available right now"* |

Google removed the `cache:` operator and the cache link from search results during 2024, publicly
framing it as no longer needed now that the Wayback Machine is linked from the "About this result"
panel [COM]. The endpoint's continued 200 response is the dangerous part: **a naive
`%{http_code}` check reports success and you save 92 KB of Google chrome as your recovered
document.**

Combine this with the existing finding in the crawler table that DuckDuckGo's HTML endpoints return
**HTTP 202 + a CAPTCHA** and that Bing returned *wrong* results (German CRM software) for a quoted
part number, and the conclusion for this knowledge base is blunt: **search engines are not a
recovery mechanism in 2026. Enumerate archives directly.**

---

## 9. This repository's archival practice (`AGENTS.md` rule 9)

Rule 9 says: preserve scarce sources by submitting them to `https://web.archive.org/save/<url>`, but
only things that are genuinely hard to acquire and unlikely to persist — not widely-mirrored content.
The crawler table adds the crucial refinement: **check `archive.org/wayback/available` first**,
because `save/` is slow and rate-limited while the availability API is neither.

### 9.1 Candidates checked this pass

| Candidate | Source of the nomination | Availability check | Action |
|---|---|---|---|
| `https://mementoweb.org/about/` | this pass — sole record of the Time Travel shutdown | captured **2026-08-19** | none needed |
| `https://www.bitsavers.org/` | this pass — the operator's policy + mirror list, hand-maintained | captured **2026-08-31** | none needed |
| `https://www.bitsavers.org/pdf/dec/tech_reports/` | [`government-…-reports.md` §7](government-and-institutional-technical-reports.md) | captured **2025-09-19** | none needed |
| `https://www.bitsavers.org/pdf/IndexByDate.txt` | this pass — the archive's own manifest | captured **2025-07-11** | none needed |
| `https://web.ma.utexas.edu/mp_arc/` | [`retrieval-notes.md §6`](retrieval-notes.md#9-archival-candidates) | captured **2026-04-12** | none needed |
| `https://roa.rutgers.edu/` | [`retrieval-notes.md §6`](retrieval-notes.md#9-archival-candidates) | captured **2026-07-11** | none needed |
| `https://roa.rutgers.edu/info.html` | [`retrieval-notes.md §6`](retrieval-notes.md#9-archival-candidates) | **no snapshot** (`{}` and CDX `[]`) | **too late — the live URL now returns HTTP 404, 196 B** |

**No `web.archive.org/save/` submissions were made in this pass**, because every still-live candidate
was already held. That is the correct outcome of rule 9 applied properly rather than reflexively.

### 9.2 The ROA lesson

The Rutgers Optimality Archive `info.html` — described in `retrieval-notes.md` as *"a hand-written
30-year systems history that exists nowhere else"* and nominated for archival on 2026-09-01/02 — is
**already gone**, one day later, with **zero Wayback captures ever** [WEB]. The site has been
restructured to `article/browse.html` plus a downloadable `article/ROA.xlsx` index of ~1,400 papers.

Three things follow, and they generalise well beyond ROA:

1. **"Identify archival candidates" is not archival.** The gap between nominating a URL and capturing
   it is exactly where documents are lost. If a page is worth nominating, submit it in the same
   session.
2. **A domain having captures tells you nothing about a page having captures.** `roa.rutgers.edu/`
   is captured back to 2002; `roa.rutgers.edu/info.html` never was.
3. **Restructures look like deaths and vice versa.** The content may survive under a new path. Run a
   CDX `matchType=prefix` query over the old directory before writing anything off.

### 9.3 Still-open archival candidates

Carried forward from [`retrieval-notes.md §6`](retrieval-notes.md#9-archival-candidates),
[`optimization-online.md`](optimization-online.md) and
[`government-and-institutional-technical-reports.md` §4.5](government-and-institutional-technical-reports.md):

- **`optimization-online.org` old-style `DB_HTML/YYYY/MM/NNN.html` records.** Durable for 22 years,
  but the operator has already migrated once and old `DB_FILE/*.pdf` links have degraded to abstract
  pages. Enumerate via the month-archive widget, then CDX-check before saving.
- **Xerox PARC technical reports** (`CSL-`, `SSL-`, `ISL-` prefixes). The companion record calls this
  *"the most serious unresolved gap"*: `parc.com/publications/` now redirects to an SRI division
  page, and the surviving scans are scattered across bitsavers' `xerox` tree (1,998 files), the
  Computer History Museum, and individual authors' pages. **No authoritative index exists.** Building
  one from bitsavers' `IndexByDate.txt` plus CDX prefix queries over `parc.com/publications/` is the
  obvious next piece of work.
- **HP Journal (1949–1998).** `hpl.hp.com/hpjournal/journal.html` is TCP-dead. bitsavers' `hp` tree
  has 2,473 files; whether the Journal run is complete there is **[NOT-VERIFIED]**.

---

## 10. Findings staged for the crawler access table

Per `AGENTS.md` rule 8 these belong in
[`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md). That file was being
modified by concurrent work when this pass ran, so **nothing was written into it.** Merge when safe.

**§ General retrieval tips — one correction and one addition:**

- ❗ **Remove or annotate the Memento Aggregator recommendation.**
  `http://timetravel.mementoweb.org/api/json/<timestamp>/<url>` is **NXDOMAIN**; the service was shut
  down at the end of 2025 (§7.2). Replace it with a manual loop over Wayback → Arquivo.pt →
  Common Crawl.
- ➕ **Wayback throttling is volume-based, not UA-based, and has two failure modes.** The ceiling is a
  moving server-side judgement, **not a fixed quota** — measured at ~3 back-to-back `/web/` requests
  on 2026-09-02 and at **16** on 2026-09-04. It fails *either* with **HTTP 429** (620-byte body,
  `x-rl: 0`) *or* with outright **TCP refusal** (`curl` exit 7, `http_code` 000) — the two are
  alternatives, not an escalation; the 2026-09-04 run never once saw a 429. Pace at ≥1.5 s.
  ⚠ **While throttled, responses flap** — identical requests 1 s apart gave `200 200 000 000 000 200
  200 000 000 000`, so a bulk fetch yields a *silent mixture* of retrieved and missing files.
  **Everything on `web.archive.org` (replay *and* CDX) fails together; everything on `archive.org`
  (`wayback/available`, `metadata/<id>`, `advancedsearch.php`) keeps working.** Rotating user agents
  is a waste of time — during a block `curl` and ClaudeBot got 200 in the same second that Googlebot
  and no-UA got 000, which is the flapping, not a policy.
- ➕ **`web.archive.org/cdx/` intermittently 503s** with an 11,832-byte "Temporarily Offline" page —
  **1 in 3** identical requests on 2026-09-02, **2 in 3** on 2026-09-04. Not a per-URL signal.
  **Retry at least twice before recording "no captures"**, or you will write down that a page was
  never archived when it was.
- ➕ **Use the `id_` replay suffix for any non-HTML file.** Plain replay injects
  `bundle-playback.js` and rewrites links (16,004 B vs 13,237 B for the same capture).
- ➕ **Google and Bing caches are gone** (§8). `webcache.googleusercontent.com` returns **HTTP 200
  with a Google Search shell** — a silent-corruption hazard of exactly the LCSC class.
- ➕ **Common Crawl byte-range recovery works and is not rate-limited**; recipe in §7.5.

**§ Sites — new entries:**

| Site | Finding |
|---|---|
| `www.bitsavers.org` | **403 (283 B Apache) to `curl` and `Wget`; 200 to a browser UA.** `robots.txt` is a **zero-byte 200**. This is deliberate policy, not an accident — the operator asks for **anonymous rsync** (`rsync://bitsavers.org/bitsavers/`) or a mirror. **The mirrors do not apply the block** (`mirrorservice.org`, `bitsavers.trailing-edge.com`, `bitsavers.informatik.uni-stuttgart.de` all 200 to default `curl`), and `ftpmirror.your.org`'s index was byte-identical to the origin's. **Use a mirror, not a UA.** Honest 404s (280 B) — status codes are trustworthy |
| `archive.softwareheritage.org` | **Inverted ladder — Anubis proof-of-work.** Chrome 131 and Firefox 128 get a **200 with a 4,667-byte "Making sure you're not a bot!" page**; ClaudeBot gets 403; **default `curl`, WhatsApp, Googlebot and no-UA-at-all get real JSON.** Second confirmed inversion after `nxp.com`. The challenge arrives with HTTP **200** — test for the string, not the status |
| `archive.ph` / `archive.today` / `archive.is` | Root 200 (16,590 B). **`/timemap/<url>` returns a real Memento TimeMap — 200, ~1.5 kB, 5/5 attempts, plain Chrome UA, no CAPTCHA** (re-probed 2026-09-04, correcting an earlier "no API" note). **`/newest/<url>` returns HTTP 429 + a 55–63 kB CAPTCHA.** Discovery is scriptable; retrieval is browser-only |
| `arquivo.pt` | **Open, fast, no UA games.** `/wayback/cdx?url=…&output=json`, `/wayback/timemap/link/<url>`, `/wayback/<ts>mp_/<url>` replay, `/textsearch?q=`. Clean 404/0-byte negative control. Holds captures IA lacks. **Also accepts save requests** at `/services/archivepagenow` — a second place to preserve a scarce URL when `web.archive.org/save/` is throttled |
| `index.commoncrawl.org` / `data.commoncrawl.org` | Open. 127 crawls back to 2008. Range-GET into WARCs works unauthenticated (HTTP 206) |
| `webarchive.loc.gov` | 403 Cloudflare "Just a moment…" (5,740 B) |
| `webarchive.org.uk` | Service **down** (British Library cyber-attack); still crawling. Valid cert — a TLS verify failure here is a **local CA-store gap** |
| `web.archive.bibalex.org` | Resolves (196.204.180.101), **TCP timeout** on :80 and :443 |
| `timetravel.mementoweb.org` | **NXDOMAIN.** Shut down end of 2025 |
| `alldatasheet.com`, `datasheets.com`, `datasheets360.com` | Cloudflare **403, ~5.6 kB** — the fingerprint from [`retrieval-notes.md §1`](retrieval-notes.md) |
| `datasheetcatalog.com` | **NXDOMAIN** — dead |
| `datasheetarchive.com` | Open (200, real results) but **no `.pdf` hrefs in the HTML** — downloads are JS-driven |
| `chipdb.org` | Open. **Chip *photograph* database, not datasheets** — 6,392 images / 1,222 categories |

---

## 11. What this pass could not verify

- **Arquivo.pt's ArchivePage Now form** was located (302 from `/services/savepagenow`, 200 on
  `/services/archivepagenow`) but **not exercised** — its behaviour, quotas and success rate are
  **[NOT-VERIFIED]**.
- **Whether `webarchive.loc.gov` exposes a CDX or Memento API** — blocked at the front door,
  **[NOT-VERIFIED]**.
- **Which bitsavers directories carry embedded Acrobat full-text indexes.** The operator says some do;
  none were located — **[NOT-VERIFIED]**.
- **Whether `bitsavers`' 91,398-item archive.org collection is current or complete** relative to the
  188,000-file live tree — **[NOT-VERIFIED]**. Assume it is neither.
- **Whether the HP Journal run survives completely on bitsavers** — **[NOT-VERIFIED]**.
- **Whether `web.archive.bibalex.org` is permanently dead** — one host, one day. **[NOT-VERIFIED]**.
- **The Wayback throttle's exact window and quota — and after two passes we now believe there is no
  fixed one to find.** The unpaced ceiling measured **~3** on 2026-09-02 and **16** on 2026-09-04,
  and the failure mode differed between the runs (429 vs TCP refusal). The archive publishes no
  figure. **[NOT-VERIFIED]**, and treated here as unknowable from outside: pace at ≥1.5 s, retry, and
  validate every file rather than trusting a request budget.
- **Whether the flapping seen on 2026-09-04 is a load balancer with per-node state, a decaying token
  bucket, or something else.** Only the *symptom* is measured. **[NOT-VERIFIED]**.
- **Whether `archive.ph/timemap/` is reliable or was merely open on the day.** It answered 5/5 on
  2026-09-04 against a 0/2 reading on 2026-09-02 for the sibling `/newest/` path. It is undocumented,
  so its stability is **[NOT-VERIFIED]** — use it, but do not depend on it unattended.
- **Google's cache-removal date.** Widely reported as 2024 [COM]; no primary Google announcement was
  retrieved here — **[NOT-VERIFIED]** as to the exact date. The *current* state is measured.

---

## 12. Sources

Retrieval date **2026-09-02** for all of the following unless stated.

- **S1** `https://web.archive.org/cdx/search/cdx?url=hpl.hp.com/techreports/Compaq-DEC/&output=json&limit=20`
  → 200, 3,444 B. Capture timeline and 301 interleaving. Negative control
  `this-domain-does-not-exist-zzq9.example/` → 200, `[]`. [API]
- **S2** `https://archive.org/wayback/available?url=…` → 200, 246 B (positive) / 77 B (`{}`, negative).
  Host-independence during throttling. [API]
- **S3** Wayback rate-limit experiment (runs A–E), full log in
  [`../../archive/research/preprint-repositories/bulk-archives/waybackratelimit.txt`](../../archive/research/preprint-repositories/bulk-archives/waybackratelimit.txt).
  429 body, `x-rl: 0`, TCP refusal, 60-s recovery, 8-UA rotation. [WEB]
- **S4** `https://web.archive.org/web/20190213111131{,id_}/http://hpl.hp.com:80/techreports/Compaq-DEC/`
  → 16,004 B vs 13,237 B. [WEB]
- **S5** `https://archive.org/advancedsearch.php?q=…&rows=0&output=json` — all `numFound` values in
  §3.1, incl. the `mediatype:texts` (52,096,704) vs `collection:"texts"` (39,535) trap and the
  silent-zero negative control. [API]
- **S6** `https://archive.org/metadata/tektronix_465` → 200, 4,438 B, 14-file manifest.
  Negative control `…/zzq9-no-such-item-exists-here` → 200, `{}`. `…/download/tektronix_465/465_djvu.txt`
  → 695,458 B (OCR sample quoted in §3.3); missing file → 404. [API]
- **S7** `https://archive.org/advancedsearch.php?q=title%3A%28tektronix+465%29…` → 14 hits, incl. the
  "Fish Finder" and "Hunting Equipment" mislabels. [API]
- **S8** `https://www.bitsavers.org/` → 200, 9,377 B. Operator's own statements: 188,000 files /
  8.86 M text pages / 1.86 TB; Wget ban dated 2026-05-10; rsync instruction; mirror and snapshot
  lists; scanning workflow (Group 4 T.6, 400→600 dpi, `tumble`, Acrobat OCR); destructive scanning;
  CHM lot `X6512.2012`. [DOC]
- **S9** `https://www.bitsavers.org/{pdf,bits,components,test_equipment,magazines,communications}/IndexByDate.txt`
  → 180,741 lines total; per-tree sizes, vendor counts, extension mix, DEC report prefix counts,
  `Compaq-DEC_TRs_HPL_mirror_2007.zip` (236,085,636 B, 2023-09-04). [API]
- **S10** bitsavers UA matrix: `Wget/1.21.4` → 403/283 B; `curl/8.21.0` → 403/283 B; Chrome 131 → 200.
  `robots.txt` → 200/0 B. `SRC-RR-1.pdf` → 200/2,239,056 B/`%PDF-1.2`; `SRC-RR-99999.pdf` → 404/280 B. [WEB]
- **S11** `rsync://bitsavers.org/` module list; `rsync --list-only rsync://bitsavers.org/bitsavers/pdf/dec/tech_reports/`
  → 522 entries. Seven web mirrors, all 200; three tested with default `curl` → 200;
  `ftpmirror.your.org` `pdf/IndexByDate.txt` byte-identical to origin. [API]
- **S12** `https://archive.softwareheritage.org/api/1/stat/counters/` → the eight counters in §6.1;
  `/api/1/origin/https://github.com/torvalds/linux/visits/` → visit 478, 2026-09-02T03:44:11Z;
  `/api/1/resolve/…` positive and 404 negative control; `/api/1/origin/search/` ranking trap. [API]
- **S13** Software Heritage UA matrix (Chrome 131, Firefox 128, ClaudeBot, `curl`, WhatsApp,
  Googlebot, no-UA) against `/api/1/origin/search/`. Anubis page title
  `Making sure you're not a bot!`. [WEB]
- **S14** `https://mementoweb.org/` → 200, 2,826 B stub; `https://mementoweb.org/about/` → 200,
  8,269 B, quoted in §7.2. `timetravel|www|labs|aggregator.mementoweb.org` → NXDOMAIN. [DOC] [WEB]
- **S15** `https://arquivo.pt/wayback/{timemap/link,cdx}` and
  `https://arquivo.pt/wayback/20081022115306mp_/http://www.hpl.hp.com/techreports/Compaq-DEC/`
  → 200, 97,670 B, recovered HP Labs index. Negative control → 404/0 B. `/textsearch` → 200 JSON. [API]
- **S16** `https://index.commoncrawl.org/collinfo.json` → 127 collections; `CC-MAIN-2026-34-index`
  query; `https://data.commoncrawl.org/<warc>` range GET → 206/660,220 B → gunzip 724,237 B, `%PDF`
  at offset 2,285. [API]
- **S17** `archive.today|.ph|.is` roots → 200/16,590 B; `/newest/` → 429 (55,512 B on 2026-09-02, 63,290 B on 2026-09-04) CAPTCHA. **`/timemap/https://www.bitsavers.org/` → 200/1,497 B, a valid RFC 7089 TimeMap, 5/5 attempts (2026-09-04)** — corrects the 2026-09-02 reading. [WEB] [API]
- **S18** `https://www.webarchive.org.uk/` → cert valid to 2027-02-24, local verify failure;
  with verification relaxed, 200/5,611 B "UK Web Archive currently unavailable" (British Library
  cyber-attack). `https://webarchive.loc.gov/all/*/…` → 403/5,740 B Cloudflare.
  `web.archive.bibalex.org` → DNS 196.204.180.101, TCP timeout. [WEB]
- **S19** `https://webcache.googleusercontent.com/search?q=cache:…` → 200/~92 KB Google Search shell,
  for two different targets. `https://cc.bingj.com/cache.aspx?…` → 400/194 B. [WEB]
- **S20** Datasheet aggregator matrix (§5): alldatasheet 403/5,603 B, datasheets.com 403/5,601 B,
  datasheets360 403/5,625 B, octopart 403/51,989 B, datasheetarchive 200/41,998 B and
  200/239,746 B for `?q=lm317` with zero PDF hrefs, datasheetcatalog NXDOMAIN, chipdb.org
  200/71,622 B ("6392 images in 1222 categories"). [WEB]
- **S21** Archival-candidate availability checks (§9.1), incl. `roa.rutgers.edu/info.html` → `{}` +
  CDX `[]` + live **404/196 B**, and `roa.rutgers.edu/` → 200/6,278 B with the restructured
  `article/browse.html` + `article/ROA.xlsx` layout. [API] [WEB]
- **S22** Companion records in this directory:
  [`government-and-institutional-technical-reports.md`](government-and-institutional-technical-reports.md)
  §4.2/§4.3/§4.5 and S20–S21 therein;
  [`retrieval-notes.md`](retrieval-notes.md) §1, §3, §6;
  [`open-access-full-text-sources.md`](open-access-full-text-sources.md) §1;
  [`zenodo.md`](zenodo.md) § Software Heritage;
  [`optimization-online.md`](optimization-online.md) §4.
- **S23** [`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md) —
  § General retrieval tips (Memento recommendation, `save/` 503 + availability-API-first rule,
  DuckDuckGo/Bing search findings), § Vendor documentation portals (the three failure classes, the
  Espressif WROVER `if_` recovery), § Electronics distributors (LCSC filename provenance,
  `digi-electronics.com` AI-generated errors). Prior work, dated 2026-08-21/24.
- **S25** **Independent re-verification pass, 2026-09-04.** Logs in
  [`../../archive/research/preprint-repositories/dead-sites/`](../../archive/research/preprint-repositories/dead-sites/)
  (`VERIFY-SUMMARY.md`, `verify-01`…`verify-13`). **Reproduced byte-for-byte:**
  `wayback/available` 200/246 B and negative control 200/77 B; CDX success 200/3,444 B, negative
  control `[]`/3 B, "Temporarily Offline" 503/11,832 B; bitsavers `Wget`→403/283 B,
  default `curl`→403/283 B, Chrome→200, `robots.txt`→200/**0 B**, `SRC-RR-1.pdf`→200/2,239,056 B/
  `%PDF-1.2`, `SRC-RR-99999.pdf`→404/280 B; `pdf/IndexByDate.txt`→8,578,234 B/93,668 lines;
  the DEC prefix counts (170/67/108/42/91/35/7, 521 total) by a **third** method — fresh index
  download plus `grep`; `Compaq-DEC_TRs_HPL_mirror_2007.zip` = 236,085,636 B confirmed with its size
  via `rsync --list-only` (522 entries, 6 rsync modules); Software Heritage Chrome→200/4,667 B Anubis,
  default `curl`→200/1,643 B JSON, ClaudeBot→403/508 B, bogus SWHID→404/131 B, plus the Gitorious
  search-ranking trap; Google cache→200/91,694 B titled `Google Search`; `cc.bingj.com`→400/194 B;
  `timetravel|labs|aggregator.mementoweb.org`→NXDOMAIN with the apex resolving; `archive.ph` root
  200/16,590 B; Arquivo.pt CDX→200/1,590 B recovering the 2008 `hpl.hp.com` capture; Common Crawl
  127 collections, `CC-MAIN-2026-34`…`CC-MAIN-2008-2009`, bogus query→honest 404/77 B;
  alldatasheet 403/5,603 B, datasheets.com 403/5,601 B, `datasheetcatalog.com` NXDOMAIN;
  `hpl.hp.com` DNS-resolves to 15.73.144.188 but **TCP times out** (`curl` exit 28) — still dead.
  **Corrected:** §2.2 throttle ceiling/mode/flapping, §2.3 host split, §7.4 `archive.ph/timemap/`.
  **Drifted (so not usable as equality fingerprints):** replay 16,004→16,006 B,
  `metadata/tektronix_465` 4,438→4,437 B, `datasheetarchive.com` 41,998→42,632 B,
  `chipdb.org` 71,622→71,623 B. [API] [WEB]
- **S24** `https://arquivo.pt/services/savepagenow` → 302 → `/services/archivepagenow` → 200,
  18,183 B ("ArchivePage Now" form). `https://www.swhid.org/` → 200, 50,398 B; news index carries
  *"SWHID standardized as ISO/IEC 18670"*. [DOC] [WEB]
