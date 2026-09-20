# Xteink X4 Classic — acquisition

**No artifact was acquired for this device, because none is publicly available.**

## Clean-clone commands

None. There is nothing to fetch.

## Wanted artifacts and their status

| Artifact | Reacquisition | Notes |
|---|---|---|
| `flashx4c.bin` — the stock dump every fact here derives from | **`blocked`** | Referenced only inside `Free-Ink/freeink-sdk` documentation. No URL exists anywhere. The maintainers hold it privately. Options: ask upstream, or dump a unit |
| Any X4C OTA package | **`blocked`** | None located |
| Vendor OTA feed response | **`manual`** | `http://gotaserver.xteink.com/api/check-update` — endpoint recovered from the X4 dump. **Not queried this session.** Would need the model/version request format, which is unknown |
| The June 2026 vendor video showing the device | **`manual`** | Referenced in [r/XTEINK `1ud0d9c`](https://old.reddit.com/r/XTEINK/comments/1ud0d9c/); no stable link captured. Currently the only known imagery |
| Any photograph | **`lost`** | None exists publicly |
| A price or listing | **`lost`** | None exists |

## Verification

`manifest.json` in this directory is an **empty artifact list with a populated
`wanted` list** — deliberately, so a verifier distinguishes "nothing was fetched"
from "nobody looked".
