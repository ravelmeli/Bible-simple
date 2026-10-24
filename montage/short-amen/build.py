"""Short « Amen vient d'un mot qui veut dire solide » en style 02 — 9:16, 79,9 s.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py). Chaque élément est calé sur transcript.json.
L'hébreu est en HTML (police Noto Sans Hebrew, OFL), jamais dans une image : à faire relire avant publication.
Lancer : python3 build.py   (puis npx hyperframes check et npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Amen - style 02", "lang": "fr"}
s.setup(here=HERE, duration=79.9, cols=3, rows=5, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

N = " "
S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10, S11, S12 = (2, 3), (1, 3), (0, 3)
S13 = (0, 4)

# Police hébraïque locale (OFL) pour le mot אָמֵן écrit en HTML.
html.append('<style>@font-face{font-family:"Noto Sans Hebrew";src:url("assets/fonts/NotoSansHebrew.ttf") format("truetype");font-weight:100 900}'
            f'.heb{{font-family:"Noto Sans Hebrew",sans-serif;direction:rtl;font-weight:700;line-height:1.1;color:{INK}}}'
            '.box.wide{width:560px;text-align:left;font-size:36px}</style>')

# --- S1 · accroche : la foule mains levées dès la première image
cam(0, S1)
sticker(S1, "foule-mains-levees", 60, 560, 600, 0.0, rot=-2, instant=True)
headline(S1, 300, ["Tu le dis", "chaque [semaine]"], 0.0, kicker="Un mot de la Bible", hl_t=T("semaine") + 0.1, size=100)
tag(S1, 60, 1230, "Amen", T("amen.") - 0.1, "acc", 110)
hit(T("amen."), 0.9)

# --- S2 · « ainsi soit-il » ? En hébreu : une racine qui veut dire solide, ferme, fiable
t2 = T("on") - 0.3
cam(t2, S2)
headline(S2, 280, ["« Ainsi soit-il » ?"], t2 + 0.1, kicker="La traduction habituelle", size=96)
heb = put(S2, 300, 440, "אָמֵן", "heb", "font-size:230px")
blur_in(heb, T("hébreu") - 0.1, 20)
label_box(S2, 60, 760, "Racine hébraïque", "« être ferme, stable, fiable »", T("racine") - 0.1)
tag(S2, 60, 920, "solide", T(f"«{N}solide") - 0.05, "acc", 60)
tag(S2, 60, 1040, "ferme", T(f"«{N}ferme") - 0.05, "acc", 60)
tag(S2, 60, 1160, "fiable", T(f"«{N}fiable") - 0.05, "acc", 60)

# --- S3 · la même racine donne « foi » et « vérité »
t3 = T("la") - 0.3
cam(t3, S3)
headline(S3, 280, ["Même racine :", "[foi] et vérité"], t3 + 0.1, kicker="La famille du mot", hl_t=T(f"«{N}foi"), size=96)
sticker(S3, "bible-hebraique-espagne", 70, 560, 900, t3 + 0.2, rot=-2)
label_box(S3, 70, 1170, "Bible hébraïque", "Espagne, 1300–1350 · Met", t3 + 0.6)

# --- S4 · Exode 17.12 : ses mains restèrent fermes
t4 = T("dans") - 0.3
cam(t4, S4)
headline(S4, 280, ["Des mains", "[fermes]"], t4 + 0.1, kicker="Exode 17", hl_t=T(f"«{N}fermes"), size=100)
sticker(S4, "moise-aaron-hur", 50, 560, 520, T("moïse") - 0.2, rot=-2)
label_box(S4, 620, 600, "Aaron et Hur", "soutiennent ses mains", T("aaron"))
sticker(S4, "moise-portrait", 640, 760, 320, T("restèrent") - 0.3, rot=3)
tag(S4, 50, 1200, "« ses mains restèrent fermes »", T(f"«{N}fermes") - 0.1, "acc", 40)
ref(S4, 50, 1290, "Exode 17.12 · Louis Segond 1910", T("restèrent"))
hit(T(f"«{N}fermes"), 0.8)

# --- S5 · Ésaïe 7.9 : croire ≈ tenir debout (sous-titres coupés pendant la citation affichée)
t5 = T("prophète") - 0.6
cam(t5, S5)
headline(S5, 280, ["Croire = [tenir]", "debout"], t5 + 0.1, kicker="Ésaïe 7.9", hl_t=T("tenir"), size=96)
sticker(S5, "vitrail-esaie", 50, 580, 300, T("ésaïe") - 0.2, rot=-3)
label_box(S5, 400, 580, "Le prophète Ésaïe", "vitrail, vers 1325 · Met", T("ésaïe"))
q5 = put(S5, 400, 720, "<small>Ésaïe 7.9 · LSG</small>« Si vous ne croyez pas, vous ne subsisterez pas. »", "box wide")
blur_in(q5, T(f"«{N}si") - 0.1, 14)
tag(S5, 400, 1040, "croire ≈ tenir debout", T("croire") - 0.1, "acc", 46)
label_box(S5, 400, 1150, "En hébreu", "deux formes de la même racine", T("même", 2))

# --- S6 · Néhémie 8.6 : le peuple répond « Amen ! Amen ! »
t6 = T("quand") - 0.3
cam(t6, S6)
headline(S6, 280, ["« Amen ! [Amen] ! »"], t6 + 0.1, kicker="Néhémie 8.6", hl_t=T("amen", 3), size=100)
sticker(S6, "esdras", 50, 470, 360, T("esdras") - 0.2, rot=-2)
sticker(S6, "foule-mains-levees", 440, 560, 560, T("peuple") - 0.2, rot=3)
label_box(S6, 50, 1200, "Esdras lit la Loi", "tout le peuple répond, mains levées", T("loi") - 0.1)
ref(S6, 600, 1215, "Néhémie 8.6 · LSG", T("amen", 2))
hit(T("amen", 2), 0.8)

# --- S7 · dire amen : « c'est solide, je m'appuie dessus »
t7 = T("dire", 2) - 0.4
cam(t7, S7)
headline(S7, 280, ["« Je m'appuie", "[dessus] »"], t7 + 0.1, kicker="Le vrai sens", hl_t=T("dessus"), size=96)
sticker(S7, "rocher", 50, 560, 440, t7 + 0.2, rot=-3)
sticker(S7, "main-rocher", 540, 540, 440, T("m'appuie") - 0.2, rot=3)
tag(S7, 50, 1080, "≠ un simple vœu", T("vœu") - 0.2, "", 50)
tag(S7, 50, 1190, "= c'est solide", T("solide", 1) - 0.1, "acc", 60)

# --- vue d'ensemble au détail étonnant, puis S8 · Jésus le place au début
t_all = T("détail") - 0.2
cam(t_all, "all")
t8 = T("l'utilise") - 0.4
cam(t8, S8)
headline(S8, 280, ["Jésus le dit", "[à l'envers]"], t8 + 0.1, kicker="Détail étonnant", hl_t=T("l'envers"), size=96)
sticker(S8, "jesus", 50, 570, 340, t8 + 0.2, rot=-2)
c1 = put(S8, 430, 600, "<small>D'habitude</small>… à la fin : « Amen. »", "box wide")
c2 = put(S8, 430, 820, "<small>Jésus</small>« Amen, je vous le dis… »", "box wide")
blur_in(c1, T("fin") - 0.2, 14)
blur_in(c2, T("début") - 0.1, 14)
tween(f"#{c2}", f'backgroundColor: "#FFFFFF", color: "{INK}"', f'backgroundColor: "{ACC}", color: "#FFFFFF", duration: 0.3', T("amen", 5))
hit(T("début"), 0.8)

# --- S9 · « En vérité, je vous le dis » (sous-titres coupés pendant la citation affichée)
t9 = T("nos") - 0.3
cam(t9, S9)
headline(S9, 280, ["« En [vérité],", "je vous le dis »"], t9 + 0.1, kicker="Nos Bibles traduisent", hl_t=T("vérité", 1), size=90)
sticker(S9, "evangeliaire-carolingien", 90, 560, 860, t9 + 0.2, rot=-2)
label_box(S9, 70, 1260, "Évangéliaire latin", "vers 825–850 · Met", t9 + 0.6)

# --- S10 · révélation en mode sombre : Jésus appelé « l'Amen » (Apocalypse 3.14)
t10 = T("l'apocalypse") - 0.7
cam(t10, S10)
dark_mode(t10 - 0.1)
headline(S10, 280, ["Jésus,", "[l'Amen]"], t10 + 0.1, kicker="Apocalypse 3.14", hl_t=T("l'amen"), size=110, dark=True)
sticker(S10, "jean-patmos", 50, 560, 320, t10 + 0.2, rot=-3)
q10 = put(S10, 410, 620, "<small>Apocalypse 3.14 · LSG</small>« l'Amen, le témoin fidèle et véritable »", "box wide")
blur_in(q10, T("l'amen") - 0.2, 14)
label_box(S10, 410, 900, "Jean à Patmos", "auteur de l'Apocalypse selon la tradition", T("témoin"), dark=True)
hit(T("l'amen"), 1.0)

# --- S11 · un mot passé tel quel dans d'autres langues
t11 = T("mot", 1) - 0.5
cam(t11, S11)
headline(S11, 280, ["Passé [tel quel]"], t11 + 0.1, kicker="Dans d'autres langues", hl_t=T("tel"), size=104, dark=True)
tag(S11, 70, 560, "Grec", T("grec"), "acc", 64)
tag(S11, 70, 680, "Latin", T("latin"), "acc", 64)
tag(S11, 70, 800, "Arabe", T("arabe"), "acc", 64)
tag(S11, 70, 920, "… et bien d'autres", T("langues") - 0.2, "dark", 56)
heb11 = put(S11, 560, 600, "אָמֵן", "heb", f"font-size:200px;color:{THEME['bg']}")
blur_in(heb11, t11 + 0.3, 20)

# --- S12 · à retenir : amen = « c'est solide »
t12 = T("prochaine") - 0.6
cam(t12, S12)
headline(S12, 280, ["Amen =", "« c'est [solide] »"], t12 + 0.1, kicker="À retenir", hl_t=T("solide", 2), size=100, dark=True)
sticker(S12, "main-rocher", 280, 640, 520, t12 + 0.2, rot=-2)
hit(T("solide", 2), 0.7)

# --- S13 · appel à commenter
t13 = T("quel", 1) - 0.3
cam(t13, S13)
headline(S13, 300, ["Quel [mot]", "ensuite ?"], t13 + 0.1, kicker="À toi", hl_t=T("mot", 2), size=120, dark=True)
sticker(S13, "moise-portrait", 560, 700, 400, t13 + 0.3, rot=3)
cta = put(S13, 70, 1150, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Réponds en commentaire', "cta")
blur_in(cta, T("dis-le") - 0.2, 14)
sfx("click", T("dis-le") - 0.2, 0.8)

# --- fin · vue d'ensemble puis carte de fin pendant « abonne-toi »
t_end = T("abonne-toi") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", "Le mot", 0, t4), ("02", "La racine", t4, t_all), ("03", "Jésus", t_all, t11), ("04", "Leçon", t11, DUR)],
    suppress=[(T(f"«{N}si") - 0.1, T("en", 1) - 0.1), (T("vérité", 1) - 0.5, T("l'apocalypse") - 0.8), (T("abonne-toi") - 0.7, DUR)],
    endcard={"kicker": "Abonne-toi", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("main-rocher", 30, 1180, 360, -6), ("moise-aaron-hur", 760, 1060, 280, 5)]},
    endcard_t=T("abonne-toi") - 0.1,
    music_volume=0.12,
)
