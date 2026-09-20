#!/usr/bin/env bash
# Re-acquire every upstream source for the Tanmatsu research tree.
#
# Clones all repositories at their PINNED commits and fetches the badge.team and
# solder.party documentation pages. Idempotent: existing clones are checked out
# to the pinned commit rather than re-cloned.
#
# Usage:  tools/fetch_sources.sh [workdir]     (default: ./_sources)
# Then:   tools/htmltext.py page.html > page.txt   to regenerate text snapshots
#
# Written 2026-08-24 after a /tmp cleanup destroyed the original clones.
set -euo pipefail
WORK="${1:-$(cd "$(dirname "$0")/.." && pwd)/_sources}"
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
mkdir -p "$WORK"; cd "$WORK"

clone() { # repo_url  commit  dir
  local url="$1" commit="$2" dir="$3"
  if [ ! -d "$dir/.git" ]; then git clone --quiet "$url" "$dir"; fi
  git -C "$dir" fetch --quiet origin "$commit" 2>/dev/null || git -C "$dir" fetch --quiet origin
  git -C "$dir" checkout --quiet "$commit"
  printf '%-42s %s\n' "$dir" "$(git -C "$dir" log -1 --format='%h %ad' --date=short)"
}

echo "=== Nicolai Electronics (pinned) ==="
clone https://github.com/Nicolai-Electronics/tanmatsu-hardware.git                 640805dd4304f4bfaac24965f8eecf81bec97bf1 tanmatsu-hardware
clone https://github.com/Nicolai-Electronics/tanmatsu-documentation.git            bd3ded51548433bd7d614f5607b7d36f5eed61fa tanmatsu-documentation
clone https://github.com/Nicolai-Electronics/tanmatsu-mechanical.git               c623cd548c9cafb95773624fe775001984449a89 tanmatsu-mechanical
clone https://github.com/Nicolai-Electronics/tanmatsu-coprocessor-firmware.git     57ff2505d7256b55cc5fea4eb9be10a9a077bafa tanmatsu-coprocessor-firmware
clone https://github.com/Nicolai-Electronics/esp32-component-tanmatsu-coprocessor.git 6eea3735346ee1b689898c77e500fb1d0c4e024e esp32-component-tanmatsu-coprocessor
clone https://github.com/Nicolai-Electronics/esp32-component-tanmatsu-wifi.git     d8ce0bf106141d6bccf4cb9a927bd494facc31af esp32-component-tanmatsu-wifi
clone https://github.com/Nicolai-Electronics/tanmatsu-radio.git                    cb4e38c02aa8ad533fd17b24921c4ca4848eeaf6 tanmatsu-radio
clone https://github.com/Nicolai-Electronics/tanmatsu-launcher.git                 20022fce316d768a1ff966b973ee2127511713f5 tanmatsu-launcher
clone https://github.com/Nicolai-Electronics/tanmatsu-template.git                 907fb9657658995efab210b754f28a3ace06d03a tanmatsu-template
clone https://github.com/Nicolai-Electronics/app-repository.git                    f83e1559553497903c083525a10d2aaf53344377 app-repository

echo "=== ecosystem ==="
clone https://github.com/badgeteam/esp32-component-badge-bsp.git 9037f0e badge-bsp || \
  git clone --quiet --depth 1 https://github.com/badgeteam/esp32-component-badge-bsp.git badge-bsp
clone https://github.com/solderparty/i2c_puppet.git f085518 i2c_puppet || \
  git clone --quiet --depth 1 https://github.com/solderparty/i2c_puppet.git i2c_puppet

echo "=== expansion boards, front panels, keypad library ==="
# NOTE: badgeteam/konsool-expansion-template is an EMPTY repo (no commits) - skipped.
for r in badgeteam/konsool-zero badgeteam/konsool-18650-expansion \
         badgeteam/konsool-template-lvgl \
         Nicolai-Electronics/tanmatsu-frontpanel-cyberdeck \
         Nicolai-Electronics/tanmatsu-frontpanel-honeycomb \
         solderparty/keebdeck_keyboard_hw solderparty/keebdeck_basic_hw; do
  d=$(basename "$r")
  [ -d "$d/.git" ] || git clone --quiet --depth 1 "https://github.com/$r.git" "$d" || true
  [ -d "$d/.git" ] && printf '%-38s %s\n' "$d" "$(git -C "$d" log -1 --format='%h %ad' --date=short)"
done

echo "=== badge.team Konsool docs (enumerate via sitemap) ==="
mkdir -p badge-team-html && cd badge-team-html
curl -sSL -A "$UA" https://badge.team/sitemap.xml -o sitemap.xml
grep -o '<loc>[^<]*</loc>' sitemap.xml | sed 's/<[^>]*>//g' | grep -i konsool | sort > urls.txt
while read -r u; do
  n=$(echo "$u" | sed 's|/docs/badges/konsool/||; s|/$||; s|/|_|g'); [ -z "$n" ] && n=index
  curl -sSL -A "$UA" -o "$n.html" "https://badge.team$u"
done < urls.txt
echo "  $(ls *.html | wc -l) pages"
cd ..

echo "=== solder.party product docs ==="
mkdir -p solder-party-html && cd solder-party-html
for p in bbq20kbd keyboard-pmod keyboard-featherwing/rev1 keyboard-featherwing/rev2 \
         keebdeck/keyboard keebdeck/basic rp2350-stamp-xl; do
  curl -sSL -A "$UA" -o "$(echo "$p" | tr / _).html" "https://www.solder.party/docs/$p/"
done
echo "  $(ls *.html | wc -l) pages"
cd ..

echo
echo "Done. Sources in: $WORK"
echo "Archive them outside the repo so a /tmp or worktree clean cannot destroy them:"
echo "  cp -a \"$WORK\" ../repo-archive/scratch/tanmatsu/sources"
