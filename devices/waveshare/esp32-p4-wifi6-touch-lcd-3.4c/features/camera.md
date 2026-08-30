# How do I use the camera? — ESP32-P4-WIFI6-Touch-LCD-3.4C

> Evidence status: **vendor documentation + vendor source code. Untested on hardware.**
> Applies equally to the [4C](../../esp32-p4-wifi6-touch-lcd-4c/README.md).

## Capability summary

A **MIPI-CSI** camera input with a hardware image signal processor (ISP) and a hardware **H.264**
encoder. Waveshare claim 1080p30 capture with H.264 and JPEG encoding. Combined with the MIPI-DSI
output, the board can do camera-to-screen passthrough without the CPU touching pixels — which is
the point of the P4 and the reason this board exists.

## Hardware path

```
camera module --MIPI-CSI 2 lane--> ESP32-P4 ISP --> H.264 / JPEG encoder
                                        |
                                        +--> MIPI-DSI --> round LCD
```

| Item | Value | Evidence |
|---|---|---|
| Interface | MIPI-CSI, **2 lane** | Wiki hardware description |
| Connector | **15-pin, 1.0 mm pitch FPC** | Wiki |
| Demo lane rate | 200 Mbps | `12_camera_dsi` `EXAMPLE_MIPI_CSI_LANE_BITRATE_MBPS` |
| Claimed capture | 1080p30, H.264 + JPEG | Wiki |
| ISP | Integrated in ESP32-P4 | Wiki |
| Sensors named on wiki | **SC2336**, **OV5647** | Wiki |
| Camera included? | **Unclear** — see below | — |

The 200 Mbps figure is what the shipped passthrough demo configures, **not** a ceiling. It is
below what 1080p30 would require, which suggests the demo runs a lower resolution or the sensor
negotiates differently. Do not read it as either the maximum or as evidence that 1080p30 works.

## Is a camera included?

**Unclear.** The 3.4C store listing spans **$64.99 – $74.99** across five option slugs whose
labels could not be extracted. A camera module is the most likely differentiator, but that is
**inference, not evidence**. Confirm at purchase — see
[C6](../gaps-and-conflicts.md#c6--purchase-options-for-the-34c--resolved-2026-08-24).

Two sensors are named on the wiki, **SC2336** and **OV5647**, implying more than one module is
supported. Which one any given bundle ships — if any — is unknown. The OV5647 is the Raspberry Pi
Camera v1 sensor, so a common 15-pin 1.0 mm FPC Pi camera may be physically compatible; whether it
is *electrically and software* compatible here was **not verified**.

## Software

```yaml
dependencies:
  esp_video:            # capture
  espressif/esp_h264:   # hardware H.264 encode
```

Reference project:
`../../esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/demo/ESP-IDF/12_camera_dsi/`

It ships two local components worth reading before writing your own:

- `components/dsi_init` — display bring-up for the passthrough path
- `components/sensor_init` — sensor detection and configuration

`12_camera_dsi` is a camera-to-display passthrough, which is the best starting point: it exercises
CSI in, ISP, and DSI out together, so if it runs, the whole video pipeline is functional.

## Resource conflicts

| Resource | Shared with | Note |
|---|---|---|
| MIPI-CSI PHY | — | Dedicated |
| ISP / H.264 encoder | — | Dedicated blocks |
| **PSRAM bandwidth** | **Display, LVGL** | The real constraint |
| I²C (SCCB sensor control) | **Touch, ES8311, ES7210** | **Confirmed shared** — GPIO7/8, schematic `J5` |

PSRAM bandwidth is where camera work actually collides with everything else. A 1080p frame plus an
800 × 800 24 bpp display buffer (~1.92 MB) plus LVGL working memory all contend for the same
external memory interface. Capacity is not the issue at 32 MB; sustained bandwidth is.

Camera + display + audio + SD concurrently is **untested and unmeasured**. It is bandwidth-bound
in principle. No number appears here because none was measured.

> **Confirmed from the schematic 2026-08-24:** connector `J5` carries `ESP_I2C_SDA` and
> `ESP_I2C_SCL` — the camera's SCCB control **does** share GPIO7/GPIO8 with touch and both audio
> chips. It is not a separate bus.
>
> That makes **four** device families on one bus. A sensor whose I²C address collides with the
> GT9271 (`0x5D`/`0x14`) or the codecs needs a mux. And a stuck device takes out camera, touch and
> audio together. See [C16](../gaps-and-conflicts.md#c16--camera-sccb-shares-the-main-i²c-bus--confirmed).

## Limits

| Limit | Value | Kind |
|---|---|---|
| CSI lanes | 2 | Board (FPC) |
| Demo lane rate | 200 Mbps | Vendor-configured |
| Claimed capture | 1080p30 H.264/JPEG | **Vendor claim, unverified** |
| Achieved frame rate | **Unknown — not measured** | — |

## Pitfalls

1. **Assuming a camera is in the box.** Confirm the bundle.
2. **Assuming Pi-camera compatibility** from the OV5647 name and connector alone.
3. **Reading 200 Mbps as a ceiling.** It is one demo's setting.
4. **Ignoring PSRAM bandwidth** when combining camera and display.
5. **Treating 1080p30 as established.** It is a marketing claim; nothing here validates it.

## Open questions

- Which sensor(s) ship, and with which bundle?
- Are standard Raspberry Pi 15-pin cameras electrically and software compatible?

- Achievable frame rate with display output active.
- Is 1080p30 H.264 real on this board, and at what bitrate?

## Related

- [Display](./display.md) — the output half of the passthrough pipeline
- [ESP32-P4 chip record](../../../../components/espressif/esp32-p4/README.md)
- [Gaps and conflicts](../gaps-and-conflicts.md)
