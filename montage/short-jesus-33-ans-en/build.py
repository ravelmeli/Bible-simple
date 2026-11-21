"""Short « La Bible ne dit jamais que Jésus est mort à 33 ans » — style 02, 9:16.

Même fichier dans les trois dossiers (short-jesus-33-ans = FR, -en, -it) : la langue vient du nom du dossier.
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
THEME = {"brand": BRAND, "title": BRAND + " - Jesus 33 ans - style 02", "lang": LANG,
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
    K = dict(n33=(1, "33"), jamais=(1, "jamais"), verset=(2, "verset"), age2=(2, "âge"), luc=(3, "Luc"), jesus=(3, "Jésus"), trente=(3, "trente"),
             env=(4, "environ"), exact=(4, "exact"), compter=(5, "compter"), trois=(5, "trois"), ans5=(5, "ans"), naiss=(6, "naissance"), herode=(6, "Hérode"), n4=(6, "4"),
             n30=(7, "30"), n37=(7, "37"), cert=(7, "certitude"), trad=(8, "tradition"), texte=(8, "texte"), age9=(9, "âge"), fait=(9, "fait"),
             idee=(10, "idée"), comm=(10, "commentaire"), abo=(11, "Abonne-toi"))
    X = dict(h1=["Mort à [33 ans] ?"], k1="La Bible ne le dit jamais", q1="« 33 ans »", st1="Pas dans la Bible",
             h2=["Aucun verset ne donne son [âge]"], k2="À sa mort", st2="Aucun verset", t2="Âge à la mort : jamais indiqué",
             h3=["Luc [3.23]"], k3="Le seul chiffre", q3="« Jésus avait environ trente ans lorsqu'il commença son ministère. »", r3="Luc 3.23 · Louis Segond 1910", f3="Le seul chiffre du texte",
             h4=["Le mot « [environ] »"], k4="Pas un âge exact", c4="« environ trente ans »", t4="Au début du ministère, pas à la mort",
             h5=["Il faut [compter]"], k5="Les fêtes de la Pâque", unit5=" Pâques", t5="Un ministère de 2 à 3 ans",
             h6=["Sa [naissance]"], k6="Matthieu", c6s="Matthieu 2", c6="Avant la mort d'Hérode le Grand", st6="4 av. notre ère",
             h7=["Entre [33] et 37 ans"], k7="Une estimation", t7a="Mort : 30 à 33 de notre ère", t7b="Âge : 33 à 37 ans environ", st7="Pas une certitude",
             h8=["Une [tradition], pas un texte"], k8="« 33 ans »", c8="Une tradition ancienne", t8="Pas un chiffre du texte",
             h9=["Ce qu'il a dit et [fait]"], k9="Les évangiles", c9="Ce qui compte : ses paroles et ses actes",
             h10=["Quelle [idée] reçue ?"], k10="À toi", c10="Quelle autre idée reçue sur la Bible t'a surpris ?", cta="Dis-le en commentaire",
             end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"), chap=("Le chiffre", "Le calcul", "La tradition", "Pour toi"))
elif LANG == "en":
    K = dict(n33=(1, "33"), jamais=(1, "never"), verset=(2, "verse"), age2=(2, "age"), luc=(3, "Luke"), jesus=(3, "Jesus"), trente=(3, "thirty"),
             env=(4, "about"), exact=(4, "exact"), compter=(5, "count"), trois=(5, "three"), ans5=(5, "years"), naiss=(6, "birth"), herode=(6, "Herod"), n4=(6, "4"),
             n30=(7, "30"), n37=(7, "37"), cert=(7, "certainty"), trad=(8, "tradition"), texte=(8, "text"), age9=(9, "age"), fait=(9, "did"),
             idee=(10, "idea"), comm=(10, "comments"), abo=(11, "Subscribe"))
    X = dict(h1=["Died at [33]?"], k1="The Bible never says it", q1="“33 years old”", st1="Not in the Bible",
             h2=["No verse gives his [age]"], k2="At death", st2="No verse", t2="Age at death: never stated",
             h3=["Luke [3:23]"], k3="The only number", q3="“Jesus himself, when he began to teach, was about thirty years old.”", r3="Luke 3:23 · World English Bible", f3="The only number in the text",
             h4=["The word “[about]”"], k4="Not an exact age", c4="“about thirty years old”", t4="At the start of his ministry, not at death",
             h5=["You have to [count]"], k5="The Passover feasts", unit5=" Passovers", t5="A ministry of 2 to 3 years",
             h6=["His [birth]"], k6="Matthew", c6s="Matthew 2", c6="Before the death of Herod the Great", st6="4 BC",
             h7=["Between [33] and 37"], k7="An estimate", t7a="Death: AD 30 to 33", t7b="Age: about 33 to 37", st7="Not a certainty",
             h8=["A [tradition], not a text"], k8="“33 years”", c8="An old tradition", t8="Not a number from the text",
             h9=["What he said and [did]"], k9="The Gospels", c9="What matters: his words and his deeds",
             h10=["Which [idea]?"], k10="Your turn", c10="Which other common idea about the Bible surprised you?", cta="Tell us in the comments",
             end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"), chap=("The number", "The count", "The tradition", "For you"))
else:
    K = dict(n33=(1, "33"), jamais=(1, "mai"), verset=(2, "versetto"), age2=(2, "età"), luc=(3, "Luca"), jesus=(3, "Gesù"), trente=(3, "trentanni"),
             env=(4, "circa"), exact=(4, "esatta"), compter=(5, "contare"), trois=(5, "tre"), ans5=(5, "anni"), naiss=(6, "nascita"), herode=(6, "Erode"), n4=(6, "4"),
             n30=(7, "30"), n37=(7, "37"), cert=(7, "certezza"), trad=(8, "tradizione"), texte=(8, "testo"), age9=(9, "età"), fait=(9, "fatto"),
             idee=(10, "idea"), comm=(10, "commenti"), abo=(11, "Iscriviti"))
    X = dict(h1=["Morto a [33 anni]?"], k1="La Bibbia non lo dice mai", q1="«33 anni»", st1="Non nella Bibbia",
             h2=["Nessun versetto dà la sua [età]"], k2="Alla morte", st2="Nessun versetto", t2="Età alla morte: mai indicata",
             h3=["Luca [3,23]"], k3="L'unico numero", q3="«Gesù, quando cominciò, avea circa trent'anni.»", r3="Luca 3,23 · Riveduta", f3="L'unico numero del testo",
             h4=["La parola «[circa]»"], k4="Non un'età esatta", c4="«circa trent'anni»", t4="All'inizio del ministero, non alla morte",
             h5=["Bisogna [contare]"], k5="Le feste di Pasqua", unit5=" Pasque", t5="Un ministero di 2-3 anni",
             h6=["La sua [nascita]"], k6="Matteo", c6s="Matteo 2", c6="Prima della morte di Erode il Grande", st6="4 a.C.",
             h7=["Tra [33] e 37 anni"], k7="Una stima", t7a="Morte: 30-33 d.C.", t7b="Età: circa 33-37 anni", st7="Non una certezza",
             h8=["Una [tradizione], non un testo"], k8="«33 anni»", c8="Una tradizione antica", t8="Non un numero del testo",
             h9=["Ciò che ha detto e [fatto]"], k9="I Vangeli", c9="Ciò che conta: le sue parole e le sue opere",
             h10=["Quale [idea]?"], k10="A te", c10="Quale altra idea comune sulla Bibbia ti ha sorpreso?", cta="Dillo nei commenti",
             end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"), chap=("Il numero", "Il calcolo", "La tradizione", "Per te"))


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
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("n33") - 0.3, size=112)
sticker(S1, "jesus-pied", 60, 720, 170, 0.0, rot=-2, instant=True)
q1 = put(S1, 300, 740, X["q1"], "card", "width:710px;font-size:80px")
blur_in(q1, 0.25, 14)
stamp(S1, 300, 960, X["st1"], kk("jamais") - 0.2, rot=-3, size=48)
hit(kk("jamais"), 0.9)

# --- S2 · aucun verset
t2 = LS[2] - 0.3
cam(t2, S2)
headline(S2, 300, X["h2"], t2 + 0.1, kicker=X["k2"], hl_t=kk("age2") - 0.3, size=88)
stamp(S2, 70, 720, X["st2"], early(kk("verset") - 0.3, 2, 0.9), rot=-3, size=64)
tag(S2, 70, 900, X["t2"], kk("age2") - 0.2, "acc", 48)

# --- S3 · Luc 3.23
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 300, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("luc") - 0.3, size=120)
q3_t0 = kk("jesus") - 0.05
q3_t1 = LS[4] - 0.3
f3 = tag(S3, 60, 720, X["f3"], LS[3] + 0.2, "", 46)
fade(f3, q3_t0 - 0.2)
kq3 = kinetic_quote(S3, 60, 720, X["r3"], X["q3"], q3_t0, q3_t1, width=960, size=56)
fade(kq3, LS[4] - 0.4)

# --- S4 · le mot « environ »
t4 = LS[4] - 0.3
cam(t4, S4)
headline(S4, 300, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=kk("env") - 0.3, size=104)
c4 = put(S4, 70, 720, X["c4"], "card", "width:940px;font-size:66px")
blur_in(c4, early(kk("env") - 0.3, 4, 0.8), 14)
tag(S4, 70, 960, X["t4"], kk("exact") - 0.4, "acc", 46)

# --- S5 · compter les Pâques
t5 = LS[5] - 0.3
cam(t5, S5)
headline(S5, 300, X["h5"], t5 + 0.1, kicker=X["k5"], hl_t=kk("compter") - 0.3, size=112)
counter(S5, 70, 720, 0, 3, early(kk("trois") - 0.4, 5, 1.4), 0.6, unit=X["unit5"], size=150)
tag(S5, 70, 1000, X["t5"], kk("ans5") - 0.5, "acc", 54)

# --- S6 · la naissance
t6 = LS[6] - 0.3
cam(t6, S6)
headline(S6, 300, X["h6"], t6 + 0.1, kicker=X["k6"], hl_t=kk("naiss") - 0.3, size=120)
c6 = put(S6, 70, 720, f"<small>{X['c6s']}</small>{X['c6']}", "card", "width:940px;font-size:56px")
blur_in(c6, early(kk("herode") - 0.4, 6, 1.0), 14)
stamp(S6, 70, 980, X["st6"], kk("n4") - 0.1, rot=-3, size=60)

# --- S7 · estimation
t7 = LS[7] - 0.3
cam(t7, S7)
headline(S7, 300, X["h7"], t7 + 0.1, kicker=X["k7"], hl_t=kk("n37") - 0.5, size=104)
tag(S7, 70, 720, X["t7a"], early(kk("n30") - 0.4, 7, 1.0), "", 52)
tag(S7, 70, 860, X["t7b"], kk("n37") - 0.8, "acc", 52)
stamp(S7, 70, 1000, X["st7"], kk("cert") - 0.3, rot=-3, size=56)

# --- S8 · une tradition
t8 = LS[8] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=kk("trad") - 0.3, size=92)
c8 = put(S8, 70, 720, X["c8"], "card", "width:940px;font-size:62px")
blur_in(c8, early(kk("trad") - 0.3, 8, 0.9), 14)
tag(S8, 70, 940, X["t8"], kk("texte") - 0.6, "acc", 52)

# --- S9 · ce qu'il a dit et fait
t9 = LS[9] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=kk("fait") - 0.4, size=104)
c9 = put(S9, 70, 720, X["c9"], "card", "width:940px;font-size:56px")
blur_in(c9, early(kk("age9") + 0.2, 9, 1.4), 14)
sticker(S9, "rouleau", 70, 980, 280, LS[9] + 1.2, rot=-2)

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
    chapters=[("01", X["chap"][0], 0, LS[3]), ("02", X["chap"][1], LS[3], LS[7]), ("03", X["chap"][2], LS[7], LS[10]), ("04", X["chap"][3], LS[10], DUR_)],
    suppress=[(q3_t0 - 0.1, q3_t1 + 0.2), (kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("foule", 30, 1450, 420, -4), ("jesus-pied", 800, 1480, 200, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
