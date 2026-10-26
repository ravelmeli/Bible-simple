"""Short « Jaël et le piquet de tente » (Juges 4-5) en style 02 — 9:16, 60,8 s.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py). Chaque élément est calé sur transcript.json.
Lancer : python3 build.py   (puis npx hyperframes check et npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Jaël - style 02", "lang": "fr"}
s.setup(here=HERE, duration=60.8, cols=3, rows=5, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10, S11, S12 = (2, 3), (1, 3), (0, 3)
S13 = (0, 4)

html.append('<style>.box.wide{text-align:left;font-weight:700;line-height:1.3}</style>')

# --- S1 · accroche : Jaël est là dès la première image
cam(0, S1)
sticker(S1, "jael-pied", 60, 560, 330, 0.0, rot=-3, instant=True)
headline(S1, 300, ["Une femme", "sans [armée]"], 0.0, kicker="Juges 4", hl_t=T("armée") + 0.05, size=104)
label_box(S1, 450, 700, "Jaël", "une femme du camp des Quénites", T("Jaël"))
tag(S1, 450, 900, "20 ans de guerre", T("vingt") - 0.1, "acc", 48)
hit(T("armée"), 0.8)

# --- S2 · le roi de Canaan opprime Israël depuis vingt ans
t2 = T("roi") - 0.4
cam(t2, S2)
headline(S2, 280, ["Le roi de", "[Canaan]"], t2 + 0.1, kicker="Israël opprimé", hl_t=T("Canaan"), size=100)
map_svg(S2, 40, 580, "assets/map.json", t2 + 0.3, T("Canaan"), width=800)
counter(S2, 60, 1215, 0, 20, T("vingt", 1) - 0.2, 1.0, unit=" ans", size=140)
ref(S2, 60, 1385, "Carte schématique · Natural Earth", T("depuis"))

# --- S3 · Sisera et neuf cents chars de fer
t3 = T("Sisera") - 1.0
cam(t3, S3)
headline(S3, 280, ["Son chef de [guerre]"], t3 + 0.1, kicker="Sisera", hl_t=T("guerre", 1), size=96)
sticker(S3, "sisera", 60, 600, 250, T("Sisera") - 0.2, rot=-2)
sticker(S3, "tablette-char", 430, 620, 480, T("chars") - 0.3, rot=3)
label_box(S3, 430, 930, "Un char de guerre", "faïence, Égypte, vers 1390 av. J.-C. · Met", T("chars"))
counter(S3, 430, 1110, 0, 900, T("neuf") - 0.1, 1.1, unit=" chars", size=96)
tag(S3, 430, 1260, "de fer", T("fer") - 0.2, "acc", 56)
hit(T("fer"), 1.0)

# --- S4 · la prophétesse Débora et Barak
t4 = T("prophétesse") - 0.5
cam(t4, S4)
headline(S4, 280, ["La prophétesse", "[Débora]"], t4 + 0.1, kicker="Juges 4.4-6", hl_t=T("Débora"), size=96)
sticker(S4, "debora", 60, 580, 320, T("Débora") - 0.3, rot=-2)
sticker(S4, "barak", 560, 640, 300, T("Barak") - 0.3, rot=3)
label_box(S4, 560, 1080, "Barak", "général israélite", T("Barak"))

# --- S5 · « Tu n'auras point de gloire… » (Juges 4.9), sous-titres coupés
t5 = T("Tu") - 0.5
cam(t5, S5)
headline(S5, 280, ["Une [promesse]", "surprenante"], t5 + 0.1, kicker="Juges 4.9", hl_t=T("gloire"), size=96)
q5 = put(S5, 60, 640, "<small>Juges 4.9 · Louis Segond 1910</small>« Tu n'auras point de gloire sur la voie où tu marches, "
         "car l'Éternel livrera Sisera entre les mains d'une femme. »", "box wide", "width:900px;font-size:36px")
blur_in(q5, T("Tu") - 0.1, 14)
tag(S5, 60, 1130, "Pas de gloire pour Barak", T("gloire") - 0.1, "", 48)
tag(S5, 60, 1240, "Entre les mains d'une femme", T("femme", 1) - 0.2, "acc", 48)
hit(T("femme", 1), 0.9)

# --- S6 · Sisera vaincu s'enfuit à pied jusqu'à la tente de Jaël
t6 = T("Sisera", 2) - 0.4
cam(t6, S6)
headline(S6, 280, ["Sisera [s'enfuit]", "à pied"], t6 + 0.1, kicker="Vaincu", hl_t=T("s'enfuit"), size=100)
sticker(S6, "sisera", 60, 600, 250, T("vaincu") - 0.2, rot=-2)
sticker(S6, "tente", 400, 680, 520, T("tente") - 0.3, rot=3)
label_box(S6, 400, 1180, "La tente de Jaël", "Juges 4.17", T("Jaël", 1) - 0.1)

# --- S7 · « Entre, mon seigneur… » (Juges 4.18), sous-titres coupés
t7 = T("Elle") - 0.4 if False else 26.0
cam(t7, S7)
headline(S7, 280, ["Elle l'[invite]"], t7 + 0.1, kicker="Juges 4.18", hl_t=T("Entre"), size=110)
sticker(S7, "jael-portrait", 580, 560, 370, t7 + 0.4, rot=3)
q7 = put(S7, 60, 1000, "<small>Juges 4.18 · LSG</small>« Entre, mon seigneur, entre chez moi, ne crains point. »",
         "box wide", "width:900px;font-size:36px")
blur_in(q7, T("Entre") - 0.1, 14)

# --- S8 · de l'eau, du lait, il s'endort
t8 = T("demande") - 0.5
cam(t8, S8)
headline(S8, 280, ["Il demande de l'eau,", "elle donne du [lait]"], t8 + 0.1, kicker="Juges 4.19", hl_t=T("lait"), size=84)
sticker(S8, "sisera", 60, 600, 250, T("demande") - 0.2, rot=-2)
tag(S8, 400, 700, "De l'eau", T("l'eau") - 0.1, "", 56)
tag(S8, 400, 820, "Du lait", T("lait") - 0.1, "acc", 56)
tag(S8, 400, 960, "Épuisé", T("épuisé") - 0.1, "", 52)
tag(S8, 400, 1070, "Il s'endort", T("s'endort") - 0.2, "acc", 52)

# --- S9 · le piquet et le marteau : mode sombre
t_all = T("Alors") - 1.2
cam(t_all, "all")
t9 = T("Alors") - 0.4
cam(t9, S9)
dark_mode(t9 - 0.1)
headline(S9, 280, ["Un [piquet]", "et un marteau"], t9 + 0.1, kicker="Juges 4.21", hl_t=T("piquet"), size=104, dark=True)
sticker(S9, "jael-pied", 60, 600, 300, T("Jaël", 2) - 0.2, rot=-2)
tag(S9, 420, 680, "Un piquet de tente", T("piquet") - 0.1, "dark", 44)
tag(S9, 420, 790, "Un marteau", T("marteau") - 0.1, "acc", 52)
tag(S9, 420, 940, "Elle frappe", T("frappe") - 0.1, "dark", 56)
tag(S9, 420, 1050, "jusqu'à terre", T("terre") - 0.3, "acc", 52)
hit(T("frappe"), 1.0)
hit(T("terre"), 0.8)

# --- S10 · le texte ne dit pas pourquoi : on ne le sait pas
t10 = T("texte") - 0.5
cam(t10, S10)
headline(S10, 280, ["Le texte", "[ne dit pas]"], t10 + 0.1, kicker="Ce qu'on ne sait pas", hl_t=T("pas", 1), size=104, dark=True)
tag(S10, 70, 680, "Pourquoi ?", T("pourquoi") - 0.1, "acc", 120)
label_box(S10, 70, 900, "Le récit se tait", "il ne donne pas son motif", T("choisi"), dark=True)
sticker(S10, "jael-portrait", 620, 1010, 300, T("choisi") - 0.2, rot=3)

# --- S11 · le chant de Débora (Juges 5.24), sous-titres coupés
t11 = T("chant") - 0.6
cam(t11, S11)
headline(S11, 280, ["Le chant de", "[Débora]"], t11 + 0.1, kicker="Juges 5.24", hl_t=T("Débora", 1), size=100, dark=True)
sticker(S11, "debora", 60, 620, 300, T("Débora", 1) - 0.3, rot=-2)
q11 = put(S11, 400, 660, "<small>Juges 5.24 · LSG</small>« Béni soit entre les femmes Jaël ! »",
          "box wide", "width:540px;font-size:40px")
blur_in(q11, T("Béni") - 0.1, 14)
hit(T("Béni"), 0.8)

# --- S12 · la gloire est allée à une femme sans épée
t12 = T("Détail") - 0.3
cam(t12, S12)
headline(S12, 280, ["La [gloire]"], t12 + 0.1, kicker="Détail étonnant", hl_t=T("gloire", 1), size=120, dark=True)
sticker(S12, "barak", 60, 590, 250, T("général", 1) - 0.4, rot=-3)
sticker(S12, "jael-pied", 620, 580, 280, T("femme", 2) - 0.4, rot=3)
tag(S12, 60, 1220, "Pas au général", T("général", 1) - 0.1, "dark", 48)
tag(S12, 60, 1320, "Mais à une femme sans épée", T("femme", 2) - 0.1, "acc", 44)
hit(T("épée"), 1.0)

# --- S13 · appel à commenter
t13 = T("Que") - 0.3
cam(t13, S13)
headline(S13, 330, ["Qu'en [penses-tu] ?"], t13 + 0.1, kicker="À ton tour", hl_t=T("penses-tu"), size=130, dark=True)
label_box(S13, 70, 700, "Que penses-tu de Jaël ?", "héroïne, ou geste troublant ?", T("Jaël", 3) - 0.3, dark=True)
sticker(S13, "jael-portrait", 600, 800, 340, t13 + 0.4, rot=3)
cta = put(S13, 70, 1150, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Réponds en commentaire', "cta")
blur_in(cta, T("dis-le") - 0.2, 14)
sfx("click", T("dis-le") - 0.2, 0.8)

# --- fin : vue d'ensemble puis carte de fin pendant « abonne-toi »
t_end = T("abonne-toi") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", "Le contexte", 0, t4), ("02", "Le récit", t4, t9), ("03", "Le geste", t9, t12), ("04", "La leçon", t12, DUR)],
    suppress=[(15.3, 21.9), (26.9, 30.3), (46.4, 49.5), (T("abonne-toi") - 0.7, DUR)],
    endcard={"kicker": "Abonne-toi", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("jael-portrait", 30, 1150, 330, -6), ("debora", 800, 1000, 200, 5)]},
    endcard_t=T("abonne-toi") - 0.1,
    music_volume=0.14,
)
