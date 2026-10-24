"""Short « Qui est mon prochain ? » (Luc 10.25-37) en style 02 — 9:16, 65,6 s.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py). Chaque élément est calé sur transcript.json.
Lancer : python3 build.py   (puis npx hyperframes check et npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Qui est mon prochain - style 02", "lang": "fr"}
s.setup(here=HERE, duration=65.6, cols=3, rows=5, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

# ================================================================ STORY
S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10, S11, S12 = (2, 3), (1, 3), (0, 3)
S13 = (0, 4)

# --- S1 · 0 – 8.6 · accroche : le docteur de la loi est là dès la première image (Luc 10.25-29)
cam(0, S1)
sticker(S1, "docteur-pied", 60, 600, 320, 0.0, rot=-3, instant=True)
headline(S1, 300, ["Obligé d'[aimer]", "qui, au juste ?"], 0.0, kicker="Explication · Luc 10", hl_t=T("d'aimer") + 0.1, size=96)
label_box(S1, 440, 640, "Un docteur de la loi", "spécialiste de la loi de Moïse", T("docteur"))
tag(S1, 440, 800, "Sa question à Jésus", T("question") - 0.1, "", 40)
tag(S1, 60, 1290, "« Et qui est mon prochain ? »", T("« Et"), "acc", 48)
ref(S1, 60, 1385, "Luc 10.29 · Louis Segond 1910", T("prochain") + 0.2)
hit(T("prochain"), 0.8)

# --- S2 · 8.6 – 10.6 · Jésus répond par une histoire
cam(8.6, S2)
headline(S2, 300, ["Une [histoire]"], T("répond") - 0.3, kicker="La réponse de Jésus", hl_t=T("histoire"), size=110)
sticker(S2, "jesus", 300, 520, 430, 8.8, rot=-2)

# --- S3 · 10.6 – 16.4 · la route : de Jérusalem (+750 m) à Jéricho (−250 m), 27 km (ordres de grandeur)
cam(10.6, S3)
headline(S3, 280, ["De [Jérusalem]", "à Jéricho"], 10.75, kicker="La route", hl_t=T("jérusalem"), size=96)
sticker(S3, "route-jericho-aerien", 60, 580, 520, T("descend"), rot=-2)
label_box(S3, 60, 975, "L'ancienne route, vue d'avion", "photo Matson, vers 1930", T("descend") + 0.3)
counter(S3, 640, 590, 0, 27, T("27") - 0.05, 0.6, " km", 120, "small")
tag(S3, 640, 770, "≈ 1 000 m", T("1 000"), "acc", 48)
ref(S3, 640, 865, "de dénivelé", T("descente"))
sx3, sy3 = st(*S3)
prof = uid()
# Profil schématique : 1 000 m sur 260 px ; le niveau de la mer est à 70 + 750 × 0,26 = 265 px.
html.append(f'<svg class="node lead" id="{prof}" style="left:{sx3 + 40}px;top:{sy3 + 1070}px" width="1000" height="360" viewBox="0 0 1000 360">'
            f'<path class="sea" d="M20 265 L980 265" style="stroke:#AEB8C3;stroke-dasharray:10 10;stroke-width:3"/>'
            f'<path class="pr" d="M40 70 C 200 80, 260 120, 360 140 S 560 200, 640 230 S 820 300, 940 330" '
            f'style="stroke:{ACC};stroke-width:8;stroke-linecap:round" stroke-dasharray="1000"/>'
            f'<circle cx="40" cy="70" r="12" style="fill:{INK}"/><circle class="end" cx="940" cy="330" r="12" style="fill:{ACC}"/>'
            f'<text x="62" y="60" style="font:700 30px Inter;fill:{INK}">Jérusalem ≈ +750 m</text>'
            f'<text class="tj" x="900" y="355" text-anchor="end" style="font:700 30px Inter;fill:{INK}">Jéricho ≈ −250 m</text>'
            f'<text x="20" y="255" style="font:600 22px Inter;fill:#6B7785;letter-spacing:2px">NIVEAU DE LA MER</text></svg>')
blur_in(prof, T("jérusalem") - 0.2, 10)
tween(f"#{prof} .pr", "strokeDashoffset: 1000", 'strokeDashoffset: 0, duration: 1.4, ease: "power2.inOut"', T("descend"))
tween(f"#{prof} .end, #{prof} .tj", "opacity: 0", "opacity: 1, duration: 0.3", T("jéricho"))

# --- S4 · 16.4 – 18.9 · les brigands (Luc 10.30)
cam(16.4, S4)
headline(S4, 300, ["À [demi mort]"], T("des") - 0.1, kicker="Les brigands", hl_t=T("demi mort"), size=110)
sticker(S4, "blesse", 90, 560, 900, T("brigands") - 0.1, rot=-2)
tag(S4, 60, 1250, "Dépouillé, frappé, abandonné", T("laissent"), "acc", 46)
ref(S4, 60, 1345, "Luc 10.30", T("demi mort"))
hit(T("brigands"), 0.8)

# --- S5 · 18.9 – 26.6 · le prêtre et le lévite passent (Luc 10.31-32)
cam(18.9, S5)
headline(S5, 280, ["Deux hommes", "du [Temple]"], 19.0, kicker="Ceux qui passent", hl_t=T("lévite") , size=96)
sticker(S5, "pretre", 60, 590, 310, T("prêtre") - 0.1, rot=-2)
label_box(S5, 60, 1170, "Un prêtre", "sert à l'autel du Temple", T("prêtre") + 0.2)
sticker(S5, "levite", 540, 590, 310, T("lévite") - 0.1, rot=2)
label_box(S5, 540, 1190, "Un lévite", "aide au service du Temple", T("lévite") + 0.2)
tag(S5, 60, 1300, "Motif : non précisé", T("texte") , "", 40)
ref(S5, 540, 1315, "Luc 10.31-32", T("texte") + 0.2)

# --- S6 · 26.6 – 33.2 · le Samaritain (Luc 10.33 ; Jean 4.9)
cam(26.6, S6)
headline(S6, 280, ["Un [Samaritain]"], T("puis") - 0.1, kicker="Le troisième", hl_t=T("samaritain"), size=104)
sticker(S6, "samaritain-portrait", 60, 470, 500, T("samaritain") - 0.2, rot=-3)
label_box(S6, 600, 560, "Juifs et Samaritains", "« n'ont pas de relations »", T("juifs") - 0.1)
ref(S6, 600, 690, "Jean 4.9", T("juifs") + 0.2)
tag(S6, 60, 1150, "Ému de compassion", T("ému"), "acc", 56)
ref(S6, 60, 1260, "Luc 10.33", T("compassion"))
hit(T("compassion"), 0.9)

# --- S7 · 33.2 – 36.4 · huile et vin (Luc 10.34)
cam(33.2, S7)
headline(S7, 280, ["[Huile] et vin"], T("il") - 0.1, kicker="Les premiers soins", hl_t=T("l'huile"), size=104)
sticker(S7, "samaritain-soigne", 50, 470, 640, T("soigne") - 0.2, rot=-2)
sticker(S7, "amphore-vin", 740, 440, 170, T("vin,") - 0.2, rot=4)
label_box(S7, 520, 1080, "Amphore à vin", "romaine, v. 100 av. J.-C.", T("vin,"))
ref(S7, 60, 1095, "Luc 10.34", T("plaies"))

# --- S8 · 36.4 – 38.2 · jusqu'à l'auberge, sur sa propre monture (Luc 10.34)
cam(36.4, S8)
headline(S8, 280, ["Jusqu'à", "l'[auberge]"], 36.5, kicker="Sur sa propre monture", hl_t=T("auberge"), size=96)
sticker(S8, "auberge-bon-samaritain-aerien", 60, 590, 560, 36.55, rot=-2)
sticker(S8, "samaritain-ane", 640, 610, 300, T("conduit"), rot=3)
label_box(S8, 60, 1030, "« Auberge du Bon Samaritain »", "site désigné par la tradition · vers 1930", T("auberge"))

# --- S9 · 38.2 – 42.3 · deux deniers ≈ deux journées de travail (Luc 10.35 ; Matthieu 20.2)
cam(38.2, S9)
headline(S9, 280, ["[2 deniers]"], T("paie") - 0.1, kicker="Le prix payé", hl_t=T("deniers"), size=110)
sticker(S9, "denier-tibere", 60, 470, 380, T("deniers") - 0.2, rot=-4)
label_box(S9, 60, 860, "Denier de Tibère", "argent, règne 14–37 apr. J.-C.", T("deniers") + 0.2)
sticker(S9, "main-deniers", 540, 470, 380, 38.45, rot=4)
boxes(S9, 60, 1000, ["1", "2"], T("jours") - 0.1)
ref(S9, 60, 1300, "1 denier ≈ 1 journée · Matthieu 20.2", T("salaire"))
hit(T("deniers"), 0.8)

# --- vue d'ensemble au retournement, puis S10 · 43.3 – 47.4 · « lequel des trois ? » (Luc 10.36)
cam(42.3, "all")
cam(43.3, S10)
headline(S10, 280, ["Lequel des [trois] ?"], 43.4, kicker="Jésus retourne la question", hl_t=T("prochain", 1), size=96)
for k, (name, w, t) in enumerate([("pretre", 250, 44.7), ("levite", 250, 45.1), ("samaritain-portrait", 280, 45.5)]):
    sticker(S10, name, 60 + k * 310, 560, w, t, rot=(-3, 2, -2)[k])
    tag(S10, 120 + k * 310, 1100, str(k + 1), t + 0.15, "acc" if k == 2 else "", 56)
ref(S10, 60, 1240, "Luc 10.36", 45.9)

# --- S11 · 47.4 – 52.9 · révélation en mode sombre : il ne dit pas « le Samaritain » (Luc 10.37)
cam(47.4, S11)
dark_mode(47.3)
headline(S11, 300, ["« Celui qui a exercé", "la [miséricorde]. »"], T("« celui") - 0.1, kicker="La réponse du docteur", hl_t=T("miséricorde"), size=84, dark=True)
ref(S11, 70, 600, "Luc 10.37 · Louis Segond 1910", T("miséricorde") + 0.2)
sticker(S11, "docteur-portrait", 50, 730, 420, T("docteur", 1) - 0.1, rot=-3)
label_box(S11, 520, 780, "Le mot « Samaritain »", "dans sa réponse", T("ne", 1), dark=True)
z = put(S11, 520, 880, "0", "zero")
tween(f"#{z}", "opacity: 0, scale: 2.2", 'opacity: 1, scale: 1, duration: 0.35, ease: "power4.in"', T("samaritain", 1))
tag(S11, 800, 1110, "fois", T("samaritain", 1) + 0.3, "dark", 56)
hit(T("samaritain", 1), 1.0)

# --- S12 · 52.9 – 56.9 · « Va, et toi, fais de même. » (captions cachées : la phrase est à l'écran)
cam(52.9, S12)
headline(S12, 300, ["« Va, et toi,", "fais [de même]. »"], T("conclut") - 0.3, kicker="Jésus conclut", hl_t=T("même", 1), size=104, dark=True)
ref(S12, 70, 600, "Luc 10.37", T("« va"))
sticker(S12, "jesus", 520, 660, 360, 53.1, rot=2)
hit(T("même", 1), 1.0)

# --- S13 · 56.9 – 61.75 · la question au spectateur, appel à commenter
cam(56.9, S13)
headline(S13, 380, ["Et [toi] ?"], T("toi", 1) - 0.3, kicker="À ton tour", hl_t=T("toi", 1), size=200, dark=True)
sticker(S13, "samaritain-ane", 560, 760, 380, 57.4, rot=3)
label_box(S13, 70, 760, "De qui vas-tu", "te rendre proche cette semaine ?", T("rendre") - 0.3, dark=True)
cta = put(S13, 70, 1260, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Réponds en commentaire', "cta")
blur_in(cta, T("dis-le") - 0.2, 14)
sfx("click", T("dis-le") - 0.2, 0.8)

# --- fin · vue d'ensemble puis carte de fin pendant « abonne-toi »
cam(61.75, "all")

# ================================================================ assemble
build(
    chapters=[("01", "La question", 0, 10.6), ("02", "L'histoire", 10.6, 42.3), ("03", "Retournement", 42.3, 56.9), ("04", "Leçon", 56.9, DUR)],
    suppress=[(6.0, 10.2), (44.6, 46.8), (47.4, 49.8), (53.4, 57.6), (61.9, DUR)],
    endcard={"kicker": "Abonne-toi", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("samaritain-portrait", 40, 1150, 330, -6), ("denier-tibere", 760, 1200, 260, 6)]},
    endcard_t=T("abonne-toi"),
)
