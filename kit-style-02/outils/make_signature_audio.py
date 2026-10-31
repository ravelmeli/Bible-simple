"""Fabrique les deux pistes de signature de la chaîne, sans droits (synthèse pure) : pulsation et jingle.

    python3 -I make_signature_audio.py --bpm 96 --duree 60 assets/audio/

- pulse.wav : tic de percussion doux à chaque temps, un peu plus marqué tous les 4 temps. Contenu surtout entre 1 et 7 kHz, pour rester
  audible sur un haut-parleur de téléphone. À mixer très bas (data-volume ≈ 0,07, environ 25 dB sous la voix).
- jingle.wav : carillon de deux notes (880 puis 1320 Hz), 0,9 s, identique à chaque vidéo. Volume conseillé 0,2.
"""
import argparse
import os
import wave

import numpy as np

SR = 44100


def write(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def tick(strong):
    n = int(SR * 0.09)
    t = np.arange(n) / SR
    rng = np.random.default_rng(3)
    noise = rng.standard_normal(n)
    # passe-haut simple (différence) pour garder les aigus
    noise = np.concatenate([[0], np.diff(noise)])
    env = np.exp(-t * 90)
    body = np.sin(2 * np.pi * (1500 if strong else 1100) * t) * np.exp(-t * 60)
    return (0.55 * noise * env + (0.9 if strong else 0.45) * body) * (1.0 if strong else 0.7)


def main(bpm, duree, out):
    n = int(SR * duree)
    x = np.zeros(n)
    beat = 60.0 / bpm
    k = 0
    while k * beat < duree - 0.1:
        t = tick(k % 4 == 0)
        i = int(k * beat * SR)
        j = min(n, i + len(t))
        x[i:j] += t[: j - i]
        k += 1
    x *= 0.7 / max(1e-9, np.abs(x).max())
    write(os.path.join(out, "pulse.wav"), x)
    # jingle : deux notes avec harmoniques et décroissance
    m = int(SR * 0.9)
    t = np.arange(m) / SR
    j = np.zeros(m)
    for f, d in ((880, 0.0), (1320, 0.16)):
        tt = np.clip(t - d, 0, None)
        env = (t >= d) * np.exp(-tt * 5.5) * np.minimum(1, tt * 400)
        j += env * (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.15 * np.sin(2 * np.pi * 3 * f * t))
    j *= 0.8 / np.abs(j).max()
    j *= np.minimum(1, (m - np.arange(m)) / (SR * 0.2))
    write(os.path.join(out, "jingle.wav"), j)
    print(f"{out}: pulse.wav ({bpm} BPM, {duree} s) et jingle.wav")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bpm", type=int, default=96)
    ap.add_argument("--duree", type=float, default=60)
    ap.add_argument("sortie")
    a = ap.parse_args()
    main(a.bpm, a.duree, a.sortie)
