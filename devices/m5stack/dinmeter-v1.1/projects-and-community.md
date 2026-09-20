# DinMeter v1.1 — projects and community

**Every project, firmware port, forum attempt and social trace found for this device family is
catalogued in [`../dinmeter/projects-and-community.md`](../dinmeter/projects-and-community.md).**
It applies to v1.1 without amendment, because **no project anywhere distinguishes the two
revisions**.

---

## The v1.1-specific finding: nothing is v1.1-specific

Searched 2026-09-04 (method in [`research-log.md`](research-log.md) §1):

| Looked for | Result |
|---|---|
| A repository targeting DinMeter v1.1 specifically | **none** |
| A board file, `#ifdef` or build flag distinguishing the revisions | **none** — `bmorcelli/Launcher`'s `m5stack-dinmeter` target, `espressif/esp-board-manager`'s `m5stack_dinmeter`, and `m5stack/M5DinMeter` all make no distinction |
| A community project mentioning Stamp-S3A on a DinMeter | **none** |
| An M5Unified issue or PR about the GPIO38 RGB-LED change | **none found** |
| Reddit discussion of v1.1 beyond the launch post | **none** |
| M5Stack forum threads | **inaccessible** — search API HTTP 401, HTML is a NodeBB JS shell |

**One relevant social artefact exists for v1.1:**

| Date | Sub | Score | Comments | Post | Evidence type |
|---|---|---:|---:|---|---|
| **2026-01-30** | r/M5Stack | 22–23 | **1** | ["Check out what's new this week!"](https://old.reddit.com/r/M5Stack/comments/1qr0ju2/check_out_whats_new_this_week/) — M5Stack's own weekly-products post announcing DinMeter v1.1 alongside the LLM-8850 Kit | **marketing** (vendor-posted) |

Its body text is the same paragraph as the product page. It corroborates the launch date, which
independently matches the shop listing's `created_at`. **That is the entire public discussion of
this revision.**

## Why that matters

Compatibility is a good thing — but it means **nobody has hit the RGB-LED change yet, or if they
have, they have not written it down where it is indexable**. The prediction in
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) V1 is unconfirmed *and* uncontradicted, and it
will stay that way until someone with a v1.1 unit tries it.

If you are that person, the test is two lines and ten minutes, and it would be the single most
useful contribution anyone could make to this record.

## Ecosystem status (unchanged from v1.0)

| Platform | DinMeter support |
|---|---|
| `bmorcelli/Launcher` (★2054, MIT) | **yes** — CI-built target, ships as `Launcher-m5stack-dinmeter.bin` via M5Burner |
| `espressif/esp-board-manager` | **yes** — full ESP-IDF board definition |
| `m5stack/uiflow-micropython` (UiFlow2) | **yes** |
| `viniciusbo/m5-palnagotchi` (★81) | yes, as one of many targets |
| **ESPHome** | **no** — 0 code-search hits |
| **Tasmota** | **no** — 0 |
| **Meshtastic** | **no** — 0 |
| `pr3y/Bruce` (upstream Bruce) | **no** — the port is in `bmorcelli/Launcher`, not Bruce |

→ [`../dinmeter/projects-and-community.md`](../dinmeter/projects-and-community.md) for the full
catalogue with per-project evidence types, and
[`../dinmeter/examples/catalog.json`](../dinmeter/examples/catalog.json) for dispositions.
