"""Vidéo longue « 666 : pourquoi tout ce qu'on vous a raconté est faux » — style 02, 16:9.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py), option retention, thème beige.
L'hébreu (נרון קסר) est écrit en HTML : à faire relire avant publication.
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

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - 666 - style 02", "lang": "fr",
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

# =====================================================================  S1
# S1 : le 666 avant l'Apocalypse (lignes 1-8)
cam(0, S1)
headline(S1, 170, ["Le [666], avant l'Apocalypse"], 0.0, kicker="Un nombre célèbre", hl_t=AL("666", 1) + 0.05, size=96)
S_(S1, "livres", 1500, 420, 200, 0.0, rot=2, instant=True)
t1 = tag(S1, 90, 430, "666 : bien avant l'Apocalypse", 0.3, "acc", 50)
gone([t1], LS[2] - 0.4)
c2 = card(S1, 90, 420, "1 Rois 10.14 · Salomon", "666 talents d\'or par an", AL("Rois", 2) - 0.2, w=900, size=52)
gone([c2], LS[3] - 0.4)
s3 = stamp(S1, 90, 440, "Pas le diable ?", E("diable", 3, 0.5, 0.6), rot=-3, size=72)
gone([s3], LS[4] - 0.4)
t4 = [tag(S1, 90, 430, "Que voulait dire ce nombre ?", LS[4] + 0.2, "", 50), tag(S1, 90, 540, "Tout est faux ?", AL("faux", 4) - 0.3, "acc", 56)]
gone(t4, LS[5] - 0.4)
t5 = [tag(S1, 90, 430, "Codes-barres", AL("codes-barres,", 5) - 0.2 if False else E("codes-barres", 5, 0.3, 0.4), "", 50), tag(S1, 90, 520, "Puces électroniques", AL("puces", 5) - 0.2, "", 50),
      tag(S1, 90, 610, "Cartes bancaires", AL("cartes", 5) - 0.2, "", 50), tag(S1, 90, 700, "Vaccins", AL("vaccins", 5) - 0.3, "acc", 50)]
gone(t5, LS[6] - 0.4)
t6 = [tag(S1, 90, 430, "Chaque époque, son 666", LS[6] + 0.3, "", 52), tag(S1, 90, 540, "Des objets qui n'existaient pas", AL("objets", 6) - 0.4, "acc", 48)]
gone(t6, LS[7] - 0.4)
t7 = [tag(S1, 90, 430, "Ce que dit le texte", LS[7] + 0.4, "", 52), tag(S1, 90, 540, "Ce que pensent les historiens", AL("historiens", 7) - 0.3, "", 48), tag(S1, 90, 650, "Ce qui n'est qu'une rumeur", AL("rumeur", 7) - 0.4, "acc", 50)]
gone(t7, LS[8] - 0.4)
tag(S1, 90, 430, "Plus simple", AL("simple", 8) - 0.3, "", 56)
tag(S1, 90, 540, "Plus étonnante", AL("étonnante", 8) - 0.3, "acc", 56)

# =====================================================================  S2 : un livre, une lettre (lignes 9-14)
t = LS[9] - 0.4
cam(t, S2)
headline(S2, 170, ["Un livre, une [lettre]"], t + 0.1, kicker="L\'Apocalypse", hl_t=AL("lettre.", 10) + 0.05 if False else E("lettre", 10, 0.2, 2.0), size=104)
S_(S2, "scribe", 1500, 420, 190, LS[10] + 0.2, rot=2)
t9 = tag(S2, 90, 430, "Qui l'a écrit ? Pour qui ?", LS[9] + 0.2, "acc", 52)
gone([t9], LS[10] - 0.4)
t10 = [tag(S2, 90, 430, "Jean, auteur", E("Jean", 10, 0.2, 1.0), "", 52), tag(S2, 90, 540, "Depuis l'île de Patmos", AL("Patmos", 10) - 0.3, "acc", 50)]
gone(t10, LS[11] - 0.4)
t11 = [tag(S2, 90, 430, "7 communautés chrétiennes", AL("sept", 11) - 0.2, "", 50), tag(S2, 90, 540, "Asie · Turquie actuelle", AL("Asie", 11) - 0.3, "acc", 50)]
gone(t11, LS[12] - 0.4)
t12 = [tag(S2, 90, 430, "Sous l'Empire romain", AL("Empire", 12) - 0.3, "", 52), tag(S2, 90, 540, "Minoritaires, parfois persécutés", AL("persécutés", 12) - 0.8, "acc", 48)]
gone(t12, LS[13] - 0.4)
c13 = card(S2, 90, 420, "Du grec : « révélation »", "Un genre apocalyptique", E("apocalyptique", 13, 0.4, 0.6), w=900, size=50)
gone([c13], LS[14] - 0.4)
tag(S2, 90, 430, "Des bêtes · des étoiles", AL("étoiles", 14) - 0.3, "", 48)
tag(S2, 90, 540, "Des trompettes · des nombres", AL("nombres", 14) - 0.4, "", 48)
tag(S2, 90, 650, "Il faut les déchiffrer", AL("déchiffrent", 14) - 0.6, "acc", 52)

# =====================================================================  S3 : la bête et la marque (lignes 15-18)
t = LS[15] - 0.4
cam(t, S3)
headline(S3, 170, ["La bête et la [marque]"], t + 0.1, kicker="Apocalypse 13", hl_t=AL("bête", 15) + 0.05, size=104)
t15 = [tag(S3, 90, 430, "Une bête sort de la mer", AL("bête", 15) - 0.2, "", 52), tag(S3, 90, 540, "« Qui est semblable à la bête ? »", AL("semblable", 15) - 0.6, "acc", 46)]
gone(t15, LS[16] - 0.4)
t16 = [tag(S3, 90, 430, "Une seconde bête", AL("seconde", 16) - 0.2, "", 52), tag(S3, 90, 540, "Le « faux prophète »", AL("prophète", 16) - 0.6, "acc", 52)]
gone(t16, LS[17] - 0.4)
tp17 = tag(S3, 90, 430, "Apocalypse 13.16 à 18", LS[17] + 0.3, "acc", 52)
gone([tp17], AL("elle", 17) - 0.45)
kq(S3, 90, 420, "Apocalypse 13.16-17" + BIB, "« Et elle fit que tous, petits et grands, riches et pauvres, libres et esclaves, reçussent une marque sur leur main droite ou sur leur front, et que personne ne pût acheter ni vendre, sans avoir la marque, le nom de la bête ou le nombre de son nom. »", 17, "elle", width=1000, size=34, fade_at=LS[18] - 0.4)
kq(S3, 90, 420, "Apocalypse 13.18" + BIB, "« C\'est ici la sagesse. Que celui qui a de l\'intelligence calcule le nombre de la bête. Car c\'est un nombre d\'homme, et son nombre est six cent soixante-six. »", 18, "ici", width=1000, size=38, fade_at=LS[19] - 0.4)

# =====================================================================  S4 : trois idées reçues (lignes 19-28)
t = LS[19] - 0.4
cam(t, S4)
headline(S4, 170, ["Trois idées [reçues]"], t + 0.1, kicker="Ce que dit le texte", hl_t=AL("idée", 19) + 0.05, size=104)
S_(S4, "ancien", 1500, 420, 190, LS[20] + 0.3, rot=2)
t19 = tag(S4, 90, 430, "Presque chaque mot contredit une idée reçue", LS[19] + 0.3, "acc", 44)
gone([t19], LS[20] - 0.4)
t20 = tag(S4, 90, 430, "Idée n°1 : le nombre de l'Antichrist", E("Première", 20, 0.1, 0.4), "", 48)
gone([t20], LS[21] - 0.4)
t21 = [stamp(S4, 90, 440, "Absent de l'Apocalypse", E("jamais", 21, 0.4, 1.0), rot=-3, size=60), tag(S4, 90, 620, "Seulement dans 1 et 2 Jean", AL("lettres", 21) - 0.5, "acc", 48)]
gone(t21, LS[22] - 0.4)
c22 = card(S4, 90, 420, "1 Jean 2.18" + BIB, "« il y a maintenant plusieurs antichrists »", AL("plusieurs", 22) - 0.6, w=1000, size=44)
gone([c22], LS[23] - 0.4)
t23 = [tag(S4, 90, 430, "Idée n°2 : le nombre du diable", E("Deuxième", 23, 0.1, 0.4), "", 48), card(S4, 90, 560, "Apocalypse 13.18", "« un nombre d\'homme »", AL("homme", 23) - 0.6, w=800, size=44, accent=True)]
gone(t23, LS[24] - 0.4)
t24 = [stamp(S4, 90, 440, "Pas « nombre de Satan »", AL("Satan", 24) - 0.6, rot=-3, size=60), tag(S4, 90, 620, "Un être humain", AL("humain", 24) - 0.4, "acc", 52)]
gone(t24, LS[25] - 0.4)
t25 = tag(S4, 90, 430, "Idée n°3 : un objet, une technologie", E("Troisième", 25, 0.1, 0.4), "", 46)
gone([t25], LS[26] - 0.4)
t26 = [tag(S4, 90, 430, "Un nom · une marque", LS[26] + 0.3, "", 52), tag(S4, 90, 540, "Achat et vente", AL("achat", 26) - 0.3, "", 52), stamp(S4, 90, 720, "Aucun objet", AL("électronique", 26) - 0.5, rot=-3, size=60)]
gone(t26, LS[27] - 0.4)
t27 = [tag(S4, 90, 430, "Papes · Napoléon · dictateurs", AL("papes", 27) - 0.3, "", 48), tag(S4, 90, 540, "Puis les ordinateurs", AL("ordinateurs", 27) - 0.5, "acc", 52)]
gone(t27, LS[28] - 0.4)
stamp(S4, 90, 440, "Toutes ont échoué", E("échoué", 28, 0.4, 0.6), rot=-3, size=64)
tag(S4, 90, 620, "Un nombre pour tous ne désigne personne", AL("personne", 28) - 0.9, "acc", 44)

# =====================================================================  S5 : calculer un nom (lignes 29-34)
t = LS[29] - 0.4
cam(t, S5)
headline(S5, 170, ["Calculer un [nom]"], t + 0.1, kicker="La gématrie", hl_t=AL("calculer", 29) + 0.05, size=104)
S_(S5, "rouleau", 1500, 420, 220, LS[30] + 0.3, rot=2)
t29 = tag(S5, 90, 430, "« Calculez »", LS[29] + 0.3, "acc", 60)
gone([t29], LS[30] - 0.4)
t30 = [tag(S5, 90, 430, "Chaque lettre = un chiffre", AL("valeur", 30) - 0.7, "", 52), tag(S5, 90, 540, "Grec · hébreu", AL("hébreu", 30) - 0.3, "acc", 52)]
gone(t30, LS[31] - 0.4)
c31 = card(S5, 90, 420, "La gématrie", "un nom → un nombre", AL("gématrie", 31) - 0.4, w=900, size=52)
gone([c31], LS[32] - 0.4)
t32 = [tag(S5, 90, 430, "Quel nom donne 666 ?", LS[32] + 0.2, "", 52), stamp(S5, 90, 570, "Néron César", AL("César", 32) - 0.5, rot=-3, size=72)]
gone(t32, LS[33] - 0.3)
c33 = put(S5, 90, 420, "<small>Néron César, en hébreu</small><span class='heb' style='font-size:130px'>נרון קסר</span>", "card", "width:1000px;font-size:46px")
blur_in(c33, AL("hébraïques", 33) - 0.3, 14)
v33 = tag(S5, 90, 730, "50 · 200 · 6 · 50 — 100 · 60 · 200", AL("nun", 33) + 0.2, "acc", 50)
gone([c33, v33], LS[34] - 0.4)
counter(S5, 90, 420, 0, 666, AL("Additionnez", 34) + 1.5, 1.2, unit="", size=230)
tag(S5, 90, 700, "50 + 200 + 6 + 50 + 100 + 60 + 200", AL("Additionnez", 34) + 0.2, "", 44)

# =====================================================================  S6 : Néron César (lignes 35-43)
t = LS[35] - 0.4
cam(t, S6)
headline(S6, 170, ["L'hypothèse [Néron]"], t + 0.1, kicker="Un calcul, un nom", hl_t=AL("616", 35) + 0.05, size=104)
S_(S6, "soldat", 1500, 420, 150, LS[39] + 0.3, rot=2)
t35 = [stamp(S6, 90, 440, "616 !", E("616", 35, 0.2, 0.6), rot=-3, size=90), tag(S6, 90, 620, "Des manuscrits très anciens", AL("manuscrits", 35) - 0.4, "acc", 50)]
gone(t35, LS[36] - 0.4)
tf36 = tag(S6, 90, 430, "Même calcul, autre orthographe", LS[36] + 0.3, "", 50)
gone([tf36], AL("dernière", 36) - 0.55)
t36 = [tag(S6, 90, 430, "Néron sans la dernière lettre", AL("dernière", 36) - 0.5, "", 50), tag(S6, 90, 540, "= 616", AL("616", 36, 0) - 0.4, "acc", 60)]
gone(t36, LS[37] - 0.4)
tf37 = tag(S6, 90, 430, "Une variante bien attestée", LS[37] + 0.3, "", 50)
gone([tf37], AL("papyrus", 37) - 0.45)
c37 = card(S6, 90, 420, "Papyrus", "IIIe ou IVe siècle", AL("papyrus", 37) - 0.4, w=800, size=52)
gone([c37], LS[38] - 0.4)
tf38 = tag(S6, 90, 430, "Un argument sérieux", LS[38] + 0.3, "", 52)
gone([tf38], AL("hypothèse", 38) - 0.5)
t38 = [stamp(S6, 90, 440, "Hypothèse", AL("hypothèse", 38) - 0.4, rot=-3, size=80), tag(S6, 90, 620, "Pas une certitude", AL("certitude", 38) - 0.4, "acc", 52), tag(S6, 90, 730, "Irénée connaît déjà 616", AL("Irénée", 38) - 0.3, "", 46)]
gone(t38, LS[39] - 0.4)
t39 = [tag(S6, 90, 430, "Pourquoi Néron ?", LS[39] + 0.2, "", 56), tag(S6, 90, 540, "Il représente déjà la bête", AL("bête", 39) - 0.5, "acc", 50)]
gone(t39, LS[40] - 0.4)
t40 = [tag(S6, 90, 430, "64 : incendie de Rome", AL("64", 40) - 0.2, "", 50), tag(S6, 90, 540, "Tacite : les chrétiens accusés", AL("Tacite", 40) - 0.3, "acc", 46)]
gone(t40, LS[41] - 0.4)
t41 = [tag(S6, 90, 430, "68 : mort de Néron", AL("68", 41) - 0.2, "", 50), tag(S6, 90, 540, "La rumeur : il reviendra", AL("reviendra", 41) - 0.6, "", 50), tag(S6, 90, 650, "Bête blessée, puis guérie", AL("guérie", 41) - 0.6, "acc", 48)]
gone(t41, LS[42] - 0.4)
c42 = card(S6, 90, 420, "Première révélation", "Une énigme pour des lecteurs précis", AL("révélation", 42) - 0.4, w=1000, size=48)
gone([c42], LS[43] - 0.4)
tag(S6, 90, 430, "Restez : la marque, puis le six", LS[43] + 0.3, "acc", 48)

# =====================================================================  S7 : la date (lignes 44-46)
t = LS[44] - 0.4
cam(t, S7)
headline(S7, 170, ["La [date] discutée"], t + 0.1, kicker="Apocalypse", hl_t=AL("date", 44) + 0.05, size=104)
S_(S7, "porte-ville", 1450, 420, 300, LS[44] + 0.5, rot=2)
t44 = tag(S7, 90, 430, "La date est discutée", LS[44] + 0.2, "acc", 56)
gone([t44], LS[45] - 0.4)
t45 = [tag(S7, 90, 430, "Tradition : vers 95 · Domitien", AL("95", 45) - 0.3, "", 48), tag(S7, 90, 540, "D'autres : vers 68-70", AL("68", 45) - 0.4, "acc", 52)]
gone(t45, LS[46] - 0.4)
tag(S7, 90, 430, "Domitien ou l'Empire", AL("Domitien", 46) - 0.3, "", 52)
tag(S7, 90, 540, "Néron, un modèle", AL("modèle", 46) - 0.4, "", 52)
tag(S7, 90, 650, "Toujours : le pouvoir romain", AL("romain", 46) - 0.4, "acc", 50)

# =====================================================================  S8 : la marque (lignes 47-51)
t = LS[47] - 0.4
cam(t, S8)
headline(S8, 170, ["La [marque]"], t + 0.1, kicker="Apocalypse 13", hl_t=AL("marque", 47) + 0.05, size=112)
S_(S8, "foule", 1250, 500, 250, LS[48] + 0.3, rot=-2)
t47 = [tag(S8, 90, 430, "Le culte de l'empereur", AL("culte", 47) - 0.3, "", 52), tag(S8, 90, 540, "Temples · statues · serments", AL("serments", 47) - 0.5, "acc", 48)]
gone(t47, LS[48] - 0.4)
t48 = [tag(S8, 90, 430, "Métiers en associations", AL("associations", 48) - 0.4, "", 50), tag(S8, 90, 540, "Refuser = perdre son travail", AL("travail", 48) - 0.6, "acc", 48)]
gone(t48, LS[49] - 0.4)
t49 = [stamp(S8, 90, 440, "Ni acheter ni vendre", AL("acheter", 49) - 0.3, rot=-3, size=60), tag(S8, 90, 620, "Un signe d'allégeance", AL("allégeance", 49) - 0.5, "acc", 52)]
gone(t49, LS[50] - 0.4)
c50 = card(S8, 90, 420, "Deutéronome 6.8", "« un signe sur la main, entre les yeux »", AL("Deutéronome", 50) - 0.3, w=900, size=44)
gone([c50], LS[51] - 0.4)
t51 = [tag(S8, 90, 430, "Marque de la bête", E("aussitôt", 51, 0.2, 0.6), "", 52), tag(S8, 90, 540, "Nom de l'Agneau sur le front", AL("Agneau", 51) - 0.4, "acc", 48), stamp(S8, 90, 680, "Deux fidélités", AL("fidélités", 51) - 0.5, rot=-3, size=60)]

# =====================================================================  S9 : pourquoi six ? (lignes 52-55)
t = LS[52] - 0.4
cam(t, S9)
headline(S9, 170, ["Pourquoi [six] ?"], t + 0.1, kicker="Genèse 1", hl_t=AL("six", 52) + 0.05, size=112)
S_(S9, "livres", 1500, 420, 200, LS[53] + 0.3, rot=2)
t52 = [tag(S9, 90, 430, "Pourquoi 6-6-6 ?", LS[52] + 0.2, "", 56), tag(S9, 90, 540, "Et chez Salomon ?", AL("Salomon", 52) - 0.3, "acc", 52)]
gone(t52, LS[53] - 0.4)
c53 = card(S9, 90, 420, "Genèse 1", "L'humain est créé le sixième jour", AL("Genèse", 53) - 0.3, w=1000, size=48)
gone([c53], LS[54] - 0.4)
t54 = [tag(S9, 90, 430, "7 jours · 7 églises", AL("sept", 54) - 0.2, "", 50), tag(S9, 90, 540, "7 sceaux · 7 trompettes", AL("trompettes", 54) - 0.5, "", 50), stamp(S9, 90, 710, "Le 7 : la plénitude", AL("plénitude", 54) - 0.4, rot=-3, size=60)]
gone(t54, LS[55] - 0.4)
t55 = [tag(S9, 90, 430, "6 : l'humain, limité ?", AL("humain", 55) - 0.5, "", 52), stamp(S9, 90, 560, "Lecture courante", AL("courante", 55) - 0.4, rot=-3, size=60), tag(S9, 90, 720, "Aucun verset ne l'énonce", AL("verset", 55) - 0.5, "acc", 50)]

# =====================================================================  S10 : Salomon et Nebucadnetsar (lignes 56-61)
t = LS[56] - 0.4
cam(t, S10)
headline(S10, 170, ["Deux scènes, le [six]"], t + 0.1, kicker="1 Rois 10 · Daniel 3", hl_t=AL("scènes", 56) + 0.05, size=104)
S_(S10, "sym-balance", 1450, 420, 260, LS[57] + 0.5, rot=2)
t56 = tag(S10, 90, 430, "Deux scènes où le six revient", LS[56] + 0.2, "acc", 52)
gone([t56], LS[57] - 0.4)
c57 = card(S10, 90, 420, "1 Rois 10.14 · Salomon", "666 talents d'or par an", AL("talents", 57) - 0.5, w=900, size=50)
t57 = [tag(S10, 90, 640, "≈ 20 tonnes d'or", AL("tonnes", 57) - 0.4, "acc", 52), tag(S10, 90, 750, "Deutéronome 17 : pas d'or accumulé", AL("Deutéronome", 57) - 0.3, "", 40)]
gone([c57] + t57, LS[58] - 0.4)
t58 = [tag(S10, 90, 430, "Des chevaux d'Égypte", AL("Égypte", 58) - 0.3, "", 52), tag(S10, 90, 540, "Des centaines d'épouses", AL("femmes", 58) - 0.4, "", 52), tag(S10, 90, 650, "L'or accumulé", AL("accumule", 58) - 0.5, "acc", 52)]
gone(t58, LS[59] - 0.4)
c59 = card(S10, 90, 420, "Daniel 3.1 · Nebucadnetsar", "Une statue d'or : 60 coudées × 6", AL("Daniel", 59) - 0.3, w=1000, size=46)
s59 = stamp(S10, 90, 660, "Se prosterner ou mourir", AL("prosterner", 59) - 0.5, rot=-3, size=60)
gone([c59, s59], LS[60] - 0.4)
t60 = [tag(S10, 90, 430, "Un pouvoir exige l'adoration", AL("adoration", 60) - 0.5, "", 50), tag(S10, 90, 540, "Des fidèles refusent", AL("fidèles", 60) - 0.4, "acc", 52)]
gone(t60, LS[61] - 0.4)
stamp(S10, 90, 440, "Une piste, pas une preuve", AL("preuve", 61) - 0.8, rot=-3, size=56)
tag(S10, 90, 620, "Jean y pensait ? Personne ne peut l'affirmer", AL("pensait", 61) - 0.3, "", 42)

# =====================================================================  S11 : le sens des nombres (lignes 62-66)
t = LS[62] - 0.4
cam(t, S11)
headline(S11, 170, ["Les nombres ont un [sens]"], t + 0.1, kicker="Écouter les échos", hl_t=AL("solide", 62) + 0.05, size=96)
S_(S11, "veilleur", 1500, 420, 200, LS[63] + 0.3, rot=2)
tf62 = tag(S11, 90, 430, "Ce qui est solide", LS[62] + 0.3, "acc", 56)
gone([tf62], AL("code", 62) - 0.55)
t62 = [tag(S11, 90, 430, "Pas de code caché", AL("code", 62) - 0.5, "", 52), tag(S11, 90, 540, "Des échos du texte", AL("échos", 62) - 0.4, "acc", 52)]
gone(t62, LS[63] - 0.4)
t63 = [tag(S11, 90, 430, "Les lectures vers l'avenir : fausses ?", LS[63] + 0.2, "", 46), stamp(S11, 90, 570, "Non", E("Non", 63, 0.2, 0.9), rot=-3, size=90)]
gone(t63, LS[64] - 0.4)
t64 = [tag(S11, 90, 430, "Le premier siècle", AL("premier", 64) - 0.3, "", 50), tag(S11, 90, 540, "L'histoire de l'Église", AL("Église", 64) - 0.3, "", 50), tag(S11, 90, 650, "Une période finale", AL("finale", 64) - 0.4, "acc", 50)]
gone(t64, LS[65] - 0.4)
t65 = [tag(S11, 90, 430, "Pas de camp à choisir", AL("camp", 65) - 0.4, "", 52), tag(S11, 90, 540, "Le texte ≠ ce qu'on y projette", AL("projeté", 65) - 0.7, "acc", 46)]
gone(t65, LS[66] - 0.4)
c66 = card(S11, 90, 420, "Matthieu 24.4" + BIB, "« Prenez garde que personne ne vous séduise »", AL("Matthieu", 66) - 0.3, w=1000, size=42)
tag(S11, 90, 650, "Vigilance, pas panique", AL("vigilance", 66) - 0.4, "acc", 52)

# =====================================================================  S12 : quand le nombre fait peur (lignes 67-71)
t = LS[67] - 0.4
cam(t, S12)
headline(S12, 170, ["Quand le nombre fait [peur]"], t + 0.1, kicker="Application", hl_t=AL("angoissées", 67) + 0.05, size=100)
S_(S12, "pere", 1500, 420, 190, LS[68] + 0.3, rot=2)
t67 = [tag(S12, 90, 430, "Peur de la fin des temps", LS[67] + 0.4, "", 52), tag(S12, 90, 540, "Peur de « recevoir la marque »", AL("marque", 67) - 0.5, "acc", 48)]
gone(t67, LS[68] - 0.4)
t68 = [stamp(S12, 90, 440, "Écrit pour consoler", AL("consoler", 68) - 0.4, rot=-3, size=64), tag(S12, 90, 620, "Pas pour terroriser", AL("terroriser", 68) - 0.5, "acc", 52)]
gone(t68, LS[69] - 0.4)
t69a = tag(S12, 90, 430, "Une bénédiction pour celui qui lit", AL("bénédiction", 69) - 0.3, "", 48)
gone([t69a], AL("essuiera", 69) - 0.5)
c69 = card(S12, 90, 420, "Apocalypse 21.4" + BIB, "« Dieu essuiera toute larme de leurs yeux »", AL("essuiera", 69) - 0.3, w=1000, size=42)
gone([c69], LS[70] - 0.4)
t70 = [tag(S12, 90, 430, "Un proche", AL("proche", 70) - 0.3, "", 52), tag(S12, 90, 540, "Un pasteur", AL("pasteur", 70) - 0.3, "", 52), tag(S12, 90, 650, "Un professionnel de santé", AL("professionnel", 70) - 0.4, "acc", 52),
       stamp(S12, 90, 770, "Pas un manque de foi", AL("foi", 70) - 0.5, rot=-3, size=52)]
gone(t70, LS[71] - 0.4)
tq = tag(S12, 90, 430, "Quelle crainte vous a marqué ?", LS[71] + 0.4, "acc", 50)
cta = put(S12, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Dites-le en commentaire', "cta")
blur_in(cta, AL("commentaire", 71) - 1.0, 14)
sfx("click", AL("commentaire", 71) - 1.0, 0.8)
gone([tq, cta], LS[72] - 0.3)

# =====================================================================  S13 : conclusion (lignes 72-77)
t = LS[72] - 0.4
cam(t, S13)
headline(S13, 170, ["Tant de [faux] sur le 666"], t + 0.1, kicker="La réponse", hl_t=AL("fausses", 72) + 0.05, size=100)
S_(S13, "scribe", 1500, 420, 190, LS[75] + 0.3, rot=2)
t72 = tag(S13, 90, 430, "Pourquoi tant de faux ?", LS[72] + 0.3, "acc", 56)
gone([t72], LS[73] - 0.4)
t73 = [tag(S13, 90, 430, "Un nombre mystérieux", AL("mystérieux", 73) - 0.4, "", 52), tag(S13, 90, 540, "Les peurs de chaque époque", AL("peurs", 73) - 0.4, "acc", 50)]
gone(t73, LS[74] - 0.4)
tf74 = tag(S13, 90, 430, "Le texte est plus sobre", LS[74] + 0.3, "", 52)
gone([tf74], AL("homme", 74) - 0.45)
t74 = [tag(S13, 90, 430, "Un nombre d'homme", AL("homme", 74) - 0.3, "", 52), tag(S13, 90, 540, "Un nom à calculer", AL("calculer", 74) - 0.3, "", 52), tag(S13, 90, 650, "Une marque : à qui l'on appartient", AL("marque", 74) - 0.3, "acc", 48)]
gone(t74, LS[75] - 0.4)
t75 = [stamp(S13, 90, 440, "Pas un code à craindre", AL("code", 75) - 0.4, rot=-3, size=60), tag(S13, 90, 620, "Une loyauté qui n'est due qu'à Dieu", AL("loyauté", 75) - 0.6, "acc", 46)]
gone(t75, LS[76] - 0.4)
t76 = [tag(S13, 90, 430, "Qui est le public ?", AL("public", 76) - 0.3, "", 52), tag(S13, 90, 540, "Quel contexte ?", AL("contexte", 76) - 0.3, "", 52), tag(S13, 90, 650, "Que dit le verset ?", AL("verset", 76) - 0.3, "acc", 52)]
gone(t76, LS[77] - 0.3)

t_end = AL("Chaque", 77) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(AL("Chaque", 77) - 0.8, DUR_)]
build(
    chapters=[("01", "Le mythe", 0, LS[9]), ("02", "Le texte", LS[9], LS[29]), ("03", "Néron", LS[29], LS[52]), ("04", "Le six", LS[52], LS[67]), ("05", "Pour vous", LS[67], DUR_)],
    suppress=supp,
    endcard={"kicker": "Chaque semaine", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("scribe", 150, 560, 280, -6), ("jesus-portrait", 1550, 330, 230, 5)]},
    endcard_t=AL("Chaque", 77) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
