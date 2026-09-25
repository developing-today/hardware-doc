# T-Display K230 — sources

`Class` ∈ {primary, authorized mirror, credible mirror, standard, community}.
`Medium` describes format. All URLs retrieved **2026-09-04** unless stated.

## Vendor — LILYGO

| ID | Title | Publisher | Class | Medium | URL | Published/updated | Establishes | Scope / limitations | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | T-Display K230 product page + `/products/t-display-k230.js` | LILYGO | primary | store listing | `https://lilygo.cc/products/t-display-k230` | created 2025-03-21 13:52+08, published 2025-03-21 14:22+08 | SKUs `K256`/`-A`/`-B`/`-C`, $98.79, SoC/display spec, images | Marketing copy; contains the RM69A10 and resolution but not the full BOM | `archive/devices/lilygo/t-display-k230/artifacts/research-scratch/shop-t-display-k230.{js,html}` |
| D2 | T-Display K230 Kit product page + `.js` | LILYGO | primary | store listing | `https://lilygo.cc/products/t-display-k230-kit` | created 2026-08-06 09:31+08, published 2026-08-20 15:10+08 | Kit SKUs and prices; **the fullest published component list**: RM69A10, SX1262, GC2093, 8 Gb LPDDR4, RTL8189, "RC01812" Ethernet | Does not mention Bluetooth or the base-board silicon | `archive/devices/lilygo/t-display-k230/artifacts/research-scratch/shop-t-display-k230-kit.{js,html}` |
| D3 | `k230_bsp/docs/HARDWARE_PINMAP.md` | LILYGO | primary | repository doc | `https://github.com/Xinyuan-LilyGO/T-Display-K230/blob/bb831ab358b66f5bd9a87ecd7c580fee4537492e/k230_bsp/docs/HARDWARE_PINMAP.md` | commit 2026-09-03 | **The authoritative pin map.** Every GPIO, bus, address, IRQ | Single source, **no schematic to corroborate it** | `archive/devices/lilygo/t-display-k230/artifacts/source-snapshots/T-Display-K230/` |
| D4 | `k230_canmv_t_display_rm69a10_defconfig` | LILYGO | primary | source | same repo, `k230_bsp/overlay/buildroot-overlay/configs/` | commit 2026-09-03 | XuanTie toolchain path and flags, kernel repo + commit, Wi-Fi packages, built-in test tools | | same |
| D5 | `linux.fragment` + 30 numbered kernel patches | LILYGO | primary | source | same repo, `k230_bsp/overlay/buildroot-overlay/linux/` | commit 2026-09-03 | Touch driver choice, USB net classes, Bluetooth dongle workarounds, display fixes, PMU power key | | same |
| D6 | `k230_canmv_v3.dts` (Canaan copyright 2023, in LilyGO's overlay) | Canaan / LILYGO | primary | source | same repo, U-Boot overlay | commit 2026-09-03 | **IO bank voltage warning**, BOOT0/BOOT1 on IO0/IO1, per-pin mux, 512 MB memory node | The memory node is the CanMV-v3 baseline — see `GC-7` | same |
| D7 | `k230_launcher/k230_phone_ui/src/ui_hardware.c` | LILYGO | primary | source | same repo | commit 2026-09-03 | **Complete keyboard key map and layout**, TCA8418 registers, PMU constants, low-battery policy, XL9555 probe behaviour | | same |
| D8 | `README.MD` + `CHANGELOG.MD` | LILYGO | primary | repository doc | same repo | v0.2.4, 2026-09-03 | Fitted-hardware list, feature status, known limitations, build and flash procedure, dated release history | | same |
| D9 | T-Display K230 wiki page | LILYGO | primary | official wiki | `https://wiki.lilygo.cc/products/t-display-series/t-display-k230/` | undated | RTL8152B Ethernet, GT9895, 1.6 TOPS claim, 16 MB flash, HDMI 1080p | ⚠ **contains at least three errors** — `GC-1`, `GC-2`, and empty schematic/dimension sections | `archive/devices/lilygo/t-display-k230/artifacts/research-scratch/wiki/` |
| D10 | T-Display K230 **Cased Version** wiki page | LILYGO | primary | official wiki | `https://wiki.lilygo.cc/products/t-display-series/t-display-k230/cased-version.html` | undated | Third variant: 110×58×30 mm, speaker, mic, 3.5 mm, QWIIC, nRF52840 header, "optional SX1262 or LR2021" | No shop listing exists for it | same |
| D11 | T-Display K230 Quick Start wiki page | LILYGO | primary | official wiki | `.../t-display-k230/quick-start.html` | undated | "No Arduino IDE"; ⚠ **inverts the core roles** (`GC-1`) | | same |
| D12 | `Xinyuan-LilyGO/T-Display-K230-nRF52840` | LILYGO | primary | repository | `https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF52840/tree/4646a728580739d487126f47a521e9b8032b3c2c` | pushed 2026-08-23 | nRF52840 pin map incl. `P0.04` 5 V boost, AT set, DFU procedure, prebuilt firmware + bootloader | No licence file | `archive/devices/lilygo/t-display-k230/artifacts/source-snapshots/` |
| D13 | `Xinyuan-LilyGO/T-Display-K230-nRF9151` | LILYGO | primary | repository | `https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF9151/tree/ed4ecbe34162dec9b81213a400198125bbd6e36f` | pushed 2026-08-14 | nRF9151 pin map, NCS v3.4.0, pinned upstream submodule, five patches, AT behaviour, TF-M caveat | No licence file | same |
| D14 | Product and wiki imagery | LILYGO | primary | images | see [`media/manifest.json`](media/manifest.json) | undated | 40-pin diagram, keyboard-extension diagram, specification card | No licence statement | `media/` |

## Chip vendor — Canaan Creative

| ID | Title | Publisher | Class | Medium | URL | Published/updated | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| C1 | K230 Product Full Datasheet **V1.0** | Canaan | primary | datasheet | `https://github.com/kendryte/k230_docs/blob/f8e30213963e0ed5cf995c3cd4701218a45e4793/en/00_hardware/K230_datasheet.md` | doc **2023-07-06** | Full feature list, KPU operators, packages, electrical sections, PMU, security | [`components/canaan/k230/artifacts/`](../../../components/canaan/k230/artifacts/) |
| C2 | K230 Brief Datasheet | Canaan | primary | datasheet | `.../en/K230_brief_datasheet.md` | repo 2025-09-12 | **Core roles and frequencies**, package sizes, SiP memory, peripheral counts | same |
| C3 | K230 Hardware Design Guide | Canaan | primary | design guide | `.../en/00_hardware/K230_Hardware_Design_Guide.md` | repo 2025-09-12 | Board-design rules | same |
| C4 | K230 PMU User Guide | Canaan | primary | manual | `.../en/01_software/board/osdrv/K230_PMU_User_Guide.md` | repo 2025-09-12 | PMU register flow, power key, shutdown | same |
| C5 | K230 nncase Development Guide | Canaan | primary | manual | `.../en/01_software/board/ai/K230_nncase_Development_Guide.md` | repo 2025-09-12 | KPU model compilation | same |
| C6 | K230 RVV in Action / RVV optimisation | Canaan | primary | tutorial | `.../en/02_applications/tutorials/K230_RVV_*.md` | repo 2025-09-12 | Practical RVV use on CPU1 | same |
| C7 | `kendryte/k230_docs` full tree listing at `f8e3021…` | Canaan | primary | repository | `https://github.com/kendryte/k230_docs` | 2025-09-12 | **Negative results**: no errata, no `K230_PINOUT` document; **positive**: the `zh/` EDA set | [`CANAAN-EDA-SET.md`](../../../components/canaan/k230/artifacts/CANAAN-EDA-SET.md) |
| C8 | `kendryte/k230_linux_sdk` | Canaan | primary | repository | `https://github.com/kendryte/k230_linux_sdk` | pushed 2026-09-03; **pinned by LilyGO at `22d02c6b6783a57a3aca7eb3160e313e772cb710`** | The SDK this board's image is built from | — |

## Independent editorial

| ID | Title | Publisher | Class | Medium | URL | Published | Establishes |
|---|---|---|---|---|---|---|---|
| N1 | "CanMV-K230 AI development board features Kendryte K230 dual-core 64-bit RISC-V processor" | CNX-Software | community | blog | `https://www.cnx-software.com/2023/10/24/canmv-k230-ai-development-board-features-kendryte-k230-dual-core-64-bit-risc-v-processor/` | 2023-10-24 | K230 launch-era coverage |
| N2 | "$29 Banana Pi BPI-CanMV-K230D-Zero…" | CNX-Software | community | blog | `https://www.cnx-software.com/2024/11/18/29-banana-pi-bpi-canmv-k230d-zero-features-kendryte-k230d-risc-v-soc-for-aiot-applications/` | 2024-11-18 | K230D board price point |
| N3 | "Kendryte K510 tri-core RISC-V AI processor deliver up to 3 TOPS" | CNX-Software | community | blog | `https://www.cnx-software.com/2021/07/09/kendryte-k510-tri-core-risc-v-ai-processor-3-tops/` | 2021-07-09 | K510 lineage |

**Negative result:** a CNX-Software site search for `K230` on 2026-09-04 returned **five** results
and **none of them is about the LilyGO T-Display K230**. As of the research date, the most
prolific independent SBC publication has never covered this product. No Hackaday article was
found either.

## Community

Full thread-level treatment with evidence labels: [`community.md`](community.md).

| ID | Thread / comment | Where | Date | Evidence type |
|---|---|---|---|---|
| R-LAUNCH | "T-Display K230 is available!" | r/LilyGO | 2025-03-21 | vendor announcement |
| R-OREBOOT | u/CyReVolt on oreboot K230 support | r/LilyGO | 2025-03-26 | **demonstrable project** (author is the maintainer) |
| R-MESH | "New Lilygo T-Display K230" — 187 pts, 40 comments | r/meshtastic | 2025-07-07 | discussion; contains firsthand observation of the RJ45 and the missing BT |
| R-STOCK | "T-Display K230 and T-Lora Pager have some stock available" | r/LilyGO | 2025-07-04 | availability |
| R-KB | "Keyboard for T-Display K230 is here" | r/LilyGO | 2026-07-28 | vendor announcement |
| R-CASE | u/Circuitnaut24: keyboard does **not** include a case | r/LilyGO | 2026-08-13 | **firsthand ownership** |
| R-KIT | "The T-Display K230 Kit is finally here!" — 83 pts | r/LilyGO | 2026-08-20 | vendor announcement + discussion |
| R-BARE | u/Opposite_Future2602: received bare board on risers, could not install an OS | r/LilyGO | 2026-08-20 | **firsthand ownership** |
| R-BRICK | u/phirzcolru: bricked by boot-medium change, unresponsive to boot pin | r/LilyGO | 2026-08-21, 2026-08-28 | **firsthand ownership** |
| R-ETH | u/Nobodytoyou_: the Ethernet port is oversized for the form factor | r/meshtastic | 2025-07-07 | firsthand observation |
| R-BATT | u/Ryan_e3p: battery-life scepticism | r/meshtastic | 2025-07-07 | **opinion** |
| R-IPX | u/No-Craft-7979: wants IP-rated options for field devices | r/LilyGO | 2026-08-20 | opinion / requirement |
| R-DEBIAN | u/Nanocupid links `intx82/k230-debian` and compares to an MQ-Pro | r/meshtastic | 2025-07-09 | **informed interpretation** |
| R-MESHUI | u/wirecrossed: building a full Meshtastic UI for this board | r/meshtastic | 2026-06-02 | **announced project**, no repo yet |
| R-TOPS | u/Middle_Chicken_2577: "the k230 has abt 17 tops" | r/meshtastic | 2025-07-08 | **unsupported assertion** — contradicted by Canaan |
| R-BUY | "Where do people buy CANMV K230 from?" | r/RISCV | 2024-05-08 | availability |
| R-RVV | "Kendryte K230 (RVV1.0 supported) available for remote access" | r/RISCV | 2024-05-09 | community interest |

## Software projects

| ID | Project | URL | Commit / branch | Licence | Stars |
|---|---|---|---|---|---|
| G1 | `Xinyuan-LilyGO/T-Display-K230` | GitHub | `bb831ab358b66f5bd9a87ecd7c580fee4537492e`, `main` | **none declared** | 1 |
| G2 | `Xinyuan-LilyGO/T-Display-K230_canmv_rt` | GitHub | `main`, pushed 2026-08-03 | none declared | 25 |
| G3 | `Xinyuan-LilyGO/T-Display-K230-nRF52840` | GitHub | `4646a728580739d487126f47a521e9b8032b3c2c`, `master` | none declared | 0 |
| G4 | `Xinyuan-LilyGO/T-Display-K230-nRF9151` | GitHub | `ed4ecbe34162dec9b81213a400198125bbd6e36f`, `main` | none declared | 0 |
| G5 | `kendryte/k230_linux_sdk` | GitHub | `dev` | BSD-2-Clause | 62 |
| G6 | `kendryte/k230_sdk` | GitHub | `main` | BSD-2-Clause | 273 |
| G7 | `kendryte/canmv_k230` | GitHub | `canmv_k230` | none declared | 119 |
| G8 | `sipeed/MaixPy` | GitHub | `main` | NOASSERTION | 843 |
| G9 | `oreboot/oreboot` | GitHub | `main` | GPL-2.0 | 1795 |
| G10 | `intx82/k230-debian` | GitHub | `6.6`, last push 2024-12-03 | BSD-2-Clause | 1 |
| G11 | `ruyisdk/linux-xuantie-kernel` | GitHub | `7d4e1f444f461dbe3833bd99a4640e7b6c2cd529` | GPL-2.0 (kernel) | — |
| G12 | LVGL, vendored | — | `59dc7e436ae97a25e32656739ea6a943f9f11b6a` + 4 LilyGO patches | MIT | — |
| G13 | Nordic Serial LTE Modem, vendored | — | `13c80da97fe4d55ecb5a9745834d97be22821307` + 5 LilyGO patches | Nordic 5-clause | — |

⚠ **Every LilyGO repository for this product has no licence file.** Redistribution status of
their source and prebuilt firmware is therefore **unknown**.
