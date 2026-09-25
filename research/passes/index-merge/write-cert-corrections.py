#!/usr/bin/env python3
"""Round-2 integration, TASK 2 — dated corrections to the refuted certification claims.

The 2026-09-04 Xteink pass recorded that no FCC/CE filing existed for these
devices.  That is refuted: Xteink holds five Original Equipment grants under
grantee code `2BTR9`.

Every stale claim gets a dated correction **appended**, quoting the original line
verbatim and citing its line number.  **No original line is edited, reworded,
reordered or removed.**  Files are skipped if they are live (`mmin -15`) or if a
correction with this marker is already present.
"""
import os, sys, time, subprocess

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
os.chdir(REPO)
DRY = '--apply' not in sys.argv
MARK = 'Correction, 2026-09-11 — Xteink FCC grants exist'

# file -> (1-based line numbers of the stale claims, depth to repo root)
TARGETS = {
 'devices/xteink/x4-pro/acquisition/README.md':        [28, 38],
 'devices/xteink/x4-pro/media.md':                     [13],
 'devices/xteink/x4-pro/README.md':                    [165],
 'devices/xteink/x4-pro/features/wifi-and-bluetooth.md': [13],
 'devices/xteink/x4-pro/compatibility-and-status.md':  [62],
 'devices/xteink/x4-pro/research-log.md':              [10, 21],
 'devices/xteink/x4-classic/media.md':                 [13],
 'devices/xteink/x4/media.md':                         [12],
 'devices/xteink/x4/gaps-and-conflicts.md':            [59],
 'devices/xteink/x4/features/wifi-and-bluetooth.md':   [10],
 'devices/xteink/x4/community.md':                     [174],
 'devices/xteink/x3/gaps-and-conflicts.md':            [109],
 'devices/xteink/s4/gaps-and-conflicts.md':            [74],
}

GRANTS = """| FCC ID | Granted | Device |
|---|---|---|
| `2BTR9-X4L` | 2026-08-13 | XTEINK X4 Light |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 |
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 |"""

def rel(f, t):
    return os.path.relpath(t, os.path.dirname(f))

def block(f, lines, src):
    own = f.split('/')[2] if f.startswith('devices/xteink/') else None
    cert = f"devices/xteink/{own}/certification-and-compliance.md"
    has_cert = os.path.exists(cert)
    L = ["", "---", "", f"## ⚠ {MARK}", "",
         "The line(s) below, still present above and deliberately unedited, are **refuted**:", ""]
    for n in lines:
        L.append(f"> *line {n}:* {src[n-1].strip()}")
        L.append(">")
    L += ["",
          "**Xteink is an FCC grantee.** Applicant **Shenzhen Xiaohu Xingtong Technology Co., "
          "Ltd.**, grantee code **`2BTR9`**, registered 2025-12-21, holding **five granted "
          "Original Equipment authorisations**:", "", GRANTS, "",
          "The original finding confused **\"no mark visible in a product photograph\"** with "
          "**\"no grant exists\"**. Those are different claims, and only the first was tested.",
          "",
          "- ✅ **Survives:** no FCC ID was legible on the exteriors photographed. Not re-tested.",
          "- ❌ **Refuted:** any reading that these devices are uncertified or unauthorised for "
          "the US.", "",
          "47 CFR §2.935 permits an **e-label** in software instead of a printed mark, which is "
          "ordinary for a device with a screen. **That is a likely explanation and it was not "
          "verified.**", "",
          "The absence was never re-searched in 2026-09-04 because **no FCC ID was known and the "
          "grantee code had not been found**. Enumerating the grantee — not searching the product "
          "name — is what resolved it. Method: "
          f"[`guides/research/finding-certification-records.md`]"
          f"({rel(f, 'guides/research/finding-certification-records.md')}).", ""]
    if has_cert:
        L += [f"Full record, with controls: [`certification-and-compliance.md`]({rel(f, cert)}).", ""]
    L += ["Listed in "
          f"[`scratch/index-merge/corrections-requiring-review.md`]"
          f"({rel(f, 'scratch/index-merge/corrections-requiring-review.md')}).", ""]
    return "\n".join(L)

now = time.time()
done, skipped = [], []
for f, lines in sorted(TARGETS.items()):
    if not os.path.exists(f):
        skipped.append((f, 'missing')); continue
    if (now - os.path.getmtime(f)) < 15 * 60:
        skipped.append((f, 'LIVE (mmin -15)')); continue
    src = open(f).read().splitlines()
    if MARK in "\n".join(src):
        skipped.append((f, 'already corrected')); continue
    bad = [n for n in lines if n > len(src)]
    if bad:
        skipped.append((f, f'line out of range {bad}')); continue
    if not DRY:
        with open(f, 'a') as fh: fh.write(block(f, lines, src))
    done.append(f)

print('DRY RUN' if DRY else 'APPLIED')
for f in done: print('  corrected:', f)
for f, why in skipped: print(f'  SKIPPED  : {f}  ({why})')
