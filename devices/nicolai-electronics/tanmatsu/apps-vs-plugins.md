# Apps vs plugins — how each is built

> Two different build systems, two different runtime models. Which you want depends on whether you are
> *replacing* the launcher or *extending* it.
> Snapshot **2026-08-24**. Read from the plugin SDK, the app template, and two working community plugins.
> **Nothing was compiled** — no ESP-IDF toolchain in this environment.

---

## The short version

| | **App** | **Plugin (AppFS extension)** |
|---|---|---|
| What it is | A **complete ESP-IDF firmware** | A **dynamically-loaded ELF shared object** |
| Build system | Standard `idf.py build` | **Custom CMake + toolchain file**, not `idf.py` |
| Output | `.bin` firmware image | **`.plugin`** (ELF, `-shared`) |
| Runs | **Instead of** the launcher — the launcher exits | **Inside** the launcher process |
| Loader | AppFS bootloader modification | **kbelf** ELF loader, into PSRAM |
| Entry | `app_main()` | `TANMATSU_PLUGIN_REGISTER(entry)` |
| Manifest | `metadata.json` | `metadata.json` **+ `plugin.json`** |
| Installed to | `/int/apps` or `/sd/apps` | `/int/plugins` or `/sd/plugins` |
| Concurrency | One at a time | **Up to 32 loaded** (`PLUGIN_MAX_LOADED`) |
| Access to hardware | Full ESP-IDF | Only the **~40 `asp_*` APIs** |
| Availability | Stable, all targets | **`default n`**, ESP32-P4 only |

---

## 1. Building an app

An app is an **entirely ordinary ESP-IDF project**. There is nothing AppFS-specific in it. From [`tanmatsu-template`](https://github.com/Nicolai-Electronics/tanmatsu-template):

```cmake
cmake_minimum_required(VERSION 3.10)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(application)
```

`main/CMakeLists.txt`:

```cmake
idf_build_get_property(idf_target IDF_TARGET)
if("${idf_target}" STREQUAL "esp32p4")
list(APPEND extra_requires esp-hosted-tanmatsu)
endif()

idf_component_register(
    SRCS "main.c"
    PRIV_REQUIRES esp_lcd fatfs nvs_flash bt badge-bsp tanmatsu-wifi ${extra_requires}
    INCLUDE_DIRS "."
)
```

Dependencies (`main/idf_component.yml`):

```yaml
dependencies:
  idf: ">=6.0.2"
  badgeteam/badge-bsp: "=1.1.0"
  nicolaielectronics/tanmatsu-wifi: "=1.3.1"
  robotman2412/pax-gfx: "=2.2.2"
```

Then simply:

```bash
idf.py set-target esp32p4
idf.py menuconfig      # select Badge.Team BSP board = Tanmatsu
idf.py build
```

> Status: **`inferred`** from the template's structure — not executed here.

**The app owns the machine.** When the launcher starts your app, the launcher is gone; you get the whole ESP32-P4, full ESP-IDF, direct access to the display, I2S, SD card and radios. You are responsible for bringing up the BSP yourself.

Note the template pins `badge-bsp =1.1.0` while the **launcher** uses `=1.4.0` — the template lags. Check for BSP API drift if you hit missing symbols.

---

## 2. Building a plugin

Plugins do **not** use `idf.py`. They use a dedicated SDK at
[`tanmatsu-launcher/tools/plugin-sdk/`](https://github.com/Nicolai-Electronics/tanmatsu-launcher/tree/main/tools/plugin-sdk):

```
plugin-sdk/
├── plugin-build.cmake        # build_tanmatsu_plugin() macro
├── toolchain-plugin.cmake    # bare RISC-V cross-compile setup
├── plugin.ld                 # linker script
├── lib/libplugin_stubs.c     # host API stubs
└── README.md
```

### `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.16)
set(PLUGIN_NAME "my-plugin")
set(TANMATSU_PLUGIN_SDK "/path/to/tanmatsu-launcher/tools/plugin-sdk")
project(${PLUGIN_NAME} C)
include(${TANMATSU_PLUGIN_SDK}/plugin-build.cmake)

set(PLUGIN_SOURCES src/main.c)
build_tanmatsu_plugin(${PLUGIN_NAME} "${PLUGIN_SOURCES}")
```

### Build invocation

Note the **explicit toolchain file** — this is the key difference from an app:

```bash
mkdir -p build && cd build
cmake -DCMAKE_TOOLCHAIN_FILE=<sdk>/toolchain-plugin.cmake ..
make
# -> build/my-plugin.plugin
```

`IDF_PATH` must still be set, but only so the toolchain file can *locate the RISC-V compiler*. ESP-IDF itself is not used as a build system.

> Status: **`reported-working`** — taken from the SDK README and two working community plugins. Not executed here.

### What the toolchain file does

```cmake
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR riscv32)

set(ARCH_FLAGS "-march=rv32imafc_zicsr_zifencei -mabi=ilp32f")
set(CMAKE_C_FLAGS_INIT "${ARCH_FLAGS} -fPIC -ffunction-sections -fdata-sections -fno-common")
set(PLUGIN_C_FLAGS    "-Wall -Wextra -Wno-unused-parameter -Os")
set(PLUGIN_LINK_FLAGS "-shared -nostdlib -Wl,--gc-sections -Wl,--no-undefined")
```

The consequential flags:

| Flag | Why it matters |
|---|---|
| **`-fPIC`** | Position-independent — the plugin is relocated into PSRAM at load time |
| **`-shared`** | Produces a shared object, not an executable |
| **`-nostdlib`** | **No C standard library.** You get the `asp_*` host APIs and nothing else |
| **`--no-undefined`** | Link fails if you reference a symbol the host does not export — a useful early error |
| `-Os` | Optimise for size |
| `rv32imafc` / `ilp32f` | ESP32-P4 with hardware float; must match the host ABI |

**`-nostdlib` is the big constraint.** No `malloc`, no `printf`, no `memcpy` unless the host exports it. That is what `lib/libplugin_stubs.c` and the `asp_*` API surface exist to replace — see [`software-architecture.md` §4](software-architecture.md).

### The linker script

`plugin.ld` targets `elf32-littleriscv` and is explicit about layout:

```ld
ENTRY(_plugin_entry)

SECTIONS
{
    /* Plugin info section - MUST be first for discovery */
    .plugin_info : ALIGN(4) {
        KEEP(*(.plugin_info))
        KEEP(*(.plugin_info.*))
    }
    .dynamic : ALIGN(4) { *(.dynamic) }
    .dynsym  : ALIGN(4) { ... }
    ...
}
```

Its own comment states plugins *"are loaded into PSRAM at runtime by the kbelf loader"*. The `.plugin_info` section must be first because that is where the host reads the `plugin_registration_t` (magic `0x544D5350`, `"TMSP"`) to identify and version-check the plugin before running any of its code.

---

## 3. Packaging differences

### An app ships

```
com.example.myapp/
├── metadata.json        # name, description, categories, version, icon,
│                        # author, license_type, application[]
├── myapp.bin            # the firmware
└── icon16/32/64.png
```

### A plugin ships an extra manifest

```
at.cavac.startup/
├── metadata.json        # same schema as an app
├── plugin.json          # PLUGIN-SPECIFIC
├── startup.plugin       # the ELF
├── icon16/32/64.png
└── tanmatsu_startup.mp3 # assets
```

`plugin.json`, from the working `tanmatsu-plugin-startup`:

```json
{
    "type": "service",
    "api_version": 2,
    "permissions": ["audio", "storage"],
    "autostart": false
}
```

Four fields, none documented on the vendor site:

| Field | Meaning |
|---|---|
| `type` | `menu` \| `service` \| `hook` — matches `PLUGIN_TYPE_*` |
| **`api_version`** | Plugin API major version. The host **rejects mismatches** |
| **`permissions`** | ⚠ **A permission model exists** — here `["audio", "storage"]` |
| `autostart` | Load at boot without user action |

The **`permissions` array is notable**: nothing in `PLUGINAPIS.md` describes it, and it is the only capability-gating mechanism seen anywhere in the Tanmatsu software stack. Whether it is enforced or merely declarative was **not determined** — the plugin manager source was not traced that far.

### Discovery on device

`find_plugin_elf()` scans the plugin directory for **any file ending `.plugin`**, falling back to `plugin.plugin`. So the filename is free-form as long as the extension matches.

---

## 4. Installing a plugin

From the community `Makefile`, which shows the real workflow:

```make
BADGEDIR := /tmp/mnt
DEST := $(BADGEDIR)/sd/plugins

install: build
	badgefs $(BADGEDIR)                       # FUSE-mount the badge
	mkdir -p $(DEST)/$(APP_SLUG_NAME)
	cp build/$(PLUGIN_NAME).plugin $(DEST)/$(APP_SLUG_NAME)/
	cp metadata/plugin.json       $(DEST)/$(APP_SLUG_NAME)/
	cp metadata/metadata.json     $(DEST)/$(APP_SLUG_NAME)/
	badgefs -u $(BADGEDIR)                    # unmount
```

**`badgefs` is a FUSE filesystem that mounts the device over USB** — presumably built on BadgeLink's filesystem operations ([`badgelink-and-appfs.md` §5](badgelink-and-appfs.md)). It appears in the app repository as `nullislandspace/tanmatsu-badgefs`. This is a considerably nicer workflow than uploading file by file, and it is **documented nowhere official**.

There is also an `apprepo` target that assembles the exact folder layout for a pull request to the app repository.

---

## 5. Which should you write?

**Write an app** if you need the whole machine — an emulator, a game, anything doing sustained graphics or wanting full ESP-IDF. You get everything and you owe nothing to the launcher.

**Write a plugin** if you want to *extend* the launcher: add a menu entry, run a background service, react to Wi-Fi/USB/SD/power events, or add a status-bar widget. The launcher keeps running, your code coexists with up to 31 others, and users do not leave the UI.

**Practical caveats for plugins:**

- **`CONFIG_ENABLE_LAUNCHERPLUGINS` is `default n`.** Stock firmware may not load plugins at all — the user needs a launcher built with plugins enabled.
- **ESP32-P4 only** (`depends on IDF_TARGET_ESP32P4`).
- **`-nostdlib`** means porting existing C code is real work. The startup plugin vendors `minimp3.h` as a single header precisely because it cannot link a normal library.
- The API is **v2.0.0** and versioned-checked; expect breakage across major versions.
- If you want concurrent audio, the launcher needs `CONFIG_ENABLE_AUDIOMIXER` too — otherwise only one source plays cleanly.

---

## 6. Worked examples

Two community plugins, both retained in the archive:

| Plugin | Type | Notes |
|---|---|---|
| [`nullislandspace/tanmatsu-plugin-startup`](https://github.com/nullislandspace/tanmatsu-plugin-startup) `3857321` | `service` | Boot logo + sound. Vendors `minimp3.h`; permissions `["audio","storage"]` |
| [`nullislandspace/tanmatsu-plugin-turret`](https://github.com/nullislandspace/tanmatsu-plugin-turret) `a1d223c` | — | Companion example |

Both use the SDK by **relative path** (`../tanmatsu-launcher/tools/plugin-sdk`), i.e. they expect the launcher checked out beside them. There is no released standalone SDK package.

---

## 8. How an app is actually executed

Traced through [`main/menu/apps.c`](https://github.com/Nicolai-Electronics/tanmatsu-launcher/blob/main/main/menu/apps.c). There are **three executable types**, and two of them reboot the device.

### `EXECUTABLE_TYPE_APPFS` — a normal app

```c
char app_path[256];
snprintf(app_path, sizeof(app_path), "%s/%s", app->path, app->slug);
appfsBootSelect(app->executable_appfs_fd, app_path);

while (wifi_stack_get_task_done() == false) { vTaskDelay(pdMS_TO_TICKS(100)); }
prepare_device_for_app_launch();
esp_restart();
```

**Launching an app reboots the ESP32-P4.** `appfsBootSelect()` records which AppFS entry the *modified
bootloader* should jump to on the next boot, then the launcher shuts down cleanly and calls
`esp_restart()`. The bootloader then starts your binary instead of the launcher.

Three details worth noting:

- The app is passed **its own directory path as an argument** (`{app->path}/{app->slug}`), so an app
  can find its assets on FAT/SD.
- The launcher **waits for the Wi-Fi task to finish** before restarting — the ESP32-C6 link is torn
  down in an orderly way rather than yanked.
- `prepare_device_for_app_launch()` runs first; `app_usage_set_last_used()` is recorded for LRU.

### Interpreter / script apps — **these work**

```c
appfs_handle_t interpreter_fd = ensure_interpreter_in_appfs(app->executable_interpreter_slug);
app_usage_set_last_used(app->executable_interpreter_slug, time(NULL));
...
snprintf(path, req + 1, "%s/%s/%s", app->path, app->slug, app->executable_filename);
appfsBootSelect(interpreter_fd, path);
esp_restart();
```

This resolves the open question about the `interpreter` / `script` metadata keys. A script app names
an **interpreter by slug**; the launcher ensures *that interpreter* is resident in AppFS, then boots it
with **the script's path as the argument**. So MicroPython scripts run by booting the MicroPython
binary and pointing it at your `.py`.

Consequences: the interpreter is an ordinary AppFS app that gets its own LRU timestamp (so a running
script does not evict its own interpreter), and script apps need **no compilation at all** — but they
still cost a reboot.

### `EXECUTABLE_TYPE_ELF` — plugins

Gated on `CONFIG_ENABLE_LAUNCHERPLUGINS`. **No reboot** — loaded in-process via kbelf.

### Summary

| Type | Reboots? | Needs compiler? | Runtime |
|---|---|---|---|
| `appfs` | **Yes** | Yes (ESP-IDF) | Owns the machine |
| `interpreter`/`script` | **Yes** (boots the interpreter) | **No** | Inside the interpreter |
| `elf` (plugin) | **No** | Yes (plugin SDK) | Inside the launcher |

---

## 9. Custom `.bin` vs installing an app

A frequent question: if I already have a firmware binary, what is different about "installing an app"?

**Nothing, structurally.** An AppFS app *is* an ordinary ESP32-P4 firmware image. The difference is
only **where it is stored and who starts it**:

| | Flashed firmware | AppFS app |
|---|---|---|
| Location | `ota_0` at `0x20000` | AppFS partition at `0x420000` |
| Written by | `esptool` over USB, device in bootloader | Launcher, BadgeLink, or file copy |
| Started by | ROM → 2nd-stage bootloader | ROM → **AppFS-patched bootloader** → selected entry |
| Replaces | **The launcher itself** | Nothing — launcher remains at `ota_0` |
| Requires | Physical bootloader entry | Nothing; done from the UI |
| Reversible | Reflash the launcher | Pick a different app, or reboot |

So to run a custom binary you have **two routes**:

**Route 1 — install it as an app** (recommended). Wrap the `.bin` with a `metadata.json`, put it in
`/int/apps/<slug>/` or `/sd/apps/<slug>/`, or upload via BadgeLink. The launcher survives; you can
switch back by rebooting. No cable required after the first install.

**Route 2 — flash it over the launcher.** `esptool ... 0x20000 myapp.bin`. Your firmware replaces the
launcher at `ota_0`. You now own the device completely — and you have lost the launcher, AppFS, the app
menu and BadgeLink until you reflash it ([`development.md` §3](development.md)).

**Route 1 is almost always what you want.** The only reasons to take route 2 are: you need the full
2 MB `ota_0` slot, you want OTA A/B updating, or you are replacing the launcher deliberately.

⚠ **An app binary must still be built for the right chip** — `esp32p4` for Tanmatsu. That is what the
`targets` array in `metadata.json` declares. See [`portability.md`](portability.md).

---

## 10. Gaps

| Question | Status |
|---|---|
| Is `plugin.json` `permissions` enforced? | **RESOLVED: no.** `parse_plugin_metadata()` reads only `type`. `permissions`, `api_version` and `autostart` are **not parsed from `plugin.json` at all** — see §11 |
| Is `badgefs` documented anywhere? | **No** — found only in a community Makefile |
| Does the SDK work standalone? | **No** — examples reference it by relative path into a launcher checkout |
| SDK README says **ESP-IDF v5.x**; launcher needs **6.0.2** | ⚠ **Inconsistent** — the SDK only needs the toolchain, so v5.x may genuinely suffice, but this is untested |
| Are `elf`/`script`/`interpreter` app types functional? | **RESOLVED** — all three are implemented. `elf` = plugins; `interpreter`/`script` boot an interpreter with the script path as argument. See §8 |
| Neither plugin was compiled | No toolchain here; **all build claims are `reported-working` or `inferred`** |

## Related

- [`software-architecture.md`](software-architecture.md) — plugin API surface, app tiering, launcher internals
- [`badgelink-and-appfs.md`](badgelink-and-appfs.md) — the protocol behind `badgefs`
- [`software-and-apps.md`](software-and-apps.md) — the app repository and `metadata.json` schema
- [`development.md`](development.md) — toolchain setup ⚠ *(documents ESP-IDF 5.x; launcher needs 6.0.2)*


---

## 11. What the plugin loader actually validates

Traced through [`main/plugin_manager.c`](https://github.com/Nicolai-Electronics/tanmatsu-launcher/blob/main/main/plugin_manager.c) (1,128 lines).

### `plugin.json` is barely read

`parse_plugin_metadata()` carries this comment:

```c
// Read plugin.json for runtime fields (type, api_version, autostart, permissions)
```

…but the code that follows parses **only `type`** (`menu` / `service` / `hook`, defaulting to menu).
`api_version`, `autostart` and `permissions` are **never read from `plugin.json`**. It then reads
`name` and `version` from `metadata.json` for display, falling back to the directory slug.

**So `"permissions": ["audio", "storage"]` is a dead field.** There is **no permission enforcement
anywhere in the launcher.** A plugin has whatever access the `asp_*` API surface gives it, regardless
of what it declares. Treat the field as aspirational.

### What *is* validated — all from the ELF, not the JSON

At load time (`plugin_manager_load`):

1. **kbelf loads the ELF** — `kbelf_dyn_create` → `kbelf_dyn_set_exec` → `kbelf_dyn_load`.
2. **Magic check:** `reg->magic != TANMATSU_PLUGIN_MAGIC` (`0x544D5350`, `"TMSP"`) → reject.
3. **Struct-size check:** `reg->struct_size > sizeof(plugin_registration_t)` → reject, with the
   comment that a larger struct means *"the plugin embeds entry-point fields past"* what this launcher
   knows, so calling them would jump *"into garbage"*. A **smaller** struct is accepted.
4. **API major version:** taken from `get_info()` **inside the ELF**, not the JSON:
   ```c
   uint32_t plugin_major = (info->api_version >> 16) & 0xFF;
   if (plugin_major != TANMATSU_PLUGIN_API_VERSION_MAJOR) { /* reject */ }
   ```
   Major must match exactly; minor and patch are informational.

The registration struct is located because `.plugin_info` is placed at **VMA 0** by `plugin.ld` — the
loader reads offset zero of the loaded image.

### Limits

`PLUGIN_MAX_LOADED` is **32**. Discovery scans `/int/plugins` and `/sd/plugins`, deduplicating by slug.
Unload is reference-counted through `_plugin_manager_unload`, and all plugins are unloaded in reverse
order at shutdown.

### Security summary

The loader defends against **the wrong file** and **the wrong API version**. It does **not** defend
against a *malicious* plugin: no signing, no sandbox, no permissions, and plugins run in-process with
`asp_plugin_input_inject` able to synthesise input. Consistent with the rest of the platform
([`badgelink-and-appfs.md` §9](badgelink-and-appfs.md)) — reasonable for a hacker badge, not a
trust boundary.
