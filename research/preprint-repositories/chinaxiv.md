# ChinaXiv — preprint repository record

- **URL:** https://chinaxiv.org/ · global index at https://global.chinaxiv.org/
- **Operator:** National Science Library, Chinese Academy of Sciences
  (中国科学院文献情报中心), built under CAS direction with support from the CAS Bureau of Science
  Communication (中国科学院科学传播局) (S2)
- **Discipline scope:** all disciplines — *as actually used*, dominated by astronomy, biology,
  psychology, physics, library/information science and medicine; computer science is present but
  small (§2, §3)
- **Launched:** **2016** — stated in ChinaXiv's own help document (S2) [DOC]
- **Status:** active. Home page and help pages served on 2026-09-01; newest listed submissions
  dated 2026-08-30 (S1) [WEB]
- **Compiled:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 1. What it is

ChinaXiv is the Chinese Academy of Sciences' national preprint platform. Its own help text
describes it as built "按照中国科学院部署" (per CAS deployment) by the CAS National Science Library
in **2016**, and states the ambition of being a "国家级预印本交流基础设施" — a *national-level*
preprint exchange infrastructure — operated "按国际通行规范" (according to internationally
accepted norms) (S2) [DOC].

Two things about it surprise Western readers.

First, **it is much smaller than its front page suggests.** The headline counter reads
4,110,127, but that is an aggregate: ChinaXiv's *own* holdings are **47,362**, and the remaining
**4,062,765** are an index of *international* preprints harvested from elsewhere (§3). If you cite
"ChinaXiv has 4.1 million papers" you have cited the wrong number by a factor of ~87.

Second, **it moderates, and it says so plainly** — including a screen that has no analogue on
arXiv. ChinaXiv's help document states that a submission is publishable so long as it contains no
"较大的政治问题或学术问题" — *major political or academic problems* (§4). That is an unusually
candid statement of a political-scope check, published by the operator itself.

Since **2022** ChinaXiv has run a "2.0" release: bilingual interface, the ChinaXiv-Global preprint
index, open commenting/review features, **CSTR** identifier registration for all preprints, and
interconnection with CAS platforms SciEngine, ScienceDB and CSCD (S2) [DOC].

## 2. Scope and subject taxonomy

ChinaXiv uses a Chinese national discipline classification, not arXiv-style category codes. The
computing- and electronics-relevant classes, with live counts from the home page browse panel
(2026-09-01) (S1) [WEB]:

| Class (Chinese) | English | Records |
|---|---|---|
| 计算机科学 | **Computer science** | **2,052** |
| 图书馆学、情报学 | Library & information science | 3,496 |
| 数字出版 | Digital publishing | 3,223 |
| 光学 | Optics | 1,590 |
| 材料科学 | Materials science | 1,234 |
| 核科学技术 | Nuclear science & technology | 930 |
| 动力与电气工程 | Power & electrical engineering | 599 |
| 土木建筑工程 | Civil & architectural engineering | 251 |
| 工程与技术科学 | Engineering & technology (general) | 224 |
| 统计学 | Statistics | 218 |
| 数学 | Mathematics | 222 |
| 矿山工程技术 | Mining engineering | 166 |
| 信息科学与系统科学 | **Information & systems science** | **85** |
| 能源科学 | Energy science | 60 |
| 航空、航天科学技术 | Aeronautics & astronautics | 55 |
| 机械工程 | Mechanical engineering | 46 |
| 电子与通信技术 | **Electronics & communications** | **40** |
| 交通运输工程 | Transport engineering | 18 |
| 水利工程 | Hydraulic engineering | 16 |
| 测绘科学技术 | Surveying & mapping | 11 |
| 安全科学技术 | Safety science | 6 |
| 食品科学技术 | Food science | 4 |
| 化学工程 | Chemical engineering | 2 |

The large non-computing classes for context: 天文学 (astronomy) 7,554 · 生物学 (biology) 5,485 ·
物理学 (physics) 3,823 · 心理学 (psychology) 3,712 · 地球科学 3,268 · 医学、药学 3,232 ·
其他 (other) 1,774.

**The engineering and electronics numbers are tiny.** Electronics & communications has **40**
records in a decade. This is the central practical fact for a hardware or systems engineer.

## 3. Size and growth

Headline counters, read from the ChinaXiv home page on **2026-09-01**, default curl UA
(S1) [WEB]. Verbatim source string:

> `搜全球 4110127 论文总量 47362 ChinaXiv论文量 4062765 国际预印本论文量 202860565 论文访问量 62412214 论文下载量`

| Counter | Chinese | Value |
|---|---|---|
| Total indexed | 论文总量 | 4,110,127 |
| **ChinaXiv's own preprints** | **ChinaXiv论文量** | **47,362** |
| International preprints indexed | 国际预印本论文量 | 4,062,765 |
| Cumulative views | 论文访问量 | 202,860,565 |
| Cumulative downloads | 论文下载量 | 62,412,214 |

**Internal consistency check (passed):** 47,362 + 4,062,765 = 4,110,127 exactly. The two
components sum to the headline, which supports reading 47,362 as native holdings and the balance
as an external index [API-style arithmetic on WEB figures] [INF].

**Second consistency check (near-miss, recorded not resolved):** the per-discipline browse counts
in §2 sum to **46,427**, against the 47,362 native figure — a shortfall of **935** (~2.0%).
Probable causes are uncategorised records or a differing refresh time between the two page
widgets. Not investigated further. [WEB] [INF]

The international index is surfaced separately at `global.chinaxiv.org`, whose links reveal
harvested records from other servers with composite IDs such as `eartharxiv_1287251` and
`psyarxiv_1287871` (S1) [WEB]. So ChinaXiv-Global is a **discovery layer over other people's
preprints**, not content ChinaXiv hosts.

**Growth is real but modest**: the home page's "最新提交" (latest submissions) listed items dated
2026-08-29 and 2026-08-30 at retrieval, i.e. the platform was taking deposits the day before the
probe (S1) [WEB].

**Not verified:** any year-by-year deposit series, and any independent scientometric measurement
of ChinaXiv's size or growth. I found no machine-readable API and did not locate a published
statistics page. **[NOT-VERIFIED]**

## 4. Screening and moderation — what gets in

ChinaXiv runs a genuine gate, documented in its own help file (S2) [DOC]. It calls this
**形式审查** — *formal examination*, explicitly a form/eligibility check rather than peer review.

Verbatim, §3.8 of the help document:

> 用户提交的论文，将经系统与管理员的**形式审查**，包括：系统自动执行**格式、重复性、剽窃性、研究性**
> 四项检验；管理员对论文详细页面进行检查，检查各字段填写是否准确、PDF打开是否正常、格式是否准确、
> **学者的身份证明**是否符合要求、学科分类是否准确。通过审查后，论文即在平台发布。

Which is, in operational terms:

1. **Four automated checks**: 格式 format · 重复性 duplication · 剽窃性 plagiarism ·
   研究性 whether it is actually research.
2. **A human administrator check**: metadata field accuracy, that the PDF opens, formatting,
   **whether the author's identity credentials meet requirements**, and correctness of the subject
   classification.
3. Only after passing does it publish.

Rejection grounds are enumerated at §4.2 (S2) [DOC]: 格式不规范 (non-conforming format) ·
重复性论文 (duplicate) · 剽窃性论文 (plagiarised) · 非研究性论文 (non-research). The author may
fix and resubmit.

**The political screen.** ChinaXiv's explanation of how preprints differ from journals says a
submission may be published so long as (S2) [DOC]:

> 只要作者提交至预印本平台的文章不存在**较大的政治问题**或学术问题，只要作者的文章具有一定的学术亮点，
> 具有学术交流的价值，便可以在预印本平台上得到发布。

— i.e. *provided the article has no major political problem or academic problem*, and has some
academic merit and exchange value. This is stated by the operator, not inferred. Record it as
such: **ChinaXiv applies a political-content criterion that arXiv, HAL and bioRxiv do not.**

**Author identity.** Depositors may optionally (and are advised to) upload
**研究身份识别材料** — research-identity credentials — including a list of their prior
peer-reviewed publications, to speed identification and release (S2) [DOC].

**Identifiers and withdrawal.** On submission a *temporary* ID is issued; the formal **ChinaXivID**
is granted only after the review passes (S2) [DOC]. Withdrawal is deliberately hard: users cannot
delete or retract an approved preprint themselves, and

> 由于预发布论文是首发证明，所以平台**理论上不执行"撤销"操作**

— because a preprint is proof of priority, the platform *in principle does not perform withdrawal*,
except in special cases with reasoned author request and platform agreement, via an administrator
(S2) [DOC]. Versions are updated in place through 版本更新 (version update) instead.

## 5. Reliability — what you can and cannot trust

What a ChinaXiv deposit **does** guarantee:

- A timestamp and priority claim (首发权), which is the platform's stated purpose (S2) [DOC].
- That an automated plagiarism/duplication check and a human formal review were passed (§4).
- A **CSTR** identifier — since the 2.0 release ChinaXiv registers CSTR for all preprints (S2)
  [DOC]. (CSTR resolution behaviour **not verified** here.)

What it **does not** guarantee:

- **No peer review.** The help text is explicit that preprints are "未经严格同行评议" — not
  rigorously peer-reviewed — and characterises quality as lower than journal articles, with
  post-hoc open review offered as the compensating mechanism (S2) [DOC].
- **No guarantee of retractability.** The near-refusal to withdraw (§4) means an erroneous or
  superseded preprint tends to stay up with a new version appended. When citing, pin the version.
- **No independent quality signal you can read from outside.** Because article pages are not
  retrievable by script (§8), you cannot cheaply audit a ChinaXiv record the way you can a HAL or
  arXiv one.

**Eventual-publication rate: not verified.** I found no measurement of what fraction of ChinaXiv
preprints later appear in journals, and did not locate scientometric literature on ChinaXiv during
this pass. **[NOT-VERIFIED]** — do not repeat any figure for this without a source.

**Known-adjacent oddity worth flagging.** The home page's "最新活动" (latest activities) panel
promotes a series of updates about a self-named "韬（τ）定律" ("Tao (τ) law"), including
*"韬（τ）定律" V2版本在ChinaXiv更新发布* (2026-07-07) and a claim of a new result in the
semiconductor field (2026-05-25) (S1) [WEB]. A named personal "law" being promoted on the
operator's own front page is the kind of thing a reader should notice; I make no judgement on its
content, which I did not read (article pages being unreachable, §8).

## 6. What you actually find there — examples

Concrete items listed on the home page's "最新提交" and related panels, **2026-09-01** (S1) [WEB].
Note these are titles-as-displayed; **I could not open the article pages** (§8), so I do not
present authors' affiliations or abstracts.

- *Freshness-Aware Robust Cooperative Task Offloading in Dynamic SAGINs* — [计算机科学], 2026-08-30,
  Lei Tao, Shihe Xu, Xinming Zhang. Space–air–ground integrated network task offloading; squarely
  a distributed-systems/networking paper, in English.
- *Proof-Valid Benchmarking for Approximate LLM Caching* — 2026-08-30. English.
- *A Time Scaling Theory for Multi-Layer Electronic Syst…* — 2026-07-03. English.
- *AMWNN: Auxiliary Multiresolution Wavelet-based Neural Networks for Solving Radiative Transfer
  Problems* — [数学], 2026-08-30, Feng Han. English.
- *Theoretical investigation of hydrogen bonding network …* — 2026-08-30, multi-author.
- Chinese-language items dominate psychology and education, e.g.
  *减负成效为何易反弹：执行功能视域下作业负担的生成机理与治理启示* — [心理学], 2026-08-30, 张海.

Most-downloaded list (热门论文排行) is overwhelmingly Chinese-language psychology, e.g.
*孤独症人群会话障碍的研究进展和展望* (15,936 views) (S1) [WEB].

**The realistic take for a Western engineer.** The computer-science stream is small (2,052 items)
but **a meaningful share of recent CS submissions are written in English** — of the CS/maths items
visible on the front page on 2026-09-01, the majority carried English titles. So ChinaXiv is not a
language-locked resource for CS the way it is for psychology. What it is *not* is a place where
you will find work you cannot find elsewhere: there is no ChinaXiv equivalent of HAL's INRIA
report series. Treat it as a **supplementary discovery surface for recent Chinese CS/ML
preprints**, not a primary literature source, and expect to be unable to fetch the PDFs
programmatically.

## 7. Landmark papers

**None identified.** I found no paper on ChinaXiv in software, distributed systems, databases,
electronics or security that has become a landmark in the sense used elsewhere in this collection.
This is consistent with the size figures (§2: 2,052 CS records, 40 electronics records) and with
the fact that Chinese CS groups overwhelmingly preprint to arXiv. Combined with the inability to
open article pages (§8), I decline to construct a landmark table. **[NOT-VERIFIED]** — absence of
evidence here is partly an artefact of my access limits, and should be re-checked by someone who
can render the site in a browser.

## 8. Access, APIs and bulk retrieval

Probed **2026-09-01**. This section is the main practical warning in this record.

**Reachability from outside China: partial.** The site *is* reachable — the home page returned
HTTP 200 with **the default curl user-agent**, no UA substitution required, in ~2.6 s
(104,948 bytes). No geoblock, no CAPTCHA, no bot-interstitial (S1).

| Target | Result (2026-09-01) | UA needed |
|---|---|---|
| `https://chinaxiv.org/home.htm` | **HTTP 200**, 104,948 B | default curl |
| `https://chinaxiv.org/user/help.htm` | **HTTP 200**, 64,223 B | default curl |
| `https://global.chinaxiv.org/` | HTTP 200, but only **2,027 B** — JS shell, no content | default curl |
| `https://chinaxiv.org/abs/202605.00224` (real ID) | **HTTP 403** | **all five UAs failed** |
| `https://chinaxiv.org/abs/202606.00108` (real ID) | **HTTP 403** | **all five UAs failed** |
| `https://chinaxiv.org/user/download.htm?id=61234` | HTTP 405 | — |
| `https://chinaxiv.org/user/about.htm` | HTTP 404 | — |

**Article pages are blocked at the route level, not by user-agent.** Every `/abs/` request returned
HTTP **403** with a page titled **系统正在维护中** ("system under maintenance", 4,729 bytes), and
this was identical across the full fallback ladder: default curl, Chrome 131, WhatsApp/2.23.20.0,
ChatGPT-User/1.0 and ClaudeBot/1.0. **Rotating user-agents does not help here** — record that, so
nobody burns time on it.

**Negative controls** (essential, because 403 and 404 mean different things here):

| Probe | Result | Reading |
|---|---|---|
| `/this-page-does-not-exist-zzz.htm` (bogus) | HTTP **404**, title 您访问的页面不存在 ("the page you visited does not exist") | Genuine 404 path exists and is distinguishable |
| `/abs/999999.99999` (bogus ID) | HTTP **403**, title 系统正在维护中 | Same as a *real* ID — so 403 carries **no** information about whether the record exists |
| `/abs/202605.00224` (real ID from home page) | HTTP **403**, title 系统正在维护中 | Confirms the block is route-wide |

The consequence: **you cannot verify the existence of an individual ChinaXiv record by HTTP status
from outside.** A 403 is returned for real and fabricated identifiers alike. Any claim in this file
about a specific paper rests on the home-page listing only.

- **URL scheme:** article pages are `https://chinaxiv.org/abs/YYYYMM.NNNNN` (e.g.
  `/abs/202606.00108`); discipline browse is
  `/user/search.htm?field=domain&value=<n>`; news is `/newsdetail.htm?id=<n>` (S1) [WEB].
- **API:** no public REST or OAI-PMH endpoint found. **[NOT-VERIFIED]**
- **Bulk retrieval:** not offered as far as I could establish. **[NOT-VERIFIED]**

## 9. Licensing and reuse

**Not verified.** I did not locate a licence statement for ChinaXiv deposits. `/user/about.htm`
returns HTTP 404 and the help page (§4 source) covers submission workflow rather than rights.
Because article pages are unreachable (§8) I could not read a per-record licence field either.
**[NOT-VERIFIED]** — do not assume CC BY, and do not assume redistribution is permitted.

## 10. Caveats and controversies

1. **The 4.1M headline is not ChinaXiv's size.** Native holdings are 47,362; the rest is a
   harvested index of other servers (§3). This is the single most likely misquotation.
2. **Article pages are unfetchable by script** — HTTP 403 for every user-agent tried, and the same
   403 for bogus IDs, so status codes prove nothing (§8).
3. **A political-scope criterion is applied and published** (§4). This is a real difference in
   kind from arXiv/HAL screening, and readers citing ChinaXiv content should know the corpus is
   shaped by it.
4. **Withdrawal is close to impossible by design** (§4) — errors are superseded, not removed.
5. **Computing and electronics coverage is thin**: 2,052 CS and 40 electronics records (§2).
6. **Licensing is undetermined** (§9).
7. **Relationship to Chinese national open-access policy: not verified.** ChinaXiv self-describes
   as national-level infrastructure under CAS (S2), and its help text references a CAS notice,
   *"中国科学院科技论文预发布平台（ChinaXiv）关于规范开展预印本学术交流的几点说明"* (S1) [WEB],
   which I did not retrieve. I found **no** evidence of a national deposit mandate.
   **[NOT-VERIFIED]**
8. **Partnerships are advertised but unverified in substance.** The home page announces a pilot
   with **Taylor & Francis / F1000** for open peer review and publishing, and a
   **SMBU China–Russia** platform accepting Chinese, English and Russian (S1, S2) [WEB] [DOC].
   Existence of the announcements is verified; their operation is not.

## 11. Sources

- **S1** — ChinaXiv home page, https://chinaxiv.org/home.htm · retrieved **2026-09-01**
  (HTTP 200, 104,948 B, **default curl UA**, UTF-8). Supports: all §3 headline counters (verbatim
  string quoted), the full §2 discipline table, §6 example titles and dates, the
  ChinaXiv-Global/`eartharxiv_`/`psyarxiv_` composite IDs, the 韬（τ）定律 activity items, the
  Taylor & Francis/F1000 announcement, and the §8 URL scheme. Local copy of the fetched body
  retained at
  `doc/hardware/scratch/preprint-repositories/regional/body_chinaxiv_home__default-curl.html`.
- **S2** — ChinaXiv help / user guide, https://chinaxiv.org/user/help.htm · retrieved
  **2026-09-01** (HTTP 200, 64,223 B, default curl UA). Supports: 2016 founding and CAS National
  Science Library operatorship, the "国家级预印本交流基础设施" self-description, the 2022 "2.0"
  release with ChinaXiv-Global/CSTR/SciEngine/ScienceDB/CSCD, the §4 moderation text (§3.8), the
  §4.2 rejection grounds, the political-and-academic-problems criterion, the research-identity
  credentials provision, temporary-vs-formal ChinaXivID, and the non-withdrawal policy.
- **S3** — Live HTTP probes of `chinaxiv.org` and `global.chinaxiv.org` · **2026-09-01**. The §8
  access table and negative controls. UA ladder per `AGENTS.md`: default curl → Chrome 131 →
  WhatsApp/2.23.20.0 → ChatGPT-User/1.0 → ClaudeBot/1.0. Probe script and raw results in
  `doc/hardware/scratch/preprint-repositories/regional/`.

### Retrieval / crawler note

**chinaxiv.org — default curl UA works for site pages; nothing works for article pages.**
Home page and `/user/help.htm` return HTTP 200 to plain `curl` with no UA header, from outside
China, with no geoblock or interstitial. But `/abs/*` returns **HTTP 403** with the page title
**系统正在维护中** under *all five* user-agents in the standard ladder (default, Chrome 131,
WhatsApp, ChatGPT-User, ClaudeBot). Because a deliberately bogus `/abs/999999.99999` returns the
**same** 403, the status code cannot be used to test record existence. A bogus `.htm` path by
contrast returns a normal HTTP 404 (您访问的页面不存在), confirming the 403 is specific to the
`/abs/` route rather than a site-wide block. `global.chinaxiv.org` returns 200 but is a
client-rendered shell (2,027 B) and yields no content to a non-JS client.
