# T-Display K230 — product history, family and lineage

## Timeline

Every row is dated from a primary source; Shopify `created_at`/`published_at` values are exact to
the minute in `+08:00` (LilyGO's timezone) and are the strongest dating evidence available.

| Date | Event | Source |
|---|---|---|
| 2018 | Kendryte **K210** — the line's origin: dual RV64GC @ 400 MHz, on-die SRAM, no DDR | — |
| 2021-07-09 | Kendryte **K510** — tri-core RISC-V, up to 3 TOPS | CNX-Software |
| **2023-07-06** | **K230 datasheet V1.0** | Canaan, document revision date |
| 2023-09-15 / 2023-10-11 | CanMV-K230 board documents dated in `k230_docs` | Canaan repository |
| 2023-10-18 / 2023-10-24 | CanMV-K230 covered on r/RISCV and CNX-Software | community, blog |
| 2023-12-15 | "How to run baremetal program on a Canaan Kendryte K230 development board?" | r/RISCV |
| 2024-05-08 | "**Where do people buy CANMV K230 from?**" — sourcing difficulty | r/RISCV |
| 2024-05-09 | "Kendryte K230 (RVV1.0 supported) available for remote access" | r/RISCV |
| 2024-11-18 | **BPI-CanMV-K230D-Zero at $29** | CNX-Software |
| 2024-12-03 | `intx82/k230-debian` last push | GitHub |
| **2025-03-21 13:52 +08** | **T-Display K230 created on lilygo.cc** | Shopify `created_at` |
| **2025-03-21 14:22 +08** | **T-Display K230 published** — 30 minutes later | Shopify `published_at` |
| 2025-03-21 | Announced on **r/LilyGO** | Reddit |
| 2025-03-24 | First user questions: "can it run linux?" · "I'd really like to see more options to add external antennas for wifi, lora and gps" | Reddit |
| 2025-03-25 | LilyGO answers "Yes" and links Canaan's developer site | Reddit |
| **2025-03-26** | **oreboot maintainer**: oreboot supports K230, boots Linux from mask ROM over USB in ~3 s; also "**Already sold out**" | Reddit |
| 2025-03-27 | LilyGO: "sales will resume soon" | Reddit |
| 2025-04-25 | "T-Display K230, integrated AMOLED display and can run Linux or RTOS" | r/LilyGO |
| 2025-07-04 | "T-Display K230 and T-Lora Pager have some stock available" | r/LilyGO |
| **2025-07-07** | **r/meshtastic post — 187 points, 40 comments.** The product's largest moment of public attention, and it came from the *mesh* community, not the RISC-V one | Reddit |
| 2025-07-09 | `k230-debian` and MQ-Pro comparison raised in that thread | Reddit |
| 2026-05-10 | "any support for meshtastic yet?" | Reddit |
| **2026-06-02** | "I am working on a **full Meshtastic UI app** for this and will publish a repo once complete" | Reddit |
| **2026-07-28** | **Keyboard announced** on r/LilyGO; LilyGO confirms the P4 keyboard is separate and "already in production" | Reddit |
| **2026-08-06 09:31 +08** | **T-Display K230 Kit created** | Shopify |
| **2026-08-13 02:10 UTC** | **`Xinyuan-LilyGO/T-Display-K230` repository created** | GitHub |
| 2026-08-13 | Owner confirms the keyboard ships **without** a case for the main board | Reddit |
| 2026-08-13 06:52 UTC | `T-Display-K230-nRF52840` repository created | GitHub |
| 2026-08-14 02:59 UTC | `T-Display-K230-nRF9151` repository created | GitHub |
| 2026-08-16 | nRF52840 AT firmware build **`r4`** | firmware filename |
| **2026-08-20 15:10 +08** | **T-Display K230 Kit published**; announced on r/LilyGO (83 points) | Shopify, Reddit |
| 2026-08-20 | Owner: received bare board on risers, "completely unable to figure out how to even get an OS installed" | Reddit |
| **2026-08-21** | **Owner reports bricking the board** | Reddit |
| 2026-08-21 | LilyGO responds, links the new repository and wiki | Reddit |
| 2026-08-23 | nRF52840 repository last push | GitHub |
| 2026-08-25 | LilyGO points a user to the **T-Display P4 keyboard** product page | Reddit |
| 2026-08-28 | Same owner: "my board is still unresponsive to boot pin and term" | Reddit |
| **2026-09-03** | **BSP v0.2.4** — PicoClaw, Meshtastic map tiles, storage expansion, async I²C scan, new F-key defaults | CHANGELOG |
| 2026-09-04 | This research snapshot | — |

## The seventeen-month gap

The board went on sale **2025-03-21**. Its board-support repository was created **2026-08-13** —
**almost seventeen months later.** Everything a developer needs (the pin map, the kernel patches,
the launcher, the build scripts, the companion firmware) arrived in that three-week burst in
August 2026, at the same time as the keyboard.

That single fact explains almost every negative community report. The people who bought in 2025
had a beautiful screen, a RISC-V chip, and nothing else. One of them wrote in August 2026: *"The
problem is I haven't been able to find anyone developing for this board, and RISC-V chips
typically have very finicky bootloaders where you can't just install any common OS."* He was
right at the time.

It also means **the product you can buy today is materially different from the product reviewed
or discussed in 2025**, even though the hardware SKU `K256` is unchanged. Treat any pre-August-2026
commentary as describing a different situation.

## Family

### Within the T-Display series

| Product | SoC | Relationship |
|---|---|---|
| **T-Display K230** | Kendryte K230 (RISC-V) | this record |
| **T-Display P4** | Espressif ESP32-P4 | The direct sibling — same series, same idea, MCU class instead of application class. **Its keyboard is incompatible with the K230's, in both directions** (LilyGO, 2026-07-28). Its keyboard was "already in production" on 2026-07-28 and on sale by 2026-08-25. |
| T-Display-S3 and its many AMOLED/Long/Pro variants | ESP32-S3 | The volume products of the series. Documented separately in this repository by another session, expected at `devices/lilygo/t-display-s3*`. Not present at the time of writing, so no link is given. |
| T-Display-Keyboard | ESP32-D0WDQ6 | **A name trap.** An old ESP32 T-Display in a keyboard shell, with a 1.14″ 240 × 135 ST7789V. Nothing to do with the K230 keyboard. |
| T-Display C5, Bar, SF32, AMOLED-Lite | various | Same series, unrelated |

### The other LilyGO keyboard handhelds

**T-Deck**, **T-Deck Plus**, **T-Deck Pro**, **T-Deck MAX** are a *different series* — all
ESP32-S3, all with the small BlackBerry-style trackball keyboard. The T-Display K230 Kit is not a
T-Deck and does not share its keyboard, its firmware or its ecosystem. Community members
repeatedly compare the two on Wi-Fi quality and form factor, which is fair, but they are not
variants of each other.

### Other K230 hardware

| Board | Vendor | Variant | RAM |
|---|---|---|---|
| CanMV-K230 | Canaan | K230 | 512 MB |
| K230 DEMO BOARD (LP3) / USIP EVB (LP4) | Canaan | K230 | — |
| K230-SIP-EVB | Canaan | K230D | 128 MB |
| BPI-CanMV-K230D-Zero | Banana Pi | K230D | 128 MB |
| **T-Display K230** | LilyGO | K230 | **1 GB** |

**The LilyGO board has the most RAM of any published K230 board** — 2× the reference board and 8×
the SiP boards. Given that memory is the binding constraint on a K230 running Linux, that is the
board's strongest technical differentiator and it is not advertised as one.

## Culture

Three characteristics, each evidenced above:

1. **Ship first, document later.** Seventeen months, then everything at once.
2. **Support happens on Reddit.** `u/LilyGoXinyuan` answered on 2025-03-25, 2025-03-27,
   2026-07-28, 2026-08-21 and 2026-08-25 — usually within a day, usually with a GitHub link. For
   a product this new the subreddit is a better support channel than the wiki.
3. **Rapid iteration once started.** v0.2.2 → v0.2.4 inside the first three weeks, with the
   changelog entries showing real responsiveness (low-battery defaults tuned, nRF52840 ownership
   arbitration added, MTP layout fixed, F-key defaults changed).
