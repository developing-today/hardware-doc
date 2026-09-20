# `dtsbytebooks.com` — what it is

> Reviewed **2026-09-11** because two third-party plugins reference it and nobody
> had checked what it was. The short answer inverts the concern that prompted the
> review.
>
> Retrievals are `executed-success`. **No account was created, nothing was logged
> into, no credential was transmitted, and no endpoint was probed beyond ordinary
> unauthenticated `GET`s of public pages.**

## It is Adobe's ebook DRM platform, under new ownership

ByteBooks is the continuation of the **Adobe eBook Platform** — Adobe Content
Server (ACS), the Reader Mobile SDK (RMSDK), and Adobe Digital Editions (ADE).
Adobe divested it. Adobe's own support site states:

> *"Ongoing platform support and feature development for Adobe eBook Platform
> Components … is now handled by **Wipro Engineering – Connected Services
> (formerly HARMAN Digital Transformation Solutions (DTS))**. As of **July 2025**,
> Adobe transitioned these responsibilities to Wipro."*

**"DTS" = Digital Transformation Solutions**, Harman's former division — which is
where the domain name comes from. End-user cutover was **2026-06-23**, when
ByteBooks IDs replaced Adobe IDs.

### The DNS is conclusive

This is not a claim that rests on marketing copy. Adobe's own production hostnames
now delegate into this domain:

| Query | Result |
|---|---|
| `adeactivate.adobe.com` | **CNAME → `activate.dtsbytebooks.com`** |
| `readerscert.adobe.com` | CNAME → `readerscert.dtsbytebooks.com` |
| `nasigningservice.adobe.com` | CNAME → `nasigningservice.dtsbytebooks.com` |
| `eusigningservice.adobe.com` | CNAME → `eusigningservice.dtsbytebooks.com` |
| `GET contentserver.dtsbytebooks.com/` | returns `"You have reached contentserver.adobe.com"` |

Only whoever controls Adobe's DNS can create those records. The TLS certificate
carries both `adeactivate.adobe.com` and `*.dtsbytebooks.com` as SANs.

## Who runs it

| | |
|---|---|
| Operator | **Wipro Ltd** (NYSE: WIT), Bengaluru |
| Legal entity | *"General Counsel, Wipro Ltd, Doddakannelli, Sarjapur Road, Bangalore"* (from the EULA) |
| Contact | `ebooks-support@wipro.com`, `contentserver-support@wipro.com` |
| Registrar | **CSC Corporate Domains** — an enterprise brand-protection registrar |
| TLS | Sectigo **OV**, issued to `Harman International Industries, Incorporated` — a transition artefact |
| Hosting | AWS (S3/CloudFront, ELB `us-west-2`) for the site and content server; **Oracle Cloud** for activation and signing |
| Domain created | **2025-10-31** · Wayback first capture **2026-05-20** |

No privacy shield, no anonymity, named public company, named general counsel.

## Funding

**Free for end users.** OverDrive's documentation: *"A ByteBooks ID is a **free**
account…"* There is no payment step in registration.

Revenue is **B2B**, exactly as Adobe's was — licensing Content Server, RMSDK and
white-label reader apps to publishers, retailers and libraries. Adobe's notice
says Wipro handles *"customer support, contract renewals … billing."* No public
price list; enterprise quote-based.

So the answer to *"if it's free, what pays for it?"* is: **publishers do, as they
always did.** This is an inherited enterprise platform, not a venture-funded
startup that needs to monetise users later.

## What using it involves

1. Register at `dtsbytebooks.com/register` — first/last name, country, email,
   password. No payment, no library card, no proof of purchase.
2. **If you have an existing Adobe ID, tick the migration box and use the exact
   same email.** That is what preserves your existing licences.
3. Existing authorised devices keep working. You need the account when
   authorising a *new* device.

Device limit is 10 per user, inherited from Adobe.

## What it receives

The published privacy text discloses processing of: user ID, device ID,
application ID, IP address (country-level), expiry/lending data, ebook metadata
(title, author, publisher, ISBN), and:

> *"**Percentage of Content Read** — Used to support subscription or usage-based
> access models"*

**That is the most privacy-adverse item**, and it deserves to be stated plainly
rather than buried: the platform is capable of reporting how far through a book
you are. It was in Adobe's platform too — cf. the 2014 ADE telemetry controversy
— so this is continuity, not a new imposition. But "it was always like this" is
not the same as "it is fine".

Also disclosed: *"If you open or read an eBook that does not include digital
rights management (DRM), ByteBooks Digital Editions does not process user or
device information."*

`robots.txt`, `sitemap.xml` and `.well-known/security.txt` all return 403. **The
absence of a `security.txt` is a small mark against them** for a service holding
account credentials.

## Legal posture

There is no "is this an Adobe-licensed operator?" question to answer, because
**it is the licensor**. The platform is designed to *enforce* ADEPT, not
circumvent it. Nothing about ByteBooks is grey-market.

## Reputation

- **Leseratte10**, author of the leading independent ACSM/Calibre plugin, tested
  the transition on 2026-06-24: *"the current versions of the plugin continue to
  work as if nothing had happened … it's now downloaded from a server under
  dtsbytebooks.com instead of an Adobe server."* No security concerns raised.
- **MobileRead** showed mild wariness, no alarm — one poster noted *"I can't find
  much about Bytebooks apart from their own material"*, and another immediately
  linked Wipro's Wikipedia entry.
- **OverDrive** and **eBooks.com** both publish official ByteBooks instructions.
- **No fraud, phishing, scam or breach reports found.** Complaints are ordinary
  migration friction — password resets, device-limit errors.

## Where the actual risk is

Not here. The genuine exposure in this stack is the **plugins**, and it is worth
being precise:

1. **`protected-content` is fetched live from a Railway URL with no repository,
   no version pinning and no licence.** Its author can change `plugin.js` at any
   time, and it loads into an unauthenticated page where you type a password.
   That is the real supply-chain concern. `libby` at least lives in a public repo
   where changes are visible.
2. **`authURL` is discovered at runtime** from the activation service, so whoever
   controls that DNS chooses where your RSA-wrapped password is posted. Inherent
   to ADEPT and equally true of Adobe Digital Editions itself — but it means trust
   ultimately rests on DNS.
3. The RSA wrapping uses **Adobe certificates that expired in 2013/2018**; ADEPT
   clients don't check expiry. Normal for the protocol, worth knowing.

The password itself is RSA-encrypted to the service certificate before it leaves
the device (`protected-content` ≈ lines 385–425), which is textbook ADEPT
`SignInDirect`.

## Known / inferred / unknown

| | |
|---|---|
| **Known** | ByteBooks = Adobe's ebook DRM platform under Wipro since July 2025; user cutover 2026-06-23; free to users, B2B-funded; the Adobe→ByteBooks CNAMEs; registrar, hosting, cert, domain age. Corroborated independently by Adobe, OverDrive, eBooks.com and Leseratte10 |
| **Inferred** | Wipro now holds the ADEPT certificate private keys — follows necessarily from operating `SignInDirect`. The Harman-named TLS cert is a transition leftover |
| **Unknown** | Server-side logging and retention specifics; B2B pricing; independent press coverage of the Harman-DTS/Wipro transfer |

**The service is not opaque** — which was the thing worth checking, and the
opposite of what was assumed.

## Method and limits

Public pages and public APIs only, unauthenticated `GET` exclusively. **No
account created, no login attempted, no credential sent, no `POST` issued, no
vulnerability probing.** Because only `GET` was used, a method-gated API route
cannot be *fully* excluded — though a CloudFront/S3 origin returning the SPA shell
for every tested path makes one very unlikely.

## See also

- [Plugin source survey](plugin-source-survey.md) — including the **retraction** of this
  knowledge base's earlier claim that the plugins call `dtsbytebooks.com/api/*`
- [The Libby path](libby-path.md)
