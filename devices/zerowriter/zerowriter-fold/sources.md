# Zerowriter Fold — source manifest

> ⚠ **This device record rests on two sources, one of which was never retrieved.** The Fold is an
> unshipped, crowdfunded product; there is no design data, no independent review, no teardown and no
> unit in the wild. Every specification in [`README.md`](README.md) is a **vendor claim about a
> product that does not yet exist**, and this manifest exists mainly to make that unusually thin
> evidence base explicit.
>
> Retrieved **2026-08-24**; URLs re-verified **2026-08-28**. Local paths are relative to this device
> folder; a dash means link-only.

`Class` is one of **primary** / **authorized mirror** / **credible mirror** / **standard** / **community**.

---

## 1. Sources

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| ZF-1 | Zerowriter Fold product page | Zerowriter (Adam Wilk) | primary | official page | <https://zerowriter.ink/pages/zerowriter-fold> | 2026-08-24 (HTTP 200 re-checked 2026-08-28) | live page, undated | **Essentially the entire record**: the claimed display (6″ frontlit, 10 brightness levels, 5″ × 3.75″ viewing area), Choc v1 hot-swap keyboard, 12″ × 5″ × 1.25″ closed / 0.6″ open, 900 g, 50–100 h battery, microSD, USB-C, `.txt` + `.md`, ~$329 retail / ~$239 First Wave (500 units), Ottawa assembly, >300 units/month, the "Zerowriter Core" open-source statement, the no-WiFi/no-AI/no-subscription positioning, the Cloud Push roadmap item, the 2024→'26 company account, the Indie Author Program, and the shipping/VAT/tariff disclosure | ⚠ **Vendor marketing for an unshipped product.** Self-published, undated, unreviewed and unfalsifiable at retrieval time. Contains **no SoC, no display controller, no panel part number, no battery capacity** and no design files. Prices exclude shipping, VAT and tariffs by the vendor's own statement | [`artifacts/product-page-2026-08-24.html`](artifacts/product-page-2026-08-24.html) — 183,585 B, SHA-256 `9f5716558ec9280cc916a6d9f1c162ba441ee8ad0207a1fa6bc0a1bb2a998b46` |
| ZF-2 | Zerowriter Fold Kickstarter campaign | Zerowriter (Adam Wilk) via Kickstarter | primary | store listing | <https://www.kickstarter.com/projects/zerowriter/zerowriter-fold> | **not retrieved** — probed 2026-08-24 and 2026-08-28 | campaign live at snapshot; "Projects We Love" | Campaign existence and the First Wave pricing structure, **as reported by ZF-1** — not read directly | ❌ **Never fetched. HTTP 403 to every user agent tried** on 2026-08-28 (default `curl`, Chrome 131, `WhatsApp/2.23.20.0`) — Kickstarter bot-blocks automated clients regardless of UA. **This is the single largest gap in the record**: campaign pages carry backer counts, funding totals, stretch goals, a risks section and updates, none of which ZF-1 contains. Recovering it needs a real browser session | – |

## 2. Contextual sources (evidence about the Fold that lives elsewhere)

The Fold was discovered while correcting the ZeroWriter Ink record, and two claims in
[`README.md`](README.md) are cross-generational rather than Fold-specific.

| ID | Title | Publisher/author | Class | Medium | URL | Retrieved | Published/updated | Establishes | Scope/limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|---|
| ZF-3 | ZeroWriter Ink device record and its sources | this repository | — (internal) | — | [`../zerowriter-ink/sources.md`](../zerowriter-ink/sources.md) | 2026-08-24 | — | The **lineage** claim (`zerowriter1` Raspberry Pi Zero → Ink → Fold) and the **"neither product's main application is open source yet"** finding, which pairs ZF-1's future-tense "Zerowriter Core … releasing as open source in the coming months" with the Ink's binaries-only firmware release | The Ink's evidence does not transfer to the Fold's hardware. If ZF-1's "we developed our own underlying display technologies, boards, and processes" is accurate, **none** of the Inkplate research applies | – |
| ZF-4 | Soldered Inkplate 5 / Gen 2 device record | this repository | — (internal) | — | [`../../soldered-electronics/inkplate-5/README.md`](../../soldered-electronics/inkplate-5/README.md) | 2026-08-24 | — | The platform the Ink is built on, and therefore the baseline against which ZF-1's in-house-hardware claim is a **discontinuity** | Cited only to mark what the Fold will *not* inherit — the Inkplate Arduino library and the TAPR-licensed design data | – |
| ZF-5 | Zerowriter vendor sourcing guide | this repository | — (internal) | — | [`../../../vendors/zerowriter/README.md`](../../../vendors/zerowriter/README.md) | 2026-08-24 | — | Where Zerowriter content actually lives, and the `zerowriter.ink` retrieval traps | ⚠ **One documented trap no longer reproduces** — see §3 below | – |

---

## 3. Retrieval findings

**The `zerowriter.ink` Chrome-UA block has lifted.** The [vendor guide](../../../vendors/zerowriter/README.md)
records that `zerowriter.ink` **403s a standard desktop Chrome UA on `/pages/*`** while serving the
site root normally, and that an alternate UA was needed. Re-probed **2026-08-28**, all three of
default `curl`, Chrome 131 and `WhatsApp/2.23.20.0` returned **HTTP 200** on
`/pages/zerowriter-fold` (181–183 KB). The block appears to have been removed or relaxed. The
vendor guide has **not** been edited here — it is outside this pass's scope — but the observation
is recorded so the next researcher does not assume a workaround is still required. Note also that
the 2026-08-28 responses are 1.8 KB smaller than the retained 2026-08-24 snapshot and differ
slightly between UAs, so the **page content has changed since capture**; ZF-1's local copy is the
pinned evidence.

**Kickstarter is hard-blocked.** ZF-2 returns 403 to every user agent attempted. Per the
repository's [web-retrieval fallback policy](../../../AGENTS.md), UA rotation was tried and
failed; the remaining routes are a real browser session or an archive capture, neither of which was
attempted in this pass.

## 4. What this evidence cannot support

Recorded so the record's limits are not mistaken for findings:

- **No hardware claim is verifiable.** SoC, display controller, panel part number and battery
  capacity are all unstated by ZF-1 and unavailable anywhere else. The [open questions in
  `README.md`](README.md#open-questions) are open because **no source addresses them**, not because
  the search was shallow.
- **No component cross-links exist in this record** — and correctly so. The Fold has **no known
  bill of materials**, so there is nothing to link to
  [`components/`](../../../components/README.md). Any component reference in
  [`README.md`](README.md) is a reference to the *Ink's* parts, and links to the Ink's record.
- **No pricing observation is a street price.** ~$329 / ~$239 are vendor-stated crowdfunding tiers
  excluding shipping (~$20–35), VAT (~19–25 % in the EU) and a stated ~10 % US tariff on
  Canadian-origin goods. The all-in estimates in [`README.md`](README.md#shipping-and-import-costs)
  are **arithmetic on vendor figures**, not observed transactions.
- **No independent coverage was searched for.** Unlike the Ink — which has eleven catalogued press
  items — no forum, blog, review, video or social search was run for the Fold in this pass.
- **The campaign was never read.** See ZF-2. This is the obvious next step for anyone continuing
  this record.

---

## 5. Related

- [ZeroWriter Ink](../zerowriter-ink/README.md) · [its sources](../zerowriter-ink/sources.md) — the shipping first-generation product
- [Zerowriter vendor guide](../../../vendors/zerowriter/README.md)
- [Soldered Inkplate 5 / Gen 2](../../soldered-electronics/inkplate-5/README.md) — the Ink's platform, which the Fold does not use
