"""Short "Jesus spoke Aramaic", English version, style 02 — 9:16, 66.4 s.

Built with the kit engine (kit-style-02/moteur/style02.py). Every element is timed on transcript.json.
Aramaic words are written in Latin letters (transcription) in HTML, never in an image.
Run: python3 build.py   (then npx hyperframes check and npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - Jesus spoke Aramaic - style 02", "lang": "en"}
s.setup(here=HERE, duration=66.4, cols=3, rows=5, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10 = (2, 3)

html.append('<style>.box.wide{text-align:left;font-weight:700;line-height:1.3}</style>')

# --- S1 · hook: Jesus is on screen from the first frame
cam(0, S1)
sticker(S1, "jesus-pied", 60, 580, 320, 0.0, rot=-3, instant=True)
headline(S1, 300, ["Jesus spoke", "[Aramaic]"], 0.0, kicker="The Gospels are in Greek", hl_t=T("Aramaic") + 0.05, size=104)
tag(S1, 440, 760, "Gospels: Greek", T("Greek") - 0.2, "", 52)
tag(S1, 440, 880, "Jesus: Aramaic", T("Aramaic") - 0.1, "acc", 52)
hit(T("Aramaic"), 0.9)

# --- S2 · the language of everyday life in first-century Palestine
t2 = T("Palestine,") - 0.7
cam(t2, S2)
headline(S2, 280, ["The language of", "[everyday life]"], t2 + 0.1, kicker="Palestine · 1st century", hl_t=T("everyday"), size=96)
map_svg(S2, 40, 620, "assets/map.json", t2 + 0.3, T("language"), width=860)
tag(S2, 60, 1230, "A Galilean speech", T("language") - 0.1, "acc", 48)
ref(S2, 60, 1340, "Schematic map · Natural Earth", T("life."))

# --- S3 · words kept just as he said them
t3 = T("Gospel") - 0.5
cam(t3, S3)
headline(S3, 280, ["Words [kept]"], t3 + 0.1, kicker="The Gospel writers", hl_t=T("kept"), size=110)
sticker(S3, "parchemin", 60, 580, 360, T("wrote") - 0.2, rot=-3)
tag(S3, 60, 1000, "Written in Greek", T("Greek", 1) - 0.1, "", 48)
sticker(S3, "ostracon-arameen", 480, 640, 470, T("just") - 0.4, rot=3)
label_box(S3, 480, 960, "Aramaic text", "ostracon, c. AD 500-600 · The Met", T("just"))
tag(S3, 60, 1110, "Just as he said them", T("said") - 0.2, "acc", 44)

# --- S4 · "Talitha cumi" (Mark 5:41), captions cut
t4 = T("Before") - 0.6
cam(t4, S4)
headline(S4, 280, ["[Talitha] cumi"], t4 + 0.1, kicker="Mark 5:41", hl_t=T("Talitha"), size=110)
sticker(S4, "fille", 60, 600, 270, T("girl") - 0.2, rot=-2)
q4 = put(S4, 400, 680, "<small>Mark 5:41 · WEB</small>“Girl, I tell you, get up!”", "box wide", "width:540px;font-size:40px")
blur_in(q4, T("Girl,") - 0.1, 14)
tag(S4, 400, 1010, "For a little girl", T("Before") - 0.1, "", 44)
hit(T("Talitha"), 1.0)

# --- S5 · "Ephphatha" (Mark 7:34)
t5 = T("deaf") - 0.9
cam(t5, S5)
headline(S5, 280, ["[Ephphatha]"], t5 + 0.1, kicker="Mark 7:34", hl_t=T("Ephphatha,"), size=110)
sticker(S5, "sourd", 60, 600, 270, T("deaf") - 0.3, rot=2)
tag(S5, 400, 700, "To a deaf man", T("deaf") - 0.1, "", 52)
tag(S5, 400, 830, "“Be opened”", T("opened.") - 0.5, "acc", 64)
ref(S5, 400, 960, "Mark 7:34 · WEB", T("opened.") + 0.2)
hit(T("Ephphatha,"), 0.9)

# --- S6 · "Abba" at Gethsemane (Mark 14:36)
t6 = T("prayer") - 0.8
cam(t6, S6)
headline(S6, 280, ["[Abba]"], t6 + 0.1, kicker="Mark 14:36 · Gethsemane", hl_t=T("Abba,"), size=130)
sticker(S6, "jesus-priere", 60, 600, 470, T("Gethsemane,") - 0.3, rot=-2)
tag(S6, 60, 1200, "In prayer", T("prayer") - 0.1, "", 48)
tag(S6, 560, 780, "Father", T("Father.") - 0.1, "acc", 100)
hit(T("Abba,"), 0.9)

# --- S7 · "Eloi, Eloi, lama sabachthani" on the cross (Mark 15:34), captions cut
t7 = T("cross,") - 0.7
cam(t7, S7)
headline(S7, 280, ["[Eloi], Eloi,", "lama sabachthani"], t7 + 0.1, kicker="Mark 15:34", hl_t=T("Eloi,"), size=84)
q7 = put(S7, 60, 690, "<small>Mark 15:34 · WEB</small>“My God, my God, why have you forsaken me?”", "box wide", "width:900px;font-size:36px")
blur_in(q7, T("my") - 0.1, 14)
tag(S7, 60, 1030, "On the cross", T("cross,") - 0.1, "", 52)
sticker(S7, "jesus-portrait", 600, 1020, 300, T("means,") - 0.2, rot=3)

# --- S8 · Hebrew and a little Greek: a hypothesis
t8 = T("Did") - 0.4
cam(t8, S8)
headline(S8, 280, ["And [Hebrew] ?"], t8 + 0.1, kicker="The question", hl_t=T("Hebrew"), size=120)
sticker(S8, "jesus-pied", 60, 600, 260, T("Did") - 0.1, rot=-2)
tag(S8, 400, 640, "Hebrew", T("Hebrew") - 0.1, "", 56)
tag(S8, 400, 760, "A little Greek", T("Greek", 2) - 0.2, "", 56)
tag(S8, 400, 920, "Hypothesis", T("hypothesis.") - 0.1, "acc", 72)
tag(S8, 400, 1060, "The text doesn't say", T("text") - 0.1, "", 40)
hit(T("hypothesis."), 1.0)

# --- S9 · dark mode: his most intimate words stayed in his mother tongue
t_all = T("Here's") - 1.2
cam(t_all, "all")
t9 = T("Here's") - 0.4
cam(t9, S9)
dark_mode(t9 - 0.1)
headline(S9, 280, ["His most [intimate]", "words"], t9 + 0.1, kicker="The surprising part", hl_t=T("intimate"), size=100, dark=True)
tag(S9, 70, 700, "At a child's bedside", T("bedside,") - 0.4, "dark", 44)
tag(S9, 70, 810, "In prayer", T("prayer", 1) - 0.1, "dark", 44)
tag(S9, 70, 920, "On the cross", T("cross,", 1) - 0.1, "dark", 44)
tag(S9, 70, 1070, "His mother tongue", T("mother") - 0.2, "acc", 56)
sticker(S9, "jesus-portrait", 620, 700, 320, T("intimate") - 0.2, rot=3)
hit(T("tongue."), 1.0)

# --- S10 · call to comment
t10 = T("Which", 1) - 0.3
cam(t10, S10)
headline(S10, 330, ["Which Aramaic", "[word] ?"], t10 + 0.1, kicker="Your turn", hl_t=T("word"), size=110, dark=True)
label_box(S10, 70, 840, "Which one struck you most?", "Talitha cumi, Ephphatha, Abba, Eloi", T("most?") - 0.3, dark=True)
sticker(S10, "jesus-portrait", 660, 900, 280, t10 + 0.4, rot=3)
cta = put(S10, 70, 1290, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Tell us in the comments', "cta")
blur_in(cta, T("Tell") - 0.2, 14)
sfx("click", T("Tell") - 0.2, 0.8)

# --- end · pull out, then the end card during "subscribe"
t_end = T("subscribe") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", "The language", 0, t4), ("02", "His words", t4, t8), ("03", "The question", t8, t9), ("04", "Lesson", t9, DUR)],
    suppress=[(T("Girl,") - 0.2, T("up.") + 0.5), (T("my") - 0.2, T("me?") + 0.6), (T("subscribe") - 0.7, DUR)],
    endcard={"kicker": "Follow along", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("jesus-portrait", 30, 1150, 330, -6), ("sourd", 800, 1000, 200, 5)]},
    endcard_t=T("subscribe") - 0.1,
    music_volume=0.14,
)
