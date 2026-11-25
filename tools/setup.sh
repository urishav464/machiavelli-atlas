#!/usr/bin/env bash
# One-time setup of the Python/Node tools used by the atlas pipeline.
# usage: bash tools/setup.sh
set -e
pip install -q --break-system-packages lxml shapely scipy pillow tifffile scikit-image pysheds affine pyproj 2>&1 | grep -v WARNING || true
CACHE=${ATLAS_CACHE:-$HOME/.atlas-cache}; mkdir -p "$CACHE"
if [ ! -f "$CACHE/leaflet/leaflet.js" ]; then
  (cd "$CACHE" && npm pack leaflet@1.9.4 -q >/dev/null 2>&1 && tar xzf leaflet-1.9.4.tgz && mkdir -p leaflet && cp package/dist/leaflet.js package/dist/leaflet.css leaflet/ && rm -rf package leaflet-1.9.4.tgz)
fi
echo "ready. cache: $CACHE"
