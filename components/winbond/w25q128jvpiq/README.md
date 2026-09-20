# Winbond W25Q128JVPIQ — merged into the family record

> **This record moved on 2026-08-30.** It is now a variant section of
> **[`components/winbond/w25q128jv/`](../w25q128jv/README.md)**.

`W25Q128JVPIQ` and `W25Q128JVS` are two ordering variants of the same die, and **Winbond publishes a
single datasheet covering both**. They were previously filed as two component records, each holding
a byte-identical 2,462,647-byte copy of that datasheet — the duplication is what surfaced the
mis-filing.

| | |
|---|---|
| Full record | [`../w25q128jv/README.md`](../w25q128jv/README.md) |
| This variant | [`W25Q128JVPIQ` — WSON-8, industrial, QE hard-wired](../w25q128jv/README.md#variants-covered-by-this-record) |
| Board integration | [`U3` on the Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../w25q128jv/README.md#used-by) |
| Datasheet | [`../w25q128jv/artifacts/w25q128jv-datasheet-rev-f.pdf`](../w25q128jv/artifacts/w25q128jv-datasheet-rev-f.pdf) — SHA-256 `809f066e62bcde10b12c2202daf05f4776929ad7dc5f9d3b5131cdcc84502bc1`, 2,462,647 bytes |

Nothing was lost in the move: the entire previous contents of this file — the §11.1 ordering-code
decode, the DIO-versus-QIO finding, the partition layout and the wiring table — are in the family
record unchanged.

Reacquire the datasheet, if ever needed:
<https://www.winbond.com/resource-files/w25q128jv%20revf%2003272018%20plus.pdf>
