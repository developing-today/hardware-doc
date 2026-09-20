# Roadmap

This project is a building block for a **Home Assistant control screen**. The camera is the first validated milestone.

## Milestone 1 — Camera foundation ✅
- [x] Flashable ESPHome config
- [x] Wi‑Fi + API + OTA
- [x] Camera working (PSRAM enabled)
- [x] HTTP stream + snapshot endpoints

## Milestone 2 — HA control screen (UI/UX)
- [ ] Define the screen UX (pages, navigation, main actions)
- [ ] Choose display hardware (touch screen size, driver support)
- [ ] ESPHome display stack (LVGL or display component)
- [ ] Core controls:
  - [ ] Home Assistant quick actions (lights, scenes, thermostats)
  - [ ] Sonos controls (play/pause, volume, favorites)
- [ ] Feedback elements:
  - [ ] Status badges (Wi‑Fi, HA connected, uptime)
  - [ ] Notifications / alerts view

## Milestone 3 — Physical enclosure & mounting
- [ ] Pick / design an enclosure (3D print, off-the-shelf, wall mount)
- [ ] Camera placement (angle, field of view, anti-glare)
- [ ] Cable management

## Milestone 4 — Power strategy (clean install)
- [ ] Keep USB-C 5V (baseline)
- [ ] Investigate direct 5V input (regulated) without a bulky charger
- [ ] Optional: PoE-to-5V splitter (external), if wall-mounted

## Milestone 5 — Reliability & performance
- [ ] Watchdog / auto-restart strategy
- [ ] Camera tuning (resolution, JPEG quality, FPS)
- [ ] Wi‑Fi roaming / reconnection robustness
- [ ] Logs & diagnostics page on the screen

## Milestone 6 — Advanced features (optional)
- [ ] Motion detection workflow (HA-side)
- [ ] Local snapshots to storage (SD / HA)
- [ ] Audio (mic) experimentation if relevant
- [ ] Privacy controls (physical shutter / disable stream)
