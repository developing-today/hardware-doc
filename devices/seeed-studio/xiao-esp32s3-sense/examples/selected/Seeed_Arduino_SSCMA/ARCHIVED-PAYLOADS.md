# Archived payloads in this library — reacquisition record

Three large non-source files were moved out of the repository on **2026-08-30**. Not deleted.

> **These files are absent from the repository.** They are not symlinks and not placeholders-in-place —
> the paths simply do not exist here any more. This record is the only thing standing in for them,
> which is why it carries a SHA-256, a byte count and a pinned reacquisition URL for every file.
>
> The archive copy is a **convenience for whoever holds it, not part of the contract**: it lives
> outside the repository at a machine-local path, so nothing here may depend on it.

## What was archived

| File | Bytes | SHA-256 |
|---|---:|---|
| `examples/we2_iic_bootloader_recover/firmware.h` | 1,485,005 | `b8d01857383273aa6117620e02802edf460af2bd7ef97e2aed124261bd21c5da` |
| `examples/camera_web_server/img/example_2.gif` | 1,193,509 | `6469d8b524478d4f4534668a85e480a9b0263973c92ff5f60db86dfb561ee4a0` |
| `examples/camera_web_server/img/example_3.gif` | 690,807 | `84ec0868a2d08acf7ca33adcbcbbb2828652707bb818cd881a1ce68ac30200ce` |

`example_0.gif` and `example_1.gif` were archived earlier, on 2026-08-28.

Archive root:
`archive/doc/hardware/devices/seeed-studio/xiao-esp32s3-sense/examples/selected/Seeed_Arduino_SSCMA/`

## What these actually are, and why the split falls where it does

This library's size is **not** in its code. Measured:

| Part | Size | Keep? |
|---|---:|---|
| `src/` — **the library itself**, `Seeed_Arduino_SSCMA.{cpp,h}` | **40 KB** | **Keep** — it is tiny |
| `examples/**/*.ino` — 14 sketches | **40.7 KB** | **Keep** — the device-relevant usage code |
| `examples/**/*.cpp` — `app_httpd.cpp`, `utils.cpp`, `ep2_isp_i2c.cpp` | ~60 KB | **Keep** — real code, larger than the sketches |
| `examples/camera_web_server/web/index.html` + `web_index.h` | 124 KB | **Keep** — the web UI, and its gzipped-embedded twin |
| `firmware.h` + 4 GIFs | **3.5 MB** | **Archived** |

> **`firmware.h` is not source.** Despite the `.h` extension it is a **generated C array holding a
> prebuilt firmware image** for the Himax WE2 bootloader-recovery procedure — its own header says
> `// Generate date: 2024-04-08 19:54:23`. It is a binary payload wearing a source-file extension,
> which is why it never showed up as "large binary" in earlier passes.
>
> **It is also not firmware for this board.** The example's own README titles it *"Grove Vision AI
> (WE2) Bootloader Recovery Tool"* — it recovers the bootloader on the **Grove Vision AI V2
> (Himax WiseEye2) module**, a separate accessory, using any I²C-capable Arduino board as the
> flashing host. The XIAO ESP32S3 Sense has no WE2; its TinyML runs on the ESP32-S3 itself. See the
> naming-confusion note in [`features/tinyml.md`](../../../features/tinyml.md) §170.
>
> So this file is a 1.45 MB firmware blob **for a different product**, carried along because the
> SSCMA library supports several Seeed AI devices. Archiving it is the clear call: it is the
> largest single file in the library, it is not code, it is not for this board, and it comes from a
> pinned commit in a public Arduino-Library-Manager repository.

The practical answer to *"is the `.ino` the real code and the rest vendored?"* is: **the `.ino`
files are the device-relevant part, but they are only ~1 % of the tree, and they are not the only
real code.** The `.cpp` files beside them matter just as much. What made this library big was one
generated firmware blob and four documentation GIFs — not library code, and not examples.

## Reacquisition

| | |
|---|---|
| Repository | `Seeed-Studio/Seeed_Arduino_SSCMA` |
| URL | <https://github.com/Seeed-Studio/Seeed_Arduino_SSCMA> |
| Commit | **`65a1b2061e80f1bd3814f688451a66646782fe1f`** |
| Also on | Arduino Library Manager |

```bash
curl -fsSL "https://codeload.github.com/Seeed-Studio/Seeed_Arduino_SSCMA/tar.gz/65a1b2061e80f1bd3814f688451a66646782fe1f" \
  -o sscma.tar.gz
tar -xzf sscma.tar.gz
sha256sum Seeed_Arduino_SSCMA-65a1b206*/examples/we2_iic_bootloader_recover/firmware.h
# expect b8d01857383273aa6117620e02802edf460af2bd7ef97e2aed124261bd21c5da
```

Or a single file at the pinned commit:

```bash
curl -fsSL "https://raw.githubusercontent.com/Seeed-Studio/Seeed_Arduino_SSCMA/65a1b2061e80f1bd3814f688451a66646782fe1f/examples/we2_iic_bootloader_recover/firmware.h"
```

This is a **public, well-known, actively maintained repository in the Arduino Library Manager** —
one of the lowest reacquisition risks in this repository, which is why archiving here is safe.

## Related

- [`features/tinyml.md`](../../../features/tinyml.md) — how SSCMA is used on this board
- [`examples/best.md`](../../best.md) · [`examples/vendored-lib-deltas/README.md`](../../vendored-lib-deltas/README.md)

## Restoring a file

Re-fetch it from the pinned upstream in the Reacquisition section above and verify against the
SHA-256 in the table. If you happen to hold the local archive, copying from the archive root shown
above is faster and gives the identical bytes.
