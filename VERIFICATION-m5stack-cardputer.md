# Verification — M5Stack Cardputer family pass

**Date 2026-09-04.** Subject: [Cardputer ADV](devices/m5stack/cardputer-adv/README.md) (full
depth) plus [v1.0](devices/m5stack/cardputer-v1.0/README.md),
[v1.1](devices/m5stack/cardputer-v1.1/README.md),
[Mesh Kit](devices/m5stack/cardputer-mesh-kit/README.md),
[CardputerZero](devices/m5stack/cardputer-zero/README.md).

*(This file follows the convention of `VERIFICATION-m5stack-papermono.md` and
`VERIFICATION-xiao-esp32s3-sense.md`. A line linking it from the umbrella `README.md` is staged
in [`scratch/m5stack-cardputer/index-fragments.md`](scratch/m5stack-cardputer/index-fragments.md)
because that file was out of scope for this session.)*

## Result

| Check | Result |
|---|---|
| Authored Markdown files | **48** across 5 device records and 10 component records |
| Relative links resolving | **331 / 331** ✅ (one batch of 3 fixed during verification) |
| JSON schemas valid | 3 / 3 ✅ (`acquisition/manifest.json`, `media/manifest.json`, `examples/catalog.json`) |
| Artifact SHA-256 + byte size vs manifest | **6 / 6 OK, 0 failures** ✅ |
| File type validated by **magic bytes** | ✅ `%PDF-1` ×2, `<!doct` ×2 (this host has no `file`) |
| Failed downloads retained under a misleading extension | **none** — the one dead PNG URL was checked by magic bytes and deleted, and is recorded as dead in three places |
| PDF text layer validated before transcription | ✅ positive control: ADV layer yields `TCA8418RTWR`/`ES8311`/`NS4150B`/`BMI270`, v1.1 layer yields `74HC138`/`NS4168`/`SPM1423HM4H-B`, both matching the corresponding product pages' PinMap tables |
| Every transcribed value also read from a **rendered** sheet crop | ✅ 10 crops, arguments recorded so each is reproducible |
| Protected files modified | **none** (root `README.md`, `devices/README.md`, `components/README.md`, `vendors/README.md`, `artifact-manifest.md`, `software/README.md`, `guides/markets/*`, `devices/m5stack/papermono*` all untouched by this session) |
| Concurrent sessions' trees modified | **none** — proposed additions staged in `index-fragments.md` |
| Anything staged or committed | **no** — everything is untracked, awaiting review |

## Findings that survived verification

* **The ADV keyboard matrix is electrically identical to the v1.0/v1.1 matrix.** Same 56
  switches, same `Y0..Y7` nets, same `R27`–`R34` 22 Ω. Only the scanner changed (74HC138 →
  TCA8418), and the two drivers' coordinate maths were shown algebraically equivalent.
* **The v1.0 and v1.1 mainboard schematics are byte-identical** — `6016c1fe…`, served under both
  product ids `481` and `1127`.
* **Cardputer v1.1 already uses Stamp-S3A**, not StampS3. A widely repeated community belief
  refuted from M5Stack's own comparison table.
* **`G13` is host TX and `G15` is host RX** on the CAP header. Four sources agree; the Cardputer
  Mesh Kit page's EXT table is wrong and contradicts its own Cap-Bus table.
* **The Stamp-S3A's `U4` is labelled `JW5712`** on the published sheet — correcting a concurrent
  session's "part number not established". Verified against a hash-matched vendor render.
* Two **live driver defects** in `M5Unified`'s ES8311 callbacks, one of which has already
  propagated into Bruce.

## Deliberate limitations, stated rather than hidden

* **No hardware.** Every build/run status in `examples/catalog.json` is `not-tested`, and no
  measurement of any kind appears in `performance.md`.
* **Certification is "not established", not "absent"** — `/en/certification` was not fetched with
  the positive control the vendor guide requires.
* **Chinese and Japanese sources were not searched.** For a Shenzhen vendor with a large Japanese
  community, that is the largest single gap.
* Three unresolved items are recorded in
  [`gaps-and-conflicts.md`](devices/m5stack/cardputer-adv/gaps-and-conflicts.md): the Grove
  SCL/SDA orientation, the BMI270 interrupt routing, and a `+3.3V` feedback divider whose
  arithmetic does not resolve. Each names what would settle it.

## Two lessons worth carrying forward

1. **Altium PDFs hide the readable text in a Form XObject.** A parser that reads only the
   `CO`/`PI`/`NL` marker layer returns hundreds of plausible-looking "words" and **none** of the
   part numbers. It fails silently. This cost two sessions independently — see
   `gaps-and-conflicts.md` §C7.
2. **`sha256sum` embeds the path you give it**, so the same 33 files produced three different
   tree digests from three working directories during this very verification. The recorded recipe
   now pins the working directory as well as the locale.
