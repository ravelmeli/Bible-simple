"""Vidéo longue « Nicodème : l'homme qui visitait Jésus la nuit, jusqu'au jour où il n'a plus eu peur » — style 02, 16:9.

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

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Nicodème - style 02", "lang": "fr",
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

# =====================================================================  S1 : l'homme de la nuit (lignes 1-7)
cam(0, S1)
headline(S1, 170, ["Nicodème, l'homme de [la nuit]"], 0.0, kicker="Évangile de Jean", hl_t=AL("nuit", 1) + 0.05, size=96)
S_(S1, "veilleur", 1500, 420, 200, 0.0, rot=2, instant=True)
t1 = tag(S1, 90, 430, "Les autres : en plein jour", AL("plein", 1) - 0.2, "", 50)
gone([t1], AL("Lui", 1) - 0.3)
tl = tag(S1, 90, 540, "Lui : de nuit", AL("Lui", 1) - 0.2, "acc", 56)
gone([tl], LS[2] - 0.4)
t2 = [tag(S1, 90, 430, "Riche en savoir", AL("riche", 2) - 0.1, "", 52), tag(S1, 90, 540, "Respecté", AL("respecté", 2) - 0.1, "", 52), tag(S1, 90, 650, "Attaché à son rang", AL("rang", 2) - 0.4, "acc", 52)]
gone(t2, LS[3] - 0.4)
t3 = tag(S1, 90, 430, "Frapper en secret à la porte de Jésus", AL("secret", 3) - 0.4, "acc", 48)
gone([t3], LS[4] - 0.4)
t4 = [tag(S1, 90, 430, "Qui est cet homme ?", AL("Qui", 4) - 0.1, "", 52), tag(S1, 90, 540, "Pourquoi de nuit ?", AL("Pourquoi", 4) - 0.1, "", 52), tag(S1, 90, 650, "Que lui arrive-t-il ?", AL("arrive-t-il", 4) - 0.3, "acc", 52)]
gone(t4, LS[5] - 0.4)
t5 = [tag(S1, 90, 430, "Une visite de nuit", AL("visite", 5) - 0.2, "", 52), tag(S1, 90, 540, "Une phrase en plein conseil", AL("conseil", 5) - 0.4, "", 50), tag(S1, 90, 650, "Un enterrement", AL("enterrement", 5) - 0.3, "acc", 52)]
gone(t5, LS[6] - 0.4)
c6 = card(S1, 90, 420, "Un portrait propre à Jean", "Jean 3 · Jean 7 · Jean 19", AL("Jean", 6, 1) - 0.3, w=900, size=52)
gone([c6], LS[7] - 0.4)
tag(S1, 90, 430, "Entre la première scène et la dernière…", LS[7] + 0.3, "acc", 46)
tag(S1, 90, 540, "…quelque chose change", E("change", 7, 0.4, 3.0), "", 52)

# =====================================================================  S2 : le décor, qui est Nicodème (lignes 8-14)
t = LS[8] - 0.4
cam(t, S2)
headline(S2, 170, ["[Jérusalem], la Pâque"], t + 0.1, kicker="Au premier siècle", hl_t=AL("Jérusalem", 8) + 0.05, size=104)
vi = S_(S2, "ville", 1450, 420, 300, LS[8] + 0.2, rot=2)
fade(vi, LS[11] - 0.4)
t9 = [tag(S2, 90, 430, "Il chasse les marchands du temple", AL("marchands", 9) - 0.3, "", 46), tag(S2, 90, 540, "Il fait des signes", AL("signes", 9) - 0.3, "acc", 52)]
gone(t9, LS[10] - 0.4)
fo = S_(S2, "foule", 1100, 560, 300, AL("pèlerins", 10) - 0.3, rot=-2)
t10 = tag(S2, 90, 430, "Qui est ce Galiléen ?", AL("Galiléen", 10) - 0.4, "acc", 52)
gone([t10, fo], LS[11] - 0.4)
S_(S2, "nicodeme-tete", 1500, 420, 190, E("Nicodème", 11, 0.3, 0.3), rot=2)
c11 = card(S2, 90, 420, "Jean 3.1" + BIB, "« un homme d\'entre les pharisiens, nommé Nicodème, un chef des Juifs »", E("pharisiens", 11, 0.5, 0.4), w=1000, size=40)
gone([c11], LS[12] - 0.4)
t12 = [tag(S2, 90, 430, "Les pharisiens", AL("pharisiens", 12) - 0.2, "", 52), tag(S2, 90, 540, "La loi de Moïse, au quotidien", AL("quotidien", 12) - 0.8, "acc", 46)]
gone(t12, LS[13] - 0.4)
t13 = [tag(S2, 90, 430, "Chef des Juifs", AL("chef", 13) - 0.1, "", 52), tag(S2, 90, 540, "Le conseil : le Sanhédrin", AL("Sanhédrin", 13) - 0.4, "acc", 50), tag(S2, 90, 650, "Un notable, prudent", AL("notable", 13) - 0.2, "", 50)]
gone(t13, LS[14] - 0.4)
c14 = card(S2, 90, 420, "Un nom grec", "Nicodème : « vainqueur du peuple »", AL("vainqueur", 14) - 0.5, w=900, size=46)

# =====================================================================  S3 : pourquoi de nuit ? (lignes 15-21)
t = LS[15] - 0.4
cam(t, S3)
headline(S3, 170, ["Pourquoi [de nuit] ?"], t + 0.1, kicker="Jean 3.2", hl_t=AL("nuit", 16) + 0.05, size=104)
t15 = tag(S3, 90, 430, "Il vient trouver Jésus", LS[15] + 0.2, "acc", 52)
gone([t15], LS[16] - 0.4)
t16 = tag(S3, 90, 430, "Le texte ne le dit pas", AL("dit", 16) - 0.8, "", 56)
gone([t16], LS[17] - 0.4)
t17 = [tag(S3, 90, 430, "Peur du regard des collègues ?", AL("craignait", 17) - 0.3, "", 46), tag(S3, 90, 540, "Une conversation calme ?", AL("calme", 17) - 0.4, "", 46), tag(S3, 90, 650, "Un symbole ?", AL("symbole", 17) - 0.3, "acc", 50)]
gone(t17, LS[18] - 0.4)
sh = stamp(S3, 90, 440, "Des hypothèses", AL("hypothèses", 18) - 0.4, rot=-3, size=70)
sn = S_(S3, "nicodeme", 1500, 420, 190, LS[18] + 0.3, rot=2)
gone([sh, sn], LS[19] - 0.4)
f19 = tag(S3, 90, 430, "Chez Jean : lumière et ténèbres", LS[19] + 0.3, "acc", 50)
kq3 = None
kq(S3, 90, 420, "Jean 1.5" + BIB, "« La lumière luit dans les ténèbres, et les ténèbres ne l\'ont point reçue. »", 19, "La", n=1, width=900, size=42, fade_at=LS[20] - 0.4)
f20 = tag(S3, 90, 430, "Judas quitte la table", LS[20] + 0.3, "", 52)
fade(f19, AL("La", 19, 1) - 0.3)
kq(S3, 90, 420, "Jean 13.30" + BIB, "« Il était nuit. »", 20, "Il", n=1, width=600, size=54, last=AL("nuit", 20) + 0.6, fade_at=AL("nuit", 20) + 1.2)
fade(f20, AL("Il", 20, 1) - 0.3)
tag(S3, 90, 660, "La nuit : un état du cœur ?", AL("cœur", 20) - 0.5, "acc", 46)

# =====================================================================  S4 : Rabbi (lignes 22-24)
t = LS[22] - 0.4
cam(t, S4)
headline(S4, 170, ["« [Rabbi], nous savons »"], t + 0.1, kicker="Jean 3.2", hl_t=AL("Rabbi", 22) + 0.05, size=100)
S_(S4, "christ-nicodeme-dessin", 1500, 420, 250, LS[22] + 0.4, rot=2)
kq(S4, 90, 420, "Jean 3.2" + BIB, "« Rabbi, nous savons que tu es un docteur venu de Dieu ; car personne ne peut faire ces miracles que tu fais, si Dieu n\'est avec lui. »", 22, "Rabbi", width=950, size=36, fade_at=LS[23] - 0.4)
t23 = [tag(S4, 90, 430, "« Nous » : d\'autres avec lui", AL("nous", 23) - 0.3, "acc", 50), tag(S4, 90, 540, "Des gens impressionnés, dans l\'élite", AL("élite", 23) - 0.5, "", 44)]
gone(t23, LS[24] - 0.4)
t24 = [tag(S4, 90, 430, "Rabbi : « mon maître »", AL("maître", 24) - 0.5, "", 52), tag(S4, 90, 540, "Un notable devant un artisan", AL("artisan", 24) - 0.4, "acc", 48)]

# =====================================================================  S5 : naître de nouveau (lignes 25-28)
t = LS[25] - 0.4
cam(t, S5)
headline(S5, 170, ["Naître [de nouveau]"], t + 0.1, kicker="Jean 3.3-4", hl_t=AL("nouveau", 25) + 0.05, size=104)
S_(S5, "jesus-pied", 1500, 420, 220, LS[25] + 0.3, rot=2)
kq(S5, 90, 420, "Jean 3.3" + BIB, "« En vérité, en vérité, je te le dis, si un homme ne naît de nouveau, il ne peut voir le royaume de Dieu. »", 25, "En", width=950, size=40, fade_at=LS[26] - 0.4)
c26 = put(S5, 90, 420, "<small>Mot grec</small><span style=\'font-size:84px\'>ἄνωθεν</span> anôthen", "card", "width:900px;font-size:66px")
blur_in(c26, AL("anôthen", 26) - 0.3, 14)
t26 = [tag(S5, 90, 700, "« de nouveau »", AL("nouveau", 26) - 0.3, "", 52), tag(S5, 560, 700, "« d\'en haut »", AL("haut", 26) - 0.3, "acc", 52)]
gone([c26] + t26, LS[27] - 0.4)
kq(S5, 90, 420, "Jean 3.4" + BIB, "« Comment un homme peut-il naître quand il est vieux ? Peut-il rentrer dans le sein de sa mère et naître une seconde fois ? »", 27, "Comment", width=950, size=38, fade_at=LS[28] - 0.4)
t28 = [tag(S5, 90, 430, "Il prend les mots au sérieux", AL("sérieux", 28) - 0.4, "", 50), stamp(S5, 90, 620, "Le mot est ambigu", AL("ambigu", 28) - 0.3, rot=-3, size=64)]

# =====================================================================  S6 : eau, Esprit, vent (lignes 29-35)
t = LS[29] - 0.4
cam(t, S6)
headline(S6, 170, ["[L\'Esprit] et le vent"], t + 0.1, kicker="Jean 3.5-10", hl_t=AL("Esprit", 31) + 0.05, size=104)
kq(S6, 90, 420, "Jean 3.5" + BIB, "« En vérité, en vérité, je te le dis, si un homme ne naît d\'eau et d\'Esprit, il ne peut entrer dans le royaume de Dieu. »", 29, "En", width=950, size=40, fade_at=LS[30] - 0.4)
c30 = card(S6, 90, 420, "Une naissance", "reçue, comme un don, et non gagnée", E("don", 30, 0.6, 0.4), w=900, size=46)
gone([c30], LS[31] - 0.4)
kq(S6, 90, 420, "Jean 3.8" + BIB, "« Le vent souffle où il veut, et tu en entends le bruit ; mais tu ne sais d\'où il vient, ni où il va. Il en est ainsi de tout homme qui est né de l\'Esprit. »", 31, "Le", width=1000, size=36, fade_at=LS[32] - 0.4)
c32 = card(S6, 90, 420, "Mot grec", "<b>pneuma</b> : vent · Esprit", AL("pneuma", 32) - 0.3, w=800, size=52)
t32 = tag(S6, 90, 640, "Comme le mot hébreu ruach", AL("ruach", 32) - 0.5, "acc", 46)
gone([c32, t32], LS[33] - 0.4)
c33 = card(S6, 90, 420, "Nicodème, déconcerté", "« Comment cela peut-il se faire ? »", AL("Comment", 33) - 0.4, w=900, size=46)
gone([c33], LS[34] - 0.4)
kq(S6, 90, 420, "Jean 3.10" + BIB, "« Tu es le docteur d\'Israël, et tu ne sais pas ces choses ! »", 34, "Tu", width=900, size=44, fade_at=LS[35] - 0.4)
stamp(S6, 90, 440, "Un choc", AL("choc", 35) - 0.3, rot=-4, size=84)
tag(S6, 90, 640, "Ce qu\'il croyait maîtriser lui échappe", AL("échappe", 35) - 0.8, "acc", 46)

# =====================================================================  S7 : le serpent, Jean 3.16 (lignes 36-39)
t = LS[36] - 0.4
cam(t, S7)
headline(S7, 170, ["Le serpent [élevé]"], t + 0.1, kicker="Jean 3.14-16 · Nombres 21", hl_t=AL("serpent", 36) + 0.05, size=104)
se = S_(S7, "serpent-airain", 1500, 420, 200, AL("serpent", 37) - 0.3, rot=2)
kq(S7, 90, 420, "Jean 3.14-15" + BIB, "« Comme Moïse éleva le serpent dans le désert, il faut de même que le Fils de l\'homme soit élevé, afin que quiconque croit en lui ait la vie éternelle. »", 36, "Comme", width=1000, size=36, fade_at=LS[37] - 0.4)
t37 = [tag(S7, 90, 430, "Nombres 21", AL("Nombres", 37) - 0.2, "", 52), tag(S7, 90, 540, "Un serpent de bronze sur une perche", AL("perche", 37) - 0.8, "acc", 46)]
gone(t37, LS[38] - 0.4)
kq(S7, 90, 420, "Jean 3.16" + BIB, "« Car Dieu a tant aimé le monde qu\'il a donné son Fils unique, afin que quiconque croit en lui ne périsse point, mais qu\'il ait la vie éternelle. »", 38, "Car", width=1000, size=36, fade_at=LS[39] - 0.4)
tag(S7, 90, 430, "Où s\'arrête la parole de Jésus ?", AL("s\'arrête", 39) - 0.4, "", 48)
tag(S7, 90, 540, "Le sens général reste le même", AL("sens", 39) - 0.3, "acc", 48)

# =====================================================================  S8 : le silence (lignes 40-42)
t = LS[40] - 0.4
cam(t, S8)
headline(S8, 170, ["Un [silence]"], t + 0.1, kicker="Fin de la scène", hl_t=AL("Rien", 40) + 0.05, size=110)
t40 = [tag(S8, 90, 430, "Il ne dit pas qu\'il croit", E("croit", 40, 0.3, 0.5), "", 50), tag(S8, 90, 540, "Ni qu\'il refuse", AL("refuse", 40) - 0.3, "", 50), tag(S8, 90, 650, "Ni qu\'il repart", AL("repart", 40) - 0.3, "acc", 50)]
gone(t40, LS[41] - 0.4)
t41 = [stamp(S8, 90, 440, "Pas de conversion", E("conversion", 41, 0.5, 0.4), rot=-3, size=70), tag(S8, 90, 650, "Elle se termine par un silence", AL("silence", 41) - 0.5, "acc", 50)]
gone(t41, LS[42] - 0.4)
tag(S8, 90, 430, "Des mois, peut-être des années", E("années", 42, 0.8, 0.4), "", 50)

# =====================================================================  S9 : Jean 7, la défense (lignes 43-53)
t = LS[43] - 0.4
cam(t, S9)
headline(S9, 170, ["Il prend [la parole]"], t + 0.1, kicker="Jean 7 · la fête des Tentes", hl_t=AL("Nicodème", 46) + 0.05, size=104)
t43 = tag(S9, 90, 430, "Jean 7 · la fête des Tentes", LS[43] + 0.3, "acc", 52)
gone([t43], LS[44] - 0.4)
lv = S_(S9, "levite", 1500, 420, 190, AL("gardes", 44) - 0.3, rot=2)
kq(S9, 90, 420, "Jean 7.46" + BIB, "« Jamais homme n\'a parlé comme cet homme. »", 44, "Jamais", width=900, size=48, fade_at=LS[45] - 0.4)
fade(lv, LS[45] - 0.4)
pr = S_(S9, "pretre", 1500, 420, 180, LS[45] + 0.3, rot=-2)
kq(S9, 90, 420, "Jean 7.49" + BIB, "« Mais cette foule, qui ne connaît pas la loi, ce sont des maudits. »", 45, "Mais", width=900, size=42, fade_at=LS[46] - 0.4)
fade(pr, LS[46] - 0.4)
S_(S9, "nicodeme", 1500, 420, 190, LS[46] + 0.3, rot=2)
kq(S9, 90, 420, "Jean 7.50" + BIB, "« Nicodème, celui qui était venu de nuit auprès de Jésus, et qui était l\'un d\'entre eux »", 46, "Nicodème", width=950, size=38, fade_at=LS[47] - 0.4)
kq(S9, 90, 420, "Jean 7.51" + BIB, "« Notre loi condamne-t-elle un homme avant qu\'on l\'entende, et qu\'on sache ce qu\'il a fait ? »", 47, "Notre", width=950, size=40, fade_at=LS[48] - 0.4)
t48 = [tag(S9, 90, 430, "Pas encore une déclaration de foi", AL("déclaration", 48) - 0.4, "", 46), tag(S9, 90, 540, "Un principe : écouter avant de juger", AL("principe", 48) - 0.4, "acc", 46)]
gone(t48, LS[49] - 0.4)
t49 = [tag(S9, 90, 430, "Devant ses collègues", AL("collègues", 49) - 0.3, "", 52), stamp(S9, 90, 620, "Un acte courageux", AL("courageux", 49) - 0.8, rot=-3, size=64)]
gone(t49, LS[50] - 0.4)
kq(S9, 90, 420, "Jean 7.52" + BIB, "« Es-tu aussi Galiléen ? Examine, et tu verras que de Galilée il ne sort point de prophète. »", 50, "Es-tu", width=950, size=40, fade_at=LS[51] - 0.4)
t51 = tag(S9, 90, 430, "Le prix de la parole : le mépris", AL("mépris", 51) - 0.8, "acc", 50)
gone([t51], LS[52] - 0.4)
t52 = [tag(S9, 90, 430, "2 Rois : Jonas, de Gath-Hépher", AL("Jonas", 52) - 0.5, "", 48), tag(S9, 90, 540, "En Galilée", AL("Galilée", 52) - 0.3, "acc", 52)]
gone(t52, LS[53] - 0.4)
tag(S9, 90, 430, "La séance est levée", AL("séance", 53) - 0.3, "", 52)
tag(S9, 90, 540, "Mais il a parlé", AL("parlé", 53) - 0.4, "acc", 56)

# =====================================================================  S10 : de la nuit au jour (lignes 54-55)
t = LS[54] - 0.4
cam(t, S10)
headline(S10, 170, ["De la nuit au [jour]"], t + 0.1, kicker="Premier changement", hl_t=AL("jour", 54) + 0.05, size=104)
t54 = [tag(S10, 90, 430, "Plus seulement un visiteur discret", E("discret", 54, 0.5, 0.4), "", 46), tag(S10, 90, 540, "Il défend un homme qu\'on veut condamner", AL("défense", 54) if False else AL("condamner", 54) - 0.6, "acc", 44)]
gone(t54, LS[55] - 0.4)
stamp(S10, 90, 440, "Le plus risqué", E("risqué", 55, 0.5, 0.4), rot=-3, size=76)

# =====================================================================  S11 : Jean 19, les aromates (lignes 56-62)
t = LS[56] - 0.4
cam(t, S11)
headline(S11, 170, ["Au pied de [la croix]"], t + 0.1, kicker="Jean 19", hl_t=AL("croix", 63) if False else AL("dix-neuf", 56) + 0.05, size=104)
t56 = [tag(S11, 90, 430, "Chapitre dix-neuf", LS[56] + 0.3, "", 52), tag(S11, 90, 540, "Jésus crucifié sous Ponce Pilate", AL("Pilate", 56) - 0.5, "", 46), tag(S11, 90, 650, "Les disciples dispersés", AL("dispersés", 56) - 0.4, "acc", 50)]
gone(t56, LS[57] - 0.4)
f57 = tag(S11, 90, 430, "Joseph d\'Arimathée", LS[57] + 0.3, "acc", 52)
fade(f57, AL("disciple", 57) - 0.4)
jo = S_(S11, "pere", 1500, 420, 190, AL("Joseph", 57) - 0.3, rot=2)
kq(S11, 90, 420, "Jean 19.38" + BIB, "« disciple de Jésus, mais secrètement par crainte des Juifs »", 57, "disciple", width=900, size=44, fade_at=LS[58] - 0.4)
t58 = [tag(S11, 90, 430, "Joseph : la peur, dite par le texte", AL("peur", 58) - 0.4, "", 46), tag(S11, 90, 540, "Nicodème : pas un mot sur la peur", AL("Nicodème", 58) - 0.3, "acc", 46)]
gone(t58, LS[59] - 0.4)
fade(jo, LS[59] - 0.4)
S_(S11, "nicodeme", 1500, 420, 190, LS[59] + 0.3, rot=2)
kq(S11, 90, 420, "Jean 19.39" + BIB, "« Nicodème, qui d\'abord était allé de nuit vers Jésus, vint aussi, apportant un mélange d\'environ cent livres de myrrhe et d\'aloès. »", 59, "Nicodème", width=1000, size=36, fade_at=LS[60] - 0.4)
c60 = card(S11, 90, 420, "Cent livres romaines", "plus de 30 kilos de parfums et d\'aromates", AL("trente", 60) - 0.6, w=900, size=44)
gone([c60], LS[61] - 0.4)
t61 = [tag(S11, 90, 430, "Deux hommes, deux peurs possibles", AL("peurs", 61) - 0.5, "", 46), tag(S11, 90, 540, "Le même geste, ensemble", AL("même", 61) - 0.4, "acc", 52)]
gone(t61, LS[62] - 0.4)
tag(S11, 90, 430, "Funérailles royales ? Une interprétation courante", AL("interprétation", 62) - 0.8, "", 42)
tag(S11, 90, 540, "Pas une certitude", AL("certitude", 62) - 0.4, "acc", 52)

# =====================================================================  S12 : au grand jour (lignes 63-70)
t = LS[63] - 0.4
cam(t, S12)
headline(S12, 170, ["Au [grand jour]"], t + 0.1, kicker="Jean 19.39-42", hl_t=AL("scène", 63) + 0.05, size=108)
tomb = S_(S12, "mise-au-tombeau-relief", 1100, 420, 330, AL("Imagine", 63) - 0.2, rot=-2)
fade(tomb, LS[66] - 0.4)
t63 = [tag(S12, 90, 430, "Un membre du Sanhédrin", AL("Sanhédrin", 63) - 0.4, "", 52), tag(S12, 90, 540, "Un homme riche, un notable", AL("notable", 63) - 0.4, "", 50), tag(S12, 90, 650, "S\'occupe de son corps", AL("corps", 63) - 0.4, "acc", 52)]
gone(t63, LS[64] - 0.4)
t64 = tag(S12, 90, 430, "Risquer sa réputation, sa position…", AL("réputation", 64) - 0.5, "acc", 48)
gone([t64], LS[65] - 0.4)
t65 = [tag(S12, 90, 430, "Des linges et des aromates", AL("aromates", 65) - 0.4, "", 50), tag(S12, 90, 540, "Un tombeau neuf, dans un jardin", AL("jardin", 65) - 0.5, "acc", 48)]
gone(t65, LS[66] - 0.4)
s66 = stamp(S12, 90, 440, "De la nuit au grand jour", E("grand", 66, 0.4, 0.4), rot=-3, size=62)
gone([s66], LS[67] - 0.4)
c67 = card(S12, 90, 420, "Jean 19.39", "« qui d\'abord était allé de nuit »", E("évangéliste", 67, 0.3, 0.4), w=900, size=44)
gone([c67], LS[68] - 0.4)
t68 = [tag(S12, 90, 430, "Jamais écrit : « devenu disciple »", E("disciple", 68, 0.5, 0.4), "", 46), tag(S12, 90, 540, "Les Actes ne le mentionnent pas", AL("Actes", 68) - 0.3, "acc", 46)]
gone(t68, LS[69] - 0.4)
c69 = [card(S12, 90, 420, "La tradition", "L\'a considéré comme un croyant", AL("tradition", 69) - 0.2, w=900, size=44), stamp(S12, 90, 680, "Apocryphe tardif · pas la Bible", AL("apocryphe", 69) - 0.3, rot=-3, size=50)]
gone(c69, LS[70] - 0.4)
tag(S12, 90, 430, "Une nuit", E("nuit", 70, 0.3, 0.4), "", 56)
tag(S12, 90, 540, "Une parole", AL("parole", 70) - 0.3, "", 56)
tag(S12, 90, 650, "Un geste", AL("geste", 70) - 0.3, "acc", 56)

# =====================================================================  S13 : pour toi (lignes 71-79)
t = LS[71] - 0.4
cam(t, S13)
headline(S13, 170, ["Ce que cette histoire [dit]"], t + 0.1, kicker="Application", hl_t=AL("dit", 71) + 0.05, size=96)
t71 = [tag(S13, 90, 430, "Approcher Jésus avec ses doutes", E("doutes", 71, 0.6, 0.4), "", 46), tag(S13, 90, 540, "Il repart avec une énigme", AL("énigme", 71) - 0.4, "", 48), tag(S13, 90, 650, "Jésus ne le chasse pas", AL("chasse", 71) - 0.3, "acc", 50)]
gone(t71, LS[72] - 0.4)
t72 = [tag(S13, 90, 430, "La foi peut être lente", AL("lente", 72) - 0.3, "", 52), tag(S13, 90, 540, "Une visite · une défense · un acte", AL("étapes", 72) - 0.6, "acc", 46)]
gone(t72, LS[73] - 0.4)
t73 = tag(S13, 90, 430, "Le courage grandit par petits pas", E("petits", 73, 0.5, 0.4), "acc", 48)
gone([t73], LS[74] - 0.4)
t74 = [tag(S13, 90, 430, "Elle ne juge pas ceux qui avancent dans l\'ombre", AL("ombre", 74) - 0.7, "", 44), tag(S13, 90, 540, "Elle ne les laisse pas où ils sont", AL("laisse", 74) - 0.3, "acc", 46)]
gone(t74, LS[75] - 0.4)
t75 = [tag(S13, 90, 430, "La peur du regard des autres", AL("regard", 75) - 0.3, "", 50), tag(S13, 90, 540, "Une personne de confiance", AL("confiance", 75) - 0.3, "", 50), tag(S13, 90, 650, "Ou un professionnel", AL("professionnel", 75) - 0.3, "acc", 50)]
gone(t75, LS[76] - 0.4)
tq = tag(S13, 90, 430, "Quelle petite étape cette semaine ?", LS[76] + 0.4, "acc", 52)
cta = put(S13, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Dis-le en commentaire', "cta")
blur_in(cta, AL("commentaire", 76) - 1.0, 14)
sfx("click", AL("commentaire", 76) - 1.0, 0.8)
gone([tq, cta], LS[77] - 0.3)
S_(S13, "veilleur", 1500, 420, 200, LS[77] + 0.3, rot=2)
t77 = tag(S13, 90, 430, "La nuit de Nicodème", AL("nuit", 77) - 0.3, "", 56)
gone([t77], LS[78] - 0.4)
t78 = [tag(S13, 90, 430, "Des aromates, devant tous", AL("aromates", 78) - 0.3, "", 52), tag(S13, 90, 540, "La peur a cédé, peu à peu", AL("cédé", 78) - 0.3, "acc", 52)]

t_end = AL("Chaque", 79) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(AL("Chaque", 79) - 0.8, DUR_)]
build(
    chapters=[("01", "La nuit", 0, LS[22]), ("02", "La conversation", LS[22], LS[43]), ("03", "Le conseil et la croix", LS[43], LS[71]), ("04", "Pour toi", LS[71], DUR_)],
    suppress=supp,
    endcard={"kicker": "Chaque semaine", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("nicodeme", 150, 560, 280, -6), ("jesus-portrait", 1550, 330, 230, 5)]},
    endcard_t=AL("Chaque", 79) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
