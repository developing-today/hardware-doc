# DinMeter — community

This device's community coverage is documented in full at
**[`projects-and-community.md`](projects-and-community.md)**, which is the single catalogue of
repositories, firmware ports, forum attempts and social evidence, with each item labelled by
evidence type (demonstrable project · reproduced documentation · firsthand report · hearsay ·
marketing).

This page exists so that the skill's standard filename resolves, and to state the headline
without making the reader open another file.

---

## The one-paragraph summary

**There is very little public community around the DinMeter, and that is a measured finding
rather than a search failure.** On 2026-09-04 a GitHub repository search
(`DinMeter in:name,description,readme`, 50 results/page) returned **19 repositories**, of which
**13** genuinely target the device; `old.reddit.com/search.json` across four query forms and
~200 inspected results returned **exactly one** relevant post — M5Stack's own launch
announcement, with one comment; and **ESPHome, Tasmota and Meshtastic each returned zero**
code-search hits. M5Stack's own forum could **not** be enumerated (its search API returns HTTP
401 and its HTML search page is a JavaScript shell), so it is a *blocked* source rather than an
empty one, and it is the largest single gap in this record.

## The three things worth knowing

1. **`bmorcelli/Launcher` (★2054, MIT) is the only substantial third-party firmware.** The
   DinMeter is a first-class board target in its release CI and ships as
   `Launcher-m5stack-dinmeter.bin` via M5Burner. Its board file is also an *independent*
   corroboration of the display pins, the GRAM offsets, the battery-divider ratio and the
   absence of PSRAM — from an author with no reason to copy M5Stack's table wrongly.
2. **The projects that exist are single-purpose instruments** — a ceramic-kiln PID controller, a
   power-tool battery analyser, a heater controller, a TOTP authenticator, a BLE volume knob.
   Nine of thirteen are one-person tools. That is the product being used exactly as its
   panel-mount, 6–36 V design intends.
3. **Do not expect home-automation firmware.** No ESPHome, no Tasmota, no Meshtastic. If you want
   Home Assistant integration you will write it, or use M5Stack's own UiFlow2 route.

## Prevalence caveat

"Almost no community" describes *public, indexed* activity on GitHub and Reddit on 2026-09-04.
The vendor forum was inaccessible, and Chinese-language platforms (Bilibili, CSDN, Taobao Q&A)
and video sources were **declared exclusions** and not searched. Do not read this as "nobody uses
it" — read it as "there is no public scene to lean on when you get stuck."

→ **[`projects-and-community.md`](projects-and-community.md)** for the full catalogue, the
per-project evidence types, the exact queries, and the negative results.
