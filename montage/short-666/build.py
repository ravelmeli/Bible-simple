"""Short « Néron et 666 » — retention-style montage (60 s, 9:16).

Beats are timed on the word-level transcript (transcript.json). Run: python3 build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from common import Short  # noqa: E402

DUR = 60
sh = Short(HERE, DUR)
T = sh.t

# ===== q1 · HOOK 0 – 3.4 : the number, then the question =====
q1 = sh.scene("q1", 0, 3.4, "patmos", zoom=(1.0, 1.08), dark=0.62)
q1.kw("666", "left:0;width:1080px;top:380px;font-size:470px;letter-spacing:6px", 0.0, how="cut", hero=True, tick=False, cls="rust")
sh.tween("#e1", "scale: 1.5", 'scale: 1, duration: 0.35, ease: "power4.out"', 0.0)
q1.ring(540, 640, 390, 0.25, "#f6d77f", 0.8)
q1.kw("= un nom ?", "left:0;width:1080px;top:960px;font-size:130px", T("nom"), "pop", hero=True, tick=False, cls="cream")
sh.sfx("hit", 0.0, 0.8)
sh.flash(0.0, "gold", 0.5)
sh.sfx("riser", T("nom") - 1.4, 0.8)
sh.sfx("hit", T("nom"), 0.5)
sh.punch("q1", T("nom"), 1.05)

# ===== q2 · 3.4 – 7.28 : Patmos, the riddle =====
q2 = sh.scene("q2", 3.4, 7.28, "patmos", pan=(-30, 0))
q2.element("personnage-01-jean-patmos", 1200, "left:-30px;top:720px", 3.5, "rise")
q2.ref("Apocalypse 13.18", "left:60px;top:190px", 3.5)
q2.kw("Île de Patmos", "left:60px;top:300px;font-size:64px", T("patmos"), "pop", rot=-3, cls="small")
q2.raw('<div class="medallion" id="med" style="left:520px;top:430px"><div class="disc"></div>'
       '<svg viewBox="0 0 500 500"><circle cx="250" cy="250" r="238" transform="rotate(-90 250 250)" />'
       '<circle class="inner" cx="250" cy="250" r="214" transform="rotate(-90 250 250)" /></svg>'
       '<div class="medal-num" id="mednum">666</div></div>')
sh.tween("#med", "opacity: 0, scale: 0.6, rotation: -20", 'opacity: 1, scale: 1, rotation: 0, duration: 0.7, ease: "back.out(1.6)"', T("666") - 0.1)
sh.tween("#med circle", "strokeDashoffset: 1500", 'strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut", stagger: 0.12', T("666"))
sh.sfx("riser", T("666") - 1.5)
sh.sfx("hit", T("666"))
sh.flash(T("666"), "gold", 0.4)
sh.sfx("mer", 3.4, 0.1)

# ===== q3 · 7.28 – 11.84 : "calculate this number" =====
q3 = sh.scene("q3", 7.28, 11.84, "bureau", pan=(30, -10), dark=0.1)
q3.ref("Apocalypse 13.18", "left:60px;top:190px", 7.4)
q3.element("objet-04-boulier", 640, "left:200px;top:520px", 8.0, "rise", z=6)
q3.kw("L'intelligence", "left:90px;top:330px;font-size:84px", T("l'intelligence"), "pop", rot=-3, cls="small")
q3.kw("Calcule", "left:0;width:1080px;top:1040px;font-size:170px", T("calcule"), "pop", hero=True, tick=False)
sh.sfx("hit", T("calcule"), 0.45)
sh.punch("q3", T("calcule"), 1.04)
sh.sfx("whoosh", 7.15)

# ===== q4 · 11.84 – 14.95 : every Hebrew letter has a value =====
q4 = sh.scene("q4", 11.84, 14.95, "bureau", pan=(-25, 0), dark=0.1)
q4.element("personnage-03-scribe-hebreu", 960, "left:-10px;top:560px", 12.0, "rise")
tiles = ""
for k, (x, l, v) in enumerate([(380, "א", 1), (590, "ב", 2), (800, "ג", 3)]):
    tiles += f'<div class="tile" id="t4{k}" style="left:{x - 190}px"><span class="val">{v}</span><span class="heb">{l}</span></div>'
q4.raw(f'<div class="tiles" style="top:360px;left:190px">{tiles}</div>')
for k, at in enumerate([T("hébreu") + 0.1, T("hébreu") + 0.55, T("hébreu") + 1.0]):
    sh.tween(f"#t4{k}", "opacity: 0, y: 40, scale: 0.8", 'opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(2)"', at)
    sh.sfx("tick", at)
q4.kw("Une valeur", "left:420px;top:760px;font-size:80px", T("valeur"), "pop", rot=3, cls="gold")

# ===== q5 · 14.95 – 22.0 : Néron César adds up to 666 =====
q5 = sh.scene("q5", 14.95, 21.98, "parchemin")
q5.kw("Néron César", "left:60px;top:230px;font-size:76px", T("Néron"), "slamL", rot=-2, cls="small")
q5.raw('<p class="hebword" id="hw" style="top:360px">נרון קסר</p>')
sh.tween("#hw", "opacity: 0, scale: 0.8", 'opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.8)"', T("Kassar") - 0.3)
order = [("נ", 50), ("ר", 200), ("ו", 6), ("ן", 50), ("ק", 100), ("ס", 60), ("ר", 200)]  # reading order, right to left
xs = [1008 - 118 - 128 * i - (40 if i >= 4 else 0) for i in range(7)]  # visual x of each tile, right to left, gap between the two words
tiles, run, tot = "", "", 0
t0 = T("Kassar") + 0.5
for k, ((l, v), x) in enumerate(zip(order, xs)):
    tiles += f'<div class="tile small" id="t5{k}" style="left:{x}px"><span class="val">{v}</span><span class="heb">{l}</span></div>'
    tot += v
    run += f'<p class="running" id="r5{k}" style="top:960px">{tot}</p>'
q5.raw(f'<div class="tiles" style="top:640px;left:0">{tiles}</div>')
q5.raw(run)
step = (T("obtient") - t0 + 0.2) / 7
for k in range(7):
    at = t0 + k * step
    sh.tween(f"#t5{k}", "opacity: 0, y: 40, scale: 0.8", 'opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(2)"', at)
    sh.tween(f"#r5{k}", "opacity: 0, scale: 0.8", 'opacity: 1, scale: 1, duration: 0.15', at + 0.05)
    if k < 6:
        sh.tween(f"#r5{k}", "opacity: 1", 'opacity: 0, duration: 0.1', at + step)
    sh.sfx("tick", at)
sh.tween("#r56", "scale: 1", 'scale: 1.4, duration: 0.3, ease: "back.out(2.5)"', T("666", 1))
sh.sfx("riser", T("666", 1) - 1.4)
sh.sfx("hit", T("666", 1))
sh.flash(T("666", 1), "gold", 0.5)
sh.punch("q5", T("666", 1), 1.05)

# ===== q6 · 21.98 – 28.67 : Nero (54-68) and the persecutions =====
q6 = sh.scene("q6", 21.98, 28.67, "rome", pan=(30, 0))
q6.element("personnage-02-neron", 1150, "left:560px;top:430px", 22.2, "rise", fade_bottom=True)
q6.ref("Néron · empereur", "left:60px;top:190px", T("Néron", 2))
q6.kw("54 – 68", "left:60px;top:300px;font-size:120px", T("54"), "pop", rot=-3, cls="gold")
q6.kw("Persécutions", "left:40px;top:560px;font-size:96px", T("persécutions"), "pop", rot=2, cls="red")
q6.element("personnage-06-chretien-priere", 600, "left:30px;top:800px", T("chrétiens"), "rise", fade_bottom=True)
sh.sfx("whoosh", 21.8)
sh.sfx("hit", T("persécutions"), 0.45)
sh.flash(T("persécutions"), "red", 0.3)

# ===== q7 · 28.67 – 35.9 : specialists, hypothesis =====
q7 = sh.scene("q7", 28.67, 35.9, "salle", pan=(-25, 0), dark=0.08)
q7.element("personnage-04-erudit-grec", 1050, "left:10px;top:520px", 28.8, "rise", fade_bottom=True)
q7.element("objet-07-loupe", 460, "left:700px;top:620px", T("spécialistes"), "pop", z=8)
q7.kw("Les spécialistes", "left:90px;top:230px;font-size:80px", T("spécialistes"), "pop", rot=-3, cls="small")
q7.raw('<div class="stamp" id="st7" style="top:720px">Hypothèse</div>')
sh.tween("#st7", "opacity: 0, scale: 1.8, rotation: -16", 'opacity: 1, scale: 1, rotation: -8, duration: 0.3, ease: "power4.in"', T("hypothèse"))
sh.sfx("hit", T("hypothèse"), 0.8)
sh.flash(T("hypothèse"), "red", 0.35)
sh.punch("q7", T("hypothèse"), 1.06)
q7.kw("D'autres noms ?", "left:230px;top:960px;font-size:76px", T("noms") - 0.6, "pop", rot=2, cls="dark small")

# ===== q8 · 35.9 – 42.9 : why keep the idea? =====
q8 = sh.scene("q8", 35.9, 42.9, "bureau", pan=(25, 0), dark=0.1)
q8.kw("Pourquoi ?", "left:0;width:1080px;top:250px;font-size:210px", T("pourquoi"), "pop", hero=True, tick=False)
sh.sfx("hit", T("pourquoi"), 0.5)
sh.flash(T("pourquoi"), "gold", 0.4)
sh.punch("q8", T("pourquoi"), 1.05)
q8.element("personnage-06-chretien-priere", 800, "left:260px;top:660px", T("chrétiens", 1) - 0.4, "rise", fade_bottom=True)
q8.kw("Les premiers chrétiens", "left:90px;top:560px;font-size:66px", T("chrétiens", 1) - 0.2, "pop", rot=-3, cls="small")
q8.kw("Avec prudence", "left:300px;top:980px;font-size:84px", T("prudence"), "pop", rot=3, cls="gold")
sh.sfx("whoosh", 35.7)

# ===== q9 · 42.9 – 48.1 : power versus faithfulness =====
q9 = sh.scene("q9", 42.9, 48.1, "rome", pan=(0, -15), dark=0.25)
bal = q9.element("objet-05-balance", 560, "left:260px;top:620px", 43.1, "rise", z=8)
sh.tween(f"#{bal}", "rotation: 0", 'rotation: -8, duration: 0.5, ease: "power2.out"', T("pouvoir"))
sh.tween(f"#{bal}", "rotation: -8", 'rotation: 8, duration: 0.6, ease: "back.out(1.6)"', T("fidélité") - 0.1)
q9.kw("Pouvoir", "left:40px;top:300px;font-size:100px", T("pouvoir"), "drop", rot=-4, cls="dark", tick=False)
q9.kw("Fidélité", "left:560px;top:300px;font-size:100px", T("fidélité"), "drop", rot=4, cls="gold", tick=False)
sh.sfx("hit", T("pouvoir"), 0.4)
sh.sfx("hit", T("fidélité"), 0.6)
sh.flash(T("fidélité"), "gold", 0.4)
sh.punch("q9", T("fidélité"), 1.05)

# ===== q10 · 48.1 – 51.8 : wisdom, not a code =====
q10 = sh.scene("q10", 48.1, 51.8, "parchemin")
q10.element("objet-09-codex-ferme", 400, "left:130px;top:760px", 48.4, "rise", z=8)
q10.element("objet-11-lampe-huile", 260, "left:640px;top:830px", 48.7, "rise", z=8)
q10.kw("Sagesse", "left:0;width:1080px;top:300px;font-size:200px", T("sagesse"), "pop", hero=True, tick=False)
sh.sfx("hit", T("sagesse"), 0.5)
sh.flash(T("sagesse"), "gold", 0.4)
q10.kw("Un code", "left:340px;top:560px;font-size:100px", T("code") - 0.2, "pop", rot=-3, cls="dark")
q10.strike_line(330, 650, 760, 610, T("code") + 0.25, width=16)

# ===== q11 · 51.8 – 55.7 : back to Patmos, the comment question =====
q11 = sh.scene("q11", 51.8, 55.7, "patmos", pan=(30, 0))
q11.element("personnage-01-jean-patmos", 1200, "left:-30px;top:720px", 51.9, "rise")
q11.kw("Quel verset ?", "left:0;width:1080px;top:300px;font-size:150px", T("verset"), "pop", hero=True, tick=False)
sh.sfx("hit", T("verset"), 0.4)
j = sh.uid()
q11.raw(f'<div class="cta" id="{j}" style="top:1050px"><svg class="bubble" viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z" /></svg>Écris-le en commentaire</div>')
q11._anim(f"#{j}", T("commentaire") - 0.25, "slamL")
sh.tween(f"#{j} path", "strokeDashoffset: 420", 'strokeDashoffset: 0, duration: 0.7, ease: "power2.inOut"', T("commentaire"))
sh.sfx("mer", 51.8, 0.1)

# ===== q12 · 55.7 – 60 : end card, over Patmos so the short loops back to its hook =====
q12 = sh.scene("q12", 55.7, DUR, "patmos", dark=0.62)
q12.raw('<div class="head" id="end" style="top:430px"><span class="endkicker" id="ek" style="color:#f6d77f">Abonne-toi</span><span class="endrule" id="r1" style="background:#f6d77f"></span>'
        '<p class="title" id="et" style="color:#f4ead2">La Bible Simple</p><span class="endrule" id="r2" style="background:#f6d77f"></span></div>')
sh.tween("#ek", "opacity: 0, y: 20", 'opacity: 1, y: 0, duration: 0.5', 55.85)
sh.tween("#r1, #r2", "scaleX: 0", 'scaleX: 1, duration: 0.8, ease: "power2.inOut"', 55.9)
sh.tween("#et", "opacity: 0, y: 30, scale: 0.9", 'opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "back.out(1.8)"', 56.05)
k = sh.uid()
q12.raw(f'<div class="subpill" id="{k}" style="top:880px"><svg viewBox="0 0 24 24" fill="#f6d77f"><path d="M12 2a6 6 0 0 0-6 6v3.6L4.2 15a1 1 0 0 0 .9 1.5h13.8a1 1 0 0 0 .9-1.5L18 11.6V8a6 6 0 0 0-6-6zm0 20a3 3 0 0 0 3-3H9a3 3 0 0 0 3 3z"/></svg>S\'abonner</div>')
q12._anim(f"#{k}", 56.4, "pop")
sh.tween(f"#{k}", "scale: 1", 'scale: 1.07, duration: 0.45, yoyo: true, repeat: 4, ease: "sine.inOut"', 56.9)
sh.sfx("hit", 56.4, 0.3)

# ===== sound bed =====
sh.audio.insert(0, ("ambiance", "assets/audio/ambiance.wav", 0, DUR, 0.16))

sh.build(os.path.join(HERE, "..", "template-short.tpl"))
