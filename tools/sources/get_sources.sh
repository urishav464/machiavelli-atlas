#!/usr/bin/env bash
# Downloads the primary sources and the Pleiades gazetteer into the cache.
# usage: bash tools/sources/get_sources.sh            (default set: Livy, Dionysius, Plutarch Romulus+Numa, Pleiades)
#        bash tools/sources/get_sources.sh lat phi0914.phi001 perseus-lat2     (any Perseus Latin work)
#        bash tools/sources/get_sources.sh grc tlg0007.tlg005 perseus-eng2     (any Perseus Greek work / translation)
# Only raw.githubusercontent.com is reachable from the container, so everything comes from GitHub mirrors.
set -e
C=${ATLAS_CACHE:-$HOME/.atlas-cache}/src; mkdir -p "$C"
L=https://raw.githubusercontent.com/PerseusDL/canonical-latinLit/master/data
G=https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data
get(){ # $1=lat|grc  $2=author.work  $3=edition
  local base=$L; [ "$1" = grc ] && base=$G
  local a=${2%%.*} w=${2#*.}
  local out="$C/$2.$3.xml"
  [ -s "$out" ] || curl -sf -o "$out" "$base/$a/$w/$2.$3.xml" && echo "$out"
}
if [ $# -ge 3 ]; then get "$1" "$2" "$3"; exit; fi
get lat phi0914.phi001 perseus-lat2   # Livy, Latin (Weissenborn-Mueller)
get lat phi0914.phi001 perseus-eng1   # Livy, English (check <editor>: Foster/Loeb or Roberts)
get lat phi0914.phi001 perseus-eng2
get lat phi0914.phi001 perseus-eng3
get grc tlg0081.tlg001 perseus-grc2   # Dionysius of Halicarnassus, Roman Antiquities, Greek
get grc tlg0007.tlg002 perseus-eng2   # Plutarch, Romulus (Perrin)
get grc tlg0007.tlg005 perseus-eng2   # Plutarch, Numa (Perrin)
P="$C/pleiades-places.csv"; [ -s "$P" ] || curl -sf -o "$P" https://raw.githubusercontent.com/isawnyu/pleiades.datasets/main/data/gis/places.csv && echo "$P"
