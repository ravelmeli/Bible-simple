"""Long video "Advent: where does this feast come from? What the Bible really says" (Faith Engineering) — style 02, 16:9. English version of montage/video-avent/.
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

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - Advent - style 02", "lang": "en",
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
# =====================================================================  S1 : hook (lines 1-6)
cam(0, S1)
headline(S1, 170, ["“[Advent]” is not in the Bible"], 0.0, kicker="Not a biblical word", hl_t=AL("Advent", 1) + 0.05, size=96)
S_(S1, "livres", 1500, 420, 200, 0.0, rot=2, instant=True)
t1 = tag(S1, 90, 430, "Nowhere in the Bible", 0.3, "acc", 52)
gone([t1], LS[2] - 0.4)
t2 = [tag(S1, 90, 430, "A first candle", AL("candle", 2) - 0.3, "", 52), tag(S1, 90, 540, "An Advent calendar", AL("calendar", 2) - 0.3, "", 52), tag(S1, 90, 650, "Waiting for Christmas", AL("Christmas", 2) - 0.5, "acc", 52)]
gone(t2, LS[3] - 0.4)
t3 = [tag(S1, 90, 430, "Where does this habit come from?", LS[3] + 0.2, "", 48), tag(S1, 90, 540, "What does the Bible say about waiting?", AL("waiting", 3) - 0.5, "", 46), tag(S1, 90, 650, "What have the centuries added?", AL("centuries", 3) - 0.5, "acc", 48)]
gone(t3, LS[4] - 0.4)
t4 = [tag(S1, 90, 430, "What the text says", E("text", 4, 0.4, 0.6), "", 52), tag(S1, 90, 540, "What tradition says", AL("tradition", 4) - 0.3, "", 52), tag(S1, 90, 650, "A modern habit", AL("modern", 4) - 0.4, "acc", 52)]
gone(t4, LS[5] - 0.4)
tag(S1, 90, 430, "The future as much as the past", E("future", 5, 0.3, 0.6), "acc", 48)

# =====================================================================  S2 : adventus, parousia (lines 7-13)
t = LS[7] - 0.4
cam(t, S2)
headline(S2, 170, ["An [emperor]'s word"], t + 0.1, kicker="Adventus · parousia", hl_t=AL("emperor", 8) + 0.05, size=104)
S_(S2, "soldat", 1500, 420, 150, LS[8] + 0.3, rot=2)
c7 = card(S2, 90, 420, "Latin: adventus", "“arrival,” “coming”", E("arrival", 7, 0.3, 0.6), w=900, size=52)
gone([c7], LS[8] - 0.4)
t8 = [tag(S2, 90, 430, "The solemn entry of an emperor", AL("emperor", 8) - 0.4, "", 48), tag(S2, 90, 540, "The city is decorated", AL("festivities", 8) - 1.4, "acc", 52)]
gone(t8, LS[9] - 0.4)
c9 = card(S2, 90, 420, "Greek: parousia", "“presence,” “coming”", AL("parousia", 9) - 0.3, w=900, size=52)
t9 = tag(S2, 90, 640, "Also the visit of a king", AL("visit", 9) - 0.4, "acc", 52)
gone([c9, t9], LS[10] - 0.4)
t10 = tag(S2, 90, 430, "A sovereign's vocabulary", AL("vocabulary", 10) - 0.5, "", 52)
gone([t10], LS[11] - 0.4)
t11 = [stamp(S2, 90, 440, "Another king comes", E("king", 11, 0.4, 0.8), rot=-3, size=70)]
gone(t11, LS[12] - 0.4)
c12 = card(S2, 90, 420, "Greek: epiphaneia", "“appearing”", AL("epiphaneia", 12) - 0.3, w=800, size=52)
gone([c12], LS[13] - 0.4)
tag(S2, 90, 430, "Not a countdown to presents", AL("countdown", 13) - 0.4, "", 48)
tag(S2, 90, 540, "The arrival of a king", AL("king", 13) - 0.5, "acc", 56)

# =====================================================================  S3 : four weeks, a tradition (lines 14-18)
t = LS[14] - 0.4
cam(t, S3)
headline(S3, 170, ["Four weeks: a [tradition]"], t + 0.1, kicker="Not in the Bible", hl_t=AL("tradition", 15) + 0.05, size=96)
S_(S3, "rouleau", 1500, 420, 220, LS[16] + 0.3, rot=2)
t14 = tag(S3, 90, 430, "No four-week period", E("surprise", 14, 0.3, 0.6), "acc", 50)
gone([t14], LS[15] - 0.4)
t15 = tag(S3, 90, 430, "Built little by little by the Church", E("little", 15, 0.6, 0.8), "", 46)
gone([t15], LS[16] - 0.4)
t16 = [tag(S3, 90, 430, "4th century · Spain", AL("Spain", 16) - 0.3, "", 50), tag(S3, 90, 540, "5th century · Gaul: 40 days", AL("Gaul", 16) - 0.3, "", 50)]
gone(t16, LS[17] - 0.4)
t17 = [tag(S3, 90, 430, "6th century · Rome: 4 weeks", AL("Rome", 17) - 0.3, "", 50), tag(S3, 90, 540, "The East: other customs", AL("Eastern", 17) - 0.3, "acc", 50)]
gone(t17, LS[18] - 0.4)
tag(S3, 90, 430, "Orthodox: 40 days from November 15", AL("November", 18) - 0.5, "", 44)
tag(S3, 90, 540, "Protestants: varied practices", AL("Protestant", 18) - 0.3, "acc", 46)

# =====================================================================  S4 : December 25 (lines 19-24)
t = LS[19] - 0.4
cam(t, S4)
headline(S4, 170, ["[December 25]"], t + 0.1, kicker="Not in the Bible either", hl_t=AL("December", 19) + 0.05, size=112)
S_(S4, "sym-balance", 1450, 420, 260, LS[21] + 0.3, rot=2)
t19 = tag(S4, 90, 430, "The date is not in the Bible", LS[19] + 0.3, "acc", 50)
gone([t19], LS[20] - 0.4)
t20 = [tag(S4, 90, 430, "The Gospels: no date", AL("Gospels", 20) - 0.3, "", 50), tag(S4, 90, 540, "First trace: Rome, 4th century", AL("Rome", 20) - 0.5, "acc", 48)]
gone(t20, LS[21] - 0.4)
t21 = [stamp(S4, 90, 440, "Two hypotheses", AL("hypotheses", 21) - 0.3, rot=-3, size=70), tag(S4, 90, 620, "Pagan sun festivals?", AL("sun", 21) - 0.6, "", 48), tag(S4, 90, 730, "Calculated from Jesus' death?", AL("death", 21) - 0.5, "", 46)]
gone(t21, LS[22] - 0.4)
t22 = [tag(S4, 90, 430, "Historians disagree", AL("Historians", 22) - 0.3, "", 52), stamp(S4, 90, 560, "No certainty", AL("certainty", 22) - 0.6, rot=-3, size=64)]
gone(t22, LS[23] - 0.4)
c23 = card(S4, 90, 420, "First revelation", "A beautiful tradition, not a prescription", AL("revelation", 23) - 0.4, w=1000, size=48)
gone([c23], LS[24] - 0.4)
tag(S4, 90, 430, "Stay: the wreath, the calendar", LS[24] + 0.3, "acc", 48)

# =====================================================================  S5 : the promises (lines 25-32)
t = LS[25] - 0.4
cam(t, S5)
headline(S5, 170, ["Centuries of [waiting]"], t + 0.1, kicker="Isaiah · Micah", hl_t=AL("waiting", 25) + 0.05, size=104)
S_(S5, "scribe", 1500, 420, 190, LS[27] + 0.3, rot=2)
t25 = tag(S5, 90, 430, "A great deal about waiting", LS[25] + 0.3, "acc", 50)
gone([t25], LS[26] - 0.4)
t26 = [tag(S5, 90, 430, "A king", AL("king", 26) - 0.3, "", 56), tag(S5, 90, 540, "A savior", AL("savior", 26) - 0.3, "", 56), tag(S5, 90, 650, "A deliverer", AL("deliverer", 26) - 0.3, "acc", 56)]
gone(t26, LS[27] - 0.4)
c27 = card(S5, 90, 420, "Isaiah 9" + BIB, "“For a child is born to us. A son is given to us.”", AL("child", 27) - 0.5, w=1000, size=44)
gone([c27], LS[28] - 0.4)
c28 = card(S5, 90, 420, "Micah 5", "Bethlehem, “small among the clans of Judah”", AL("Bethlehem", 28) - 0.4, w=1000, size=44)
gone([c28], LS[29] - 0.4)
c29 = card(S5, 90, 420, "Isaiah 7" + BIB, "“the virgin will conceive… Immanuel”", AL("virgin", 29) - 0.5, w=1000, size=44)
gone([c29], LS[30] - 0.4)
c30 = put(S5, 90, 420, "<small>Hebrew word</small><span style='font-size:84px'>almah</span> “young woman”", "card", "width:900px;font-size:58px")
blur_in(c30, AL("almah", 30) - 0.3, 14)
gone([c30], LS[31] - 0.4)
c31 = put(S5, 90, 420, "<small>Septuagint · Greek</small><span style='font-size:84px'>parthenos</span> “virgin”", "card", "width:900px;font-size:58px")
blur_in(c31, AL("parthenos", 31) - 0.3, 14)
gone([c31], LS[32] - 0.4)
stamp(S5, 90, 440, "Immanuel: “God with us”", AL("Immanuel", 32) - 0.4, rot=-3, size=56)

# =====================================================================  S6 : promise in the ruins (lines 33-38)
t = LS[33] - 0.4
cam(t, S6)
headline(S6, 170, ["A promise in the [ruins]"], t + 0.1, kicker="Isaiah 11 · Jeremiah 33 · Isaiah 40", hl_t=AL("ruins", 36) + 0.05, size=96)
S_(S6, "ville", 1450, 420, 300, LS[34] + 0.3, rot=2)
c33 = card(S6, 90, 420, "Isaiah 11" + BIB, "“A shoot will come out of the stump of Jesse”", AL("shoot", 33) - 0.4, w=1000, size=44)
gone([c33], LS[34] - 0.4)
c34 = card(S6, 90, 420, "Jeremiah 33" + BIB, "“I will perform that good word”", AL("promises", 34) - 0.6, w=1000, size=44)
t34 = tag(S6, 90, 650, "A promise made during the exile", AL("exile", 34) - 0.4, "acc", 48)
gone([c34, t34], LS[35] - 0.4)
c35 = card(S6, 90, 420, "Isaiah 40" + BIB, "“Comfort, comfort my people”", AL("Comfort", 35) - 0.3, w=1000, size=46)
gone([c35], LS[36] - 0.4)
t36 = [tag(S6, 90, 430, "Dark times", E("dark", 36, 0.3, 0.6), "", 52), tag(S6, 90, 540, "A promise whispered", AL("ruins", 36) - 0.6, "acc", 52)]
gone(t36, LS[37] - 0.4)
c37 = card(S6, 90, 420, "Intertestamental period", "≈ 4 centuries of silence", AL("intertestamental", 37) - 0.5, w=900, size=48)
gone([c37], LS[38] - 0.4)
tag(S6, 90, 430, "No recognized prophet", AL("prophet", 38) - 0.3, "", 50)
tag(S6, 90, 540, "A people under foreign rule", AL("foreign", 38) - 0.3, "", 50)
tag(S6, 90, 650, "A painful waiting", AL("painful", 38) - 0.5, "acc", 50)

# =====================================================================  S7 : prepare the way (lines 39-41)
t = LS[39] - 0.4
cam(t, S7)
headline(S7, 170, ["Prepare the [way]"], t + 0.1, kicker="Luke 3", hl_t=AL("Make", 39) + 0.05, size=112)
S_(S7, "veilleur", 1500, 420, 200, LS[39] + 0.5, rot=2)
c39 = card(S7, 90, 420, "Luke 3" + BIB, "“Make ready the way of the Lord. Make his paths straight.”", AL("Make", 39) - 0.3, w=1000, size=42)
gone([c39], LS[40] - 0.4)
t40 = [tag(S7, 90, 430, "The heart of Advent", E("heart", 40, 0.5, 0.8), "acc", 56), tag(S7, 90, 540, "Roads were repaired before a king", AL("roads", 40) - 0.4, "", 46)]
gone(t40, LS[41] - 0.4)
tag(S7, 90, 430, "Prepare your heart like a road", AL("road", 41) - 0.8, "acc", 50)

# =====================================================================  S8 : Luke's people (lines 42-54)
t = LS[42] - 0.4
cam(t, S8)
headline(S8, 170, ["Those who [wait]"], t + 0.1, kicker="Gospel of Luke", hl_t=AL("waiting", 42) + 0.05, size=112)
S_(S8, "ancien", 1500, 420, 190, LS[43] + 0.3, rot=2)
t42 = tag(S8, 90, 430, "People who are waiting", LS[42] + 0.3, "acc", 48)
gone([t42], LS[43] - 0.4)
t43 = [tag(S8, 90, 430, "Zechariah, an elderly priest", AL("Zechariah", 43) - 0.3, "", 50), tag(S8, 90, 540, "He doubts, he loses his speech", AL("speech", 43) - 0.5, "acc", 48)]
gone(t43, LS[44] - 0.4)
t44 = [stamp(S8, 90, 440, "Nine months of silence", AL("silence", 44) - 0.5, rot=-3, size=60)]
gone(t44, LS[45] - 0.4)
c45 = card(S8, 90, 420, "Luke 1" + BIB, "“Behold, the handmaid of the Lord”", AL("handmaid", 45) - 0.4, w=1000, size=44)
gone([c45], LS[46] - 0.4)
c46 = card(S8, 90, 420, "The Magnificat", "“My soul magnifies the Lord”", AL("magnifies", 46) - 0.5, w=1000, size=46)
gone([c46], LS[47] - 0.4)
t47 = [tag(S8, 90, 430, "Joseph: a dream", AL("dream", 47) - 0.3, "", 52), tag(S8, 90, 540, "He hesitates, then welcomes her", AL("home", 47) - 0.9, "acc", 48)]
gone(t47, LS[48] - 0.4)
t48 = [tag(S8, 90, 430, "Augustus' decree: a census", AL("census", 48) - 0.5, "", 48), tag(S8, 90, 540, "Joseph and Mary go up to Bethlehem", AL("Bethlehem", 48) - 0.3, "", 44)]
gone(t48, LS[49] - 0.4)
c49 = card(S8, 90, 420, "Luke 2" + BIB, "“laid him in a feeding trough”", AL("trough", 49) - 0.7, w=1000, size=46)
gone([c49], LS[50] - 0.4)
c50 = put(S8, 90, 420, "<small>Greek word</small><span style='font-size:84px'>kataluma</span> a guest room", "card", "width:1000px;font-size:50px")
blur_in(c50, AL("kataluma", 50) - 0.3, 14)
gone([c50], LS[51] - 0.4)
s51 = stamp(S8, 90, 440, "A humble place", AL("humble", 51) - 0.5, rot=-3, size=70)
gone([s51], LS[52] - 0.4)
t52 = [tag(S8, 90, 430, "Doubt · trust", AL("doubt", 52) - 0.3, "", 50), tag(S8, 90, 540, "Silence · decision", AL("decision", 52) - 0.5, "", 50)]
gone(t52, LS[53] - 0.4)
t53 = [tag(S8, 90, 430, "Simeon: “the consolation of Israel”", AL("Simeon", 53) - 0.3, "", 46), tag(S8, 90, 540, "Anna, a prophetess", AL("Anna", 53) - 0.3, "acc", 52)]
gone(t53, LS[54] - 0.4)
tag(S8, 90, 430, "Waiting rewarded", AL("rewarded", 54) - 0.5, "acc", 52)

# =====================================================================  S9 : two comings (lines 55-62)
t = LS[55] - 0.4
cam(t, S9)
headline(S9, 170, ["Two [comings]"], t + 0.1, kicker="Bethlehem and the end of time", hl_t=AL("second", 56) + 0.05, size=112)
S_(S9, "porte-ville", 1450, 420, 300, LS[56] + 0.3, rot=2)
t55 = tag(S9, 90, 430, "Advent is not only about Bethlehem", LS[55] + 0.3, "acc", 46)
gone([t55], LS[56] - 0.4)
t56 = [tag(S9, 90, 430, "1st coming: the child of Bethlehem", AL("first", 56) - 0.3, "", 48), tag(S9, 90, 540, "2nd coming: the end of time", AL("second", 56) - 0.3, "acc", 48)]
gone(t56, LS[57] - 0.4)
c57 = card(S9, 90, 420, "Matthew 24" + BIB, "“Watch therefore…”", AL("Watch", 57) - 0.3, w=900, size=52)
gone([c57], LS[58] - 0.4)
c58 = card(S9, 90, 420, "Revelation 22" + BIB, "“Yes, come, Lord Jesus.”", AL("Lord", 58) - 0.5, w=900, size=52)
gone([c58], LS[59] - 0.4)
c59 = put(S9, 90, 420, "<small>Aramaic word · 1 Corinthians 16</small><span style='font-size:84px'>maranatha</span>", "card", "width:1000px;font-size:46px")
blur_in(c59, AL("maranatha", 59) - 0.3, 14)
gone([c59], LS[60] - 0.4)
t60 = [tag(S9, 90, 430, "“Our Lord, come!”", AL("ways", 60) - 0.2, "", 52), tag(S9, 90, 540, "“Our Lord comes.”", AL("translation", 60) - 2.0, "acc", 52)]
gone(t60, LS[61] - 0.4)
s61 = stamp(S9, 90, 440, "A prayer: Come", AL("prayer", 61) - 0.4, rot=-3, size=70)
gone([s61], LS[62] - 0.4)
tag(S9, 90, 620, "Looking back, looking ahead", AL("strange", 62) - 0.5, "acc", 44)

# =====================================================================  S10 : wreath and calendar (lines 63-67)
t = LS[63] - 0.4
cam(t, S10)
headline(S10, 170, ["Wreath and [calendar]"], t + 0.1, kicker="What was added", hl_t=AL("wreath", 63) + 0.05, size=104)
S_(S10, "livres", 1500, 420, 200, LS[65] + 0.3, rot=2)
t63 = tag(S10, 90, 430, "The wreath: fairly recent", AL("wreath", 63) - 0.3, "acc", 50)
gone([t63], LS[64] - 0.4)
t64 = [tag(S10, 90, 430, "19th century · Germany", LS[64] + 0.3, "", 50), tag(S10, 90, 540, "Wichern, a pastor in Hamburg", AL("Wichern", 64) - 0.3, "acc", 48)]
gone(t64, LS[65] - 0.4)
t65 = [tag(S10, 90, 430, "The calendar: Germany too", AL("calendar", 65) - 0.3, "", 50), tag(S10, 90, 540, "Little doors", AL("doors", 65) - 0.3, "", 52)]
gone(t65, LS[66] - 0.4)
t66 = [tag(S10, 90, 430, "4 candles: hope, peace, joy, love", AL("hope", 66) - 0.3, "", 44), stamp(S10, 90, 560, "Names vary", AL("fixes", 66) - 0.6, rot=-3, size=60)]
gone(t66, LS[67] - 0.4)
tag(S10, 90, 430, "Church gestures, not commandments", AL("gestures", 67) - 0.3, "acc", 46)

# =====================================================================  S11 : what to keep (lines 68-76)
t = LS[68] - 0.4
cam(t, S11)
headline(S11, 170, ["What we can [keep]"], t + 0.1, kicker="Today", hl_t=AL("keep", 68) + 0.05, size=104)
S_(S11, "veilleur", 1500, 420, 200, LS[69] + 0.3, rot=2)
t68 = tag(S11, 90, 430, "What to keep from Advent?", LS[68] + 0.2, "acc", 52)
gone([t68], LS[69] - 0.4)
t69 = [tag(S11, 90, 430, "1. The waiting", AL("waiting", 69) - 0.3, "", 56), tag(S11, 90, 540, "An act of resistance", AL("resistance", 69) - 0.5, "acc", 50)]
gone(t69, LS[70] - 0.4)
t70 = [tag(S11, 90, 430, "2. The preparation", AL("preparation", 70) - 0.3, "", 56), tag(S11, 90, 540, "Slow down", AL("slow", 70) - 0.3, "acc", 56)]
gone(t70, LS[71] - 0.4)
t71 = [tag(S11, 90, 430, "3. The hope", AL("hope", 71) - 0.3, "", 56), tag(S11, 90, 540, "God keeps his promises", AL("promises", 71) - 0.4, "acc", 50)]
gone(t71, LS[72] - 0.4)
c72 = put(S11, 90, 420, "<small>Hebrew word</small><span style='font-size:84px'>tiqvah</span> “hope”", "card", "width:900px;font-size:56px")
blur_in(c72, AL("tiqvah", 72) - 0.3, 14)
t72 = tag(S11, 90, 700, "Root qavah: to wait, to stretch toward", AL("qavah", 72) - 0.4, "acc", 46)
gone([c72, t72], LS[73] - 0.4)
c73 = card(S11, 90, 420, "Joshua 2" + BIB, "tiqvah = also a cord (the scarlet cord)", AL("cord", 73) - 0.5, w=1000, size=44)
gone([c73], LS[74] - 0.4)
t74 = [stamp(S11, 90, 440, "A reading, not a fact", AL("reading", 74) - 0.5, rot=-3, size=58), tag(S11, 90, 620, "A stretched cord: a waiting that holds", AL("cord", 74) - 0.4, "", 44)]
gone(t74, LS[75] - 0.4)
c75 = put(S11, 90, 420, "<small>Gaudete · Philippians 4</small><span style='font-size:70px'>“Rejoice in the Lord always!”</span>", "card", "width:1000px;font-size:46px")
blur_in(c75, AL("Gaudete", 75) - 0.3, 14)
gone([c75], LS[76] - 0.4)
tag(S11, 90, 430, "A joy that knows the road moves forward", AL("weariness", 76) - 0.5, "acc", 44)

# =====================================================================  S12 : a hard season (lines 77-81)
t = LS[77] - 0.4
cam(t, S12)
headline(S12, 170, ["When the season is [hard]"], t + 0.1, kicker="Application", hl_t=AL("hard", 77) + 0.05, size=100)
S_(S12, "pere", 1500, 420, 190, LS[79] + 0.3, rot=2)
t77 = tag(S12, 90, 430, "A hard season for many", LS[77] + 0.3, "acc", 46)
gone([t77], LS[78] - 0.4)
t78 = [tag(S12, 90, 430, "Loneliness", AL("loneliness", 78) - 0.3, "", 52), tag(S12, 90, 540, "Grief", AL("grief", 78) - 0.3, "", 52), tag(S12, 90, 650, "Left out of the celebrations", AL("celebrations", 78) - 0.6, "acc", 48)]
gone(t78, LS[79] - 0.4)
t79 = [tag(S12, 90, 430, "You are not alone", AL("alone", 79) - 0.3, "acc", 56), tag(S12, 90, 540, "Hannah, mother of Samuel: she wept", AL("wept", 79) - 0.8, "", 44)]
gone(t79, LS[80] - 0.4)
t80 = [tag(S12, 90, 430, "A loved one", AL("loved", 80) - 0.3, "", 52), tag(S12, 90, 540, "A pastor", AL("pastor", 80) - 0.3, "", 52), tag(S12, 90, 650, "A health professional", AL("professional", 80) - 0.4, "acc", 52),
       stamp(S12, 90, 770, "Not a lack of faith", AL("faith", 80) - 0.5, rot=-3, size=52)]
gone(t80, LS[81] - 0.4)
tq = tag(S12, 90, 430, "What are you really waiting for?", LS[81] + 0.4, "acc", 46)
cta = put(S12, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Tell me in the comments', "cta")
blur_in(cta, AL("comments", 81) - 1.0, 14)
sfx("click", AL("comments", 81) - 1.0, 0.8)
gone([tq, cta], LS[82] - 0.3)

# =====================================================================  S13 : conclusion (lines 82-87)
t = LS[82] - 0.4
cam(t, S13)
headline(S13, 170, ["Advent, [waiting] for a king"], t + 0.1, kicker="The answer", hl_t=AL("question", 82) + 0.05, size=96)
S_(S13, "scribe", 1500, 420, 190, LS[85] + 0.3, rot=2)
t82 = tag(S13, 90, 430, "Not in the Bible, and yet…", LS[82] + 0.3, "acc", 50)
gone([t82], LS[83] - 0.4)
t83 = [tag(S13, 90, 430, "A word of emperors", AL("emperors", 83) - 0.4, "", 52), tag(S13, 90, 540, "Taken up to say another king comes", AL("another", 83) - 0.4, "acc", 46)]
gone(t83, LS[84] - 0.4)
t84 = [tag(S13, 90, 430, "Weeks, candles, doors", AL("candles", 84) - 0.4, "", 46), tag(S13, 90, 540, "Beautiful, not required", AL("required", 84) - 0.5, "acc", 52)]
gone(t84, LS[85] - 0.4)
t85 = [tag(S13, 90, 430, "Prepare your road", E("message", 85, 0.3, 0.6), "", 52), tag(S13, 90, 540, "Stay watchful", AL("watchful", 85) - 0.3, "", 52), tag(S13, 90, 650, "Hope", AL("hope", 85) - 0.3, "acc", 56)]
gone(t85, LS[86] - 0.4)
t86 = [stamp(S13, 90, 440, "The first candle", AL("candle", 86) - 0.5, rot=-3, size=64), tag(S13, 90, 620, "What it means, and what it does not", AL("mean", 86) - 0.5, "acc", 44)]
gone(t86, LS[87] - 0.3)

t_end = AL("Every", 87) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(AL("Every", 87) - 0.8, DUR_)]
build(
    chapters=[("01", "The word", 0, LS[14]), ("02", "The tradition", LS[14], LS[25]), ("03", "Biblical waiting", LS[25], LS[55]), ("04", "Today", LS[55], DUR_)],
    suppress=supp,
    endcard={"kicker": "Every week", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("scribe", 150, 560, 280, -6), ("jesus-portrait", 1550, 330, 230, 5)]},
    endcard_t=AL("Every", 87) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
