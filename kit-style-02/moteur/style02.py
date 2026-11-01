"""Style 02 « Explainer à autocollants » — moteur de montage réutilisable (HyperFrames, 9:16 ou 16:9).

Une grande toile (COLS × ROWS écrans) parcourue par une caméra continue. Chaque élément est calé sur la
transcription mot par mot (transcript.json : [{"text", "start", "end"}, ...]).

Utilisation type (voir exemple-esther/build.py) :

    import style02 as s
    s.setup(here=HERE, duration=62.4, cols=3, rows=5, theme=THEME)
    from style02 import *          # après setup : W, H, html, T(), sticker(), headline(), cam(), ...
    cam(0, (0, 0))
    sticker((0, 0), "objet", 50, 600, 640, 0.0, instant=True)
    ...
    build(chapters=[...], suppress=[...], endcard=..., endcard_t=...)

Le projet doit contenir : transcript.json, assets/voix.wav, assets/audio/music.wav (facultatif),
assets/audio/lib/*.mp3 (effets), assets/fonts/Inter.ttf, assets/stickers/*.png. Le gabarit est lu dans le
dossier de ce fichier (template.tpl) sauf si le projet a son propre template.tpl.
"""
import json
import os
import re

from PIL import Image

MOTEUR = os.path.dirname(os.path.abspath(__file__))

# Thème par défaut = celui de « La Bible Simple ». Pour une autre chaîne, ne changer que ces valeurs.
THEME_DEFAUT = {
    "brand": "La Bible Simple",       # signature en haut à gauche
    "title": "Video - style 02",      # <title> de la page
    "lang": "fr",
    "acc": "#F85830",                 # accent unique (mot surligné, chiffre clé, trait de caméra)
    "bg": "#E9EDF1",                  # toile claire
    "ink": "#1B242E",                 # texte, contours, mode sombre
    "grey": "#6B7785",                # sous-titres gris
    "grey2": "#8A97A6",               # gris en mode sombre, flèches
    "line": "#AEB8C3",                # bordure des références, côtes de la carte
    "tile": "#CBD3DC",                # cases éteintes des grilles
    "land": "#D3DAE2",                # terres de la carte
}

W, H, DUR = 1080, 1920, 60.0
COLS, ROWS = 3, 5
WORLD_W, WORLD_H = COLS * W, ROWS * H
HERE = os.getcwd()
ACC = THEME_DEFAUT["acc"]
INK = THEME_DEFAUT["ink"]
THEME = dict(THEME_DEFAUT)
words = []
html, tw, audio = [], [], []
CAM = []          # (temps, station | "all", échelle)
_uid = [0]
_dark = [None]    # instant du passage en mode sombre (barre de chapitres en clair)
STICKERS = []     # (id, instant d'apparition) : base du mouvement permanent
NODES = {}        # station -> ids des éléments posés (pour wipe)
ZOOM = [1.0]      # zoom par défaut des plans (cam sans échelle) ; avec XM/YM : recale les positions pour garder tout dans l'écran
XM = [None]       # (a, b) : x' = a + (x - 70) * b
YM = [None]       # (a, b) : y' = a + (y - 170) * b
BPM = [96]        # tempo de la pulsation (flottement des autocollants, piste assets/audio/pulse.wav)


def setup(here, duration, cols=3, rows=5, fmt="9:16", theme=None, transcript="transcript.json", bpm=96, zoom=1.0, xmap=None, ymap=None):
    """Prépare un projet. fmt : "9:16" (1080 × 1920) ou "16:9" (1920 × 1080)."""
    global W, H, DUR, COLS, ROWS, WORLD_W, WORLD_H, HERE, ACC, INK, THEME, words
    W, H = (1080, 1920) if fmt == "9:16" else (1920, 1080)
    DUR, COLS, ROWS, HERE = duration, cols, rows, here
    WORLD_W, WORLD_H = cols * W, rows * H
    THEME = dict(THEME_DEFAUT, **(theme or {}))
    ACC, INK = THEME["acc"], THEME["ink"]
    words = json.load(open(os.path.join(here, transcript)))
    del html[:], tw[:], audio[:], CAM[:], STICKERS[:]
    NODES.clear()
    _uid[0] = 0
    _dark[0] = None
    BPM[0] = bpm
    ZOOM[0], XM[0], YM[0] = zoom, xmap, ymap


# ---------------------------------------------------------------- calage sur la transcription
def norm(t):
    return re.sub(r"[\.,\?!:;«»“”\"'’()\u00a0\u202f ]", "", t).lower()


def T(word, n=0):
    """Début (s) de la n-ième occurrence (0 = première) du mot dans la transcription."""
    hits = [w for w in words if norm(w["text"]) == norm(word)]
    if len(hits) <= n:
        raise KeyError(f"mot introuvable dans transcript.json : {word!r} (occurrence {n})")
    return hits[n]["start"]


def uid():
    _uid[0] += 1
    return f"x{_uid[0]}"


def at(t):
    return f"{t:.3f}"


def tween(sel, frm, to, t):
    tw.append(f'tl.fromTo("{sel}", {{ {frm} }}, {{ {to} }}, {at(t)});')


def st(c, r):
    """Coordonnées sur la toile de la station (colonne c, rangée r) ; une station = un écran."""
    return c * W, r * H


# ---------------------------------------------------------------- primitives visuelles
def _tx(x):
    return round(XM[0][0] + (x - 70) * XM[0][1]) if XM[0] else x


def _ty(y):
    return round(YM[0][0] + (y - 170) * YM[0][1]) if YM[0] else y


def put(station, x, y, inner, cls="", style=""):
    sx, sy = st(*station)
    i = uid()
    html.append(f'<div class="node {cls}" id="{i}" style="left:{sx + _tx(x)}px;top:{sy + _ty(y)}px;{style}">{inner}</div>')
    NODES.setdefault(station, []).append(i)
    return i


def wipe(station, t, dur=0.35):
    """Efface (fondu) tout ce qui a été posé sur cette station jusqu'ici : permet de revenir sur un plan avec un état différent."""
    ids = NODES.get(station, [])
    if ids:
        sel = ", ".join(f"#{i}" for i in ids)
        tw.append(f'tl.to("{sel}", {{ opacity: 0, duration: {dur}, ease: "power1.in", immediateRender: false }}, {at(t)});')
    NODES[station] = []


def fade(i, t, dur=0.3):
    """Fait disparaître un élément posé (citation remplacée, étiquette qui a rempli son rôle)."""
    tw.append(f'tl.to("#{i}", {{ opacity: 0, duration: {dur}, ease: "power1.in", immediateRender: false }}, {at(t)});')


def blur_in(i, t, dy=24):
    """Entrée « défloutée » : opacité, montée et flou 14 px → 0 en 0,55 s."""
    tween(f"#{i}", f"opacity: 0, y: {dy}, filter: \"blur(14px)\"", 'opacity: 1, y: 0, filter: "blur(0px)", duration: 0.55, ease: "power3.out"', t)


def pop(i, t, rot=-3):
    tween(f"#{i}", f"opacity: 0, scale: 0.55, rotation: {rot - 8}", f'opacity: 1, scale: 1, rotation: {rot}, duration: 0.6, ease: "back.out(1.9)"', t)


def sticker(station, name, x, y, w, t, rot=-3, label=None, sub=None, lab_dx=0, lab_dy=0, side="right", instant=False):
    """Autocollant assets/stickers/<name>.png, largeur w px (hauteur calculée). instant=True : visible dès t (accroche)."""
    iw, ih = Image.open(os.path.join(HERE, "assets/stickers", name + ".png")).size
    h = round(ih * w / iw)
    i = put(station, x, y, f'<img src="assets/stickers/{name}.png" style="width:{w}px;height:{h}px" />', "sticker")
    STICKERS.append((i, max(t, 0.9) if instant else t + 0.7))
    if instant:
        tween(f"#{i}", f"opacity: 1, scale: 1.14, rotation: {rot - 3}", f'opacity: 1, scale: 1, rotation: {rot}, duration: 0.9, ease: "power3.out"', t)
    else:
        pop(i, t, rot)
        sfx("pop", t, 0.32)
    if label:
        lx = x + w + 30 if side == "right" else x - 330
        ly = y + h // 2 - 40 + lab_dy
        lx += lab_dx
        leader(station, (x + w * (0.85 if side == "right" else 0.15), y + h * 0.5), (lx if side == "right" else lx + 300, ly + 22), t + 0.1)
        label_box(station, lx, ly, label, sub, t + 0.15)
    return i, h


def leader(station, a, b, t):
    """Ligne fine qui se dessine de a vers b, avec un point d'accent au départ."""
    sx, sy = st(*station)
    i = uid()
    (x1, y1), (x2, y2) = (_tx(a[0]), _ty(a[1])), (_tx(b[0]), _ty(b[1]))
    ln = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5) + 2
    html.append(f'<svg class="node lead" id="{i}" style="left:{sx}px;top:{sy}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-dasharray="{ln}" />'
                f'<circle cx="{x1}" cy="{y1}" r="7" /></svg>')
    tween(f"#{i} line", f"strokeDashoffset: {ln}", 'strokeDashoffset: 0, duration: 0.4, ease: "power2.out"', t)
    tween(f"#{i} circle", "scale: 0, transformOrigin: \"50% 50%\"", 'scale: 1, duration: 0.25, ease: "back.out(3)"', t)


def label_box(station, x, y, title, sub, t, dark=False):
    """Étiquette : titre gras + sous-ligne grise, trait d'accent à gauche. dark=True sur fond sombre."""
    inner = f'<b>{title}</b>' + (f'<span>{sub}</span>' if sub else "")
    i = put(station, x, y, inner, "label dark" if dark else "label")
    blur_in(i, t, 10)
    sfx("click", t, 0.5)
    return i


def tag(station, x, y, text, t, cls="", size=44):
    """Bandeau qui s'ouvre de gauche à droite. cls : "" (blanc), "acc" (accent), "dark" (texte clair sans fond)."""
    i = put(station, x, y, text, f"tag {cls}", f"font-size:{size}px")
    tween(f"#{i}", "opacity: 0, scaleX: 0.2, transformOrigin: \"0% 50%\"", 'opacity: 1, scaleX: 1, duration: 0.35, ease: "power3.out"', t)
    return i


def ref(station, x, y, text, t):
    """Référence (source, verset, date) en petites capitales encadrées."""
    i = put(station, x, y, text, "ref")
    blur_in(i, t, 8)
    return i


def headline(station, y, lines, t, kicker=None, sub=None, size=96, x=70, dark=False, hl=None, hl_t=None):
    """Grand titre ; les mots entre [crochets] reçoivent un soulignement d'accent qui s'étire à hl_t."""
    parts = []
    for ln in lines:
        ln = re.sub(r"\[(.+?)\]", r'<em class="hl"><span>\1</span><i></i></em>', ln)
        parts.append(f"<div>{ln}</div>")
    k = f'<div class="kick"><i></i>{kicker}</div>' if kicker else ""
    s = f'<div class="sub">{sub}</div>' if sub else ""
    i = put(station, x, y, k + f'<div class="h" style="font-size:{size}px">' + "".join(parts) + "</div>" + s,
            "headline" + (" dark" if dark else ""), f"width:{W - 2 * x - 60}px")
    blur_in(i, t, 30)
    if hl_t is not None:
        tween(f"#{i} .hl i", "scaleX: 0", 'scaleX: 1, duration: 0.45, ease: "power3.out"', hl_t)
    return i


def counter(station, x, y, frm, to, t, dur, unit="", size=200, cls=""):
    """Compteur qui défile de frm à to (tic-tac si dur > 0,5 s). cls "dark" sur fond sombre."""
    i = put(station, x, y, f'<span class="num" id="{uid()}">{frm}</span><span class="unit">{unit}</span>', f"counter {cls}", f"font-size:{size}px")
    num = html[-1].split('class="num" id="')[1].split('"')[0]
    blur_in(i, t - 0.1, 16)
    tw.append(f'(function(){{ const o = {{ v: {frm} }}; const el = document.getElementById("{num}"); '
              f'tl.fromTo(o, {{ v: {frm} }}, {{ v: {to}, duration: {dur}, ease: "power2.out", '
              f'onUpdate: () => {{ el.textContent = Math.round(o.v); }} }}, {at(t)}); }})();')
    if dur > 0.5:
        sfx("tick", t, 0.25, min(dur, 1.5))
    return i


def boxes(station, x, y, labels, t, step=320, gap=0.42, cls="day", small="Jour"):
    """Cases qui passent du blanc à l'accent une par une (jours, étapes)."""
    for k, lab in enumerate(labels):
        d = put(station, x + k * step, y, f'<small>{small}</small>{lab}', cls)
        tween(f"#{d}", f'opacity: 0, y: 40, backgroundColor: "#FFFFFF", color: "{INK}"',
              f'opacity: 1, y: 0, backgroundColor: "{ACC}", color: "#FFFFFF", duration: 0.35, ease: "back.out(2)"', t + k * gap)
        sfx("click", t + k * gap, 0.7)


def bar_to_scale(station, x, base_y, height, t, width=140, acc=True, dur=0.9):
    """Barre verticale à l'échelle, qui pousse depuis sa base."""
    b = put(station, x, base_y - height, "", "bar acc" if acc else "bar", f"width:{width}px;height:{height}px")
    tween(f"#{b}", "scaleY: 0, transformOrigin: \"50% 100%\"", f'scaleY: 1, duration: {dur}, ease: "power3.out"', t)
    return b


def map_svg(station, x, y, map_json, t_show, t_draw, width=770, dot_step=0.022):
    """Carte construite par outils/make_map.py : terres, zone qui se trace, points un à un, lieux."""
    M = json.load(open(os.path.join(HERE, map_json)))
    sc = width / M["w"]
    mid = uid()
    land = "".join(f'<path class="land" d="{d}"/>' for d in M["land"])
    dots = "".join(f'<circle class="pdot" id="{mid}p{k}" cx="{px:.1f}" cy="{py:.1f}" r="7"/>' for k, (px, py) in enumerate(M["points"]))
    pl = "".join(f'<g class="place" id="{mid}{i}"><circle cx="{px:.1f}" cy="{py:.1f}" r="10"/><text x="{px + 16:.1f}" y="{py + 9:.1f}">{n}</text></g>'
                 for i, (n, (px, py)) in enumerate(M["places"].items()))
    zone = f'<path class="empire" id="{mid}e" d="{M["empire"]}"/>' if M.get("empire") else ""
    mi = put(station, x, y, f'<svg class="map" width="{width}" height="{round(M["h"] * sc)}" viewBox="0 0 {M["w"]} {M["h"]}">'
             f'{land}{zone}{dots}{pl}</svg>', "mapwrap")
    blur_in(mi, t_show, 14)
    if zone:
        tween(f"#{mid}e", "fillOpacity: 0, strokeDashoffset: 3000", 'fillOpacity: 1, strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut"', t_draw)
    for k in range(len(M["points"])):
        tween(f"#{mid}p{k}", "opacity: 0, scale: 0, transformOrigin: \"50% 50%\"", 'opacity: 1, scale: 1, duration: 0.18, ease: "back.out(3)"',
              t_draw + 0.4 + k * dot_step)
    for i in range(len(M["places"])):
        tween(f"#{mid}{i}", "opacity: 0", 'opacity: 1, duration: 0.3', t_draw + 0.2 + i * 0.25)
    return mi, len(M["points"])


# ---------------------------------------------------------------- éléments de rétention (bibliothèque réutilisable)
def stamp(station, x, y, text, t, rot=-6, size=64):
    """Tampon d'accent qui s'abat avec une secousse de caméra (« DÉTAIL ÉTONNANT », « HYPOTHÈSE »). Même geste d'une vidéo à l'autre."""
    i = put(station, x, y, text, "stamp", f"font-size:{size}px")
    tween(f"#{i}", f"opacity: 0, scale: 2.4, rotation: {rot + 14}", f'opacity: 1, scale: 1, rotation: {rot}, duration: 0.28, ease: "power4.in"', t)
    hit(t + 0.26, 1.0)
    tw.append(f'tl.fromTo("#drift", {{ x: 0 }}, {{ x: 9, duration: 0.04, yoyo: true, repeat: 5, ease: "none", immediateRender: false }}, {at(t + 0.26)});')
    tw.append(f'tl.set("#drift", {{ x: 0 }}, {at(t + 0.52)});')
    return i


def burst(station, x, y, t, n=12, r0=70, r1=150):
    """Rafale de traits d'accent autour d'un point (mot-clé prononcé)."""
    import math
    sx, sy = st(*station)
    i = uid()
    lines = "".join(f'<line x1="{200 + r0 * math.cos(a):.1f}" y1="{200 + r0 * math.sin(a):.1f}" x2="{200 + r1 * math.cos(a):.1f}" y2="{200 + r1 * math.sin(a):.1f}" />'
                    for a in (k * 2 * math.pi / n for k in range(n)))
    html.append(f'<svg class="node burst" id="{i}" style="left:{sx + _tx(x) - 200}px;top:{sy + _ty(y) - 200}px;opacity:0" width="400" height="400" viewBox="0 0 400 400">{lines}</svg>')
    tween(f"#{i}", 'opacity: 1, scale: 0.35, transformOrigin: "50% 50%"', 'opacity: 0, scale: 1.3, duration: 0.55, ease: "power2.out"', t)
    return i


def ring(station, x, y, t, size=240):
    """Anneau d'accent qui se dilate puis disparaît (nom prononcé, chiffre qui tombe)."""
    i = put(station, x - size // 2, y - size // 2, "", "ring", f"width:{size}px;height:{size}px;opacity:0")
    tween(f"#{i}", 'opacity: 1, scale: 0.25', 'opacity: 0, scale: 1.5, duration: 0.7, ease: "power2.out"', t)
    return i


def arrow(station, a, b, t):
    """Flèche d'accent qui se dessine de a vers b (relie deux éléments)."""
    import math
    sx, sy = st(*station)
    i = uid()
    (x1, y1), (x2, y2) = (_tx(a[0]), _ty(a[1])), (_tx(b[0]), _ty(b[1]))
    ln = int(math.hypot(x2 - x1, y2 - y1)) + 2
    ang = math.atan2(y2 - y1, x2 - x1)
    hx = [(x2 - 30 * math.cos(ang - 0.45), y2 - 30 * math.sin(ang - 0.45)), (x2, y2), (x2 - 30 * math.cos(ang + 0.45), y2 - 30 * math.sin(ang + 0.45))]
    html.append(f'<svg class="node arrow" id="{i}" style="left:{sx}px;top:{sy}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-dasharray="{ln}" />'
                f'<polyline class="hd" points="{" ".join(f"{px:.0f},{py:.0f}" for px, py in hx)}" /></svg>')
    tween(f"#{i} line", f"strokeDashoffset: {ln}", 'strokeDashoffset: 0, duration: 0.4, ease: "power2.out"', t)
    tween(f"#{i} .hd", "opacity: 0", 'opacity: 1, duration: 0.15', t + 0.35)
    return i


def teaser(station, x, y, text, t, hold=2.6):
    """Puce « boucle ouverte » (« Attends le détail final ») : promet une suite réelle de la vidéo, disparaît après hold secondes."""
    i = put(station, x, y, f'<b></b>{text}', "teaser")
    blur_in(i, t, 10)
    tween(f"#{i} b", "scale: 0.6", 'scale: 1.3, duration: 0.4, yoyo: true, repeat: 5, ease: "sine.inOut"', t)
    tw.append(f'tl.to("#{i}", {{ opacity: 0, duration: 0.3 }}, {at(t + hold)});')
    sfx("click", t, 0.4)
    return i


def dark_mode(t):
    """Passage au fond sombre (révélation) : la toile s'assombrit et la barre de chapitres passe en clair."""
    tween("#darkbg", "opacity: 0", 'opacity: 1, duration: 0.6, ease: "power2.inOut"', t)
    _dark[0] = t


# ---------------------------------------------------------------- son
# Effets de la bibliothèque HyperFrames copiés dans assets/audio/lib/ (licence Pixabay), avec leur durée utile.
LIB = {"whoosh": ("assets/audio/lib/whoosh-short.mp3", 0.57), "click": ("assets/audio/lib/click-soft.mp3", 0.37),
       "pop": ("assets/audio/lib/pop.mp3", 0.72), "bass": ("assets/audio/lib/impact-bass-2.mp3", 2.0),
       "tick": ("assets/audio/lib/typing.mp3", 1.5), "spark": ("assets/audio/lib/sparkle.mp3", 1.2)}
# Volumes de base (data-volume) : chaque effet environ 10 dB sous la voix.
BASE = {"whoosh": 0.10, "click": 0.22, "pop": 0.28, "bass": 0.07, "tick": 0.12, "spark": 0.06}


def sfx(kind, t, k=1.0, dur=None):
    path, d = LIB[kind]
    d = min(dur or d, DUR - t)
    audio.append((f"a{len(audio)}", path, round(t, 3), round(d, 3), round(BASE[kind] * k, 3)))


def hit(t, k=1.0):
    """Temps fort : impact grave + « pop » par-dessus, pour rester audible sur un haut-parleur de téléphone."""
    sfx("bass", t, k)
    sfx("pop", t, 1.4 * k)


# ---------------------------------------------------------------- caméra
def cam(t, station, scale=1.0):
    """À t, la caméra rejoint la station (ou "all" : vue d'ensemble de toute la toile)."""
    if station != "all" and scale == 1.0:
        scale = ZOOM[0]
    CAM.append((t, station, scale))


def cam_xy(station, scale):
    if station == "all":
        s = min(W / WORLD_W, H / WORLD_H) * 0.92
        return (W - WORLD_W * s) / 2, (H - WORLD_H * s) / 2, s
    sx, sy = st(*station)
    return W / 2 - (sx + W / 2) * scale, H / 2 - (sy + H / 2) * scale, scale


def _camera(drift=1.035, retention=False):
    cam_tw, route_html = [], []
    x0, y0, s0 = cam_xy(CAM[0][1], 1.0)
    cam_tw.append(f'tl.set("#world", {{ x: {x0:.1f}, y: {y0:.1f}, scale: {s0} }}, 0);')
    if retention:
        cam_tw.append(f'tl.set("#plx", {{ x: {x0 * 0.3:.1f}, y: {y0 * 0.3:.1f} }}, 0);')
    for k, (t, stn, sc) in enumerate(CAM):
        x, y, s = cam_xy(stn, sc)
        move = 0.95 if stn == "all" else 0.75
        if k:
            px, py, ps = cam_xy(CAM[k - 1][1], CAM[k - 1][2])
            cam_tw.append(f'tl.fromTo("#world", {{ x: {px:.1f}, y: {py:.1f}, scale: {ps:.4f} }}, '
                          f'{{ x: {x:.1f}, y: {y:.1f}, scale: {s:.4f}, duration: {move}, ease: "power3.inOut", immediateRender: false }}, {at(t)});')
            blur = 2 if "all" in (stn, CAM[k - 1][1]) else 5
            cam_tw.append(f'tl.fromTo("#world", {{ filter: "blur(0px)" }}, {{ filter: "blur({blur}px)", duration: {move / 2}, yoyo: true, repeat: 1, ease: "power2.in", immediateRender: false }}, {at(t)});')
            sfx("whoosh", t, 0.9)
            if retention:
                cam_tw.append(f'tl.fromTo("#plx", {{ x: {px * 0.3:.1f}, y: {py * 0.3:.1f} }}, {{ x: {x * 0.3:.1f}, y: {y * 0.3:.1f}, duration: {move}, ease: "power3.inOut", immediateRender: false }}, {at(t)});')
                cam_tw.append(f'tl.fromTo("#sweep", {{ x: 0, opacity: 1 }}, {{ x: {int(W * 1.9)}, opacity: 1, duration: {move + 0.15:.2f}, ease: "power2.inOut", immediateRender: false }}, {at(t)});')
                cam_tw.append(f'tl.set("#sweep", {{ opacity: 0 }}, {at(t + move + 0.17)});')
            # Trait d'accent tiré de la station précédente à la suivante pendant le déplacement.
            prev = CAM[k - 1][1] if CAM[k - 1][1] != "all" else (CAM[k - 2][1] if k >= 2 else None)
            if stn != "all" and prev not in (None, "all"):
                (ax, ay), (bx, by) = st(*prev), st(*stn)
                ax, ay, bx, by = ax + W / 2, ay + H * 0.62, bx + W / 2, by + H * 0.62
                ln = int(((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5) + 2
                rid = uid()
                route_html.append(f'<svg class="node route" id="{rid}" style="left:0;top:0" width="{WORLD_W}" height="{WORLD_H}" viewBox="0 0 {WORLD_W} {WORLD_H}">'
                                  f'<line x1="{ax:.0f}" y1="{ay:.0f}" x2="{bx:.0f}" y2="{by:.0f}" stroke-dasharray="{ln}"/>'
                                  f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="16"/></svg>')
                cam_tw.append(f'tl.fromTo("#{rid} line", {{ strokeDashoffset: {ln} }}, {{ strokeDashoffset: 0, duration: {move}, ease: "power3.inOut" }}, {at(t)});')
                cam_tw.append(f'tl.fromTo("#{rid} circle", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.3, ease: "back.out(3)" }}, {at(t + move * 0.8)});')
                cam_tw.append(f'tl.to("#{rid}", {{ opacity: 0, duration: 0.5 }}, {at(t + move + 0.3)});')
        # Lente dérive (zoom 1 → 1,035) pendant qu'on reste sur une station.
        end = CAM[k + 1][0] if k + 1 < len(CAM) else DUR
        hold_from = t + (move if k else 0)
        if end - hold_from > 0.4:
            cam_tw.append(f'tl.fromTo("#drift", {{ scale: 1 }}, {{ scale: {drift}, duration: {end - hold_from:.2f}, ease: "none", immediateRender: false }}, {at(hold_from)});')
    return cam_tw, route_html


# ---------------------------------------------------------------- carte de fin
def _hl(text):
    return re.sub(r"\[(.+?)\]", r'<em class="hl"><span>\1</span><i></i></em>', text)


def _endcard(card, t):
    """card = {"kicker", "title" (lignes séparées par <br />, [mot] surligné), "button", "stickers": [(nom, left, top, largeur, rotation), ...]}"""
    imgs = []
    for k, (name, left, top, w, rot) in enumerate(card.get("stickers", [])):
        iw, ih = Image.open(os.path.join(HERE, "assets/stickers", name + ".png")).size
        imgs.append(f'        <img class="es" id="es{k + 1}" src="assets/stickers/{name}.png" style="left:{left}px;top:{top}px;width:{w}px;height:{round(ih * w / iw)}px;transform:rotate({rot}deg)" />')
    out = ('<div id="endcard">\n'
           f'        <div class="kick">{card["kicker"]}</div>\n'
           f'        <div class="h">{_hl(card["title"])}</div>\n'
           f'        <div class="sub2">{card["button"]}</div>\n' + "".join(i + "\n" for i in imgs) + "      </div>\n")
    tw.append(f'tl.fromTo("#world", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.4, ease: "power1.in", immediateRender: false }}, {at(t - 0.1)});')
    tw.append(f'tl.fromTo("#chrome", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.3, immediateRender: false }}, {at(t - 0.5)});')
    tw.append(f'tl.fromTo("#endcard", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {at(t)});')
    tw.append(f'tl.fromTo("#endcard .h", {{ y: 40, filter: "blur(12px)" }}, {{ y: 0, filter: "blur(0px)", duration: 0.6, ease: "power3.out" }}, {at(t + 0.05)});')
    tw.append(f'tl.fromTo("#endcard .hl i", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "power3.out" }}, {at(t + 0.5)});')
    if imgs:
        sel = ", ".join(f"#es{k + 1}" for k in range(len(imgs)))
        tw.append(f'tl.fromTo("{sel}", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: "back.out(1.6)", stagger: 0.12 }}, {at(t + 0.25)});')
    tw.append(f'tl.fromTo("#endcard .sub2", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }}, {at(t + 0.7)});')
    tw.append(f'tl.fromTo("#endcard .sub2", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.4, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, {at(t + 1.2)});')
    hit(t + 0.7, 0.5)
    return out


# ---------------------------------------------------------------- assemblage
def _rgb(hexa):
    h = hexa.lstrip("#")
    return ", ".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def build(chapters, suppress=(), endcard=None, endcard_t=None, music_volume=0.15, max_words=4, out="index.html",
          retention=False, pulse_volume=0.07, jingle_volume=0.12):
    """Assemble index.html.
    retention=True : mouvement permanent (autocollants qui flottent au tempo BPM), fond en parallaxe, poussière, balayage à chaque
    changement de plan, pop des mots, zoom lent 1,06, piste de pulsation et jingle (assets/audio/pulse.wav, jingle.wav).
    chapters : [("01", "Libellé", début, fin), ...] ; suppress : intervalles sans sous-titres (citation affichée, fin) ;
    endcard / endcard_t : carte de fin et son instant d'apparition (voir _endcard)."""
    cam_tw, route_html = _camera(1.06 if retention else 1.035, retention)
    card_html = _endcard(endcard, endcard_t) if endcard else ""

    # Barre de chapitres, avec progression.
    chap_html = "".join(f'<div class="ch" id="ch{k}"><b>{n}</b> {lab}<i></i></div>' for k, (n, lab, a, b) in enumerate(chapters))
    for k, (n, lab, a, b) in enumerate(chapters):
        tw.append(f'tl.fromTo("#ch{k} i", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {b - a:.2f}, ease: "none", immediateRender: {"true" if k == 0 else "false"} }}, {at(a)});')
        tw.append(f'tl.fromTo("#ch{k}", {{ opacity: 0.45 }}, {{ opacity: 1, duration: 0.2, immediateRender: {"true" if k == 0 else "false"} }}, {at(a)});')
        if k + 1 < len(chapters):
            tw.append(f'tl.to("#ch{k}", {{ opacity: 0.45, duration: 0.2 }}, {at(b)});')
    if _dark[0] is not None:
        tw.append(f'tl.fromTo("#chrome", {{ color: "{INK}" }}, {{ color: "{THEME["bg"]}", duration: 0.6 }}, {at(_dark[0])});')

    # Sous-titres : groupes de max_words mots, mot prononcé en couleur d'accent.
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if w["text"].rstrip().endswith((".", "?", "!", ",", ":")) or len(cur) == max_words:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    caps = []
    for n, ch in enumerate(chunks):
        s = ch[0]["start"]
        nxt = chunks[n + 1][0]["start"] if n + 1 < len(chunks) else DUR
        e = min(max(ch[-1]["end"] + 0.22, s + 0.55), nxt)
        if any(a - 0.05 <= s and ch[-1]["end"] <= b + 0.35 for a, b in suppress):
            continue
        spans = " ".join(f'<span class="cw" id="w{n}_{k}">{w["text"]}</span>' for k, w in enumerate(ch))
        caps.append(f'<p class="clip cap" id="cap{n}" data-start="{s:.3f}" data-duration="{e - s:.3f}"><span class="capin" id="ci{n}">{spans}</span></p>')
        tw.append(f'tl.fromTo("#ci{n}", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }}, {at(s)});')
        for k, w in enumerate(ch):
            tw.append(f'tl.fromTo("#w{n}_{k}", {{ color: "{INK}" }}, {{ color: "{ACC}", duration: 0.08 }}, {at(w["start"])});')
            tw.append(f'tl.to("#w{n}_{k}", {{ color: "{INK}", duration: 0.12 }}, {at(max(w["end"], w["start"] + 0.16))});')


    plx_html = dust_html = sweep_html = ""
    if retention:
        import random
        rnd = random.Random(7)
        beat = 60.0 / BPM[0]
        period = 4 * beat
        # mouvement permanent : chaque autocollant flotte et s'incline au tempo, tant que la vidéo dure
        for n, (sid, t0) in enumerate(STICKERS):
            half = period / 2
            reps = int((DUR - t0) / half) - 1
            if reps >= 1:
                sgn = 1 if n % 2 == 0 else -1
                tw.append(f'tl.fromTo("#{sid} img", {{ y: 0, rotation: {-1.2 * sgn} }}, {{ y: -10, rotation: {1.2 * sgn}, duration: {half:.3f}, ease: "sine.inOut", yoyo: true, repeat: {reps}, immediateRender: false }}, {at(t0)});')
        # poussière flottante (écran fixe, derrière les éléments)
        dots = []
        for k in range(26):
            d = rnd.uniform(9, 17)
            x0 = rnd.randint(30, W - 30)
            r = rnd.choice([4, 5, 6, 8])
            op = rnd.choice([0.14, 0.2, 0.28])
            col = ACC if k % 3 == 0 else INK
            dots.append(f'<i id="du{k}" style="left:{x0}px;top:0;width:{r * 2}px;height:{r * 2}px;background:{col};opacity:{op}"></i>')
            y0 = rnd.randint(0, H)
            first = d * (y0 + 40) / (H + 70)
            tw.append(f'tl.fromTo("#du{k}", {{ y: {y0} }}, {{ y: -40, duration: {first:.2f}, ease: "none", immediateRender: true }}, 0);')
            reps = int(DUR / d) + 1
            tw.append(f'tl.fromTo("#du{k}", {{ y: {H + 30} }}, {{ y: -40, duration: {d:.2f}, ease: "none", repeat: {reps}, immediateRender: false }}, {at(first)});')
            tw.append(f'tl.fromTo("#du{k}", {{ x: -14 }}, {{ x: 14, duration: {d / 3:.2f}, ease: "sine.inOut", yoyo: true, repeat: {reps * 3 + 1}, immediateRender: false }}, 0);')
        dust_html = '<div id="dust">' + "".join(dots) + '</div>'
        plx_html = '<div id="plx"></div>'
        sweep_html = '<div id="sweep"></div>'
        # pop des mots : chaque mot prononcé claque légèrement
        for n, ch in enumerate(chunks):
            for k, w in enumerate(ch):
                if any(f'id="w{n}_{k}"' in c for c in caps):
                    tw.append(f'tl.fromTo("#w{n}_{k}", {{ scale: 1.07 }}, {{ scale: 1, duration: 0.2, ease: "back.out(2)", immediateRender: false }}, {at(w["start"])});')
        # pistes de signature : pulsation au tempo, jingle d'ouverture
        if os.path.exists(os.path.join(HERE, "assets/audio/pulse.wav")):
            audio.insert(0, ("pulse", "assets/audio/pulse.wav", 0, DUR, pulse_volume))
        if os.path.exists(os.path.join(HERE, "assets/audio/jingle.wav")):
            audio.insert(0, ("jingle", "assets/audio/jingle.wav", 0, 1.2, jingle_volume))
    if music_volume and os.path.exists(os.path.join(HERE, "assets/audio/music.wav")):
        audio.insert(0, ("music", "assets/audio/music.wav", 0, DUR, music_volume))
    audio_html = "\n      ".join(f'<audio id="{a}" src="{p}" data-start="{s}" data-duration="{d}" data-volume="{v}"></audio>' for a, p, s, d, v in audio)
    tpl_path = os.path.join(HERE, "template.tpl")
    tpl = open(tpl_path if os.path.exists(tpl_path) else os.path.join(MOTEUR, "template.tpl")).read()
    th = THEME
    for key, val in [("{{ACC_RGB}}", _rgb(th["acc"])), ("{{INK_RGB}}", _rgb(th["ink"])), ("{{ACC}}", th["acc"]), ("{{BG}}", th["bg"]),
                     ("{{INK}}", th["ink"]), ("{{GREY2}}", th["grey2"]), ("{{GREY}}", th["grey"]), ("{{LINE}}", th["line"]),
                     ("{{TILE}}", th["tile"]), ("{{LAND}}", th["land"]), ("{{LANG}}", th["lang"]), ("{{TITLE}}", th["title"]),
                     ("{{BRAND}}", th["brand"]), ("{{ACC_HEX}}", th["acc"].lstrip("#")),
                     ("{{PLX_W}}", str(int(W + WORLD_W * 0.3 + 600))), ("{{PLX_H}}", str(int(H + WORLD_H * 0.3 + 600)))]:
        tpl = tpl.replace(key, val)
    if W != 1080:
        tpl = tpl.replace('content="width=1080, height=1920"', f'content="width={W}, height={H}"').replace(
            'data-width="1080" data-height="1920"', f'data-width="{W}" data-height="{H}"')
        # 16:9 : sous-titres plus haut et plus larges, barre de chapitres plus large (zones sûres d'une vidéo longue).
        tpl = tpl.replace("left: 60px;\n        top: 1440px;\n        width: 820px;", "left: 260px;\n        top: 880px;\n        width: 1400px;")
        tpl = tpl.replace("top: 160px; width: 870px;", "top: 60px; width: 1200px;")
    page = (tpl.replace("{{PLX}}", plx_html).replace("{{DUST}}", dust_html).replace("{{SWEEP}}", sweep_html).replace("{{WORLD}}", "\n        ".join(route_html + html)).replace("{{WORLD_W}}", str(WORLD_W)).replace("{{WORLD_H}}", str(WORLD_H))
            .replace("{{CHAPTERS}}", chap_html).replace("{{CAPTIONS}}", "\n      ".join(caps)).replace("{{DURATION}}", str(DUR))
            .replace("      {{ENDCARD}}\n", "      " + card_html if card_html else "")
            .replace("{{AUDIO}}", f'<audio id="voix" src="assets/voix.wav" data-start="0" data-duration="{DUR}" data-volume="1"></audio>\n      ' + audio_html)
            .replace("{{TWEENS}}", "\n      ".join(cam_tw + tw)))
    open(os.path.join(HERE, out), "w").write(page)
    print(f"nodes {len(html)}  tweens {len(cam_tw) + len(tw)}  captions {len(caps)}  audio {len(audio) + 1}  camera stops {len(CAM)}")
