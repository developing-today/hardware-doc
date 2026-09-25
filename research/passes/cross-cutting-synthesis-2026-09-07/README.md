# scratch/cross-cutting-synthesis

Working notes for the cross-cutting synthesis pass of **2026-09-07**.

## What this pass produced

Four new authored files, no artifacts fetched, nothing built or flashed:

| File | Purpose |
|---|---|
| `guides/markets/handheld-and-eink-device-landscape-2026-09.md` | Buyer-oriented landscape across every device record |
| `guides/hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md` | Capability-by-capability feasibility for LoRa / NFC / RGB sidelight |
| `devices/xteink/firmware-ecosystem.md` | Hardware-side map of CrossPoint / FreeInk / CrossPlay |
| `guides/hardware/soc-choice-for-battery-eink-devices.md` | SoC selection for battery e-ink handhelds |

Plus append-only cross-reference sections in a small number of existing
`comparisons-and-recommendations.md` files and `devices/xteink/README.md`.

## Sources

**No network retrieval was performed.** Every claim in the four documents is read
out of records already in this repository, and cites the record it came from.
Where a record itself labels something `inferred`, `reported-working` or
`not-tested`, that label is carried through rather than upgraded.

## Notable negative results recorded during the pass

- **No component record in this repository states an ESP32-C3 or ESP32-S3
  deep-sleep current.** `components/espressif/esp32-c3/README.md` has no power
  table at all and its datasheet is `not-attempted`;
  `components/espressif/esp32-s3r8/README.md` covers radio, PSRAM and PIE but no
  sleep figures. Every sleep number available in this repository is a
  *board*-level vendor claim under unstated conditions. This is why
  `guides/hardware/soc-choice-for-battery-eink-devices.md` cannot rank the SoCs
  on deep-sleep current and says so.
- **No Xteink device has a published battery capacity except the X3** (650 mAh,
  from a teardown photo caption). X4, X4 Pro and X4 Classic are all unknown, so
  no runtime comparison is possible inside that family.
- **No e-ink device in this repository has a measured refresh-power or
  battery-life figure from anyone.** Vendor refresh *times* exist; power does not.
- `guides/markets/device-comparison-matrix.md` (2026-08-30) covers fourteen
  devices and **predates** the Xteink, M5Stack Cardputer/PaperMono/Cap and LilyGO
  sessions. It was read, not edited; the new landscape file links to it one-way,
  per the task's constraint.

## Files touched outside `guides/`, `devices/xteink/firmware-ecosystem.md`

Append-only "cross-reference" sections, each headed
`## Cross-references added 2026-09-07`. **Nothing was deleted or reworded**, and
every edit was performed as `oldString = existing tail` → `newString = existing
tail + new section`, so deletion was impossible by construction.

| File | Lines before → after |
|---|---|
| `devices/xteink/README.md` | 206 → 221 |
| `devices/xteink/x3/comparisons-and-recommendations.md` | 103 → 126 |
| `devices/xteink/x4/comparisons-and-recommendations.md` | 109 → 133 |
| `devices/xteink/x4-pro/comparisons-and-recommendations.md` | 105 → 129 |
| `devices/lilygo/t-display-k230/comparisons-and-recommendations.md` | 106 → 129 |
| `devices/lilygo/t-display-s3/comparisons-and-recommendations.md` | 140 → 164 |
| `devices/m5stack/cardputer-adv/comparisons-and-recommendations.md` | 153 → 186 |
| `devices/m5stack/dinmeter/comparisons-and-recommendations.md` | 200 → 219 |
| `devices/m5stack/dinmeter-v1.1/comparisons-and-recommendations.md` | 66 → 86 |

Each file was tested with `find <file> -mmin -15` immediately before editing; none
returned. **`devices/lilygo/t-display-s3/comparisons-and-recommendations.md` was
last written 53 minutes earlier by an active sibling session** — outside the
15-minute rule this pass was given, but inside the skill's one-hour
"actively owned" heuristic. The append was made at end-of-file only, is flagged as
such inside the file, and was re-verified present afterwards.

**Not touched, deliberately:** `README.md`, `devices/README.md`,
`components/README.md`, `vendors/README.md`, `artifact-manifest.md`, anything
under `software/`, anything under `devices/m5stack/papermono*` (including its own
`comparisons-and-recommendations.md`), `guides/README.md`,
`guides/hardware/README.md` and `guides/markets/README.md`. A sibling session was
observed writing several of these during this pass; **their changes were left
alone and no index was repaired unilaterally.** The three new guides are therefore
**not yet linked from any index** — that is a known, deliberate gap for whoever
owns those indexes.

**No state-changing git command was run.** `HEAD` is unchanged; nothing was
staged, stashed, committed or reverted by this pass. The 91 staged files visible in
`git status` predate it and belong to other sessions.

---

# Promoted into the repository — 2026-09-20

*Appended. Everything above is preserved as written.*

This document was `scratch/cross-cutting-synthesis/README.md`. It was moved into the repository on
2026-09-20, unchanged (1 file, 4,787 bytes, digest
`dc598e25467377cc4de3ae615ac15e0f9f42cd64954fe9e62f72c82011b06ebd`), because it is **authored
analysis that exists nowhere else**.

Specifically, its *"Notable negative results"* section is the only place in this knowledge base
that records:

- that **no component record states an ESP32-C3 or ESP32-S3 deep-sleep current**, which is why
  [`guides/hardware/soc-choice-for-battery-eink-devices.md`](../../../guides/hardware/soc-choice-for-battery-eink-devices.md)
  cannot rank SoCs on that axis and says so;
- that **no Xteink device has a published battery capacity except the X3**, so no runtime
  comparison inside that family is possible;
- that **no e-ink device here has a measured refresh-power or battery-life figure from anyone** —
  vendor refresh *times* exist, power does not.

Negative results of that kind are the first thing lost when a working directory is discarded, and
the guides that depend on them would then look like unexplained omissions.

The pass performed **no network retrieval**. Every claim in the four documents it produced is read
out of records already in this repository, carrying through each source record's own
`inferred` / `reported-working` / `not-tested` label rather than upgrading it.

Relocation map for every subject:
[`SCRATCH-RELOCATION-2026-09-20.md`](../../../SCRATCH-RELOCATION-2026-09-20.md).
