"""Short « Cette reine a risqué sa vie pour sauver tout un peuple » (Esther) — retention-style montage (62.4 s, 9:16).

Beats are timed on the word-level transcript (transcript.json). Run: python3 build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from common import Short  # noqa: E402

DUR = 62.4
MUSIC_VOL = 0.15
sh = Short(HERE, DUR, lib_sfx=True)
T = sh.t

# ===== e1 · HOOK 0 – 5.74 : the golden door nobody may open =====
e1 = sh.scene("s1", 0, 5.74, "couloir", zoom=(1.0, 1.12), pan=(0, -20), dark=0.12)
e1.element("personnage-19-esther-pied", 760, "left:300px;top:760px", 0.1, "rise", fade_bottom=True)
e1.kw("SANS INVITATION", "left:0;width:1080px;top:230px;font-size:128px", T("sans"), "pop", hero=True, tick=False, cls="cream")
e1.kw("MORT", "left:0;width:1080px;top:470px;font-size:260px", T("mort"), "drop", hero=True, tick=False, cls="rust")
sh.sfx("hit", T("sans"), 0.6)
sh.sfx("hit", T("mort"), 1.0)
sh.flash(T("mort"), "red", 0.45)
sh.punch("s1", T("mort"), 1.06)
sh.sfx("riser", T("mort") - 1.4, 0.8)

# ===== e2 · 5.74 – 10.82 : Esther, queen of Persia, secretly Jewish (Est 2:10) =====
e2 = sh.scene("s2", 5.74, 10.82, "trone", zoom=(1.0, 1.1), pan=(-30, 0), dark=0.25)
e2.element("personnage-20-esther-portrait", 760, "left:160px;top:560px", 5.85, "rise", fade_bottom=True)
e2.ref("Esther 2.10", "left:60px;top:190px", 5.9)
e2.kw("ESTHER", "left:0;width:1080px;top:270px;font-size:210px", T("esther"), "pop", hero=True, tick=False)
e2.kw("Reine de Perse", "left:60px;top:1010px;font-size:70px", T("perse"), "pop", rot=-3, cls="small")
e2.kw("Juive ?", "left:600px;top:1000px;font-size:110px", T("juive"), "drop", rot=3, cls="gold", tick=False)
sh.flash(T("juive"), "gold", 0.35)
sh.sfx("whoosh", 5.6)

# ===== e3 · 10.82 – 17.98 : Haman's decree (Est 3:13) =====
e3 = sh.scene("s3", 10.82, 17.98, "trone", zoom=(1.12, 1.02), pan=(30, 0), dark=0.5)
e3.element("personnage-23-haman", 1000, "left:560px;top:520px", T("haman"), "slamR", fade_bottom=True)
e3.ref("Esther 3.13", "left:60px;top:190px", 10.95)
e3.element("objet-33-decret-scelle", 440, "left:40px;top:760px", T("décret"), "pop", z=9)
e3.kw("DÉCRET", "left:0;width:1080px;top:270px;font-size:210px", T("décret"), "drop", hero=True, tick=False, cls="rust")
sh.sfx("hit", T("décret"), 0.9)
sh.flash(T("décret"), "red", 0.4)
sh.punch("s3", T("décret"), 1.05)
e3.kw("1 seul jour", "left:60px;top:1050px;font-size:96px", T("jour"), "pop", rot=-3, cls="dark")
sh.sfx("whoosh", 10.7)

# ===== e4 · 17.98 – 22.98 : only the golden scepter can save her (Est 4:11) =====
e4 = sh.scene("s4", 17.98, 22.98, "couloir", zoom=(1.0, 1.1), pan=(25, -10), dark=0.15)
e4.element("personnage-19-esther-pied", 900, "left:80px;top:700px", 18.1, "rise", fade_bottom=True)
e4.ref("Esther 4.11", "left:60px;top:190px", 18.1)
e4.kw("ELLE HÉSITE", "left:0;width:1080px;top:280px;font-size:140px", T("hésite"), "pop", hero=True, tick=False, cls="cream")
e4.element("objet-31-sceptre", 480, "left:430px;top:650px", T("sceptre"), "pop", z=9)
sh.tween(f"#e{sh._uid}", "rotation: -14", 'rotation: 0, duration: 0.6, ease: "power3.out"', T("sceptre"))
e4.kw("Sceptre d'or", "left:480px;top:960px;font-size:78px", T("sceptre") + 0.15, "pop", rot=3, cls="gold")
e4.ring(850, 690, 105, T("sceptre") + 0.2, "#f6d77f", 0.8)

# ===== e5 · 22.98 – 28.64 : Mordecai's challenge (Est 4:14) =====
e5 = sh.scene("s5", 22.98, 28.64, "trone", zoom=(1.08, 1.18), pan=(-30, 0), dark=0.35)
e5.element("personnage-21-mardochee", 1000, "left:60px;top:520px", T("mardochée"), "rise", fade_bottom=True)
e5.ref("Esther 4.14", "left:60px;top:190px", 23.1)
e5.kw("Pour un temps<br>comme celui-ci", "left:380px;top:400px;font-size:82px", T("temps"), "pop", rot=3, cls="gold")
sh.sfx("whoosh", 22.85)

# ===== e6 · 28.64 – 31.4 : three days of fasting (Est 4:16) =====
e6 = sh.scene("s6", 28.64, 31.4, "jeune", zoom=(1.0, 1.1), pan=(-30, 0), dark=0.05)
e6.element("personnage-24-peuple-jeune", 620, "left:200px;top:860px", 28.75, "rise", fade_bottom=False)
e6.ref("Esther 4.16", "left:60px;top:190px", 28.75)
e6.kw("3 JOURS", "left:0;width:1080px;top:290px;font-size:230px", T("trois"), "pop", hero=True, tick=False)
sh.sfx("hit", T("trois"), 0.8)
sh.flash(T("trois"), "gold", 0.3)
e6.element("objet-38-sac-cendres", 330, "left:40px;top:620px", T("jeûne"), "pop", z=8)
sh.sfx("whoosh", 28.5)

# ===== e7 · 31.4 – 34.96 : « If I perish, I perish » =====
e7 = sh.scene("s7", 31.4, 34.96, "jeune", zoom=(1.12, 1.0), pan=(20, 0), dark=0.3)
e7.element("personnage-20-esther-portrait", 800, "left:130px;top:560px", 31.5, "rise", fade_bottom=True)
e7.kw("SI JE DOIS PÉRIR", "left:0;width:1080px;top:230px;font-size:104px", T("périr"), "pop", hero=True, tick=False, cls="cream")
e7.kw("JE PÉRIRAI", "left:0;width:1080px;top:400px;font-size:150px", T("périrai"), "drop", hero=True, tick=False)
sh.sfx("riser", T("périrai") - 1.4, 0.8)
sh.sfx("hit", T("périrai"), 1.0)
sh.flash(T("périrai"), "gold", 0.5)
sh.punch("s7", T("périrai"), 1.06)

# ===== e8 · 34.96 – 36.88 : she walks in =====
e8 = sh.scene("s8", 34.96, 36.88, "couloir", zoom=(1.2, 1.0), pan=(0, -30), dark=0.1)
e8.element("personnage-19-esther-pied", 980, "left:300px;top:620px", 35.05, "rise", fade_bottom=True)
e8.kw("ELLE ENTRE", "left:0;width:1080px;top:260px;font-size:170px", T("entre"), "pop", hero=True, tick=False, cls="cream")
sh.sfx("riser", 35.2, 0.5)

# ===== e9 · 36.88 – 38.68 : the king holds out the golden scepter (Est 5:2) =====
e9 = sh.scene("s9", 36.88, 38.68, "trone", zoom=(1.0, 1.12), pan=(0, 0), dark=0.0)
e9.raw('<div class="gold-glow" id="g9"></div>')
sh.tween("#g9", "opacity: 0", 'opacity: 1, duration: 0.4, ease: "power1.out"', 36.9)
e9.element("personnage-22-roi-sceptre", 900, "left:120px;top:640px", 36.95, "slamL", fade_bottom=True)
e9.ref("Esther 5.2", "left:60px;top:190px", 36.95)
e9.kw("IL TEND", "left:0;width:1080px;top:270px;font-size:210px", T("tend"), "pop", hero=True, tick=False)
sh.sfx("hit", T("tend"), 1.0)
sh.sfx("spark", T("sceptre", 1), 1.0)
sh.flash(T("tend"), "gold", 0.6)
sh.punch("s9", T("tend"), 1.07)

# ===== e10 · 38.68 – 43.8 : the banquet, then Haman is exposed (Est 5:4, 7:1-6) =====
e10 = sh.scene("s10", 38.68, 43.8, "festin", zoom=(1.0, 1.12), pan=(30, 0))
e10.element("personnage-20-esther-portrait", 720, "left:330px;top:540px", 38.8, "rise", fade_bottom=True)
e10.ref("Esther 5.4 · 7.1-6", "left:60px;top:190px", 38.8)
e10.kw("FESTIN", "left:0;width:1080px;top:270px;font-size:210px", T("festin"), "pop", hero=True, tick=False)
e10.element("objet-36-plat-fruits", 360, "left:30px;top:900px", T("festin") + 0.2, "pop", z=9)
e10.element("objet-35-coupe-or", 330, "left:790px;top:900px", T("festin") + 0.5, "pop", z=9)
e10.kw("DÉNONCE", "left:0;width:1080px;top:270px;font-size:170px", T("dénonce"), "drop", hero=True, tick=False, cls="rust")
sh.sfx("hit", T("dénonce"), 0.9)
sh.flash(T("dénonce"), "red", 0.4)
# The first keyword leaves when the accusation lands.
sh.tween("#e" + str(sh._uid - 3), "opacity: 1", 'opacity: 0, duration: 0.2', T("dénonce") - 0.1)

# ===== e11 · 43.8 – 46.6 : Haman hanged on his own gallows (Est 7:10) =====
e11 = sh.scene("s11", 43.8, 46.6, "couloir", zoom=(1.0, 1.1), pan=(-25, 0), dark=0.62)
e11.element("objet-42-potence", 1450, "left:330px;top:300px", T("potence") - 0.3, "rise", fade_bottom=True)
e11.ref("Esther 7.10", "left:60px;top:190px", 43.9)
e11.kw("POTENCE", "left:0;width:1080px;top:290px;font-size:190px", T("potence"), "drop", hero=True, tick=False, cls="cream")
sh.sfx("hit", T("potence"), 1.0)
sh.flash(T("potence"), "red", 0.45)
sh.punch("s11", T("potence"), 1.06)

# ===== e12 · 46.6 – 50.8 : the people are saved — Purim (Est 9) =====
e12 = sh.scene("s12", 46.6, 50.8, "festin", zoom=(1.1, 1.0), pan=(-30, 0))
e12.raw('<div class="gold-glow" id="g12"></div>')
sh.tween("#g12", "opacity: 0", 'opacity: 1, duration: 0.8, ease: "power1.out"', T("sauvé") - 0.3)
e12.element("personnage-24-peuple-jeune", 560, "left:260px;top:880px", 46.7, "rise")
e12.ref("Esther 9.20-28", "left:60px;top:190px", 46.7)
sauve = e12.kw("SAUVÉ", "left:0;width:1080px;top:270px;font-size:230px", T("sauvé"), "pop", hero=True, tick=False)
sh.sfx("hit", T("sauvé"), 0.9)
sh.flash(T("sauvé"), "gold", 0.5)
sh.tween(f"#{sauve}", "opacity: 1", 'opacity: 0, duration: 0.2', T("purim") - 0.1)
e12.kw("PURIM", "left:0;width:1080px;top:300px;font-size:230px", T("purim"), "drop", hero=True, tick=False, cls="cream")
e12.element("objet-35-coupe-or", 340, "left:60px;top:900px", T("purim") + 0.1, "pop", z=9)
e12.element("objet-36-plat-fruits", 380, "left:690px;top:940px", T("purim") + 0.3, "pop", z=9)
sh.sfx("spark", T("purim"), 0.8)
sh.sfx("whoosh", 46.45)

# ===== e13 · 50.8 – 54.76 : the book never names God =====
e13 = sh.scene("s13", 50.8, 54.76, "trone", zoom=(1.05, 1.15), pan=(25, 0), dark=0.6)
e13.element("objet-41-trone-or", 780, "left:350px;top:640px", 51.0, "rise", fade_bottom=True)
e13.kw("Le livre d'Esther", "left:90px;top:300px;font-size:88px", 51.0, "pop", rot=-2, cls="small", tick=False)
e13.kw("NE NOMME JAMAIS", "left:0;width:1080px;top:520px;font-size:120px", T("jamais") - 0.7, "pop", hero=True, tick=False, cls="cream")
e13.kw("DIEU", "left:0;width:1080px;top:740px;font-size:260px", T("dieu"), "pop", hero=True, tick=False)
sh.sfx("hit", T("dieu"), 0.7)
sh.flash(T("dieu"), "gold", 0.35)

# ===== e14 · 54.76 – 59.8 : the question and the comment call =====
e14 = sh.scene("s14", 54.76, 59.8, "couloir", zoom=(1.2, 1.0), pan=(0, 0), dark=0.1)
e14.element("personnage-19-esther-pied", 920, "left:70px;top:700px", 54.9, "rise", fade_bottom=True)
e14.kw("ET TOI ?", "left:0;width:1080px;top:280px;font-size:230px", T("toi"), "pop", hero=True, tick=False)
sh.sfx("hit", T("toi"), 0.7)
sh.flash(T("toi"), "gold", 0.4)
e14.kw("Quel courage ?", "left:480px;top:760px;font-size:82px", T("courage"), "pop", rot=3, cls="gold")
j = sh.uid()
e14.raw(f'<div class="cta" id="{j}" style="top:1010px"><svg class="bubble" viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z" /></svg>À toi de répondre</div>')
e14._anim(f"#{j}", T("commentaire") - 0.5, "slamL")
sh.tween(f"#{j} path", "strokeDashoffset: 420", 'strokeDashoffset: 0, duration: 0.7, ease: "power2.inOut"', T("commentaire") - 0.3)

# ===== e15 · 59.8 – 62.4 : end card =====
e15 = sh.scene("s15", 59.8, DUR, "parchemin")
e15.raw('<div class="head" id="end" style="top:430px"><span class="endkicker" id="ek">Abonne-toi</span><span class="endrule" id="r1"></span>'
        '<p class="title" id="et">La Bible Simple</p><span class="endrule" id="r2"></span></div>')
sh.tween("#ek", "opacity: 0, y: 20", 'opacity: 1, y: 0, duration: 0.5', 59.9)
sh.tween("#r1, #r2", "scaleX: 0", 'scaleX: 1, duration: 0.8, ease: "power2.inOut"', 59.95)
sh.tween("#et", "opacity: 0, y: 30, scale: 0.9", 'opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "back.out(1.8)"', 60.1)
k = sh.uid()
e15.raw(f'<div class="subpill" id="{k}" style="top:880px"><svg viewBox="0 0 24 24" fill="#f6d77f"><path d="M12 2a6 6 0 0 0-6 6v3.6L4.2 15a1 1 0 0 0 .9 1.5h13.8a1 1 0 0 0 .9-1.5L18 11.6V8a6 6 0 0 0-6-6zm0 20a3 3 0 0 0 3-3H9a3 3 0 0 0 3 3z"/></svg>S\'abonner</div>')
e15._anim(f"#{k}", 60.5, "pop")
sh.tween(f"#{k}", "scale: 1", 'scale: 1.07, duration: 0.45, yoyo: true, repeat: 3, ease: "sine.inOut"', 61.0)

# ===== sound bed =====
if os.path.exists(os.path.join(HERE, "assets/audio/music.wav")):
    sh.audio.insert(0, ("music", "assets/audio/music.wav", 0, DUR, MUSIC_VOL))

sh.build(os.path.join(HERE, "..", "template-short.tpl"), suppress=[(59.7, DUR)])
