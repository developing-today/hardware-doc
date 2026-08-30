# `sscom5.13.1/` — extracted contents of `../Sscom5.13.1.zip`

Extracted **2026-08-24**. The ZIP itself (`../Sscom5.13.1.zip`, 420,199 bytes) remains in this
repository as the byte-exact original.

## What SSCOM is

**SSCOM** (`串口调试助手`, "serial-port debugging assistant") is a long-standing, free
Windows serial-terminal / debug-monitor by **Song Kaihua (宋凯华, "大虾" / "daxia")**,
distributed from <http://www.daxia.com>. It is one of the two or three de-facto standard serial
terminals in Chinese embedded development, which is why Waveshare links it from this board's
wiki page (§ *Serial port debugging*) rather than shipping its own.

It is **not board-specific and not required**. Any serial terminal works with this board —
`screen`, `minicom`, `picocom`, `tio`, PuTTY, `idf.py monitor`, the Arduino IDE serial monitor.
SSCOM is offered as a convenience for Windows users.

## Contents

| Member | Bytes | SHA-256 | Status |
|---|---:|---|---|
| `sscom51.ini` | 5,082 | `5ea729c438b2203b45d62a6d223b8788432a460e9318a4e758738a03515f3c42` | **Kept** — see below |
| `sscom51.ini.utf8.txt` | — | *(generated)* | **Added** — UTF-8 transcode of the above, see below |
| `sscom5.13.1.exe` | 451,072 | `51ea245a3d07436a86a4449b2791c1f37fa60e181dd128e8d7dd79cc1ad836ce` | **Archived** — see [`sscom5.13.1.exe.REMOVED.md`](./sscom5.13.1.exe.REMOVED.md) |

Total when fully extracted: **456,154 bytes across 3 files** (`unzip -l` reports 3 members
including the `sscom5.13.1/` directory entry; 2 are regular files).

Extracted-tree content digest, **as originally extracted** (both files, before the `.exe` was
archived and before `sscom51.ini.utf8.txt` was added):

```bash
find sscom5.13.1 -type f -exec sha256sum {} + \
  | sed 's|  sscom5.13.1/|  |' | sort -k2 | sha256sum
# 456,154 bytes / 2 regular files
```

## Why `sscom51.ini` was kept

It is the only human-readable file in the archive, and it is genuinely documentary rather than
just configuration. It contains the program's own inline **documentation of its settings file
format** — every key is preceded by a Chinese comment explaining it — plus the author's contact
details and licensing/registration pitch. It is 5 KB.

Notable content, since it is not obvious from a mojibake `cat`:

- The file is encoded **GB2312/GB18030**, *not* UTF-8. Reading it with a UTF-8 locale produces
  garbage. A transcoded copy is provided as `sscom51.ini.utf8.txt` for grep-ability; the
  original byte-for-byte `sscom51.ini` is retained unchanged and remains authoritative.
- Header: *"删除本文件可以恢复默认值"* — deleting this file restores defaults; the program
  rewrites it automatically, so it should not be edited externally.
- Format: `Nx=H,…` is a hex byte string, `Nx=A,…` an ASCII string; `N101`–`N199` are the
  multi-string sender slots with their labels and repeat intervals.
- `N1051`–`N1100` are the documented runtime settings: checksum mode
  (`0=None, 1=modbusCRC16, 2=ADD, 3=XOR`), DTR/RTS assertion, packet-split timeout,
  HEX display, receive-buffer colour, UI geometry, and `N1100` = UI language (`中文`/`E`).
- Baked-in defaults from the packager: `N1080=COM13`, `N1081=115200`.
- The author solicits registration via QQ `800058315` and a remote host at `120.76.28.211:80`
  (`N1068`/`N1069`). **Note that the program contains an outbound network default.** Nothing
  here executes, but be aware of it before running the `.exe` on a networked machine.

## Encoding note for the whole archive

`Sscom5.13.1.zip` stores its member names in ASCII, so no GBK filename decoding is needed for
this archive — unlike the Espressif adapter-board ZIPs elsewhere in this tree.
