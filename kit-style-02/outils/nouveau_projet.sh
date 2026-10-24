#!/usr/bin/env bash
# Crée un projet style 02 prêt à monter : bash outils/nouveau_projet.sh ../montage/mon-short
# Copie l'exemple (build.py à réécrire), la police Inter, les effets sonores de la bibliothèque HyperFrames.
set -euo pipefail
KIT="$(cd "$(dirname "$0")/.." && pwd)"
DST="$1"
mkdir -p "$DST"/assets/{source,stickers,fonts,audio/lib} "$DST"/renders
cp "$KIT/exemple-esther/build.py" "$DST/build.py"
sed -i "s#os.path.join(HERE, \"..\", \"moteur\")#\"$KIT/moteur\"#" "$DST/build.py"
cp "$KIT/exemple-esther/assets/fonts/"* "$DST/assets/fonts/"
# Effets : bibliothèque intégrée à HyperFrames (installée par « npx skills add heygen-com/hyperframes »), licence Pixabay.
SFX="$(git -C "$KIT" rev-parse --show-toplevel 2>/dev/null)/.agents/skills/media-use/audio/assets/sfx"
[ -d "$SFX" ] || SFX="$KIT/exemple-esther/assets/audio/lib"
for f in whoosh-short click-soft pop impact-bass-2 typing sparkle; do cp "$SFX/$f.mp3" "$DST/assets/audio/lib/"; done
echo "Projet prêt : $DST"
echo "À fournir : $DST/assets/voix.wav, $DST/transcript.json, $DST/assets/stickers/*.png, (facultatif) $DST/assets/audio/music.wav"
