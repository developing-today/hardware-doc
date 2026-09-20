#!/usr/bin/env python3
"""Adjudicate the badge.team E-numbering conflict using fabrication data.

Two vendor pages disagree about which ESP32-P4 GPIO carries each E-numbered
expansion pin. This resolves it from the IPC-D-356 fabrication netlist (exported
from the actual PCB) plus the ESP32-P4 datasheet pin table -- neither of which
is prose, and neither of which can drift from the copper.

Executed 2026-08-24.
"""
import os, sys, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p4_pinmap import PINS
from parse_ipc_netlist import parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
nets = parse(os.path.join(ROOT, "artifacts/production/netlist.ipc"))

# Claim A - Nicolai Electronics connector page AND badge.team back-expansion page
CONNECTOR = {"E0":36,"E1":0,"E2":6,"E3":46,"E4":47,"E5":48,"E6":45,
             "E7":7,"E8":54,"E9":49,"E10":53,"E11":52,"E12":51,"E13":50}
# Claim B - badge.team ESP32-P4 IC page
IC_PAGE   = {"E2":0,"E1":6,"E7":49,"E8":50,"E9":51,"E10":52,"E11":53,"E12":54}

print(f"{'net':<5} {'U7 pin':>7}  {'actual':<8} {'connector':<10} {'IC page':<9} verdict")
print("-"*62)
a_ok=a_bad=b_ok=b_bad=0
for e in [f"E{i}" for i in range(14)]:
    pads = nets.get(e, [])
    u7 = [p for r,p in pads if r == "U7"]
    if not u7:
        print(f"{e:<5} {'-':>7}  (no U7 pad found)"); continue
    sig = PINS.get(int(u7[0]), "?")
    actual = int(sig[4:]) if sig.startswith("GPIO") else None
    ca, cb = CONNECTOR.get(e), IC_PAGE.get(e)
    va = "ok" if ca == actual else ("MISMATCH" if ca is not None else "-")
    vb = "ok" if cb == actual else ("MISMATCH" if cb is not None else "-")
    if ca is not None: a_ok += va=="ok"; a_bad += va!="ok"
    if cb is not None: b_ok += vb=="ok"; b_bad += vb!="ok"
    others = [f"{r}.{p}" for r,p in pads if r not in ("U7","J7")]
    extra = ("   also: " + ", ".join(others)) if others else ""
    print(f"{e:<5} {u7[0]:>7}  {sig:<8} {str(ca):<10} {str(cb):<9} A={va} B={vb}{extra}")

print("-"*62)
print(f"connector page : {a_ok} correct, {a_bad} wrong")
print(f"IC page        : {b_ok} correct, {b_bad} wrong")
