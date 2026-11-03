"""Long video "Every healing of Jesus, sorted by type of illness" (Faith Engineering) — style 02, 16:9. English version of montage/video-guerisons/.

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

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - The healings of Jesus - style 02", "lang": "en",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
DUR_ = 666.5
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
WEB = " · World English Bible"

# S1: the door at Capernaum (lines 1-9)
cam(0, S1)
headline(S1, 170, ["A whole city at [one door]"], 0.0, kicker="Mark 1.32-33", hl_t=AL("door", 1) + 0.05, size=92)
f0 = S_(S1, "foule", 1100, 420, 330, 0.0, rot=-3, instant=True)
fade(f0, AL("at", 3) - 0.7)
f3 = tag(S1, 90, 430, "Mark tells the scene", LS[3] + 0.2, "acc", 52)
fade(f3, AL("at", 3) - 0.7)
t2 = [tag(S1, 90, 430, "Capernaum", AL("capernaum", 2) - 0.2, "", 52), tag(S1, 90, 540, "The Sea of Galilee", AL("galilee", 2) - 0.2, "", 52)]
gone(t2, LS[3] - 0.5)
kq(S1, 90, 420, "Mark 1.32-33" + WEB,
   "“At evening, when the sun had set, they brought to him all who were sick, and those who were possessed by demons. All the city was gathered together at the door.”",
   3, "at", width=900, size=36, fade_at=LS[4] - 0.4)
S_(S1, "jesus-pied", 1500, 420, 210, AL("door", 3) - 0.5, rot=2)
t4 = tag(S1, 90, 430, "Jesus heals… many", AL("many", 4) - 0.8, "acc", 52)
gone([t4], LS[5] - 0.5)
s5 = stamp(S1, 90, 440, "How many?", AL("many", 5) - 0.6, rot=-4, size=84)
gone([s5], LS[6] - 0.5)
c6 = counter(S1, 90, 420, 0, 20, AL("twenty", 6) - 1.6, 2.4, unit=" accounts", size=130)
t6 = tag(S1, 90, 640, "The text gives no total", AL("total", 6) - 1.0, "acc", 44)
gone([c6, t6], LS[7] - 0.5)
t7 = [tag(S1, 90, 430, "The skin", AL("skin", 7) - 0.2, "", 42), tag(S1, 90, 530, "The eyes", AL("eyes", 7) - 0.2, "", 42),
      tag(S1, 90, 630, "Ears and speech", AL("ears", 7) - 0.2, "", 42), tag(S1, 90, 730, "Movement", AL("movement", 7) - 0.2, "", 42),
      tag(S1, 800, 430, "Fever and blood", AL("fever", 7) - 0.2, "", 42), tag(S1, 800, 530, "Spirits", AL("spirits", 7) - 0.2, "", 42),
      tag(S1, 800, 630, "Death", AL("death", 7) - 0.2, "acc", 42)]
s8 = stamp(S1, 700, 760, "The gestures vary", AL("gestures", 8) - 0.6, rot=-3, size=44)
gone(t7 + [s8], LS[9] - 0.5)
c9 = card(S1, 90, 420, "The method", "One account = one person healed, with their story", AL("method", 9) - 0.3, w=900, size=38)
t9 = tag(S1, 90, 700, "Crowds healed all at once: summaries", AL("crowds", 9) - 0.2, "", 42)
gone([c9, t9], LS[10] - 0.5)

# S2: the skin (lines 10-18)
t = LS[10] - 0.4
cam(t, S2)
headline(S2, 170, ["The [skin]"], t + 0.1, kicker="Leprosy", hl_t=AL("skin", 10) + 0.05, size=110)
t10 = tag(S2, 90, 430, "The most feared of the time", AL("feared", 10) - 0.4, "acc", 52)
gone([t10], LS[11] - 0.5)
c11 = card(S2, 90, 420, "The Greek word", "<b>lepra</b>: a range of skin conditions", AL("lepra", 11) - 0.3, w=900, size=40)
t11 = [tag(S2, 90, 640, "Leviticus 13", AL("leviticus", 11) - 0.2, "", 46), tag(S2, 90, 750, "Not necessarily today's leprosy", AL("necessarily", 11) - 0.5, "acc", 38)]
gone([c11] + t11, LS[12] - 0.5)
f12 = tag(S2, 90, 430, "The sick person lives apart", LS[12] + 0.2, "", 50)
fade(f12, AL("unclean", 12) - 0.7)
s12 = stamp(S2, 90, 440, "Unclean!", AL("unclean", 12) - 0.1, rot=-4, size=84)
t12 = tag(S2, 90, 640, "An exclusion as much as an illness", AL("exclusion", 12) - 0.6, "acc", 46)
S_(S2, "lepreux", 1500, 420, 170, AL("illness", 12) - 0.3, rot=-2)
gone([s12, t12], LS[13] - 0.5)
kq(S2, 90, 420, "Mark 1.40" + WEB, "“If you want to, you can make me clean.”", 13, "if", width=900, size=44, fade_at=LS[14] - 0.4)
c14 = card(S2, 90, 420, "Mark 1.41", "“moved with compassion”", AL("compassion", 14) - 0.5, w=800, size=44)
t14 = [tag(S2, 90, 620, "Some manuscripts: “angry”", AL("angry", 14) - 0.4, "", 40), tag(S2, 90, 730, "Specialists debate it", AL("debate", 14) - 0.6, "acc", 40)]
gone([c14] + t14, LS[15] - 0.5)
s15 = stamp(S2, 90, 440, "He touches him", AL("touching", 15) - 0.1, rot=-4, size=72)
fade(s15, AL("priest", 15) - 1.4)
c15 = card(S2, 90, 620, "He says", "“I want to. Be made clean.”", AL("want", 15) - 0.4, w=800, size=44, accent=True)
t15 = tag(S2, 90, 440, "Go show yourself to the priest", AL("priest", 15) - 0.8, "", 46)
gone([c15, t15], LS[16] - 0.5)
c16 = card(S2, 90, 420, "Luke 17", "Ten lepers, calling from afar: cleansed on the way", AL("ten", 16) - 0.2, w=900, size=38)
t16 = tag(S2, 90, 650, "Jesus does not touch them", AL("touch", 16) - 0.3, "", 46)
gone([c16, t16], LS[17] - 0.5)
S_(S2, "samaritain", 1100, 420, 260, AL("samaritan", 17) - 0.8, rot=2)
t17 = [tag(S2, 90, 430, "Only one comes back", AL("back", 17) - 0.3, "", 52), tag(S2, 90, 540, "A Samaritan, a foreigner", AL("samaritan", 17) - 0.6, "acc", 50)]
gone(t17, LS[18] - 0.5)
teaser(S2, 90, 440, "The rest, in the same vein", LS[18] + 0.3, hold=4.4)

# S3: sight (lines 19-24)
t = LS[19] - 0.4
cam(t, S3)
headline(S3, 170, ["[Sight]"], t + 0.1, kicker="Second category", hl_t=AL("sight", 19) + 0.05, size=110)
t19 = tag(S3, 90, 430, "One of the most frequent", AL("frequent", 19) - 0.6, "acc", 52)
gone([t19], LS[20] - 0.5)
jr = S_(S3, "jericho", 1100, 420, 380, AL("jericho", 20) - 0.2, rot=2)
fade(jr, LS[21] - 0.5)
kq(S3, 90, 420, "Mark 10.47 · Bartimaeus at Jericho", "“Jesus, you son of David, have mercy on me!”", 20, "jesus", width=800, size=40, fade_at=LS[21] - 0.4)
t20 = [tag(S3, 90, 700, "The crowd tells him to be quiet", AL("quiet", 20) - 0.8, "", 44), tag(S3, 90, 800, "He cries out louder", AL("louder", 20) - 0.4, "acc", 46)]
gone(t20, LS[21] - 0.5)
S_(S3, "bartimee", 1500, 420, 190, AL("cloak", 21) - 0.4, rot=-2)
t21 = [tag(S3, 90, 430, "He throws off his cloak", AL("cloak", 21) - 0.4, "", 52), stamp(S3, 90, 580, "To see", AL("see", 21) - 0.4, rot=-4, size=96)]
S_(S3, "bartimee-portrait", 1100, 420, 280, AL("see", 21) - 0.3, rot=2)
gone(t21, LS[22] - 0.5)
kq(S3, 90, 420, "Mark 10.52" + WEB, "“Go your way. Your faith has made you well.”", 22, "go", width=800, size=44, fade_at=LS[23] - 0.4)
c22 = card(S3, 90, 690, "Greek", "<b>sozo</b>: to save and to heal", AL("sozo", 22) - 0.3, w=800, size=40)
gone([c22], LS[23] - 0.5)
t23 = tag(S3, 90, 430, "Bethsaida: in two stages", AL("bethsaida", 23) - 0.3, "acc", 50)
fade(t23, AL("see", 23) - 0.7)
c23 = card(S3, 90, 420, "Mark 8.24", "“I see men; for I see them like trees walking.”", AL("see", 23) - 0.4, w=800, size=40)
gone([c23], LS[24] - 0.5)
t24 = tag(S3, 90, 430, "A healing in stages", AL("stages", 24) - 0.9, "acc", 56)
gone([t24], LS[25] - 0.5)

# S4: the man born blind (lines 25-27)
t = LS[25] - 0.4
cam(t, S4)
headline(S4, 170, ["The man born [blind]"], t + 0.1, kicker="John 9", hl_t=AL("born", 25) + 0.05, size=96)
elg = S_(S4, "el-greco-aveugle", 1100, 420, 470, AL("born", 25) + 0.2, rot=2)
fade(elg, LS[26] - 0.5)
c25 = card(S4, 90, 420, "The disciples ask", "Who sinned, this man or his parents?", AL("sinned", 25) - 0.8, w=800, size=40)
s25 = stamp(S4, 90, 620, "Neither", AL("neither", 25) - 0.3, rot=-3, size=72)
gone([c25, s25], LS[26] - 0.5)
t26 = [tag(S4, 90, 430, "Mud, saliva", AL("mud", 26) - 0.3, "", 48), tag(S4, 90, 540, "The pool of Siloam", AL("siloam", 26) - 0.3, "acc", 48),
       tag(S4, 90, 650, "Siloam: “sent”", AL("sent", 26) - 0.6, "", 48)]
S_(S4, "siloe", 1100, 420, 430, AL("siloam", 26) - 0.3, rot=-2)
gone(t26, LS[27] - 0.5)
c27 = card(S4, 90, 420, "His one answer", "“though I was blind, now I see”", AL("repeats", 27) - 0.3, w=800, size=44)
t27 = tag(S4, 90, 700, "His parents stay silent", AL("parents", 27) - 0.3, "", 44)

# S5: hearing and speech (lines 28-32)
t = LS[28] - 0.4
cam(t, S5)
headline(S5, 170, ["[Hearing] and speech"], t + 0.1, kicker="Third category", hl_t=AL("hearing", 28) + 0.05, size=96)
t28 = tag(S5, 90, 430, "Hearing, speaking", AL("speech", 28) - 0.6, "acc", 52)
gone([t28], LS[29] - 0.5)
S_(S5, "villageois", 1500, 420, 250, AL("deaf", 29) - 0.3, rot=2)
t29 = [tag(S5, 90, 430, "The Decapolis", AL("decapolis", 29) - 0.3, "", 52), tag(S5, 90, 540, "Aside, away from the crowd", AL("aside", 29) - 0.3, "", 46),
       tag(S5, 90, 650, "Fingers, saliva, a sigh", AL("saliva", 29) - 0.3, "acc", 46)]
gone(t29, LS[30] - 0.5)
c30 = card(S5, 90, 420, "An Aramaic word", "<b>Ephphatha</b>: “Be opened”", AL("ephphatha", 30) - 0.6, w=800, size=48)
burst(S5, 1000, 520, AL("ephphatha", 30) - 0.2)
gone([c30], LS[31] - 0.5)
kq(S5, 90, 420, "Mark 7.37" + WEB, "“He has done all things well. He makes even the deaf hear, and the mute speak.”", 31, "has", width=900, size=42, fade_at=LS[32] - 0.4)
tag(S5, 90, 430, "A mute man", AL("mute", 32) - 0.3, "", 52)
tag(S5, 90, 540, "An evil spirit, driven out", AL("spirit", 32) - 0.3, "", 46)
tag(S5, 90, 650, "He speaks", AL("speaks", 32) - 0.3, "acc", 52)

# S6: movement (lines 33-39)
t = LS[33] - 0.4
cam(t, S6)
headline(S6, 170, ["[Movement]"], t + 0.1, kicker="Fourth category", hl_t=AL("movement", 33) + 0.05, size=104)
f33 = tag(S6, 90, 430, "Paralyzed · hands · backs", LS[33] + 0.4, "acc", 52)
fade(f33, LS[34] - 0.5)
p34 = S_(S6, "porteurs", 90, 420, 480, AL("four", 34) - 0.3, rot=-2)
t34 = [tag(S6, 700, 430, "Four men", AL("four", 34) - 0.3, "", 50), tag(S6, 700, 540, "The roof opened", AL("roof", 34) - 0.3, "acc", 50)]
gone([p34] + t34, LS[35] - 0.5)
pd = S_(S6, "paralytique-dessin", 1100, 420, 420, AL("faith", 35) - 0.3, rot=2)
fade(pd, LS[36] - 0.5)
kq(S6, 90, 420, "Mark 2.5" + WEB, "“Son, your sins are forgiven you.”", 35, "son", width=800, size=44, fade_at=LS[36] - 0.4)
t35 = [tag(S6, 90, 700, "Some scribes are outraged", AL("scribes", 35) - 0.3, "", 44), tag(S6, 90, 800, "He orders: get up", AL("orders", 35) - 0.3, "acc", 44)]
gone(t35, LS[36] - 0.5)
c36 = card(S6, 90, 420, "Bethesda · John 5", "Sick for thirty-eight years", AL("thirty-eight", 36) - 0.6, w=800, size=44)
t36 = tag(S6, 90, 620, "“Do you want to be made well?”", AL("do", 36) - 0.3, "acc", 52)
bd = S_(S6, "bethesda-dessin", 1100, 420, 420, AL("bethesda", 36) - 0.5, rot=-2)
fade(bd, LS[38] - 0.5)
gone([c36, t36], LS[37] - 0.5)
t37 = [tag(S6, 90, 430, "A crowd of sick people", AL("crowd", 37) - 0.3, "", 52), tag(S6, 90, 540, "Only one healed in this account", AL("only", 37) - 0.3, "acc", 46)]
gone(t37, LS[38] - 0.5)
f38 = tag(S6, 90, 430, "A withered hand", LS[38] + 0.2, "acc", 52)
fade(f38, AL("stretch", 38) - 1.2)
c38 = card(S6, 90, 420, "On a Sabbath", "“Stretch out your hand”", AL("stretch", 38) - 0.8, w=800, size=48)
t38 = tag(S6, 90, 620, "And the debate begins", AL("debate", 38) - 0.3, "", 44)
gone([c38, t38], LS[39] - 0.5)
S_(S6, "femme-courbee", 1500, 420, 215, AL("bent", 39) - 0.3, rot=2)
tag(S6, 90, 430, "Eighteen years", AL("eighteen", 39) - 0.3, "", 56)
tag(S6, 90, 540, "“A daughter of Abraham”", AL("daughter", 39) - 0.4, "acc", 52)
tag(S6, 90, 650, "She stands up straight", AL("stands", 39) - 0.3, "", 48)

# S7: fever and blood (lines 40-46)
t = LS[40] - 0.4
cam(t, S7)
headline(S7, 170, ["[Fever] and blood"], t + 0.1, kicker="Fifth category", hl_t=AL("fever", 40) + 0.05, size=96)
f40 = tag(S7, 90, 430, "Fever and blood", LS[40] + 0.3, "acc", 52)
fade(f40, LS[41] - 0.5)
t41 = [tag(S7, 90, 430, "Peter's mother-in-law", AL("mother-in-law", 41) - 0.3, "", 50), tag(S7, 90, 540, "He takes her by the hand", AL("hand", 41) - 0.3, "", 46),
       tag(S7, 90, 650, "She begins to serve them", AL("serve", 41) - 0.5, "acc", 46)]
gone(t41, LS[42] - 0.5)
f42 = [tag(S7, 90, 430, "A royal official", LS[42] + 0.3, "", 52), tag(S7, 90, 540, "His son is dying", AL("dying", 42) - 0.4, "", 50)]
gone(f42, AL("go", 42) - 0.8)
kq(S7, 90, 420, "John 4.50" + WEB, "“Go your way. Your son lives.”", 42, "go", width=700, size=48, fade_at=LS[43] - 0.4)
t42 = tag(S7, 90, 700, "From a distance: the same hour", AL("hour", 42) - 0.5, "acc", 44)
gone([t42], LS[43] - 0.5)
ce = S_(S7, "centurion", 1500, 420, 190, AL("centurion", 43) - 0.3, rot=2)
t43 = [tag(S7, 90, 430, "A Roman centurion", AL("centurion", 43) - 0.3, "", 50), tag(S7, 90, 540, "A word is enough", AL("enough", 43) - 0.4, "acc", 52),
       tag(S7, 90, 650, "Healed from a distance", AL("distance", 43) - 0.3, "", 48)]
gone([ce] + t43, LS[44] - 0.5)
S_(S7, "femme-sang", 1100, 420, 380, AL("bleeding", 44) - 0.2, rot=-2)
t44 = [tag(S7, 90, 430, "Twelve years", AL("twelve", 44) - 0.3, "", 56), tag(S7, 90, 540, "No relief", AL("relief", 44) - 0.8, "acc", 44)]
pr = S_(S7, "pince-romaine", 90, 660, 330, AL("doctors", 44) - 0.3, rot=-3)
gone(t44 + [pr], LS[45] - 0.5)
c45 = card(S7, 90, 420, "She says to herself", "“If I just touch his clothes, I will be healed.”", AL("touch", 45) - 1.0, w=800, size=36)
t45a = tag(S7, 90, 700, "The bleeding stops", AL("bleeding", 45) - 0.3, "acc", 50)
fade(t45a, AL("who", 45) - 0.7)
t45 = [t45a, tag(S7, 90, 700, "“Who touched my clothes?”", AL("who", 45) - 0.3, "", 42)]
gone([c45] + t45, LS[46] - 0.5)
kq(S7, 90, 420, "Mark 5.34" + WEB, "“Daughter, your faith has made you well. Go in peace, and be cured of your disease.”", 46, "your", width=800, size=40, fade_at=LS[47] - 0.4)

# S8: spirits (lines 47-52)
t = LS[47] - 0.4
cam(t, S8)
headline(S8, 170, ["The [spirits]"], t + 0.1, kicker="Sixth category", hl_t=AL("spirits", 47) + 0.05, size=104)
f47 = tag(S8, 90, 430, "Unclean spirits", LS[47] + 0.3, "acc", 52)
fade(f47, AL("casting", 47) - 0.9)
t47 = [tag(S8, 90, 430, "Illness or unclean spirit", AL("casting", 47) - 0.6, "", 52), tag(S8, 90, 540, "Often distinguished", AL("distinguish", 47) - 0.3, "acc", 52)]
gone(t47, LS[48] - 0.5)
f48 = tag(S8, 90, 430, "An old debate", LS[48] + 0.3, "", 52)
fade(f48, AL("diagnosis", 48) - 1.3)
c48 = card(S8, 90, 420, "Specialists discuss it", "No medical diagnosis in the text", AL("diagnosis", 48) - 0.9, w=900, size=40)
s48 = stamp(S8, 90, 640, "No diagnosis", AL("diagnosis", 48) - 0.3, rot=-3, size=60)
gone([c48, s48], LS[49] - 0.5)
S_(S8, "jesus-pied", 1500, 420, 210, AL("synagogue", 49) - 0.3, rot=2)
kq(S8, 90, 420, "Mark 1.24" + WEB, "“I know who you are: the Holy One of God!”", 49, "know", width=900, size=44, fade_at=LS[50] - 0.4)
t49 = [tag(S8, 90, 700, "He orders it out", AL("orders", 49) - 0.3, "", 44), tag(S8, 90, 800, "He speaks with authority", AL("authority", 49) - 0.6, "acc", 44)]
gone(t49, LS[50] - 0.5)
t50 = [tag(S8, 90, 430, "The country of the Gadarenes", AL("gadarenes", 50) - 0.3, "", 50), tag(S8, 90, 540, "Among the tombs", AL("tombs", 50) - 0.3, "", 48),
       tag(S8, 90, 650, "Sitting, clothed, in his right mind", AL("mind", 50) - 0.8, "acc", 44)]
gone(t50, LS[51] - 0.5)
pf = S_(S8, "pere-fils", 1100, 420, 165, AL("father", 51) - 0.3, rot=-2)
kq(S8, 90, 420, "Mark 9.23" + WEB, "“All things are possible to him who believes.”", 51, "all", width=800, size=42, fade_at=LS[52] - 0.4)
c51 = card(S8, 90, 690, "The father answers", "“I believe. Help my unbelief!”", AL("unbelief", 51) - 0.8, w=800, size=36)
gone([pf, c51], LS[52] - 0.5)
t52 = [tag(S8, 90, 430, "A Canaanite mother", AL("canaanite", 52) - 0.3, "", 52), tag(S8, 90, 540, "A foreigner", AL("foreigner", 52) - 0.3, "", 48)]
kq(S8, 90, 650, "Matthew 15.28" + WEB, "“Woman, great is your faith!”", 52, "woman", width=800, size=44)

# S9: death (lines 53-57)
t = LS[53] - 0.4
cam(t, S9)
headline(S9, 170, ["[Death]"], t + 0.1, kicker="Last category", hl_t=AL("death", 53) + 0.05, size=110)
t53 = tag(S9, 90, 430, "Three times, he gives life back", LS[53] + 0.3, "acc", 52)
gone([t53], LS[54] - 0.5)
fj = S_(S9, "fille-jairus", 1500, 420, 150, AL("daughter", 54) - 0.3, rot=2)
t54 = tag(S9, 90, 430, "Jairus's daughter · twelve", AL("daughter", 54) - 0.3, "", 52)
c54 = card(S9, 90, 560, "In Aramaic", "<b>Talitha koumi</b>: “Girl, get up”", AL("talitha", 54) - 0.3, w=800, size=40)
gone([fj, t54, c54], LS[55] - 0.5)
vc = S_(S9, "veuve-cortege", 90, 420, 520, AL("nain", 55) - 0.3, rot=-2)
t55 = [tag(S9, 760, 430, "Nain", AL("nain", 55) - 0.3, "", 52), tag(S9, 760, 540, "A widow's only son", AL("only", 55) - 0.3, "", 46),
       tag(S9, 760, 650, "“Arise”", AL("arise", 55) - 0.3, "acc", 52)]
gone([vc] + t55, LS[56] - 0.5)
lz = S_(S9, "lazare", 1500, 420, 220, AL("lazarus", 56) - 0.3, rot=2)
lg = S_(S9, "lazare-gravure", 1000, 420, 400, AL("lazarus", 56) - 0.2, rot=-2)
t56 = [tag(S9, 90, 430, "Dead four days", AL("four", 56) - 0.3, "", 50), tag(S9, 90, 540, "Jesus weeps", AL("weeps", 56) - 0.3, "", 52),
       tag(S9, 90, 650, "“Lazarus, come out!”", AL("come", 56) - 0.4, "acc", 52)]
gone([lg] + t56, LS[57] - 0.5)
c57 = card(S9, 90, 420, "Christian tradition", "Signs that point to the resurrection of Jesus", AL("signs", 57) - 0.4, w=900, size=38)
t57 = tag(S9, 90, 690, "The usual reading: died again", AL("died", 57) - 0.9, "", 40)

# S10: the big picture (lines 58-64)
t = LS[58] - 0.4
cam(t, S10)
headline(S10, 170, ["The [whole] picture"], t + 0.1, kicker="What they have in common", hl_t=AL("whole", 58) + 0.05, size=96)
t58 = [tag(S10, 90, 430, "In common?", AL("common", 58) - 0.4, "", 52), tag(S10, 90, 540, "Differences?", AL("differ", 58) - 0.3, "acc", 52)]
gone(t58, LS[59] - 0.5)
g59 = [card(S10, 90, 420, "A gesture", "A word", AL("word", 59) - 0.3, w=400, size=32),
       card(S10, 580, 420, "A gesture", "A touch", AL("touch", 59) - 0.3, w=400, size=32),
       card(S10, 90, 640, "A gesture", "Mud, saliva", AL("mud", 59) - 0.3, w=400, size=32),
       card(S10, 580, 640, "A gesture", "From a distance", AL("distance", 59) - 0.3, w=400, size=32, accent=True)]
gone(g59, LS[60] - 0.5)
f60 = tag(S10, 90, 430, "Faith: often, not always", LS[60] + 0.3, "acc", 52)
fade(f60, AL("sick", 60) - 0.7)
g60 = [card(S10, 90, 420, "Faith", "The sick person's", AL("sick", 60) - 0.3, w=400, size=32),
       card(S10, 580, 420, "Faith", "Their friends'", AL("friends", 60) - 0.3, w=400, size=32),
       card(S10, 90, 640, "Faith", "A father's, a centurion's", AL("centurion", 60) - 0.3, w=400, size=32),
       card(S10, 580, 640, "Faith", "Sometimes, nothing is said", AL("dead", 60) - 1.2, w=400, size=32, accent=True)]
gone(g60, LS[61] - 0.5)
t61 = tag(S10, 90, 430, "He does not always heal", LS[61] + 0.3, "acc", 52)
fade(t61, AL("could", 61) - 0.7)
kq(S10, 90, 420, "Mark 6.5" + WEB, "“He could do no mighty work there, except that he laid his hands on a few sick people, and healed them.”", 61, "could", width=950, size=38,
   fade_at=LS[62] - 0.4)
f62 = tag(S10, 90, 430, "The answer to John the Baptist", LS[62] + 0.3, "acc", 52)
fade(f62, AL("blind", 62) - 0.8)
kq(S10, 90, 420, "Matthew 11.5" + WEB,
   "“the blind receive their sight, and the lame walk, the lepers are cleansed, and the deaf hear, the dead are raised up, and the poor have good news preached to them.”",
   62, "blind", width=950, size=38, fade_at=LS[63] - 0.4)
s63 = stamp(S10, 90, 440, "Our categories", AL("categories", 63) - 0.5, rot=-3, size=72)
c63 = card(S10, 90, 620, "Isaiah 35 · Isaiah 61", "An echo of Isaiah's promises", AL("isaiah", 63) - 0.3, w=800, size=38)
gone([s63, c63], LS[64] - 0.5)
S_(S10, "cent-florins", 1100, 420, 470, AL("signs", 64) - 0.5, rot=-2)
tag(S10, 90, 430, "Not only relief", AL("relief", 64) - 0.6, "", 46)
tag(S10, 90, 540, "In John: signs", AL("signs", 64) - 0.3, "acc", 50)
tag(S10, 90, 650, "Something new begins", AL("new", 64) - 0.4, "", 44)

# S11: when healing does not come (lines 65-69)
t = LS[65] - 0.4
cam(t, S11)
headline(S11, 170, ["When healing [does not come]"], t + 0.1, kicker="The New Testament", hl_t=AL("healing", 67) + 0.05, size=88)
f65 = tag(S11, 90, 430, "Sick people who are not healed", LS[65] + 0.3, "", 48)
fade(f65, AL("thorn", 65) - 0.9)
pa = S_(S11, "paul", 1500, 420, 160, AL("paul", 65) - 0.3, rot=-2)
fade(pa, LS[66] - 0.5)
t65 = [tag(S11, 90, 430, "Paul: a thorn in the flesh", AL("thorn", 65) - 0.5, "", 48), tag(S11, 90, 540, "He asks three times", AL("three", 65) - 0.3, "acc", 48)]
gone(t65, AL("answer", 65) - 0.7)
kq(S11, 90, 420, "2 Corinthians 12.9" + WEB, "“My grace is sufficient for you, for my power is made perfect in weakness.”", 65, "my", width=900, size=42, fade_at=LS[66] - 0.4)
f66 = tag(S11, 90, 430, "In another letter", LS[66] + 0.3, "", 52)
fade(f66, AL("trophimus", 66) - 0.7)
t66 = tag(S11, 90, 430, "Trophimus, sick at Miletus", AL("trophimus", 66) - 0.3, "", 52)
gone([t66], LS[67] - 0.5)
c67 = card(S11, 90, 420, "If you pray for a healing", "The text does not say that you lack faith", LS[67] + 0.3, w=900, size=38)
t67 = tag(S11, 90, 640, "Nor that your suffering does not matter", AL("matter", 67) - 1.6, "acc", 40)
gone([c67, t67], LS[68] - 0.5)
f68 = tag(S11, 90, 430, "If you are sick", LS[68] + 0.3, "acc", 52)
fade(f68, AL("doctor", 68) - 0.8)
S_(S11, "mains-lampe", 1500, 420, 300, AL("doctor", 68) - 0.3, rot=2)
t68 = [tag(S11, 90, 430, "Seeing a doctor", AL("doctor", 68) - 0.3, "", 52), tag(S11, 90, 540, "Does not oppose faith", AL("oppose", 68) - 0.3, "acc", 50),
       tag(S11, 90, 650, "Luke, “the beloved physician”", AL("beloved", 68) - 0.5, "", 46)]
gone(t68, LS[69] - 0.5)
t69 = tag(S11, 90, 430, "Which one touches you most?", AL("which", 69) - 0.3, "acc", 56)
cta = put(S11, 90, 600, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Tell us in the comments', "cta")
blur_in(cta, AL("comments", 69) - 1.2, 14)
sfx("click", AL("comments", 69) - 1.2, 0.8)

# S1 revisited: conclusion (lines 70-73)
cam(LS[70] - 2.0, "all")
wipe(S1, LS[70] - 2.1)
t = LS[70] - 0.4
cam(t, S1)
headline(S1, 170, ["In front of each, he [stops]"], t + 0.1, kicker="Capernaum", hl_t=AL("stops", 71) + 0.05, size=92)
S_(S1, "foule", 1500, 420, 300, AL("door", 70) - 0.3, rot=2)
kq(S1, 90, 420, "Mark 1.34" + WEB, "“He healed many who were sick with various diseases.”", 70, "healed", width=900, size=44, fade_at=LS[71] - 0.4)
t71 = [tag(S1, 90, 430, "The skin", AL("skin", 71) - 0.1, "", 50), tag(S1, 90, 540, "The eyes", AL("eyes", 71) - 0.1, "", 50), tag(S1, 90, 650, "The voice", AL("voice", 71) - 0.1, "", 50),
       tag(S1, 800, 430, "The legs", AL("legs", 71) - 0.1, "", 50), tag(S1, 800, 540, "The blood", AL("blood", 71) - 0.1, "", 50), tag(S1, 800, 650, "Death", AL("death", 71) - 0.1, "", 50)]
gone(t71, LS[72] - 0.5)
t72 = [tag(S1, 90, 430, "Too far", AL("far", 72) - 0.1, "", 56), tag(S1, 90, 540, "Too unclean", AL("unclean", 72) - 0.1, "", 56),
       tag(S1, 90, 650, "Too sick", AL("sick", 72) - 0.1, "", 56), tag(S1, 90, 760, "Too dead", AL("dead", 72) - 0.1, "", 56),
       stamp(S1, 800, 540, "He stops", AL("stop", 72) - 0.3, rot=-3, size=84)]
gone(t72, LS[73] - 0.3)

t_end = AL("more", 73) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(LS[70] - 2.8, LS[70] - 0.5), (AL("more", 73) - 0.8, DUR_)]
build(
    chapters=[("01", "The door at Capernaum", 0, LS[10]), ("02", "The skin", LS[10], LS[19]), ("03", "Sight", LS[19], LS[28]), ("04", "Hearing and movement", LS[28], LS[40]),
              ("05", "Fever, spirits, death", LS[40], LS[58]), ("06", "The big picture", LS[58], DUR_)],
    suppress=supp,
    endcard={"kicker": "Every week", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("jesus-portrait", 150, 560, 300, -6), ("bartimee-portrait", 1550, 330, 220, 5)]},
    endcard_t=AL("more", 73) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
