"""Long video "End-of-the-world prophecies (2027, Nostradamus): what does the Bible say?" (Faith Engineering) — style 02, 16:9, 565.4 s.
English version of montage/video-fin-du-monde/ : same layout and the same audit (kit-style-02/outils/audit_chevauchements.js).

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

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - End-of-the-world prophecies - style 02", "lang": "en",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
DUR_ = 563.9
s.setup(here=HERE, duration=DUR_, cols=5, rows=4, fmt="16:9", theme=THEME, bpm=96, zoom=1.15, xmap=(190, 0.8539), ymap=(208, 0.85))
from style02 import *  # noqa: E402,F401,F403
import style02  # noqa: E402

MANQUES = []
SUPP = []


def _norm(t):
    return re.sub(r"[^\w]", "", t.lower().replace("’", "").replace("'", ""))


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
S11, S12, S13 = (0, 2), (1, 2), (2, 2)
WEB = "World English Bible"

html.append('<style>'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

# =====================================================================  S1: announced dates (lines 1-7)
cam(0, S1)
headline(S1, 170, ["The end of the world, [postponed]"], 0.0, kicker="Announcements", hl_t=AL("postponed", 1) + 0.05, size=88)
v0 = S_(S1, "villageois", 1100, 420, 300, 0.0, rot=-3, instant=True)
fade(v0, LS[2] - 0.2)
tg1 = [tag(S1, 90, 430, "Announced", AL("announced", 1) - 0.1, "", 56), tag(S1, 90, 540, "Postponed", AL("postponed", 1) - 0.1, "acc", 56)]
gone(tg1, LS[2] - 0.2)
an = S_(S1, "animateur", 1500, 420, 190, LS[2] - 0.1, rot=2)
c1 = card(S1, 90, 420, "Harold Camping's announcement", "May 21, 2011", AL("Camping", 2) - 0.2, w=700, size=56)
st1 = stamp(S1, 90, 660, "Nothing", AL("nothing", 3) + 0.1, rot=-4, size=72)
gone([c1, st1], AL("corrects", 3) - 0.2)
c2 = card(S1, 90, 420, "Corrected announcement", "October 21, 2011", AL("corrects", 3) + 0.2, w=760, size=56, accent=True)
st2 = stamp(S1, 90, 660, "Still nothing", AL("nothing", 4) + 0.1, rot=-3, size=64)
gone([c2, st2, an], LS[5] - 0.15)
cn = counter(S1, 90, 420, 2011, 2027, AL("twenty-seven", 5) - 0.8, 2.2, size=170)
tn = [tag(S1, 800, 440, "Nostradamus", AL("Nostradamus", 5) - 0.1, "", 52), tag(S1, 800, 550, "Quatrains", AL("quatrains", 5) - 0.1, "acc", 52)]
gone([cn] + tn, LS[6] - 0.5)
tq = tag(S1, 90, 440, "Does the Bible say when?", AL("Bible", 6) - 0.4, "acc", 56)
v6 = S_(S1, "villageois", 1100, 420, 300, AL("believers", 6) - 0.3, rot=2)
ring(S1, 1260, 600, AL("anxiety", 6), size=260)
gone([tq], LS[7] - 0.5)
tx = [tag(S1, 90, 430, "The text", AL("text", 7) - 0.1, "", 54), tag(S1, 90, 540, "History", AL("history", 7) - 0.1, "", 54),
      tag(S1, 90, 650, "What Jesus answered", AL("Jesus", 7) - 0.1, "acc", 54)]

# =====================================================================  S2: Nostradamus (lines 8-14)
t = LS[8] - 0.4
cam(t, S2)
headline(S2, 170, ["[Nostradamus]"], t + 0.1, kicker="The Prophecies, 1555", hl_t=AL("Nostradamus", 8) + 0.05, size=104)
S_(S2, "nostradamus-pied", 1500, 420, 160, AL("Nostradamus", 8) - 0.2, rot=-2)
t8 = tag(S2, 90, 430, "A name that always comes back", AL("back", 8) - 0.5, "", 50)
fade(t8, LS[9] - 0.5)
c9 = card(S2, 90, 420, "Michel de Nostredame", "physician and astrologer · 1503-1566", AL("Michel", 9) - 0.1, w=900, size=38)
fade(c9, LS[10] - 0.5)
n10 = counter(S2, 90, 420, 1500, 1555, AL("fifteen", 10) - 0.2, 2.0, size=150)
t10 = [tag(S2, 90, 620, "Lyon · The Prophecies", AL("Lyon", 10) - 0.2, "acc", 46), tag(S2, 90, 740, "Deliberately obscure quatrains", AL("obscure", 10) - 1.0, "", 40)]
ast = S_(S2, "astrolabe", 1050, 420, 260, AL("Prophecies", 10) - 0.2, rot=3)
fade(ast, LS[12] - 0.5)
gone([n10] + t10, LS[11] - 0.5)
t11 = [tag(S2, 90, 430, "Very vague verses", AL("vague", 11) - 0.3, "acc", 56), tag(S2, 90, 560, "Meaning found after the fact", AL("fact", 11) - 1.0, "", 50)]
gone(t11, LS[12] - 0.5)
c12 = card(S2, 90, 420, "Famous quatrain", "“the year nineteen ninety-nine, seven months”", AL("quatrain", 12) - 0.1, w=900, size=36)
t12 = [tag(S2, 90, 640, "A great king of terror", AL("king", 12) - 0.3, "", 46), stamp(S2, 900, 640, "Nothing", AL("Nothing", 12), rot=-4, size=64),
       tag(S2, 90, 760, "Then, a new reading", AL("reinterpreted", 12) - 1.0, "acc", 40)]
gone([c12] + t12, LS[13] - 0.5)
s13 = stamp(S2, 90, 430, "Fake", AL("fake", 13) - 0.2, rot=-4, size=84)
t13 = [tag(S2, 90, 600, "Written in the 1990s by a student", AL("student", 13) - 0.6, "", 40),
       tag(S2, 90, 720, "Wrongly attributed to Nostradamus", AL("anything", 13) - 1.4, "acc", 40)]
gone([s13] + t13, LS[14] - 0.5)
teaser(S2, 90, 440, "What follows sheds light", AL("patiently", 14) - 0.5, hold=4.6)

# =====================================================================  S3: the biblical test (lines 15-19)
t = LS[15] - 0.4
cam(t, S3)
headline(S3, 170, ["A prophet's [test]"], t + 0.1, kicker="Deuteronomy 18", hl_t=AL("test", 16) + 0.05, size=96)
t15 = tag(S3, 90, 430, "The Bible judges differently", AL("judges", 15) - 0.3, "acc", 52)
fade(t15, LS[16] - 0.5)
S_(S3, "rouleau", 1500, 420, 230, AL("Deuteronomy", 16) - 0.2, rot=3)
f16 = tag(S3, 90, 430, "God gives a test", LS[16] + 0.5, "acc", 52)
fade(f16, AL("if", 16) - 0.6)
kq(S3, 90, 420, "Deuteronomy 18.22 · " + WEB,
   "“If the thing doesn't follow, nor come to pass, that is the thing which Yahweh has not spoken.”",
   16, "if", width=900, size=38, fade_at=LS[17] - 0.4)
t17 = [tag(S3, 90, 430, "A precise prediction", AL("precise", 17) - 0.6, "", 52), tag(S3, 90, 540, "Not fulfilled: not from Yahweh", AL("come", 17) - 0.3, "acc", 46)]
gone(t17, LS[18] - 0.5)
t18 = tag(S3, 90, 430, "A prophet calls us back", AL("return", 18) - 0.8, "acc", 52)
gone([t18], LS[19] - 0.5)
S_(S3, "jonas", 1100, 420, 220, AL("Jonah", 19) - 0.3, rot=-3)
card(S3, 90, 420, "Jonah 3.4", "“Yet forty days, and Nineveh will be overthrown”", AL("Yet", 19) - 0.2, w=760, size=36)
tag(S3, 90, 640, "The city repents", AL("repents", 19) - 0.3, "", 46)
tag(S3, 90, 750, "The goal: conversion", AL("conversion", 19) - 0.4, "acc", 46)

# =====================================================================  S4: the question to Jesus (lines 20-24)
t = LS[20] - 0.4
cam(t, S4)
headline(S4, 170, ["What does [Jesus] say?"], t + 0.1, kicker="Matthew 24", hl_t=AL("Jesus", 20) + 0.05, size=96)
S_(S4, "jesus-pied", 1500, 420, 210, AL("Jesus", 20) - 0.3, rot=2)
t20 = tag(S4, 90, 430, "The date of the end?", AL("date", 20) - 0.2, "acc", 56)
fade(t20, LS[21] - 0.5)
kq(S4, 90, 420, "Matthew 24.3 · " + WEB,
   "“Tell us, when will these things be? What is the sign of your coming, and of the end of the age?”", 21, "tell", width=900, size=40,
   fade_at=LS[22] - 0.4)
c22 = card(S4, 90, 420, "In Greek", "<b>synteleia tou aionos</b>", AL("synteleia", 22) - 0.2, w=760, size=40)
t22 = tag(S4, 90, 600, "The completion of an age", AL("completion", 22) - 0.4, "acc", 50)
gone([c22, t22], LS[23] - 0.5)
a23 = S_(S4, "arc-titus", 90, 420, 430, AL("temple", 23) - 0.3, rot=-2)
s23 = stamp(S4, 640, 450, "Year 70", AL("seventy", 23) - 0.2, rot=-4, size=72)
t23 = tag(S4, 640, 610, "The temple destroyed", AL("temple", 23), "", 48)
gone([a23, s23, t23], LS[24] - 0.5)
tag(S4, 90, 430, "Reading 1: the year 70", AL("event", 24) - 0.4, "", 52)
tag(S4, 90, 560, "Reading 2: the end of time", AL("time", 24) - 0.2, "acc", 52)

# =====================================================================  S5: the day and the hour (lines 25-28)
t = LS[25] - 0.4
cam(t, S5)
headline(S5, 170, ["The day and [the hour]"], t + 0.1, kicker="Matthew 24.36", hl_t=AL("hour", 25) + 0.05, size=96)
S_(S5, "jesus-portrait", 1500, 420, 250, AL("Jesus", 25) - 0.3, rot=3)
kq(S5, 90, 420, "Matthew 24.36 · " + WEB,
   "“But no one knows of that day and hour, not even the angels of heaven, nor the Son, but the Father alone.”", 25, "but", n=1,
   width=950, size=40, fade_at=LS[26] - 0.4)
t26 = [tag(S5, 90, 430, "Mark: the same saying", AL("Mark", 26) - 0.2, "", 52), tag(S5, 90, 540, "The day remains the Father's secret", AL("secret", 26) - 0.8, "acc", 46)]
gone(t26, LS[27] - 0.5)
kq(S5, 90, 420, "Acts 1.7 · " + WEB,
   "“It isn't for you to know times or seasons which the Father has set within his own authority.”", 27, "it", n=1, width=950, size=38,
   fade_at=LS[28] - 0.4)
stamp(S5, 90, 440, "Contradicts", AL("contradict", 28) - 0.2, rot=-4, size=84)
tag(S5, 90, 670, "Just reread Matthew", AL("reread", 28) - 0.6, "acc", 50)

# =====================================================================  S6: the signs (lines 29-32)
t = LS[29] - 0.4
cam(t, S6)
headline(S6, 170, ["What about the [signs]?"], t + 0.1, kicker="Matthew 24.4-6", hl_t=AL("signs", 29) + 0.05, size=96)
t29 = tag(S6, 90, 430, "Look at how he begins", AL("look", 29) - 0.3, "", 52)
fade(t29, LS[30] - 0.5)
S_(S6, "cavaliers", 1500, 420, 290, AL("wars", 30) - 0.3, rot=2)
kq(S6, 90, 420, "Matthew 24.4-6 · " + WEB,
   "“Be careful that no one leads you astray. For many will come in my name, saying, ‘I am the Christ,’ and will lead many astray. "
   "You will hear of wars and rumors of wars. See that you aren't troubled, for all this must happen, but the end is not yet.”",
   30, "be", width=1050, size=32, fade_at=LS[31] - 0.4)
t31 = [tag(S6, 90, 430, "No calendar", AL("calendar", 31) - 0.6, "", 52), tag(S6, 90, 540, "A warning", AL("warning", 31) - 0.3, "acc", 52),
       tag(S6, 90, 650, "Against deception and panic", AL("panic", 31) - 1.2, "", 44)]
gone(t31, LS[32] - 0.5)
card(S6, 90, 420, "Jesus says", "“the end is not yet”", AL("end", 32) - 0.2, w=780, size=48)
stamp(S6, 90, 680, "Not a countdown", AL("countdown", 32) - 0.2, rot=-3, size=52)

# =====================================================================  S7: Paul and Peter (lines 33-36)
t = LS[33] - 0.4
cam(t, S7)
headline(S7, 170, ["Paul and [Peter]"], t + 0.1, kicker="1 Thessalonians · 2 Peter", hl_t=AL("Peter", 35) + 0.05, size=96)
S_(S7, "paul", 1500, 420, 170, AL("Pauls", 33) - 0.3, rot=-2)
t33 = [tag(S7, 90, 430, "Thessalonica", AL("Thessalonica", 33) - 0.3, "", 52), tag(S7, 90, 540, "Not to be shaken", AL("shaken", 33) - 0.6, "acc", 46)]
gone(t33, LS[34] - 0.5)
kq(S7, 90, 420, "1 Thessalonians 5.2 · " + WEB, "“the day of the Lord comes like a thief in the night”", 34, "the", width=900, size=42,
   last=AL("night", 34) + 0.5, fade_at=LS[35] - 0.4)
t34 = tag(S7, 90, 700, "A thief gives no warning", AL("warning", 34) - 0.6, "acc", 50)
gone([t34], LS[35] - 0.5)
S_(S7, "sablier", 1250, 420, 110, AL("Peter", 35) - 0.2, rot=2)
kq(S7, 90, 420, "2 Peter 3.8-9 · " + WEB,
   "“one day is with the Lord as a thousand years, and a thousand years as one day. The Lord is not slow concerning his promise, as some count slowness; "
   "but is patient with us, not wishing that any should perish, but that all should come to repentance.”",
   35, "one", width=900, size=32, fade_at=LS[36] - 0.4)
tag(S7, 90, 430, "Not for calculating", AL("calculating", 36) - 0.2, "", 52)
tag(S7, 90, 540, "Patience, not slowness", AL("patience", 36) - 0.4, "acc", 50)

# =====================================================================  S8: William Miller (lines 37-40)
t = LS[37] - 0.4
cam(t, S8)
headline(S8, 170, ["William [Miller], 1844"], t + 0.1, kicker="Nineteenth century", hl_t=AL("Miller", 37) + 0.05, size=96)
f37 = tag(S8, 90, 430, "A long history of dates", LS[37] + 0.3, "", 52)
fade(f37, AL("Daniel", 37) - 0.6)
S_(S8, "miller", 1500, 420, 190, AL("Miller", 37) - 0.3, rot=-2)
t37 = [tag(S8, 90, 430, "The prophecies of Daniel", AL("Daniel", 37) - 0.3, "", 48), tag(S8, 90, 560, "Return expected around 1843", AL("forty-three", 37) - 1.0, "acc", 52)]
gone(t37, LS[38] - 0.5)
c38 = card(S8, 90, 420, "Date set", "October 22, 1844", AL("twenty-second", 38) - 0.4, w=720, size=52)
t38 = [tag(S8, 90, 640, "Tens of thousands of people", AL("Tens", 38) - 0.2, "", 42), tag(S8, 90, 750, "Fields left, possessions sold", AL("fields", 38) - 0.3, "", 40)]
gone([c38] + t38, LS[39] - 0.5)
s39 = [stamp(S8, 90, 430, "Nothing", AL("Nothing", 39) - 0.1, rot=-4, size=84),
       tag(S8, 90, 650, "The Great Disappointment", AL("Disappointment", 39) - 0.6, "acc", 52)]
gone(s39, LS[40] - 0.5)
t40 = [tag(S8, 90, 430, "Adventist churches", AL("Adventist", 40) - 0.5, "", 48), tag(S8, 90, 540, "No more dates set", AL("gave", 40) - 0.5, "acc", 48)]

# =====================================================================  S9: the same pattern (lines 41-45)
t = LS[41] - 0.4
cam(t, S9)
headline(S9, 170, ["The same [pattern]"], t + 0.1, kicker="The history of dates", hl_t=AL("pattern", 43) + 0.05, size=104)
S_(S9, "sablier", 1500, 420, 110, AL("Europe", 41) - 0.2, rot=-2)
c41 = card(S9, 90, 420, "The year one thousand", "A general panic? Mostly a legend", AL("Europe", 41) - 0.2, w=900, size=40)
t41 = tag(S9, 90, 620, "Built later", AL("legend", 41) - 0.8, "acc", 50)
gone([c41, t41], LS[42] - 0.5)
c42 = card(S9, 90, 420, "Maya calendar · 2012", "The end of a counting cycle, not a prediction of the end of the world", AL("Maya", 42) - 0.5, w=900, size=38)
gone([c42], LS[43] - 0.5)
bx = [card(S9, 90, 420, "Step 1", "A date", AL("date", 43) - 0.3, w=400, size=34),
      card(S9, 580, 420, "Step 2", "A fear", AL("fear", 43) - 0.3, w=400, size=34),
      card(S9, 90, 600, "Step 3", "A silence", AL("silence", 43) - 0.3, w=400, size=34),
      card(S9, 580, 600, "Step 4", "A new date", AL("new", 43) - 0.3, w=400, size=34, accent=True)]
gone(bx, LS[44] - 0.5)
c44 = card(S9, 90, 420, "Why?", "Uncertainty is frightening: a date gives the feeling of taking back control", AL("Why", 44) - 0.1, w=900, size=38)
gone([c44], LS[45] - 0.5)
stamp(S9, 90, 440, "Not a date", AL("date", 45) - 0.3, rot=-4, size=76)
tag(S9, 90, 620, "A way of living", AL("living", 45) - 0.8, "acc", 56)

# =====================================================================  S10: the Apocalypse (lines 46-52)
t = LS[46] - 0.4
cam(t, S10)
headline(S10, 170, ["The [Apocalypse]"], t + 0.1, kicker="The most quoted book", hl_t=AL("Apocalypse", 46) + 0.05, size=110)
f46 = tag(S10, 90, 430, "The book everyone quotes", LS[46] + 0.3, "acc", 52)
fade(f46, AL("apokalypsis", 47) - 0.7)
S_(S10, "cavaliers", 1500, 420, 255, AL("Apocalypse", 46) - 0.2, rot=2)
c47 = card(S10, 90, 420, "From the Greek apokalypsis", "unveiling, revelation", AL("apokalypsis", 47) - 0.3, w=780, size=44)
s47 = stamp(S10, 90, 620, "≠ catastrophe", AL("catastrophe", 47) - 0.3, rot=-3, size=64)
gone([c47, s47], LS[48] - 0.5)
S_(S10, "jean-pied", 1200, 420, 185, AL("Blessed", 48) - 0.2, rot=-2)
kq(S10, 90, 420, "Revelation 1.3 · " + WEB,
   "“Blessed is he who reads and those who hear the words of the prophecy, and keep the things that are written in it, for the time is at hand.”",
   48, "blessed", width=900, size=36, fade_at=LS[49] - 0.4)
t49 = [tag(S10, 90, 430, "Seven very real churches", AL("seven", 49) - 0.2, "", 52), tag(S10, 90, 540, "Asia Minor · present-day Turkey", AL("Turkey", 49) - 0.7, "", 44),
       tag(S10, 90, 650, "Under the Roman Empire", AL("Roman", 49) - 0.3, "acc", 48)]
gone(t49, LS[50] - 0.5)
cc = [card(S10, 90, 420, "Reading 1", "The world of the first readers", AL("world", 50) - 0.3, w=400, size=30),
      card(S10, 580, 420, "Reading 2", "The history of the Church", AL("history", 50) - 0.3, w=400, size=30),
      card(S10, 90, 640, "Reading 3", "Events still to come", AL("come", 50) - 0.3, w=400, size=30),
      card(S10, 580, 640, "Reading 4", "A symbolic picture", AL("symbolic", 50) - 0.3, w=400, size=30, accent=True)]
gone(cc, LS[51] - 0.5)
c51 = card(S10, 90, 420, "Numbers", "a thousand years, a hundred and forty-four thousand: first of all symbols", AL("Numbers", 51) - 0.2, w=900, size=38)
s51 = stamp(S10, 90, 690, "Not a code", AL("code", 51) - 0.3, rot=-4, size=64)
gone([c51, s51], LS[52] - 0.5)
kq(S10, 90, 420, "Revelation 22.20 · " + WEB, "“Yes, I come quickly.”", 52, "yes", width=700, size=48, last=AL("quickly", 52) + 0.5,
   fade_at=LS[53] - 0.45)
tag(S10, 90, 660, "“Come, Lord Jesus.”", AL("Come", 52) - 0.3, "acc", 56)

# =====================================================================  S11: parousia and watching (lines 53-56)
t = LS[53] - 0.4
cam(t, S11)
headline(S11, 170, ["The [parousia]"], t + 0.1, kicker="Presence, arrival", hl_t=AL("parousia", 53) + 0.05, size=104)
c53 = card(S11, 90, 420, "In Greek", "<b>parousia</b>: presence, arrival", AL("parousia", 53) - 0.3, w=800, size=44)
t53 = tag(S11, 90, 600, "The official visit of a king", AL("king", 53) - 0.4, "", 46)
gone([c53, t53], LS[54] - 0.5)
s54 = stamp(S11, 90, 440, "Not a countdown", AL("countdown", 54) - 0.3, rot=-3, size=56)
t54 = tag(S11, 90, 600, "An expected arrival", AL("arrival", 54) - 0.4, "acc", 54)
gone([s54, t54], LS[55] - 0.5)
kq(S11, 90, 420, "Matthew 24.42 · " + WEB, "“Watch therefore, for you don't know in what hour your Lord comes.”", 55, "watch",
   width=900, size=42, fade_at=LS[56] - 0.4)
tw55 = tag(S11, 90, 740, "To watch = to stay awake", AL("awake", 55) - 0.5, "acc", 46)
fade(tw55, LS[56] - 0.5)
S_(S11, "veilleur", 1500, 420, 290, AL("sky", 56) - 0.3, rot=2)
S_(S11, "vierge-lampe", 1160, 420, 190, AL("oil", 56) - 0.3, rot=-2)
S_(S11, "pain", 740, 420, 320, AL("hungry", 56) - 0.3, rot=2)

# =====================================================================  S12: three questions (lines 57-60)
t = LS[57] - 0.4
cam(t, S12)
headline(S12, 170, ["Three [questions]"], t + 0.1, kicker="Facing a prophecy", hl_t=AL("free", 57) + 0.05, size=104)
f57 = tag(S12, 90, 430, "Three simple questions", LS[57] + 0.3, "acc", 56)
fade(f57, AL("date", 58) - 0.8)
card(S12, 90, 420, "Question 1", "Does it give a date?", AL("date", 58) - 0.3, w=500, size=34)
tag(S12, 90, 650, "Contradicts Matthew 24.36", AL("contradicts", 58) - 0.2, "acc", 34)
card(S12, 690, 420, "Question 2", "Does it push you toward fear?", AL("fear", 59) - 0.3, w=500, size=34)
tag(S12, 690, 650, "“See that you aren't troubled”", AL("troubled", 59) - 0.5, "acc", 32)
card(S12, 1300, 420, "Question 3", "Does it ask you for money?", AL("leave", 60) - 0.3, w=500, size=34)
tag(S12, 1300, 650, "Be careful: don't be led astray", AL("astray", 60) - 0.8, "acc", 32)

# =====================================================================  S13: support and a question (lines 61-62)
t = LS[61] - 0.4
cam(t, S13)
headline(S13, 170, ["You are not [alone]"], t + 0.1, kicker="When anxiety takes up too much room", hl_t=AL("alone", 61) + 0.05, size=104)
glow(S13, 1560, 540, AL("anxiety", 61), size=360, dur=8.0)
S_(S13, "mains-lampe", 1420, 420, 300, AL("anxiety", 61) - 0.2, rot=2)
t61 = [tag(S13, 90, 430, "A doctor", AL("doctor", 61) - 0.1, "", 52), tag(S13, 90, 540, "A therapist", AL("therapist", 61) - 0.1, "", 52),
       tag(S13, 90, 650, "A trusted friend", AL("friend", 61) - 0.1, "", 52), tag(S13, 90, 760, "It takes nothing away from faith", AL("faith", 61) - 0.9, "acc", 46)]
gone(t61, LS[62] - 0.5)
tq2 = tag(S13, 90, 430, "A promise that helped you?", LS[62] + 0.4, "acc", 54)
cta = put(S13, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Share it in the comments', "cta")
blur_in(cta, AL("comments", 62) - 1.0, 14)
sfx("click", AL("comments", 62) - 1.0, 0.8)

# =====================================================================  S1 (revisited): conclusion (lines 63-66)
cam(LS[63] - 2.0, "all")
wipe(S1, LS[63] - 2.1)
t = LS[63] - 0.4
cam(t, S1)
headline(S1, 170, ["The world was [still there]"], t + 0.1, kicker="October 21, 2011", hl_t=AL("still", 63) + 0.05, size=96)
an2 = S_(S1, "animateur", 1500, 420, 190, AL("morning", 63) - 0.3, rot=2)
fade(an2, LS[65] - 0.5)
t63 = tag(S1, 90, 430, "The day and the hour remain the Father's secret", AL("secret", 63) - 1.4, "acc", 46)
gone([t63], LS[64] - 0.5)
t64 = [tag(S1, 90, 430, "It belongs to God", AL("God", 64) - 0.2, "", 52), tag(S1, 90, 540, "It cannot be calculated", AL("calculated", 64) - 0.3, "", 52),
       tag(S1, 90, 650, "Hope depends on no date", AL("hope", 64) - 0.5, "acc", 46)]
gone(t64, LS[65] - 0.5)
gH = glow(S1, 900, 600, LS[65], size=520, dur=9.0)
f65 = tag(S1, 90, 430, "What the text leaves us", LS[65] + 0.2, "", 54)
fade(f65, AL("watch", 65) - 0.6)
w65 = []
for _x, _w, _k in ((90, "to watch", "watch"), (700, "to love", "love"), (1180, "to hope", "hope")):
    wid = put(S1, _x, 500, _w, "word", "font-size:100px")
    blur_in(wid, AL(_k, 65) - 0.1, 20)
    w65.append(wid)
gone(w65, LS[66] - 0.2)

t_end = AL("Every", 66) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(LS[63] - 2.8, LS[63] - 0.5), (AL("Every", 66) - 0.8, DUR_)]
build(
    chapters=[("01", "Announced dates", 0, LS[8]), ("02", "Nostradamus", LS[8], LS[15]), ("03", "What Jesus says", LS[15], LS[37]),
              ("04", "History of dates", LS[37], LS[46]), ("05", "The Apocalypse", LS[46], LS[53]), ("06", "Watching", LS[53], DUR_)],
    suppress=supp,
    endcard={"kicker": "Every week", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("jean-portrait", 150, 560, 300, -6), ("vierge-lampe", 1550, 330, 180, 5)]},
    endcard_t=AL("Every", 66) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
