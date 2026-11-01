"""Voix off avec l'API Gemini TTS, par blocs de lignes, assemblée en un seul WAV.

    export GOOGLE_API_KEY=...        # jamais écrite dans un fichier ni dans git
    python3 -I tts_gemini.py script.md assets/voix.wav --voix Koda --lignes 6

- Le style se donne dans le texte, sous la forme « # Style: ... / # Transcript », sinon la voix lit la consigne à voix haute.
  Ce modèle refuse systemInstruction (« Developer instruction is not enabled »).
- Les mots à prononcer autrement s'écrivent dans un fichier JSON (--prononciation) : {"ḥokhmah": "khokhma"}. Le script d'origine reste intact.
- Chaque bloc est vérifié : durée plausible (0,22 à 0,6 s par mot), nouvel essai sinon.
- Sortie : WAV mono 24 kHz, blocs séparés par 0,35 s de silence. Les blocs sont gardés dans <sortie>.blocs/ ; --refaire 3,5 ne régénère que ceux-là.
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.request
import wave

MODELE = "gemini-3.8-flash-tts"
STYLE = "Narration — commanding, rich vocal modulation, dramatic pauses. Warm documentary narrator, natural French."


def appel(cle, texte, voix, modele):
    corps = {"contents": [{"parts": [{"text": texte}]}],
             "generationConfig": {"responseModalities": ["AUDIO"],
                                  "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voix}}}}}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{modele}:generateContent",
                                 data=json.dumps(corps).encode(), headers={"x-goog-api-key": cle, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.load(r)
    return base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])


def main(script, sortie, voix, lignes, style, prono, modele, refaire=None):
    """refaire : numéros de blocs (1, 2, ...) à régénérer ; les autres sont repris du dossier <sortie>.blocs/."""
    cle = os.environ["GOOGLE_API_KEY"]
    dossier = sortie + ".blocs"
    os.makedirs(dossier, exist_ok=True)
    rempl = json.load(open(prono)) if prono else {}
    L = [l for l in open(script).read().split("\n") if l.strip()]
    blocs = [L[i:i + lignes] for i in range(0, len(L), lignes)]
    morceaux = []
    for n, b in enumerate(blocs):
        txt = " ".join(b)
        for a, c in rempl.items():
            txt = txt.replace(a, c)
        mots = len(txt.split())
        tmp = os.path.join(dossier, f"bloc{n + 1:02d}.wav")
        if refaire is not None and (n + 1) not in refaire and os.path.exists(tmp):
            morceaux.append(tmp)
            continue
        for essai in range(4):
            try:
                raw = appel(cle, f"# Style: {style}\n# Transcript\n{txt}", voix, modele)
            except Exception as e:  # noqa: BLE001
                print(f"bloc {n + 1}: erreur {e}", file=sys.stderr)
                continue
            open(tmp, "wb").write(raw)
            with wave.open(tmp) as w:
                dur = w.getnframes() / w.getframerate()
            print(f"bloc {n + 1}/{len(blocs)} : {mots} mots, {dur:.1f} s ({dur / mots:.2f} s/mot)")
            if 0.22 <= dur / mots <= 0.6:
                morceaux.append(tmp)
                break
        else:
            sys.exit(f"bloc {n + 1} : échec")
    # assemblage avec 0,35 s de silence
    liste = []
    for k, m in enumerate(morceaux):
        liste.append(m)
        if k + 1 < len(morceaux):
            sil = f"{sortie}.sil.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "0.35", sil], check=True)
            liste.append(sil)
    lst = f"{sortie}.liste.txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in liste))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-ar", "24000", "-ac", "1", sortie], check=True)
    for x in (f"{sortie}.sil.wav", lst):
        if os.path.exists(x):
            os.remove(x)
    print("écrit :", sortie)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("sortie")
    ap.add_argument("--voix", default="Koda")
    ap.add_argument("--lignes", type=int, default=6)
    ap.add_argument("--style", default=STYLE)
    ap.add_argument("--prononciation")
    ap.add_argument("--modele", default=MODELE)
    ap.add_argument("--refaire", help="blocs à régénérer, ex. 3,5 (les autres sont repris)")
    a = ap.parse_args()
    r = [int(x) for x in a.refaire.split(",")] if a.refaire else None
    main(a.script, a.sortie, a.voix, a.lignes, a.style, a.prononciation, a.modele, r)
