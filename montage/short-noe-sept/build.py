"""Short « Noé n'a pas fait monter que 2 animaux de chaque espèce » (Genèse 7.2) en style 02 — 9:16, 57,2 s.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py). Chaque élément est calé sur transcript.json.
Lancer : python3 build.py   (puis npx hyperframes check et npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Noé, sept couples - style 02", "lang": "fr"}
s.setup(here=HERE, duration=57.2, cols=3, rows=4, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)


def tiles(station, x, y, n, t, cols=7, size=56, gap=12, step=0.09):
    """Cases grises qui passent à l'accent une à une (une case = un animal)."""
    cells = "".join(f'<i style="width:{size}px;height:{size}px"></i>' for _ in range(n))
    i = put(station, x, y, cells, "grid", f"grid-template-columns:repeat({cols},{size}px);gap:{gap}px")
    blur_in(i, t - 0.3, 10)
    tw.append(f'tl.fromTo("#{i} i", {{ backgroundColor: "{THEME["tile"]}", scale: 0.6 }}, '
              f'{{ backgroundColor: "{ACC}", scale: 1, duration: 0.2, ease: "back.out(3)", stagger: {step} }}, {at(t)});')
    sfx("tick", t, 0.25, min(n * step + 0.2, 1.5))
    return i


# --- S1 · accroche : Noé et le vitrail de l'arche dès la première image
cam(0, S1)
sticker(S1, "noe-pied", 60, 600, 330, 0.0, rot=-3, instant=True)
headline(S1, 300, ["Combien d'animaux", "dans l'[arche] ?"], 0.0, kicker="Explication · Genèse 6–8", hl_t=T("l'arche") + 0.1, size=92)
sticker(S1, "vitrail-porte-arche", 560, 620, 330, 0.8, rot=3)
label_box(S1, 440, 1290, "Vitrail, vers 1190", "Dieu ferme la porte de l'arche", 1.2)

# --- S2 · « deux de chaque espèce ? »
t2 = T("deux") - 0.3
cam(t2, S2)
headline(S2, 300, ["[Deux] de chaque", "espèce ?"], t2 + 0.1, kicker="Ce qu'on croit", hl_t=T("deux"), size=100)
sticker(S2, "moutons", 140, 620, 640, t2 + 0.2, rot=-2)
tag(S2, 60, 1250, "Pas tout à fait", T("pas") - 0.1, "acc", 60)
hit(T("pas"), 0.8)

# --- S3 · Genèse 6 : deux de chaque espèce, un mâle et une femelle
t3 = T("au") - 0.3
cam(t3, S3)
headline(S3, 280, ["Genèse 6 :", "[2] par espèce"], t3 + 0.1, kicker="Premier ordre", hl_t=T("deux", 1), size=100)
sticker(S3, "colombe-1", 60, 560, 420, T("deux", 1) - 0.2, rot=-4)
sticker(S3, "colombe-2", 540, 560, 420, T("deux", 1) + 0.1, rot=4)
label_box(S3, 60, 1050, "Un mâle", "", T("mâle") - 0.1)
label_box(S3, 540, 1050, "une femelle", "", T("femelle") - 0.1)
ref(S3, 60, 1180, "Genèse 6.19", T("femelle"))

# --- S4 · Genèse 7 : sept couples d'animaux purs, une paire d'animaux impurs (infographie)
t4 = T("mais") - 0.3
cam(t4, S4)
headline(S4, 280, ["Genèse 7 :", "[7 couples]"], t4 + 0.1, kicker="La précision", hl_t=T("sept"), size=100)
sticker(S4, "moutons", 50, 600, 300, T("purs") - 0.4, rot=-3)
label_box(S4, 390, 600, "Animaux purs", "7 couples, mâle et femelle", T("purs") - 0.2)
tiles(S4, 390, 720, 14, T("sept"))
sticker(S4, "chameaux", 50, 960, 300, T("paire") - 0.4, rot=3)
label_box(S4, 390, 960, "Animaux impurs", "une seule paire", T("paire") - 0.2)
tiles(S4, 390, 1080, 2, T("paire"))
ref(S4, 60, 1320, "Genèse 7.2 · Louis Segond 1910", T("« tu"))
hit(T("sept"), 0.8)

# --- S5 · pourquoi ? Noé offre des sacrifices d'animaux purs (Genèse 8.20)
t5 = T("pourquoi") - 0.3
cam(t5, S5)
headline(S5, 280, ["Pourquoi plus", "d'animaux [purs] ?"], t5 + 0.1, kicker="L'indice", hl_t=T("purs", 2), size=92)
sticker(S5, "plat-sacrifice-noe", 50, 560, 520, T("indice") - 0.2, rot=-3)
label_box(S5, 50, 1100, "Le sacrifice de Noé", "plat italien, vers 1600 · Met", T("sacrifices") - 0.2)
sticker(S5, "autel-priere", 600, 620, 400, T("sacrifices") - 0.4, rot=3)
ref(S5, 600, 1000, "Genèse 8.20", T("sacrifices"))
tag(S5, 50, 1250, "1 seul couple = espèce perdue", T("seul") - 0.1, "acc", 44)

# --- S6 · avant la loi de Moïse, la différence pur / impur existe déjà (Lévitique 11)
t6 = T("détail") - 0.3
cam(t6, S6)
headline(S6, 280, ["Avant la [loi]", "de Moïse"], t6 + 0.1, kicker="Détail étonnant", hl_t=T("loi"), size=100)
sx6, sy6 = st(*S6)
tl6 = uid()
html.append(f'<svg class="node lead" id="{tl6}" style="left:{sx6}px;top:{sy6}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<path d="M140 620 L860 620" stroke-dasharray="730" style="stroke-width:6"/>'
            f'<circle cx="140" cy="620" r="14" style="fill:{ACC}"/><circle class="e" cx="860" cy="620" r="14" style="fill:{INK}"/></svg>')
tween(f"#{tl6} path", "strokeDashoffset: 730", 'strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut"', T("moïse") - 0.2)
label_box(S6, 60, 660, "Noé", "Genèse 7", T("loi") - 0.1)
label_box(S6, 640, 660, "Loi de Moïse", "Lévitique 11", T("moïse"))
sticker(S6, "chameau-terre-cuite", 80, 820, 360, T("différence") - 0.3, rot=-3)
label_box(S6, 470, 900, "Chameau : impur", "Lévitique 11.4", T("impur"))
label_box(S6, 470, 1010, "Figurine en terre cuite", "Égypte romaine, IIe–IIIe s. · Met", T("impur") + 0.3)
tag(S6, 60, 1250, "Pur / impur : déjà là", T("déjà") - 0.2, "acc", 52)

# --- vue d'ensemble, puis S7 · révélation en mode sombre : l'hébreu dit « sept, sept »
t_all = T("en", 1) - 0.4
cam(t_all, "all")
t7 = T("hébreu") + 0.1
cam(t7, S7)
dark_mode(t7 - 0.1)
headline(S7, 300, ["« Sept, [sept] »"], t7 + 0.1, kicker="En hébreu · shiv'ah shiv'ah", hl_t=T("sept, sept"), size=130, dark=True)
b1 = put(S7, 70, 640, "<small>Louis Segond</small>7 couples", "box out", "width:430px;font-size:60px")
b2 = put(S7, 560, 640, "<small>Autres versions</small>7 bêtes", "box out", "width:430px;font-size:60px")
blur_in(b1, T("couples", 1) - 0.2, 14)
blur_in(b2, T("bêtes") - 0.2, 14)
label_box(S7, 70, 900, "Les traducteurs hésitent", "le texte hébreu admet les deux lectures", T("traducteurs") - 0.1, dark=True)
hit(T("sept, sept"), 1.0)

# --- S8 · deux lectures chez les spécialistes
t8 = T("certains") - 0.3
cam(t8, S8)
headline(S8, 300, ["Deux [lectures]"], t8 + 0.1, kicker="Chez les spécialistes", hl_t=T("récits"), size=110, dark=True)
c1 = put(S8, 70, 560, "<small>Hypothèse</small>Deux récits mêlés", "box", "width:430px")
c2 = put(S8, 560, 560, "<small>Lecture suivie</small>Règle puis précision", "box", "width:430px")
blur_in(c1, T("récits") - 0.2, 14)
blur_in(c2, T("règle") - 0.2, 14)
sticker(S8, "tablette-atra-hasis", 120, 860, 300, T("précision") - 0.6, rot=-3)
label_box(S8, 460, 920, "Le Déluge, aussi à Babylone", "tablette d'Atra-hasis · Met", T("précision") - 0.4, dark=True)

# --- S9 · appel à commenter
t9 = T("tu", 1) - 0.3
cam(t9, S9)
headline(S9, 300, ["Tu le [savais] ?"], t9 + 0.1, kicker="À toi", hl_t=T("savais"), size=120, dark=True)
sticker(S9, "noe-portrait", 520, 600, 440, t9 + 0.2, rot=3)
cta = put(S9, 70, 1150, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Réponds en commentaire', "cta")
blur_in(cta, T("dis-le") - 0.2, 14)
sfx("click", T("dis-le") - 0.2, 0.8)

# --- fin · vue d'ensemble puis carte de fin pendant « abonne-toi »
t_end = T("abonne-toi") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", "La question", 0, t3), ("02", "Le texte", t3, t5), ("03", "L'explication", t5, t_all), ("04", "L'hébreu", t_all, DUR)],
    suppress=[(T("abonne-toi") - 0.7, DUR)],
    endcard={"kicker": "Abonne-toi", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("moutons", 30, 1180, 380, -6), ("noe-pied", 800, 1040, 220, 5)]},
    endcard_t=T("abonne-toi") - 0.1,
)
