#!/usr/bin/env python3
"""ESP32-P4 QFN104 physical pin -> signal name, from datasheet v0.7 Table 2-1.

Transcribed 2026-08-24 from esp32-p4-datasheet.pdf pages 14-16 (the copy held at
doc/hardware/components/espressif/esp32-p4/artifacts/). Used to convert the
reference-designator pin numbers in the Tanmatsu IPC-D-356 fabrication netlist
into GPIO numbers, so documented pinouts can be checked against actual copper.
"""
PINS = {}
# contiguous GPIO runs: (first_pin, first_gpio, count)
for first, gpio, n in [(1,1,8),(10,9,7),(17,16,4),(22,20,4),(52,24,2),(55,26,4),
                       (60,30,2),(63,32,4),(68,36,3),(80,39,5),(86,44,5),
                       (92,49,4),(97,53,2)]:
    for i in range(n):
        PINS[first+i] = f"GPIO{gpio+i}"
PINS[104] = "GPIO0"
for p, nm in {9:"VDD_LP",21:"VDD_IO_0",26:"VDD_HP_0",27:"FLASH_CS",28:"FLASH_Q",
  29:"FLASH_WP",30:"VDD_FLASHIO",31:"FLASH_HOLD",32:"FLASH_CK",33:"FLASH_D",
  34:"DSI_REXT",35:"DSI_DATAP1",36:"DSI_DATAN1",37:"DSI_CLKN",38:"DSI_CLKP",
  39:"DSI_DATAP0",40:"DSI_DATAN0",41:"VDD_MIPI_DPHY",42:"CSI_DATAN0",
  43:"CSI_DATAP0",44:"CSI_CLKP",45:"CSI_CLKN",46:"CSI_DATAN1",47:"CSI_DATAP1",
  48:"CSI_REXT",49:"USB_DM",50:"USB_DP",51:"VDD_USBPHY",54:"VDD_HP_1",
  59:"VDD_PSRAM_0",62:"VDD_IO_4",67:"VDD_PSRAM_1",71:"VDDO_FLASH",
  72:"VDDO_PSRAM",73:"VDDO_3",74:"VDDO_4",75:"VDD_LDO",76:"VDD_HP_2",
  77:"VDD_DCDCC",78:"FB_DCDC",79:"EN_DCDC",85:"VDD_IO_5",91:"VDD_HP_3",
  96:"VDD_IO_6",99:"XTAL_N",100:"XTAL_P",101:"VDD_ANA",102:"VDD_BAT",
  103:"CHIP_PU",105:"GND"}.items():
    PINS[p] = nm

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for a in sys.argv[1:]:
            print(f"U7.{a} = {PINS.get(int(a),'?')}")
    else:
        gp = sum(1 for v in PINS.values() if v.startswith("GPIO"))
        print(f"{len(PINS)} pins mapped, {gp} GPIOs (expect 105 / 55)")
