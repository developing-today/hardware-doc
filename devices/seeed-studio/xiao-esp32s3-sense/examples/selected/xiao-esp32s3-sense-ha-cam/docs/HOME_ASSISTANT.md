# Home Assistant — Dashboard cards & tips

Once the device is added through the ESPHome integration, you can display the camera in a dashboard.

## Option A — Use the ESPHome camera entity (recommended)
1. Edit your dashboard
2. **Add card**
3. Choose **Camera** (or **Picture Entity**)
4. Select the camera entity exposed by ESPHome (entity name depends on your setup)

## Option B — Use the HTTP stream for quick debugging
If you prefer to display the HTTP stream directly:
- Stream URL: `http://<IP>:8080`
- Snapshot URL: `http://<IP>:8081`

Add a **Webpage** card and paste the stream URL.

## Practical control entities to add
If you enabled the `restart` button (see YAML):
- Add a **Button** card linked to the restart entity for quick recovery.

## Networking notes
- Make sure Home Assistant and the device are on the same LAN/VLAN.
- mDNS name: `minicam-esp32.local` (may depend on your network).
