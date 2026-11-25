#!/usr/bin/env bash
# Elevation (SRTM, CGIAR v4.1, 3 arc-sec ~90 m, 5x5 degree tiles) and water bodies (ASTER WBD, 1 arc-sec, 1x1 degree).
# Only GitHub is reachable from the container, so both come from public GitHub mirrors:
#   SRTM: github.com/acasadoalonso/SGP-2D-Live-Tracking (branch oldver, folder hgt/) -- has tiles for parts of Europe only.
#   WBD:  github.com/NiciusB/is-on-water (Git LFS -> media.githubusercontent.com).
# CGIAR tile name for a point: srtm_XX_YY, XX = floor((lon+180)/5)+1, YY = floor((60-lat)/5)+1.  Rome = srtm_39_04.
# usage: bash tools/terrain/get_dem.sh srtm_39_04 N41E012 N42E012
# If a tile is missing from the mirror: search GitHub code (gh api -X GET search/code -f q="filename:srtm_XX_YY")
# and report to Uri rather than inventing terrain.
set -e
C=${ATLAS_CACHE:-$HOME/.atlas-cache}/dem; mkdir -p "$C/wbd"
for t in "$@"; do
  case $t in
    srtm_*) for e in tif tfw; do f="$C/$t.$e"; [ -s "$f" ] || curl -sf -o "$f" "https://raw.githubusercontent.com/acasadoalonso/SGP-2D-Live-Tracking/oldver/hgt/$t.$e"; done; ls -la "$C/$t.tif";;
    N*|S*) z="$C/ASTWBDV001_$t.zip"; [ -s "$z" ] || curl -sfL -o "$z" "https://media.githubusercontent.com/media/NiciusB/is-on-water/main/dataset/ASTWBDV001_$t.zip"; unzip -o -q "$z" -d "$C/wbd"; ls "$C/wbd" | grep "$t";;
  esac
done
