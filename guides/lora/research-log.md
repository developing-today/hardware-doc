# Research log — LoRa transceiver generations

> **Promoted into the repository 2026-09-20** from
> `archive/guides/lora/artifacts/lora-generations-pass-2026-09-04/research-log.md`, because
> [`SKILL.md` § 3](../../.agents/skills/hardware-device-research/SKILL.md) requires a pass to
> maintain `research-log.md` **as a repository document**, and this one was reachable only through
> the archive. Content is unchanged apart from the two relative links below, repointed for this
> directory. The archive copy is retained and marked superseded.

Pass date **2026-09-04** (see the date note in the pass's own
[`README.md`](../../archive/guides/lora/artifacts/lora-generations-pass-2026-09-04/README.md)).
Search cutoff: 2026-09-04.
Ordered roughly as executed. Statuses: `useful` · `duplicate` · `rejected` · `inaccessible` · `dead` · `archived`.

---

## 1. Establishing what "4th generation" means

| # | Service / host | Exact query or path | Depth | Status | Outcome |
|---|---|---|---|---|---|
| 1 | `www.semtech.com` | `/products/wireless-rf/lora-connect/lr2021` | 1 | **dead** | **HTTP 404**, 106 118 B. Wrong family — the first useful negative |
| 2 | `www.semtech.com` | `/products/wireless-rf/lora-connect` and `/lora-core` index pages | 1 | partial | 200. ⚠ Neither lists the LR2021; `lora-connect` lists `lr1121` but not `lr1110`/`lr1120` |
| 3 | `www.semtech.com` | `/sitemap.xml` → `/sitemap-products.xml` | full | **useful** | ⭐ Revealed a **`lora-plus`** family holding **`lr2012`, `lr2021`, `lr2022`** plus three `LR2021EVK2*` SKUs. This is the enumeration that unlocked the task |
| 4 | `www.semtech.com` | `/products/wireless-rf/lora-plus/lr2021` | 1 | **useful** | 200, 224 120 B. `<title>` = *"LoRa Plus™ LR2021 \| **Fourth-generation LoRa® IP** …"* — first primary confirmation |
| 5 | `www.semtech.com` | 10 further product pages (lr1121, lr1110, lr1120, sx1276, sx1272, sx1268, llcc68, sx1280, lora-plus, evk) | 1 | **useful** | ⚠ Slow (~20 s/page); run in background. LR1121 page states *"third generation"* |
| 6 | `www.semtech.com` | `/products/wireless-rf/lora-plus/lr9999` (**negative control**) | 1 | control | 404, 106 118 B — same size as #1, so #1 is a genuine 404 |

## 2. Getting the datasheet

| # | Service / host | Query / path | Status | Outcome |
|---|---|---|---|---|
| 7 | `semtech.my.salesforce.com` | `/sfc/p/E0000000JelG/a/RQ00000EZ5fu/<token>` (the LR2021 *Datasheet* link) | **inaccessible** | 200 + 1 359 B self-POSTing shell |
| 8 | idem | POST to `/sfc/p/` with `compositePageName` (fragment stripped) | **inaccessible** | 200 + 53 747 B Lightning Out bootstrap; exposed `distributionId = 05DRQ00000EZ5fu` and `/sfc/ld/` |
| 9 | idem | `/sfc/ld/…` by GET, POST, `/app.js`, `/app.js?aura.format=JSON…`, `/aura?r=1` | **inaccessible** | 550 B *"Unable to Process Request"* every time |
| 10 | idem | `/sfc/dist/version/download/?oid=00DE0000000JelG&d=…&asPdf=false` | **inaccessible** | 200 `application/json`, **0 bytes** — endpoint exists, wants `ids=` |
| 11 | idem | `/sfc/servlet.shepherd/document/download/05DRQ00000EZ5fu` | **inaccessible** | 200, 787 B HTML |
| 12 | idem | **invented token** (negative control) | control | ⚠ **200, 1 363 B** — the endpoint is unprobeable |
| 13 | `web.archive.org` CDX | `url=semtech.my.salesforce.com/*` | **dead end** | Only bare-host redirects captured. No archive route to any gated document |
| 14 | `www.bing.com` | `LR2021 datasheet pdf Semtech` | **useful** | ⭐ Yielded the **Mouser** and **Digi-Key** mirror URLs, plus Seeed, Waveshare, NiceRF product pages. **The single most valuable query of the session** |
| 15 | `mm.digikey.com` | `…/docus/8924/600_62785538.LR20xxDatasheet_V2_1.pdf` | **useful** | 200, 5 809 234 B, `%PDF`. **Rev 2.1** |
| 16 | `www.mouser.com` | `/pdfDocs/61979758LR2021_V1_1_datasheet.pdf`, Chrome UA | **rejected** | ⚠ 200 + **13 895 B HTML** captcha page. Kept as the specimen |
| 17 | idem, `WhatsApp/2.23.20.0` | same URL | **useful** | 200, 5 158 757 B, `%PDF`. **Rev 1.1** — a *different revision* |
| 18 | `web.archive.org/save/` | the Mouser URL | **archived** | 302 accepted 2026-09-04 |

## 3. Enumerating Semtech's whole output

| # | Host | Path | Status | Outcome |
|---|---|---|---|---|
| 19 | `www.semtech.com` | `/design-support/development-support-documents/` | **useful** | ⭐ 805 220 B page carrying an inline `var doc_portal` JSON object — **1 984 document entries**, dates 2018-11-14 … 2026-08-25 |
| 20 | derived | category / platform / host histograms of #19 | **useful** | 1 005 datasheets, 346 app notes, **only 5 errata**; hosts: 1 726 `my.salesforce.com`, 120 `my.site.com`, **103 dead `force.com`**, 30 GitHub |
| 21 | `semtech.force.com` | `/DP/DP_CommunityLogin?docId=<valid>` and `<bogus>` | **dead** | **404** for both — the host, not the document |
| 22 | `semtech.my.site.com` | same `docId`s | partial | 200 + login page for both. **Recovery = swap the host** |
| 23 | `www.semtech.com` | `/uploads/documents/{DS_SX1276-7-8-9_W_APP_V7,sx1276,DS_SX1261-2_V1.2,DS_SX1280-1_V3.2,DOESNOTEXIST}.pdf` | **dead** | ⚠ **All five: 200 + identical 21 149 B HTML.** Soft-404 across the whole subtree |
| 24 | `www.semtech.com` | `/uploads/{common,technology}/…pdf` + a bogus control | **useful** | Real PDFs; bogus → honest 404 (103 375 B). Subtree-specific behaviour |
| 25 | `www.semtech.com` | `/robots.txt`, all six sitemaps, `sitemap-DOESNOTEXIST.xml` | **useful** | All 200 except the control (404) |
| 26 | `www.semtech.com` | UA matrix: Chrome / bare `curl` / ClaudeBot / WhatsApp | **useful** | ⚠ WhatsApp **403**; everything else 200. Inverse of Mouser |

## 4. Recovering the older generations

| # | Host | Query | Status | Outcome |
|---|---|---|---|---|
| 27 | `web.archive.org` CDX | `url=semtech.com/uploads/documents/*&filter=mimetype:application/pdf` | **useful** | 3 LoRa hits incl. `DS_SX1276-7-8-9_W_APP_V5.pdf` |
| 28 | idem | `url=semtech.com/*&matchType=domain`, limit 6 000 | **useful** | The legacy `images/datasheet/` store: SX1272/SX1276 datasheets and both errata, 2013–2017 |
| 29 | idem | grep for `lr11`/`lr20` | **negative result** | ⭐ **Zero hits.** No archive route to any Gen-3 or Gen-4 document |
| 30 | `web.archive.org` | `…/20180903190247if_/…DS_SX1276-7-8-9_W_APP_V5.pdf` + 2 errata | **useful** | Three `%PDF` files retrieved and filed |

## 5. Software and ecosystem

| # | Host | Query | Status | Outcome |
|---|---|---|---|---|
| 31 | GitHub API | `orgs/{LoRa-Net,Lora-net}/repos` | **useful** | Identical lists (case-insensitive org). ⚠ **No standalone `lr2021_driver`** — Gen-4 driver lives inside `usp` |
| 32 | GitHub API | `repos/LoRa-Net/usp` metadata, releases, tags, recursive tree | **useful** | 47 768 093 B / 1 419 files; driver subtree 66 files / 688 630 B; pinned `512a095e…` |
| 33 | `raw.githubusercontent.com` | 70 files of the `lr20xx_driver` subtree + USP licences | **useful** | Snapshotted → 106 656 B tarball. **BSD-3-Clause-Clear** |
| 34 | GitHub API | `search/code q=LR2021 repo:jgromes/RadioLib` | **useful** | 41 hits; `src/modules/LR2021`, 15 files |
| 35 | GitHub API | `commits?path=src/modules/LR2021` (paginated, 135 commits) | **useful** | First `2472fbdf…` 2025-06-09; latest `267d4e95…` 2026-08-12 |
| 36 | GitHub API | `contents/src/modules/LR2021?ref=<tag>` for 7 tags | **useful** | ⭐ Absent at 7.2.1/7.3.0/7.4.0/**7.5.0**; present at 7.6.0+. **First release = 7.6.0** |
| 37 | GitHub API | RadioLib release 7.6.0 body; PRs #1676, #1700; issue #1457 | **useful** | Issue opened **2025-03-13**, one day after the announcement; PR merged 2026-01-30 |
| 38 | `raw.githubusercontent.com` | `RadioLib/{7.2.1,7.7.1}/license.txt` | **useful** | ⭐ **MIT at both** — resolves the SX1262 record's open LGPL-3.0 question. ⚠ `LICENSE` 404s; the file is `license.txt` |
| 39 | GitHub API | Meshtastic: code search, issue search, `commits?path=src/mesh/LR2021Interface.cpp`, PR #10401, tags | **useful** | Merged 2026-05-08; ⚠ **absent from `v2.7.26`**, present in `v2.8.0.*` |
| 40 | GitHub API | Meshtastic `LoRaRadioType.h` at HEAD and at `v2.7.26` | **useful** | `LR2021_RADIO` at HEAD only |
| 41 | GitHub API | `LLCC68.cpp`, `LLCC68.h`, `LR2021.h` contents | **useful** | LLCC68 SF/BW restrictions as executable code; LR2021 frequency ranges; a datasheet-vs-RadioLib conflict on the STDBY_RC clock |

## 6. Community

| # | Host | Query | Depth | Status |
|---|---|---|---|---|
| 42 | `old.reddit.com/search.json` | `q=LR2021&sort=new&limit=25` (UA `WhatsApp/2.23.20.0`) | 25 results | **useful** — the whole sample |
| 43 | idem | `q=LR2021 meshtastic` | 7 results | **duplicate** of #42 |
| 44 | idem | `q=LoRa fourth generation LR2021` | 25 results | ⚠ **rejected** — Reddit fell back to a global recency feed; results entirely unrelated. Multi-word queries do not work on this endpoint |
| 45 | `old.reddit.com/<permalink>.json` | 9 threads with full comment trees | 100 comments each | **useful** — quoted and classified in `projects-and-community.md` |

## 7. Vendors and pricing

| # | Host | Status | Outcome |
|---|---|---|---|
| 46 | `www.seeedstudio.com` | **useful** | LR2021 EVK 915 MHz US V2.0 — **$99.00**, two nodes |
| 47 | `www.waveshare.com/Core2021-XF.htm` | **useful** | $11.99/$12.99; three SKUs; ⭐ a comparison table asserting **no AES / no key store** on the LR2021 vs the LR1121 |
| 48 | `www.nicerf.com/lora-module/lora2021f33-2g4.html` | **inaccessible** | **403** to Chrome *and* WhatsApp |
| 49 | `www.mouser.com/c/?q=` | **inaccessible** | 13 895 B Access Denied to every agent |

---

## Search engines — a warning worth repeating

| Engine | Behaviour |
|---|---|
| **Bing** | Worked for query **1** (#14, the crucial one) and then returned **wrong** results for every later query — thesaurus pages for `LR1121 datasheet`, package-tracking sites for `LR1121 datasheet filetype:pdf`, Xbox pages for `SX1268 datasheet pdf semtech`. **Not zero results — wrong ones.** |
| **DuckDuckGo `html/`** | **HTTP 202** (throttle) to Chrome and to WhatsApp |
| **DuckDuckGo `lite/`** | 200 once with the WhatsApp UA, then 202 |
| **`search.marginalia.nu`** | 200 but no useful hits for part numbers |

**Consequence:** the LR1121, LLCC68 and SX1268 datasheets could **not** be located and are recorded
as explicit gaps in their records, rather than guessed at. That is the honest outcome, and the three
records say so in their §1/§6 rather than quietly omitting the artifact.

---

## Known exclusions

- **No account was created** on the mySemtech Document Portal. What lies beyond the login wall is
  `not-tested`. (⚠ Not needed for LoRa — §4.3 of the vendor guide shows no LoRa document is gated.)
- **No hardware was tested.** No LR2021, LR11xx or SX127x part exists in this knowledge base.
- **Chinese-language sources were not searched.** NiceRF and Waveshare both have Chinese sites that
  may carry documents their English pages do not.
- **Semtech press releases were not enumerated**, which is why the Gen-2 and Gen-3 introduction
  dates remain `inferred`/`unresolved`
  ([lineage guide §7](../hardware/lora-radio-generations.md)).
- **TTN forum, Meshtastic Discourse and the Meshtastic Discord were not searched** — Reddit and
  GitHub carried enough, and the sample is declared rather than implied.
- **`AN1200.*` application notes were all `blocked`**; none was read. The LR2021 record cites their
  titles and dates only.
