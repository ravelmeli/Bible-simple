"""Long video « Ruach: the Hebrew word for "spirit" that also means "wind" and "breath" » (Faith Engineering) — style 02, 16:9, 378.7 s.

English version of montage/video-ruach/, rebuilt with a stricter layout: no element may hide another one.
Rules used here (checked by kit-style-02/outils/audit_chevauchements.js after the build):
  - content starts at design y = 400 (below the headline text), column L = x 90 to ~1100, column R = x 1100 to 1850;
  - a quote (kinetic_quote) owns its zone: everything else in that zone is faded out before it appears and it is faded out when read;
  - captions sit at the bottom: content never goes below screen y 830.
Hebrew and Greek words are transliterated in Latin letters, written in HTML: have them proofread before publishing.
Run: python3 build.py   (then node ../../kit-style-02/outils/audit_chevauchements.js ., npx hyperframes check, render)
"""
import difflib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - Ruach, wind, breath and spirit - style 02", "lang": "en",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
DUR_ = 378.7
s.setup(here=HERE, duration=DUR_, cols=5, rows=4, fmt="16:9", theme=THEME, bpm=96, zoom=1.15, xmap=(190, 0.8539), ymap=(208, 0.85))
from style02 import *  # noqa: E402,F401,F403
import style02  # noqa: E402

MANQUES = []
SUPP = []


def _norm(t):
    return re.sub(r"[^\w]", "", t.lower())


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


def S_(station, name, x, y, w, t, **kw):
    i, h = sticker(station, name, x, y, w, t, **kw)
    bas = 208 + 0.85 * (y - 170) + h
    if bas > 830:
        print(f"ATTENTION {name} y={y} w={w} : bas à {bas:.0f}")
    return i


def kq(station, x, y, ref_txt, text, line, first, width=1000, size=34, last=None, fade_at=None):
    """Word-by-word quote; fades out at `fade_at` (default: end of the line) so that it never hides what comes next."""
    t0 = AL(first, line) - 0.05
    t1 = (LS[line + 1] - 0.25) if last is None else last
    SUPP.append((t0 - 0.1, t1 + 0.2))
    i = kinetic_quote(station, x, y, ref_txt, text, t0, t1, width=width, size=size)
    fade(i, (LS[line + 1] - 0.05) if fade_at is None else fade_at)
    return i


def gone(ids, t):
    for _i in ids:
        fade(_i, t)


HOREB, TROIS, HOREB2, EXODE, SOUFFLE = (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)
NESHAMAH, ESPRIT, EZECHIEL, NT, ATTENTION = (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)
APPLI = (0, 2)
WEB = "World English Bible"

html.append('<style>'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

# =====================================================================  HOREB (lines 1-5): wind, earthquake, fire
cam(0, HOREB)
S_(HOREB, "elie", 1500, 400, 230, 0.0, rot=-3, instant=True)
S_(HOREB, "montagne", 1030, 420, 360, AL("Mount", 1) - 0.2, rot=2)
headline(HOREB, 170, ["On Mount [Horeb]"], 0.0, kicker="1 Kings 19", hl_t=AL("Horeb", 1) + 0.05, size=92)
hb = [tag(HOREB, 90, 420, "A wind", AL("wind", 2) - 0.1, "", 50),
      tag(HOREB, 90, 525, "An earthquake", AL("earthquake", 2) - 0.1, "", 50),
      tag(HOREB, 90, 630, "A fire", AL("fire", 2) - 0.1, "", 50)]
wind(HOREB, 600, 410, AL("wind", 2) - 0.2, size=380, dur=4.0)
hb.append(S_(HOREB, "rocher", 600, 670, 190, AL("earthquake", 2) - 0.2, rot=-3))
hb.append(S_(HOREB, "flamme", 845, 640, 170, AL("fire", 2) - 0.2, rot=3))
burst(HOREB, 1100, 600, AL("wind", 2) + 0.1)
gone(hb, AL("three", 3) - 0.15)
stm = stamp(HOREB, 90, 480, "Not in it", AL("three", 3) + 0.2, rot=-4, size=72)
fade(stm, AL("Yet", 4) - 0.3)
th = teaser(HOREB, 90, 780, "One word hides three meanings", AL("Yet", 4) - 0.2, hold=3.2)
tw_ = tag(HOREB, 90, 420, "wind = spirit", AL("spirit", 4) - 0.2, "acc", 50)
fade(tw_, AL("ruach", 5) - 0.15)
fade(th, AL("ruach", 5) - 0.15)
r0 = put(HOREB, 90, 540, "ruach", "word", "font-size:190px")
blur_in(r0, AL("ruach", 5) - 0.1, 20)
hit(AL("ruach", 5), 1.0)

# =====================================================================  THREE WORDS (lines 6-9)
t = LS[6] - 0.4
cam(t, TROIS)
headline(TROIS, 170, ["Three words for [one]"], t + 0.1, kicker="Ruach", hl_t=AL("single", 6) + 0.05, size=96)
S_(TROIS, "bible-hebraique", 1100, 420, 480, AL("Hebrew", 6) - 0.3, rot=-2)
t3 = [tag(TROIS, 90, 420, "The wind", AL("wind", 6) - 0.1, "", 52),
      tag(TROIS, 90, 525, "The breath", AL("breath", 6) - 0.1, "", 52),
      tag(TROIS, 90, 630, "The spirit", AL("spirit", 6) - 0.1, "acc", 52)]
t3.append(S_(TROIS, "souffle", 760, 420, 165, AL("breath", 6) - 0.1, rot=2))
lat = [tag(TROIS, 90, 765, "Latin: spiritus = breath", AL("Latin", 7) - 0.2, "", 38),
       tag(TROIS, 820, 765, "Greek: pneuma", AL("pneuma", 7) - 0.3, "acc", 38)]
gone(t3 + lat, AL("So", 8) - 0.2)
stamp(TROIS, 90, 450, "Confusion?", AL("confusion", 8) - 0.2, rot=-4, size=64)
arrow(TROIS, (700, 520), (1030, 560), AL("message", 8))
burst(TROIS, 1350, 600, AL("message", 8) + 0.1)

# =====================================================================  HOREB, reading (lines 10-13)
t = LS[10] - 0.4
cam(t, HOREB2)
headline(HOREB2, 170, ["The scene at [Horeb]"], t + 0.1, kicker="1 Kings 19.11", hl_t=AL("scene", 10) + 0.05, size=96)
h10 = [tag(HOREB2, 90, 430, "1 Kings, chapter 19", LS[10] + 0.4, "acc", 56),
       S_(HOREB2, "montagne", 1100, 420, 360, AL("Horeb", 10) + 0.2, rot=2)]
gone(h10, AL("Behold", 11) - 0.35)
kq(HOREB2, 90, 420, "1 Kings 19.11 · " + WEB,
   "“Behold, Yahweh passed by, and a great and strong wind tore the mountains, and broke in pieces the rocks before Yahweh; "
   "but Yahweh was not in the wind. After the wind, an earthquake; but Yahweh was not in the earthquake.”",
   11, "behold", width=900, size=34)
S_(HOREB2, "elie-portrait", 1500, 410, 250, AL("Behold", 11) + 0.2, rot=3)
wind(HOREB2, 1150, 440, AL("wind", 11) - 0.2, size=300, dur=5.0)
S_(HOREB2, "rocher", 1180, 660, 170, AL("rocks", 11), rot=3)
stamp(HOREB2, 90, 450, "1 · The wind", AL("first", 12) + 0.2, rot=-4, size=56)
tag(HOREB2, 90, 590, "First meaning: the wind", AL("first", 12) - 0.2, "acc", 56)
tag(HOREB2, 90, 710, "A real wind, a force of nature", AL("real", 12) - 0.1, "", 44)
burst(HOREB2, 1550, 600, AL("God", 13) + 0.1)

# =====================================================================  EXODUS (lines 14-16)
t = LS[14] - 0.4
cam(t, EXODE)
headline(EXODE, 170, ["The [east] wind"], t + 0.1, kicker="Exodus 14.21", hl_t=AL("east", 14) + 0.05, size=104)
S_(EXODE, "moise", 110, 410, 270, AL("sea", 14) - 0.3, rot=-2)
wind(EXODE, 1560, 420, AL("wind", 14) - 0.3, size=300, dur=7.0)
kq(EXODE, 560, 420, "Exodus 14.21 · " + WEB, "“Yahweh caused the sea to go back by a strong east wind all night.”",
   14, "Yahweh", width=800, size=36, last=AL("night", 14) + 0.5, fade_at=LS[15] - 0.1)
fw = tag(EXODE, 560, 440, "The four winds", AL("four", 15) - 0.3, "acc", 56)
ring(EXODE, 1000, 540, AL("four", 15), size=240)
fade(fw, AL("First", 16) - 0.2)
stamp(EXODE, 560, 440, "1 · The wind", AL("First", 16) + 0.1, rot=-4, size=52)
tag(EXODE, 560, 590, "A force you cannot see, with visible effects", AL("effects", 16) - 0.9, "", 40)

# =====================================================================  BREATH (lines 17-20)
t = LS[17] - 0.4
cam(t, SOUFFLE)
headline(SOUFFLE, 170, ["The [breath]"], t + 0.1, kicker="2 · Second meaning", hl_t=AL("breath", 18) + 0.05, size=110)
glow(SOUFFLE, 1620, 600, t + 0.5, size=320, dur=6.0)
S_(SOUFFLE, "lampe", 1500, 480, 220, t + 0.5, rot=-3)
ts_ = tag(SOUFFLE, 90, 430, "Stay a little longer", AL("stay", 17) - 0.3, "", 44)
fade(ts_, AL("Second", 18) - 0.2)
sb = [S_(SOUFFLE, "souffle", 90, 420, 230, AL("Second", 18) - 0.1, rot=2)]
breath(SOUFFLE, 340, 480, AL("Second", 18), size=420, dur=5.0)
ring(SOUFFLE, 215, 540, AL("Second", 18), size=260)
sb.append(S_(SOUFFLE, "shofar-grave", 800, 420, 520, AL("breath", 18) + 0.4, rot=-3))
sb.append(label_box(SOUFFLE, 800, 690, "A shofar", "ram's horn, 18th c. · The Met", AL("Psalm", 19) - 1.6))
gone(sb, AL("Psalm", 19) - 0.3)
kq(SOUFFLE, 90, 420, "Psalm 104.29-30 · " + WEB,
   "“You take away their breath, they die, and return to their dust. You send out your Spirit, they are created. You renew the surface of the ground.”",
   19, "You", width=1000, size=34)
tag(SOUFFLE, 90, 430, "The breath of life", AL("ruach", 20) - 0.3, "acc", 56)
tag(SOUFFLE, 90, 550, "It leaves: life stops", AL("leaves", 20) - 0.2, "", 44)
tag(SOUFFLE, 90, 660, "It is sent: life begins again", AL("sent", 20) - 0.2, "", 44)

# =====================================================================  NESHAMAH (lines 21-24)
t = LS[21] - 0.4
cam(t, NESHAMAH)
headline(NESHAMAH, 170, ["Another word: [neshamah]"], t + 0.1, kicker="Genesis 2.7", hl_t=AL("neshamah", 21) + 0.05, size=92)
nz = []
d21 = tag(NESHAMAH, 90, 420, "A detail worth knowing", LS[21] + 0.4, "acc", 52)
fade(d21, AL("breath", 21) - 0.6)
c1 = put(NESHAMAH, 90, 420, "<small>Genesis 2.7</small>a “breath of life”: <b>neshamah</b>", "card", "width:700px;font-size:36px")
blur_in(c1, AL("breath", 21) - 0.3, 14)
c2 = put(NESHAMAH, 1000, 420, "<small>Most often</small><b>ruach</b>: movement and force", "card", "width:700px;font-size:36px;border-color:" + ACC)
blur_in(c2, AL("ruach", 22) - 0.4, 14)
nz += [c1, c2]
nz.append(S_(NESHAMAH, "bible-hebraique", 90, 620, 380, AL("Genesis", 21) - 0.2, rot=-2))
sbn = S_(NESHAMAH, "sym-balance", 610, 620, 190, AL("close", 22) - 0.2, rot=0)
animate(sbn, "rock", AL("close", 22) - 0.2, dur=6.0)
nz.append(sbn)
nz.append(tag(NESHAMAH, 1000, 640, "Close, not interchangeable", AL("interchangeable", 22) - 0.6, "acc", 40))
gone(nz, AL("Ecclesiastes", 23) - 0.3)
kq(NESHAMAH, 90, 420, "Ecclesiastes 12.7 · " + WEB,
   "“the dust returns to the earth as it was, and the spirit returns to God who gave it.”", 23, "the", width=1000, size=40,
   last=AL("gave", 23) + 0.6, fade_at=LS[24] - 0.05)
stamp(NESHAMAH, 90, 470, "3 · The spirit", AL("third", 24) + 0.1, rot=-4, size=64)

# =====================================================================  SPIRIT (lines 25-29)
t = LS[25] - 0.4
cam(t, ESPRIT)
headline(ESPRIT, 170, ["The [spirit]"], t + 0.1, kicker="3 · Third meaning", hl_t=AL("spirit", 25) + 0.05, size=110)
S_(ESPRIT, "rouleau", 1500, 420, 260, t + 0.5, rot=3)
kq(ESPRIT, 90, 420, "Genesis 1.2 · " + WEB, "“the Spirit of God was hovering over the surface of the waters.”", 26, "Spirit", width=900, size=44,
   last=AL("waters", 26) + 0.6, fade_at=LS[27] - 0.05)
wind(ESPRIT, 1180, 440, AL("second", 26) - 0.2, size=300, dur=5.0)
ta_ = tag(ESPRIT, 90, 580, "Translators do not agree", AL("honest", 27) - 0.2, "acc", 42)
cA = put(ESPRIT, 90, 420, "“the Spirit of God”", "card", "width:520px;font-size:34px")
cB = put(ESPRIT, 700, 420, "“a wind from God”", "card", "width:520px;font-size:34px")
blur_in(cA, AL("some", 27) - 0.2, 14)
blur_in(cB, AL("others", 27) - 0.2, 14)
gone([cA, cB, ta_], LS[28] - 0.1)
jc = S_(ESPRIT, "jacob", 860, 400, 230, AL("Jacob", 28) - 0.3, rot=-3)
tj = tag(ESPRIT, 90, 440, "The spirit of Jacob revived", AL("revived", 28) - 0.8, "", 38)
ring(ESPRIT, 975, 560, AL("Jacob", 28), size=260)
gone([jc, tj], AL("Psalm", 29) - 0.3)
kq(ESPRIT, 90, 420, "Psalm 34.18 · " + WEB,
   "“Yahweh is near to those who have a broken heart, and saves those who have a crushed spirit.”", 29, "Yahweh", width=1000, size=40,
   fade_at=LS[30] - 0.05)

# =====================================================================  EZEKIEL (lines 30-35)
t = LS[30] - 0.5
cam(t, EZECHIEL)
headline(EZECHIEL, 170, ["The valley of [Ezekiel]"], t + 0.1, kicker="Ezekiel 37", hl_t=AL("valley", 31) + 0.05, size=96)
t30 = tag(EZECHIEL, 920, 420, "wind · breath · spirit", LS[30] + 0.3, "acc", 56)
fade(t30, AL("prophet", 31) - 0.2)
S_(EZECHIEL, "ossements", 90, 420, 430, AL("valley", 30) - 0.2, rot=-2)
S_(EZECHIEL, "ezechiel", 640, 410, 200, AL("prophet", 31) - 0.2, rot=3)
kq(EZECHIEL, 920, 420, "Ezekiel 37.9 · " + WEB,
   "“Prophesy to the wind, prophesy, son of man, and say to the wind, Thus says the Lord Yahweh: Come from the four winds, breath, "
   "and breathe on these slain, that they may live.”", 32, "prophesy", width=800, size=32, fade_at=LS[33] - 0.2)
ezw = []
for k_, lab in enumerate(["wind", "breath", "spirit"]):
    rid = put(EZECHIEL, 920 + k_ * 270, 420, "ruach", "word", "font-size:80px")
    blur_in(rid, AL("ruach", 33) + k_ * 0.9, 14)
    ezw.append(rid)
    ezw.append(tag(EZECHIEL, 920 + k_ * 270, 560, lab, AL("ruach", 33) + 0.5 + k_ * 0.9, "acc" if k_ == 2 else "", 40))
gone(ezw, AL("house", 34) - 0.4)
tm = [tag(EZECHIEL, 920, 440, "the whole house of Israel", AL("house", 34) - 0.3, "acc", 46),
      tag(EZECHIEL, 920, 560, "discouraged, in exile", AL("exile", 34) - 0.4, "", 44)]
gone(tm, LS[35] - 0.1)
S_(EZECHIEL, "foule", 920, 670, 170, AL("promise", 35) - 0.2, rot=2)
kq(EZECHIEL, 920, 420, "Ezekiel 37.14 · " + WEB, "“I will put my Spirit in you, and you will live.”", 35, "I", width=800, size=44,
   last=AL("live", 35) + 0.6, fade_at=LS[36] - 0.05)

# =====================================================================  NEW TESTAMENT (lines 36-41)
t = LS[36] - 0.4
cam(t, NT)
headline(NT, 170, ["The Greek: [pneuma]"], t + 0.1, kicker="The New Testament", hl_t=AL("pneuma", 36) + 0.05, size=104)
g36 = [tag(NT, 100, 430, "Written in Greek", LS[36] + 0.3, "", 56),
       tag(NT, 100, 550, "pneuma", AL("pneuma", 36) - 0.1, "acc", 64)]
gone(g36, AL("Nicodemus", 37) - 0.75)
S_(NT, "nicodeme", 100, 410, 210, AL("Nicodemus", 37) - 0.3, rot=-3)
S_(NT, "jesus-pied", 380, 410, 190, AL("Jesus", 37) - 0.3, rot=3)
kq(NT, 640, 420, "John 3.8 · " + WEB,
   "“The wind blows where it wants to, and you hear its sound, but don't know where it comes from and where it is going. "
   "So is everyone who is born of the Spirit.”", 37, "the", width=850, size=32, fade_at=LS[38] - 0.2)
wind(NT, 1650, 440, AL("wind", 37) - 0.2, size=230, dur=6.0)
nt_tags = [tag(NT, 640, 430, "pneuma = wind = Spirit", AL("Greek", 38) - 0.2, "", 46),
           stamp(NT, 640, 550, "Hypothesis", AL("hypothesis", 38) - 0.2, rot=-4, size=60),
           tag(NT, 640, 720, "Jesus spoke Aramaic", AL("Aramaic", 38) - 0.2, "", 40)]
gone(nt_tags, LS[39] - 0.1)
breath(NT, 1300, 470, AL("breathed", 39) - 0.2, size=260, dur=3.5)
jp = S_(NT, "jesus-portrait", 1600, 410, 190, AL("breathed", 39) - 0.2, rot=3)
tg1 = tag(NT, 640, 450, "Jesus breathed: a breath", AL("breathed", 39) + 0.6, "", 38)
gone([jp, tg1], LS[40] - 0.1)
S_(NT, "pentecote", 1200, 410, 260, AL("Pentecost", 40) - 0.6, rot=-2)
tag(NT, 640, 450, "“a mighty wind”", AL("mighty", 40) - 0.4, "acc", 38)
tag(NT, 640, 720, "One word, one story", AL("Pentecost", 41) - 0.8, "acc", 40)

# =====================================================================  CAREFUL (lines 42-43)
t = LS[42] - 0.4
cam(t, ATTENTION)
headline(ATTENTION, 170, ["[Context] decides"], t + 0.1, kicker="But careful", hl_t=AL("context", 42) + 0.05, size=100)
sbA = S_(ATTENTION, "sym-balance", 1300, 400, 330, t + 0.4, rot=0)
animate(sbA, "rock", t + 0.4, dur=14.0)
tf = tag(ATTENTION, 90, 430, "Three meanings don't fit everywhere", AL("fit", 42) - 0.4, "", 46)
fade(tf, LS[43] - 0.1)
S_(ATTENTION, "elie-portrait", 90, 420, 260, AL("Elijah", 43) - 0.3, rot=2)
stamp(ATTENTION, 560, 460, "Not the wind", AL("wind", 43) - 0.2, rot=-3, size=52)
tag(ATTENTION, 560, 640, "The wind is a sign", AL("sign", 43) - 0.3, "acc", 50)

# =====================================================================  APPLICATION (lines 44-46)
t = LS[44] - 0.4
cam(t, APPLI)
headline(APPLI, 170, ["This week, [one minute]"], t + 0.1, kicker="For you", hl_t=AL("minute", 44) + 0.05, size=100)
ap = [S_(APPLI, "souffle", 90, 430, 190, AL("breathing", 44) - 0.5, rot=2)]
breath(APPLI, 300, 470, AL("breathing", 44) - 0.5, size=400, dur=8.0, pulses=4)
ap.append(counter(APPLI, 830, 420, 0, 60, AL("minute", 44), 6.0, unit=" s", size=170))
qa = kq(APPLI, 830, 640, "Psalm 34.18 · " + WEB, "“Yahweh is near to those who have a broken heart”", 44, "Psalm", width=700, size=34,
        last=AL("eighteen", 44) + 0.8, fade_at=LS[45] - 0.3)
gone(ap, AL("support", 45) - 0.35)
glow(APPLI, 1560, 520, AL("support", 45) - 0.4, size=360, dur=8.0)
mlp = S_(APPLI, "mains-lampe", 1400, 420, 280, AL("support", 45) - 0.4, rot=2)
tp = [tag(APPLI, 90, 430, "Support can help", AL("support", 45) - 0.3, "acc", 50),
      tag(APPLI, 90, 560, "Faith and medical care don't oppose each other", AL("medical", 45) - 0.4, "", 38)]
gone(tp + [mlp], LS[46] - 0.1)
S_(APPLI, "foule", 1150, 420, 300, LS[46] + 0.2, rot=-2)
tag(APPLI, 90, 430, "A breath that set you back on your feet", AL("breath", 46) - 0.2, "acc", 44)
cta = put(APPLI, 90, 600, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Tell us in the comments', "cta")
blur_in(cta, AL("comments", 46) - 0.6, 14)
sfx("click", AL("comments", 46) - 0.6, 0.8)

# =====================================================================  HOREB (revisited): the whisper (lines 47-49)
cam(LS[47] - 2.0, "all")
wipe(HOREB, LS[47] - 2.1)
t = LS[47] - 0.4
cam(t, HOREB)
headline(HOREB, 170, ["A still small [voice]"], t + 0.1, kicker="1 Kings 19.12", hl_t=AL("voice", 47) + 0.05, size=96)
glow(HOREB, 1000, 520, AL("Horeb", 47), size=480, dur=9.0)
S_(HOREB, "grotte", 700, 410, 360, AL("Horeb", 47), rot=2)
S_(HOREB, "elie-portrait", 130, 400, 300, AL("Elijah", 47) - 0.3, rot=-3)
breath(HOREB, 480, 560, AL("voice", 47) - 0.3, size=380, dur=4.5)
hv = [tag(HOREB, 1250, 430, "Wind. Earthquake. Fire.", AL("earthquake", 47) - 0.5, "", 40),
      tag(HOREB, 1250, 560, "“a still small voice”", AL("voice", 47) - 0.1, "acc", 48)]
gone(hv, LS[48] - 0.1)
S_(HOREB, "ossements", 1250, 420, 300, AL("bones", 48) - 0.5, rot=-2)
S_(HOREB, "souffle", 1650, 430, 160, AL("breath", 48) - 0.2, rot=3)
tag(HOREB, 1250, 720, "The same story", AL("story", 48) - 0.3, "acc", 44)
hit(AL("story", 48), 0.8)

t_end = AL("One", 49) - 0.2
cam(t_end, "all")

# automatic retirements computed by the overlap audit (see kit-style-02/outils/audit_chevauchements.js --auto)
_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(LS[47] - 2.8, LS[47] - 0.5), (AL("One", 49) - 0.8, DUR_)]
build(
    chapters=[("01", "The wind", 0, LS[18]), ("02", "The breath", LS[18], LS[25]), ("03", "The spirit", LS[25], LS[36]),
              ("04", "The New Testament", LS[36], LS[44]), ("05", "For you", LS[44], DUR_)],
    suppress=supp,
    endcard={"kicker": "Every week", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("elie-portrait", 150, 560, 300, -6), ("ezechiel", 1550, 330, 200, 5)]},
    endcard_t=AL("One", 49) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
