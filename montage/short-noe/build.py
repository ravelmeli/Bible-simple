"""Short « Cet homme a construit une arche… et personne ne l'a écouté » — retention-style montage (52.6 s, 9:16).

Beats are timed on the word-level transcript (transcript.json). Run: python3 build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from common import Short  # noqa: E402

DUR = 52.6
MUSIC_VOL = 0.15  # about 15 dB under the voice once the track is normalised to -16 LUFS
sh = Short(HERE, DUR, lib_sfx=True)
T = sh.t

# Whisper fixes, applied on the exact occurrence (the script says « qu'ils … doutaient » and « huit »).
for w in sh.words:
    if abs(w["start"] - 29.92) < 0.05 and w["text"] == "qu'il":
        w["text"] = "qu'ils"
    if w["text"] == "doutait":
        w["text"] = "doutaient"
    if w["text"] == "8":
        w["text"] = "huit"

# ===== n1 · HOOK 0 – 3.3 : the ark on the hill, Noah alone =====
n1 = sh.scene("n1", 0, 3.3, "arche", zoom=(1.0, 1.1), pan=(-30, 0), dark=0.28)
n1.element("personnage-13-noe-pied-marteau", 760, "left:20px;top:880px", 0.05, "rise", fade_bottom=True)
n1.kw("ARCHE", "left:0;width:1080px;top:190px;font-size:200px", T("construit"), "cut", hero=True, tick=False)
sh.sfx("hit", 0.2, 0.9)
sh.flash(T("construit"), "gold", 0.45)
n1.kw("PERSONNE", "left:0;width:1080px;top:430px;font-size:140px", T("personne"), "drop", hero=True, tick=False, cls="rust")
sh.sfx("hit", T("personne"), 0.6)
sh.flash(T("personne"), "red", 0.35)
sh.punch("n1", T("personne"), 1.05)

# ===== n2 · 3.3 – 8.5 : Noah, a righteous man who walked with God (Gen 6:9) =====
n2 = sh.scene("n2", 3.3, 8.5, "arche", zoom=(1.08, 1.18), pan=(40, -10), dark=0.4)
n2.element("personnage-14-noe-portrait", 1050, "left:20px;top:470px", 3.4, "rise", fade_bottom=True)
n2.ref("Genèse 6.9", "left:60px;top:190px", 3.5)
n2.kw("NOÉ", "left:0;width:1080px;top:270px;font-size:240px", T("noé"), "pop", hero=True, tick=False)
sh.sfx("hit", T("noé"), 0.7)
sh.flash(T("noé"), "gold", 0.4)
n2.kw("Homme juste", "left:560px;top:760px;font-size:76px", T("juste"), "pop", rot=3, cls="gold")
n2.ring(540, 770, 150, T("juste") + 0.1, "#f6d77f", 0.8)
n2.kw("Il marchait avec Dieu", "left:90px;top:1010px;font-size:70px", T("marchait"), "pop", rot=-2, cls="small")
sh.sfx("riser", T("juste") - 1.4, 0.13)

# ===== n3 · 8.5 – 10.98 : the earth is full of violence (Gen 6:11) =====
n3 = sh.scene("n3", 8.5, 10.98, "violence", zoom=(1.0, 1.1), pan=(-35, 0), dark=0.1)
n3.ref("Genèse 6.11", "left:60px;top:190px", 8.6)
n3.element("personnage-18-guerrier", 1000, "left:540px;top:520px", T("autour") if False else 8.7, "slamR", fade_bottom=True)
n3.kw("VIOLENCE", "left:0;width:1080px;top:290px;font-size:190px", T("violence"), "drop", hero=True, tick=False, cls="cream")
sh.sfx("hit", T("violence"), 0.9)
sh.flash(T("violence"), "red", 0.45)
sh.punch("n3", T("violence"), 1.06)

# ===== n4 · 10.98 – 14.09 : « Construis une arche » =====
n4 = sh.scene("n4", 10.98, 14.09, "arche", zoom=(1.12, 1.0), pan=(0, 0), dark=0.1)
n4.element("personnage-15-noe-mains-levees", 1050, "left:240px;top:480px", 11.1, "rise", fade_bottom=True)
n4.ref("Genèse 6.14", "left:60px;top:190px", 11.1)
n4.kw("CONSTRUIS", "left:0;width:1080px;top:300px;font-size:180px", T("construis"), "pop", hero=True, tick=False)
sh.sfx("hit", T("construis"), 0.8)
sh.flash(T("construis"), "gold", 0.45)
sh.sfx("riser", T("construis") - 1.1, 0.15)

# ===== n5 · 14.09 – 16.46 : 300 cubits, 130 m =====
n5 = sh.scene("n5", 14.09, 16.46, "arche", zoom=(1.0, 1.12), pan=(30, 0), dark=0.22)
n5.kw("300 coudées", "left:0;width:1080px;top:300px;font-size:130px", T("300"), "pop", hero=True, tick=False, cls="cream")
n5.kw("130 m +", "left:0;width:1080px;top:540px;font-size:230px", T("130"), "pop", hero=True, tick=False)
sh.sfx("hit", T("130"), 0.9)
sh.flash(T("130"), "gold", 0.5)
n5.element("objet-22-planches", 560, "left:60px;top:1020px", T("300"), "pop", z=8)
n5.element("objet-24-regle", 560, "left:780px;top:960px", T("130"), "pop", z=8)

# ===== n6 · 16.46 – 19.54 : the flood nobody had ever seen =====
n6 = sh.scene("n6", 16.46, 19.54, "violence", zoom=(1.0, 1.1), pan=(40, 0), dark=0.45)
n6.element("personnage-13-noe-pied-marteau", 900, "left:30px;top:620px", 16.6, "rise", fade_bottom=True)
n6.kw("DÉLUGE ?", "left:0;width:1080px;top:280px;font-size:190px", T("déluge"), "pop", hero=True, tick=False, cls="cream")
sh.sfx("hit", T("déluge"), 0.7)
n6.kw("Jamais vu", "left:520px;top:780px;font-size:90px", T("jamais"), "pop", rot=3, cls="dark")
sh.flash(T("jamais"), "white", 0.25)

# ===== n7 · 19.54 – 22.18 : Noah does all that God commanded (Gen 6:22) =====
n7 = sh.scene("n7", 19.54, 22.18, "arche", zoom=(1.05, 1.15), pan=(-40, 0), dark=0.15)
n7.ref("Genèse 6.22", "left:60px;top:190px", 19.62)
n7.element("objet-29-main-maillet", 900, "left:200px;top:480px", T("fait"), "slamL", z=8)
n7.kw("Il fait tout", "left:0;width:1080px;top:290px;font-size:140px", T("fait"), "pop", hero=True, tick=False, cls="cream")
n7.ring(520, 600, 170, T("ordonné") - 0.3, "#f6d77f", 0.7)
sh.punch("n7", T("ordonné"), 1.05)

# ===== n8 · 22.18 – 25.47 : « prédicateur de la justice » (2 Pierre 2:5) =====
n8 = sh.scene("n8", 22.18, 25.47, "arche", zoom=(1.18, 1.05), pan=(-30, 20), dark=0.4)
n8.element("personnage-14-noe-portrait", 1050, "left:20px;top:470px", 22.3, "rise", fade_bottom=True)
n8.ref("2 Pierre 2.5", "left:60px;top:190px", 22.3)
n8.kw("Prédicateur", "left:200px;top:330px;font-size:120px", T("prédicateur"), "pop", rot=-3, cls="gold")
n8.kw("de la justice", "left:260px;top:560px;font-size:100px", T("justice") - 0.9, "pop", rot=3, cls="small")
sh.flash(T("prédicateur"), "gold", 0.35)

# ===== n9 · 25.47 – 29.49 : eating, drinking, marrying =====
n9 = sh.scene("n9", 25.47, 29.49, "banquet", zoom=(1.0, 1.12), pan=(35, 0))
n9.element("personnage-16-couple-banquet", 820, "left:420px;top:430px", 25.6, "rise", fade_bottom=True)
n9.kw("Ils mangent", "left:40px;top:300px;font-size:80px", T("mangent"), "pop", rot=-4, cls="gold")
n9.element("objet-26-pain", 240, "left:50px;top:560px", T("mangent"), "pop", z=9)
n9.kw("Ils boivent", "left:560px;top:380px;font-size:80px", T("boivent"), "pop", rot=3, cls="gold")
n9.element("objet-25-gobelet", 300, "left:60px;top:830px", T("boivent"), "pop", z=9)
n9.kw("Ils se marient", "left:300px;top:930px;font-size:86px", T("marient"), "pop", rot=-2, cls="gold")
n9.element("objet-28-couronne-fleurs", 260, "left:20px;top:1010px", T("marient"), "pop", z=9)

# ===== n10 · 29.49 – 32.76 : « they suspected nothing » (Matt 24:37-39) =====
n10 = sh.scene("n10", 29.49, 32.76, "banquet", zoom=(1.12, 1.2), pan=(-30, 0), dark=0.08)
n10.ref("Matthieu 24.37-39", "left:60px;top:190px", 29.6)
doubt = n10.kw("Ils ne se doutaient<br>de rien", "left:120px;top:330px;font-size:84px", T("doutaient"), "pop", rot=-2, cls="small")
n10.element("personnage-16-couple-banquet", 820, "left:330px;top:560px", 29.6, "rise", fade_bottom=True)
sh.tween("#n10 .veil", "opacity: 0", 'opacity: 0.55, duration: 0.7, ease: "power2.in"', 31.6)
n10.kw("DÉLUGE", "left:0;width:1080px;top:290px;font-size:200px", T("déluge", 1), "drop", hero=True, tick=False, cls="rust")
sh.sfx("hit", T("déluge", 1), 0.9)
sh.flash(T("déluge", 1), "red", 0.45)
sh.punch("n10", T("déluge", 1), 1.06)
# The first card fades out when the flood word lands.
sh.tween(f"#{doubt}", "opacity: 1", 'opacity: 0, duration: 0.2', T("déluge", 1) - 0.12)

# ===== n11 · 32.76 – 36.74 : how many years? =====
n11 = sh.scene("n11", 32.76, 36.74, "arche", zoom=(1.0, 1.1), pan=(25, -10), dark=0.5)
n11.kw("COMBIEN<br>D'ANNÉES ?", "left:0;width:1080px;top:250px;font-size:150px", T("combien"), "pop", hero=True, tick=False, cls="cream")
sh.flash(T("combien"), "gold", 0.3)
n11.element("personnage-14-noe-portrait", 900, "left:90px;top:760px", T("combien") + 0.2, "rise", fade_bottom=True)
n11.kw("La Bible ne le précise pas", "left:100px;top:1010px;font-size:68px", T("précise") - 0.6, "pop", rot=-2, cls="dark small")

# ===== n12 · 36.74 – 39.88 : eight people enter (Gen 7:13) =====
n12 = sh.scene("n12", 36.74, 39.88, "porte", zoom=(1.0, 1.1), pan=(-30, 0), dark=0.05)
n12.ref("Genèse 7.13", "left:60px;top:190px", 36.85)
n12.kw("8", "left:0;width:1080px;top:230px;font-size:460px", T("huit") if False else 37.42, "pop", hero=True, tick=False)
sh.sfx("hit", 37.42, 1.0)
sh.flash(37.42, "gold", 0.5)
sh.punch("n12", 37.42, 1.06)
n12.kw("Seulement", "left:250px;top:840px;font-size:100px", T("seulement"), "pop", rot=-3, cls="dark")
n12.ring(430, 960, 190, T("entrent"), "#f6d77f", 0.8)

# ===== n13 · 39.88 – 44.28 : faith (Heb 11:7) =====
n13 = sh.scene("n13", 39.88, 44.28, "porte", zoom=(1.1, 1.2), pan=(30, 0), dark=0.3)
n13.ref("Hébreux 11.7", "left:60px;top:190px", 39.95)
n13.element("personnage-15-noe-mains-levees", 1050, "left:240px;top:480px", 40.1, "rise", fade_bottom=True)
n13.kw("FOI", "left:0;width:1080px;top:290px;font-size:260px", T("foi"), "pop", hero=True, tick=False)
sh.sfx("hit", T("foi"), 0.8)
sh.flash(T("foi"), "gold", 0.45)
sh.sfx("riser", T("foi") - 1.4, 0.13)
n13.kw("Ce qu'il ne voyait pas", "left:90px;top:1010px;font-size:70px", T("voyait") - 0.8, "pop", rot=-2, cls="gold")

# ===== n14 · 44.28 – 49.86 : the question, then the comment call =====
n14 = sh.scene("n14", 44.28, 49.86, "arche", zoom=(1.2, 1.0), pan=(0, 0), dark=0.2)
n14.element("personnage-13-noe-pied-marteau", 900, "left:30px;top:700px", 44.4, "rise", fade_bottom=True)
n14.kw("ET TOI ?", "left:0;width:1080px;top:290px;font-size:230px", T("toi"), "pop", hero=True, tick=False)
sh.sfx("hit", T("toi"), 0.8)
sh.flash(T("toi"), "gold", 0.4)
n14.kw("Que personne<br>ne voyait", "left:480px;top:760px;font-size:76px", T("voyait", 1) - 1.0, "pop", rot=3, cls="gold")
j = sh.uid()
n14.raw(f'<div class="cta" id="{j}" style="top:1010px"><svg class="bubble" viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z" /></svg>À toi de répondre</div>')
n14._anim(f"#{j}", 48.59 - 0.15, "slamL")
sh.tween(f"#{j} path", "strokeDashoffset: 420", 'strokeDashoffset: 0, duration: 0.7, ease: "power2.inOut"', 48.59)

# ===== n15 · 49.86 – 52.6 : end card =====
n15 = sh.scene("n15", 49.86, DUR, "parchemin")
n15.raw('<div class="head" id="end" style="top:430px"><span class="endkicker" id="ek">Abonne-toi</span><span class="endrule" id="r1"></span>'
        '<p class="title" id="et">La Bible Simple</p><span class="endrule" id="r2"></span></div>')
sh.tween("#ek", "opacity: 0, y: 20", 'opacity: 1, y: 0, duration: 0.5', 50.0)
sh.tween("#r1, #r2", "scaleX: 0", 'scaleX: 1, duration: 0.8, ease: "power2.inOut"', 50.05)
sh.tween("#et", "opacity: 0, y: 30, scale: 0.9", 'opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "back.out(1.8)"', 50.2)
k = sh.uid()
n15.raw(f'<div class="subpill" id="{k}" style="top:880px"><svg viewBox="0 0 24 24" fill="#f6d77f"><path d="M12 2a6 6 0 0 0-6 6v3.6L4.2 15a1 1 0 0 0 .9 1.5h13.8a1 1 0 0 0 .9-1.5L18 11.6V8a6 6 0 0 0-6-6zm0 20a3 3 0 0 0 3-3H9a3 3 0 0 0 3 3z"/></svg>S\'abonner</div>')
n15._anim(f"#{k}", 50.7, "pop")
sh.tween(f"#{k}", "scale: 1", 'scale: 1.07, duration: 0.45, yoyo: true, repeat: 3, ease: "sine.inOut"', 51.2)

# ===== scene-change swishes (only the main ones) =====
for t in (3.3, 10.98, 22.18, 25.47, 36.74):
    sh.sfx("whoosh", t - 0.12)

# ===== sound bed =====
if os.path.exists(os.path.join(HERE, "assets/audio/music.wav")):
    sh.audio.insert(0, ("music", "assets/audio/music.wav", 0, DUR, MUSIC_VOL))
sh.audio.insert(1, ("sfx-mer-bed", ".media/audio/sfx/sfx_002.mp3", 3.3, 9.4, 0.04))

sh.build(os.path.join(HERE, "..", "template-short.tpl"))
