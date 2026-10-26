"""Short "Jael and the tent peg" (Judges 4-5), English version, style 02 — 9:16, 62.4 s.

Built with the kit engine (kit-style-02/moteur/style02.py). Every element is timed on transcript.json.
Run: python3 build.py   (then npx hyperframes check and npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - Jael - style 02", "lang": "en"}
s.setup(here=HERE, duration=62.4, cols=3, rows=5, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10, S11, S12 = (2, 3), (1, 3), (0, 3)
S13 = (0, 4)

html.append('<style>.box.wide{text-align:left;font-weight:700;line-height:1.3}</style>')

# --- S1 · hook: Jael is on screen from the first frame
cam(0, S1)
sticker(S1, "jael-pied", 60, 560, 330, 0.0, rot=-3, instant=True)
headline(S1, 300, ["One woman", "with no [army]"], 0.0, kicker="Judges 4", hl_t=T("army") + 0.05, size=104)
label_box(S1, 450, 700, "Jael", "wife of Heber the Kenite", T("Jael"))
tag(S1, 450, 900, "20 years of war", T("twenty") - 0.1, "acc", 48)
hit(T("army"), 0.8)

# --- S2 · the king of Canaan oppresses Israel for twenty years
t2 = T("king") - 0.4
cam(t2, S2)
headline(S2, 280, ["The king of", "[Canaan]"], t2 + 0.1, kicker="Israel oppressed", hl_t=T("Canaan"), size=100)
map_svg(S2, 40, 580, "assets/map.json", t2 + 0.3, T("Canaan"), width=800)
counter(S2, 60, 1215, 0, 20, T("twenty", 1) - 0.2, 1.0, unit=" years", size=140)
ref(S2, 60, 1385, "Schematic map · Natural Earth", T("for", 1))

# --- S3 · Sisera and nine hundred iron chariots
t3 = T("commander") - 0.6
cam(t3, S3)
headline(S3, 280, ["His [commander]"], t3 + 0.1, kicker="Sisera", hl_t=T("commander"), size=104)
sticker(S3, "sisera", 60, 600, 250, T("Sisera") - 0.2, rot=-2)
sticker(S3, "tablette-char", 430, 620, 480, T("nine") - 0.3, rot=3)
label_box(S3, 430, 930, "A war chariot", "faience, Egypt, c. 1390 BC · The Met", T("chariots") - 0.5)
counter(S3, 430, 1110, 0, 900, T("nine") - 0.1, 1.1, unit=" chariots", size=96)
tag(S3, 430, 1260, "made of iron", T("iron") - 0.1, "acc", 56)
hit(T("iron"), 1.0)

# --- S4 · the prophetess Deborah and Barak
t4 = T("prophetess") - 0.5
cam(t4, S4)
headline(S4, 280, ["The prophetess", "[Deborah]"], t4 + 0.1, kicker="Judges 4:4-6", hl_t=T("Deborah"), size=96)
sticker(S4, "debora", 60, 580, 320, T("Deborah") - 0.3, rot=-2)
sticker(S4, "barak", 560, 640, 300, T("Barak") - 0.3, rot=3)
label_box(S4, 560, 1080, "Barak", "Israelite general", T("Barak"))

# --- S5 · "The journey that you take won't be for your honor" (Judges 4:9), captions cut
t5 = T("journey") - 0.6
cam(t5, S5)
headline(S5, 280, ["A [surprising]", "prophecy"], t5 + 0.1, kicker="Judges 4:9", hl_t=T("honor"), size=96)
q5 = put(S5, 60, 640, "<small>Judges 4:9 · World English Bible</small>“The journey that you take won't be for your honor; "
         "for Yahweh will sell Sisera into the hand of a woman.”", "box wide", "width:900px;font-size:36px")
blur_in(q5, T("journey") - 0.1, 14)
tag(S5, 60, 1130, "No honor for Barak", T("honor") - 0.1, "", 48)
tag(S5, 60, 1240, "Into the hand of a woman", T("hand") - 0.2, "acc", 48)
hit(T("woman", 1), 0.9)

# --- S6 · Sisera is defeated and flees on foot to Jael's tent
t6 = T("Sisera", 2) - 0.4
cam(t6, S6)
headline(S6, 280, ["Sisera [flees]", "on foot"], t6 + 0.1, kicker="Defeated", hl_t=T("flees"), size=100)
sticker(S6, "sisera", 60, 600, 250, T("defeated") - 0.2, rot=-2)
sticker(S6, "tente", 400, 680, 520, T("foot") - 0.3, rot=3)
label_box(S6, 400, 1180, "Jael's tent", "Judges 4:17", T("foot") + 0.1)

# --- S7 · "Turn in, my lord…" (Judges 4:18), captions cut
t7 = 27.5
cam(t7, S7)
headline(S7, 280, ["She [invites] him"], t7 + 0.1, kicker="Judges 4:18", hl_t=T("turn"), size=100)
sticker(S7, "jael-portrait", 580, 560, 370, t7 + 0.4, rot=3)
q7 = put(S7, 60, 1000, "<small>Judges 4:18 · WEB</small>“Turn in, my lord, turn in to me; don't be afraid.”",
         "box wide", "width:900px;font-size:36px")
blur_in(q7, T("turn") - 0.1, 14)

# --- S8 · water, milk, he falls asleep
t8 = T("asks") - 0.5
cam(t8, S8)
headline(S8, 280, ["He asks for water,", "she gives [milk]"], t8 + 0.1, kicker="Judges 4:19", hl_t=T("milk"), size=84)
sticker(S8, "sisera", 60, 600, 250, T("asks") - 0.2, rot=-2)
tag(S8, 400, 700, "Water", T("water") - 0.1, "", 56)
tag(S8, 400, 820, "Milk", T("milk") - 0.1, "acc", 56)
tag(S8, 400, 960, "Exhausted", T("exhausted") - 0.1, "", 52)
tag(S8, 400, 1070, "He falls asleep", T("falls") - 0.1, "acc", 52)

# --- S9 · the peg and the hammer: dark mode
t_all = T("Then") - 1.2
cam(t_all, "all")
t9 = T("Then") - 0.4
cam(t9, S9)
dark_mode(t9 - 0.1)
headline(S9, 280, ["A tent [peg]", "and a hammer"], t9 + 0.1, kicker="Judges 4:21", hl_t=T("peg"), size=104, dark=True)
sticker(S9, "jael-pied", 60, 600, 300, T("Jael", 1) - 0.2, rot=-2)
tag(S9, 420, 680, "A tent peg", T("peg") - 0.1, "dark", 52)
tag(S9, 420, 790, "A hammer", T("hammer") - 0.1, "acc", 52)
tag(S9, 420, 940, "She strikes", T("strikes") - 0.1, "dark", 56)
tag(S9, 420, 1050, "into the ground", T("ground") - 0.3, "acc", 52)
hit(T("strikes"), 1.0)
hit(T("ground"), 0.8)

# --- S10 · the text doesn't say why: we don't know
t10 = T("text") - 0.5
cam(t10, S10)
headline(S10, 280, ["The text", "[doesn't say]"], t10 + 0.1, kicker="What we don't know", hl_t=T("say", 0), size=104, dark=True)
tag(S10, 70, 680, "Why?", T("why") - 0.1, "acc", 120)
label_box(S10, 70, 900, "The story is silent", "it gives no reason", T("chose"), dark=True)
sticker(S10, "jael-portrait", 620, 1010, 300, T("chose") - 0.2, rot=3)

# --- S11 · Deborah's song (Judges 5:24), captions cut
t11 = T("song") - 0.8
cam(t11, S11)
headline(S11, 280, ["Deborah's", "[song]"], t11 + 0.1, kicker="Judges 5:24", hl_t=T("song"), size=100, dark=True)
sticker(S11, "debora", 60, 620, 300, T("deborah's") - 0.3, rot=-2)
q11 = put(S11, 400, 660, "<small>Judges 5:24 · WEB</small>“Most blessed of women be Jael.”",
          "box wide", "width:540px;font-size:40px")
blur_in(q11, T("most") - 0.1, 14)
hit(T("blessed"), 0.8)

# --- S12 · the glory went to a woman with no sword
t12 = T("Here's") - 0.3
cam(t12, S12)
headline(S12, 280, ["The [glory]"], t12 + 0.1, kicker="The surprising part", hl_t=T("glory"), size=120, dark=True)
sticker(S12, "barak", 60, 590, 225, T("general") - 0.4, rot=-3)
sticker(S12, "jael-pied", 620, 580, 280, T("woman", 2) - 0.4, rot=3)
tag(S12, 60, 1240, "Not to the general", T("general") - 0.1, "dark", 48)
tag(S12, 60, 1335, "But to a woman with no sword", T("woman", 2) - 0.1, "acc", 44)
hit(T("sword"), 1.0)

# --- S13 · call to comment
t13 = T("What") - 0.3
cam(t13, S13)
headline(S13, 330, ["What do you [think] ?"], t13 + 0.1, kicker="Your turn", hl_t=T("think"), size=110, dark=True)
label_box(S13, 70, 700, "What do you think of Jael?", "hero, or troubling act?", T("Jael", 3) - 0.3, dark=True)
sticker(S13, "jael-portrait", 600, 800, 340, t13 + 0.4, rot=3)
cta = put(S13, 70, 1150, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Tell us in the comments', "cta")
blur_in(cta, T("tell") - 0.2, 14)
sfx("click", T("tell") - 0.2, 0.8)

# --- end · pull out, then the end card during "subscribe"
t_end = T("subscribe") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", "Context", 0, t4), ("02", "The story", t4, t9), ("03", "The act", t9, t12), ("04", "Lesson", t12, DUR)],
    suppress=[(17.5, 24.0), (28.7, 32.0), (48.3, 50.5), (T("subscribe") - 0.7, DUR)],
    endcard={"kicker": "Follow along", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("jael-portrait", 30, 1150, 330, -6), ("debora", 800, 1000, 200, 5)]},
    endcard_t=T("subscribe") - 0.1,
    music_volume=0.14,
)
