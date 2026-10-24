"""English short « Noah didn't take only 2 of every animal » (Genesis 7:2) for Faith Engineering, style 02 — 9:16, 60.4 s.

Same stations, stickers and music as montage/short-noe-sept/ (French); texts translated, quote from the World English
Bible (public domain), every beat retimed on the English transcript.
Run: python3 build.py   (then npx hyperframes check and npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "Faith Engineering", "title": "Faith Engineering - Noah, seven pairs - style 02", "lang": "en"}
s.setup(here=HERE, duration=60.4, cols=3, rows=4, theme=THEME)
from style02 import *  # noqa: E402,F401,F403

S1, S2, S3 = (0, 0), (1, 0), (2, 0)
S4, S5, S6 = (2, 1), (1, 1), (0, 1)
S7, S8, S9 = (0, 2), (1, 2), (2, 2)


def tiles(station, x, y, n, t, cols=7, size=56, gap=12, step=0.09):
    """Grey cells that turn to the accent colour one by one (one cell = one animal)."""
    cells = "".join(f'<i style="width:{size}px;height:{size}px"></i>' for _ in range(n))
    i = put(station, x, y, cells, "grid", f"grid-template-columns:repeat({cols},{size}px);gap:{gap}px")
    blur_in(i, t - 0.3, 10)
    tw.append(f'tl.fromTo("#{i} i", {{ backgroundColor: "{THEME["tile"]}", scale: 0.6 }}, '
              f'{{ backgroundColor: "{ACC}", scale: 1, duration: 0.2, ease: "back.out(3)", stagger: {step} }}, {at(t)});')
    sfx("tick", t, 0.25, min(n * step + 0.2, 1.5))
    return i


# --- S1 · hook: Noah and the ark stained glass from the first frame
cam(0, S1)
sticker(S1, "noe-pied", 60, 600, 330, 0.0, rot=-3, instant=True)
headline(S1, 300, ["How many animals", "on the [ark]?"], 0.0, kicker="Explained · Genesis 6–8", hl_t=T("ark") + 0.1, size=92)
sticker(S1, "vitrail-porte-arche", 560, 620, 330, 0.8, rot=3)
label_box(S1, 440, 1290, "Stained glass, c. 1190", "God closes the door of the ark", 1.2)

# --- S2 · "two of every kind?"
t2 = T("two") - 0.3
cam(t2, S2)
headline(S2, 300, ["[Two] of every", "kind?"], t2 + 0.1, kicker="What we think", hl_t=T("two"), size=100)
sticker(S2, "moutons", 140, 620, 640, t2 + 0.2, rot=-2)
tag(S2, 60, 1250, "Not quite", T("not") - 0.1, "acc", 60)
hit(T("not"), 0.8)

# --- S3 · Genesis 6: two of every kind, a male and a female
t3 = T("in") - 0.3
cam(t3, S3)
headline(S3, 280, ["Genesis 6:", "[2] per kind"], t3 + 0.1, kicker="First command", hl_t=T("two", 1), size=100)
sticker(S3, "colombe-1", 60, 560, 420, T("two", 1) - 0.2, rot=-4)
sticker(S3, "colombe-2", 540, 560, 420, T("two", 1) + 0.1, rot=4)
label_box(S3, 60, 1050, "A male", "", T("male") - 0.1)
label_box(S3, 540, 1050, "a female", "", T("female") - 0.1)
ref(S3, 60, 1180, "Genesis 6:19", T("female"))

# --- S4 · Genesis 7: seven pairs of clean animals, one pair of unclean animals (infographic)
t4 = T("but") - 0.3
cam(t4, S4)
headline(S4, 280, ["Genesis 7:", "[7 pairs]"], t4 + 0.1, kicker="The detail", hl_t=T("seven"), size=100)
sticker(S4, "moutons", 50, 600, 300, T("clean") - 0.4, rot=-3)
label_box(S4, 390, 600, "Clean animals", "7 pairs, male and female", T("clean") - 0.2)
tiles(S4, 390, 720, 14, T("seven"))
sticker(S4, "chameaux", 50, 960, 300, T("two", 2) - 0.6, rot=3)
label_box(S4, 390, 960, "Unclean animals", "only one pair", T("two", 2) - 0.4)
tiles(S4, 390, 1080, 2, T("two", 2))
ref(S4, 60, 1320, "Genesis 7:2 · World English Bible", T("“you"))
hit(T("seven"), 0.8)

# --- S5 · why? Noah offers sacrifices of clean animals (Genesis 8:20)
t5 = T("why") - 0.3
cam(t5, S5)
headline(S5, 280, ["Why more", "[clean] animals?"], t5 + 0.1, kicker="The clue", hl_t=T("clean", 2), size=96)
sticker(S5, "plat-sacrifice-noe", 50, 560, 520, T("clue") - 0.2, rot=-3)
label_box(S5, 50, 1100, "Noah's sacrifice", "Italian plate, c. 1600 · The Met", T("sacrifices") - 0.2)
sticker(S5, "autel-priere", 600, 620, 400, T("sacrifices") - 0.4, rot=3)
ref(S5, 600, 1000, "Genesis 8:20", T("sacrifices"))
tag(S5, 50, 1250, "One pair only = species lost", T("only") - 0.1, "acc", 44)

# --- S6 · before the Law of Moses, clean / unclean already exists (Leviticus 11)
t6 = T("here's") - 0.3
cam(t6, S6)
headline(S6, 280, ["Before the [Law]", "of Moses"], t6 + 0.1, kicker="The surprising part", hl_t=T("law"), size=100)
sx6, sy6 = st(*S6)
tl6 = uid()
html.append(f'<svg class="node lead" id="{tl6}" style="left:{sx6}px;top:{sy6}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<path d="M140 620 L860 620" stroke-dasharray="730" style="stroke-width:6"/>'
            f'<circle cx="140" cy="620" r="14" style="fill:{ACC}"/><circle class="e" cx="860" cy="620" r="14" style="fill:{INK}"/></svg>')
tween(f"#{tl6} path", "strokeDashoffset: 730", 'strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut"', T("moses") - 0.2)
label_box(S6, 60, 660, "Noah", "Genesis 7", T("law") - 0.1)
label_box(S6, 620, 660, "Law of Moses", "Leviticus 11", T("moses"))
sticker(S6, "chameau-terre-cuite", 80, 820, 360, T("difference") - 0.3, rot=-3)
label_box(S6, 470, 900, "Camel: unclean", "Leviticus 11:4", T("unclean"))
label_box(S6, 470, 1010, "Terracotta figurine", "Roman Egypt, 2nd–3rd c. · The Met", T("unclean") + 0.3)
tag(S6, 60, 1250, "Clean / unclean: already there", T("already") - 0.2, "acc", 46)

# --- pull-out, then S7 · dark-mode reveal: the Hebrew says "seven, seven"
t_all = T("hebrew") - 0.9
cam(t_all, "all")
t7 = T("hebrew") + 0.1
cam(t7, S7)
dark_mode(t7 - 0.1)
headline(S7, 300, ["“Seven, [seven]”"], t7 + 0.1, kicker="In Hebrew · shiv'ah shiv'ah", hl_t=T("“seven, seven.”"), size=120, dark=True)
b1 = put(S7, 70, 640, "<small>World English Bible</small>7 pairs", "box out", "width:430px;font-size:60px")
b2 = put(S7, 560, 640, "<small>Other versions</small>7 animals", "box out", "width:430px;font-size:60px")
blur_in(b1, T("pairs", 1) - 0.2, 14)
blur_in(b2, T("pairs", 1) + 0.9, 14)
label_box(S7, 70, 900, "Translators disagree", "the Hebrew allows both readings", T("translators") - 0.1, dark=True)
hit(T("“seven, seven.”"), 1.0)

# --- S8 · two readings among scholars
t8 = T("some") - 0.3
cam(t8, S8)
headline(S8, 300, ["Two [readings]"], t8 + 0.1, kicker="Among scholars", hl_t=T("stories"), size=110, dark=True)
c1 = put(S8, 70, 560, "<small>Hypothesis</small>Two stories woven", "box", "width:430px")
c2 = put(S8, 560, 560, "<small>Plain reading</small>A rule, then a detail", "box", "width:430px")
blur_in(c1, T("stories") - 0.2, 14)
blur_in(c2, T("rule") - 0.2, 14)
sticker(S8, "tablette-atra-hasis", 120, 860, 300, T("detail") - 0.6, rot=-3)
label_box(S8, 460, 920, "The Flood, also in Babylon", "Atra-hasis tablet · The Met", T("detail") - 0.4, dark=True)

# --- S9 · call to comment
t9 = T("did", 1) - 0.3
cam(t9, S9)
headline(S9, 300, ["Did you [know]?"], t9 + 0.1, kicker="Your turn", hl_t=T("know"), size=120, dark=True)
sticker(S9, "noe-portrait", 520, 600, 440, t9 + 0.2, rot=3)
cta = put(S9, 70, 1150, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Reply in the comments', "cta")
blur_in(cta, T("tell") - 0.2, 14)
sfx("click", T("tell") - 0.2, 0.8)

# --- end · pull out, then the end card during "subscribe"
t_end = T("subscribe") - 0.6
cam(t_end, "all")

build(
    chapters=[("01", "The question", 0, t3), ("02", "The text", t3, t5), ("03", "The reason", t5, t_all), ("04", "The Hebrew", t_all, DUR)],
    suppress=[(T("subscribe") - 0.7, DUR)],
    endcard={"kicker": "Follow along", "title": "Faith<br />[Engineering]", "button": "Subscribe",
             "stickers": [("moutons", 30, 1180, 380, -6), ("noe-pied", 800, 1040, 220, 5)]},
    endcard_t=T("subscribe") - 0.1,
)
