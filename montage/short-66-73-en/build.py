"""Short "66 books or 73?", English version, style 02 — 9:16, 56.7 s.

Built with the kit engine (kit-style-02/moteur/style02.py). Every element is timed on transcript.json.
Run: python3 build.py   (then npx hyperframes check and npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - 66 or 73 books - style 02", "lang": "en"}
s.setup(here=HERE, duration=56.7, cols=3, rows=5, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10, S11 = (2, 3), (1, 3)

# --- S1 · hook: seven more books
cam(0, S1)
sticker(S1, "feuillet-bible-latine", 660, 600, 270, 0.0, rot=4, instant=True)
headline(S1, 300, ["[7] more", "books"], 0.0, kicker="Catholic Bible", hl_t=T("seven") + 0.05, size=118)
tag(S1, 60, 760, "Catholic Bible", T("Catholic") - 0.1, "acc", 48)
tag(S1, 60, 880, "Protestant Bible", T("Protestant") - 0.1, "", 48)
hit(T("seven"), 0.8)

# --- S2 · 66 or 73
t2 = T("sixty-six") - 0.5
cam(t2, S2)
headline(S2, 280, ["66 or [73] ?"], t2 + 0.1, kicker="Why?", hl_t=T("seventy-three"), size=130)
counter(S2, 70, 600, 0, 66, T("sixty-six") - 0.1, 0.8, unit=" books", size=150)
counter(S2, 70, 860, 0, 73, T("seventy-three") - 0.1, 0.8, unit=" books", size=150)
tag(S2, 640, 700, "Protestant", T("sixty-six") + 0.3, "", 40)
tag(S2, 640, 960, "Catholic", T("seventy-three") + 0.3, "acc", 40)
tag(S2, 70, 1200, "Why?", T("Why?") - 0.1, "acc", 100)
hit(T("Why?"), 0.9)

# --- S3 · the New Testament is the same everywhere
t3 = T("New") - 0.5
cam(t3, S3)
headline(S3, 280, ["New Testament:", "[27]"], t3 + 0.1, kicker="The same everywhere", hl_t=T("twenty-seven"), size=100)
counter(S3, 70, 640, 0, 27, T("twenty-seven") - 0.2, 0.7, unit=" books", size=190)
tag(S3, 70, 960, "Identical everywhere", T("everywhere,") - 0.1, "", 52)
tag(S3, 70, 1080, "The difference: the Old Testament", T("difference") - 0.1, "acc", 40)

# --- S4 · Protestants follow the Hebrew Bible: 39 books
t4 = T("Protestants") - 0.5
cam(t4, S4)
headline(S4, 280, ["The [Hebrew]", "Bible"], t4 + 0.1, kicker="Protestants", hl_t=T("Hebrew"), size=104)
counter(S4, 70, 640, 0, 39, T("thirty-nine") - 0.2, 0.8, unit=" books", size=190)
tag(S4, 70, 960, "Old Testament", T("thirty-nine") + 0.2, "", 52)

# --- S5 · Catholics also follow the Septuagint: seven more
t5 = T("Catholics") - 0.5
cam(t5, S5)
headline(S5, 280, ["The [Septuagint]"], t5 + 0.1, kicker="Catholics also", hl_t=T("Septuagint,"), size=104)
sticker(S5, "scribe", 60, 600, 280, T("ancient") - 0.3, rot=-2)
tag(S5, 420, 700, "Greek translation", T("Greek") - 0.1, "", 48)
counter(S5, 420, 840, 0, 7, T("seven", 1) - 0.3, 0.6, unit=" more", size=150)

# --- S6 · the seven books
t6 = T("Tobit,") - 0.6
cam(t6, S6)
headline(S6, 280, ["Seven [books]"], t6 + 0.1, kicker="The extra ones", hl_t=T("Tobit,"), size=104)
tag(S6, 70, 580, "Tobit", T("Tobit,") - 0.1, "", 44)
tag(S6, 70, 680, "Judith", T("Judith,") - 0.1, "", 44)
tag(S6, 70, 780, "Wisdom", T("Wisdom,") - 0.1, "", 44)
tag(S6, 70, 880, "Sirach", T("Sirach,") - 0.1, "", 44)
tag(S6, 70, 980, "Baruch", T("Baruch,") - 0.1, "", 44)
tag(S6, 70, 1080, "1 Maccabees", T("two") - 0.1, "acc", 44)
tag(S6, 70, 1180, "2 Maccabees", T("Maccabees.") - 0.2, "acc", 44)
sticker(S6, "feuillet-nehemie", 640, 640, 290, T("Tobit,") + 0.2, rot=3)

# --- S7 · Luther sets them apart (16th century)
t7 = T("sixteenth") - 0.5
cam(t7, S7)
headline(S7, 280, ["Luther sets", "them [apart]"], t7 + 0.1, kicker="16th century", hl_t=T("apart"), size=100)
sticker(S7, "luther", 60, 620, 270, T("Luther") - 0.3, rot=-2)
tag(S7, 420, 740, "Useful reading", T("useful") - 0.1, "", 52)
tag(S7, 420, 880, "Outside the Bible", T("outside") - 0.1, "acc", 52)
hit(T("outside"), 0.8)

# --- S8 · the Council of Trent, 1546
t8 = T("1546,") - 0.5
cam(t8, S8)
headline(S8, 280, ["The Council", "of [Trent]"], t8 + 0.1, kicker="1546", hl_t=T("Trent"), size=104)
sticker(S8, "eveques", 60, 620, 560, T("Council") - 0.3, rot=-2)
counter(S8, 70, 1070, 1500, 1546, T("1546,") - 0.1, 0.8, size=170)
tag(S8, 70, 1300, "Declared canonical", T("canonical.") - 0.2, "acc", 52)
hit(T("canonical."), 1.0)

# --- S9 · the Orthodox Churches count even more
t9 = T("Orthodox") - 0.8
cam(t9, S9)
headline(S9, 280, ["The [Orthodox]", "Churches"], t9 + 0.1, kicker="Even more", hl_t=T("Orthodox"), size=100)
tag(S9, 70, 680, "Even more books", T("even") - 0.1, "acc", 60)
tag(S9, 70, 820, "Depending on tradition", T("traditions.") - 0.3, "", 48)
sticker(S9, "livres", 640, 960, 280, T("count") - 0.2, rot=3)

# --- S10 · dark mode: Jerome and the Vulgate
t_all = T("Here's") - 1.2
cam(t_all, "all")
t10 = T("Here's") - 0.4
cam(t10, S10)
dark_mode(t10 - 0.1)
headline(S10, 280, ["Jerome and", "the [Vulgate]"], t10 + 0.1, kicker="The surprising part", hl_t=T("Vulgate,"), size=100, dark=True)
sticker(S10, "jerome-pied", 60, 620, 250, T("Jerome,") - 0.2, rot=-2)
sticker(S10, "saint-jerome-peinture", 640, 640, 270, T("Jerome,") + 0.2, rot=3)
tag(S10, 340, 1010, "Translator of the Vulgate", T("translator") - 0.1, "dark", 40)
tag(S10, 340, 1100, "Not in the Hebrew Bible", T("Hebrew", 1) - 0.4, "dark", 36)
tag(S10, 340, 1190, "Yet he included them", T("included") - 0.2, "acc", 44)
hit(T("anyway."), 1.0)

# --- S11 · call to comment
t11 = T("Which", 1) - 0.3
cam(t11, S11)
headline(S11, 330, ["Which [Bible]", "do you read ?"], t11 + 0.1, kicker="Your turn", hl_t=T("Bible", 8) if False else T("read?"), size=110, dark=True)
label_box(S11, 70, 840, "Catholic, Protestant, Orthodox?", "tell us yours", T("read?") - 0.2, dark=True)
sticker(S11, "jerome-portrait", 640, 900, 280, t11 + 0.4, rot=3)
cta = put(S11, 70, 1290, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Tell us in the comments', "cta")
blur_in(cta, T("Tell") - 0.2, 14)
sfx("click", T("Tell") - 0.2, 0.8)

# --- end · pull out, then the end card during "subscribe"
t_end = T("subscribe") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", "The numbers", 0, t4), ("02", "The difference", t4, t_all), ("03", "Jerome", t_all, t11), ("04", "Lesson", t11, DUR)],
    suppress=[(T("subscribe") - 0.7, DUR)],
    endcard={"kicker": "Follow along", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("jerome-portrait", 30, 1150, 330, -6), ("luther", 800, 1000, 200, 5)]},
    endcard_t=T("subscribe") - 0.1,
    music_volume=0.14,
)
