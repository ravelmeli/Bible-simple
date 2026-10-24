"""Short « Le nom du roi David gravé dans la pierre » (stèle de Tel Dan) en style 02 — 9:16, 59,5 s.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py). Chaque élément est calé sur transcript.json.
Lancer : python3 build.py   (puis npx hyperframes check et npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Stèle de Tel Dan - style 02", "lang": "fr"}
s.setup(here=HERE, duration=59.5, cols=3, rows=4, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

# ================================================================ STORY
S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10 = (2, 3)

# --- S1 · accroche : David est là dès la première image
cam(0, S1)
sticker(S1, "david-lyre", 60, 600, 320, 0.0, rot=-3, instant=True)
headline(S1, 300, ["David a-t-il", "vraiment [existé] ?"], 0.0, kicker="Archéologie · Tel Dan", hl_t=T("existé") + 0.1, size=100)
label_box(S1, 440, 760, "Aucune trace sûre", "hors de la Bible, avant 1993", T("chercheurs") - 0.1)
tag(S1, 440, 900, "Des chercheurs doutent", T("douté") - 0.2, "", 40)

# --- S2 · la découverte : 1993, Tel Dan, au nord d'Israël
t2 = T("puis") - 0.2
cam(t2, S2)
headline(S2, 280, ["[1993], Tel Dan"], t2 + 0.1, kicker="La découverte", hl_t=T("1993"), size=104)
sticker(S2, "archeologue", 40, 500, 280, T("1993") - 0.1, rot=-2)
mi, _ = map_svg(S2, 330, 470, "assets/map.json", T("tel") - 0.3, T("dan"), width=600)
tag(S2, 50, 1150, "Remployée dans un mur", T("mur") - 0.2, "acc", 46)
ref(S2, 50, 1250, "Carte : Natural Earth", T("mur"))

# --- S3 · l'objet : un fragment de basalte couvert d'écriture araméenne
t3 = T("morceau") - 0.5
cam(t3, S3)
headline(S3, 280, ["Un fragment", "de [basalte]"], t3 + 0.1, kicker="L'objet", hl_t=T("basalte"), size=96)
sticker(S3, "stele-tel-dan", 110, 590, 820, T("morceau") - 0.2, rot=-2)
tag(S3, 60, 1290, "Écrit en araméen", T("araméen") - 0.1, "acc", 48)

# --- S4 · l'auteur : un roi de Damas se vante (2 Rois 9 raconte la même année)
t4 = T("roi", 1) - 0.5
cam(t4, S4)
headline(S4, 280, ["Un roi de [Damas]"], t4 + 0.1, kicker="L'auteur", hl_t=T("damas"), size=100)
sticker(S4, "roi-damas-pied", 50, 460, 360, T("roi", 1) - 0.2, rot=-2)
label_box(S4, 470, 470, "Probablement Hazaël", "roi d'Aram-Damas · hypothèse", T("vante") - 0.1)
sticker(S4, "ivoire-femme-fenetre", 520, 620, 260, T("victoire") - 0.3, rot=4)
label_box(S4, 520, 1010, "Ivoire syrien", "IXe–VIIIe s. av. J.-C. · Met", T("victoire"))
tag(S4, 50, 1190, "Tué : le roi d'Israël", T("tué"), "", 42)
tag(S4, 50, 1285, "Tué : le roi de la « maison de David »", T("« maison") - 0.1, "acc", 40)
hit(T("« maison"), 0.9)

# --- S5 · les mots : la ligne « maison de David » sur la pierre
t5 = T("la", 2) - 0.3
cam(t5, S5)
headline(S5, 280, ["« Maison de [David] »"], t5 + 0.1, kicker="Les mots clés", hl_t=T("david", 2), size=96)
sticker(S5, "ligne-maison-david", 60, 520, 900, t5 + 0.15, rot=-1)
label_box(S5, 60, 840, "BYTDWD", "« maison de David », lu de droite à gauche", t5 + 0.5)
tag(S5, 60, 1000, "= sa dynastie", T("dynastie") - 0.1, "acc", 56)

# --- S6 · la date : environ 150 ans après son règne ; première mention largement acceptée
t6 = T("date") - 0.6
cam(t6, S6)
headline(S6, 280, ["[150 ans] plus tard"], t6 + 0.1, kicker="La date", hl_t=T("150"), size=100)
sticker(S6, "david-lyre", 60, 480, 200, t6 + 0.2, rot=-3)
sticker(S6, "stele-tel-dan", 690, 560, 280, t6 + 0.4, rot=3)
counter(S6, 300, 660, 0, 150, T("150") - 0.05, 0.9, " ans", 110, "small")
sx6, sy6 = st(*S6)
tl6 = uid()
html.append(f'<svg class="node lead" id="{tl6}" style="left:{sx6}px;top:{sy6}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<path d="M160 1000 L830 1000" stroke-dasharray="680" style="stroke-width:6"/>'
            f'<circle cx="160" cy="1000" r="14" style="fill:{INK}"/><circle class="e" cx="830" cy="1000" r="14" style="fill:{ACC}"/></svg>')
tween(f"#{tl6} path", "strokeDashoffset: 680", 'strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut"', T("150") - 0.1)
tween(f"#{tl6} .e", "scale: 0, transformOrigin: \"50% 50%\"", 'scale: 1, duration: 0.3, ease: "back.out(3)"', T("150") + 0.8)
label_box(S6, 60, 1040, "David", "vers 1000 av. J.-C.", T("règne") - 0.3)
label_box(S6, 640, 1040, "La stèle", "vers 840 av. J.-C.", T("règne"))
tag(S6, 60, 1200, "1re mention hors de la Bible", T("première"), "acc", 46)
ref(S6, 60, 1300, "Largement acceptée par les spécialistes", T("acceptée"))

# --- S7 · c'est un ennemi qui l'écrit
t7 = T("et", 1) - 0.2
cam(t7, S7)
headline(S7, 280, ["Écrit par", "un [ennemi]"], t7 + 0.1, kicker="Le témoin", hl_t=T("ennemi"), size=100)
sticker(S7, "roi-damas-portrait", 200, 560, 640, t7 + 0.2, rot=-2)
hit(T("ennemi"), 0.8)

# --- vue d'ensemble au détail étonnant, puis S8 · la Bible attribue la mort des deux rois à Jéhu (2 Rois 9)
t_all = T("détail") - 0.2
cam(t_all, "all")
t8 = T("raconte") - 0.3
cam(t8, S8)
headline(S8, 280, ["La Bible dit :", "[Jéhu]"], t8 + 0.1, kicker="Détail étonnant", hl_t=T("jéhu"), size=100)
sticker(S8, "jehu-arc", 50, 560, 420, T("rois", 0) - 0.4, rot=-2)
label_box(S8, 520, 600, "Joram", "roi d'Israël", T("rois", 0) - 0.2)
label_box(S8, 520, 720, "Achazia", "roi de Juda", T("rois", 0))
ref(S8, 520, 850, "2 Rois 9", T("rois", 0) + 0.2)
tag(S8, 50, 1240, "Deux camps, deux versions", T("général") - 0.2, "acc", 48)

# --- S9 · révélation en mode sombre : pour ses voisins, la maison de David était réelle
t9 = T("cette") - 0.3
cam(t9, S9)
dark_mode(t9 - 0.1)
headline(S9, 280, ["La maison de David", "était bien [réelle]"], t9 + 0.1, kicker="Ce que montre la pierre", hl_t=T("réelle"), size=86, dark=True)
label_box(S9, 70, 560, "Une seule pierre", "pas la preuve de tout le récit", T("prouve") - 0.1, dark=True)
ref(S9, 70, 680, "Musée d'Israël, Jérusalem", T("prouve") + 0.3)
sticker(S9, "stele-tel-dan", 180, 760, 660, T("mais", 1) - 0.1, rot=2)
hit(T("réelle"), 1.0)

# --- S10 · appel à commenter
t10 = T("quelle") - 0.3
cam(t10, S10)
headline(S10, 300, ["Quelle [découverte]", "ensuite ?"], t10 + 0.1, kicker="À toi", hl_t=T("découverte"), size=104, dark=True)
sticker(S10, "archeologue", 560, 700, 400, t10 + 0.3, rot=3)
cta = put(S10, 70, 1150, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Réponds en commentaire', "cta")
blur_in(cta, T("dis-le") - 0.2, 14)
sfx("click", T("dis-le") - 0.2, 0.8)

# --- fin · vue d'ensemble puis carte de fin pendant « abonne-toi »
t_end = T("abonne-toi") - 0.6
cam(t_end, "all")

# ================================================================ assemble
build(
    chapters=[("01", "La découverte", 0, t3), ("02", "L'inscription", t3, t_all), ("03", "Le détail", t_all, t9), ("04", "Leçon", t9, DUR)],
    suppress=[(T("abonne-toi") - 0.7, DUR)],
    endcard={"kicker": "Abonne-toi", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("stele-tel-dan", 40, 1180, 380, -6), ("david-lyre", 800, 1040, 220, 5)]},
    endcard_t=T("abonne-toi") - 0.1,
    music_volume=0.2,
)
