"""English short « Amen comes from a word that means solid » for Faith Engineering, style 02 — 9:16, 80.4 s.

Same stations, stickers and music as montage/short-amen/ (French); texts translated, quotes from the World English
Bible (public domain), every beat retimed on the English transcript. The Hebrew word is HTML (Noto Sans Hebrew, OFL).
Run: python3 build.py   (then npx hyperframes check and npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - Amen - style 02", "lang": "en"}
s.setup(here=HERE, duration=80.4, cols=3, rows=5, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10, S11, S12 = (2, 3), (1, 3), (0, 3)
S13 = (0, 4)

html.append('<style>@font-face{font-family:"Noto Sans Hebrew";src:url("assets/fonts/NotoSansHebrew.ttf") format("truetype");font-weight:100 900}'
            f'.heb{{font-family:"Noto Sans Hebrew",sans-serif;direction:rtl;font-weight:700;line-height:1.1;color:{INK}}}'
            '.box.wide{width:560px;text-align:left;font-size:36px}</style>')

# --- S1 · hook: the crowd with raised hands from the first frame
cam(0, S1)
sticker(S1, "foule-mains-levees", 60, 560, 600, 0.0, rot=-2, instant=True)
headline(S1, 300, ["You say it", "every [week]"], 0.0, kicker="A word from the Bible", hl_t=T("week") + 0.1, size=100)
tag(S1, 60, 1230, "Amen", T("amen.") - 0.1, "acc", 110)
hit(T("amen."), 0.9)

# --- S2 · "so be it"? In Hebrew: a root meaning solid, firm, reliable
t2 = T("it's") - 0.3
cam(t2, S2)
headline(S2, 280, ["“So be it”?"], t2 + 0.1, kicker="The usual translation", size=96)
heb = put(S2, 300, 440, "אָמֵן", "heb", "font-size:230px")
blur_in(heb, T("hebrew") - 0.1, 20)
label_box(S2, 60, 760, "Hebrew root", "“to be firm, stable, reliable”", T("root") - 0.1)
tag(S2, 60, 920, "solid", T("solid") - 0.05, "acc", 60)
tag(S2, 60, 1040, "firm", T("firm") - 0.05, "acc", 60)
tag(S2, 60, 1160, "reliable", T("reliable") - 0.05, "acc", 60)

# --- S3 · the same root gives "faith" and "truth"
t3 = T("the") - 0.3
cam(t3, S3)
headline(S3, 280, ["Same root:", "[faith] and truth"], t3 + 0.1, kicker="The word family", hl_t=T("faith"), size=96)
sticker(S3, "bible-hebraique-espagne", 70, 560, 900, t3 + 0.2, rot=-2)
label_box(S3, 70, 1170, "Hebrew Bible", "Spain, 1300–1350 · The Met", t3 + 0.6)

# --- S4 · Exodus 17:12: his hands were steady
t4 = T("in", 1) - 0.3
cam(t4, S4)
headline(S4, 280, ["Steady", "[hands]"], t4 + 0.1, kicker="Exodus 17", hl_t=T("steady"), size=100)
sticker(S4, "moise-aaron-hur", 50, 560, 520, T("moses") - 0.2, rot=-2)
label_box(S4, 620, 600, "Aaron and Hur", "hold up his hands", T("aaron"))
sticker(S4, "moise-portrait", 640, 760, 320, T("steady") - 0.3, rot=3)
tag(S4, 50, 1200, "“his hands were steady”", T("steady") - 0.1, "acc", 42)
ref(S4, 50, 1290, "Exodus 17:12 · World English Bible", T("steady"))
hit(T("steady"), 0.8)

# --- S5 · Isaiah 7:9: believing ≈ standing firm (captions hidden during the on-screen quote)
t5 = T("prophet") - 0.6
cam(t5, S5)
headline(S5, 280, ["Believe = [stand]", "firm"], t5 + 0.1, kicker="Isaiah 7:9", hl_t=T("standing"), size=96)
sticker(S5, "vitrail-esaie", 50, 580, 300, T("isaiah") - 0.2, rot=-3)
label_box(S5, 400, 580, "The prophet Isaiah", "stained glass, c. 1325 · The Met", T("isaiah"))
q5 = put(S5, 400, 720, "<small>Isaiah 7:9 · WEB</small>“If you will not believe, surely you shall not be established.”", "box wide")
blur_in(q5, T("“if") - 0.1, 14)
tag(S5, 400, 1080, "believe ≈ stand firm", T("believing") - 0.1, "acc", 46)
label_box(S5, 400, 1190, "In Hebrew", "two forms of the same root", T("same", 1))

# --- S6 · Nehemiah 8:6: the people answer "Amen! Amen!"
t6 = T("when") - 0.3
cam(t6, S6)
headline(S6, 280, ["“Amen! [Amen]!”"], t6 + 0.1, kicker="Nehemiah 8:6", hl_t=T("amen", 3), size=110)
sticker(S6, "esdras", 50, 470, 360, T("ezra") - 0.2, rot=-2)
sticker(S6, "foule-mains-levees", 440, 560, 560, T("people") - 0.2, rot=3)
label_box(S6, 50, 1200, "Ezra reads the Law", "all the people answer, hands raised", T("law") - 0.1)
ref(S6, 620, 1215, "Nehemiah 8:6 · WEB", T("amen", 2))
hit(T("amen", 2), 0.8)

# --- S7 · saying amen: "this is solid, I'm leaning on it"
t7 = T("saying") - 0.4
cam(t7, S7)
headline(S7, 280, ["“I'm [leaning]", "on it”"], t7 + 0.1, kicker="The real meaning", hl_t=T("leaning"), size=96)
sticker(S7, "rocher", 50, 560, 440, t7 + 0.2, rot=-3)
sticker(S7, "main-rocher", 540, 540, 440, T("leaning") - 0.2, rot=3)
tag(S7, 50, 1080, "≠ just a wish", T("wish") - 0.2, "", 50)
tag(S7, 50, 1190, "= this is solid", T("solid", 1) - 0.1, "acc", 60)

# --- pull-out at the surprising part, then S8 · Jesus puts it at the beginning
t_all = T("here's") - 0.2
cam(t_all, "all")
t8 = T("uses") - 0.4
cam(t8, S8)
headline(S8, 280, ["Jesus says it", "[backwards]"], t8 + 0.1, kicker="The surprising part", hl_t=T("backwards"), size=96)
sticker(S8, "jesus", 50, 570, 340, t8 + 0.2, rot=-2)
c1 = put(S8, 430, 600, "<small>Usually</small>… at the end: “Amen.”", "box wide")
c2 = put(S8, 430, 820, "<small>Jesus</small>“Amen, I tell you…”", "box wide")
blur_in(c1, T("end") - 0.2, 14)
blur_in(c2, T("beginning") - 0.1, 14)
tween(f"#{c2}", f'backgroundColor: "#FFFFFF", color: "{INK}"', f'backgroundColor: "{ACC}", color: "#FFFFFF", duration: 0.3', T("amen", 5))
hit(T("beginning"), 0.8)

# --- S9 · "Truly, I tell you" (captions hidden during the on-screen quote)
t9 = T("our") - 0.3
cam(t9, S9)
headline(S9, 280, ["“[Truly],", "I tell you”"], t9 + 0.1, kicker="Our Bibles translate", hl_t=T("“truly"), size=100)
sticker(S9, "evangeliaire-carolingien", 90, 560, 860, t9 + 0.2, rot=-2)
label_box(S9, 70, 1260, "Latin Gospel book", "c. 825–850 · The Met", t9 + 0.6)
ref(S9, 70, 1350, "WEB: “Most certainly I tell you”", t9 + 0.8)

# --- S10 · dark-mode reveal: Jesus called "the Amen" (Revelation 3:14)
t10 = T("revelation") - 0.7
cam(t10, S10)
dark_mode(t10 - 0.1)
headline(S10, 280, ["Jesus,", "[the Amen]"], t10 + 0.1, kicker="Revelation 3:14", hl_t=T("amen", 6), size=110, dark=True)
sticker(S10, "jean-patmos", 50, 560, 320, t10 + 0.2, rot=-3)
q10 = put(S10, 410, 620, "<small>Revelation 3:14 · WEB</small>“the Amen, the Faithful and True Witness”", "box wide")
blur_in(q10, T("amen", 6) - 0.2, 14)
label_box(S10, 410, 900, "John on Patmos", "author of Revelation by tradition", T("witness"), dark=True)
hit(T("amen", 6), 1.0)

# --- S11 · a word passed unchanged into other languages
t11 = T("word", 1) - 0.5
cam(t11, S11)
headline(S11, 280, ["Passed on", "[unchanged]"], t11 + 0.1, kicker="Into other languages", hl_t=T("unchanged"), size=100, dark=True)
tag(S11, 70, 600, "Greek", T("greek"), "acc", 64)
tag(S11, 70, 720, "Latin", T("latin"), "acc", 64)
tag(S11, 70, 840, "Arabic", T("arabic"), "acc", 64)
tag(S11, 70, 960, "… and many more", T("languages") - 0.2, "dark", 56)
heb11 = put(S11, 560, 640, "אָמֵן", "heb", f"font-size:200px;color:{THEME['bg']}")
blur_in(heb11, t11 + 0.3, 20)

# --- S12 · remember: amen = "this is solid"
t12 = T("next") - 0.6
cam(t12, S12)
headline(S12, 280, ["Amen =", "“this is [solid]”"], t12 + 0.1, kicker="Remember", hl_t=T("solid", 2), size=96, dark=True)
sticker(S12, "main-rocher", 280, 640, 520, t12 + 0.2, rot=-2)
hit(T("solid", 2), 0.7)

# --- S13 · call to comment
t13 = T("which") - 0.3
cam(t13, S13)
headline(S13, 300, ["Which [word]", "next?"], t13 + 0.1, kicker="Your turn", hl_t=T("word", 2), size=120, dark=True)
sticker(S13, "moise-portrait", 560, 700, 400, t13 + 0.3, rot=3)
cta = put(S13, 70, 1150, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Reply in the comments', "cta")
blur_in(cta, T("tell") - 0.2, 14)
sfx("click", T("tell") - 0.2, 0.8)

# --- end · pull out, then the end card during "subscribe"
t_end = T("subscribe") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", "The word", 0, t4), ("02", "The root", t4, t_all), ("03", "Jesus", t_all, t11), ("04", "Lesson", t11, DUR)],
    suppress=[(T("“if") - 0.1, T("in", 2) - 0.1), (T("“truly") - 0.2, T("revelation") - 0.8), (T("subscribe") - 0.7, DUR)],
    endcard={"kicker": "Follow along", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("main-rocher", 30, 1180, 360, -6), ("moise-aaron-hur", 760, 1060, 280, 5)]},
    endcard_t=T("subscribe") - 0.1,
    music_volume=0.14,
)
