# PDM microphone — Seeed XIAO ESP32S3 Sense — **RESOLVED**

> ✅ **This part was identified on 2026-08-24.** It is a **MEMSensing MSM261D3526H1CPM**.
>
> **Superseded by → [`components/memsensing/msm261d3526h1cpm`](../../../memsensing/msm261d3526h1cpm/README.md)**

## How it was resolved

The part was unidentified for most of this research pass because Seeed appeared to publish no schematic for the Sense daughterboard.

In fact the file distributed as **"XIAO ESP32S3 Exp. Board v1.0"** *is* the Sense sensor board — not the separate OLED/RTC/buzzer expansion accessory that the name suggests. Parsing its EAGLE XML gave, unambiguously:

```
MIC1    MSM261D3526H1CPM    MIC-MSM261D3526H1CPM    (library: Making)
```

That confirms the part number which had circulated online for years without primary evidence.

**Lesson worth keeping:** the misleading filename cost most of a research pass, and an FCC-filing detour that did not resolve it either. Seeed's "Exp. Board" naming does not distinguish the Sense sensor board from the unrelated expansion accessory. **Parse the file; do not trust the label.** Recorded in the [Seeed vendor guide](../../../../vendors/seeed-studio/README.md).

This stub is retained so existing links to the unidentified path continue to resolve.
