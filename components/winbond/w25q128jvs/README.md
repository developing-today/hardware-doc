# Winbond W25Q128JVS — merged into the family record

> **This record moved on 2026-08-30.** It is now a variant section of
> **[`components/winbond/w25q128jv/`](../w25q128jv/README.md)**.

`W25Q128JVS` and `W25Q128JVPIQ` are two ordering variants of the same die, and **Winbond publishes a
single datasheet covering both**. They were previously filed as two component records, each holding
a byte-identical 2,462,647-byte copy of that datasheet — the duplication is what surfaced the
mis-filing.

| | |
|---|---|
| Full record | [`../w25q128jv/README.md`](../w25q128jv/README.md) |
| This variant | [`W25Q128JVS` — SOIC-8, 208 mil](../w25q128jv/README.md#variants-covered-by-this-record) |
| Board integration | [`U9` on the Nicolai Electronics Tanmatsu](../w25q128jv/README.md#used-by) |
| Datasheet | [`../w25q128jv/artifacts/w25q128jv-datasheet-rev-f.pdf`](../w25q128jv/artifacts/w25q128jv-datasheet-rev-f.pdf) — SHA-256 `809f066e62bcde10b12c2202daf05f4776929ad7dc5f9d3b5131cdcc84502bc1`, 2,462,647 bytes |

**A correction was made during the merge.** This record previously stated that *"no local datasheet
copies were retained"* for the `JVS` variant. That was true of this directory in isolation, but the
family datasheet had in fact been retained all along under the `JVPIQ` record — the same document
Winbond publishes for both variants. The claim was an artefact of the split filing, not a real gap.

The `JVS`-specific caveat that **does** still stand: nothing about the Tanmatsu integration was
verified on hardware.

Reacquire the datasheet, if ever needed:
<https://www.winbond.com/resource-files/w25q128jv%20revf%2003272018%20plus.pdf>
