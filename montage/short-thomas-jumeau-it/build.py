"""Short « Quel apôtre avait pour surnom « le jumeau » ? » — style 02, 9:16.

Même fichier dans les trois dossiers (short-thomas-jumeau = FR, -en, -it) : la langue vient du nom du dossier.
Construit avec le moteur du kit (kit-style-02/moteur/style02.py), option retention, calé mot par mot sur transcript.json.
Contrôles : python3 build.py ; node ../../kit-style-02/outils/audit_chevauchements.js . 0.25 400 ; npx hyperframes check
"""
import difflib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

LANG = "en" if HERE.endswith("-en") else "it" if HERE.endswith("-it") else "fr"
DUR_ = json.load(open(os.path.join(HERE, "dur.json")))["dur"]
BRAND = {"fr": "La Bible Simple", "en": "Faith Engineering", "it": "La Bibbia Semplice"}[LANG]
THEME = {"brand": BRAND, "title": BRAND + " - Thomas le jumeau - style 02", "lang": LANG,
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
s.setup(here=HERE, duration=DUR_, cols=3, rows=4, theme=THEME)
from style02 import *  # noqa: E402,F401,F403
import style02  # noqa: E402

MANQUES = []
PRE = ("", "l", "d", "j", "n", "s", "qu", "c", "m", "t", "dell", "nell", "all", "dall", "sull", "un", "v", "quest", "nel", "sant", "tutt")


def _norm(t):
    return re.sub(r"[^\wà-ÿ]", "", t.lower().replace("’", "").replace("'", ""))


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
    keys = {style02.norm(pre + word) for pre in PRE}
    hits = sorted(w["start"] for w in style02.words if style02.norm(w["text"]) in keys and w["start"] >= after - 0.01)
    if len(hits) > n:
        return hits[n]
    MANQUES.append((word, after, n))
    return max(after, 1.0) + 0.5


def AL(word, line, n=0):
    return A(word, LS[line] - 0.05, n)


def tiles(station, x, y, n, t, cols=7, size=56, gap=12, step=0.09):
    """Cases grises qui passent à l'accent une à une (une case = un animal)."""
    cells = "".join(f'<i style="width:{size}px;height:{size}px"></i>' for _ in range(n))
    i = put(station, x, y, cells, "grid", f"grid-template-columns:repeat({cols},{size}px);gap:{gap}px")
    blur_in(i, t - 0.3, 10)
    tw.append(f'tl.fromTo("#{i} i", {{ backgroundColor: "{THEME.get("tile", "#DDD0B6")}", scale: 0.6 }}, '
              f'{{ backgroundColor: "{ACC}", scale: 1, duration: 0.2, ease: "back.out(3)", stagger: {step} }}, {at(t)});')
    sfx("tick", t, 0.25, min(n * step + 0.2, 1.5))
    return i


def gone(ids, t):
    for _i in ids:
        fade(_i, t)


# --------------------------------------------------------------------- textes par langue
if LANG == "fr":
    K = dict(thomas=(1, "Thomas"), jum1=(1, "jumeau"), didyme=(2, "Didyme"), aram=(3, "araméen"), grec=(3, "grec"), jum3=(3, "jumeau"), dit=(4, "dit"),
             actes=(5, "Actes"), tardive=(5, "tardive"), evang=(5, "Évangiles"), incr=(6, "incrédule"), refuse=(6, "refuse"), plaies=(6, "plaies"),
             parce=(7, "Parce"), heureux=(7, "Heureux"), cour=(8, "courageux"), allons=(8, "Allons"), conf=(9, "confession"), mon=(9, "Mon"),
             doute=(10, "doute"), comm=(10, "commentaire"), abo=(11, "Abonne-toi"))
    X = dict(h1=["Le [jumeau]"], k1="Quel apôtre ?", q1="« Le jumeau »", st1="Thomas",
             h2=["Thomas, appelé [Didyme]"], k2="Évangile de Jean", c2="« Thomas, appelé Didyme »", t2="Jean 11.16 · 20.24 · 21.2",
             h3=["Deux noms, une [idée]"], k3="Jumeau", t3a="Thomas : araméen", t3b="Didyme : grec", c3="= jumeau",
             h4=["Jumeau de [qui] ?"], k4="Question ouverte", st4="La Bible ne le dit pas",
             h5=["Une [tradition] tardive"], k5="Hors de la Bible", c5s="Écrit non biblique", c5="Actes de Thomas", t5a="Jumeau de Jésus ?", t5b="Tradition tardive", st5="Pas dans les Évangiles",
             h6=["L'[incrédule] ?"], k6="Jean 20", t6a="Un surnom traditionnel", t6b="Veut voir et toucher", t6c="Les plaies de Jésus",
             h7=["Jean [20.29]"], k7="Huit jours plus tard", q7="« Parce que tu m'as vu, tu as cru. Heureux ceux qui n'ont pas vu, et qui ont cru ! »", r7="Jean 20.29 · Louis Segond 1910",
             h8=["Un [courage] discret"], k8="Jean 11.16", q8="« Allons aussi, afin de mourir avec lui ! »", r8="Jean 11.16 · Louis Segond 1910",
             h9=["La plus forte [confession]"], k9="Jean 20.28", c9="« Mon Seigneur et mon Dieu ! »",
             h10=["Ton [doute] ?"], k10="À toi", c10="Te reconnais-tu dans le doute de Thomas ?", cta="Dis-le en commentaire",
             end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"), chap=("Le surnom", "La tradition", "Le doute", "Pour toi"))
elif LANG == "en":
    K = dict(thomas=(1, "Thomas"), jum1=(1, "twin"), didyme=(2, "Didymus"), aram=(3, "Aramaic"), grec=(3, "Greek"), jum3=(3, "twin"), dit=(4, "say"),
             actes=(5, "Acts"), tardive=(5, "late"), evang=(5, "Gospels"), incr=(6, "doubter"), refuse=(6, "refuses"), plaies=(6, "wounds"),
             parce=(7, "Because"), heureux=(7, "Blessed"), cour=(8, "courageous"), allons=(8, "Let's"), conf=(9, "confession"), mon=(9, "My"),
             doute=(10, "doubt"), comm=(10, "comments"), abo=(11, "Subscribe"))
    X = dict(h1=["The [twin]"], k1="Which apostle?", q1="“The twin”", st1="Thomas",
             h2=["Thomas, called [Didymus]"], k2="Gospel of John", c2="“Thomas, who is called Didymus”", t2="John 11:16 · 20:24 · 21:2",
             h3=["Two names, one [idea]"], k3="Twin", t3a="Thomas: Aramaic", t3b="Didymus: Greek", c3="= twin",
             h4=["Twin of [whom]?"], k4="An open question", st4="The Bible does not say",
             h5=["A late [tradition]"], k5="Outside the Bible", c5s="Non-biblical writing", c5="Acts of Thomas", t5a="Twin of Jesus?", t5b="Late tradition", st5="Not in the Gospels",
             h6=["The [doubter]?"], k6="John 20", t6a="A traditional nickname", t6b="Wants to see and touch", t6c="The wounds of Jesus",
             h7=["John [20:29]"], k7="Eight days later", q7="“Because you have seen me, you have believed. Blessed are those who have not seen, and have believed.”", r7="John 20:29 · World English Bible",
             h8=["A quiet [courage]"], k8="John 11:16", q8="“Let's go also, that we may die with him.”", r8="John 11:16 · World English Bible",
             h9=["The strongest [confession]"], k9="John 20:28", c9="“My Lord and my God!”",
             h10=["Your [doubt]?"], k10="Your turn", c10="Do you see yourself in Thomas's doubt?", cta="Tell us in the comments",
             end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"), chap=("The nickname", "The tradition", "The doubt", "For you"))
else:
    K = dict(thomas=(1, "Tommaso"), jum1=(1, "gemello"), didyme=(2, "Didimo"), aram=(3, "aramaico"), grec=(3, "greco"), jum3=(3, "gemello"), dit=(4, "dice"),
             actes=(5, "Atti"), tardive=(5, "tarda"), evang=(5, "Vangeli"), incr=(6, "incredulo"), refuse=(6, "Rifiuta"), plaies=(6, "piaghe"),
             parce=(7, "Perché"), heureux=(7, "beati"), cour=(8, "coraggioso"), allons=(8, "Andiamo"), conf=(9, "confessione"), mon=(9, "Signor"),
             doute=(10, "dubbio"), comm=(10, "commenti"), abo=(11, "Iscriviti"))
    X = dict(h1=["Il [gemello]"], k1="Quale apostolo?", q1="«Il gemello»", st1="Tommaso",
             h2=["Tommaso, detto [Didimo]"], k2="Vangelo di Giovanni", c2="«Tommaso, detto Didimo»", t2="Giovanni 11,16 · 20,24 · 21,2",
             h3=["Due nomi, una [idea]"], k3="Gemello", t3a="Tommaso: aramaico", t3b="Didimo: greco", c3="= gemello",
             h4=["Gemello di [chi]?"], k4="Una domanda aperta", st4="La Bibbia non lo dice",
             h5=["Una [tradizione] tarda"], k5="Fuori dalla Bibbia", c5s="Scritto non biblico", c5="Atti di Tommaso", t5a="Gemello di Gesù?", t5b="Tradizione tarda", st5="Non nei Vangeli",
             h6=["L'[incredulo]?"], k6="Giovanni 20", t6a="Un soprannome tradizionale", t6b="Vuole vedere e toccare", t6c="Le piaghe di Gesù",
             h7=["Giovanni [20,29]"], k7="Otto giorni dopo", q7="«Perché m'hai veduto, tu hai creduto; beati quelli che non hanno veduto, e hanno creduto!»", r7="Giovanni 20,29 · Riveduta",
             h8=["Un [coraggio] discreto"], k8="Giovanni 11,16", q8="«Andiamo anche noi, per morire con lui!»", r8="Giovanni 11,16 · Riveduta",
             h9=["La più forte [confessione]"], k9="Giovanni 20,28", c9="«Signor mio e Dio mio!»",
             h10=["Il tuo [dubbio]?"], k10="A te", c10="Ti riconosci nel dubbio di Tommaso?", cta="Dillo nei commenti",
             end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"), chap=("Il soprannome", "La tradizione", "Il dubbio", "Per te"))


def kk(name, n=0):
    k = K[name]
    return AL(k[1], k[0], k[2] if len(k) > 2 else n)


def early(t, line, d=0.8):
    return min(t, LS[line] + d)


html.append('<style>'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

ST = [(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (1, 3), (0, 3)]
S1, S2, S3, S4, S5, S6, S7, S8, S9, S10 = ST[:10]

# --- S1 · accroche
cam(0, S1)
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("jum1") - 0.3, size=120)
sticker(S1, "pere", 60, 720, 230, 0.0, rot=-2, instant=True)
q1 = put(S1, 340, 740, X["q1"], "card", "width:670px;font-size:64px")
blur_in(q1, 0.25, 14)
stamp(S1, 340, 960, X["st1"], kk("thomas") - 0.1, rot=-4, size=110)
hit(kk("thomas"), 0.9)

# --- S2 · Thomas, appelé Didyme
t2 = LS[2] - 0.3
cam(t2, S2)
headline(S2, 300, X["h2"], t2 + 0.1, kicker=X["k2"], hl_t=kk("didyme") - 0.3, size=100)
c2 = put(S2, 70, 720, X["c2"], "card", "width:940px;font-size:62px")
blur_in(c2, early(kk("didyme") - 0.9, 2, 0.9), 14)
tag(S2, 70, 980, X["t2"], kk("didyme") + 0.4, "acc", 50)

# --- S3 · deux noms, une idée
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 300, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("jum3") - 0.3, size=100)
tag(S3, 70, 720, X["t3a"], early(kk("aram") - 0.5, 3, 1.3), "", 58)
tag(S3, 70, 860, X["t3b"], kk("grec") - 0.3, "", 58)
c3 = put(S3, 70, 1000, X["c3"], "card", "width:700px;font-size:84px;border-color:" + ACC)
blur_in(c3, kk("jum3") - 0.3, 14)

# --- S4 · jumeau de qui ?
t4 = LS[4] - 0.3
cam(t4, S4)
headline(S4, 300, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=LS[4] + 0.3, size=112)
stamp(S4, 70, 720, X["st4"], early(kk("dit") - 0.7, 4, 0.9), rot=-4, size=72)
sticker(S4, "veilleur", 70, 980, 230, LS[4] + 1.0, rot=-2)

# --- S5 · une tradition tardive
t5 = LS[5] - 0.3
cam(t5, S5)
headline(S5, 300, X["h5"], t5 + 0.1, kicker=X["k5"], hl_t=kk("tardive") - 0.4, size=100)
c5 = put(S5, 70, 720, f"<small>{X['c5s']}</small>{X['c5']}", "card", "width:760px;font-size:60px")
blur_in(c5, early(kk("actes") - 0.3, 5, 0.9), 14)
tag(S5, 70, 960, X["t5a"], kk("actes") + 0.6, "", 52)
tag(S5, 70, 1090, X["t5b"], kk("tardive") - 0.4, "acc", 52)
stamp(S5, 70, 1235, X["st5"], kk("evang") - 0.5, rot=-4, size=56)

# --- S6 · l'incrédule
t6 = LS[6] - 0.3
cam(t6, S6)
headline(S6, 300, X["h6"], t6 + 0.1, kicker=X["k6"], hl_t=kk("incr") - 0.3, size=112)
tag(S6, 70, 720, X["t6a"], early(kk("incr") - 0.3, 6, 1.0), "", 54)
tag(S6, 70, 860, X["t6b"], kk("refuse") - 0.3, "", 54)
tag(S6, 70, 1000, X["t6c"], kk("plaies") - 0.4, "acc", 54)

# --- S7 · Jean 20.29
t7 = LS[7] - 0.3
cam(t7, S7)
headline(S7, 300, X["h7"], t7 + 0.1, kicker=X["k7"], hl_t=kk("heureux") - 0.4, size=112)
q7_t0 = kk("parce") - 0.05
q7_t1 = LS[8] - 0.3
f7 = tag(S7, 60, 720, X["r7"], LS[7] + 0.2, "", 40)
fade(f7, q7_t0 - 0.2)
kq7 = kinetic_quote(S7, 60, 720, X["r7"], X["q7"], q7_t0, q7_t1, width=960, size=50)
fade(kq7, LS[8] - 0.4)

# --- S8 · Jean 11.16
t8 = LS[8] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=kk("cour") - 0.3, size=112)
q8_t0 = kk("allons") - 0.05
q8_t1 = LS[9] - 0.3
f8 = tag(S8, 60, 720, X["r8"], LS[8] + 0.2, "", 40)
fade(f8, q8_t0 - 0.2)
kq8 = kinetic_quote(S8, 60, 720, X["r8"], X["q8"], q8_t0, q8_t1, width=960, size=60)
fade(kq8, LS[9] - 0.4)

# --- S9 · la confession
t9 = LS[9] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=kk("conf") - 0.3, size=100)
c9 = put(S9, 70, 720, X["c9"], "card", "width:940px;font-size:72px;border-color:" + ACC)
blur_in(c9, early(kk("mon") - 0.3, 9, 1.6), 14)
sticker(S9, "jesus-pied", 800, 980, 150, LS[9] + 1.0, rot=2)

# --- S10 · commentaire
t10 = LS[10] - 0.3
cam(t10, S10)
headline(S10, 300, X["h10"], t10 + 0.1, kicker=X["k10"], hl_t=kk("doute") - 0.2, size=112)
c10 = put(S10, 70, 720, X["c10"], "card", "width:940px;font-size:58px")
blur_in(c10, LS[10] + 0.4, 14)
cta = put(S10, 70, 1080, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>' + X["cta"], "cta")
blur_in(cta, kk("comm") - 1.2, 14)
sfx("click", kk("comm") - 1.2, 0.8)

t_end = kk("abo") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", X["chap"][0], 0, LS[4]), ("02", X["chap"][1], LS[4], LS[6]), ("03", X["chap"][2], LS[6], LS[9]), ("04", X["chap"][3], LS[9], DUR_)],
    suppress=[(q7_t0 - 0.1, q7_t1 + 0.2), (q8_t0 - 0.1, q8_t1 + 0.2), (kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("foule", 30, 1450, 420, -4), ("jesus-pied", 800, 1480, 200, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
