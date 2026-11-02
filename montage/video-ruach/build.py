"""Vidéo longue « Ruach : le mot hébreu pour esprit, vent et souffle » — style 02, 16:9, 370,5 s.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py) : option retention, citations mot par mot, animations de code
(vent, souffle, lueur, balance...). 12 plans, dont Horeb revisité avec un état différent. Tout est calé sur transcript.json.
Les mots hébreux et grecs sont translittérés en lettres latines, écrits en HTML : à faire relire avant publication.
Lancer : python3 build.py   (puis npx hyperframes check et npx hyperframes render -q draft)
"""
import difflib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Ruach, vent, souffle et esprit - style 02", "lang": "fr",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
DUR_ = 370.5
s.setup(here=HERE, duration=DUR_, cols=5, rows=4, fmt="16:9", theme=THEME, bpm=96, zoom=1.15, xmap=(190, 0.8539), ymap=(208, 0.85))
from style02 import *  # noqa: E402,F401,F403
import style02  # noqa: E402

MANQUES = []
SUPP = []


def _norm(t):
    return re.sub(r"[^\wÀ-ÿ]", "", t.lower())


# début de chaque ligne du script (s), par alignement script / transcription
_lines = [l for l in open(os.path.join(HERE, "script.md")).read().split("\n") if l.strip()]
_idx = [i for i, x in enumerate(style02.words) if _norm(x["text"])]
_tw = [_norm(style02.words[i]["text"]) for i in _idx]
_sw, _ls = [], []
for _L, _l in enumerate(_lines):
    for _t in _l.split():
        if _norm(_t):
            _sw.append(_norm(_t))
            _ls.append(_L + 1)
_map = {}
for _tag, _i1, _i2, _j1, _j2 in difflib.SequenceMatcher(None, _sw, _tw, autojunk=False).get_opcodes():
    if _tag == "equal":
        for _k in range(_i2 - _i1):
            _map[_i1 + _k] = _j1 + _k
LS = {}
for _si, _L in enumerate(_ls):
    if _L not in LS and _si in _map:
        LS[_L] = style02.words[_idx[_map[_si]]]["start"]
for _L in range(1, len(_lines) + 2):
    if _L not in LS:  # ligne non alignée : repère = ligne précédente
        LS[_L] = LS.get(_L - 1, 0.0) + 2.0
LS[len(_lines) + 1] = DUR_


def A(word, after=0.0, n=0):
    """Début de la n-ième occurrence de `word` prononcée à partir de `after` secondes."""
    hits = [w["start"] for w in style02.words if style02.norm(w["text"]) == style02.norm(word) and w["start"] >= after - 0.01]
    if len(hits) <= n:
        MANQUES.append((word, after, n))
        return max(after, 1.0) + 0.5
    return hits[n]


def AL(word, line, n=0):
    """Occurrence de `word` à partir du début de la ligne `line`."""
    return A(word, LS[line] - 0.05, n)


def S_(station, name, x, y, w, t, **kw):
    i, h = sticker(station, name, x, y, w, t, **kw)
    bas = 208 + 0.85 * (y - 170) + h
    if bas > 830:
        print(f"ATTENTION {name} y={y} w={w} : bas à {bas:.0f}")
    return i


def kq(station, x, y, ref_txt, text, line, first, width=1000, size=38, last=None):
    """Citation mot par mot : `first` = premier mot de la citation (cherché depuis le début de la ligne)."""
    t0 = AL(first, line) - 0.05
    t1 = (LS[line + 1] - 0.25) if last is None else last
    SUPP.append((t0 - 0.1, t1 + 0.2))
    return kinetic_quote(station, x, y, ref_txt, text, t0, t1, width=width, size=size)


def slot(station, name, x, y, w, t0, t1, **kw):
    i = S_(station, name, x, y, w, t0, **kw)
    fade(i, t1)
    return i


HOREB, TROIS, HOREB2, EXODE, SOUFFLE = (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)
NESHAMAH, ESPRIT, EZECHIEL, NT, ATTENTION = (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)
APPLI = (0, 2)

html.append('<style>'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

# =====================================================================  HOREB (lignes 1-5) : vent, séisme, feu
cam(0, HOREB)
S_(HOREB, "elie", 1480, 330, 230, 0.0, rot=-3, instant=True)
S_(HOREB, "montagne", 1000, 330, 440, AL("montagne", 1) - 0.2, rot=2)
headline(HOREB, 170, ["Sur la montagne d'[Horeb]"], 0.0, kicker="1 Rois 19", hl_t=AL("Horeb", 1) + 0.05, size=92)
tag(HOREB, 90, 360, "Un vent", AL("vent", 2) - 0.1, "", 50)
tag(HOREB, 90, 450, "Un séisme", AL("tremblement", 2) - 0.1, "", 50)
tag(HOREB, 90, 540, "Un feu", AL("feu", 2) - 0.1, "", 50)
w0 = wind(HOREB, 480, 330, AL("vent", 2) - 0.2, size=420, dur=4.5)
S_(HOREB, "rocher", 560, 630, 190, AL("tremblement", 2) - 0.2, rot=-3)
S_(HOREB, "flamme", 800, 610, 170, AL("feu", 2) - 0.2, rot=3)
stamp(HOREB, 500, 420, "Pas là", AL("trois", 3) + 0.3, rot=-4, size=72)
teaser(HOREB, 90, 760, "Un seul mot cache trois sens", AL("Pourtant", 4) - 0.2, hold=3.2)
tag(HOREB, 1000, 760, "vent = esprit", AL("esprit", 4) - 0.2, "acc", 50)
r0 = put(HOREB, 90, 600, "ruach", "word", "font-size:200px")
blur_in(r0, AL("ruach", 5) - 0.1, 20)
burst(HOREB, 1100, 420, AL("vent", 2) + 0.1)
hit(AL("ruach", 5), 1.0)

# =====================================================================  TROIS MOTS (lignes 6-9)
t = LS[6] - 0.4
cam(t, TROIS)
headline(TROIS, 170, ["Trois mots pour [un seul]"], t + 0.1, kicker="Ruach", hl_t=AL("seul", 6) + 0.05, size=96)
S_(TROIS, "bible-hebraique", 1100, 330, 500, AL("hébreu", 6) - 0.3, rot=-2)
tag(TROIS, 90, 360, "Le vent", AL("vent", 6) - 0.1, "", 58)
tag(TROIS, 90, 470, "Le souffle", AL("souffle", 6) - 0.1, "", 58)
tag(TROIS, 90, 580, "L'esprit", AL("esprit", 6) - 0.1, "acc", 58)
S_(TROIS, "souffle", 760, 340, 190, AL("souffle", 6) - 0.1, rot=2)
tag(TROIS, 90, 700, "Latin : spiritus = souffle", AL("latin", 7) - 0.2, "", 40)
tag(TROIS, 560, 700, "Grec : pneuma", AL("pneuma", 7) - 0.3, "acc", 40)
stamp(TROIS, 760, 560, "Confusion ?", AL("confusion", 8) - 0.2, rot=-4, size=64)
arrow(TROIS, (1100, 760), (1420, 760), AL("message", 8))
burst(TROIS, 1350, 450, AL("message", 8) + 0.1)

# =====================================================================  HOREB, lecture (lignes 10-13)
t = LS[10] - 0.4
cam(t, HOREB2)
headline(HOREB2, 170, ["La scène d'[Horeb]"], t + 0.1, kicker="1 Rois 19.11", hl_t=AL("scène", 10) + 0.05, size=96)
kq(HOREB2, 90, 330, "1 Rois 19.11 · Louis Segond 1910",
   "« Et voici, l'Éternel passa. Et devant l'Éternel, il y eut un vent fort et violent qui déchirait les montagnes et brisait les rochers : "
   "l'Éternel n'était pas dans le vent. Et après le vent, ce fut un tremblement de terre : l'Éternel n'était pas dans le tremblement de terre. »",
   11, "voici", width=1000, size=36)
S_(HOREB2, "elie-portrait", 1450, 330, 280, AL("Et", 11) + 0.2, rot=3)
w1 = wind(HOREB2, 1050, 330, AL("vent", 11) - 0.2, size=360, dur=5.0)
tag(HOREB2, 90, 700, "Premier sens : le vent", AL("premier", 12) - 0.2, "acc", 56)
stamp(HOREB2, 1050, 700, "1 · Le vent", AL("premier", 12) + 0.2, rot=-4, size=56)
S_(HOREB2, "rocher", 1500, 640, 180, AL("rochers", 11), rot=3)
tag(HOREB2, 560, 770, "Un vrai vent", AL("vrai", 12) - 0.1, "", 44)
burst(HOREB2, 1550, 420, AL("Dieu", 13) + 0.1)

# =====================================================================  EXODE (lignes 14-16)
t = LS[14] - 0.4
cam(t, EXODE)
headline(EXODE, 170, ["Le vent d'[orient]"], t + 0.1, kicker="Exode 14.21", hl_t=AL("d'orient", 14) + 0.05, size=104)
S_(EXODE, "moise", 110, 330, 270, AL("mer", 14) - 0.3, rot=-2)
w2 = wind(EXODE, 460, 330, AL("vent", 14) - 0.3, size=620, dur=7.0)
kq(EXODE, 460, 640, "Exode 14.21 · Louis Segond 1910", "« l'Éternel refoula la mer par un vent d'orient impétueux toute la nuit »",
   14, "léternel", width=900, size=36, last=AL("nuit", 14) + 0.5)
tag(EXODE, 1500, 330, "Les 4 vents", AL("quatre", 15) - 0.3, "acc", 50)
ring(EXODE, 1560, 520, AL("quatre", 15), size=240)
stamp(EXODE, 1400, 720, "1 · Le vent", AL("premier", 16) + 0.1, rot=-4, size=52)
tag(EXODE, 460, 810, "Une force invisible, aux effets visibles", AL("invisible", 16) - 0.4, "", 40)

# =====================================================================  SOUFFLE (lignes 17-20)
t = LS[17] - 0.4
cam(t, SOUFFLE)
headline(SOUFFLE, 170, ["Le [souffle]"], t + 0.1, kicker="2 · Deuxième sens", hl_t=AL("souffle", 18) + 0.05, size=110)
gl = glow(SOUFFLE, 1620, 600, t + 0.5, size=320, dur=6.0)
S_(SOUFFLE, "lampe", 1500, 520, 220, t + 0.5, rot=-3)
ts_ = tag(SOUFFLE, 90, 430, "Reste un moment avec nous", AL("reste", 17) - 0.3, "", 44)
fade(ts_, AL("deuxième", 18) - 0.2)
S_(SOUFFLE, "souffle", 90, 420, 230, AL("deuxième", 18) - 0.1, rot=2)
bz = breath(SOUFFLE, 330, 500, AL("deuxième", 18), size=420, dur=5.0)
S_(SOUFFLE, "shofar-grave", 800, 360, 560, AL("souffle", 18) + 0.4, rot=-3)
label_box(SOUFFLE, 800, 520, "Un chofar", "corne de bélier, XVIIIe s. · The Met", AL("Psaume", 19) - 0.2)
kq(SOUFFLE, 90, 640, "Psaume 104.29-30 · Louis Segond 1910",
   "« Tu leur retires le souffle : ils expirent, et retournent dans leur poussière. Tu envoies ton souffle : ils sont créés, "
   "et tu renouvelles la face de la terre. »", 19, "tu", width=1000, size=34)
tag(SOUFFLE, 1250, 400, "Le souffle de vie", AL("ruach", 20) - 0.3, "acc", 48)
ring(SOUFFLE, 215, 540, AL("deuxième", 18), size=260)

# =====================================================================  NESHAMAH (lignes 21-24)
t = LS[21] - 0.4
cam(t, NESHAMAH)
headline(NESHAMAH, 170, ["Un autre mot : [neshamah]"], t + 0.1, kicker="Genèse 2.7", hl_t=AL("neshamah", 21) + 0.05, size=92)
c1 = put(NESHAMAH, 90, 340, "<small>Genèse 2.7</small>un « souffle de vie » : <b>neshamah</b>", "card", "width:780px;font-size:36px")
blur_in(c1, AL("souffle", 21) - 0.3, 14)
c2 = put(NESHAMAH, 960, 340, "<small>Le plus souvent</small><b>ruach</b> : mouvement et force", "card", "width:780px;font-size:36px;border-color:" + ACC)
blur_in(c2, AL("ruach", 22) - 0.4, 14)
S_(NESHAMAH, "bible-hebraique", 90, 540, 380, AL("neshamah", 21) + 0.2, rot=-2)
sbn = S_(NESHAMAH, "sym-balance", 540, 540, 200, AL("proches", 22) - 0.2, rot=0)
animate(sbn, "rock", AL("proches", 22) - 0.2, dur=6.0)
tg_n = tag(NESHAMAH, 960, 790, "Proches, pas interchangeables", AL("interchangeables", 22) - 0.6, "acc", 38)
kq(NESHAMAH, 960, 540, "Ecclésiaste 12.7 · Louis Segond 1910", "« la poussière retourne à la terre, comme elle y avait été, et l'esprit retourne à Dieu qui l'a donné »",
   23, "la", width=740, size=28, last=AL("donné", 23) + 0.6)

# =====================================================================  ESPRIT (lignes 25-29)
t = LS[25] - 0.4
cam(t, ESPRIT)
headline(ESPRIT, 170, ["L'[esprit]"], t + 0.1, kicker="3 · Troisième sens", hl_t=AL("esprit", 25) + 0.05, size=110)
S_(ESPRIT, "rouleau", 1500, 330, 260, t + 0.5, rot=3)
kq(ESPRIT, 90, 330, "Genèse 1.2 · Louis Segond 1910", "« l'esprit de Dieu se mouvait au-dessus des eaux »", 26, "esprit", width=900, size=44,
   last=AL("eaux", 26) + 0.6)
w3 = wind(ESPRIT, 1000, 330, AL("deuxième", 26) - 0.2, size=420, dur=5.0)
cA = put(ESPRIT, 90, 540, "« l'Esprit de Dieu »", "card", "width:520px;font-size:34px")
cB = put(ESPRIT, 700, 540, "« un vent de Dieu »", "card", "width:520px;font-size:34px")
blur_in(cA, AL("certains", 27) - 0.2, 14)
blur_in(cB, AL("d'autres", 27) - 0.2, 14)
tag(ESPRIT, 90, 700, "Les traducteurs ne sont pas d'accord", AL("honnêtes", 27) - 0.2, "acc", 42)
S_(ESPRIT, "jacob", 1400, 360, 230, AL("Jacob", 28) - 0.3, rot=-3)
tag(ESPRIT, 90, 770, "L'esprit de Jacob se ranima", AL("ranima", 28) - 0.6, "", 40)
ring(ESPRIT, 1515, 520, AL("Jacob", 28), size=260)
fade(cA, AL("Psaume", 29) - 0.3)
fade(cB, AL("Psaume", 29) - 0.3)
kq(ESPRIT, 90, 540, "Psaume 34.19 · Louis Segond 1910", "« L'Éternel est près de ceux qui ont le cœur brisé, et il sauve ceux qui ont l'esprit dans l'abattement »",
   29, "léternel", width=1000, size=36)

# =====================================================================  ÉZÉCHIEL (lignes 30-35)
t = LS[30] - 0.5
cam(t, EZECHIEL)
headline(EZECHIEL, 170, ["La vallée d'[Ézéchiel]"], t + 0.1, kicker="Ézéchiel 37", hl_t=AL("vallée", 30) + 0.05, size=96)
S_(EZECHIEL, "ossements", 90, 330, 430, AL("vallée", 31) - 0.3, rot=-2)
S_(EZECHIEL, "ezechiel", 600, 330, 200, AL("prophète", 31) - 0.2, rot=3)
q9 = kq(EZECHIEL, 860, 330, "Ézéchiel 37.9 · Louis Segond 1910",
   "« Prophétise, et parle à l'esprit ! Prophétise, fils de l'homme, et dis à l'esprit : Ainsi parle le Seigneur, l'Éternel : "
   "Esprit, viens des quatre vents, souffle sur ces morts, et qu'ils revivent ! »", 32, "prophétise", width=900, size=34)
fade(q9, LS[33] - 0.2)
bz2 = breath(EZECHIEL, 600, 700, AL("souffle", 32), size=360, dur=4.0)
w4 = wind(EZECHIEL, 90, 640, AL("vents", 32) - 0.2, size=420, dur=4.0)
# le mot ruach revient : vent, souffle, esprit
rw = [put(EZECHIEL, 860 + k_ * 270, 560, ["ruach", "ruach", "ruach"][k_], "word", "font-size:80px") for k_ in range(3)]
for k_, (rid, lab) in enumerate(zip(rw, ["vent", "souffle", "esprit"])):
    blur_in(rid, AL("ruach", 33) + k_ * 0.9, 14)
    rw.append(tag(EZECHIEL, 860 + k_ * 270, 680, lab, AL("ruach", 33) + 0.5 + k_ * 0.9, "acc" if k_ == 2 else "", 40))
for _i in rw:
    fade(_i, AL("maison", 34) - 0.4)
tm = [tag(EZECHIEL, 860, 560, "toute la maison d'Israël", AL("maison", 34) - 0.3, "acc", 46), tag(EZECHIEL, 860, 650, "découragée, en exil", AL("exil", 34) - 0.4, "", 44)]
for _i in tm:
    fade(_i, LS[35] - 0.1)
S_(EZECHIEL, "foule", 1400, 400, 330, AL("promesse", 35) - 0.2, rot=2)
kq(EZECHIEL, 860, 330, "Ézéchiel 37.14 · Louis Segond 1910", "« Je mettrai mon esprit en vous, et vous vivrez »", 35, "je", width=900, size=44,
   last=AL("vivrez", 35) + 0.6)

# =====================================================================  NOUVEAU TESTAMENT (lignes 36-41)
t = LS[36] - 0.4
cam(t, NT)
headline(NT, 170, ["Le grec : [pneuma]"], t + 0.1, kicker="Le Nouveau Testament", hl_t=AL("pneuma", 36) + 0.05, size=104)
S_(NT, "nicodeme", 100, 340, 210, AL("Nicodème", 37) - 0.3, rot=-3)
S_(NT, "jesus-pied", 340, 340, 190, AL("Jésus", 37) - 0.3, rot=3)
qj = kq(NT, 600, 330, "Jean 3.8 · Louis Segond 1910",
        "« Le vent souffle où il veut, et tu en entends le bruit ; mais tu ne sais d'où il vient, ni où il va. Il en est ainsi de tout homme "
        "qui est né de l'Esprit »", 37, "vent", width=880, size=34)
fade(qj, LS[38] - 0.2)
w5 = wind(NT, 1600, 330, AL("vent", 37) - 0.2, size=230, dur=6.0)
nt_tags = [tag(NT, 600, 610, "pneuma = vent = Esprit", AL("grec", 38) - 0.2, "", 46),
           stamp(NT, 1180, 600, "Hypothèse", AL("hypothèse", 38) - 0.2, rot=-4, size=60),
           tag(NT, 600, 720, "Jésus parlait araméen", AL("araméen", 38) - 0.2, "", 40)]
for _i in nt_tags:
    fade(_i, LS[40] - 0.1)
bj = breath(NT, 1400, 340, AL("souffla", 39) - 0.2, size=300, dur=3.5)
S_(NT, "jesus-portrait", 1560, 330, 200, AL("souffla", 39) - 0.2, rot=3)
S_(NT, "pentecote", 1300, 330, 280, AL("Pentecôte", 40) - 0.6, rot=-2)
tag(NT, 1300, 760, "« un vent impétueux »", AL("impétueux", 40) - 0.4, "acc", 40)
tag(NT, 100, 780, "D'Horeb à la Pentecôte : un seul mot", AL("Pentecôte", 41) - 0.8, "acc", 40)

# =====================================================================  ATTENTION (lignes 42-43)
t = LS[42] - 0.4
cam(t, ATTENTION)
headline(ATTENTION, 170, ["Le [contexte] décide"], t + 0.1, kicker="Mais attention", hl_t=AL("contexte", 42) + 0.05, size=100)
sbA = S_(ATTENTION, "sym-balance", 1300, 330, 330, t + 0.4, rot=0)
animate(sbA, "rock", t + 0.4, dur=14.0)
tag(ATTENTION, 90, 400, "Trois sens ne se valent pas partout", AL("valent", 42) - 0.4, "", 46)
S_(ATTENTION, "elie-portrait", 640, 330, 260, AL("Élie", 43) - 0.3, rot=2)
stamp(ATTENTION, 90, 540, "Dieu n'est pas le vent", AL("vent", 43) - 0.2, rot=-3, size=52)
tag(ATTENTION, 90, 700, "Le vent est un signe", AL("signe", 43) - 0.3, "acc", 50)

# =====================================================================  APPLICATION (lignes 44-46)
t = LS[44] - 0.4
cam(t, APPLI)
headline(APPLI, 170, ["Cette semaine, [une minute]"], t + 0.1, kicker="Pour toi", hl_t=AL("minute", 44) + 0.05, size=100)
bz3 = breath(APPLI, 90, 330, AL("respiration", 44) - 0.5, size=480, dur=8.0, pulses=4)
S_(APPLI, "souffle", 90, 330, 190, AL("respiration", 44) - 0.5, rot=2)
counter(APPLI, 700, 340, 0, 60, AL("minute", 44), 6.0, unit=" s", size=170)
qa = kq(APPLI, 700, 560, "Psaume 34.19 · Louis Segond 1910", "« L'Éternel est près de ceux qui ont le cœur brisé »", 44, "psaume", width=700, size=34,
        last=AL("dix-neuf", 44) + 0.8)
fade(qa, LS[45] - 0.3)
gA = glow(APPLI, 1560, 520, AL("accompagnement", 45) - 0.4, size=360, dur=8.0)
mlp = S_(APPLI, "mains-lampe", 1420, 420, 280, AL("accompagnement", 45) - 0.4, rot=2)
fade(mlp, LS[46] - 0.1)
tag(APPLI, 90, 650, "Un accompagnement peut aider", AL("accompagnement", 45) - 0.3, "acc", 44)
tag(APPLI, 90, 750, "La foi et les soins ne s'opposent pas", AL("soins", 45) - 0.6, "", 38)
S_(APPLI, "foule", 1000, 400, 300, AL("commentaire", 46) - 2.0, rot=-2)
cta = put(APPLI, 90, 520, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Dis-le en commentaire', "cta")
blur_in(cta, AL("commentaire", 46) - 0.6, 14)
sfx("click", AL("commentaire", 46) - 0.6, 0.8)

# =====================================================================  HOREB (revisite) : le murmure (lignes 47-49)
cam(LS[47] - 2.0, "all")
wipe(HOREB, LS[47] - 2.1)
t = LS[47] - 0.4
cam(t, HOREB)
headline(HOREB, 170, ["Un murmure [doux et léger]"], t + 0.1, kicker="1 Rois 19.12", hl_t=AL("murmure", 47) + 0.05, size=96)
gH = glow(HOREB, 1000, 520, AL("Horeb", 47), size=480, dur=9.0)
S_(HOREB, "grotte", 700, 330, 420, AL("Horeb", 47), rot=2)
S_(HOREB, "elie-portrait", 130, 330, 300, AL("Élie", 47) - 0.3, rot=-3)
bH = breath(HOREB, 480, 560, AL("murmure", 47) - 0.3, size=380, dur=4.5)
tag(HOREB, 90, 700, "Après le vent, le séisme, le feu", AL("tremblement", 47) - 0.5, "", 44)
tag(HOREB, 90, 790, "« un murmure doux et léger »", AL("murmure", 47) - 0.1, "acc", 50)
S_(HOREB, "ossements", 1250, 400, 300, AL("ossements", 48) - 0.5, rot=-2)
S_(HOREB, "souffle", 1560, 330, 170, AL("souffle", 48) - 0.2, rot=3)
tag(HOREB, 1250, 770, "La même histoire", AL("histoire", 48) - 0.3, "acc", 44)
hit(AL("histoire", 48), 0.8)

t_end = AL("Un", 49) - 0.2
cam(t_end, "all")

supp = list(SUPP) + [(LS[47] - 2.8, LS[47] - 0.5), (AL("Un", 49) - 0.8, DUR_)]
build(
    chapters=[("01", "Le vent", 0, LS[18]), ("02", "Le souffle", LS[18], LS[25]), ("03", "L'esprit", LS[25], LS[36]),
              ("04", "Le Nouveau Testament", LS[36], LS[44]), ("05", "Pour toi", LS[44], DUR_)],
    suppress=supp,
    endcard={"kicker": "Chaque semaine", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("elie-portrait", 150, 560, 300, -6), ("ezechiel", 1550, 330, 200, 5)]},
    endcard_t=AL("Un", 49) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
