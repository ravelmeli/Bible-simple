"""Short « Vrai ou faux : Noé a fait entrer 2 animaux de chaque espèce » (Genèse 6.19 et 7.2) — style 02, 9:16.

Même fichier dans les trois dossiers (short-noe-animaux = FR, -en, -it) : la langue vient du nom du dossier.
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
THEME = {"brand": BRAND, "title": BRAND + " - Noé et les animaux - style 02", "lang": LANG}
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
# K : mots-repères (ligne du script, mot, occurrence) ; X : libellés à l'écran
if LANG == "fr":
    BIBLE = "Louis Segond 1910"
    K = dict(faux=(1, "faux"), autre=(2, "autre"), ch7=(3, "sept"), q_sept=(3, "sept", 1), q_purs=(3, "purs"), q_paire=(3, "paire"),
             l4_purs=(4, "purs"), l4_sacr=(4, "sacrifice"), l4_seule=(4, "seule"), pourquoi=(5, "pourquoi"), sacr=(5, "sacrifices"),
             six=(6, "six"), deux=(6, "deux"), trad=(7, "traditions"), hypo=(7, "hypothèse"), hebreu=(8, "hébreu"), esp=(8, "espèce"),
             mn=(8, "min"), sorte=(8, "sorte"), incomplet=(9, "incomplet"), comm=(10, "commentaire"), detail=(10, "détail"), abo=(11, "abonne-toi"))
    X = dict(h1=["Vrai ou", "[faux] ?"], k1="Noé · Genèse 6–7", c_ask="Deux de chaque espèce ?", c_not="Pas tout à fait",
             h2=["La Genèse dit", "[autre chose]"], k2="Ce que dit le texte", h3=["Genèse 7 :", "[7 couples]"], k3="La précision",
             pure="Animaux purs", pure_s="7 couples, mâle et femelle", impure="Animaux impurs", impure_s="une seule paire", ref7="Genèse 7.2 · ",
             sacr_tag="Purs = offerts en sacrifice", h4=["Pourquoi plus", "d'animaux [purs] ?"], k4="Le texte ne le dit pas",
             sacr_lab="Le sacrifice de Noé", sacr_sub="plat italien, vers 1600 · Met", ref8="Genèse 8.20", h5=["Genèse 6 :", "[2] par sorte"], k5="Le premier ordre",
             male="Un mâle", femelle="une femelle", ref6="Genèse 6.19", h6=["Deux [traditions] ?"], k6="Hypothèse, pas certitude",
             b1s="Hypothèse", b1="Deux traditions réunies", b2s="Autre lecture", b2="Une précision", tab_lab="Le Déluge, aussi à Babylone", tab_sub="tablette d'Atra-hasis · Met",
             h7=["« [Espèce] »", "ou « sorte » ?"], k7="En hébreu · min", m1s="Traduit par", m1="espèce", m2s="Sens littéral", m2="sorte",
             note="Pas la notion moderne d'espèce", st_inc="Incomplet", h8=["[Vrai] ou faux ?"], k8="La réponse", h9=["Quel [détail] ?"], k9="À toi",
             cta="Dis-le en commentaire", end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"), chap=("La question", "Le texte", "L'explication", "L'hébreu"))
elif LANG == "en":
    BIBLE = "World English Bible"
    K = dict(faux=(1, "false"), autre=(2, "else"), ch7=(3, "seven"), q_sept=(3, "seven", 1), q_purs=(3, "clean"), q_paire=(3, "two"),
             l4_purs=(4, "clean"), l4_sacr=(4, "sacrifice"), l4_seule=(4, "just"), pourquoi=(5, "why"), sacr=(5, "sacrifices"),
             six=(6, "six"), deux=(6, "two"), trad=(7, "traditions"), hypo=(7, "hypothesis"), hebreu=(8, "Hebrew"), esp=(8, "species"),
             mn=(8, "min"), sorte=(8, "kind"), incomplet=(9, "incomplete"), comm=(10, "comments"), detail=(10, "detail"), abo=(11, "Subscribe"))
    X = dict(h1=["True or", "[false] ?"], k1="Noah · Genesis 6–7", c_ask="Two of every kind?", c_not="Not quite",
             h2=["Genesis says", "[something else]"], k2="What the text says", h3=["Genesis 7:", "[7 pairs]"], k3="The detail",
             pure="Clean animals", pure_s="7 pairs, male and female", impure="Unclean animals", impure_s="just one pair", ref7="Genesis 7:2 · ",
             sacr_tag="Clean = offered in sacrifice", h4=["Why more", "[clean] animals?"], k4="The text doesn't say",
             sacr_lab="Noah's sacrifice", sacr_sub="Italian dish, ca. 1600 · Met", ref8="Genesis 8:20", h5=["Genesis 6:", "[2] of each kind"], k5="The first command",
             male="A male", femelle="a female", ref6="Genesis 6:19", h6=["Two [traditions]?"], k6="A hypothesis, not a certainty",
             b1s="Hypothesis", b1="Two traditions woven together", b2s="Other reading", b2="A clarification", tab_lab="The Flood, in Babylon too", tab_sub="Atra-hasis tablet · Met",
             h7=["“[Species]” or", "“kind”?"], k7="In Hebrew · min", m1s="Translated", m1="species", m2s="Literal meaning", m2="kind",
             note="Not the modern idea of a species", st_inc="Incomplete", h8=["[True] or false?"], k8="The answer", h9=["Which [detail]?"], k9="Your turn",
             cta="Tell us in the comments", end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"), chap=("The question", "The text", "The explanation", "The Hebrew"))
else:
    BIBLE = "Riveduta"
    K = dict(faux=(1, "falso"), autre=(2, "altro"), ch7=(3, "sette"), q_sept=(3, "sette", 1), q_purs=(3, "puri"), q_paire=(3, "paio"),
             l4_purs=(4, "puri"), l4_sacr=(4, "sacrificio"), l4_seule=(4, "sola"), pourquoi=(5, "perché"), sacr=(5, "sacrifici"),
             six=(6, "sei"), deux=(6, "due"), trad=(7, "tradizioni"), hypo=(7, "ipotesi"), hebreu=(8, "ebraica"), esp=(8, "specie"),
             mn=(8, "min"), sorte=(8, "genere"), incomplet=(9, "incompleto"), comm=(10, "commenti"), detail=(10, "dettaglio"), abo=(11, "Iscriviti"))
    X = dict(h1=["Vero o", "[falso] ?"], k1="Noè · Genesi 6–7", c_ask="Due per ogni genere?", c_not="Non proprio",
             h2=["La Genesi dice", "[altro]"], k2="Che cosa dice il testo", h3=["Genesi 7:", "[7 paia]"], k3="La precisazione",
             pure="Animali puri", pure_s="7 paia, maschio e femmina", impure="Animali immondi", impure_s="una sola coppia", ref7="Genesi 7,2 · ",
             sacr_tag="Puri = offerti in sacrificio", h4=["Perché più", "animali [puri] ?"], k4="Il testo non lo dice",
             sacr_lab="Il sacrificio di Noè", sacr_sub="piatto italiano, circa 1600 · Met", ref8="Genesi 8,20", h5=["Genesi 6:", "[2] per genere"], k5="Il primo ordine",
             male="Un maschio", femelle="una femmina", ref6="Genesi 6,19", h6=["Due [tradizioni] ?"], k6="Un'ipotesi, non una certezza",
             b1s="Ipotesi", b1="Due tradizioni riunite", b2s="Altra lettura", b2="Una precisazione", tab_lab="Il diluvio, anche a Babilonia", tab_sub="tavoletta di Atrahasis · Met",
             h7=["«[Specie]» o", "«genere» ?"], k7="In ebraico · min", m1s="Tradotto con", m1="specie", m2s="Senso letterale", m2="genere",
             note="Non la nozione moderna di specie", st_inc="Incompleto", h8=["[Vero] o falso?"], k8="La risposta", h9=["Quale [dettaglio]?"], k9="A te",
             cta="Dillo nei commenti", end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"), chap=("La domanda", "Il testo", "La spiegazione", "L'ebraico"))


def kk(name, n=0):
    k = K[name]
    return AL(k[1], k[0], k[2] if len(k) > 2 else n)


S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)

# --- S1 · accroche : Noé et le vitrail de l'arche dès la première image
cam(0, S1)
sticker(S1, "noe-pied", 60, 780, 280, 0.0, rot=-3, instant=True)
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("faux") + 0.05, size=118)
sticker(S1, "vitrail-porte-arche", 600, 780, 230, 0.7, rot=3)
tag(S1, 60, 650, X["c_ask"], 0.9, "", 52)

# --- S2 · la Genèse dit autre chose
t2 = LS[2] - 0.3
cam(t2, S2)
headline(S2, 300, X["h2"], t2 + 0.1, kicker=X["k2"], hl_t=kk("autre"), size=100)
sticker(S2, "moutons", 140, 620, 640, t2 + 0.2, rot=-2)
tag(S2, 60, 1250, X["c_not"], kk("autre") - 0.1, "acc", 60)
hit(kk("autre"), 0.8)

# --- S3 · Genèse 7 : infographie 7 couples purs / 1 paire d'impurs (citation + ligne 4)
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 280, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("q_sept"), size=100)
sticker(S3, "moutons", 50, 600, 300, LS[3] + 1.2, rot=-3)
label_box(S3, 390, 600, X["pure"], X["pure_s"], LS[3] + 1.5)
tiles(S3, 390, 720, 14, kk("q_sept"))
sticker(S3, "chameaux", 50, 960, 300, kk("q_paire") - 0.4, rot=3)
label_box(S3, 390, 960, X["impure"], X["impure_s"], kk("q_paire") - 0.2)
tiles(S3, 390, 1080, 2, kk("q_paire"))
ref(S3, 390, 1250, X["ref7"] + BIBLE, LS[3] + 0.4)
hit(kk("q_sept"), 0.8)
tag(S3, 390, 1150, X["sacr_tag"], kk("l4_sacr") - 0.2, "acc", 40)
ring(S3, 420, 1108, kk("l4_seule"), size=160)

# --- S4 · pourquoi ? les sacrifices de Noé (Genèse 8.20)
t4 = LS[5] - 0.3
cam(t4, S4)
headline(S4, 280, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=kk("pourquoi") + 0.2, size=92)
sticker(S4, "plat-sacrifice-noe", 50, 560, 520, min(kk("sacr") - 0.8, LS[5] + 0.6), rot=-3)
label_box(S4, 50, 1100, X["sacr_lab"], X["sacr_sub"], kk("sacr") - 0.2)
sticker(S4, "autel-priere", 600, 620, 400, kk("sacr") - 0.4, rot=3)
ref(S4, 600, 1000, X["ref8"], kk("sacr"))

# --- S5 · Genèse 6 : deux de chaque sorte, un mâle et une femelle
t5 = LS[6] - 0.3
cam(t5, S5)
headline(S5, 280, X["h5"], t5 + 0.1, kicker=X["k5"], hl_t=kk("deux"), size=100)
sticker(S5, "colombe-1", 60, 560, 420, kk("deux") - 0.2, rot=-4)
sticker(S5, "colombe-2", 540, 560, 420, kk("deux") + 0.1, rot=4)
label_box(S5, 60, 1050, X["male"], "", kk("deux") + 0.2)
label_box(S5, 540, 1050, X["femelle"], "", kk("deux") + 0.4)
ref(S5, 60, 1180, X["ref6"], kk("sorte", 0) if False else LS[6] + 0.8)

# --- vue d'ensemble puis mode sombre : l'hypothèse des deux traditions
t_all = LS[7] - 0.9
cam(t_all, "all")
t6 = LS[7] - 0.2
cam(t6, S6)
dark_mode(t6 - 0.1)
headline(S6, 300, X["h6"], t6 + 0.1, kicker=X["k6"], hl_t=kk("trad"), size=104, dark=True)
b1 = put(S6, 70, 640, f"<small>{X['b1s']}</small>{X['b1']}", "box out", "width:430px;font-size:48px")
b2 = put(S6, 560, 640, f"<small>{X['b2s']}</small>{X['b2']}", "box out", "width:430px;font-size:48px")
blur_in(b1, kk("trad") - 0.2, 14)
blur_in(b2, kk("hypo") + 0.3, 14)
sticker(S6, "tablette-atra-hasis", 120, 960, 300, kk("hypo") - 0.2, rot=-3)
label_box(S6, 460, 1020, X["tab_lab"], X["tab_sub"], kk("hypo") - 0.1, dark=True)
hit(kk("hypo"), 0.8)

# --- S7 · le mot hébreu min : « espèce » ou « sorte » ?
t7 = LS[8] - 0.3
cam(t7, S7)
headline(S7, 300, X["h7"], t7 + 0.1, kicker=X["k7"], hl_t=kk("esp"), size=110, dark=True)
m1 = put(S7, 70, 700, f"<small>{X['m1s']}</small>{X['m1']}", "box out", "width:430px;font-size:64px")
m2 = put(S7, 560, 700, f"<small>{X['m2s']}</small>{X['m2']}", "box out", "width:430px;font-size:64px")
blur_in(m1, kk("esp") - 0.2, 14)
blur_in(m2, kk("sorte") - 0.2, 14)
tag(S7, 70, 1000, X["note"], kk("mn") + 0.4, "acc", 44)
hit(kk("mn"), 1.0)

# --- S8 · réponse : incomplet
t8 = LS[9] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=kk("faux") if False else LS[9] + 0.5, size=118, dark=True)
sticker(S8, "noe-portrait", 560, 640, 400, t8 + 0.3, rot=3)
stamp(S8, 60, 1160, X["st_inc"], kk("incomplet") - 0.1, rot=-4, size=80)
hit(kk("incomplet"), 1.0)

# --- S9 · appel à commenter
t9 = LS[10] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=kk("detail"), size=120, dark=True)
sticker(S9, "noe-pied", 600, 640, 330, t9 + 0.2, rot=3)
cta = put(S9, 70, 1150, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>' + X["cta"], "cta")
blur_in(cta, kk("comm") - 1.2, 14)
sfx("click", kk("comm") - 1.2, 0.8)

# --- fin · vue d'ensemble puis carte de fin pendant « abonne-toi »
t_end = kk("abo") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", X["chap"][0], 0, t3), ("02", X["chap"][1], t3, t_all), ("03", X["chap"][2], t_all, t7), ("04", X["chap"][3], t7, DUR_)],
    suppress=[(kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("moutons", 30, 1180, 380, -6), ("noe-pied", 800, 1040, 220, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
