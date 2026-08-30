# Finding projects that use a board or component

> Device-independent research technique. Written **2026-08-26** after it produced a step change in
> results on the Waveshare ESP32-P4-WIFI6-Touch-LCD-XC boards.

## The problem

Searching a product's **marketing name** finds the vendor's own repositories and little else. Real
projects rarely put the full product name anywhere a repository search can index — their README
says "Waveshare XC", or "my P4 dashboard", or nothing at all.

On the ESP32-P4 boards, product-name searches across several passes found **two** community
projects. Two techniques below took that to **a dozen or more**, and turned up the vendor's own BSP
source repository that earlier passes had concluded was unavailable.

## Technique 1 — search for the dependency, not the product

**A project that uses a board must declare its dependency.** That string is far more
distinctive and far more reliably present than the product name.

For an ESP-IDF board this is the **BSP component name**:

```bash
# Product name — finds the vendor, mostly
gh api -X GET search/repositories -f q='ESP32-P4-WIFI6-Touch-LCD-3.4C' --jq '.total_count'
# -> 3

# BSP component name — finds users
gh api -X GET search/repositories -f q='esp32_p4_wifi6_touch_lcd_xc' --jq '.total_count'
# -> 2, but including a native Linux port no product-name query ever surfaced
```

Good dependency strings by ecosystem:

| Ecosystem | Search for |
|---|---|
| ESP-IDF | BSP or driver component name, e.g. `esp32_p4_wifi6_touch_lcd_xc`, `esp_lcd_jd9365` |
| Arduino | Library name from `library.properties` |
| Rust | Crate name |
| Python | Distribution name on PyPI |
| Zephyr | Board identifier or devicetree compatible string |
| Linux | Devicetree `compatible` string, or the driver's `MODULE_ALIAS` |

## Technique 2 — code search, which needs a token

Repository search only indexes names and descriptions. **Code search reads file contents**, which
is where dependency declarations actually live — `idf_component.yml`, `dependencies.lock`,
`sdkconfig`, `platformio.ini`, `Cargo.toml`.

Code search **requires authentication**. Unauthenticated it returns:

```
HTTP 401  {"message": "Requires authentication"}
```

### Getting a token

If the GitHub CLI is installed and logged in, it will hand you one:

```bash
gh auth token          # prints the token
gh auth status         # check first; prints the account
```

Use it directly, without ever writing it to a file:

```bash
T=$(gh auth token)
curl -sSL -H "Authorization: Bearer $T" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/code?q=BSP_LCD_TYPE_800_800_3_4_INCH&per_page=20"
```

Or let `gh` handle auth entirely, which is tidier:

```bash
gh api -X GET search/code -f q='BSP_LCD_TYPE_800_800_3_4_INCH' \
  --jq '.items[] | "\(.repository.full_name) | \(.path)"' | sort -u
```

**Never echo a token into a log, a file, or a document.** Capture it into a shell variable and let
it die with the shell.

### What to search for

Pick strings that only appear in a real user's build:

| String type | Example | Appears in |
|---|---|---|
| Board-selection macro | `BSP_LCD_TYPE_800_800_3_4_INCH` | `sdkconfig`, `sdkconfig.defaults` |
| Component name | `waveshare__esp32_p4_wifi6_touch_lcd_xc` | `managed_components/`, `dependencies.lock` |
| Driver symbol | `esp_lcd_new_panel_jd9365` | application source |
| Distinctive constant | an unusual I²C address or magic number | driver or config |

The `managed_components/` and `dependencies.lock` hits are especially good signal: they only exist
because someone actually **built** the project against that dependency.

## Worked result

Both techniques applied to one board on 2026-08-26:

| Query | Type | Outcome |
|---|---|---|
| `ESP32-P4-WIFI6-Touch-LCD-3.4C` | repo | 3 hits — vendor + 2 community |
| `esp32_p4_wifi6_touch_lcd_xc` | repo | Found a **native Linux port** that documents the ESP32-C6 SDIO link |
| `BSP_LCD_TYPE_800_800_3_4_INCH` | **code** | **187 hits**, 8+ distinct real projects |
| `esp32_p4_wifi6_touch_lcd_xc` | **code** | **178 hits**, including the vendor's **BSP source repository** |

The BSP repository (`waveshareteam/Waveshare-ESP32-components`, 74★) mattered most. An earlier pass
had recorded the BSP as *"resolved by the Component Manager, not vendored"* and stopped there.
Code search found the source, which then **independently confirmed sixteen GPIO assignments** that
had been derived by reading a schematic PDF visually — and confirmed two deliberate omissions in
vendor software that had been flagged as risks.

## Why this is worth doing early

Both techniques are cheap and neither needs the artifact in hand. Running them **before** deep
artifact analysis would have saved hours of manual schematic reading on this device — the vendor's
own header had the answers.

Sequence to prefer:

1. Product name → find the vendor.
2. **Dependency name** → find users and the dependency's own source.
3. **Code search on a build-artifact string** → find projects that never name the product.
4. *Then* analyse artifacts, using the above to cross-check.

## Results across five devices in this library

Run 2026-08-26 with an authenticated token. The pattern is consistent: **repository search finds the
vendor, code search finds the users.**

| Device | Best query | Distinct projects | Notable |
|---|---|---:|---|
| Waveshare ESP32-P4-WIFI6-Touch-LCD-XC | `BSP_LCD_TYPE_800_800_3_4_INCH` | **8+** | Found the **BSP source repo**; a 256★ and an 89★ project |
| Waveshare ESP32-S3-Knob-Touch-LCD-1.8 | `ESP32-S3-Knob-Touch-LCD-1.8` | 3 | **ESPHome device page** for the Guition clone — 8 matching pins |
| Nicolai Tanmatsu | `tanmatsu esp32p4` | **9** | `Nicolai-Electronics/tanmatsu-template` (official), plus a cluster of "konsool" projects |
| Soldered Inkplate 5 | `Inkplate5` | 5 | `SolderedElectronics/Soldered-Inkplate-ESPHome` (vendor ESPHome), `lanrat/homeplate`, `bitbank2/FastEPD` |
| ZeroWriter Ink | *(none effective)* | 0 | See the false-positive note below |

### When the product name is a common word

`zerowriter` returned **254 matches** — headed by `golang/go` and `NationalSecurityAgency/ghidra`.
Those are not ZeroWriter projects; the string appears incidentally in unrelated code.

Narrowing with `zerowriter+inkplate`, `zerowriter_ink` and `ZeroWriter+eink` all returned **0**.

Two lessons:

1. **A high `total_count` is not a signal.** Always inspect the repository names before believing it.
2. **Zero after narrowing is a real result**, and a more honest one than 254 false positives. For
   this device, GitHub code search simply does not find users — which is itself worth recording
   rather than leaving the impression that a search was never run.

### Sibling-board contamination

On the P4 boards the same BSP macro appeared in projects for the **4B** and **7B** — different
panels, different BSP variants. Always confirm the variant from the project's own `sdkconfig`
before treating a hit as evidence for your board:

```bash
curl -sSL https://raw.githubusercontent.com/<owner>/<repo>/main/sdkconfig \
  | grep -E "^CONFIG_BSP_LCD_TYPE.*=y"
```

That one check moved four projects from "maybe relevant" to "confirmed on this exact variant", and
correctly rejected three popular ones.

## Limitations

- Code search is **rate-limited more aggressively** than repository search.
- It indexes a subset of GitHub — very large repositories and some file types are excluded.
- `total_count` is a match count, **not** a project count. Deduplicate by repository:
  ```bash
  gh api -X GET search/code -f q='<string>' --jq '.items[].repository.full_name' | sort -u
  ```
- It searches **GitHub only**. GitLab, Codeberg and Gitee need separate handling.
- A hit proves a string appears, not that the project works or targets your exact variant. On this
  board the same macro appeared in projects for **sibling boards** — always confirm the variant.

## Related

- [`vendors/waveshare/README.md`](../../vendors/waveshare/README.md) §8 — vendor-specific patterns
- [`devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/examples/search-log.md`](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/examples/search-log.md) — the log these findings came from
