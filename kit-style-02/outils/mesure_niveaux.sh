#!/usr/bin/env bash
# Mesure le niveau (LUFS intégré) d'un fichier, éventuellement découpé et atténué comme dans le montage.
#   bash mesure_niveaux.sh assets/voix.wav                     → voix seule (viser environ -19 LUFS)
#   bash mesure_niveaux.sh assets/audio/music.wav 0 30 0.15    → musique telle que mixée (viser 13 à 15 dB sous la voix)
#   bash mesure_niveaux.sh assets/audio/lib/pop.mp3 0 0.72 0.28 → un effet tel que mixé (viser environ 10 dB sous la voix)
# Le rendu HyperFrames semble normaliser le total : comparer le mix final à la voix seule ne prouve rien.
f="$1"; start="${2:-0}"; dur="${3:-9999}"; vol="${4:-1}"
ffmpeg -nostats -hide_banner -i "$f" -af "atrim=start=$start:duration=$dur,volume=$vol,ebur128=framelog=quiet" -f null - 2>&1 | grep -E "^\s+I:" | head -1
