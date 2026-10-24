"""English short « Who is my neighbor? » (Luke 10:25-37) for the channel Faith Engineering, style 02 — 9:16, 60.9 s.

Same stations, stickers and music as montage/short-prochain/ (French); texts translated, Bible quotes from the
World English Bible (public domain), distances in miles and feet. Every beat is timed on the English transcript.
Run: python3 build.py   (then npx hyperframes check and npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - Who is my neighbor - style 02", "lang": "en"}
s.setup(here=HERE, duration=60.9, cols=3, rows=5, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

# ================================================================ STORY
S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10, S11, S12 = (2, 3), (1, 3), (0, 3)
S13 = (0, 4)

# --- S1 · hook: the teacher of the law is on screen from the first frame (Luke 10:25-29)
cam(0, S1)
sticker(S1, "docteur-pied", 60, 600, 320, 0.0, rot=-3, instant=True)
headline(S1, 300, ["Required to [love]", "whom, exactly?"], 0.0, kicker="Explained · Luke 10", hl_t=T("love") + 0.1, size=96)
label_box(S1, 440, 640, "A teacher of the law", "expert in the Law of Moses", T("teacher"))
tag(S1, 440, 800, "His question to Jesus", T("asks") - 0.1, "", 40)
tag(S1, 60, 1290, "“And who is my neighbor?”", T("and"), "acc", 48)
ref(S1, 60, 1385, "Luke 10:29 · World English Bible", T("neighbor") + 0.2)
hit(T("neighbor"), 0.8)

# --- S2 · Jesus answers with a story
t2 = T("answers") - 0.6
cam(t2, S2)
headline(S2, 300, ["A [story]"], t2 + 0.1, kicker="Jesus’ answer", hl_t=T("story"), size=110)
sticker(S2, "jesus", 300, 520, 430, t2 + 0.2, rot=-2)

# --- S3 · the road: Jerusalem (≈ +2,500 ft) down to Jericho (≈ −800 ft), about 17 miles (orders of magnitude)
t3 = T("man") - 0.6
cam(t3, S3)
headline(S3, 280, ["From [Jerusalem]", "to Jericho"], t3 + 0.15, kicker="The road", hl_t=T("jerusalem"), size=96)
sticker(S3, "route-jericho-aerien", 60, 580, 520, T("going"), rot=-2)
label_box(S3, 60, 975, "The old road, from the air", "Matson photo, c. 1930", T("going") + 0.3)
counter(S3, 640, 590, 0, 17, T("17") - 0.05, 0.6, " mi", 120, "small")
tag(S3, 640, 770, "≈ 3,300 ft", T("3,000"), "acc", 48)
ref(S3, 640, 865, "drop", T("feet"))
sx3, sy3 = st(*S3)
prof = uid()
# Schematic profile: 3,300 ft over 260 px; sea level at 70 + 2,500 × 0.079 ≈ 265 px.
html.append(f'<svg class="node lead" id="{prof}" style="left:{sx3 + 40}px;top:{sy3 + 1070}px" width="1000" height="360" viewBox="0 0 1000 360">'
            f'<path class="sea" d="M20 265 L980 265" style="stroke:#AEB8C3;stroke-dasharray:10 10;stroke-width:3"/>'
            f'<path class="pr" d="M40 70 C 200 80, 260 120, 360 140 S 560 200, 640 230 S 820 300, 940 330" '
            f'style="stroke:{ACC};stroke-width:8;stroke-linecap:round" stroke-dasharray="1000"/>'
            f'<circle cx="40" cy="70" r="12" style="fill:{INK}"/><circle class="end" cx="940" cy="330" r="12" style="fill:{ACC}"/>'
            f'<text x="62" y="60" style="font:700 30px Inter;fill:{INK}">Jerusalem ≈ +2,500 ft</text>'
            f'<text class="tj" x="900" y="355" text-anchor="end" style="font:700 30px Inter;fill:{INK}">Jericho ≈ −800 ft</text>'
            f'<text x="20" y="255" style="font:600 22px Inter;fill:#6B7785;letter-spacing:2px">SEA LEVEL</text></svg>')
blur_in(prof, T("jerusalem") - 0.2, 10)
tween(f"#{prof} .pr", "strokeDashoffset: 1000", 'strokeDashoffset: 0, duration: 1.4, ease: "power2.inOut"', T("going"))
tween(f"#{prof} .end, #{prof} .tj", "opacity: 0", "opacity: 1, duration: 0.3", T("jericho"))

# --- S4 · the robbers (Luke 10:30)
t4 = T("robbers") - 0.3
cam(t4, S4)
headline(S4, 300, ["Left [half dead]"], t4 + 0.1, kicker="The robbers", hl_t=T("half dead"), size=110)
sticker(S4, "blesse", 90, 560, 900, T("robbers") - 0.1, rot=-2)
tag(S4, 60, 1250, "Stripped, beaten, abandoned", T("leave"), "acc", 46)
ref(S4, 60, 1345, "Luke 10:30", T("half dead"))
hit(T("robbers"), 0.8)

# --- S5 · the priest and the Levite pass by (Luke 10:31-32)
t5 = T("priest") - 0.7
cam(t5, S5)
headline(S5, 280, ["Two men", "of the [Temple]"], t5 + 0.1, kicker="Those who pass by", hl_t=T("levite"), size=96)
sticker(S5, "pretre", 60, 590, 310, T("priest") - 0.1, rot=-2)
label_box(S5, 60, 1170, "A priest", "served at the Temple altar", T("priest") + 0.2)
sticker(S5, "levite", 540, 590, 310, T("levite") - 0.1, rot=2)
label_box(S5, 540, 1190, "A Levite", "assisted in Temple service", T("levite") + 0.2)
tag(S5, 60, 1300, "Reason: not stated", T("text"), "", 40)
ref(S5, 540, 1315, "Luke 10:31-32", T("text") + 0.2)

# --- S6 · the Samaritan (Luke 10:33; John 4:9)
t6 = T("then") - 0.2
cam(t6, S6)
headline(S6, 280, ["A [Samaritan]"], t6 + 0.1, kicker="The third man", hl_t=T("samaritan"), size=104)
sticker(S6, "samaritain-portrait", 60, 470, 500, T("samaritan") - 0.2, rot=-3)
label_box(S6, 600, 560, "Jews and Samaritans", "“have no dealings”", T("jews") - 0.1)
ref(S6, 600, 690, "John 4:9", T("jews") + 0.2)
tag(S6, 60, 1150, "Moved with compassion", T("moved"), "acc", 56)
ref(S6, 60, 1260, "Luke 10:33", T("compassion"))
hit(T("compassion"), 0.9)

# --- S7 · oil and wine (Luke 10:34)
t7 = T("treats") - 0.6
cam(t7, S7)
headline(S7, 280, ["[Oil] and wine"], t7 + 0.1, kicker="First aid", hl_t=T("oil"), size=104)
sticker(S7, "samaritain-soigne", 50, 470, 640, T("treats") - 0.2, rot=-2)
sticker(S7, "amphore-vin", 740, 440, 170, T("wine") - 0.2, rot=4)
label_box(S7, 520, 1080, "Wine amphora", "Roman, c. 100 BC", T("wine"))
ref(S7, 60, 1095, "Luke 10:34", T("wounds"))

# --- S8 · to the inn, on his own animal (Luke 10:34)
t8 = T("takes") - 0.2
cam(t8, S8)
headline(S8, 280, ["To the [inn]"], t8 + 0.1, kicker="On his own animal", hl_t=T("inn"), size=110)
sticker(S8, "auberge-bon-samaritain-aerien", 60, 590, 560, t8 + 0.15, rot=-2)
sticker(S8, "samaritain-ane", 640, 610, 300, T("takes"), rot=3)
label_box(S8, 60, 1030, "“Inn of the Good Samaritan”", "traditional site · c. 1930", T("inn"))

# --- S9 · two denarii ≈ two days' pay (Luke 10:35; Matthew 20:2)
t9 = T("pays") - 0.3
cam(t9, S9)
headline(S9, 280, ["[2 denarii]"], t9 + 0.1, kicker="The price paid", hl_t=T("denarii"), size=110)
sticker(S9, "denier-tibere", 60, 470, 380, T("denarii") - 0.2, rot=-4)
label_box(S9, 60, 860, "Denarius of Tiberius", "silver, reign AD 14–37", T("denarii") + 0.2)
sticker(S9, "main-deniers", 540, 470, 380, t9 + 0.25, rot=4)
boxes(S9, 60, 1000, ["1", "2"], T("days’ wages") - 0.1, small="Day")
ref(S9, 60, 1300, "1 denarius ≈ 1 day’s pay · Matthew 20:2", T("days’ wages") + 0.4)
hit(T("denarii"), 0.8)

# --- pull-out at the twist, then S10 · "which of the three?" (Luke 10:36)
t_all = T("then", 1) - 0.1
cam(t_all, "all")
t10 = T("around") - 0.1
cam(t10, S10)
headline(S10, 280, ["Which of the [three]?"], t10 + 0.1, kicker="Jesus turns the question", hl_t=T("neighbor", 1), size=96)
tq = T("who", 2)
for k, (name, w) in enumerate([("pretre", 250), ("levite", 250), ("samaritain-portrait", 280)]):
    sticker(S10, name, 60 + k * 310, 560, w, tq + k * 0.4, rot=(-3, 2, -2)[k])
    tag(S10, 120 + k * 310, 1100, str(k + 1), tq + k * 0.4 + 0.15, "acc" if k == 2 else "", 56)
ref(S10, 60, 1240, "Luke 10:36", tq + 1.2)

# --- S11 · dark-mode reveal: he does not say "the Samaritan" (Luke 10:37)
t11 = T("he", 2) - 0.3
cam(t11, S11)
dark_mode(t11 - 0.1)
headline(S11, 300, ["“He who showed", "[mercy] on him.”"], t11 + 0.1, kicker="The teacher’s answer", hl_t=T("mercy"), size=90, dark=True)
ref(S11, 70, 600, "Luke 10:37 · World English Bible", T("mercy") + 0.2)
sticker(S11, "docteur-portrait", 50, 730, 420, T("teacher", 1) - 0.1, rot=-3)
label_box(S11, 520, 780, "The word “Samaritan”", "in his answer", T("doesn't", 1), dark=True)
z = put(S11, 520, 880, "0", "zero")
tween(f"#{z}", "opacity: 0, scale: 2.2", 'opacity: 1, scale: 1, duration: 0.35, ease: "power4.in"', T("samaritan", 1))
tag(S11, 780, 1110, "times", T("samaritan", 1) + 0.3, "dark", 56)
hit(T("samaritan", 1), 1.0)

# --- S12 · "Go and do likewise." (captions hidden: the line is on screen)
t12 = T("jesus", 3) - 0.2
cam(t12, S12)
headline(S12, 300, ["“Go and do", "[likewise].”"], t12 + 0.1, kicker="Jesus concludes", hl_t=T("likewise"), size=110, dark=True)
ref(S12, 70, 600, "Luke 10:37", T("go"))
sticker(S12, "jesus", 520, 660, 360, t12 + 0.2, rot=2)
hit(T("likewise"), 1.0)

# --- S13 · the question to the viewer, call to comment
t13 = T("you") - 0.6
cam(t13, S13)
headline(S13, 380, ["And [you]?"], t13 + 0.1, kicker="Your turn", hl_t=T("you"), size=170, dark=True)
sticker(S13, "samaritain-ane", 560, 760, 380, t13 + 0.5, rot=3)
label_box(S13, 70, 760, "Who will you be", "a neighbor to this week?", T("will") - 0.3, dark=True)
cta = put(S13, 70, 1260, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Reply in the comments', "cta")
blur_in(cta, T("tell") - 0.2, 14)
sfx("click", T("tell") - 0.2, 0.8)

# --- end · pull out, then the end card during "subscribe"
t_end = T("subscribe") - 0.4
cam(t_end, "all")

# ================================================================ assemble
build(
    chapters=[("01", "The question", 0, t3), ("02", "The story", t3, t_all), ("03", "The twist", t_all, t13), ("04", "Lesson", t13, DUR)],
    suppress=[(T("and") - 0.1, t3), (T("who", 2) - 0.1, T("he", 2) - 0.2), (T("he", 2) - 0.1, T("teacher", 1) - 0.2),
              (T("go") - 0.1, t13), (T("subscribe") - 0.6, DUR)],
    endcard={"kicker": "Follow along", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("samaritain-portrait", 40, 1150, 330, -6), ("denier-tibere", 760, 1200, 260, 6)]},
    endcard_t=T("subscribe") + 0.1,
    music_volume=0.13,
)
