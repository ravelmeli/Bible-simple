"""Generate index.html for the 54-second 9:16 short « La marque de la bête et le sceau de Dieu ».

Scene and caption timings come from the word-level transcript (transcript.json, local Whisper large-v3).
Run: python3 build.py
"""
import json

DURATION = 54
SIZES = {
    "personnage-07-ange-sceau": (688, 1052),
    "personnage-08-femme-sceau-front": (644, 880),
    "personnage-09-homme-marque-front": (564, 892),
    "personnage-10-israelite-tefillin": (716, 832),
    "personnage-11-officiel-romain-cachet": (604, 860),
    "personnage-12-groupe-fideles": (628, 812),
    "objet-14-cachet-cire": (580, 572),
    "objet-16-panier-pain-figues": (724, 748),
    "objet-17-bourse": (588, 732),
    "objet-18-fer-a-marquer": (464, 764),
}
SCENES = []
TWEENS = []


def el(src, h, style, cls):
    w0, h0 = SIZES[src]
    w = round(w0 * h / h0)
    return f'<img class="el {cls}" src="assets/elements/{src}.png" style="width:{w}px;height:{h}px;{style}" />'


def card(inner, top, cls, left=70, width=940):
    return (f'<div class="card-wrap {cls}" style="top:{top}px;left:{left}px;width:{width}px">'
            f'<div class="card">{inner}</div></div>')


def appear(sel, at, y=30, dur=0.6, ease="power3.out", rot=None):
    frm = f"opacity: 0, y: {y}" + (f", rotation: {rot[0]}" if rot else "")
    to = f'opacity: 1, y: 0, duration: {dur}, ease: "{ease}"' + (f", rotation: {rot[1]}" if rot else "")
    TWEENS.append(f'tl.fromTo("{sel}", {{ {frm} }}, {{ {to} }}, {at});')


def fade_out(sel, at, dur=0.35):
    TWEENS.append(f'tl.to("{sel}", {{ opacity: 0, duration: {dur}, ease: "power1.in" }}, {at});')


def portrait(src, left, top, img_w, img_x, img_y, cls):
    w0, h0 = SIZES[src]
    img_h = round(h0 * img_w / w0)
    return (f'<div class="portrait {cls}" style="left:{left}px;top:{top}px">'
            f'<img src="assets/elements/{src}.png" style="width:{img_w}px;height:{img_h}px;left:{img_x}px;top:{img_y}px" /></div>')


# p1 · 0 – 2.55 · Hook: two foreheads side by side.
p1 = (card('<span class="kicker">Apocalypse</span><p class="big">Deux marques, un même endroit&nbsp;: <span class="accent">le front</span>.</p>', 170, "c1")
      + portrait("personnage-09-homme-marque-front", 70, 760, 560, -95, -40, "pm")
      + portrait("personnage-08-femme-sceau-front", 630, 760, 600, -110, -30, "pf"))
SCENES.append(("p1", 0, 2.55, "parchemin", p1))
appear("#p1 .c1 .card", 0.05, 40, 0.6, rot=(-3, -1.5))
TWEENS.append('tl.fromTo("#p1 .pm", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, 0.35);')
TWEENS.append('tl.fromTo("#p1 .pf", { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, 0.55);')

# p2 · 2.55 – 7.3 · The beast imposes its mark (Rev 13:16).
p2 = (card('<span class="kicker">Apocalypse 13.16</span><p class="mid">Une marque sur la <span class="accent">main droite</span> ou sur le <span class="accent">front</span>.</p>', 160, "c2")
      + el("personnage-09-homme-marque-front", 980, "left:-20px;bottom:120px", "p2-homme")
      + el("objet-18-fer-a-marquer", 560, "right:70px;bottom:520px", "p2-fer"))
SCENES.append(("p2", 2.55, 7.3, "rome", p2))
appear("#p2 .p2-homme", 2.6, 80, 0.9)
appear("#p2 .c2 .card", 2.75, 30, rot=(2, 1))
TWEENS.append('tl.fromTo("#p2 .p2-fer", { opacity: 0, rotation: -25, y: -40 }, { opacity: 1, rotation: -12, y: 0, duration: 0.7, ease: "back.out(1.6)" }, 4.6);')

# p3 · 7.3 – 10.09 · Neither buy nor sell.
p3 = (card('<p class="big">Sans elle, ni <span class="accent">acheter</span>, ni <span class="accent">vendre</span>.</p>', 170, "c3")
      + el("objet-16-panier-pain-figues", 470, "left:60px;bottom:330px", "p3-panier")
      + el("objet-17-bourse", 430, "right:90px;bottom:340px", "p3-bourse"))
SCENES.append(("p3", 7.3, 10.09, "marche", p3))
appear("#p3 .c3 .card", 7.45, 30, rot=(-2, -1))
appear("#p3 .p3-panier", 7.7, 40, 0.7)
appear("#p3 .p3-bourse", 8.0, 40, 0.7)

# p4 · 10.09 – 15.61 · Six chapters earlier: the seal (Rev 7:3).
p4 = (card('<span class="kicker">Apocalypse 7.3 · six chapitres plus tôt</span><p class="mid">Dieu marque ses serviteurs d\'un <span class="accent">sceau</span>, sur le front.</p>', 160, "c4")
      + '<div class="gold-glow g4"></div>'
      + el("personnage-07-ange-sceau", 1040, "left:-60px;bottom:-30px", "p4-ange")
      + el("personnage-12-groupe-fideles", 640, "right:10px;bottom:150px", "p4-groupe"))
SCENES.append(("p4", 10.09, 15.61, "patmos", p4))
appear("#p4 .p4-ange", 10.2, 80, 1.0)
appear("#p4 .c4 .card", 10.35, 30, rot=(2, 0.8))
TWEENS.append('tl.fromTo("#p4 .g4", { opacity: 0 }, { opacity: 1, duration: 1.2, ease: "power1.out" }, 11.5);')
appear("#p4 .p4-groupe", 12.6, 50, 0.9)

# p5 · 15.61 – 20.28 · The parallel, drawn as a diagram.
p5 = ('<div class="head" style="top:170px"><span class="kicker">Un parallèle voulu</span><p class="big ink">Le même endroit</p></div>'
      + portrait("personnage-09-homme-marque-front", 90, 520, 560, -95, -40, "d-m")
      + portrait("personnage-08-femme-sceau-front", 610, 520, 600, -110, -30, "d-f")
      + '<p class="plabel d-lm" style="left:60px;top:930px">Apocalypse 13<b>La marque</b></p>'
      + '<p class="plabel d-lf" style="left:580px;top:930px">Apocalypse 7<b>Le sceau</b></p>'
      + '<svg class="arrows d-arc" viewBox="0 0 1080 1920"><path d="M 290 520 C 380 400, 700 400, 800 520" /></svg>'
      + card('<p class="mid">Jean reprend une image de l\'<span class="accent">Ancien Testament</span>.</p>', 1110, "c5", left=110, width=860))
SCENES.append(("p5", 15.61, 20.28, "parchemin", p5))
appear("#p5 .head", 15.75, 24)
TWEENS.append('tl.fromTo("#p5 .d-m", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.8)" }, 16.0);')
TWEENS.append('tl.fromTo("#p5 .d-f", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.8)" }, 16.3);')
appear("#p5 .d-lm", 16.5, 16, 0.4)
appear("#p5 .d-lf", 16.7, 16, 0.4)
TWEENS.append('tl.fromTo("#p5 .d-arc path", { strokeDashoffset: 900 }, { strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut" }, 17.0);')
appear("#p5 .c5 .card", 18.15, 30, rot=(-2, -0.8))

# p6 · 20.28 – 29.3 · Deuteronomy 6:8 — hand and forehead.
p6 = (card('<span class="kicker">Deutéronome 6.8</span><p class="mid">Lier ses paroles sur la <span class="accent">main</span> et entre les <span class="accent">yeux</span>.</p>', 150, "c6")
      + el("personnage-10-israelite-tefillin", 900, "left:-60px;top:720px", "p6-isr")
      + '<p class="tag t-front" style="left:600px;top:700px">Le front&nbsp;: ce que l\'on pense</p>'
      + '<p class="tag t-main" style="left:560px;top:1140px">La main&nbsp;: ce que l\'on fait</p>'
      + '<svg class="arrows a-front" viewBox="0 0 1080 1920"><path d="M 600 760 C 520 760, 450 780, 390 800" /></svg>'
      + '<svg class="arrows a-main" viewBox="0 0 1080 1920"><path d="M 560 1200 C 400 1220, 260 1260, 170 1300" /></svg>')
SCENES.append(("p6", 20.28, 29.3, "bureau", p6))
appear("#p6 .p6-isr", 20.4, 80, 1.0)
appear("#p6 .c6 .card", 20.55, 30, rot=(-2, -1))
appear("#p6 .t-main", 25.5, 20, 0.5)
TWEENS.append('tl.fromTo("#p6 .a-main path", { strokeDashoffset: 900 }, { strokeDashoffset: 0, duration: 0.6, ease: "power2.out" }, 25.7);')
appear("#p6 .t-front", 27.3, 20, 0.5)
TWEENS.append('tl.fromTo("#p6 .a-front path", { strokeDashoffset: 900 }, { strokeDashoffset: 0, duration: 0.6, ease: "power2.out" }, 27.5);')

# p7 · 29.3 – 36.51 · A question of loyalty.
p7 = (card('<span class="kicker">Une question de</span><p class="big accent">loyauté</p>'
           '<p class="small">pas une <span class="strike">puce<i class="s1"></i></span>, pas un <span class="strike">tatouage<i class="s2"></i></span></p>', 200, "c7")
      + card('<p class="mid">À qui appartiennent mes <span class="accent">pensées</span> et mes <span class="accent">actes</span>&nbsp;?</p>', 800, "c7b"))
SCENES.append(("p7", 29.3, 36.51, "salle", p7))
appear("#p7 .c7 .card", 29.45, 30, rot=(-2, -1))
TWEENS.append('tl.fromTo("#p7 .s1", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power2.out" }, 31.6);')
TWEENS.append('tl.fromTo("#p7 .s2", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power2.out" }, 32.4);')
appear("#p7 .c7b .card", 33.25, 30, rot=(2, 0.8))

# p8 · 36.51 – 38.8 · The mark comes under pressure.
p8 = (card('<p class="mid">La marque s\'obtient sous la <span class="accent">pression</span>.</p>', 170, "c8")
      + el("personnage-11-officiel-romain-cachet", 950, "right:20px;bottom:200px", "p8-off"))
SCENES.append(("p8", 36.51, 38.8, "rome", p8))
appear("#p8 .p8-off", 36.6, 60, 0.6)
appear("#p8 .c8 .card", 36.7, 30, rot=(-2, -1))

# p9 · 38.8 – 42.44 · The seal protects the faithful.
p9 = (card('<p class="mid">Le sceau de Dieu protège ceux qui restent <span class="accent">fidèles</span>.</p>', 170, "c9")
      + '<div class="gold-glow g9"></div>'
      + el("personnage-07-ange-sceau", 1040, "left:-60px;bottom:-30px", "p9-ange")
      + el("personnage-12-groupe-fideles", 640, "right:10px;bottom:150px", "p9-groupe"))
SCENES.append(("p9", 38.8, 42.44, "patmos", p9))
TWEENS.append('tl.fromTo("#p9 .g9", { opacity: 0.4 }, { opacity: 1, duration: 2.5, ease: "power1.out" }, 38.8);')
appear("#p9 .c9 .card", 38.95, 30, rot=(2, 0.8))
appear("#p9 .p9-groupe", 39.3, 40, 0.8)

# p10 · 42.44 – 50.24 · The promise (Rev 22:4), then the comment question.
bubble = ('<svg class="bubble" viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 '
          'a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z" /></svg>')
p10 = (card('<span class="kicker">Apocalypse 22.4 · une promesse</span><p class="quote">« Son nom sera sur leurs fronts. »</p>', 170, "c10")
       + card('<p class="mid">Quelle image te vient en lisant ce passage&nbsp;?</p>'
              f'<span class="cta c10-cta">{bubble}Dis-le en commentaire</span>', 170, "c10b")
       + el("personnage-08-femme-sceau-front", 760, "left:262px;bottom:280px", "p10-femme"))
SCENES.append(("p10", 42.44, 50.24, "promesse", p10))
appear("#p10 .p10-femme", 42.6, 60, 1.0)
appear("#p10 .c10 .card", 42.7, 30, rot=(-2, -1))
fade_out("#p10 .c10 .card", 46.0)
appear("#p10 .c10b .card", 46.35, 30, rot=(2, 0.8))
appear("#p10 .c10-cta", 49.55, 16, 0.45)
TWEENS.append('tl.fromTo("#p10 .bubble path", { strokeDashoffset: 420 }, { strokeDashoffset: 0, duration: 0.7, ease: "power2.inOut" }, 49.55);')

# p11 · 50.24 – 54 · End card.
p11 = ('<div class="head end" style="top:560px"><span class="kicker">Abonne-toi</span><span class="rule"></span>'
       '<p class="title ink">La Bible Simple</p><span class="rule"></span>'
       '<p class="mid ink p11-sub">Comprendre l\'Apocalypse, un symbole à la fois.</p></div>')
SCENES.append(("p11", 50.24, DURATION, "parchemin", p11))
appear("#p11 .kicker", 50.4, 16)
TWEENS.append('tl.fromTo("#p11 .rule", { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power2.inOut", stagger: 0.15 }, 50.45);')
appear("#p11 .title", 50.6, 24, 0.7)
appear("#p11 .p11-sub", 52.2, 20, 0.6)

# ---------- Captions from word timings ----------
words = json.load(open("transcript.json"))
FIX = {"seau": "sceau", "seau,": "sceau,"}
for i, w in enumerate(words):
    w["text"] = FIX.get(w["text"], w["text"])
# Whisper hears « leur front » for the plural « leurs fronts » (Rev 22:4).
for i in range(len(words) - 1):
    if words[i]["text"] == "leur" and words[i + 1]["text"].startswith("front"):
        words[i]["text"] = "leurs"
        words[i + 1]["text"] = "fronts."
for w in words:
    if w["text"].endswith("?") and not w["text"].endswith(" ?"):
        w["text"] = w["text"][:-1] + " ?"

chunks, cur = [], []
for w in words:
    cur.append(w)
    if w["text"].rstrip().endswith((".", "?", "!", ",", ":")) or len(cur) == 4:
        chunks.append(cur)
        cur = []
if cur:
    chunks.append(cur)

caps = []
for n, ch in enumerate(chunks):
    start = ch[0]["start"]
    nxt = chunks[n + 1][0]["start"] if n + 1 < len(chunks) else DURATION
    end = min(max(ch[-1]["end"] + 0.25, start + 0.6), nxt)
    if start >= 50.2:
        # The end card carries the last line; no caption over it.
        continue
    spans = " ".join(f'<span class="cw cw{n}-{k}">{w["text"]}</span>' for k, w in enumerate(ch))
    caps.append(f'<p class="clip cap" id="cap{n}" data-start="{start:.3f}" data-duration="{end - start:.3f}">{spans}</p>')
    for k, w in enumerate(ch):
        TWEENS.append(f'tl.fromTo(".cw{n}-{k}", {{ color: "#1a1410" }}, {{ color: "#8b2e1f", duration: 0.08 }}, {w["start"]:.3f});')
        TWEENS.append(f'tl.to(".cw{n}-{k}", {{ color: "#1a1410", duration: 0.12 }}, {max(w["end"], w["start"] + 0.15):.3f});')

# ---------- Assemble ----------
FADE = 0.3
scene_html = []
bg_tweens = []
for i, (sid, start, end, decor, inner) in enumerate(SCENES):
    s = max(0, start - (FADE / 2 if i else 0))
    e = min(DURATION, end + (FADE / 2 if i < len(SCENES) - 1 else 0))
    dur = round(e - s, 3)
    scene_html.append(
        f'<div class="clip scene" id="{sid}" data-start="{s:.3f}" data-duration="{dur}">'
        f'<div class="sc-in"><div class="bgset"><img class="bgimg" src="assets/decors/{decor}.jpg" />'
        f'<img class="paper" src="assets/decors/parchemin.jpg" /><div class="vignette"></div></div>'
        f'{inner}</div></div>')
    bg_tweens.append(f'tl.fromTo("#{sid} .bgimg", {{ scale: 1.04 }}, {{ scale: 1.12, duration: {dur}, ease: "none" }}, {s:.3f});')
    if i:
        bg_tweens.append(f'tl.fromTo("#{sid} .sc-in", {{ opacity: 0 }}, {{ opacity: 1, duration: {FADE}, ease: "none" }}, {s:.3f});')

AUDIO = [
    ("voix", "assets/voix.wav", 0, DURATION, 1),
    ("sfx-impact-1", ".media/audio/sfx/sfx_001.mp3", 0.1, 2, 0.5),
    ("sfx-whoosh-1", ".media/audio/sfx/sfx_004.mp3", 2.4, 2, 0.15),
    ("sfx-mer-1", ".media/audio/sfx/sfx_002.mp3", 10.1, 5.5, 0.08),
    ("sfx-impact-2", ".media/audio/sfx/sfx_001.mp3", 36.6, 2, 0.8),
    ("sfx-mer-2", ".media/audio/sfx/sfx_002.mp3", 38.8, 3.6, 0.08),
    ("sfx-whoosh-2", ".media/audio/sfx/sfx_004.mp3", 50.05, 2, 0.15),
]
audio_html = "\n      ".join(
    f'<audio id="{a}" src="{src}" data-start="{st}" data-duration="{d}" data-volume="{v}"></audio>'
    for a, src, st, d, v in AUDIO)

motes = "".join(
    f'<i class="mote" style="left:{(i * 137) % 1000 + 40}px;top:{(i * 263) % 1700 + 100}px;'
    f'width:{3 + (i * 7) % 5}px;height:{3 + (i * 7) % 5}px;opacity:{0.2 + ((i * 11) % 5) * 0.07:.2f}"></i>'
    for i in range(18))
mote_tween = (f'gsap.utils.toArray(".mote").forEach((m, i) => {{ tl.fromTo(m, {{ y: 0, x: 0 }}, '
              f'{{ y: -240 - (i % 4) * 60, x: ((i % 3) - 1) * 50, duration: {DURATION}, ease: "none" }}, 0); }});')

template = open("template.tpl").read()
out = (template.replace("{{SCENES}}", "\n      ".join(scene_html))
       .replace("{{CAPTIONS}}", "\n      ".join(caps))
       .replace("{{AUDIO}}", audio_html)
       .replace("{{MOTES}}", motes)
       .replace("{{TWEENS}}", "\n      ".join(bg_tweens + TWEENS + [mote_tween])))
open("index.html", "w").write(out)
print("scenes:", len(SCENES), "captions:", len(caps), "tweens:", len(bg_tweens) + len(TWEENS) + 1)
