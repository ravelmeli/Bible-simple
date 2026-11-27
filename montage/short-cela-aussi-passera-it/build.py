"""Short « Cela aussi passera » n'est pas dans la Bible — style 02, 9:16.

Même fichier dans les trois dossiers (short-cela-aussi-passera = FR, -en, -it) : la langue vient du nom du dossier.
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
THEME = {"brand": BRAND, "title": BRAND + " - Cela aussi passera - style 02", "lang": LANG,
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
# K : mot-clé -> (ligne du script, mot, n-ième occurrence dans la ligne)
if LANG == "fr":
    K = dict(passera=(1, "passera"), pas=(1, "pas"), aucun=(2, "aucun"), anc=(2, "ancien"), nouv=(2, "nouveau"),
             legende=(3, "légende"), salomon=(3, "Salomon"), persanes=(3, "persanes"), joie=(4, "joie"), peinek=(4, "peine"),
             siecle=(5, "siècle"), lincoln=(5, "Lincoln"), n1859=(5, "1859"), eccl=(6, "Ecclésiaste"), q6=(6, "il"), psaume=(7, "Psaume"), q7=(7, "soir"),
             promet=(8, "promet"), peine8=(8, "peine"), dernier=(8, "dernier"), esaie=(9, "Ésaïe"), q9=(9, "parole"),
             peine10=(10, "peine"), prof=(10, "professionnel"), foi=(10, "foi"), phrase=(11, "phrase"), comm=(11, "commentaire"), abo=(12, "Abonne-toi"))
    X = dict(h1=["« Cela aussi [passera] »"], k1="Dans la Bible ?", st1="Pas dans la Bible",
             h2=["Aucun [livre] biblique"], k2="Ancien et Nouveau Testament", t2a="Ancien Testament : absent", t2b="Nouveau Testament : absent",
             h3=["Une [légende]"], k3="Autour du roi Salomon", t3="Traditions juives et persanes",
             h4=["Une phrase pour [tout]"], k4="Un roi cherche", c4="Vraie dans la joie comme dans la peine",
             h5=["Au XIXe [siècle]"], k5="En anglais", c5="Abraham Lincoln", st5="Discours de 1859",
             h6=["[Ecclésiaste] 3"], k6="Ce que dit la Bible", r6="Ecclésiaste 3 · Louis Segond 1910", q6="« Il y a un temps pour tout, un temps pour toute chose sous les cieux. »",
             h7=["[Psaume] 30"], k7="Ce que dit la Bible", r7="Psaume 30 · Louis Segond 1910", q7="« Le soir arrivent les pleurs, et le matin l'allégresse. »",
             h8=["Pas une [promesse] de vitesse"], k8="Ce que dit le texte", t8a="La peine a son temps", t8b="Pas le dernier mot",
             h9=["Ce qui [ne passe pas]"], k9="Ésaïe 40", r9="Ésaïe 40 · Louis Segond 1910", q9="« La parole de notre Dieu subsiste à jamais. »",
             h10=["Si ta [peine] dure"], k10="Parles-en", c10="À un proche ou à un professionnel", t10="Pas un manque de foi",
             h11=["Quelle [phrase] ?"], k11="À toi", c11="Quelle phrase t'a aidé dans l'épreuve ?", cta="Dis-le en commentaire",
             end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"), chap=("L'idée reçue", "La légende", "Ce que dit la Bible", "Pour toi"))
elif LANG == "en":
    K = dict(passera=(1, "pass"), pas=(1, "isn't"), aucun=(2, "any"), anc=(2, "Old"), nouv=(2, "New"),
             legende=(3, "legend"), salomon=(3, "Solomon"), persanes=(3, "Persian"), joie=(4, "joy"), peinek=(4, "sorrow"),
             siecle=(5, "century"), lincoln=(5, "Lincoln"), n1859=(5, "1859"), eccl=(6, "Ecclesiastes"), q6=(6, "For"), psaume=(7, "Psalm"), q7=(7, "Weeping"),
             promet=(8, "promise"), peine8=(8, "pain"), dernier=(8, "last"), esaie=(9, "Isaiah"), q9=(9, "word"),
             peine10=(10, "pain"), prof=(10, "professional"), foi=(10, "faith"), phrase=(11, "sentence"), comm=(11, "comments"), abo=(12, "Subscribe"))
    X = dict(h1=["“This too shall [pass]”"], k1="In the Bible?", st1="Not in the Bible",
             h2=["No biblical [book]"], k2="Old and New Testament", t2a="Old Testament: absent", t2b="New Testament: absent",
             h3=["A [legend]"], k3="About King Solomon", t3="Jewish and Persian traditions",
             h4=["A sentence for [everything]"], k4="A king looks for", c4="True in joy as in sorrow",
             h5=["In the nineteenth [century]"], k5="In English", c5="Abraham Lincoln", st5="Speech of 1859",
             h6=["[Ecclesiastes] 3"], k6="What the Bible says", r6="Ecclesiastes 3 · World English Bible", q6="“For everything there is a season, and a time for every purpose under heaven.”",
             h7=["[Psalm] 30"], k7="What the Bible says", r7="Psalm 30 · World English Bible", q7="“Weeping may stay for the night, but joy comes in the morning.”",
             h8=["Not a quick [promise]"], k8="What the text says", t8a="Pain has its time", t8b="Not the last word",
             h9=["What does [not pass]"], k9="Isaiah 40", r9="Isaiah 40 · World English Bible", q9="“The word of our God stands forever.”",
             h10=["If your [pain] lasts"], k10="Talk about it", c10="To a loved one or a professional", t10="Not a lack of faith",
             h11=["Which [sentence]?"], k11="Your turn", c11="Which sentence helped you in hard times?", cta="Tell us in the comments",
             end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"), chap=("The common idea", "The legend", "What the Bible says", "For you"))
else:
    K = dict(passera=(1, "passerà"), pas=(1, "non"), aucun=(2, "nessun"), anc=(2, "Antico"), nouv=(2, "Nuovo"),
             legende=(3, "leggenda"), salomon=(3, "Salomone"), persanes=(3, "persiane"), joie=(4, "gioia"), peinek=(4, "dolore"),
             siecle=(5, "Ottocento"), lincoln=(5, "Lincoln"), n1859=(5, "1859"), eccl=(6, "Ecclesiaste"), q6=(6, "Per"), psaume=(7, "Salmo"), q7=(7, "sera"),
             promet=(8, "promette"), peine8=(8, "dolore"), dernier=(8, "ultima"), esaie=(9, "Isaia"), q9=(9, "parola"),
             peine10=(10, "dolore"), prof=(10, "professionista"), foi=(10, "fede"), phrase=(11, "frase"), comm=(11, "commenti"), abo=(12, "Iscriviti"))
    X = dict(h1=["«Anche questo [passerà]»"], k1="Nella Bibbia?", st1="Non nella Bibbia",
             h2=["Nessun [libro] biblico"], k2="Antico e Nuovo Testamento", t2a="Antico Testamento: assente", t2b="Nuovo Testamento: assente",
             h3=["Una [leggenda]"], k3="Attorno al re Salomone", t3="Tradizioni ebraiche e persiane",
             h4=["Una frase per [tutto]"], k4="Un re cerca", c4="Vera nella gioia come nel dolore",
             h5=["Nell'[Ottocento]"], k5="In inglese", c5="Abraham Lincoln", st5="Discorso del 1859",
             h6=["[Ecclesiaste] 3"], k6="Ciò che dice la Bibbia", r6="Ecclesiaste 3 · Riveduta", q6="«Per tutto c'è il suo tempo, c'è il suo momento per ogni cosa sotto il cielo.»",
             h7=["[Salmo] 30"], k7="Ciò che dice la Bibbia", r7="Salmo 30 · Riveduta", q7="«La sera subentra il pianto, ma la mattina viene il giubilo.»",
             h8=["Non una [promessa] di fretta"], k8="Ciò che dice il testo", t8a="Il dolore ha il suo tempo", t8b="Non l'ultima parola",
             h9=["Ciò che [non passa]"], k9="Isaia 40", r9="Isaia 40 · Riveduta", q9="«La parola del nostro Dio sussiste in eterno.»",
             h10=["Se il tuo [dolore] dura"], k10="Parlane", c10="Con una persona cara o un professionista", t10="Non è mancanza di fede",
             h11=["Quale [frase]?"], k11="A te", c11="Quale frase ti ha aiutato nella prova?", cta="Dillo nei commenti",
             end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"), chap=("L'idea comune", "La leggenda", "Ciò che dice la Bibbia", "Per te"))


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
S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11 = ST[:11]

# --- S1 · accroche
cam(0, S1)
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("passera") - 0.3, size=104)
sticker(S1, "livres", 60, 700, 330, 0.0, rot=-3, instant=True)
stamp(S1, 150, 1150, X["st1"], kk("pas") - 0.2, rot=-3, size=56)
hit(kk("pas"), 0.9)

# --- S2 · aucun livre
t2 = LS[2] - 0.3
cam(t2, S2)
headline(S2, 300, X["h2"], t2 + 0.1, kicker=X["k2"], hl_t=kk("aucun") - 0.3, size=104)
tag(S2, 70, 740, X["t2a"], early(kk("anc") - 0.3, 2, 1.2), "", 50)
tag(S2, 70, 900, X["t2b"], kk("nouv") - 0.3, "acc", 50)

# --- S3 · la légende
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 300, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("legende") - 0.3, size=120)
sticker(S3, "ancien", 70, 720, 240, early(kk("salomon") - 0.2, 3, 1.0), rot=-2)
tag(S3, 70, 1220, X["t3"], kk("persanes") - 0.5, "acc", 46)

# --- S4 · une phrase pour tout
t4 = LS[4] - 0.3
cam(t4, S4)
headline(S4, 300, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=kk("joie") - 0.4, size=100)
c4 = put(S4, 70, 720, X["c4"], "card", "width:940px;font-size:64px")
blur_in(c4, early(kk("joie") - 0.4, 4, 0.9), 14)
sticker(S4, "sagesse-pied", 640, 960, 200, kk("peinek") - 0.2, rot=3)

# --- S5 · XIXe siècle, Lincoln
t5 = LS[5] - 0.3
cam(t5, S5)
headline(S5, 300, X["h5"], t5 + 0.1, kicker=X["k5"], hl_t=kk("siecle") - 0.3, size=96)
c5 = put(S5, 70, 720, X["c5"], "card", "width:940px;font-size:72px")
blur_in(c5, early(kk("lincoln") - 0.4, 5, 1.3), 14)
stamp(S5, 70, 960, X["st5"], kk("n1859") - 0.3, rot=-3, size=56)

# --- S6 · Ecclésiaste 3
t6 = LS[6] - 0.3
cam(t6, S6)
headline(S6, 300, X["h6"], t6 + 0.1, kicker=X["k6"], hl_t=kk("eccl") - 0.3, size=112)
sticker(S6, "livres", 70, 1150, 170, LS[6] + 0.5, rot=-3)
q6_t0 = kk("q6") - 0.05
q6_t1 = LS[7] - 0.3
kq6 = kinetic_quote(S6, 60, 720, X["r6"], X["q6"], q6_t0, q6_t1, width=960, size=56)
fade(kq6, LS[7] - 0.4)

# --- S7 · Psaume 30
t7 = LS[7] - 0.3
cam(t7, S7)
headline(S7, 300, X["h7"], t7 + 0.1, kicker=X["k7"], hl_t=kk("psaume") - 0.3, size=120)
q7_t0 = kk("q7") - 0.05
q7_t1 = LS[8] - 0.3
kq7 = kinetic_quote(S7, 60, 720, X["r7"], X["q7"], q7_t0, q7_t1, width=960, size=60)
fade(kq7, LS[8] - 0.4)

# --- S8 · pas une promesse de vitesse
t8 = LS[8] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=kk("promet") - 0.3, size=92)
tag(S8, 70, 740, X["t8a"], early(kk("peine8") - 0.3, 8, 1.4), "", 56)
tag(S8, 70, 920, X["t8b"], kk("dernier") - 0.4, "acc", 56)

# --- S9 · Ésaïe 40
t9 = LS[9] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=kk("esaie") - 0.3, size=100)
sticker(S9, "rouleau", 70, 1100, 250, LS[9] + 0.8, rot=-2)
q9_t0 = kk("q9") - 0.05
q9_t1 = LS[10] - 0.3
kq9 = kinetic_quote(S9, 60, 720, X["r9"], X["q9"], q9_t0, q9_t1, width=960, size=60)
fade(kq9, LS[10] - 0.4)

# --- S10 · si ta peine dure
t10 = LS[10] - 0.3
cam(t10, S10)
headline(S10, 300, X["h10"], t10 + 0.1, kicker=X["k10"], hl_t=kk("peine10") - 0.3, size=104)
c10 = put(S10, 70, 720, X["c10"], "card", "width:940px;font-size:60px")
blur_in(c10, early(kk("prof") - 0.8, 10, 1.4), 14)
tag(S10, 70, 980, X["t10"], kk("foi") - 0.5, "acc", 54)

# --- S11 · commentaire
t11 = LS[11] - 0.3
cam(t11, S11)
headline(S11, 300, X["h11"], t11 + 0.1, kicker=X["k11"], hl_t=kk("phrase") - 0.2, size=112)
c11 = put(S11, 70, 720, X["c11"], "card", "width:940px;font-size:56px")
blur_in(c11, LS[11] + 0.4, 14)
cta = put(S11, 70, 1080, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>' + X["cta"], "cta")
blur_in(cta, kk("comm") - 1.2, 14)
sfx("click", kk("comm") - 1.2, 0.8)

t_end = kk("abo") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", X["chap"][0], 0, LS[3]), ("02", X["chap"][1], LS[3], LS[6]), ("03", X["chap"][2], LS[6], LS[10]), ("04", X["chap"][3], LS[10], DUR_)],
    suppress=[(q6_t0 - 0.1, q6_t1 + 0.2), (q7_t0 - 0.1, q7_t1 + 0.2), (q9_t0 - 0.1, q9_t1 + 0.2), (kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("foule", 30, 1450, 420, -4), ("sagesse-pied", 800, 1480, 200, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
