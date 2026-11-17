"""Short « Dieu ne te donne pas plus que tu ne peux supporter » n'est pas dans la Bible — style 02, 9:16.

Même fichier dans les trois dossiers (short-dieu-supporter = FR, -en, -it) : la langue vient du nom du dossier.
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
THEME = {"brand": BRAND, "title": BRAND + " - Dieu ne te donne pas plus - style 02", "lang": LANG,
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
    K = dict(bible=(1, "Bible"), deuil=(2, "deuil"), mal=(2, "maladie"), verset=(3, "verset"), cor=(3, "Corinthiens"), dieu4=(4, "Dieu"),
             peir=(5, "peirasmos"), tent=(5, "tentation"), idol=(5, "idolâtrie"), souf=(5, "souffrance"), prom=(6, "promesse"), issue=(6, "issue"),
             paul=(7, "Paul"), acc=(7, "accablés"), dep=(8, "dépassé"), foi=(8, "foi"), bout=(9, "bout"), dieu9=(9, "Dieu"), entour=(9, "entourent"),
             comm=(10, "commentaire"), abo=(11, "Abonne-toi"))
    X = dict(h1=["Pas dans la [Bible]"], k1="Une phrase très connue", q1="« Dieu ne te donne pas plus que tu ne peux supporter »", st1="Pas dans la Bible",
             h2=["On la dit pour [consoler]"], k2="Quand quelqu'un souffre", t2a="Un deuil", t2b="Une maladie",
             h3=["Un vrai [verset]"], k3="Mal compris", c3s="Le texte réel", c3="1 Corinthiens 10.13",
             h4=["Ce que dit [le texte]"], k4="1 Corinthiens 10.13", q4="« Dieu, qui est fidèle, ne permettra pas que vous soyez tentés au-delà de vos forces ; mais avec la tentation il préparera aussi le moyen d'en sortir. »", r4="1 Corinthiens 10.13 · Louis Segond 1910",
             h5=["Un mot [grec]"], k5="peirasmos", c5s="Mot grec", c5="peirasmos : tentation · mise à l'épreuve", t5a="Le risque d'idolâtrie", t5b="Pas chaque souffrance de la vie",
             h6=["La [promesse]"], k6="Ce qu'elle dit vraiment", c6a="Pas : « Dieu t'envoie ce que tu peux porter »", c6b="Dieu prépare une issue",
             h7=["Même [Paul]"], k7="2 Corinthiens 1.8", q7="« accablés au-delà de nos forces, au point de désespérer même de la vie. »", r7="2 Corinthiens 1.8 · Louis Segond 1910",
             h8=["Sans manquer de [foi]"], k8="Être dépassé", st8="Dépassé", c8="Pas un manque de foi",
             h9=["Demande de [l'aide]"], k9="Si tu es à bout", t9a="À Dieu", t9b="À ceux qui t'entourent",
             h10=["Quelle [phrase] ?"], k10="À toi", c10="Quelle phrase t'a-t-on dite pour te consoler ?", cta="Dis-le en commentaire",
             end=("Abonne-toi", "La Bible<br />[Simple]", "S'abonner"), chap=("Le faux", "Le vrai verset", "La promesse", "Pour toi"))
elif LANG == "en":
    K = dict(bible=(1, "Bible"), deuil=(2, "loss"), mal=(2, "illness"), verset=(3, "verse"), cor=(3, "Corinthians"), dieu4=(4, "God"),
             peir=(5, "peirasmos"), tent=(5, "temptation"), idol=(5, "idolatry"), souf=(5, "suffering"), prom=(6, "promise"), issue=(6, "way"),
             paul=(7, "Paul"), acc=(7, "weighed"), dep=(8, "overwhelmed"), foi=(8, "faith"), bout=(9, "rope"), dieu9=(9, "God"), entour=(9, "around"),
             comm=(10, "comments"), abo=(11, "Subscribe"))
    X = dict(h1=["Not in the [Bible]"], k1="A very familiar sentence", q1="“God won't give you more than you can handle”", st1="Not in the Bible",
             h2=["Said to [comfort]"], k2="When someone is hurting", t2a="A loss", t2b="An illness",
             h3=["A real [verse]"], k3="Misunderstood", c3s="The real text", c3="1 Corinthians 10:13",
             h4=["What the [text] says"], k4="1 Corinthians 10:13", q4="“God is faithful, who will not allow you to be tempted above what you are able, but will with the temptation also make the way of escape.”", r4="1 Corinthians 10:13 · World English Bible",
             h5=["A [Greek] word"], k5="peirasmos", c5s="Greek word", c5="peirasmos: temptation · test", t5a="The risk of idolatry", t5b="Not every suffering in life",
             h6=["The [promise]"], k6="What it really says", c6a="Not: “God sends you what you can carry”", c6b="God prepares a way out",
             h7=["Even [Paul]"], k7="2 Corinthians 1:8", q7="“weighed down exceedingly, beyond our power, so that we despaired even of life.”", r7="2 Corinthians 1:8 · World English Bible",
             h8=["Without lacking [faith]"], k8="Being overwhelmed", st8="Overwhelmed", c8="Not a lack of faith",
             h9=["Ask for [help]"], k9="If you are at the end of your rope", t9a="From God", t9b="From people around you",
             h10=["Which [sentence]?"], k10="Your turn", c10="What sentence did someone say to comfort you?", cta="Tell us in the comments",
             end=("Subscribe", "Faith<br />[Engineering]", "Subscribe"), chap=("The myth", "The real verse", "The promise", "For you"))
else:
    K = dict(bible=(1, "Bibbia"), deuil=(2, "lutto"), mal=(2, "malattia"), verset=(3, "versetto"), cor=(3, "Corinzi"), dieu4=(4, "Iddio"),
             peir=(5, "peirasmos"), tent=(5, "tentazione"), idol=(5, "idolatria"), souf=(5, "sofferenza"), prom=(6, "promessa"), issue=(6, "uscita"),
             paul=(7, "Paolo"), acc=(7, "premuti"), dep=(8, "sopraffatti"), foi=(8, "fede"), bout=(9, "stremo"), dieu9=(9, "Dio"), entour=(9, "vicino"),
             comm=(10, "commenti"), abo=(11, "Iscriviti"))
    X = dict(h1=["Non è nella [Bibbia]"], k1="Una frase molto nota", q1="«Dio non ti dà più di quanto puoi sopportare»", st1="Non è nella Bibbia",
             h2=["Si dice per [consolare]"], k2="Quando qualcuno soffre", t2a="Un lutto", t2b="Una malattia",
             h3=["Un [versetto] vero"], k3="Frainteso", c3s="Il testo reale", c3="1 Corinzi 10,13",
             h4=["Che cosa dice il [testo]"], k4="1 Corinzi 10,13", q4="«Iddio, che è fedele, non permetterà che siate tentati al di là di quel che potete; ma con la tentazione vi darà anche la via d'uscirne.»", r4="1 Corinzi 10,13 · Riveduta",
             h5=["Una parola [greca]"], k5="peirasmos", c5s="Parola greca", c5="peirasmos: tentazione · prova", t5a="Il rischio dell'idolatria", t5b="Non ogni sofferenza della vita",
             h6=["La [promessa]"], k6="Che cosa dice davvero", c6a="Non: «Dio ti manda ciò che puoi portare»", c6b="Dio prepara una via d'uscita",
             h7=["Anche [Paolo]"], k7="2 Corinzi 1,8", q7="«premuti oltremodo, al di là delle nostre forze, tanto da disperare perfino della vita.»", r7="2 Corinzi 1,8 · Riveduta",
             h8=["Senza mancare di [fede]"], k8="Essere sopraffatti", st8="Sopraffatti", c8="Non una mancanza di fede",
             h9=["Chiedi [aiuto]"], k9="Se sei allo stremo", t9a="A Dio", t9b="A chi ti sta vicino",
             h10=["Quale [frase]?"], k10="A te", c10="Quale frase ti hanno detto per consolarti?", cta="Dillo nei commenti",
             end=("Iscriviti", "La Bibbia<br />[Semplice]", "Iscriviti"), chap=("Il mito", "Il versetto vero", "La promessa", "Per te"))


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
headline(S1, 300, X["h1"], 0.0, kicker=X["k1"], hl_t=kk("bible") - 0.6, size=104)
sticker(S1, "veilleur", 60, 720, 300, 0.0, rot=-2, instant=True)
q1 = put(S1, 400, 720, X["q1"], "card", "width:610px;font-size:46px")
blur_in(q1, 0.25, 14)
stamp(S1, 70, 1130, X["st1"], kk("bible") - 0.1, rot=-4, size=84)
hit(kk("bible"), 0.9)

# --- S2 · on la dit pour consoler
t2 = LS[2] - 0.3
cam(t2, S2)
headline(S2, 300, X["h2"], t2 + 0.1, kicker=X["k2"], hl_t=kk("deuil") - 0.7, size=104)
tag(S2, 70, 720, X["t2a"], kk("deuil") - 0.3, "", 60)
tag(S2, 70, 860, X["t2b"], kk("mal") - 0.3, "acc", 60)
sticker(S2, "pere", 700, 700, 250, LS[2] + 0.3, rot=2)

# --- S3 · un vrai verset
t3 = LS[3] - 0.3
cam(t3, S3)
headline(S3, 300, X["h3"], t3 + 0.1, kicker=X["k3"], hl_t=kk("verset") - 0.2, size=112)
c3 = put(S3, 70, 720, f"<small>{X['c3s']}</small>{X['c3']}", "card", "width:940px;font-size:70px")
blur_in(c3, kk("cor") - 0.3, 14)
sticker(S3, "livres", 70, 1020, 300, LS[3] + 0.6, rot=-2)

# --- S4 · la citation
t4 = LS[4] - 0.3
cam(t4, S4)
headline(S4, 300, X["h4"], t4 + 0.1, kicker=X["k4"], hl_t=LS[4] + 0.3, size=104)
q4_t0 = kk("dieu4") - 0.05
q4_t1 = LS[5] - 0.3
SUPP_Q = (q4_t0 - 0.1, q4_t1 + 0.2)
f4 = tag(S4, 60, 720, X["r4"], LS[4] + 0.2, "", 40)
fade(f4, q4_t0 - 0.2)
kq4 = kinetic_quote(S4, 60, 720, X["r4"], X["q4"], q4_t0, q4_t1, width=960, size=50)
fade(kq4, LS[5] - 0.4)

# --- S5 · peirasmos
t5 = LS[5] - 0.3
cam(t5, S5)
headline(S5, 300, X["h5"], t5 + 0.1, kicker=X["k5"], hl_t=kk("peir") - 0.3, size=112)
c5 = put(S5, 70, 720, f"<small>{X['c5s']}</small>{X['c5']}", "card", "width:940px;font-size:62px")
blur_in(c5, kk("peir") - 0.3, 14)
tag(S5, 70, 1000, X["t5a"], kk("idol") - 0.5, "acc", 52)
tag(S5, 70, 1120, X["t5b"], kk("souf") - 0.9, "", 46)

# --- S6 · la promesse
t6 = LS[6] - 0.3
cam(t6, S6)
headline(S6, 300, X["h6"], t6 + 0.1, kicker=X["k6"], hl_t=kk("prom"), size=112)
c6a = put(S6, 70, 720, X["c6a"], "card", "width:940px;font-size:54px")
blur_in(c6a, LS[6] + 0.3, 14)
c6b = put(S6, 70, 1060, X["c6b"], "card", "width:940px;font-size:64px;border-color:" + ACC)
blur_in(c6b, kk("issue") - 0.9, 14)

# --- S7 · Paul lui-même
t7 = LS[7] - 0.3
cam(t7, S7)
headline(S7, 300, X["h7"], t7 + 0.1, kicker=X["k7"], hl_t=kk("paul") + 0.05, size=112)
q7_t0 = kk("acc") - 0.05
q7_t1 = LS[8] - 0.3
SUPP_Q2 = (q7_t0 - 0.1, q7_t1 + 0.2)
f7 = tag(S7, 60, 720, X["r7"], LS[7] + 0.2, "", 40)
fade(f7, q7_t0 - 0.2)
kq7 = kinetic_quote(S7, 60, 720, X["r7"], X["q7"], q7_t0, q7_t1, width=960, size=54)
fade(kq7, LS[8] - 0.4)

# --- S8 · dépassé sans manquer de foi
t8 = LS[8] - 0.3
cam(t8, S8)
headline(S8, 300, X["h8"], t8 + 0.1, kicker=X["k8"], hl_t=kk("foi") - 0.3, size=100)
stamp(S8, 70, 720, X["st8"], kk("dep") - 0.2, rot=-4, size=70)
c8 = put(S8, 70, 1060, X["c8"], "card", "width:940px;font-size:70px;border-color:" + ACC)
blur_in(c8, kk("foi") - 0.4, 14)
sticker(S8, "veilleur", 800, 700, 210, LS[8] + 0.8, rot=-2)

# --- S9 · demander de l'aide
t9 = LS[9] - 0.3
cam(t9, S9)
headline(S9, 300, X["h9"], t9 + 0.1, kicker=X["k9"], hl_t=kk("bout") - 0.8, size=112)
tag(S9, 70, 720, X["t9a"], kk("dieu9") - 0.3, "", 60)
tag(S9, 70, 860, X["t9b"], kk("entour") - 0.9, "acc", 56)
sticker(S9, "foule", 70, 980, 330, LS[9] + 0.8, rot=2)

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
    chapters=[("01", X["chap"][0], 0, LS[3]), ("02", X["chap"][1], LS[3], LS[6]), ("03", X["chap"][2], LS[6], LS[9]), ("04", X["chap"][3], LS[9], DUR_)],
    suppress=[SUPP_Q, SUPP_Q2, (kk("abo") - 0.7, DUR_)],
    endcard={"kicker": X["end"][0], "title": X["end"][1], "button": X["end"][2],
             "stickers": [("foule", 30, 1450, 420, -4), ("jesus-pied", 800, 1480, 200, 5)]},
    endcard_t=kk("abo") - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
