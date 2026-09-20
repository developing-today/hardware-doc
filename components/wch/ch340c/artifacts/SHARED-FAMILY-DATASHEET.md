# `ch340-datasheet-v3.4.pdf` lives at the vendor level

The CH340 datasheet is a **family document** — it specifies CH340B/C/E/G/K/N/T/X together, not one
variant. Holding a copy under each component record meant storing the same 322,745 bytes twice and
letting two copies drift apart independently.

It now lives once, at the WCH vendor record:

| | |
|---|---|
| Canonical file | [`vendors/wch/artifacts/ch340-datasheet-v3.4.pdf`](../../../../vendors/wch/artifacts/ch340-datasheet-v3.4.pdf) |
| **SHA-256** | `4d7b150edfda88e44eb8f499c22693318666968125ff17f652ca9983d9929e5e` |
| **Size** | 322,745 bytes |
| Vendor record | [`vendors/wch/README.md`](../../../../vendors/wch/README.md) |
| Reacquire | <https://www.wch-ic.com/downloads/CH340DS1_PDF.html> |

`ch340-datasheet-v3.4.pdf` in this directory is a **relative symlink** to that file, so tooling and
`artifacts/`-relative paths keep working unchanged.

## The other records that share it

| Record | Variant | Package |
|---|---|---|
| [`components/wch/ch340x`](../../ch340x/README.md) | **CH340X** | MSOP-10 |
| [`components/wch/ch340c`](../../ch340c/README.md) | **CH340C** | SOP-16 |

These are **different parts**, not duplicates of each other. Only the datasheet is shared. An
earlier reading of this repository mistook them for one part filed twice — they are not, and the
two records deliberately cover different boards and different pin topologies.

## Variant-specific files stay here

Anything that is *not* family-wide remains in this directory — for CH340C that is
`ch341ser-linux-v1.8.zip` and `wch-win7-x64-driver-install-note-v1.0.pdf`.
