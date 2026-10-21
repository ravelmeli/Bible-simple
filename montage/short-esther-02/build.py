"""Short « Esther » in style 02 « Explainer à autocollants » (PaperClip-like) — 9:16, 62.4 s.

One giant canvas (3 × 5 screens) travelled by one continuous camera. Every beat is timed on the word-level
transcript (transcript.json). Separate from the style-01 builder (montage/common.py) on purpose.
Run: python3 build.py
"""
import json
import os
import re

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, DUR = 1080, 1920, 62.4
ACC = "#F85830"
words = json.load(open(os.path.join(HERE, "transcript.json")))


def norm(t):
    return re.sub(r"[\.,\?!:;«»\"'’() ]", "", t).lower()


def T(word, n=0):
    hits = [w for w in words if norm(w["text"]) == norm(word)]
    return hits[n]["start"]


html, tw, audio = [], [], []
_uid = [0]


def uid():
    _uid[0] += 1
    return f"x{_uid[0]}"


def at(t):
    return f"{t:.3f}"


def tween(sel, frm, to, t):
    tw.append(f'tl.fromTo("{sel}", {{ {frm} }}, {{ {to} }}, {at(t)});')


def st(c, r):
    """World coordinates of a station (one screen) on the canvas."""
    return c * W, r * H


# ---------------------------------------------------------------- primitives
def put(station, x, y, inner, cls="", style=""):
    sx, sy = st(*station)
    i = uid()
    html.append(f'<div class="node {cls}" id="{i}" style="left:{sx + x}px;top:{sy + y}px;{style}">{inner}</div>')
    return i


def blur_in(i, t, dy=24):
    tween(f"#{i}", f"opacity: 0, y: {dy}, filter: \"blur(14px)\"", 'opacity: 1, y: 0, filter: "blur(0px)", duration: 0.55, ease: "power3.out"', t)


def pop(i, t, rot=-3):
    tween(f"#{i}", f"opacity: 0, scale: 0.55, rotation: {rot - 8}", f'opacity: 1, scale: 1, rotation: {rot}, duration: 0.6, ease: "back.out(1.9)"', t)


def sticker(station, name, x, y, w, t, rot=-3, label=None, sub=None, lab_dx=0, lab_dy=0, side="right"):
    iw, ih = Image.open(os.path.join(HERE, "assets/stickers", name + ".png")).size
    h = round(ih * w / iw)
    i = put(station, x, y, f'<img src="assets/stickers/{name}.png" style="width:{w}px;height:{h}px" />', "sticker")
    pop(i, t, rot)
    sfx("pop", t, 0.32)
    if label:
        lx = x + w + 30 if side == "right" else x - 330
        ly = y + h // 2 - 40 + lab_dy
        lx += lab_dx
        leader(station, (x + w * (0.85 if side == "right" else 0.15), y + h * 0.5), (lx if side == "right" else lx + 300, ly + 22), t + 0.25)
        label_box(station, lx, ly, label, sub, t + 0.35)
    return i, h


def leader(station, a, b, t):
    sx, sy = st(*station)
    i = uid()
    (x1, y1), (x2, y2) = a, b
    ln = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5) + 2
    html.append(f'<svg class="node lead" id="{i}" style="left:{sx}px;top:{sy}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-dasharray="{ln}" />'
                f'<circle cx="{x1}" cy="{y1}" r="7" /></svg>')
    tween(f"#{i} line", f"strokeDashoffset: {ln}", 'strokeDashoffset: 0, duration: 0.4, ease: "power2.out"', t)
    tween(f"#{i} circle", "scale: 0, transformOrigin: \"50% 50%\"", 'scale: 1, duration: 0.25, ease: "back.out(3)"', t)


def label_box(station, x, y, title, sub, t):
    inner = f'<b>{title}</b>' + (f'<span>{sub}</span>' if sub else "")
    i = put(station, x, y, inner, "label")
    blur_in(i, t, 10)
    sfx("click", t, 0.5)
    return i


def tag(station, x, y, text, t, cls="", size=44):
    i = put(station, x, y, text, f"tag {cls}", f"font-size:{size}px")
    tween(f"#{i}", "opacity: 0, scaleX: 0.2, transformOrigin: \"0% 50%\"", 'opacity: 1, scaleX: 1, duration: 0.35, ease: "power3.out"', t)
    return i


def ref(station, x, y, text, t):
    i = put(station, x, y, text, "ref")
    blur_in(i, t, 8)
    return i


def headline(station, y, lines, t, kicker=None, sub=None, size=96, x=70, dark=False, hl=None, hl_t=None):
    """Headline with an optional orange underline under the words wrapped in [ ]."""
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
    i = put(station, x, y, f'<span class="num" id="{uid()}">{frm}</span><span class="unit">{unit}</span>', f"counter {cls}", f"font-size:{size}px")
    num = html[-1].split('class="num" id="')[1].split('"')[0]
    blur_in(i, t - 0.1, 16)
    tw.append(f'(function(){{ const o = {{ v: {frm} }}; const el = document.getElementById("{num}"); '
              f'tl.fromTo(o, {{ v: {frm} }}, {{ v: {to}, duration: {dur}, ease: "power2.out", '
              f'onUpdate: () => {{ el.textContent = Math.round(o.v); }} }}, {at(t)}); }})();')
    if dur > 0.5:
        sfx("tick", t, 0.25, min(dur, 1.5))
    return i


# ---------------------------------------------------------------- audio
LIB = {"whoosh": ("assets/audio/lib/whoosh-short.mp3", 0.57), "click": ("assets/audio/lib/click-soft.mp3", 0.37),
       "pop": ("assets/audio/lib/pop.mp3", 0.72), "bass": ("assets/audio/lib/impact-bass-2.mp3", 2.0),
       "tick": ("assets/audio/lib/typing.mp3", 1.5), "spark": ("assets/audio/lib/sparkle.mp3", 1.2)}
BASE = {"whoosh": 0.10, "click": 0.22, "pop": 0.28, "bass": 0.07, "tick": 0.12, "spark": 0.06}


def sfx(kind, t, k=1.0, dur=None):
    path, d = LIB[kind]
    d = min(dur or d, DUR - t)
    audio.append((f"a{len(audio)}", path, round(t, 3), round(d, 3), round(BASE[kind] * k, 3)))


def hit(t, k=1.0):
    """Hero hit: low impact + pop on top so it reads on a phone speaker."""
    sfx("bass", t, k)
    sfx("pop", t, 1.4 * k)


# ---------------------------------------------------------------- camera
CAM = []  # (time, station, scale)


def cam(t, station, scale=1.0):
    CAM.append((t, station, scale))


# ================================================================ STORY
S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S9 = (0, 2), (2, 2)
S10, S11, S12 = (2, 3), (1, 3), (0, 3)
S13 = (0, 4)

# --- S1 · 0 – 5.74 · hook: entering uninvited means death (Est 4:11)
cam(0, S1)
headline(S1, 300, ["Entrer chez le roi", "sans [invitation] ?"], 0.0, kicker="Explication · Esther", hl_t=T("sans") + 0.2, size=100)
sticker(S1, "tete-garde-perse", 90, 760, 560, 0.35, rot=-4, label="Garde perse", sub="relief, v. 486–465 av. J.-C.")
tag(S1, 600, 1130, "= la mort", T("mort"), "acc", 64)
ref(S1, 600, 1230, "Esther 4.11", T("mort") + 0.2)
hit(T("mort"), 1.0)

# --- S2 · 5.74 – 10.82 · Esther, queen of Persia, secretly Jewish (Est 2:10)
cam(5.62, S2)
headline(S2, 300, ["Esther,", "reine de [Perse]"], T("esther") - 0.3, kicker="Le personnage", hl_t=T("perse"), size=104)
sticker(S2, "daric-roi", 80, 700, 420, 6.2, rot=5, label="Le roi de Perse", sub="daric en or, IVe s. av. J.-C.", lab_dy=-90)
sticker(S2, "rouleau-esther", 600, 820, 300, 7.0, rot=-6)
label_box(S2, 560, 1180, "Le livre d'Esther", "rouleau, XVIIIe s.", 7.4)
tag(S2, 80, 1190, "Secret : elle est juive", T("juive"), "acc", 46)
ref(S2, 80, 1285, "Esther 2.10", T("juive") + 0.2)

# --- S3 · 10.82 – 17.98 · Haman's decree to every province, one single day (Est 1:1, 3:12-13)
cam(10.7, S3)
headline(S3, 280, ["Le [décret] de Haman"], T("haman") - 0.3, kicker="Le danger", hl_t=T("décret"), size=92)
sticker(S3, "tablette-scellee", 70, 470, 360, T("décret") - 0.2, rot=-5, label="Document scellé", sub="tablette perse, v. 500 av. J.-C.", lab_dy=-10)
grid_id = uid()
tiles = "".join(f'<i id="{grid_id}t{k}"></i>' for k in range(127))
gi = put(S3, 70, 800, f'<div class="grid">{tiles}</div>', "gridwrap")
blur_in(gi, T("décret") + 0.1, 12)
for k in range(127):
    tween(f"#{grid_id}t{k}", 'backgroundColor: "#CBD3DC"', f'backgroundColor: "{ACC}", duration: 0.08', T("décret") + 0.35 + k * 0.018)
counter(S3, 760, 790, 0, 127, T("décret") + 0.35, 127 * 0.018, "", 120, "small")
label_box(S3, 760, 930, "provinces", "tout l'empire", T("décret") + 0.6)
tag(S3, 70, 1300, "Exécution : 1 seul jour", T("jour") - 0.15, "acc", 50)
ref(S3, 690, 1314, "Esther 1.1 · 3.13", T("jour"))
hit(T("décret"), 0.8)

# --- S4 · 17.98 – 22.98 · the scepter rule as a decision chart (Est 4:11)
cam(17.85, S4)
headline(S4, 280, ["Seul le [sceptre d'or]"], 18.0, kicker="La loi du palais", hl_t=T("sceptre"), size=92)
tag(S4, 70, 470, "Esther hésite", T("hésite"), "", 40)
ref(S4, 760, 482, "Esther 4.11", T("hésite") + 0.2)
f1 = put(S4, 290, 600, "Entrer sans être appelé", "box")
blur_in(f1, 19.2, 14)
f2 = put(S4, 230, 790, "Le roi tend-il<br>son sceptre d'or ?", "box q")
blur_in(f2, T("sceptre"), 14)
sx4, sy4 = st(*S4)
arrows = uid()
html.append(f'<svg class="node lead arrows" id="{arrows}" style="left:{sx4}px;top:{sy4}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<path class="a0" d="M540 690 L540 780" stroke-dasharray="100"/>'
            f'<path class="a1" d="M380 950 L240 1060" stroke-dasharray="200"/>'
            f'<path class="a2" d="M700 950 L840 1060" stroke-dasharray="200"/></svg>')
tween(f"#{arrows} .a0", "strokeDashoffset: 100", 'strokeDashoffset: 0, duration: 0.3', T("sceptre") - 0.2)
tween(f"#{arrows} .a1, #{arrows} .a2", "strokeDashoffset: 200", 'strokeDashoffset: 0, duration: 0.4, stagger: 0.15', T("sceptre") + 0.4)
no = put(S4, 90, 1070, "<small>Non</small>Mort", "box out")
yes = put(S4, 690, 1070, "<small>Oui</small>Vie", "box out")
blur_in(no, T("sceptre") + 0.6, 12)
blur_in(yes, T("vie") - 0.3, 12)
sfx("click", T("sceptre") + 0.6, 0.6)

# --- S5 · 22.98 – 28.64 · Mordecai's challenge (Est 4:14)
cam(22.85, S5)
headline(S5, 290, ["« Pour un temps", "comme [celui-ci] »"], T("temps") - 0.2, kicker="Mardochée · Esther 4.14", hl_t=T("temps") + 0.5, size=96)
sticker(S5, "chapiteau-taureau", 140, 760, 480, 23.2, rot=4, label="Palais perse", sub="chapiteau, Ve s. av. J.-C.", lab_dy=-40)
tag(S5, 120, 1240, "Et si c'était le moment ?", T("reine", 2) - 0.6, "", 44)

# --- S6 · 28.64 – 31.4 · three days of fasting (Est 4:16)
cam(28.5, S6)
headline(S6, 300, ["[3 jours] de jeûne"], T("trois") - 0.2, kicker="La préparation", hl_t=T("trois") + 0.2, size=100)
for k in range(3):
    d = put(S6, 70 + k * 320, 620, f'<small>Jour</small>{k + 1}', "day")
    tween(f"#{d}", 'opacity: 0, y: 40, backgroundColor: "#FFFFFF", color: "#1B242E"',
          f'opacity: 1, y: 0, backgroundColor: "{ACC}", color: "#FFFFFF", duration: 0.35, ease: "back.out(2)"', T("trois") + 0.15 + k * 0.42)
    sfx("click", T("trois") + 0.15 + k * 0.42, 0.7)
label_box(S6, 70, 1000, "Tout le peuple jeûne", "à Suse, nuit et jour", T("jeûne"))
ref(S6, 70, 1120, "Esther 4.16", T("jeûne") + 0.2)

# --- S7 · 31.4 – 34.96 · « If I perish, I perish » (captions hidden: the line is on screen)
cam(31.25, S7)
q = headline(S7, 520, ["Si je dois périr,", "je [périrai]."], T("périr") - 0.6, kicker="Esther · Esther 4.16", hl_t=T("périrai"), size=124)
hit(T("périrai"), 1.0)

# --- S4 again · 34.96 – 38.68 · she walks in, the king holds out the scepter: the « Oui » path lights up (Est 5:2)
cam(34.85, S4, 0.92)
tag(S4, 70, 1270, "Elle entre", T("entre"), "", 48)
tween(f"#{arrows} .a2", f'stroke: "#8A97A6"', f'stroke: "{ACC}", strokeWidth: 10, duration: 0.3', T("tend"))
tween(f"#{yes}", 'backgroundColor: "#FFFFFF", color: "#1B242E"', f'backgroundColor: "{ACC}", color: "#FFFFFF", duration: 0.25', T("tend"))
tween(f"#{yes}", "scale: 1", 'scale: 1.18, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out"', T("tend"))
tween(f"#{no}", "opacity: 1", 'opacity: 0.25, duration: 0.4', T("tend"))
ref(S4, 700, 1282, "Esther 5.2", T("tend") + 0.2)
hit(T("tend"), 1.2)
sfx("spark", T("sceptre", 1), 1.0)

# --- S9 · 38.68 – 43.8 · two banquets, then Haman exposed (Est 5:4-8, 7:1-6)
cam(38.55, S9)
headline(S9, 280, ["Deux festins,", "un [piège] inversé"], T("festin") - 0.4, kicker="Le retournement", hl_t=T("dénonce"), size=88)
sx9, sy9 = st(*S9)
tl_id = uid()
html.append(f'<svg class="node lead" id="{tl_id}" style="left:{sx9}px;top:{sy9}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<path d="M120 640 L120 1180" stroke-dasharray="540"/></svg>')
tween(f"#{tl_id} path", "strokeDashoffset: 540", 'strokeDashoffset: 0, duration: 2.4, ease: "none"', T("festin") - 0.1)
for k, (title, sub, t) in enumerate([("Festin n° 1", "Esther 5.4", T("festin")), ("Festin n° 2", "Esther 7.1", T("festin") + 0.9),
                                     ("Révélation", "Esther 7.3-6", T("identité"))]):
    dot = put(S9, 106, 630 + k * 250, "", "dot")
    tween(f"#{dot}", "scale: 0", 'scale: 1, duration: 0.3, ease: "back.out(3)"', t)
    label_box(S9, 160, 610 + k * 250, title, sub, t)
sticker(S9, "rhyton-belier", 640, 560, 300, T("festin") + 0.3, rot=6)
sticker(S9, "coupe-inscription-royale", 600, 900, 330, T("festin") + 0.8, rot=-4)
label_box(S9, 600, 1250, "Vaisselle royale perse", "Ve s. av. J.-C.", T("festin") + 1.1)
tag(S9, 160, 1290, "Haman dénoncé", T("dénonce"), "acc", 50)
hit(T("dénonce"), 0.7)

# --- S10 · 43.8 – 46.6 · the gallows, to scale (Est 5:14, 7:10)
cam(43.65, S10)
headline(S10, 280, ["Pendu à sa", "propre [potence]"], 43.85, kicker="La chute de Haman", hl_t=T("potence"), size=92)
bar_h = 760                       # 50 cubits ≈ 22 m  → about 34.5 px per metre
man_h = round(1.7 * bar_h / 22)   # a man ≈ 1.7 m, same scale
base_y = 1380
b1 = put(S10, 220, base_y - bar_h, "", "bar acc", f"width:140px;height:{bar_h}px")
tween(f"#{b1}", "scaleY: 0, transformOrigin: \"50% 100%\"", 'scaleY: 1, duration: 0.9, ease: "power3.out"', T("potence"))
b2 = put(S10, 430, base_y - man_h, "", "bar", f"width:60px;height:{man_h}px")
tween(f"#{b2}", "scaleY: 0, transformOrigin: \"50% 100%\"", 'scaleY: 1, duration: 0.3, ease: "power3.out"', T("potence") + 0.4)
label_box(S10, 400, 640, "Potence : 50 coudées", "≈ 22 m (coudée ≈ 44,5 cm)", T("potence") + 0.2)
label_box(S10, 520, base_y - 120, "Un homme", "≈ 1,7 m, même échelle", T("potence") + 0.6)
ref(S10, 400, 790, "Esther 5.14 · 7.10", T("potence") + 0.4)
hit(T("potence"), 0.9)

# --- S11 · 46.6 – 50.8 · the people saved, Purim (Est 9:20-28)
cam(46.45, S11)
headline(S11, 280, ["Le peuple est [sauvé]"], T("sauvé") - 0.5, kicker="L'issue", hl_t=T("sauvé"), size=92)
sticker(S11, "relief-serviteurs-festin", 90, 500, 380, 46.9, rot=-4, label="Repas de fête", sub="relief perse, IVe s. av. J.-C.", lab_dy=-60)
for k, dname in enumerate(["14 Adar", "15 Adar"]):
    d = put(S11, 90 + k * 330, 1020, f'<small>Purim</small>{dname}', "day wide")
    tween(f"#{d}", 'opacity: 0, y: 40, backgroundColor: "#FFFFFF", color: "#1B242E"',
          f'opacity: 1, y: 0, backgroundColor: "{ACC}", color: "#FFFFFF", duration: 0.35, ease: "back.out(2)"', T("purim") + k * 0.35)
ref(S11, 90, 1260, "Esther 9.20-28", T("purim") + 0.3)
hit(T("sauvé"), 0.6)

# --- S12 · 50.8 – 54.76 · dark mode reveal: the book never names God
cam(50.65, S12)
tween("#darkbg", "opacity: 0", 'opacity: 1, duration: 0.6, ease: "power2.inOut"', 50.6)
headline(S12, 280, ["Le livre d'Esther"], 50.95, kicker="Détail étonnant", size=92, dark=True)
sticker(S12, "rouleau-esther", 700, 470, 240, 51.1, rot=6)
counter(S12, 70, 520, 0, 10, 51.4, 0.8, " chapitres", 96, "dark small")
counter(S12, 70, 680, 0, 167, 52.0, 1.0, " versets", 96, "dark small")
label_box(S12, 70, 880, "Le nom de Dieu", "dans le texte hébreu", T("jamais") - 0.3)
z = put(S12, 70, 980, "0", "zero")
tween(f"#{z}", "opacity: 0, scale: 2.2", 'opacity: 1, scale: 1, duration: 0.35, ease: "power4.in"', T("dieu"))
tag(S12, 460, 1110, "fois", T("dieu") + 0.3, "dark", 56)
hit(T("dieu"), 1.0)

# --- S13 · 54.76 – 59.8 · the question
cam(54.6, S13)
headline(S13, 520, ["Et [toi] ?"], T("toi") - 0.2, kicker="À ton tour", hl_t=T("toi"), size=200, dark=True)
cta = put(S13, 70, 1010, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Réponds en commentaire', "cta")
blur_in(cta, T("commentaire") - 0.5, 14)
sfx("click", T("commentaire") - 0.5, 0.8)

# --- end · 59.8 – 62.4 · pull out over the whole canvas, title card
cam(59.65, "all")

# ================================================================ assemble
WORLD_W, WORLD_H = 3 * W, 5 * H


def cam_xy(station, scale):
    if station == "all":
        s = min(W / WORLD_W, H / WORLD_H) * 0.92
        return (W - WORLD_W * s) / 2, (H - WORLD_H * s) / 2, s
    sx, sy = st(*station)
    return W / 2 - (sx + W / 2) * scale, H / 2 - (sy + H / 2) * scale, scale


cam_tw = []
x0, y0, s0 = cam_xy(CAM[0][1], 1.0)
cam_tw.append(f'tl.set("#world", {{ x: {x0:.1f}, y: {y0:.1f}, scale: {s0} }}, 0);')
for k, (t, stn, sc) in enumerate(CAM):
    x, y, s = cam_xy(stn, sc)
    move = 0.95 if stn == "all" else 0.75
    if k:
        px, py, ps = cam_xy(CAM[k - 1][1], CAM[k - 1][2])
        cam_tw.append(f'tl.fromTo("#world", {{ x: {px:.1f}, y: {py:.1f}, scale: {ps:.4f} }}, '
                      f'{{ x: {x:.1f}, y: {y:.1f}, scale: {s:.4f}, duration: {move}, ease: "power3.inOut", immediateRender: false }}, {at(t)});')
        cam_tw.append(f'tl.fromTo("#world", {{ filter: "blur(0px)" }}, {{ filter: "blur(5px)", duration: {move / 2}, yoyo: true, repeat: 1, ease: "power2.in", immediateRender: false }}, {at(t)});')
        sfx("whoosh", t, 0.9)
    # Slow drift while holding a station.
    end = CAM[k + 1][0] if k + 1 < len(CAM) else DUR
    hold_from = t + (move if k else 0)
    if end - hold_from > 0.4:
        cam_tw.append(f'tl.fromTo("#drift", {{ scale: 1 }}, {{ scale: 1.035, duration: {end - hold_from:.2f}, ease: "none", immediateRender: false }}, {at(hold_from)});')

# End title card: the pulled-out canvas is shown briefly, then fades under the card.
tw.append(f'tl.fromTo("#world", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.4, ease: "power1.in", immediateRender: false }}, {at(60.1)});')
tw.append(f'tl.fromTo("#chrome", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.3, immediateRender: false }}, {at(59.7)});')
tw.append(f'tl.fromTo("#endcard", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {at(60.2)});')
tw.append(f'tl.fromTo("#endcard .h", {{ y: 40, filter: "blur(12px)" }}, {{ y: 0, filter: "blur(0px)", duration: 0.6, ease: "power3.out" }}, {at(60.25)});')
tw.append(f'tl.fromTo("#endcard .hl i", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "power3.out" }}, {at(60.7)});')
tw.append(f'tl.fromTo("#endcard .sub2", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }}, {at(60.9)});')
tw.append(f'tl.fromTo("#endcard .sub2", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.4, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, {at(61.4)});')
hit(60.9, 0.5)

# Chapter bar.
CHAP = [("01", "Danger", 0, 17.85), ("02", "Décision", 17.85, 34.85), ("03", "Retournement", 34.85, 50.65), ("04", "Leçon", 50.65, DUR)]
chap_html = "".join(f'<div class="ch" id="ch{k}"><b>{n}</b> {lab}<i></i></div>' for k, (n, lab, a, b) in enumerate(CHAP))
for k, (n, lab, a, b) in enumerate(CHAP):
    tw.append(f'tl.fromTo("#ch{k} i", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {b - a:.2f}, ease: "none", immediateRender: {"true" if k == 0 else "false"} }}, {at(a)});')
    tw.append(f'tl.fromTo("#ch{k}", {{ opacity: 0.45 }}, {{ opacity: 1, duration: 0.2, immediateRender: {"true" if k == 0 else "false"} }}, {at(a)});')
    if k + 1 < len(CHAP):
        tw.append(f'tl.to("#ch{k}", {{ opacity: 0.45, duration: 0.2 }}, {at(b)});')
tw.append(f'tl.fromTo("#chrome", {{ color: "#1B242E" }}, {{ color: "#E9EDF1", duration: 0.6 }}, {at(50.6)});')

# Captions (hidden while the hero quote is on screen and over the end card).
SUPPRESS = [(31.3, 34.9), (59.6, DUR)]
chunks, cur = [], []
for w in words:
    cur.append(w)
    if w["text"].rstrip().endswith((".", "?", "!", ",", ":")) or len(cur) == 4:
        chunks.append(cur); cur = []
if cur:
    chunks.append(cur)
caps = []
for n, ch in enumerate(chunks):
    s = ch[0]["start"]
    nxt = chunks[n + 1][0]["start"] if n + 1 < len(chunks) else DUR
    e = min(max(ch[-1]["end"] + 0.22, s + 0.55), nxt)
    if any(a - 0.05 <= s and ch[-1]["end"] <= b + 0.35 for a, b in SUPPRESS):
        continue
    spans = " ".join(f'<span class="cw" id="w{n}_{k}">{w["text"]}</span>' for k, w in enumerate(ch))
    caps.append(f'<p class="clip cap" id="cap{n}" data-start="{s:.3f}" data-duration="{e - s:.3f}"><span class="capin" id="ci{n}">{spans}</span></p>')
    tw.append(f'tl.fromTo("#ci{n}", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }}, {at(s)});')
    for k, w in enumerate(ch):
        tw.append(f'tl.fromTo("#w{n}_{k}", {{ color: "#1B242E" }}, {{ color: "{ACC}", duration: 0.08 }}, {at(w["start"])});')
        tw.append(f'tl.to("#w{n}_{k}", {{ color: "#1B242E", duration: 0.12 }}, {at(max(w["end"], w["start"] + 0.16))});')

audio_html = "\n      ".join(f'<audio id="{a}" src="{p}" data-start="{s}" data-duration="{d}" data-volume="{v}"></audio>' for a, p, s, d, v in audio)
tpl = open(os.path.join(HERE, "template.tpl")).read()
out = (tpl.replace("{{WORLD}}", "\n        ".join(html)).replace("{{WORLD_W}}", str(WORLD_W)).replace("{{WORLD_H}}", str(WORLD_H))
       .replace("{{CHAPTERS}}", chap_html).replace("{{CAPTIONS}}", "\n      ".join(caps)).replace("{{DURATION}}", str(DUR))
       .replace("{{AUDIO}}", '<audio id="voix" src="assets/voix.wav" data-start="0" data-duration="62.4" data-volume="1"></audio>\n      ' + audio_html)
       .replace("{{TWEENS}}", "\n      ".join(cam_tw + tw)))
open(os.path.join(HERE, "index.html"), "w").write(out)
print(f"nodes {len(html)}  tweens {len(cam_tw) + len(tw)}  captions {len(caps)}  audio {len(audio) + 1}  camera stops {len(CAM)}")
