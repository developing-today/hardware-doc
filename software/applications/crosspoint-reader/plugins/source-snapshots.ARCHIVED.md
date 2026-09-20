# Plugin-ecosystem source snapshots — ARCHIVED

**Archived to** `archive/software/applications/crosspoint-reader/plugins/source-snapshots/`
**Date:** 2026-09-11 · **Total:** ~176 MB, 18 entries

The archive is machine-local and absent from a fresh clone. Everything needed to
reacquire these is below; the archive path is a convenience, not the contract.

## Why these were archived

The CrossPoint SD-card plugin ecosystem is **almost entirely unlicensed and
largely unmirrored**. Of 18 snapshots, **15 carry no licence file at all**, most
sit at ★0, and one — the ADEPT client that makes library loans work — exists on
a single Railway host with **no git repository anywhere**.

This is a documentation ecosystem with a real risk of silent disappearance, and
the Libby path documented in [`libby-path.md`](libby-path.md) depends on it.

## What is held

### The store and its forks

| Repository | HEAD | Licence |
|---|---|---|
| `itsthisjustin/sd-plugins` — **the canonical store** | `dfc0a88858d1486a2707e1c4ba61517b94646dfe` | none |
| `marczykm/sd-plugins` | `98a92d09e9f921e2278d9c01db86a8aff6d9f34e` | none |
| `pagdot/sd-plugins` | `98a92d09e9f921e2278d9c01db86a8aff6d9f34e` | none |
| `Haas-Robert/sd-plugins` | `6dc90087b03cc29048a5c6aaed3a0e739afda521` | none |
| `josmerod/sd-plugins` | `6dc90087b03cc29048a5c6aaed3a0e739afda521` | none |
| `dezren39/sd-plugins` | `0b2989bdc9645b25398fd953fbf448a7bf316527` | none |
| `mjonessa/sd-plugins` | `08527fe5a09906f82c05cc4a25f6ce6cbac90bba` | none |
| `jadehawk/sd-plugins` | `b2affa12a8946284b4e27feff4f919135afee10b` | none |
| `shelbeeely/sd-plugins` | `b2affa12a8946284b4e27feff4f919135afee10b` | none |
| `ejoh1101/crosspoint-sd-plugins` | `b2affa12a8946284b4e27feff4f919135afee10b` | none |
| `aluhrs13/crosspoint-readwise-plugin` | `b2affa12a8946284b4e27feff4f919135afee10b` | none |

**Four forks share two HEADs** (`98a92d09` ×2, `6dc90087` ×2) and **four more sit
on `b2affa12`** — they are stale snapshots of the store at three points in time,
not independent work. That is itself the finding: the fork catalogues advertising
`libby` v0.2.0 are frozen at a commit whose target URL no longer exists.

### The Libby implementations

| Snapshot | Contents |
|---|---|
| `ruqqq/crosspoint-plugins` @ `8aa65e18a4e6f8b5348ef5b29c0eb8570607bba1` | **The working `libby` 1.0.2**, plus `kopi`. No licence |
| `_plugins__ruqqq-libby/` | Standalone copy of `libby/{manifest.json,plugin.js,README.md}` — belt and braces |
| `_offrepo__protected-content-railway/` | **The off-repository ADEPT client** — see below |

### The native-ELF plugin system (a separate design)

| Repository | HEAD | Licence |
|---|---|---|
| `mekhontsev/crosspoint-reader` — firmware fork, the plugin **host** | `33197aad82d47410165705ad9260eca237f30229` | MIT |
| `mekhontsev/crosspoint-plugins` — native `.so` modules | `750bbe2aff46318fb12b196334269d73c8f11a0e` | MIT |
| `mekhontsev/pagewire` — Android/Termux client + protocol | `ee56ef3ac178a1ef42855c8e9ee6a09b66c5e14b` | MIT |

Cloned `--depth 200` for the firmware fork (160 MB); the other two are full.
These are the only MIT-licensed members of the set.

### Other

`samfoy/crosspoint-bookorbit-plugin` @ `d5957f13320c1e12531c0fdd2275761ed5e19fa4`, no licence.

## The scarce one: `protected-content`

**This is the artifact that justifies the whole archive.**

| | |
|---|---|
| Source | `https://protected-content-host-production.up.railway.app/` |
| `manifest.json` | 170 B · `sha256:15d72dcdcc4643be…` |
| `plugin.js` | **53,887 B** · `sha256:e35ecc85d095882a…` |
| Licence | **none** |
| Git repository | **none — anywhere** |

Every other plugin in `itsthisjustin/sd-plugins`' catalogue is served from
`raw.githubusercontent.com`. Only this one is served from a third-party PaaS, and
only this one ships no README. `README.md` and `device.json` both return **404**,
confirming it is a two-file, web-UI-only plugin.

**Wayback submission was attempted and returned HTTP 523** (origin unreachable
through their fetcher) for both files, so **no public mirror exists**. If the
Railway deployment lapses, the local snapshot is the only copy.

## Reacquisition

```bash
# git repositories — all public, all reacquirable
git clone https://github.com/<owner>/<repo> && git -C <repo> checkout <HEAD from the tables above>

# the off-repository plugin — single host, no mirror, may vanish
curl -O https://protected-content-host-production.up.railway.app/manifest.json
curl -O https://protected-content-host-production.up.railway.app/plugin.js
```

Status: **`automatic`** for the 16 git repositories; **`blocked`/at-risk** for the
Railway files — reachable today, unmirrored, no second source.

## Licensing

**15 of 18 snapshots carry no licence** and are therefore all-rights-reserved by
default. They are retained as **research artifacts** — evidence of what existed
at a date — not as redistributable code. Do not vendor from them.

The three MIT exceptions are the `mekhontsev` repositories.

Per this project's policy licence is recorded as metadata, not treated as a gate
on acquisition; see the method's *"Record licensing as metadata"*.

## See also

- [The Libby path](libby-path.md) — what these snapshots support
- [SD-card plugins and protected content](sd-plugins-and-protected-content.md)
- [Plugin systems overview](README.md)
- `MANIFEST.md` inside the archive directory carries the same table, generated.
