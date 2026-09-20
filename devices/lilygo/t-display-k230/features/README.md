# T-Display K230 — feature guides

One guide per fitted capability. Each answers a natural question, names the exact hardware path
through linked component records, and states its own evidence status.

**Repository-wide caveat for every guide here: nothing was executed on hardware.** The highest
evidence class reached anywhere in this set is `reported-working` — i.e. LilyGO's shipped BSP
does it, and the source that does it is cited.

| Guide | Question it answers | Hardware |
|---|---|---|
| [display.md](display.md) | How do I drive the AMOLED? | RM69A10 + K230 MIPI DSI |
| [touch.md](touch.md) | How do I read touch? | GT9895 |
| [keyboard.md](keyboard.md) | How do I read the QWERTY keyboard and its backlight? | TCA8418 + XL9555 |
| [camera.md](camera.md) | How do I capture and process images? | GC2093 + K230 ISP |
| [kpu-npu.md](kpu-npu.md) | How do I run a neural network on the NPU? | K230 KPU + nncase |
| [dual-core-riscv.md](dual-core-riscv.md) | How do the two RISC-V cores work, and how do I use RVV? | K230 CPU0/CPU1 |
| [wifi-and-bluetooth.md](wifi-and-bluetooth.md) | How do I get on Wi-Fi? Why is there no Bluetooth? | RTL8189FS + USB dongle |
| [ethernet.md](ethernet.md) | How do I use the RJ45? | USB Ethernet |
| [lora.md](lora.md) | How do I send LoRa / run Meshtastic? | SX1262 or LR2021 |
| [audio.md](audio.md) | How do I play and record audio? | K230 codec + MAX98357A |
| [microsd.md](microsd.md) | How do I use the SD card? | K230 MMC1 |
| [usb.md](usb.md) | How do I use USB host and gadget? | K230 USB 2.0 OTG ×2 |
| [battery-and-power.md](battery-and-power.md) | How do I read battery and configure charging? | BQ25896 + BQ27220 + PMU |
| [gpio-and-expansion.md](gpio-and-expansion.md) | What can I actually attach to the 40-pin header? | K230 GPIO/ADC/I²C/PWM |
| [nrf52840-ble.md](nrf52840-ble.md) | How do I do BLE? | nRF52840 over UART1 |
| [nrf9151-cellular-gnss.md](nrf9151-cellular-gnss.md) | How do I do cellular and GNSS? | nRF9151 over UART3 |
