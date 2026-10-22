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


def setup(here, duration, cols=3, rows=5, fmt="9:16", theme=None, transcript="transcript.json"):
    """Prépare un projet. fmt : "9:16" (1080 × 1920) ou "16:9" (1920 × 1080)."""
    global W, H, DUR, COLS, ROWS, WORLD_W, WORLD_H, HERE, ACC, INK, THEME, words
    W, H = (1080, 1920) if fmt == "9:16" else (1920, 1080)
    DUR, COLS, ROWS, HERE = duration, cols, rows, here
    WORLD_W, WORLD_H = cols * W, rows * H
    THEME = dict(THEME_DEFAUT, **(theme or {}))
    ACC, INK = THEME["acc"], THEME["ink"]
    words = json.load(open(os.path.join(here, transcript)))
    del html[:], tw[:], audio[:], CAM[:]
    _uid[0] = 0
    _dark[0] = None


# ---------------------------------------------------------------- calage sur la transcription
def norm(t):
    return re.sub(r"[\.,\?!:;«»\"'’()\u00a0\u202f ]", "", t).lower()


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
def put(station, x, y, inner, cls="", style=""):
    sx, sy = st(*station)
    i = uid()
    html.append(f'<div class="node {cls}" id="{i}" style="left:{sx + x}px;top:{sy + y}px;{style}">{inner}</div>')
    return i


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
    (x1, y1), (x2, y2) = a, b
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
    CAM.append((t, station, scale))


def cam_xy(station, scale):
    if station == "all":
        s = min(W / WORLD_W, H / WORLD_H) * 0.92
        return (W - WORLD_W * s) / 2, (H - WORLD_H * s) / 2, s
    sx, sy = st(*station)
    return W / 2 - (sx + W / 2) * scale, H / 2 - (sy + H / 2) * scale, scale


def _camera():
    cam_tw, route_html = [], []
    x0, y0, s0 = cam_xy(CAM[0][1], 1.0)
    cam_tw.append(f'tl.set("#world", {{ x: {x0:.1f}, y: {y0:.1f}, scale: {s0} }}, 0);')
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
            cam_tw.append(f'tl.fromTo("#drift", {{ scale: 1 }}, {{ scale: 1.035, duration: {end - hold_from:.2f}, ease: "none", immediateRender: false }}, {at(hold_from)});')
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


def build(chapters, suppress=(), endcard=None, endcard_t=None, music_volume=0.15, max_words=4, out="index.html"):
    """Assemble index.html.
    chapters : [("01", "Libellé", début, fin), ...] ; suppress : intervalles sans sous-titres (citation affichée, fin) ;
    endcard / endcard_t : carte de fin et son instant d'apparition (voir _endcard)."""
    cam_tw, route_html = _camera()
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

    if music_volume and os.path.exists(os.path.join(HERE, "assets/audio/music.wav")):
        audio.insert(0, ("music", "assets/audio/music.wav", 0, DUR, music_volume))
    audio_html = "\n      ".join(f'<audio id="{a}" src="{p}" data-start="{s}" data-duration="{d}" data-volume="{v}"></audio>' for a, p, s, d, v in audio)
    tpl_path = os.path.join(HERE, "template.tpl")
    tpl = open(tpl_path if os.path.exists(tpl_path) else os.path.join(MOTEUR, "template.tpl")).read()
    th = THEME
    for key, val in [("{{ACC_RGB}}", _rgb(th["acc"])), ("{{INK_RGB}}", _rgb(th["ink"])), ("{{ACC}}", th["acc"]), ("{{BG}}", th["bg"]),
                     ("{{INK}}", th["ink"]), ("{{GREY2}}", th["grey2"]), ("{{GREY}}", th["grey"]), ("{{LINE}}", th["line"]),
                     ("{{TILE}}", th["tile"]), ("{{LAND}}", th["land"]), ("{{LANG}}", th["lang"]), ("{{TITLE}}", th["title"]),
                     ("{{BRAND}}", th["brand"])]:
        tpl = tpl.replace(key, val)
    if W != 1080:
        tpl = tpl.replace('content="width=1080, height=1920"', f'content="width={W}, height={H}"').replace(
            'data-width="1080" data-height="1920"', f'data-width="{W}" data-height="{H}"')
        # 16:9 : sous-titres plus haut et plus larges, barre de chapitres plus large (zones sûres d'une vidéo longue).
        tpl = tpl.replace("left: 60px;\n        top: 1440px;\n        width: 820px;", "left: 260px;\n        top: 880px;\n        width: 1400px;")
        tpl = tpl.replace("top: 160px; width: 870px;", "top: 60px; width: 1200px;")
    page = (tpl.replace("{{WORLD}}", "\n        ".join(route_html + html)).replace("{{WORLD_W}}", str(WORLD_W)).replace("{{WORLD_H}}", str(WORLD_H))
            .replace("{{CHAPTERS}}", chap_html).replace("{{CAPTIONS}}", "\n      ".join(caps)).replace("{{DURATION}}", str(DUR))
            .replace("      {{ENDCARD}}\n", "      " + card_html if card_html else "")
            .replace("{{AUDIO}}", f'<audio id="voix" src="assets/voix.wav" data-start="0" data-duration="{DUR}" data-volume="1"></audio>\n      ' + audio_html)
            .replace("{{TWEENS}}", "\n      ".join(cam_tw + tw)))
    open(os.path.join(HERE, out), "w").write(page)
    print(f"nodes {len(html)}  tweens {len(cam_tw) + len(tw)}  captions {len(caps)}  audio {len(audio) + 1}  camera stops {len(CAM)}")
