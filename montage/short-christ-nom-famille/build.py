"""Short « Christ » n'est pas le nom de famille de Jésus — style 02, 9:16.

Même fichier dans les trois dossiers (short-christ-nom-famille = FR, -en, -it) : la langue vient du nom du dossier.
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
THEME = {"brand": BRAND, "title": BRAND + " - Christ nom de famille - style 02", "lang": LANG,
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
    K = dict(christ=(1, "Christ"), fam=(1, "famille"), naz=(2, "Nazareth"), jos=(2, "Joseph"), matt=(3, "Matthieu"), q3=(3, "enfantera"),
             yeh=(4, "Yehoshoua"), sauve=(4, "Éternel"), titre=(5, "titre"), oint=(5, "oint"), mash=(6, "Mashiah"), rois=(6, "rois"),
             q7=(7, "Tu"), titre7=(7, "titre"), mess=(8, "Messie"), foi=(8, "foi"), paul=(9, "Paul"), actes=(10, "Actes"), q10=(10, "fut"),
             comm=(11, "commentaire"), abo=(12, "Abonne-toi"))
    X = dict(h1=["« [Christ] » n'est pas un nom de famille"], k1="Jésus-Christ", st1="Pas un nom de famille",
             h2=["Pas de nom de [famille]"], k2="En Judée, au Ier siècle", t2a="Jésus de Nazareth", t2b="Le fils de Joseph",
             h3=["[Matthieu] 1.21"], k3="Son nom", r3="Matthieu 1.21 · Louis Segond 1910", q3="« Elle enfantera un fils, et tu lui donneras le nom de Jésus ; c'est lui qui sauvera son peuple de ses péchés. »",
             h4=["[Jésus] = Yehoshoua"], k4="Un nom hébreu courant", c4="Yehoshoua", t4="« L'Éternel sauve »",
             h5=["Un [titre], pas un nom"], k5="Christos", c5="Christos = « oint »", t5="Un mot grec",
             h6=["Le [Messie]"], k6="Mashiah", c6="Mashiah = celui qu'on oignait d'huile", t6="Comme les rois et les prêtres",
             h7=["Pierre reconnaît un [titre]"], k7="Matthieu 16.16", r7="Matthieu 16.16 · Louis Segond 1910", q7="« Tu es le Christ, le Fils du Dieu vivant. »",
             h8=["Jésus, le [Messie]"], k8="Jésus-Christ veut dire", c8="Jésus, le Messie", t8="Une affirmation de foi",
             h9=["Presque un [nom]"], k9="Avec le temps", t9="Surtout chez Paul",
             h10=["[Actes] 11.26"], k10="Antioche", r10="Actes 11.26 · Louis Segond 1910", q10="« Ce fut à Antioche que, pour la première fois, les disciples furent appelés chrétiens. »",
             h11=["Quel [mot] ?"], k11="À toi", c11="Quel autre mot de la Bible pensais-tu connaître ?", cta="Dis-le en commentaire",
             end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"), chap=("L'idée reçue", "Le nom", "Le titre", "Pour toi"))
elif LANG == "en":
    K = dict(christ=(1, "Christ"), fam=(1, "last"), naz=(2, "Nazareth"), jos=(2, "Joseph"), matt=(3, "Matthew"), q3=(3, "She"),
             yeh=(4, "Yehoshua"), sauve=(4, "saves"), titre=(5, "title"), oint=(5, "anointed"), mash=(6, "Mashiach"), rois=(6, "kings"),
             q7=(7, "You"), titre7=(7, "title"), mess=(8, "Messiah"), foi=(8, "faith"), paul=(9, "Paul"), actes=(10, "Acts"), q10=(10, "disciples"),
             comm=(11, "comments"), abo=(12, "Subscribe"))
    X = dict(h1=["“[Christ]” is not a last name"], k1="Jesus Christ", st1="Not a last name",
             h2=["No [family] names"], k2="Judea, first century", t2a="Jesus of Nazareth", t2b="The son of Joseph",
             h3=["[Matthew] 1:21"], k3="His name", r3="Matthew 1:21 · World English Bible", q3="“She shall give birth to a son. You shall call his name Jesus, for it is he who shall save his people from their sins.”",
             h4=["[Jesus] = Yehoshua"], k4="A common Hebrew name", c4="Yehoshua", t4="“The Lord saves”",
             h5=["A [title], not a name"], k5="Christos", c5="Christos = “anointed”", t5="A Greek word",
             h6=["The [Messiah]"], k6="Mashiach", c6="Mashiach = the one anointed with oil", t6="Like kings and priests",
             h7=["Peter recognizes a [title]"], k7="Matthew 16:16", r7="Matthew 16:16 · World English Bible", q7="“You are the Christ, the Son of the living God.”",
             h8=["Jesus, the [Messiah]"], k8="Jesus Christ means", c8="Jesus, the Messiah", t8="A statement of faith",
             h9=["Almost a [name]"], k9="Over time", t9="Especially in Paul",
             h10=["[Acts] 11:26"], k10="Antioch", r10="Acts 11:26 · World English Bible", q10="“The disciples were first called Christians in Antioch.”",
             h11=["Which [word]?"], k11="Your turn", c11="Which other word in the Bible did you think you knew?", cta="Tell us in the comments",
             end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"), chap=("The common idea", "The name", "The title", "For you"))
else:
    K = dict(christ=(1, "Cristo"), fam=(1, "cognome"), naz=(2, "Nazaret"), jos=(2, "Giuseppe"), matt=(3, "Matteo"), q3=(3, "partorirà"),
             yeh=(4, "Yehoshua"), sauve=(4, "salva"), titre=(5, "titolo"), oint=(5, "unto"), mash=(6, "Mashiach"), rois=(6, "re"),
             q7=(7, "Tu"), titre7=(7, "titolo"), mess=(8, "Messia"), foi=(8, "fede"), paul=(9, "Paolo"), actes=(10, "Atti"), q10=(10, "Fu"),
             comm=(11, "commenti"), abo=(12, "Iscriviti"))
    X = dict(h1=["«[Cristo]» non è un cognome"], k1="Gesù Cristo", st1="Non un cognome",
             h2=["Niente [cognomi]"], k2="Giudea, primo secolo", t2a="Gesù di Nazaret", t2b="Il figlio di Giuseppe",
             h3=["[Matteo] 1,21"], k3="Il suo nome", r3="Matteo 1,21 · Riveduta", q3="«Ed ella partorirà un figliuolo, e tu gli porrai nome Gesù, perché è lui che salverà il suo popolo dai loro peccati.»",
             h4=["[Gesù] = Yehoshua"], k4="Un nome ebraico comune", c4="Yehoshua", t4="«Il Signore salva»",
             h5=["Un [titolo], non un nome"], k5="Christos", c5="Christos = «unto»", t5="Una parola greca",
             h6=["Il [Messia]"], k6="Mashiach", c6="Mashiach = colui che veniva unto con olio", t6="Come i re e i sacerdoti",
             h7=["Pietro riconosce un [titolo]"], k7="Matteo 16,16", r7="Matteo 16,16 · Riveduta", q7="«Tu sei il Cristo, il Figliuol dell'Iddio vivente.»",
             h8=["Gesù, il [Messia]"], k8="Gesù Cristo significa", c8="Gesù, il Messia", t8="Un'affermazione di fede",
             h9=["Quasi un [nome]"], k9="Col tempo", t9="Soprattutto in Paolo",
             h10=["[Atti] 11,26"], k10="Antiochia", r10="Atti 11,26 · Riveduta", q10="«Fu in Antiochia che per la prima volta i discepoli furon chiamati Cristiani.»",
             h11=["Quale [parola]?"], k11="A te", c11="Quale altra parola della Bibbia pensavi di conoscere?", cta="Dillo nei commenti",
             end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"), chap=("L'idea comune", "Il nome", "Il titolo", "Per te"))


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

html.append('<style>'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

ST = [(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (1, 3), (0, 3)]
S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11 = ST[:11]

# --- S1 · accroche
cam(0, S1)
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("christ") - 0.3, size=96)
sticker(S1, "jesus-pied", 60, 760, 260, 0.0, rot=-2, instant=True)
stamp(S1, 310, 1000, X["st1"], kk("fam") - 0.2, rot=-3, size=42)
hit(kk("fam"), 0.9)

# --- S2 · pas de nom de famille
t2 = LS[2] - 0.3
cam(t2, S2)
headline(S2, 300, X["h2"], t2 + 0.1, kicker=X["k2"], hl_t=LS[2] + 0.4, size=104)
tag(S2, 70, 760, X["t2a"], early(kk("naz") - 0.4, 2, 1.8), "", 54)
tag(S2, 70, 920, X["t2b"], kk("jos") - 0.4, "acc", 54)

# --- S3 · Matthieu 1.21
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 300, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("matt") - 0.3, size=112)
sticker(S3, "rouleau", 70, 1170, 170, LS[3] + 0.4, rot=-3)
q3_t0 = kk("q3") - 0.3
q3_t1 = LS[4] - 0.3
kq3 = kinetic_quote(S3, 60, 720, X["r3"], X["q3"], q3_t0, q3_t1, width=960, size=52)
fade(kq3, LS[4] - 0.4)

# --- S4 · Yehoshoua
t4 = LS[4] - 0.3
cam(t4, S4)
headline(S4, 300, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=kk("yeh") - 0.3, size=100)
c4 = put(S4, 70, 720, X["c4"], "card", "width:940px;font-size:84px")
blur_in(c4, early(kk("yeh") - 0.3, 4, 1.0), 14)
tag(S4, 70, 980, X["t4"], kk("sauve") - 0.4, "acc", 56)

# --- S5 · titre, oint
t5 = LS[5] - 0.3
cam(t5, S5)
headline(S5, 300, X["h5"], t5 + 0.1, kicker=X["k5"], hl_t=kk("titre") - 0.3, size=96)
c5 = put(S5, 70, 720, X["c5"], "card", "width:940px;font-size:68px")
blur_in(c5, early(kk("oint") - 0.5, 5, 1.2), 14)
tag(S5, 70, 960, X["t5"], kk("oint") - 0.2, "acc", 54)

# --- S6 · Messie
t6 = LS[6] - 0.3
cam(t6, S6)
headline(S6, 300, X["h6"], t6 + 0.1, kicker=X["k6"], hl_t=kk("mash") - 0.3, size=120)
c6 = put(S6, 70, 720, X["c6"], "card", "width:940px;font-size:60px")
blur_in(c6, early(kk("mash") - 0.3, 6, 1.2), 14)
tag(S6, 70, 1000, X["t6"], kk("rois") - 0.4, "acc", 54)

# --- S7 · Matthieu 16.16
t7 = LS[7] - 0.3
cam(t7, S7)
headline(S7, 300, X["h7"], t7 + 0.1, kicker=X["k7"], hl_t=kk("titre7") - 0.4, size=88)
q7_t0 = kk("q7") - 0.1
q7_t1 = LS[8] - 0.3
kq7 = kinetic_quote(S7, 60, 720, X["r7"], X["q7"], q7_t0, q7_t1, width=960, size=60)
fade(kq7, LS[8] - 0.4)

# --- S8 · Jésus-Christ = Jésus, le Messie
t8 = LS[8] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=kk("mess") - 0.3, size=104)
c8 = put(S8, 70, 720, X["c8"], "card", "width:940px;font-size:72px")
blur_in(c8, early(kk("mess") - 0.3, 8, 1.0), 14)
tag(S8, 70, 960, X["t8"], kk("foi") - 0.5, "acc", 54)

# --- S9 · presque un nom
t9 = LS[9] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=LS[9] + 0.8, size=120)
sticker(S9, "rouleau", 70, 760, 260, early(kk("paul") - 0.3, 9, 1.0), rot=-2)
tag(S9, 70, 1160, X["t9"], kk("paul") - 0.3, "acc", 54)

# --- S10 · Actes 11.26
t10 = LS[10] - 0.3
cam(t10, S10)
headline(S10, 300, X["h10"], t10 + 0.1, kicker=X["k10"], hl_t=kk("actes") - 0.3, size=112)
q10_t0 = kk("q10") - 0.2
q10_t1 = LS[11] - 0.3
kq10 = kinetic_quote(S10, 60, 720, X["r10"], X["q10"], q10_t0, q10_t1, width=960, size=56)
fade(kq10, LS[11] - 0.4)

# --- S11 · commentaire
t11 = LS[11] - 0.3
cam(t11, S11)
headline(S11, 300, X["h11"], t11 + 0.1, kicker=X["k11"], hl_t=LS[11] + 0.6, size=112)
c11 = put(S11, 70, 720, X["c11"], "card", "width:940px;font-size:56px")
blur_in(c11, LS[11] + 0.4, 14)
cta = put(S11, 70, 1080, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>' + X["cta"], "cta")
blur_in(cta, kk("comm") - 1.2, 14)
sfx("click", kk("comm") - 1.2, 0.8)

t_end = kk("abo") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", X["chap"][0], 0, LS[3]), ("02", X["chap"][1], LS[3], LS[5]), ("03", X["chap"][2], LS[5], LS[10]), ("04", X["chap"][3], LS[10], DUR_)],
    suppress=[(q3_t0 - 0.1, q3_t1 + 0.2), (q7_t0 - 0.1, q7_t1 + 0.2), (q10_t0 - 0.1, q10_t1 + 0.2), (kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("foule", 30, 1450, 420, -4), ("jesus-pied", 800, 1480, 200, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
