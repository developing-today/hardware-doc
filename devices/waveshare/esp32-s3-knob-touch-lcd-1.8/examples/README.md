# Community examples

- **[catalog.md](catalog.md)** — annotated catalogue of 28 third-party projects for this board, plus non-repository resources (videos, forums). Start with §1 "Highest-value projects".
- **[catalog.json](catalog.json)** — the same repository set as machine-readable metadata: pinned commit, licence, framework, dates, retention flag.
- **`selected/`** — source tarballs of five permissively-licensed projects, pinned to the commits recorded in the catalogue.

Compiled 2026-08-23. Nothing here is vendor-endorsed, and **no entry was built or run by us** — `build_status` is recorded as *not determinable* throughout.

## `selected/` contents

| File | Repo @ commit | Licence |
|---|---|---|
| `BlueKnob.tar.gz` | `joshuacant/BlueKnob` @ `c71c98ff5b` | Apache-2.0 (`LICENSE` present) |
| `esp32-s3-knob-hardware-explorer.tar.gz` | `IngoDuesentrieb/esp32-s3-knob-hardware-explorer` @ `87602cacde` | MIT (`LICENSE` present) |
| `lvgl_kawaii_face.tar.gz` | `0015/lvgl_kawaii_face` @ `d58e1c8f8e` | MIT (`LICENSE` present) |
| `lyngdorf-secondary-sleep.tar.gz` | `svwhisper/lyngdorf-secondary-sleep` @ `dfc372fb07` | ⚠️ MIT in README only |
| `Waveshare-…-first-successful-screen-test.tar.gz` | `UnkMihai/…` @ `3cd890b473` | ⚠️ MIT in README only |

The two flagged entries declare MIT in prose but ship no licence file. See [catalog.md §4](catalog.md) before redistributing either.

~~~sh
# Re-fetch any pinned tarball
curl -L -o NAME.tar.gz https://codeload.github.com/OWNER/REPO/tar.gz/COMMIT
~~~
