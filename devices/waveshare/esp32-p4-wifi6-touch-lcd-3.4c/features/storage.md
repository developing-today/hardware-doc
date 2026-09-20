# How do I mount the microSD card? — ESP32-P4-WIFI6-Touch-LCD-3.4C

> Evidence status: **pins read from the schematic 2026-08-24. Untested on hardware.**
> Applies equally to the [4C](../../esp32-p4-wifi6-touch-lcd-4c/README.md).

## Pin map

Read from the schematic (connector `SD1`), not from the demo:

| SD1 pin | Signal | GPIO |
|---:|---|---:|
| 1 | DAT2 | **41** |
| 2 | CD/DAT3 | **42** |
| 3 | CMD | **44** |
| 4 | VDD | `SD1_VDD` — **switched, see below** |
| 5 | CLK | **43** |
| 6 | VSS | GND |
| 7 | DAT0 | **39** |
| 8 | DAT1 | **40** |
| 9 | CD (card detect) | destination not traced |
| 10 | GND | — |
| — | **VDD power switch** | **45** |

Full 4-bit SDIO is wired, so `slot_config.width = 4` is supported.

## The part every demo misses: GPIO45 powers the card

`SD1_VDD` is gated by an **AO3401 P-channel MOSFET** whose gate is driven by **GPIO45**. The card
has no power until that switch is turned on, and **no shipped demo drives it**.

If you write SDMMC code from scratch, configure GPIO45 *before* `sdmmc` init or the card will not
enumerate — with symptoms indistinguishable from a bad card or bad wiring.

Because it is a P-channel device high-side switching the rail, the gate is pulled **low to turn the
card on**. That polarity is **inferred from the topology**, not stated on the schematic. Verify it
before trusting it; if the card does not appear, try the other level.

The upside: you can power-cycle a wedged card in software without resetting the board.

```c
gpio_config_t pwr = {
    .pin_bit_mask = 1ULL << 45,
    .mode = GPIO_MODE_OUTPUT,
};
gpio_config(&pwr);
gpio_set_level(45, 0);        // P-MOSFET: low = card powered.  INFERRED - verify.
vTaskDelay(pdMS_TO_TICKS(10));
```

## The BSP takes a different route

`bsp_sdcard_mount()` uses **`SDMMC_HOST_SLOT_0`** with an **on-chip LDO (channel 4)** for power,
and does **not** touch GPIO45. Slot 0 is IO-MUX fixed-function, which is why the pins are not
configurable and why the generic demo defaults happened to be correct.

Two consequences: it corroborates that microSD and the C6 radio share one DW-MMC host (card on
slot 0, radio on slot 1), and it leaves the GPIO45 question open — see
[C13](../gaps-and-conflicts.md#c13--microsd-sits-on-a-switched-rail-no-demo-enables). If you use
the BSP, try it before adding GPIO45 handling.

Bus is 4-bit at `SDMMC_FREQ_HIGHSPEED` (40 MHz), with card-detect unused (`SDMMC_SLOT_NO_CD`).

## Mounting

```c
sdmmc_host_t host = SDMMC_HOST_DEFAULT();
sdmmc_slot_config_t slot_config = SDMMC_SLOT_CONFIG_DEFAULT();
slot_config.width = 4;
slot_config.clk = 43;
slot_config.cmd = 44;
slot_config.d0  = 39;
slot_config.d1  = 40;
slot_config.d2  = 41;
slot_config.d3  = 42;
slot_config.flags |= SDMMC_SLOT_FLAG_INTERNAL_PULLUP;

esp_vfs_fat_sdmmc_mount("/sdcard", &host, &slot_config, &mount_config, &card);
```

`SDMMC_SLOT_FLAG_INTERNAL_PULLUP` comes from the upstream example. Internal pull-ups are weak;
whether this board fits external ones was not determined. If 4-bit is unreliable, drop to
`width = 1` to isolate the problem.

## About the shipped `03_sdmmc` demo

It is **unmodified upstream Espressif code**, and its `IDF_TARGET_ESP32P4` Kconfig defaults
(`CMD=44, CLK=43, D0=39`) **happen to be correct** for this board — Waveshare followed Espressif's
reference pin assignment.

It works by design convergence, not by board-specific configuration. Two consequences:

1. It is **not evidence** about this board. It would look equally authoritative if it were wrong.
2. It does **not** drive GPIO45, so it depends on the card rail being on by some other means.

See [C1](../gaps-and-conflicts.md#c1--microsd-pin-assignment--resolved-2026-08-24) and
[C13](../gaps-and-conflicts.md#c13--microsd-sits-on-a-switched-rail-no-demo-enables).

## Resource conflict — SD and Wi-Fi are both SDIO

The board has two SDIO consumers: this card slot and the SDIO link to the ESP32-C6 radio. Whether
they use separate SDMMC host peripherals or share one is **unresolved** — the P4 has more than one
host, so separate hosts are plausible, but the schematic was not traced for this.

**A community Linux port states they are mutually exclusive** — *"P4 exposes one DW-MMC host"*,
with microSD on slot 0 and the C6 link on slot 1. That is the best answer available, but it is
community evidence about a Linux port and is unvalidated on hardware.

**Do not assume SD and Wi-Fi coexist.** See [wifi-and-bluetooth.md](./wifi-and-bluetooth.md).

## Limits

| Limit | Value | Kind |
|---|---|---|
| Bus width | 4-bit wired | Board (schematic) |
| Interface | SDIO 3.0 | Vendor claim |
| Throughput | **Unknown — not measured** | — |
| Max card capacity | **Not stated** | — |

## Pitfalls

1. **Forgetting GPIO45.** The most likely cause of "card not detected" on this board.
2. **Assuming GPIO45 polarity.** Inferred, not confirmed.
3. **Assuming SD + Wi-Fi coexist.** Both SDIO; unverified.
4. **Treating the demo as board evidence.** It is right by coincidence.

## Open questions

- GPIO45 active level — confirm on hardware.
- Card-detect (SD1 pin 9) destination.
- External pull-ups fitted?
- ~~Does the card slot share an SDMMC host with the C6 link?~~ — **likely yes**; confirm on hardware.

## Related

- [Full pinout](../pinouts-and-buses.md#microsd--connector-sd1)
- [Wi-Fi and Bluetooth](./wifi-and-bluetooth.md) — the other SDIO consumer
- [microSD / SDMMC generic record](../../../../components/generic/micro-sd-sdmmc/README.md)
