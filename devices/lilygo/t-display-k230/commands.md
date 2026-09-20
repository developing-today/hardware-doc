# T-Display K230 — command ledger

Status vocabulary: `executed-success` · `executed-failed` · `reported-working` · `inferred` ·
`not-tested`.

**No command touching the target hardware was executed.** Everything under §2–§5 is
`reported-working` (LilyGO or Canaan documents it and the supporting source exists) or `inferred`.
§1 was executed on the research host and is labelled accordingly.

Host for §1: Linux, `bash`, `curl 8.x`, `git 2.x`, `gh` (authenticated), `python3`.

---

## 1. Research commands — `executed-success`

```sh
# Establish the marketed name and SKUs. Returns 3 products; one is the SKU collision.
curl -sS "https://lilygo.cc/search?q=K230&type=product" -H "User-Agent: <browser UA>"

# Full structured product record: variants, SKUs, cent prices, created_at/published_at, images
curl -sS https://lilygo.cc/products/t-display-k230.js      | python3 -m json.tool
curl -sS https://lilygo.cc/products/t-display-k230-kit.js  | python3 -m json.tool

# Enumerate the whole LilyGO org (254 repos) and filter
gh api "orgs/Xinyuan-LilyGO/repos?per_page=100&sort=pushed" --paginate

# Repository identity: default branch matters — Canaan uses 'dev' and 'canmv_k230'
gh api repos/kendryte/k230_linux_sdk -q '.default_branch'

# 837-entry recursive listing of the Canaan doc repo. gh, not curl: this can exhaust the
# 60/hour anonymous limit and the resulting 403 looks exactly like a bot block.
gh api repos/kendryte/k230_docs/git/trees/main?recursive=1

# Pin the doc commit for citations
gh api repos/kendryte/k230_docs/commits/main -q '.sha+" "+.commit.committer.date'
#   -> f8e30213963e0ed5cf995c3cd4701218a45e4793 2025-09-12T07:01:37Z

# Fetch a Canaan document
curl -sSL https://raw.githubusercontent.com/kendryte/k230_docs/main/en/00_hardware/K230_datasheet.md

# Reddit. www.reddit.com returns 403; old.reddit.com + this UA returns 200.
curl -sS -H "User-Agent: WhatsApp/2.23.20.0" \
  "https://old.reddit.com/search.json?q=lilygo%20k230&sort=new&limit=25&t=all"
curl -sS -H "User-Agent: WhatsApp/2.23.20.0" \
  "https://old.reddit.com/r/LilyGO/comments/1vtcjuj.json?limit=100"

# Clone the BSP (shallow) and pin the commit
git clone --depth 1 https://github.com/Xinyuan-LilyGO/T-Display-K230.git
git -C T-Display-K230 rev-parse HEAD    # bb831ab358b66f5bd9a87ecd7c580fee4537492e

# The single most productive analysis command of the session: part-number census
grep -rhoiE "\b(rtl[0-9]{4}[a-z]{0,3}|lt[0-9]{4}|max[0-9]{4,5}[a-z]?|tps[0-9]{4,5}|bq[0-9]{5}|gc[0-9]{4}|rm69[a-z0-9]+|gt9[0-9]{3}|xl[0-9]{4}|tca[0-9]{4}|aht[0-9]{2}|sx12[0-9]{2}|lr[0-9]{4}|nrf[0-9]{4,5}|k230[a-z]?|es8[0-9]{3}|axp[0-9]{4})\b" \
  --include=*.c --include=*.cpp --include=*.h --include=*.md --include=*.MD \
  --include=*.sh --include=*.patch --include=*.dts --include=*_defconfig . \
  | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn

# Negative result that settles the Ethernet question
grep -ni "ethernet\|gmac\|rmii" K230_datasheet.md K230_brief_datasheet.md   # -> no output

# Validate file type from content, never from the URL suffix
file media/*.jpg && sha256sum media/*.jpg
```

## 2. Building the K230 image — `reported-working` (LilyGO)

```sh
sudo apt update && sudo apt install -y git ca-certificates build-essential make rsync python3
git clone --recurse-submodules https://github.com/Xinyuan-LilyGO/T-Display-K230.git t-display-k230
cd t-display-k230
git submodule update --init --recursive     # if you forgot --recurse-submodules
./scripts/setup_ubuntu.sh                   # installs XuanTie toolchain to /opt/toolchain
./scripts/apply_to_sdk.sh
./scripts/build_sdcard_image.sh
# -> k230_bsp/images/sysimage-sdcard.img

# clean rebuild
rm -rf k230_linux_sdk/output && ./scripts/apply_to_sdk.sh && ./scripts/build_sdcard_image.sh
```

Prereqs: Ubuntu 22.04/24.04 (LilyGO) or 20.04/Docker (Canaan); WSL2 on Windows, **not** under
`/mnt/c/`. Requires network — Buildroot downloads into `dl/` during the build.

Canaan's Docker alternative — `reported-working` (LilyGO wiki):

```sh
docker pull ghcr.io/kendryte/k230_sdk
git clone https://github.com/kendryte/k230_sdk && cd k230_sdk && make prepare_sourcecode
docker run -u root -it -v $(pwd):$(pwd) -v $(pwd)/toolchain:/opt/toolchain -w $(pwd) \
  ghcr.io/kendryte/k230_sdk /bin/bash
make CONF=k230_evb_defconfig
```

⚠ `k230_evb_defconfig` is the **Canaan EVB** target, not this board. It will not drive the
AMOLED, touch or keyboard.

## 3. Flashing — `reported-working`

```sh
# Linux
sudo dd if=k230_bsp/images/sysimage-sdcard.img of=/dev/sdX bs=8M status=progress conv=fsync && sync
# macOS
diskutil unmountDisk /dev/diskN
sudo dd if=k230_bsp/images/sysimage-sdcard.img of=/dev/rdiskN bs=8m status=progress && sync
# Windows: Rufus, "Write in DD Image mode". Cancel the "format unknown partition" prompt.
```

Canaan's variant, same effect: `sudo dd if=sysimage-sdcard.img of=/dev/sdx bs=1M oflag=sync`.

## 4. Companion firmware — `reported-working`

```sh
# nRF52840
python3 -m pip install --user platformio
cd t-display-k230-nrf52840 && pio run
python3 ./scripts/uf2conv.py .pio/build/nrf52840/firmware.hex -c -f 0xADA52840 \
  -o .pio/build/nrf52840/k230_nrf52840_at.uf2
# DFU: jumper RST to GND twice quickly (or touch the USB-C shell), then drag the .uf2

# nRF9151
nrfutil install sdk-manager
nrfutil sdk-manager install --install-dir "$PWD/ncs" v3.4.0
export NCS_ROOT=/path/to/ncs/v3.4.0        # only if installed elsewhere
git clone --recurse-submodules https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF9151
cd T-Display-K230-nRF9151 && ./build_serial_modem.sh
find build/serial_modem_k230 -path '*/zephyr/tfm_merged.hex' -o -path '*/zephyr/zephyr.hex'
```

## 5. On-board diagnostics — `inferred` (tools are built into the image; not run here)

```sh
cat /proc/cpuinfo                       # settles GC-1: which core runs Linux
free -h                                 # settles GC-7: 512 MB vs 1 GB
readlink /sys/class/net/eth0/device/driver ; lsusb    # settles GC-3: the Ethernet controller
zcat /proc/config.gz | grep -i rtl8152  # ditto
dmesg | grep -iE 'rtl|blue|goodix|gc2093|k230'
cat /proc/mtd                           # settles GC-9: the 16 MB flash
i2cdetect -y 4                          # I2C4: expect 0x34 0x38 0x55 0x6B and one of 0x20-0x27
i2cdetect -y <touch-bus>                # settles GC-4: a second address means LT9611 is fitted
evtest                                  # keyboard and PMU power key
gpioinfo                                # line ownership
aplay -l ; amixer                       # settles the audio route question
coremark                                # built in; nobody has ever published the result

# Fast iteration once networked
./scripts/deploy_launcher.sh 192.168.1.100
./scripts/deploy_launcher.sh 192.168.1.100 --full --reboot
```

## 6. Recovery — `not-tested`

No vendor procedure exists ([`factory-firmware.md` §5](factory-firmware.md)). The two documented
leads, neither exercised:

```sh
# Canaan's own tool — see K230_SDK_Burntool_User_Guide.md in kendryte/k230_docs
# k230_burntool ...

# oreboot's kendryte_boot — author reports Linux from mask ROM over USB in ~3 s
# https://github.com/oreboot/oreboot
```

**Do not present either as authoritative.** They are the paths to try, not paths that have been
shown to work on this board.

## 7. Commands that failed — kept deliberately

| Command | Failure | Diagnosis | Correct form |
|---|---|---|---|
| `curl .../products/t-display-series/t-display-k230-cased-version/` | **404** | Guessed the wiki URL shape; the Cased Version is a *child page*, not a sibling product | `.../t-display-series/t-display-k230/cased-version.html` |
| Searching only `en/` in `k230_docs` for schematics | zero results | Wrong conclusion ("Canaan publishes no schematics"). The artifacts are in the **`zh/`** tree | list `zh/00_hardware/` as well |
| First `k230_docs` listing missed `K230_brief_datasheet.md` | not in `00_hardware/` | The brief datasheet sits at the **tree root** (`en/`), not under `00_hardware/` | list the whole tree, filter afterwards |
