#!/usr/bin/env python3
"""Extract per-project entries + their hyperlinks from Seeed's XIAO Reference
Design catalogue PDF (129 pages, Adobe InDesign).

Two problems the PDF creates and this solves:
  1. InDesign exports kerned text with spaces inside words ("W e ar ables").
     Fixed by building a vocabulary from the pages that are NOT kerned, then
     greedily re-merging short token runs that reconstruct a known word.
  2. The "Read more details" call-to-action is a link annotation, not text, so
     the project URLs are invisible to text extraction. Pulled from /Annots.

Usage: extract_showcase.py <pdf> <out.json>
Executed 2026-08-24.
"""
import re, sys, json, pypdf
from collections import Counter

CATS = ["Wearables", "Robotics", "Smart Home", "Smart Agriculture", "Health",
        "Industrial", "Environment", "Education", "Art", "Audio", "Gaming",
        "Tools", "Networking", "Drones", "Security", "Automotive", "Science", "AI"]
VARIANTS = ["XIAO ESP32-S3 Sense", "XIAO ESP32-S3 Plus", "XIAO ESP32-S3",
            "XIAO ESP32-C6", "XIAO ESP32-C3", "XIAO nRF52840 Sense", "XIAO nRF52840",
            "XIAO RP2350", "XIAO RP2040", "XIAO SAMD21", "XIAO RA4M1",
            "XIAO MG24 Sense", "XIAO MG24", "XIAO nRF54L15 Sense", "XIAO nRF54L15"]


def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def main():
    r = pypdf.PdfReader(sys.argv[1])
    pages = [" ".join((p.extract_text() or "").split()) for p in r.pages]

    vocab = Counter()
    for t in pages:
        toks = t.split()
        if not toks:
            continue
        if sum(1 for x in toks if len(x) <= 2) / len(toks) < 0.25:
            for w in re.findall(r"[A-Za-z][A-Za-z'-]{2,}", t):
                vocab[w.lower()] += 1
    V = set(vocab)

    def dekern(t):
        toks = t.split()
        out, i = [], 0
        while i < len(toks):
            best = None
            for j in range(min(i + 7, len(toks)), i + 1, -1):
                cand = "".join(toks[i:j])
                if len(cand) > 2 and cand.lower() in V:
                    best = (cand, j)
                    break
            if best:
                out.append(best[0]); i = best[1]
            else:
                out.append(toks[i]); i += 1
        return " ".join(out)

    links = {}
    for i, p in enumerate(r.pages):
        seen = []
        for a in p.get("/Annots") or []:
            try:
                u = (a.get_object().get("/A") or {}).get("/URI")
                if u and u not in seen:
                    seen.append(u)
            except Exception:
                pass
        links[i + 1] = seen

    out = []
    for i, raw in enumerate(pages):
        t = dekern(raw)
        n = norm(t)
        if "introduction" not in n:
            continue
        cat = next((c for c in CATS if n.startswith(norm(c))), None)
        var = next((v for v in VARIANTS if norm(v) in n[:220]), None)
        m = re.search(r"\bBy\s+(.{3,120}?)\s+Introduction\s*:", t, re.I | re.S)
        author = " ".join(m.group(1).split()) if m else None
        parts = re.split(r"Introduction\s*:", t, maxsplit=1, flags=re.I)
        intro = " ".join(parts[1].split()) if len(parts) > 1 else ""
        kw = None
        km = re.search(r"Keywords?\s*:\s*(.*?)(?:>>|Read more|Use Case|$)", intro, re.I)
        if km:
            kw = [k.strip(" ;.") for k in km.group(1).split(";") if k.strip(" ;.")]
        intro = re.sub(r"Keywords?\s*:.*$", "", intro, flags=re.I).strip()
        intro = re.sub(r">>\s*Read more det ?ails?\.?", "", intro, flags=re.I).strip()
        intro = re.sub(r"\s*Use Case \d+\s*$", "", intro).strip()
        title = None
        if var and m:
            seg = t[:m.start()]
            idx = seg.lower().rfind(var.lower()[-8:])
            if idx >= 0:
                title = " ".join(seg[idx + 8:].split())
        if not title:
            title = " ".join(t[:100].split())
        ext = [u for u in links.get(i + 1, []) if "seeedstudio.com" not in u or "/p-" not in u]
        out.append(dict(page=i + 1, category=cat, variant=var, title=title,
                        author=author, keywords=kw, intro=intro,
                        links=links.get(i + 1, []), project_links=ext))
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    print(f"extracted {len(out)} entries; "
          f"{sum(1 for o in out if o['project_links'])} have project links")
    print("variants:", Counter(o["variant"] for o in out).most_common())


main()
