# Chip documents are not here — and that is deliberate

A document is filed by **what it describes**, not by what was being researched when it was
fetched. The Kendryte K230 datasheet describes a **chip**, so it is a *component* artifact even
though a board task fetched it.

All K230 documentation retrieved during this device's research lives at:

**[`components/canaan/k230/artifacts/`](../../../../../components/canaan/k230/artifacts/)**

| File | Bytes | Establishes |
|---|---:|---|
| `K230_datasheet-v1.0-2023-07-06.md` | 83 002 | Full feature list, KPU operators, packages, electrical sections, PMU, security |
| `K230_brief_datasheet.md` | 7 781 | **CPU0/CPU1 roles and frequencies**, package dimensions, SiP memory, peripheral counts |
| `K230_Hardware_Design_Guide.md` | 49 061 | Board-design rules |
| `K230_PMU_User_Guide.md` | 10 039 | PMU registers, power key, shutdown |
| `K230_nncase_Development_Guide.md` | 81 128 | KPU model compilation |
| `K230_RVV_In_Action.md` | 12 528 | Practical RVV on CPU1 |
| `K230_RVV_optimization_performance_description.md` | 12 004 | Vector speed-up figures |
| `SHA256SUMS` | 677 | Verification |
| `CANAAN-EDA-SET.md` | — | 22 Canaan reference-board EDA files, enumerated with exact sizes and two reacquisition URLs each |

All seven documents were retrieved 2026-09-04 from `kendryte/k230_docs` at commit
**`f8e30213963e0ed5cf995c3cd4701218a45e4793`**.

Component datasheets for the other fitted parts follow the same rule and are under their own
manufacturers: [`raydium/rm69a10`](../../../../../components/raydium/rm69a10/README.md),
[`goodix/gt9895`](../../../../../components/goodix/gt9895/README.md),
[`galaxycore/gc2093`](../../../../../components/galaxycore/gc2093/README.md),
[`realtek/rtl8189fs`](../../../../../components/realtek/rtl8189fs/README.md),
[`realtek/rtl8152b`](../../../../../components/realtek/rtl8152b/README.md),
[`semtech/sx1262`](../../../../../components/semtech/sx1262/README.md),
[`semtech/lr2021`](../../../../../components/semtech/lr2021/README.md),
[`nordic-semiconductor/nrf52840`](../../../../../components/nordic-semiconductor/nrf52840/README.md),
[`nordic-semiconductor/nrf9151`](../../../../../components/nordic-semiconductor/nrf9151/README.md),
[`texas-instruments/tca8418`](../../../../../components/texas-instruments/tca8418/README.md),
[`texas-instruments/bq25896`](../../../../../components/texas-instruments/bq25896/README.md),
[`texas-instruments/bq27220`](../../../../../components/texas-instruments/bq27220/README.md),
[`xlsemi/xl9555`](../../../../../components/xlsemi/xl9555/README.md),
[`analog-devices/max98357a`](../../../../../components/analog-devices/max98357a/README.md),
[`asair/aht20`](../../../../../components/asair/aht20/README.md),
[`lontium/lt9611`](../../../../../components/lontium/lt9611/README.md).
