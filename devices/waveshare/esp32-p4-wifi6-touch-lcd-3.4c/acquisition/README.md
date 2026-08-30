# Acquisition — clean-clone instructions

> ESP32-P4-WIFI6-Touch-LCD-3.4C and 4C. Verified **2026-08-24**.
> Machine-readable form: [`manifest.json`](./manifest.json).

Both variants share every artifact. They live once under
`../../esp32-p4-wifi6-touch-lcd-xc-shared/`.

## Already in the repository

No action needed after cloning:

| Path (under the shared record) | Bytes |
|---|---:|
| `artifacts/schematic/ESP32-P4-WIFI6-Touch-LCD-XC-Schematic.pdf` | 1,869,787 |
| `artifacts/demo/` — board-specific sources | ~2.3 MiB |
| `artifacts/source-snapshots/` — both wiki pages | ~204 KiB |

## Step 1 — the demo archive (optional, 112 MiB)

Needed only if you want the bundled LVGL / Arduino_GFX / Brookesia trees, or the byte-exact
original. All **board-specific** sources are already vendored.

```bash
curl -L -O https://files.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-XC/ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip
sha256sum ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip
# expect b5319593738e114270852d84be0fdd8ccdc21ef1dac897b15f4fad5069dd66b8
unzip -q ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip   # -> 5052 files, 289 MiB
```

Verify the extraction:

```bash
find . -type f -exec sha256sum {} + \
  | sed 's|^\(.\{64\}\)  \./|\1  |' | sort -k2 | sha256sum
# expect a856b1941de93ba892b244f03f139d958cb200807284f4ed66cd5d74b428c838
```

Status: **automatic**. Probed 2026-08-24 — `HTTP 200`, `Content-Length: 117768225`, matching the
recorded byte size exactly.

## Step 2 — re-verify the schematic (optional)

```bash
curl -L -O https://files.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-XC/ESP32-P4-WIFI6-Touch-LCD-XC-Schematic.pdf
sha256sum ESP32-P4-WIFI6-Touch-LCD-XC-Schematic.pdf
# expect 7a12998f1e641c49ab5e38f4765bdaf76aad2269e908e87ccffd572316647d68
```

## Step 3 — bundled dependencies, if rebuilding

**LVGL and Arduino_GFX were diffed against upstream on 2026-08-24 and are byte-identical to their
tags** — no patch step is needed. `esp-brookesia` remains unverified. See
[C5](../gaps-and-conflicts.md#c5--bundled-third-party-libraries--resolved-2026-08-24).

```bash
git clone https://github.com/lvgl/lvgl.git && git -C lvgl checkout v9.3.0
git clone https://github.com/moononournation/Arduino_GFX.git   # tag 1.6.0
```

Then diff against the copies inside the demo archive before relying on either:

```bash
diff -rq lvgl <extracted>/Arduino/libraries/lvgl
```

Expected tree digests, if you want to confirm you have the same bytes we analysed:

| Tree | Digest (prefix) | Bytes | Files |
|---|---|---:|---:|
| `Arduino/libraries/lvgl` | `ae0606a48e68723a` | 186,517,201 | 4267 |
| `Arduino/libraries/GFX_Library_for_Arduino` | `f18c8606b56faebf` | 27,130,057 | 309 |
| `ESP-IDF/11_esp_brookesia_phone` | `e76fab6f24efafd1` | 73,198,225 | 306 |

`esp-brookesia` is **manual**: the demo does not pin a version, so resolve it from that project's
`idf_component.yml` first.

## Expected failure modes

| Symptom | Cause | Action |
|---|---|---|
| `HTTP 404` on the demo/schematic | Waveshare reorganised the `XC` directory | Check both product wikis for the new path |
| Hash mismatch, right size | File replaced in place | Record the new hash and date; **do not** overwrite the old record |
| Wiki API returns PHP error | Known broken — [C10](../gaps-and-conflicts.md#c10--waveshare-mediawiki-api-is-broken) | Use rendered HTML + regex instead |
| 4C store URL 404s | Expected — [C2](../gaps-and-conflicts.md#c2--4c-availability--resolved-2026-08-24) | Not a failure |

## Preservation risk

The schematic and demo archive exist **only** on `files.waveshare.com`, under a product-specific
directory, with **no third-party mirror located**. Unlike Waveshare's `/wiki/common/` pool, these
are not shared across product lines and would disappear with the product.

Both are good candidates for `https://web.archive.org/save/`. The archived local copy under
`archive/hardware-doc/devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/originals/`
is currently the only guaranteed-identical source for the demo ZIP's exact bytes. The archive
mirrors the **repository-root** path, so restoring is a straight copy back.

## Licensing

**Every artifact here has `redistribution_status: unknown`.** No LICENSE file exists anywhere in
the 5052-file demo archive, and Waveshare state no terms on the wiki, the schematic, or the store
page. Vendor demo code is conventionally treated as freely usable — that is convention, not
evidence.

All Waveshare artifacts are therefore held **unstaged** pending review. See
[C7](../gaps-and-conflicts.md#c7--demo-licence--resolved-2026-08-24).
