"""Vidéo longue « Prophéties de fin du monde (2027, Nostradamus) : que dit la Bible ? » — style 02, 16:9, 536 s.

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

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Prophéties de fin du monde - style 02", "lang": "fr",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
DUR_ = 536.3
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
    hits = [w["start"] for w in style02.words if style02.norm(w["text"]) == style02.norm(word) and w["start"] >= after - 0.01]
    if len(hits) <= n:
        MANQUES.append((word, after, n))
        return max(after, 1.0) + 0.5
    return hits[n]


def AL(word, line, n=0):
    return A(word, LS[line] - 0.05, n)


def FW(name, w, maxh=385):
    """Largeur d'un autocollant limitée pour que sa hauteur (px de conception) ne dépasse pas maxh."""
    iw, ih = Image.open(os.path.join(HERE, "assets/stickers", name + ".png")).size
    return round(min(w, maxh * iw / ih))


def S_(station, name, x, y, w, t, **kw):
    i, h = sticker(station, name, x, y, FW(name, w), t, **kw)
    return i


def kq(station, x, y, ref_txt, text, line, first, width=1000, size=34, last=None, fade_at=None):
    t0 = AL(first, line) - 0.05
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
S11, S12, S13 = (0, 2), (1, 2), (2, 2)

html.append('<style>'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

# =====================================================================  S1 : les dates annoncées (lignes 1-7)
cam(0, S1)
headline(S1, 170, ["La fin du monde, [reportée]"], 0.0, kicker="Annonces", hl_t=AL("reportée", 1) + 0.05, size=96)
v0 = S_(S1, "villageois", 1100, 420, 300, 0.0, rot=-3, instant=True)
fade(v0, LS[2] - 0.2)
tg1 = [tag(S1, 90, 430, "Annoncée", AL("annoncée", 1) - 0.1, "", 56), tag(S1, 90, 540, "Reportée", AL("reportée", 1) - 0.1, "acc", 56)]
gone(tg1, LS[2] - 0.2)
an = S_(S1, "animateur", 1500, 420, 190, AL("animateur", 2) - 0.3, rot=2)
c1 = card(S1, 90, 420, "Annonce de Harold Camping", "21 mai 2011", AL("Camping", 2) - 0.2, w=640, size=56)
st1 = stamp(S1, 90, 660, "Rien", AL("rien", 3) + 0.1, rot=-4, size=72)
gone([c1, st1], AL("corrige", 3) - 0.2)
c2 = card(S1, 90, 420, "Annonce corrigée", "21 octobre 2011", AL("corrige", 3) + 0.2, w=700, size=56, accent=True)
st2 = stamp(S1, 90, 660, "Toujours rien", AL("rien", 4) + 0.1, rot=-3, size=64)
gone([c2, st2, an], LS[5] - 0.5)
cn = counter(S1, 90, 420, 2011, 2027, AL("vingt-sept", 5) - 0.8, 2.2, size=170)
tn = [tag(S1, 800, 440, "Nostradamus", AL("Nostradamus", 5) - 0.1, "", 52), tag(S1, 800, 550, "Quatrains", AL("quatrains", 5) - 0.1, "acc", 52)]
gone([cn] + tn, LS[6] - 0.5)
tq = tag(S1, 90, 440, "La Bible dit-elle quand ?", AL("Bible", 6) - 0.4, "acc", 56)
v6 = S_(S1, "villageois", 1100, 420, 300, AL("croyants", 6) - 0.3, rot=2)
ring(S1, 1260, 600, AL("langoisse", 6), size=260)
gone([tq], LS[7] - 0.5)
tx = [tag(S1, 90, 430, "Le texte", AL("texte", 7) - 0.1, "", 54), tag(S1, 90, 540, "L'histoire", AL("lhistoire", 7) - 0.1, "", 54),
      tag(S1, 90, 650, "Ce que Jésus a répondu", AL("Jésus", 7) - 0.1, "acc", 54)]

# =====================================================================  S2 : Nostradamus (lignes 8-14)
t = LS[8] - 0.4
cam(t, S2)
headline(S2, 170, ["[Nostradamus]"], t + 0.1, kicker="Les Prophéties, 1555", hl_t=AL("Nostradamus", 8) + 0.05, size=104)
S_(S2, "nostradamus-pied", 1500, 420, 160, AL("Nostradamus", 8) - 0.2, rot=-2)
t8 = tag(S2, 90, 430, "Un nom qui revient toujours", AL("revient", 8) - 0.3, "", 50)
fade(t8, LS[9] - 0.5)
c9 = card(S2, 90, 420, "Michel de Nostredame", "médecin et astrologue · 1503-1566", AL("Michel", 9) - 0.1, w=860, size=38)
fade(c9, LS[10] - 0.5)
n10 = counter(S2, 90, 420, 1500, 1555, AL("quinze", 10) - 0.2, 2.0, size=150)
t10 = [tag(S2, 90, 620, "Lyon · Les Prophéties", AL("Lyon", 10) - 0.2, "acc", 46), tag(S2, 90, 740, "Des quatrains volontairement obscurs", AL("obscurs", 10) - 1.2, "", 40)]
ast = S_(S2, "astrolabe", 1050, 420, 260, AL("Prophéties", 10) - 0.2, rot=3)
fade(ast, LS[12] - 0.5)
gone([n10] + t10, LS[11] - 0.5)
t11 = [tag(S2, 90, 430, "Des vers très vagues", AL("vagues", 11) - 0.3, "acc", 56), tag(S2, 90, 560, "Un sens trouvé après coup", AL("coup", 11) - 0.8, "", 50)]
gone(t11, LS[12] - 0.5)
c12 = card(S2, 90, 420, "Quatrain célèbre", "« l'an mil neuf cent nonante-neuf, sept mois »", AL("quatrain", 12) - 0.1, w=900, size=36)
t12 = [tag(S2, 90, 640, "Un grand roi d'effroi", AL("roi", 12) - 0.3, "", 46), stamp(S2, 900, 640, "Rien", AL("Rien", 12), rot=-4, size=64),
       tag(S2, 90, 760, "Puis, une nouvelle lecture", AL("réinterprété", 12) - 1.0, "acc", 40)]
gone([c12] + t12, LS[13] - 0.5)
s13 = stamp(S2, 90, 430, "Faux", AL("faux", 13) - 0.2, rot=-4, size=84)
t13 = [tag(S2, 90, 600, "Écrit dans les années 1990 par un étudiant", AL("étudiant", 13) - 0.6, "", 40),
       tag(S2, 90, 720, "Attribué à tort à Nostradamus", AL("vague", 13) - 1.4, "acc", 40)]
gone([s13] + t13, LS[14] - 0.5)
teaser(S2, 90, 440, "La suite éclaire beaucoup", AL("patiemment", 14) - 0.5, hold=4.6)

# =====================================================================  S3 : le test biblique (lignes 15-19)
t = LS[15] - 0.4
cam(t, S3)
headline(S3, 170, ["Le [test] d'un prophète"], t + 0.1, kicker="Deutéronome 18", hl_t=AL("test", 16) + 0.05, size=96)
t15 = tag(S3, 90, 430, "La Bible juge autrement", AL("juge", 15) - 0.3, "acc", 52)
fade(t15, LS[16] - 0.5)
S_(S3, "rouleau", 1500, 420, 230, AL("Deutéronome", 16) - 0.2, rot=3)
f16 = tag(S3, 90, 430, "Dieu donne un test", LS[16] + 0.5, "acc", 52)
fade(f16, AL("quand", 16) - 0.6)
kq(S3, 90, 420, "Deutéronome 18.22 · Louis Segond 1910",
   "« Quand ce que dira le prophète n'aura pas lieu et n'arrivera pas, ce sera une parole que l'Éternel n'aura point dite. »",
   16, "quand", width=900, size=38, fade_at=LS[17] - 0.4)
t17 = [tag(S3, 90, 430, "Une prédiction précise", AL("précise", 17) - 0.6, "", 52), tag(S3, 90, 540, "Non réalisée : pas de l'Éternel", AL("réalise", 17) - 0.3, "acc", 46)]
gone(t17, LS[18] - 0.5)
t18 = tag(S3, 90, 430, "Un prophète appelle à revenir", AL("revenir", 18) - 0.8, "acc", 52)
gone([t18], LS[19] - 0.5)
S_(S3, "jonas", 1100, 420, 220, AL("Jonas", 19) - 0.3, rot=-3)
card(S3, 90, 420, "Jonas 3.4", "« Encore quarante jours, et Ninive sera détruite »", AL("encore", 19) - 0.2, w=760, size=36)
tag(S3, 90, 640, "La ville se repent", AL("repent", 19) - 0.3, "", 46)
tag(S3, 90, 750, "Le but : la conversion", AL("conversion", 19) - 0.4, "acc", 46)

# =====================================================================  S4 : la question à Jésus (lignes 20-24)
t = LS[20] - 0.4
cam(t, S4)
headline(S4, 170, ["Que dit [Jésus] ?"], t + 0.1, kicker="Matthieu 24", hl_t=AL("Jésus", 20) + 0.05, size=104)
S_(S4, "jesus-pied", 1500, 420, 210, AL("Jésus", 20) - 0.3, rot=2)
t20 = tag(S4, 90, 430, "La date de la fin ?", AL("date", 20) - 0.2, "acc", 56)
fade(t20, LS[21] - 0.5)
kq(S4, 90, 420, "Matthieu 24.3 · Louis Segond 1910",
   "« Quand cela arrivera-t-il, et quel sera le signe de ton avènement et de la fin du monde ? »", 21, "quand", width=900, size=40,
   fade_at=LS[22] - 0.4)
c22 = card(S4, 90, 420, "En grec", "<b>synteleia tou aiônos</b>", AL("synteleia", 22) - 0.2, w=760, size=40)
t22 = tag(S4, 90, 600, "L'achèvement d'un âge", AL("âge", 22) - 0.8, "acc", 50)
gone([c22, t22], LS[23] - 0.5)
a23 = S_(S4, "arc-titus", 90, 420, 430, AL("temple", 23) - 0.3, rot=-2)
s23 = stamp(S4, 640, 450, "An 70", AL("soixante-dix", 23) - 0.2, rot=-4, size=72)
t23 = tag(S4, 640, 610, "Le temple détruit", AL("temple", 23), "", 48)
gone([a23, s23, t23], LS[24] - 0.5)
tag(S4, 90, 430, "Lecture 1 : l'an 70", AL("événement", 24) - 0.4, "", 52)
tag(S4, 90, 560, "Lecture 2 : la fin des temps", AL("temps", 24) - 0.2, "acc", 52)

# =====================================================================  S5 : le jour et l'heure (lignes 25-28)
t = LS[25] - 0.4
cam(t, S5)
headline(S5, 170, ["Le jour et [l'heure]"], t + 0.1, kicker="Matthieu 24.36", hl_t=AL("lheure", 25) + 0.05, size=104)
S_(S5, "jesus-portrait", 1500, 420, 250, AL("Jésus", 25) - 0.3, rot=3)
kq(S5, 90, 420, "Matthieu 24.36 · Louis Segond 1910",
   "« Pour ce qui est du jour et de l'heure, personne ne le sait, ni les anges des cieux, ni le Fils, mais le Père seul. »", 25, "pour",
   width=950, size=40, fade_at=LS[26] - 0.4)
t26 = [tag(S5, 90, 430, "Marc : la même parole", AL("Marc", 26) - 0.2, "", 52), tag(S5, 90, 540, "Le jour reste le secret du Père", AL("secret", 26) - 0.8, "acc", 46)]
gone(t26, LS[27] - 0.5)
kq(S5, 90, 420, "Actes 1.7 · Louis Segond 1910",
   "« Ce n'est pas à vous de connaître les temps ou les moments que le Père a fixés de sa propre autorité. »", 27, "ce", width=950, size=38,
   fade_at=LS[28] - 0.4)
stamp(S5, 90, 440, "Contredit", AL("contredit", 28) - 0.2, rot=-4, size=84)
tag(S5, 90, 670, "Il suffit de relire Matthieu", AL("relire", 28) - 0.6, "acc", 50)

# =====================================================================  S6 : les signes (lignes 29-32)
t = LS[29] - 0.4
cam(t, S6)
headline(S6, 170, ["Les [signes] ?"], t + 0.1, kicker="Matthieu 24.4-6", hl_t=AL("signes", 29) + 0.05, size=104)
t29 = tag(S6, 90, 430, "Regarde comment il commence", AL("regarde", 29) - 0.3, "", 52)
fade(t29, LS[30] - 0.5)
S_(S6, "cavaliers", 1500, 420, 290, AL("guerre", 30) - 0.3, rot=2)
kq(S6, 90, 420, "Matthieu 24.4-6 · Louis Segond 1910",
   "« Prenez garde que personne ne vous séduise. Car plusieurs viendront sous mon nom, disant : C'est moi qui suis le Christ. Et ils séduiront "
   "beaucoup de gens. Vous entendrez parler de guerres et de bruits de guerres : gardez-vous d'être troublés, car il faut que ces choses arrivent. "
   "Mais ce ne sera pas encore la fin. »", 30, "prenez", width=1050, size=32, fade_at=LS[31] - 0.4)
t31 = [tag(S6, 90, 430, "Pas de calendrier", AL("calendrier", 31) - 0.6, "", 52), tag(S6, 90, 540, "Un avertissement", AL("avertissement", 31) - 0.3, "acc", 52),
       tag(S6, 90, 650, "Contre la séduction et la panique", AL("panique", 31) - 1.4, "", 44)]
gone(t31, LS[32] - 0.5)
card(S6, 90, 420, "Jésus dit", "« pas encore la fin »", AL("fin", 32) - 0.2, w=780, size=48)
stamp(S6, 90, 680, "Pas un compte à rebours", AL("compte", 32) - 0.2, rot=-3, size=52)

# =====================================================================  S7 : Paul et Pierre (lignes 33-36)
t = LS[33] - 0.4
cam(t, S7)
headline(S7, 170, ["Paul et [Pierre]"], t + 0.1, kicker="1 Thessaloniciens · 2 Pierre", hl_t=AL("Pierre", 35) + 0.05, size=104)
S_(S7, "paul", 1500, 420, 170, AL("Paul", 33) - 0.3, rot=-2)
t33 = [tag(S7, 90, 430, "Thessalonique", AL("Thessalonique", 33) - 0.3, "", 52), tag(S7, 90, 540, "Ne pas se laisser troubler", AL("troubler", 33) - 0.6, "acc", 46)]
gone(t33, LS[34] - 0.5)
kq(S7, 90, 420, "1 Thessaloniciens 5.2 · Louis Segond 1910", "« le jour du Seigneur viendra comme un voleur dans la nuit »", 34, "le", width=900, size=42,
   last=AL("nuit", 34) + 0.5, fade_at=LS[35] - 0.4)
t34 = tag(S7, 90, 700, "Un voleur ne prévient pas", AL("prévient", 34) - 0.6, "acc", 50)
gone([t34], LS[35] - 0.5)
S_(S7, "sablier", 1250, 420, 110, AL("Pierre", 35) - 0.2, rot=2)
kq(S7, 90, 420, "2 Pierre 3.8-9 · Louis Segond 1910",
   "« devant le Seigneur, un jour est comme mille ans, et mille ans sont comme un jour. Le Seigneur ne tarde pas dans l'accomplissement de la promesse, "
   "comme quelques-uns le croient ; mais il use de patience envers vous, voulant que personne ne périsse, mais que tous arrivent à la repentance. »",
   35, "devant", width=900, size=32, fade_at=LS[36] - 0.4)
tag(S7, 90, 430, "Pas pour calculer", AL("calculer", 36) - 0.2, "", 52)
tag(S7, 90, 540, "Une patience, pas un retard", AL("patience", 36) - 0.4, "acc", 50)

# =====================================================================  S8 : William Miller (lignes 37-40)
t = LS[37] - 0.4
cam(t, S8)
headline(S8, 170, ["William [Miller], 1844"], t + 0.1, kicker="Dix-neuvième siècle", hl_t=AL("Miller", 37) + 0.05, size=96)
f37 = tag(S8, 90, 430, "Une longue histoire de dates", LS[37] + 0.3, "", 52)
fade(f37, AL("Daniel", 37) - 0.6)
S_(S8, "miller", 1500, 420, 190, AL("Miller", 37) - 0.3, rot=-2)
t37 = [tag(S8, 90, 430, "Les prophéties de Daniel", AL("Daniel", 37) - 0.3, "", 48), tag(S8, 90, 560, "Retour attendu vers 1843", AL("quarante-trois", 37) - 1.0, "acc", 52)]
gone(t37, LS[38] - 0.5)
c38 = card(S8, 90, 420, "Date fixée", "22 octobre 1844", AL("vingt-deux", 38) - 0.4, w=720, size=52)
t38 = [tag(S8, 90, 640, "Des dizaines de milliers de personnes", AL("dizaines", 38) - 0.2, "", 42), tag(S8, 90, 750, "Champs laissés, biens vendus", AL("champ", 38) - 0.3, "", 40)]
gone([c38] + t38, LS[39] - 0.5)
s39 = [stamp(S8, 90, 430, "Rien", AL("Rien", 39) - 0.1, rot=-4, size=84),
       tag(S8, 90, 650, "Le Grand Désappointement", AL("Désappointement", 39) - 0.6, "acc", 52)]
gone(s39, LS[40] - 0.5)
t40 = [tag(S8, 90, 430, "Églises adventistes", AL("adventistes", 40) - 0.5, "", 48), tag(S8, 90, 540, "Plus de dates fixées", AL("renoncé", 40) - 0.5, "acc", 48)]

# =====================================================================  S9 : le même schéma (lignes 41-45)
t = LS[41] - 0.4
cam(t, S9)
headline(S9, 170, ["Le même [schéma]"], t + 0.1, kicker="L'histoire des dates", hl_t=AL("schéma", 43) + 0.05, size=104)
S_(S9, "sablier", 1500, 420, 110, AL("leurope", 41) - 0.2, rot=-2)
c41 = card(S9, 90, 420, "L'an mille", "Une panique générale ? Surtout une légende", AL("leurope", 41) - 0.2, w=900, size=40)
t41 = tag(S9, 90, 620, "Construite plus tard", AL("légende", 41) - 0.8, "acc", 50)
gone([c41, t41], LS[42] - 0.5)
c42 = card(S9, 90, 420, "Calendrier maya · 2012", "Fin d'un cycle de comptage, pas une prédiction de fin du monde", AL("maya", 42) - 0.5, w=900, size=38)
gone([c42], LS[43] - 0.5)
bx = [card(S9, 90, 420, "Étape 1", "Une date", AL("date", 43) - 0.3, w=400, size=34),
      card(S9, 580, 420, "Étape 2", "Une peur", AL("peur", 43) - 0.3, w=400, size=34),
      card(S9, 90, 600, "Étape 3", "Un silence", AL("silence", 43) - 0.3, w=400, size=34),
      card(S9, 580, 600, "Étape 4", "Une nouvelle date", AL("nouvelle", 43) - 0.3, w=400, size=34, accent=True)]
gone(bx, LS[44] - 0.5)
c44 = card(S9, 90, 420, "Pourquoi ?", "L'incertitude fait peur : une date donne l'impression de reprendre le contrôle", AL("Pourquoi", 44) - 0.1, w=900, size=38)
gone([c44], LS[45] - 0.5)
stamp(S9, 90, 440, "Pas une date", AL("date", 45) - 0.3, rot=-4, size=76)
tag(S9, 90, 620, "Une manière de vivre", AL("vivre", 45) - 0.8, "acc", 56)

# =====================================================================  S10 : l'Apocalypse (lignes 46-52)
t = LS[46] - 0.4
cam(t, S10)
headline(S10, 170, ["L'[Apocalypse]"], t + 0.1, kicker="Le livre le plus cité", hl_t=AL("lapocalypse", 46) + 0.05, size=110)
S_(S10, "cavaliers", 1500, 420, 255, AL("lapocalypse", 46) - 0.2, rot=2)
c47 = card(S10, 90, 420, "Du grec apokalypsis", "dévoilement, révélation", AL("apokalypsis", 47) - 0.3, w=780, size=44)
s47 = stamp(S10, 90, 620, "≠ catastrophe", AL("catastrophe", 47) - 0.3, rot=-3, size=64)
gone([c47, s47], LS[48] - 0.5)
S_(S10, "jean-pied", 1200, 420, 185, AL("Heureux", 48) - 0.2, rot=-2)
kq(S10, 90, 420, "Apocalypse 1.3 · Louis Segond 1910",
   "« Heureux celui qui lit et ceux qui entendent les paroles de la prophétie, et qui gardent les choses qui y sont écrites ! Car le temps est proche. »",
   48, "heureux", width=900, size=36, fade_at=LS[49] - 0.4)
t49 = [tag(S10, 90, 430, "Sept Églises bien réelles", AL("sept", 49) - 0.2, "", 52), tag(S10, 90, 540, "Asie Mineure · Turquie actuelle", AL("Turquie", 49) - 0.7, "", 44),
       tag(S10, 90, 650, "Sous l'Empire romain", AL("lempire", 49) - 0.3, "acc", 48)]
gone(t49, LS[50] - 0.5)
cc = [card(S10, 90, 420, "Lecture 1", "Le monde des premiers lecteurs", AL("monde", 50) - 0.3, w=400, size=30),
      card(S10, 580, 420, "Lecture 2", "L'histoire de l'Église", AL("lhistoire", 50) - 0.3, w=400, size=30),
      card(S10, 90, 640, "Lecture 3", "Des événements à venir", AL("venir", 50) - 0.3, w=400, size=30),
      card(S10, 580, 640, "Lecture 4", "Un tableau symbolique", AL("symbolique", 50) - 0.3, w=400, size=30, accent=True)]
gone(cc, LS[51] - 0.5)
c51 = card(S10, 90, 420, "Les nombres", "mille ans, cent quarante-quatre mille : d'abord des symboles", AL("nombres", 51) - 0.2, w=900, size=38)
s51 = stamp(S10, 90, 690, "Pas un code", AL("code", 51) - 0.3, rot=-4, size=64)
gone([c51, s51], LS[52] - 0.5)
kq(S10, 90, 420, "Apocalypse 22.20 · Louis Segond 1910", "« Oui, je viens bientôt. »", 52, "oui", width=700, size=48, last=AL("bientôt", 52) + 0.5,
   fade_at=LS[53] - 0.45)
tag(S10, 90, 660, "« Viens, Seigneur Jésus ! »", AL("Viens", 52) - 0.3, "acc", 56)

# =====================================================================  S11 : parousia et veiller (lignes 53-56)
t = LS[53] - 0.4
cam(t, S11)
headline(S11, 170, ["La [parousia]"], t + 0.1, kicker="Présence, arrivée", hl_t=AL("parousia", 53) + 0.05, size=104)
c53 = card(S11, 90, 420, "En grec", "<b>parousia</b> : présence, arrivée", AL("parousia", 53) - 0.3, w=800, size=44)
t53 = tag(S11, 90, 600, "La visite officielle d'un roi", AL("roi", 53) - 0.4, "", 46)
gone([c53, t53], LS[54] - 0.5)
s54 = stamp(S11, 90, 440, "Pas un compte à rebours", AL("compte", 54) - 0.3, rot=-3, size=56)
t54 = tag(S11, 90, 600, "Une arrivée attendue", AL("arrivée", 54) - 0.4, "acc", 54)
gone([s54, t54], LS[55] - 0.5)
kq(S11, 90, 420, "Matthieu 24.42 · Louis Segond 1910", "« Veillez donc, puisque vous ne savez pas quel jour votre Seigneur viendra. »", 55, "veillez",
   width=900, size=42, fade_at=LS[56] - 0.4)
tag(S11, 90, 740, "Veiller = rester éveillé", AL("éveillé", 55) - 0.5, "acc", 46)
S_(S11, "veilleur", 1500, 420, 290, AL("ciel", 56) - 0.3, rot=2)
S_(S11, "vierge-lampe", 1160, 420, 190, AL("huile", 56) - 0.3, rot=-2)
S_(S11, "pain", 740, 420, 320, AL("affamés", 56) - 0.3, rot=2)

# =====================================================================  S12 : trois questions (lignes 57-60)
t = LS[57] - 0.4
cam(t, S12)
headline(S12, 170, ["Trois [questions]"], t + 0.1, kicker="Face à une prophétie", hl_t=AL("trois", 57) + 0.05, size=104)
f57 = tag(S12, 90, 430, "Trois questions simples", LS[57] + 0.3, "acc", 56)
fade(f57, AL("date", 58) - 0.8)
card(S12, 90, 420, "Question 1", "Donne-t-elle une date ?", AL("date", 58) - 0.3, w=500, size=34)
tag(S12, 90, 650, "Contredit Matthieu 24.36", AL("contredit", 58) - 0.2, "acc", 34)
card(S12, 690, 420, "Question 2", "Te pousse-t-elle à la peur ?", AL("peur", 59) - 0.3, w=500, size=34)
tag(S12, 690, 650, "Gardez-vous d'être troublés", AL("troublés", 59) - 0.5, "acc", 32)
card(S12, 1300, 420, "Question 3", "Te demande-t-elle de l'argent ?", AL("quitter", 60) - 0.3, w=500, size=34)
tag(S12, 1300, 650, "Garde-toi d'être séduit", AL("séduise", 60) - 0.8, "acc", 32)

# =====================================================================  S13 : accompagnement et question (lignes 61-62)
t = LS[61] - 0.4
cam(t, S13)
headline(S13, 170, ["Tu n'es pas [seul]"], t + 0.1, kicker="Si l'angoisse prend trop de place", hl_t=AL("seul", 61) + 0.05, size=104)
glow(S13, 1560, 540, AL("langoisse", 61), size=360, dur=8.0)
S_(S13, "mains-lampe", 1420, 420, 300, AL("langoisse", 61) - 0.2, rot=2)
t61 = [tag(S13, 90, 430, "Un médecin", AL("médecin", 61) - 0.1, "", 52), tag(S13, 90, 540, "Un psychologue", AL("psychologue", 61) - 0.1, "", 52),
       tag(S13, 90, 650, "Un proche de confiance", AL("proche", 61) - 0.1, "", 52), tag(S13, 90, 760, "Cela n'enlève rien à la foi", AL("nenlève", 61) - 0.3, "acc", 46)]
gone(t61, LS[62] - 0.5)
tq2 = tag(S13, 90, 430, "Une promesse qui t'a aidé ?", LS[62] + 0.4, "acc", 54)
cta = put(S13, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Partage-la en commentaire', "cta")
blur_in(cta, AL("commentaire", 62) - 1.0, 14)
sfx("click", AL("commentaire", 62) - 1.0, 0.8)

# =====================================================================  S1 (revisité) : conclusion (lignes 63-66)
cam(LS[63] - 2.0, "all")
wipe(S1, LS[63] - 2.1)
t = LS[63] - 0.4
cam(t, S1)
headline(S1, 170, ["Le monde était [toujours là]"], t + 0.1, kicker="21 octobre 2011", hl_t=AL("toujours", 63) + 0.05, size=96)
an2 = S_(S1, "animateur", 1500, 420, 190, AL("matin", 63) - 0.3, rot=2)
fade(an2, LS[65] - 0.5)
t63 = tag(S1, 90, 430, "Le jour et l'heure restent le secret du Père", AL("secret", 63) - 1.2, "acc", 48)
gone([t63], LS[64] - 0.5)
t64 = [tag(S1, 90, 430, "Elle appartient à Dieu", AL("Dieu", 64) - 0.2, "", 52), tag(S1, 90, 540, "Elle ne se calcule pas", AL("calcule", 64) - 0.3, "", 52),
       tag(S1, 90, 650, "L'espérance ne dépend d'aucune date", AL("lespérance", 64) - 0.5, "acc", 46)]
gone(t64, LS[65] - 0.5)
gH = glow(S1, 900, 600, LS[65], size=520, dur=9.0)
f65 = tag(S1, 90, 430, "Ce que le texte nous laisse", LS[65] + 0.2, "", 54)
fade(f65, AL("veiller", 65) - 0.6)
w65 = []
for _x, _w, _k in ((90, "veiller", "veiller"), (660, "aimer", "aimer"), (1080, "espérer", "espérer")):
    wid = put(S1, _x, 500, _w, "word", "font-size:110px")
    blur_in(wid, AL(_k, 65) - 0.1, 20)
    w65.append(wid)
gone(w65, LS[66] - 0.2)

t_end = AL("Chaque", 66) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(LS[63] - 2.8, LS[63] - 0.5), (AL("Chaque", 66) - 0.8, DUR_)]
build(
    chapters=[("01", "Les dates annoncées", 0, LS[8]), ("02", "Nostradamus", LS[8], LS[15]), ("03", "Ce que dit Jésus", LS[15], LS[37]),
              ("04", "L'histoire des dates", LS[37], LS[46]), ("05", "L'Apocalypse", LS[46], LS[53]), ("06", "Veiller", LS[53], DUR_)],
    suppress=supp,
    endcard={"kicker": "Chaque semaine", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("jean-portrait", 150, 560, 300, -6), ("vierge-lampe", 1550, 330, 180, 5)]},
    endcard_t=AL("Chaque", 66) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
