"""Short « Jésus ne s'appelait pas « Jésus » (Yeshoua) » — style 02, 9:16.

Même fichier dans les trois dossiers (short-yeshoua = FR, -en, -it) : la langue vient du nom du dossier.
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
THEME = {"brand": BRAND, "title": BRAND + " - Yeshoua - style 02", "lang": LANG,
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
HE1, HE2, GR = "ישוע", "יהושע", "Ἰησοῦς"
if LANG == "fr":
    K = dict(ye1=(1, "Yeshoua"), aram=(2, "araméen"), hebr=(2, "hébreu"), ye3=(3, "Yeshoua"), yeho=(3, "Yehoshoua"), jos=(3, "Josué"), sei=(4, "Seigneur"), sauve=(4, "sauve"),
             q0=(5, "Elle"), grec=(6, "grec"), iesous=(6, "Iêsous"), term=(6, "terminaison"), lat=(7, "latin"), iesus=(7, "Iesus"), jesusfr=(7, "Jésus"), jesusen=(7, "Jesus"), gesu=(7, "Gesù"),
             jos8=(8, "Josué"), ies8=(8, "Iêsous"), meme=(8, "même"), cour=(9, "courant"), naz=(9, "Nazareth"), droit=(10, "droit"), sur=(10, "sûr"), meme10=(10, "même"),
             ye11=(11, "Yeshoua"), sauve11=(11, "sauve"), sens=(11, "sens"), comm=(12, "commentaire"), abo=(13, "Abonne-toi"))
    X = dict(h1=["Jésus ne s'appelait", "pas « [Jésus] »"], k1="Le vrai nom", c1s="Ses proches disaient", c1="Yeshoua",
             h2=["Il parle [araméen]"], k2="Galilée · premier siècle", t2a="Araméen : la langue du quotidien", t2b="Hébreu : sans doute aussi",
             h3=["[Yeshoua]", "forme courte"], k3="Le nom", c3a="Forme longue", c3b="Forme courte", c3c="en français", c3d="Josué",
             h4=["Un nom qui [sauve]"], k4="Le sens courant", c4="« Le Seigneur sauve »", st4="Sens courant", h5=["Matthieu [explique]"], k5="Matthieu 1.21 · Louis Segond 1910",
             q="« Elle enfantera un fils, et tu lui donneras le nom de Jésus ; car c'est lui qui sauvera son peuple de ses péchés. »", qref="Matthieu 1.21 · Louis Segond 1910",
             h6=["En [grec]"], k6="Les évangiles sont écrits en grec", g1s="Hébreu · araméen", g2s="Grec", st6="+ s final", t6="Une terminaison grecque",
             h7=["Puis le [latin]"], k7="Jusqu'à nos langues", l1s="Latin", l2s="Français", l3s="Anglais", l4s="Italien", l1="Iesus", l2="Jésus", l3="Jesus", l4="Gesù",
             h8=["Josué aussi"], k8="Un détail étonnant", j1s="Josué (hébreu)", j1="Yehoshoua", j2s="Josué (grec)", j2=GR + " · Iêsous", st8="Le même nom",
             h9=["Un nom très [courant]"], k9="Judée · premier siècle", c9s="On précisait", c9="Jésus de Nazareth", t9="Yeshoua : très courant en Judée",
             h10=["Dire « [Jésus] » ?"], k10="A-t-on le droit ?", st10="Oui", c10="Même nom, une autre langue", h11=["Le [sens] du nom"], k11="Yeshoua", c11="« Le Seigneur sauve »",
             h12=["Tu le [savais] ?"], k12="À toi", cta="Dis-le en commentaire", end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"), chap=("Le nom", "Le sens", "Les langues", "Le sens")) 
elif LANG == "en":
    K = dict(ye1=(1, "Yeshua"), aram=(2, "Aramaic"), hebr=(2, "Hebrew"), ye3=(3, "Yeshua"), yeho=(3, "Yehoshua"), jos=(3, "Joshua"), sei=(4, "Lord"), sauve=(4, "saves"),
             q0=(5, "She"), grec=(6, "Greek"), iesous=(6, "Iēsous"), term=(6, "ending"), lat=(7, "Latin"), iesus=(7, "Iesus"), jesusfr=(7, "Jesus"), jesusen=(7, "Jésus"), gesu=(7, "Gesù"),
             jos8=(8, "Joshua"), ies8=(8, "Iēsous"), meme=(8, "same"), cour=(9, "common"), naz=(9, "Nazareth"), droit=(10, "wrong"), sur=(10, "course"), meme10=(10, "same"),
             ye11=(11, "Yeshua"), sauve11=(11, "saves"), sens=(11, "meaning"), comm=(12, "comments"), abo=(13, "Subscribe"))
    X = dict(h1=["Jesus wasn't called", "“[Jesus]”"], k1="The real name", c1s="His family and friends said", c1="Yeshua",
             h2=["He speaks [Aramaic]"], k2="Galilee · first century", t2a="Aramaic: the everyday language", t2b="Hebrew: probably too",
             h3=["[Yeshua]", "a short form"], k3="The name", c3a="Long form", c3b="Short form", c3c="in English", c3d="Joshua",
             h4=["A name that [saves]"], k4="The usual meaning", c4="“The Lord saves”", st4="Usual meaning", h5=["Matthew [explains]"], k5="Matthew 1:21 · World English Bible",
             q="“She will give birth to a son. You shall call his name Jesus, for it is he who will save his people from their sins.”", qref="Matthew 1:21 · World English Bible",
             h6=["In [Greek]"], k6="The Gospels are written in Greek", g1s="Hebrew · Aramaic", g2s="Greek", st6="+ final s", t6="A Greek ending",
             h7=["Then [Latin]"], k7="Down to our languages", l1s="Latin", l2s="English", l3s="French", l4s="Italian", l1="Iesus", l2="Jesus", l3="Jésus", l4="Gesù",
             h8=["Joshua too"], k8="A surprising detail", j1s="Joshua (Hebrew)", j1="Yehoshua", j2s="Joshua (Greek)", j2=GR + " · Iēsous", st8="The same name",
             h9=["A very [common] name"], k9="Judea · first century", c9s="People added", c9="Jesus of Nazareth", t9="Yeshua: very common in Judea",
             h10=["Saying “[Jesus]”?"], k10="Are we wrong?", st10="Not at all", c10="Same name, another language", h11=["The [meaning] of the name"], k11="Yeshua", c11="“The Lord saves”",
             h12=["Did you [know]?"], k12="Your turn", cta="Tell us in the comments", end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"), chap=("The name", "The meaning", "The languages", "The meaning"))
else:
    K = dict(ye1=(1, "Yeshua"), aram=(2, "aramaico"), hebr=(2, "ebraico"), ye3=(3, "Yeshua"), yeho=(3, "Yehoshua"), jos=(3, "Giosuè"), sei=(4, "Signore"), sauve=(4, "salva"),
             q0=(5, "Ella"), grec=(6, "greco"), iesous=(6, "Iēsous"), term=(6, "desinenza"), lat=(7, "latino"), iesus=(7, "Iesus"), jesusfr=(7, "Jésus"), jesusen=(7, "Jesus"), gesu=(7, "Gesù"),
             jos8=(8, "Giosuè"), ies8=(8, "Iēsous"), meme=(8, "stesso"), cour=(9, "comune"), naz=(9, "Nazaret"), droit=(10, "dire"), sur=(10, "Certo"), meme10=(10, "stesso"),
             ye11=(11, "Yeshua"), sauve11=(11, "salva"), sens=(11, "senso"), comm=(12, "commenti"), abo=(13, "Iscriviti"))
    X = dict(h1=["Gesù non si chiamava", "«[Gesù]»"], k1="Il vero nome", c1s="I suoi cari dicevano", c1="Yeshua",
             h2=["Parla [aramaico]"], k2="Galilea · primo secolo", t2a="Aramaico: la lingua di ogni giorno", t2b="Ebraico: probabilmente anche",
             h3=["[Yeshua]", "forma breve"], k3="Il nome", c3a="Forma lunga", c3b="Forma breve", c3c="in italiano", c3d="Giosuè",
             h4=["Un nome che [salva]"], k4="Il senso comune", c4="«Il Signore salva»", st4="Senso comune", h5=["Matteo [spiega]"], k5="Matteo 1,21 · Riveduta",
             q="«Ella partorirà un figliuolo, e tu gli porrai nome Gesù, perché è lui che salverà il suo popolo dai suoi peccati.»", qref="Matteo 1,21 · Riveduta",
             h6=["In [greco]"], k6="I vangeli sono scritti in greco", g1s="Ebraico · aramaico", g2s="Greco", st6="+ «s» finale", t6="Una desinenza greca",
             h7=["Poi il [latino]"], k7="Fino alle nostre lingue", l1s="Latino", l2s="Francese", l3s="Inglese", l4s="Italiano", l1="Iesus", l2="Jésus", l3="Jesus", l4="Gesù",
             h8=["Anche Giosuè"], k8="Un dettaglio sorprendente", j1s="Giosuè (ebraico)", j1="Yehoshua", j2s="Giosuè (greco)", j2=GR + " · Iēsous", st8="Lo stesso nome",
             h9=["Un nome molto [comune]"], k9="Giudea · primo secolo", c9s="Si precisava", c9="Gesù di Nazaret", t9="Yeshua: molto comune in Giudea",
             h10=["Dire «[Gesù]»?"], k10="Si può?", st10="Certo", c10="Stesso nome, un'altra lingua", h11=["Il [senso] del nome"], k11="Yeshua", c11="«Il Signore salva»",
             h12=["Lo [sapevi]?"], k12="A te", cta="Dillo nei commenti", end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"), chap=("Il nome", "Il senso", "Le lingue", "Il senso"))


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
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("ye1") - 1.2, size=100)
c1 = put(S1, 70, 720, f"<small>{X['c1s']}</small>{X['c1']}<span class='heb' style='font-size:140px;margin-top:10px'>{HE1}</span>", "card", "width:600px;font-size:84px")
blur_in(c1, kk("ye1") - 0.2, 14)
sticker(S1, "jesus-pied", 700, 700, 300, 0.0, rot=3, instant=True)

# --- S2 · araméen, hébreu
t2 = LS[2] - 0.3
cam(t2, S2)
headline(S2, 300, X["h2"], t2 + 0.1, kicker=X["k2"], hl_t=kk("aram"), size=104)
sticker(S2, "jesus-portrait", 640, 900, 270, kk("aram") - 0.2, rot=-3)
tag(S2, 60, 700, X["t2a"], kk("aram") - 0.1, "acc", 38)
tag(S2, 60, 810, X["t2b"], kk("hebr") - 0.1, "", 38)

# --- S3 · Yeshoua, forme courte de Yehoshoua (Josué)
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 300, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("ye3"), size=104)
a3 = put(S3, 70, 700, f"<small>{X['c3a']}</small>Yehoshoua<span class='heb' style='font-size:92px'>{HE2}</span>", "card", "width:440px;font-size:52px")
b3 = put(S3, 560, 700, f"<small>{X['c3b']}</small>Yeshoua<span class='heb' style='font-size:92px'>{HE1}</span>", "card", "width:440px;font-size:52px;border-color:" + ACC)
blur_in(a3, kk("yeho") - 0.4, 14)
blur_in(b3, kk("ye3") - 0.2, 14)
d3 = put(S3, 70, 1040, f"<small>{X['c3c']}</small>{X['c3d']}", "card", "width:600px;font-size:62px")
blur_in(d3, kk("jos") - 0.3, 14)

# --- S4 · « le Seigneur sauve »
t4 = LS[4] - 0.3
cam(t4, S4)
headline(S4, 300, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=kk("sauve"), size=104)
c4 = put(S4, 70, 720, X["c4"], "card", "width:940px;font-size:86px")
blur_in(c4, kk("sei") - 0.3, 14)
stamp(S4, 70, 1000, X["st4"], kk("sauve") + 0.2, rot=-4, size=84)

# --- S5 · Matthieu 1.21 (citation)
t5 = LS[5] - 0.3
cam(t5, S5)
headline(S5, 300, X["h5"], t5 + 0.1, kicker=X["k5"], hl_t=LS[5] + 0.4, size=104)
q_t0 = kk("q0") - 0.05
q_t1 = LS[6] - 0.3
SUPP_Q = (q_t0 - 0.1, q_t1 + 0.2)
kq = kinetic_quote(S5, 60, 700, X["qref"], X["q"], q_t0, q_t1, width=960, size=50)
fade(kq, LS[6] - 0.4)
f5 = tag(S5, 60, 1120, "Matthieu 1.21" if LANG == "fr" else ("Matthew 1:21" if LANG == "en" else "Matteo 1,21"), LS[5] + 0.2, "", 44)
fade(f5, q_t0 - 0.1)

# --- S6 · le grec : Yeshoua devient Iêsous, avec un « s » final
t6 = LS[6] - 0.3
cam(t6, S6)
headline(S6, 300, X["h6"], t6 + 0.1, kicker=X["k6"], hl_t=kk("grec"), size=112)
g1 = put(S6, 70, 700, f"<small>{X['g1s']}</small>Yeshoua", "card", "width:940px;font-size:56px")
blur_in(g1, LS[6] + 0.3, 14)
g2 = put(S6, 70, 880, f"<small>{X['g2s']}</small>{GR}<br />Iêsous" if LANG == "fr" else f"<small>{X['g2s']}</small>{GR}<br />Iēsous", "card", "width:940px;font-size:58px;border-color:" + ACC)
blur_in(g2, kk("iesous") - 0.3, 14)
stamp(S6, 100, 1190, X["st6"], kk("term") - 0.2, rot=-4, size=44)

# --- S7 · le latin, puis les langues d'Europe
t7 = LS[7] - 0.3
cam(t7, S7)
headline(S7, 300, X["h7"], t7 + 0.1, kicker=X["k7"], hl_t=kk("lat"), size=112)
tag(S7, 60, 1200, "Iesus → Jésus · Jesus · Gesù", LS[7] + 0.3, "acc", 42)
ll = [("l1", 70, 720, "iesus"), ("l2", 560, 720, "jesusfr"), ("l3", 70, 960, "jesusen"), ("l4", 560, 960, "gesu")]
for key, x, y, a in ll:
    bx = put(S7, x, y, f"<small>{X[key + 's']}</small>{X[key]}", "card", "width:440px;font-size:64px" + (";border-color:" + ACC if key == "l1" else ""))
    blur_in(bx, kk(a) - 0.3, 14)

# --- S8 · Josué s'appelle aussi Iêsous
t8 = LS[8] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=kk("jos8"), size=108)
f8 = tag(S8, 60, 700, "Yehoshua → Iēsous", LS[8] + 0.2, "acc", 46)
fade(f8, kk("jos8") - 0.4)
j1 = put(S8, 70, 700, f"<small>{X['j1s']}</small>{X['j1']}<span class='heb' style='font-size:80px'>{HE2}</span>", "card", "width:940px;font-size:56px")
blur_in(j1, kk("jos8") - 0.2, 14)
j2 = put(S8, 70, 1000, f"<small>{X['j2s']}</small>{X['j2']}", "card", "width:940px;font-size:56px;border-color:" + ACC)
blur_in(j2, kk("ies8") - 0.3, 14)
stamp(S8, 70, 1190, X["st8"], kk("meme") - 0.2, rot=-4, size=60)

# --- S9 · nom très courant
t9 = LS[9] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=kk("cour"), size=100)
tag(S9, 60, 700, X["t9"], kk("cour") - 0.5, "acc", 40)
c9 = put(S9, 70, 820, f"<small>{X['c9s']}</small>{X['c9']}", "card", "width:940px;font-size:62px")
blur_in(c9, kk("naz") - 0.5, 14)
sticker(S9, "jesus-pied", 700, 1010, 220, kk("naz") - 0.3, rot=3)

# --- S10 · a-t-on le droit de dire « Jésus » ?
t10 = LS[10] - 0.3
cam(t10, S10)
headline(S10, 300, X["h10"], t10 + 0.1, kicker=X["k10"], hl_t=kk("droit"), size=112)
stamp(S10, 70, 740, X["st10"], kk("sur") - 0.1, rot=-4, size=110)
c10 = put(S10, 70, 1000, X["c10"], "card", "width:940px;font-size:62px")
blur_in(c10, kk("meme10") - 0.3, 14)

# --- S11 · le sens du nom
t11 = LS[11] - 0.3
cam(t11, S11)
headline(S11, 300, X["h11"], t11 + 0.1, kicker=X["k11"], hl_t=kk("sens"), size=104)
c11 = put(S11, 70, 690, f"<small>{X['k11']}</small>{X['c11']}<span class='heb' style='font-size:90px;margin-top:6px'>{HE1}</span>", "card", "width:940px;font-size:72px")
blur_in(c11, kk("ye11") - 0.2, 14)
sticker(S11, "jesus-portrait", 700, 980, 230, kk("sauve11") - 0.2, rot=3)

# --- S12 · appel à commenter
t12 = LS[12] - 0.3
cam(t12, S12)
headline(S12, 300, X["h12"], t12 + 0.1, kicker=X["k12"], hl_t=LS[12] + 0.5, size=120)
sticker(S12, "jesus-portrait", 560, 700, 380, t12 + 0.3, rot=3)
cta = put(S12, 70, 1170, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>' + X["cta"], "cta")
blur_in(cta, kk("comm") - 1.2, 14)
sfx("click", kk("comm") - 1.2, 0.8)

t_end = kk("abo") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", X["chap"][0], 0, LS[4]), ("02", X["chap"][1], LS[4], LS[6]), ("03", X["chap"][2], LS[6], LS[9]), ("04", X["chap"][3], LS[9], DUR_)],
    suppress=[SUPP_Q, (kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("jesus-pied", 30, 1480, 240, -6), ("jesus-portrait", 800, 1480, 230, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
