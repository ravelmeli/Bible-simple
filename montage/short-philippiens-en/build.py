"""English short « I can do all things through Christ who strengthens me » (Philippians 4:11-13) for Faith Engineering,
style 02 — 9:16, 85.6 s.

Same stations, stickers and music as montage/short-philippiens/ (French); texts translated, quotes from the World
English Bible (public domain), every beat retimed on the English transcript. The Greek word is HTML (Inter font).
Run: python3 build.py   (then npx hyperframes check and npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - Philippians 4:13 - style 02", "lang": "en"}
s.setup(here=HERE, duration=85.6, cols=3, rows=5, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)
S10, S11, S12 = (2, 3), (1, 3), (0, 3)
S13 = (0, 4)

html.append('<style>.box.wide{text-align:left;font-weight:700;line-height:1.3}'
            f'.grk{{font-weight:800;line-height:1.1;color:{THEME["bg"]};letter-spacing:-2px}}</style>')

# --- S1 · hook: the jersey is on screen from the first frame, then tattoos, game, exam
cam(0, S1)
sticker(S1, "maillot", 60, 640, 380, 0.0, rot=-4, instant=True)
headline(S1, 300, ["“I can do", "[all things]”"], 0.0, kicker="The most quoted verse", hl_t=T("things") + 0.1, size=100)
sticker(S1, "avant-bras-tatoue", 560, 640, 330, T("tattoos") - 0.2, rot=4)
tag(S1, 60, 1130, "Tattoos", T("tattoos"), "", 44)
tag(S1, 60, 1230, "Jerseys", T("jerseys"), "", 44)
tag(S1, 500, 1130, "A game", T("game"), "", 44)
tag(S1, 500, 1230, "An exam", T("exam"), "", 44)
ref(S1, 60, 1340, "Philippians 4:13 · World English Bible", T("me"))
hit(T("things"), 0.7)

# --- S2 · Paul wasn't talking about winning
t2 = T("but") - 0.4
cam(t2, S2)
headline(S2, 280, ["Paul wasn't talking", "about [winning]"], t2 + 0.1, kicker="The context", hl_t=T("winning"), size=92)
sticker(S2, "paul-pied", 80, 600, 400, t2 + 0.3, rot=-2)
tag(S2, 540, 780, "≠ a victory", T("winning") - 0.1, "acc", 56)
hit(T("winning"), 0.8)

# --- S3 · he writes from prison
t3 = T("when") - 0.3
cam(t3, S3)
headline(S3, 280, ["He writes", "in [prison]"], t3 + 0.1, kicker="Where is Paul?", hl_t=T("prison"), size=100)
sticker(S3, "paul-pied", 60, 560, 420, T("prison") - 0.4, rot=-2)
sticker(S3, "encrier-stylet-romain", 540, 640, 420, T("words") + 0.2, rot=4)
label_box(S3, 540, 1020, "Roman inkwell", "terracotta, 1st–2nd c. · The Met", T("words") + 0.5)
ref(S3, 60, 1320, "Philippians 1:7 and 1:13", T("prison"))

# --- S4 · not his first hardship: beatings, shipwrecks, hunger, cold (2 Corinthians 11:25-27)
t4 = T("hardship") - 1.5
cam(t4, S4)
headline(S4, 280, ["Not his first", "[hardship]"], t4 + 0.1, kicker="What Paul lived through", hl_t=T("hardship"), size=96)
tag(S4, 70, 620, "Beatings", T("beatings"), "", 60)
tag(S4, 70, 760, "Shipwrecks", T("shipwrecks"), "", 60)
tag(S4, 70, 900, "Hunger", T("hunger"), "acc", 60)
tag(S4, 70, 1040, "Cold", T("cold"), "acc", 60)
ref(S4, 70, 1200, "2 Corinthians 11:25-27 · WEB", T("cold") + 0.2)
hit(T("hunger"), 0.7)

# --- S5 · to the Christians in Philippi, who just sent help (Philippians 4:10, 4:18)
t5 = T("he's") - 0.3
cam(t5, S5)
headline(S5, 280, ["To the Christians", "in [Philippi]"], t5 + 0.1, kicker="The recipients", hl_t=T("philippi"), size=96)
map_svg(S5, 40, 640, "assets/map.json", T("christians") - 0.3, T("philippi"), width=580)
sticker(S5, "epaphrodite", 690, 620, 250, T("sent") - 0.3, rot=3)
label_box(S5, 60, 1070, "Epaphroditus brings the help", "Philippians 4:18", T("sent"))
tag(S5, 60, 1220, "Help sent to Paul", T("help") - 0.1, "acc", 44)
ref(S5, 60, 1320, "Map: Natural Earth", T("help"))

# --- S6 · right before: "I have learned to be content" (Philippians 4:11-12), captions hidden
t6 = T("right") - 0.4
cam(t6, S6)
headline(S6, 280, ["Right [before]", "this verse"], t6 + 0.1, kicker="Philippians 4:11-12", hl_t=T("before"), size=100)
q6 = put(S6, 60, 610, "<small>Philippians 4:11-12 · WEB</small>“I have learned to be content in whatever circumstances I am. "
         "I know how to be humbled, and I also know how to abound.”", "box wide", "width:900px;font-size:36px")
blur_in(q6, 24.8, 14)
tag(S6, 60, 1080, "Content", T("content") - 0.1, "acc", 60)
tag(S6, 60, 1200, "Humbled", T("humbled"), "", 48)
tag(S6, 500, 1200, "Abound", T("abound"), "", 48)
sticker(S6, "lettre-papyrus-grec", 720, 1000, 230, t6 + 0.6, rot=4)

# --- S7 · filled and hungry, in abundance and in need (Philippians 4:12), captions hidden
t7 = 32.5
cam(t7, S7)
headline(S7, 280, ["In any and", "all [circumstances]"], t7 + 0.1, kicker="Philippians 4:12", hl_t=T("circumstances", 1), size=96)
q7 = put(S7, 60, 610, "<small>Philippians 4:12 · WEB</small>“In any and all circumstances, I have learned the secret of being filled and of going hungry.”",
         "box wide", "width:900px;font-size:36px")
blur_in(q7, 33.0, 14)
sticker(S7, "bols", 140, 880, 640, T("filled") - 0.3, rot=-2)
tag(S7, 60, 1260, "Filled", T("filled", 1), "acc", 44)
tag(S7, 440, 1260, "Hungry", T("hungry", 1), "", 44)
tag(S7, 60, 1350, "Abundance", T("abundance"), "acc", 44)
tag(S7, 440, 1350, "Need", T("need") - 0.2, "", 44)

# --- S8 · Paul's "all things": standing firm in every situation
t8 = T("paul's") - 0.3
cam(t8, S8)
headline(S8, 280, ["Paul's", "“[all things]”"], t8 + 0.1, kicker="What “all things” means", hl_t=T("things", 1), size=100)
sticker(S8, "paul-pied", 50, 560, 400, T("means") - 0.4, rot=-2)
tag(S8, 500, 640, "Standing firm", T("standing"), "acc", 64)
tag(S8, 500, 780, "in every situation", T("situation") - 0.3, "", 40)
tag(S8, 500, 880, "even the worst", T("worst") - 0.3, "acc", 44)
hit(T("firm"), 0.9)

# --- pull-out, then S9 · dark-mode reveal: "I have learned" = "I have been initiated" (Greek)
t_all = T("here's") - 0.9
cam(t_all, "all")
t9 = T("here's") - 0.3
cam(t9, S9)
dark_mode(t9 - 0.1)
headline(S9, 280, ["“I have [learned]”"], t9 + 0.1, kicker="The surprising part · in Greek", hl_t=T("learned", 2), size=100, dark=True)
grk = put(S9, 70, 520, "μεμύημαι", "grk", "font-size:190px")
blur_in(grk, T("greek") - 0.1, 20)
label_box(S9, 70, 800, "Memyēmai", "literally: “I have been initiated”", T("initiated") - 0.2, dark=True)
tag(S9, 70, 960, "a secret you discover", T("secret", 1) - 0.2, "dark", 44)
tag(S9, 70, 1060, "by walking through hunger", T("walking") - 0.1, "acc", 44)
sticker(S9, "paul-portrait", 640, 1000, 290, T("secret", 1) - 0.2, rot=3)
hit(T("initiated"), 1.0)

# --- S10 · the next verse: Philippians 4:14, captions hidden
t10 = T("look") - 0.7
cam(t10, S10)
headline(S10, 280, ["The [next]", "verse"], t10 + 0.1, kicker="Philippians 4:14", hl_t=T("next"), size=100, dark=True)
q10 = put(S10, 60, 690, "<small>Philippians 4:14 · WEB</small>“However, you did well that you shared in my affliction.”",
          "box wide", "width:900px;font-size:36px")
blur_in(q10, 61.0, 14)
sticker(S10, "epaphrodite", 60, 980, 300, T("shared") - 0.3, rot=-3)
label_box(S10, 420, 1080, "The friends in Philippi", "they share in his affliction", T("affliction") - 0.1, dark=True)

# --- S11 · Paul thanks his friends: his strength doesn't come from himself alone
t11 = T("right", 1) - 0.3
cam(t11, S11)
headline(S11, 280, ["Paul [thanks]", "his friends"], t11 + 0.1, kicker="Right after “I can do all things”", hl_t=T("thanks"), size=100, dark=True)
sticker(S11, "paul-pied", 60, 620, 340, T("paul", 1) - 0.3, rot=-2)
sticker(S11, "epaphrodite", 540, 600, 290, T("friends") - 0.3, rot=3)
tag(S11, 60, 1200, "His strength is not his alone", T("strength") - 0.1, "acc", 38)
ref(S11, 60, 1310, "Philippians 4:13-14", T("alone"))

# --- S12 · not victory: the strength to hold on, whether you win or lose
t12 = T("victory") - 1.5
cam(t12, S12)
headline(S12, 280, ["Not [victory]"], t12 + 0.1, kicker="What the verse promises", hl_t=T("victory"), size=110, dark=True)
c1 = put(S12, 70, 560, "<small>This verse doesn't promise</small>Victory", "box", "width:880px")
c2 = put(S12, 70, 800, "<small>It promises</small>The strength to hold on", "box", "width:880px")
blur_in(c1, T("doesn't", 1) - 0.2, 14)
blur_in(c2, T("promises") - 0.2, 14)
tween(f"#{c2}", f'backgroundColor: "#FFFFFF", color: "{INK}"', f'backgroundColor: "{ACC}", color: "#FFFFFF", duration: 0.3', T("hold"))
tag(S12, 70, 1100, "You win", T("win"), "dark", 56)
tag(S12, 500, 1100, "You lose", T("lose") - 0.2, "dark", 56)
hit(T("hold"), 0.9)

# --- S13 · call to comment
t13 = 77.5
cam(t13, S13)
headline(S13, 330, ["And [you]?"], t13 + 0.1, kicker="Your turn", hl_t=78.3, size=170, dark=True)
label_box(S13, 70, 760, "In what situation", "do you need this strength?", T("situation", 1) - 0.3, dark=True)
sticker(S13, "paul-portrait", 600, 800, 340, t13 + 0.4, rot=3)
cta = put(S13, 70, 1150, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Reply in the comments', "cta")
blur_in(cta, T("tell") - 0.2, 14)
sfx("click", T("tell") - 0.2, 0.8)

# --- end · pull out, then the end card during "subscribe"
t_end = T("subscribe") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", "The verse", 0, t6), ("02", "The context", t6, t_all), ("03", "The word", t_all, t11), ("04", "Lesson", t11, DUR)],
    suppress=[(24.8, 32.4), (33.0, 38.3), (61.0, 64.0), (T("subscribe") - 0.7, DUR)],
    endcard={"kicker": "Follow along", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("paul-portrait", 30, 1150, 330, -6), ("epaphrodite", 800, 1000, 200, 5)]},
    endcard_t=T("subscribe") - 0.1,
    music_volume=0.14,
)
