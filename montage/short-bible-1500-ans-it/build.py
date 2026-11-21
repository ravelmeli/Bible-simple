"""Short « Saviez-vous que la Bible a été écrite sur environ 1 500 ans ? » — style 02, 9:16.

Même fichier dans les trois dossiers (short-bible-1500-ans = FR, -en, -it) : la langue vient du nom du dossier.
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
THEME = {"brand": BRAND, "title": BRAND + " - Bible 1500 ans - style 02", "lang": LANG,
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
    K = dict(ans=(1, "ans"), bib1=(1, "bibliothèque"), biblia=(2, "biblia"), livres=(2, "livres"), n66=(3, "soixante-six"), moi=(4, "Moïse"), apo=(4, "Apocalypse"),
             q15=(5, "quinze"), mille=(5, "mille"), disc=(5, "discute"), quar=(6, "quarantaine"), david=(6, "David"), amos=(6, "Amos"), luc=(6, "Luc"),
             heb=(7, "hébreu"), aram=(7, "araméen"), grec=(7, "grec"), fil=(8, "fil"), rel=(8, "relation"), sie=(9, "siècles"), epo=(9, "époque"),
             livre=(10, "livre"), comm=(10, "commentaire"), abo=(11, "Abonne-toi"))
    X = dict(h1=["Écrite sur [1 500 ans]"], k1="La Bible", unit1=" ans", t1="Pas un livre : une bibliothèque",
             h2=["Le mot [biblia]"], k2="Du grec", c2s="Grec", c2="biblia = « les livres »", t2="Une bibliothèque",
             h3=["[66] livres"], k3="Bibles protestantes", unit3=" livres", t3="Le canon protestant",
             h4=["De Moïse à l'[Apocalypse]"], k4="Selon la tradition", c4a="Moïse : vers 1400 av. n. è.", c4b="Apocalypse : fin du Ier siècle",
             h5=["Environ [15 siècles]"], k5="Ou un peu plus de 1 000 ans", t5a="Tradition : ~1 500 ans", t5b="Beaucoup de chercheurs : ~1 000 ans", st5="Durée discutée",
             h6=["Une [quarantaine] d'auteurs"], k6="Des profils variés", t6a="Un roi : David", t6b="Un berger : Amos", t6c="Un médecin : Luc",
             h7=["Trois [langues]"], k7="Hébreu · araméen · grec", t7a="Hébreu", t7b="Un peu d'araméen", t7c="Grec",
             h8=["Un même [fil]"], k8="Pour les croyants", c8="La relation entre Dieu et les humains", st8="Lecture de foi",
             h9=["Chaque texte à son [époque]"], k9="Traverser des siècles", t9="Remettre le texte dans son époque",
             h10=["Quel [livre] ?"], k10="À toi", c10="Quel livre veux-tu lire en premier ?", cta="Dis-le en commentaire",
             end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"), chap=("Le mot", "La durée", "Les auteurs", "Pour toi"))
elif LANG == "en":
    K = dict(ans=(1, "years"), bib1=(1, "library"), biblia=(2, "biblia"), livres=(2, "books"), n66=(3, "sixty-six"), moi=(4, "Moses"), apo=(4, "Revelation"),
             q15=(5, "fifteen"), mille=(5, "thousand"), disc=(5, "debated"), quar=(6, "forty"), david=(6, "David"), amos=(6, "Amos"), luc=(6, "Luke"),
             heb=(7, "Hebrew"), aram=(7, "Aramaic"), grec=(7, "Greek"), fil=(8, "thread"), rel=(8, "relationship"), sie=(9, "centuries"), epo=(9, "time"),
             livre=(10, "book"), comm=(10, "comments"), abo=(11, "Subscribe"))
    X = dict(h1=["Written over [1,500 years]"], k1="The Bible", unit1=" years", t1="Not one book: a library",
             h2=["The word [biblia]"], k2="From Greek", c2s="Greek", c2="biblia = “the books”", t2="A library",
             h3=["[66] books"], k3="Protestant Bibles", unit3=" books", t3="The Protestant canon",
             h4=["From Moses to [Revelation]"], k4="According to tradition", c4a="Moses: around 1400 BC", c4b="Revelation: end of the 1st century",
             h5=["About [15 centuries]"], k5="Or a little over 1,000 years", t5a="Tradition: ~1,500 years", t5b="Many scholars: ~1,000 years", st5="Debated span",
             h6=["About [forty] authors"], k6="Varied backgrounds", t6a="A king: David", t6b="A shepherd: Amos", t6c="A physician: Luke",
             h7=["Three [languages]"], k7="Hebrew · Aramaic · Greek", t7a="Hebrew", t7b="A little Aramaic", t7c="Greek",
             h8=["One [thread]"], k8="For believers", c8="The relationship between God and humans", st8="A faith reading",
             h9=["Each text in its [time]"], k9="Crossing centuries", t9="Put the text back in its time",
             h10=["Which [book]?"], k10="Your turn", c10="Which book do you want to read first?", cta="Tell us in the comments",
             end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"), chap=("The word", "The span", "The authors", "For you"))
else:
    K = dict(ans=(1, "anni"), bib1=(1, "biblioteca"), biblia=(2, "biblia"), livres=(2, "libri"), n66=(3, "sessantasei"), moi=(4, "Mosè"), apo=(4, "Apocalisse"),
             q15=(5, "quindici"), mille=(5, "mille"), disc=(5, "discussa"), quar=(6, "quaranta"), david=(6, "Davide"), amos=(6, "Amos"), luc=(6, "Luca"),
             heb=(7, "ebraico"), aram=(7, "aramaico"), grec=(7, "greco"), fil=(8, "filo"), rel=(8, "rapporto"), sie=(9, "secoli"), epo=(9, "epoca"),
             livre=(10, "libro"), comm=(10, "commenti"), abo=(11, "Iscriviti"))
    X = dict(h1=["Scritta in [1.500 anni]"], k1="La Bibbia", unit1=" anni", t1="Non un libro: una biblioteca",
             h2=["La parola [biblia]"], k2="Dal greco", c2s="Greco", c2="biblia = «i libri»", t2="Una biblioteca",
             h3=["[66] libri"], k3="Bibbie protestanti", unit3=" libri", t3="Il canone protestante",
             h4=["Da Mosè all'[Apocalisse]"], k4="Secondo la tradizione", c4a="Mosè: verso il 1400 a.C.", c4b="Apocalisse: fine del I secolo",
             h5=["Circa [15 secoli]"], k5="O poco più di 1.000 anni", t5a="Tradizione: ~1.500 anni", t5b="Molti studiosi: ~1.000 anni", st5="Durata discussa",
             h6=["Circa [quaranta] autori"], k6="Profili vari", t6a="Un re: Davide", t6b="Un pastore: Amos", t6c="Un medico: Luca",
             h7=["Tre [lingue]"], k7="Ebraico · aramaico · greco", t7a="Ebraico", t7b="Un po' di aramaico", t7c="Greco",
             h8=["Un unico [filo]"], k8="Per i credenti", c8="Il rapporto tra Dio e gli uomini", st8="Lettura di fede",
             h9=["Ogni testo nella sua [epoca]"], k9="Attraversare i secoli", t9="Rimettere il testo nella sua epoca",
             h10=["Quale [libro]?"], k10="A te", c10="Quale libro vuoi leggere per primo?", cta="Dillo nei commenti",
             end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"), chap=("La parola", "La durata", "Gli autori", "Per te"))


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

# --- S1 · accroche : 1 500 ans
cam(0, S1)
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("ans") - 0.4, size=104)
sticker(S1, "livres", 60, 720, 250, 0.0, rot=-2, instant=True)
counter(S1, 340, 720, 0, 1500, max(kk("ans") - 1.3, 0.5), 1.2, unit=X["unit1"], size=130)
tag(S1, 340, 980, X["t1"], kk("bib1") - 0.6, "acc", 48)
hit(kk("bib1"), 0.9)

# --- S2 · biblia
t2 = LS[2] - 0.3
cam(t2, S2)
headline(S2, 300, X["h2"], t2 + 0.1, kicker=X["k2"], hl_t=kk("biblia") - 0.2, size=112)
c2 = put(S2, 70, 720, f"<small>{X['c2s']}</small>{X['c2']}", "card", "width:940px;font-size:66px")
blur_in(c2, early(kk("biblia") - 0.3, 2, 0.9), 14)
tag(S2, 70, 1000, X["t2"], kk("livres") - 0.2, "acc", 56)
sticker(S2, "rouleau", 690, 1000, 300, LS[2] + 1.0, rot=2)

# --- S3 · 66 livres
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 300, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("n66") - 0.4, size=120)
counter(S3, 70, 720, 0, 66, early(kk("n66") - 0.3, 3, 0.9), 0.8, unit=X["unit3"], size=170)
tag(S3, 70, 1040, X["t3"], LS[3] + 1.2, "", 52)

# --- S4 · de Moïse à l'Apocalypse
t4 = LS[4] - 0.3
cam(t4, S4)
headline(S4, 300, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=kk("apo") - 0.5, size=100)
c4a = put(S4, 70, 720, X["c4a"], "card", "width:700px;font-size:52px")
blur_in(c4a, early(kk("moi") - 0.3, 4, 0.9), 14)
c4b = put(S4, 70, 940, X["c4b"], "card", "width:700px;font-size:52px;border-color:" + ACC)
blur_in(c4b, kk("apo") - 0.5, 14)
sticker(S4, "scribe", 820, 720, 190, LS[4] + 0.6, rot=2)

# --- S5 · durée discutée
t5 = LS[5] - 0.3
cam(t5, S5)
headline(S5, 300, X["h5"], t5 + 0.1, kicker=X["k5"], hl_t=kk("q15") - 0.3, size=104)
tag(S5, 70, 720, X["t5a"], early(kk("q15") - 0.5, 5, 0.9), "", 50)
tag(S5, 70, 860, X["t5b"], kk("mille") - 0.6, "acc", 50)
stamp(S5, 70, 1010, X["st5"], kk("disc") - 0.3, rot=-4, size=76)

# --- S6 · une quarantaine d'auteurs
t6 = LS[6] - 0.3
cam(t6, S6)
headline(S6, 300, X["h6"], t6 + 0.1, kicker=X["k6"], hl_t=kk("quar") - 0.3, size=100)
tag(S6, 70, 720, X["t6a"], early(kk("david") - 0.3, 6, 1.4), "", 56)
tag(S6, 70, 860, X["t6b"], kk("amos") - 0.3, "", 56)
tag(S6, 70, 1000, X["t6c"], kk("luc") - 0.3, "acc", 56)

# --- S7 · trois langues
t7 = LS[7] - 0.3
cam(t7, S7)
headline(S7, 300, X["h7"], t7 + 0.1, kicker=X["k7"], hl_t=LS[7] + 0.2, size=112)
tag(S7, 70, 720, X["t7a"], early(kk("heb") - 0.3, 7, 0.9), "", 60)
tag(S7, 70, 860, X["t7b"], kk("aram") - 0.4, "", 60)
tag(S7, 70, 1000, X["t7c"], kk("grec") - 0.3, "acc", 60)

# --- S8 · un même fil
t8 = LS[8] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=kk("fil") - 0.3, size=112)
c8 = put(S8, 70, 720, X["c8"], "card", "width:940px;font-size:62px;border-color:" + ACC)
blur_in(c8, early(kk("rel") - 0.9, 8, 1.2), 14)
stamp(S8, 70, 1060, X["st8"], kk("rel") + 0.3, rot=-4, size=76)

# --- S9 · chaque texte à son époque
t9 = LS[9] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=kk("epo") - 0.4, size=96)
tag(S9, 70, 720, X["t9"], early(kk("epo") - 1.0, 9, 1.4), "acc", 48)
sticker(S9, "porte-ville", 70, 920, 330, LS[9] + 0.9, rot=-2)

# --- S10 · commentaire
t10 = LS[10] - 0.3
cam(t10, S10)
headline(S10, 300, X["h10"], t10 + 0.1, kicker=X["k10"], hl_t=kk("livre") - 0.2, size=112)
c10 = put(S10, 70, 720, X["c10"], "card", "width:940px;font-size:58px")
blur_in(c10, LS[10] + 0.4, 14)
cta = put(S10, 70, 1080, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>' + X["cta"], "cta")
blur_in(cta, kk("comm") - 1.2, 14)
sfx("click", kk("comm") - 1.2, 0.8)

t_end = kk("abo") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", X["chap"][0], 0, LS[3]), ("02", X["chap"][1], LS[3], LS[6]), ("03", X["chap"][2], LS[6], LS[9]), ("04", X["chap"][3], LS[9], DUR_)],
    suppress=[(kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("foule", 30, 1450, 420, -4), ("jesus-pied", 800, 1480, 200, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
