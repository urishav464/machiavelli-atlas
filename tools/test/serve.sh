#!/usr/bin/env bash
# Local test copy of the site: same index.html, but Leaflet from the cache (cdnjs is blocked in the container).
# usage: bash tools/test/serve.sh  -> http://localhost:8765/test.html
set -e
R=$(cd "$(dirname "$0")/../.." && pwd); C=${ATLAS_CACHE:-$HOME/.atlas-cache}; S=$C/site; mkdir -p "$S"
for d in t tl ovl; do ln -sfn "$R/$d" "$S/$d"; done
cp "$C/leaflet/leaflet.js" "$S/leaflet.js"
sed 's#https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js#leaflet.js#' "$R/index.html" > "$S/test.html"
pkill -f "http.server 8765" 2>/dev/null || true; sleep 0.5
(cd "$S" && nohup python3 -m http.server 8765 >/dev/null 2>&1 &)
sleep 1; echo "http://localhost:8765/test.html"
