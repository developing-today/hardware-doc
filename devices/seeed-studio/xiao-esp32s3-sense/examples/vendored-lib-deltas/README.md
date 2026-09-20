# Vendored dependency deltas

Some of the example projects in [`selected/`](../selected/) ship copies of third-party libraries inside the project tree rather than resolving them from a package manager. Those copies are a hazard: they look like ordinary source, but they are frozen at whatever upstream looked like on the day the author zipped them, and they occasionally contain edits that exist nowhere else.

This directory records, for every vendored dependency found in this research pass, **whether it is an unmodified upstream snapshot or a modified fork**, and captures the delta as a small patch so the information survives even if the bulky copy is ever archived out.

Generated **2026-08-24** with [`../tools/diff_vendored_lib.py`](../../../../../tools/diff_vendored_lib.py). Method: fetch the current upstream default branch, `diff -ruN` against the vendored tree, normalise paths, and record the upstream zip's SHA-256 so the comparison is reproducible.

> **A non-empty diff does not prove local modification.** Upstream keeps moving; a vendored copy is usually just older. The verdict column below reflects reading the actual hunks, not merely the presence of a diff.

## Findings

| Vendored copy | Upstream | Files differing | Verdict | Patch |
|---|---|---:|---|---|
| `XIAO-ESP32S3-Geolocation/libraries/QuickDebug-master.zip` | [gmag11/QuickDebug](https://github.com/gmag11/QuickDebug) | 0 | **Identical to upstream master** | [`QuickDebug.patch`](QuickDebug.patch) |
| `.../TJpg_Decoder-master.zip` | [Bodmer/TJpg_Decoder](https://github.com/Bodmer/TJpg_Decoder) | 3 | **Older upstream release, not a fork** | [`TJpg_Decoder.patch`](TJpg_Decoder.patch) |
| `.../WifiLocation-master.zip` | [gmag11/WifiLocation](https://github.com/gmag11/WifiLocation) | 2 | **Older upstream release, not a fork — but functionally broken today** | [`WifiLocation.patch`](WifiLocation.patch) |

**None of the three is a patched fork.** All are plain upstream snapshots. That is the good outcome: nothing unique is at risk, and each could in principle be replaced by a package-manager dependency. They are nonetheless **retained in place** — together they are only ~352 KB, and reproducing an exact *historical* `master` snapshot (as opposed to a tagged release) is not straightforward, so keeping the bytes costs little and removes a reproducibility risk.

## What the diffs actually say

### QuickDebug — no change

Byte-identical to current upstream `master`. Safe to substitute with the upstream library at any time.

### TJpg_Decoder — v1.0.9 vendored, v1.1.0 upstream

The vendored `library.properties` declares `version=1.0.9`; upstream is now `1.1.0`. The only code change is an upstream **bug fix** in `src/tjpgd.c`:

```diff
-					*pix++ = (uint8_t)*py++;			/* Get and store a Y value as grayscale */
+					if (JD_FASTDECODE >= 1) {
+						*pix++ = BYTECLIP(*py++);	/* Get and store a Y value as grayscale */
+					} else {
+						*pix++ = *py++;				/* Get and store a Y value as grayscale */
+					}
```

This adds saturation clipping (`BYTECLIP`) on the grayscale path when the fast decoder is enabled. Without it, out-of-range luma values wrap instead of clamping, producing speckled artefacts in grayscale JPEG decodes. If you reuse the vendored 1.0.9 copy for grayscale decoding, **prefer upstream 1.1.0**; for the colour path used by the Geolocation example it makes no difference.

### WifiLocation — vendored copy contains an **expired root certificate**

This is the finding worth acting on. The vendored copy pins the Bing Maps geocoding TLS chain to a hardcoded root CA:

```diff
-static const char CyberTrustRootCA[] PROGMEM = R"EOF(
-MIIDdzCCAl+gAwIBAgIEAgAAuTANBgkqhkiG9w0BAQUFADBaMQswCQYDVQQGEwJJ
… Baltimore CyberTrust Root …
+static const char DigiCertRootCA[] PROGMEM = R"EOF(
+MIIDjjCCAnagAwIBAgIQAzrx5qcRqaC7KGSxHQn65TANBgkqhkiG9w0BAQsFADBh
… DigiCert Global Root G2 …
```

The vendored version embeds the **Baltimore CyberTrust Root**, whose certificate carries `notAfter = 2025-05-12`. Upstream has since migrated to **DigiCert Global Root G2** (valid to 2038-01-15).

Consequence: **the vendored copy's HTTPS request to the geolocation endpoint fails certificate validation as of 2025-05-12 and will not recover.** Any build of the `XIAO-ESP32S3-Geolocation` example using the bundled library will report a TLS handshake failure rather than a location fix, and the symptom looks like a network or API-key problem rather than an expired trust anchor.

**Fix:** replace the bundled `WifiLocation-master.zip` with current upstream, or apply the certificate hunk from [`WifiLocation.patch`](WifiLocation.patch) in reverse (the patch is oriented upstream → vendored, so applying it *forward* to the vendored tree brings it up to date):

```bash
cd examples/selected/XIAO-ESP32S3-Geolocation/libraries
unzip WifiLocation-master.zip -d /tmp/wl
patch -p1 -d /tmp/wl/WifiLocation-master < ../../../vendored-lib-deltas/WifiLocation.patch
```

> Status: **`inferred`**. The certificate expiry date is read directly from the embedded PEM and the upstream replacement is observed in the diff; the end-to-end failure has **not** been reproduced on hardware here.

This is a good illustration of why vendored dependencies get audited rather than trusted: the library looks fine, compiles fine, and is quietly broken by the passage of time.

## Upstream snapshots are stored locally

Because upstream `master` moves, the comparison above would not be reproducible from URLs alone. The exact upstream trees used are retained, pinned by commit:

| File | Upstream @ commit |
|---|---|
| [`QuickDebug-upstream-4f4156c3.zip`](../../artifacts/upstream-libs/QuickDebug-upstream-4f4156c3.zip) | `gmag11/QuickDebug` @ `4f4156c3` |
| [`TJpg_Decoder-upstream-71bfc260.zip`](../../artifacts/upstream-libs/TJpg_Decoder-upstream-71bfc260.zip) | `Bodmer/TJpg_Decoder` @ `71bfc260` |
| [`WifiLocation-upstream-21c4ce7b.zip`](../../artifacts/upstream-libs/WifiLocation-upstream-21c4ce7b.zip) | `gmag11/WifiLocation` @ `21c4ce7b` |

All three verified as valid archives. Together they are ~360 KB.

## Restoring or replacing a vendored library

Each vendored copy is a GitHub `-master.zip` snapshot. To obtain the equivalent upstream tree:

```bash
# current upstream master (moves over time)
curl -fsSL https://codeload.github.com/gmag11/WifiLocation/zip/refs/heads/master -o WifiLocation-master.zip

# a specific tagged release, if the project publishes tags (stable, preferred)
curl -fsSL https://codeload.github.com/Bodmer/TJpg_Decoder/zip/refs/tags/1.1.0 -o TJpg_Decoder-1.1.0.zip
```

To re-run the comparison yourself and regenerate any patch:

```bash
python3 tools/diff_vendored_lib.py \
  --vendored examples/selected/XIAO-ESP32S3-Geolocation/libraries/WifiLocation-master.zip \
  --upstream-repo gmag11/WifiLocation \
  --out examples/vendored-lib-deltas/WifiLocation.patch
```

Exit status is `0` when identical to upstream and `1` when it differs, so it is usable as a CI drift check.

## Other dependency handling in the selected examples

Not every project vendors its dependencies; most pin them instead, which is preferable and needs no delta tracking:

| Project | Mechanism | Pinning quality |
|---|---|---|
| `XIAO_Webcam` | ESP-IDF component manager, [`main/idf_component.yml`](../selected/XIAO_Webcam/main/idf_component.yml) | Weak — `espressif/usb_device_uvc: "=*"` and `esp32-camera: "=*"` accept any version |
| `XIAO-ESP32S3-Sense_Retro_Camera` | PlatformIO `lib_deps` | Mixed — `ESPAsyncWebServer @ ^3.6.0` and `AsyncTCP @ ^3.3.2` are pinned; `LovyanGFX`, `esp32-camera`, `QRCode` float |
| `Seeed_Arduino_SSCMA` | Arduino `library.properties` / `library.json` | Library itself, no vendored deps |
| `esp32-birdnet-mic` | PlatformIO, plus a vendored **`esp-web-tools` 10.4.0** under `web-flasher/vendor/` | The vendored web tooling is a released, version-stamped distribution with its own `LICENSE` — archived with the rest of `web-flasher/`, see [`selected/esp32-birdnet-mic/web-flasher.ARCHIVED.md`](../selected/esp32-birdnet-mic/web-flasher.ARCHIVED.md) |
| `XIAO-ESP32S3-Geolocation` | **Vendored zips** — the subject of this document | Frozen snapshots, no version metadata beyond `library.properties` |

The `"=*"` pins in `XIAO_Webcam` are worth flagging: that project builds against whatever `esp32-camera` the component registry serves on the day you build, which for a camera driver with an active API is a real reproducibility problem. If you build it, pin the versions yourself and record them.

## Related

- [`catalog.json`](../catalog.json) — every example evaluated, with disposition
- [`best.md`](../best.md) — which examples to actually start from and why
- [`../tools/diff_vendored_lib.py`](../../../../../tools/diff_vendored_lib.py) — the comparison tool
- [`../tools/archive_artifact.py`](../../../../../tools/archive_artifact.py) — the archive-with-placeholder tool
