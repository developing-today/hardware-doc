# Feature guides — Cap LoRa-1262 (U214)

| Feature | Guide | Status |
|---|---|---|
| LoRa (SX1262) | [`lora.md`](lora.md) | documented from schematic + vendor code + Meshtastic upstream; **not hardware-tested here** |
| GNSS (ATGM336H-6N / AT6668) | [`gnss.md`](gnss.md) | documented; known documentation trap on the UART pins |
| I/O expander + antenna RF switch | [`io-expander-and-rf-switch.md`](io-expander-and-rf-switch.md) | documented; also the runtime Cap-detection mechanism |
| Power rail + Grove pass-through | [`power-and-grove.md`](power-and-grove.md) | documented; enable-net polarity unresolved |

Not applicable to this board: display, touch, audio, storage, USB, battery — all belong to
the host. See `devices/m5stack/cardputer-adv/` (parallel research pass).

Cross-cutting: [`guides/lora`](../../../../guides/lora/README.md) ·
[`guides/nfc`](../../../../guides/nfc/README.md) (relevant only for the sibling
[Cap CC1101](../../cap-cc1101/features/nfc.md)).
