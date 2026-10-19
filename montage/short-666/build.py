"""Generate index.html for the 60-second 9:16 short « 666 ».

Scene timings follow the Whisper segments of the voice-over (assets/voix.wav).
Run: python3 build.py
"""

SCENES = []  # (id, start, end, decor, html)
TWEENS = []  # JS lines


def el(src, w, h, style, cls="el"):
    return f'<img class="{cls}" src="assets/elements/{src}.png" style="width:{w}px;height:{h}px;{style}" />'


def card(inner, top, extra_cls="", left=70, width=940):
    return (f'<div class="card-wrap {extra_cls}" style="top:{top}px;left:{left}px;width:{width}px">'
            f'<div class="card">{inner}</div></div>')


def appear(sel, at, y=30, dur=0.6, ease="power3.out", rot=None):
    frm = f"opacity: 0, y: {y}" + (f", rotation: {rot[0]}" if rot else "")
    to = f"opacity: 1, y: 0, duration: {dur}, ease: \"{ease}\"" + (f", rotation: {rot[1]}" if rot else "")
    TWEENS.append(f'tl.fromTo("{sel}", {{ {frm} }}, {{ {to} }}, {at});')


def fade_out(sel, at, dur=0.4):
    TWEENS.append(f'tl.to("{sel}", {{ opacity: 0, duration: {dur}, ease: "power1.in" }}, {at});')


# ---------- P1 Patmos: hook, Jean, 666, verse (0 – 12.5) ----------
hook = card(
    '<span class="kicker">Apocalypse 13</span><span class="rule"></span>'
    '<p class="big">' + " ".join(
        f'<span class="w{" accent" if w == "nom" else ""}">{w}</span>'
        for w in ["Un", "nombre", "peut-il", "cacher", "le", "nom", "d'un", "homme&nbsp;?"]) + "</p>",
    330, "p1-hook")
p1 = (
    hook
    + el("personnage-01-jean-patmos", 607, 1180, "left:-30px;bottom:-40px", "el p1-jean")
    + '<p class="ribbon p1-cap" style="top:170px">Depuis Patmos, Jean donne une énigme…</p>'
    + '<div class="medallion p1-medal" style="left:495px;top:500px"><div class="disc"></div>'
      '<svg viewBox="0 0 500 500"><circle cx="250" cy="250" r="238" transform="rotate(-90 250 250)" />'
      '<circle class="inner" cx="250" cy="250" r="214" transform="rotate(-90 250 250)" /></svg>'
      '<div class="medal-num">666</div></div>'
    + card('<p class="quote">« Que celui qui a de l\'intelligence calcule ce&nbsp;nombre. »</p>'
           '<span class="ref">Apocalypse 13.18</span>', 150, "p1-quote")
)
SCENES.append(("p1", 0, 12.5, "patmos", p1))
TWEENS += [
    'tl.fromTo("#p1 .p1-hook .card", { opacity: 0, y: 40, rotation: -3 }, { opacity: 1, y: 0, rotation: -1.5, duration: 0.7, ease: "power3.out" }, 0.05);',
    'tl.fromTo("#p1 .p1-hook .rule", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power2.inOut" }, 0.4);',
    'tl.fromTo("#p1 .p1-hook .w", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out", stagger: 0.24 }, 0.55);',
    'tl.to("#p1 .p1-hook .card", { opacity: 0, y: -60, rotation: -3, duration: 0.45, ease: "power2.in" }, 3.0);',
    'tl.fromTo("#p1 .p1-jean", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 1.1, ease: "power3.out" }, 3.2);',
]
appear("#p1 .p1-cap", 3.4, 20, 0.7, "power2.out")
fade_out("#p1 .p1-cap", 7.2)
TWEENS += [
    'tl.fromTo("#p1 .p1-medal", { opacity: 0, scale: 0.6, rotation: -20 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.7, ease: "back.out(1.6)" }, 5.75);',
    'tl.fromTo("#p1 .p1-medal circle", { strokeDashoffset: 1500 }, { strokeDashoffset: 0, duration: 1.1, ease: "power2.inOut", stagger: 0.12 }, 5.9);',
    'tl.fromTo("#p1 .p1-medal .medal-num", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, 6.5);',
    'tl.to("#p1 .p1-medal", { opacity: 0, y: -40, duration: 0.5, ease: "power2.in" }, 7.8);',
]
appear("#p1 .p1-quote .card", 8.15, 40, 0.7, rot=(2.5, 1))

# ---------- P2 Bureau: Hebrew letters carry numbers (12.5 – 15.3) ----------
tiles = "".join(
    f'<div class="tile p2-t" style="left:{x}px"><span class="val">{v}</span><span class="heb">{l}</span></div>'
    for x, l, v in [(190, "ג", 3), (430, "ב", 2), (670, "א", 1)])
p2 = (card('<p class="mid">En hébreu, chaque lettre a une <span class="accent">valeur numérique</span>.</p>', 170, "p2-card")
      + f'<div class="tiles" style="top:600px">{tiles}</div>'
      + el("personnage-03-scribe-hebreu", 410, 1076, "left:20px;bottom:-40px", "el p2-scribe"))
SCENES.append(("p2", 12.5, 15.3, "bureau", p2))
appear("#p2 .p2-card .card", 12.75, 30, rot=(-2, -1))
appear("#p2 .p2-scribe", 12.8, 80, 0.9)
TWEENS.append('tl.fromTo("#p2 .p2-t", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.8)", stagger: -0.35 }, 13.4);')

# ---------- P3 Parchment: Néron César in Hebrew = 666 (15.3 – 22.7) ----------
# Visual left-to-right order of the right-to-left word נרון קסר.
letters = [("ר", 200), ("ס", 60), ("ק", 100), None, ("ן", 50), ("ו", 6), ("ר", 200), ("נ", 50)]
x = 60
html_tiles = []
reading = []
for item in letters:
    if item is None:
        x += 40
        continue
    l, v = item
    html_tiles.append((x, l, v))
    x += 128
# Reveal right to left, the reading order of Hebrew.
order = list(reversed(range(len(html_tiles))))
tiles = ""
for idx, (tx, l, v) in enumerate(html_tiles):
    rank = order.index(idx)
    tiles += f'<div class="tile small p3-t p3-t{rank}" style="left:{tx}px"><span class="val">{v}</span><span class="heb">{l}</span></div>'
p3 = (
    '<div class="head" style="top:170px"><span class="kicker">Néron César en hébreu</span>'
    '<p class="big ink">Néron César</p></div>'
    f'<div class="tiles" style="top:560px">{tiles}</div>'
    '<p class="sum p3-sum" style="top:900px">50 + 200 + 6 + 50 + 100 + 60 + 200</p>'
    '<p class="total p3-total" style="top:1010px">= 666</p>'
)
SCENES.append(("p3", 15.3, 22.7, "parchemin", p3))
appear("#p3 .head", 15.55, 24)
for rank in range(7):
    TWEENS.append(f'tl.fromTo("#p3 .p3-t{rank}", {{ opacity: 0, y: 30, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.8)" }}, {16.6 + rank * 0.5:.2f});')
appear("#p3 .p3-sum", 20.0, 20, 0.6)
TWEENS.append('tl.fromTo("#p3 .p3-total", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.6, ease: "back.out(2.2)" }, 21.2);')

# ---------- P4 Rome: Néron, 54 – 68, persecutions (22.7 – 28.5) ----------
p4 = (card('<span class="kicker">Néron · empereur de Rome</span><p class="big">54 – 68 <span class="smallcaps">apr. J.-C.</span></p>', 170, "p4-card")
      + card('<p class="mid">Des historiens rapportent ses <span class="accent">persécutions</span> contre les chrétiens.</p>', 530, "p4-card2")
      + el("personnage-02-neron", 470, 1150, "right:30px;bottom:-40px", "el p4-neron")
      + el("personnage-06-chretien-priere", 400, 630, "left:30px;bottom:60px", "el p4-chretien"))
SCENES.append(("p4", 22.7, 28.5, "rome", p4))
appear("#p4 .p4-neron", 22.9, 100, 1.0)
appear("#p4 .p4-card .card", 23.1, 30, rot=(-2.5, -1))
appear("#p4 .p4-card2 .card", 25.4, 30, rot=(2, 0.8))
appear("#p4 .p4-chretien", 25.9, 60, 0.9)

# ---------- P5 Study: scholars, hypothesis (28.5 – 35.9) ----------
p5 = (card('<p class="mid">Beaucoup de spécialistes pensent que Jean visait <span class="accent">ce nom</span>.</p>', 160, "p5-card")
      + '<div class="stamp p5-stamp" style="top:520px">Hypothèse</div>'
      + card('<p class="small">Le même calcul donne aussi d\'autres noms.</p>', 720, "p5-card2", left=150, width=780)
      + el("personnage-04-erudit-grec", 481, 1050, "left:10px;bottom:-30px", "el p5-erudit")
      + el("objet-07-loupe", 217, 460, "right:110px;bottom:180px", "el p5-loupe"))
SCENES.append(("p5", 28.5, 35.9, "salle", p5))
appear("#p5 .p5-erudit", 28.7, 80, 0.9)
appear("#p5 .p5-card .card", 28.9, 30, rot=(-2, -1))
appear("#p5 .p5-loupe", 29.6, 40, 0.8)
TWEENS.append('tl.fromTo("#p5 .p5-stamp", { opacity: 0, scale: 1.8, rotation: -14 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.35, ease: "power4.in" }, 31.9);')
appear("#p5 .p5-card2 .card", 33.9, 24, rot=(1.5, 0.5))

# ---------- P6 Desk: why keep the idea (35.9 – 42.9) ----------
p6 = (card('<p class="big">Alors pourquoi garder cette idée&nbsp;?</p>', 170, "p6-card")
      + card('<p class="mid">Elle montre comment les premiers chrétiens lisaient leur époque<span class="p6-prud">… <span class="accent">avec prudence</span>.</span></p>', 560, "p6-card2")
      + el("personnage-06-chretien-priere", 420, 661, "right:40px;bottom:50px", "el p6-chretien"))
SCENES.append(("p6", 35.9, 42.9, "bureau", p6))
appear("#p6 .p6-card .card", 36.2, 30, rot=(-2, -1))
appear("#p6 .p6-card2 .card", 38.3, 30, rot=(2, 0.6))
appear("#p6 .p6-chretien", 38.6, 60, 0.9)
TWEENS.append('tl.fromTo("#p6 .p6-prud", { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "power1.out" }, 41.5);')

# ---------- P7 Rome: the lesson (42.9 – 48.1) ----------
p7 = (card('<span class="kicker">Ce que le texte nous apprend</span><span class="rule"></span>'
           '<p class="big">Ne pas laisser le pouvoir décider de notre <span class="accent">fidélité</span>.</p>', 300, "p7-card")
      + el("objet-05-balance", 440, 461, "left:320px;bottom:230px", "el p7-balance"))
SCENES.append(("p7", 42.9, 48.1, "rome", p7))
appear("#p7 .p7-card .card", 43.3, 40, rot=(-2.5, -1))
TWEENS.append('tl.fromTo("#p7 .p7-card .rule", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power2.inOut" }, 43.6);')
appear("#p7 .p7-balance", 44.2, 50, 0.9)

# ---------- P8 Parchment: wisdom, not a code (48.1 – 51.8) ----------
p8 = ('<div class="head" style="top:360px"><p class="big ink">Lire ce passage,<br />c\'est chercher la sagesse,</p>'
      '<p class="big accent p8-pas">pas un code.</p></div>'
      + el("objet-09-codex-ferme", 330, 380, "left:220px;bottom:400px", "el p8-codex")
      + el("objet-11-lampe-huile", 329, 220, "right:170px;bottom:420px", "el p8-lampe"))
SCENES.append(("p8", 48.1, 51.8, "parchemin", p8))
appear("#p8 .head .ink", 48.45, 24)
appear("#p8 .p8-pas", 50.2, 20, 0.5, "back.out(2)")
appear("#p8 .p8-codex", 48.8, 40, 0.8)
appear("#p8 .p8-lampe", 49.1, 40, 0.8)

# ---------- P9 Patmos callback: comment (51.8 – 55.7) ----------
bubble = ('<svg class="bubble" viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 '
          'a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z" /></svg>')
p9 = (card('<p class="mid">Quel verset de l\'Apocalypse t\'a le plus <span class="accent">intrigué</span>&nbsp;?</p>'
           f'<span class="cta p9-cta">{bubble}Écris-le en commentaire</span>', 190, "p9-card")
      + el("personnage-01-jean-patmos", 607, 1180, "left:-30px;bottom:-40px", "el p9-jean"))
SCENES.append(("p9", 51.8, 55.7, "patmos", p9))
appear("#p9 .p9-jean", 51.9, 80, 0.9)
appear("#p9 .p9-card .card", 52.05, 30, rot=(-2, -1))
appear("#p9 .p9-cta", 54.5, 16, 0.5)
TWEENS.append('tl.fromTo("#p9 .bubble path", { strokeDashoffset: 420 }, { strokeDashoffset: 0, duration: 0.8, ease: "power2.inOut" }, 54.5);')

# ---------- P10 End card (55.7 – 60) ----------
p10 = ('<div class="head end" style="top:560px"><span class="kicker">Abonne-toi</span><span class="rule"></span>'
       '<p class="title ink">La Bible Simple</p><span class="rule"></span>'
       '<p class="mid ink p10-sub">La Bible, pas à pas, sans jargon.</p></div>')
SCENES.append(("p10", 55.7, 60, "parchemin", p10))
appear("#p10 .kicker", 55.95, 16)
TWEENS.append('tl.fromTo("#p10 .rule", { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power2.inOut", stagger: 0.15 }, 56.0);')
appear("#p10 .title", 56.2, 24, 0.7)
appear("#p10 .p10-sub", 56.9, 20, 0.6)

# ---------- Assemble ----------
FADE = 0.3
scene_html = []
for i, (sid, start, end, decor, inner) in enumerate(SCENES):
    s = max(0, start - (FADE / 2 if i else 0))
    e = min(60, end + (FADE / 2 if i < len(SCENES) - 1 else 0))
    dur = round(e - s, 3)
    scene_html.append(
        f'<div class="clip scene" id="{sid}" data-start="{s:.3f}" data-duration="{dur}">'
        f'<div class="sc-in"><div class="bgset"><img class="bgimg" src="assets/decors/{decor}.jpg" />'
        f'<img class="paper" src="assets/decors/parchemin.jpg" /><div class="vignette"></div></div>'
        f'{inner}</div></div>')
    TWEENS.insert(0, f'tl.fromTo("#{sid} .bgimg", {{ scale: 1.04 }}, {{ scale: 1.12, duration: {dur}, ease: "none" }}, {s:.3f});')
    if i:
        TWEENS.insert(0, f'tl.fromTo("#{sid} .sc-in", {{ opacity: 0 }}, {{ opacity: 1, duration: {FADE}, ease: "none" }}, {s:.3f});')

AUDIO = [
    ("voix", "assets/voix.wav", 0, 60, 1),
    ("sfx-whoosh-1", ".media/audio/sfx/sfx_004.mp3", 2.95, 2, 0.18),
    ("sfx-mer-1", ".media/audio/sfx/sfx_002.mp3", 3.2, 9.3, 0.09),
    ("sfx-impact-1", ".media/audio/sfx/sfx_001.mp3", 6.5, 2, 1),
    ("sfx-whoosh-2", ".media/audio/sfx/sfx_004.mp3", 12.3, 2, 0.15),
    ("sfx-impact-2", ".media/audio/sfx/sfx_001.mp3", 21.2, 2, 1),
    ("sfx-stamp", ".media/audio/sfx/sfx_001.mp3", 32.15, 2, 0.45),
    ("sfx-whoosh-3", ".media/audio/sfx/sfx_004.mp3", 35.7, 2, 0.15),
    ("sfx-mer-2", ".media/audio/sfx/sfx_002.mp3", 51.8, 3.9, 0.08),
    ("sfx-whoosh-4", ".media/audio/sfx/sfx_004.mp3", 55.5, 2, 0.15),
]
audio_html = "\n      ".join(
    f'<audio id="{a}" src="{src}" data-start="{st}" data-duration="{d}" data-volume="{v}"></audio>'
    for a, src, st, d, v in AUDIO)

motes = "".join(
    f'<i class="mote" style="left:{(i * 137) % 1000 + 40}px;top:{(i * 263) % 1700 + 100}px;'
    f'width:{3 + (i * 7) % 5}px;height:{3 + (i * 7) % 5}px;opacity:{0.2 + ((i * 11) % 5) * 0.07:.2f}"></i>'
    for i in range(18))
TWEENS.append('gsap.utils.toArray(".mote").forEach((m, i) => { tl.fromTo(m, { y: 0, x: 0 }, { y: -260 - (i % 4) * 60, x: ((i % 3) - 1) * 50, duration: 60, ease: "none" }, 0); });')

template = open("template.tpl").read()
out = (template.replace("{{SCENES}}", "\n      ".join(scene_html))
       .replace("{{AUDIO}}", audio_html)
       .replace("{{MOTES}}", motes)
       .replace("{{TWEENS}}", "\n      ".join(TWEENS)))
open("index.html", "w").write(out)
print("scenes:", len(SCENES), "tweens:", len(TWEENS))
