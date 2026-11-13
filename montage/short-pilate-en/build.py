"""Short « La pierre de Ponce Pilate (Césarée, 1961) » — style 02, 9:16.

Même fichier dans les trois dossiers (short-pilate = FR, -en, -it) : la langue vient du nom du dossier.
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
THEME = {"brand": BRAND, "title": BRAND + " - La pierre de Pilate - style 02", "lang": LANG,
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
    K = dict(pierre=(1, "pierre"), cesaree=(2, "Césarée"), theatre=(2, "théâtre"), ital=(3, "italienne"), calc=(3, "calcaire"), marche=(3, "marche"),
             latin=(4, "latin"), pont=(4, "Pontius"), pref=(4, "préfet"), tib=(5, "Tiberieum"), disc=(5, "discutée"), g26=(6, "26"), g36=(6, "36"),
             luc=(7, "Luc"), q0=(7, "La"), gouv=(8, "gouverneur"), pref8=(8, "préfet"), gen=(8, "général"), jos=(9, "Josèphe"), phi=(9, "Philon"), tac=(9, "Tacite"),
             cele=(9, "célèbre"), mont=(10, "montre"), exi=(10, "existé"), nemont=(11, "montre"), proc=(11, "procès"), musee=(12, "musée"), copie=(12, "copie"),
             comm=(13, "commentaire"), abo=(14, "Abonne-toi"))
    X = dict(h1=["Une [pierre],", "un nom"], k1="Césarée · 1961", lab1="Inscription de Pilate", lab1s="Musée d'Israël, Jérusalem", h2=["[Césarée],", "côte de la Méditerranée"], k2="Un théâtre romain en ruines",
             t2a="Césarée", t2b="Théâtre romain", h3=["Un bloc de [calcaire]"], k3="Une équipe italienne", t3a="Équipe italienne", t3b="Réemploi : marche d'escalier",
             h4=["[Pontius] Pilatus"], k4="Inscription en latin", c4s="Lignes 2 et 3 · lecture courante", c4a="PONTIUS PILATUS", c4b="PRAEFECTUS IUDAEAE", st4="Préfet de Judée",
             h5=["Une lecture [discutée]"], k5="La première ligne", c5s="Ligne 1 · incomplète", c5="…TIBERIEUM", t5="Un édifice pour Tibère ?", ring_lab="Tibère, intaglio sur bague", ring_sub="vers 14–37 · Met",
             h6=["Pilate, [préfet]", "de Judée"], k6="Sous l'empereur Tibère", c6="de l'an 26 à l'an 36 environ", t7="L'évangile de Luc", h7=["Luc le [situe]"], k7="Luc 3.1 · Louis Segond 1910",
             q="« La quinzième année du règne de l'empereur Tibère, Ponce Pilate étant gouverneur de la Judée. »", qref="Luc 3.1 · Louis Segond 1910",
             h8=["« [Gouverneur] »", "ou « préfet » ?"], k8="Le titre", b1s="Luc écrit", b1="gouverneur", b2s="La pierre donne", b2="préfet", t8="« Gouverneur » : mot plus général",
             h9=["Pilate, déjà [connu]"], k9="Les autres sources", s1="Josèphe", s1s="historien juif", s2="Philon", s2s="philosophe", s3="Tacite", s3s="historien romain", t9="La trace gravée la plus célèbre",
             h10=["Ce que la [pierre]", "montre"], k10="Et ce qu'elle ne montre pas", m1s="Elle montre", m1="Un préfet romain nommé Pilate a existé", m2s="Elle ne montre pas", m2="Le procès de Jésus", st10="Textes ≠ pierre",
             h11=["Où est-elle [aujourd'hui] ?"], k11="Original et copie", o1s="Original", o1="Musée d'Israël, Jérusalem", o2s="Copie", o2="Césarée, là où elle fut trouvée",
             h12=["Quel autre [nom] ?"], k12="À toi", cta="Dis-le en commentaire", end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"),
             chap=("La découverte", "L'inscription", "Les sources", "La pierre"), credit_th="Théâtre de Césarée · Berthold Werner")
elif LANG == "en":
    K = dict(pierre=(1, "stone"), cesaree=(2, "Caesarea"), theatre=(2, "theater"), ital=(3, "Italian"), calc=(3, "limestone"), marche=(3, "step"),
             latin=(4, "Latin"), pont=(4, "Pontius"), pref=(4, "prefect"), tib=(5, "Tiberieum"), disc=(5, "debated"), g26=(6, "26"), g36=(6, "36"),
             luc=(7, "Luke"), q0=(7, "Now"), gouv=(8, "governor"), pref8=(8, "prefect"), gen=(8, "general"), jos=(9, "Josephus"), phi=(9, "Philo"), tac=(9, "Tacitus"),
             cele=(9, "famous"), mont=(10, "shows"), exi=(10, "existed"), nemont=(11, "doesn't"), proc=(11, "trial"), musee=(12, "Museum"), copie=(12, "copy"),
             comm=(13, "comments"), abo=(14, "Subscribe"))
    X = dict(h1=["A [stone],", "a name"], k1="Caesarea · 1961", lab1="The Pilate inscription", lab1s="Israel Museum, Jerusalem", h2=["[Caesarea],", "Mediterranean coast"], k2="A ruined Roman theater",
             t2a="Caesarea", t2b="Roman theater", h3=["A block of [limestone]"], k3="An Italian team", t3a="Italian team", t3b="Reused: a stair step",
             h4=["[Pontius] Pilatus"], k4="A Latin inscription", c4s="Lines 2 and 3 · common reading", c4a="PONTIUS PILATUS", c4b="PRAEFECTUS IUDAEAE", st4="Prefect of Judea",
             h5=["A [debated] reading"], k5="The first line", c5s="Line 1 · incomplete", c5="…TIBERIEUM", t5="A building for Tiberius?", ring_lab="Tiberius, intaglio on a ring", ring_sub="ca. AD 14–37 · Met",
             h6=["Pilate, [prefect]", "of Judea"], k6="Under the emperor Tiberius", c6="from about AD 26 to 36", t7="The Gospel of Luke", h7=["Luke [places] him"], k7="Luke 3:1 · World English Bible",
             q="“Now in the fifteenth year of the reign of Tiberius Caesar, Pontius Pilate being governor of Judea.”", qref="Luke 3:1 · World English Bible",
             h8=["“[Governor]”", "or “prefect”?"], k8="The title", b1s="Luke writes", b1="governor", b2s="The stone gives", b2="prefect", t8="“Governor”: a more general word",
             h9=["Pilate, already [known]"], k9="Other sources", s1="Josephus", s1s="Jewish historian", s2="Philo", s2s="philosopher", s3="Tacitus", s3s="Roman historian", t9="The most famous engraved trace",
             h10=["What the [stone]", "shows"], k10="And what it doesn't show", m1s="It shows", m1="A Roman prefect named Pilate existed", m2s="It doesn't show", m2="The trial of Jesus", st10="Texts ≠ stone",
             h11=["Where is it [today]?"], k11="Original and copy", o1s="Original", o1="Israel Museum, Jerusalem", o2s="Copy", o2="Caesarea, where it was found",
             h12=["Which other [name]?"], k12="Your turn", cta="Tell us in the comments", end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"),
             chap=("The discovery", "The inscription", "The sources", "The stone"), credit_th="Caesarea theater · Berthold Werner")
else:
    K = dict(pierre=(1, "pietra"), cesaree=(2, "Cesarea"), theatre=(2, "teatro"), ital=(3, "italiana"), calc=(3, "calcare"), marche=(3, "gradino"),
             latin=(4, "latino"), pont=(4, "Pontius"), pref=(4, "prefetto"), tib=(5, "Tiberieum"), disc=(5, "discussa"), g26=(6, "ventisei"), g36=(6, "trentasei"),
             luc=(7, "Luca"), q0=(7, "Nell'anno"), gouv=(8, "governatore"), pref8=(8, "prefetto"), gen=(8, "generale"), jos=(9, "Giuseppe"), phi=(9, "Filone"), tac=(9, "Tacito"),
             cele=(9, "famosa"), mont=(10, "mostra"), exi=(10, "esistito"), nemont=(11, "non"), proc=(11, "processo"), musee=(12, "Museo"), copie=(12, "copia"),
             comm=(13, "commenti"), abo=(14, "Iscriviti"))
    X = dict(h1=["Una [pietra],", "un nome"], k1="Cesarea · 1961", lab1="L'iscrizione di Pilato", lab1s="Museo d'Israele, Gerusalemme", h2=["[Cesarea],", "costa del Mediterraneo"], k2="Un teatro romano in rovina",
             t2a="Cesarea", t2b="Teatro romano", h3=["Un blocco di [calcare]"], k3="Una squadra italiana", t3a="Squadra italiana", t3b="Riutilizzo: gradino di scala",
             h4=["[Pontius] Pilatus"], k4="Iscrizione in latino", c4s="Righe 2 e 3 · lettura comune", c4a="PONTIUS PILATUS", c4b="PRAEFECTUS IUDAEAE", st4="Prefetto di Giudea",
             h5=["Una lettura [discussa]"], k5="La prima riga", c5s="Riga 1 · incompleta", c5="…TIBERIEUM", t5="Un edificio per Tiberio?", ring_lab="Tiberio, intaglio su anello", ring_sub="circa 14–37 · Met",
             h6=["Pilato, [prefetto]", "di Giudea"], k6="Sotto l'imperatore Tiberio", c6="dal 26 al 36 circa", t7="Il vangelo di Luca", h7=["Luca lo [colloca]"], k7="Luca 3,1 · Riveduta",
             q="«Nell'anno quindicesimo dell'impero di Tiberio Cesare, mentre Ponzio Pilato governava la Giudea.»", qref="Luca 3,1 · Riveduta",
             h8=["«[Governatore]»", "o «prefetto»?"], k8="Il titolo", b1s="Luca scrive", b1="governatore", b2s="La pietra dà", b2="prefetto", t8="«Governatore»: parola più generale",
             h9=["Pilato, già [noto]"], k9="Altre fonti", s1="Giuseppe Flavio", s1s="storico ebreo", s2="Filone", s2s="filosofo", s3="Tacito", s3s="storico romano", t9="La traccia incisa più famosa",
             h10=["Ciò che la [pietra]", "mostra"], k10="E ciò che non mostra", m1s="Mostra", m1="Un prefetto romano di nome Pilato è esistito", m2s="Non mostra", m2="Il processo a Gesù", st10="Testi ≠ pietra",
             h11=["Dov'è [oggi]?"], k11="Originale e copia", o1s="Originale", o1="Museo d'Israele, Gerusalemme", o2s="Copia", o2="Cesarea, dove fu scoperta",
             h12=["Quale altro [nome]?"], k12="A te", cta="Dillo nei commenti", end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"),
             chap=("La scoperta", "L'iscrizione", "Le fonti", "La pietra"), credit_th="Teatro di Cesarea · Berthold Werner")


def kk(name, n=0):
    k = K[name]
    return AL(k[1], k[0], k[2] if len(k) > 2 else n)


html.append('<style>'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

ST = [(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (1, 3), (0, 3)]
S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12 = ST

# --- S1 · accroche : la pierre dès la première image
cam(0, S1)
sticker(S1, "pierre-pilate", 50, 690, 500, 0.0, rot=-2, instant=True)
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("pierre") + 0.1, size=112)
label_box(S1, 580, 720, X["lab1"], X["lab1s"], 0.9)

# --- S2 · Césarée, un théâtre romain
t2 = LS[2] - 0.3
cam(t2, S2)
headline(S2, 300, X["h2"], t2 + 0.1, kicker=X["k2"], hl_t=kk("cesaree"), size=100)
counter(S2, 70, 740, 1951, 1961, kk("cesaree") - 0.2, 1.6, unit="", size=300)
ring(S2, 560, 880, kk("theatre"), size=420)
tag(S2, 60, 1130, X["t2a"], kk("cesaree") - 0.1, "acc", 48)
tag(S2, 60, 1240, X["t2b"], kk("theatre") - 0.1, "", 48)

# --- S3 · une équipe italienne, un bloc de calcaire, une marche d'escalier
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 300, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("calc"), size=100)
sticker(S3, "pierre-pilate", 50, 690, 440, kk("calc") - 0.2, rot=3)
tag(S3, 540, 720, X["t3a"], kk("ital") - 0.2, "", 38)
tag(S3, 540, 830, X["t3b"], kk("marche") - 0.3, "acc", 34)

# --- S4 · l'inscription latine : Pontius Pilatus, préfet de Judée
t4 = LS[4] - 0.3
cam(t4, S4)
headline(S4, 300, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=kk("pont"), size=108)
c4 = put(S4, 70, 700, f"<small>{X['c4s']}</small>{X['c4a']}<br />{X['c4b']}", "card", "width:940px;font-size:74px;letter-spacing:2px")
blur_in(c4, LS[4] + 0.5, 14)
stamp(S4, 70, 1080, X["st4"], kk("pref") - 0.1, rot=-4, size=92)
hit(kk("pref"), 0.9)

# --- S5 · la première ligne : « Tiberieum », lecture discutée
t5 = LS[5] - 0.3
cam(t5, S5)
headline(S5, 300, X["h5"], t5 + 0.1, kicker=X["k5"], hl_t=kk("disc") - 0.5, size=104)
c5 = put(S5, 70, 700, f"<small>{X['c5s']}</small>{X['c5']}", "card", "width:940px;font-size:84px;letter-spacing:2px")
blur_in(c5, LS[5] + 0.6, 14)
sticker(S5, "anneau-tibere", 740, 930, 215, kk("tib") - 0.2, rot=3)
label_box(S5, 60, 960, X["ring_lab"], X["ring_sub"], kk("tib") + 0.1)
tag(S5, 60, 1120, X["t5"], kk("tib") + 0.4, "acc", 44)

# --- S6 · de l'an 26 à l'an 36
t6 = LS[6] - 0.3
cam(t6, S6)
headline(S6, 300, X["h6"], t6 + 0.1, kicker=X["k6"], hl_t=kk("g26"), size=100)
counter(S6, 70, 760, 26, 36, kk("g26") - 0.3, kk("g36") - kk("g26") + 0.4, unit="", size=300)
tag(S6, 70, 1130, X["c6"], kk("g26"), "acc", 50)

# --- S7 · la citation de Luc
t7 = LS[7] - 0.3
cam(t7, S7)
headline(S7, 300, X["h7"], t7 + 0.1, kicker=X["k7"], hl_t=kk("luc"), size=104)
f7 = tag(S7, 60, 700, X["t7"], LS[7] + 0.2, "", 52)
q_t0 = kk("q0") - 0.05
q_t1 = LS[8] - 0.3
fade(f7, q_t0 - 0.2)
SUPP_Q = (q_t0 - 0.1, q_t1 + 0.2)
kq = kinetic_quote(S7, 60, 700, X["qref"], X["q"], q_t0, q_t1, width=960, size=48)
fade(kq, LS[8] - 0.4)

# --- S8 · gouverneur ou préfet ?
t8 = LS[8] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=kk("gouv"), size=104)
bb1 = put(S8, 70, 700, f"<small>{X['b1s']}</small>{X['b1']}", "card", "width:440px;font-size:66px")
bb2 = put(S8, 560, 700, f"<small>{X['b2s']}</small>{X['b2']}", "card", "width:440px;font-size:66px;border-color:" + ACC)
blur_in(bb1, kk("gouv") - 0.3, 14)
blur_in(bb2, kk("pref8") - 0.2, 14)
tag(S8, 70, 1020, X["t8"], kk("gen") - 0.2, "acc", 48)
hit(kk("pref8"), 0.9)

# --- S9 · d'autres sources parlent de lui
t9 = LS[9] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=kk("jos"), size=104)
for n, (k, y) in enumerate((("jos", 700), ("phi", 880), ("tac", 1060))):
    key = "s%d" % (n + 1)
    bx = put(S9, 70, y, f"<small>{X[key + 's']}</small>{X[key]}", "card", "width:860px;font-size:58px")
    blur_in(bx, kk(k) - 0.3, 14)
tag(S9, 70, 1250, X["t9"], kk("cele") - 0.3, "acc", 42)

# --- S10 · ce qu'elle montre, ce qu'elle ne montre pas
t10 = LS[10] - 0.3
cam(t10, S10)
headline(S10, 300, X["h10"], t10 + 0.1, kicker=X["k10"], hl_t=kk("mont"), size=104)
mm1 = put(S10, 70, 700, f"<small>{X['m1s']}</small>{X['m1']}", "card", "width:940px;font-size:62px")
blur_in(mm1, kk("mont") - 0.3, 14)
gone([mm1], LS[11] - 0.5)
mm2 = put(S10, 70, 700, f"<small>{X['m2s']}</small>{X['m2']}", "card", "width:940px;font-size:66px;border-color:" + ACC)
blur_in(mm2, kk("nemont") - 0.3, 14)
stamp(S10, 70, 1080, X["st10"], kk("proc") - 0.1, rot=-4, size=88)

# --- S11 · où est la pierre aujourd'hui ?
t11 = LS[12] - 0.3
cam(t11, S11)
headline(S11, 300, X["h11"], t11 + 0.1, kicker=X["k11"], hl_t=kk("musee"), size=104)
oo1 = put(S11, 70, 700, f"<small>{X['o1s']}</small>{X['o1']}", "card", "width:940px;font-size:62px")
oo2 = put(S11, 70, 990, f"<small>{X['o2s']}</small>{X['o2']}", "card", "width:940px;font-size:62px;border-color:" + ACC)
blur_in(oo1, kk("musee") - 0.3, 14)
blur_in(oo2, kk("copie") - 0.3, 14)

# --- S12 · appel à commenter
t12 = LS[13] - 0.3
cam(t12, S12)
headline(S12, 300, X["h12"], t12 + 0.1, kicker=X["k12"], hl_t=kk("comm") - 2.0, size=112)
sticker(S12, "anneau-tibere", 600, 640, 330, t12 + 0.3, rot=3)
sticker(S12, "pierre-pilate", 40, 700, 430, t12 + 0.5, rot=-3)
cta = put(S12, 70, 1230, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>' + X["cta"], "cta")
blur_in(cta, kk("comm") - 1.2, 14)
sfx("click", kk("comm") - 1.2, 0.8)

t_end = kk("abo") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", X["chap"][0], 0, t4), ("02", X["chap"][1], t4, t9), ("03", X["chap"][2], t9, t10), ("04", X["chap"][3], t10, DUR_)],
    suppress=[SUPP_Q, (kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("pierre-pilate", 30, 1500, 300, -6), ("anneau-tibere", 820, 1480, 150, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
