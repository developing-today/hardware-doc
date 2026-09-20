# CellWise (CW) — battery fuel gauges

Shenzhen CellWise Microelectronics designs the **CW2xxx** family of low-cost
single-cell Li-ion fuel gauges, widely used in Chinese consumer devices as a
cheaper alternative to TI's BQ27xxx line.

| Part | Where |
|---|---|
| [`cw2017`](cw2017/README.md) | Xteink X4 Pro, Xteink X4 Classic |

**The family trait that bites:** CellWise gauges are **profile-driven**. They
report nothing useful until the host uploads a battery-model table, and they
expose **no current register**, so charge/discharge direction is not observable
from the gauge at all.
