"""Short « Ce prophète a marché nu pendant 3 ans sur ordre de Dieu (Ésaïe 20) » — style 02, 9:16.

Même fichier dans les trois dossiers (short-esaie-nu = FR, -en, -it) : la langue vient du nom du dossier.
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
THEME = {"brand": BRAND, "title": BRAND + " - Esaie nu - style 02", "lang": LANG,
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
    K = dict(nu1=(1, "nu"), trois1=(1, "trois"), dieu1=(1, "Dieu"), vingt=(2, "vingt"), n711=(3, "711"), ash=(3, "Ashdod"), egy3=(3, "Égypte"), va=(4, "Va"),
             nu5=(5, "nu"), mant=(5, "manteau"), deb=(5, "débattent"), trois6=(6, "trois"), signe=(6, "signe"), ambi=(6, "ambigu"),
             clair=(7, "clair"), roi=(7, "roi"), capt=(7, "captifs"), ethi=(7, "Éthiopie"), espoir=(8, "espoir"), egy8=(8, "Égypte"),
             geste=(9, "geste"), jer=(9, "Jérémie"), eze=(9, "Ézéchiel"), comm=(10, "commentaire"), abo=(11, "Abonne-toi"))
    X = dict(h1=["Le prophète [nu]"], k1="Ésaïe 20", q1="Nu et déchaussé", st1="3 ans", t1="Sur ordre de Dieu",
             h2=["Ésaïe, [chapitre 20]"], k2="Pas une légende", c2s="Dans la Bible", c2="Ésaïe 20",
             h3=["[711] avant notre ère"], k3="Le contexte", t3a="L'Assyrie prend Ashdod", t3b="Juda regarde vers l'Égypte",
             h4=["La [scène]"], k4="Ésaïe 20.2", q4="« Va, détache le sac de tes reins, et ôte tes souliers de tes pieds. Il fit ainsi, marchant nu et déchaussé. »", r4="Ésaïe 20.2 · Louis Segond 1910",
             h5=["Que veut dire « [nu] » ?"], k5="Un mot hébreu débattu", c5="Peut-être : sans manteau, en tunique", st5="Débattu",
             h6=["Et les [trois ans] ?"], k6="Une ambiguïté", t6a="Ésaïe marche trois ans", t6b="Le signe dure trois ans", st6="Texte ambigu",
             h7=["Le [sens] est clair"], k7="Ésaïe 20.4", t7a="Le roi d'Assyrie", t7b="Captifs d'Égypte", t7c="et d'Éthiopie",
             h8=["Pas d'espoir en [l'Égypte]"], k8="Le message", c8="Ne mettez pas votre espoir dans l'Égypte", st8="Pas l'Égypte",
             h9=["Un [geste] qui parle"], k9="Chez les prophètes", t9a="Jérémie : un joug", t9b="Ézéchiel : un siège",
             h10=["Quel [geste] ?"], k10="À toi", c10="Quel geste de prophète t'a le plus surpris ?", cta="Dis-le en commentaire",
             end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"), chap=("Le geste", "Le texte", "Le sens", "Pour toi"))
elif LANG == "en":
    K = dict(nu1=(1, "naked"), trois1=(1, "three"), dieu1=(1, "God's"), vingt=(2, "twenty"), n711=(3, "711"), ash=(3, "Ashdod"), egy3=(3, "Egypt"), va=(4, "Go"),
             nu5=(5, "naked"), mant=(5, "cloak"), deb=(5, "debate"), trois6=(6, "three"), signe=(6, "sign"), ambi=(6, "ambiguous"),
             clair=(7, "clear"), roi=(7, "king"), capt=(7, "captives"), ethi=(7, "Ethiopia"), espoir=(8, "hope"), egy8=(8, "Egypt"),
             geste=(9, "gesture"), jer=(9, "Jeremiah"), eze=(9, "Ezekiel"), comm=(10, "comments"), abo=(11, "Subscribe"))
    X = dict(h1=["The [naked] prophet"], k1="Isaiah 20", q1="Naked and barefoot", st1="3 years", t1="On God's orders",
             h2=["Isaiah, [chapter 20]"], k2="Not a legend", c2s="In the Bible", c2="Isaiah 20",
             h3=["[711] BC"], k3="The context", t3a="Assyria takes Ashdod", t3b="Judah looks to Egypt",
             h4=["The [scene]"], k4="Isaiah 20:2", q4="“Go, and loosen the sackcloth from off your waist, and take your shoes from off your feet.” He did so, walking naked and barefoot.", r4="Isaiah 20:2 · World English Bible",
             h5=["What does “[naked]” mean?"], k5="A debated Hebrew word", c5="Perhaps: without a cloak, in a tunic", st5="Debated",
             h6=["And the [three years]?"], k6="An ambiguity", t6a="Isaiah walks three years", t6b="The sign lasts three years", st6="Ambiguous text",
             h7=["The [meaning] is clear"], k7="Isaiah 20:4", t7a="The king of Assyria", t7b="Captives from Egypt", t7c="and from Ethiopia",
             h8=["No hope in [Egypt]"], k8="The message", c8="Do not put your hope in Egypt", st8="Not Egypt",
             h9=["A [gesture] that speaks"], k9="Among the prophets", t9a="Jeremiah: a yoke", t9b="Ezekiel: a siege",
             h10=["Which [gesture]?"], k10="Your turn", c10="Which prophet's gesture surprised you the most?", cta="Tell us in the comments",
             end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"), chap=("The gesture", "The text", "The meaning", "For you"))
else:
    K = dict(nu1=(1, "nudo"), trois1=(1, "tre"), dieu1=(1, "Dio"), vingt=(2, "venti"), n711=(3, "711"), ash=(3, "Asdod"), egy3=(3, "Egitto"), va=(4, "Va'"),
             nu5=(5, "nudo"), mant=(5, "mantello"), deb=(5, "discutono"), trois6=(6, "tre"), signe=(6, "segno"), ambi=(6, "ambiguo"),
             clair=(7, "chiaro"), roi=(7, "re"), capt=(7, "prigionieri"), ethi=(7, "Etiopia"), espoir=(8, "speranza"), egy8=(8, "Egitto"),
             geste=(9, "gesto"), jer=(9, "Geremia"), eze=(9, "Ezechiele"), comm=(10, "commenti"), abo=(11, "Iscriviti"))
    X = dict(h1=["Il profeta [nudo]"], k1="Isaia 20", q1="Nudo e scalzo", st1="3 anni", t1="Per ordine di Dio",
             h2=["Isaia, [capitolo 20]"], k2="Non una leggenda", c2s="Nella Bibbia", c2="Isaia 20",
             h3=["[711] avanti Cristo"], k3="Il contesto", t3a="L'Assiria prende Asdod", t3b="Giuda guarda all'Egitto",
             h4=["La [scena]"], k4="Isaia 20,2", q4="«Va', sciogliti il cilicio dai fianchi, e levati i calzari dai piedi.» Ed egli fece così, andando nudo e scalzo.", r4="Isaia 20,2 · Riveduta",
             h5=["Che cosa vuol dire «[nudo]»?"], k5="Una parola ebraica discussa", c5="Forse: senza mantello, in tunica", st5="Discusso",
             h6=["E i [tre anni]?"], k6="Un'ambiguità", t6a="Isaia cammina tre anni", t6b="Il segno dura tre anni", st6="Testo ambiguo",
             h7=["Il [senso] è chiaro"], k7="Isaia 20,4", t7a="Il re d'Assiria", t7b="Prigionieri dall'Egitto", t7c="e dall'Etiopia",
             h8=["Nessuna speranza nell'[Egitto]"], k8="Il messaggio", c8="Non mettete la vostra speranza nell'Egitto", st8="Non l'Egitto",
             h9=["Un [gesto] che parla"], k9="Per i profeti", t9a="Geremia: un giogo", t9b="Ezechiele: un assedio",
             h10=["Quale [gesto]?"], k10="A te", c10="Quale gesto di un profeta ti ha sorpreso di più?", cta="Dillo nei commenti",
             end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"), chap=("Il gesto", "Il testo", "Il senso", "Per te"))


def kk(name, n=0):
    k = K[name]
    return AL(k[1], k[0], k[2] if len(k) > 2 else n)


html.append('<style>'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

ST = [(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (1, 3), (0, 3)]
S1, S2, S3, S4, S5, S6, S7, S8, S9, S10 = ST[:10]

# --- S1 · accroche
cam(0, S1)
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("nu1") - 0.5, size=104)
sticker(S1, "ancien", 60, 720, 230, 0.0, rot=-2, instant=True)
q1 = put(S1, 340, 740, X["q1"], "card", "width:670px;font-size:56px")
blur_in(q1, 0.25, 14)
stamp(S1, 340, 960, X["st1"], kk("trois1") - 0.1, rot=-4, size=96)
tag(S1, 340, 1130, X["t1"], kk("dieu1") - 0.4, "acc", 48)
hit(kk("trois1"), 0.9)

# --- S2 · pas une légende
t2 = LS[2] - 0.3
cam(t2, S2)
headline(S2, 300, X["h2"], t2 + 0.1, kicker=X["k2"], hl_t=kk("vingt") - 0.3, size=104)
c2 = put(S2, 70, 720, f"<small>{X['c2s']}</small>{X['c2']}", "card", "width:940px;font-size:80px")
blur_in(c2, LS[2] + 0.5, 14)
sticker(S2, "livres", 70, 1020, 280, LS[2] + 0.8, rot=-2)

# --- S3 · contexte
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 300, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("n711") - 0.2, size=104)
tag(S3, 70, 720, X["t3a"], kk("ash") - 0.4, "", 52)
tag(S3, 70, 860, X["t3b"], kk("egy3") - 0.8, "acc", 52)
sticker(S3, "soldat", 860, 700, 150, LS[3] + 0.3, rot=2)
sticker(S3, "porte-ville", 70, 1010, 330, LS[3] + 0.8, rot=-2)

# --- S4 · la scène
t4 = LS[4] - 0.3
cam(t4, S4)
headline(S4, 300, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=LS[4] + 0.3, size=112)
q4_t0 = kk("va") - 0.05
q4_t1 = LS[5] - 0.3
SUPP_Q = (q4_t0 - 0.1, q4_t1 + 0.2)
f4 = tag(S4, 60, 720, X["r4"], LS[4] + 0.2, "", 40)
fade(f4, q4_t0 - 0.2)
kq4 = kinetic_quote(S4, 60, 720, X["r4"], X["q4"], q4_t0, q4_t1, width=960, size=52)
fade(kq4, LS[5] - 0.4)

# --- S5 · que veut dire « nu » ?
t5 = LS[5] - 0.3
cam(t5, S5)
headline(S5, 300, X["h5"], t5 + 0.1, kicker=X["k5"], hl_t=kk("nu5") - 0.3, size=100)
c5 = put(S5, 70, 720, X["c5"], "card", "width:940px;font-size:62px")
blur_in(c5, min(kk("mant") - 0.5, LS[5] + 0.9), 14)
stamp(S5, 70, 1070, X["st5"], kk("deb") - 0.3, rot=-4, size=84)

# --- S6 · et les trois ans ?
t6 = LS[6] - 0.3
cam(t6, S6)
headline(S6, 300, X["h6"], t6 + 0.1, kicker=X["k6"], hl_t=kk("trois6") - 0.2, size=104)
tag(S6, 70, 720, X["t6a"], kk("trois6") - 0.3, "", 54)
tag(S6, 70, 860, X["t6b"], kk("signe") - 0.5, "", 54)
stamp(S6, 70, 1010, X["st6"], kk("ambi") - 0.3, rot=-4, size=76)

# --- S7 · le sens est clair
t7 = LS[7] - 0.3
cam(t7, S7)
headline(S7, 300, X["h7"], t7 + 0.1, kicker=X["k7"], hl_t=kk("clair") - 0.2, size=104)
tag(S7, 70, 720, X["t7a"], min(kk("roi") - 0.3, LS[7] + 0.7), "", 56)
tag(S7, 70, 860, X["t7b"], kk("capt") - 0.3, "acc", 56)
tag(S7, 70, 1000, X["t7c"], kk("ethi") - 0.5, "acc", 56)
sticker(S7, "foule", 690, 1060, 320, kk("capt") + 0.2, rot=2)

# --- S8 · le message
t8 = LS[8] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=kk("egy8") - 0.5, size=100)
c8 = put(S8, 70, 720, X["c8"], "card", "width:940px;font-size:64px;border-color:" + ACC)
blur_in(c8, kk("espoir") - 0.9, 14)
stamp(S8, 70, 1060, X["st8"], kk("egy8") - 0.3, rot=-4, size=84)

# --- S9 · un geste qui parle
t9 = LS[9] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=kk("geste") - 0.2, size=104)
tag(S9, 70, 720, X["t9a"], kk("jer") - 0.3, "", 56)
tag(S9, 70, 860, X["t9b"], kk("eze") - 0.3, "acc", 56)
sticker(S9, "rouleau", 70, 1010, 300, LS[9] + 1.0, rot=-2)

# --- S10 · commentaire
t10 = LS[10] - 0.3
cam(t10, S10)
headline(S10, 300, X["h10"], t10 + 0.1, kicker=X["k10"], hl_t=LS[10] + 0.3, size=112)
c10 = put(S10, 70, 720, X["c10"], "card", "width:940px;font-size:58px")
blur_in(c10, LS[10] + 0.4, 14)
cta = put(S10, 70, 1080, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>' + X["cta"], "cta")
blur_in(cta, kk("comm") - 1.2, 14)
sfx("click", kk("comm") - 1.2, 0.8)

t_end = kk("abo") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", X["chap"][0], 0, LS[4]), ("02", X["chap"][1], LS[4], LS[7]), ("03", X["chap"][2], LS[7], LS[9]), ("04", X["chap"][3], LS[9], DUR_)],
    suppress=[SUPP_Q, (kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("foule", 30, 1450, 420, -4), ("jesus-pied", 800, 1480, 200, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
