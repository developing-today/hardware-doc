# RISC-V and vendor-SDK toolchains on NixOS

Companion to [`guides/nixos/README.md`](README.md), which covers ESP-IDF, Arduino, PlatformIO
and the SDR/mesh tooling. **This file is new (2026-09-04) and adds a case that guide does not
cover: a vendor SoC SDK that is not ESP-IDF, is not Arduino, is not upstream RISC-V GCC, and is
built by Buildroot against a hard-coded absolute path.**

The worked example is the [Canaan Kendryte K230](../../components/canaan/k230/README.md) as
built by [LilyGO's T-Display K230 BSP](../../devices/lilygo/t-display-k230/README.md), which is
the first RISC-V Linux target in this repository.

> **Evidence boundary, stated up front.** Nothing here has been built. **No `nix build`, no
> `nixos-rebuild`, no Buildroot run, no flash.** Every claim is either read directly out of the
> vendor's committed build configuration (labelled *read from source*) or is reasoning about how
> NixOS behaves (labelled *inferred*). Treat build success as unverified.

---

## 1. Why `guides/nixos/README.md` does not already answer this

That guide's §2 lists `pkgsCross.riscv64-embedded` and `pkgsCross.riscv32-embedded` as present
in the locked nixpkgs. Both exist. **Neither is usable for this target**, for three independent
reasons, all *read from source* in the vendor Buildroot defconfig:

```
BR2_TOOLCHAIN_EXTERNAL=y
BR2_TOOLCHAIN_EXTERNAL_CUSTOM=y
BR2_TOOLCHAIN_EXTERNAL_PATH="/opt/toolchain/Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V3.0.2/"
BR2_TOOLCHAIN_EXTERNAL_CUSTOM_PREFIX="riscv64-unknown-linux-gnu"
BR2_TOOLCHAIN_EXTERNAL_CUSTOM_GLIBC=y
BR2_TARGET_OPTIMIZATION="-mcpu=c908v -mtune=c908 -mrvv-v0p10-compatible -mrvv-auto-vectorize"
```

1. **`-mcpu=c908v` is not a mainline GCC option value.** It is a T-Head/XuanTie extension.
   Mainline `riscv64-unknown-linux-gnu-gcc` rejects it. There is no flag translation that
   preserves the vendor's intent, because the vendor compiler also carries T-Head-specific
   scheduling and extension support.
2. **`-mrvv-v0p10-compatible` targets the *draft* RVV 0.10 encoding**, not ratified RVV 1.0.
   The C908 implements RVV 1.0, but the shipped userspace is deliberately built in the
   compatibility mode. A mainline RVV-1.0 GCC produces a different, non-interchangeable ABI.
3. **`riscv64-embedded` is a bare-metal (`-elf`) cross, not `-linux-gnu`.** Wrong libc, wrong
   target triple, wrong sysroot model. `pkgsCross.riscv64-linux` would be the right *shape*, but
   see (1) and (2).

**Conclusion (inferred):** for the K230 Linux SDK there is no nixpkgs substitute. The vendor
compiler must be obtained and used as a binary.

## 2. The `/opt/toolchain` problem, and the three ways out

`BR2_TOOLCHAIN_EXTERNAL_PATH` is an **absolute path baked into a committed config file**. On a
normal distribution you untar the XuanTie release into `/opt/toolchain/` and it works. NixOS has
no `/opt`, and even if you create one, the toolchain binaries are dynamically linked against a
standard-FHS `ld-linux-x86-64.so.2` and glibc that do not exist at those paths.

| Route | What it is | Assessment |
|---|---|---|
| **A. Docker** | Canaan publishes `ghcr.io/kendryte/k230_sdk` and documents it as the supported build environment. `virtualisation.docker.enable = true;` and build inside. | **Recommended.** It is the vendor's own supported path, it sidesteps every FHS issue, and it is what LilyGO's wiki tells you to do on Windows too. The one cost is that the container is opaque and unpinned by digest in the vendor's instructions — pin it yourself. |
| **B. `buildFHSEnv`** | Wrap the whole Buildroot invocation in an FHS sandbox that provides `/opt/toolchain`, glibc, and the usual `/usr/lib` shape. | Workable and is the same pattern this repository already uses for [SquareLine Studio](README.md#5-squareline-studio). More work than Docker for a build that runs once. |
| **C. `autoPatchelfHook` + a store path** | `fetchurl` the XuanTie tarball, patch its ELF interpreters, then either symlink it to `/opt/toolchain/...` or override `BR2_TOOLCHAIN_EXTERNAL_PATH`. | The most "Nix-native" answer and the most fragile. Buildroot also wants a *writable* tree in places and will fight a read-only store path. |

**Whichever route you take, override the path rather than creating `/opt`.** Buildroot reads
the variable from `.config`, so `make BR2_TOOLCHAIN_EXTERNAL_PATH=... ` or a `defconfig` fragment
is cleaner than an impure filesystem mutation. *(Inferred — not executed.)*

## 3. The rest of the build is ordinary Buildroot, with ordinary Buildroot NixOS problems

Read from the same defconfig:

- The kernel is **not mainline**: `BR2_LINUX_KERNEL_CUSTOM_REPO_URL="https://github.com/ruyisdk/linux-xuantie-kernel.git"`
  pinned at commit `7d4e1f444f461dbe3833bd99a4640e7b6c2cd529`, defconfig `k230`.
- Buildroot **downloads during the build** (`BR2_DL_DIR="$(TOPDIR)/../../dl"`). A pure Nix
  derivation cannot do that. Either pre-populate `dl/` and run outside Nix, or accept an impure
  build. This is the standard Buildroot-on-Nix conflict and it is not K230-specific.
- Buildroot's own host tooling wants `/usr/bin/env`-style assumptions in a number of packages.
  `nix-shell -p` with the usual set (`git`, `gnumake`, `rsync`, `python3`, `bc`, `ncurses`,
  `perl`, `wget`, `cpio`, `unzip`, `file`, `which`, `openssl`) plus an FHS wrapper is the
  pragmatic combination.

**Host requirement stated by the vendors:** Canaan documents Ubuntu 20.04; LilyGO documents
Ubuntu 22.04 or 24.04 and runs `./scripts/setup_ubuntu.sh` to install host dependencies. That
script is `apt`-based and will not run on NixOS. Read it for the dependency list, then translate.

## 4. The other three toolchains this board needs

The K230 board is the extreme case where **one product needs four unrelated toolchains**. Only
one of them is a problem on NixOS.

| Target | Toolchain | NixOS status |
|---|---|---|
| K230 (RISC-V Linux) | XuanTie GCC + Buildroot | **Hard** — §2 above |
| nRF52840 companion | **PlatformIO**, `platform = nordicnrf52`, board `nrf52840_dk_adafruit` | **Fine.** `platformio` is present in the locked nixpkgs, and `platformio-core.udev` is already in this repository's `services.udev.packages`. |
| nRF9151 companion | **nRF Connect SDK v3.4.0** via `nrfutil sdk-manager` | **Mixed.** `nrfutil` is present in the locked nixpkgs. But `guides/nixos/README.md` §2 records `west` and `zephyr` as **absent** — and NCS *is* a Zephyr/west workspace. `nrfutil sdk-manager install --install-dir "$PWD/ncs" v3.4.0` downloads its own SDK and toolchain into a repository-relative directory, which is exactly the "downloaded binary toolchain" pattern from §2 and needs the same FHS treatment. |
| Flashing the SD image | `dd` | Trivial. |

The nRF9151 case is the interesting one because it **installs into `$PWD/ncs` rather than a
system path**, and honours `NCS_ROOT`. That is materially friendlier than `/opt/toolchain`: a
`buildFHSEnv` shell with a project-local `ncs/` directory is enough, with no path override
needed. *(Inferred from LilyGO's documented commands; not executed.)*

## 5. Device access

Nothing new is needed for the K230 itself — its normal workflow is **write an SD card and boot**,
plus SSH over Wi-Fi/Ethernet for iteration (`./scripts/deploy_launcher.sh <ip>`). No custom udev
rule, no vendor programmer.

The companions do need rules, and this repository already ships them:

- **nRF52840 UF2 bootloader** enumerates as USB **mass storage** — no udev rule required, but the
  device must be mountable by the user. Also enumerates as a USB CDC serial port for logs.
- **nRF52840 / nRF9151 serial** → `dialout` group, already configured.
- **PlatformIO** → `platformio-core.udev`, already in `services.udev.packages`.

## 6. What would make this verifiable

In order of value:

1. Run `./scripts/setup_ubuntu.sh` under `strace`/read it, and produce the exact host dependency
   list as a Nix package set.
2. Build once inside `ghcr.io/kendryte/k230_sdk` on this host and record the image digest.
3. Attempt route C (`autoPatchelfHook` on the XuanTie tarball) and record whether Buildroot's
   writability assumptions break it, and where.

None of the three were attempted on 2026-09-04.

## 7. Cross-references

- [`guides/nixos/README.md`](README.md) — the parent guide (ESP-IDF, PlatformIO, device access, package availability)
- [`components/canaan/k230`](../../components/canaan/k230/README.md) §14 — the toolchain facts, at the chip level
- [`devices/lilygo/t-display-k230/development.md`](../../devices/lilygo/t-display-k230/development.md) — the board's full build and flash procedure
