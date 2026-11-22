"""Long video "666: why almost everything you were told is wrong" (Faith Engineering) — style 02, 16:9. English version of montage/video-666/.

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

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - 666 - style 02", "lang": "en",
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
BIB = " · World English Bible"

html.append('<style>'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '@font-face{font-family:"Frank Ruhl Libre";src:url("assets/fonts/FrankRuhlLibre.ttf") format("truetype");font-weight:300 900}'
            '.heb{font-family:"Frank Ruhl Libre",serif;direction:rtl;display:inline-block}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

# =====================================================================  S1
# =====================================================================  S1 : 666 before Revelation (lines 1-8)
cam(0, S1)
headline(S1, 170, ["[666], before Revelation"], 0.0, kicker="A famous number", hl_t=AL("666", 1) + 0.05, size=96)
S_(S1, "livres", 1500, 420, 200, 0.0, rot=2, instant=True)
t1 = tag(S1, 90, 430, "666: long before Revelation", 0.3, "acc", 50)
gone([t1], LS[2] - 0.4)
c2 = card(S1, 90, 420, "1 Kings 10:14 · Solomon", "666 talents of gold a year", AL("Kings", 2) - 0.2, w=900, size=52)
gone([c2], LS[3] - 0.4)
s3 = stamp(S1, 90, 440, "Not the devil?", E("devil", 3, 0.5, 0.6), rot=-3, size=72)
gone([s3], LS[4] - 0.4)
t4 = [tag(S1, 90, 430, "What did this number mean?", LS[4] + 0.2, "", 50), tag(S1, 90, 540, "Everything is wrong?", AL("wrong", 4) - 0.3, "acc", 56)]
gone(t4, LS[5] - 0.4)
t5 = [tag(S1, 90, 430, "Barcodes", E("barcodes", 5, 0.3, 0.4), "", 50), tag(S1, 90, 530, "Microchips", AL("microchips", 5) - 0.2, "", 50),
      tag(S1, 90, 630, "Bank cards", AL("cards", 5) - 0.2, "", 50), tag(S1, 90, 730, "Vaccines", AL("vaccines", 5) - 0.3, "acc", 50)]
gone(t5, LS[6] - 0.4)
t6 = [tag(S1, 90, 430, "Every era, its own 666", LS[6] + 0.3, "", 52), tag(S1, 90, 540, "Objects that did not exist", AL("objects", 6) - 0.4, "acc", 48)]
gone(t6, LS[7] - 0.4)
t7 = [tag(S1, 90, 430, "What the text says", LS[7] + 0.4, "", 52), tag(S1, 90, 540, "What historians think", AL("historians", 7) - 0.3, "", 48), tag(S1, 90, 650, "What is only a rumor", AL("rumor", 7) - 0.4, "acc", 50)]
gone(t7, LS[8] - 0.4)
tag(S1, 90, 430, "Simpler", AL("simpler", 8) - 0.3, "", 56)
tag(S1, 90, 540, "More surprising", AL("surprising", 8) - 0.3, "acc", 56)

# =====================================================================  S2 : one book, one letter (lines 9-14)
t = LS[9] - 0.4
cam(t, S2)
headline(S2, 170, ["One book, one [letter]"], t + 0.1, kicker="Revelation", hl_t=E("letter", 10, 0.2, 2.0), size=104)
S_(S2, "scribe", 1500, 420, 190, LS[10] + 0.2, rot=2)
t9 = tag(S2, 90, 430, "Who wrote it? For whom?", LS[9] + 0.2, "acc", 52)
gone([t9], LS[10] - 0.4)
t10 = [tag(S2, 90, 430, "John, the author", E("John", 10, 0.2, 1.0), "", 52), tag(S2, 90, 540, "From the island of Patmos", AL("Patmos", 10) - 0.3, "acc", 50)]
gone(t10, LS[11] - 0.4)
t11 = [tag(S2, 90, 430, "7 Christian communities", AL("seven", 11) - 0.2, "", 50), tag(S2, 90, 540, "Asia · modern Turkey", AL("Asia", 11) - 0.3, "acc", 50)]
gone(t11, LS[12] - 0.4)
t12 = [tag(S2, 90, 430, "Under the Roman Empire", AL("Roman", 12) - 0.3, "", 52), tag(S2, 90, 540, "A minority, sometimes persecuted", AL("persecuted", 12) - 0.8, "acc", 48)]
gone(t12, LS[13] - 0.4)
c13 = card(S2, 90, 420, "From Greek: “revelation”", "An apocalyptic genre", E("apocalyptic", 13, 0.4, 0.6), w=900, size=50)
gone([c13], LS[14] - 0.4)
tag(S2, 90, 430, "Beasts · stars", AL("stars", 14) - 0.3, "", 48)
tag(S2, 90, 540, "Trumpets · numbers", AL("numbers", 14) - 0.4, "", 48)
tag(S2, 90, 650, "They must be deciphered", AL("deciphered", 14) - 0.6, "acc", 52)

# =====================================================================  S3 : the beast and the mark (lines 15-18)
t = LS[15] - 0.4
cam(t, S3)
headline(S3, 170, ["The beast and the [mark]"], t + 0.1, kicker="Revelation 13", hl_t=AL("beast", 15) + 0.05, size=104)
t15 = [tag(S3, 90, 430, "A beast rises from the sea", AL("beast", 15) - 0.2, "", 52), tag(S3, 90, 540, "“Who is like the beast?”", AL("like", 15) - 0.4, "acc", 46)]
gone(t15, LS[16] - 0.4)
t16 = [tag(S3, 90, 430, "A second beast", AL("second", 16) - 0.2, "", 52), tag(S3, 90, 540, "The “false prophet”", AL("prophet", 16) - 0.6, "acc", 52)]
gone(t16, LS[17] - 0.4)
tp17 = tag(S3, 90, 430, "Revelation 13:16-18", LS[17] + 0.3, "acc", 52)
gone([tp17], AL("causes", 17) - 0.45)
kq(S3, 90, 420, "Revelation 13:16-17" + BIB, "“He causes all, the small and the great, and the rich and the poor, and the free and the slaves, to be given a mark on their right hand, or on their forehead; and that no one would be able to buy or to sell, except one who has the mark, even the name of the beast or the number of his name.”", 17, "causes", width=1000, size=34, fade_at=LS[18] - 0.4)
kq(S3, 90, 420, "Revelation 13:18" + BIB, "“Here is wisdom. He who has understanding, let him calculate the number of the beast, for it is the number of a man. His number is six hundred sixty-six.”", 18, "Here", width=1000, size=38, fade_at=LS[19] - 0.4)

# =====================================================================  S4 : three popular ideas (lines 19-28)
t = LS[19] - 0.4
cam(t, S4)
headline(S4, 170, ["Three popular [ideas]"], t + 0.1, kicker="What the text says", hl_t=AL("popular", 19) + 0.05, size=104)
S_(S4, "ancien", 1500, 420, 190, LS[20] + 0.3, rot=2)
t19 = tag(S4, 90, 430, "Almost every word contradicts a popular idea", LS[19] + 0.3, "acc", 44)
gone([t19], LS[20] - 0.4)
t20 = tag(S4, 90, 430, "Idea #1: the number of the Antichrist", E("First", 20, 0.1, 0.4), "", 48)
gone([t20], LS[21] - 0.4)
t21 = [stamp(S4, 90, 440, "Absent from Revelation", E("never", 21, 0.4, 1.0), rot=-3, size=60), tag(S4, 90, 620, "Only in 1 and 2 John", AL("letters", 21) - 0.5, "acc", 48)]
gone(t21, LS[22] - 0.4)
c22 = card(S4, 90, 420, "1 John 2:18" + BIB, "“even now many antichrists have arisen”", AL("many", 22) - 0.6, w=1000, size=44)
gone([c22], LS[23] - 0.4)
t23 = [tag(S4, 90, 430, "Idea #2: the number of the devil", E("Second", 23, 0.1, 0.4), "", 48), card(S4, 90, 560, "Revelation 13:18", "“the number of a man”", AL("man", 23) - 0.6, w=800, size=44, accent=True)]
gone(t23, LS[24] - 0.4)
t24 = [stamp(S4, 90, 440, "Not “number of Satan”", AL("Satan", 24) - 0.6, rot=-3, size=60), tag(S4, 90, 620, "A human being", AL("human", 24) - 0.4, "acc", 52)]
gone(t24, LS[25] - 0.4)
t25 = tag(S4, 90, 430, "Idea #3: an object, a technology", E("Third", 25, 0.1, 0.4), "", 46)
gone([t25], LS[26] - 0.4)
t26 = [tag(S4, 90, 430, "A name · a mark", LS[26] + 0.3, "", 52), tag(S4, 90, 540, "Buying and selling", AL("buying", 26) - 0.3, "", 52), stamp(S4, 90, 720, "No object", AL("electronic", 26) - 0.5, rot=-3, size=60)]
gone(t26, LS[27] - 0.4)
t27 = [tag(S4, 90, 430, "Popes · Napoleon · dictators", AL("popes", 27) - 0.3, "", 48), tag(S4, 90, 540, "Then computers", AL("computers", 27) - 0.5, "acc", 52)]
gone(t27, LS[28] - 0.4)
stamp(S4, 90, 440, "All failed", E("failed", 28, 0.4, 0.6), rot=-3, size=64)
tag(S4, 90, 620, "A number for everyone points to no one", AL("everyone", 28) - 0.2, "acc", 44)

# =====================================================================  S5 : calculating a name (lines 29-34)
t = LS[29] - 0.4
cam(t, S5)
headline(S5, 170, ["Calculating a [name]"], t + 0.1, kicker="Gematria", hl_t=AL("calculate", 29) + 0.05, size=104)
S_(S5, "rouleau", 1500, 420, 220, LS[30] + 0.3, rot=2)
t29 = tag(S5, 90, 430, "“Calculate”", LS[29] + 0.3, "acc", 60)
gone([t29], LS[30] - 0.4)
t30 = [tag(S5, 90, 430, "Each letter = a number", AL("numerical", 30) - 0.5, "", 52), tag(S5, 90, 540, "Greek · Hebrew", AL("Hebrew", 30) - 0.3, "acc", 52)]
gone(t30, LS[31] - 0.4)
c31 = card(S5, 90, 420, "Gematria", "a name → a number", AL("gematria", 31) - 0.4, w=900, size=52)
gone([c31], LS[32] - 0.4)
t32 = [tag(S5, 90, 430, "Which name gives 666?", LS[32] + 0.2, "", 52), stamp(S5, 90, 570, "Nero Caesar", AL("Caesar", 32) - 0.5, rot=-3, size=72)]
gone(t32, LS[33] - 0.3)
c33 = put(S5, 90, 420, "<small>Nero Caesar, in Hebrew</small><span class='heb' style='font-size:130px'>נרון קסר</span>", "card", "width:1000px;font-size:46px")
blur_in(c33, AL("Hebrew", 33) - 0.3, 14)
v33 = tag(S5, 90, 730, "50 · 200 · 6 · 50 — 100 · 60 · 200", AL("nun", 33) + 0.2, "acc", 50)
gone([c33, v33], LS[34] - 0.4)
counter(S5, 90, 420, 0, 666, AL("Add", 34) + 1.5, 1.2, unit="", size=230)
tag(S5, 90, 700, "50 + 200 + 6 + 50 + 100 + 60 + 200", AL("Add", 34) + 0.2, "", 44)

# =====================================================================  S6 : Nero Caesar (lines 35-43)
t = LS[35] - 0.4
cam(t, S6)
headline(S6, 170, ["The [Nero] hypothesis"], t + 0.1, kicker="A calculation, a name", hl_t=AL("616", 35) + 0.05, size=104)
S_(S6, "soldat", 1500, 420, 150, LS[39] + 0.3, rot=2)
t35 = [stamp(S6, 90, 440, "616!", E("616", 35, 0.2, 0.6), rot=-3, size=90), tag(S6, 90, 620, "Very ancient manuscripts", AL("manuscripts", 35) - 0.4, "acc", 50)]
gone(t35, LS[36] - 0.4)
tf36 = tag(S6, 90, 430, "Same calculation, other spelling", LS[36] + 0.3, "", 50)
gone([tf36], AL("last", 36) - 0.55)
t36 = [tag(S6, 90, 430, "Nero without the last letter", AL("last", 36) - 0.5, "", 50), tag(S6, 90, 540, "= 616", AL("616", 36, 0) - 0.4, "acc", 60)]
gone(t36, LS[37] - 0.4)
tf37 = tag(S6, 90, 430, "A well-attested variant", LS[37] + 0.3, "", 50)
gone([tf37], AL("papyrus", 37) - 0.45)
c37 = card(S6, 90, 420, "Papyrus", "3rd or 4th century", AL("papyrus", 37) - 0.4, w=800, size=52)
gone([c37], LS[38] - 0.4)
tf38 = tag(S6, 90, 430, "A serious argument", LS[38] + 0.3, "", 52)
gone([tf38], AL("hypothesis", 38) - 0.5)
t38 = [stamp(S6, 90, 440, "Hypothesis", AL("hypothesis", 38) - 0.4, rot=-3, size=80), tag(S6, 90, 620, "Not a certainty", AL("certainty", 38) - 0.4, "acc", 52), tag(S6, 90, 730, "Irenaeus already knows 616", AL("Irenaeus", 38) - 0.3, "", 46)]
gone(t38, LS[39] - 0.4)
t39 = [tag(S6, 90, 430, "Why Nero?", LS[39] + 0.2, "", 56), tag(S6, 90, 540, "Already seen as the beast", AL("beast", 39) - 0.5, "acc", 50)]
gone(t39, LS[40] - 0.4)
t40 = [tag(S6, 90, 430, "64: the fire of Rome", AL("64", 40) - 0.2, "", 50), tag(S6, 90, 540, "Tacitus: Christians blamed", AL("Tacitus", 40) - 0.3, "acc", 46)]
gone(t40, LS[41] - 0.4)
t41 = [tag(S6, 90, 430, "68: Nero's death", AL("68", 41) - 0.2, "", 50), tag(S6, 90, 540, "The rumor: he will return", AL("return", 41) - 0.6, "", 50), tag(S6, 90, 650, "Beast wounded, then healed", AL("healed", 41) - 0.6, "acc", 48)]
gone(t41, LS[42] - 0.4)
c42 = card(S6, 90, 420, "First revelation", "A riddle for specific readers", AL("revelation", 42) - 0.4, w=1000, size=48)
gone([c42], LS[43] - 0.4)
tag(S6, 90, 430, "Stay: the mark, then the six", LS[43] + 0.3, "acc", 48)

# =====================================================================  S7 : the date (lines 44-46)
t = LS[44] - 0.4
cam(t, S7)
headline(S7, 170, ["The [date] debated"], t + 0.1, kicker="Revelation", hl_t=AL("date", 44) + 0.05, size=104)
S_(S7, "porte-ville", 1450, 420, 300, LS[44] + 0.5, rot=2)
t44 = tag(S7, 90, 430, "The date is debated", LS[44] + 0.2, "acc", 56)
gone([t44], LS[45] - 0.4)
t45 = [tag(S7, 90, 430, "Tradition: around 95 · Domitian", AL("95", 45) - 0.3, "", 48), tag(S7, 90, 540, "Others: around 68-70", AL("68", 45) - 0.4, "acc", 52)]
gone(t45, LS[46] - 0.4)
tag(S7, 90, 430, "Domitian or the Empire", AL("Domitian", 46) - 0.3, "", 52)
tag(S7, 90, 540, "Nero, a model", AL("model", 46) - 0.4, "", 52)
tag(S7, 90, 650, "Always: Roman imperial power", AL("Roman", 46) - 0.4, "acc", 50)

# =====================================================================  S8 : the mark (lines 47-51)
t = LS[47] - 0.4
cam(t, S8)
headline(S8, 170, ["The [mark]"], t + 0.1, kicker="Revelation 13", hl_t=AL("mark", 47) + 0.05, size=112)
S_(S8, "foule", 1250, 500, 250, LS[48] + 0.3, rot=-2)
t47 = [tag(S8, 90, 430, "The cult of the emperor", E("cult", 47, 0.3, 0.9), "", 52), tag(S8, 90, 540, "Temples · statues · oaths", AL("oaths", 47) - 0.5, "acc", 48)]
gone(t47, LS[48] - 0.4)
t48 = [tag(S8, 90, 430, "Trades in associations", AL("associations", 48) - 0.4, "", 50), tag(S8, 90, 540, "Refuse = lose your job", AL("job", 48) - 0.6, "acc", 48)]
gone(t48, LS[49] - 0.4)
t49 = [stamp(S8, 90, 440, "Neither buy nor sell", AL("buy", 49) - 0.3, rot=-3, size=60), tag(S8, 90, 620, "A sign of allegiance", AL("allegiance", 49) - 0.5, "acc", 52)]
gone(t49, LS[50] - 0.4)
c50 = card(S8, 90, 420, "Deuteronomy 6:8", "“a sign on your hand, between your eyes”", AL("Deuteronomy", 50) - 0.3, w=900, size=44)
gone([c50], LS[51] - 0.4)
t51 = [tag(S8, 90, 430, "The mark of the beast", E("immediately", 51, 0.2, 0.6), "", 52), tag(S8, 90, 540, "The Lamb's name on the forehead", AL("Lamb", 51) - 0.4, "acc", 48), stamp(S8, 90, 680, "Two loyalties", AL("loyalties", 51) - 0.5, rot=-3, size=60)]

# =====================================================================  S9 : why six? (lines 52-55)
t = LS[52] - 0.4
cam(t, S9)
headline(S9, 170, ["Why [six]?"], t + 0.1, kicker="Genesis 1", hl_t=AL("six", 52) + 0.05, size=112)
S_(S9, "livres", 1500, 420, 200, LS[53] + 0.3, rot=2)
t52 = [tag(S9, 90, 430, "Why 6-6-6?", LS[52] + 0.2, "", 56), tag(S9, 90, 540, "And with Solomon?", AL("Solomon", 52) - 0.3, "acc", 52)]
gone(t52, LS[53] - 0.4)
c53 = card(S9, 90, 420, "Genesis 1", "Humankind is created on the sixth day", AL("Genesis", 53) - 0.3, w=1000, size=48)
gone([c53], LS[54] - 0.4)
t54 = [tag(S9, 90, 430, "7 days · 7 churches", AL("Seven", 54) - 0.2, "", 50), tag(S9, 90, 540, "7 seals · 7 trumpets", AL("trumpets", 54) - 0.5, "", 50), stamp(S9, 90, 710, "Seven: fullness", AL("fullness", 54) - 0.4, rot=-3, size=60)]
gone(t54, LS[55] - 0.4)
t55 = [tag(S9, 90, 430, "6: the human, limited?", AL("human", 55) - 0.5, "", 52), stamp(S9, 90, 560, "A common reading", AL("common", 55) - 0.4, rot=-3, size=60), tag(S9, 90, 720, "No verse states it", AL("verse", 55) - 0.5, "acc", 50)]

# =====================================================================  S10 : Solomon and Nebuchadnezzar (lines 56-61)
t = LS[56] - 0.4
cam(t, S10)
headline(S10, 170, ["Two scenes, the [six]"], t + 0.1, kicker="1 Kings 10 · Daniel 3", hl_t=AL("scenes", 56) + 0.05, size=104)
S_(S10, "sym-balance", 1450, 420, 260, LS[57] + 0.5, rot=2)
t56 = tag(S10, 90, 430, "Two scenes where six returns", LS[56] + 0.2, "acc", 52)
gone([t56], LS[57] - 0.4)
c57 = card(S10, 90, 420, "1 Kings 10:14 · Solomon", "666 talents of gold a year", AL("talents", 57) - 0.5, w=900, size=50)
t57 = [tag(S10, 90, 640, "≈ 20 tons of gold", AL("tons", 57) - 0.4, "acc", 52), tag(S10, 90, 750, "Deuteronomy 17: no hoarded gold", AL("Deuteronomy", 57) - 0.3, "", 40)]
gone([c57] + t57, LS[58] - 0.4)
t58 = [tag(S10, 90, 430, "Horses from Egypt", AL("Egypt", 58) - 0.3, "", 52), tag(S10, 90, 540, "Hundreds of wives", AL("women", 58) - 0.4, "", 52), tag(S10, 90, 650, "Gold accumulated", AL("accumulates", 58) - 0.5, "acc", 52)]
gone(t58, LS[59] - 0.4)
c59 = card(S10, 90, 420, "Daniel 3:1 · Nebuchadnezzar", "A gold statue: 60 cubits × 6", AL("Daniel", 59) - 0.3, w=1000, size=46)
s59 = stamp(S10, 90, 660, "Bow down or die", AL("bow", 59) - 0.5, rot=-3, size=60)
gone([c59, s59], LS[60] - 0.4)
t60 = [tag(S10, 90, 430, "A power demands worship", AL("worship", 60) - 0.5, "", 50), tag(S10, 90, 540, "The faithful refuse", AL("faithful", 60) - 0.4, "acc", 52)]
gone(t60, LS[61] - 0.4)
stamp(S10, 90, 440, "A lead, not a proof", AL("proof", 61) - 0.8, rot=-3, size=56)
tag(S10, 90, 620, "Was John thinking of it? No one can claim it", AL("thinking", 61) - 0.3, "", 42)

# =====================================================================  S11 : the meaning of numbers (lines 62-66)
t = LS[62] - 0.4
cam(t, S11)
headline(S11, 170, ["Numbers have [meaning]"], t + 0.1, kicker="Listening to the echoes", hl_t=AL("solid", 62) + 0.05, size=96)
S_(S11, "veilleur", 1500, 420, 200, LS[63] + 0.3, rot=2)
tf62 = tag(S11, 90, 430, "What is solid", LS[62] + 0.3, "acc", 56)
gone([tf62], AL("code", 62) - 0.55)
t62 = [tag(S11, 90, 430, "No hidden code", AL("code", 62) - 0.5, "", 52), tag(S11, 90, 540, "Echoes of the text", AL("echoes", 62, 0) - 0.4, "acc", 52)]
gone(t62, LS[63] - 0.4)
t63 = [tag(S11, 90, 430, "Readings toward the future: false?", LS[63] + 0.2, "", 46), stamp(S11, 90, 570, "No", E("No", 63, 0.2, 0.9), rot=-3, size=90)]
gone(t63, LS[64] - 0.4)
t64 = [tag(S11, 90, 430, "The first century", AL("century", 64) - 0.5, "", 50), tag(S11, 90, 540, "The history of the Church", AL("Church", 64) - 0.3, "", 50), tag(S11, 90, 650, "A final period", AL("final", 64) - 0.4, "acc", 50)]
gone(t64, LS[65] - 0.4)
t65 = [tag(S11, 90, 430, "No side to choose", AL("side", 65) - 0.4, "", 52), tag(S11, 90, 540, "The text ≠ what we project", AL("projected", 65) - 0.7, "acc", 46)]
gone(t65, LS[66] - 0.4)
c66 = card(S11, 90, 420, "Matthew 24:4" + BIB, "“Be careful that no one leads you astray”", AL("Matthew", 66) - 0.3, w=1000, size=42)
tag(S11, 90, 650, "Vigilance, not panic", AL("vigilance", 66) - 0.4, "acc", 52)

# =====================================================================  S12 : when the number brings fear (lines 67-71)
t = LS[67] - 0.4
cam(t, S12)
headline(S12, 170, ["When the number brings [fear]"], t + 0.1, kicker="Application", hl_t=AL("anxious", 67) + 0.05, size=100)
S_(S12, "pere", 1500, 420, 190, LS[68] + 0.3, rot=2)
t67 = [tag(S12, 90, 430, "Fear of the end of time", LS[67] + 0.4, "", 52), tag(S12, 90, 540, "Fear of “receiving the mark”", AL("mark", 67) - 0.5, "acc", 48)]
gone(t67, LS[68] - 0.4)
t68 = [stamp(S12, 90, 440, "Written to comfort", AL("comfort", 68) - 0.4, rot=-3, size=64), tag(S12, 90, 620, "Not to terrorize", AL("terrorize", 68) - 0.5, "acc", 52)]
gone(t68, LS[69] - 0.4)
t69a = tag(S12, 90, 430, "A blessing for the one who reads", AL("blessing", 69) - 0.3, "", 48)
gone([t69a], AL("wipe", 69) - 0.5)
c69 = card(S12, 90, 420, "Revelation 21:4" + BIB, "“God will wipe away every tear from their eyes”", AL("wipe", 69) - 0.3, w=1000, size=42)
gone([c69], LS[70] - 0.4)
t70 = [tag(S12, 90, 430, "A loved one", AL("loved", 70) - 0.3, "", 52), tag(S12, 90, 540, "A pastor", AL("pastor", 70) - 0.3, "", 52), tag(S12, 90, 650, "A health professional", AL("professional", 70) - 0.4, "acc", 52),
       stamp(S12, 90, 770, "Not a lack of faith", AL("faith", 70) - 0.5, rot=-3, size=52)]
gone(t70, LS[71] - 0.4)
tq = tag(S12, 90, 430, "Which fear marked you most?", LS[71] + 0.4, "acc", 50)
cta = put(S12, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Tell me in the comments', "cta")
blur_in(cta, AL("comments", 71) - 1.0, 14)
sfx("click", AL("comments", 71) - 1.0, 0.8)
gone([tq, cta], LS[72] - 0.3)

# =====================================================================  S13 : conclusion (lines 72-77)
t = LS[72] - 0.4
cam(t, S13)
headline(S13, 170, ["So much [false] about 666"], t + 0.1, kicker="The answer", hl_t=AL("false", 72) + 0.05, size=100)
S_(S13, "scribe", 1500, 420, 190, LS[75] + 0.3, rot=2)
t72 = tag(S13, 90, 430, "Why so many false things?", LS[72] + 0.3, "acc", 56)
gone([t72], LS[73] - 0.4)
t73 = [tag(S13, 90, 430, "A mysterious number", AL("mysterious", 73) - 0.4, "", 52), tag(S13, 90, 540, "The fears of every era", AL("fears", 73) - 0.4, "acc", 50)]
gone(t73, LS[74] - 0.4)
tf74 = tag(S13, 90, 430, "The text is more sober", LS[74] + 0.3, "", 52)
gone([tf74], AL("man", 74) - 0.45)
t74 = [tag(S13, 90, 430, "A number of a man", AL("man", 74) - 0.3, "", 52), tag(S13, 90, 540, "A name to calculate", AL("calculate", 74) - 0.3, "", 52), tag(S13, 90, 650, "A mark: who you belong to", AL("mark", 74) - 0.3, "acc", 48)]
gone(t74, LS[75] - 0.4)
t75 = [stamp(S13, 90, 440, "Not a code to fear", AL("code", 75) - 0.4, rot=-3, size=60), tag(S13, 90, 620, "A loyalty owed only to God", AL("loyalty", 75) - 0.6, "acc", 46)]
gone(t75, LS[76] - 0.4)
t76 = [tag(S13, 90, 430, "Who is the audience?", AL("audience", 76) - 0.3, "", 52), tag(S13, 90, 540, "What context?", AL("context", 76) - 0.3, "", 52), tag(S13, 90, 650, "What does the verse say?", AL("verse", 76) - 0.3, "acc", 52)]
gone(t76, LS[77] - 0.3)

t_end = AL("Every", 77) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(AL("Every", 77) - 0.8, DUR_)]
build(
    chapters=[("01", "The myth", 0, LS[9]), ("02", "The text", LS[9], LS[29]), ("03", "Nero", LS[29], LS[52]), ("04", "The six", LS[52], LS[67]), ("05", "For you", LS[67], DUR_)],
    suppress=supp,
    endcard={"kicker": "Every week", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("scribe", 150, 560, 280, -6), ("jesus-portrait", 1550, 330, 230, 5)]},
    endcard_t=AL("Every", 77) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
