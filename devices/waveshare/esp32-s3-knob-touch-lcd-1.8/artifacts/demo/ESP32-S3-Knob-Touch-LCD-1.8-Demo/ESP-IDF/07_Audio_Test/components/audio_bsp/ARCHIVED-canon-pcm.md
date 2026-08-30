# Archived: `canon.pcm` — raw audio test sample

Moved out of the repository on **2026-08-30**. Not deleted. 

> **These files are absent from the repository.** They are not symlinks and not placeholders-in-place —
> the paths simply do not exist here any more. This record is the only thing standing in for them,
> which is why it carries a SHA-256, a byte count and a pinned reacquisition URL for every file.
>
> The archive copy is a **convenience for whoever holds it, not part of the contract**: it lives
> outside the repository at a machine-local path, so nothing here may depend on it.

| | |
|---|---|
| Original path | `ESP-IDF/07_Audio_Test/components/audio_bsp/canon.pcm` |
| **SHA-256** | `8e0693da7412f2743b07b285bc46fca879e31222d1db521a8bd6a36e7eeffa41` |
| **Size** | **5,297,084 bytes** (5.05 MiB) |
| Archive path | `archive/hardware-doc/devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/ESP-IDF/07_Audio_Test/components/audio_bsp/canon.pcm` |

## Why this one

It was **54 % of the entire remaining demo tree** and the **only file in it cited by no authored
document**. Of 140 files in this demo, 139 are referenced by path somewhere in ``;
this was the exception. It is a media asset, not board-specific code — nothing about the hardware
can be learned from it that `audio_bsp.c` does not state directly.

Everything else in this demo stays. The tree had already had **LVGL 8.4.0 and SensorLib removed**
(see [`../../../../vendored-deps/README.md`](../../../../vendored-deps/README.md)); what remains is
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

> ⚠ **This is the least reliably reacquirable source in the repository.** The ZIP is
> vendor-hosted, **unversioned, untagged and carries no LICENSE file anywhere in its 5,052
> entries**. Waveshare rotate and silently update these archives, and the wiki sits behind a WAF
> that required a MediaWiki-API workaround to read. If the hash above does not match, you have a
> different revision of the demo — which is itself worth recording.

## Restoring a file

Re-fetch it from the pinned upstream in the Reacquisition section above and verify against the
SHA-256 in the table. If you happen to hold the local archive, copying from the archive root shown
above is faster and gives the identical bytes.

Removing this file is a **local modification** to a vendored snapshot: upstream has it present at
the pinned commit. Reconcile against the hash above before concluding a diff means something.
