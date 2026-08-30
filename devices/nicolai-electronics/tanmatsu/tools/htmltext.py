#!/usr/bin/env python3
"""Extract readable plain text from a server-rendered HTML documentation page.

Used to snapshot badge.team and solder.party pages (both Hugo static sites) into
diffable text. Tables are flattened with ' | ' separators so the pin tables on
badge.team survive extraction, which matters because those tables are the only
published source for several Tanmatsu facts.

Deliberately dependency-free: no bs4/lxml, so it runs anywhere.
NOTE: the stored artifacts are the OUTPUT of this script, not the original HTML.
Re-running a fetch will not reproduce their hashes unless you use this extractor.

Usage: htmltext.py <file.html>
Executed 2026-08-24.
"""
import html
import re
import sys


def extract(raw: str) -> str:
    m = re.search(r"(?is)<main.*?</main>", raw) or re.search(r"(?is)<article.*?</article>", raw)
    t = m.group(0) if m else raw
    t = re.sub(r"(?is)<(script|style|nav|footer|head).*?</\1>", " ", t)
    t = re.sub(r"(?i)<br\s*/?>", "\n", t)
    t = re.sub(r"(?i)</(p|div|li|tr|h\d)>", "\n", t)
    t = re.sub(r"(?i)</t[dh]>", " | ", t)
    t = re.sub(r"(?s)<[^>]+>", "", t)
    t = html.unescape(t)
    out, prev = [], None
    for line in (l.strip() for l in t.split("\n")):
        if not line or line == prev:
            continue
        out.append(line)
        prev = line
    return "\n".join(out)


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
        print(extract(f.read()))
