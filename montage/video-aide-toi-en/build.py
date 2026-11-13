"""Long video "God helps those who help themselves" isn't in the Bible: where does it come from? (Faith Engineering) — style 02, 16:9. English version of montage/video-aide-toi/.

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

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - God helps those who help themselves - style 02", "lang": "en",
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


PRE = ("",)


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
BIB = " · World English Bible"

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
headline(S1, 170, ["“God helps [those] who help themselves”"], 0.0, kicker="A sentence everyone knows", hl_t=AL("isn't", 1) + 0.05, size=88)
S_(S1, "foule", 1100, 420, 330, 0.0, rot=-3, instant=True)
st1 = stamp(S1, 90, 440, "Not in the Bible", AL("isn't", 1) - 0.1, rot=-4, size=76)
gone([st1], LS[3] - 0.3)
t3 = [tag(S1, 90, 430, "A trial", AL("trial", 3) - 0.1, "", 52), tag(S1, 90, 540, "An exam", AL("exam", 3) - 0.1, "", 52),
      tag(S1, 90, 650, "Almost a verse", AL("verse", 3) - 0.3, "acc", 52)]
gone(t3, LS[4] - 0.4)
st4 = [stamp(S1, 90, 440, "Not there", AL("find", 4) - 0.3, rot=-3, size=80), tag(S1, 90, 650, "From Genesis to Revelation", AL("Revelation", 4) - 1.0, "", 44)]
gone(st4, LS[5] - 0.4)
t5 = [tag(S1, 90, 430, "Where from?", AL("where", 5) - 0.1, "acc", 52), tag(S1, 90, 540, "Who said it first?", AL("Who", 5) - 0.1, "", 52),
      tag(S1, 90, 650, "Is it true?", AL("true", 5) - 0.3, "", 52)]
gone(t5, LS[6] - 0.4)
t6 = [tag(S1, 90, 430, "France · 17th century", AL("France", 6) - 0.2, "", 50), tag(S1, 90, 540, "Ancient Greece", AL("Greece", 6) - 0.2, "", 50),
      tag(S1, 90, 650, "What the Bible says", AL("biblical", 6) - 0.4, "acc", 50)]
gone(t6, LS[7] - 0.4)
teaser(S1, 90, 440, "A French poet", LS[7] + 0.3, hold=3.4)

# =====================================================================  S2 : La Fontaine (lignes 8-13)
t = LS[8] - 0.4
cam(t, S2)
headline(S2, 170, ["[La Fontaine], 1668"], t + 0.1, kicker="Fables · book VI", hl_t=AL("Fontaine", 8) + 0.05, size=96)
liv = S_(S2, "livres", 1350, 420, 230, LS[8] + 0.4, rot=2)
f8 = tag(S2, 90, 430, "A French poet", LS[8] + 0.3, "", 52)
fade(f8, AL("carter", 8) - 0.6)
c8 = card(S2, 90, 420, "The fable", "The carter stuck in the mud", AL("carter", 8) - 0.3, w=900, size=52)
fade(liv, LS[9] - 0.4)
gone([c8], LS[9] - 0.4)
her = S_(S2, "hercule-statuette", 1500, 420, 150, AL("Hercules", 9) - 0.3, rot=2)
t9 = [tag(S2, 90, 430, "The wheel sinks into the mud", AL("wheel", 9) - 0.2, "", 46), tag(S2, 90, 540, "He calls on Hercules", AL("Hercules", 9) - 0.3, "acc", 50)]
gone(t9, LS[10] - 0.4)
t10 = [tag(S2, 90, 430, "A hero of Greek mythology", AL("hero", 10) - 0.3, "", 46), tag(S2, 90, 540, "Worshipped as a demigod", AL("demigod", 10) - 0.6, "acc", 46)]
gone(t10, LS[11] - 0.4)
t11 = [tag(S2, 90, 430, "Shoulder to the wheel", AL("shoulder", 11) - 0.2, "", 50), tag(S2, 90, 540, "Clear the stones", AL("stones", 11) - 0.2, "", 50),
       tag(S2, 90, 650, "Fill the rut", AL("rut", 11) - 0.2, "acc", 50)]
gone(t11, LS[12] - 0.4)
c12 = card(S2, 90, 420, "La Fontaine · The carter stuck in the mud", "“Aide-toi, le Ciel t'aidera.”", AL("Aide-toi", 12) - 0.2, w=1000, size=54, accent=True)
gone([c12], LS[13] - 0.4)
t13 = stamp(S2, 90, 430, "Not the God of Israel", AL("Israel", 13) - 0.3, rot=-3, size=70)
tag(S2, 90, 660, "A Greek god", AL("Hercules", 13) - 0.1, "acc", 54)

# =====================================================================  S3 : Ésope (lignes 14-17)
t = LS[14] - 0.4
cam(t, S3)
headline(S3, 170, ["[Aesop], ancient Greece"], t + 0.1, kicker="The source of the fable", hl_t=AL("Aesop", 14) + 0.05, size=96)
S_(S3, "esope-statuette", 1500, 420, 140, AL("Aesop", 14) - 0.3, rot=-2)
t14 = tag(S3, 90, 430, "La Fontaine borrows it", E("borrows", 14, 0.4, 0.4), "acc", 52)
gone([t14], LS[15] - 0.4)
c15 = card(S3, 90, 420, "In Aesop's version", "Put your hand to the work before praying", AL("Hercules", 15) - 0.4, w=900, size=44)
gone([c15], LS[16] - 0.4)
t16 = [tag(S3, 90, 430, "A very old idea", AL("old", 16) - 0.8, "", 52), tag(S3, 90, 540, "Long before Jesus", AL("Jesus", 16) - 0.3, "acc", 52)]
gone(t16, LS[17] - 0.4)
stamp(S3, 90, 440, "Origin: a Greek fable", AL("fable", 17) - 0.5, rot=-3, size=60)

# =====================================================================  S4 : la version anglaise (lignes 18-23)
t = LS[18] - 0.4
cam(t, S4)
headline(S4, 170, ["The [English] version"], t + 0.1, kicker="A sentence that travels", hl_t=AL("English", 19) + 0.05, size=104)
teaser(S4, 90, 440, "What follows changes the view", LS[18] + 0.3, hold=7.4)
c19 = card(S4, 90, 420, "In English", "God helps those who help themselves", E("God", 19, 0.3, 0.2), w=1000, size=48)
gone([c19], LS[20] - 0.4)
c20 = card(S4, 90, 420, "George Herbert · 1651", "“Help thyself, and God will help thee.”", E("Herbert", 20, 0.3), w=1000, size=44)
gone([c20], LS[21] - 0.4)
c21 = card(S4, 90, 420, "Algernon Sidney", "late 17th century · “a proverb”", E("Sidney", 21, 0.3), w=900, size=44)
gone([c21], LS[22] - 0.4)
fr = S_(S4, "franklin", 1500, 420, 300, AL("Franklin", 22) - 0.3, rot=2)
c22 = card(S4, 90, 420, "Benjamin Franklin", "almanac · 1736", AL("Franklin", 22) - 0.2, w=700, size=52)
gone([c22], LS[23] - 0.4)
t23 = [tag(S4, 90, 430, "A printer, a practical man", AL("printer", 23) - 0.3, "", 50), stamp(S4, 90, 620, "A proverb, not a verse", AL("proverb", 23) - 0.2, rot=-3, size=58)]

# =====================================================================  S5 : du proverbe au « verset » (lignes 24-27)
t = LS[24] - 0.4
cam(t, S5)
headline(S5, 170, ["From proverb to [“verse”]"], t + 0.1, kicker="How it came to seem biblical", hl_t=AL("biblical", 25) + 0.05, size=92)
c24 = card(S5, 90, 420, "France · 1820s", "The society “Aide-toi, le ciel t'aidera”", E("society", 24, 0.3), w=1000, size=44)
gone([c24], LS[25] - 0.4)
t25 = [tag(S5, 90, 430, "Fables", AL("fables", 25) - 0.1, "", 50), tag(S5, 90, 540, "Politics", AL("politics", 25) - 0.1, "", 50),
       tag(S5, 90, 650, "Speeches", AL("speeches", 25) - 0.1, "", 50), tag(S5, 800, 430, "Sermons", AL("sermons", 25) - 0.1, "acc", 50)]
gone(t25, LS[26] - 0.4)
t26 = tag(S5, 90, 430, "US polls: a large share of believers", AL("Polls", 26) - 0.2, "", 40)
gone([t26], LS[27] - 0.4)
s27 = stamp(S5, 90, 440, "Not in the Bible", AL("sum", 27) + 0.5, rot=-4, size=76)
t27 = [tag(S5, 90, 650, "A fable", AL("fable", 27) - 0.1, "", 48), tag(S5, 500, 650, "A proverb", AL("proverb", 27) - 0.1, "", 48),
       tag(S5, 960, 650, "Practical morality", AL("morality", 27) - 0.2, "acc", 48)]

# =====================================================================  S6 : l'aide de Dieu dans les Psaumes (lignes 28-35)
t = LS[28] - 0.4
cam(t, S6)
headline(S6, 170, ["God's [help]"], t + 0.1, kicker="What the Bible really says", hl_t=AL("help", 29) + 0.05, size=104)
t28 = tag(S6, 90, 430, "Is it true?", E("true", 28, 0.4, 0.4), "acc", 54)
gone([t28], LS[29] - 0.4)
t29 = tag(S6, 90, 430, "The text says almost the opposite", E("opposite", 29, 0.9, 0.4), "", 48)
gone([t29], LS[30] - 0.4)
c30 = put(S6, 90, 420, "<small>Hebrew word</small><span class='heb' style='font-size:92px;margin-right:18px'>עזר</span>ezer", "card", "width:800px;font-size:70px")
blur_in(c30, AL("ezer", 30) - 0.3, 14)
t30 = tag(S6, 90, 700, "“help” · “aid”", AL("aid", 30) - 0.4, "acc", 52)
gone([c30, t30], LS[31] - 0.4)
f31 = tag(S6, 90, 430, "Psalm 33, verse 20", LS[31] + 0.3, "", 52)
fade(f31, AL("Our", 31) - 0.3)
kq(S6, 90, 420, "Psalm 33:20" + BIB, "“Our soul has waited for Yahweh. He is our help and our shield.”", 31, "Our", width=900, size=40, fade_at=LS[32] - 0.4)
t32 = tag(S6, 90, 430, "The help of those who cannot manage alone", E("alone", 32, 1.2, 0.4), "acc", 46)
gone([t32], LS[33] - 0.4)
f33 = tag(S6, 90, 430, "Psalm 121", LS[33] + 0.3, "", 52)
fade(f33, AL("I", 33) - 0.3)
kq(S6, 90, 420, "Psalm 121:1-2" + BIB, "“I will lift up my eyes to the hills. Where does my help come from? My help comes from Yahweh, who made heaven and earth.”", 33, "I", width=950, size=36, fade_at=LS[34] - 0.4)
kq(S6, 90, 420, "Psalm 46:1" + BIB, "“God is our refuge and strength, a very present help in trouble.”", 34, "God", width=950, size=38, fade_at=LS[35] - 0.4)
stamp(S6, 90, 440, "No one says: first, help yourself", AL("Notice", 35) + 0.3, rot=-3, size=50)
tag(S6, 90, 700, "The help comes from God", AL("help", 35, 1) - 0.4, "acc", 52)

# =====================================================================  S7 : sans force, par la grâce (lignes 36-39)
t = LS[36] - 0.4
cam(t, S7)
headline(S7, 170, ["[Weak]"], t + 0.1, kicker="Romans 5 · Ephesians 2", hl_t=AL("Weak", 37) + 0.05, size=110)
S_(S7, "paul-pied", 1500, 420, 150, AL("Paul", 36) - 0.3, rot=-2)
kq(S7, 90, 420, "Romans 5:6" + BIB, "“For while we were yet weak, at the right time Christ died for the ungodly.”", 36, "For", width=950, size=40, fade_at=LS[37] - 0.4)
t37 = [tag(S7, 90, 430, "“Weak”", AL("Weak", 37) - 0.3, "", 56), tag(S7, 90, 540, "Far from “help yourself”", AL("far", 37) - 0.2, "acc", 52)]
gone(t37, LS[38] - 0.4)
kq(S7, 90, 420, "Ephesians 2:8-9" + BIB, "“For by grace you have been saved through faith, and that not of yourselves; it is the gift of God, not of works, that no one would boast.”", 38, "For", width=1000, size=34, fade_at=LS[39] - 0.4)
stamp(S7, 90, 440, "Salvation is a gift", AL("gift", 39) - 0.6, rot=-3, size=76)

# =====================================================================  S8 : l'effort n'est pas inutile (lignes 40-45)
t = LS[40] - 0.4
cam(t, S8)
headline(S8, 170, ["And [effort]?"], t + 0.1, kicker="Proverbs 6 · 2 Thessalonians 3", hl_t=AL("effort", 40) + 0.05, size=110)
S_(S8, "paul-portrait", 1500, 420, 230, AL("Paul", 43) - 0.3, rot=2)
t40 = tag(S8, 90, 430, "Effort is not useless", E("useless", 40, 0.6, 0.4), "acc", 52)
gone([t40], LS[41] - 0.4)
kq(S8, 90, 420, "Proverbs 6:6" + BIB, "“Go to the ant, you sluggard. Consider her ways, and be wise.”", 41, "Go", width=900, size=44, fade_at=LS[42] - 0.4)
t42 = [tag(S8, 90, 430, "Work", AL("work", 42) - 0.2, "", 52), tag(S8, 90, 540, "Foresight", AL("foresight", 42) - 0.2, "", 52),
       tag(S8, 90, 650, "Practical wisdom", AL("wisdom", 42) - 0.2, "acc", 52)]
gone(t42, LS[43] - 0.4)
kq(S8, 90, 420, "2 Thessalonians 3:10" + BIB, "“If anyone isn't willing to work, neither let him eat.”", 43, "If", width=900, size=42, fade_at=LS[44] - 0.4)
c44 = card(S8, 90, 420, "Personal effort", "is not forbidden", AL("forbidden", 44) - 0.5, w=800, size=54)
gone([c44], LS[45] - 0.4)
t45 = [tag(S8, 90, 430, "Those who refuse to work", AL("refuse", 45) - 0.2, "", 46), tag(S8, 90, 540, "Not those who cannot", AL("cannot", 45) - 0.3, "acc", 46),
       tag(S8, 90, 650, "Paul: worked with his own hands", AL("hands", 45) - 0.4, "", 44)]

# =====================================================================  S9 : agir ou se confier ? la mer Rouge (lignes 46-49)
t = LS[46] - 0.4
cam(t, S9)
headline(S9, 170, ["Act or [trust]?"], t + 0.1, kicker="Exodus 14", hl_t=AL("trust", 46) + 0.05, size=100)
t46 = [tag(S9, 90, 430, "Act", AL("act", 46) - 0.1, "", 56), tag(S9, 90, 540, "Trust God", AL("trust", 46) - 0.2, "", 56), tag(S9, 90, 650, "Both", AL("Both", 46) - 0.2, "acc", 56)]
gone(t46, LS[47] - 0.4)
f47 = tag(S9, 90, 430, "First example: the Red Sea", LS[47] + 0.3, "", 50)
fade(f47, AL("Yahweh", 47) - 0.3)
mo = S_(S9, "moise", 1500, 420, 190, LS[47] + 0.4, rot=2)
fade(mo, LS[49] - 0.4)
kq(S9, 90, 420, "Exodus 14:14" + BIB, "“Yahweh will fight for you, and you shall be still.”", 47, "Yahweh", width=900, size=42, fade_at=LS[48] - 0.4)
kq(S9, 90, 420, "Exodus 14:15" + BIB, "“Why do you cry to me? Speak to the children of Israel, that they go forward.”", 48, "Why", width=900, size=42, fade_at=LS[49] - 0.4)
stamp(S9, 90, 440, "A help that asks for a response", E("response", 49, 0.8, 0.4), rot=-3, size=50)

# =====================================================================  S10 : Néhémie, Proverbes, Psaume 127 (lignes 50-57)
t = LS[50] - 0.4
cam(t, S10)
headline(S10, 170, ["[Prayer] and vigilance"], t + 0.1, kicker="Nehemiah · Proverbs · Psalm 127", hl_t=AL("Prayer", 51) + 0.05, size=96)
nh = S_(S10, "feuillet-nehemie", 1100, 420, 270, AL("Nehemiah", 50) - 0.2, rot=2)
so = S_(S10, "soldat", 1500, 420, 170, AL("guards", 50) - 0.3, rot=-2)
gone([nh, so], LS[51] - 0.3)
t50 = [tag(S10, 90, 430, "Nehemiah", AL("Nehemiah", 50) - 0.1, "", 54), tag(S10, 90, 540, "They pray", AL("pray", 50) - 0.2, "acc", 54), tag(S10, 90, 650, "Guards, day and night", AL("guards", 50) - 0.2, "", 50)]
gone(t50, LS[51] - 0.3)
t51 = stamp(S10, 90, 440, "Prayer + vigilance", AL("Prayer", 51) - 0.1, rot=-3, size=70)
gone([t51], LS[52] - 0.4)
kq(S10, 90, 420, "Proverbs 21:31" + BIB, "“The horse is prepared for the day of battle, but victory is with Yahweh.”", 52, "The", width=900, size=40, fade_at=LS[53] - 0.4)
t53 = [tag(S10, 90, 430, "The horse", AL("horse", 53) - 0.1, "", 50), tag(S10, 90, 540, "The army", AL("army", 53) - 0.1, "", 50), tag(S10, 90, 650, "The victory", AL("victory", 53) - 0.2, "acc", 50)]
gone(t53, LS[54] - 0.4)
kq(S10, 90, 420, "Proverbs 16:9" + BIB, "“A man's heart plans his course, but Yahweh directs his steps.”", 54, "A", width=900, size=42, fade_at=LS[55] - 0.4)
t55 = [tag(S10, 90, 430, "You plan", AL("plan", 55) - 0.1, "", 50), tag(S10, 90, 540, "You don't control everything", AL("control", 55) - 0.3, "acc", 50)]
gone(t55, LS[56] - 0.4)
f56 = tag(S10, 90, 430, "Psalm 127", LS[56] + 0.3, "", 52)
fade(f56, AL("Unless", 56) - 0.3)
kq(S10, 90, 420, "Psalm 127:1" + BIB, "“Unless Yahweh builds the house, they labor in vain who build it.”", 56, "Unless", width=900, size=42, fade_at=LS[57] - 0.4)
tag(S10, 90, 430, "They really do build", AL("builders", 57) - 0.4, "", 50)
tag(S10, 90, 540, "But effort is not enough", AL("enough", 57) - 0.6, "acc", 50)

# =====================================================================  S11 : le vrai équilibre, les dangers (lignes 58-62)
t = LS[58] - 0.4
cam(t, S11)
headline(S11, 170, ["The true [balance]"], t + 0.1, kicker="Neither “act alone” nor “do nothing”", hl_t=AL("balance", 58) + 0.05, size=104)
c58 = [card(S11, 90, 420, "The text says", "Act", E("act", 58, 0.2, 0.4), w=420, size=56), card(S11, 700, 420, "And", "Don't trust in your own action alone", E("trust", 58, 0.4, 1.0), w=760, size=44, accent=True)]
gone(c58, LS[59] - 0.4)
t59 = [tag(S11, 90, 430, "Not entirely false", AL("false", 59) - 0.4, "", 52), tag(S11, 90, 540, "A measure of practical wisdom", AL("wisdom", 59) - 0.3, "acc", 50)]
gone(t59, LS[60] - 0.4)
s60 = stamp(S11, 90, 440, "Dangerous as a law of God", AL("dangerous", 60) - 0.2, rot=-3, size=56)
gone([s60], LS[61] - 0.4)
S_(S11, "sym-balance", 1500, 420, 190, AL("earned", 61) - 0.3, rot=2)
t61 = [tag(S11, 90, 430, "Must God's help be earned?", AL("earned", 61) - 0.3, "", 50), tag(S11, 90, 540, "The whole Bible speaks of grace", AL("grace", 61) - 0.4, "acc", 50)]
gone(t61, LS[62] - 0.4)
c62 = card(S11, 90, 420, "What the sentence can sound like", "“If God doesn't help you, it's because you aren't helping yourself enough.”", AL("reproach", 62) - 0.3, w=1000, size=40)
t62 = tag(S11, 90, 720, "Sick · in debt · exhausted · out of work", AL("exhausted", 62) - 0.5, "", 40)

# =====================================================================  S12 : Job, les pauvres, les soins (lignes 63-67)
t = LS[63] - 0.4
cam(t, S12)
headline(S12, 170, ["Job and [the poor]"], t + 0.1, kicker="Job 42 · Leviticus 19 · Proverbs 19", hl_t=AL("poor", 64) + 0.05, size=96)
jb = S_(S12, "job-blake", 1150, 420, 600, AL("Job", 63) - 0.2, rot=-2)
fade(jb, LS[64] - 0.4)
kq(S12, 90, 420, "Job 42:7" + BIB, "“You have not spoken of me the thing that is right, as my servant Job has.”", 63, "You", width=900, size=40, fade_at=LS[64] - 0.4)
gl = S_(S12, "glaneuses-millet", 1150, 420, 600, E("gleanings", 64, 0.3, 0.4), rot=2)
fade(gl, LS[65] - 0.4)
t64 = tag(S12, 90, 430, "Leave the gleanings", E("gleanings", 64, 0.3, 0.4), "acc", 52)
gone([t64], LS[65] - 0.4)
kq(S12, 90, 420, "Proverbs 19:17" + BIB, "“He who has pity on the poor lends to Yahweh; he will reward him.”", 65, "He", width=900, size=40, fade_at=LS[66] - 0.4)
s66 = stamp(S12, 90, 440, "To the others: help them", E("others", 66, 0.5, 0.4), rot=-3, size=64)
gone([s66], LS[67] - 0.4)
f67 = tag(S12, 90, 430, "A very heavy time", LS[67] + 0.3, "", 52)
fade(f67, AL("doctor", 67) - 0.4)
t67 = [tag(S12, 90, 430, "A doctor", AL("doctor", 67) - 0.1, "", 52), tag(S12, 90, 540, "A psychologist", AL("psychologist", 67) - 0.1, "", 52), tag(S12, 90, 650, "Someone close", AL("close", 67) - 0.1, "", 52),
       tag(S12, 90, 760, "Faith does not stand against care", AL("care", 67) - 0.6, "acc", 46)]

# =====================================================================  S13 : que faire de cette phrase ? (lignes 68-73)
t = LS[68] - 0.4
cam(t, S13)
headline(S13, 170, ["What to do with [this sentence]?"], t + 0.1, kicker="A proverb, not a promise", hl_t=AL("sentence", 68) + 0.05, size=92)
t68 = [tag(S13, 90, 430, "A proverb of common sense", E("proverb", 68, 0.3, 0.4), "", 52), tag(S13, 90, 540, "Act · get ready", AL("act", 68) - 0.3, "", 52)]
gone(t68, LS[69] - 0.4)
f69 = tag(S13, 90, 430, "God's promise", LS[69] + 0.3, "", 52)
fade(f69, AL("My", 69) - 0.3)
kq(S13, 90, 420, "Psalm 121:2" + BIB, "“My help comes from Yahweh.”", 69, "My", width=800, size=50, fade_at=LS[70] - 0.4)
tq = tag(S13, 90, 430, "When did help come undeserved?", LS[70] + 0.4, "acc", 48)
cta = put(S13, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Tell us in the comments', "cta")
blur_in(cta, AL("comments", 70) - 1.0, 14)
sfx("click", AL("comments", 70) - 1.0, 0.8)
gone([tq, cta], LS[71] - 0.3)
S_(S13, "hercule-statuette", 1500, 420, 150, LS[71] + 0.3, rot=2)
t71 = [tag(S13, 90, 430, "Push the wheel", AL("push", 71) - 0.2, "", 56), tag(S13, 90, 540, "And call out too", AL("call", 71) - 0.2, "acc", 56)]
gone(t71, LS[72] - 0.4)
stamp(S13, 90, 440, "Both are allowed", AL("Both", 72) - 0.3, rot=-3, size=76)

t_end = AL("Every", 73) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(AL("Every", 73) - 0.8, DUR_)]
build(
    chapters=[("01", "The sentence", 0, LS[8]), ("02", "The origin", LS[8], LS[28]), ("03", "What the Bible says", LS[28], LS[58]), ("04", "For you", LS[58], DUR_)],
    suppress=supp,
    endcard={"kicker": "Every week", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("moise-portrait", 150, 560, 300, -6), ("paul-portrait", 1550, 330, 230, 5)]},
    endcard_t=AL("Every", 73) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
