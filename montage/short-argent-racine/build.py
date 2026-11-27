"""Short « L'argent est la racine de tous les maux » (Black Friday) — style 02, 9:16.

Même fichier dans les trois dossiers (short-argent-racine = FR, -en, -it) : la langue vient du nom du dossier.
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
THEME = {"brand": BRAND, "title": BRAND + " - Argent racine - style 02", "lang": LANG,
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
    K = dict(racine=(1, "racine"), pas=(1, "pas"), q2=(2, "Car"), tim=(2, "Timothée"), amour=(3, "amour"), une=(4, "une"), autres=(4, "autres"),
             q5=(5, "quelques-uns"), luc=(6, "Luc"), q6=(6, "Gardez-vous"), heb=(7, "Hébreux"), q7=(7, "Ne"), cond=(8, "condamnent"), attach=(8, "attachement"),
             achet=(9, "acheter"), poss=(9, "possède"), cont=(10, "contentement"), culp=(10, "culpabilité"), comm=(11, "commentaire"), abo=(12, "Abonne-toi"))
    X = dict(h1=["« L'argent est la [racine] de tous les maux »"], k1="Black Friday", st1="Pas ce que dit le texte",
             h2=["1 [Timothée] 6.10"], k2="Le verset", r2="1 Timothée 6.10 · Louis Segond 1910", q2="« Car l'amour de l'argent est une racine de tous les maux. »",
             h3=["L'[amour] de l'argent"], k3="Premier détail", t3a="Pas : « l'argent »", t3b="Mais : « l'amour de l'argent »",
             h4=["[Une] racine"], k4="Deuxième détail", t4a="Pas : « la » racine", t4b="Une racine, parmi d'autres",
             h5=["La [suite] du verset"], k5="1 Timothée 6.10", r5="1 Timothée 6.10 · Louis Segond 1910", q5="« quelques-uns, en étant possédés, se sont égarés loin de la foi, et se sont jetés eux-mêmes dans bien des tourments. »",
             h6=["[Luc] 12.15"], k6="Jésus", r6="Luc 12.15 · Louis Segond 1910", q6="« Gardez-vous avec soin de toute avarice ; car la vie d'un homme ne dépend pas de ses biens, fût-il dans l'abondance. »",
             h7=["[Hébreux] 13.5"], k7="Même message", r7="Hébreux 13.5 · Louis Segond 1910", q7="« Ne vous livrez pas à l'amour de l'argent ; contentez-vous de ce que vous avez. »",
             h8=["L'argent n'est pas [condamné]"], k8="Ces textes", c8="Ils mettent en garde contre l'attachement qu'on lui porte", t8="L'attachement est visé",
             h9=["Qu'est-ce qui me [possède] ?"], k9="La vraie question", t9a="Pas : « Ai-je le droit d'acheter ? »", t9b="Mais : « Qu'est-ce qui me possède ? »",
             h10=["Le [contentement]"], k10="Le texte invite", t10="Pas à la culpabilité",
             h11=["Quel [verset] ?"], k11="À toi", c11="Quel verset sur l'argent t'a marqué ?", cta="Dis-le en commentaire",
             end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"), chap=("L'idée reçue", "Le verset", "Autres textes", "La question"))
elif LANG == "en":
    K = dict(racine=(1, "root"), pas=(1, "not"), q2=(2, "For"), tim=(2, "Timothy"), amour=(3, "love"), une=(4, "root", 1), autres=(4, "among"),
             q5=(5, "Some"), luc=(6, "Luke"), q6=(6, "Beware"), heb=(7, "Hebrews"), q7=(7, "Be"), cond=(8, "condemn"), attach=(8, "attachment"),
             achet=(9, "buy"), poss=(9, "owns"), cont=(10, "contentment"), culp=(10, "guilt"), comm=(11, "comments"), abo=(12, "Subscribe"))
    X = dict(h1=["“Money is the [root] of all evil”"], k1="Black Friday", st1="Not what the text says",
             h2=["1 [Timothy] 6:10"], k2="The verse", r2="1 Timothy 6:10 · World English Bible", q2="“For the love of money is a root of all kinds of evil.”",
             h3=["The [love] of money"], k3="First detail", t3a="Not: “money”", t3b="But: “the love of money”",
             h4=["[A] root"], k4="Second detail", t4a="Not: “the” root", t4b="A root, among others",
             h5=["The [rest] of the verse"], k5="1 Timothy 6:10", r5="1 Timothy 6:10 · World English Bible", q5="“Some have been led astray from the faith in their greed, and have pierced themselves through with many sorrows.”",
             h6=["[Luke] 12:15"], k6="Jesus", r6="Luke 12:15 · World English Bible", q6="“Beware! Keep yourselves from covetousness, for a man's life doesn't consist of the abundance of the things which he possesses.”",
             h7=["[Hebrews] 13:5"], k7="Same message", r7="Hebrews 13:5 · World English Bible", q7="“Be free from the love of money, content with such things as you have.”",
             h8=["Money is not [condemned]"], k8="These texts", c8="They warn against attachment to it", t8="Attachment is the target",
             h9=["What [owns] me?"], k9="The real question", t9a="Not: “Am I allowed to buy?”", t9b="But: “What owns me?”",
             h10=["[Contentment]"], k10="The text invites", t10="Not guilt",
             h11=["Which [verse]?"], k11="Your turn", c11="Which verse about money stayed with you?", cta="Tell us in the comments",
             end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"), chap=("The common idea", "The verse", "Other texts", "The question"))
else:
    K = dict(racine=(1, "radice"), pas=(1, "non"), q2=(2, "Poiché"), tim=(2, "Timoteo"), amour=(3, "amore"), une=(4, "unica"), autres=(4, "altre"),
             q5=(5, "alcuni"), luc=(6, "Luca"), q6=(6, "Badate"), heb=(7, "Ebrei"), q7=(7, "Non"), cond=(8, "condannano"), attach=(8, "attaccamento"),
             achet=(9, "comprare"), poss=(9, "possiede"), cont=(10, "contentezza"), culp=(10, "colpa"), comm=(11, "commenti"), abo=(12, "Iscriviti"))
    X = dict(h1=["«Il denaro è la [radice] di tutti i mali»"], k1="Black Friday", st1="Non è ciò che dice il testo",
             h2=["1 [Timoteo] 6,10"], k2="Il versetto", r2="1 Timoteo 6,10 · Riveduta", q2="«Poiché l'amor del danaro è radice d'ogni sorta di mali.»",
             h3=["L'[amore] del denaro"], k3="Primo dettaglio", t3a="Non: «il denaro»", t3b="Ma: «l'amore del denaro»",
             h4=["Non l'[unica] radice"], k4="Secondo dettaglio", t4a="«Radice d'ogni sorta di mali»", t4b="Una radice tra le altre",
             h5=["Il [seguito] del versetto"], k5="1 Timoteo 6,10", r5="1 Timoteo 6,10 · Riveduta", q5="«alcuni che vi si sono dati, si sono sviati dalla fede e si son trafitti di molti dolori.»",
             h6=["[Luca] 12,15"], k6="Gesù", r6="Luca 12,15 · Riveduta", q6="«Badate e guardatevi da ogni avarizia; perché non è dall'abbondanza de' beni che uno possiede, ch'egli ha la sua vita.»",
             h7=["[Ebrei] 13,5"], k7="Stesso messaggio", r7="Ebrei 13,5 · Riveduta", q7="«Non siate amanti del danaro, siate contenti delle cose che avete.»",
             h8=["Il denaro non è [condannato]"], k8="Questi testi", c8="Mettono in guardia contro l'attaccamento", t8="Nel mirino: l'attaccamento",
             h9=["Che cosa mi [possiede]?"], k9="La vera domanda", t9a="Non: «Posso comprare?»", t9b="Ma: «Che cosa mi possiede?»",
             h10=["La [contentezza]"], k10="Il testo invita", t10="Non al senso di colpa",
             h11=["Quale [versetto]?"], k11="A te", c11="Quale versetto sul denaro ti ha colpito?", cta="Dillo nei commenti",
             end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"), chap=("L'idea comune", "Il versetto", "Altri testi", "La domanda"))


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


def quote_station(S, n, qkey, hl, size_h, qsize, sticker_name=None):
    """Station à citation : titre, citation animée mot par mot, fondu à la fin de la ligne."""
    t = LS[n] - 0.3
    cam(t, S)
    headline(S, 300, X["h%d" % n], t + 0.1, kicker=X["k%d" % n], hl_t=hl, size=size_h)
    if sticker_name:
        sticker(S, sticker_name, 70, 1120, 150, LS[n] + 0.4, rot=-3)
    t0 = kk(qkey) - 0.2
    t1 = LS[n + 1] - 0.3
    k = kinetic_quote(S, 60, 720, X["r%d" % n], X["q%d" % n], t0, t1, width=960, size=qsize)
    fade(k, LS[n + 1] - 0.4)
    return (t0 - 0.1, t1 + 0.2)


# --- S1 · accroche
cam(0, S1)
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("racine") - 0.3, size=84)
sticker(S1, "livres", 60, 760, 300, 0.0, rot=-3, instant=True)
stamp(S1, 120, 1230, X["st1"], kk("pas") - 0.2, rot=-3, size=46)
hit(kk("pas"), 0.9)

# --- S2 · 1 Timothée 6.10
SUP = [quote_station(S2, 2, "q2", kk("tim") - 0.3, 112, 60, "rouleau")]

# --- S3 · l'amour de l'argent
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 300, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("amour") - 0.4, size=104)
tag(S3, 70, 760, X["t3a"], early(LS[3] + 0.5, 3, 0.8), "", 56)
tag(S3, 70, 930, X["t3b"], kk("amour") - 0.4, "acc", 56)

# --- S4 · une racine
t4 = LS[4] - 0.3
cam(t4, S4)
headline(S4, 300, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=kk("une") - 0.3, size=112)
tag(S4, 70, 760, X["t4a"], early(LS[4] + 0.5, 4, 0.8), "", 56)
tag(S4, 70, 930, X["t4b"], kk("autres") - 0.5, "acc", 56)

# --- S5 · la suite du verset
SUP.append(quote_station(S5, 5, "q5", LS[5] + 0.4, 104, 48))

# --- S6 · Luc 12.15
SUP.append(quote_station(S6, 6, "q6", kk("luc") - 0.3, 120, 52, "jesus-pied"))

# --- S7 · Hébreux 13.5
SUP.append(quote_station(S7, 7, "q7", kk("heb") - 0.3, 112, 60, "rouleau"))

# --- S8 · pas condamné
t8 = LS[8] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=kk("cond") - 0.3, size=88)
c8 = put(S8, 70, 720, X["c8"], "card", "width:940px;font-size:60px")
blur_in(c8, early(kk("attach") - 0.6, 8, 1.4), 14)
tag(S8, 70, 1000, X["t8"], kk("attach") - 0.2, "acc", 54)

# --- S9 · la vraie question
t9 = LS[9] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=kk("poss") - 0.4, size=88)
tag(S9, 70, 760, X["t9a"], early(kk("achet") - 0.6, 9, 1.0), "", 46)
tag(S9, 70, 930, X["t9b"], kk("poss") - 0.5, "acc", 46)

# --- S10 · contentement
t10 = LS[10] - 0.3
cam(t10, S10)
headline(S10, 300, X["h10"], t10 + 0.1, kicker=X["k10"], hl_t=kk("cont") - 0.3, size=120)
sticker(S10, "sagesse-pied", 640, 760, 240, early(kk("cont") - 0.2, 10, 0.9), rot=3)
tag(S10, 70, 1200, X["t10"], kk("culp") - 0.5, "acc", 56)

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
    chapters=[("01", X["chap"][0], 0, LS[2]), ("02", X["chap"][1], LS[2], LS[5]), ("03", X["chap"][2], LS[5], LS[8]), ("04", X["chap"][3], LS[8], DUR_)],
    suppress=SUP + [(kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("foule", 30, 1450, 420, -4), ("sagesse-pied", 800, 1480, 200, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
