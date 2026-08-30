# Tanmatsu — command ledger

> Every consequential command from this research pass, with honest execution status.
> **2026-08-24.** Environment: Linux, bash, Python 3.14, git 2.x, `uvx`. **No Tanmatsu hardware was present.**

Status values: `executed-success` · `executed-failed` · `reported-working` (vendor-documented, not run here) · `inferred` · `not-tested`

---

## 1. Acquisition — `executed-success`

```bash
# All ten official repositories. Shallow clones; commits recorded in sources.md
for r in tanmatsu-hardware tanmatsu-documentation tanmatsu-mechanical \
         tanmatsu-coprocessor-firmware esp32-component-tanmatsu-coprocessor \
         tanmatsu-launcher tanmatsu-radio esp32-component-tanmatsu-wifi \
         tanmatsu-template app-repository; do
  git clone --depth 1 "https://github.com/Nicolai-Electronics/$r.git" "$r"
done

git clone --depth 1 https://github.com/badgeteam/esp32-component-badge-bsp.git badge-bsp
git clone --depth 1 https://github.com/solderparty/i2c_puppet.git
```

All succeeded. Total ≈ 490 MB. Record exact commits:

```bash
for r in */; do printf '%s\t%s\t%s\n' "${r%/}" \
  "$(git -C "$r" rev-parse HEAD)" "$(git -C "$r" log -1 --format=%cI)"; done
```

## 2. Enumerating badge.team documentation — `executed-success`

The sidebar is **not** in the served HTML, so link-scraping fails. The sitemap is authoritative:

```bash
curl -sSL -A "$UA" https://badge.team/sitemap.xml -o sm.xml
grep -o '<loc>[^<]*</loc>' sm.xml | sed 's/<[^>]*>//g' | grep -i konsool | sort
# → 42 URLs
```

```bash
# UA used throughout; badge.team and solder.party are server-rendered Hugo and
# did not require it, but it was applied consistently.
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
```

### Failed attempts — `executed-failed`

```bash
curl -sSL "https://badge.team/docs/badges/konsool/quick-start/"       # 404 → /quickstart/
curl -sSL "https://badge.team/docs/badges/konsool/expansion-boards/"  # 404 → /expansion_boards/
curl -sSL "https://raw.githubusercontent.com/badgeteam/konsool-zero/main/README.md"  # 404, branch is not 'main'
```

**Lesson:** enumerate from the sitemap; do not guess badge.team paths — separator style is inconsistent.

## 3. Parsing the design data — `executed-success`

```bash
# BOM: 84 lines with LCSC part numbers
python3 -c "
import csv
rows=list(csv.DictReader(open('production/bom.csv')))
print(len(rows),'lines')"

# App ecosystem statistics from 57 metadata.json files
python3 tools/… # see software-and-apps.md
```

```bash
# Firmware facts — read directly, no build required
sed -n '1,90p' tanmatsu-coprocessor-firmware/src/application/keyboard.c
cat tanmatsu-coprocessor-firmware/src/application/i2c_registers.h
cat badge-bsp/targets/tanmatsu/tanmatsu_hardware.h
```

```bash
# Prove WHY2025 is different hardware
diff <(grep -oE '#define [A-Z0-9_]+ +[^ ]+' badge-bsp/targets/tanmatsu/tanmatsu_hardware.h | sort) \
     <(grep -oE '#define [A-Z0-9_]+ +[^ ]+' badge-bsp/targets/why2025/why2025_hardware.h | sort)
```

## 4. Manifest and verification — `executed-success`

```bash
python3 tools/build_manifest.py    # 188 files, 30.7 MiB, SHA-256 each
python3 tools/verify_manifest.py   # 188 files: 188 ok, 0 mismatched, 0 missing
```

`verify_manifest.py` exits non-zero on any mismatch, so it is usable in CI.

## 5. HTML → text extraction — `executed-success`

```bash
python3 /tmp/htmltext.py page.html > page.txt
```

Retained as text rather than HTML so the snapshots are diffable. **The original HTML was not kept** —
a deliberate trade recorded in `acquisition/manifest.json`.

---

## 6. Flashing the launcher — `reported-working`, NOT executed

Quoted verbatim from the vendor's flash-layout documentation. **No hardware; never run here.**

```bash
# Full flash — ERASES the FAT partition
python -m esptool --chip esp32p4 -b 460800 \
  --before default_reset --after hard_reset write_flash \
  --flash_mode dio --flash_size 16MB --flash_freq 80m \
  0x2000 bootloader.bin 0x8000 partition-table.bin \
  0x1d000 ota_data_initial.bin 0x20000 tanmatsu-launcher.bin \
  0xc20000 locfd.bin

# Firmware only — preserves FAT
python -m esptool --chip esp32p4 -b 460800 \
  --before default_reset --after hard_reset write_flash \
  --flash_mode dio --flash_size 16MB --flash_freq 80m \
  0x2000 bootloader.bin 0x8000 partition-table.bin \
  0x1d000 ota_data_initial.bin 0x20000 tanmatsu-launcher.bin
```

**Bootloader entry** (`reported-working`): power off with the power button, then hold the third
right-side button (`-`/down) while plugging in USB-C. Screen stays black — expected.

## 7. ESP-IDF project setup — `reported-working`, NOT executed

Three non-default settings, all mandatory. See [`display.md` §4](display.md).

```bash
idf.py menuconfig
#  Component config → Badge.Team BSP → Board → "Nicolai Electronics Tanmatsu"
#  Bootloader config → Reserve RTC FAST memory for custom purposes → 0x100
#  (main) Make experimental features visible
#  Component config → ESP PSRAM → Support for external PSRAM
#                   → PSRAM config → Set PSRAM clock speed → 200MHz

idf.py build flash monitor --port /dev/ttyACM0
```

Failure signature if PSRAM is left at the 20 MHz default:

```
E (230) lcd.dsi.dpi: esp_lcd_new_panel_dpi(226): no memory for frame buffer
E (230) st7701_mipi: esp_lcd_new_panel_st7701_mipi(103): create MIPI DPI panel failed
```

## 8. BadgeLink — `reported-working`, NOT executed

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
sudo cp 60-badgelink.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
./badgelink.sh appfs list
./badgelink.sh appfs download konsool64 konsool64.bin
```

Switch the device to USB device mode first with the **purple diamond key**.

## 9. AppFS bootloader integration — `reported-working`, NOT executed

```bash
idf.py add-dependency "badgeteam/appfs^1.0.0"
mkdir bootloader_components
ln -s managed_components/badgeteam__appfs bootloader_components/appfs
ln -s managed_components/badgeteam__appfs/bootloader_main bootloader_components/main
```

The symlink step is **easy to miss** — without it the build succeeds but cannot launch apps.

## 10. `i2c_puppet` build — `reported-working`, NOT executed

```bash
git clone https://github.com/solderparty/i2c_puppet && cd i2c_puppet
git submodule update --init
cd 3rdparty/pico-sdk && git submodule update --init && cd ../..
mkdir build && cd build
cmake -DPICO_BOARD=bbq20kbd_breakout -DCMAKE_BUILD_TYPE=Debug .. && make
```

⚠ **Do not use `--recursive`** — the Pico SDK vendors TinyUSB and its submodule tree is large.

## 11. Mechanical export — `reported-working`, NOT executed

```bash
./tools/export_manufacturing_files.sh     # run with FreeCAD CLOSED
```

Requires the **Fasteners** workbench. Emits STEP + AMF into `release/`. Produces known harmless
errors from Fasteners ([FreeCAD_FastenersWB#454](https://github.com/shaise/FreeCAD_FastenersWB/issues/454)).
FreeCAD was **not available** in this environment.

---

## Not attempted

| Task | Why |
|---|---|
| Building any firmware | No ESP-IDF toolchain installed; no hardware to validate against |
| Flashing anything | No hardware |
| Parsing `production/netlist.ipc` | Time; pin data obtained from BSP instead. **Would allow independent verification** |
| Opening the FreeCAD files | FreeCAD unavailable |
| Reading `production/tanmatsu.zip` | Not opened — presumed Gerbers |
