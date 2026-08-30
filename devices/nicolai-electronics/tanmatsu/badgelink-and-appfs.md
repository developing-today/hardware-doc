# BadgeLink and AppFS — protocol and on-device details

> The USB management protocol and the app filesystem, read from source rather than documentation.
> Snapshot **2026-08-24**. Sources: [`badgeteam/esp32-component-badgelink`](https://github.com/badgeteam/esp32-component-badgelink) @ `3e3e695` (2026-05-01, **MIT**) and the launcher firmware @ `20022fce`.
> **Nothing was built, flashed or run** — this is source reading.

The vendor documentation covers *using* BadgeLink ([`development.md` §5](development.md#5-badgelink--managing-the-device-over-usb)). This page covers *how it works*, which matters if you want to write your own client, debug a transfer, or understand the failure modes.

---

## 1. BadgeLink in one paragraph

BadgeLink is a **Protobuf-over-COBS-over-USB-vendor-class** protocol for managing **NVS settings, AppFS applications and FAT filesystem contents** on ESP-IDF devices. It exists because the ESP32-P4 can swap its USB PHY away from USB-serial/JTAG to a TinyUSB vendor device — so the same USB-C port is either a debugger *or* a management interface, never both at once.

Its own README is two lines long; the **authoritative specification is [`badgelink.proto`](https://github.com/badgeteam/esp32-component-badgelink/blob/main/badgelink.proto)**, 234 lines of proto3.

---

## 2. Wire format

```
 Protobuf message  ->  COBS encode  ->  NUL terminator  ->  31-byte USB fragments
```

| Layer | Detail |
|---|---|
| Serialisation | **proto3**, compiled with **nanopb** (vendored in-tree) |
| Framing | **COBS** (Consistent Overhead Byte Stuffing), `cobs.c` — © 2025 Julian Scheffers, MIT |
| Delimiter | COBS emits a **NUL terminator**; decode expects it still present |
| Fragment | **31 bytes payload + 1 length byte = 32 bytes** (`fragment_t { uint8_t data[31]; uint8_t len; }`) |
| RX queue | `CONFIG_BADGELINK_QUEUE_SIZE`, default **256 fragments**, range 16–1024 |
| Transport | USB **vendor class** (TinyUSB), plus WebUSB from Chromium browsers |

COBS is the right choice here: it guarantees no NUL byte appears inside an encoded frame, so a single NUL unambiguously delimits messages on a byte stream — no escaping, no length prefix needed, worst-case overhead of 1 byte per 254.

**Buffer sizing**, from `cobs.h`:

```c
#define COBS_ENCODED_MAX_LENGTH(len) ((len) + (((len) + 253) / 254) + 1)
#define COBS_DECODED_MAX_LENGTH(len) ((len) - 1)
```

At the default queue depth the device can buffer 256 × 31 = **7,936 bytes** of in-flight fragments.

## 3. Version negotiation

```c
#define BADGELINK_PROTOCOL_VERSION 3
static uint16_t negotiated_version = 1;
...
uint16_t negotiated = client_version < BADGELINK_PROTOCOL_VERSION
                        ? client_version : BADGELINK_PROTOCOL_VERSION;
```

The device is at **protocol version 3**; it negotiates **`min(client, device)`** and defaults to 1 before negotiation. `VersionReq{client_version}` → `VersionResp{server_version, negotiated_version}`.

So an older client keeps working against newer firmware, at the older feature level.

## 4. Packet structure

```protobuf
message Packet {
  oneof packet { Request request = 2; Response response = 3; bool sync = 4; }
  uint64 serial = 1;
}
```

Every packet carries a **`uint64` serial** for request/response correlation, and there is a **`sync`** packet type for resynchronising a confused stream — useful if a client disconnects mid-transfer.

### Requests

| Request | Purpose |
|---|---|
| `appfs_action` | Manage installed applications |
| `fs_action` | FAT filesystem operations |
| `nvs_action` | Read/write NVS settings |
| `upload_chunk` | Bulk data in |
| `xfer_ctrl` | `XferContinue` / `XferAbort` / `XferFinish` |
| `start_app` | Launch an app by slug, **with an argument string** |
| `set_usb_mode` | `UsbModeDebug` ⇄ `UsbModeDevice` |
| `version_req` | Negotiate |

Responses carry a `StatusCode` plus an optional payload (`download_chunk`, `appfs_resp`, `fs_resp`, `nvs_resp`, `version_resp`).

**`StartAppReq` takes `{slug, arg}`** — you can pass an argument when launching an app remotely. Nothing in the vendor documentation mentions this.

## 5. Filesystem operations

`FsActionType` — 11 operations:

`List` · `Delete` · `Mkdir` · `Upload` · `Download` · `Stat` · **`Crc23`** *(sic — CRC-32, the enum name is a typo)* · `GetUsage` · `Rmdir` · `Copy` · `Rename`

`FsStat` returns `size`, **`mtime`/`ctime`/`atime` as `uint64`**, and `is_dir`. `FsUsage` returns `size` + `used`, so a client can show free space.

**Directory listing is paginated**: `FsActionReq.list_offset` in, `FsDirentList.total_size` back. Large directories will not blow the 31-byte fragment budget.

**Integrity is CRC-32 throughout** — `crc32` fields on both request and response for uploads, downloads and the explicit CRC action. Transfers are verified, not assumed.

## 6. NVS access

`NvsActionType`: `List` · `Read` · `Write` · `Delete`, over `{namespc, key}`.

`NvsValueType` covers **uint8/int8/uint16/int16/uint32/int32/uint64/int64/string/blob** — the full ESP-IDF NVS type set. `NvsValue` is a `oneof` of `numericval` (u64), `stringval`, `blobval`, tagged with its declared type.

This is a **complete settings-editing interface over USB**: any namespace, any key. Worth knowing from a security standpoint — see [§9](#9-security-observations).

## 7. AppFS

### What it is

An ESP-IDF component implementing a pseudo-filesystem for **whole firmware binaries**, plus a **bootloader modification** that can start an application directly out of that partition. Created by **Jeroen Domburg (sprite_tm)** for the PocketSprite; extended by Badge.Team. Supports ESP-IDF 5.3+, with bootloader changes for ESP32, ESP32-C6 and ESP32-P4.

On Tanmatsu it occupies **8 MB** at `0x420000` — the largest single flash region, larger than both 2 MB firmware slots combined ([`development.md` §2](development.md#2-esp32-p4-flash-layout)).

### Metadata model

```protobuf
message AppfsMetadata {
  string slug = 1; string title = 2; uint32 version = 3; uint32 size = 4;
}
```

Four fields only — **`slug`, `title`, `version`, `size`**. Note what is *absent*: no author, no signature, no checksum, no dependency list, no permissions. Richer metadata (categories, icons, licence, author) lives in the **app repository's `metadata.json`**, not on the device — see [`software-and-apps.md`](software-and-apps.md).

Listing is paginated the same way (`list_offset` / `total_size`), and `AppfsActionResp` can return `FsUsage` so a client can show remaining app space.

### Launcher-side settings

From `tanmatsu-launcher/main/appfs_settings.c`, NVS namespace **`"appfs"`**:

| Setting | Behaviour |
|---|---|
| `auto_cleanup` | Automatic removal of apps |
| `mismatch_reinstall` | Reinstall on version/target mismatch |

Neither appears in the vendor documentation.

### Integrating AppFS yourself

```bash
idf.py add-dependency "badgeteam/appfs^1.0.0"
mkdir bootloader_components
ln -s managed_components/badgeteam__appfs bootloader_components/appfs
ln -s managed_components/badgeteam__appfs/bootloader_main bootloader_components/main
```

⚠ **The symlink step is mandatory and easy to miss.** Adding the dependency exposes the API but does *not* apply the bootloader modification — you get a build that compiles cleanly and cannot launch apps. Apps themselves need no changes; only a *launcher* needs the component.

## 8. USB mode switching

```protobuf
enum UsbMode {
  UsbModeDebug = 0;   // Flash/monitor mode (ESP32 built-in USB-serial/JTAG).
  UsbModeDevice = 1;  // BadgeLink mode (TinyUSB vendor device).
}
```

Switchable **in software** via `SetUsbModeReq`, or **on the device** with the purple diamond key (second from top-right); the status icon changes from a bug to a USB symbol.

The two modes are mutually exclusive — the P4 has one USB PHY routed to the hub port, and it is either the ROM's serial/JTAG or a TinyUSB vendor device. **Switching to `UsbModeDevice` therefore disconnects your debugger**, and switching back interrupts BadgeLink.

## 9. Security observations

Stated as design facts, not criticisms — the threat model for a hacker badge is legitimately different from a phone.

- **No authentication anywhere in the protocol.** Anything that can open the USB vendor interface can read and write NVS, the FAT filesystem and AppFS, and launch arbitrary installed apps.
- **No signature or integrity field on `AppfsMetadata`.** CRC-32 protects transfers against corruption, not tampering — it is not a MAC.
- **Secure boot is permanently disabled by design** on Tanmatsu, *"to prevent accidental bricking"*.
- **WebUSB means a web page can drive all of this**, subject to the browser's device-permission prompt.

For a device intended to be modified this is a coherent set of choices. Just do not treat a Tanmatsu as a trusted store for secrets, and be deliberate about which pages you grant WebUSB access.

## 10. Client tooling

Python client and `60-badgelink.rules` ship in `tools.zip` on the component's [releases](https://github.com/badgeteam/esp32-component-badgelink/releases) page; a WebUSB front-end works in Chromium/Edge. Setup and udev instructions: [`development.md` §5](development.md#5-badgelink--managing-the-device-over-usb).

Because the schema is plain proto3, **you can generate a client in any language** — `protoc badgelink.proto` and implement COBS + 31-byte fragmenting. That is a far smaller job than the absence of documentation suggests.

## 11. Gaps

| Question | Status |
|---|---|
| USB VID/PID for the vendor interface | **Not found** in the component source — likely set by the host firmware's TinyUSB descriptor, not by BadgeLink |
| AppFS **on-flash** layout (headers, page tables) | **Partially resolved** — real component now fetched (`esp32-component-appfs` @ `eee29be`). Boot selection and OTA-slot substitution documented in §12; the sector/page allocation format is still not fully transcribed |
| What `sync` does exactly | Present in `Packet`; handler not traced |
| Are protocol versions 1 and 2 documented anywhere? | **No** — only `min()` negotiation is visible |
| Practical transfer throughput | **Unmeasured** — no hardware |
| `FsActionCrc23` naming | Enum typo for CRC-32; harmless but will confuse generated clients |

---

## 12. How the bootloader chooses: launcher or app?

Answered from the **real AppFS component** — [`badgeteam/esp32-component-appfs`](https://github.com/badgeteam/esp32-component-appfs) @ `eee29be` (2026-08-25, **Apache-2.0**). Earlier sections used the mock bundled with BadgeLink; this is the shipping implementation.

### The selection record lives in RTC retained memory

```c
#define APPFS_BOOTSEL_MAGIC  0x2af7de4a994f7236
#define APPFS_MAX_ARG_LENGTH 127

typedef struct {
    uint64_t magic;
    appfs_handle_t fd;
    bool     valid;
    char     arg[APPFS_MAX_ARG_LENGTH + 1];
} appfs_bootsel_t;
```

`appfsBootSelect(fd, arg)` writes this into `bootloader_common_get_rtc_retain_mem()->custom` — **RTC
retained memory, which survives a reset but not a power cycle.** It sets `magic`, the AppFS file
descriptor, `valid = true`, and copies the argument (silently discarded if longer than 127 bytes).

> This is why the launcher requires `CONFIG_BOOTLOADER_CUSTOM_RESERVE_RTC` with a user section —
> see [`display.md` §4.3](display.md). The bootsel struct lives in that reservation.

There is a fallback mode, `CONFIG_APPFS_USE_RTC_REG`, that stores only `0xA5000000 | fd` in a single
RTC register (`RTC_CNTL_STORE0_REG`, or `LP_AON_STORE0_REG` on newer parts). In that mode
**arguments are not supported** and the code logs a warning — so script/interpreter apps
([`apps-vs-plugins.md` §8](apps-vs-plugins.md)) cannot work with it enabled.

### Does RTC retained memory need a battery?

**No.** This is a common confusion because "RTC" appears in two unrelated roles on this device.

**ESP32-P4 RTC retained memory** is SRAM in the chip's low-power domain. It survives a **software
reset** (`esp_restart()`) and **deep sleep**, because the domain stays powered throughout — the chip
never actually loses power during a reset. That is all AppFS boot selection needs: write the record,
reboot, read it back a few hundred milliseconds later.

It does **not** survive a full power-down, and it does not need to. If the battery is removed, the
pending selection is lost and the device boots the launcher — the safe default.

Confirmed from the fabrication netlist: the ESP32-P4's **`VDD_BAT` (pin 102) and `VDD_LP` (pin 9) are
both tied directly to the main `+3.3V` rail**, not to any separate cell. **There is no coin cell of
any kind on the Tanmatsu** — the only battery entry in the BOM is `J11`, the JST-PH connector for the
main 2500 mAh LiPo.

For contrast, the **timekeeping** RTC is a different thing entirely: it lives in the **CH32V203
coprocessor**, backed by a 32.768 kHz watch crystal (`Y3`) and kept alive by the always-on 2.5 V LDO
(`LR8341A-M25`) fed from the LiPo — see [`keyboard.md` §1.10](keyboard.md). So the clock survives
"off", but from the main battery, not a CR2032. Remove the LiPo and you lose the time.

| | AppFS boot selection | Timekeeping |
|---|---|---|
| Where | ESP32-P4 RTC retained SRAM | CH32V203 coprocessor + 32.768 kHz crystal |
| Powered by | `+3.3V` main rail | 2.5 V standby LDO from the LiPo |
| Survives reset | ✅ | ✅ |
| Survives power off | ❌ (and need not) | ✅ while a LiPo is connected |
| Coin cell | **none** | **none** |

### The bootloader's decision

On every boot the patched bootloader reads that struct:

1. **No valid magic → boot normally**, i.e. the launcher from `ota_0`.
   The log line is explicit: `"No AppFS app selected or failed to open app, starting launcher"`.
2. **Valid selection → boot the app instead**, by a neat piece of misdirection:

```c
// Note that the rest of the bootloader code has no clue about appfs, and as such won't try
// to boot it. We 'fix' that by chucking the appfs partition (which is now wrapped so the rest
// of the bootloader reads from the selected file when it thinks it loads from the app) into
// the top OTA slot.
bs->ota[0].offset = appfs_pos;
bs->ota[0].size   = appfs_len;
bs->app_count     = 1;
// And bingo bango, we can now boot from appfs as if it is the first ota partition.
```

The AppFS partition is **substituted into the OTA slot table**, with flash reads wrapped
(`appfs_flashfunctions_wrapper.c`) so that a read of "the app partition" is transparently redirected
to the selected file's pages. Stock ESP-IDF boot code then proceeds unmodified.

### It is one-shot

```c
// Mark bootsel as invalid to prevent repeated start.
bootsel->valid = false;
```

The selection is **cleared immediately before the app is loaded**. So:

- Launching an app is a **single-shot** action — reboot again and you are back in the launcher.
- A **crash loop in an app cannot trap the device**: the next reset finds `valid == false` and boots the launcher.
- To relaunch the same app you must go through the launcher again.

That is a genuinely good safety property, and it explains why "reboot" is the universal escape from a misbehaving app.

### Answering the question directly

> **Is the launcher "included"?**

The launcher is **ordinary firmware in `ota_0`** — it is not part of AppFS and AppFS does not contain
it. AppFS is a *separate partition* the bootloader can be redirected into. **The launcher is the
default boot target**; an app only runs when a valid one-shot selection is present in RTC memory.

Flashing your own firmware to `ota_0` replaces the launcher and you simply never get the app menu
(see [`apps-vs-plugins.md` §9](apps-vs-plugins.md)). AppFS keeps working, but nothing is left to
select apps from.

## 13. AppFS has no permission model

Directly answering whether the **latest** AppFS checks permissions: **it does not.**

Grepping `permission|capabilit|sandbox|privile|signature|verify` across `src/`, `include/` and
`bootloader_main/` at `eee29be` returns only:

- `"Verify that arg is null-terminated"` — a `strnlen` bounds check
- `"Verify the validity of `fd`"` — `appfsFdValid()`
- `esp_partition_table_verify()` — stock ESP-IDF partition-table integrity
- an Apache-2.0 licence header containing the word "permissions"

There is **no signing, no capability model, no sandbox, and no permission field** anywhere in AppFS.
An app selected via `appfsBootSelect()` runs as ordinary firmware with full hardware access. This
matches the launcher side, where `plugin.json`'s `permissions` array is
[parsed by nothing at all](apps-vs-plugins.md).

## 14. AppFS supports ten targets

`idf_component.yml` at `eee29be`:

```yaml
targets: [esp32, esp32s3, esp32c6, esp32p4, esp32c5, esp32c3, esp32c61, esp32h2, esp32s31, esp32c2]
dependencies: { idf: ">=6.0.2", cmake_utilities: "0.*" }
license: Apache-2.0
```

Substantially wider than the documentation's *"bootloader modifications for the ESP32, ESP32-C6 and
ESP32-P4 included. Other ESP32 variants are not supported yet"* — that statement is **stale**. See
[`portability.md`](portability.md).

## Related

- [`development.md`](development.md) — using BadgeLink and AppFS
- [`software-and-apps.md`](software-and-apps.md) — the app repository and its richer metadata
- [`pinouts-and-buses.md` §6](pinouts-and-buses.md#6-usb-topology) — USB hub topology and why one PHY is shared
- [`sources.md`](sources.md) — provenance
