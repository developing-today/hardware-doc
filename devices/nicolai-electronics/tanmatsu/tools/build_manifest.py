#!/usr/bin/env python3
"""Build acquisition/manifest.json for the Tanmatsu research tree.

Every artifact here came from one of ten pinned git repositories or from
badge.team / solder.party documentation pages. Rather than hashing each file as
an independent download, artifacts are grouped by *source*, because that is the
unit you actually re-acquire. Per-file SHA-256 is still recorded so integrity
can be verified after a clean clone. Executed 2026-08-24.
"""
import hashlib, json, os, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOS = {  # repo -> (commit, licence, what it provided)
 "tanmatsu-hardware": ("640805dd4304f4bfaac24965f8eecf81bec97bf1","CERN-OHL-P","KiCad design, schematic.pdf, production BOM/positions/IPC netlist"),
 "tanmatsu-documentation": ("bd3ded51548433bd7d614f5607b7d36f5eed61fa","none","Sphinx/MyST documentation source"),
 "tanmatsu-mechanical": ("c623cd548c9cafb95773624fe775001984449a89","CERN-OHL-P","Case/spacer/speaker-adapter FreeCAD + STEP"),
 "tanmatsu-coprocessor-firmware": ("57ff2505d7256b55cc5fea4eb9be10a9a077bafa","MIT","CH32V203 firmware: keyboard.c, i2c_registers.h, hardware.h"),
 "esp32-component-tanmatsu-coprocessor": ("6eea3735346ee1b689898c77e500fb1d0c4e024e","none","Coprocessor driver header (keymap struct)"),
 "esp32-component-tanmatsu-wifi": ("d8ce0bf106141d6bccf4cb9a927bd494facc31af","MIT","Wi-Fi wrapper"),
 "tanmatsu-radio": ("cb4e38c02aa8ad533fd17b24921c4ca4848eeaf6","Apache-2.0","ESP32-C6 radio firmware"),
 "tanmatsu-launcher": ("20022fce316d768a1ff966b973ee2127511713f5","MIT","Launcher firmware"),
 "tanmatsu-template": ("907fb9657658995efab210b754f28a3ace06d03a","none","Template app"),
 "app-repository": ("f83e1559553497903c083525a10d2aaf53344377","none","57 app metadata.json files"),
}
BSP = ("badgeteam/esp32-component-badge-bsp","9037f0e","MIT","Board support package: tanmatsu target + Kconfig")
PUPPET = ("solderparty/i2c_puppet","f085518","MIT","BlackBerry keyboard firmware + protocol README")

def sha(p):
    h = hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda: f.read(1<<20), b""): h.update(c)
    return h.hexdigest()

def classify(rel):
    if rel.startswith("artifacts/badge-team-docs/"): return "badge.team"
    if rel.startswith("artifacts/solder-party-docs/"): return "solder.party"
    if rel.startswith("artifacts/source-snapshots/i2c_puppet"): return "i2c_puppet"
    if rel.startswith("artifacts/source-snapshots/badge-bsp"): return "badge-bsp"
    if rel.startswith("artifacts/source-snapshots/tanmatsu-documentation"): return "tanmatsu-documentation"
    if rel.startswith("artifacts/mechanical"): return "tanmatsu-mechanical"
    if rel.startswith(("artifacts/schematics","artifacts/production")): return "tanmatsu-hardware"
    if rel.startswith("artifacts/app-repository"): return "app-repository"
    if rel.startswith("artifacts/source-snapshots/"): return "tanmatsu-coprocessor-firmware"
    return "unknown"

files=[]
for dp,_,fs in os.walk(os.path.join(ROOT,"artifacts")):
    for f in sorted(fs):
        p=os.path.join(dp,f); rel=os.path.relpath(p,ROOT)
        files.append({"path":rel,"bytes":os.path.getsize(p),"sha256":sha(p),"source":classify(rel)})

sources={}
for name,(commit,lic,desc) in REPOS.items():
    sources[name]={"kind":"git","url":f"https://github.com/Nicolai-Electronics/{name}",
      "commit":commit,"license":lic,"provides":desc,
      "reacquire":f"git clone https://github.com/Nicolai-Electronics/{name} && git -C {name} checkout {commit}",
      "reacquisition":"automatic"}
sources["badge-bsp"]={"kind":"git","url":f"https://github.com/{BSP[0]}","commit_short":BSP[1],"license":BSP[2],
  "provides":BSP[3],"reacquire":f"git clone --depth 1 https://github.com/{BSP[0]}","reacquisition":"automatic"}
sources["i2c_puppet"]={"kind":"git","url":f"https://github.com/{PUPPET[0]}","commit_short":PUPPET[1],"license":PUPPET[2],
  "provides":PUPPET[3],"reacquire":f"git clone --depth 1 https://github.com/{PUPPET[0]}","reacquisition":"automatic"}
sources["badge.team"]={"kind":"web","url":"https://badge.team/docs/badges/konsool/","license":"unknown",
  "provides":"42 Konsool documentation pages, text-extracted","enumerate":"https://badge.team/sitemap.xml (filter /konsool/)",
  "note":"Server-rendered Hugo site; plain curl with a browser User-Agent works. Stored as extracted text, not original HTML.",
  "reacquisition":"automatic"}
sources["solder.party"]={"kind":"web","url":"https://www.solder.party/docs/","license":"unknown",
  "provides":"7 product documentation pages, text-extracted",
  "note":"Server-rendered Hugo site; /docs/ index enumerates every product.","reacquisition":"automatic"}

man={"device":"nicolai-electronics/tanmatsu","generated":datetime.date.today().isoformat(),
 "generator":"tools/build_manifest.py",
 "note":("All artifacts derive from pinned git commits or from server-rendered documentation "
         "pages. No artifact required authentication, paywall or manual steps. Web pages are "
         "stored as extracted plain text (see 'note' per source) so they are diffable; the "
         "original HTML was not retained."),
 "redistribution_review":{
   "CERN-OHL-P":"hardware + mechanical design files - permissive, redistribution allowed, attribution required",
   "MIT":"firmware, BSP, i2c_puppet - redistribution allowed",
   "Apache-2.0":"radio firmware - redistribution allowed",
   "none":("tanmatsu-documentation, tanmatsu-template, app-repository and "
           "esp32-component-tanmatsu-coprocessor have NO licence file. Text is quoted and "
           "snapshotted for research; wholesale redistribution is legally unclear. FLAGGED FOR REVIEW."),
   "web-docs":"badge.team and solder.party pages carry no stated licence. Stored as extracted text for research use. FLAGGED FOR REVIEW.",
   "branding":"Nicolai Electronics / Tanmatsu names, logos and artwork are ALL RIGHTS RESERVED and explicitly excluded from CERN-OHL-P."},
 "sources":sources,
 "file_count":len(files),"total_bytes":sum(f["bytes"] for f in files),
 "files":files}
os.makedirs(os.path.join(ROOT,"acquisition"),exist_ok=True)
json.dump(man,open(os.path.join(ROOT,"acquisition","manifest.json"),"w"),indent=1)
print(f"{len(files)} files, {sum(f['bytes'] for f in files)/1024/1024:.1f} MiB")
from collections import Counter
for k,v in Counter(f["source"] for f in files).most_common(): print(f"  {v:4d}  {k}")
