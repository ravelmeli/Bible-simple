"""Short « Jésus parlait araméen » en style 02 — 9:16, 60,4 s.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py). Chaque élément est calé sur transcript.json.
Les mots araméens sont écrits en lettres latines (transcription) dans le HTML, jamais dans une image.
Lancer : python3 build.py   (puis npx hyperframes check et npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Jésus parlait araméen - style 02", "lang": "fr"}
s.setup(here=HERE, duration=60.4, cols=3, rows=5, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10 = (2, 3)

html.append('<style>.box.wide{text-align:left;font-weight:700;line-height:1.3}</style>')

# --- S1 · accroche : Jésus est là dès la première image
cam(0, S1)
sticker(S1, "jesus-pied", 60, 580, 320, 0.0, rot=-3, instant=True)
headline(S1, 300, ["Jésus parlait", "[araméen]"], 0.0, kicker="Les évangiles sont en grec", hl_t=T("araméen") + 0.05, size=104)
tag(S1, 440, 760, "Évangiles : grec", T("grec") - 0.2, "", 52)
tag(S1, 440, 880, "Jésus : araméen", T("araméen") - 0.1, "acc", 52)
hit(T("araméen"), 0.9)

# --- S2 · la langue de tous les jours en Palestine, au premier siècle
t2 = T("Palestine") - 0.5
cam(t2, S2)
headline(S2, 280, ["La langue de", "[tous les jours]"], t2 + 0.1, kicker="Palestine · Ier siècle", hl_t=T("jours"), size=96)
map_svg(S2, 40, 620, "assets/map.json", t2 + 0.3, T("langue"), width=860)
tag(S2, 60, 1230, "Un parler de Galilée", T("langue") - 0.1, "acc", 48)
ref(S2, 60, 1340, "Carte schématique · Natural Earth", T("jours"))

# --- S3 · des mots gardés tels quels dans des évangiles en grec
t3 = T("évangélistes") - 0.5
cam(t3, S3)
headline(S3, 280, ["Des mots [gardés]"], t3 + 0.1, kicker="Les évangélistes", hl_t=T("gardé"), size=110)
sticker(S3, "parchemin", 60, 580, 360, T("écrivent") - 0.2, rot=-3)
tag(S3, 60, 1000, "Écrit en grec", T("grec", 1) - 0.1, "", 48)
sticker(S3, "ostracon-arameen", 480, 640, 470, T("prononcés") - 0.6, rot=3)
label_box(S3, 480, 960, "Texte en araméen", "tesson, vers 500-600 apr. J.-C. · The Met", T("prononcés"))
tag(S3, 60, 1110, "Tels qu'il les a prononcés", T("prononcés") - 0.2, "acc", 44)

# --- S4 · « Talitha koumi » (Marc 5.41), sous-titres coupés
t4 = T("Devant") - 0.6
cam(t4, S4)
headline(S4, 280, ["[Talitha] koumi"], t4 + 0.1, kicker="Marc 5.41", hl_t=T("Talitha"), size=110)
sticker(S4, "fille", 60, 600, 270, T("fillette") - 0.2, rot=-2)
q4 = put(S4, 400, 680, "<small>Marc 5.41 · LSG</small>« Jeune fille, je te le dis, lève-toi. »", "box wide", "width:540px;font-size:40px")
blur_in(q4, T("Jeune") - 0.1, 14)
tag(S4, 400, 1010, "Devant une fillette", T("Devant") - 0.1, "", 44)
hit(T("Talitha"), 1.0)

# --- S5 · « Éphphatha » (Marc 7.34)
t5 = T("sourd") - 0.9
cam(t5, S5)
headline(S5, 280, ["[Éphphatha]"], t5 + 0.1, kicker="Marc 7.34", hl_t=T("Éphphatha"), size=110)
sticker(S5, "sourd", 60, 600, 270, T("sourd") - 0.3, rot=2)
tag(S5, 400, 700, "À un sourd", T("sourd") - 0.1, "", 52)
tag(S5, 400, 830, "« Ouvre-toi »", T("Ouvre-toi") - 0.1, "acc", 64)
ref(S5, 400, 960, "Marc 7.34 · LSG", T("Ouvre-toi") + 0.2)
hit(T("Éphphatha"), 0.9)

# --- S6 · « Abba » à Gethsémané (Marc 14.36)
t6 = T("prière") - 0.8
cam(t6, S6)
headline(S6, 280, ["[Abba]"], t6 + 0.1, kicker="Marc 14.36 · Gethsémané", hl_t=T("Abba,"), size=130)
sticker(S6, "jesus-priere", 60, 600, 470, T("Gethsémané,") - 0.3, rot=-2)
tag(S6, 60, 1200, "Dans la prière", T("prière") - 0.1, "", 48)
tag(S6, 560, 780, "Père", T("Père") - 0.1, "acc", 100)
hit(T("Abba,"), 0.9)

# --- S7 · « Éloï, Éloï, lama sabachthani » sur la croix (Marc 15.34), sous-titres coupés
t7 = T("croix") - 0.7
cam(t7, S7)
headline(S7, 280, ["[Éloï], Éloï,", "lama sabachthani"], t7 + 0.1, kicker="Marc 15.34", hl_t=T("Éloï,"), size=84)
q7 = put(S7, 60, 690, "<small>Marc 15.34 · LSG</small>« Mon Dieu, mon Dieu, pourquoi m'as-tu abandonné ? »", "box wide", "width:900px;font-size:36px")
blur_in(q7, T("Mon") - 0.1, 14)
tag(S7, 60, 1030, "Sur la croix", T("croix") - 0.1, "", 52)
sticker(S7, "jesus-portrait", 600, 1020, 300, T("signifie") - 0.2, rot=3)

# --- S8 · l'hébreu et un peu de grec : hypothèse
t8 = T("Savait-il") - 0.4
cam(t8, S8)
headline(S8, 280, ["Et [l'hébreu] ?"], t8 + 0.1, kicker="La question", hl_t=T("l'hébreu"), size=120)
sticker(S8, "jesus-pied", 60, 600, 260, T("Savait-il") - 0.1, rot=-2)
tag(S8, 400, 640, "L'hébreu", T("l'hébreu") - 0.1, "", 56)
tag(S8, 400, 760, "Un peu de grec", T("grec", 2) - 0.2, "", 56)
tag(S8, 400, 920, "Hypothèse", T("hypothèse") - 0.1, "acc", 72)
tag(S8, 400, 1060, "Le texte ne le dit pas", T("texte") - 0.1, "", 40)
hit(T("hypothèse"), 1.0)

# --- S9 · mode sombre : les mots les plus intimes restent dans sa langue maternelle
t_all = T("Détail") - 1.2
cam(t_all, "all")
t9 = T("Détail") - 0.4
cam(t9, S9)
dark_mode(t9 - 0.1)
headline(S9, 280, ["Les mots [intimes]"], t9 + 0.1, kicker="Détail étonnant", hl_t=T("intimes"), size=110, dark=True)
tag(S9, 70, 640, "Au chevet d'une enfant", T("chevet") - 0.1, "dark", 44)
tag(S9, 70, 750, "Dans la prière", T("prière", 1) - 0.1, "dark", 44)
tag(S9, 70, 860, "Sur la croix", T("croix", 1) - 0.1, "dark", 44)
tag(S9, 70, 1010, "Sa langue maternelle", T("maternelle") - 0.3, "acc", 56)
sticker(S9, "jesus-portrait", 620, 640, 320, T("intimes") - 0.2, rot=3)
hit(T("maternelle"), 1.0)

# --- S10 · appel à commenter
t10 = T("Quel") - 0.3
cam(t10, S10)
headline(S10, 330, ["Quel [mot]", "araméen ?"], t10 + 0.1, kicker="À ton tour", hl_t=T("mot"), size=130, dark=True)
label_box(S10, 70, 840, "Lequel t'a le plus marqué ?", "Talitha koumi, Éphphatha, Abba, Éloï", T("marqué?") - 0.3, dark=True)
sticker(S10, "jesus-portrait", 640, 1000, 300, t10 + 0.4, rot=3)
cta = put(S10, 70, 1150, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Réponds en commentaire', "cta")
blur_in(cta, T("Dis-le") - 0.2, 14)
sfx("click", T("Dis-le") - 0.2, 0.8)

# --- fin : vue d'ensemble puis carte de fin pendant « abonne-toi »
t_end = T("abonne-toi") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", "La langue", 0, t4), ("02", "Ses mots", t4, t8), ("03", "La question", t8, t9), ("04", "Leçon", t9, DUR)],
    suppress=[(T("Jeune") - 0.2, T("lève-toi") + 0.5), (T("Mon") - 0.2, T("abandonné?") + 0.6), (T("abonne-toi") - 0.7, DUR)],
    endcard={"kicker": "Abonne-toi", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("jesus-portrait", 30, 1150, 330, -6), ("sourd", 800, 1000, 200, 5)]},
    endcard_t=T("abonne-toi") - 0.1,
    music_volume=0.14,
)
