"""Short « Le plus long chapitre de la Bible compte 176 versets (Psaume 119) » — style 02, 9:16.

Même fichier dans les trois dossiers (short-psaume-119 = FR, -en, -it) : la langue vient du nom du dossier.
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
THEME = {"brand": BRAND, "title": BRAND + " - Psaume 119 - style 02", "lang": LANG,
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
    K = dict(n176=(1, "176"), ps=(1, "Psaume"), p117=(2, "117"), p118=(2, "118"), alpha=(3, "alphabet"), acro=(4, "acrostiche"), lettres=(4, "lettres"),
             huit=(5, "huit"), alef=(5, "alef"), sixsept=(5, "soixante-seize"), parole=(6, "parole"), loi=(6, "loi"), prec=(6, "préceptes"), cmd=(6, "commandements"),
             v105=(7, "105"), ta=(7, "Ta"), aimer=(8, "aimer"), conso=(8, "consolation"), suppl=(8, "supplie"), nomme=(9, "nomme"),
             verset=(10, "verset"), comm=(10, "commentaire"), abo=(11, "Abonne-toi"))
    X = dict(h1=["[176] versets"], k1="Le plus long chapitre", unit1=" versets", st1="Psaume 119",
             h2=["117 · 118 · [119]"], k2="Trois psaumes voisins", c2a="Psaume 117 : 2 versets", c2b="Psaume 118", c2c="Psaume 119 : 176 versets",
             h3=["Un poème en [alphabet]"], k3="Pourquoi tant de versets ?", c3="Un poème construit comme un alphabet",
             h4=["Un [acrostiche]"], k4="En hébreu", unit4=" strophes", t4="Une lettre par strophe",
             h5=["8 × 22 = [176]"], k5="De alef à tav", c5a="8 versets par strophe", c5b="22 strophes", c5c="8 × 22 = 176",
             h6=["La parole de [Dieu]"], k6="De quoi parle-t-il ?", t6a="Loi", t6b="Préceptes", t6c="Commandements",
             h7=["Le verset [105]"], k7="Le plus connu", q7="« Ta parole est une lampe à mes pieds, et une lumière sur mon sentier. »", r7="Psaume 119.105 · Louis Segond 1910",
             h8=["Pas un code [froid]"], k8="L'auteur", t8a="Il aime cette parole", t8b="Il y trouve de la consolation", t8c="Il supplie Dieu dans l'épreuve",
             h9=["Un auteur [inconnu]"], k9="Le texte ne le nomme pas", st9="Auteur non nommé",
             h10=["Quel [verset] ?"], k10="À toi", c10="Quel verset du Psaume 119 préfères-tu ?", cta="Dis-le en commentaire",
             end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"), chap=("Le record", "L'alphabet", "La parole", "Pour toi"))
elif LANG == "en":
    K = dict(n176=(1, "176"), ps=(1, "Psalm"), p117=(2, "117"), p118=(2, "118"), alpha=(3, "alphabet"), acro=(4, "acrostic"), lettres=(4, "letters"),
             huit=(5, "eight"), alef=(5, "alef"), sixsept=(5, "seventy-six"), parole=(6, "word"), loi=(6, "law"), prec=(6, "precepts"), cmd=(6, "commandments"),
             v105=(7, "105"), ta=(7, "Your"), aimer=(8, "loves"), conso=(8, "comfort"), suppl=(8, "begs"), nomme=(9, "name"),
             verset=(10, "verse"), comm=(10, "comments"), abo=(11, "Subscribe"))
    X = dict(h1=["[176] verses"], k1="The longest chapter", unit1=" verses", st1="Psalm 119",
             h2=["117 · 118 · [119]"], k2="Three neighbouring psalms", c2a="Psalm 117: 2 verses", c2b="Psalm 118", c2c="Psalm 119: 176 verses",
             h3=["A poem as an [alphabet]"], k3="Why so many verses?", c3="A poem built like an alphabet",
             h4=["An [acrostic]"], k4="In Hebrew", unit4=" stanzas", t4="One letter per stanza",
             h5=["8 × 22 = [176]"], k5="From alef to tav", c5a="8 verses per stanza", c5b="22 stanzas", c5c="8 × 22 = 176",
             h6=["The word of [God]"], k6="What is it about?", t6a="Law", t6b="Precepts", t6c="Commandments",
             h7=["Verse [105]"], k7="The best known", q7="“Your word is a lamp to my feet, and a light for my path.”", r7="Psalm 119:105 · World English Bible",
             h8=["Not a [cold] code"], k8="The author", t8a="He loves this word", t8b="He finds comfort in it", t8c="He begs God in hardship",
             h9=["An [unknown] author"], k9="The text does not name him", st9="Author not named",
             h10=["Which [verse]?"], k10="Your turn", c10="Which verse of Psalm 119 do you prefer?", cta="Tell us in the comments",
             end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"), chap=("The record", "The alphabet", "The word", "For you"))
else:
    K = dict(n176=(1, "176"), ps=(1, "Salmo"), p117=(2, "117"), p118=(2, "118"), alpha=(3, "alfabeto"), acro=(4, "acrostico"), lettres=(4, "lettere"),
             huit=(5, "otto"), alef=(5, "alef"), sixsept=(5, "centosettantasei"), parole=(6, "parola"), loi=(6, "legge"), prec=(6, "precetti"), cmd=(6, "comandamenti"),
             v105=(7, "105"), ta=(7, "La"), aimer=(8, "amare"), conso=(8, "consolazione"), suppl=(8, "supplica"), nomme=(9, "nomina"),
             verset=(10, "versetto"), comm=(10, "commenti"), abo=(11, "Iscriviti"))
    X = dict(h1=["[176] versetti"], k1="Il capitolo più lungo", unit1=" versetti", st1="Salmo 119",
             h2=["117 · 118 · [119]"], k2="Tre salmi vicini", c2a="Salmo 117: 2 versetti", c2b="Salmo 118", c2c="Salmo 119: 176 versetti",
             h3=["Una poesia a [alfabeto]"], k3="Perché tanti versetti?", c3="Una poesia costruita come un alfabeto",
             h4=["Un [acrostico]"], k4="In ebraico", unit4=" strofe", t4="Una lettera per strofa",
             h5=["8 × 22 = [176]"], k5="Da alef a tav", c5a="8 versetti per strofa", c5b="22 strofe", c5c="8 × 22 = 176",
             h6=["La parola di [Dio]"], k6="Di che cosa parla?", t6a="Legge", t6b="Precetti", t6c="Comandamenti",
             h7=["Il versetto [105]"], k7="Il più noto", q7="«La tua parola è una lampada al mio piede, ed una luce sul mio sentiero.»", r7="Salmo 119,105 · Riveduta",
             h8=["Non un codice [freddo]"], k8="L'autore", t8a="Ama questa parola", t8b="Vi trova consolazione", t8c="Supplica Dio nella prova",
             h9=["Un autore [ignoto]"], k9="Il testo non lo nomina", st9="Autore non nominato",
             h10=["Quale [versetto]?"], k10="A te", c10="Quale versetto del Salmo 119 preferisci?", cta="Dillo nei commenti",
             end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"), chap=("Il record", "L'alfabeto", "La parola", "Per te"))


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

# --- S1 · accroche : 176 versets
cam(0, S1)
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("n176") - 0.4, size=112)
sticker(S1, "livres", 60, 720, 250, 0.0, rot=-2, instant=True)
counter(S1, 340, 740, 0, 176, max(kk("n176") - 1.2, 0.5), 1.1, unit=X["unit1"], size=96)
stamp(S1, 340, 960, X["st1"], kk("ps") - 0.1, rot=-4, size=84)
hit(kk("n176"), 0.9)

# --- S2 · 117, 118, 119
t2 = LS[2] - 0.3
cam(t2, S2)
headline(S2, 300, X["h2"], t2 + 0.1, kicker=X["k2"], hl_t=kk("p118") - 0.2, size=112)
c2a = put(S2, 70, 720, X["c2a"], "card", "width:760px;font-size:52px")
blur_in(c2a, early(kk("p117") - 0.3, 2, 0.9), 14)
c2b = put(S2, 70, 880, X["c2b"], "card", "width:760px;font-size:52px")
blur_in(c2b, kk("p118") - 0.3, 14)
c2c = put(S2, 70, 1040, X["c2c"], "card", "width:760px;font-size:52px;border-color:" + ACC)
blur_in(c2c, kk("p118") + 0.6, 14)

# --- S3 · un poème comme un alphabet
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 300, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("alpha") - 0.3, size=100)
c3 = put(S3, 70, 720, X["c3"], "card", "width:940px;font-size:62px")
blur_in(c3, early(kk("alpha") - 0.9, 3, 1.2), 14)
sticker(S3, "rouleau", 690, 1000, 300, LS[3] + 1.4, rot=2)

# --- S4 · acrostiche, 22 strophes
t4 = LS[4] - 0.3
cam(t4, S4)
headline(S4, 300, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=kk("acro") - 0.3, size=112)
counter(S4, 70, 720, 0, 22, early(kk("acro") - 0.2, 4, 1.0), 0.8, unit=X["unit4"], size=150)
tag(S4, 70, 1040, X["t4"], kk("lettres") - 0.6, "acc", 56)

# --- S5 · 8 x 22 = 176
t5 = LS[5] - 0.3
cam(t5, S5)
headline(S5, 300, X["h5"], t5 + 0.1, kicker=X["k5"], hl_t=kk("sixsept") - 0.5, size=112)
c5a = put(S5, 70, 720, X["c5a"], "card", "width:760px;font-size:54px")
blur_in(c5a, early(kk("huit") - 0.3, 5, 0.8), 14)
c5b = put(S5, 70, 880, X["c5b"], "card", "width:760px;font-size:54px")
blur_in(c5b, kk("alef") - 0.8, 14)
c5c = put(S5, 70, 1040, X["c5c"], "card", "width:760px;font-size:70px;border-color:" + ACC)
blur_in(c5c, kk("sixsept") - 1.0, 14)

# --- S6 · la parole de Dieu
t6 = LS[6] - 0.3
cam(t6, S6)
headline(S6, 300, X["h6"], t6 + 0.1, kicker=X["k6"], hl_t=kk("parole") - 0.3, size=112)
tag(S6, 70, 720, X["t6a"], early(kk("loi") - 0.3, 6, 1.3), "", 60)
tag(S6, 70, 860, X["t6b"], kk("prec") - 0.3, "", 60)
tag(S6, 70, 1000, X["t6c"], kk("cmd") - 0.4, "acc", 60)

# --- S7 · le verset 105
t7 = LS[7] - 0.3
cam(t7, S7)
headline(S7, 300, X["h7"], t7 + 0.1, kicker=X["k7"], hl_t=kk("v105") - 0.2, size=112)
q7_t0 = kk("ta") - 0.05
q7_t1 = LS[8] - 0.3
SUPP_Q = (q7_t0 - 0.1, q7_t1 + 0.2)
f7 = tag(S7, 60, 720, X["r7"], LS[7] + 0.2, "", 40)
fade(f7, q7_t0 - 0.2)
kq7 = kinetic_quote(S7, 60, 720, X["r7"], X["q7"], q7_t0, q7_t1, width=960, size=56)
fade(kq7, LS[8] - 0.4)

# --- S8 · pas un code froid
t8 = LS[8] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=LS[8] + 0.5, size=104)
tag(S8, 70, 720, X["t8a"], early(kk("aimer") - 0.3, 8, 1.4), "", 52)
tag(S8, 70, 860, X["t8b"], kk("conso") - 0.4, "", 52)
tag(S8, 70, 1000, X["t8c"], kk("suppl") - 0.3, "acc", 52)

# --- S9 · auteur non nommé
t9 = LS[9] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=kk("nomme") - 0.4, size=112)
stamp(S9, 70, 720, X["st9"], early(kk("nomme") - 0.3, 9, 0.9), rot=-4, size=76)
sticker(S9, "scribe", 70, 940, 150, LS[9] + 0.6, rot=2)

# --- S10 · commentaire
t10 = LS[10] - 0.3
cam(t10, S10)
headline(S10, 300, X["h10"], t10 + 0.1, kicker=X["k10"], hl_t=kk("verset") - 0.2, size=112)
c10 = put(S10, 70, 720, X["c10"], "card", "width:940px;font-size:58px")
blur_in(c10, LS[10] + 0.4, 14)
cta = put(S10, 70, 1080, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>' + X["cta"], "cta")
blur_in(cta, kk("comm") - 1.2, 14)
sfx("click", kk("comm") - 1.2, 0.8)

t_end = kk("abo") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", X["chap"][0], 0, LS[3]), ("02", X["chap"][1], LS[3], LS[6]), ("03", X["chap"][2], LS[6], LS[9]), ("04", X["chap"][3], LS[9], DUR_)],
    suppress=[SUPP_Q, (kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("foule", 30, 1450, 420, -4), ("jesus-pied", 800, 1480, 200, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
