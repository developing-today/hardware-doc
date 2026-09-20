# T-Display K230 — compatibility and status

Keyed by BSP version where known. **No entry in this file was verified on hardware by this
session**; the status column reflects what LilyGO states plus what community members report.

## LilyGO's own feature status — BSP v0.2.4 (2026-09-03)

### Stated **stable**

Camera · gallery · music · network radio · recorder · video player · terminal · MTP · Wi-Fi ·
Ethernet · display · audio · notification · battery · charger · sensor · keyboard · system
settings.

### Stated **beta**

| Feature | Caveat stated by LilyGO |
|---|---|
| **Meshtastic** | Chat, node display, map view, channel sharing work. **Voice/photo transfer requires LR2021**; SX1262 gets text only |
| LoRaWAN | — |
| **Xiaozhi** voice assistant | Needs network **and** a compatible Xiaozhi service; wake word only while the app owns the mic |
| **PicoClaw** | Needs network **and** an OpenAI-compatible API key. The board does not run a model locally |
| nRF9151 cellular / GNSS | Requires the keyboard base |
| nRF52840 UART DFU | Ownership arbitrated against Meshtastic BLE since v0.2.2 |

### Stated **not included / user-supplied**

NES ROMs · offline map tiles · user media. **HDMI** is "kept as a diagnostic feature"; AMOLED is
the default path.

### Runtime-optional, detected only if present

nRF9151 · nRF52840 · TCA8418 · BQ27220 · BQ25896 · XL9555 · AHT20. On a bare `K256` board, none
of these exists and the corresponding UI does not appear.

## Community-reported status

| Report | Date | Evidence class | Status |
|---|---|---|---|
| **Board bricked** by a boot-medium change; unresponsive to boot pin and terminal afterwards | 2026-08-21 / 2026-08-28 | **firsthand ownership** | **Failing.** Not contradicted by anyone. No recovery reported. |
| Got "an mp3 player and notepad working"; then the "fun" features bricked it | 2026-08-21 | firsthand ownership | Partial |
| "completely unable to figure out how to even get an OS installed" (bare board, pre-BSP era) | 2026-08-20 | firsthand ownership | Failing at the time; the BSP now exists |
| Keyboard base does **not** include a case for the main board | 2026-08-13 | firsthand ownership | Confirmed limitation |
| Early units shipped as bare board on risers — no case, no battery | 2026-08-20 | firsthand ownership | Confirmed for pre-kit purchases |
| Ethernet port physically present and large for the form factor | 2025-07-07 | firsthand observation | Confirmed |
| No Bluetooth markings visible; K230 page does not mention Bluetooth | 2025-07-08 | firsthand observation | Consistent with the BSP |
| oreboot supports K230; boots Linux from mask ROM over USB in ~3 s | 2025-03-26 | **demonstrable project**, author's own statement | Reported-working **for K230 generally**, not demonstrated on this board |
| Independent Meshtastic UI in progress, "lots of challenges adapting to the K230's preferred formats" | 2026-06-02 | announced project | In progress, no repository |
| "sold out" days after launch | 2025-03-26 | firsthand | Availability, since resolved |

**Prevalence:** four distinct firsthand-ownership reports were found across **26 comments in the
two largest threads** reviewed. That is the whole sample. It is far too small to support any
statement about how common bricking is — only that it happened at least once, to someone who
described the exact sequence.

## Software-version compatibility

| Component | Version this board is pinned to | Notes |
|---|---|---|
| Kendryte Linux SDK | `22d02c6b6783a57a3aca7eb3160e313e772cb710` (`dev`) | Recorded in `k230_bsp/metadata/upstream_sdk_commit.txt` |
| Kernel | `ruyisdk/linux-xuantie-kernel` @ `7d4e1f444f461dbe3833bd99a4640e7b6c2cd529`, defconfig `k230` | **Not mainline** |
| Toolchain | XuanTie GCC `Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V3.0.2` | Hard-coded `/opt/toolchain` path |
| LVGL | `59dc7e436ae97a25e32656739ea6a943f9f11b6a` + 4 LilyGO patches | Upstream pin retained |
| NCS (nRF9151) | **v3.4.0** | Repository-relative install |
| Nordic Serial LTE Modem | `13c80da97fe4d55ecb5a9745834d97be22821307` + 5 patches | Upstream pin retained |
| SoftDevice (nRF52840) | **S140 6.1.1** | In the shipped bootloader |
| PlatformIO (nRF52840) | `nordicnrf52`, board `nrf52840_dk_adafruit` | Arduino framework |

**Everything is pinned.** That is unusually good hygiene and it means a rebuild in a year should
still produce the same image — provided the XuanTie tarball and the upstream Git remotes survive.

## Known incompatibilities

| Claim | Status |
|---|---|
| Arduino IDE for the K230 | **Incompatible.** LilyGO's own FAQ says so. |
| ESP-IDF | **Incompatible.** Different architecture and vendor. |
| The T-Display **P4** keyboard | **Incompatible** with this board — LilyGO, 2026-07-28 |
| The T-Display K230 keyboard on a P4 | **Incompatible** — same source |
| Mainline Linux | **Not supported.** Vendor kernel only. |
| Zephyr | **No K230 support upstream** as of 2026-09-04 |
| CanMV / MaixPy | Run on K230; **no board profile for this board** — display, touch and keyboard need porting |
| Canaan `k230_evb_defconfig` images | Boot, but drive none of this board's peripherals |
| Mainline RVV-1.0 binaries | Not interchangeable with the shipped `-mrvv-v0p10-compatible` userspace |
