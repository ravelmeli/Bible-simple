"""Vidéo longue « « Aide-toi, le ciel t'aidera » n'est pas dans la Bible : d'où vient cette phrase ? » — style 02, 16:9.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py), option retention, thème beige.
Règles de mise en page (contrôlées par kit-style-02/outils/audit_chevauchements.js après chaque build) :
  - contenu à partir de y = 420 (sous le titre), colonne gauche x = 90, colonne droite x >= 1100, autocollants hauts à x = 1500 ;
  - une citation occupe sa zone seule : tout ce qui s'y trouvait disparaît avant, elle disparaît à la fin de la ligne ;
  - le contenu s'arrête avant les sous-titres (bas d'écran).
Les mots grecs (synteleia tou aiônos, apokalypsis, parousia) sont écrits en HTML : à faire relire avant publication.
Lancer : python3 build.py ; node ../../kit-style-02/outils/audit_chevauchements.js . ; npx hyperframes check
"""
import difflib
import json
import os
import re
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Aide-toi, le ciel t'aidera - style 02", "lang": "fr",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
DUR_ = json.load(open(os.path.join(HERE, "dur.json")))["dur"]
s.setup(here=HERE, duration=DUR_, cols=5, rows=4, fmt="16:9", theme=THEME, bpm=96, zoom=1.15, xmap=(190, 0.8539), ymap=(208, 0.85))
from style02 import *  # noqa: E402,F401,F403
import style02  # noqa: E402

MANQUES = []
SUPP = []


def _norm(t):
    return re.sub(r"[^\wÀ-ÿ]", "", t.lower().replace("’", "").replace("'", ""))


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
    if _L not in LS:
        LS[_L] = LS.get(_L - 1, 0.0) + 2.0
LS[len(_lines) + 1] = DUR_


PRE = ("", "l", "d", "j", "n", "s", "qu", "c", "m", "t", "dell", "un", "v", "quest", "sant", "tutt")


def A(word, after=0.0, n=0):
    keys = {style02.norm(pre + word) for pre in PRE}
    hits = sorted(w["start"] for w in style02.words if style02.norm(w["text"]) in keys and w["start"] >= after - 0.01)
    if len(hits) > n:
        return hits[n]
    MANQUES.append((word, after, n))
    return max(after, 1.0) + 0.5


def AL(word, line, n=0):
    return A(word, LS[line] - 0.05, n)


def FW(name, w, maxh=385):
    """Largeur d'un autocollant limitée pour que sa hauteur (px de conception) ne dépasse pas maxh."""
    iw, ih = Image.open(os.path.join(HERE, "assets/stickers", name + ".png")).size
    return round(min(w, maxh * iw / ih))


def S_(station, name, x, y, w, t, **kw):
    i, h = sticker(station, name, x, y, FW(name, w), t, **kw)
    return i


def kq(station, x, y, ref_txt, text, line, first, width=1000, size=34, last=None, fade_at=None, n=0):
    t0 = AL(first, line, n) - 0.05
    t1 = (LS[line + 1] - 0.25) if last is None else last
    SUPP.append((t0 - 0.1, t1 + 0.2))
    i = kinetic_quote(station, x, y, ref_txt, text, t0, t1, width=width, size=size)
    fade(i, (LS[line + 1] - 0.4) if fade_at is None else fade_at)
    return i


def E(word, line, dt, early=0.5):
    """Instant d'apparition : le mot moins dt, mais au plus tard LS[ligne] + early (pas de scène vide)."""
    return min(AL(word, line) - dt, LS[line] + early)


def gone(ids, t):
    for _i in ids:
        fade(_i, t)


def card(station, x, y, small, body, t, w=800, size=38, accent=False):
    c = put(station, x, y, f"<small>{small}</small>{body}", "card", f"width:{w}px;font-size:{size}px" + (f";border-color:{ACC}" if accent else ""))
    blur_in(c, t, 14)
    return c


def grab(station, fn):
    n0 = len(style02.NODES.get(station, []))
    fn()
    return list(style02.NODES[station][n0:])


S1, S2, S3, S4, S5 = (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)
S6, S7, S8, S9, S10 = (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)
S11, S12, S13 = (0, 2), (1, 2), (2, 2)
BIB = " · Louis Segond 1910"

html.append('<style>'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '@font-face{font-family:"Frank Ruhl Libre";src:url("assets/fonts/FrankRuhlLibre.ttf") format("truetype");font-weight:300 900}'
            '.heb{font-family:"Frank Ruhl Libre",serif;direction:rtl;display:inline-block}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

# =====================================================================  S1 : la phrase, l'enquête (lignes 1-7)
cam(0, S1)
headline(S1, 170, ["« Aide-toi, [le ciel] t'aidera »"], 0.0, kicker="Une phrase que tout le monde connaît", hl_t=AL("pas", 1) + 0.05, size=88)
S_(S1, "foule", 1100, 420, 330, 0.0, rot=-3, instant=True)
st1 = stamp(S1, 90, 440, "Pas dans la Bible", AL("pas", 1) - 0.1, rot=-4, size=76)
gone([st1], LS[3] - 0.3)
t3 = [tag(S1, 90, 430, "Une épreuve", AL("épreuve", 3) - 0.1, "", 52), tag(S1, 90, 540, "Un examen", AL("examen", 3) - 0.1, "", 52),
      tag(S1, 90, 650, "Presque un verset", AL("verset", 3) - 0.3, "acc", 52)]
gone(t3, LS[4] - 0.4)
st4 = [stamp(S1, 90, 440, "Introuvable", AL("trouveras", 4) - 0.3, rot=-3, size=80), tag(S1, 90, 650, "De la Genèse à l'Apocalypse", AL("Apocalypse", 4) - 1.0, "", 44)]
gone(st4, LS[5] - 0.4)
t5 = [tag(S1, 90, 430, "D'où vient-elle ?", AL("d'où", 5) - 0.1, "acc", 52), tag(S1, 90, 540, "Qui l'a dite ?", AL("qui", 5) - 0.1, "", 52),
      tag(S1, 90, 650, "Est-elle vraie ?", AL("vraie", 5) - 0.3, "", 52)]
gone(t5, LS[6] - 0.4)
t6 = [tag(S1, 90, 430, "France · XVIIe siècle", AL("France", 6) - 0.2, "", 50), tag(S1, 90, 540, "Grèce ancienne", AL("Grèce", 6) - 0.2, "", 50),
      tag(S1, 90, 650, "Ce que dit la Bible", AL("biblique", 6) - 0.4, "acc", 50)]
gone(t6, LS[7] - 0.4)
teaser(S1, 90, 440, "Un poète français", LS[7] + 0.3, hold=3.4)

# =====================================================================  S2 : La Fontaine (lignes 8-13)
t = LS[8] - 0.4
cam(t, S2)
headline(S2, 170, ["[La Fontaine], 1668"], t + 0.1, kicker="Fables · livre VI", hl_t=AL("Fontaine", 8) + 0.05, size=96)
liv = S_(S2, "livres", 1350, 420, 230, LS[8] + 0.4, rot=2)
f8 = tag(S2, 90, 430, "Un poète français", LS[8] + 0.3, "", 52)
fade(f8, AL("charretier", 8) - 0.6)
c8 = card(S2, 90, 420, "La fable", "Le charretier embourbé", AL("charretier", 8) - 0.3, w=900, size=52)
fade(liv, LS[9] - 0.4)
gone([c8], LS[9] - 0.4)
her = S_(S2, "hercule-statuette", 1500, 420, 150, AL("Hercule", 9) - 0.3, rot=2)
t9 = [tag(S2, 90, 430, "La roue s'enfonce dans la boue", AL("roue", 9) - 0.2, "", 46), tag(S2, 90, 540, "Il appelle Hercule", AL("Hercule", 9) - 0.3, "acc", 50)]
gone(t9, LS[10] - 0.4)
t10 = [tag(S2, 90, 430, "Héros de la mythologie grecque", AL("héros", 10) - 0.3, "", 46), tag(S2, 90, 540, "Adoré comme un demi-dieu", AL("demi-dieu", 10) - 0.6, "acc", 46)]
gone(t10, LS[11] - 0.4)
t11 = [tag(S2, 90, 430, "L'épaule à la roue", AL("épaule", 11) - 0.2, "", 50), tag(S2, 90, 540, "Enlever les pierres", AL("pierres", 11) - 0.2, "", 50),
       tag(S2, 90, 650, "Combler l'ornière", AL("ornière", 11) - 0.2, "acc", 50)]
gone(t11, LS[12] - 0.4)
c12 = card(S2, 90, 420, "La Fontaine · Le Charretier embourbé", "« Aide-toi, le Ciel t'aidera. »", AL("Aide-toi", 12) - 0.2, w=1000, size=54, accent=True)
gone([c12], LS[13] - 0.4)
t13 = stamp(S2, 90, 430, "Pas le Dieu d'Israël", AL("Israël", 13) - 0.3, rot=-3, size=70)
tag(S2, 90, 660, "Un dieu grec", AL("Hercule", 13, 1) - 0.1, "acc", 54)

# =====================================================================  S3 : Ésope (lignes 14-17)
t = LS[14] - 0.4
cam(t, S3)
headline(S3, 170, ["[Ésope], Grèce antique"], t + 0.1, kicker="La source de la fable", hl_t=AL("Ésope", 14) + 0.05, size=96)
S_(S3, "esope-statuette", 1500, 420, 140, AL("Ésope", 14) - 0.3, rot=-2)
t14 = tag(S3, 90, 430, "La Fontaine emprunte", AL("emprunte", 14) - 0.4, "acc", 52)
gone([t14], LS[15] - 0.4)
c15 = card(S3, 90, 420, "Dans la version d'Ésope", "Mets la main à l'ouvrage avant de prier", AL("Hercule", 15, 1) - 0.4, w=900, size=44)
gone([c15], LS[16] - 0.4)
t16 = [tag(S3, 90, 430, "Une idée très ancienne", AL("ancienne", 16) - 0.8, "", 52), tag(S3, 90, 540, "Bien avant Jésus", AL("Jésus", 16) - 0.3, "acc", 52)]
gone(t16, LS[17] - 0.4)
stamp(S3, 90, 440, "Origine : une fable grecque", AL("fable", 17) - 0.5, rot=-3, size=60)

# =====================================================================  S4 : la version anglaise (lignes 18-23)
t = LS[18] - 0.4
cam(t, S4)
headline(S4, 170, ["Version [anglaise]"], t + 0.1, kicker="Une phrase qui voyage", hl_t=AL("anglaise", 19) + 0.05, size=104)
teaser(S4, 90, 440, "La suite change le regard", LS[18] + 0.3, hold=4.6)
c19 = card(S4, 90, 420, "En anglais", "God helps those who help themselves", E("God", 19, 0.3, 0.2), w=1000, size=48)
gone([c19], LS[20] - 0.4)
c20 = card(S4, 90, 420, "George Herbert · 1651", "« Aide-toi toi-même, et Dieu t'aidera. »", E("Herbert", 20, 0.3), w=1000, size=44)
gone([c20], LS[21] - 0.4)
c21 = card(S4, 90, 420, "Algernon Sidney", "fin du XVIIe siècle · « un proverbe »", E("Sidney", 21, 0.3), w=900, size=44)
gone([c21], LS[22] - 0.4)
fr = S_(S4, "franklin", 1500, 420, 300, AL("Franklin", 22) - 0.3, rot=2)
c22 = card(S4, 90, 420, "Benjamin Franklin", "almanach · 1736", AL("Franklin", 22) - 0.2, w=700, size=52)
gone([c22], LS[23] - 0.4)
t23 = [tag(S4, 90, 430, "Imprimeur, homme pratique", AL("imprimeur", 23) - 0.3, "", 50), stamp(S4, 90, 620, "Un proverbe, pas un verset", AL("proverbe", 23) - 0.2, rot=-3, size=58)]

# =====================================================================  S5 : du proverbe au « verset » (lignes 24-27)
t = LS[24] - 0.4
cam(t, S5)
headline(S5, 170, ["Du proverbe au [« verset »]"], t + 0.1, kicker="Comment on a cru qu'elle était biblique", hl_t=AL("biblique", 25) + 0.05, size=92)
c24 = card(S5, 90, 420, "France · années 1820", "La société « Aide-toi, le ciel t'aidera »", E("société", 24, 0.3), w=1000, size=44)
gone([c24], LS[25] - 0.4)
t25 = [tag(S5, 90, 430, "Les fables", AL("fables", 25) - 0.1, "", 50), tag(S5, 90, 540, "La politique", AL("politique", 25) - 0.1, "", 50),
       tag(S5, 90, 650, "Les discours", AL("discours", 25) - 0.1, "", 50), tag(S5, 800, 430, "Les sermons", AL("sermons", 25) - 0.1, "acc", 50)]
gone(t25, LS[26] - 0.4)
t26 = tag(S5, 90, 430, "Sondages américains : une large part des croyants", AL("sondages", 26) - 0.2, "", 40)
gone([t26], LS[27] - 0.4)
s27 = stamp(S5, 90, 440, "Pas dans la Bible", AL("Résumons", 27) + 0.5, rot=-4, size=76)
t27 = [tag(S5, 90, 650, "Une fable", AL("fable", 27) - 0.1, "", 48), tag(S5, 500, 650, "Un proverbe", AL("proverbe", 27) - 0.1, "", 48),
       tag(S5, 960, 650, "De la morale pratique", AL("morale", 27) - 0.2, "acc", 48)]

# =====================================================================  S6 : l'aide de Dieu dans les Psaumes (lignes 28-35)
t = LS[28] - 0.4
cam(t, S6)
headline(S6, 170, ["L'aide de [Dieu]"], t + 0.1, kicker="Ce que dit vraiment la Bible", hl_t=AL("aide", 29) + 0.05, size=104)
t28 = tag(S6, 90, 430, "Est-ce que c'est vrai ?", E("vrai", 28, 0.4, 0.4), "acc", 54)
gone([t28], LS[29] - 0.4)
t29 = tag(S6, 90, 430, "Le texte raconte presque l'inverse", E("inverse", 29, 0.9, 0.4), "", 48)
gone([t29], LS[30] - 0.4)
c30 = put(S6, 90, 420, "<small>Mot hébreu</small><span class='heb' style='font-size:92px;margin-right:18px'>עזר</span>ézer", "card", "width:800px;font-size:70px")
blur_in(c30, AL("ézer", 30) - 0.3, 14)
t30 = tag(S6, 90, 700, "« aide » · « secours »", AL("secours", 30) - 0.4, "acc", 52)
gone([c30, t30], LS[31] - 0.4)
f31 = tag(S6, 90, 430, "Psaume 33, verset 20", LS[31] + 0.3, "", 52)
fade(f31, AL("Notre", 31) - 0.3)
kq(S6, 90, 420, "Psaume 33.20" + BIB, "« Notre âme espère en l'Éternel ; il est notre secours et notre bouclier. »", 31, "Notre", width=900, size=40, fade_at=LS[32] - 0.4)
t32 = tag(S6, 90, 430, "Le secours de ceux qui ne peuvent pas seuls", AL("seuls", 32) - 1.2, "acc", 46)
gone([t32], LS[33] - 0.4)
kq(S6, 90, 420, "Psaume 121.1-2" + BIB, "« Je lève mes yeux vers les montagnes : d'où viendra mon secours ? Mon secours vient de l'Éternel, qui a fait les cieux et la terre. »", 33, "Je", width=950, size=36, fade_at=LS[34] - 0.4)
kq(S6, 90, 420, "Psaume 46.2" + BIB, "« Dieu est pour nous un refuge et un appui, un secours qui ne manque jamais dans les détresses. »", 34, "Dieu", width=950, size=38, fade_at=LS[35] - 0.4)
stamp(S6, 90, 440, "Personne ne dit : d'abord, aide-toi", AL("Remarque", 35) + 0.3, rot=-3, size=50)
tag(S6, 90, 700, "Le secours vient de Dieu", AL("secours", 35) - 0.4, "acc", 52)

# =====================================================================  S7 : sans force, par la grâce (lignes 36-39)
t = LS[36] - 0.4
cam(t, S7)
headline(S7, 170, ["[Sans force]"], t + 0.1, kicker="Romains 5 · Éphésiens 2", hl_t=AL("force", 37) + 0.05, size=110)
S_(S7, "paul-pied", 1500, 420, 150, AL("Paul", 36) - 0.3, rot=-2)
kq(S7, 90, 420, "Romains 5.6" + BIB, "« Car, lorsque nous étions encore sans force, Christ, au temps marqué, est mort pour des impies. »", 36, "Car", width=950, size=40, fade_at=LS[37] - 0.4)
t37 = [tag(S7, 90, 430, "« Sans force »", AL("force", 37) - 0.3, "", 56), tag(S7, 90, 540, "Loin de « aide-toi »", AL("loin", 37) - 0.2, "acc", 52)]
gone(t37, LS[38] - 0.4)
kq(S7, 90, 420, "Éphésiens 2.8-9" + BIB, "« Car c'est par la grâce que vous êtes sauvés, par le moyen de la foi. Et cela ne vient pas de vous, c'est le don de Dieu. Ce n'est point par les œuvres, afin que personne ne se glorifie. »", 38, "Car", width=1000, size=34, fade_at=LS[39] - 0.4)
stamp(S7, 90, 440, "Le salut est un don", AL("don", 39) - 0.6, rot=-3, size=76)

# =====================================================================  S8 : l'effort n'est pas inutile (lignes 40-45)
t = LS[40] - 0.4
cam(t, S8)
headline(S8, 170, ["Et [l'effort] ?"], t + 0.1, kicker="Proverbes 6 · 2 Thessaloniciens 3", hl_t=AL("effort", 40) + 0.05, size=110)
S_(S8, "paul-portrait", 1500, 420, 230, AL("Paul", 43) - 0.3, rot=2)
t40 = tag(S8, 90, 430, "L'effort n'est pas inutile", E("inutile", 40, 0.6, 0.4), "acc", 52)
gone([t40], LS[41] - 0.4)
kq(S8, 90, 420, "Proverbes 6.6" + BIB, "« Va vers la fourmi, paresseux. »", 41, "Va", width=900, size=48, fade_at=LS[42] - 0.4)
t42 = [tag(S8, 90, 430, "Le travail", AL("travail", 42) - 0.2, "", 52), tag(S8, 90, 540, "La prévoyance", AL("prévoyance", 42) - 0.2, "", 52),
       tag(S8, 90, 650, "La sagesse pratique", AL("sagesse", 42) - 0.2, "acc", 52)]
gone(t42, LS[43] - 0.4)
kq(S8, 90, 420, "2 Thessaloniciens 3.10" + BIB, "« Si quelqu'un ne veut pas travailler, qu'il ne mange pas non plus. »", 43, "Si", width=900, size=42, fade_at=LS[44] - 0.4)
c44 = card(S8, 90, 420, "L'effort personnel", "n'est pas interdit", AL("interdit", 44) - 0.5, w=800, size=54)
gone([c44], LS[45] - 0.4)
t45 = [tag(S8, 90, 430, "Ceux qui refusent de travailler", AL("refusent", 45) - 0.2, "", 46), tag(S8, 90, 540, "Pas ceux qui ne peuvent pas", AL("peuvent", 45) - 0.3, "acc", 46),
       tag(S8, 90, 650, "Paul : travaillé de ses mains", AL("mains", 45) - 0.4, "", 44)]

# =====================================================================  S9 : agir ou se confier ? la mer Rouge (lignes 46-49)
t = LS[46] - 0.4
cam(t, S9)
headline(S9, 170, ["Agir ou [se confier] ?"], t + 0.1, kicker="Exode 14", hl_t=AL("confier", 46) + 0.05, size=100)
t46 = [tag(S9, 90, 430, "Agir", AL("agir", 46) - 0.1, "", 56), tag(S9, 90, 540, "Se confier à Dieu", AL("confier", 46) - 0.2, "", 56), tag(S9, 90, 650, "Les deux", AL("deux", 46) - 0.2, "acc", 56)]
gone(t46, LS[47] - 0.4)
f47 = tag(S9, 90, 430, "Premier exemple : la mer Rouge", LS[47] + 0.3, "", 50)
fade(f47, AL("L'Éternel", 47) - 0.3)
mo = S_(S9, "moise", 1500, 420, 190, LS[47] + 0.4, rot=2)
fade(mo, LS[49] - 0.4)
kq(S9, 90, 420, "Exode 14.14" + BIB, "« L'Éternel combattra pour vous ; et vous, gardez le silence. »", 47, "L'Éternel", width=900, size=42, fade_at=LS[48] - 0.4)
kq(S9, 90, 420, "Exode 14.15" + BIB, "« Pourquoi ces cris ? Parle aux enfants d'Israël, et qu'ils marchent. »", 48, "Pourquoi", width=900, size=42, fade_at=LS[49] - 0.4)
stamp(S9, 90, 440, "Un secours qui demande une réponse", E("réponse", 49, 0.8, 0.4), rot=-3, size=50)

# =====================================================================  S10 : Néhémie, Proverbes, Psaume 127 (lignes 50-57)
t = LS[50] - 0.4
cam(t, S10)
headline(S10, 170, ["[Prière] et vigilance"], t + 0.1, kicker="Néhémie · Proverbes · Psaume 127", hl_t=AL("Prière", 51) + 0.05, size=96)
nh = S_(S10, "feuillet-nehemie", 1100, 420, 270, AL("Néhémie", 50) - 0.2, rot=2)
so = S_(S10, "soldat", 1500, 420, 170, AL("gardes", 50) - 0.3, rot=-2)
gone([nh, so], LS[51] - 0.3)
t50 = [tag(S10, 90, 430, "Néhémie", AL("Néhémie", 50) - 0.1, "", 54), tag(S10, 90, 540, "Ils prient", AL("prient", 50) - 0.2, "acc", 54), tag(S10, 90, 650, "Des gardes, jour et nuit", AL("gardes", 50) - 0.2, "", 50)]
gone(t50, LS[51] - 0.3)
t51 = stamp(S10, 90, 440, "Prière + vigilance", AL("Prière", 51) - 0.1, rot=-3, size=70)
gone([t51], LS[52] - 0.4)
kq(S10, 90, 420, "Proverbes 21.31" + BIB, "« Le cheval est équipé pour le jour de la bataille, mais la délivrance appartient à l'Éternel. »", 52, "Le", width=900, size=40, fade_at=LS[53] - 0.4)
t53 = [tag(S10, 90, 430, "Le cheval", AL("cheval", 53) - 0.1, "", 50), tag(S10, 90, 540, "L'armée", AL("armée", 53) - 0.1, "", 50), tag(S10, 90, 650, "La victoire", AL("victoire", 53) - 0.2, "acc", 50)]
gone(t53, LS[54] - 0.4)
kq(S10, 90, 420, "Proverbes 16.9" + BIB, "« Le cœur de l'homme médite sa voie, mais c'est l'Éternel qui dirige ses pas. »", 54, "Le", width=900, size=42, fade_at=LS[55] - 0.4)
t55 = [tag(S10, 90, 430, "Tu planifies", AL("planifies", 55) - 0.1, "", 50), tag(S10, 90, 540, "Tu ne contrôles pas tout", AL("contrôles", 55) - 0.3, "acc", 50)]
gone(t55, LS[56] - 0.4)
kq(S10, 90, 420, "Psaume 127.1" + BIB, "« Si l'Éternel ne bâtit la maison, ceux qui la bâtissent travaillent en vain. »", 56, "Si", width=900, size=42, fade_at=LS[57] - 0.4)
tag(S10, 90, 430, "Ils bâtissent bel et bien", AL("bâtissent", 57) - 0.4, "", 50)
tag(S10, 90, 540, "Mais l'effort ne suffit pas", AL("suffit", 57) - 0.6, "acc", 50)

# =====================================================================  S11 : le vrai équilibre, les dangers (lignes 58-62)
t = LS[58] - 0.4
cam(t, S11)
headline(S11, 170, ["Le vrai [équilibre]"], t + 0.1, kicker="Ni « agis seul », ni « ne fais rien »", hl_t=AL("équilibre", 58) + 0.05, size=104)
c58 = [card(S11, 90, 420, "Le texte dit", "Agis", E("agis", 58, 0.2, 0.4), w=420, size=56), card(S11, 700, 420, "Et", "Ne mets pas ta confiance dans ton action seule", E("confiance", 58, 0.4, 1.0), w=760, size=44, accent=True)]
gone(c58, LS[59] - 0.4)
t59 = [tag(S11, 90, 430, "Pas entièrement fausse", AL("fausse", 59) - 0.4, "", 52), tag(S11, 90, 540, "Une part de sagesse pratique", AL("sagesse", 59) - 0.3, "acc", 50)]
gone(t59, LS[60] - 0.4)
s60 = stamp(S11, 90, 440, "Dangereuse si c'est une loi de Dieu", AL("dangereuse", 60) - 0.2, rot=-3, size=56)
gone([s60], LS[61] - 0.4)
S_(S11, "sym-balance", 1500, 420, 190, AL("mérite", 61) - 0.3, rot=2)
t61 = [tag(S11, 90, 430, "L'aide de Dieu se mérite ?", AL("mérite", 61) - 0.3, "", 50), tag(S11, 90, 540, "Toute la Bible parle de grâce", AL("grâce", 61) - 0.4, "acc", 50)]
gone(t61, LS[62] - 0.4)
c62 = card(S11, 90, 420, "Ce que la phrase peut sonner comme", "« Si Dieu ne t'aide pas, c'est que tu ne t'aides pas assez. »", AL("reproche", 62) - 0.3, w=1000, size=40)
t62 = tag(S11, 90, 720, "Malade · endetté · épuisé · sans travail", AL("épuisé", 62) - 0.5, "", 40)

# =====================================================================  S12 : Job, les pauvres, les soins (lignes 63-67)
t = LS[63] - 0.4
cam(t, S12)
headline(S12, 170, ["Job et [les pauvres]"], t + 0.1, kicker="Job 42 · Lévitique 19 · Proverbes 19", hl_t=AL("pauvres", 64) + 0.05, size=96)
jb = S_(S12, "job-blake", 1150, 420, 600, AL("Job", 63) - 0.2, rot=-2)
fade(jb, LS[64] - 0.4)
kq(S12, 90, 420, "Job 42.7" + BIB, "« Vous n'avez pas parlé de moi avec droiture, comme l'a fait mon serviteur Job. »", 63, "Vous", width=900, size=40, fade_at=LS[64] - 0.4)
gl = S_(S12, "glaneuses-millet", 1150, 420, 600, E("glanures", 64, 0.3, 0.4), rot=2)
fade(gl, LS[65] - 0.4)
t64 = tag(S12, 90, 430, "Laisser les glanures", E("glanures", 64, 0.3, 0.4), "acc", 52)
gone([t64], LS[65] - 0.4)
kq(S12, 90, 420, "Proverbes 19.17" + BIB, "« Celui qui a pitié du pauvre prête à l'Éternel, qui lui rendra son bienfait. »", 65, "Celui", width=900, size=40, fade_at=LS[66] - 0.4)
s66 = stamp(S12, 90, 440, "Aux autres : aidez-le", E("aidez-le", 66, 0.5, 0.4), rot=-3, size=64)
gone([s66], LS[67] - 0.4)
f67 = tag(S12, 90, 430, "Une période très lourde", LS[67] + 0.3, "", 52)
fade(f67, AL("médecin", 67) - 0.4)
t67 = [tag(S12, 90, 430, "Un médecin", AL("médecin", 67) - 0.1, "", 52), tag(S12, 90, 540, "Un psychologue", AL("psychologue", 67) - 0.1, "", 52), tag(S12, 90, 650, "Un proche", AL("proche", 67) - 0.1, "", 52),
       tag(S12, 90, 760, "La foi ne s'oppose pas aux soins", AL("soins", 67) - 0.6, "acc", 46)]

# =====================================================================  S13 : que faire de cette phrase ? (lignes 68-73)
t = LS[68] - 0.4
cam(t, S13)
headline(S13, 170, ["Que faire de [cette phrase] ?"], t + 0.1, kicker="Un proverbe, pas une promesse", hl_t=AL("phrase", 68) + 0.05, size=92)
t68 = [tag(S13, 90, 430, "Un proverbe de bon sens", AL("proverbe", 68) - 0.3, "", 52), tag(S13, 90, 540, "Agis · prépare-toi", AL("agis", 68) - 0.3, "", 52)]
gone(t68, LS[69] - 0.4)
f69 = tag(S13, 90, 430, "La promesse de Dieu", LS[69] + 0.3, "", 52)
fade(f69, AL("Mon", 69) - 0.3)
kq(S13, 90, 420, "Psaume 121.2" + BIB, "« Mon secours vient de l'Éternel. »", 69, "Mon", width=800, size=50, fade_at=LS[70] - 0.4)
tq = tag(S13, 90, 430, "Quand l'aide est venue sans la mériter ?", LS[70] + 0.4, "acc", 48)
cta = put(S13, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Dis-le en commentaire', "cta")
blur_in(cta, AL("commentaire", 70) - 1.0, 14)
sfx("click", AL("commentaire", 70) - 1.0, 0.8)
gone([tq, cta], LS[71] - 0.3)
S_(S13, "hercule-statuette", 1500, 420, 150, LS[71] + 0.3, rot=2)
t71 = [tag(S13, 90, 430, "Pousse la roue", AL("pousse", 71) - 0.2, "", 56), tag(S13, 90, 540, "Et appelle aussi", AL("appelle", 71) - 0.2, "acc", 56)]
gone(t71, LS[72] - 0.4)
stamp(S13, 90, 440, "Les deux sont permis", AL("deux", 72) - 0.3, rot=-3, size=76)

t_end = AL("Chaque", 73) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(AL("Chaque", 73) - 0.8, DUR_)]
build(
    chapters=[("01", "La phrase", 0, LS[8]), ("02", "L'origine", LS[8], LS[28]), ("03", "Ce que dit la Bible", LS[28], LS[58]), ("04", "Pour toi", LS[58], DUR_)],
    suppress=supp,
    endcard={"kicker": "Chaque semaine", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("moise-portrait", 150, 560, 300, -6), ("paul-portrait", 1550, 330, 230, 5)]},
    endcard_t=AL("Chaque", 73) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
