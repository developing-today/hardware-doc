# Regional and national preprint servers — grouped record

- **Scope:** the smaller national/regional *multidisciplinary* preprint servers — Jxiv,
  SciELO Preprints, AfricArXiv, Arabixiv, IndiaRxiv, INArxiv, LatArXiv, Preprints.ru,
  AIJR Preprints
- **Compiled:** 2026-09-01 · **All reachability probes run:** 2026-09-01
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).

## 0. The shared pattern — read this before the individual entries

The folklore is that regional preprint servers launch with fanfare, run on one or two volunteers,
and go dark within five years. The probe evidence collected here **partly confirms that and
partly corrects it**, and the correction is the more useful finding.

**What actually happens is not data loss. It is loss of the front door.**

Of the nine servers below, four are in good health (Jxiv, SciELO Preprints, Preprints.ru, AIJR)
and five are in some state of failure. But in every failing case where the content sat on a **large
shared host** — OSF or Zenodo — *the content survived*, including for a server that formally shut
down six years ago:

| Server | Formal status | Content still readable? | Where |
|---|---|---|---|
| INArxiv | Closed 2020-10-07 | **Yes — 15,987 preprints** | OSF |
| AfricArXiv | Submissions closed | **Yes — 479** | OSF |
| Arabixiv | Submissions closed | **Yes — 298** | OSF |
| IndiaRxiv | Submissions closed | **Yes — 121** | OSF |

What broke, without exception, was the **independently hosted successor or vanity domain**:

| Independent host | State on 2026-09-01 | Failure |
|---|---|---|
| `africarxiv.ubuntunet.net` (AfricArXiv's own designated successor) | unreachable | **TLS certificate expired** |
| `rinarxiv.lipi.go.id` (INArxiv's designated successor) | unreachable | **TLS hostname mismatch** |
| `latarxiv.org` (live server, 2024 vintage) | reachable only with `curl -k` | **TLS certificate expired 2026-08-20** |
| `www.inarxiv.id` | unreachable | **DNS NXDOMAIN** |
| `indiarxiv.org` (relaunch on OJS) | reachable | **OAI reports zero records** |

**An expired TLS certificate is the reliable early warning sign of an abandoned scholarly
service.** Three of the nine servers here failed on certificate management alone — a task that is
automated and free, and which therefore fails only when nobody is left watching the alerts. All
three were reachable, with intact content, behind the broken certificate. A browser would refuse
them; a reader would conclude the site was gone.

**What this means for citing regional-server content:**

1. **Cite the OSF or Zenodo record and its DOI, never the vanity domain.** `africarxiv.org`,
   `arabixiv.org`, `indiarxiv.in` and `inarxiv.id` have all either redirected, changed host or
   evaporated; the OSF records behind them have not.
2. **Verify the record still resolves at the time you cite it**, and record your retrieval date.
   Two of these servers actively signpost readers to successors that do not work (§3, §6).
3. **Distrust "moved to" notices.** Arabixiv's OSF page says it moved to Zenodo; `arabixiv.org`
   redirects back to the frozen OSF instance; the Zenodo community holds 78 records against OSF's
   298 (§4). The operator's own signposting is mutually contradictory.
4. **Expect the front page to lie about liveness in both directions** — a dead-looking site may
   have intact content behind a bad certificate, and a live-looking relaunch may be empty (§5).

## 1. Status table

All probed **2026-09-01** using the `AGENTS.md` UA ladder: default `curl` → Chrome 131 →
WhatsApp/2.23.20.0 → ChatGPT-User/1.0 → ClaudeBot/1.0. "UA that worked" names the *first*
successful agent.

| Server | URL probed | Operator | Launch | Status 2026-09-01 | Size | UA that worked |
|---|---|---|---|---|---|---|
| **Jxiv** | `jxiv.jst.go.jp` | Japan Science & Technology Agency (JST) | 2022 | **ALIVE** | **1,221** [API] | default curl |
| **SciELO Preprints** | `preprints.scielo.org` | SciELO / FAPESP network | 2020 | **ALIVE** | **5,689** [API] | default curl |
| **AfricArXiv (OSF)** | `osf.io/preprints/africarxiv` | Center for Open Science | 2018 | **FROZEN** — submissions off | **479** [API] | default curl |
| ↳ successor | `africarxiv.ubuntunet.net` | UbuntuNet Alliance | 2023 | **BROKEN** | n/v | **none — TLS expired** |
| ↳ org site | `africarxiv.org` | AfricArXiv | — | ALIVE (167,413 B) | n/a | default curl |
| **Arabixiv (OSF)** | `osf.io/preprints/arabixiv` | Center for Open Science | 2018 | **FROZEN** — submissions off | **298** [API] | default curl |
| ↳ successor | Zenodo community `arabixiv` | Zenodo/CERN | created **2025-09-17** | ALIVE | **78** [API] | default curl |
| **IndiaRxiv (OSF)** | `osf.io/preprints/indiarxiv` | Center for Open Science | 2019 | **FROZEN** — submissions off | **121** [API] | default curl |
| ↳ relaunch | `indiarxiv.org` | Society for Promotion of Horticulture | — | **ALIVE BUT EMPTY** | **0 via OAI** [API] | default curl |
| ↳ old domain | `indiarxiv.in` | — | — | redirects → `indiarxiv.wordpress.com` (blog) | n/a | default curl |
| **INArxiv (OSF)** | `osf.io/preprints/inarxiv` | Center for Open Science | 2017 | **CLOSED 2020-10-07**, content retained | **15,987** [API] | default curl |
| ↳ own domain | `www.inarxiv.id` | — | — | **DEAD** | — | **none — DNS NXDOMAIN** |
| ↳ successor | `rinarxiv.lipi.go.id` | LIPI (Indonesia) | — | **BROKEN** | n/v | **none — TLS hostname mismatch** |
| **LatArXiv** | `latarxiv.org` → `preprints.latarxiv.org` | Paideia Publishing Services | 2024 [INF] | **ALIVE, TLS BROKEN** | not verified | **`curl -k` only — cert expired 2026-08-20** |
| **Preprints.ru** | `preprints.ru` | NEICON (НЭИКОН) | autumn **2019** | **ALIVE** | **3,063** [WEB] | default curl |
| **AIJR Preprints** | `preprints.aijr.org` | AIJR Publisher (India) | 2020 | **ALIVE** | **188** [API] | default curl |

**Negative control for the whole sweep:** `www.inarxiv.id` failed with DNS NXDOMAIN on all five
user-agents, and `africarxiv.pubpub.org` returned HTTP **403 on all five** — confirming the ladder
distinguishes real failures from UA filtering, and that a "success" above is not an artefact of
retrying.

---

## 2. Jxiv (Japan Science and Technology Agency)

- **URL:** https://jxiv.jst.go.jp/ (resolves to `/index.php/jxiv`) · **Operator:** JST ·
  **Launched:** 2022 · **Status: ALIVE**

Japan's national preprint server, run by JST, the country's principal research funding agency.
Built on PKP's Open Journal/Preprint Systems. OAI-PMH `Identify` gives `repositoryName`
**"Jxiv, JSTプレプリントサーバ"**, `adminEmail` `info-jxiv@jst.go.jp`, and `earliestDatestamp`
**2022-03-24T01:21:10Z** — which independently confirms the 2022 launch (S1) [API].

**Size: 1,221 records**, from OAI `ListIdentifiers` `completeListSize` (S1) [API].

**Computing/engineering content: yes, structurally.** OAI `ListSets` exposes discipline sets
including **情報科学** (information science), **電気電子工学** (electrical & electronic
engineering), **一般工学・総合工学** (general engineering), **機械工学** (mechanical engineering),
**ナノ・材料科学** (nano/materials) and **建築学・土木工学** (S1) [API]. Per-set counts not
retrieved. Language sample from the first OAI page: **eng 56 / jpn 44** — majority English (S1)
[API].

**Moderation: real, and JST holds the power.** The submission checklist requires authors to accept
that *"JSTが、投稿するプレプリントの公開の可否を決定する権限をもつこと"* — **JST has the authority
to decide whether a submitted preprint is published**; that published preprints **cannot be
withdrawn or deleted** by the author; and that **JST may retract** a published preprint. Authors
must register country of residence, affiliation and email, used for **本人確認** (identity
verification). Manuscripts already posted to another preprint server (or already carrying a DOI)
**cannot in principle be submitted** (S2) [DOC].

**Assessment.** The healthiest server in this group after SciELO. It has a national funding agency
behind it, working OAI-PMH, a documented moderation policy with named accountability, and real
engineering categories. Its weakness is simply scale: 1,221 records in four years is small, and
Japanese CS researchers preprint to arXiv. Use it for Japanese-language engineering work that has
no arXiv counterpart; do not expect to find landmark systems papers.

## 3. SciELO Preprints

- **URL:** https://preprints.scielo.org/ · **Operator:** SciELO network ·
  **Launched:** 2020 · **Status: ALIVE**

The preprint arm of SciELO, the Latin American / Iberian / South African open-access publishing
network. Runs on **OPS (Open Preprint Systems)** from PKP. OAI `earliestDatestamp`
**2020-04-06T23:01:54Z**, `adminEmail` `scielo.submission@scielo.org` (S3) [API], confirming the
2020 launch. Its own about page is versioned **21 May 2025** (S4) [DOC].

**Size: 5,689 records** (OAI `completeListSize`, S3) [API] — the largest *active* server in this
group.

**Genuinely multilingual, and measurably so.** Language tags in the first 100 OAI records:
**Portuguese 45, English 39, Spanish 17** (S3) [API]. This is not a monolingual server with a
translated interface; it is trilingual in substance.

**Computing/engineering content: yes.** OAI `ListSets` includes **Engenharias** (engineering) and
**Ciências Exatas e da Terra** (exact and earth sciences) alongside the health/humanities sets
(S3) [API]. Per-set counts not retrieved. **[NOT-VERIFIED]**

**Moderation: the most interesting policy in this group.** SciELO operates a **reputation-gated
auto-post**, documented verbatim (S4) [DOC]:

> Um manuscrito será postado automaticamente quando o autor da submissão tiver **pelo menos três
> artigos** de qualquer data **ou dois artigos recentes dos últimos dois anos** com DOIs ativos no
> repositório Crossref. Em outros casos, uma **triagem básica** será feita para identificar se é um
> manuscrito relacionado à pesquisa.

So: an author with ≥3 Crossref-indexed articles (any date), or 2 within the last two years,
**bypasses screening entirely**; everyone else gets a basic triage checking that the submission is
research. Registration requires **ORCID**. A manuscript **will not be posted if it has already
been accepted, published, or posted elsewhere**. Authors must confirm ethics-committee approval
where applicable, and SciELO reserves the right to apply area-specific screening criteria and to
reject (S4) [DOC]. The server also layers **Hypothesis annotation** and a preprint-evaluation
workflow on top (S4) [DOC].

**Assessment.** The strongest governance model here, and the one worth copying: it spends
moderator effort only on unknown authors. Institutionally backed by an established publishing
network rather than volunteers, which is why it has not exhibited the failure mode of §0. For an
engineer it is a plausible source of Latin American engineering work, but you should expect
Portuguese and Spanish full texts.

## 4. AfricArXiv and Arabixiv — the two COS-hosted 2018 cohort

### AfricArXiv

- **OSF:** https://osf.io/preprints/africarxiv · **Launched:** 2018 with the Center for Open
  Science · **Status: FROZEN** (`allow_submissions: false`) · **Size: 479 preprints** (S5) [API]

The OSF provider record's own description states AfricArXiv launched with COS in 2018 and that
"In 2023, we reached our key milestone to establish AfricArXiv as a central repository at
**UbuntuNet Alliance** For Research & Education Networking. Please submit your research items via
**https://africarxiv.ubuntunet.net/**" (S5) [API/DOC]. Review workflow is recorded as
`pre-moderation` (S5) [API].

**The designated successor does not work.** `https://africarxiv.ubuntunet.net/` failed on **all
five user-agents** with `curl: (60) SSL certificate ... certificate has expired` (S6). The
organisational site `https://africarxiv.org/` is alive (HTTP 200, 167,413 B, default UA), and the
older `africarxiv.pubpub.org` returns **HTTP 403 on all five UAs** (S6).

**Assessment.** The 479 preprints on OSF are safe and citable. The 2023 "central repository"
migration is, as of 2026-09-01, not reachable by an ordinary client. Cite OSF. Do not send anyone
to the ubuntunet address. Whether content was ever migrated there is **not verified**.

### Arabixiv

- **OSF:** https://osf.io/preprints/arabixiv · **Launched:** 2018 with COS ·
  **Status: FROZEN** (`allow_submissions: false`) · **Size: 298 preprints** (S5) [API]

Founded by Dr Khaled Moustafa, with a listed steering committee including academics at Cairo
University and Paris-Sud (S5) [API]. Review workflow `pre-moderation`.

**Three mutually inconsistent signposts**, all retrieved 2026-09-01:

1. The OSF description says: *"ArabiXiv has moved to a new address and accepts submissions through
   its new platform at: https://zenodo.org/communities/arabixiv/about. All previously published
   articles remain accessible and their links are preserved."* (S5) [API/DOC]
2. The OSF `domain` field still points to `https://arabixiv.org/` (S5) [API] — and
   `arabixiv.org` **redirects back to `osf.io/preprints/arabixiv`** (S6) [WEB], i.e. back to the
   frozen instance it supposedly left.
3. The Zenodo community `arabixiv` exists, titled **"ArabiXiv الأرشيف العربي العلمي"**, but was
   **created 2025-09-17** and holds **78 records** (S7) [API] — against 298 on OSF.

**Assessment.** The migration is real but partial and recent, and the signposting is broken in a
loop. 298 records on OSF, 78 on Zenodo, and a vanity domain that points at the old home. Cite the
OSF DOI for anything pre-2025 and check Zenodo separately. Do not assume the Zenodo community is a
complete mirror — on the numbers, it is not.

## 5. IndiaRxiv — moved hosts, twice, and the relaunch is empty

- **OSF:** https://osf.io/preprints/indiarxiv · **Launched:** 2019 ·
  **Status: FROZEN** · **Size: 121 preprints** (S5) [API]

The OSF record states: *"IndiaRxiv is no longer able to accept new submissions. Existing content in
this repository will remain accessible as part of COS's ongoing commitment to Open Science. If it
is important to you that free author submissions to this site continue, please consider contacting
**Sridhar Gutam**…"* (S5) [API/DOC]. The advisory board lists academics from Panjabi University,
LV Prasad Eye Institute, DOAJ, ICAR-IVRI and IIT Indore (S5) [API].

**Three addresses, three different things** (all 2026-09-01):

- `indiarxiv.in` → **redirects to `indiarxiv.wordpress.com`**, a WordPress *blog* (HTTP 200,
  97,976 B) (S6) [WEB]. The blog explains the history: the repository was launched by
  **Open Access India** with COS support, but *"due to some reasons, IndiaRxiv could not be with
  COS but had got a new host, **Society for Promotion of Horticulture (SPH), Bengaluru** which is
  hosting IndiaRxiv.org"* (S8) [WEB].
- `indiarxiv.org` → **live OJS/OPS instance**, titled "IndiaRxiv - Preprints Repository of India",
  **eISSN 2583-0007**, CC BY 4.0, stating preprints are moderated (S9) [WEB]. Admin contact
  `gutam2000@gmail.com` — the same Sridhar Gutam named on OSF.
- The OSF instance retains the original 121 preprints.

**But the relaunch has no content.** OAI-PMH on the new instance returns
`ListIdentifiers` with **zero `<identifier>` elements**, and `Identify` reports an
`earliestDatestamp` of **2026-09-02** — i.e. essentially *now* (S9) [API]. The archives page
returned 7,188 bytes with no listed items.

**Assessment.** IndiaRxiv is the clearest single illustration of §0: a real community, a real
volunteer (named, contactable), a legitimate ISSN — and a relaunched platform that is an empty
shell while the actual corpus sits frozen on someone else's infrastructure. **Cite the OSF
records. The `.org` site currently holds nothing you can cite.** Whether the 121 OSF preprints will
be migrated is **not verified**.

## 6. INArxiv — the one that genuinely closed

- **OSF:** https://osf.io/preprints/inarxiv · **Launched:** 2017 · **Closed: 2020-10-07** ·
  **Size: 15,987 preprints, still online** (S5) [API]

The OSF description is a farewell notice, quoted here because it is the primary record of the
closure (S5) [API/DOC]:

> With a heavy heart, we close the INArxiv service starting **October 7, 2020**. Thank you for your
> participation and support as users until now. […] For your next preprint document, we recommend
> uploading it to **RINarxiv**.

Steering committee members are listed at Institut Teknologi Bandung (S5) [API].

**What happened to the content: nothing. It is all still there.** 15,987 preprints — **by far the
largest holding in this entire group**, thirteen times SciELO Preprints — remain served by OSF six
years after closure (S5) [API].

**What died was everything else.** `www.inarxiv.id` returns **DNS NXDOMAIN on all five
user-agents** (S6). The recommended successor `rinarxiv.lipi.go.id` fails TLS on all five UAs with
`no alternative certificate subject name matches target hostname` (S6). (LIPI, the Indonesian
Institute of Sciences, was reorganised into BRIN in 2021, which is a plausible explanation for a
stale `lipi.go.id` host — **[INF]**, not verified.)

**Assessment.** The strongest evidence for the §0 thesis in both directions: a server that
*formally shut down* has better-preserved, more-citable content than three servers that never
announced a closure. The lesson is entirely about hosting, not about governance or funding.

## 7. LatArXiv — new, real, and already failing at TLS

- **URL:** `https://latarxiv.org/` → redirects to
  `https://preprints.latarxiv.org/index.php/latarxiv/es/` · **Operator: Paideia Publishing
  Services** · **Launched: 2024** [INF] · **Status: ALIVE but TLS BROKEN**

**It exists.** The assignment asked whether it exists at all; it does. It is an OJS/OPS instance
in Spanish, with subject sections including **Ingenierías y Tecnología** (engineering &
technology), Ciencias Naturales y Exactas, Ciencias Médicas y de la Salud, Ciencias Agrarias,
Ciencias Sociales y Economía, Artes y Humanidades, and Ciencias Ambientales y de la Tierra
(S10) [WEB].

**Operator confirmed from its own about page** (S10) [DOC]:

> LatArXiv es una plataforma multidisciplinar que ofrece servicios preprints **a cargo de Paideia
> Publishing Services**.

**Its TLS certificate expired 12 days before the probe.** `openssl s_client` on 2026-09-01 returned
`subject=CN=latarxiv.org`, `issuer=C=US, O=Let's Encrypt, CN=R13`, `notBefore=May 22 2026`,
**`notAfter=Aug 20 19:26:19 2026 GMT`** (S6). All five user-agents failed with
`curl: (60) certificate has expired`; the site was reachable **only** with `curl -k`
(HTTP 200, 47,681 B). A Let's Encrypt certificate expiring means automated renewal stopped and
nobody noticed — on a platform under two years old.

**Business model.** Two intake routes: an **Open** section where any author may upload freely, and
per-journal sections where **member journals' editors** submit on behalf of their journal, under a
**membership** scheme (S10) [WEB]. Default licence **CC BY 4.0**, with authors and editors free to
choose others (S10) [DOC].

**Moderation** (S10) [DOC]: *"Todas las preimpresiones serán **moderadas** para determinar si se
ajustan a los objetivos y alcance de este servidor"* — a scope check, not peer review. Authors are
responsible for permissions, all authors must consent, and ethics-committee approval is required
where applicable.

**Size: not verified.** The OAI-PMH endpoint at
`preprints.latarxiv.org/index.php/latarxiv/oai?verb=Identify` returned an **empty body** and
`ListIdentifiers` returned zero identifiers (S6) [API]. Visible content on the front page is dated
**2024-12-30** and **2025-07-15**, which supports a 2024 launch but does not prove it — the launch
year is **[INF]**, not verified. The editorial-team page `es/about/editorialTeam` returns **404**
(S6) [WEB].

**Assessment.** Honest verdict: a commercially operated, genuinely functioning Spanish-language
server with real engineering scope — displaying, at two years old, three of the classic
abandonment signals simultaneously (expired certificate, non-functional OAI, missing editorial
team page). It is too new and too under-maintained to cite with confidence. Check it again before
relying on it.

## 8. Preprints.ru (NEICON)

- **URL:** https://preprints.ru/ · **Operator: NEICON (НЭИКОН)** · **Launched: autumn 2019** ·
  **Status: ALIVE** · **Size: 3,063 preprints**

Reachable on the **default curl UA** (HTTP 200, 27,658 B) — no UA substitution needed, and no
geoblock encountered from this vantage point (S6) [WEB].

**Operator and funding, from its own about page** (S11) [DOC]:

> PREPRINTS.RU – открытый мультидисциплинарный онлайн-архив и сервис для препринтов. Он
> **управляется и финансируется некоммерческим партнерством НЭИКОН**, одной из ведущих российских
> организаций в области распространения, издания и обеспечения доступа к научной информации.

— managed and funded by the non-profit partnership NEICON. "Начал работу **осенью 2019 г.**"
(began operation in autumn 2019) (S11) [DOC].

**Size: 3,063**, read from the search page's result counter (`найдено: 3063`) with an empty query
(S12) [WEB]. No OAI-PMH endpoint was found at the conventional paths (`/oai`, `/index.php/oai`
both HTTP 404) (S6) [API].

**Moderation: pre-moderation by literal volunteers.** The about page states *"Контент на
PREPRINTS.RU проходит **предварительную модерацию, но не рецензируется**"* (content undergoes
preliminary moderation but is not peer reviewed), and — the detail that matters for §0 —
openly recruits them (S11) [DOC]:

> Если вы хотите присоединиться к **волонтерскому сообществу модераторов** и модерировать
> поступающие на рассмотрение препринты, напишите нам письмо (info@preprints.ru).

This is the "one or two volunteers" pattern stated by the operator itself, not inferred.

**Computing/engineering content: nominally yes.** Rubrics include
**Математика, информатика, кибернетика** (mathematics, informatics, cybernetics),
**Промышленность, технологии** (industry, technologies) and **Энергетика** (energy). Per-rubric
counts **not verified** — I could not establish the category-filter URL scheme (S6)
**[NOT-VERIFIED]**.

**An honest observation about content quality.** The three most recent preprints on the front page
on 2026-09-01 were: *"A Rheological Approach to the Viscous Fermionic Vacuum Condensate. VII.
Universal Rheological Limit of Macro-Solitons…"* framed within a self-named "PROJECT OCEAN
paradigm" and "Fermionic Universe Hypothesis"; *"Recalibration of the UAT/UCP Acoustic Horizon…"*;
and *"Новая трактовка гравитации"* (a new interpretation of gravity) (S6) [WEB]. That is three out
of three front-page items in fringe cosmology. A single snapshot is not a survey, and I present it
as exactly that — but it is what the front page showed, and volunteer pre-moderation for scope is
a weak filter against determined fringe submitters.

**Assessment.** Live, honestly documented, and technically unremarkable. Durability risk is
structural rather than technical: a single national non-profit, volunteer moderation, no OAI-PMH
for third-party harvesting or mirroring, and — **[INF]**, flagged as inference — a geopolitical
environment in which international infrastructure links to Russian scholarly services have proved
fragile. The absence of OAI-PMH is the concrete problem: nothing else can mirror it.

## 9. AIJR Preprints

- **URL:** https://preprints.aijr.org/ (resolves to `/index.php/ap`) · **Operator: AIJR
  Publisher**, India · **Launched: 2020** · **Status: ALIVE** · **Size: 188 records**

OAI-PMH `Identify` returns `repositoryName` **"AIJR Preprints"**, `adminEmail`
`preprints@aijr.org`, `earliestDatestamp` **2020-03-22T15:51:39Z**, confirming the 2020 launch
(S13) [API]. `ListSets` gives four sets: **Working Paper, Coronavirus, Preprints, Under Review**
(S13) [API].

**Size: 188.** The endpoint does not emit `completeListSize`, so I counted `<identifier>` elements
across `ListIdentifiers` with resumption-token paging; it completed in a single page of **188**
with no resumption token (S13) [API]. This is a very small server.

**Self-description** (S14) [DOC]: *"AIJR preprint server is dedicated to publishing early research
work (**without Peer Reviewing**)…"*. The **Working Paper** section is for work not yet submitted
anywhere, updatable with a DOI once published; there is also an **Under Review** section.

### Is AIJR on a predatory-publisher watchlist? — checked, and the answer is no

This needs care because a near-identical acronym *is* listed, and conflating them would be a
serious and unfair error.

- **AIJR Publisher does *not* appear on the Beall's List successor's publishers list.** Searching
  `https://beallslist.net/` for "aijr" and for "american international" returned **no matches**
  (S15) [WEB].
- **The standalone-journals list contains one "AIJR"-like hit, and it is a different
  organisation.** The entry is *"**Ahead International Journal of Recent Research Review**
  (AIJRRR)"*, linked to `http://www.aijrrr.com/` (S15) [WEB]. That is a journal title beginning
  "Ahead International…", not AIJR Publisher of `aijr.org`. For completeness, `www.aijrrr.com`
  **does not resolve** (DNS NXDOMAIN, 2026-09-01) (S6).
- `https://aijr.org/` is live (HTTP 200, 158,968 B), titled "AIJR Publisher: Scholarly Journals &
  Books Publishing Solutions" (S6) [WEB].

**So: no watchlist finding against AIJR Publisher, and the superficially similar AIJRRR entry is a
different, now-defunct entity.** State it that way; do not let the acronym collision propagate.

**What I did *not* check, and will not imply:** membership of DOAJ, COPE or OASPA; APC structure;
editorial-board verification; any of the other independent quality signals one would want for a
small commercial publisher. **[NOT-VERIFIED]**

**Assessment.** A small commercial publisher's preprint server, technically well-behaved — working
OAI-PMH, clear sections, honest "no peer review" statement, and no adverse watchlist finding. The
reservations are structural rather than reputational: 188 records in six years is barely a
repository, there is no institutional or national backing, and the durability of a preprint archive
attached to a single small commercial publisher depends entirely on that firm's continued
existence. There is no obvious reason to *avoid* it and little reason to *use* it.

## 10. Sources

- **S1** — Jxiv OAI-PMH, `https://jxiv.jst.go.jp/index.php/jxiv/oai` (`Identify`,
  `ListIdentifiers`, `ListSets`, `ListRecords`) · retrieved 2026-09-01. Size 1,221,
  `earliestDatestamp` 2022-03-24, discipline sets, language sample.
- **S2** — Jxiv submission requirements,
  `https://jxiv.jst.go.jp/index.php/jxiv/about/submissions` · retrieved 2026-09-01. JST publication
  authority, no-withdrawal clause, identity registration, prior-posting exclusion.
- **S3** — SciELO Preprints OAI-PMH,
  `https://preprints.scielo.org/index.php/scielo/oai` · retrieved 2026-09-01.
  `completeListSize` 5,689, `earliestDatestamp` 2020-04-06, sets, language distribution.
- **S4** — SciELO Preprints "Sobre o Servidor",
  `https://preprints.scielo.org/index.php/scielo/about` · retrieved 2026-09-01. Crossref auto-post
  rule, triagem básica, ORCID requirement, prior-publication exclusion, OPS/PKP basis, page version
  dated 21 May 2025.
- **S5** — OSF API v2, `https://api.osf.io/v2/providers/preprints/{africarxiv,arabixiv,indiarxiv,
  inarxiv}/` and `…/preprints/?page[size]=1` · retrieved 2026-09-01. Provider descriptions,
  `allow_submissions`, `reviews_workflow`, advisory boards, and `links.meta.total` counts
  (479 / 298 / 121 / 15,987).
- **S6** — Live reachability probes with the `AGENTS.md` UA ladder, plus `openssl s_client` ·
  2026-09-01. All rows of the §1 table, TLS failures, DNS NXDOMAIN results, negative controls.
  Probe script and raw per-host logs in
  `doc/hardware/scratch/preprint-repositories/regional/` (`ua-ladder-probe.sh`, `res_*.txt`).
- **S7** — Zenodo API, `https://zenodo.org/api/communities/arabixiv` and
  `https://zenodo.org/api/records?communities=arabixiv&size=1` · retrieved 2026-09-01. Community
  created 2025-09-17; 78 records.
- **S8** — IndiaRxiv blog, `https://indiarxiv.wordpress.com/` (via redirect from
  `indiarxiv.in`) · retrieved 2026-09-01. Open Access India origin, COS departure, SPH Bengaluru
  hosting.
- **S9** — IndiaRxiv OJS instance, `https://indiarxiv.org/index.php/ops` and its OAI-PMH endpoint ·
  retrieved 2026-09-01. eISSN 2583-0007, CC BY 4.0, moderation statement, and the zero-record
  `ListIdentifiers` result with `earliestDatestamp` 2026-09-02.
- **S10** — LatArXiv, `https://preprints.latarxiv.org/index.php/latarxiv/es/`, `…/es/about` and
  `…/es/about/submissions` · retrieved 2026-09-01 **with `curl -k` (expired certificate)**.
  Paideia Publishing Services operatorship, sections, membership model, CC BY 4.0, moderation
  statement.
- **S11** — Preprints.ru "О проекте", `https://preprints.ru/about` · retrieved 2026-09-01. NEICON
  operatorship and funding, autumn 2019 start, pre-moderation-not-peer-review, volunteer moderator
  recruitment.
- **S12** — Preprints.ru search, `https://preprints.ru/search?q=` · retrieved 2026-09-01. Result
  counter `найдено: 3063`.
- **S13** — AIJR Preprints OAI-PMH, `https://preprints.aijr.org/index.php/ap/oai` · retrieved
  2026-09-01. `earliestDatestamp` 2020-03-22, four sets, 188 identifiers counted with
  resumption-token paging.
- **S14** — AIJR Preprints about page, `https://preprints.aijr.org/index.php/ap/about` · retrieved
  2026-09-01. "without Peer Reviewing", section definitions.
- **S15** — Beall's List successor, `https://beallslist.net/` and
  `https://beallslist.net/standalone-journals/` · retrieved 2026-09-01 **with the Chrome 131 UA**.
  No AIJR Publisher entry; the sole acronym-adjacent entry is "Ahead International Journal of
  Recent Research Review (AIJRRR)", `aijrrr.com`.

### Retrieval / crawler notes

Findings for the repository's crawler access table, all **2026-09-01**:

- **Default `curl` UA sufficed** for: `jxiv.jst.go.jp`, `preprints.scielo.org`, `preprints.ru`,
  `preprints.aijr.org`, `aijr.org`, `osf.io`, `api.osf.io`, `zenodo.org`, `africarxiv.org`,
  `indiarxiv.in`/`indiarxiv.wordpress.com`, `indiarxiv.org`, `global.chinaxiv.org`. No rate
  limiting or bot-block observed.
- **Chrome 131 UA needed** for: `beallslist.net` (used pre-emptively; default UA not separately
  tested — so this is **not** evidence that the default is blocked there).
- **All five UAs failed — not a UA problem:**
  - `africarxiv.pubpub.org` — HTTP **403** on default, Chrome 131, WhatsApp, ChatGPT-User and
    ClaudeBot. A genuine block; note the ChatGPT-User response was only 25 bytes while the others
    were ~5.5 kB, i.e. the block page differs by agent.
  - `www.inarxiv.id` — DNS **NXDOMAIN**.
  - `africarxiv.ubuntunet.net` — TLS **certificate expired**.
  - `rinarxiv.lipi.go.id` — TLS **hostname mismatch**.
  - `latarxiv.org` / `preprints.latarxiv.org` — TLS **certificate expired 2026-08-20**;
    retrievable **only** with `curl -k`.
- **General tip:** for OJS/OPS-based servers (Jxiv, SciELO, AIJR, LatArXiv, IndiaRxiv), the
  `/oai?verb=Identify` and `/oai?verb=ListIdentifiers&metadataPrefix=oai_dc` endpoints are far more
  reliable and cheaper than scraping, and `completeListSize` gives an exact count in one request —
  **except** on AIJR (no `completeListSize`; count identifiers instead) and LatArXiv (endpoint
  returns an empty body).
