"""Short « La marque de la bête et le sceau de Dieu » — retention-style montage (54 s, 9:16).

Beats are timed on the word-level transcript (transcript.json). Run: python3 build.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import Short  # noqa: E402

DUR = 54
sh = Short(os.path.dirname(os.path.abspath(__file__)), DUR, fixes={"seau": "sceau", "seau,": "sceau,"})
# Whisper hears « leur front » for the plural of Revelation 22:4.
for i in range(len(sh.words) - 1):
    if sh.words[i]["text"] == "leur" and sh.words[i + 1]["text"].startswith("front"):
        sh.words[i]["text"] = "leurs"
        sh.words[i + 1]["text"] = "fronts."

T = sh.t
FR = [w["start"] for w in sh.words if w["text"].lower().startswith("front")]  # every « front » in order
print("front at", [round(x, 2) for x in FR])


def portrait(sc, name, w, h, left, top, img_w, img_x, img_y, at, how="pop", border="#c8963e"):
    from PIL import Image
    w0, h0 = Image.open(os.path.join(sh.dir, "assets/elements", name + ".png")).size
    img_h = round(h0 * img_w / w0)
    i = sh.uid()
    sc.raw(f'<div class="portrait" id="{i}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:50%;z-index:6;border-color:{border}">'
           f'<img src="assets/elements/{name}.png" style="width:{img_w}px;height:{img_h}px;left:{img_x}px;top:{img_y}px" /></div>')
    sc._anim(f"#{i}", at, how)
    return i


# ===== p1 · HOOK 0 – 2.55 : two foreheads, split screen =====
p1 = sh.scene("p1", 0, 2.55, "parchemin", zoom=(1.0, 1.06), dark=0.25)
p1.raw('<div class="half" id="h1" style="left:0;width:540px;background:linear-gradient(160deg,#1a1410 0%,#34273a 100%);z-index:4">'
       '<img id="h1i" src="assets/elements/personnage-09-homme-marque-front.png" style="width:700px;height:1107px;left:-80px;top:360px" /></div>')
p1.raw('<div class="half" id="h2" style="left:540px;width:540px;background:radial-gradient(ellipse at 50% 40%,#f6d77f 0%,#c8963e 70%);z-index:4">'
       '<img id="h2i" src="assets/elements/personnage-08-femme-sceau-front.png" style="width:810px;height:1107px;left:-130px;top:360px" /></div>')
p1.raw('<div class="divider" id="dv"></div>')
sh.tween("#h1i", "scale: 1.18", 'scale: 1, duration: 0.55, ease: "power3.out"', 0.0)
sh.tween("#h2i", "scale: 1.18", 'scale: 1, duration: 0.55, ease: "power3.out"', 0.0)
sh.tween("#dv", "scaleY: 0", 'scaleY: 1, duration: 0.35, ease: "power2.out"', 0.05)
p1.kw("Deux marques", "left:0;width:1080px;top:160px;font-size:112px", 0.0, how="cut", hero=True, tick=False, cls="cream")
p1.kw("Le front", "left:0;width:1080px;top:900px;font-size:176px", FR[0], how="pop", hero=True, tick=False)
sh.sfx("hit", 0.0, 0.4)
sh.sfx("riser", max(FR[0] - 1.4, 0.2))
sh.sfx("hit", FR[0])
sh.flash(FR[0], "gold", 0.45)
sh.punch("p1", FR[0], 1.05)

# ===== p2 · 2.55 – 7.30 : the beast imposes its mark (Rev 13:16) =====
p2 = sh.scene("p2", 2.55, 7.30, "rome", pan=(-40, 0))
p2.element("personnage-09-homme-marque-front", 1010, "left:40px;top:410px", 2.6, "rise", fade_bottom=True)
p2.ref("Apocalypse 13.16", "left:60px;top:190px", 2.7)
iron = p2.element("objet-18-fer-a-marquer", 560, "left:700px;top:520px", T("marque", 0), "slamR", z=8)
sh.tween(f"#{iron}", "rotation: -30", 'rotation: -14, duration: 0.5, ease: "power3.out"', T("marque", 0))
p2.kw("Main droite", "left:560px;top:930px;font-size:70px", T("main"), "pop", rot=-4, cls="red small")
p2.ring(358, 640, 105, FR[1] - 0.2, "#8b2e1f")
p2.kw("Front", "left:600px;top:520px;font-size:70px", FR[1], "pop", rot=3, cls="small")
sh.sfx("whoosh", 2.4)
sh.sfx("hit", T("marque", 0), 0.35)

# ===== p3 · 7.30 – 10.09 : neither buy nor sell (Rev 13:17) =====
p3 = sh.scene("p3", 7.30, 10.09, "marche", pan=(40, 0))
p3.ref("Apocalypse 13.17", "left:60px;top:190px", 7.4)
p3.element("objet-16-panier-pain-figues", 520, "left:50px;top:660px", T("acheter"), "pop")
p3.element("objet-17-bourse", 500, "left:570px;top:690px", T("vendre"), "pop")
p3.ring(540, 880, 360, T("personne"), "#8b2e1f", 0.7)
p3.strike_line(300, 640, 780, 1120, T("acheter") + 0.1)
sh.sfx("hit", T("acheter") + 0.1, 0.45)
sh.flash(T("acheter") + 0.1, "red", 0.3)

# ===== p4 · 10.09 – 15.61 : six chapters earlier, the seal (Rev 7:3) =====
p4 = sh.scene("p4", 10.09, 15.61, "patmos", pan=(30, -10))
p4.raw('<div class="gold-glow" id="g4"></div>')
sh.tween("#g4", "opacity: 0", 'opacity: 1, duration: 1.0, ease: "power1.out"', T("sceau") - 0.3)
p4.element("personnage-07-ange-sceau", 1100, "left:-80px;top:520px", 10.2, "rise")
p4.element("personnage-12-groupe-fideles", 640, "left:560px;top:760px", 12.4, "rise", fade_bottom=True)
p4.ref("Apocalypse 7.3", "left:60px;top:190px", 10.3)
p4.ref("Six chapitres plus tôt", "left:60px;top:290px", 10.9, "slamL")
p4.kw("Le sceau", "left:0;width:1080px;top:420px;font-size:170px", T("sceau"), "pop", hero=True, tick=False)
p4.ring(560, 880, 70, T("sceau") + 0.15, "#f6d77f")
sh.sfx("riser", T("sceau") - 1.4)
sh.sfx("hit", T("sceau"))
sh.flash(T("sceau"), "gold", 0.5)
sh.punch("p4", T("sceau"), 1.04)
sh.sfx("mer", 10.1, 0.06)

# ===== p5 · 15.61 – 20.28 : the parallel, drawn =====
p5 = sh.scene("p5", 15.61, 20.28, "parchemin", dark=0.0)
p5.kw("Un parallèle voulu", "left:90px;top:180px;font-size:84px", 15.75, "drop", rot=-1.5, tick=False)
sh.sfx("hit", 15.95, 0.35)
portrait(p5, "personnage-09-homme-marque-front", 430, 430, 60, 400, 540, -55, -20, 16.1)
portrait(p5, "personnage-08-femme-sceau-front", 430, 430, 590, 400, 590, -80, -25, 16.4)
p5.kw("La marque<small>Apocalypse 13</small>", "left:50px;top:870px;width:450px;font-size:62px", 16.7, "pop", cls="small")
p5.kw("Le sceau<small>Apocalypse 7</small>", "left:580px;top:870px;width:450px;font-size:62px", 16.95, "pop", cls="small")
p5.raw('<svg class="strikeline" id="arc5" viewBox="0 0 1080 1920" style="z-index:8"><path d="M 275 380 C 400 230, 680 230, 805 380" fill="none" stroke="#8b2e1f" stroke-width="8" stroke-linecap="round" stroke-dasharray="900" /></svg>')
sh.tween("#arc5 path", "strokeDashoffset: 900", 'strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut"', 17.1)
p5.element("objet-01-rouleau-papyrus", 260, "left:410px;top:1010px", T("l'Ancien"), "pop", z=8)
p5.kw("Ancien Testament", "left:200px;top:1060px;font-size:66px", T("l'Ancien") + 0.1, "slamL", rot=-2, cls="dark small")

# ===== p6 · 20.28 – 29.30 : Deuteronomy 6:8, hand and forehead =====
p6 = sh.scene("p6", 20.28, 29.30, "bureau", pan=(-30, 10))
p6.element("personnage-10-israelite-tefillin", 1020, "left:-110px;top:400px", 20.4, "rise", fade_bottom=True)
p6.ref("Deutéronome 6.8", "left:60px;top:190px", 20.5)
fr3 = FR[3]
p6.ring(358, 560, 95, T("yeux") - 0.5, "#f6d77f")
p6.ring(180, 1090, 105, T("main", 2) - 0.1, "#f6d77f")
p6.kw("Actes<small>la main</small>", "left:560px;top:880px;font-size:84px", T("fait"), "pop", rot=3, cls="gold")
p6.kw("Pensées<small>le front</small>", "left:540px;top:520px;font-size:84px", T("pense"), "pop", rot=-3, cls="gold")
sh.sfx("whoosh", 20.2)
sh.sfx("hit", T("fait"), 0.3)
sh.sfx("hit", T("pense"), 0.3)

# ===== p7 · 29.30 – 36.51 : loyalty, not a chip or a tattoo =====
p7 = sh.scene("p7", 29.30, 36.51, "salle", pan=(25, 0), dark=0.12)
p7.kw("Loyauté", "left:0;width:1080px;top:250px;font-size:200px", T("loyauté"), "pop", hero=True, tick=False)
sh.sfx("hit", T("loyauté"))
sh.flash(T("loyauté"), "gold", 0.4)
sh.punch("p7", T("loyauté"), 1.04)
p7.kw("Une puce", "left:90px;top:640px;font-size:76px", T("puce"), "pop", rot=-4, cls="small")
p7.strike_line(110, 740, 440, 700, T("puce") + 0.4)
p7.kw("Un tatouage", "left:520px;top:780px;font-size:76px", T("tatouage"), "pop", rot=3, cls="small")
p7.strike_line(540, 880, 930, 840, T("tatouage") + 0.4)
p7.kw("Pensées", "left:90px;top:1010px;font-size:80px", T("pensées"), "pop", rot=-3, cls="gold")
p7.kw("Actes", "left:600px;top:1010px;font-size:80px", T("actes"), "pop", rot=3, cls="gold")

# ===== p8 · 36.51 – 38.80 : the mark comes under pressure =====
p8 = sh.scene("p8", 36.51, 38.80, "rome", pan=(0, 0), dark=0.2)
p8.element("personnage-11-officiel-romain-cachet", 1000, "left:300px;top:440px", 36.6, "rise", fade_bottom=True)
p8.kw("Pression", "left:0;width:1080px;top:230px;font-size:190px", T("pression"), "drop", hero=True, tick=False, cls="rust")
p8.image("objet-14-cachet-cire", 330, 325, "left:90px;top:760px", T("pression") + 0.05, "drop", z=9)
sh.sfx("hit", T("pression"), 0.8)
sh.flash(T("pression"), "red", 0.45)
sh.punch("p8", T("pression"), 1.06)

# ===== p9 · 38.80 – 42.44 : the seal protects the faithful =====
p9 = sh.scene("p9", 38.80, 42.44, "patmos", pan=(-30, 0))
p9.raw('<div class="gold-glow" id="g9"></div>')
sh.tween("#g9", "opacity: 0.3", 'opacity: 1, duration: 2.0, ease: "power1.out"', 38.8)
p9.element("personnage-07-ange-sceau", 1100, "left:-80px;top:520px", 38.9, "rise")
p9.element("personnage-12-groupe-fideles", 640, "left:560px;top:760px", 39.2, "rise", fade_bottom=True)
p9.kw("Fidèles", "left:0;width:1080px;top:300px;font-size:180px", T("fidèles"), "pop", hero=True, tick=False)
p9.ring(790, 1060, 270, T("fidèles") + 0.1, "#f6d77f")
sh.sfx("hit", T("fidèles"), 0.45)
sh.flash(T("fidèles"), "gold", 0.4)

# ===== p10 · 42.44 – 50.24 : the promise (Rev 22:4), then the comment question =====
p10 = sh.scene("p10", 42.44, 50.24, "promesse", pan=(0, -20))
p10.element("personnage-08-femme-sceau-front", 900, "left:210px;top:520px", 42.6, "rise", fade_bottom=True)
p10.ref("Apocalypse 22.4", "left:60px;top:190px", 42.7)
p10.kw("Son nom sera<br>sur leurs fronts", "left:130px;top:290px;font-size:84px", T("nom"), "pop", rot=-2, cls="gold")
p10.ring(540, 655, 120, T("nom") + 0.4, "#f6d77f")
sh.sfx("riser", T("nom") - 1.4)
sh.sfx("hit", T("nom"))
sh.flash(T("nom"), "gold", 0.5)
i = sh.uid()
p10.raw(f'<div class="cta" id="{i}" style="top:1050px"><svg class="bubble" viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z" /></svg>Dis-le en commentaire</div>')
p10._anim(f"#{i}", T("commentaire") - 0.2, "slamL")
sh.tween(f"#{i} path", "strokeDashoffset: 420", 'strokeDashoffset: 0, duration: 0.7, ease: "power2.inOut"', T("commentaire"))

# ===== p11 · 50.24 – 54 : end card =====
p11 = sh.scene("p11", 50.24, DUR, "parchemin")
p11.raw('<div class="head" id="end" style="top:430px"><span class="endkicker" id="ek">Abonne-toi</span><span class="endrule" id="r1"></span>'
        '<p class="title" id="et">La Bible Simple</p><span class="endrule" id="r2"></span></div>')
sh.tween("#ek", "opacity: 0, y: 20", 'opacity: 1, y: 0, duration: 0.5', 50.4)
sh.tween("#r1, #r2", "scaleX: 0", 'scaleX: 1, duration: 0.8, ease: "power2.inOut"', 50.45)
sh.tween("#et", "opacity: 0, y: 30, scale: 0.9", 'opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "back.out(1.8)"', 50.6)
sh.sfx("hit", 50.6, 0.3)
j = sh.uid()
p11.raw(f'<div class="subpill" id="{j}" style="top:880px"><svg viewBox="0 0 24 24" fill="#f6d77f"><path d="M12 2a6 6 0 0 0-6 6v3.6L4.2 15a1 1 0 0 0 .9 1.5h13.8a1 1 0 0 0 .9-1.5L18 11.6V8a6 6 0 0 0-6-6zm0 20a3 3 0 0 0 3-3H9a3 3 0 0 0 3 3z"/></svg>S\'abonner</div>')
p11._anim(f"#{j}", 51.1, "pop")
sh.tween(f"#{j}", "scale: 1", 'scale: 1.07, duration: 0.45, yoyo: true, repeat: 5, ease: "sine.inOut"', 51.6)
sh.sfx("hit", 51.1, 0.3)

# ===== sound bed =====
sh.audio.insert(0, ("ambiance", "assets/audio/ambiance.wav", 0, DUR, 0.16))

sh.build(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "template-short.tpl"),
         suppress=[(T("nom") - 0.1, T("fronts", end=True))])
