# Bulk libraries and shadow archives — what they are, and why this repository does not cite them

- **Compiled:** 2026-09-02. Every figure carries a source and a date.
- **Evidence labels:** [API] [WEB] [DOC] [LIT] [COM] [INF] [NOT-VERIFIED] — see the
  [index](README.md#evidence-and-method).
- **Method statement, up front and non-negotiable:** **no shadow-library service was accessed in
  producing this record.** Everything in §§3–6 comes from Wikipedia's referenced articles,
  Crossref-verified scholarly literature, court reporting, and the operators' own statements as
  relayed by third parties. Operator figures are labelled as *claims*, never as measurements. Raw
  probe log:
  [`../../scratch/preprint-repositories/bulk-archives/probe-log-2026-09-02.txt`](../../scratch/preprint-repositories/bulk-archives/probe-log-2026-09-02.txt).
- **This record contains no mirror domains, no proxy hosts, no onion addresses and no instructions
  for reaching a blocked service.** Those rotate too fast to capture, are the operational-
  circumvention part, and would make this document wrong within a month. Services are named and
  historicised only. That is a deliberate editorial decision, stated so nobody reads it as an
  oversight.

---

## 1. Read this first: the lawful copy almost certainly exists

**For the overwhelming majority of the technical literature this knowledge base cares about there is
a free, lawful, publisher- or funder-sanctioned copy, and the ladder in
[`open-access-full-text-sources.md`](open-access-full-text-sources.md) finds it.** That is not a
platitude — it is a property of this specific field, which is unusually well served by open access:

| Body of work | Where the lawful free copy is | Record |
|---|---|---|
| Operating systems, storage, networking, systems security | **USENIX** — OSDI, NSDI, ATC, FAST, USENIX Security. *All of it, all years, free by policy*, including full-proceedings PDFs | [`open-access-full-text-sources.md` §3.1](open-access-full-text-sources.md) |
| Cryptography, side-channel and embedded security | **IACR Cryptology ePrint** (27,552 reports) and TCHES — diamond OA | [`cryptology-eprint-archive.md`](cryptology-eprint-archive.md) |
| Almost anything in CS or EE with an arXiv ID | **arXiv** — 3,152,666 submissions, `cs` alone 931,100 | [`arxiv.md`](arxiv.md) |
| Computational linguistics / NLP | **ACL Anthology** — the entire proceedings corpus, free | [`open-access-full-text-sources.md`](open-access-full-text-sources.md) |
| IEEE-published work | The author's copy on **TechRxiv**, found via Crossref's `is-preprint-of` relation | [`techrxiv.md`](techrxiv.md) |
| Aerospace, energy, national-lab engineering | **NTRS**, **OSTI**, agency technical-report servers | [`government-and-institutional-technical-reports.md`](government-and-institutional-technical-reports.md) |
| Protocol specifications | **RFC Editor** — entirely free, always has been | [`open-access-full-text-sources.md` §5](open-access-full-text-sources.md) |
| Life-science and bioinformatics software papers | **PMC / Europe PMC** | [`open-access-full-text-sources.md` §3.5](open-access-full-text-sources.md) |
| Historical vendor manuals, data books, corporate tech reports | **bitsavers**, **archive.org**, **Arquivo.pt**, the Wayback Machine | [`recovering-dead-technical-sites.md`](recovering-dead-technical-sites.md) |

The companion record's own summary is that **rungs 1–3 of its ladder (Unpaywall → Semantic Scholar
`externalIds.ArXiv` → OpenAlex `locations[]`) resolve the large majority of computing and
electronics citations**, and rung 4 — "is it a USENIX paper?" — resolves much of the remainder.
Rung 9, *email the author*, is slow, legitimate, and works. **Shadow libraries are a last resort,
not a first one, and this file is not a shortcut around the ladder.** They are documented here
because they are the largest bodies of technical text in existence and therefore constantly
discussed, because they sit at the centre of current AI-training litigation, and because an engineer
handed a PDF of unknown provenance needs a way to judge it (§7).

---

## 2. Definitions, and the distinction that runs through this whole file

**"Shadow library"** — also *pirate library*, also *black open access* — is the term used in the
scholarly literature for an online repository of works that are normally paywalled or otherwise
access-controlled [COM] (S2). The category is old; what changed in the 2010s was scale. The single
most useful distinction, and one that maps closely onto the legal line:

| | Indexing **metadata** | Redistributing **full text** |
|---|---|---|
| What it is | Titles, authors, DOIs, ISBNs, checksums — "this work exists, and a file of it is N bytes" | The bytes of the copyrighted work |
| Legal status | **Generally lawful.** Facts are not copyrightable in most jurisdictions, and bibliographic databases are routinely published openly | **The contested part.** This is what the injunctions and judgments are about |
| Examples | Crossref public data file, OpenAlex snapshot, dblp, Open Library dumps, `awesome-*` link lists, arXiv OAI-PMH | Sci-Hub, LibGen, Z-Library file corpora |
| Useful to this repository? | **Yes, heavily** — see §8 | Only as an object of study |

Keep that line in view: several things below sit on the lawful side of it and are used in mainstream
research, several do not — and §5.4 shows the line is not absolute, because *how* metadata was
acquired can itself be unlawful.

---

## 3. Sci-Hub

### 3.1 What it is, and the one fact that matters most

Founded in **Kazakhstan by Alexandra Elbakyan in 2011** in response to paywall pricing. Unlike
Library Genesis it deals in **papers, not books**. It worked by using institutional credentials to
fetch articles on demand and caching what it fetched; until the end of 2014 it used LibGen as its
storage back end [COM] (S1).

**The operationally decisive fact: Sci-Hub has been effectively frozen since December 2020.**

Verbatim from the retrieved extract [COM] (S1): *"On 15 July 2022, Sci-Hub reported that its
collection comprised 88,343,822 files. In December 2020, the site paused uploads due to legal
troubles. Since then, the site has archived a much lower fraction of new articles."* The mechanism
was the **Delhi High Court** case (§3.3) — the court restricted uploading until 6 January 2021, and
Elbakyan *"complied with a preliminary injunction issued by an Indian court, and suspended in 2021
upload of new publications, except for some batch releases of content"*. One such batch was the
tenth-anniversary release of **over 2.3 million articles in a single day in September 2021**.

So the verified position is a **two-step freeze**: uploads paused **December 2020**; new-publication
uploads formally **suspended during 2021** under the Indian injunction, with occasional batches
since. The 88,343,822-file figure is an **operator self-report dated 2022-07-15**, not a measurement.

**Consequence for technical literature work in 2026: Sci-Hub does not have the last five years.** It
is functionally a 2011–2020 snapshot with sporadic additions, so anything published since roughly
2021 has to come from the lawful ladder regardless.

### 3.2 The coverage literature — legitimate, citable, and worth reading

Studies *about* Sci-Hub are ordinary peer-reviewed scholarship and are cited here as such. **Every
DOI below was fetched from `api.crossref.org` and its title machine-checked against the response on
2026-09-02** [API] (S7):
| Study | Identifier | What it found |
|---|---|---|
| Himmelstein, Romero, Levernier, Munro, McLaughlin, Greshake Tzovaras & Greene, **"Sci-Hub provides access to nearly all scholarly literature"**, *eLife*, 2018 | [`10.7554/eLife.32822`](https://doi.org/10.7554/eLife.32822) | The canonical coverage study. Establishes scale empirically rather than from operator claims |
| Bohannon, **"Who's downloading pirated papers? Everyone"**, *Science*, 2016 | [`10.1126/science.352.6285.508`](https://doi.org/10.1126/science.352.6285.508) | The 28-million-request download-log analysis; showed heavy use from high-income countries too |
| Greshake, **"Looking into Pandora's Box: The Content of Sci-Hub and its Usage"**, *F1000Research*, 2017 | [`10.12688/f1000research.11366.1`](https://doi.org/10.12688/f1000research.11366.1) | Content composition and usage patterns |
| Correa, Laverde-Rojas, Tejada & Marmolejo-Ramos, **"The Sci-Hub effect on papers' citations"**, *Scientometrics*, 2021 | [`10.1007/s11192-020-03806-w`](https://doi.org/10.1007/s11192-020-03806-w) | Reports a citation differential; **contested** — see below |
| Maddi & Sapinho, **"On the culture of open access: the Sci-hub paradox"**, *Scientometrics*, 2023 | [`10.1007/s11192-023-04792-5`](https://doi.org/10.1007/s11192-023-04792-5) | Finds Sci-Hub use is not confined to, nor explained by, lack of legal access |
| Walters, **"Comparing conventional and alternative mechanisms of discovering and accessing the scientific literature"**, *PNAS*, 2025 | [`10.1073/pnas.2503051122`](https://doi.org/10.1073/pnas.2503051122) | A recent mainstream-venue comparison of discovery and access routes |

**Two caveats, stated rather than glossed.** The **citation-advantage** result (Correa et al.) is
disputed — *"the study's methods and conclusions were disputed by Phil Davis in a Scholarly Kitchen
article"* [COM] (S1); report it as contested, not established. And the often-quoted coverage
percentages (85% of paywalled-journal articles as of March 2017; ~96% of requests successful) come
from that 2017–2018 window [COM] (S1) — **given the freeze they are historical figures and must never
be presented as current coverage.**

**A discipline note.** Four plausible-looking DOIs guessed while assembling this table resolved to
entirely unrelated papers — `10.1007/s11192-021-04068-w` is about letters to the editor in
exercise-science journals; `10.1002/leap.1205` is "ALPSP Awards 2018" [API] (S7). **A DOI that looks
right is not a citation.** This is [README rule 5](README.md#evidence-and-method) in miniature.

### 3.3 Legal status — stated without minimising

Sci-Hub distributes copyrighted works without authorisation, and has been found unlawful repeatedly:

| Case | Court | Outcome |
|---|---|---|
| **Elsevier et al. v. Sci-Hub et al.** (filed 2015; LibGen a co-defendant) | S.D.N.Y. | **June 2017: default judgment, US$15 million**, plus an injunction that cost the original `.org` domain [COM] |
| **ACS v. Sci-Hub** (filed June 2017) | E.D. Va. | **6 November 2017: default judgment, US$4.8 million**, plus a permanent injunction binding *"any Internet search engines, web hosting and Internet service providers, domain name registrars, and domain name registries"*. Four domains went inactive and its Cloudflare account was terminated within weeks [COM] |
| **Elsevier, Wiley & ACS v. Sci-Hub and LibGen** (filed December 2020) | **Delhi High Court** | Sought a *dynamic* injunction — future domains/IPs covered without returning to court. Uploads restricted from the outset; Elbakyan complied and froze new uploads (§3.1). Her defence rested on India's fair-dealing exception. **19 August 2025: the Delhi High Court banned Sci-Hub and Library Genesis** [COM] |

Both US judgments were **defaults** — Sci-Hub did not appear — which is legally significant: they
establish liability of record but were not adversarially tested on the merits. That nuance does not
make the conduct lawful.

Beyond the courts: in **February 2021** Elsevier and Springer Nature obtained a UK blocking
injunction against an ISP, and in **March 2021 the City of London Police's Intellectual Property
Crime Unit warned universities and students** that the site *"could steal credentials"* and that
users could *"inadvertently download potentially dangerous content"* [COM] (S1). Institutions
routinely block it, and **access may itself be unlawful where the reader is.** In 2025 Elbakyan
launched **Sci-Net**, described as a social network for requesting and uploading papers [COM] (S1);
its legal position is **[NOT-VERIFIED]** here.

---

## 4. Library Genesis

### 4.1 History, forks and splits

LibGen's lineage is Russian: Soviet-era **samizdat** hand-copying culture, which moved onto RuNet in
the 1990s as uncoordinated collections and was consolidated into a single system **around 2008**. It
absorbed the contents of **library.nu** after that site was closed by legal action in 2012, and had
**1.2 million records by 2014** [COM] (S3). It describes itself as a *"links aggregator"* of items
*"collected from publicly available public Internet resources"* plus user uploads — a
characterisation no court has accepted.

In **2020 the project forked** over internal conflict, producing a separate domain whose database
was maintained independently; *"as a consequence, the works available differed"* between the two
[COM] (S3). That fork's domain had been seized by 2025. By **August 2024** the main project
*"appeared to no longer be actively managed"* and its lead programmer was reported *"inactive"*
[COM] (S3).

**So "LibGen" is not one thing.** It is a family of divergent databases of uncertain currency, under
uncertain maintenance, reachable through domains that change under legal pressure. A file "from
LibGen" carries no information about which database, which fork, or which era produced it — which is
the root of the reliability problem in §7.

### 4.2 What the collections actually contain

This is the part people get wrong. LibGen is **overwhelmingly a book library**, and the composition
matters if you are hunting a technical paper. Self-reported as of **4 February 2024** [COM] (S3):

| Category | Claimed count |
|---|---|
| Science journal articles | **80 million** |
| Non-fiction books | 2.4 million |
| Fiction books | 2.2 million |
| **Comics files** | **2 million** |
| Magazine issues | 0.4 million |

Note what is *not* there: **standards**. IEEE, JEDEC, IEC and ISO documents are not a LibGen
strength — and for standards the lawful picture is far better than most engineers assume. IETF,
RISC-V International and USB-IF publish free; JEDEC is free behind registration; only IEEE SA is
mostly paid ([`government-and-institutional-technical-reports.md` §5](government-and-institutional-technical-reports.md)).

### 4.3 Legal status

- **Elsevier v. LibGen** (S.D.N.Y., filed 3 June 2015): October 2015 shutdown order for the then-main
  domain [COM].
- **Pearson Education, McGraw Hill, Macmillan and Cengage v. LibGen** (S.D.N.Y., filed 14 September
  2023): **26 September 2024, US$30 million judgment**; in December 2024 the publishers seized the
  then-primary domain and took most others offline [COM] (S3).
- **Germany, December 2024:** the **CUII** (*Clearingstelle Urheberrecht im Internet*, a
  rightsholder/ISP body) instituted a **country-wide ISP block without court authorisation** — the
  Federal Network Agency was consulted only on net-neutrality compliance [COM] (S3).
- Blocked by ISPs in the UK, France, Germany, Greece, Italy, Belgium, the Netherlands and Russia;
  registered in **both Russia and the Netherlands**, part of why jurisdiction has been so contested;
  and **banned alongside Sci-Hub by the Delhi High Court on 19 August 2025** [COM] (S1, S3).

### 4.4 AI-training litigation — why this is now front-page law

LibGen is the corpus at the centre of the generative-AI copyright cases. **Anthropic:** court
documents unsealed June 2025 indicated LibGen material was used in training, and in **September 2025
Anthropic settled for US$1.5 billion** over knowingly using pirated sources, reportedly including
**at least 5 million books** from LibGen (*Bartz, Graeber & Johnson v. Anthropic*) [COM] (S3).
**Meta:** documents unsealed March 2025 in *Kadrey, Silverman & Golden v. Meta* indicated LibGen use,
and separately that Meta downloaded **over 81 terabytes** through Anna's Archive torrents; in **June
2025 the court partially ruled for Meta**, finding the training *"highly transformative"* and
therefore fair use — while Judge Vince Chhabria expressly said the ruling *"did not mean that Meta's
actions were in fact legitimate"* and identified **"market dilution"** as the strong argument the
plaintiffs had failed to develop [COM] (S4).

**Do not read the Meta ruling as a general licence.** One district judge, on one record, on
arguments the plaintiffs conceded — decided the same year another AI company paid US$1.5 billion over
the same corpus. This record draws **no legal conclusion** from the two beyond the obvious one: the
law here is unsettled and moving.

---

## 5. Anna's Archive

### 5.1 What it is

A **search and aggregation layer**, not primarily a host. Launched by a pseudonymous operator
("Anna") days after the November 2022 Z-Library enforcement action, out of the **Pirate Library
Mirror (PiLiMi)** project — which had completed a full copy of Z-Library in September 2022 and which
openly stated it *"deliberately violated the copyright law in most countries"* [COM] (S4). Its source
libraries are LibGen, Sci-Hub, Z-Library, the Internet Archive, DuXiu, MagzDB, Nexus/STC and
HathiTrust; Open Library, WorldCat and Google Books are listed as **metadata-only** sources; its own
source code is dedicated to the public domain under **CC0** [COM] (S4).

**Self-reported scale as of 20 August 2026: 71,400,751 books and 157,010,964 papers, with a unified
torrent list of roughly 1.1 petabytes** [COM] (S4). **These are the operator's claims, reported as
claims.** No independent verification exists in this record, and by policy this pass did not attempt
one.

### 5.2 Its own framing, reported as framing

The operator describes the project as **preservation**: the stated objectives are *"to catalog all
the books in existence"* and *"track humanity's progress toward making all these books easily
available in digital form"*, and it calls itself *"the largest truly open library in human history"*
[COM] (S4). Anna has defended the position on ethical grounds — *"we believe that preserving and
hosting these files is morally right"* — has argued that Western countries should create **legal
carveouts for text and data mining** to stay competitive in AI, and cites Aaron Swartz as an
influence [COM] (S4). Its legal-liability theory is that it hosts nothing and merely indexes
metadata and links to third-party downloads. **That theory has not survived contact with any court
that has examined it** — §5.3.

A commercial dimension sits awkwardly beside the preservation framing, and both belong in the record:
it **sells bulk SFTP access to LLM trainers** for money or data, and said it had provided such access
to about **30 companies (primarily Chinese) as of January 2025**, including data brokers; DeepSeek's
VL model was reported as partly trained on its ebook data [COM] (S4).

### 5.3 Legal status

| Action | Court / body | Outcome |
|---|---|---|
| **OCLC v. Anna's Archive** — over a scrape of **WorldCat**, the world's largest bibliographic database | S.D. Ohio (filed January 2024) | Damages demand dropped November 2025; **January 2026: default judgment (Judge Michael H. Watson)**, ordering deletion of the WorldCat data and barring further scraping or sharing [COM] |
| **Spotify + Universal, Sony, Warner v. Anna's Archive** — after a reported ~300 TB Spotify scrape publishing 256 million metadata rows | S.D.N.Y. (filed December 2025, under seal) | TRO January 2026; **preliminary injunction 16 January 2026 (Judge Jed Rakoff)** reaching domain registries, hosts and Cloudflare, with several domains suspended; **default judgment 15 April 2026: US$322 million** plus a permanent injunction directed at service providers [COM] |
| **13 publishers v. Anna's Archive** | S.D.N.Y. (filed March 2026) | **19 May 2026: default judgment, US$19.5 million**, plus an order for a **global domain takedown** [COM] |
| ISP blocking | Rotterdam District Court, March 2024 (dynamic order, via BREIN); **UK High Court, December 2024** under s.97A CDPA; **Germany, October 2025** via CUII | The UK Publishers Association said it had identified **over one million records** of copyrighted books and journal articles on the site's domains [COM] |

Note the pattern across §§3–6: these are almost all **default judgments**. The operators do not
appear. Liability is established of record; the merits are largely untested.

### 5.4 The genuinely useful part: the metadata releases — and their limit

Anna's Archive publishes **openly downloadable metadata datasets and torrent lists**, standardised
since August 2023 in a format it calls **AAC (Anna's Archive Containers)**: line-delimited JSON
compressed with **Zstandard**, with optional binary payloads alongside, designed for incremental
release over torrents and ingestion into a MariaDB/Elasticsearch/Python stack [COM] (S4).
**Metadata about books — titles, authors, ISBNs, editions, file checksums — is not the copyrighted
work**, and corpora of it are used in ordinary bibliometric and preservation research. Measured
2026-09-02: **OpenAlex indexes 56 works matching `"Anna's Archive"`** [API] (S8), including Walters,
*PNAS* 2025, [`10.1073/pnas.2503051122`](https://doi.org/10.1073/pnas.2503051122) — a comparison of
conventional and alternative discovery/access mechanisms in a top-tier venue — and a 2026 figshare
dataset, [`10.6084/m9.figshare.32454042`](https://doi.org/10.6084/m9.figshare.32454042), comparing a
university library's course-textbook holdings against availability on the site: a
*collection-development* study, exactly the kind of legitimate work metadata enables.

**However**, and this is why the WorldCat judgment matters: some of those datasets were **obtained by
scraping a third party's proprietary database**, and a US federal court has ordered them deleted
(§5.3). *"It is only metadata"* is a sound general principle and a poor blanket defence — lawfulness
turns on **how the metadata was acquired**, not only on what it contains. §8.1 lists metadata corpora
whose provenance is not in question, and they are the ones to use.

---

## 6. Z-Library

Began life as a **mirror of Library Genesis** and grew far beyond it. Self-reported February 2023:
**over 13.35 million books and over 84.8 million articles**, a database **over 220 TB** [COM] (S5).
It never opened its full database publicly; the copy that circulates was taken by PiLiMi in 2022
(§5.1).

**The 2022 US enforcement action.** On **3 November 2022** the US Department of Justice and FBI
seized **over 240 domain names** under court order, and two Russian nationals — **Anton Napolsky**
and **Valeriia Ermakova** — were arrested in **Argentina**. The **E.D.N.Y. indictment was unsealed
on 16 November 2022**, charging **criminal copyright infringement, wire fraud and money laundering**
for conduct alleged between 2018 and 2022; the FBI identified the operators using search warrants
served on Google and Amazon among others. **The pair escaped house arrest in July 2024**; an
Interpol notice was issued and their whereabouts are unknown [COM] (S5). This is the point at which
the category stops being a civil-litigation story: **criminal charges, not just damages awards.**

Further seizure rounds followed in May 2023, November 2023 (US and Austria), January 2024 and May
2024. France's *Tribunal Judiciaire de Paris* ordered ISP blocks against 209 domains in September
2022 and 98 more in September 2024; India blocked it in August 2022 via the Tis Hazari district
court [COM] (S5).

**The malware and phishing risk is documented, not hypothetical.** From the retrieved article:
*"Some phishing scams have attempted to impersonate Z-Library by using similar domain names and an
identical visual design in order to extract login credentials and ask for donations. In June 2024,
the news outlet Cybernews reported the discovery of a leaked database containing the personal data
of nearly 10 million users, which had been collected by the scam clone site […]"* [COM] (S5) — the
clone's domain is named in the source and is deliberately elided here, per the policy in the header.

**That is the concrete reason this file lists no domains.** When a service is under a global
domain-takedown order, *every* plausible-looking domain is a coin flip, and the documented downside
is a credential-harvesting clone holding ten million user records. Combine that with the City of
London Police's credential-theft warning about Sci-Hub (§3.3) and the pattern is consistent across
the whole category: **the imitation sites are a bigger practical hazard to the reader than the
originals ever were.**

---

## 7. Reliability — the section that actually matters here

Everything above is context. **This is the operative part**, and it applies to *any* unprovenanced
bulk source, lawful or not.

### 7.1 What a PDF from an unprovenanced bulk library does not tell you

You have a file with a plausible title page. From the file alone you cannot establish:

| You cannot verify | Why it bites |
|---|---|
| **That it is the version of record** | Preprint, accepted manuscript and published version differ. [`open-access-full-text-sources.md` §5](open-access-full-text-sources.md) makes the point precisely: an accepted manuscript is scientifically equivalent to the VoR but **its page and line numbers are not.** Quote a page number from the wrong version and the citation is wrong |
| **Which edition or printing** | These collections hold multiple editions of the same textbook under the same title with no reliable edition field. For a standard, an errata-corrected reprint or a datasheet revision, this is the difference between a working design and a dead board |
| **That the scan is complete** | Silently truncated scans, missing appendices and missing plate sections are a known failure mode of bulk-uploaded material. Nothing in the file announces the omission |
| **That it is unaltered** | No checksum against a publisher master, no signature, no chain of custody |
| **That the metadata is right** | Bulk collections inherit metadata from whatever scraped them. Not speculative: **archive.org's own catalogue** — a *lawful, curated* collection — lists a Tektronix oscilloscope manual as *"Tektronix Fish Finder 465 AND DM44 User Guide"* and a TAS455/465 as *"Tektronix Hunting Equipment"* [API], measured 2026-09-02. If a curated archive does that, an unprovenanced one does worse |
| **That the OCR is usable** | Also measured: the OCR layer of that same real Tektronix manual degrades to `r'\|'“ , p ■ '"I E. : . J" 51` within a page. See [`recovering-dead-technical-sites.md` §3.3](recovering-dead-technical-sites.md) |

Note that none of these failure modes is a *legal* objection. They apply just as much to a PDF found
on a dead lab web page or in a forum attachment. **Provenance, not legality, is what makes a
document citable.**

### 7.2 The rule

> **Never cite from an unprovenanced bulk library without resolving the DOI and confirming the
> bibliographic record against Crossref, DataCite or dblp. For anything load-bearing — a design
> decision, a specification, a number that goes into this repository — obtain the publisher or
> repository copy.**

This is not an extra hurdle invented for this file. It is
[`README.md § Evidence and method`](README.md#evidence-and-method) applied to full text: rule 1
(*an unsourced number is worse than no number*), rule 2 (*prefer machine-readable primary
evidence*), and rule 5 (*landmark papers must resolve*) together mean a file with no resolvable
identifier **cannot carry an evidence label at all** — the strongest thing you could honestly write
next to it is **[NOT-VERIFIED]**.

The check is three cheap API calls, all verified working on 2026-09-02 [API] (S7, S9):

```bash
# 1. Does the identifier exist, and is the title what you think it is? (DataCite for data/software)
curl -s "https://api.crossref.org/works/<DOI>" | jq -r '.message.title[0], .message."container-title"[0]'
# 2. Is there a lawful free copy?  -> open-access-full-text-sources.md rungs 1-3
curl -s "https://api.unpaywall.org/v2/<DOI>?email=you@your.org" | jq '.best_oa_location.url_for_pdf'
curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:<DOI>?fields=externalIds" | jq '.externalIds.ArXiv'
# 3. For CS, dblp is the best title -> canonical-citation resolver there is. No key needed.
curl -s "https://dblp.org/search/publ/api?q=<title>&format=json" | jq '.result.hits.hit[]?.info'
```

Worked example, 2026-09-02 [API] (S9): querying dblp for *"In Search of an Understandable Consensus
Algorithm"* returns `@total: 1` — **USENIX ATC 2014**, with `ee` pointing at usenix.org. One call
gives the canonical venue, the year, *and* the lawful full text. That is the whole argument for the
ladder in one line. **If step 1 fails, you do not have a citation — you have a file.**

### 7.3 Why this matters more for hardware than for most fields

The rest of this directory is about papers, where being one version out is embarrassing. In hardware
documentation it is expensive: **datasheet revisions change absolute maximum ratings** (the
repository's crawler table already records Espressif *withdrawing* documents for EOL parts, and a
distributor-adjacent site publishing AI-generated prose that **misstated an operating temperature by
20 °C** against the manufacturer datasheet); **a single mis-OCR'd digit is invisible and
catastrophic** — 3.3 V and 8.3 V differ by one glyph; and **bulk libraries do not carry the revision
string in their metadata**, so you cannot tell what you have without opening the cover page, at which
point you may as well have gone to the vendor or to bitsavers, where the directory path *is* the
attribution.

**Practical rule for this repository:** record the **byte size**, the **magic bytes**, the
**revision string from the cover page**, and the **URL and retrieval date** for every document you
rely on — exactly as the existing records do (`SRC-RR-1.pdf` → 200, 2,239,056 B, `%PDF-1.2`).
Provenance you wrote down is worth more than provenance you assumed.

---

## 8. The lawful things that do most of what people want from bulk libraries

### 8.1 Openly published metadata corpora

The "indexing" side of the §2 line — large, free, redistributable, provenance-clean. Probed
2026-09-02 with a browser UA and `-L` [WEB] (S6):

| Corpus | What it is | Probe |
|---|---|---|
| **Crossref public data file** | The full Crossref metadata corpus, released annually, free | HTTP 200; the landing page is a redirect stub of 403 *bytes* — not an HTTP 403 |
| **OpenAlex snapshot** | The whole OpenAlex graph — works, authors, institutions, venues — **CC0**, S3-hosted | 200, 19,226 B. See [`open-access-full-text-sources.md` §2.2](open-access-full-text-sources.md) |
| **dblp** | The canonical CS bibliography. Daily XML dump, **CC0**, ~1.10 GB gzipped | 200, 2,512 B index. Fetch the DTD too or it will not parse |
| **Open Library data dumps** | Internet Archive's open bibliographic database of books | 200, 30,187 B |
| **Unpaywall data snapshot** | OA-location data for tens of millions of DOIs | 200, 1,421 B |
| **arXiv / HAL / Zenodo OAI-PMH** | Per-repository harvest interfaces | See the individual records in this directory |
| **HathiTrust Hathifiles** | Item-level metadata for the HathiTrust corpus | **200, 45,607 B** on the deep Hathifiles path with a browser UA. A **403 against the bare hostname** was recorded earlier in this pass — worth carrying into [`retrieval-notes.md`](retrieval-notes.md): the shallow URL is not a reliable test of the deep one |
| **DOAB** (Directory of Open Access Books) | Metadata for openly licensed scholarly books | **403, 5,556 B** (Cloudflare) to scripts on the probe date |

Between them these answer nearly every question people actually take to a shadow library's search
box — *does this work exist, who wrote it, what is its canonical citation, is there a free copy* —
without touching a copyrighted byte.

### 8.2 "Private collections": personal, lab and course collections

The grey middle: personal paper stashes, lab collections, Zotero/Mendeley group libraries,
university course-page PDF directories, curated GitHub reading lists. Many are **lawful** — author
copies posted under a publisher's self-archiving allowance, materials used under fair use / fair
dealing in teaching, or explicitly licensed works — and they are genuinely useful, because a human
curated them and wrote down why each item is on the list.

Named examples, each measured on **2026-09-02** [WEB] [API] (S6):

| Collection | What it is | Measured |
|---|---|---|
| **MIT 6.5840 / 6.824 Distributed Systems** — `pdos.csail.mit.edu/6.824/schedule.html` | Course reading list: MapReduce, GFS, "Paxos Made Simple", the extended Raft paper, Spanner, ZooKeeper, FaRM | 200, 17,414 B, **20 linked PDFs**. `6.5840` and `6.824` serve the identical document. Stable for years; the best curated entry point to the distributed-systems canon |
| **Readings in Database Systems, 5th ed. ("the Red Book")** — `redbook.io` | Bailis, Hellerstein & Stonebraker (eds). Free HTML and PDF chapters with editorial commentary | 200 (redirects to `www.`), 5,594 B, 15 PDF links. **Published free by its own editors** — the model of what a curated collection should be |
| **CMU 15-721 Advanced Database Systems** — `15721.courses.cs.cmu.edu/spring2024/schedule.html` | Andy Pavlo's per-lecture reading list, with slides and notes | 200, 117,066 B, **166 paper links**. Companion `15445.courses.cs.cmu.edu` 200, 32,181 B |
| **SAFARI / ETH Zürich Computer Architecture** — `safari.ethz.ch/architecture/fall2023/doku.php` | Onur Mutlu's course: openly published lecture materials and per-topic reading lists across memory systems, DRAM, processing-in-memory | 200, 32,717 B (`<title>start [Computer Architecture - Fall 2023]</title>`). Faculty page `people.inf.ethz.ch/omutlu/` 200, 19,912 B |
| **`0xor0ne/awesome-list`** — "Awesome Cybersecurity List" | Curated links to blog posts, write-ups and papers, heavy on embedded/IoT/firmware security — directly relevant to this knowledge base | **CC-BY-SA-4.0**, 4,089★, pushed 2026-08-30. Contents are `README.md` + `topics/` — **links, not files** |
| **`secfigo/Awesome-Fuzzing`** · **`sbilly/awesome-security`** | Curated fuzzing papers/tools; broad security resource list | **CC0-1.0**, 5,910★, 163 KB · **MIT**, 14,827★, 781 KB. Both explicitly licensed and links-only |
| **`theanalyst/awesome-distributed-systems`** · **`dgryski/awesome-consensus`** | Distributed-systems and consensus bibliographies | 12,359★ / 96 KB and 2,146★ / 37 KB, both **`license: null`** — links-only, so squarely lawful, but nothing is declared |
| **USENIX proceedings** · **IACR ePrint** | Every USENIX paper free by policy; 27,552 ePrint reports, CC-BY, full OAI-PMH | The two largest *lawful* bulk corpora in systems and crypto. [`open-access-full-text-sources.md` §3.1](open-access-full-text-sources.md) · [`cryptology-eprint-archive.md`](cryptology-eprint-archive.md) |
| **Zenodo communities** | Curated, DOI-minted, explicitly licensed collections of papers, datasets and firmware. `q="RISC-V"` → **496 records** [API] (S9) | [`zenodo.md`](zenodo.md). **This is how to make your own curated collection citable and lawful** |

**And now the counter-examples**, because "curated by a nice person on GitHub" is not a legal status.
GitHub API, 2026-09-02 [API] (S6):

| Repo | Measured | The problem |
|---|---|---|
| **`papers-we-love/papers-we-love`** | **109,438★, ~225 MB**, pushed 2026-08-31, ~50 topic dirs (`computer_architecture`, `distributed_systems`, `datastores`, `concurrency`, `garbage_collection`, `cryptography`, …) | One of the best-known curated CS paper collections in existence — and **`license: null`, no `LICENSE` file in the root.** It redistributes PDFs whose individual copyright status is mixed and undeclared |
| **`wcventure/FuzzingPaper`** | 2,768★, **~224 MB**, **MIT**, with a `Paper/` directory of PDFs | The MIT licence covers the *repository*, not the third-party papers inside it. A declared licence on a repo that redistributes others' work tells you nothing about the work |
| **`larsbrinkhoff/awesome-cpus`** | 2,003★, **~461 MB**, **CC0-1.0** | An "awesome list" that also stores documents. Same caution |
| **`rxin/db-readings`** · **`aphyr/distsys-class`** | 8,138★ / ~29 MB / `null`; 9,881★ / 96 KB / `null` (its `README.markdown` states no licence) | Excellent curation, undeclared terms |

**The pattern:** a link list is almost always fine; a repository that ships the PDFs is a
redistribution question no matter how good the curation or how permissive the repo's own licence.
Use all of them to *find* the paper, then run §7.2 and fetch the copy whose provenance you can state.

### 8.3 Trackers and preservation projects — where the line falls

- **Bibliographic and coverage trackers** — the scientometric studies in §3.2, OpenAlex's OA-status
  fields, Unpaywall's location data, dblp. These *measure* what exists and what is open. **Lawful,
  useful, citable**, and the reason anyone can discuss shadow-library coverage in numbers at all
  without redistributing anything.
- **Web and code archives** — the Internet Archive, Arquivo.pt, Software Heritage, bitsavers, Common
  Crawl. These *do* redistribute full text, but under statutory exceptions, rightsholder tolerance,
  explicit permission, or the operator's own ownership of the physical originals (bitsavers, where
  Al Kossow scanned his own collection). See
  [`recovering-dead-technical-sites.md`](recovering-dead-technical-sites.md).
- **Community torrent-seeding of shadow-library dumps** — the 2019 LibGen seeding effort and the
  2021 r/DataHoarder Sci-Hub backup organised in response to the Delhi filing [COM] (S1, S3).
  Sincerely motivated by preservation; **still redistribution of copyrighted works**, and no court in
  §§3–6 treated preservation motive as a defence.

The distinction is not about intent. It is about whether the bytes being moved are the copyrighted
work.

---

## 9. Decision table

| What you are looking for | Where to look | Lawful? | Reliable? |
|---|---|---|---|
| A systems / OS / networking / storage / security **conference paper** | **USENIX**, then dblp → publisher | ✅ | ✅ version of record |
| A **crypto or embedded-security** paper | **IACR ePrint**, TCHES | ✅ | ✅ |
| An **NLP / computational-linguistics** paper | **ACL Anthology** | ✅ | ✅ |
| Anything with an **arXiv ID** | arXiv, via Semantic Scholar `externalIds.ArXiv` (Unpaywall misses these) | ✅ | ⚠️ check whether the arXiv version is the published one |
| A **paywalled IEEE** paper | TechRxiv via Crossref `is-preprint-of`; then the author's page; then email the author | ✅ | ⚠️ author's version, not the VoR |
| The **canonical citation** for a half-remembered CS paper | **dblp** | ✅ | ✅ best in class |
| Whether a **free copy exists anywhere** | Unpaywall → OpenAlex `locations[]` → CORE / BASE / OpenAIRE | ✅ | ✅ |
| A **reading list** in distributed systems, databases, architecture or security | MIT 6.5840 · CMU 15-721 · SAFARI/ETH · the Red Book · `0xor0ne/awesome-list` · `secfigo/Awesome-Fuzzing` (§8.2) | ✅ (link lists and course pages) | ✅ for discovery — then resolve the DOI |
| A **historical vendor manual, data book or corporate tech report** | **bitsavers**, then archive.org, then Wayback / Arquivo.pt | ✅ | ✅ scan is sound; **catalogue metadata often is not** (§7.1) |
| A **dead vendor documentation URL** | Wayback `id_` → Arquivo.pt → Common Crawl WARC range-GET | ✅ | ✅ byte-exact if you use `id_` / range-GET |
| A **deleted source repository** | **Software Heritage** | ✅ | ✅ content-addressed, verifiable offline |
| **Bibliographic metadata at scale** | Crossref public data file, OpenAlex snapshot, dblp, Open Library dumps, Hathifiles | ✅ | ✅ |
| A **current (post-2021) paper** | The ladder above. **Sci-Hub is frozen and does not have it** (§3.1) | — | — |
| A **textbook** | Your library, the publisher's OA programme, DOAB, HathiTrust, Open Library controlled digital lending | ✅ | ✅ |
| A **standard** | IETF/RFC free · RISC-V free · USB-IF free · JEDEC free w/ registration · IEEE SA ⚠️ mostly paid, partial GET Program | ✅ | ✅ |
| A **GitHub repo that ships PDFs** (`papers-we-love`, `FuzzingPaper`, `awesome-cpus`) | Use it to find the citation, not as the source | ⚠️ repo licence ≠ paper licence (§8.2) | ⚠️ unstated version and edition |
| Anything, from a **shadow library** | — | ❌ **Distributes copyrighted works without authorisation; found unlawful in multiple jurisdictions; may be unlawful where you are; commonly institution-blocked; documented credential-phishing and cloned-site risk** | ❌ **Version, edition, completeness and integrity all unverifiable** |

**The short version:** for technical literature the lawful route is not a compromise — it is usually
*better*, because it arrives with a resolvable identifier, a stated version and a URL you can cite.
That is exactly what an unprovenanced PDF cannot give you, and exactly what this repository's
evidence discipline requires.

---

## 10. What this record could not verify

- **Every operator-reported collection size** — Sci-Hub's 88,343,822 files (2022-07-15), Anna's
  Archive's 71,400,751 books / 157,010,964 papers / ~1.1 PB (2026-08-20), Z-Library's 13.35 M books /
  84.8 M articles / 220 TB (2023-02), LibGen's 80 M articles (2024-02-04) — is a **self-report relayed
  by a third party**. **[NOT-VERIFIED]**; by policy this pass did not attempt to verify them, and the
  current operational state of these services was likewise not probed, deliberately.
- **Sci-Hub's freeze at primary-source level.** "Uploads paused December 2020; new-publication uploads
  suspended during 2021 under the Indian injunction, except for batch releases" is consistently
  reported [COM] and quoted verbatim in §3.1, but **no primary operator statement or court order was
  retrieved** — **[NOT-VERIFIED]** as to the exact date and mechanism. Likewise the legal status of
  **Sci-Net** (2025), and whether Anna's Archive metadata releases are lawfully sourced in the general
  case (the WorldCat portion is now under a deletion order; the rest is unknown).
- **Court documents were not read directly.** Every case in §§3–6 is sourced from Wikipedia's
  referenced articles and the press reporting they cite — not from PACER, the Delhi High Court, or any
  court's own docket. **Case numbers are therefore deliberately omitted.** Courts, dates, outcomes and
  amounts are consistently reported across those sources, but the primary record was not consulted.
  **No legal conclusion in this file is the author's own; each is a report of a court's or a source's
  statement.**
- **Licence status of the *contents* of any collection in §8.2.** What was measured is the repository-
  or page-level licence field, not the copyright status of individual PDFs. That distinction is the
  point of the counter-examples, and it is **[NOT-VERIFIED]** item by item.
- **Three probes that failed, so nothing is claimed from them:** `doabooks.org` **403** (5,556 B,
  Cloudflare), so DOAB's bulk-metadata terms were not read; `people.eecs.berkeley.edu/~kubitron/cs262/`
  (Berkeley CS262A reading list) **failed to connect** (curl `000`); and `blog.acolyer.org` ("The
  Morning Paper") answered **200 / 104,126 B** but could not be shown to be still updated, so it is not
  listed as a live collection. All **[NOT-VERIFIED]**.
- **Length note.** This record is longer than the 300–400 lines targeted for files in this directory.
  The eleven subjects it was scoped to cover, each with the house evidence labels and a full sources
  block, did not compress below this without dropping sourced content. Recorded rather than hidden.

---

## 11. Sources

Retrieval date **2026-09-02** throughout. Raw output:
[`../../scratch/preprint-repositories/bulk-archives/`](../../scratch/preprint-repositories/bulk-archives/).

Wikipedia extracts were taken via `en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1`
and saved to the scratch directory. All are **[COM]** — press and community reporting, once removed.

- **S1** *Sci-Hub* (32,354 chars, `wp-Sci-Hub.txt`) — founding and Elbakyan; the December 2020 upload
  pause and 2021 suspension (quoted verbatim in §3.1); the 2022-07-15 file count; the September 2021
  2.3 M batch; the US$15 M and US$4.8 M default judgments; the Delhi High Court case and the
  2025-08-19 ban; the 2021 UK injunction and City of London Police warning; Sci-Net; the coverage
  percentages; the Scholarly Kitchen dispute; the r/DataHoarder backup effort.
- **S2** *Shadow library* (REST summary, 1,977 B) — the definition and the synonyms *pirate library* /
  *black open access* in §2.
- **S3** *Library Genesis* (9,020 chars) — the samizdat/RuNet lineage; ~2008 consolidation; library.nu
  absorption; the 2024-02-04 composition table; the 2020 fork and its divergence; the August 2024
  abandonment reports; the 2015 Elsevier and 2023–24 Pearson et al. litigation and the US$30 M
  judgment; the CUII block; dual Russia/Netherlands registration; the Anthropic US$1.5 bn settlement.
- **S4** *Anna's Archive* (19,649 chars) — the PiLiMi origin; CC0 source code; the source-library list;
  the 2026-08-20 self-reported scale; the AAC format; the LLM SFTP-access programme; the OCLC,
  Spotify/labels and 13-publisher matters; the Netherlands/UK/Germany blocking orders; the Meta ruling
  and Chhabria's caveat.
- **S5** *Z-Library* (10,964 chars) — the LibGen-mirror origin; the February 2023 self-reported scale
  and 220 TB figure; the 2022-11-03 seizure of >240 domains; the E.D.N.Y. indictment of Napolsky and
  Ermakova unsealed 2022-11-16; the July 2024 escape and Interpol notice; the later seizure rounds;
  the French and Indian blocking orders; the Cybernews report of the ~10-million-user clone-site data
  leak (quoted verbatim in §6).
- **S6** Direct probes of lawful collections and corpora. **Full response codes and byte sizes are in
  `probe-log-2026-09-02.txt`; the figures cited inline in §8 come from it.** [API] [WEB] Covers:
  GitHub `/repos/…` for the ten curated repos named in §8.2 (stars, size, `license.spdx_id`,
  `pushed_at`); the course and collection pages MIT `6.824`/`6.5840`, `redbook.io`, CMU `15-721` and
  `15-445`, SAFARI/ETH `architecture/fall2023`, `people.inf.ethz.ch/omutlu/`; and the metadata
  corpora Crossref public data file, OpenAlex snapshot docs, Open Library dumps, `dblp.org/xml/`,
  Unpaywall snapshot, HathiTrust Hathifiles (**200 / 45,607 B**), `doabooks.org` (**403 / 5,556 B**)
  and Berkeley CS262A (**connect failure**). Chrome UA with `-L` throughout, per
  [`AGENTS.md`](../../AGENTS.md) step 2.
- **S7** `api.crossref.org/works/<DOI>` for every identifier in §3.2, each title machine-checked
  against the response — all six confirmed with venue and creation date. Also records the four
  wrong-guess DOIs noted in §3.2. **[API]**
- **S8** `api.openalex.org/works?search="Anna's Archive"` → `meta.count` **56**, including
  `10.1073/pnas.2503051122` and `10.6084/m9.figshare.32454042`. **[API]**
- **S9** `dblp.org/search/publ/api` for *"In Search of an Understandable Consensus Algorithm"* →
  `@total: 1`, USENIX ATC 2014, `ee` = usenix.org. `zenodo.org/api/records?q="RISC-V"&size=1` →
  `hits.total` **496**, consistent with [`README.md §4`](README.md#6-probing-traps)'s
  quoted-vs-unquoted finding. **[API]**
- **S10** Companion records: [`open-access-full-text-sources.md`](open-access-full-text-sources.md)
  (the ladder, §3.1 USENIX, §5 green OA and version terminology),
  [`recovering-dead-technical-sites.md`](recovering-dead-technical-sites.md) (§3.3 the archive.org
  metadata and OCR failures, §4 bitsavers, §6 Software Heritage),
  [`government-and-institutional-technical-reports.md`](government-and-institutional-technical-reports.md)
  (§5 standards bodies), [`cryptology-eprint-archive.md`](cryptology-eprint-archive.md),
  [`techrxiv.md`](techrxiv.md), [`zenodo.md`](zenodo.md), [`arxiv.md`](arxiv.md), and
  [`README.md § Evidence and method`](README.md#evidence-and-method).
- **S11** [`ai-crawler-site-access-table.md` § General retrieval tips](../../ai-crawler-site-access-table.md#general-retrieval-tips) —
  the existing entry under *Alternate hosting of papers/PDFs* names Library Genesis and Anna's Archive
  as places that "*may* hold what you're looking for when the original host is gone". **This record
  does not contradict that framing; it qualifies it.** That entry already puts arXiv, ar5iv and author
  self-archiving first, and treats bulk libraries as a fallback for material whose original host is
  *gone*. This file supplies what that entry has no room for: for the technical literature in scope
  the lawful copy nearly always exists (§1); the binding constraint on an unprovenanced copy is
  reliability, not convenience (§7); and the legal and security position is as set out in §§3–6.

