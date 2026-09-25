# CrossPoint simulator source snapshots — ARCHIVED

**Archived to** `archive/software/tooling/source-snapshots/`
**Date:** 2026-09-20 · **2 snapshots · 1 700 666 B · 260 files**

The archive is machine-local and absent from a fresh clone. Reacquisition is below; the archive
path is a convenience, not the contract.

## What is held

| Snapshot | Remote | HEAD | Commits | Licence | Bytes |
|---|---|---|---:|---|---:|
| `crosspoint-reader_crosspoint-simulator` | `github.com/crosspoint-reader/crosspoint-simulator` | `c55f168bc0e677fdb32312c8be4b5874469465e6` (`main`) | **1** | MIT | 850 820 |
| `crosspoint-reader_crosspoint-simulator__second-copy` | same | same | **1** | MIT | 849 846 |

Cloned 2026-09-02 and 2026-09-04 by two different sessions; upstream live 2026-09-20 (39 refs).

This is the simulator behind
[`crosspoint-simulator-build-notes.md`](crosspoint-simulator-build-notes.md), whose `pgmspace`
shim is reproduced in this repository as [`sim-compat.h`](sim-compat.h).

## ⚠ Both are shallow — one commit each

`.git/shallow` present in both. **Neither carries any history.** The simulator's development
record is not preserved locally; re-clone from upstream if you need it.

## Two copies, and exactly how they differ

Both were kept. Nothing is deleted from this archive, and redundancy is *proven* rather than
assumed — measured 2026-09-20:

- **The working trees are byte-identical.** Excluding `.git/`, both content listings hash to
  `07747c7ad4556e7c11e12677f013b87299de2d98fcfa2a5b153fbfee01432bb5`.
- **The `.git/objects` trees are identical** — same packfile, same HEAD, same single commit.
- The whole-tree digests differ only because of **git-installation noise**: every
  `.git/hooks/*.sample` differs (different git versions wrote them, and one set includes
  `sendemail-validate.sample` and `pre-merge-commit.sample` the other lacks), and the second copy
  has **reflogs** (`.git/logs/…`, all `5ddde10b…`) that the first does not.

**No source file, no git object and no ref differs.** Use either. An earlier survey described
the delta as "only `.git/hooks/*.sample`" — nearly right, but it missed the reflogs and the two
extra hook templates.

## Why filed under `tooling/`

The simulator is a host-side development tool in its own repository, not firmware. The firmware
clone — whose dirty `platformio.ini` carries the native-build experiment — is at
`archive/software/applications/crosspoint-reader/source-snapshots/crosspoint-reader_crosspoint-reader/`
([placeholder](../applications/crosspoint-reader/source-snapshots/README.md)); the **pristine**
`platformio.ini` is at
`archive/software/ecosystems/crosspoint-freeink/research-captures/partial-extracts/cpr/platformio.ini`
([placeholder](../ecosystems/crosspoint-freeink/research-captures.ARCHIVED.md)).

The load-bearing finding from that experiment —
`-DCROSSPOINT_SIM_USE_NATIVE_DECODERS` **does not work**, because of `#include_next` ordering —
is in [`crosspoint-simulator-build-notes.md`](crosspoint-simulator-build-notes.md) §4, so the
archive can be absent without losing it.

## Reacquisition

Status **`automatic`**:

```bash
git clone https://github.com/crosspoint-reader/crosspoint-simulator.git
git -C crosspoint-simulator checkout c55f168bc0e677fdb32312c8be4b5874469465e6
```

A clone taken from either archived snapshot reproduces only the single commit.
