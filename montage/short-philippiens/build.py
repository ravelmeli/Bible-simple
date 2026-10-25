"""Short « Je puis tout par Celui qui me fortifie » (Philippiens 4.11-13) en style 02 — 9:16, 81,7 s.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py). Chaque élément est calé sur transcript.json.
Le mot grec est écrit en HTML (police Inter, qui contient le grec), jamais dans une image : à faire relire avant publication.
Lancer : python3 build.py   (puis npx hyperframes check et npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Philippiens 4.13 - style 02", "lang": "fr"}
s.setup(here=HERE, duration=81.7, cols=3, rows=5, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

N = " "
S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10, S11, S12 = (2, 3), (1, 3), (0, 3)
S13 = (0, 4)

html.append('<style>.box.wide{text-align:left;font-weight:700;line-height:1.3}'
            f'.grk{{font-weight:800;line-height:1.1;color:{THEME["bg"]};letter-spacing:-2px}}</style>')

# --- S1 · accroche : le maillot est là dès la première image, puis tatouages, match, examen
cam(0, S1)
sticker(S1, "maillot", 60, 600, 380, 0.0, rot=-4, instant=True)
headline(S1, 300, ["« Je puis [tout] »"], 0.0, kicker="Le verset le plus cité", hl_t=T("tout") + 0.1, size=110)
sticker(S1, "avant-bras-tatoue", 560, 580, 330, T("tatouages") - 0.2, rot=4)
tag(S1, 60, 1100, "Tatouages", T("tatouages"), "", 44)
tag(S1, 60, 1200, "Maillots", T("maillots"), "", 44)
tag(S1, 500, 1100, "Un match", T("match"), "", 44)
tag(S1, 500, 1200, "Un examen", T("examen"), "", 44)
ref(S1, 60, 1330, "Philippiens 4.13 · Louis Segond 1910", T("fortifie"))
hit(T("tout"), 0.7)

# --- S2 · « Paul ne parlait pas de gagner »
t2 = T("mais") - 0.4
cam(t2, S2)
headline(S2, 280, ["Paul ne parlait pas", "de [gagner]"], t2 + 0.1, kicker="Le contexte", hl_t=T("gagner"), size=92)
sticker(S2, "paul-pied", 80, 560, 400, t2 + 0.3, rot=-2)
tag(S2, 540, 760, "≠ une victoire", T("gagner") - 0.1, "acc", 56)
hit(T("gagner"), 0.8)

# --- S3 · il écrit en prison
t3 = T("quand") - 0.3
cam(t3, S3)
headline(S3, 280, ["Il écrit", "en [prison]"], t3 + 0.1, kicker="Où est Paul ?", hl_t=T("prison"), size=100)
sticker(S3, "paul-pied", 60, 560, 420, T("prison") - 0.4, rot=-2)
sticker(S3, "encrier-stylet-romain", 540, 640, 420, T("écrit") + 0.2, rot=4)
label_box(S3, 540, 1020, "Encrier romain", "terre cuite, Ier–IIe s. · Met", T("écrit") + 0.5)
ref(S3, 60, 1320, "Philippiens 1.7 et 1.13", T("prison"))

# --- S4 · pas sa première épreuve : coups, naufrages, faim, froid (2 Corinthiens 11.25-27)
t4 = T("première") - 0.9
cam(t4, S4)
headline(S4, 280, ["Pas sa première", "[épreuve]"], t4 + 0.1, kicker="Ce que Paul a vécu", hl_t=T("épreuve"), size=96)
tag(S4, 70, 620, "Les coups", T("coups"), "", 60)
tag(S4, 70, 760, "Les naufrages", T("naufrages"), "", 60)
tag(S4, 70, 900, "La faim", T("faim"), "acc", 60)
tag(S4, 70, 1040, "Le froid", T("froid"), "acc", 60)
ref(S4, 70, 1200, "2 Corinthiens 11.25-27 · LSG", T("froid") + 0.2)
hit(T("faim"), 0.7)

# --- S5 · aux chrétiens de Philippes, qui viennent de lui envoyer de l'aide (Philippiens 4.10, 4.18)
t5 = T("chrétiens") - 1.2
cam(t5, S5)
headline(S5, 280, ["Aux chrétiens", "de [Philippes]"], t5 + 0.1, kicker="Les destinataires", hl_t=T("philippes"), size=96)
map_svg(S5, 40, 640, "assets/map.json", T("chrétiens") - 0.3, T("philippes"), width=580)
sticker(S5, "epaphrodite", 690, 620, 250, T("envoyer") - 0.3, rot=3)
label_box(S5, 60, 1070, "Épaphrodite apporte l'aide", "Philippiens 4.18", T("envoyer"))
tag(S5, 60, 1220, "Une aide envoyée à Paul", T("l'aide") - 0.1, "acc", 44)
ref(S5, 60, 1320, "Carte : Natural Earth", T("l'aide"))

# --- S6 · juste avant : « j'ai appris à être content » (Philippiens 4.11-12), sous-titres coupés
t6 = T("juste") - 0.5
cam(t6, S6)
headline(S6, 280, ["Juste [avant]", "ce verset"], t6 + 0.1, kicker="Philippiens 4.11-12", hl_t=T("avant", 1), size=100)
q6 = put(S6, 60, 610, "<small>Philippiens 4.11-12 · LSG</small>« J'ai appris à être content de l'état où je me trouve. "
         "Je sais vivre dans l'humiliation, et je sais vivre dans l'abondance. »", "box wide", "width:900px;font-size:36px")
blur_in(q6, 23.4, 14)
tag(S6, 60, 1080, "Content", T("content") - 0.1, "acc", 60)
tag(S6, 60, 1200, "L'humiliation", T("l'humiliation"), "", 48)
tag(S6, 500, 1200, "L'abondance", T("l'abondance"), "", 48)
sticker(S6, "lettre-papyrus-grec", 720, 1000, 230, t6 + 0.6, rot=4)

# --- S7 · rassasié et affamé, dans l'abondance et dans le manque (Philippiens 4.12), sous-titres coupés
t7 = 30.2
cam(t7, S7)
headline(S7, 280, ["En tout", "et [partout]"], t7 + 0.1, kicker="Philippiens 4.12", hl_t=T("partout"), size=100)
q7 = put(S7, 60, 610, "<small>Philippiens 4.12 · LSG</small>« En tout et partout j'ai appris à être rassasié et à avoir faim. »",
         "box wide", "width:900px;font-size:36px")
blur_in(q7, 30.7, 14)
sticker(S7, "bols", 140, 880, 640, T("rassasié") - 0.3, rot=-2)
tag(S7, 60, 1260, "Rassasié", T("rassasié", 1), "acc", 44)
tag(S7, 440, 1260, "Affamé", T("affamé"), "", 44)
tag(S7, 60, 1350, "Abondance", T("l'abondance", 1), "acc", 44)
tag(S7, 440, 1350, "Manque", T("manque") - 0.2, "", 44)

# --- S8 · le « tout » de Paul : tenir dans toutes les situations
t8 = 38.9
cam(t8, S8)
headline(S8, 280, ["Le « [tout] »", "de Paul"], t8 + 0.1, kicker="Ce que veut dire « tout »", hl_t=T("tout", 2), size=100)
sticker(S8, "paul-pied", 50, 560, 400, T("paul", 1) - 0.3, rot=-2)
tag(S8, 500, 640, "Tenir", T("tenir"), "acc", 80)
tag(S8, 500, 780, "dans toutes les situations", T("situations") - 0.4, "", 36)
tag(S8, 500, 880, "même les pires", T("pires") - 0.2, "acc", 44)
hit(T("tenir"), 0.9)

# --- vue d'ensemble, puis S9 · révélation en mode sombre : « j'ai appris » = « j'ai été initié » (grec)
t_all = T("détail") - 1.0
cam(t_all, "all")
t9 = T("détail") - 0.3
cam(t9, S9)
dark_mode(t9 - 0.1)
headline(S9, 280, ["« J'ai [appris] »"], t9 + 0.1, kicker="Détail étonnant · en grec", hl_t=T("appris", 2), size=110, dark=True)
grk = put(S9, 70, 520, "μεμύημαι", "grk", "font-size:190px")
blur_in(grk, T("grec") - 0.1, 20)
label_box(S9, 70, 800, "Memyēmai", "littéralement : « j'ai été initié »", T("initié") - 0.2, dark=True)
tag(S9, 70, 960, "un secret qu'on découvre", T("secret") - 0.2, "dark", 44)
tag(S9, 70, 1060, "en traversant la faim", T("traversant") - 0.1, "acc", 44)
sticker(S9, "paul-portrait", 600, 1120, 340, T("secret") - 0.2, rot=3)
hit(T("initié"), 1.0)

# --- S10 · le verset suivant : Philippiens 4.14, sous-titres coupés
t10 = T("regarde") - 0.7
cam(t10, S10)
headline(S10, 280, ["Le verset", "[suivant]"], t10 + 0.1, kicker="Philippiens 4.14", hl_t=T("suivant"), size=100, dark=True)
q10 = put(S10, 60, 690, "<small>Philippiens 4.14 · LSG</small>« Cependant, vous avez bien fait de prendre part à ma détresse. »",
          "box wide", "width:900px;font-size:36px")
blur_in(q10, 57.0, 14)
sticker(S10, "epaphrodite", 60, 980, 300, T("prendre") - 0.3, rot=-3)
label_box(S10, 420, 1080, "Les amis de Philippes", "ils prennent part à sa détresse", T("détresse") - 0.1, dark=True)

# --- S11 · Paul remercie ses amis : sa force ne vient pas de lui seul
t11 = T("juste", 1) - 0.3
cam(t11, S11)
headline(S11, 280, ["Paul [remercie]", "ses amis"], t11 + 0.1, kicker="Juste après « je puis tout »", hl_t=T("remercie"), size=100, dark=True)
sticker(S11, "paul-pied", 60, 620, 340, T("paul", 2) - 0.3, rot=-2)
sticker(S11, "epaphrodite", 540, 600, 290, T("amis") - 0.3, rot=3)
tag(S11, 60, 1200, "Sa force ne vient pas de lui seul", T("force") - 0.1, "acc", 38)
ref(S11, 60, 1310, "Philippiens 4.13-14", T("seul"))

# --- S12 · pas la victoire : la force de tenir, que tu gagnes ou que tu perdes
t12 = T("promet") - 1.1
cam(t12, S12)
headline(S12, 280, ["Pas la [victoire]"], t12 + 0.1, kicker="Ce que promet le verset", hl_t=T("victoire"), size=110, dark=True)
c1 = put(S12, 70, 560, "<small>Ce verset ne promet pas</small>La victoire", "box", "width:880px")
c2 = put(S12, 70, 800, "<small>Il promet</small>La force de tenir", "box", "width:880px")
blur_in(c1, T("promet") - 0.2, 14)
blur_in(c2, T("promet", 1) - 0.2, 14)
tween(f"#{c2}", f'backgroundColor: "#FFFFFF", color: "{INK}"', f'backgroundColor: "{ACC}", color: "#FFFFFF", duration: 0.3', T("tenir", 1))
tag(S12, 70, 1100, "Tu gagnes", T("gagnes"), "dark", 56)
tag(S12, 500, 1100, "Tu perdes", T("perdes") - 0.2, "dark", 56)
hit(T("tenir", 1), 0.9)

# --- S13 · appel à commenter
t13 = T("toi") - 0.3
cam(t13, S13)
headline(S13, 330, ["Et [toi] ?"], t13 + 0.1, kicker="À ton tour", hl_t=T("toi"), size=170, dark=True)
label_box(S13, 70, 760, "Dans quelle situation", "as-tu besoin de cette force ?", T("situation") - 0.3, dark=True)
sticker(S13, "paul-portrait", 600, 800, 340, t13 + 0.4, rot=3)
cta = put(S13, 70, 1150, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Réponds en commentaire', "cta")
blur_in(cta, T("dis-le") - 0.2, 14)
sfx("click", T("dis-le") - 0.2, 0.8)

# --- fin · vue d'ensemble puis carte de fin pendant « abonne-toi »
t_end = T("abonne-toi") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", "Le verset", 0, t6), ("02", "Le contexte", t6, t_all), ("03", "Le mot", t_all, t11), ("04", "Leçon", t11, DUR)],
    suppress=[(23.3, 30.1), (30.5, 38.9), (57.1, 60.3), (T("abonne-toi") - 0.7, DUR)],
    endcard={"kicker": "Abonne-toi", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("paul-portrait", 30, 1150, 330, -6), ("epaphrodite", 800, 1000, 200, 5)]},
    endcard_t=T("abonne-toi") - 0.1,
    music_volume=0.14,
)
