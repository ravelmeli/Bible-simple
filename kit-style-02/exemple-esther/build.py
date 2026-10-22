"""Exemple complet du style 02 : le short « Esther » (9:16, 62,4 s), reconstruit avec le moteur du kit.

Copier ce fichier dans le dossier d'un nouveau projet, puis remplacer les stations (STORY) par la nouvelle histoire.
Lancer : python3 build.py   (puis npx hyperframes check et npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "moteur"))          # chemin vers kit-style-02/moteur
import style02 as s  # noqa: E402

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Esther - style 02", "lang": "fr"}
s.setup(here=HERE, duration=62.4, cols=3, rows=5, theme=THEME)
from style02 import *  # noqa: E402,F401,F403  (après setup : W, H, html, T, sticker, headline, cam...)

# ================================================================ STORY
S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10, S11, S12 = (2, 3), (1, 3), (0, 3)
S13 = (0, 4)

# --- S1 · 0 – 5.62 · hook: the guard is on screen from the very first frame (Est 4:11)
cam(0, S1)
g, gh = sticker(S1, "tete-garde-perse", 50, 600, 640, 0.0, rot=-4, instant=True)
label_box(S1, 60, 600 + gh + 20, "Garde perse", "relief, v. 486–465 av. J.-C.", 0.6)
headline(S1, 300, ["Entrer chez le roi", "sans [invitation] ?"], 0.0, kicker="Explication · Esther", hl_t=T("sans") + 0.2, size=100)
tag(S1, 60, 1250, "= la mort", T("mort"), "acc", 64)
ref(S1, 380, 1268, "Esther 4.11", T("mort") + 0.2)
sticker(S1, "esther-pied", 730, 640, 300, T("reine", 0) - 0.3, rot=3)
hit(T("mort"), 1.0)

# --- S2 · 5.62 – 10.7 · Esther, queen of Persia, secretly Jewish (Est 2:10)
cam(5.62, S2)
headline(S2, 300, ["Esther,", "reine de [Perse]"], T("esther") - 0.3, kicker="Le personnage", hl_t=T("perse"), size=104)
sticker(S2, "esther-portrait", 40, 590, 540, 5.9, rot=-3)
d_, dh = sticker(S2, "daric-roi", 620, 600, 380, 6.6, rot=5)
label_box(S2, 620, 600 + dh + 20, "Le roi de Perse", "daric en or, IVe s. av. J.-C.", 6.8)
tag(S2, 40, 1270, "Secret : elle est juive", T("juive"), "acc", 48)
ref(S2, 620, 1284, "Esther 2.10", T("juive") + 0.2)

# --- S3 · 10.7 – 17.85 · the decree spreads over 127 provinces, from India to Ethiopia (Est 1:1, 3:12-13)
cam(10.7, S3)
headline(S3, 280, ["Le [décret] de Haman"], T("haman") - 0.3, kicker="Le danger", hl_t=T("décret"), size=92)
map_svg(S3, 40, 560, "assets/map.json", T("haman") - 0.1, T("décret"))
sticker(S3, "haman", 830, 520, 190, T("haman") - 0.1, rot=4)
counter(S3, 40, 1150, 0, 127, T("décret") + 0.4, 127 * 0.022, " provinces", 110, "small")
label_box(S3, 610, 1160, "De l'Inde à l'Éthiopie", "Esther 1.1 · tracé schématique", T("décret") + 0.8)
tag(S3, 40, 1300, "Exécution : 1 seul jour", T("jour") - 0.15, "acc", 50)
ref(S3, 690, 1314, "Esther 3.13", T("jour"))
hit(T("décret"), 0.8)

# --- S4 · 17.85 – 22.85 · the scepter rule as a decision chart (Est 4:11)
cam(17.85, S4)
headline(S4, 280, ["Seul le [sceptre d'or]"], 18.0, kicker="La loi du palais", hl_t=T("sceptre"), size=92)
tag(S4, 70, 470, "Esther hésite", T("hésite"), "", 40)
ref(S4, 760, 482, "Esther 4.11", T("hésite") + 0.2)
f1 = put(S4, 290, 640, "Entrer sans être appelé", "box")
blur_in(f1, 19.2, 14)
f2 = put(S4, 230, 860, "Le roi tend-il<br>son sceptre d'or ?", "box q")
blur_in(f2, T("sceptre"), 14)
sx4, sy4 = st(*S4)
arrows = uid()
html.append(f'<svg class="node lead arrows" id="{arrows}" style="left:{sx4}px;top:{sy4}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<path class="a0" d="M540 748 L540 852" stroke-dasharray="110"/>'
            f'<path class="a1" d="M380 1014 L240 1172" stroke-dasharray="220"/>'
            f'<path class="a2" d="M700 1014 L840 1172" stroke-dasharray="220"/></svg>')
tween(f"#{arrows} .a0", "strokeDashoffset: 110", 'strokeDashoffset: 0, duration: 0.3', T("sceptre") - 0.2)
tween(f"#{arrows} .a1, #{arrows} .a2", "strokeDashoffset: 220", 'strokeDashoffset: 0, duration: 0.4, stagger: 0.15', T("sceptre") + 0.4)
no = put(S4, 90, 1180, "<small>Non</small>Mort", "box out")
yes = put(S4, 690, 1180, "<small>Oui</small>Vie", "box out")
blur_in(no, T("sceptre") + 0.6, 12)
blur_in(yes, T("vie") - 0.3, 12)
sfx("click", T("sceptre") + 0.6, 0.6)

# --- S5 · 22.85 – 28.5 · Mordecai's challenge (Est 4:14)
cam(22.85, S5)
headline(S5, 290, ["« Pour un temps", "comme [celui-ci] »"], T("temps") - 0.2, kicker="Mardochée · Esther 4.14", hl_t=T("temps") + 0.5, size=96)
sticker(S5, "mardochee", 60, 580, 410, T("mardochée") - 0.2, rot=-3)
c_, ch_ = sticker(S5, "chapiteau-taureau", 600, 620, 380, 23.6, rot=4)
label_box(S5, 600, 620 + ch_ + 20, "Palais perse", "chapiteau, Ve s. av. J.-C.", 23.8)
tag(S5, 520, 1200, "Et si c'était le moment ?", T("reine", 2) - 0.6, "", 38)

# --- S6 · 28.5 – 31.25 · three days of fasting (Est 4:16)
cam(28.5, S6)
headline(S6, 300, ["[3 jours] de jeûne"], T("trois") - 0.2, kicker="La préparation", hl_t=T("trois") + 0.2, size=100)
boxes(S6, 70, 560, ["1", "2", "3"], T("trois") + 0.15)
sticker(S6, "peuple-jeune", 40, 900, 600, 28.7, rot=-2)
sticker(S6, "sac-cendres", 690, 900, 320, T("jeûne"), rot=5)
label_box(S6, 690, 1150, "Tout le peuple jeûne", "sac et cendre, à Suse", T("jeûne") + 0.1)
ref(S6, 690, 1300, "Esther 4.16", T("jeûne") + 0.2)

# --- S7 · 31.25 – 34.7 · « If I perish, I perish » (captions hidden: the line is on screen)
cam(31.25, S7)
headline(S7, 380, ["Si je dois périr,", "je [périrai]."], T("périr") - 0.6, kicker="Esther · Esther 4.16", hl_t=T("périrai"), size=124)
sticker(S7, "esther-portrait", 470, 760, 520, 31.5, rot=3)
hit(T("périrai"), 1.0)

# --- mid-video pull-out over the whole canvas, then S8 · 35.65 – 38.55 · she enters, the king holds out the scepter (Est 5:2)
cam(34.7, "all")
cam(35.65, S8)
headline(S8, 280, ["Elle [entre]"], 35.7, kicker="Le moment décisif", hl_t=T("entre"), size=110)
ok = put(S8, 700, 300, "<small>Oui</small>Vie", "box out")
blur_in(ok, 36.0, 10)
es = sticker(S8, "esther-pied", 40, 540, 380, T("entre") + 0.1, rot=-2)
sticker(S8, "roi-sceptre", 420, 600, 620, 36.0, rot=2)
tween(f"#{ok}", 'backgroundColor: "#FFFFFF", color: "#1B242E"', f'backgroundColor: "{ACC}", color: "#FFFFFF", duration: 0.25', T("tend"))
tween(f"#{ok}", "scale: 1", 'scale: 1.18, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false', T("tend"))
tag(S8, 40, 1300, "Il tend son sceptre d'or", T("tend"), "acc", 48)
ref(S8, 700, 1314, "Esther 5.2", T("tend") + 0.2)
hit(T("tend"), 1.2)
sfx("spark", T("sceptre", 1), 1.0)

# --- S9 · 38.55 – 43.65 · two banquets, then Haman exposed (Est 5:4-8, 7:1-6)
cam(38.55, S9)
headline(S9, 280, ["Deux festins,", "un [piège] inversé"], T("festin") - 0.4, kicker="Le retournement", hl_t=T("dénonce"), size=88)
sx9, sy9 = st(*S9)
tl_id = uid()
html.append(f'<svg class="node lead" id="{tl_id}" style="left:{sx9}px;top:{sy9}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<path d="M120 640 L120 1180" stroke-dasharray="540"/></svg>')
tween(f"#{tl_id} path", "strokeDashoffset: 540", 'strokeDashoffset: 0, duration: 2.4, ease: "none"', T("festin") - 0.1)
for k, (title, sub, t) in enumerate([("Festin n° 1", "Esther 5.4", T("festin")), ("Festin n° 2", "Esther 7.1", T("festin") + 0.9),
                                     ("Révélation", "Esther 7.3-6", T("identité"))]):
    dot = put(S9, 106, 630 + k * 250, "", "dot")
    tween(f"#{dot}", "scale: 0", 'scale: 1, duration: 0.3, ease: "back.out(3)"', t)
    label_box(S9, 160, 610 + k * 250, title, sub, t)
sticker(S9, "rhyton-belier", 640, 560, 300, T("festin") + 0.3, rot=6)
sticker(S9, "coupe-inscription-royale", 600, 900, 330, T("festin") + 0.8, rot=-4)
label_box(S9, 600, 1250, "Vaisselle royale perse", "Ve s. av. J.-C.", T("festin") + 1.1)
tag(S9, 160, 1300, "Haman dénoncé", T("dénonce"), "acc", 50)
hit(T("dénonce"), 0.7)

# --- S10 · 43.65 – 46.45 · the gallows, to scale (Est 5:14, 7:10)
cam(43.65, S10)
headline(S10, 280, ["Pendu à sa", "propre [potence]"], 43.85, kicker="La chute de Haman", hl_t=T("potence"), size=92)
bar_h = 760                       # 50 cubits ≈ 22 m  → about 34.5 px per metre
man_h = round(1.7 * bar_h / 22)   # a man ≈ 1.7 m, same scale
base_y = 1380
bar_to_scale(S10, 220, base_y, bar_h, T("potence"))
bar_to_scale(S10, 430, base_y, man_h, T("potence") + 0.4, width=60, acc=False, dur=0.3)
label_box(S10, 400, 640, "Potence : 50 coudées", "≈ 22 m (coudée ≈ 44,5 cm)", T("potence") + 0.2)
label_box(S10, 520, base_y - 120, "Un homme", "≈ 1,7 m, même échelle", T("potence") + 0.6)
ref(S10, 400, 790, "Esther 5.14 · 7.10", T("potence") + 0.4)
sticker(S10, "haman", 820, 860, 200, 43.9, rot=4)
hit(T("potence"), 0.9)

# --- S11 · 46.45 – 50.65 · the people saved, Purim (Est 9:20-28)
cam(46.45, S11)
headline(S11, 280, ["Le peuple est [sauvé]"], T("sauvé") - 0.5, kicker="L'issue", hl_t=T("sauvé"), size=92)
r_, rh = sticker(S11, "relief-serviteurs-festin", 40, 500, 420, 46.8, rot=-4)
label_box(S11, 40, 500 + rh + 18, "Repas de fête", "relief perse, IVe s. av. J.-C.", 47.0)
sticker(S11, "esther-pied", 640, 500, 330, T("sauvé") - 0.2, rot=3)
for k, dname in enumerate(["14 Adar", "15 Adar"]):
    d = put(S11, 40 + k * 330, 1200, f'<small>Purim</small>{dname}', "day wide")
    tween(f"#{d}", 'opacity: 0, y: 40, backgroundColor: "#FFFFFF", color: "#1B242E"',
          f'opacity: 1, y: 0, backgroundColor: "{ACC}", color: "#FFFFFF", duration: 0.35, ease: "back.out(2)"', T("purim") + k * 0.35)
ref(S11, 720, 1240, "Esther 9.20-28", T("purim") + 0.3)
hit(T("sauvé"), 0.6)

# --- S12 · 50.65 – 54.6 · dark mode reveal: the book never names God
cam(50.65, S12)
dark_mode(50.6)
headline(S12, 280, ["Le livre d'Esther"], 50.95, kicker="Détail étonnant", size=92, dark=True)
sticker(S12, "rouleau-esther", 720, 470, 250, 51.1, rot=6)
counter(S12, 70, 520, 0, 10, 51.4, 0.8, " chapitres", 96, "dark small")
counter(S12, 70, 680, 0, 167, 52.0, 1.0, " versets", 96, "dark small")
label_box(S12, 70, 880, "Le nom de Dieu", "dans le texte hébreu", T("jamais") - 0.3, dark=True)
z = put(S12, 70, 980, "0", "zero")
tween(f"#{z}", "opacity: 0, scale: 2.2", 'opacity: 1, scale: 1, duration: 0.35, ease: "power4.in"', T("dieu"))
tag(S12, 460, 1110, "fois", T("dieu") + 0.3, "dark", 56)
hit(T("dieu"), 1.0)

# --- S13 · 54.6 – 59.65 · the question
cam(54.6, S13)
headline(S13, 480, ["Et [toi] ?"], T("toi") - 0.2, kicker="À ton tour", hl_t=T("toi"), size=200, dark=True)
sticker(S13, "esther-pied", 720, 820, 300, 54.8, rot=3)
cta = put(S13, 70, 1010, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Réponds en commentaire', "cta")
blur_in(cta, T("commentaire") - 0.5, 14)
sfx("click", T("commentaire") - 0.5, 0.8)

# --- end · 59.65 – 62.4 · pull out over the whole canvas, title card
cam(59.65, "all")


# ================================================================ assemble
build(
    chapters=[("01", "Danger", 0, 17.85), ("02", "Décision", 17.85, 34.85), ("03", "Retournement", 34.85, 50.65), ("04", "Leçon", 50.65, DUR)],
    suppress=[(31.3, 36.0), (59.6, DUR)],     # citation affichée en grand, puis carte de fin : pas de sous-titres
    endcard={"kicker": "Abonne-toi", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("tete-garde-perse", 40, 1180, 380, -6), ("esther-pied", 790, 1060, 240, 5)]},
    endcard_t=60.2,
)
