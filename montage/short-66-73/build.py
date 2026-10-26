"""Short « 66 livres ou 73 ? » en style 02 — 9:16, 57,4 s.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py). Chaque élément est calé sur transcript.json.
Lancer : python3 build.py   (puis npx hyperframes check et npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - 66 ou 73 livres - style 02", "lang": "fr"}
s.setup(here=HERE, duration=57.4, cols=3, rows=5, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10, S11 = (2, 3), (1, 3)

# --- S1 · accroche : sept livres de plus
cam(0, S1)
sticker(S1, "feuillet-bible-latine", 660, 600, 270, 0.0, rot=4, instant=True)
headline(S1, 300, ["[7] livres", "de plus"], 0.0, kicker="Bible catholique", hl_t=T("sept") + 0.05, size=118)
tag(S1, 60, 760, "Bible catholique", T("catholique") - 0.1, "acc", 48)
tag(S1, 60, 880, "Bible protestante", T("protestante.") - 0.1, "", 48)
hit(T("sept"), 0.8)

# --- S2 · 66 ou 73
t2 = T("soixante-six") - 0.5
cam(t2, S2)
headline(S2, 280, ["66 ou [73] ?"], t2 + 0.1, kicker="Pourquoi ?", hl_t=T("soixante-treize"), size=130)
counter(S2, 70, 600, 0, 66, T("soixante-six") - 0.1, 0.8, unit=" livres", size=150)
counter(S2, 70, 860, 0, 73, T("soixante-treize") - 0.1, 0.8, unit=" livres", size=150, cls="")
tag(S2, 640, 700, "Protestante", T("soixante-six") + 0.3, "", 40)
tag(S2, 640, 960, "Catholique", T("soixante-treize") + 0.3, "acc", 40)
tag(S2, 70, 1200, "Pourquoi ?", T("Pourquoi?") - 0.1, "acc", 100)
hit(T("Pourquoi?"), 0.9)

# --- S3 · le Nouveau Testament est le même partout
t3 = T("Nouveau") - 0.5
cam(t3, S3)
headline(S3, 280, ["Le Nouveau", "Testament : [27]"], t3 + 0.1, kicker="Le même partout", hl_t=T("vingt-sept"), size=100)
counter(S3, 70, 640, 0, 27, T("vingt-sept") - 0.2, 0.7, unit=" livres", size=190)
tag(S3, 70, 960, "Identique partout", T("partout,") - 0.1, "", 52)
tag(S3, 70, 1080, "La différence : l'Ancien Testament", T("différence") - 0.1, "acc", 40)

# --- S4 · les protestants suivent la Bible hébraïque : 39 livres
t4 = T("protestants") - 0.5
cam(t4, S4)
headline(S4, 280, ["La Bible", "[hébraïque]"], t4 + 0.1, kicker="Les protestants", hl_t=T("hébraïque,"), size=104)
counter(S4, 70, 640, 0, 39, T("trente-neuf") - 0.2, 0.8, unit=" livres", size=190)
tag(S4, 70, 960, "Ancien Testament", T("trente-neuf") + 0.2, "", 52)

# --- S5 · les catholiques suivent aussi la Septante : sept de plus
t5 = T("catholiques") - 0.5
cam(t5, S5)
headline(S5, 280, ["La [Septante]"], t5 + 0.1, kicker="Les catholiques aussi", hl_t=T("Septante,"), size=120)
sticker(S5, "scribe", 60, 600, 280, T("ancienne") - 0.3, rot=-2)
tag(S5, 420, 700, "Traduction grecque", T("grecque") - 0.1, "", 48)
counter(S5, 420, 840, 0, 7, T("sept", 1) - 0.3, 0.6, unit=" de plus", size=150)

# --- S6 · les sept livres
t6 = T("Tobie,") - 0.6
cam(t6, S6)
headline(S6, 280, ["Les sept [livres]"], t6 + 0.1, kicker="En plus", hl_t=T("Tobie,"), size=104)
tag(S6, 70, 580, "Tobie", T("Tobie,") - 0.1, "", 44)
tag(S6, 70, 680, "Judith", T("Judith,") - 0.1, "", 44)
tag(S6, 70, 780, "La Sagesse", T("Sagesse,") - 0.1, "", 44)
tag(S6, 70, 880, "Le Siracide", T("Siracide,") - 0.1, "", 44)
tag(S6, 70, 980, "Baruch", T("Baruch") - 0.1, "", 44)
tag(S6, 70, 1080, "1 Maccabées", T("deux") - 0.1, "acc", 44)
tag(S6, 70, 1180, "2 Maccabées", T("Maccabées.") - 0.2, "acc", 44)
sticker(S6, "feuillet-nehemie", 640, 640, 290, T("Tobie,") + 0.2, rot=3)

# --- S7 · Luther les place à part (XVIe siècle)
t7 = T("seizième") - 0.5
cam(t7, S7)
headline(S7, 280, ["Luther les", "place [à part]"], t7 + 0.1, kicker="XVIe siècle", hl_t=T("part,"), size=100)
sticker(S7, "luther", 60, 620, 270, T("Luther") - 0.3, rot=-2)
tag(S7, 420, 740, "Lecture utile", T("utile") - 0.1, "", 52)
tag(S7, 420, 880, "Hors de la Bible", T("hors") - 0.1, "acc", 52)
hit(T("hors"), 0.8)

# --- S8 · le concile de Trente, 1546
t8 = T("1546,") - 0.5
cam(t8, S8)
headline(S8, 280, ["Le concile", "de [Trente]"], t8 + 0.1, kicker="1546", hl_t=T("Trente"), size=104)
sticker(S8, "eveques", 60, 620, 560, T("Concile") - 0.3, rot=-2)
counter(S8, 70, 1070, 1500, 1546, T("1546,") - 0.1, 0.8, size=170)
tag(S8, 70, 1300, "Déclarés canoniques", T("canoniques") - 0.2, "acc", 52)
hit(T("canoniques"), 1.0)

# --- S9 · les Églises orthodoxes en comptent davantage
t9 = T("orthodoxes") - 0.8
cam(t9, S9)
headline(S9, 280, ["Les Églises", "[orthodoxes]"], t9 + 0.1, kicker="Encore davantage", hl_t=T("orthodoxes"), size=100)
tag(S9, 70, 680, "Encore davantage", T("davantage,") - 0.1, "acc", 60)
tag(S9, 70, 820, "Selon leur tradition", T("tradition.") - 0.2, "", 48)
sticker(S9, "livres", 640, 960, 280, T("comptent") - 0.2, rot=3)

# --- S10 · mode sombre : Jérôme et la Vulgate
t_all = T("Détail") - 1.2
cam(t_all, "all")
t10 = T("Détail") - 0.4
cam(t10, S10)
dark_mode(t10 - 0.1)
headline(S10, 280, ["Jérôme et la", "[Vulgate]"], t10 + 0.1, kicker="Détail étonnant", hl_t=T("Vulgate,"), size=100, dark=True)
sticker(S10, "jerome-pied", 60, 620, 250, T("Jérôme,") - 0.2, rot=-2)
sticker(S10, "saint-jerome-peinture", 640, 640, 270, T("Jérôme,") + 0.2, rot=3)
tag(S10, 340, 1010, "Traducteur de la Vulgate", T("traducteur") - 0.1, "dark", 40)
tag(S10, 340, 1100, "Absents de la Bible hébraïque", T("hébraïque,", 1) - 0.4, "dark", 36)
tag(S10, 340, 1190, "Mais il les inclut", T("inclus.") - 0.5, "acc", 44)
hit(T("inclus."), 1.0)

# --- S11 · appel à commenter
t11 = T("Quelle") - 0.3
cam(t11, S11)
headline(S11, 330, ["Quelle [Bible]", "lis-tu ?"], t11 + 0.1, kicker="À ton tour", hl_t=T("Bible", 8) if False else T("lis-tu"), size=120, dark=True)
label_box(S11, 70, 840, "Catholique, protestante, orthodoxe ?", "dis-nous la tienne", T("lis-tu") - 0.2, dark=True)
sticker(S11, "jerome-portrait", 640, 900, 280, t11 + 0.4, rot=3)
cta = put(S11, 70, 1290, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Réponds en commentaire', "cta")
blur_in(cta, T("Dis-le") - 0.2, 14)
sfx("click", T("Dis-le") - 0.2, 0.8)

# --- fin : vue d'ensemble puis carte de fin pendant « abonne-toi »
t_end = T("abonne-toi") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", "Les chiffres", 0, t4), ("02", "La différence", t4, t_all), ("03", "Jérôme", t_all, t11), ("04", "Leçon", t11, DUR)],
    suppress=[(T("abonne-toi") - 0.7, DUR)],
    endcard={"kicker": "Abonne-toi", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("jerome-portrait", 30, 1150, 330, -6), ("luther", 800, 1000, 200, 5)]},
    endcard_t=T("abonne-toi") - 0.1,
    music_volume=0.14,
)
