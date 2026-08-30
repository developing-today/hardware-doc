#!/usr/bin/env bash
#
# restore-demo-deps.sh — rebuild the two vendored dependencies that were removed from
# Waveshare's ESP32-S3-Knob-Touch-LCD-1.8 demo tree, from upstream sources.
#
#   * LVGL      8.4.0  -> <dest>/Arduino/libraries/lvgl
#   * SensorLib 0.3.1  -> <dest>/ESP-IDF/03_DRV2605_Test/components/SensorLib
#
# Both are unmodified upstream releases apart from one one-line Waveshare patch each.
# The patches live in ../artifacts/vendored-deps/patches/ and are applied here.
#
# The result is verified byte-for-byte against content digests recorded in
# ../artifacts/vendored-deps/README.md.  See ./README.md for full documentation.
#
# Dependencies: bash, curl, unzip, patch, sha256sum, find, sort.  Nothing exotic.
#
set -euo pipefail

# ---------------------------------------------------------------------------
# Pinned facts.  Do not edit without re-deriving the tree digests.
# ---------------------------------------------------------------------------

LVGL_VERSION="8.4.0"
LVGL_TAG="v8.4.0"
LVGL_URL="https://github.com/lvgl/lvgl/archive/refs/tags/${LVGL_TAG}.zip"
LVGL_ZIP_SHA256="28ff0b5b1e544f83b670533cd9bdf193df5c2260687af8a8ca48b737c937ca9f"
LVGL_TOPDIR="lvgl-${LVGL_VERSION}"
LVGL_TREE_SHA256="a5e84c30a760f8fecf68b3a2ea98386b11db95acf06af125876f4e51f634c47e"
LVGL_FILES=1355
LVGL_BYTES=160828075

SLIB_VERSION="0.3.1"
SLIB_TAG="v0.3.1"
SLIB_URL="https://github.com/lewisxhe/SensorLib/archive/refs/tags/${SLIB_TAG}.zip"
SLIB_ZIP_SHA256="99234b9296af8b5504aa6e3cf9828c93f25dde7ec852de4c42b82fad8ef7f808"
SLIB_TOPDIR="SensorLib-${SLIB_VERSION}"
SLIB_TREE_SHA256="a60fd281a66a027b0eefc37384c743125a23ff8dfc06b7436dd879b877ff1608"
SLIB_TREE_SHA256_NODOCS="2e5060efad5e2dfbb2fafd8bc0ddd33ef980895670480deb0d1efac31d30e6f6"
SLIB_FILES=302
SLIB_BYTES=43501941

# LVGL dotfiles/dirs that Waveshare's packaging stripped.  Removing them is required
# to reproduce the recorded digest.
LVGL_STRIP=(
  ".codecov.yml"
  ".editorconfig"
  ".github"
  ".gitignore"
  ".pre-commit-config.yaml"
  "scripts/.gitignore"
  "tests/.gitignore"
)

# SensorLib datasheets renamed from Chinese filenames to portable ASCII.
# Format: "<upstream name>|<ascii name>"
SLIB_RENAMES=(
  "CHSC5816触控芯片使用说明V1-20221114.pdf|CHSC5816-touch-controller-datasheet-v1-20221114.pdf"
  "海栎创触摸芯片移植手册-v3.5-20220701(1).pdf|hynitron-touch-driver-guide-v3.5-20220701.pdf"
  "环境光与接近传感器应用与选型.pdf|ambient-light-and-proximity-sensor-selection.pdf"
)

# ---------------------------------------------------------------------------
# Plumbing
# ---------------------------------------------------------------------------

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DEVICE_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
PATCH_DIR="${DEVICE_DIR}/artifacts/vendored-deps/patches"
REPO_DEMO_TREE="${DEVICE_DIR}/artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo"

DEST=""
CACHE_DIR="${KNOB_DEPS_CACHE:-${TMPDIR:-/tmp}/knob-demo-deps-cache}"
FORCE=0
WANT_DATASHEETS=1
ALLOW_ZIP_DRIFT=0
ONLY=""

RED=''
GRN=''
YEL=''
BLD=''
RST=''
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  RED=$'\033[31m'
  GRN=$'\033[32m'
  YEL=$'\033[33m'
  BLD=$'\033[1m'
  RST=$'\033[0m'
fi

# Progress messages go to stderr so helper functions can return values on stdout.
say() { printf '%s\n' "$*"; }
info() { printf '  %s\n' "$*" >&2; }
ok() { printf '  %sOK%s   %s\n' "$GRN" "$RST" "$*" >&2; }
warn() { printf '  %sWARN%s %s\n' "$YEL" "$RST" "$*" >&2; }
die() {
  printf '\n%sFATAL:%s %s\n' "$RED$BLD" "$RST" "$*" >&2
  exit 1
}
hdr() { printf '\n%s==> %s%s\n' "$BLD" "$*" "$RST"; }

usage() {
  cat <<'USAGE'
restore-demo-deps.sh — restore LVGL 8.4.0 and SensorLib 0.3.1 into a copy of the
Waveshare ESP32-S3-Knob-Touch-LCD-1.8 demo tree.

USAGE
  restore-demo-deps.sh --dest <demo-tree-root >[options]

  <demo-tree-root >is the directory that contains Arduino/ and ESP-IDF/ — i.e. a copy of
  ESP32-S3-Knob-Touch-LCD-1.8-Demo/. It is created if it does not exist.

  OPTIONS
  --dest DIR Where to install. Required.
  --only lvgl | sensorlib
  Restore only one of the two dependencies.
  --no-datasheets Skip SensorLib's datasheet/ directory (17.9 MiB of PDFs that
                       have no effect on the build).  Verified against a separate
                       code-only digest.
    --force            Replace an existing tree even if it does not verify.
    --cache DIR        Download cache directory.
                       Default: $KNOB_DEPS_CACHE or $TMPDIR/knob-demo-deps-cache
    --allow-zip-drift  Do not abort if the GitHub source archive hash differs from the
                       recorded one.  GitHub auto-generated tag archives are NOT
                       guaranteed byte-stable; the authoritative check is the extracted
                       tree digest, which is still enforced.
    -h, --help         This message.

The script is idempotent: if a target tree already exists and matches its recorded
digest, it is left alone.

It refuses to write into this repository's own artifacts/demo/ tree, which is
  deliberately kept without these dependencies.
  USAGE
}

while [ $# -gt 0 ]; do
  case "$1" in
  --dest)
    DEST="${2:?--dest needs a value}"
    shift 2
    ;;
  --only)
    ONLY="${2:?--only needs a value}"
    shift 2
    ;;
  --cache)
    CACHE_DIR="${2:?--cache needs a value}"
    shift 2
    ;;
  --no-datasheets)
    WANT_DATASHEETS=0
    shift
    ;;
  --force)
    FORCE=1
    shift
    ;;
  --allow-zip-drift)
    ALLOW_ZIP_DRIFT=1
    shift
    ;;
  -h | --help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    die "unknown argument: $1"
    ;;
  esac
done

[ -n "$DEST" ] || {
  usage >&2
  die "--dest is required"
}
case "$ONLY" in "" | lvgl | sensorlib) ;; *) die "--only must be 'lvgl' or 'sensorlib'" ;; esac

for tool in curl unzip patch sha256sum find sort; do
  command -v "$tool" >/dev/null 2>&1 || die "required tool not found: $tool"
done

mkdir -p -- "$DEST"
DEST="$(cd -- "$DEST" && pwd)"

# Guard: never restore into the committed demo tree.
if [ "$DEST" = "$REPO_DEMO_TREE" ] || case "$DEST" in "$REPO_DEMO_TREE"/*) true ;; *) false ;; esac then
  die "refusing to write into the repository's own demo tree:
    $REPO_DEMO_TREE
  That tree is deliberately kept WITHOUT these dependencies; they are reproducible and
  are not committed.  Copy it somewhere else and point --dest at the copy:

    cp -a '$REPO_DEMO_TREE' /tmp/knob-demo
    '$0' --dest /tmp/knob-demo"
fi

mkdir -p -- "$CACHE_DIR"

# tree_digest <parent-dir> <tree-name> [<exclude-glob-relative-to-parent>]
# Recipe (matches artifacts/vendored-deps/README.md):
#   cd <parent>; find <name> -type f -exec sha256sum {} + | sort -k2 | sha256sum
tree_digest() {
  local parent="$1" name="$2" excl="${3:-}"
  if [ -n "$excl" ]; then
    (cd -- "$parent" && find "$name" -type f ! -path "$excl" -exec sha256sum {} + |
      LC_ALL=C sort -k2 | sha256sum | cut -d' ' -f1)
  else
    (cd -- "$parent" && find "$name" -type f -exec sha256sum {} + |
      LC_ALL=C sort -k2 | sha256sum | cut -d' ' -f1)
  fi
}
tree_files() { (cd -- "$1" && find "$2" -type f | wc -l | tr -d ' '); }
tree_bytes() { (cd -- "$1" && find "$2" -type f -exec cat {} + | wc -c | tr -d ' '); }

# fetch <url> <sha256> <cache-filename> <label>
fetch() {
  local url="$1" want="$2" out="$CACHE_DIR/$3" label="$4" got
  if [ -f "$out" ]; then
    got="$(sha256sum "$out" | cut -d' ' -f1)"
    if [ "$got" = "$want" ]; then
      ok "$label archive already cached and verified ($out)"
      printf '%s' "$out"
      return 0
    fi
    warn "$label cached archive failed verification; re-downloading"
    rm -f -- "$out"
  fi
  info "downloading $label from $url"
  curl -fSL --no-progress-meter --retry 3 --retry-delay 2 -o "$out.part" "$url" ||
    die "download failed: $url"
  mv -f -- "$out.part" "$out"
  got="$(sha256sum "$out" | cut -d' ' -f1)"
  if [ "$got" != "$want" ]; then
    if [ "$ALLOW_ZIP_DRIFT" -eq 1 ]; then
      warn "$label archive hash drift (expected $want, got $got) — continuing because --allow-zip-drift was given; the tree digest check still applies"
    else
      die "$label source archive hash mismatch.
    url      : $url
    expected : $want
    actual   : $got
  GitHub's auto-generated tag archives are not guaranteed byte-stable over time, so
  this may be recompression rather than tampering.  The authoritative check is the
  extracted tree digest.  To proceed and rely on that instead:
      $0 --dest '$DEST' --allow-zip-drift
  Or use the byte-pinned git source:
      git clone $(printf '%s' "$url" | sed 's|/archive/refs/tags/.*|.git|') && git -C \$(basename \$_ .git) checkout ${label}"
    fi
  else
    ok "$label archive sha256 verified ($want)"
  fi
  printf '%s' "$out"
}

# verify_or_report <parent> <name> <want-digest> <want-files> <want-bytes> <label>
verify_tree() {
  local parent="$1" name="$2" wd="$3" wf="$4" wb="$5" label="$6"
  local gd gf gb
  gd="$(tree_digest "$parent" "$name" "${7:-}")"
  gf="$(tree_files "$parent" "$name")"
  gb="$(tree_bytes "$parent" "$name")"
  if [ "$gd" = "$wd" ]; then
    ok "$label tree digest $gd"
    info "   $gf files, $gb bytes"
    return 0
  fi
  warn "$label tree digest MISMATCH"
  warn "   expected $wd  ($wf files, $wb bytes)"
  warn "   actual   $gd  ($gf files, $gb bytes)"
  return 1
}

CHANGED=0

# ---------------------------------------------------------------------------
# LVGL
# ---------------------------------------------------------------------------
restore_lvgl() {
  local parent="$DEST/Arduino/libraries"
  local target="$parent/lvgl"

  hdr "LVGL ${LVGL_VERSION} -> Arduino/libraries/lvgl"

  if [ -d "$target" ] && [ ! -f "$target/lvgl.h" ]; then
    info "existing $target/ is not an LVGL install (no lvgl.h) — treating as a stub and replacing"
    rm -rf -- "$target"
  fi

  if [ -d "$target" ] && [ "$FORCE" -eq 0 ]; then
    if verify_tree "$parent" "lvgl" "$LVGL_TREE_SHA256" "$LVGL_FILES" "$LVGL_BYTES" "LVGL"; then
      info "already present and verified — nothing to do"
      return 0
    fi
    die "an LVGL tree already exists at
    $target
  but it does not match the recorded digest.  Re-run with --force to replace it."
  fi

  local zip
  zip="$(fetch "$LVGL_URL" "$LVGL_ZIP_SHA256" "lvgl-${LVGL_TAG}.zip" "$LVGL_TAG")"

  local work
  work="$(mktemp -d "${TMPDIR:-/tmp}/lvgl-restore.XXXXXX")"
  # shellcheck disable=SC2064
  trap "rm -rf -- '$work'" RETURN

  info "extracting"
  unzip -qq "$zip" -d "$work"
  [ -d "$work/$LVGL_TOPDIR" ] || die "expected '$LVGL_TOPDIR/' inside $zip"
  local src="$work/$LVGL_TOPDIR"

  info "stripping ${#LVGL_STRIP[@]} packaging dotfiles Waveshare removed"
  local p
  for p in "${LVGL_STRIP[@]}"; do rm -rf -- "${src:?}/$p"; done

  info "duplicating demos/ -> src/demos/ (Arduino only compiles sources under src/)"
  rm -rf -- "$src/src/demos"
  cp -a -- "$src/demos" "$src/src/demos"

  info "applying lvgl-8.4.0-waveshare.patch (even flush-row height for rotated ST77916)"
  patch -p1 -s -d "$src" <"$PATCH_DIR/lvgl-8.4.0-waveshare.patch" ||
    die "failed to apply lvgl-8.4.0-waveshare.patch"

  info "installing"
  mkdir -p -- "$parent"
  rm -rf -- "$target"
  mv -- "$src" "$target"

  verify_tree "$parent" "lvgl" "$LVGL_TREE_SHA256" "$LVGL_FILES" "$LVGL_BYTES" "LVGL" ||
    die "restored LVGL tree does not match the recorded digest — refusing to claim success"
  CHANGED=1
}

# ---------------------------------------------------------------------------
# SensorLib
# ---------------------------------------------------------------------------
restore_sensorlib() {
  local parent="$DEST/ESP-IDF/03_DRV2605_Test/components"
  local target="$parent/SensorLib"
  local want_digest want_files want_bytes excl=""
  if [ "$WANT_DATASHEETS" -eq 1 ]; then
    want_digest="$SLIB_TREE_SHA256"
    want_files="$SLIB_FILES"
    want_bytes="$SLIB_BYTES"
  else
    want_digest="$SLIB_TREE_SHA256_NODOCS"
    want_files="287"
    want_bytes="25301012"
    excl="SensorLib/datasheet/*"
  fi

  hdr "SensorLib ${SLIB_VERSION} -> ESP-IDF/03_DRV2605_Test/components/SensorLib"

  # The committed demo tree keeps three orphaned datasheet PDFs at this path (they have
  # mangled CP437 filenames and were left behind when the library was archived).  A
  # SensorLib directory with no src/ is such a stub, not an install.
  if [ -d "$target" ] && [ ! -d "$target/src" ]; then
    info "existing $target/ is not a SensorLib install (no src/) — treating as a stub and replacing"
    rm -rf -- "$target"
  fi

  if [ -d "$target" ] && [ "$FORCE" -eq 0 ]; then
    if verify_tree "$parent" "SensorLib" "$want_digest" "$want_files" "$want_bytes" "SensorLib" "$excl"; then
      info "already present and verified — nothing to do"
      return 0
    fi
    die "a SensorLib tree already exists at
    $target
  but it does not match the recorded digest.  Re-run with --force to replace it."
  fi

  local zip
  zip="$(fetch "$SLIB_URL" "$SLIB_ZIP_SHA256" "sensorlib-${SLIB_TAG}.zip" "$SLIB_TAG")"

  local work
  work="$(mktemp -d "${TMPDIR:-/tmp}/sensorlib-restore.XXXXXX")"
  # shellcheck disable=SC2064
  trap "rm -rf -- '$work'" RETURN

  info "extracting"
  unzip -qq "$zip" -d "$work"
  [ -d "$work/$SLIB_TOPDIR" ] || die "expected '$SLIB_TOPDIR/' inside $zip"
  local src="$work/$SLIB_TOPDIR"

  info "applying sensorlib-0.3.1-waveshare.patch (#include <cmath> in SensorQMI8658.hpp)"
  patch -p1 -s -d "$src" <"$PATCH_DIR/sensorlib-0.3.1-waveshare.patch" ||
    die "failed to apply sensorlib-0.3.1-waveshare.patch"

  if [ "$WANT_DATASHEETS" -eq 1 ]; then
    info "renaming 3 datasheets from Chinese filenames to portable ASCII"
    local r from to
    for r in "${SLIB_RENAMES[@]}"; do
      from="${r%%|*}"
      to="${r##*|}"
      if [ -f "$src/datasheet/$from" ]; then
        mv -- "$src/datasheet/$from" "$src/datasheet/$to"
      elif [ -f "$src/datasheet/$to" ]; then
        : # already renamed
      else
        die "expected datasheet not found: $from
  (upstream SensorLib $SLIB_TAG layout changed, or your filesystem mangled the name)"
      fi
    done
  else
    info "dropping datasheet/ (--no-datasheets)"
    rm -rf -- "$src/datasheet"
  fi

  info "installing"
  mkdir -p -- "$parent"
  rm -rf -- "$target"
  mv -- "$src" "$target"

  verify_tree "$parent" "SensorLib" "$want_digest" "$want_files" "$want_bytes" "SensorLib" "$excl" ||
    die "restored SensorLib tree does not match the recorded digest — refusing to claim success"
  CHANGED=1
}

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

say "${BLD}restore-demo-deps.sh${RST}"
info "dest  : $DEST"
info "cache : $CACHE_DIR"
info "patches: $PATCH_DIR"

[ -d "$PATCH_DIR" ] || die "patch directory not found: $PATCH_DIR"

[ "$ONLY" = "sensorlib" ] || restore_lvgl
[ "$ONLY" = "lvgl" ] || restore_sensorlib

hdr "lv_conf.h"
LVCONF="$DEST/Arduino/libraries/lv_conf.h"
if [ -f "$LVCONF" ]; then
  ok "present at Arduino/libraries/lv_conf.h ($(wc -c <"$LVCONF" | tr -d ' ') bytes)"
  info "This is Waveshare's board-specific LVGL config.  It lives OUTSIDE the lvgl/"
  info "directory on purpose and is NOT restored by this script — it is committed."
else
  warn "Arduino/libraries/lv_conf.h is MISSING from your destination tree."
  warn "LVGL will not build for this board without it.  Copy it from the repository:"
  warn "    cp '$REPO_DEMO_TREE/Arduino/libraries/lv_conf.h' '$LVCONF'"
fi

hdr "Result"
if [ "$CHANGED" -eq 1 ]; then
  say "  Dependencies restored and verified against the digests recorded in"
  say "  artifacts/vendored-deps/README.md."
else
  say "  Nothing changed; everything was already present and verified."
fi
say ""
say "  Next: see ../getting-started.md for Arduino and ESP-IDF build instructions."
say ""
