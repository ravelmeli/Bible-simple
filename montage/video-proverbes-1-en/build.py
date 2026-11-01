"""Long video "Why Proverbs 1 is a key to reading the whole Bible" — English version 2 (visual upgrade), style 02, 16:9, 362.5 s.

Built with the kit engine (kit-style-02/moteur/style02.py), retention option, kinetic quotes, animated symbols.
18 stations, 21 camera stops, three stations revisited with a different state (wipe). Everything is timed on transcript.json.
Hebrew words are transliterated in Latin letters and written in HTML: have them proofread before publishing.
Run: python3 build.py   (then npx hyperframes check and npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - Proverbs 1, a key to reading - style 02", "lang": "en",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
DUR_ = 362.5
s.setup(here=HERE, duration=DUR_, cols=5, rows=4, fmt="16:9", theme=THEME, bpm=96, zoom=1.15, xmap=(190, 0.8539), ymap=(208, 0.85))
from style02 import *  # noqa: E402,F401,F403
import style02  # noqa: E402

MANQUES = []
SUPP = []
# début de chaque ligne du script (s) : repères de plan
LS = {1: 0.0, 2: 4.8, 3: 8.5, 4: 12.9, 5: 18.4, 6: 24.6, 7: 31.9, 8: 40.4, 9: 41.9, 10: 48.4, 11: 54.9, 12: 64.4, 13: 73.1, 14: 80.0,
      15: 84.8, 16: 98.8, 17: 101.0, 18: 104.3, 19: 117.7, 20: 125.3, 21: 128.9, 22: 136.1, 23: 147.3, 24: 155.5, 25: 165.3, 26: 169.3,
      27: 173.6, 28: 178.5, 29: 185.0, 30: 190.6, 31: 198.2, 32: 204.0, 33: 215.3, 34: 224.9, 35: 233.7, 36: 241.9, 37: 246.0, 38: 255.4,
      39: 267.8, 40: 276.1, 41: 281.8, 42: 285.4, 43: 290.1, 44: 298.4, 45: 308.2, 46: 320.5, 47: 332.0, 48: 340.9, 49: 347.5, 50: 355.3, 51: DUR_}


def A(word, after=0.0, n=0):
    """Start of the n-th occurrence of `word` spoken at or after `after` seconds."""
    hits = [w["start"] for w in style02.words if style02.norm(w["text"]) == style02.norm(word) and w["start"] >= after - 0.01]
    if len(hits) <= n:
        MANQUES.append((word, after, n))
        return max(after, 1.0) + 0.5
    return hits[n]


RATIO = {}


def S_(station, name, x, y, w, t, **kw):
    """sticker() with an exact overflow check against the caption band (zoom 1.15, ymap)."""
    i, h = sticker(station, name, x, y, w, t, **kw)
    bas = 208 + 0.85 * (y - 170) + h
    if bas > 830:
        print(f"WARNING {name} at y={y} w={w}: bottom at {bas:.0f} (limit 830)")
    return i


def kq(station, x, y, ref_txt, text, line, first, width=1000, size=38, last=None):
    """Kinetic quote: lights up word by word. `first` = first spoken word of the quote (searched from line start)."""
    t0 = A(first, LS[line]) - 0.05
    t1 = (LS[line + 1] - 0.25) if last is None else last
    SUPP.append((t0 - 0.1, t1 + 0.2))
    return kinetic_quote(station, x, y, ref_txt, text, t0, t1, width=width, size=size)


MARCHE, CLE, SALOMON, EZECHIAS, EGYPTE = (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)
PROLOGUE, HOKHMAH, MOUSSAR, YIRAH, CENTRE = (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)
PERE, BANDE, CHEMINS, SAGESSE, FRISE = (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)
NT, LECTURES, APPEL = (4, 3), (3, 3), (2, 3)

html.append('<style>'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')


def slot(station, name, x, y, w, t0, t1, **kw):
    """Sticker that shows from t0 to t1 (then fades): used for sequences of illustrations on the same slot."""
    i = S_(station, name, x, y, w, t0, **kw)
    fade(i, t1)
    return i


# =====================================================================  MARKETPLACE (0 → 18.4)
cam(0, MARCHE)
S_(MARCHE, "sagesse-pied", 110, 330, 270, 0.0, rot=-3, instant=True)
headline(MARCHE, 170, ["A woman [shouts] in the marketplace"], 0.0, kicker="Proverbs 1", hl_t=A("shouting") + 0.05, size=88)
f1 = S_(MARCHE, "foule", 940, 330, 330, A("middle") - 0.3, rot=2)
e1 = S_(MARCHE, "etal", 1380, 330, 300, A("marketplace") - 0.2, rot=3)
tag(MARCHE, 520, 380, "No stall", A("stall") - 0.1, "", 54)
tag(MARCHE, 520, 490, "No army", A("army") - 0.1, "", 54)
tag(MARCHE, 520, 600, "No title", A("title") - 0.1, "acc", 54)
burst(MARCHE, 700, 280, A("shouting") + 0.1)
teaser(MARCHE, 520, 740, "Who is she?", 9.4, hold=3.4)
for _i in (f1, e1):
    fade(_i, A("gates") - 0.2)
S_(MARCHE, "porte-ville", 1000, 380, 520, A("gates") - 0.1, rot=-2)
label_box(MARCHE, 1000, 740, "The city gates", "where decisions are made", A("decisions") - 0.4)
ring(MARCHE, 265, 480, A("Wisdom") + 0.0, size=300)
hit(A("Wisdom"), 0.8)
tag(MARCHE, 520, 760, "Proverbs, chapter 1", A("chapter") - 0.1, "acc", 46)

# =====================================================================  KEY (18.4 → 40.4): where do I begin?
t = A("question", 18.0) - 0.5
cam(t, CLE)
headline(CLE, 170, ["Where do I [begin] ?"], t + 0.1, kicker="The question", hl_t=A("begin", 18.0) + 0.05, size=100)
S_(CLE, "panneau", 110, 330, 330, LS[5] + 0.5, rot=-2)
tag(CLE, 520, 360, "Reading plans", A("plans") - 0.2, "", 48)
tag(CLE, 520, 450, "Summaries", A("summaries") - 0.2, "", 48)
tag(CLE, 520, 540, "Commentaries", A("commentaries") - 0.2, "", 48)
tag(CLE, 520, 640, "One key is missing", A("missing") - 0.5, "acc", 58)
gk = glow(CLE, 1640, 480, A("key", 24.0) - 0.2, size=400)
k1 = S_(CLE, "cle", 1550, 330, 190, A("key", 24.0) - 0.2, rot=8)
animate(k1, "turn", A("key", 24.0) + 0.2)
S_(CLE, "cma-cle-romaine", 1250, 330, 230, A("key", 31.0) - 0.4, rot=-3)
label_box(CLE, 1290, 760, "A Roman key", "1st c. · Cleveland Museum of Art", A("key", 31.0) + 0.1)
label_box(CLE, 520, 740, "Proverbs 1", "a key to reading", A("Proverbs", 31.0) - 0.1)
tag(CLE, 880, 745, "Not the only key", A("only") - 0.2, "", 40)
hit(A("key", 24.0), 0.8)

# =====================================================================  SOLOMON (40.4 → 54.9): the context
t = A("start", 39.0) - 0.4
cam(t, SALOMON)
headline(SALOMON, 170, ["The [context]"], t + 0.1, kicker="Proverbs 1:1", hl_t=A("context", 39.0) + 0.05, size=100)
kq(SALOMON, 90, 380, "Proverbs 1:1 · World English Bible", "“The proverbs of Solomon, the son of David, king of Israel.”", 9, "proverbs", width=1000, size=44)
S_(SALOMON, "salomon", 1450, 330, 215, A("Solomon", 41.9) - 0.1, rot=3)
gc = glow(SALOMON, 1300, 440, A("wisest") - 0.4, size=320)
S_(SALOMON, "sym-couronne", 1150, 340, 250, A("wisest") - 0.4, rot=-6)
tag(SALOMON, 90, 640, "10th century BC", A("tenth") - 0.2, "acc", 56)
tag(SALOMON, 90, 760, "The wisest king of his time", A("wisest") - 0.4, "", 44)
ring(SALOMON, 1555, 450, A("Solomon", 48.0), size=240)
burst(SALOMON, 600, 700, A("tenth") + 0.1)

# =====================================================================  HEZEKIAH (54.9 → 64.4)
t = A("Historians") - 0.5
cam(t, EZECHIAS)
headline(EZECHIAS, 170, ["A book [shaped] later"], t + 0.1, kicker="Historians think", hl_t=A("shape") + 0.05, size=88)
S_(EZECHIAS, "ville", 700, 400, 330, A("Hezekiah") - 0.5, rot=-2)
S_(EZECHIAS, "scribe", 100, 380, 390, A("Hezekiah") - 0.2, rot=-2)
tag(EZECHIAS, 700, 640, "King Hezekiah's men", A("Hezekiah") - 0.1, "", 46)
tag(EZECHIAS, 700, 740, "copied more proverbs", A("copied") - 0.1, "acc", 42)
S_(EZECHIAS, "sceau-anse-jarre", 1250, 380, 400, A("copied") + 0.3, rot=3)
label_box(EZECHIAS, 1250, 700, "Jar handle with a seal", "Israel, late 8th-7th c. BC · The Met", A("copied") + 0.6)
label_box(EZECHIAS, 100, 760, "Proverbs 25:1", "the text itself hints at it", A("hints") - 0.2)

# =====================================================================  EGYPT (64.4 → 80.0): a shared language
t = A("Several") - 0.5
cam(t, EGYPTE)
headline(EGYPTE, 170, ["A shared [language]"], t + 0.1, kicker="Echoes from Egypt", hl_t=A("language", 64.0) + 0.05, size=96)
map_svg(EGYPTE, 70, 330, "assets/map.json", t + 0.3, A("Amenemope") - 0.3, width=640)
S_(EGYPTE, "cma-scribe-medthu", 960, 330, 270, A("Egyptian") - 0.2, rot=-3)
label_box(EGYPTE, 960, 780, "Seated scribe", "Egypt, c. 1450 BC · Cleveland Museum of Art", A("Egyptian") + 0.2)
S_(EGYPTE, "papyrus-hieratique", 1300, 360, 480, A("Instruction") - 0.1, rot=3)
label_box(EGYPTE, 1300, 530, "Letter on papyrus", "Egypt, c. 1470 BC · The Met", A("Amenemope") + 0.2)
tag(EGYPTE, 1300, 640, "A shared language", A("shared") - 0.1, "acc", 42)
gl = glow(EGYPTE, 1640, 790, A("stay") - 0.3, size=280)
S_(EGYPTE, "lampe", 1560, 740, 170, A("stay") - 0.3, rot=-3)
tag(EGYPTE, 960, 700, "One passage at a time", A("passage") - 0.2, "", 40)
burst(EGYPTE, 1100, 330, A("Amenemope") + 0.15)

# =====================================================================  PROLOGUE (80.0 → 98.8): what this book wants to do
t = A("what", 79.0) - 0.4
cam(t, PROLOGUE)
headline(PROLOGUE, 170, ["What this book [wants to do]"], t + 0.1, kicker="Proverbs 1:2-4", hl_t=A("right", 80.0) + 0.05, size=84)
teaser(PROLOGUE, 1000, 185, "Three Hebrew words to remember", 94.8, hold=3.2)
ru0 = slot(PROLOGUE, "rouleau", 1330, 380, 300, t + 0.4, A("wisdom", 84.8) - 0.1, rot=3)
animate(ru0, "unroll", t + 0.4)
kq(PROLOGUE, 90, 330, "Proverbs 1:2-4 · World English Bible",
   "“To know wisdom and instruction; to discern the words of understanding; to receive instruction in wise dealing, in righteousness, "
   "justice, and equity; to give prudence to the simple, to the young man knowledge and discretion.”", 15, "know", width=980, size=36)
# one illustration per idea, on the same slot
gP = glow(PROLOGUE, 1480, 480, A("wisdom", 84.8) - 0.1, size=380, dur=3.0)
slot(PROLOGUE, "lampe", 1330, 380, 300, A("wisdom", 84.8) - 0.1, A("instruction", 84.8) - 0.1, rot=-3)
slot(PROLOGUE, "rouleau", 1330, 380, 300, A("instruction", 84.8) - 0.1, A("understanding", 84.8) - 0.1, rot=3)
sp = slot(PROLOGUE, "sym-porte", 1360, 330, 230, A("understanding", 84.8) - 0.1, A("righteousness") - 0.1, rot=2)
animate(sp, "open", A("understanding", 84.8) - 0.1)
sb = slot(PROLOGUE, "sym-balance", 1330, 340, 320, A("righteousness") - 0.1, A("prudence") - 0.1, rot=0)
animate(sb, "rock", A("righteousness") - 0.1, dur=5.0)
slot(PROLOGUE, "fils", 1450, 330, 140, A("prudence") - 0.1, A("knowledge") - 0.1, rot=2)
slot(PROLOGUE, "etudiant", 1330, 340, 310, A("knowledge") - 0.1, A("discretion") + 1.4, rot=-2)

# =====================================================================  CHOKHMAH (98.8 → 117.7)
t = A("pause") - 0.5
cam(t, HOKHMAH)
headline(HOKHMAH, 170, ["Three Hebrew [words]"], t + 0.1, kicker="1 · Wisdom", hl_t=A("Hebrew", 98.0) + 0.05, size=96)
gh0 = glow(HOKHMAH, 1430, 520, t + 0.3, size=420, dur=5.0)
lh0 = slot(HOKHMAH, "lampe", 1290, 400, 280, t + 0.3, A("Bezalel") - 0.4, rot=-3)
w1 = put(HOKHMAH, 90, 330, "chokhmah", "word", "font-size:190px")
blur_in(w1, A("chokhmah") - 0.1, 20)
tag(HOKHMAH, 90, 600, "« wisdom »", A("translate") - 0.1, "", 56)
gb = glow(HOKHMAH, 1430, 520, A("Bezalel") - 0.3, size=420)
S_(HOKHMAH, "betsaleel", 1300, 330, 250, A("Bezalel") - 0.3, rot=3)
tag(HOKHMAH, 90, 700, "Not first about theory", A("theory") - 0.4, "", 50)
tag(HOKHMAH, 90, 790, "The skill of a craftsman", A("craftsman") - 0.2, "acc", 50)
S_(HOKHMAH, "or-ornement", 1650, 360, 110, A("sanctuary") - 0.2, rot=-4)
label_box(HOKHMAH, 700, 700, "Bezalel", "Exodus 31:1-6", A("Bezalel") + 0.1)
tag(HOKHMAH, 700, 790, "Knowing how to make, how to live", A("live", 110.0) - 0.8, "", 36)
burst(HOKHMAH, 1450, 330, A("Bezalel") + 0.15)

# =====================================================================  MUSAR (117.7 → 125.3)
t = A("second", 117.0) - 0.4
cam(t, MOUSSAR)
headline(MOUSSAR, 170, ["The second word"], t + 0.1, kicker="2 · Instruction", size=96)
w2 = put(MOUSSAR, 90, 330, "musar", "word", "font-size:190px")
blur_in(w2, A("musar") - 0.1, 20)
S_(MOUSSAR, "tablette-ecole", 900, 340, 420, A("musar") + 0.2, rot=-2)
label_box(MOUSSAR, 900, 640, "A pupil's writing board", "Egypt, c. 1900 BC · The Met", A("discipline") - 0.4)
S_(MOUSSAR, "etudiant", 1400, 330, 330, A("instruction", 117.7) - 0.1, rot=3)
tag(MOUSSAR, 90, 620, "« instruction »", A("instruction", 117.7) - 0.1, "", 52)
tag(MOUSSAR, 90, 720, "or « discipline »", A("discipline") - 0.1, "acc", 52)

# =====================================================================  YIRAH (125.3 → 147.3)
t = A("third", 125.0) - 0.4
cam(t, YIRAH)
headline(YIRAH, 170, ["The third word"], t + 0.1, kicker="3 · Fear", size=96)
w3 = put(YIRAH, 90, 300, "yirah", "word", "font-size:190px")
blur_in(w3, A("yirah") - 0.1, 20)
tag(YIRAH, 90, 560, "« fear »", A("fear", 125.3) - 0.1, "acc", 56)
kq(YIRAH, 90, 650, "Proverbs 1:7 · World English Bible",
   "“The fear of Yahweh is the beginning of knowledge; but the foolish despise wisdom and instruction.”", 21, "fear", width=1000, size=36)
slot(YIRAH, "ancien", 1450, 300, 190, A("respect") - 0.3, A("wonder") - 0.2, rot=2)
sm_ = slot(YIRAH, "montagne", 1300, 340, 380, A("wonder") - 0.2, A("awareness") - 0.3, rot=-2)
animate(sm_, "zoom", A("wonder") - 0.2, dur=4.0)
gy = glow(YIRAH, 1480, 480, A("awareness") - 0.3, size=360, dur=5.0)
S_(YIRAH, "mains-lampe", 1330, 360, 330, A("awareness") - 0.3, rot=2)
tag(YIRAH, 1000, 300, "Not only dread", A("dread") - 0.3, "", 44)
burst(YIRAH, 700, 520, A("surprising") + 0.1)

# =====================================================================  CENTER (147.3 → 165.3): an order
t = A("sets") - 0.6
cam(t, CENTRE)
headline(CENTRE, 170, ["An [order]"], t + 0.1, kicker="Proverbs 1:7", hl_t=A("order") + 0.05, size=110)
tag(CENTRE, 90, 400, "Not at the center", A("center") - 0.4, "", 56)
tag(CENTRE, 90, 520, "God in his place", A("place", 147.3) - 0.3, "acc", 56)
bal0 = S_(CENTRE, "sym-balance", 780, 520, 200, t + 0.4, rot=0)
animate(bal0, "rock", t + 0.4, dur=7.0)
fade(bal0, A("key", 155.5) - 0.5)
tr = S_(CENTRE, "sym-arbre", 1330, 330, 180, A("begin", 147.3) - 0.3, rot=0)
animate(tr, "grow", A("begin", 147.3) - 0.3)
gC = glow(CENTRE, 1630, 540, A("key", 155.5) - 0.2, size=380)
k2 = S_(CENTRE, "cle", 1560, 330, 190, A("key", 155.5) - 0.2, rot=6)
animate(k2, "turn", A("key", 155.5) + 0.1)
stamp(CENTRE, 720, 430, "The key", A("key", 155.5) + 0.1, rot=-5, size=84)
bA = put(CENTRE, 90, 650, "“Be clever, and you will find God”", "card", "width:700px;font-size:34px;color:" + THEME["grey"])
blur_in(bA, A("clever") - 0.2, 14)
bB = put(CENTRE, 880, 650, "“Recognize God, and understanding will begin”", "card", "width:700px;font-size:34px;border-color:" + ACC)
blur_in(bB, A("recognize", 155.5) - 0.2, 14)
arrow(CENTRE, (800, 750), (870, 750), A("recognize", 155.5) - 0.1)

# =====================================================================  FATHER (165.3 → 178.5): first scene
t = A("prologue") - 0.5
cam(t, PERE)
headline(PERE, 170, ["Two [scenes]"], t + 0.1, kicker="Proverbs 1:8-33", hl_t=A("scenes", 165.0) + 0.05, size=104)
c1 = put(PERE, 90, 380, "<small>Scene 1</small>Verses 8 to 19: a father speaks to his son", "card", "width:820px;font-size:38px")
blur_in(c1, A("First", 168.0) - 0.1, 14)
S_(PERE, "pere", 1250, 330, 215, A("father", 169.0) - 0.2, rot=-2)
S_(PERE, "fils", 1520, 330, 150, A("son", 169.0) - 0.1, rot=3)
kq(PERE, 90, 520, "Proverbs 1:8 · World English Bible", "“My son, hear the instruction of your father, and don't forsake the teaching of your mother.”", 27, "son", width=820, size=36)
ring(PERE, 1360, 450, A("hear") - 0.1, size=260)

# =====================================================================  MEN (178.5 → 190.6): the lure and the trap
t = A("warns") - 0.7
cam(t, BANDE)
headline(BANDE, 170, ["Men who want to [lure] you"], t + 0.1, kicker="Proverbs 1:10-19", hl_t=A("follow") + 0.05, size=84)
S_(BANDE, "bande", 1000, 330, 500, A("men", 178.5) - 0.2, rot=-2)
tag(BANDE, 90, 400, "A share of the loot", A("loot") - 0.3, "", 54)
tag(BANDE, 90, 510, "A common purse", A("purse") - 0.3, "", 54)
S_(BANDE, "sym-coffre", 1560, 380, 250, A("loot") - 0.2, rot=4)
tag(BANDE, 90, 680, "The traps close on themselves", A("close", 185.0) - 0.5, "acc", 50)
burst(BANDE, 600, 440, A("loot") + 0.1)
burst(BANDE, 1000, 700, A("close", 185.0) + 0.1)
arrow(BANDE, (850, 760), (1050, 640), A("close", 185.0) - 0.1)

# =====================================================================  ROADS (190.6 → 198.2)
t = A("first", 190.0) - 0.8
cam(t, CHEMINS)
headline(CHEMINS, 170, ["Two [roads]"], t + 0.1, kicker="The first choice of the book", hl_t=A("roads") + 0.05, size=110)
S_(CHEMINS, "panneau", 700, 330, 320, A("roads") + 0.1, rot=-2)
ch = S_(CHEMINS, "chemins", 1150, 360, 400, A("quick") - 0.3, rot=2)
animate(ch, "zoom", A("quick") - 0.3, dur=6.0)
tag(CHEMINS, 90, 440, "Promises quick gains", A("quick") - 0.2, "", 50)
tag(CHEMINS, 90, 560, "Builds slowly", A("slowly") - 0.3, "acc", 56)
hit(A("roads") + 0.1, 0.7)

# =====================================================================  WISDOM SPEAKS (198.2 → 241.9)
t = A("Second", 198.0) - 0.4
cam(t, SAGESSE)
headline(SAGESSE, 170, ["Wisdom [speaks]"], t + 0.1, kicker="Scene 2 · verses 20-33", hl_t=A("speak") + 0.05, size=96)
S_(SAGESSE, "sagesse-pied", 100, 330, 270, A("Second", 198.0) + 0.3, rot=-3)
q1 = kq(SAGESSE, 520, 380, "Proverbs 1:20-21 · World English Bible",
        "“Wisdom calls aloud in the street. She utters her voice in the public squares. She calls at the head of the noisy crowd. "
        "At the entrance of the gates, in the city, she utters her words.”", 32, "Wisdom", width=1000, size=36)
fade(q1, LS[33] - 0.3)
old_ = [S_(SAGESSE, "porte-ville", 520, 330, 400, LS[33] - 0.1, rot=-2),
        S_(SAGESSE, "foule", 960, 330, 400, A("calls", 215.0) - 0.4, rot=2),
        S_(SAGESSE, "etal", 1470, 350, 280, A("noise") - 0.9, rot=3),
        S_(SAGESSE, "montagne", 520, 640, 300, A("mountaintop") - 0.3, rot=-2),
        tag(SAGESSE, 880, 680, "Not hidden on a mountaintop", A("hidden") - 0.2, "", 40),
        tag(SAGESSE, 880, 760, "Offered to everyone, in the noise", A("offered") - 0.2, "acc", 42)]
for _i in old_:
    fade(_i, A("refusal") - 0.6)
burst(SAGESSE, 1650, 350, A("noise") + 0.1)
rf = [tag(SAGESSE, 520, 380, "She calls…", A("refusal") - 0.3, "", 56), tag(SAGESSE, 520, 500, "…and nobody listens", A("listens") - 0.4, "", 56),
      tag(SAGESSE, 520, 640, "The fruit of our own choices", A("fruit") - 0.3, "acc", 50)]
# the mountain scene fades before the refusal
for _i in (rf[0],):
    pass
q2 = kq(SAGESSE, 520, 380, "Proverbs 1:33 · World English Bible",
        "“But whoever listens to me will dwell securely, and will be at ease, without fear of harm.”", 35, "But", width=1000, size=40,
        last=A("harm") + 0.4)
for _i in rf:
    fade(_i, LS[35] - 0.1)
sd = S_(SAGESSE, "sym-porte", 1580, 330, 200, A("securely") - 0.5, rot=2)
animate(sd, "open", A("securely") - 0.5)
gd = glow(SAGESSE, 1680, 480, A("securely") - 0.5, size=380, dur=6.0)
S_(SAGESSE, "sym-arbre", 1300, 600, 120, A("ease") - 0.4, rot=0)

# =====================================================================  ACROSS THE BIBLE (241.9 → 276.1)
t = A("talk", 241.0) - 0.8
cam(t, FRISE)
headline(FRISE, 170, ["A [key] running through the Bible"], t + 0.1, kicker="Three books, the same ground", hl_t=A("key", 242.0) + 0.05, size=84)
c_psa = kq(FRISE, 90, 360, "Psalm 111:10 · WEB", "“The fear of Yahweh is the beginning of wisdom.”", 37, "fear", width=480, size=32, last=A("wisdom", 246.0) + 0.8)
gF = glow(FRISE, 330, 770, A("Almost") - 1.5, size=300, dur=5.0)
S_(FRISE, "lampe", 240, 700, 220, A("Almost") - 1.5, rot=-3)
c_job = kq(FRISE, 650, 360, "Job 28:28 · WEB", "“Behold, the fear of the Lord, that is wisdom; to depart from evil is understanding.”", 38, "Behold", width=480, size=32)
S_(FRISE, "sym-coffre", 700, 670, 180, A("gold") - 0.3, rot=-3)
S_(FRISE, "or-ornement", 930, 650, 85, A("gold") - 0.1, rot=4)
c_ecc = kq(FRISE, 1210, 360, "Ecclesiastes 12:13 · WEB", "“Fear God, and keep his commandments; for this is the whole duty of man.”", 39, "Fear", width=480, size=32)
sbf = S_(FRISE, "sym-balance", 1290, 620, 200, A("duty") - 0.6, rot=0)
animate(sbf, "rock", A("duty") - 0.6, dur=6.0)
burst(FRISE, 330, 330, A("Almost") + 0.1)
burst(FRISE, 1700, 330, A("trying") + 0.1)

# =====================================================================  NEW TESTAMENT (276.1 → 290.1)
t = A("Then", 275.0) - 0.4
cam(t, NT)
headline(NT, 170, ["The New Testament picks up this [language]"], t + 0.1, kicker="Matthew · 1 Corinthians · James", hl_t=A("language", 276.0) + 0.05, size=72)
S_(NT, "jesus-pied", 90, 340, 190, A("Jesus", 276.0) - 0.2, rot=-3)
S_(NT, "salomon", 330, 345, 165, A("Solomon", 276.0) - 0.3, rot=3)
label_box(NT, 90, 790, "Matthew 12:42", "“someone greater than Solomon”", A("greater") - 0.1)
S_(NT, "paul-portrait", 700, 350, 300, A("Paul", 276.0) - 0.2, rot=-2)
label_box(NT, 700, 790, "1 Corinthians 1:24", "“the power of God and the wisdom of God”", A("power") - 0.2)
S_(NT, "lettre-papyrus-grec", 1230, 330, 230, A("James") - 0.3, rot=3)
gN = glow(NT, 1640, 480, A("ask", 285.0) - 0.3, size=360, dur=4.0)
S_(NT, "mains-lampe", 1500, 380, 280, A("ask", 285.0) - 0.3, rot=2)
label_box(NT, 1230, 790, "James 1:5", "“let him ask of God”", A("ask", 285.0) - 0.1)
ring(NT, 200, 540, A("Jesus", 276.0), size=300)

# =====================================================================  TWO READINGS (290.1 → 308.2)
t = A("honest", 289.0) - 0.7
cam(t, LECTURES)
headline(LECTURES, 170, ["Two [readings]"], t + 0.1, kicker="Let's be honest", hl_t=A("Christian", 290.0) + 0.05, size=104)
stamp(LECTURES, 1000, 190, "Christian tradition", A("Christian", 290.0) - 0.2, rot=-4, size=40)
tag(LECTURES, 90, 400, "Jesus = the wisdom of God", A("wisdom", 290.0) - 0.4, "acc", 50)
tag(LECTURES, 90, 520, "A Christian reading", A("Christian", 290.0) - 0.1, "", 50)
tag(LECTURES, 90, 640, "Not the Jewish reading", A("Jewish") - 0.2, "", 50)
cA = put(LECTURES, 90, 740, "<small>What the text says</small>Wisdom begins with a relationship with God, and it calls everyone",
         "card", "width:830px;font-size:30px")
blur_in(cA, A("What", 298.0) - 0.1, 14)
cB = put(LECTURES, 1000, 330, "<small>What Christian tradition adds</small>This wisdom took on a face",
         "card", "width:830px;font-size:34px;border-color:" + ACC)
blur_in(cB, A("tradition", 300.0) - 0.2, 14)
sbL = S_(LECTURES, "sym-balance", 1000, 560, 220, A("tradition", 300.0) - 0.6, rot=0)
animate(sbL, "rock", A("tradition", 300.0) - 0.6, dur=6.0)
S_(LECTURES, "jesus-portrait", 1450, 470, 270, A("face") - 0.2, rot=3)

# =====================================================================  KEY (revisit) 308.2 → 320.5
cam(LS[45] - 2.0, "all")
wipe(CLE, LS[45] - 2.1)
t = LS[45] - 0.4
cam(t, CLE)
headline(CLE, 170, ["A key to [reading]"], t + 0.1, kicker="The answer", hl_t=A("reading", 308.0) + 0.05, size=104)
gk2 = glow(CLE, 1620, 500, A("key", 308.0) - 0.1, size=420, dur=8.0)
k3 = S_(CLE, "cle", 1530, 300, 190, A("key", 308.0), rot=-6)
animate(k3, "turn", A("key", 308.0) + 0.5)
stamp(CLE, 90, 400, "A key to reading", A("gives", 308.0) + 0.2, rot=-4, size=72)
sdr = S_(CLE, "sym-porte", 1200, 330, 230, A("humility") - 0.5, rot=2)
animate(sdr, "open", A("humility") - 0.5)
tag(CLE, 90, 600, "With humility", A("humility") - 0.2, "", 56)
tag(CLE, 90, 700, "Living what we understand", A("live", 308.0) - 0.3, "acc", 56)
tag(CLE, 90, 800, "Rather than collecting information", A("collecting") - 0.3, "", 44)
burst(CLE, 1620, 400, A("read", 310.0) + 0.1)

# =====================================================================  CROSSROADS (revisit) 320.5 → 332.0
wipe(CHEMINS, LS[46] - 0.8)
t = LS[46] - 0.4
cam(t, CHEMINS)
headline(CHEMINS, 170, ["Your [crossroads]"], t + 0.1, kicker="This week", hl_t=A("crossroads") + 0.05, size=110)
S_(CHEMINS, "panneau", 1420, 330, 280, A("crossroads") - 0.3, rot=2)
sr = S_(CHEMINS, "etudiant", 1050, 330, 240, A("Slowly", 320.0) - 0.1, rot=-2)
label_box(CHEMINS, 90, 700, "Reread slowly", "the first seven verses of Proverbs 1", A("Slowly", 320.0) - 0.3)
tag(CHEMINS, 90, 590, "At which crossroads?", A("crossroads") - 0.1, "acc", 64)
tag(CHEMINS, 700, 700, "What do I already hear?", A("hear", 322.0) - 0.4, "", 48)
ring(CHEMINS, 1560, 470, A("crossroads") + 0.1, size=300)

# =====================================================================  CALL (332.0 → 340.9)
t = LS[47] - 0.3
cam(t, APPEL)
headline(APPEL, 170, ["Has a verse [guided] you?"], t + 0.1, kicker="Your turn", hl_t=A("guided") + 0.05, size=96)
S_(APPEL, "sagesse-portrait", 1400, 330, 330, t + 0.5, rot=3)
S_(APPEL, "foule", 960, 400, 340, A("together", 332.0) - 0.8, rot=-2)
label_box(APPEL, 90, 420, "Or a decision", "for which you're still seeking wisdom?", A("decision") - 0.2)
cta = put(APPEL, 90, 640, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Write it in the comments', "cta")
blur_in(cta, A("Write", 332.0) - 0.2, 14)
sfx("click", A("Write", 332.0) - 0.2, 0.8)
tag(APPEL, 90, 790, "No pressure: we're all reading together", A("pressure") - 0.2, "", 40)

# =====================================================================  MARKETPLACE (revisit) 340.9 → end
cam(LS[48] - 1.9, "all")
wipe(MARCHE, LS[48] - 2.0)
t = LS[48] - 0.4
cam(t, MARCHE)
headline(MARCHE, 170, ["She is still [shouting]"], t + 0.1, kicker="Conclusion", hl_t=A("shouting", 340.0) + 0.05, size=104)
S_(MARCHE, "sagesse-portrait", 1300, 330, 400, A("shouting", 340.0) - 0.2, rot=-3)
tag(MARCHE, 90, 400, "Not to shame you", A("shame") - 0.3, "", 56)
tag(MARCHE, 90, 520, "She knows where the two roads lead", A("roads", 341.0) - 0.8, "acc", 48)
gM = glow(MARCHE, 1500, 540, A("begin", 347.0) - 0.3, size=460, dur=6.0)
tag(MARCHE, 90, 700, "Begin in the right place", A("begin", 347.0) - 0.2, "acc", 56)
tag(MARCHE, 90, 800, "Recognize God in his place", A("recognize", 350.0) - 0.2, "", 50)
hit(A("recognize", 350.0), 0.8)

t_end = A("Every", 354.0) - 0.3
cam(t_end, "all")

supp = [(a, b) for a, b in SUPP] + [(A("Every", 354.0) - 0.8, DUR_)]
supp += [(LS[45] - 2.0, LS[45] - 0.5), (LS[48] - 1.9, LS[48] - 0.5)]
build(
    chapters=[("01", "Context", 0, LS[14]), ("02", "Three words", LS[14], LS[25]), ("03", "Two scenes", LS[25], LS[36]),
              ("04", "Across the Bible", LS[36], LS[45]), ("05", "How to read", LS[45], DUR_)],
    suppress=supp,
    endcard={"kicker": "Every week", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("sagesse-portrait", 150, 560, 330, -6), ("salomon", 1500, 330, 240, 5)]},
    endcard_t=A("Every", 354.0) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MISSING:", MANQUES)
