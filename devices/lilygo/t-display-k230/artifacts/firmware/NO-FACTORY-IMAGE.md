# There is no factory firmware image for this board

**Verified 2026-09-04.** Negative result.

LilyGO publishes **no prebuilt system image** for the T-Display K230. Their own README says:

> "Generated image files under `k230_bsp/images/` are local build artifacts."

To get a running system you must **build `sysimage-sdcard.img` yourself** — see
[`../../development.md`](../../development.md) — which needs Ubuntu 22.04/24.04 (or Docker, or
WSL2) and the XuanTie toolchain at `/opt/toolchain`.

Canaan publishes generic K230 images at `developer.canaan-creative.com` → *K230* → *Images*.
Those boot a K230, but they drive **none** of this board's peripherals: the AMOLED, touch,
keyboard, camera, Wi-Fi and radio support are all in LilyGO's overlay.

## Why this matters more than usual

A user who bricks a board cannot download a known-good image and start again. Combined with the
absence of any documented recovery procedure ([`../../factory-firmware.md` §5](../../factory-firmware.md)),
this is the single largest practical risk of owning the product — and it is exactly what one
owner ran into on 2026-08-21.

## The only prebuilt binaries LilyGO does publish

Both are for the **nRF52840 companion**, in a different repository, and both have **no licence**.
**Both are now held in this directory** and have been parsed —
see **[`nrf52840-coprocessor-firmware.md`](nrf52840-coprocessor-firmware.md)**.

| File | Bytes | SHA-256 | Role |
|---|---:|---|---|
| [`k230_nrf52840_at_20260816_r4_k230_uart_dfu.uf2`](k230_nrf52840_at_20260816_r4_k230_uart_dfu.uf2) | 296,960 | `931948dd024425ce8e8e455da7637cf8e9924a587e1e78b81b690416549e6022` | AT/BLE-Central application, build **2026-08-16**, revision **r4**, UF2 family `0xADA52840`, loads at **0x26000** |
| [`k230_nrf52840_bootloader_uartdfu_115200_s140_6.1.1.hex`](k230_nrf52840_bootloader_uartdfu_115200_s140_6.1.1.hex) | 525,680 | `6c4eab9534e55d0e80a7797616674d68e9d9eda139222a1bb1439214ae16b7a3` | **Adafruit UF2 bootloader 0.11.0-5-g4d321e2** + MBR + **SoftDevice S140 v6.1.1**, board ID `nRF52840-k230-v1` |

> ⚠ **Corrected 2026-09-20.** Both files were previously recorded `disposition: reference-only`,
> `repo_state: not-downloaded`, `sha256: null` in
> [`../../acquisition/manifest.json`](../../acquisition/manifest.json) — while in fact they had
> been fetched on 2026-09-04 inside the vendor-repository clone at
> `archive/devices/lilygo/t-display-k230/artifacts/source-snapshots/T-Display-K230-nRF52840/`. They are now held here, hashed, and mined.
> The same applied to the annotated pin photograph, now at
> [`../media/nrf52840-baseboard-pins-annotated.png`](../media/nrf52840-baseboard-pins-annotated.png).
>
> The scratch clone retains its own copies: it is a coherent `git` working tree pinned to a
> commit, and removing files from it would break that. The duplication is deliberate — 1.5 MB.

Reacquisition (**automatic**), from the pinned commit:

```
https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF52840/raw/4646a728580739d487126f47a521e9b8032b3c2c/firmware/k230_nrf52840_at_20260816_r4_k230_uart_dfu.uf2
https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF52840/raw/4646a728580739d487126f47a521e9b8032b3c2c/bootloader/k230_nrf52840_bootloader_uartdfu_115200_s140_6.1.1.hex
```

Second, mutable URL for each: replace the commit SHA with `master`.

**SHA-256 for both is unknown** — they were enumerated from the Git tree API rather than
downloaded. Recorded as unknown rather than omitted. Byte sizes above are exact and are enough to
confirm identity on reacquisition.

Full records: [`../../acquisition/manifest.json`](../../acquisition/manifest.json),
entries `nrf52840-firmware-uf2` and `nrf52840-bootloader-hex`.
