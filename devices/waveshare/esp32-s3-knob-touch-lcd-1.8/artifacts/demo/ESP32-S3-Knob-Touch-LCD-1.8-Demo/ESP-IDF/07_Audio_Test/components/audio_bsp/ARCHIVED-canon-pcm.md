# Archived: `canon.pcm` — raw audio test sample

Moved out of the repository on **2026-08-30**. Not deleted. 

> **A symlink now stands in for each file at its original path**, pointing through this repo's
> `archive/` link. With the archive present the paths resolve and the tree behaves as though
> nothing moved; without it they dangle, and this record is what remains.
>
> That is why this record still carries a SHA-256, a byte count and a pinned reacquisition URL
> for every file: **the archive copy is a convenience for whoever holds it, not part of the
> contract.** It lives outside the repository at a machine-local path, so nothing here may
> depend on it, and the symlinks are a local nicety rather than a substitute for these hashes.

| | |
|---|---|
| Original path | `ESP-IDF/07_Audio_Test/components/audio_bsp/canon.pcm` |
| **SHA-256** | `8e0693da7412f2743b07b285bc46fca879e31222d1db521a8bd6a36e7eeffa41` |
| **Size** | **5,297,084 bytes** (5.05 MiB) |
| Archive path | `archive/devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/ESP-IDF/07_Audio_Test/components/audio_bsp/canon.pcm` |

## Why this one

It was **54 % of the entire remaining demo tree** and the **only file in it cited by no authored
document**. Of 140 files in this demo, 139 are referenced by path somewhere in the knowledge base;
this was the exception. It is a media asset, not board-specific code — nothing about the hardware
can be learned from it that `audio_bsp.c` does not state directly.

Everything else in this demo stays. The tree had already had **LVGL 8.4.0 and SensorLib removed**
(see [`../../../../../../vendored-deps/README.md`](../../../../../../vendored-deps/README.md)); what remains is
Waveshare BSP code, examples and `sdkconfig` snapshots, all heavily cited.

## Format — derived from the source, not from the file

`canon.pcm` is **headerless raw PCM**. The parameters are not in the file; they are in the driver
that plays it, and would be lost with it. Recorded here so they are not:

| Property | Value | Established by |
|---|---|---|
| Sample rate | **44,100 Hz** | `audio_bsp.c:22` — `#define I2S_SAMPLE_RATE 44100` |
| Bit depth | **16-bit** | `audio_bsp.c:23` — `I2S_DATA_BIT_WIDTH_16BIT` |
| Channels | **Stereo** | `audio_bsp.c:25/27` — `I2S_SLOT_MODE_STEREO` |
| Duration | **exactly 30.0 s** | 5,297,084 ÷ (44100 × 2 ch × 2 B) = 30.03 s |
| Container | none — raw interleaved LE samples | linked in via `_binary_canon_pcm_start` |

> The exact 30-second result is what confirms **stereo**. The same byte count read as 16-bit *mono*
> would be 60.1 s — not a round number, and inconsistent with a deliberately prepared demo clip.

Content is Pachelbel's *Canon in D* — public domain as a composition; the specific recording's
provenance is unstated by Waveshare.

## Playing or verifying it

```bash
# play the archived copy
ffplay -f s16le -ar 44100 -ch_layout stereo canon.pcm

# convert to WAV
ffmpeg -f s16le -ar 44100 -ac 2 -i canon.pcm canon.wav
```

## Reacquisition

Only distributed inside Waveshare's demo ZIP — there is no standalone URL.

```bash
curl -fsSL "https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip" \
  -o demo.zip
unzip -j demo.zip '*/ESP-IDF/07_Audio_Test/components/audio_bsp/canon.pcm'
sha256sum canon.pcm   # expect 8e0693da7412f2743b07b285bc46fca879e31222d1db521a8bd6a36e7eeffa41
```

> ⚠ **Waveshare's own copy is weakly sourced.** The ZIP is vendor-hosted, **unversioned,
> untagged and carries no LICENSE file anywhere in its 5,052 entries**. Waveshare rotate and
> silently update these archives, and the wiki sits behind a WAF that required a MediaWiki-API
> workaround to read. If the hash does not match, you have a different revision of the demo —
> itself worth recording.

### Independent mirror — verified byte-identical

A third party mirrored the whole demo tree to GitHub, which gives this file something the
vendor path does not: a **direct, unauthenticated, single-request URL under a different
custodian**.

```bash
curl -fsSL "https://raw.githubusercontent.com/mylesdebastion/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-Demo/HEAD/ESP-IDF/07_Audio_Test/components/audio_bsp/canon.pcm" \
  -o canon.pcm
sha256sum canon.pcm   # 8e0693da7412f2743b07b285bc46fca879e31222d1db521a8bd6a36e7eeffa41
```

**Verified 2026-08-30**, not merely cited: fetched, and the bytes match this record's SHA-256
and the local archive copy exactly — 5,297,084 bytes, `8e0693da…ffa41` from all three.

- Mirror repository: <https://github.com/mylesdebastion/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-Demo>
- Two further third-party trees carrying the same demo, unverified here but worth trying if the
  above disappears:
  <https://github.com/nkinnan/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8_and_Guition-K5-Knob-Series-JC3636K518>
  and <https://github.com/EmbeddedWizardGUI/ESP32-S3-Knob-Touch-LCD-1.8-EN>

> A mirror is a **copy of unknown provenance**, not an authority. It is trustworthy here only
> because the hash matches; if a future fetch disagrees with the SHA-256 above, believe the hash
> and treat the mirror as having drifted. Nothing guarantees a third party keeps the repository.

### Vendor rediscovery paths

Both on a different host from `files.waveshare.com` (verified 200, browser UA, 2026-08-30) —
but the **same custodian**, so this is redundancy of path, not of party:

- Wiki page, *Demo* / *Resources*: <https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8>
- Product page: <https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm>

## Restoring a file

Re-fetch it from the pinned upstream in the Reacquisition section above and verify against the
SHA-256 in the table. If you happen to hold the local archive, copying from the archive root shown
above is faster and gives the identical bytes.

Removing this file is a **local modification** to a vendored snapshot: upstream has it present at
the pinned commit. Reconcile against the hash above before concluding a diff means something.
