"""Video lunga « Ruach : la parola ebraica per «spirito» che significa anche «vento» e «soffio» » (La Bibbia Semplice) — style 02, 16:9, 398.4 s. Versione italiana di montage/video-ruach-en/.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py), option retention, thème beige.
Règles de mise en page (contrôlées par kit-style-02/outils/audit_chevauchements.js après chaque build) :
  - contenu à partir de y = 420 (sous le titre), colonne gauche x = 90, colonne droite x >= 1100, autocollants hauts à x = 1500 ;
  - une citation occupe sa zone seule : tout ce qui s'y trouvait disparaît avant, elle disparaît à la fin de la ligne ;
  - le contenu s'arrête avant les sous-titres (bas d'écran).
Les mots grecs (synteleia tou aiônos, apokalypsis, parousia) sont écrits en HTML : à faire relire avant publication.
Lancer : python3 build.py ; node ../../kit-style-02/outils/audit_chevauchements.js . ; npx hyperframes check
"""
import difflib
import json
import os
import re
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "La Bibbia Semplice", "title": "La Bibbia Semplice - Ruach, vento, soffio e spirito - style 02", "lang": "it",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
DUR_ = 398.4
s.setup(here=HERE, duration=DUR_, cols=5, rows=4, fmt="16:9", theme=THEME, bpm=96, zoom=1.15, xmap=(190, 0.8539), ymap=(208, 0.85))
from style02 import *  # noqa: E402,F401,F403
import style02  # noqa: E402

MANQUES = []
SUPP = []


def _norm(t):
    return re.sub(r"[^\wà-ÿ]", "", t.lower().replace("’", "").replace("'", ""))


_lines = [l for l in open(os.path.join(HERE, "script.md")).read().split("\n") if l.strip()]
_idx = [i for i, x in enumerate(style02.words) if _norm(x["text"])]
_tw = [_norm(style02.words[i]["text"]) for i in _idx]
_sw, _ls = [], []
for _L, _l in enumerate(_lines):
    for _t in _l.split():
        if _norm(_t):
            _sw.append(_norm(_t))
            _ls.append(_L + 1)
_map = {}
for _tag, _i1, _i2, _j1, _j2 in difflib.SequenceMatcher(None, _sw, _tw, autojunk=False).get_opcodes():
    if _tag == "equal":
        for _k in range(_i2 - _i1):
            _map[_i1 + _k] = _j1 + _k
LS = {}
for _si, _L in enumerate(_ls):
    if _L not in LS and _si in _map:
        LS[_L] = style02.words[_idx[_map[_si]]]["start"]
for _L in range(1, len(_lines) + 2):
    if _L not in LS:
        LS[_L] = LS.get(_L - 1, 0.0) + 2.0
LS[len(_lines) + 1] = DUR_


def A(word, after=0.0, n=0):
    keys = {style02.norm(pre + word) for pre in ("", "l", "d", "j", "n", "s", "qu", "c", "m", "t", "dell", "nell", "all", "dall", "sull", "un", "v", "quest", "nel")}
    hits = sorted(w["start"] for w in style02.words if style02.norm(w["text"]) in keys and w["start"] >= after - 0.01)
    if len(hits) > n:
        return hits[n]
    MANQUES.append((word, after, n))
    return max(after, 1.0) + 0.5


def AL(word, line, n=0):
    return A(word, LS[line] - 0.05, n)


def FW(name, w, maxh=385):
    """Largeur d'un autocollant limitée pour que sa hauteur (px de conception) ne dépasse pas maxh."""
    iw, ih = Image.open(os.path.join(HERE, "assets/stickers", name + ".png")).size
    return round(min(w, maxh * iw / ih))


def S_(station, name, x, y, w, t, **kw):
    i, h = sticker(station, name, x, y, FW(name, w), t, **kw)
    return i


def kq(station, x, y, ref_txt, text, line, first, width=1000, size=34, last=None, fade_at=None, n=0):
    t0 = AL(first, line, n) - 0.05
    t1 = (LS[line + 1] - 0.25) if last is None else last
    SUPP.append((t0 - 0.1, t1 + 0.2))
    i = kinetic_quote(station, x, y, ref_txt, text, t0, t1, width=width, size=size)
    fade(i, (LS[line + 1] - 0.4) if fade_at is None else fade_at)
    return i


def gone(ids, t):
    for _i in ids:
        fade(_i, t)


def card(station, x, y, small, body, t, w=800, size=38, accent=False):
    c = put(station, x, y, f"<small>{small}</small>{body}", "card", f"width:{w}px;font-size:{size}px" + (f";border-color:{ACC}" if accent else ""))
    blur_in(c, t, 14)
    return c


def grab(station, fn):
    n0 = len(style02.NODES.get(station, []))
    fn()
    return list(style02.NODES[station][n0:])


HOREB, TROIS, HOREB2, EXODE, SOUFFLE = (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)
NESHAMAH, ESPRIT, EZECHIEL, NT, ATTENTION = (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)
APPLI = (0, 2)
RIV = " · Riveduta"

html.append('<style>'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

# OREB (righe 1-5)
cam(0, HOREB)
S_(HOREB, "elie", 1500, 400, 230, 0.0, rot=-3, instant=True)
S_(HOREB, "montagne", 1060, 420, 340, AL("monte", 1) - 0.2, rot=2)
headline(HOREB, 170, ["Sul monte [Oreb]"], 0.0, kicker="1 Re 19", hl_t=AL("oreb", 1) + 0.05, size=92)
hb = [tag(HOREB, 90, 420, "Un vento", AL("vento", 2) - 0.1, "", 50),
      tag(HOREB, 90, 525, "Un terremoto", AL("terremoto", 2) - 0.1, "", 50),
      tag(HOREB, 90, 630, "Un fuoco", AL("fuoco", 2) - 0.1, "", 50)]
wind(HOREB, 600, 410, AL("vento", 2) - 0.2, size=380, dur=4.0)
hb.append(S_(HOREB, "rocher", 600, 670, 190, AL("terremoto", 2) - 0.2, rot=-3))
hb.append(S_(HOREB, "flamme", 845, 640, 170, AL("fuoco", 2) - 0.2, rot=3))
burst(HOREB, 1100, 600, AL("vento", 2) + 0.1)
gone(hb, AL("tre", 3) - 0.4)
stm = stamp(HOREB, 90, 480, "Non era lì", AL("tre", 3) + 0.2, rot=-4, size=72)
fade(stm, AL("eppure", 4) - 0.5)
th = teaser(HOREB, 90, 780, "Una parola, tre significati", AL("eppure", 4) - 0.2, hold=3.2)
tw_ = tag(HOREB, 90, 420, "vento = spirito", AL("spirito", 4) - 0.2, "acc", 50)
fade(tw_, AL("ruach", 5) - 0.5)
fade(th, AL("ruach", 5) - 0.5)
r0 = put(HOREB, 90, 540, "ruach", "word", "font-size:190px")
blur_in(r0, AL("ruach", 5) - 0.1, 20)
hit(AL("ruach", 5), 1.0)

# TRE PAROLE (righe 6-9)
t = LS[6] - 0.4
cam(t, TROIS)
headline(TROIS, 170, ["Tre parole per [una]"], t + 0.1, kicker="Ruach", hl_t=AL("ebraica", 6) + 0.05, size=96)
S_(TROIS, "bible-hebraique", 1100, 420, 480, AL("ebraica", 6) - 0.3, rot=-2)
t3 = [tag(TROIS, 90, 420, "Il vento", AL("vento", 6) - 0.1, "", 52),
      tag(TROIS, 90, 525, "Il soffio", AL("soffio", 6) - 0.1, "", 52),
      tag(TROIS, 90, 630, "Lo spirito", AL("spirito", 6) - 0.1, "acc", 52)]
t3.append(S_(TROIS, "souffle", 760, 420, 165, AL("soffio", 6) - 0.1, rot=2))
lat = [tag(TROIS, 90, 765, "Latino: spiritus = soffio", AL("latino", 7) - 0.2, "", 38),
       tag(TROIS, 790, 765, "Greco: pneuma", AL("pneuma", 7) - 0.3, "acc", 38)]
gone(t3 + lat, AL("perché", 8) - 0.5)
stamp(TROIS, 90, 450, "Confusione ?", AL("confusione", 8) - 0.2, rot=-4, size=64)
arrow(TROIS, (700, 520), (1030, 560), AL("messaggio", 8))
burst(TROIS, 1350, 600, AL("messaggio", 8) + 0.1)

# OREB, lettura (righe 10-13)
t = LS[10] - 0.4
cam(t, HOREB2)
headline(HOREB2, 170, ["La scena dell'[Oreb]"], t + 0.1, kicker="1 Re 19.11", hl_t=AL("scena", 10) + 0.05, size=96)
h10 = [tag(HOREB2, 90, 430, "1 Re, capitolo 19", LS[10] + 0.4, "acc", 56),
       S_(HOREB2, "montagne", 1100, 420, 360, AL("scena", 10) + 0.2, rot=2)]
gone(h10, AL("ed", 11) - 0.45)
kq(HOREB2, 90, 420, "1 Re 19.11-12" + RIV,
   "«Ed ecco passare l'Eterno. Un vento forte e impetuoso spaccava i monti e spezzava le rocce davanti all'Eterno; ma l'Eterno non era nel vento. "
   "E, dopo il vento, un terremoto; ma l'Eterno non era nel terremoto.»", 11, "ed", width=900, size=34)
S_(HOREB2, "elie-portrait", 1500, 410, 250, AL("ed", 11) + 0.2, rot=3)
wind(HOREB2, 1150, 440, AL("vento", 11) - 0.2, size=300, dur=5.0)
S_(HOREB2, "rocher", 1180, 660, 170, AL("rocce", 11), rot=3)
stamp(HOREB2, 90, 450, "1 · Il vento", AL("primo", 12) + 0.2, rot=-4, size=56)
tag(HOREB2, 90, 590, "Primo significato: il vento", AL("primo", 12) - 0.2, "acc", 52)
tag(HOREB2, 90, 710, "Un vento vero, una forza della natura", AL("vero", 12) - 0.1, "", 42)
burst(HOREB2, 1550, 600, AL("dio", 13) + 0.1)

# ESODO (righe 14-16)
t = LS[14] - 0.4
cam(t, EXODE)
headline(EXODE, 170, ["Il vento [orientale]"], t + 0.1, kicker="Esodo 14.21", hl_t=AL("orientale", 14) + 0.05, size=100)
S_(EXODE, "moise", 110, 410, 270, AL("mare", 14) - 0.3, rot=-2)
wind(EXODE, 1560, 420, AL("vento", 14) - 0.3, size=300, dur=7.0)
kq(EXODE, 560, 420, "Esodo 14.21" + RIV, "«l'Eterno fece ritirare il mare per mezzo di un forte vento orientale durato tutta la notte»",
   14, "eterno", width=800, size=34, last=AL("notte", 14) + 0.5, fade_at=LS[15] - 0.4)
fw = tag(EXODE, 560, 440, "I quattro venti", AL("quattro", 15) - 0.3, "acc", 56)
ring(EXODE, 1000, 540, AL("quattro", 15), size=240)
fade(fw, AL("primo", 16) - 0.5)
stamp(EXODE, 560, 440, "1 · Il vento", AL("primo", 16) + 0.1, rot=-4, size=52)
tag(EXODE, 560, 590, "Una forza invisibile, dagli effetti visibili", AL("effetti", 16) - 0.9, "", 38)

# SOFFIO (righe 17-20)
t = LS[17] - 0.4
cam(t, SOUFFLE)
headline(SOUFFLE, 170, ["Il [soffio]"], t + 0.1, kicker="2 · Secondo significato", hl_t=AL("soffio", 18) + 0.05, size=110)
glow(SOUFFLE, 1620, 600, t + 0.5, size=320, dur=6.0)
S_(SOUFFLE, "lampe", 1500, 480, 220, t + 0.5, rot=-3)
ts_ = tag(SOUFFLE, 90, 430, "Resta ancora un po'", AL("resta", 17) - 0.3, "", 44)
fade(ts_, AL("secondo", 18) - 0.5)
sb = [S_(SOUFFLE, "souffle", 90, 420, 230, AL("secondo", 18) - 0.1, rot=2)]
breath(SOUFFLE, 340, 480, AL("secondo", 18), size=420, dur=5.0)
ring(SOUFFLE, 215, 540, AL("secondo", 18), size=260)
sb.append(S_(SOUFFLE, "shofar-grave", 800, 420, 520, AL("soffio", 18) + 0.4, rot=-3))
sb.append(label_box(SOUFFLE, 800, 690, "Uno shofar", "corno di montone, XVIII sec. · The Met", AL("salmo", 19) - 1.6))
gone(sb, AL("salmo", 19) - 0.5)
kq(SOUFFLE, 90, 420, "Salmo 104.29-30" + RIV,
   "«Tu ritiri il loro fiato, essi muoiono e ritornano nella loro polvere. Tu mandi il tuo spirito, e sono creati, e tu rinnovi la faccia della terra.»",
   19, "tu", width=1000, size=34)
tag(SOUFFLE, 90, 430, "Il soffio di vita", AL("ruach", 20) - 0.3, "acc", 56)
tag(SOUFFLE, 90, 550, "Se ne va: la vita si ferma", AL("ferma", 20) - 0.5, "", 44)
tag(SOUFFLE, 90, 660, "Viene mandato: la vita ricomincia", AL("ricomincia", 20) - 0.5, "", 42)

# NESHAMAH (righe 21-24)
t = LS[21] - 0.4
cam(t, NESHAMAH)
headline(NESHAMAH, 170, ["Un'altra parola: [neshamah]"], t + 0.1, kicker="Genesi 2.7", hl_t=AL("neshamah", 21) + 0.05, size=88)
nz = []
d21 = tag(NESHAMAH, 90, 420, "Un dettaglio da conoscere", LS[21] + 0.4, "acc", 52)
fade(d21, AL("soffio", 21) - 0.6)
c1 = put(NESHAMAH, 90, 420, "<small>Genesi 2.7</small>un «soffio di vita»: <b>neshamah</b>", "card", "width:700px;font-size:36px")
blur_in(c1, AL("soffio", 21) - 0.3, 14)
c2 = put(NESHAMAH, 1000, 420, "<small>Più spesso</small><b>ruach</b>: movimento e forza", "card", "width:700px;font-size:36px;border-color:" + ACC)
blur_in(c2, AL("ruach", 22) - 0.4, 14)
nz += [c1, c2]
nz.append(S_(NESHAMAH, "bible-hebraique", 90, 620, 380, AL("genesi", 21) - 0.2, rot=-2))
sbn = S_(NESHAMAH, "sym-balance", 610, 620, 190, AL("vicine", 22) - 0.2, rot=0)
animate(sbn, "rock", AL("vicine", 22) - 0.2, dur=6.0)
nz.append(sbn)
nz.append(tag(NESHAMAH, 1000, 640, "Vicine, non intercambiabili", AL("intercambiabili", 22) - 0.6, "acc", 40))
gone(nz, AL("ecclesiaste", 23) - 0.4)
kq(NESHAMAH, 90, 420, "Ecclesiaste 12.7" + RIV,
   "«la polvere torni alla terra, com'era prima, e lo spirito torni a Dio che l'ha dato»", 23, "la", width=1000, size=40,
   last=AL("dato", 23) + 0.6, fade_at=LS[24] - 0.4)
stamp(NESHAMAH, 90, 470, "3 · Lo spirito", AL("terzo", 24) + 0.1, rot=-4, size=64)

# SPIRITO (righe 25-29)
t = LS[25] - 0.4
cam(t, ESPRIT)
headline(ESPRIT, 170, ["Lo [spirito]"], t + 0.1, kicker="3 · Terzo significato", hl_t=AL("spirito", 25) + 0.05, size=110)
S_(ESPRIT, "rouleau", 1500, 420, 260, t + 0.5, rot=3)
kq(ESPRIT, 90, 420, "Genesi 1.2" + RIV, "«lo Spirito di Dio aleggiava sulla superficie delle acque»", 26, "lo", width=900, size=44,
   last=AL("acque", 26) + 0.6, fade_at=LS[27] - 0.4)
wind(ESPRIT, 1180, 440, AL("secondo", 26) - 0.2, size=300, dur=5.0)
ta_ = tag(ESPRIT, 90, 580, "I traduttori non sono d'accordo", AL("onesti", 27) - 0.2, "acc", 42)
cA = put(ESPRIT, 90, 420, "«lo Spirito di Dio»", "card", "width:520px;font-size:34px")
cB = put(ESPRIT, 700, 420, "«un vento di Dio»", "card", "width:520px;font-size:34px")
blur_in(cA, AL("alcuni", 27) - 0.2, 14)
blur_in(cB, AL("altri", 27) - 0.2, 14)
gone([cA, cB, ta_], LS[28] - 0.5)
jc = S_(ESPRIT, "jacob", 860, 400, 230, AL("giacobbe", 28) - 0.3, rot=-3)
tj = tag(ESPRIT, 90, 440, "Lo spirito di Giacobbe si ravvivò", AL("ravvivò", 28) - 0.8, "", 36)
ring(ESPRIT, 975, 560, AL("giacobbe", 28), size=260)
gone([jc, tj], AL("salmo", 29) - 0.5)
kq(ESPRIT, 90, 420, "Salmo 34.18" + RIV,
   "«L'Eterno è vicino a quelli che hanno il cuore afflitto, e salva quelli che hanno lo spirito abbattuto.»", 29, "eterno", width=1000, size=40,
   fade_at=LS[30] - 0.4)

# EZECHIELE (righe 30-35)
t = LS[30] - 0.5
cam(t, EZECHIEL)
headline(EZECHIEL, 170, ["La valle di [Ezechiele]"], t + 0.1, kicker="Ezechiele 37", hl_t=AL("valle", 31) + 0.05, size=92)
t30 = tag(EZECHIEL, 920, 420, "vento · soffio · spirito", LS[30] + 0.3, "acc", 56)
fade(t30, AL("profeta", 31) - 0.5)
S_(EZECHIEL, "ossements", 90, 420, 430, AL("valle", 30) - 0.2, rot=-2)
S_(EZECHIEL, "ezechiel", 640, 410, 200, AL("profeta", 31) - 0.2, rot=3)
kq(EZECHIEL, 920, 420, "Ezechiele 37.9" + RIV,
   "«Profetizza allo spirito, profetizza, figliuol d'uomo, e di' allo spirito: Così dice il Signore, l'Eterno: Vieni dai quattro venti, o spirito, "
   "soffia su questi uccisi, e fa' che rivivano!»", 32, "profetizza", width=800, size=32, fade_at=LS[33] - 0.5)
ezw = []
for k_, lab in enumerate(["vento", "soffio", "spirito"]):
    rid = put(EZECHIEL, 920 + k_ * 270, 420, "ruach", "word", "font-size:80px")
    blur_in(rid, AL("ruach", 33) + k_ * 0.9, 14)
    ezw.append(rid)
    ezw.append(tag(EZECHIEL, 920 + k_ * 270, 560, lab, AL("ruach", 33) + 0.5 + k_ * 0.9, "acc" if k_ == 2 else "", 40))
gone(ezw, AL("casa", 34) - 0.5)
tm = [tag(EZECHIEL, 920, 440, "tutta la casa d'Israele", AL("casa", 34) - 0.3, "acc", 46),
      tag(EZECHIEL, 920, 560, "scoraggiata, in esilio", AL("esilio", 34) - 0.4, "", 44)]
gone(tm, LS[35] - 0.5)
S_(EZECHIEL, "foule", 920, 670, 170, AL("promessa", 35) - 0.2, rot=2)
kq(EZECHIEL, 920, 420, "Ezechiele 37.14" + RIV, "«Metterò il mio spirito in voi, e voi vivrete»", 35, "metterò", width=800, size=44,
   last=AL("vivrete", 35) + 0.6, fade_at=LS[36] - 0.4)

# NUOVO TESTAMENTO (righe 36-41)
t = LS[36] - 0.4
cam(t, NT)
headline(NT, 170, ["Il greco: [pneuma]"], t + 0.1, kicker="Il Nuovo Testamento", hl_t=AL("pneuma", 36) + 0.05, size=104)
g36 = [tag(NT, 100, 430, "Scritto in greco", LS[36] + 0.3, "", 56),
       tag(NT, 100, 550, "pneuma", AL("pneuma", 36) - 0.1, "acc", 64)]
gone(g36, AL("nicodemo", 37) - 1.3)
S_(NT, "nicodeme", 100, 410, 210, AL("nicodemo", 37) - 0.3, rot=-3)
S_(NT, "jesus-pied", 380, 410, 190, AL("gesù", 37) - 0.3, rot=3)
kq(NT, 640, 420, "Giovanni 3.8" + RIV,
   "«Il vento soffia dove vuole, e tu ne odi il rumore, ma non sai né donde viene né dove va; così è di chiunque è nato dallo Spirito.»", 37, "il", width=850, size=32,
   fade_at=LS[38] - 0.4)
wind(NT, 1650, 440, AL("vento", 37) - 0.2, size=230, dur=6.0)
nt_tags = [tag(NT, 640, 430, "pneuma = vento = Spirito", AL("greco", 38) - 0.2, "", 46),
           stamp(NT, 640, 550, "Ipotesi", AL("ipotesi", 38) - 0.2, rot=-4, size=60),
           tag(NT, 640, 720, "Gesù parlava aramaico", AL("aramaico", 38) - 0.2, "", 40)]
gone(nt_tags, LS[39] - 0.5)
breath(NT, 1300, 470, AL("soffiò", 39) - 0.2, size=260, dur=3.5)
jp = S_(NT, "jesus-portrait", 1600, 410, 190, AL("soffiò", 39) - 0.2, rot=3)
tg1 = tag(NT, 640, 450, "Gesù soffiò: un soffio", AL("soffiò", 39) + 0.6, "", 38)
gone([jp, tg1], LS[40] - 0.5)
S_(NT, "pentecote", 1200, 410, 260, AL("pentecoste", 40) - 0.6, rot=-2)
tag(NT, 640, 450, "«un vento impetuoso»", AL("impetuoso", 40) - 0.4, "acc", 38)
tag(NT, 640, 720, "Una parola, una storia", AL("pentecoste", 41) - 0.8, "acc", 40)

# ATTENZIONE (righe 42-43)
t = LS[42] - 0.4
cam(t, ATTENTION)
headline(ATTENTION, 170, ["Il [contesto] decide"], t + 0.1, kicker="Ma attenzione", hl_t=AL("contesto", 42) + 0.05, size=96)
sbA = S_(ATTENTION, "sym-balance", 1300, 400, 330, t + 0.4, rot=0)
animate(sbA, "rock", t + 0.4, dur=14.0)
tf = tag(ATTENTION, 90, 430, "Tre significati, non ovunque", AL("valgono", 42) - 0.5, "", 46)
fade(tf, LS[43] - 0.5)
S_(ATTENTION, "elie-portrait", 90, 420, 260, AL("elia", 43) - 0.3, rot=2)
stamp(ATTENTION, 560, 460, "Non è il vento", AL("vento", 43) - 0.2, rot=-3, size=44)
tag(ATTENTION, 560, 640, "Il vento è un segno", AL("segno", 43) - 0.3, "acc", 50)

# APPLICAZIONE (righe 44-46)
t = LS[44] - 0.4
cam(t, APPLI)
headline(APPLI, 170, ["Questa settimana, [un minuto]"], t + 0.1, kicker="Per te", hl_t=AL("minuto", 44) + 0.05, size=92)
ap = [S_(APPLI, "souffle", 90, 430, 190, AL("respiro", 44) - 0.5, rot=2)]
breath(APPLI, 300, 470, AL("respiro", 44) - 0.5, size=400, dur=8.0, pulses=4)
ap.append(counter(APPLI, 830, 420, 0, 60, AL("minuto", 44), 6.0, unit=" s", size=170))
qa = kq(APPLI, 830, 640, "Salmo 34.18" + RIV, "«L'Eterno è vicino a quelli che hanno il cuore afflitto»", 44, "salmo", width=700, size=34,
        last=AL("diciotto", 44) + 0.8, fade_at=LS[45] - 0.5)
gone(ap, AL("sostegno", 45) - 0.4)
glow(APPLI, 1560, 520, AL("sostegno", 45) - 0.4, size=360, dur=8.0)
mlp = S_(APPLI, "mains-lampe", 1400, 420, 280, AL("sostegno", 45) - 0.4, rot=2)
tp = [tag(APPLI, 90, 430, "Un sostegno può aiutare", AL("sostegno", 45) - 0.3, "acc", 50),
      tag(APPLI, 90, 560, "La fede e le cure non si oppongono", AL("oppongono", 45) - 0.8, "", 38)]
gone(tp + [mlp], LS[46] - 0.5)
S_(APPLI, "foule", 1150, 420, 300, LS[46] + 0.2, rot=-2)
tag(APPLI, 90, 430, "Un soffio che ti ha rimesso in piedi", AL("soffio", 46) - 0.2, "acc", 44)
cta = put(APPLI, 90, 600, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Raccontalo nei commenti', "cta")
blur_in(cta, AL("commenti", 46) - 0.6, 14)
sfx("click", AL("commenti", 46) - 0.6, 0.8)

# OREB rivisitato: il sussurro (righe 47-49)
cam(LS[47] - 2.0, "all")
wipe(HOREB, LS[47] - 2.1)
t = LS[47] - 0.4
cam(t, HOREB)
headline(HOREB, 170, ["Un sussurro [dolce e leggero]"], t + 0.1, kicker="1 Re 19.12", hl_t=AL("sussurro", 47) + 0.05, size=88)
glow(HOREB, 1000, 520, AL("oreb", 47), size=480, dur=9.0)
S_(HOREB, "grotte", 700, 410, 360, AL("oreb", 47), rot=2)
S_(HOREB, "elie-portrait", 130, 400, 300, AL("elia", 47) - 0.3, rot=-3)
breath(HOREB, 480, 560, AL("sussurro", 47) - 0.3, size=380, dur=4.5)
hv = [tag(HOREB, 1250, 430, "Vento. Terremoto. Fuoco.", AL("terremoto", 47) - 0.5, "", 40),
      tag(HOREB, 1250, 560, "«un sussurro dolce e leggero»", AL("sussurro", 47) - 0.1, "acc", 44)]
gone(hv, LS[48] - 0.5)
S_(HOREB, "ossements", 1250, 420, 300, AL("ossa", 48) - 0.5, rot=-2)
S_(HOREB, "souffle", 1650, 430, 160, AL("soffio", 48) - 0.2, rot=3)
tag(HOREB, 1250, 720, "La stessa storia", AL("storia", 48) - 0.3, "acc", 44)
hit(AL("storia", 48), 0.8)

t_end = AL("settimana", 49) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(LS[47] - 2.8, LS[47] - 0.5), (AL("settimana", 49) - 0.8, DUR_)]
build(
    chapters=[("01", "Il vento", 0, LS[18]), ("02", "Il soffio", LS[18], LS[25]), ("03", "Lo spirito", LS[25], LS[36]),
              ("04", "Il Nuovo Testamento", LS[36], LS[44]), ("05", "Per te", LS[44], DUR_)],
    suppress=supp,
    endcard={"kicker": "Ogni settimana", "title": "La Bibbia<br />[Semplice]", "button": "Iscriviti",
             "stickers": [("elie-portrait", 150, 560, 300, -6), ("ezechiel", 1550, 330, 200, 5)]},
    endcard_t=AL("settimana", 49) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
