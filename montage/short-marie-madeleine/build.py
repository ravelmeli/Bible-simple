"""Short « Rien dans la Bible ne dit que Marie-Madeleine était une prostituée » — style 02, 9:16.

Même fichier dans les trois dossiers (short-marie-madeleine = FR, -en, -it) : la langue vient du nom du dossier.
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
THEME = {"brand": BRAND, "title": BRAND + " - Marie-Madeleine - style 02", "lang": LANG,
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
    K = dict(prost=(1, "prostituée"), mad=(1, "Marie-Madeleine"), magd=(2, "Magdala"), gal=(2, "Galilée"), luc=(3, "Luc"), marie=(3, "Marie"),
             dem4=(4, "démons"), pech=(4, "péchés"), pros4=(4, "prostitution"), mel=(5, "mélange"), pecheresse=(5, "pécheresse"), pieds=(5, "pieds"),
             n591=(6, "591"), greg=(6, "Grégoire"), sie=(6, "siècles"), aucun=(7, "aucun"), n1969=(7, "1969"), croix=(8, "croix"), prem=(8, "première"),
             n2016=(9, "2016"), apo=(9, "apôtres"), idee=(10, "idée"), comm=(10, "commentaire"), abo=(11, "Abonne-toi"))
    X = dict(h1=["Pas une [prostituée]"], k1="Marie-Madeleine", q1="Marie-Madeleine", st1="Aucun texte biblique",
             h2=["[Magdala]"], k2="Son nom", c2s="Son nom", c2="Magdala", t2="Au bord du lac de Galilée",
             h3=["Luc [8.2]"], k3="Le premier texte", q3="« Marie, dite de Magdala, de laquelle étaient sortis sept démons. »", r3="Luc 8.2 · Louis Segond 1910", f3="Le premier texte qui parle d'elle",
             h4=["Sept démons, pas de [péchés]"], k4="Ce que dit le texte", t4a="Sept démons", t4b="Pas de péchés", st4="Jamais de prostitution",
             h5=["Un [mélange]"], k5="D'où vient l'idée ?", c5s="Luc 7 · sans nom", c5="Une femme pécheresse", t5="Elle parfume les pieds de Jésus",
             h6=["591 : Grégoire le [Grand]"], k6="Une homélie", c6="591 · Grégoire le Grand", t6a="Identifie les deux femmes", t6b="Lecture dominante en Occident",
             h7=["Aucun passage ne les [identifie]"], k7="Mais", st7="Aucun passage biblique", c7s="Église catholique", c7="1969 : calendrier liturgique",
             h8=["Ce que disent les [Évangiles]"], k8="Marie de Magdala", t8a="Elle suit Jésus", t8b="Présente à la croix", t8c="Première à voir le ressuscité",
             h9=["« Apôtre des [apôtres] »"], k9="2016", c9s="Pape François · 2016", c9="« Apôtre des apôtres »",
             h10=["Quelle [idée] reçue ?"], k10="À toi", c10="Quelle idée reçue sur la Bible t'a le plus surpris ?", cta="Dis-le en commentaire",
             end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"), chap=("Le texte", "L'origine", "Ce qu'on sait", "Pour toi"))
elif LANG == "en":
    K = dict(prost=(1, "prostitute"), mad=(1, "Magdalene"), magd=(2, "Magdala"), gal=(2, "Galilee"), luc=(3, "Luke"), marie=(3, "Mary"),
             dem4=(4, "demons"), pech=(4, "sins"), pros4=(4, "prostitution"), mel=(5, "mix-up"), pecheresse=(5, "sinful"), pieds=(5, "feet"),
             n591=(6, "591"), greg=(6, "Gregory"), sie=(6, "centuries"), aucun=(7, "identifies"), n1969=(7, "1969"), croix=(8, "cross"), prem=(8, "first"),
             n2016=(9, "2016"), apo=(9, "apostles"), idee=(10, "idea"), comm=(10, "comments"), abo=(11, "Subscribe"))
    X = dict(h1=["Not a [prostitute]"], k1="Mary Magdalene", q1="Mary Magdalene", st1="No biblical text",
             h2=["[Magdala]"], k2="Her name", c2s="Her name", c2="Magdala", t2="On the Sea of Galilee",
             h3=["Luke [8:2]"], k3="The first text", q3="“Mary who was called Magdalene, from whom seven demons had gone out.”", r3="Luke 8:2 · World English Bible", f3="The first text that mentions her",
             h4=["Seven demons, not [sins]"], k4="What the text says", t4a="Seven demons", t4b="Not sins", st4="Never prostitution",
             h5=["A [mix-up]"], k5="Where does the idea come from?", c5s="Luke 7 · unnamed", c5="A sinful woman", t5="She anoints the feet of Jesus",
             h6=["591: Gregory the [Great]"], k6="A homily", c6="591 · Gregory the Great", t6a="Identifies the two women", t6b="The dominant reading in the West",
             h7=["No passage [identifies] them"], k7="But", st7="No biblical passage", c7s="Catholic Church", c7="1969: liturgical calendar",
             h8=["What the [Gospels] say"], k8="Mary of Magdala", t8a="She follows Jesus", t8b="Present at the cross", t8c="First to see the risen Christ",
             h9=["“Apostle of the [apostles]”"], k9="2016", c9s="Pope Francis · 2016", c9="“Apostle of the apostles”",
             h10=["Which [idea]?"], k10="Your turn", c10="Which common idea about the Bible surprised you the most?", cta="Tell us in the comments",
             end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"), chap=("The text", "The origin", "What we know", "For you"))
else:
    K = dict(prost=(1, "prostituta"), mad=(1, "Maddalena"), magd=(2, "Magdala"), gal=(2, "Galilea"), luc=(3, "Luca"), marie=(3, "Maria"),
             dem4=(4, "demoni"), pech=(4, "peccati"), pros4=(4, "prostituzione"), mel=(5, "confusione"), pecheresse=(5, "peccatrice"), pieds=(5, "piedi"),
             n591=(6, "591"), greg=(6, "Gregorio"), sie=(6, "secoli"), aucun=(7, "nessun"), n1969=(7, "1969"), croix=(8, "croce"), prem=(8, "prima"),
             n2016=(9, "2016"), apo=(9, "apostola"), idee=(10, "idea"), comm=(10, "commenti"), abo=(11, "Iscriviti"))
    X = dict(h1=["Non una [prostituta]"], k1="Maria Maddalena", q1="Maria Maddalena", st1="Nessun testo biblico",
             h2=["[Magdala]"], k2="Il suo nome", c2s="Il suo nome", c2="Magdala", t2="Sulla riva del lago di Galilea",
             h3=["Luca [8,2]"], k3="Il primo testo", q3="«Maria detta Maddalena, dalla quale erano usciti sette demoni.»", r3="Luca 8,2 · Riveduta", f3="Il primo testo che parla di lei",
             h4=["Sette demoni, non [peccati]"], k4="Che cosa dice il testo", t4a="Sette demoni", t4b="Non peccati", st4="Mai prostituzione",
             h5=["Una [confusione]"], k5="Da dove viene l'idea?", c5s="Luca 7 · senza nome", c5="Una donna peccatrice", t5="Cosparge di profumo i piedi di Gesù",
             h6=["591: Gregorio [Magno]"], k6="Un'omelia", c6="591 · Gregorio Magno", t6a="Identifica le due donne", t6b="Lettura dominante in Occidente",
             h7=["Nessun passo le [identifica]"], k7="Ma", st7="Nessun passo biblico", c7s="Chiesa cattolica", c7="1969: calendario liturgico",
             h8=["Che cosa dicono i [Vangeli]"], k8="Maria di Magdala", t8a="Segue Gesù", t8b="Presente alla croce", t8c="La prima a vedere il risorto",
             h9=["«[Apostola] degli apostoli»"], k9="2016", c9s="Papa Francesco · 2016", c9="«Apostola degli apostoli»",
             h10=["Quale [idea]?"], k10="A te", c10="Quale idea comune sulla Bibbia ti ha sorpreso di più?", cta="Dillo nei commenti",
             end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"), chap=("Il testo", "L'origine", "Quel che si sa", "Per te"))


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
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("prost") - 0.3, size=104)
sticker(S1, "livres", 60, 720, 250, 0.0, rot=-2, instant=True)
q1 = put(S1, 340, 740, X["q1"], "card", "width:670px;font-size:56px")
blur_in(q1, 0.25, 14)
stamp(S1, 70, 1070, X["st1"], kk("prost") - 0.1, rot=-3, size=48)
hit(kk("prost"), 0.9)

# --- S2 · Magdala
t2 = LS[2] - 0.3
cam(t2, S2)
headline(S2, 300, X["h2"], t2 + 0.1, kicker=X["k2"], hl_t=kk("magd") - 0.3, size=130)
c2 = put(S2, 70, 720, f"<small>{X['c2s']}</small>{X['c2']}", "card", "width:940px;font-size:76px")
blur_in(c2, early(kk("magd") - 0.3, 2, 0.9), 14)
tag(S2, 70, 960, X["t2"], kk("gal") - 0.5, "acc", 54)
sticker(S2, "porte-ville", 70, 1080, 300, LS[2] + 1.2, rot=-2)

# --- S3 · Luc 8.2
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 300, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("luc") - 0.3, size=120)
q3_t0 = kk("marie") - 0.05
q3_t1 = LS[4] - 0.3
f3 = tag(S3, 60, 720, X["f3"], LS[3] + 0.2, "", 46)
fade(f3, q3_t0 - 0.2)
kq3 = kinetic_quote(S3, 60, 720, X["r3"], X["q3"], q3_t0, q3_t1, width=960, size=56)
fade(kq3, LS[4] - 0.4)

# --- S4 · sept démons, pas de péchés
t4 = LS[4] - 0.3
cam(t4, S4)
headline(S4, 300, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=kk("pech") - 0.3, size=88)
tag(S4, 70, 720, X["t4a"], early(kk("dem4") - 0.3, 4, 0.9), "", 58)
tag(S4, 70, 860, X["t4b"], kk("pech") - 0.3, "", 58)
stamp(S4, 70, 1000, X["st4"], kk("pros4") - 0.3, rot=-3, size=48)

# --- S5 · un mélange
t5 = LS[5] - 0.3
cam(t5, S5)
headline(S5, 300, X["h5"], t5 + 0.1, kicker=X["k5"], hl_t=kk("mel") - 0.3, size=120)
c5 = put(S5, 70, 720, f"<small>{X['c5s']}</small>{X['c5']}", "card", "width:940px;font-size:62px")
blur_in(c5, early(kk("mel") + 0.6, 5, 1.6), 14)
tag(S5, 70, 980, X["t5"], kk("pieds") - 0.8, "acc", 50)
sticker(S5, "rouleau", 70, 1090, 230, LS[5] + 2.2, rot=-2)

# --- S6 · 591, Grégoire
t6 = LS[6] - 0.3
cam(t6, S6)
headline(S6, 300, X["h6"], t6 + 0.1, kicker=X["k6"], hl_t=kk("greg") - 0.3, size=96)
c6 = put(S6, 70, 720, X["c6"], "card", "width:740px;font-size:58px")
blur_in(c6, early(kk("n591") - 0.3, 6, 0.9), 14)
tag(S6, 70, 900, X["t6a"], kk("greg") + 0.5, "", 50)
tag(S6, 70, 1040, X["t6b"], kk("sie") - 0.8, "acc", 50)
sticker(S6, "pretre", 860, 720, 150, LS[6] + 0.8, rot=2)

# --- S7 · aucun passage ; 1969
t7 = LS[7] - 0.3
cam(t7, S7)
headline(S7, 300, X["h7"], t7 + 0.1, kicker=X["k7"], hl_t=kk("aucun") - 0.3, size=88)
stamp(S7, 70, 720, X["st7"], early(kk("aucun") - 0.3, 7, 0.9), rot=-3, size=48)
c7 = put(S7, 70, 960, f"<small>{X['c7s']}</small>{X['c7']}", "card", "width:940px;font-size:58px;border-color:" + ACC)
blur_in(c7, kk("n1969") - 0.6, 14)

# --- S8 · ce que disent les Évangiles
t8 = LS[8] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=LS[8] + 0.5, size=88)
tag(S8, 70, 720, X["t8a"], early(LS[8] + 0.8, 8, 1.2), "", 54)
tag(S8, 70, 860, X["t8b"], kk("croix") - 0.4, "", 54)
tag(S8, 70, 1000, X["t8c"], kk("prem") - 0.4, "acc", 50)

# --- S9 · apôtre des apôtres
t9 = LS[9] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=kk("apo") - 0.3, size=100)
c9 = put(S9, 70, 720, f"<small>{X['c9s']}</small>{X['c9']}", "card", "width:940px;font-size:66px;border-color:" + ACC)
blur_in(c9, early(kk("n2016") - 0.3, 9, 0.9), 14)

# --- S10 · commentaire
t10 = LS[10] - 0.3
cam(t10, S10)
headline(S10, 300, X["h10"], t10 + 0.1, kicker=X["k10"], hl_t=kk("idee") - 0.2, size=104)
c10 = put(S10, 70, 720, X["c10"], "card", "width:940px;font-size:56px")
blur_in(c10, LS[10] + 0.4, 14)
cta = put(S10, 70, 1080, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>' + X["cta"], "cta")
blur_in(cta, kk("comm") - 1.2, 14)
sfx("click", kk("comm") - 1.2, 0.8)

t_end = kk("abo") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", X["chap"][0], 0, LS[4]), ("02", X["chap"][1], LS[4], LS[7]), ("03", X["chap"][2], LS[7], LS[10]), ("04", X["chap"][3], LS[10], DUR_)],
    suppress=[(q3_t0 - 0.1, q3_t1 + 0.2), (kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("foule", 30, 1450, 420, -4), ("jesus-pied", 800, 1480, 200, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
