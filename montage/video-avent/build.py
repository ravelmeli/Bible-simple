"""Vidéo longue « L'Avent : d'où vient cette fête ? Ce que la Bible dit vraiment » — style 02, 16:9.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py), option retention, thème beige.
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

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Avent - style 02", "lang": "fr",
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
# =====================================================================  S1 : accroche (lignes 1-6)
cam(0, S1)
headline(S1, 170, ["Le mot « [Avent] » est absent"], 0.0, kicker="Dans la Bible", hl_t=AL("Avent", 1) + 0.05, size=96)
S_(S1, "livres", 1500, 420, 200, 0.0, rot=2, instant=True)
t1 = tag(S1, 90, 430, "Nulle part dans la Bible", 0.3, "acc", 52)
gone([t1], LS[2] - 0.4)
t2 = [tag(S1, 90, 430, "Une première bougie", AL("bougie", 2) - 0.3, "", 52), tag(S1, 90, 540, "Un calendrier de l'Avent", AL("calendrier", 2) - 0.3, "", 52), tag(S1, 90, 650, "Attendre Noël", AL("Noël", 2) - 0.5, "acc", 52)]
gone(t2, LS[3] - 0.4)
t3 = [tag(S1, 90, 430, "D'où vient cette habitude ?", LS[3] + 0.2, "", 50), tag(S1, 90, 540, "Que dit la Bible de l'attente ?", AL("attente", 3) - 0.4, "", 48), tag(S1, 90, 650, "Qu'ont ajouté les siècles ?", AL("siècles", 3) - 0.5, "acc", 48)]
gone(t3, LS[4] - 0.4)
t4 = [tag(S1, 90, 430, "Ce que dit le texte", E("texte", 4, 0.4, 0.6), "", 52), tag(S1, 90, 540, "Ce que dit la tradition", AL("tradition", 4) - 0.3, "", 52), tag(S1, 90, 650, "Une habitude moderne", AL("moderne", 4) - 0.4, "acc", 52)]
gone(t4, LS[5] - 0.4)
tag(S1, 90, 430, "L'avenir autant que le passé", E("avenir", 5, 0.3, 0.6), "acc", 50)

# =====================================================================  S2 : adventus, parousia (lignes 7-13)
t = LS[7] - 0.4
cam(t, S2)
headline(S2, 170, ["Un mot d'[empereur]"], t + 0.1, kicker="Adventus · parousia", hl_t=AL("empereur", 8) + 0.05, size=104)
S_(S2, "soldat", 1500, 420, 150, LS[8] + 0.3, rot=2)
c7 = card(S2, 90, 420, "Latin : adventus", "« arrivée », « venue »", E("arrivée", 7, 0.3, 0.6), w=900, size=52)
gone([c7], LS[8] - 0.4)
t8 = [tag(S2, 90, 430, "L'entrée solennelle d'un empereur", AL("empereur", 8) - 0.4, "", 46), tag(S2, 90, 540, "La ville se pare", AL("fêtes", 8) - 1.4, "acc", 52)]
gone(t8, LS[9] - 0.4)
c9 = card(S2, 90, 420, "Grec : parousia", "« présence », « venue »", AL("parousia", 9) - 0.3, w=900, size=52)
t9 = tag(S2, 90, 640, "Aussi la visite d'un roi", AL("visite", 9) - 0.4, "acc", 52)
gone([c9, t9], LS[10] - 0.4)
t10 = tag(S2, 90, 430, "Le vocabulaire d'un souverain", AL("vocabulaire", 10) - 0.5, "", 52)
gone([t10], LS[11] - 0.4)
t11 = [stamp(S2, 90, 440, "Un autre roi vient", E("roi", 11, 0.4, 0.8), rot=-3, size=70)]
gone(t11, LS[12] - 0.4)
c12 = card(S2, 90, 420, "Grec : epiphaneia", "« apparition »", AL("epiphaneia", 12) - 0.3, w=800, size=52)
gone([c12], LS[13] - 0.4)
tag(S2, 90, 430, "Pas un compte à rebours de cadeaux", AL("cadeaux", 13) - 0.9, "", 46)
tag(S2, 90, 540, "L'arrivée d'un roi", AL("roi", 13) - 0.5, "acc", 56)

# =====================================================================  S3 : quatre semaines, une tradition (lignes 14-18)
t = LS[14] - 0.4
cam(t, S3)
headline(S3, 170, ["Quatre semaines : une [tradition]"], t + 0.1, kicker="Pas dans la Bible", hl_t=AL("tradition", 15) + 0.05, size=96)
S_(S3, "rouleau", 1500, 420, 220, LS[16] + 0.3, rot=2)
t14 = tag(S3, 90, 430, "Aucune période de 4 semaines", E("surprise", 14, 0.3, 0.6), "acc", 50)
gone([t14], LS[15] - 0.4)
t15 = tag(S3, 90, 430, "Bâtie progressivement par l'Église", E("progressivement", 15, 0.6, 0.8), "", 48)
gone([t15], LS[16] - 0.4)
t16 = [tag(S3, 90, 430, "IVe siècle · Espagne", AL("Espagne", 16) - 0.3, "", 50), tag(S3, 90, 540, "Ve siècle · Gaule : 40 jours", AL("Gaule", 16) - 0.3, "", 50)]
gone(t16, LS[17] - 0.4)
t17 = [tag(S3, 90, 430, "VIe siècle · Rome : 4 semaines", AL("Rome", 17) - 0.3, "", 50), tag(S3, 90, 540, "L'Orient : d'autres usages", AL("Orient", 17) - 0.3, "acc", 50)]
gone(t17, LS[18] - 0.4)
tag(S3, 90, 430, "Orthodoxes : 40 jours dès le 15 novembre", AL("novembre", 18) - 0.5, "", 44)
tag(S3, 90, 540, "Protestants : des pratiques variées", AL("protestantes", 18) - 0.3, "acc", 46)

# =====================================================================  S4 : le 25 décembre (lignes 19-24)
t = LS[19] - 0.4
cam(t, S4)
headline(S4, 170, ["Le [25 décembre]"], t + 0.1, kicker="Pas dans la Bible non plus", hl_t=AL("décembre", 19) + 0.05, size=112)
S_(S4, "sym-balance", 1450, 420, 260, LS[21] + 0.3, rot=2)
t19 = tag(S4, 90, 430, "La date n'est pas dans la Bible", LS[19] + 0.3, "acc", 50)
gone([t19], LS[20] - 0.4)
t20 = [tag(S4, 90, 430, "Les évangiles : pas de date", AL("évangiles", 20) - 0.3, "", 50), tag(S4, 90, 540, "Première trace : Rome, IVe siècle", AL("Rome", 20) - 0.5, "acc", 48)]
gone(t20, LS[21] - 0.4)
t21 = [stamp(S4, 90, 440, "Deux hypothèses", AL("hypothèses", 21) - 0.3, rot=-3, size=70), tag(S4, 90, 620, "Fêtes païennes du soleil ?", AL("soleil", 21) - 0.6, "", 48), tag(S4, 90, 730, "Calcul depuis la mort de Jésus ?", AL("mort", 21) - 0.5, "", 46)]
gone(t21, LS[22] - 0.4)
t22 = [tag(S4, 90, 430, "Les historiens divergent", AL("historiens", 22) - 0.3, "", 52), stamp(S4, 90, 560, "Pas de certitude", AL("certitude", 22) - 0.6, rot=-3, size=64)]
gone(t22, LS[23] - 0.4)
c23 = card(S4, 90, 420, "Première révélation", "Une tradition belle, pas une prescription", AL("révélation", 23) - 0.4, w=1000, size=48)
gone([c23], LS[24] - 0.4)
tag(S4, 90, 430, "Restez : la couronne, le calendrier", LS[24] + 0.3, "acc", 48)

# =====================================================================  S5 : les promesses (lignes 25-32)
t = LS[25] - 0.4
cam(t, S5)
headline(S5, 170, ["Des siècles [d'attente]"], t + 0.1, kicker="Ésaïe · Michée", hl_t=AL("attendre", 25) + 0.05, size=104)
S_(S5, "scribe", 1500, 420, 190, LS[27] + 0.3, rot=2)
t25 = tag(S5, 90, 430, "Elle parle beaucoup d'attendre", LS[25] + 0.3, "acc", 50)
gone([t25], LS[26] - 0.4)
t26 = [tag(S5, 90, 430, "Un roi", AL("roi", 26) - 0.3, "", 56), tag(S5, 90, 540, "Un sauveur", AL("sauveur", 26) - 0.3, "", 56), tag(S5, 90, 650, "Un libérateur", AL("libérateur", 26) - 0.3, "acc", 56)]
gone(t26, LS[27] - 0.4)
c27 = card(S5, 90, 420, "Ésaïe 9" + BIB, "« un enfant nous est né, un fils nous est donné »", AL("enfant", 27) - 0.5, w=1000, size=44)
gone([c27], LS[28] - 0.4)
c28 = card(S5, 90, 420, "Michée 5", "Bethléhem, « petite entre les milliers de Juda »", AL("Bethléhem", 28) - 0.4, w=1000, size=44)
gone([c28], LS[29] - 0.4)
c29 = card(S5, 90, 420, "Ésaïe 7" + BIB, "« la vierge deviendra enceinte… Emmanuel »", AL("vierge", 29) - 0.5, w=1000, size=44)
gone([c29], LS[30] - 0.4)
c30 = put(S5, 90, 420, "<small>Mot hébreu</small><span style='font-size:84px'>almah</span> « jeune femme »", "card", "width:900px;font-size:58px")
blur_in(c30, AL("almah", 30) - 0.3, 14)
gone([c30], LS[31] - 0.4)
c31 = put(S5, 90, 420, "<small>Septante · grec</small><span style='font-size:84px'>parthenos</span> « vierge »", "card", "width:900px;font-size:58px")
blur_in(c31, AL("parthenos", 31) - 0.3, 14)
gone([c31], LS[32] - 0.4)
stamp(S5, 90, 440, "Emmanuel : « Dieu avec nous »", AL("Emmanuel", 32) - 0.4, rot=-3, size=56)

# =====================================================================  S6 : ruines et promesse (lignes 33-38)
t = LS[33] - 0.4
cam(t, S6)
headline(S6, 170, ["Une promesse dans les [ruines]"], t + 0.1, kicker="Ésaïe 11 · Jérémie 33 · Ésaïe 40", hl_t=AL("ruines", 36) + 0.05 if False else E("sombres", 36, 0.2, 2.0), size=92)
S_(S6, "ville", 1450, 420, 300, LS[34] + 0.3, rot=2)
c33 = card(S6, 90, 420, "Ésaïe 11" + BIB, "« Un rameau sortira du tronc d'Isaï »", AL("rameau", 33) - 0.4, w=1000, size=44)
gone([c33], LS[34] - 0.4)
c34 = card(S6, 90, 420, "Jérémie 33" + BIB, "« j'accomplirai la bonne parole »", AL("promesse", 34) - 1.4, w=1000, size=44)
t34 = tag(S6, 90, 650, "Promesse faite pendant l'exil", AL("exil", 34) - 0.4, "acc", 48)
gone([c34, t34], LS[35] - 0.4)
c35 = card(S6, 90, 420, "Ésaïe 40" + BIB, "« Consolez, consolez mon peuple »", AL("Consolez", 35) - 0.3, w=1000, size=46)
gone([c35], LS[36] - 0.4)
t36 = [tag(S6, 90, 430, "Des époques sombres", E("sombres", 36, 0.3, 0.6), "", 52), tag(S6, 90, 540, "Une promesse murmurée", AL("ruines", 36) - 0.6, "acc", 52)]
gone(t36, LS[37] - 0.4)
c37 = card(S6, 90, 420, "Période intertestamentaire", "≈ 4 siècles de silence", AL("intertestamentaire", 37) - 0.5, w=900, size=48)
gone([c37], LS[38] - 0.4)
tag(S6, 90, 430, "Pas de prophète reconnu", AL("prophète", 38) - 0.3, "", 50)
tag(S6, 90, 540, "Un peuple sous domination", AL("domination", 38) - 0.3, "", 50)
tag(S6, 90, 650, "Une attente douloureuse", AL("douloureuse", 38) - 0.5, "acc", 50)

# =====================================================================  S7 : préparer le chemin (lignes 39-41)
t = LS[39] - 0.4
cam(t, S7)
headline(S7, 170, ["Préparer le [chemin]"], t + 0.1, kicker="Luc 3", hl_t=AL("Préparez", 39) + 0.05, size=112)
S_(S7, "veilleur", 1500, 420, 200, LS[39] + 0.5, rot=2)
c39 = card(S7, 90, 420, "Luc 3" + BIB, "« Préparez le chemin du Seigneur, aplanissez ses sentiers »", AL("Préparez", 39) - 0.3, w=1000, size=42)
gone([c39], LS[40] - 0.4)
t40 = [tag(S7, 90, 430, "Le cœur de l'Avent", E("chemin", 40, 0.5, 0.8), "acc", 56), tag(S7, 90, 540, "On réparait les routes avant un roi", AL("routes", 40) - 0.4, "", 46)]
gone(t40, LS[41] - 0.4)
tag(S7, 90, 430, "Préparer son cœur comme une route", AL("route", 41) - 0.8, "acc", 50)

# =====================================================================  S8 : les personnages de Luc (lignes 42-54)
t = LS[42] - 0.4
cam(t, S8)
headline(S8, 170, ["Ceux qui [attendent]"], t + 0.1, kicker="Évangile de Luc", hl_t=AL("attendent", 42) + 0.05, size=112)
S_(S8, "ancien", 1500, 420, 190, LS[43] + 0.3, rot=2)
t42 = tag(S8, 90, 430, "Des personnages qui attendent", LS[42] + 0.3, "acc", 48)
gone([t42], LS[43] - 0.4)
t43 = [tag(S8, 90, 430, "Zacharie, prêtre âgé", AL("Zacharie", 43) - 0.3, "", 52), tag(S8, 90, 540, "Il doute, il perd la parole", AL("parole", 43) - 0.5, "acc", 48)]
gone(t43, LS[44] - 0.4)
t44 = [stamp(S8, 90, 440, "Neuf mois de silence", AL("silence", 44) - 0.5, rot=-3, size=60)]
gone(t44, LS[45] - 0.4)
c45 = card(S8, 90, 420, "Luc 1" + BIB, "« Je suis la servante du Seigneur »", AL("servante", 45) - 0.4, w=1000, size=44)
gone([c45], LS[46] - 0.4)
c46 = card(S8, 90, 420, "Le Magnificat", "« Mon âme exalte le Seigneur »", AL("exalte", 46) - 0.5, w=1000, size=46)
gone([c46], LS[47] - 0.4)
t47 = [tag(S8, 90, 430, "Joseph : un songe", AL("songe", 47) - 0.3, "", 52), tag(S8, 90, 540, "Il hésite, puis il accueille", AL("accueille", 47) - 0.6, "acc", 50)]
gone(t47, LS[48] - 0.4)
t48 = [tag(S8, 90, 430, "Édit d'Auguste : un recensement", AL("recensement", 48) - 0.5, "", 48), tag(S8, 90, 540, "Joseph et Marie montent à Bethléhem", AL("Bethléhem", 48) - 0.3, "", 46)]
gone(t48, LS[49] - 0.4)
c49 = card(S8, 90, 420, "Luc 2" + BIB, "« l'emmaillota et le coucha dans une crèche »", AL("emmaillota", 49) - 0.5, w=1000, size=44)
gone([c49], LS[50] - 0.4)
c50 = put(S8, 90, 420, "<small>Mot grec</small><span style='font-size:84px'>kataluma</span> une pièce d'accueil", "card", "width:1000px;font-size:50px")
blur_in(c50, AL("kataluma", 50) - 0.3, 14)
gone([c50], LS[51] - 0.4)
s51 = stamp(S8, 90, 440, "Un lieu modeste", AL("modeste", 51) - 0.5, rot=-3, size=70)
gone([s51], LS[52] - 0.4)
t52 = [tag(S8, 90, 430, "Le doute · la confiance", AL("doute", 52) - 0.3, "", 50), tag(S8, 90, 540, "Le silence · la décision", AL("décision", 52) - 0.5, "", 50)]
gone(t52, LS[53] - 0.4)
t53 = [tag(S8, 90, 430, "Syméon : « la consolation d'Israël »", AL("Syméon", 53) - 0.3, "", 46), tag(S8, 90, 540, "Anne, prophétesse", AL("Anne", 53) - 0.3, "acc", 52)]
gone(t53, LS[54] - 0.4)
tag(S8, 90, 430, "Une attente récompensée", AL("récompensée", 54) - 0.5, "acc", 52)

# =====================================================================  S9 : deux venues (lignes 55-62)
t = LS[55] - 0.4
cam(t, S9)
headline(S9, 170, ["Deux [venues]"], t + 0.1, kicker="Bethléhem et la fin des temps", hl_t=AL("seconde", 56) + 0.05, size=112)
S_(S9, "porte-ville", 1450, 420, 300, LS[56] + 0.3, rot=2)
t55 = tag(S9, 90, 430, "L'Avent ne parle pas que de Bethléhem", LS[55] + 0.3, "acc", 46)
gone([t55], LS[56] - 0.4)
t56 = [tag(S9, 90, 430, "1re venue : l'enfant de Bethléhem", AL("première", 56) - 0.3, "", 48), tag(S9, 90, 540, "2e venue : la fin des temps", AL("seconde", 56) - 0.3, "acc", 48)]
gone(t56, LS[57] - 0.4)
c57 = card(S9, 90, 420, "Matthieu 24" + BIB, "« Veillez donc… »", AL("Veillez", 57) - 0.3, w=900, size=52)
gone([c57], LS[58] - 0.4)
c58 = card(S9, 90, 420, "Apocalypse 22" + BIB, "« Viens, Seigneur Jésus ! »", AL("Viens", 58) - 0.5, w=900, size=52)
gone([c58], LS[59] - 0.4)
c59 = put(S9, 90, 420, "<small>Mot araméen · 1 Corinthiens 16</small><span style='font-size:84px'>maranatha</span>", "card", "width:1000px;font-size:46px")
blur_in(c59, AL("maranatha", 59) - 0.3, 14)
gone([c59], LS[60] - 0.4)
t60 = [tag(S9, 90, 430, "« Notre Seigneur, viens ! »", AL("manières", 60) - 0.2, "", 52), tag(S9, 90, 540, "« Notre Seigneur vient. »", AL("viens", 60, 1) - 0.4 if False else E("traduction", 60, 2.0, 3.0), "acc", 52)]
gone(t60, LS[61] - 0.4)
s61 = stamp(S9, 90, 440, "Une prière : Viens", AL("prière", 61) - 0.4, rot=-3, size=70)
gone([s61], LS[62] - 0.4)
tag(S9, 90, 620, "Regarder en arrière, regarder en avant", AL("étrange", 62) - 0.5, "acc", 44)

# =====================================================================  S10 : couronne et calendrier (lignes 63-67)
t = LS[63] - 0.4
cam(t, S10)
headline(S10, 170, ["Couronne et [calendrier]"], t + 0.1, kicker="Ce qui s'est ajouté", hl_t=AL("couronne", 63) + 0.05, size=104)
S_(S10, "livres", 1500, 420, 200, LS[65] + 0.3, rot=2)
t63 = tag(S10, 90, 430, "La couronne : assez récente", AL("couronne", 63) - 0.3, "acc", 50)
gone([t63], LS[64] - 0.4)
t64 = [tag(S10, 90, 430, "XIXe siècle · Allemagne", E("Wichern", 64, 0.3, 0.8) if False else LS[64] + 0.3, "", 50), tag(S10, 90, 540, "Wichern, pasteur à Hambourg", AL("Wichern", 64) - 0.3, "acc", 48)]
gone(t64, LS[65] - 0.4)
t65 = [tag(S10, 90, 430, "Le calendrier : Allemagne aussi", AL("calendrier", 65) - 0.3, "", 50), tag(S10, 90, 540, "De petites cases", AL("cases", 65) - 0.3, "", 52)]
gone(t65, LS[66] - 0.4)
t66 = [tag(S10, 90, 430, "4 bougies : espérance, paix, joie, amour", AL("espérance", 66) - 0.3, "", 42), stamp(S10, 90, 560, "Noms variables", AL("fixe", 66) - 0.6, rot=-3, size=60)]
gone(t66, LS[67] - 0.4)
tag(S10, 90, 430, "Gestes d'Église, pas commandements", AL("gestes", 67) - 0.3, "acc", 46)

# =====================================================================  S11 : ce qu'on garde (lignes 68-76)
t = LS[68] - 0.4
cam(t, S11)
headline(S11, 170, ["Ce qu'on peut [garder]"], t + 0.1, kicker="Aujourd'hui", hl_t=AL("garder", 68) + 0.05, size=104)
S_(S11, "veilleur", 1500, 420, 200, LS[69] + 0.3, rot=2)
t68 = tag(S11, 90, 430, "Que garder de l'Avent ?", LS[68] + 0.2, "acc", 52)
gone([t68], LS[69] - 0.4)
t69 = [tag(S11, 90, 430, "1. L'attente", AL("attente", 69) - 0.3, "", 56), tag(S11, 90, 540, "Un acte de résistance", AL("résistance", 69) - 0.5, "acc", 50)]
gone(t69, LS[70] - 0.4)
t70 = [tag(S11, 90, 430, "2. La préparation", AL("préparation", 70) - 0.3, "", 56), tag(S11, 90, 540, "Ralentir", AL("ralentir", 70) - 0.3, "acc", 56)]
gone(t70, LS[71] - 0.4)
t71 = [tag(S11, 90, 430, "3. L'espérance", AL("espérance", 71) - 0.3, "", 56), tag(S11, 90, 540, "Dieu tient ses promesses", AL("promesses", 71) - 0.4, "acc", 50)]
gone(t71, LS[72] - 0.4)
c72 = put(S11, 90, 420, "<small>Mot hébreu</small><span style='font-size:84px'>tiqvah</span> « espérance »", "card", "width:900px;font-size:56px")
blur_in(c72, AL("tiqvah", 72) - 0.3, 14)
t72 = tag(S11, 90, 700, "Racine qavah : attendre, tendre vers", AL("qavah", 72) - 0.4, "acc", 46)
gone([c72, t72], LS[73] - 0.4)
c73 = card(S11, 90, 420, "Josué 2" + BIB, "tiqvah = aussi une corde (le cordon écarlate)", AL("corde", 73) - 0.5, w=1000, size=44)
gone([c73], LS[74] - 0.4)
t74 = [stamp(S11, 90, 440, "Une lecture, pas un fait", AL("lecture", 74) - 0.5, rot=-3, size=58), tag(S11, 90, 620, "Une corde tendue : une attente qui tient", AL("corde", 74) - 0.4, "", 44)]
gone(t74, LS[75] - 0.4)
c75 = put(S11, 90, 420, "<small>Gaudete · Philippiens 4</small><span style='font-size:70px'>« Réjouissez-vous »</span>", "card", "width:1000px;font-size:46px")
blur_in(c75, AL("Gaudete", 75) - 0.3, 14)
gone([c75], LS[76] - 0.4)
tag(S11, 90, 430, "La joie qui sait que la route avance", AL("fatigue", 76) - 0.5, "acc", 46)

# =====================================================================  S12 : période difficile (lignes 77-81)
t = LS[77] - 0.4
cam(t, S12)
headline(S12, 170, ["Quand la fête est [difficile]"], t + 0.1, kicker="Application", hl_t=AL("difficile", 77) + 0.05, size=96)
S_(S12, "pere", 1500, 420, 190, LS[79] + 0.3, rot=2)
t77 = tag(S12, 90, 430, "Une période difficile pour beaucoup", LS[77] + 0.3, "acc", 46)
gone([t77], LS[78] - 0.4)
t78 = [tag(S12, 90, 430, "Solitude", AL("solitude", 78) - 0.3, "", 52), tag(S12, 90, 540, "Deuil", AL("deuil", 78) - 0.3, "", 52), tag(S12, 90, 650, "Fatigue · à l'écart des fêtes", AL("fêtes", 78) - 0.6, "acc", 48)]
gone(t78, LS[79] - 0.4)
t79 = [tag(S12, 90, 430, "Vous n'êtes pas seul", AL("seul", 79) - 0.3, "acc", 56), tag(S12, 90, 540, "Anne, mère de Samuel : elle pleurait", AL("pleurait", 79) - 0.8, "", 44)]
gone(t79, LS[80] - 0.4)
t80 = [tag(S12, 90, 430, "Un proche", AL("proche", 80) - 0.3, "", 52), tag(S12, 90, 540, "Un pasteur", AL("pasteur", 80) - 0.3, "", 52), tag(S12, 90, 650, "Un professionnel de santé", AL("professionnel", 80) - 0.4, "acc", 52),
       stamp(S12, 90, 770, "Pas un manque de foi", AL("foi", 80) - 0.5, rot=-3, size=52)]
gone(t80, LS[81] - 0.4)
tq = tag(S12, 90, 430, "Qu'attendez-vous vraiment cette année ?", LS[81] + 0.4, "acc", 46)
cta = put(S12, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Dites-le en commentaire', "cta")
blur_in(cta, AL("commentaire", 81) - 1.0, 14)
sfx("click", AL("commentaire", 81) - 1.0, 0.8)
gone([tq, cta], LS[82] - 0.3)

# =====================================================================  S13 : conclusion (lignes 82-87)
t = LS[82] - 0.4
cam(t, S13)
headline(S13, 170, ["L'Avent, [attendre] un roi"], t + 0.1, kicker="La réponse", hl_t=AL("départ", 82) + 0.05, size=100)
S_(S13, "scribe", 1500, 420, 190, LS[85] + 0.3, rot=2)
t82 = tag(S13, 90, 430, "Pas dans la Bible, et pourtant…", LS[82] + 0.3, "acc", 50)
gone([t82], LS[83] - 0.4)
t83 = [tag(S13, 90, 430, "Un mot d'empereur", AL("empereurs", 83) - 0.4, "", 52), tag(S13, 90, 540, "Repris pour dire : un autre roi vient", E("autre", 83, 0.6, 3.0), "acc", 46)]
gone(t83, LS[84] - 0.4)
t84 = [tag(S13, 90, 430, "Des semaines, des bougies, des cases", AL("bougies", 84) - 0.4, "", 46), tag(S13, 90, 540, "Beau, pas obligatoire", AL("obligatoire", 84) - 0.5, "acc", 52)]
gone(t84, LS[85] - 0.4)
t85 = [tag(S13, 90, 430, "Préparer sa route", E("message", 85, 0.3, 0.6), "", 52), tag(S13, 90, 540, "Veiller", AL("veiller", 85) - 0.3, "", 52), tag(S13, 90, 650, "Espérer", AL("espérer", 85) - 0.3, "acc", 56)]
gone(t85, LS[86] - 0.4)
t86 = [stamp(S13, 90, 440, "La première bougie", AL("bougie", 86) - 0.5, rot=-3, size=64), tag(S13, 90, 620, "Ce qu'elle veut dire, et ce qu'elle ne dit pas", AL("veut", 86) - 0.5, "acc", 44)]
gone(t86, LS[87] - 0.3)

t_end = AL("Chaque", 87) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(AL("Chaque", 87) - 0.8, DUR_)]
build(
    chapters=[("01", "Le mot", 0, LS[14]), ("02", "La tradition", LS[14], LS[25]), ("03", "L'attente biblique", LS[25], LS[55]), ("04", "Aujourd'hui", LS[55], DUR_)],
    suppress=supp,
    endcard={"kicker": "Chaque semaine", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("scribe", 150, 560, 280, -6), ("jesus-portrait", 1550, 330, 230, 5)]},
    endcard_t=AL("Chaque", 87) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
