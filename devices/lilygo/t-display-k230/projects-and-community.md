# T-Display K230 — software projects and community

Every firmware, SDK and project targeting this board or the K230 generally, with repository,
pinned revision, licence, build route and board-support status. Then the community record, with
each contribution labelled by evidence type.

---

## Part 1 — Software projects

### Targeting this board specifically

| Project | Repository | Revision | Licence | Build | Board support |
|---|---|---|---|---|---|
| **T-Display-K230 BSP + launcher** | `Xinyuan-LilyGO/T-Display-K230` | `bb831ab358b66f5bd9a87ecd7c580fee4537492e` (`main`), 2026-09-03, **v0.2.4** | ⚠ **none declared** | `./scripts/{setup_ubuntu,apply_to_sdk,build_sdcard_image}.sh` | **Complete** — this *is* the board's software |
| **nRF52840 AT firmware** | `Xinyuan-LilyGO/T-Display-K230-nRF52840` | `4646a728580739d487126f47a521e9b8032b3c2c` (`master`), 2026-08-23 | ⚠ **none declared** | PlatformIO `nordicnrf52` / `nrf52840_dk_adafruit` | Complete; prebuilt UF2 (`r4`, 2026-08-16) and bootloader shipped |
| **nRF9151 Serial LTE Modem** | `Xinyuan-LilyGO/T-Display-K230-nRF9151` | `ed4ecbe34162dec9b81213a400198125bbd6e36f` (`main`), 2026-08-14 | ⚠ **none declared** | NCS v3.4.0 + `./build_serial_modem.sh` | Complete; source only, no prebuilt |
| **T-Display-K230_canmv_rt** | `Xinyuan-LilyGO/T-Display-K230_canmv_rt` | `main`, 2026-08-03, **25★** | ⚠ **none declared** | not examined | **Not examined in this pass.** 745 MB repository; the name suggests a CanMV/RT-Smart variant for this board and it has more stars than the main BSP. **A real gap** — see below. |

> ⚠ **Not one LilyGO repository for this product carries a licence file.** Redistribution status
> of their source *and* of the prebuilt nRF52840 binaries is **unknown**. Nothing from them has
> been copied into this repository.

### K230 platform software

| Project | Repository | Revision / branch | Licence | Stars | Board support |
|---|---|---|---|---|---|
| **k230_linux_sdk** | `kendryte/k230_linux_sdk` | branch **`dev`**; LilyGO pins `22d02c6b6783a57a3aca7eb3160e313e772cb710` | **BSD-2-Clause** | 62 | **The upstream this board builds from.** Linux-only. |
| **k230_sdk** (dual-OS) | `kendryte/k230_sdk` | `main`, last push 2025-09-12 | BSD-2-Clause | 273 | Targets Canaan EVB/CanMV. **No profile for this board.** RT-Smart on CPU1 + Linux on CPU0. Docker image `ghcr.io/kendryte/k230_sdk`. |
| **CanMV (MicroPython)** | `kendryte/canmv_k230` | branch **`canmv_k230`**, 2026-09-03 | none declared | 119 | Runs on K230. **No board profile** — display, touch and keyboard would need porting. |
| **MaixPy** | `sipeed/MaixPy` | `main`, 2026-08-28 | NOASSERTION | 843 | Same situation. Sipeed's Python runtime. |
| **oreboot** | `oreboot/oreboot` | `main`, 2026-07-13 | **GPL-2.0** | **1795** | **Has K230 support.** Maintainer states it boots Linux from mask ROM over USB in ~3 s. Board-specific status unknown, but this is the most credible recovery lever. |
| **k230-debian** | `intx82/k230-debian` | branch `6.6`, last push **2024-12-03** | BSD-2-Clause | 1 | Debian rootfs experiment. Low activity; a starting point, not a distribution. |
| **linux-xuantie-kernel** | `ruyisdk/linux-xuantie-kernel` | `7d4e1f444f461dbe3833bd99a4640e7b6c2cd529` | GPL-2.0 | — | The kernel this board actually runs |
| **nncase** | Canaan | version must match the SDK | — | — | KPU model compiler |
| **RT-Thread / RT-Smart** | upstream | — | Apache-2.0 | — | CPU1 OS in the dual-OS SDK; not used by this board's image |
| **Zephyr** | upstream | — | Apache-2.0 | — | ❌ **No K230 SoC or board support upstream** as of 2026-09-04 |

### Vendored dependencies inside the BSP — identity and delta

Both are properly pinned, which is worth crediting.

| Tree | Upstream pin | Modifications | Reproducible? |
|---|---|---|---|
| **LVGL** | commit `59dc7e436ae97a25e32656739ea6a943f9f11b6a` (in the directory name) | **4 patches**, retained beside the pin: `0001` pcpp Python preprocessor fallback · `0002` K230 plane rotation in the DRM backend · `0003` FreeType fixed-colour-bitmap scaling · `0004` K230 staging scanout buffer | **Yes** — upstream commit + patch series |
| **Nordic Serial LTE Modem** | submodule at `13c80da97fe4d55ecb5a9745834d97be22821307` | **5 patches**: `0001` GNSS NMEA URC + LED · `0002` optional XDFU · `0003` UART diag · `0004` GNSS NMEA URC worker · `0005` LED AT control | **Yes** |
| Kernel | `linux-xuantie-kernel` @ `7d4e1f44…` | **30+ numbered patches** `0025`–`0064`, plus one **retained `.rejected`** file | **Yes** |

Keeping `linux/rejected/0044-drm-canaan-use-wc-allocation-for-dumb-buffers.rejected` in the tree
is good practice — it records that write-combine dumb-buffer allocation was attempted and did not
apply, which saves the next person the experiment.

### Community projects

| Project | Status | Evidence |
|---|---|---|
| **Independent Meshtastic UI** | Announced 2026-06-02, "will publish a repo once complete". **No repository located** as of 2026-09-04. | announced project |
| `kendryte_boot` | Boot tool by the oreboot maintainer, "on GitHub" per the author | demonstrable project, URL not captured |
| `Bruce` firmware | A user asked in r/brucefw (2025-10-23) about device support. Bruce is ESP32-only; **not applicable** to a RISC-V board. Recorded as a refuted association. | hearsay, refuted |

### Gap: `T-Display-K230_canmv_rt`

This repository has **25 stars — more than the main BSP's 1** — was created 2025-03-05 (two weeks
before the product launched) and was last pushed 2026-08-03. Its 745 MB size suggests vendored
SDK content. It was **not cloned or examined** in this pass because of its size, and that is the
largest single unexplored software artifact for this board. Anyone continuing this work should
start there.

---

## Part 2 — Community

Evidence labels: **firsthand measurement** · **firsthand ownership** · **demonstrable project** ·
**announced project** · **informed interpretation** · **opinion** · **hearsay** · **unsupported
assertion**.

### Where the community is

| Venue | Activity | Note |
|---|---|---|
| **r/LilyGO** | Active; **LilyGO staff answer as `u/LilyGoXinyuan`**, usually within a day | The de-facto support channel |
| **r/meshtastic** | The single largest thread about this board (187 pts / 40 comments) | Mesh users found it before RISC-V users did |
| **r/RISCV** | Discusses the K230 chip and CanMV boards; **has never discussed the LilyGO board** | Notable absence |
| **CNX-Software** | Covered CanMV-K230 (2023) and BPI-CanMV-K230D-Zero (2024); **never this board** | Site search returned 5 K230 results, none about it |
| **Hackaday** | **Nothing found** | |
| GitHub issues | `.github/workflows/issues.yaml` exists in every LilyGO repo; issue traffic not examined | gap |
| Chinese sources (Bilibili, Zhihu) | **Not searched directly** | Recorded gap |

### The anecdotes that matter

**The brick — firsthand ownership, 2026-08-21 and 2026-08-28, u/phirzcolru**

> "extensive attempts to work with this device. i managed to get an mp3 player and notepad
> working for it. but once i attempted to turn on the 'fun' features it bricked it. its not quite
> user friendly. i will be switching to an orange pi… that said im no programmer. the display is
> awesome looking."

> "I also saw the newer k230 stuff. Alas my board is still unresponsive to boot pin and term. I
> think I flashed it into mmc mode vs sd card and it's stuck. Now that you have the keyboard and
> the esp I might purchase again… Still a great board for the record."

The most consequential report about this product. Note the last sentence of each: the user is not
hostile, he is stuck. Also note "**and the esp**" — a possible independent hint at
[`GC-2`](gaps-and-conflicts.md), or an echo of the wiki.

**The bare board — firsthand ownership, 2026-08-20, u/Opposite_Future2602**

> "I got one of these but it was just the screen and motherboard on risers in the package. Just
> fair warning, I've also been completely unable to figure out how to even get an OS installed."

> "The CPU is in the name, it uses a Kendryte K230. It's a RISC-V chip that's probably capable of
> running some cut down form of Linux. The problem is I haven't been able to find anyone
> developing for this board, and RISC-V chips typically have very finicky bootloaders where you
> can't just install any common OS."

Accurate for the situation before 2026-08-13. LilyGO replied the next day with the repository and
wiki links.

**oreboot — demonstrable project, 2025-03-26, u/CyReVolt**

> "I'm a developer of the oreboot firmware project, and we have support for the K230, can boot
> Linux from mask ROM over USB in 3 seconds. You can find a demo on my YouTube channel. Also
> check out the kendryte_boot tool that I made, it's on GitHub."

Author of the project making a claim about his own work, with a demo. **The single most useful
recovery lead** in the whole corpus.

**The keyboard ships without a case — firsthand ownership, 2026-08-13, u/Circuitnaut24**

> "I can confirm it does not. It seems like the encased K230 model that goes with keyboard is a
> newer one that isn't listed on the website yet."

Independently corroborates the wiki's undocumented "Cased Version".

**Ethernet — firsthand observation, 2025-07-07, u/Nobodytoyou_**

> "It's very interesting, though the ethernet port is an odd choice. It just seems too big for
> this type of device, lol."

**Missing Bluetooth — firsthand observation, 2025-07-08**

> u/skeptikoz: "But Bluetooth seems to be missing — might that be an impediment to porting the…"
> u/Hot-Win2571: "You're right. I don't see BT labels on the board, and the K230 page does not
> mention Bluetooth."
> u/ExcitingTabletop: "USB C Bluetooth adaptors are $20, but that seems like a REALLY weird
> omission."

Three independent observers reaching the same conclusion the BSP confirms.

**Value judgement — opinion, 2025-07-08, u/skeptikoz**

> "It seems more of a development platform than an end-user product, but WOW that is a lot of
> bang for <$100! Two RISC-V cores, one fast with a Vector Processor, a KPU capable of running
> ResNet or Yolo in real-time, 2D and 3D graphics engines, HDMI out, multiple MIPI camera ports,
> the list goes on. LoRa is icing on top!"

The most accurate one-paragraph summary of the product written by anyone, including LilyGO.

**Battery scepticism — opinion, 2025-07-07, u/Ryan_e3p**

> "Seems like it's getting to the point where I'd rather just get a phone de-Google'd, and install
> Meshtastic on it. It seems like the battery life on this would be less then it would be with a
> phone and a regular nRF node on a 1000mAh battery."

Unmeasured, and nobody has measured it since. See [`performance.md`](performance.md).

**MQ-Pro comparison — informed interpretation, 2025-07-09, u/Nanocupid**

> "This board has 1G ram and a 1.6GHz RVV1 'big' core. It's basically more powerful than the 1GHz
> non RVV core in my MQ-Pro, and has 8x the memory."

Correct arithmetic on published specifications. **Not a measurement.**

**"17 TOPS" — unsupported assertion, 2025-07-08, u/Middle_Chicken_2577**

> "(k230 is the new k210 which i have in my maixcam pro)… sounds fun, since the k230 has abt 17
> tops and therefore can surely do stuff."

Contradicted by every Canaan document, which publish **no** TOPS figure. Recorded only because it
circulates.

**ATAK interest — opinion, 2025-07-07, u/Electroboy101 (31 points)**

> "If you could run ATAK on this, it might just become even more interesting."

The top-voted comment on the largest thread. ATAK is Android; this is not an Android device. It
tells you what the mesh community wants from a Linux handheld with a screen, GPS and LoRa.

**IP rating — opinion / requirement, 2026-08-20, u/No-Craft-7979**

> "Wish there were more IPX water resistant options across all your product lines. I prototype
> field devices. The designs are not taken seriously because they are afraid of water."

**Purchasing confusion — 2026-08-20, u/Silly_Abalone_288**

> "I'm confused on what is what I'm in the USA and I want the kit with the keyboard. What do I
> buy?"

**Unanswered.** See [§1 of the README](README.md#1-identity-skus-and-variants) — the answer is two
SKUs, `K256-03` + `K256-04`.

### Prevalence — stated honestly

**Four** distinct firsthand-ownership reports were found, across **26 comments** in the two
largest threads and **6 threads** in total mentioning the product by name. That is the entire
sample. It supports statements like "at least one owner bricked a board this way", and supports
nothing at all about how often it happens.
