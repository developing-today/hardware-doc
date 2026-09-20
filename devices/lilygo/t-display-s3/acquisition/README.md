# T-Display-S3 — acquisition

Clean-clone reproduction, in execution order. All entries verified **2026-09-07**.

## 0. Prerequisites

```bash
gh auth login          # api.github.com limits per identity: 60/h anonymous, 5000/h with a token
python3 --version      # 3.9+
```
`curl` is sufficient for everything; `gh` is only needed for the API enumeration steps.

## 1. Tracked artifacts — already in the repository

Board-level artifacts for this PCB live in
[`../../t-display-s3-shared/artifacts/`](../../t-display-s3-shared/artifacts/) because they
also cover the Touch variant. Nothing needs downloading for those; verify with:

```bash
cd devices/lilygo/t-display-s3-shared/artifacts
sha256sum -c <<'EOF'
607b63300636521fc78fbb36ed371ac10e81e3145ffa770784f45c2bf52e08c9  schematic/T_Display_S3.pdf
c3d5651d79b933d0995f294caeb60f4ee0c5f59090a531f13915868d125c7ce6  schematic/SCH_T-Display-S3-MIDI_V1.1.pdf
f288081645eecf7bf6a17fd7b5bc2e724121d00cdc2099b5a5ea7db5107eb9fa  firmware/t-display-s3-touch-20230417_0x0.bin
f288081645eecf7bf6a17fd7b5bc2e724121d00cdc2099b5a5ea7db5107eb9fa  firmware/t-display-s3-no-touch-20231013_0x0.bin
4af91e520a3f5037d9b0420aa620f8736e4e6469601098fea6eb4985323d847f  firmware/t-display-s3-lvgl-demo-20250109_0x0.bin
45385b2a90070a7616b7fceca553d60ca984e33115f4b9586a5ebb6ddb8213f1  firmware/t-display-s3-tft-espi-20231113_0x0.bin
2f0cf68a3ac19cec982735d7ccbcb93e522e65c9d8736e440efbf4001f9707fd  firmware/t-display-s3-screen-detect-20230315_0x0.bin
f6883c8ba9be6b1c0b9840943a79fb6eee7d4e5af506ea42b01a95a1c7a9134a  firmware/t-display-s3-midi-v1.0.1-20231013_0x0.bin
809949416716286a5b2db0821608251a1d69463ceea5721ccc5598a7fd841a5c  tft-espi/Setup206_LilyGo_T_Display_S3.h
529abb0314591c5f3c31f517f32b9af98b19cb5e240784e22939512e0d65281a  originals/boards-lilygo-t-display-s3.json
d0ce207e8bdea5f36e682ab143297f97869ef8302ee757a9ef802d1b8f882cb9  originals/platformio.ini
c400cc8dcc1ccf28a6f3bba00483b64230f9d6d074490cc516a6278ef5fe90f0  originals/LilyGo-Display-IDF-product_pins.h
EOF
```

**The two identical firmware hashes are not a copy-paste error** — see
[`../factory-firmware.md`](../factory-firmware.md) §2.

## 2. Component datasheets

Filed under their components, not here, per repository policy:

| Artifact | Destination |
|---|---|
| `ST7789V_SPEC_V1.4.pdf` | [`components/sitronix/st7789v/artifacts/`](../../../../components/sitronix/st7789v/artifacts/) |
| CST816S register guide | [`components/hynitron/cst816d/artifacts/`](../../../../components/hynitron/cst816d/artifacts/) |
| CST328 datasheet V2.2 | [`components/hynitron/cst328/artifacts/`](../../../../components/hynitron/cst328/artifacts/) |

Reacquisition commands are in each component's own record.

## 3. Not tracked — the vendor source tree

**Reacquisition: automatic.** ~180 MB, one `git clone` away, and 5 MB of it is a single image
header. Not vendored.

```bash
git clone https://github.com/Xinyuan-LilyGO/T-Display-S3.git
cd T-Display-S3
git checkout ec889e789b3cf093412689a143f7f37b42b56af7   # the commit every citation here uses
```

Or a single file without cloning:

```bash
curl -fsSL -H "Authorization: Bearer $(gh auth token)" \
  https://raw.githubusercontent.com/Xinyuan-LilyGO/T-Display-S3/ec889e789b3cf093412689a143f7f37b42b56af7/examples/factory/pin_config.h
```

Fallback if GitHub is unavailable: `https://codeload.github.com/Xinyuan-LilyGO/T-Display-S3/tar.gz/<sha>`,
or the Software Heritage archive.

## 4. Not tracked — market data

```bash
curl -sS -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
  'https://lilygo.cc/collections/all/products.json?limit=250&page=1'
```
**Reacquisition: automatic, but the data changes daily.** The 2026-09-07 snapshot is in
scratch; the derived table is in [`../market-and-pricing.md`](../market-and-pricing.md).

## 5. Validation

Never trust a file extension — LilyGO's CDN and GitHub redirects have both been known to serve
HTML for missing paths.

```bash
python3 scratch/lilygo-t-display-s3/magic.py <files...>   # magic bytes, size, SHA-256
```

`file(1)` was **not available** on the host used for this pass, which is why a replacement
exists. Every artifact in this record passed; no HTML was retained under a binary extension.

## 6. Expected failure modes

| Symptom | Cause | Action |
|---|---|---|
| HTTP 403 with `X-RateLimit-Remaining: 0` | GitHub API limit, not bot-blocking | authenticate; do **not** rotate User-Agent |
| HTTP 404 on `raw.githubusercontent.com` | the commit or path is wrong | LilyGO force-pushes; re-resolve the tip with `gh api repos/…/commits/<branch>` and record the new SHA |
| `products.json` returns HTML | Shopify bot protection | retry with the browser User-Agent above |
| Default branch is not `main`/`master` | **normal for LilyGO** — `T-Display-S3-Long` defaults to `T-Display-S3-Long-cst3530`, `T-Display-S3-AMOLED-1.64` to `arduino-esp32-libs_V2.0.14` | always read `.default_branch`; never assume |
