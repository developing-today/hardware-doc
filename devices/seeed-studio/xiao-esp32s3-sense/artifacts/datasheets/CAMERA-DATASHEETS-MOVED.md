# Camera sensor datasheets are filed under `components/`, not here

The OV2640 and OV5640 datasheets used to sit in this directory as device-local copies. They are
**part-level documents, not board-level ones** — the same PDFs apply to every board carrying those
sensors — so they now live once under `components/omnivision/`, and this device cites them.

Moved **2026-08-30**. Nothing was lost; the bytes are unchanged and still in the repository.

| Sensor | Canonical file | Bytes | SHA-256 |
|---|---|---:|---|
| **OV2640** | [`components/omnivision/ov2640/artifacts/ov2640-datasheet-v2.2.pdf`](../../../../../components/omnivision/ov2640/artifacts/ov2640-datasheet-v2.2.pdf) | 676,989 | `4460f2f13b761eae4d1778a28f6d86db50a54e77b96cf8af9ddb2fa3168feab7` |
| **OV5640** | [`components/omnivision/ov5640/artifacts/ov5640-datasheet-v2.03.pdf`](../../../../../components/omnivision/ov5640/artifacts/ov5640-datasheet-v2.03.pdf) | 1,749,719 | `0e0b34b90706043782568c39d982922f1727dbed41b288cfb7d404dde22fb742` |

Component records, which carry the register-level detail and the cross-device usage:

- [`components/omnivision/ov2640`](../../../../../components/omnivision/ov2640/README.md) — the sensor on the standard Sense daughterboard
- [`components/omnivision/ov5640`](../../../../../components/omnivision/ov5640/README.md) — the autofocus upgrade module
- [`camera-sensors.md`](../../camera-sensors.md) — which sensor ships on which variant, and how they differ in practice on this board

## Reacquisition

Both are OmniVision documents distributed through third parties; OmniVision does not publish them
openly. See each component record's own source table for the retrieval path used.

> **Note on the OV2640 "application notes".** A file named
> `ov2640-camera-module-software-application-notes.pdf` used to sit beside the OV2640 datasheet in
> the component record. It was **byte-identical to the datasheet** — the application notes were
> never actually obtained, and the download produced a second copy of the datasheet under the wrong
> name. That file has been removed and the gap recorded honestly at
> [`components/omnivision/ov2640/artifacts/MISSING-application-notes.md`](../../../../../components/omnivision/ov2640/artifacts/MISSING-application-notes.md).
> Nothing unique was lost, but do not assume the application notes are held here — they are not.

---

## Addendum — OV3660 and the module specs (2026-08-30)

The same rule was applied to the remaining camera documents in this directory, completing the move:

| Document | Bytes | SHA-256 | Now at |
|---|---:|---|---|
| **OV3660** datasheet | 1,917,798 | `5afc0efd12b27a58f87a4cfc4fab1edcdaf86e5e12ea25722df6bf1ab72c81bc` | [`components/omnivision/ov3660/artifacts/ov3660-datasheet.pdf`](../../../../../components/omnivision/ov3660/artifacts/ov3660-datasheet.pdf) |
| **OV3660** camera-module spec | 387,241 | `c38741e9cf0083322f73a09c53a7a3fb9a89c420700eee8849763e27019e87fa` | [`components/omnivision/ov3660/artifacts/ov3660-camera-module-spec.pdf`](../../../../../components/omnivision/ov3660/artifacts/ov3660-camera-module-spec.pdf) |
| **OV5640** camera-module spec | 1,749,719 → see file | `0a6e6120a71eb0d1bb323f76679a50e7f2c3c584db522e4c97ece9cafca84b43` | [`components/omnivision/ov5640/artifacts/ov5640-camera-module-spec.pdf`](../../../../../components/omnivision/ov5640/artifacts/ov5640-camera-module-spec.pdf) |

All hashes re-verified unchanged after the move; all validate as `application/pdf`.

- [`components/omnivision/ov3660`](../../../../../components/omnivision/ov3660/README.md) — the sensor on some Sense units

> ⚠ **The OV3660 datasheet is scarce — do not archive it out of the repository.** It is a
> **v1.3, May 2011 PRELIMINARY** document that OmniVision does not publish; it reached us through a
> Seeed mirror that no longer serves it, and **all five independent re-fetch URLs returned 404 on
> 2026-08-30**. Its redistribution status is `prohibited`, which is also why it was **moved rather
> than copied** — a second copy would be the wrong direction on both counts.
