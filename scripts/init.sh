#!/usr/bin/env bash
# Point this repository's archive/ and scratch/ symlinks at the sibling artifact archive.
#
# Run after cloning, or any time the archive is added, moved or renamed:
#
#     ./scripts/init.sh
#
# You usually do not need to. The symlinks are committed in relative form
# (../repo-archive/hardware-doc and ../repo-archive/scratch/hardware-doc), so a fresh
# clone already works if the archive sits beside this repo:
#
#     <parent>/
#     |- hardware-doc/     <- this repository
#     \- repo-archive/     <- artifacts (own repo, usually unpublished)
#
# This script matters when the archive is somewhere else, or when this repo is checked
# out as a linked worktree whose parent is not the archive's parent.
#
# It never clones and never deletes. Absent archive is fine: the symlinks stay in their
# committed relative form and simply dangle, and every *.ARCHIVED.md placeholder still
# carries hashes and recovery URLs.
set -uo pipefail

c_g=$'\033[32m'; c_y=$'\033[33m'; c_d=$'\033[2m'; c_0=$'\033[0m'
[ -t 1 ] || { c_g=; c_y=; c_d=; c_0=; }
ok()   { printf '%s✓%s %s\n' "$c_g" "$c_0" "$*"; }
warn() { printf '%s!%s %s\n' "$c_y" "$c_0" "$*" >&2; }
dim()  { printf '%s%s%s\n' "$c_d" "$*" "$c_0"; }

command -v git >/dev/null || { echo "git not found" >&2; exit 1; }

# Real repository root: --git-common-dir, not --show-toplevel, so a linked worktree
# resolves to the main checkout's parent rather than its own.
COMMON="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)" \
  || { echo "not inside a git repository" >&2; exit 1; }
ROOT="$(dirname "$COMMON")"
WORKTREE="$(git rev-parse --show-toplevel)"
NAME="$(basename "$ROOT")"

ARCHIVE_ROOT="${REPO_ARCHIVE_ROOT:-$(dirname "$ROOT")/repo-archive}"
ART="$ARCHIVE_ROOT/$NAME"
SCR="$ARCHIVE_ROOT/scratch/$NAME"

dim "repo   : $ROOT"
dim "archive: $ARCHIVE_ROOT"

if [ ! -d "$ARCHIVE_ROOT" ]; then
  warn "no archive at $ARCHIVE_ROOT — leaving symlinks as committed"
  dim "  Placeholders (*.ARCHIVED.md) carry hashes and recovery URLs, so the"
  dim "  archive is optional. Clone or move it beside this repo and re-run."
  exit 0
fi

# rel <link-path> <target> : shortest relative target, so the result stays portable
rel() { python3 -c 'import os,sys;print(os.path.relpath(sys.argv[2],os.path.dirname(sys.argv[1])))' "$1" "$2"; }

link() {
  local name="$1" target="$2" path="$WORKTREE/$1"

  if [ ! -d "$target" ]; then
    warn "$name: $target does not exist — not touching the link"
    return
  fi
  if [ -e "$path" ] && [ ! -L "$path" ]; then
    warn "$name exists and is not a symlink — refusing to replace it"
    return
  fi

  # Prefer the relative form; fall back to absolute only if it cannot reach.
  local want; want="$(rel "$path" "$target")"
  ln -sfn "$want" "$path"
  if [ "$(cd "$path" 2>/dev/null && pwd -P)" != "$(cd "$target" && pwd -P)" ]; then
    ln -sfn "$target" "$path"
  fi

  if [ "$(cd "$path" 2>/dev/null && pwd -P)" = "$(cd "$target" && pwd -P)" ]; then
    ok "$name -> $(readlink "$path")"
  else
    warn "$name -> $(readlink "$path")  (does not resolve)"
    return
  fi

  # If the link now differs from what HEAD records, say so rather than hiding it.
  # .gitignore cannot suppress a tracked path; only --skip-worktree can, and doing
  # that silently is how a stale committed target survives unnoticed.
  if git -C "$WORKTREE" ls-files --error-unmatch "$name" >/dev/null 2>&1 \
     && ! git -C "$WORKTREE" diff --quiet -- "$name" 2>/dev/null; then
    warn "  $name differs from its committed value"
    dim  "    committed: $(git -C "$WORKTREE" show ":$name" 2>/dev/null)"
    dim  "    on disk:   $(readlink "$path")"
    dim  "    If the new value is right for everyone: git add $name"
    dim  "    If it is local to this checkout only:   git update-index --skip-worktree $name"
  fi
}

link archive "$ART"
link scratch "$SCR"

dim ""
dim "Both links point into the same repository ($ARCHIVE_ROOT), which is namespaced"
dim "per source repo. From either one, 'git add -A' stages the whole archive;"
dim "'git add .' stages only the directory you are standing in."
