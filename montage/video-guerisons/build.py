"""Vidéo longue « Chaque guérison de Jésus classée par type de maladie » — style 02, 16:9, 641 s.

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

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Les guérisons de Jésus - style 02", "lang": "fr",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
DUR_ = 641.2
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


def A(word, after=0.0, n=0):
    keys = {style02.norm(pre + word) for pre in ("", "l", "d", "j", "n", "s", "qu", "c", "m", "t")}
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
S11 = (0, 2)

html.append('<style>'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')
LSG = " · Louis Segond 1910"

# =====================================================================  S1 : la porte de Capharnaüm (lignes 1-9)
cam(0, S1)
headline(S1, 170, ["Toute une ville à [une porte]"], 0.0, kicker="Marc 1.32-33", hl_t=AL("porte", 1) + 0.05, size=92)
f0 = S_(S1, "foule", 1100, 420, 330, 0.0, rot=-3, instant=True)
fade(f0, AL("le", 3) - 0.7)
f3 = tag(S1, 90, 430, "Marc raconte la scène", LS[3] + 0.2, "acc", 52)
fade(f3, AL("le", 3) - 0.7)
t2 = [tag(S1, 90, 430, "Capharnaüm", AL("capharnaüm", 2) - 0.2, "", 52), tag(S1, 90, 540, "Le lac de Galilée", AL("galilée", 2) - 0.2, "", 52)]
gone(t2, LS[3] - 0.5)
kq(S1, 90, 420, "Marc 1.32-33" + LSG,
   "« Le soir, après le coucher du soleil, on lui amena tous les malades et les démoniaques. Et toute la ville était rassemblée devant la porte. »",
   3, "le", width=900, size=38, fade_at=LS[4] - 0.4)
S_(S1, "jesus-pied", 1500, 420, 210, AL("porte", 3) - 0.5, rot=2)
t4 = tag(S1, 90, 430, "Jésus guérit… beaucoup", AL("beaucoup", 4) - 0.8, "acc", 52)
gone([t4], LS[5] - 0.5)
s5 = stamp(S1, 90, 440, "Combien ?", AL("combien", 5) - 0.1, rot=-4, size=84)
gone([s5], LS[6] - 0.5)
c6 = counter(S1, 90, 420, 0, 20, AL("vingtaine", 6) - 1.6, 2.4, unit=" récits", size=140)
t6 = tag(S1, 90, 640, "Le texte ne donne aucun total", AL("total", 6) - 1.2, "acc", 44)
gone([c6, t6], LS[7] - 0.5)
t7 = [tag(S1, 90, 430, "La peau", AL("peau", 7) - 0.2, "", 42), tag(S1, 90, 530, "Les yeux", AL("yeux", 7) - 0.2, "", 42),
      tag(S1, 90, 630, "Les oreilles et la parole", AL("oreilles", 7) - 0.2, "", 42), tag(S1, 90, 730, "Le mouvement", AL("mouvement", 7) - 0.2, "", 42),
      tag(S1, 800, 430, "La fièvre et le sang", AL("fièvre", 7) - 0.2, "", 42), tag(S1, 800, 530, "Les esprits", AL("esprits", 7) - 0.2, "", 42),
      tag(S1, 800, 630, "La mort", AL("mort", 7) - 0.2, "acc", 42)]
s8 = stamp(S1, 700, 760, "Les gestes varient", AL("gestes", 8) - 0.6, rot=-3, size=44)
gone(t7 + [s8], LS[9] - 0.5)
c9 = card(S1, 90, 420, "La méthode", "Un récit = une personne guérie, avec son histoire", AL("méthode", 9) - 0.3, w=900, size=38)
t9 = tag(S1, 90, 700, "Les foules guéries en bloc : des résumés", AL("foules", 9) - 0.2, "", 42)
gone([c9, t9], LS[10] - 0.5)

# =====================================================================  S2 : la peau (lignes 10-18)
t = LS[10] - 0.4
cam(t, S2)
headline(S2, 170, ["La [peau]"], t + 0.1, kicker="La lèpre", hl_t=AL("peau", 10) + 0.05, size=110)
t10 = tag(S2, 90, 430, "La plus redoutée de l'époque", AL("redoutée", 10) - 0.4, "acc", 52)
gone([t10], LS[11] - 0.5)
c11 = card(S2, 90, 420, "Le mot grec", "<b>lepra</b> : un ensemble d'affections de la peau", AL("lepra", 11) - 0.3, w=900, size=40)
t11 = [tag(S2, 90, 640, "Lévitique 13", AL("lévitique", 11) - 0.2, "", 46), tag(S2, 90, 750, "Pas forcément la lèpre d'aujourd'hui", AL("forcément", 11) - 0.5, "acc", 38)]
gone([c11] + t11, LS[12] - 0.5)
s12 = stamp(S2, 90, 440, "Impur !", AL("impur", 12) - 0.1, rot=-4, size=84)
t12 = tag(S2, 90, 640, "Une exclusion autant qu'une maladie", AL("exclusion", 12) - 0.6, "acc", 46)
S_(S2, "lepreux", 1500, 420, 170, AL("malade", 12) - 0.2, rot=-2)
gone([s12, t12], LS[13] - 0.5)
kq(S2, 90, 420, "Marc 1.40" + LSG, "« Si tu le veux, tu peux me rendre pur. »", 13, "si", width=900, size=44, fade_at=LS[14] - 0.4)
c14 = card(S2, 90, 420, "Marc 1.41", "« ému de compassion »", AL("compassion", 14) - 0.5, w=800, size=44)
t14 = [tag(S2, 90, 620, "Certains manuscrits : « irrité »", AL("irrité", 14) - 0.4, "", 40), tag(S2, 90, 730, "Les spécialistes en débattent", AL("débattent", 14) - 0.6, "acc", 40)]
gone([c14] + t14, LS[15] - 0.5)
s15 = stamp(S2, 90, 440, "Il le touche", AL("toucher", 15) - 0.1, rot=-4, size=72)
fade(s15, AL("sacrificateur", 15) - 1.4)
c15 = card(S2, 90, 620, "Il dit", "« Je le veux, sois pur. »", AL("veux", 15) - 0.4, w=800, size=44, accent=True)
t15 = tag(S2, 90, 440, "Va te montrer au sacrificateur", AL("sacrificateur", 15) - 0.8, "", 46)
gone([c15, t15], LS[16] - 0.5)
c16 = card(S2, 90, 420, "Luc 17", "Dix lépreux, appelés de loin : purifiés en chemin", AL("dix", 16) - 0.2, w=900, size=38)
t16 = tag(S2, 90, 650, "Jésus ne les touche pas", AL("touche", 16) - 0.3, "", 46)
gone([c16, t16], LS[17] - 0.5)
S_(S2, "samaritain", 1100, 420, 260, AL("samaritain", 17) - 0.8, rot=2)
t17 = [tag(S2, 90, 430, "Un seul revient", AL("revient", 17) - 0.3, "", 52), tag(S2, 90, 540, "Un Samaritain, un étranger", AL("samaritain", 17) - 0.6, "acc", 50)]
gone(t17, LS[18] - 0.5)
teaser(S2, 90, 440, "La suite, dans la même veine", LS[18] + 0.3, hold=4.4)

# =====================================================================  S3 : la vue (lignes 19-24)
t = LS[19] - 0.4
cam(t, S3)
headline(S3, 170, ["La [vue]"], t + 0.1, kicker="Deuxième catégorie", hl_t=AL("vue", 19) + 0.05, size=110)
t19 = tag(S3, 90, 430, "L'une des plus fréquentes", AL("fréquentes", 19) - 0.6, "acc", 52)
gone([t19], LS[20] - 0.5)
jr = S_(S3, "jericho", 1100, 420, 380, AL("jéricho", 20) - 0.2, rot=2)
fade(jr, LS[21] - 0.5)
kq(S3, 90, 420, "Marc 10.47 · Bartimée à Jéricho", "« Fils de David, aie pitié de moi ! »", 20, "fils", width=800, size=42, fade_at=LS[21] - 0.4)
t20 = [tag(S3, 90, 620, "La foule lui dit de se taire", AL("taire", 20) - 0.8, "", 46), tag(S3, 90, 730, "Il crie plus fort", AL("fort", 20) - 0.4, "acc", 46)]
gone(t20, LS[21] - 0.5)
S_(S3, "bartimee", 1500, 420, 190, AL("jette", 21) - 0.4, rot=-2)
t21 = [tag(S3, 90, 430, "Il jette son manteau", AL("manteau", 21) - 0.4, "", 52), stamp(S3, 90, 580, "Voir", AL("voir", 21) - 0.4, rot=-4, size=96)]
S_(S3, "bartimee-portrait", 1100, 420, 280, AL("voir", 21) - 0.3, rot=2)
gone(t21, LS[22] - 0.5)
kq(S3, 90, 420, "Marc 10.52" + LSG, "« Va, ta foi t'a sauvé. »", 22, "va", width=800, size=46, fade_at=LS[23] - 0.4)
c22 = card(S3, 90, 600, "Grec", "<b>sôzô</b> : sauver et guérir", AL("sôzô", 22) - 0.3, w=800, size=40)
gone([c22], LS[23] - 0.5)
t23 = tag(S3, 90, 430, "Bethsaïda : en deux temps", AL("bethsaïda", 23) - 0.3, "acc", 50)
fade(t23, AL("aperçois", 23) - 0.7)
c23 = card(S3, 90, 420, "Marc 8.24", "« J'aperçois les hommes, mais j'en vois comme des arbres, et qui marchent. »", AL("aperçois", 23) - 0.4, w=800, size=38)
gone([c23], LS[24] - 0.5)
t24 = tag(S3, 90, 430, "Une guérison par étapes", AL("étapes", 24) - 0.8, "acc", 56)
gone([t24], LS[25] - 0.5)
# (bartimee et portrait restent jusqu'au changement de plan)

# =====================================================================  S4 : l'aveugle de naissance (lignes 25-27)
t = LS[25] - 0.4
cam(t, S4)
headline(S4, 170, ["L'aveugle de [naissance]"], t + 0.1, kicker="Jean 9", hl_t=AL("naissance", 25) + 0.05, size=96)
elg = S_(S4, "el-greco-aveugle", 1100, 420, 470, AL("aveugle", 25) + 0.2, rot=2)
fade(elg, LS[26] - 0.5)
c25 = card(S4, 90, 420, "Les disciples demandent", "« Qui a péché, lui ou ses parents ? »", AL("péché", 25) - 0.8, w=800, size=40)
s25 = stamp(S4, 90, 620, "Ni l'un ni l'autre", AL("lautre", 25) - 0.3, rot=-3, size=60)
gone([c25, s25], LS[26] - 0.5)
t26 = [tag(S4, 90, 430, "De la boue, de la salive", AL("boue", 26) - 0.3, "", 48), tag(S4, 90, 540, "La piscine de Siloé", AL("siloé", 26) - 0.3, "acc", 48),
       tag(S4, 90, 650, "Siloé : « envoyé »", AL("envoyé", 26) - 0.6, "", 48)]
S_(S4, "siloe", 1100, 420, 430, AL("siloé", 26) - 0.3, rot=-2)
gone(t26, LS[27] - 0.5)
c27 = card(S4, 90, 420, "Sa seule réponse", "« J'étais aveugle, et maintenant je vois. »", AL("répète", 27) - 0.3, w=800, size=44)
t27 = tag(S4, 90, 700, "Ses parents se taisent", AL("parents", 27) - 0.3, "", 44)

# =====================================================================  S5 : l'ouïe et la parole (lignes 28-32)
t = LS[28] - 0.4
cam(t, S5)
headline(S5, 170, ["L'[ouïe] et la parole"], t + 0.1, kicker="Troisième catégorie", hl_t=AL("ouïe", 28) + 0.05, size=96)
t28 = tag(S5, 90, 430, "Entendre, parler", AL("parole", 28) - 0.6, "acc", 52)
gone([t28], LS[29] - 0.5)
S_(S5, "villageois", 1500, 420, 250, AL("sourd", 29) - 0.3, rot=2)
t29 = [tag(S5, 90, 430, "La Décapole", AL("décapole", 29) - 0.3, "", 52), tag(S5, 90, 540, "À l'écart, loin de la foule", AL("écart", 29) - 0.3, "", 46),
       tag(S5, 90, 650, "Doigts, salive, soupir", AL("salive", 29) - 0.3, "acc", 46)]
gone(t29, LS[30] - 0.5)
c30 = card(S5, 90, 420, "Un mot araméen", "<b>Ephphatha</b> : « ouvre-toi »", AL("ephphatha", 30) - 0.6, w=800, size=48)
burst(S5, 1000, 520, AL("ephphatha", 30) - 0.2)
gone([c30], LS[31] - 0.5)
kq(S5, 90, 420, "Marc 7.37" + LSG, "« Il fait tout à merveille ; il fait entendre les sourds, et parler les muets. »", 31, "il", width=900, size=42, fade_at=LS[32] - 0.4)
tag(S5, 90, 430, "Un muet", AL("muet", 32) - 0.3, "", 52)
tag(S5, 90, 540, "Un esprit mauvais, chassé", AL("esprit", 32) - 0.3, "", 46)
tag(S5, 90, 650, "Il parle", AL("parle", 32) - 0.3, "acc", 52)

# =====================================================================  S6 : le mouvement (lignes 33-39)
t = LS[33] - 0.4
cam(t, S6)
headline(S6, 170, ["Le [mouvement]"], t + 0.1, kicker="Quatrième catégorie", hl_t=AL("mouvement", 33) + 0.05, size=104)
f33 = tag(S6, 90, 430, "Paralysés · mains · dos", LS[33] + 0.4, "acc", 52)
fade(f33, LS[34] - 0.5)
p34 = S_(S6, "porteurs", 90, 420, 480, AL("quatre", 34) - 0.3, rot=-2)
t34 = [tag(S6, 700, 430, "Quatre hommes", AL("quatre", 34) - 0.3, "", 50), tag(S6, 700, 540, "Le toit découvert", AL("toit", 34) - 0.3, "acc", 50)]
gone([p34] + t34, LS[35] - 0.5)
pd = S_(S6, "paralytique-dessin", 1100, 420, 420, AL("jésus", 35) - 0.3, rot=2)
fade(pd, LS[36] - 0.5)
kq(S6, 90, 420, "Marc 2.5" + LSG, "« Mon enfant, tes péchés sont pardonnés. »", 35, "mon", width=800, size=42, fade_at=LS[36] - 0.4)
t35 = [tag(S6, 90, 700, "Les scribes s'indignent", AL("scribes", 35) - 0.3, "", 44), tag(S6, 90, 800, "Il ordonne : lève-toi", AL("ordonne", 35) - 0.3, "acc", 44)]
gone(t35, LS[36] - 0.5)
c36 = card(S6, 90, 420, "Béthesda · Jean 5", "Malade depuis trente-huit ans", AL("trente-huit", 36) - 0.6, w=800, size=44)
t36 = tag(S6, 90, 620, "« Veux-tu être guéri ? »", AL("veux-tu", 36) - 0.3, "acc", 52)
bd = S_(S6, "bethesda-dessin", 1100, 420, 420, AL("béthesda", 36) - 0.5, rot=-2)
fade(bd, LS[38] - 0.5)
gone([c36, t36], LS[37] - 0.5)
t37 = [tag(S6, 90, 430, "Une multitude de malades", AL("multitude", 37) - 0.3, "", 52), tag(S6, 90, 540, "Un seul guéri dans ce récit", AL("guérison-là", 37) - 0.8, "acc", 46)]
gone(t37, LS[38] - 0.5)
f38 = tag(S6, 90, 430, "Une main desséchée", LS[38] + 0.2, "acc", 52)
fade(f38, AL("étends", 38) - 1.2)
c38 = card(S6, 90, 420, "Un jour de sabbat", "« Étends ta main »", AL("étends", 38) - 0.8, w=800, size=48)
t38 = tag(S6, 90, 620, "Et la discussion commence", AL("discussion", 38) - 0.3, "", 44)
gone([c38, t38], LS[39] - 0.5)
S_(S6, "femme-courbee", 1500, 420, 215, AL("courbée", 39) - 0.3, rot=2)
tag(S6, 90, 430, "Dix-huit ans", AL("dix-huit", 39) - 0.3, "", 56)
tag(S6, 90, 540, "« Fille d'Abraham »", AL("abraham", 39) - 0.4, "acc", 52)
tag(S6, 90, 650, "Elle se redresse", AL("redresse", 39) - 0.3, "", 48)

# =====================================================================  S7 : la fièvre et le sang (lignes 40-46)
t = LS[40] - 0.4
cam(t, S7)
headline(S7, 170, ["La [fièvre] et le sang"], t + 0.1, kicker="Cinquième catégorie", hl_t=AL("fièvre", 40) + 0.05, size=96)
t41 = [tag(S7, 90, 430, "La belle-mère de Pierre", AL("belle-mère", 41) - 0.3, "", 50), tag(S7, 90, 540, "Il la prend par la main", AL("main", 41) - 0.3, "", 46),
       tag(S7, 90, 650, "Elle se met à les servir", AL("servir", 41) - 0.5, "acc", 46)]
gone(t41, LS[42] - 0.5)
f42 = [tag(S7, 90, 430, "Un officier royal", LS[42] + 0.3, "", 52), tag(S7, 90, 540, "Son fils est mourant", AL("mourant", 42) - 0.4, "", 50)]
gone(f42, AL("va", 42) - 0.8)
kq(S7, 90, 420, "Jean 4.50" + LSG, "« Va, ton fils vit. »", 42, "va", width=700, size=52, fade_at=LS[43] - 0.4)
t42 = tag(S7, 90, 620, "À distance : la même heure", AL("heure", 42) - 0.5, "acc", 44)
gone([t42], LS[43] - 0.5)
ce = S_(S7, "centurion", 1500, 420, 190, AL("centurion", 43) - 0.3, rot=2)
t43 = [tag(S7, 90, 430, "Un centurion romain", AL("centurion", 43) - 0.3, "", 50), tag(S7, 90, 540, "Une parole suffit", AL("suffit", 43) - 0.4, "acc", 52),
       tag(S7, 90, 650, "Guéri à distance", AL("distance", 43) - 0.3, "", 48)]
gone([ce] + t43, LS[44] - 0.5)
S_(S7, "femme-sang", 1100, 420, 380, AL("perd", 44) - 0.2, rot=-2)
t44 = [tag(S7, 90, 430, "Douze ans", AL("douze", 44) - 0.3, "", 56), tag(S7, 90, 540, "Sans aucun soulagement", AL("soulagement", 44) - 0.8, "acc", 44)]
pr = S_(S7, "pince-romaine", 90, 660, 330, AL("médecins", 44) - 0.3, rot=-3)
gone(t44 + [pr], LS[45] - 0.5)
c45 = card(S7, 90, 420, "Elle se dit", "« Si je touche seulement ses vêtements, je serai guérie. »", AL("touche", 45) - 1.0, w=800, size=36)
t45a = tag(S7, 90, 700, "Le flux s'arrête", AL("flux", 45) - 0.3, "acc", 50)
fade(t45a, AL("qui", 45) - 0.7)
t45 = [t45a, tag(S7, 90, 700, "« Qui a touché mes vêtements ? »", AL("qui", 45) - 0.3, "", 42)]
gone([c45] + t45, LS[46] - 0.5)
kq(S7, 90, 420, "Marc 5.34" + LSG, "« Ta foi t'a sauvée ; va en paix, et sois guérie de ton mal. »", 46, "ta", width=800, size=42, fade_at=LS[47] - 0.4)

# =====================================================================  S8 : les esprits (lignes 47-52)
t = LS[47] - 0.4
cam(t, S8)
headline(S8, 170, ["Les [esprits]"], t + 0.1, kicker="Sixième catégorie", hl_t=AL("esprits", 47) + 0.05, size=104)
f47 = tag(S8, 90, 430, "Les esprits impurs", LS[47] + 0.3, "acc", 52)
fade(f47, AL("expulsion", 47) - 0.9)
t47 = [tag(S8, 90, 430, "Maladie ou esprit impur", AL("expulsion", 47) - 0.6, "", 52), tag(S8, 90, 540, "Souvent distingués", AL("distinguent", 47) - 0.3, "acc", 52)]
gone(t47, LS[48] - 0.5)
f48 = tag(S8, 90, 430, "Un débat ancien", LS[48] + 0.3, "", 52)
fade(f48, AL("diagnostic", 48) - 1.3)
c48 = card(S8, 90, 420, "Les spécialistes en discutent", "Pas de diagnostic médical dans le texte", AL("diagnostic", 48) - 0.9, w=900, size=40)
s48 = stamp(S8, 90, 640, "Pas de diagnostic", AL("pose", 48) - 0.3, rot=-3, size=60)
gone([c48, s48], LS[49] - 0.5)
S_(S8, "jesus-pied", 1500, 420, 210, AL("synagogue", 49) - 0.3, rot=2)
kq(S8, 90, 420, "Marc 1.24" + LSG, "« Je sais qui tu es : le Saint de Dieu. »", 49, "je", width=900, size=44, fade_at=LS[50] - 0.4)
t49 = [tag(S8, 90, 620, "Il lui ordonne de sortir", AL("ordonne", 49) - 0.3, "", 46), tag(S8, 90, 730, "Il parle avec autorité", AL("autorité", 49) - 0.6, "acc", 46)]
gone(t49, LS[50] - 0.5)
t50 = [tag(S8, 90, 430, "Chez les Gadaréniens", AL("gadaréniens", 50) - 0.3, "", 52), tag(S8, 90, 540, "Parmi les tombeaux", AL("tombeaux", 50) - 0.3, "", 48),
       tag(S8, 90, 650, "Assis, vêtu, dans son bon sens", AL("sens", 50) - 0.8, "acc", 46)]
gone(t50, LS[51] - 0.5)
pf = S_(S8, "pere-fils", 1100, 420, 185, AL("père", 51) - 0.3, rot=-2)
kq(S8, 90, 420, "Marc 9.23" + LSG, "« Tout est possible à celui qui croit. »", 51, "tout", width=800, size=42, fade_at=LS[52] - 0.4)
c51 = card(S8, 90, 690, "Le père répond", "« Je crois ! viens au secours de mon incrédulité ! »", AL("crois", 51) - 0.4, w=800, size=36)
gone([pf, c51], LS[52] - 0.5)
t52 = [tag(S8, 90, 430, "Une mère cananéenne", AL("cananéenne", 52) - 0.3, "", 52), tag(S8, 90, 540, "Une étrangère", AL("étrangère", 52) - 0.3, "", 48)]
kq(S8, 90, 650, "Matthieu 15.28" + LSG, "« Ô femme, ta foi est grande ! »", 52, "ô", width=800, size=44)

# =====================================================================  S9 : la mort (lignes 53-57)
t = LS[53] - 0.4
cam(t, S9)
headline(S9, 170, ["La [mort]"], t + 0.1, kicker="Dernière catégorie", hl_t=AL("mort", 53) + 0.05, size=110)
t53 = tag(S9, 90, 430, "Trois fois, il rend la vie", LS[53] + 0.3, "acc", 52)
gone([t53], LS[54] - 0.5)
fj = S_(S9, "fille-jairus", 1500, 420, 150, AL("jaïrus", 54) - 0.3, rot=2)
t54 = tag(S9, 90, 430, "Jaïrus · douze ans", AL("jaïrus", 54) - 0.3, "", 52)
c54 = card(S9, 90, 560, "En araméen", "<b>Talitha koumi</b> : « jeune fille, lève-toi »", AL("talitha", 54) - 0.3, w=800, size=40)
gone([fj, t54, c54], LS[55] - 0.5)
vc = S_(S9, "veuve-cortege", 90, 420, 520, AL("naïn", 55) - 0.3, rot=-2)
t55 = [tag(S9, 760, 430, "Naïn", AL("naïn", 55) - 0.3, "", 52), tag(S9, 760, 540, "Le fils unique d'une veuve", AL("unique", 55) - 0.3, "", 46),
       tag(S9, 760, 650, "« Lève-toi »", AL("lève-toi", 55) - 0.3, "acc", 52)]
gone([vc] + t55, LS[56] - 0.5)
lz = S_(S9, "lazare", 1500, 420, 220, AL("lazare", 56) - 0.3, rot=2)
lg = S_(S9, "lazare-gravure", 1000, 420, 400, AL("lazare", 56) - 0.2, rot=-2)
t56 = [tag(S9, 90, 430, "Mort depuis quatre jours", AL("quatre", 56) - 0.3, "", 50), tag(S9, 90, 540, "Jésus pleure", AL("pleure", 56) - 0.3, "", 52),
       tag(S9, 90, 650, "« Lazare, sors ! »", AL("sors", 56) - 0.4, "acc", 52)]
gone([lg] + t56, LS[57] - 0.5)
c57 = card(S9, 90, 420, "La tradition chrétienne", "Des signes qui annoncent la résurrection de Jésus", AL("signes", 57) - 0.4, w=900, size=38)
t57 = tag(S9, 90, 690, "Lecture habituelle : morts de nouveau", AL("nouveau", 57) - 1.8, "", 40)

# =====================================================================  S10 : le bilan (lignes 58-64)
t = LS[58] - 0.4
cam(t, S10)
headline(S10, 170, ["[Regardons] l'ensemble"], t + 0.1, kicker="Ce qu'ils ont en commun", hl_t=AL("regardons", 58) + 0.05, size=96)
t58 = [tag(S10, 90, 430, "Points communs ?", AL("commun", 58) - 0.4, "", 52), tag(S10, 90, 540, "Différences ?", AL("diffèrent-ils", 58) - 0.3, "acc", 52)]
gone(t58, LS[59] - 0.5)
g59 = [card(S10, 90, 420, "Un geste", "Une parole", AL("parole", 59) - 0.3, w=400, size=32),
       card(S10, 580, 420, "Un geste", "Un contact", AL("contact", 59) - 0.3, w=400, size=32),
       card(S10, 90, 640, "Un geste", "De la boue, de la salive", AL("boue", 59) - 0.3, w=400, size=32),
       card(S10, 580, 640, "Un geste", "À distance", AL("distance", 59) - 0.3, w=400, size=32, accent=True)]
gone(g59, LS[60] - 0.5)
g60 = [card(S10, 90, 420, "La foi", "Celle du malade", AL("malade", 60) - 0.3, w=400, size=32),
       card(S10, 580, 420, "La foi", "Celle de ses amis", AL("amis", 60) - 0.3, w=400, size=32),
       card(S10, 90, 640, "La foi", "Celle d'un père, d'un centurion", AL("centurion", 60) - 0.3, w=400, size=32),
       card(S10, 580, 640, "La foi", "Parfois, rien n'est dit", AL("défunt", 60) - 1.2, w=400, size=32, accent=True)]
gone(g60, LS[61] - 0.5)
t61 = tag(S10, 90, 430, "Il ne guérit pas toujours", LS[61] + 0.3, "acc", 52)
fade(t61, AL("put", 61) - 0.7)
kq(S10, 90, 420, "Marc 6.5" + LSG, "« Il ne put faire là aucun miracle, si ce n'est qu'il imposa les mains à quelques malades et les guérit. »", 61, "put", width=950, size=38,
   fade_at=LS[62] - 0.4)
f62 = tag(S10, 90, 430, "La réponse à Jean-Baptiste", LS[62] + 0.3, "acc", 52)
fade(f62, AL("les", 62) - 0.8)
kq(S10, 90, 420, "Matthieu 11.5" + LSG,
   "« les aveugles voient, les boiteux marchent, les lépreux sont purifiés, les sourds entendent, les morts ressuscitent, et la bonne nouvelle est annoncée aux pauvres. »",
   62, "les", width=950, size=38, fade_at=LS[63] - 0.4)
s63 = stamp(S10, 90, 440, "Nos catégories", AL("catégories", 63) - 0.5, rot=-3, size=72)
c63 = card(S10, 90, 620, "Ésaïe 35 · Ésaïe 61", "Un écho des promesses d'Ésaïe", AL("désaïe", 63) - 0.3, w=800, size=38)
gone([s63, c63], LS[64] - 0.5)
S_(S10, "cent-florins", 1100, 420, 470, AL("signes", 64) - 0.5, rot=-2)
tag(S10, 90, 430, "Pas seulement des soulagements", AL("soulagements", 64) - 0.6, "", 46)
tag(S10, 90, 540, "Chez Jean : des signes", AL("signes", 64) - 0.3, "acc", 50)
tag(S10, 90, 650, "Quelque chose de nouveau commence", AL("nouveau", 64) - 0.4, "", 42)

# =====================================================================  S11 : quand la guérison ne vient pas (lignes 65-69)
t = LS[65] - 0.4
cam(t, S11)
headline(S11, 170, ["Quand la guérison [ne vient pas]"], t + 0.1, kicker="Le Nouveau Testament", hl_t=AL("guérison", 67) + 0.05, size=88)
f65 = tag(S11, 90, 430, "Des malades qui ne sont pas guéris", LS[65] + 0.3, "", 48)
fade(f65, AL("écharde", 65) - 0.9)
pa = S_(S11, "paul", 1500, 420, 160, AL("paul", 65) - 0.3, rot=-2)
fade(pa, LS[66] - 0.5)
t65 = [tag(S11, 90, 430, "Paul : une écharde dans la chair", AL("écharde", 65) - 0.5, "", 48), tag(S11, 90, 540, "Il demande trois fois", AL("trois", 65) - 0.3, "acc", 48)]
gone(t65, AL("réponse", 65) - 0.7)
kq(S11, 90, 420, "2 Corinthiens 12.9" + LSG, "« Ma grâce te suffit, car ma puissance s'accomplit dans la faiblesse. »", 65, "ma", width=900, size=42, fade_at=LS[66] - 0.4)
t66 = tag(S11, 90, 430, "Trophime, malade à Milet", AL("trophime", 66) - 0.3, "", 52)
gone([t66], LS[67] - 0.5)
c67 = card(S11, 90, 420, "Si tu pries pour une guérison", "Le texte ne dit pas que tu manques de foi", LS[67] + 0.3, w=900, size=38)
t67 = tag(S11, 90, 640, "Il ne dit pas que ta souffrance ne compte pas", AL("compte", 67) - 2.0, "acc", 40)
gone([c67, t67], LS[68] - 0.5)
f68 = tag(S11, 90, 430, "Si tu es malade", LS[68] + 0.3, "acc", 52)
fade(f68, AL("médecin", 68) - 0.8)
S_(S11, "mains-lampe", 1500, 420, 300, AL("médecin", 68) - 0.3, rot=2)
t68 = [tag(S11, 90, 430, "Consulter un médecin", AL("médecin", 68) - 0.3, "", 52), tag(S11, 90, 540, "Ne s'oppose pas à la foi", AL("oppose", 68) - 0.3, "acc", 50),
       tag(S11, 90, 650, "Luc, « le médecin bien-aimé »", AL("bien-aimé", 68) - 0.5, "", 46)]
gone(t68, LS[69] - 0.5)

# =====================================================================  S11 (suite) puis S1 revisité : conclusion (lignes 69-73)
t69 = tag(S11, 90, 430, "Lequel te touche le plus ?", AL("lequel", 69) - 0.3, "acc", 56)
cta = put(S11, 90, 600, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Dis-le en commentaire', "cta")
blur_in(cta, AL("commentaire", 69) - 1.2, 14)
sfx("click", AL("commentaire", 69) - 1.2, 0.8)

cam(LS[70] - 2.0, "all")
wipe(S1, LS[70] - 2.1)
t = LS[70] - 0.4
cam(t, S1)
headline(S1, 170, ["Devant chacune, il [s'arrête]"], t + 0.1, kicker="Capharnaüm", hl_t=AL("arrête", 71) + 0.05, size=92)
S_(S1, "foule", 1500, 420, 300, AL("porte", 70) - 0.3, rot=2)
kq(S1, 90, 420, "Marc 1.34" + LSG, "« Il guérit beaucoup de malades, atteints de diverses maladies. »", 70, "il", width=900, size=42, fade_at=LS[71] - 0.4)
t71 = [tag(S1, 90, 430, "La peau", AL("peau", 71) - 0.1, "", 50), tag(S1, 90, 540, "Les yeux", AL("yeux", 71) - 0.1, "", 50), tag(S1, 90, 650, "La voix", AL("voix", 71) - 0.1, "", 50),
       tag(S1, 800, 430, "Les jambes", AL("jambes", 71) - 0.1, "", 50), tag(S1, 800, 540, "Le sang", AL("sang", 71) - 0.1, "", 50), tag(S1, 800, 650, "La mort", AL("mort", 71) - 0.1, "", 50)]
gone(t71, LS[72] - 0.5)
t72 = [tag(S1, 90, 430, "Trop loin", AL("loin", 72) - 0.1, "", 56), tag(S1, 90, 540, "Trop impur", AL("impur", 72) - 0.1, "", 56),
       tag(S1, 90, 650, "Trop malade", AL("malade", 72) - 0.1, "", 56), tag(S1, 90, 760, "Trop mort", AL("mort", 72) - 0.1, "", 56),
       stamp(S1, 800, 540, "Il s'arrête", AL("arrête", 72) - 0.3, rot=-3, size=84)]
gone(t72, LS[73] - 0.3)

t_end = AL("autres", 73) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(LS[70] - 2.8, LS[70] - 0.5), (AL("autres", 73) - 0.8, DUR_)]
build(
    chapters=[("01", "La porte de Capharnaüm", 0, LS[10]), ("02", "La peau", LS[10], LS[19]), ("03", "La vue", LS[19], LS[28]), ("04", "L'ouïe et le mouvement", LS[28], LS[40]),
              ("05", "Fièvre, esprits, mort", LS[40], LS[58]), ("06", "Le bilan", LS[58], DUR_)],
    suppress=supp,
    endcard={"kicker": "Chaque semaine", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("jesus-portrait", 150, 560, 300, -6), ("bartimee-portrait", 1550, 330, 220, 5)]},
    endcard_t=AL("autres", 73) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
