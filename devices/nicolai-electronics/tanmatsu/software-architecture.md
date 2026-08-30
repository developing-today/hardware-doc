# Software architecture and app development — Tanmatsu

> How the launcher is built, how apps and plugins actually work, and what the firmware reveals about the hardware.
> Snapshot **2026-08-24**, launcher @ `20022fce` (2026-08-23). Read from source; **nothing was built or run**.

The vendor documentation describes AppFS as a place to store app binaries. The source shows something considerably more elaborate: a **tiered storage system with LRU eviction**, an **ELF plugin runtime**, and **per-unit identity in eFuses**. This page documents what the code actually does.

---

## 1. The launcher's dependency graph

From [`main/idf_component.yml`](https://github.com/Nicolai-Electronics/tanmatsu-launcher/blob/main/main/idf_component.yml) — every version is pinned with `=`, not a caret, except cJSON:

| Component | Version | Role |
|---|---|---|
| **`idf`** | **`>=6.0.2`** | ⚠ **ESP-IDF 6.x**, not the 5.3 the docs imply |
| `badgeteam/badge-bsp` | `=1.4.0` | Board support |
| `badgeteam/appfs` | **`=2.1.0`** | ⚠ Docs say `^1.0.0` |
| `badgeteam/badgelink` | `=0.2.0` | USB management protocol |
| `robotman2412/pax-gfx` | `=2.2.2` | 2D graphics |
| `robotman2412/pax-codecs` | `=1.0.1` | Image decode |
| `nicolaielectronics/tanmatsu-wifi` | `=1.3.1` | esp-hosted wrapper for the C6 |
| `nicolaielectronics/tanmatsu-lora` | `=0.6.0` | LoRa |
| `nicolaielectronics/tanmatsu-addon` | `=0.1.0` | Add-on detection |
| `nicolaielectronics/tanmatsu-settings` | `=1.2.0` | Settings |
| `nicolaielectronics/wifi-manager` | `=0.3.0` | Provisioning |
| `nicolaielectronics/scd4x` | `=0.0.1` | Optional CO₂ sensor |
| `nicolaielectronics/rvswd` | `=0.3.0` | P4→CH32V203 flashing *(P4 only)* |
| `badgeteam/esptool` | `=0.1.0` | **On-device esptool** *(P4 only)* |
| `badgeteam/badge-elf` + `badge-elf-api` | `=0.8.0` / `=0.7.0` | **ELF plugin loader** *(P4 only, opt-in)* |
| `espressif/esp_tinyusb` | `=2.2.1` | USB device stack |

Two entries deserve attention. **`badgeteam/esptool`** means the device can flash other ESP32s itself — consistent with `rvswd` reflashing the coprocessor. And **`badge-elf`** is a dynamic ELF loader, which is the foundation of the plugin system in [§4](#4-the-plugin-system).

> ⚠ **The documented ESP-IDF version is wrong.** [`development.md`](development.md) and the vendor guide describe an ESP-IDF 5.x workflow; the launcher now requires **≥ 6.0.2** (commit `db589fd`, *"Build with ESP-IDF v6.0.2"*). If you follow the published setup you will not build the current launcher.

---

## 2. The real partition table

The vendor's flash-layout page describes `0x9000`–`0x18FFF` as *"Unused"* and OTA data as 12 KB. The actual table shipped in the launcher ([`partition_tables/esp32p4-16mb.csv`](https://github.com/Nicolai-Electronics/tanmatsu-launcher/blob/main/partition_tables/esp32p4-16mb.csv)) says otherwise:

| Name | Type | SubType | Offset | Size |
|---|---|---|---|---|
| **`coredump`** | data | coredump | **`0x9000`** | **64 K** |
| `nvs` | data | nvs | `0x19000` | 16 K |
| `otadata` | data | ota | `0x1D000` | **8 K** |
| **`phy_init`** | data | phy | **`0x1F000`** | **4 K** |
| `ota_0` | app | ota_0 | `0x20000` | 2048 K |
| `ota_1` | app | ota_1 | `0x220000` | 2048 K |
| **`appfs`** | **`0x43`** | **`3`** | `0x420000` | 8192 K |
| `locfd` | data | fat | `0xC20000` | 3968 K |

**Corrections to the published layout:**

- The 64 KB at `0x9000` is **not unused** — it is the **coredump** partition. After a crash, `espcoredump.py` can extract a backtrace from it.
- OTA data is **8 KB**, not 12 KB; the remaining 4 KB at `0x1F000` is **`phy_init`** (RF calibration data).
- AppFS uses a **custom partition type `0x43`, subtype `3`** — which is why a stock `esptool`/`parttool` will show it as an unrecognised type.

Other targets have their own tables (`esp32s3-16mb`, `esp32s3-8mb`, `esp32s3-8mb-noappfs`, `mch2022`, `hackerhotel2024`, `esp32s31-16mb`), each with an `.ods` spreadsheet alongside.

---

## 3. Apps: a tiered cache, not a filesystem

This is the biggest architectural surprise. **AppFS is a cache tier**, and apps have four possible homes:

```c
typedef enum {
    APP_MGMT_LOCATION_INTERNAL = 0,      // /int/apps
    APP_MGMT_LOCATION_SD,                // /sd/apps
    APP_MGMT_LOCATION_INTERNAL_PLUGINS,  // /int/plugins
    APP_MGMT_LOCATION_SD_PLUGINS,        // /sd/plugins
} app_mgmt_location_t;
```

So an app lives on the **FAT filesystem** (internal or SD) and is *promoted into AppFS* to run. The management API in [`app_management.h`](https://github.com/Nicolai-Electronics/tanmatsu-launcher/blob/main/main/app_management.h) makes the model explicit:

| Function | What it does |
|---|---|
| `app_mgmt_install(repository_url, slug, location, cb)` | Download and install from a repository |
| `app_mgmt_install_from_file` / `_from_buffer` | Install from local data |
| `app_mgmt_ensure_in_appfs(slug, …)` | **Promote into the AppFS cache** |
| `app_mgmt_cache_to_appfs(…)` | Copy in explicitly |
| `app_mgmt_remove_from_appfs(slug)` | Evict one app |
| **`app_mgmt_appfs_evict_lru(needed_bytes)`** | **LRU eviction to make room** |
| `app_mgmt_can_uncache(slug)` | Is a FAT copy available to fall back to? |
| `app_mgmt_is_int_only(slug)` | App exists *only* in internal storage |
| `app_mgmt_move(slug, from, to)` / `app_mgmt_can_move` | Migrate between tiers |
| `app_mgmt_copy_appfs_to_install_dir(slug)` | Reverse: AppFS → FAT |

There is a companion `app_usage.c` tracking access for the LRU ordering, and `appfs_settings.c` exposes two NVS knobs in namespace **`"appfs"`**: `auto_cleanup` and `mismatch_reinstall`.

**Practical consequences:**

- The **8 MB AppFS is not your app storage limit** — it is your *working set* limit. Total capacity is AppFS + 3.9 MB internal FAT + whatever SD card you fit.
- **Apps can be evicted automatically.** If AppFS fills, the least-recently-used app is removed — but only if `can_uncache()` says a FAT copy survives.
- **An SD card meaningfully expands the device**, and apps installed to `/sd/apps` survive a firmware reflash (which does not touch AppFS or FAT).

## 3.1 App metadata: more than the docs describe

Strings parsed by [`app_metadata_parser.c`](https://github.com/Nicolai-Electronics/tanmatsu-launcher/blob/main/main/app_metadata_parser.c):

```
appfs · application · author · categories · description · elf · executable ·
icon · interpreter · license_file · license_type · name · repository ·
revision · script · targets · type · version
```

The `type` field is documented as *"currently only `appfs` is supported"*. The parser also recognises **`elf`**, **`interpreter`** and **`script`** — so the launcher is being extended toward **dynamically-loaded ELF apps and interpreted/scripted apps**, not just flashed binaries. It also reads a **`repository`** field, i.e. apps can name their own source.

> Status: these keys exist in the parser. Whether the corresponding runtimes are complete was **not verified** — no app in the official repository uses anything but `appfs`.

---

## 4. The plugin system

**Entirely absent from the vendor documentation site**, but the launcher ships an 840-line API reference at [`docs/PLUGINAPIS.md`](https://github.com/Nicolai-Electronics/tanmatsu-launcher/blob/main/docs/PLUGINAPIS.md) — **API version 2.0.0**, dated 2026-02-14.

Plugins are **dynamically loaded ELF shared libraries** run on the ESP32-P4 via the **BadgeELF** loader. Opt-in at build time:

```
CONFIG_ENABLE_LAUNCHERPLUGINS   # default n, ESP32-P4 only
```

### Three plugin types

| Type | Behaviour |
|---|---|
| `PLUGIN_TYPE_MENU` (0) | Adds items to the launcher menu |
| `PLUGIN_TYPE_SERVICE` (1) | Background service in its **own FreeRTOS task** |
| `PLUGIN_TYPE_HOOK` (2) | Receives system events |

### Registration

```c
static const plugin_entry_t entry = {
    .get_info = get_info,
    .init     = plugin_init,
    .cleanup  = plugin_cleanup,
};
TANMATSU_PLUGIN_REGISTER(entry);
```

The macro writes a `plugin_registration_t` into a dedicated **`.plugin_info` ELF section**, carrying magic **`0x544D5350`** (`"TMSP"`), the struct size, and the entry points. The host **rejects plugins built against an incompatible API version**.

Callbacks: `get_info`, `init`, `cleanup` (all required), plus `menu_render` / `menu_select`, `service_run`, or `hook_event` depending on type.

### API surface

All exported functions use an `asp_*` prefix for BadgeELF compatibility, grouped as:

**Logging** `asp_log_info/warn/error` · **Display** `asp_disp_get_pax_buf`, `asp_disp_write`, `asp_disp_write_part` · **Status bar** widget register/unregister · **Input** poll, key state, hook register/unregister, **inject** · **RGB LED** · **Storage** open/read/write/seek/tell/close/exists/mkdir/remove · **Timers** `delay_ms`, `get_tick_ms`, `should_stop` · **Menu** add/remove item · **Events** register/unregister · **Network** `asp_net_is_connected`, `asp_http_get`, `asp_http_post` · **Settings** get/set string and int · **Dialogs** info and text.

Note `asp_plugin_input_inject` — plugins can **synthesise input events**, which is powerful and worth being aware of security-wise.

### System events available to hooks

`APP_LAUNCH` · `APP_EXIT` · `WIFI_CONNECTED` · `WIFI_DISCONNECTED` · `USB_CONNECTED` · `USB_DISCONNECTED` · `SD_INSERTED` · `SD_REMOVED` · `POWER_LOW`

### Related build option

`CONFIG_ENABLE_AUDIOMIXER` (default `n`) compiles a **per-stream software audio mixer** that owns the I2S channel so multiple sources can play concurrently. Without it, *"plugin audio falls back to writing directly to I2S (only one source can play cleanly at a time)."* If you plan concurrent audio, enable it.

Also `CONFIG_FATFS_USE_FASTOPEN` — allocates stdio buffers in **internal DMA-capable RAM** rather than PSRAM, avoiding cache overhead on SD/flash I/O. Default `n`, up to 8 files, 8192-byte buffers.

---

## 5. Per-unit identity lives in eFuses

[`main/esp_efuse_custom_table.csv`](https://github.com/Nicolai-Electronics/tanmatsu-launcher/blob/main/main/esp_efuse_custom_table.csv) defines a manufacturing block in **`EFUSE_BLK3`**:

| Field | Bits | Offset |
|---|---:|---:|
| `HARDWARE_NAME` | 128 | 0 |
| `HARDWARE_VENDOR` | 80 | 128 |
| `HARDWARE_RESERVED0` | 8 | 208 |
| **`HARDWARE_REVISION`** | 8 | 216 |
| **`HARDWARE_VARIANT_RADIO`** | 8 | 224 |
| **`HARDWARE_VARIANT_COLOR`** | 8 | 232 |
| **`HARDWARE_REGION`** | 16 | 240 |

This answers a question left open in [`gaps-and-conflicts.md`](gaps-and-conflicts.md): **board revision is burned into eFuse**, which is how `Settings > Device information` reports it. Radio variant (868/915 vs 433) and region are recorded per unit too.

⚠ **eFuses are one-time-programmable.** These are factory-set; do not write them.

The firmware uses the region field for regulatory correctness — see next section.

---

## 6. How the three processors coordinate at runtime

Traced through [`main/main.c`](https://github.com/Nicolai-Electronics/tanmatsu-launcher/blob/main/main/main.c):

### Radio (ESP32-C6) startup

1. The P4 waits for `wifi_stack_get_initialized()`, which additionally requires the coprocessor to report `BSP_POWER_RADIO_STATE_APPLICATION` — i.e. **the CH32V203 controls whether the radio is powered and out of bootloader**, and the P4 polls that state.
2. The P4 queries the radio's firmware version and **pins it to `"v3.4.0"`**:
   ```c
   wifi_firmware_version_mismatch = (strcmp(radio_information.firmware_version, "v3.4.0") != 0);
   ```
   A mismatch is surfaced to the user — the P4 launcher and C6 radio firmware are **version-coupled**.
3. If the radio's stored **board revision or country code** differs from the eFuse identity, the P4 **pushes a new configuration to the radio**. So regulatory region propagates from P4 eFuses → C6 radio at every boot.

### LoRa

Handled in a **separate FreeRTOS task** (commit `7dc0820`, *"Move LoRa to separate task"*). The firmware **detects which Semtech part is inside the Ebyte module**:

```c
if (status.chip_type == LORA_PROTOCOL_CHIP_SX1268) …  else /* SX1262 */
```

So E22 modules ship with either an **SX1262** or **SX1268** die, and the stack adapts. This is a useful hardware detail published nowhere: the LoRa module is not a single fixed part.

Consistent with the netlist finding that **LoRa is wired to the ESP32-C6, not the P4** ([`gaps-and-conflicts.md` §19](gaps-and-conflicts.md)) — the P4 reaches it through the radio protocol client, not over SPI.

### Coprocessor

`coprocessor_management.c` plus `rvswd` give the P4 the ability to **query and reflash the CH32V203**. `main.c` also handles the case where the coprocessor does not answer: *"This probably means something is wrong with the I2C bus, we check if the coprocessor is present."*

---

## 7. Recent development direction

From the launcher's git history (most recent first):

| Commit | Change |
|---|---|
| `20022fc` | **"Allow for BadgeLink over the USB debug peripheral"** |
| `dc4b4d4` | Audio tests in the testing menu |
| `7043218`, `649ad51` | **ESP32-S31-KORVO-1 devkit support** |
| `85857f3` | FreeRTOS stats enabled on Tanmatsu |
| `7dc0820` | LoRa moved to its own task |
| `db589fd` | **Build with ESP-IDF v6.0.2** |
| `1c89273` | User-agent in OTA updates |
| `24d131c`, `7b8d4de`, `ac594e4` | **Autostart feature**, cancellable with HOME/ESC/space |
| `e55e797` | **Favourite apps menu** |
| **`162b96f`** | **"Remove ifdefs for Konsool target"** |
| `65833ee` | "Remove Konsool FAT files" |

Two things worth drawing out:

**BadgeLink now works over the USB *debug* peripheral.** The head commit removes the hard either/or between debugging and management described in [`badgelink-and-appfs.md` §8](badgelink-and-appfs.md) and in the vendor docs. If you are on current firmware you may no longer need the purple-diamond mode switch.

**Konsool-specific code has been deleted**, not added. `162b96f` and `65833ee` collapse Konsool into the Tanmatsu target — independently confirming the analysis in [`konsool-and-family.md`](konsool-and-family.md) that they are one device. The build-target divergence is being actively removed.

---

## 8. How to add a new app

### Route A — publish to the official repository

1. Build a firmware binary for `esp32p4`.
2. Fork [`Nicolai-Electronics/app-repository`](https://github.com/Nicolai-Electronics/app-repository), add a folder named with a **reverse-DNS slug** (`com.example.myapp`).
3. Add `metadata.json` — see [`software-and-apps.md`](software-and-apps.md) for the schema. Declare **both** `tanmatsu` and `konsool` in `targets`.
4. Open a pull request. No review fee, no signing.

### Route B — install directly over USB

Use BadgeLink: `AppfsActionReq` with an upload, or `app_mgmt_install_from_file`. See [`badgelink-and-appfs.md`](badgelink-and-appfs.md).

### Route C — drop it on the SD card

Place the binary under **`/sd/apps/<slug>/`**. The launcher scans SD storage, and the app is promoted into AppFS on demand. This survives firmware reflashes and needs no network.

### Starting point

| Template | Graphics | Licence |
|---|---|---|
| [`tanmatsu-template`](https://github.com/Nicolai-Electronics/tanmatsu-template) | PAX | ⚠ **none stated** |
| [`konsool-template-lvgl`](https://github.com/badgeteam/konsool-template-lvgl) | LVGL | **CC0-1.0** |

Apps need **no AppFS-specific code** — they are ordinary ESP-IDF applications. Only a *launcher* needs the AppFS component and its bootloader symlinks.

> **Build details for both routes — toolchain, flags, linker script, packaging — are in
> [`apps-vs-plugins.md`](apps-vs-plugins.md).**

### Or write a plugin instead

If you want to extend the launcher rather than replace it — add a menu entry, run a background service, react to Wi-Fi/USB/SD events — write a **plugin** ([§4](#4-the-plugin-system)) rather than an app. Plugins keep the launcher running and can be installed to `/int/plugins` or `/sd/plugins`.

---

## 9. Gaps

| Question | Status |
|---|---|
| Are `elf` / `interpreter` / `script` app types functional? | **Unverified** — keys exist in the parser, no app uses them |
| AppFS on-flash format (headers, page tables) | **Not examined** — component lives in the Espressif registry |
| Is the plugin API stable? | v2.0.0 dated 2026-02-14; **default-off**, `depends on IDF_TARGET_ESP32P4` |
| Are there published example plugins? | **Found two** community plugins (`nullislandspace/tanmatsu-plugin-startup`, `-turret`) — see [`apps-vs-plugins.md`](apps-vs-plugins.md). Still none official |
| Does BadgeLink-over-debug work end to end? | Head commit only; **untested** |
| Why is `badgeteam/esptool` a dependency? | Presumably C6/coprocessor flashing; **not traced** |
| Radio firmware `v3.4.0` — where is it published? | `tanmatsu-radio` releases **not checked** |

## Related

- [`badgelink-and-appfs.md`](badgelink-and-appfs.md) — wire protocol and AppFS metadata
- [`software-and-apps.md`](software-and-apps.md) — the app repository and its 57 apps
- [`development.md`](development.md) — toolchain setup *(⚠ documents ESP-IDF 5.x; the launcher now needs 6.0.2)*
- [`konsool-and-family.md`](konsool-and-family.md) — the Konsool consolidation visible in the git log
- [`pinouts-and-buses.md`](pinouts-and-buses.md) — the hardware these processors coordinate over
