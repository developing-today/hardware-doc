# Compatibility and status — Cap LoRa-1262 (U214)

Keyed by host, firmware and version. Snapshot 2026-09-04. **Nothing in this table was
tested by this research pass**; every row states its own evidence class.

## 1. Hosts

| Host | Fits? | Evidence |
|---|---|---|
| **Cardputer-Adv (K132-ADV)** | ✅ designed for it | vendor **[DOC]**, schematic annotates every Cap-Bus pin with its Cardputer-Adv GPIO |
| **CardputerZero** | ✅ claimed | vendor **[DOC]** on both the U214 and U219 pages. Note the CC1101 announcement says band-select SW0 moves from **G13 (ADV) to G14 (Zero)** — so *pin mapping differs between hosts* and firmware must know which host it is on |
| **Cardputer P4 ("Next")** | ⛔ unreleased; claimed compatible | **[COM]** M5Stack community post, [r/CardPuter 2026-08-28](https://old.reddit.com/r/CardPuter/comments/1w0nwti/) |
| **Cardputer K132 / K132-V11 (original)** | ❌ **no** | The original has only a Grove HY2.0-4P (`PORT.CUSTOM`, G2/G1) and no expansion bus **[DOC]**. Community answer the day the ADV launched: *"No, not enough gpio pins"* — u/IceSubstantial5572, [r/CardPuter 2025-09-04](https://old.reddit.com/r/CardPuter/comments/1n8d8j2/) |
| PaperMono / other M5Stack cores | ❌ | different bus entirely |

## 2. Firmware

| Firmware | LoRa | GNSS | Status | Evidence |
|---|---|---|---|---|
| **Meshtastic** ≥ 2.7.20 | ✅ | ✅ | **Upstream official.** Antenna switch broken until 2.7.24 | **[SRC]** variant files + commit history |
| Meshtastic 2.7.19 and earlier | ❌ | ❌ | No variant existed. Users ran third-party M5Burner builds and hit "very common issues" — u/thetestbug, [r/CardPuter 2026-02-15](https://old.reddit.com/r/CardPuter/comments/1r4waav/), linking PR #9540 as the fix in progress | **[COM]** |
| **M5Stack Arduino examples** | ✅ | ✅ | Published; auto-detects U214 vs U201 | **[DOC]** |
| **UiFlow2** | ✅ | ✅ | Vendor page exists; unexplored here | **[DOC]** |
| **MeshCore** (community) | ✅ | ✅ | `MeshCore-Cardputer-ADV` v1.1.0 released 2026-01-27, 104 upvotes / 42 comments | **[COM]** |
| **Plai** (d4rkmen) | ✅ | ✅ | Standalone Meshtastic node firmware, 175 stars | **[COM]** |
| **Bruce** | ✅ (sub-GHz focus) | ✅ | Used as a GNSS-diagnosis tool by owners | **[COM]** |
| **LoRaWAN (any stack)** | ❓ | — | **Nothing demonstrated.** No example, no project, no regional-parameters config located | negative result, `executed-success` |

## 3. Version-specific reports worth keeping

| Date | Report | Class |
|---|---|---|
| 2026-02-15 | Meshtastic on Cardputer-Adv "a disaster: on esp32 wifi is unusable: web server crashes, on esp32-s3 — same story with bluetooth" — u/d4rkmen (author of Plai), [r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1r4waav/) | firsthand developer opinion, pre-upstream-support |
| 2026-06-12 | Battery percentage unreliable with a Cap fitted; several owners agree the reading is voltage-only with no BMS. u/pyreht adds that the host's 5 V IN/OUT switch perturbs the G10 battery-sense reading when the Grove port is loaded, [r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1u3qeez/) | firsthand, host-side |
| 2026-08-22 | Owner could never get Meshtastic working; thread resolves to a wrong-band antenna for NA, [r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1vvlcs9/) | firsthand, resolved |
| 2026-08-28 → 09-02 | "GNSS dead on arrival" → resolved by manually setting Meshtastic's GPS RX/TX pins; separately, M5Launcher **2.8.0** broke GPS across firmwares and the launcher author confirmed a fix in Beta 2.9, [r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1w0gv7y/) | firsthand + maintainer response |
| 2026-01-17/18 | Meshtastic position 2 miles off vs vendor demo "spot on" — cause was Meshtastic's default degraded channel precision, not the receiver, [r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1qf0z9v/) | firsthand, resolved |

## 4. Untested / unknown

- Every RF number: range, sensitivity, output power at the connector, spurious emissions.
- Current draw in any resolved state (the vendor gives two unconditioned aggregates).
- LoRa TX desensitising the co-located GNSS front end.
- Behaviour of the Cap across host deep-sleep cycles.
- Whether `0x43` collides with any commonly-used Grove unit in practice.
- LoRaWAN of any kind.
