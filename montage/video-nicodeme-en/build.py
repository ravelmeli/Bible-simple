"""Long video "Nicodemus: the man who visited Jesus at night, until the day he was no longer afraid" (Faith Engineering) — style 02, 16:9. English version of montage/video-nicodeme/.

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

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - Nicodemus - style 02", "lang": "en",
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

# =====================================================================  S1 : l'homme de la nuit (lignes 1-7)
cam(0, S1)
headline(S1, 170, ["Nicodemus, the man of [the night]"], 0.0, kicker="Gospel of John", hl_t=AL("night", 1) + 0.05, size=96)
S_(S1, "veilleur", 1500, 420, 200, 0.0, rot=2, instant=True)
t1 = tag(S1, 90, 430, "The others: in broad daylight", AL("broad", 1) - 0.2, "", 50)
gone([t1], AL("comes", 1) - 0.3)
tl = tag(S1, 90, 540, "Him: at night", AL("comes", 1) - 0.2, "acc", 56)
gone([tl], LS[2] - 0.4)
t2 = [tag(S1, 90, 430, "Rich in learning", AL("rich", 2) - 0.1, "", 52), tag(S1, 90, 540, "Respected", AL("respected", 2) - 0.1, "", 52), tag(S1, 90, 650, "Attached to his rank", AL("rank", 2) - 0.4, "acc", 52)]
gone(t2, LS[3] - 0.4)
t3 = tag(S1, 90, 430, "Knocking in secret at Jesus' door", AL("secret", 3) - 0.4, "acc", 48)
gone([t3], LS[4] - 0.4)
t4 = [tag(S1, 90, 430, "Who is this man?", AL("Who", 4) - 0.1, "", 52), tag(S1, 90, 540, "Why at night?", AL("Why", 4) - 0.1, "", 52), tag(S1, 90, 650, "What happens to him?", AL("happens", 4) - 0.3, "acc", 52)]
gone(t4, LS[5] - 0.4)
t5 = [tag(S1, 90, 430, "A visit at night", AL("visit", 5) - 0.2, "", 52), tag(S1, 90, 540, "A sentence in the council", AL("council", 5) - 0.4, "", 50), tag(S1, 90, 650, "A burial", AL("burial", 5) - 0.3, "acc", 52)]
gone(t5, LS[6] - 0.4)
c6 = card(S1, 90, 420, "A portrait unique to John", "John 3 · John 7 · John 19", AL("John", 6, 1) - 0.3, w=900, size=52)
gone([c6], LS[7] - 0.4)
tag(S1, 90, 430, "Between the first scene and the last…", LS[7] + 0.3, "acc", 46)
tag(S1, 90, 540, "…something changes", E("changes", 7, 0.4, 3.0), "", 52)

# =====================================================================  S2 : le décor, qui est Nicodème (lignes 8-14)
t = LS[8] - 0.4
cam(t, S2)
headline(S2, 170, ["[Jerusalem], Passover"], t + 0.1, kicker="In the first century", hl_t=AL("Jerusalem", 8) + 0.05, size=104)
vi = S_(S2, "ville", 1450, 420, 300, LS[8] + 0.2, rot=2)
fade(vi, LS[11] - 0.4)
t9 = [tag(S2, 90, 430, "He drives out the temple merchants", AL("merchants", 9) - 0.3, "", 46), tag(S2, 90, 540, "He does signs", AL("signs", 9) - 0.3, "acc", 52)]
gone(t9, LS[10] - 0.4)
fo = S_(S2, "foule", 1100, 560, 300, AL("pilgrims", 10) - 0.3, rot=-2)
t10 = tag(S2, 90, 430, "Who is this Galilean?", AL("Galilean", 10) - 0.4, "acc", 52)
gone([t10, fo], LS[11] - 0.4)
S_(S2, "nicodeme-tete", 1500, 420, 190, E("Nicodemus", 11, 0.3, 0.3), rot=2)
c11 = card(S2, 90, 420, "John 3:1" + BIB, "“a man of the Pharisees, named Nicodemus, a ruler of the Jews”", E("Pharisees", 11, 0.5, 0.4), w=1000, size=40)
gone([c11], LS[12] - 0.4)
t12 = [tag(S2, 90, 430, "The Pharisees", AL("Pharisees", 12) - 0.2, "", 52), tag(S2, 90, 540, "The law of Moses, every day", AL("everyday", 12) - 0.8, "acc", 46)]
gone(t12, LS[13] - 0.4)
t13 = [tag(S2, 90, 430, "Ruler of the Jews", AL("Ruler", 13) - 0.1, "", 52), tag(S2, 90, 540, "The council: the Sanhedrin", AL("Sanhedrin", 13) - 0.4, "acc", 50), tag(S2, 90, 650, "A notable, cautious", AL("notable", 13) - 0.2, "", 50)]
gone(t13, LS[14] - 0.4)
c14 = card(S2, 90, 420, "A Greek name", "Nicodemus: “victor over the people”", AL("victor", 14) - 0.5, w=900, size=46)

# =====================================================================  S3 : pourquoi de nuit ? (lignes 15-21)
t = LS[15] - 0.4
cam(t, S3)
headline(S3, 170, ["Why [at night]?"], t + 0.1, kicker="John 3:2", hl_t=AL("night", 16) + 0.05, size=104)
t15 = tag(S3, 90, 430, "He comes to find Jesus", LS[15] + 0.2, "acc", 52)
gone([t15], LS[16] - 0.4)
t16 = tag(S3, 90, 430, "The text does not say", AL("say", 16) - 0.8, "", 56)
gone([t16], LS[17] - 0.4)
t17 = [tag(S3, 90, 430, "Fear of colleagues' gaze?", AL("feared", 17) - 0.3, "", 46), tag(S3, 90, 540, "A quiet conversation?", AL("quiet", 17) - 0.4, "", 46), tag(S3, 90, 650, "A symbol?", AL("symbol", 17) - 0.3, "acc", 50)]
gone(t17, LS[18] - 0.4)
sh = stamp(S3, 90, 440, "Hypotheses", AL("hypotheses", 18) - 0.4, rot=-3, size=70)
sn = S_(S3, "nicodeme", 1500, 420, 190, LS[18] + 0.3, rot=2)
gone([sh, sn], LS[19] - 0.4)
f19 = tag(S3, 90, 430, "In John: light and darkness", LS[19] + 0.3, "acc", 50)
kq3 = None
kq(S3, 90, 420, "John 1:5" + BIB, "“The light shines in the darkness, and the darkness hasn't overcome it.”", 19, "The", n=2, width=900, size=42, fade_at=LS[20] - 0.4)
f20 = tag(S3, 90, 430, "Judas leaves the table", LS[20] + 0.3, "", 52)
fade(f19, AL("The", 19, 2) - 0.3)
kq(S3, 90, 420, "John 13:30" + BIB, "“It was night.”", 20, "It", n=0, width=600, size=54, last=AL("night", 20) + 0.6, fade_at=AL("night", 20) + 1.2)
fade(f20, AL("It", 20) - 0.3)
tag(S3, 90, 660, "Night: a state of the heart?", min(AL("heart", 20) - 0.5, AL("night", 20) + 1.3), "acc", 46)

# =====================================================================  S4 : Rabbi (lignes 22-24)
t = LS[22] - 0.4
cam(t, S4)
headline(S4, 170, ["“[Rabbi], we know”"], t + 0.1, kicker="John 3:2", hl_t=AL("Rabbi", 22) + 0.05, size=100)
S_(S4, "christ-nicodeme-dessin", 1500, 420, 250, LS[22] + 0.4, rot=2)
kq(S4, 90, 420, "John 3:2" + BIB, "“Rabbi, we know that you are a teacher come from God, for no one can do these signs that you do, unless God is with him.”", 22, "Rabbi", width=950, size=36, fade_at=LS[23] - 0.4)
t23 = [tag(S4, 90, 430, "“We”: others with him", AL("we", 23) - 0.3, "acc", 50), tag(S4, 90, 540, "Impressed people, within the elite", AL("elite", 23) - 0.5, "", 44)]
gone(t23, LS[24] - 0.4)
t24 = [tag(S4, 90, 430, "Rabbi: “my teacher”", AL("teacher", 24) - 0.5, "", 52), tag(S4, 90, 540, "A notable before a craftsman", AL("craftsman", 24) - 0.4, "acc", 48)]

# =====================================================================  S5 : naître de nouveau (lignes 25-28)
t = LS[25] - 0.4
cam(t, S5)
headline(S5, 170, ["Born [anew]"], t + 0.1, kicker="John 3:3-4", hl_t=AL("anew", 25) + 0.05, size=104)
S_(S5, "jesus-pied", 1500, 420, 220, LS[25] + 0.3, rot=2)
kq(S5, 90, 420, "John 3:3" + BIB, "“Most certainly, I tell you, unless one is born anew, he can't see the Kingdom of God.”", 25, "Most", width=950, size=40, fade_at=LS[26] - 0.4)
c26 = put(S5, 90, 420, "<small>Greek word</small><span style=\'font-size:84px\'>ἄνωθεν</span> anôthen", "card", "width:900px;font-size:66px")
blur_in(c26, AL("anōthen", 26) - 0.3, 14)
t26 = [tag(S5, 90, 700, "“again”", AL("again", 26) - 0.3, "", 52), tag(S5, 560, 700, "“from above”", AL("above", 26) - 0.3, "acc", 52)]
gone([c26] + t26, LS[27] - 0.4)
kq(S5, 90, 420, "John 3:4" + BIB, "“How can a man be born when he is old? Can he enter a second time into his mother's womb, and be born?”", 27, "How", width=950, size=38, fade_at=LS[28] - 0.4)
t28 = [tag(S5, 90, 430, "He takes words seriously", AL("seriously", 28) - 0.4, "", 50), stamp(S5, 90, 620, "The word is ambiguous", AL("ambiguous", 28) - 0.3, rot=-3, size=64)]

# =====================================================================  S6 : eau, Esprit, vent (lignes 29-35)
t = LS[29] - 0.4
cam(t, S6)
headline(S6, 170, ["[The Spirit] and the wind"], t + 0.1, kicker="John 3:5-10", hl_t=AL("Spirit", 31) + 0.05, size=104)
kq(S6, 90, 420, "John 3:5" + BIB, "“Most certainly I tell you, unless one is born of water and spirit, he can't enter into the Kingdom of God.”", 29, "Most", width=950, size=40, fade_at=LS[30] - 0.4)
c30 = card(S6, 90, 420, "A birth", "received, like a gift, not earned", E("gift", 30, 0.6, 0.4), w=900, size=46)
gone([c30], LS[31] - 0.4)
kq(S6, 90, 420, "John 3:8" + BIB, "“The wind blows where it wants to, and you hear its sound, but don't know where it comes from and where it is going. So is everyone who is born of the Spirit.”", 31, "The", width=1000, size=36, fade_at=LS[32] - 0.4)
c32 = card(S6, 90, 420, "Greek word", "<b>pneuma</b>: wind · Spirit", AL("pneuma", 32) - 0.3, w=800, size=52)
t32 = tag(S6, 90, 640, "Like the Hebrew word ruach", AL("ruach", 32) - 0.5, "acc", 46)
gone([c32, t32], LS[33] - 0.4)
c33 = card(S6, 90, 420, "Nicodemus, bewildered", "“How can these things be?”", AL("How", 33) - 0.4, w=900, size=46)
gone([c33], LS[34] - 0.4)
f34 = tag(S6, 90, 430, "Jesus answers, with gentle irony", LS[34] + 0.3, "acc", 46)
fade(f34, AL("Are", 34) - 0.3)
kq(S6, 90, 420, "John 3:10" + BIB, "“Are you the teacher of Israel, and don't understand these things?”", 34, "Are", width=900, size=44, fade_at=LS[35] - 0.4)
stamp(S6, 90, 440, "A shock", AL("shock", 35) - 0.3, rot=-4, size=84)
tag(S6, 90, 640, "What he thought he mastered slips away", AL("slips", 35) - 0.8, "acc", 46)

# =====================================================================  S7 : le serpent, John 3:16 (lignes 36-39)
t = LS[36] - 0.4
cam(t, S7)
headline(S7, 170, ["The serpent [lifted up]"], t + 0.1, kicker="John 3:14-16 · Numbers 21", hl_t=AL("serpent", 36) + 0.05, size=104)
se = S_(S7, "serpent-airain", 1500, 420, 200, AL("serpent", 37) - 0.3, rot=2)
kq(S7, 90, 420, "John 3:14-15" + BIB, "“As Moses lifted up the serpent in the wilderness, even so must the Son of Man be lifted up, that whoever believes in him should not perish, but have eternal life.”", 36, "As", width=1000, size=36, fade_at=LS[37] - 0.4)
t37 = [tag(S7, 90, 430, "Numbers 21", AL("Numbers", 37) - 0.2, "", 52), tag(S7, 90, 540, "A bronze serpent on a pole", AL("pole", 37) - 0.8, "acc", 46)]
gone(t37, LS[38] - 0.4)
# (la voix EN ne lit pas Jean 3:16 : carte retirée)
tag(S7, 90, 430, "Where do Jesus' words end?", AL("end", 39) - 0.4, "", 48)
tag(S7, 90, 540, "The general meaning stays the same", AL("meaning", 39) - 0.3, "acc", 48)

# =====================================================================  S8 : le silence (lignes 40-42)
t = LS[40] - 0.4
cam(t, S8)
headline(S8, 170, ["A [silence]"], t + 0.1, kicker="End of the scene", hl_t=AL("Nothing", 40) + 0.05, size=110)
t40 = [tag(S8, 90, 430, "He doesn't say he believes", E("believes", 40, 0.3, 0.5), "", 50), tag(S8, 90, 540, "Nor that he refuses", AL("refuses", 40) - 0.3, "", 50), tag(S8, 90, 650, "Nor that he leaves", AL("leaves", 40) - 0.3, "acc", 50)]
gone(t40, LS[41] - 0.4)
t41 = [stamp(S8, 90, 440, "No conversion", E("conversion", 41, 0.5, 0.4), rot=-3, size=70), tag(S8, 90, 650, "It ends with a silence", AL("silence", 41) - 0.5, "acc", 50)]
gone(t41, LS[42] - 0.4)
tag(S8, 90, 430, "Months, perhaps years", E("years", 42, 0.8, 0.4), "", 50)

# =====================================================================  S9 : Jean 7, la défense (lignes 43-53)
t = LS[43] - 0.4
cam(t, S9)
headline(S9, 170, ["He [speaks up]"], t + 0.1, kicker="John 7 · the festival of Tabernacles", hl_t=AL("Nicodemus", 46) + 0.05, size=104)
t43 = tag(S9, 90, 430, "John 7 · the festival of Tabernacles", LS[43] + 0.3, "acc", 52)
gone([t43], LS[44] - 0.4)
lv = S_(S9, "levite", 1500, 420, 190, AL("guards", 44) - 0.3, rot=2)
kq(S9, 90, 420, "John 7:46" + BIB, "“No man ever spoke like this man!”", 44, "No", width=900, size=48, fade_at=LS[45] - 0.4)
fade(lv, LS[45] - 0.4)
pr = S_(S9, "pretre", 1500, 420, 180, LS[45] + 0.3, rot=-2)
kq(S9, 90, 420, "John 7:49" + BIB, "“But this multitude that doesn't know the law is accursed.”", 45, "But", width=900, size=42, fade_at=LS[46] - 0.4)
fade(pr, LS[46] - 0.4)
S_(S9, "nicodeme", 1500, 420, 190, LS[46] + 0.3, rot=2)
kq(S9, 90, 420, "John 7:50" + BIB, "“Nicodemus (he who came to him by night, being one of them)”", 46, "Nicodemus", width=950, size=38, fade_at=LS[47] - 0.4)
kq(S9, 90, 420, "John 7:51" + BIB, "“Does our law judge a man, unless it first hears from him and knows what he does?”", 47, "Does", width=950, size=40, fade_at=LS[48] - 0.4)
t48 = [tag(S9, 90, 430, "Not yet a declaration of faith", AL("declaration", 48) - 0.4, "", 46), tag(S9, 90, 540, "A principle: listen before judging", AL("principle", 48) - 0.4, "acc", 46)]
gone(t48, LS[49] - 0.4)
t49 = [tag(S9, 90, 430, "In front of his colleagues", AL("colleagues", 49) - 0.3, "", 52), stamp(S9, 90, 620, "A courageous act", AL("courageous", 49) - 0.8, rot=-3, size=64)]
gone(t49, LS[50] - 0.4)
kq(S9, 90, 420, "John 7:52" + BIB, "“Are you also from Galilee? Search, and see that no prophet has arisen out of Galilee.”", 50, "Are", width=950, size=40, fade_at=LS[51] - 0.4)
t51 = tag(S9, 90, 430, "The price of speaking: contempt", AL("contempt", 51) - 0.8, "acc", 50)
gone([t51], LS[52] - 0.4)
t52 = [tag(S9, 90, 430, "2 Kings: Jonah, from Gath Hepher", AL("Jonah", 52) - 0.5, "", 48), tag(S9, 90, 540, "In Galilee", AL("Galilee", 52) - 0.3, "acc", 52)]
gone(t52, LS[53] - 0.4)
tag(S9, 90, 430, "The meeting is adjourned", AL("meeting", 53) - 0.3, "", 52)
tag(S9, 90, 540, "But he has spoken", AL("spoken", 53) - 0.4, "acc", 56)

# =====================================================================  S10 : de la nuit au jour (lignes 54-55)
t = LS[54] - 0.4
cam(t, S10)
headline(S10, 170, ["From night to [day]"], t + 0.1, kicker="First change", hl_t=AL("day", 54) + 0.05, size=104)
t54 = [tag(S10, 90, 430, "No longer only a discreet visitor", E("discreet", 54, 0.5, 0.4), "", 46), tag(S10, 90, 540, "He defends a man others want to condemn", AL("defends", 54) if False else AL("condemn", 54) - 0.6, "acc", 44)]
gone(t54, LS[55] - 0.4)
stamp(S10, 90, 440, "The most risky", E("risky", 55, 0.5, 0.4), rot=-3, size=76)

# =====================================================================  S11 : John 19, les aromates (lignes 56-62)
t = LS[56] - 0.4
cam(t, S11)
headline(S11, 170, ["At the foot of [the cross]"], t + 0.1, kicker="John 19", hl_t=AL("cross", 63) if False else AL("nineteen", 56) + 0.05, size=104)
t56 = [tag(S11, 90, 430, "Chapter nineteen", LS[56] + 0.3, "", 52), tag(S11, 90, 540, "Jesus crucified under Pontius Pilate", AL("Pilate", 56) - 0.5, "", 46), tag(S11, 90, 650, "The disciples scattered", AL("scattered", 56) - 0.4, "acc", 50)]
gone(t56, LS[57] - 0.4)
f57 = tag(S11, 90, 430, "Joseph of Arimathea", LS[57] + 0.3, "acc", 52)
fade(f57, AL("disciple", 57) - 0.4)
jo = S_(S11, "pere", 1500, 420, 190, AL("Joseph", 57) - 0.3, rot=2)
kq(S11, 90, 420, "John 19:38" + BIB, "“a disciple of Jesus, but secretly for fear of the Jews”", 57, "disciple", width=900, size=44, fade_at=LS[58] - 0.4)
t58 = [tag(S11, 90, 430, "Joseph: fear, stated by the text", AL("afraid", 58) - 0.4, "", 46), tag(S11, 90, 540, "Nicodemus: not a word about fear", AL("Nicodemus", 58) - 0.3, "acc", 46)]
gone(t58, LS[59] - 0.4)
fade(jo, LS[59] - 0.4)
S_(S11, "nicodeme", 1500, 420, 190, LS[59] + 0.3, rot=2)
kq(S11, 90, 420, "John 19:39" + BIB, "“Nicodemus, who at first came to him by night, also came, bringing a mixture of myrrh and aloes, about a hundred pounds.”", 59, "Nicodemus", width=1000, size=36, fade_at=LS[60] - 0.4)
c60 = card(S11, 90, 420, "A hundred Roman pounds", "about 30 kilos of perfumes and spices", AL("thirty", 60) - 0.6, w=900, size=44)
gone([c60], LS[61] - 0.4)
t61 = [tag(S11, 90, 430, "Two men, two possible fears", AL("fears", 61) - 0.5, "", 46), tag(S11, 90, 540, "The same gesture, together", AL("same", 61) - 0.4, "acc", 52)]
gone(t61, LS[62] - 0.4)
tag(S11, 90, 430, "A royal funeral? A common interpretation", AL("interpretation", 62) - 0.8, "", 42)
tag(S11, 90, 540, "Not a certainty", AL("certainty", 62) - 0.4, "acc", 52)

# =====================================================================  S12 : au grand jour (lignes 63-70)
t = LS[63] - 0.4
cam(t, S12)
headline(S12, 170, ["In [broad daylight]"], t + 0.1, kicker="John 19:39-42", hl_t=AL("scene", 63) + 0.05, size=108)
tomb = S_(S12, "mise-au-tombeau-relief", 1100, 420, 330, AL("Picture", 63) - 0.2, rot=-2)
fade(tomb, LS[66] - 0.4)
t63 = [tag(S12, 90, 430, "A member of the Sanhedrin", AL("Sanhedrin", 63) - 0.4, "", 52), tag(S12, 90, 540, "A rich man, a notable", AL("notable", 63) - 0.4, "", 50), tag(S12, 90, 650, "Takes care of his body", AL("body", 63) - 0.4, "acc", 52)]
gone(t63, LS[64] - 0.4)
t64 = tag(S12, 90, 430, "Risking his reputation, his position…", AL("reputation", 64) - 0.5, "acc", 48)
gone([t64], LS[65] - 0.4)
t65 = [tag(S12, 90, 430, "Linen cloths and spices", AL("spices", 65) - 0.4, "", 50), tag(S12, 90, 540, "A new tomb, in a garden", AL("garden", 65) - 0.5, "acc", 48)]
gone(t65, LS[66] - 0.4)
s66 = stamp(S12, 90, 440, "From night to broad daylight", E("broad", 66, 0.4, 0.4), rot=-3, size=62)
gone([s66], LS[67] - 0.4)
c67 = card(S12, 90, 420, "John 19:39", "“who at first came by night”", E("expression", 67, 0.3, 0.4), w=900, size=44)
gone([c67], LS[68] - 0.4)
t68 = [tag(S12, 90, 430, "Never written: “became a disciple”", E("disciple", 68, 0.5, 0.4), "", 46), tag(S12, 90, 540, "Acts does not mention him", AL("Acts", 68) - 0.3, "acc", 46)]
gone(t68, LS[69] - 0.4)
c69 = [card(S12, 90, 420, "Tradition", "Regarded him as a believer", AL("tradition", 69) - 0.2, w=900, size=44), stamp(S12, 90, 680, "Late apocryphal text · not the Bible", AL("apocryphal", 69) - 0.3, rot=-3, size=50)]
gone(c69, LS[70] - 0.4)
tag(S12, 90, 430, "A night", E("night", 70, 0.3, 0.4), "", 56)
tag(S12, 90, 540, "A word", AL("word", 70) - 0.3, "", 56)
tag(S12, 90, 650, "A gesture", AL("gesture", 70) - 0.3, "acc", 56)

# =====================================================================  S13 : pour toi (lignes 71-79)
t = LS[71] - 0.4
cam(t, S13)
headline(S13, 170, ["What this story [says]"], t + 0.1, kicker="Application", hl_t=AL("tell", 71) + 0.05, size=96)
t71 = [tag(S13, 90, 430, "Approach Jesus with your doubts", E("doubts", 71, 0.6, 0.4), "", 46), tag(S13, 90, 540, "He leaves with a riddle", AL("riddle", 71) - 0.4, "", 48), tag(S13, 90, 650, "Jesus does not drive him away", AL("drive", 71) - 0.3, "acc", 50)]
gone(t71, LS[72] - 0.4)
t72 = [tag(S13, 90, 430, "Faith can be slow", AL("slow", 72) - 0.3, "", 52), tag(S13, 90, 540, "A visit · a defense · an act", AL("stages", 72) - 0.6, "acc", 46)]
gone(t72, LS[73] - 0.4)
t73 = tag(S13, 90, 430, "Courage grows in small steps", E("small", 73, 0.5, 0.4), "acc", 48)
gone([t73], LS[74] - 0.4)
t74 = [tag(S13, 90, 430, "It does not judge those who move in the shadows", AL("shadows", 74) - 0.7, "", 44), tag(S13, 90, 540, "It does not leave them where they are", AL("leave", 74) - 0.3, "acc", 46)]
gone(t74, LS[75] - 0.4)
t75 = [tag(S13, 90, 430, "Fear of other people's gaze", E("gaze", 75, 0.3, 0.4), "", 50), tag(S13, 90, 540, "Someone you trust", AL("trust", 75) - 0.3, "", 50), tag(S13, 90, 650, "Or a professional", AL("professional", 75) - 0.3, "acc", 50)]
gone(t75, LS[76] - 0.4)
tq = tag(S13, 90, 430, "What small step this week?", LS[76] + 0.4, "acc", 52)
cta = put(S13, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Tell us in the comments', "cta")
blur_in(cta, AL("comments", 76) - 1.0, 14)
sfx("click", AL("comments", 76) - 1.0, 0.8)
gone([tq, cta], LS[77] - 0.3)
S_(S13, "veilleur", 1500, 420, 200, LS[77] + 0.3, rot=2)
t77 = tag(S13, 90, 430, "Nicodemus' night", AL("night", 77) - 0.3, "", 56)
gone([t77], LS[78] - 0.4)
t78 = [tag(S13, 90, 430, "Spices, in front of everyone", AL("spices", 78) - 0.3, "", 52), tag(S13, 90, 540, "Fear gave way, little by little", AL("gave", 78) - 0.3, "acc", 52)]

t_end = AL("Every", 79) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(AL("Every", 79) - 0.8, DUR_)]
build(
    chapters=[("01", "The night", 0, LS[22]), ("02", "The conversation", LS[22], LS[43]), ("03", "The council and the cross", LS[43], LS[71]), ("04", "For you", LS[71], DUR_)],
    suppress=supp,
    endcard={"kicker": "Every week", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("nicodeme", 150, 560, 280, -6), ("jesus-portrait", 1550, 330, 230, 5)]},
    endcard_t=AL("Every", 79) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
