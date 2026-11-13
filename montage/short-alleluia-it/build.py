"""Short « Alléluia n'est pas un cri de joie, c'est un ordre » — style 02, 9:16.

Même fichier dans les trois dossiers (short-alleluia = FR, -en, -it) : la langue vient du nom du dossier.
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
THEME = {"brand": BRAND, "title": BRAND + " - Alléluia - style 02", "lang": LANG,
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
HE_ALL, HE_HAL, HE_YAH, GRK = "הללו־יה", "הללו", "יה", "ἁλληλουϊά"
if LANG == "fr":
    K = dict(ordre=(1, "ordre"), halelou=(2, "Halelou"), yah2=(2, "Yah"), halal=(3, "halal"), louer=(3, "louer"), imp=(3, "impératif"), plur=(3, "pluriel"), groupe=(4, "groupe"),
             yah5=(5, "Yah"), yhwh=(5, "YHWH"), all6=(6, "Alléluia"), louez6=(6, "Louez"), psaumes=(7, "Psaumes"), q0=(7, "Que"), heb8=(8, "hébreu"), hy8=(8, "Halelou-Yah"),
             grec=(9, "grec"), latin=(9, "latin"), lang=(9, "langues"), apo=(10, "Apocalypse"), dixneuf=(10, "dix-neuf"), foule=(10, "foule"), joie=(11, "joie"), chanter=(11, "chanter"),
             appel=(11, "appel"), ens=(11, "ensemble"), parle=(12, "parle"), comm=(13, "commentaire"), abo=(14, "Abonne-toi"))
    X = dict(h1=["« [Alléluia] »", "pas un cri de joie"], k1="Un ordre", st1="Un ordre", c1="Halelou-Yah",
             h2=["Deux [parties]"], k2="En hébreu", p1s="Première partie", p1="Halelou", p2s="Seconde partie", p2="Yah",
             h3=["Un [verbe]"], k3="Halelou · halal", v1s="Racine", v1="halal : « louer »", st3="Impératif · pluriel", c3="« Louez ! »",
             h4=["Pour tout un [groupe]"], k4="Un pluriel", c4="« Louez, vous tous ! »", h5=["Yah, le nom de [Dieu]"], k5="Forme abrégée", c5s="Le nom de Dieu", c5="YHWH", t5="Yah : forme abrégée",
             h6=["Alléluia ="], k6="Le sens", e1="Halelou + Yah", e2="« Louez Yah ! »", st6="Un ordre",
             h7=["Dans les [Psaumes]"], k7="Psaume 150.6 · Louis Segond 1910", q="« Que tout ce qui respire loue l'Éternel ! Louez l'Éternel ! »", qref="Psaume 150.6 · Louis Segond 1910",
             h8=["Dans l'[hébreu]"], k8="La dernière phrase", c8s="Texte hébreu", c8="Halelou-Yah",
             h9=["Un mot qui [voyage]"], k9="Sans être traduit", w1s="Hébreu", w2s="Grec", w3s="Latin", w4s="Nos langues", w3="Alleluia", w4="Alléluia · Hallelujah",
             h10=["L'[Apocalypse]"], k10="Le seul livre du Nouveau Testament", c10s="Apocalypse 19", c10="Une grande foule",
             h11=["Pas contre la [joie]"], k11="Un appel", c11a="Louer, c'est souvent chanter", c11b="Un appel à louer ensemble",
             h12=["On te [parle]"], k12="À toi", t12="« Alléluia » s'adresse à toi", h13=["Quel [chant] ?"], k13="À toi", cta="Dis-le en commentaire",
             end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"), chap=("L'ordre", "Le sens", "Le voyage", "Pour toi"))
elif LANG == "en":
    K = dict(ordre=(1, "command"), halelou=(2, "Hallelu"), yah2=(2, "Yah"), halal=(3, "halal"), louer=(3, "praise"), imp=(3, "imperative"), plur=(3, "plural"), groupe=(4, "group"),
             yah5=(5, "Yah"), yhwh=(5, "YHWH"), all6=(6, "hallelujah"), louez6=(6, "Praise"), psaumes=(7, "Psalms"), q0=(7, "Let"), heb8=(8, "Hebrew"), hy8=(8, "Hallelu-Yah"),
             grec=(9, "Greek"), latin=(9, "Latin"), lang=(9, "languages"), apo=(10, "Revelation"), dixneuf=(10, "nineteen"), foule=(10, "crowd"), joie=(11, "joy"), chanter=(11, "singing"),
             appel=(11, "call"), ens=(11, "together"), parle=(12, "spoken"), comm=(13, "comments"), abo=(14, "Subscribe"))
    X = dict(h1=["“[Hallelujah]”", "not a cry of joy"], k1="A command", st1="A command", c1="Hallelu-Yah",
             h2=["Two [parts]"], k2="In Hebrew", p1s="First part", p1="Hallelu", p2s="Second part", p2="Yah",
             h3=["A [verb]"], k3="Hallelu · halal", v1s="Root", v1="halal: “to praise”", st3="Imperative · plural", c3="“Praise!”",
             h4=["For a whole [group]"], k4="A plural", c4="“Praise, all of you!”", h5=["Yah, the name of [God]"], k5="A short form", c5s="God's name", c5="YHWH", t5="Yah: a short form",
             h6=["Hallelujah ="], k6="The meaning", e1="Hallelu + Yah", e2="“Praise Yah!”", st6="A command",
             h7=["In the [Psalms]"], k7="Psalm 150:6 · World English Bible", q="“Let everything that has breath praise Yah! Praise Yah!”", qref="Psalm 150:6 · World English Bible",
             h8=["In the [Hebrew]"], k8="The last sentence", c8s="Hebrew text", c8="Hallelu-Yah",
             h9=["A word that [travels]"], k9="Without being translated", w1s="Hebrew", w2s="Greek", w3s="Latin", w4s="Our languages", w3="Alleluia", w4="Hallelujah · Alléluia",
             h10=["[Revelation]"], k10="The only New Testament book", c10s="Revelation 19", c10="A great crowd",
             h11=["Not against [joy]"], k11="A call", c11a="Praising is often singing", c11b="A call to praise together",
             h12=["You are being [spoken to]"], k12="Your turn", t12="“Hallelujah” is addressed to you", h13=["Which [song]?"], k13="Your turn", cta="Tell us in the comments",
             end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"), chap=("The command", "The meaning", "The journey", "For you"))
else:
    K = dict(ordre=(1, "ordine"), halelou=(2, "Hallelu"), yah2=(2, "Yah"), halal=(3, "halal"), louer=(3, "lodare"), imp=(3, "imperativo"), plur=(3, "plurale"), groupe=(4, "gruppo"),
             yah5=(5, "Yah"), yhwh=(5, "YHWH"), all6=(6, "Alleluia"), louez6=(6, "Lodate"), psaumes=(7, "Salmi"), q0=(7, "Ogni"), heb8=(8, "ebraico"), hy8=(8, "Hallelu-Yah"),
             grec=(9, "greco"), latin=(9, "latino"), lang=(9, "lingue"), apo=(10, "Apocalisse"), dixneuf=(10, "diciannove"), foule=(10, "folla"), joie=(11, "gioia"), chanter=(11, "cantare"),
             appel=(11, "appello"), ens=(11, "insieme"), parle=(12, "parla"), comm=(13, "commenti"), abo=(14, "Iscriviti"))
    X = dict(h1=["«[Alleluia]»", "non è un grido di gioia"], k1="Un ordine", st1="Un ordine", c1="Hallelu-Yah",
             h2=["Due [parti]"], k2="In ebraico", p1s="Prima parte", p1="Hallelu", p2s="Seconda parte", p2="Yah",
             h3=["Un [verbo]"], k3="Hallelu · halal", v1s="Radice", v1="halal: «lodare»", st3="Imperativo · plurale", c3="«Lodate!»",
             h4=["Per un intero [gruppo]"], k4="Un plurale", c4="«Lodate, voi tutti!»", h5=["Yah, il nome di [Dio]"], k5="Forma abbreviata", c5s="Il nome di Dio", c5="YHWH", t5="Yah: forma abbreviata",
             h6=["Alleluia ="], k6="Il senso", e1="Hallelu + Yah", e2="«Lodate Yah!»", st6="Un ordine",
             h7=["Nei [Salmi]"], k7="Salmo 150,6 · Riveduta", q="«Ogni cosa che respira lodi l'Eterno! Alleluia!»", qref="Salmo 150,6 · Riveduta",
             h8=["Nell'[ebraico]"], k8="L'ultima frase", c8s="Testo ebraico", c8="Hallelu-Yah",
             h9=["Una parola che [viaggia]"], k9="Senza essere tradotta", w1s="Ebraico", w2s="Greco", w3s="Latino", w4s="Le nostre lingue", w3="Alleluia", w4="Alleluia · Hallelujah",
             h10=["L'[Apocalisse]"], k10="L'unico libro del Nuovo Testamento", c10s="Apocalisse 19", c10="Una grande folla",
             h11=["Non contro la [gioia]"], k11="Un appello", c11a="Lodare è spesso cantare", c11b="Un appello a lodare insieme",
             h12=["Si [parla] a te"], k12="A te", t12="«Alleluia» si rivolge a te", h13=["Quale [canto]?"], k13="A te", cta="Dillo nei commenti",
             end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"), chap=("L'ordine", "Il senso", "Il viaggio", "Per te"))


def kk(name, n=0):
    k = K[name]
    return AL(k[1], k[0], k[2] if len(k) > 2 else n)


html.append('<style>'
            '@font-face{font-family:"Frank Ruhl Libre";src:url("assets/fonts/FrankRuhlLibre.ttf") format("truetype");font-weight:300 900}'
            '.heb{font-family:"Frank Ruhl Libre",serif;direction:rtl;display:block;line-height:1.1}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

ST = [(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (1, 3), (0, 3)]
S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12 = ST

# --- S1 · accroche
cam(0, S1)
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("ordre") - 0.6, size=104)
sticker(S1, "foule", 60, 740, 440, 0.0, rot=-2, instant=True)
stamp(S1, 70, 1150, X["st1"], kk("ordre") - 0.1, rot=-4, size=90)
hit(kk("ordre"), 0.9)

# --- S2 · deux parties : Halelou, Yah
t2 = LS[2] - 0.3
cam(t2, S2)
headline(S2, 300, X["h2"], t2 + 0.1, kicker=X["k2"], hl_t=kk("halelou"), size=112)
a2 = put(S2, 70, 700, f"<small>{X['p1s']}</small>{X['p1']}<span class='heb' style='font-size:120px'>{HE_HAL}</span>", "card", "width:600px;font-size:64px")
b2 = put(S2, 70, 1010, f"<small>{X['p2s']}</small>{X['p2']}<span class='heb' style='font-size:120px'>{HE_YAH}</span>", "card", "width:600px;font-size:64px;border-color:" + ACC)
blur_in(a2, kk("halelou") - 0.2, 14)
blur_in(b2, kk("yah2") - 0.2, 14)

# --- S3 · un verbe à l'impératif pluriel
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 300, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("halal"), size=112)
v3 = put(S3, 70, 700, f"<small>{X['v1s']}</small>{X['v1']}", "card", "width:940px;font-size:66px")
blur_in(v3, kk("halal") - 0.2, 14)
stamp(S3, 70, 940, X["st3"], kk("imp") - 0.1, rot=-4, size=66)
c3 = put(S3, 70, 1090, X["c3"], "card", "width:700px;font-size:84px;border-color:" + ACC)
blur_in(c3, kk("louer") + 0.5, 14)

# --- S4 · pour tout un groupe
t4 = LS[4] - 0.3
cam(t4, S4)
headline(S4, 300, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=kk("groupe"), size=100)
c4 = put(S4, 70, 700, X["c4"], "card", "width:940px;font-size:70px")
blur_in(c4, LS[4] + 1.0, 14)
sticker(S4, "foule", 200, 900, 380, kk("groupe") - 0.2, rot=2)

# --- S5 · Yah, le nom de Dieu
t5 = LS[5] - 0.3
cam(t5, S5)
headline(S5, 300, X["h5"], t5 + 0.1, kicker=X["k5"], hl_t=kk("yhwh") - 0.8, size=100)
c5 = put(S5, 70, 700, f"<small>{X['c5s']}</small>YHWH", "card", "width:940px;font-size:96px;letter-spacing:8px")
blur_in(c5, kk("yhwh") - 0.5, 14)
tag(S5, 70, 1000, X["t5"], kk("yah5") - 0.2, "acc", 50)

# --- S6 · Alléluia = Louez Yah !
t6 = LS[6] - 0.3
cam(t6, S6)
headline(S6, 300, X["h6"], t6 + 0.1, kicker=X["k6"], hl_t=kk("all6"), size=112)
e1 = put(S6, 70, 700, X["e1"], "card", "width:940px;font-size:70px")
blur_in(e1, kk("all6") + 0.3, 14)
e2 = put(S6, 70, 930, X["e2"], "card", "width:940px;font-size:80px;border-color:" + ACC)
blur_in(e2, kk("louez6") - 0.2, 14)
stamp(S6, 70, 1160, X["st6"], kk("louez6") + 0.3, rot=-4, size=70)

# --- S7 · le Psaume 150.6
t7 = LS[7] - 0.3
cam(t7, S7)
headline(S7, 300, X["h7"], t7 + 0.1, kicker=X["k7"], hl_t=kk("psaumes"), size=112)
q_t0 = kk("q0") - 0.05
q_t1 = LS[8] - 0.3
SUPP_Q = (q_t0 - 0.1, q_t1 + 0.2)
f7 = tag(S7, 60, 700, X["qref"], LS[7] + 0.2, "", 44)
fade(f7, q_t0 - 0.2)
kq = kinetic_quote(S7, 60, 700, X["qref"], X["q"], q_t0, q_t1, width=960, size=54)
fade(kq, LS[8] - 0.4)

# --- S8 · le texte hébreu
t8 = LS[8] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=kk("heb8"), size=112)
c8 = put(S8, 70, 700, f"<small>{X['c8s']}</small>{X['c8']}<span class='heb' style='font-size:170px;margin-top:10px'>{HE_ALL}</span>", "card", "width:940px;font-size:76px")
blur_in(c8, LS[8] + 0.6, 14)
hit(kk("hy8"), 1.0)

# --- S9 · le mot voyage : hébreu, grec, latin, nos langues
t9 = LS[9] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=kk("grec") - 0.4, size=100)
w = [("w1s", HE_ALL, 70, 700, "heb8", True), ("w2s", GRK, 560, 700, "grec", False), ("w3s", X["w3"], 70, 960, "latin", False), ("w4s", X["w4"], 560, 960, "lang", False)]
for key, txt, x, y, a, heb in w:
    inner = f"<small>{X[key]}</small>" + (f"<span class='heb' style='font-size:76px'>{txt}</span>" if heb else txt)
    bx = put(S9, x, y, inner, "card", "width:440px;font-size:50px" + (";border-color:" + ACC if key == "w4s" else ""))
    blur_in(bx, (LS[9] + 0.5 if a == "heb8" else kk(a) - 0.3), 14)

# --- S10 · l'Apocalypse 19
t10 = LS[10] - 0.3
cam(t10, S10)
headline(S10, 300, X["h10"], t10 + 0.1, kicker=X["k10"], hl_t=kk("apo"), size=112)
c10 = put(S10, 70, 700, f"<small>{X['c10s']}</small>{X['c10']}", "card", "width:940px;font-size:70px")
blur_in(c10, kk("apo") + 0.2, 14)
sticker(S10, "foule", 200, 900, 380, kk("foule") - 0.3, rot=2)

# --- S11 · pas contre la joie : un appel
t11 = LS[11] - 0.3
cam(t11, S11)
headline(S11, 300, X["h11"], t11 + 0.1, kicker=X["k11"], hl_t=kk("joie"), size=112)
c11a = put(S11, 70, 700, X["c11a"], "card", "width:940px;font-size:62px")
blur_in(c11a, kk("chanter") - 0.3, 14)
c11b = put(S11, 70, 960, X["c11b"], "card", "width:940px;font-size:62px;border-color:" + ACC)
blur_in(c11b, kk("appel") - 0.3, 14)

# --- S12 · on te parle, puis appel à commenter
t12 = LS[12] - 0.3
cam(t12, S12)
headline(S12, 300, X["h12"], t12 + 0.1, kicker=X["k12"], hl_t=kk("parle") - 0.8, size=112)
tag(S12, 70, 700, X["t12"], LS[12] + 0.4, "acc", 44)
c13 = put(S12, 70, 860, "<small>" + X["k13"] + "</small>" + X["h13"][0].replace("[", "").replace("]", ""), "card", "width:940px;font-size:80px")
blur_in(c13, LS[13] + 0.2, 14)
cta = put(S12, 70, 1170, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>' + X["cta"], "cta")
blur_in(cta, kk("comm") - 1.2, 14)
sfx("click", kk("comm") - 1.2, 0.8)

t_end = kk("abo") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", X["chap"][0], 0, LS[3]), ("02", X["chap"][1], LS[3], LS[7]), ("03", X["chap"][2], LS[7], LS[11]), ("04", X["chap"][3], LS[11], DUR_)],
    suppress=[SUPP_Q, (kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("foule", 30, 1450, 420, -4), ("jesus-pied", 800, 1480, 200, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
