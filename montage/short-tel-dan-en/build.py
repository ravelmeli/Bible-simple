"""English short « King David's name carved in stone » (Tel Dan stele) for Faith Engineering, style 02 — 9:16, 58 s.

Same stations, stickers and music as montage/short-tel-dan/ (French); texts translated, every beat retimed on the
English transcript.
Run: python3 build.py   (then npx hyperframes check and npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - Tel Dan stele - style 02", "lang": "en"}
s.setup(here=HERE, duration=58.0, cols=3, rows=4, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

# ================================================================ STORY
S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10 = (2, 3)

# --- S1 · hook: David is on screen from the first frame
cam(0, S1)
sticker(S1, "david-lyre", 60, 600, 320, 0.0, rot=-3, instant=True)
headline(S1, 300, ["Did David", "really [exist]?"], 0.0, kicker="Archaeology · Tel Dan", hl_t=T("exist") + 0.1, size=100)
label_box(S1, 440, 760, "No sure trace", "outside the Bible before 1993", T("scholars") - 0.1)
tag(S1, 440, 900, "Scholars doubted", T("doubted") - 0.2, "", 40)

# --- S2 · the discovery: 1993, Tel Dan, northern Israel
t2 = T("then") - 0.2
cam(t2, S2)
headline(S2, 280, ["[1993], Tel Dan"], t2 + 0.1, kicker="The discovery", hl_t=T("1993"), size=104)
sticker(S2, "archeologue", 40, 500, 280, T("1993") - 0.1, rot=-2)
mi, _ = map_svg(S2, 330, 470, "assets/map.json", T("tel") - 0.3, T("dan"), width=600)
tag(S2, 50, 1150, "Reused in a wall", T("wall") - 0.2, "acc", 46)
ref(S2, 50, 1250, "Map: Natural Earth", T("wall"))

# --- S3 · the object: a basalt fragment covered in Aramaic writing
t3 = T("piece") - 0.5
cam(t3, S3)
headline(S3, 280, ["A fragment", "of [basalt]"], t3 + 0.1, kicker="The object", hl_t=T("basalt"), size=96)
sticker(S3, "stele-tel-dan", 110, 590, 820, T("piece") - 0.2, rot=-2)
tag(S3, 60, 1290, "Written in Aramaic", T("aramaic") - 0.1, "acc", 48)

# --- S4 · the author: a king of Damascus boasts
t4 = T("king", 1) - 0.5
cam(t4, S4)
headline(S4, 280, ["A king of [Damascus]"], t4 + 0.1, kicker="The author", hl_t=T("damascus"), size=96)
sticker(S4, "roi-damas-pied", 50, 460, 360, T("king", 1) - 0.2, rot=-2)
label_box(S4, 470, 470, "Probably Hazael", "king of Aram-Damascus · hypothesis", T("boasts") - 0.1)
sticker(S4, "ivoire-femme-fenetre", 520, 620, 260, T("victory") - 0.3, rot=4)
label_box(S4, 520, 1010, "Syrian ivory", "9th–8th c. BC · The Met", T("victory"))
tag(S4, 50, 1190, "Killed: the king of Israel", T("killed"), "", 40)
tag(S4, 50, 1285, "Killed: the king of the “House of David”", T("“House") - 0.1, "acc", 36)
hit(T("“House"), 0.9)

# --- S5 · the words: the "House of David" line on the stone
t5 = T("house", 1) - 0.6
cam(t5, S5)
headline(S5, 280, ["“House of [David]”"], t5 + 0.1, kicker="The key words", hl_t=T("david", 2), size=96)
sticker(S5, "ligne-maison-david", 60, 520, 900, t5 + 0.15, rot=-1)
label_box(S5, 60, 840, "BYTDWD", "“House of David,” read right to left", t5 + 0.5)
tag(S5, 60, 1000, "= his dynasty", T("dynasty") - 0.1, "acc", 56)

# --- S6 · the date: about 150 years after his reign; first widely accepted mention
t6 = T("dates") - 0.9
cam(t6, S6)
headline(S6, 280, ["[150 years] later"], t6 + 0.1, kicker="The date", hl_t=T("150"), size=100)
sticker(S6, "david-lyre", 60, 480, 200, t6 + 0.2, rot=-3)
sticker(S6, "stele-tel-dan", 690, 560, 280, t6 + 0.4, rot=3)
counter(S6, 290, 660, 0, 150, T("150") - 0.05, 0.9, " years", 100, "small")
sx6, sy6 = st(*S6)
tl6 = uid()
html.append(f'<svg class="node lead" id="{tl6}" style="left:{sx6}px;top:{sy6}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<path d="M160 1000 L830 1000" stroke-dasharray="680" style="stroke-width:6"/>'
            f'<circle cx="160" cy="1000" r="14" style="fill:{INK}"/><circle class="e" cx="830" cy="1000" r="14" style="fill:{ACC}"/></svg>')
tween(f"#{tl6} path", "strokeDashoffset: 680", 'strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut"', T("150") - 0.1)
tween(f"#{tl6} .e", "scale: 0, transformOrigin: \"50% 50%\"", 'scale: 1, duration: 0.3, ease: "back.out(3)"', T("150") + 0.8)
label_box(S6, 60, 1040, "David", "c. 1000 BC", T("reign") - 0.3)
label_box(S6, 640, 1040, "The stele", "c. 840 BC", T("reign"))
tag(S6, 60, 1200, "1st mention outside the Bible", T("first"), "acc", 44)
ref(S6, 60, 1300, "Widely accepted by scholars", T("accepted"))

# --- S7 · written by an enemy
t7 = T("and", 1) - 0.2
cam(t7, S7)
headline(S7, 280, ["Written by", "an [enemy]"], t7 + 0.1, kicker="The witness", hl_t=T("enemy"), size=100)
sticker(S7, "roi-damas-portrait", 200, 560, 640, t7 + 0.2, rot=-2)
hit(T("enemy"), 0.8)

# --- pull-out at the surprising part, then S8 · the Bible credits the two kings' deaths to Jehu (2 Kings 9)
t_all = T("here's") - 0.2
cam(t_all, "all")
t8 = T("bible", 1) - 0.4
cam(t8, S8)
# The chapter bar fades out while the whole canvas is shown, so it never sits on top of the tiny station texts.
tween("#chrome", "opacity: 1", 'opacity: 0, duration: 0.25, immediateRender: false', t_all)
tween("#chrome", "opacity: 0", 'opacity: 1, duration: 0.3, immediateRender: false', t8 + 0.6)
headline(S8, 280, ["The Bible says:", "[Jehu]"], t8 + 0.1, kicker="The surprising part", hl_t=T("jehu"), size=100)
sticker(S8, "jehu-arc", 50, 560, 420, T("kings’ deaths") - 0.4, rot=-2)
label_box(S8, 520, 600, "Joram", "king of Israel", T("kings’ deaths") - 0.2)
label_box(S8, 520, 720, "Ahaziah", "king of Judah", T("kings’ deaths"))
ref(S8, 520, 850, "2 Kings 9", T("kings’ deaths") + 0.2)
tag(S8, 50, 1240, "Two sides, two versions", T("general") - 0.2, "acc", 48)

# --- S9 · dark-mode reveal: to his neighbors, the House of David was real
t9 = T("this") - 0.3
cam(t9, S9)
dark_mode(t9 - 0.1)
headline(S9, 280, ["The House of David", "was [real]"], t9 + 0.1, kicker="What the stone shows", hl_t=T("real"), size=90, dark=True)
label_box(S9, 70, 560, "One single stone", "not proof of the whole story", T("prove") - 0.1, dark=True)
ref(S9, 70, 680, "Israel Museum, Jerusalem", T("prove") + 0.3)
sticker(S9, "stele-tel-dan", 180, 760, 660, T("but", 1) - 0.1, rot=2)
hit(T("real"), 1.0)

# --- S10 · call to comment
t10 = T("what") - 0.3
cam(t10, S10)
headline(S10, 300, ["What [discovery]", "next?"], t10 + 0.1, kicker="Your turn", hl_t=T("discovery"), size=104, dark=True)
sticker(S10, "archeologue", 560, 700, 400, t10 + 0.3, rot=3)
cta = put(S10, 70, 1150, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Reply in the comments', "cta")
blur_in(cta, T("tell") - 0.2, 14)
sfx("click", T("tell") - 0.2, 0.8)

# --- end · pull out, then the end card during "subscribe"
t_end = T("subscribe") - 0.6
cam(t_end, "all")

# ================================================================ assemble
build(
    chapters=[("01", "The discovery", 0, t3), ("02", "The inscription", t3, t_all), ("03", "The twist", t_all, t9), ("04", "Lesson", t9, DUR)],
    suppress=[(T("subscribe") - 0.7, DUR)],
    endcard={"kicker": "Follow along", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("stele-tel-dan", 40, 1180, 380, -6), ("david-lyre", 800, 1040, 220, 5)]},
    endcard_t=T("subscribe") - 0.1,
    music_volume=0.14,
)
