"""Video lunga « 666: perché quasi tutto ciò che vi hanno raccontato è sbagliato » (La Bibbia Semplice) — stile 02, 16:9. Versione italiana di montage/video-666/.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py), option retention, thème beige.
L'hébreu (נרון קסר) est écrit en HTML : à faire relire avant publication.
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

THEME = {"brand": "La Bibbia Semplice", "title": "La Bibbia Semplice - 666 - style 02", "lang": "it",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
DUR_ = json.load(open(os.path.join(HERE, "dur.json")))["dur"]
s.setup(here=HERE, duration=DUR_, cols=5, rows=4, fmt="16:9", theme=THEME, bpm=96, zoom=1.15, xmap=(190, 0.8539), ymap=(208, 0.85))
from style02 import *  # noqa: E402,F401,F403
import style02  # noqa: E402

MANQUES = []
SUPP = []


def _norm(t):
    return re.sub(r"[^\wÀ-ÿ]", "", t.lower().replace("’", "").replace("'", ""))


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


PRE = ("", "l", "d", "j", "n", "s", "qu", "c", "m", "t", "v", "dell", "nell", "all", "dall", "sull", "un", "quest", "nel", "sant", "tutt", "po")


def A(word, after=0.0, n=0):
    keys = {style02.norm(pre + word) for pre in PRE}
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


def E(word, line, dt, early=0.5):
    """Instant d'apparition : le mot moins dt, mais au plus tard LS[ligne] + early (pas de scène vide)."""
    return min(AL(word, line) - dt, LS[line] + early)


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


S1, S2, S3, S4, S5 = (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)
S6, S7, S8, S9, S10 = (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)
S11, S12, S13 = (0, 2), (1, 2), (2, 2)
BIB = " · Riveduta"

html.append('<style>'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '@font-face{font-family:"Frank Ruhl Libre";src:url("assets/fonts/FrankRuhlLibre.ttf") format("truetype");font-weight:300 900}'
            '.heb{font-family:"Frank Ruhl Libre",serif;direction:rtl;display:inline-block}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

# =====================================================================  S1
# =====================================================================  S1 : il 666 prima dell'Apocalisse (righe 1-8)
cam(0, S1)
headline(S1, 170, ["Il [666], prima dell\'Apocalisse"], 0.0, kicker="Un numero famoso", hl_t=AL("666", 1) + 0.05, size=96)
S_(S1, "livres", 1500, 420, 200, 0.0, rot=2, instant=True)
t1 = tag(S1, 90, 430, "666: molto prima dell\'Apocalisse", 0.3, "acc", 50)
gone([t1], LS[2] - 0.4)
c2 = card(S1, 90, 420, "1 Re 10,14 · Salomone", "666 talenti d\'oro all\'anno", AL("talenti", 2) - 0.5, w=900, size=52)
gone([c2], LS[3] - 0.4)
s3 = stamp(S1, 90, 440, "Non il diavolo?", E("diavolo", 3, 0.5, 0.6), rot=-3, size=72)
gone([s3], LS[4] - 0.4)
t4 = [tag(S1, 90, 430, "Che cosa voleva dire?", LS[4] + 0.2, "", 50), tag(S1, 90, 540, "Tutto è falso?", AL("falso", 4) - 0.3, "acc", 56)]
gone(t4, LS[5] - 0.4)
t5 = [tag(S1, 90, 430, "Codici a barre", E("codici", 5, 0.3, 0.4), "", 50), tag(S1, 90, 530, "Microchip", AL("microchip", 5) - 0.2, "", 50),
      tag(S1, 90, 630, "Carte di credito", AL("carte", 5) - 0.2, "", 50), tag(S1, 90, 730, "Vaccini", AL("vaccini", 5) - 0.3, "acc", 50)]
gone(t5, LS[6] - 0.4)
t6 = [tag(S1, 90, 430, "Ogni epoca, il suo 666", LS[6] + 0.3, "", 52), tag(S1, 90, 540, "Oggetti che non esistevano", AL("oggetti", 6) - 0.4, "acc", 48)]
gone(t6, LS[7] - 0.4)
t7 = [tag(S1, 90, 430, "Ciò che dice il testo", LS[7] + 0.4, "", 52), tag(S1, 90, 540, "Ciò che pensano gli storici", AL("storici", 7) - 0.3, "", 48), tag(S1, 90, 650, "Ciò che è solo una voce", AL("voce", 7) - 0.4, "acc", 50)]
gone(t7, LS[8] - 0.4)
tag(S1, 90, 430, "Più semplice", AL("semplice", 8) - 0.3, "", 56)
tag(S1, 90, 540, "Più sorprendente", AL("sorprendente", 8) - 0.3, "acc", 56)

# =====================================================================  S2 : un libro, una lettera (righe 9-14)
t = LS[9] - 0.4
cam(t, S2)
headline(S2, 170, ["Un libro, una [lettera]"], t + 0.1, kicker="L\'Apocalisse", hl_t=E("lettera", 10, 0.2, 2.0), size=104)
S_(S2, "scribe", 1500, 420, 190, LS[10] + 0.2, rot=2)
t9 = tag(S2, 90, 430, "Chi l\'ha scritto? Per chi?", LS[9] + 0.2, "acc", 52)
gone([t9], LS[10] - 0.4)
t10 = [tag(S2, 90, 430, "Giovanni, l\'autore", E("Giovanni", 10, 0.2, 1.0), "", 52), tag(S2, 90, 540, "Dall\'isola di Patmos", AL("Patmos", 10) - 0.3, "acc", 50)]
gone(t10, LS[11] - 0.4)
t11 = [tag(S2, 90, 430, "7 comunità cristiane", AL("sette", 11) - 0.2, "", 50), tag(S2, 90, 540, "Asia · attuale Turchia", AL("Asia", 11) - 0.3, "acc", 50)]
gone(t11, LS[12] - 0.4)
t12 = [tag(S2, 90, 430, "Sotto l\'Impero romano", AL("Impero", 12) - 0.3, "", 52), tag(S2, 90, 540, "Minoranza, a volte perseguitata", AL("perseguitata", 12) - 0.8, "acc", 48)]
gone(t12, LS[13] - 0.4)
c13 = card(S2, 90, 420, "Dal greco: «rivelazione»", "Un genere apocalittico", E("apocalittico", 13, 0.4, 0.6), w=900, size=50)
gone([c13], LS[14] - 0.4)
tag(S2, 90, 430, "Bestie · stelle", AL("stelle", 14) - 0.3, "", 48)
tag(S2, 90, 540, "Trombe · numeri", AL("numeri", 14) - 0.4, "", 48)
tag(S2, 90, 650, "Vanno decifrate", AL("decifrano", 14) - 0.6, "acc", 52)

# =====================================================================  S3 : la bestia e il marchio (righe 15-18)
t = LS[15] - 0.4
cam(t, S3)
headline(S3, 170, ["La bestia e il [marchio]"], t + 0.1, kicker="Apocalisse 13", hl_t=AL("bestia", 15) + 0.05, size=104)
t15 = [tag(S3, 90, 430, "Una bestia sale dal mare", AL("bestia", 15) - 0.2, "", 52), tag(S3, 90, 540, "«Chi è simile alla bestia?»", AL("simile", 15) - 0.5, "acc", 46)]
gone(t15, LS[16] - 0.4)
t16 = [tag(S3, 90, 430, "Una seconda bestia", AL("seconda", 16) - 0.2, "", 52), tag(S3, 90, 540, "Il «falso profeta»", AL("profeta", 16) - 0.6, "acc", 52)]
gone(t16, LS[17] - 0.4)
tp17 = tag(S3, 90, 430, "Apocalisse 13,16-18", LS[17] + 0.3, "acc", 52)
gone([tp17], AL("fa", 17) - 0.45)
kq(S3, 90, 420, "Apocalisse 13,16-17" + BIB, "«E fa sì che a tutti, piccoli e grandi, ricchi e poveri, liberi e schiavi, sia posto un marchio sulla loro mano destra o sulla loro fronte, e che nessuno possa comprare o vendere se non chi ha il marchio, il nome della bestia o il numero del suo nome.»", 17, "fa", width=1000, size=34, fade_at=LS[18] - 0.4)
kq(S3, 90, 420, "Apocalisse 13,18" + BIB, "«Qui è la sapienza. Chi ha intelligenza calcoli il numero della bestia, perché è un numero d\'uomo; e il suo numero è seicentosessantasei.»", 18, "Qui", width=1000, size=38, fade_at=LS[19] - 0.4)

# =====================================================================  S4 : tre idee diffuse (righe 19-28)
t = LS[19] - 0.4
cam(t, S4)
headline(S4, 170, ["Tre idee [diffuse]"], t + 0.1, kicker="Che cosa dice il testo", hl_t=AL("diffusa", 19) + 0.05, size=104)
S_(S4, "ancien", 1500, 420, 190, LS[20] + 0.3, rot=2)
t19 = tag(S4, 90, 430, "Quasi ogni parola smentisce un\'idea diffusa", LS[19] + 0.3, "acc", 44)
gone([t19], LS[20] - 0.4)
t20 = tag(S4, 90, 430, "Idea n°1: il numero dell\'Anticristo", E("Prima", 20, 0.1, 0.4), "", 48)
gone([t20], LS[21] - 0.4)
t21 = [stamp(S4, 90, 440, "Assente dall\'Apocalisse", E("mai", 21, 0.4, 1.0), rot=-3, size=60), tag(S4, 90, 620, "Solo in 1 e 2 Giovanni", AL("lettere", 21) - 0.5, "acc", 48)]
gone(t21, LS[22] - 0.4)
c22 = card(S4, 90, 420, "1 Giovanni 2,18" + BIB, "«ora sono sorti molti anticristi»", AL("sorti", 22) - 0.6, w=1000, size=44)
gone([c22], LS[23] - 0.4)
t23 = [tag(S4, 90, 430, "Idea n°2: il numero del diavolo", E("Seconda", 23, 0.1, 0.4), "", 48), card(S4, 90, 560, "Apocalisse 13,18", "«un numero d\'uomo»", AL("uomo", 23) - 0.6, w=800, size=44, accent=True)]
gone(t23, LS[24] - 0.4)
t24 = [stamp(S4, 90, 440, "Non «numero di Satana»", AL("Satana", 24) - 0.6, rot=-3, size=60), tag(S4, 90, 620, "Un essere umano", AL("umano", 24) - 0.4, "acc", 52)]
gone(t24, LS[25] - 0.4)
t25 = tag(S4, 90, 430, "Idea n°3: un oggetto, una tecnologia", E("Terza", 25, 0.1, 0.4), "", 46)
gone([t25], LS[26] - 0.4)
t26 = [tag(S4, 90, 430, "Un nome · un marchio", LS[26] + 0.3, "", 52), tag(S4, 90, 540, "Comprare e vendere", AL("comprare", 26) - 0.3, "", 52), stamp(S4, 90, 720, "Nessun oggetto", AL("elettronico", 26) - 0.5, rot=-3, size=60)]
gone(t26, LS[27] - 0.4)
t27 = [tag(S4, 90, 430, "Papi · Napoleone · dittatori", AL("papi", 27) - 0.3, "", 48), tag(S4, 90, 540, "Poi i computer", AL("computer", 27) - 0.5, "acc", 52)]
gone(t27, LS[28] - 0.4)
stamp(S4, 90, 440, "Tutte fallite", E("fallite", 28, 0.4, 0.6), rot=-3, size=64)
tag(S4, 90, 620, "Un numero per tutti non indica nessuno", AL("nessuno", 28) - 0.8, "acc", 44)

# =====================================================================  S5 : calcolare un nome (righe 29-34)
t = LS[29] - 0.4
cam(t, S5)
headline(S5, 170, ["Calcolare un [nome]"], t + 0.1, kicker="La gematria", hl_t=AL("calcolare", 29) + 0.05, size=104)
S_(S5, "rouleau", 1500, 420, 220, LS[30] + 0.3, rot=2)
t29 = tag(S5, 90, 430, "«Calcolare»", LS[29] + 0.3, "acc", 60)
gone([t29], LS[30] - 0.4)
t30 = [tag(S5, 90, 430, "Ogni lettera = un numero", AL("valore", 30) - 0.6, "", 52), tag(S5, 90, 540, "Greco · ebraico", AL("ebraico", 30) - 0.3, "acc", 52)]
gone(t30, LS[31] - 0.4)
c31 = card(S5, 90, 420, "La gematria", "un nome → un numero", AL("gematria", 31) - 0.4, w=900, size=52)
gone([c31], LS[32] - 0.4)
t32 = [tag(S5, 90, 430, "Quale nome dà 666?", LS[32] + 0.2, "", 52), stamp(S5, 90, 570, "Nerone Cesare", AL("Cesare", 32) - 0.5, rot=-3, size=72)]
gone(t32, LS[33] - 0.3)
c33 = put(S5, 90, 420, "<small>Nerone Cesare, in ebraico</small><span class='heb' style='font-size:130px'>נרון קסר</span>", "card", "width:1000px;font-size:46px")
blur_in(c33, AL("ebraiche", 33) - 0.3, 14)
v33 = tag(S5, 90, 730, "50 · 200 · 6 · 50 — 100 · 60 · 200", AL("nun", 33) + 0.2, "acc", 50)
gone([c33, v33], LS[34] - 0.4)
counter(S5, 90, 420, 0, 666, AL("Sommate", 34) + 1.5, 1.2, unit="", size=230)
tag(S5, 90, 700, "50 + 200 + 6 + 50 + 100 + 60 + 200", AL("Sommate", 34) + 0.2, "", 44)

# =====================================================================  S6 : Nerone Cesare (righe 35-43)
t = LS[35] - 0.4
cam(t, S6)
headline(S6, 170, ["L\'ipotesi [Nerone]"], t + 0.1, kicker="Un calcolo, un nome", hl_t=AL("616", 35) + 0.05, size=104)
S_(S6, "soldat", 1500, 420, 150, LS[39] + 0.3, rot=2)
t35 = [stamp(S6, 90, 440, "616!", E("616", 35, 0.2, 0.6), rot=-3, size=90), tag(S6, 90, 620, "Manoscritti molto antichi", AL("manoscritti", 35) - 0.4, "acc", 50)]
gone(t35, LS[36] - 0.4)
tf36 = tag(S6, 90, 430, "Stesso calcolo, altra grafia", LS[36] + 0.3, "", 50)
gone([tf36], AL("ultima", 36) - 0.55)
t36 = [tag(S6, 90, 430, "Nerone senza l\'ultima lettera", AL("ultima", 36) - 0.5, "", 50), tag(S6, 90, 540, "= 616", AL("616", 36, 0) - 0.4, "acc", 60)]
gone(t36, LS[37] - 0.4)
tf37 = tag(S6, 90, 430, "Una variante ben attestata", LS[37] + 0.3, "", 50)
gone([tf37], AL("papiro", 37) - 0.45)
c37 = card(S6, 90, 420, "Papiro", "III o IV secolo", AL("papiro", 37) - 0.4, w=800, size=52)
gone([c37], LS[38] - 0.4)
tf38 = tag(S6, 90, 430, "Un argomento serio", LS[38] + 0.3, "", 52)
gone([tf38], AL("ipotesi", 38) - 0.5)
t38 = [stamp(S6, 90, 440, "Ipotesi", AL("ipotesi", 38) - 0.4, rot=-3, size=80), tag(S6, 90, 620, "Non una certezza", AL("certezza", 38) - 0.4, "acc", 52), tag(S6, 90, 730, "Ireneo conosce già il 616", AL("Ireneo", 38) - 0.3, "", 46)]
gone(t38, LS[39] - 0.4)
t39 = [tag(S6, 90, 430, "Perché Nerone?", LS[39] + 0.2, "", 56), tag(S6, 90, 540, "Già visto come la bestia", AL("bestia", 39) - 0.5, "acc", 50)]
gone(t39, LS[40] - 0.4)
t40 = [tag(S6, 90, 430, "64: l\'incendio di Roma", AL("64", 40) - 0.2, "", 50), tag(S6, 90, 540, "Tacito: i cristiani accusati", AL("Tacito", 40) - 0.3, "acc", 46)]
gone(t40, LS[41] - 0.4)
t41 = [tag(S6, 90, 430, "68: morte di Nerone", AL("68", 41) - 0.2, "", 50), tag(S6, 90, 540, "La voce: tornerà", AL("tornerà", 41) - 0.6, "", 50), tag(S6, 90, 650, "Bestia ferita, poi guarita", AL("guarita", 41) - 0.6, "acc", 48)]
gone(t41, LS[42] - 0.4)
c42 = card(S6, 90, 420, "Prima rivelazione", "Un enigma per lettori precisi", AL("rivelazione", 42) - 0.4, w=1000, size=48)
gone([c42], LS[43] - 0.4)
tag(S6, 90, 430, "Restate: il marchio, poi il sei", LS[43] + 0.3, "acc", 48)

# =====================================================================  S7 : la data (righe 44-46)
t = LS[44] - 0.4
cam(t, S7)
headline(S7, 170, ["La [data] discussa"], t + 0.1, kicker="Apocalisse", hl_t=AL("data", 44) + 0.05, size=104)
S_(S7, "porte-ville", 1450, 420, 300, LS[44] + 0.5, rot=2)
t44 = tag(S7, 90, 430, "La data è discussa", LS[44] + 0.2, "acc", 56)
gone([t44], LS[45] - 0.4)
t45 = [tag(S7, 90, 430, "Tradizione: verso il 95 · Domiziano", AL("95", 45) - 0.3, "", 48), tag(S7, 90, 540, "Altri: verso il 68-70", AL("68", 45) - 0.4, "acc", 52)]
gone(t45, LS[46] - 0.4)
tag(S7, 90, 430, "Domiziano o l\'Impero", AL("Domiziano", 46) - 0.3, "", 52)
tag(S7, 90, 540, "Nerone, un modello", AL("modello", 46) - 0.4, "", 52)
tag(S7, 90, 650, "Sempre: il potere romano", AL("romano", 46) - 0.4, "acc", 50)

# =====================================================================  S8 : il marchio (righe 47-51)
t = LS[47] - 0.4
cam(t, S8)
headline(S8, 170, ["Il [marchio]"], t + 0.1, kicker="Apocalisse 13", hl_t=AL("marchio", 47) + 0.05, size=112)
S_(S8, "foule", 1250, 500, 250, LS[48] + 0.3, rot=-2)
t47 = [tag(S8, 90, 430, "Il culto dell\'imperatore", E("culto", 47, 0.3, 0.9), "", 52), tag(S8, 90, 540, "Templi · statue · giuramenti", AL("giuramenti", 47) - 0.5, "acc", 48)]
gone(t47, LS[48] - 0.4)
t48 = [tag(S8, 90, 430, "Mestieri in associazioni", AL("associazioni", 48) - 0.4, "", 50), tag(S8, 90, 540, "Rifiutare = perdere il lavoro", AL("lavoro", 48) - 0.6, "acc", 48)]
gone(t48, LS[49] - 0.4)
t49 = [stamp(S8, 90, 440, "Né comprare né vendere", AL("comprare", 49) - 0.3, rot=-3, size=56), tag(S8, 90, 620, "Un segno di appartenenza", AL("appartenenza", 49) - 0.5, "acc", 52)]
gone(t49, LS[50] - 0.4)
c50 = card(S8, 90, 420, "Deuteronomio 6,8", "«un segno sulla mano, tra gli occhi»", AL("Deuteronomio", 50) - 0.3, w=900, size=44)
gone([c50], LS[51] - 0.4)
t51 = [tag(S8, 90, 430, "Il marchio della bestia", E("subito", 51, 0.2, 0.6), "", 52), tag(S8, 90, 540, "Il nome dell\'Agnello sulla fronte", AL("Agnello", 51) - 0.4, "acc", 48), stamp(S8, 90, 680, "Due fedeltà", AL("fedeltà", 51) - 0.5, rot=-3, size=60)]

# =====================================================================  S9 : perché sei? (righe 52-55)
t = LS[52] - 0.4
cam(t, S9)
headline(S9, 170, ["Perché [sei]?"], t + 0.1, kicker="Genesi 1", hl_t=AL("sei", 52) + 0.05, size=112)
S_(S9, "livres", 1500, 420, 200, LS[53] + 0.3, rot=2)
t52 = [tag(S9, 90, 430, "Perché 6-6-6?", LS[52] + 0.2, "", 56), tag(S9, 90, 540, "E con Salomone?", AL("Salomone", 52) - 0.3, "acc", 52)]
gone(t52, LS[53] - 0.4)
c53 = card(S9, 90, 420, "Genesi 1", "L\'uomo è creato il sesto giorno", AL("Genesi", 53) - 0.3, w=1000, size=48)
gone([c53], LS[54] - 0.4)
t54 = [tag(S9, 90, 430, "7 giorni · 7 chiese", AL("sette", 54) - 0.2, "", 50), tag(S9, 90, 540, "7 sigilli · 7 trombe", AL("trombe", 54) - 0.5, "", 50), stamp(S9, 90, 710, "Il 7: la pienezza", AL("pienezza", 54) - 0.4, rot=-3, size=60)]
gone(t54, LS[55] - 0.4)
t55 = [tag(S9, 90, 430, "6: l\'umano, limitato?", AL("umano", 55) - 0.5, "", 52), stamp(S9, 90, 560, "Lettura comune", AL("comune", 55) - 0.4, rot=-3, size=60), tag(S9, 90, 720, "Nessun versetto la afferma", AL("versetto", 55) - 0.5, "acc", 50)]

# =====================================================================  S10 : Salomone e Nebucadnetsar (righe 56-61)
t = LS[56] - 0.4
cam(t, S10)
headline(S10, 170, ["Due scene, il [sei]"], t + 0.1, kicker="1 Re 10 · Daniele 3", hl_t=AL("scene", 56) + 0.05, size=104)
S_(S10, "sym-balance", 1450, 420, 260, LS[57] + 0.5, rot=2)
t56 = tag(S10, 90, 430, "Due scene in cui il sei ritorna", LS[56] + 0.2, "acc", 52)
gone([t56], LS[57] - 0.4)
c57 = card(S10, 90, 420, "1 Re 10,14 · Salomone", "666 talenti d\'oro all\'anno", AL("talenti", 57) - 0.5, w=900, size=50)
t57 = [tag(S10, 90, 640, "≈ 20 tonnellate d\'oro", AL("tonnellate", 57) - 0.4, "acc", 52), tag(S10, 90, 750, "Deuteronomio 17: niente oro accumulato", AL("Deuteronomio", 57) - 0.3, "", 40)]
gone([c57] + t57, LS[58] - 0.4)
t58 = [tag(S10, 90, 430, "Cavalli dall\'Egitto", AL("Egitto", 58) - 0.3, "", 52), tag(S10, 90, 540, "Centinaia di donne", AL("donne", 58) - 0.4, "", 52), tag(S10, 90, 650, "Oro accumulato", AL("accumula", 58) - 0.5, "acc", 52)]
gone(t58, LS[59] - 0.4)
c59 = card(S10, 90, 420, "Daniele 3,1 · Nebucadnetsar", "Una statua d\'oro: 60 cubiti × 6", AL("Daniele", 59) - 0.3, w=1000, size=46)
s59 = stamp(S10, 90, 660, "Prostrarsi o morire", AL("prostrarsi", 59) - 0.5, rot=-3, size=60)
gone([c59, s59], LS[60] - 0.4)
t60 = [tag(S10, 90, 430, "Un potere esige adorazione", AL("adorazione", 60) - 0.5, "", 50), tag(S10, 90, 540, "I fedeli rifiutano", AL("fedeli", 60) - 0.4, "acc", 52)]
gone(t60, LS[61] - 0.4)
stamp(S10, 90, 440, "Una pista, non una prova", AL("prova", 61) - 0.8, rot=-3, size=56)
tag(S10, 90, 620, "Giovanni vi pensava? Nessuno può affermarlo", AL("pensava", 61) - 0.3, "", 42)

# =====================================================================  S11 : il senso dei numeri (righe 62-66)
t = LS[62] - 0.4
cam(t, S11)
headline(S11, 170, ["I numeri hanno un [senso]"], t + 0.1, kicker="Ascoltare gli echi", hl_t=AL("solido", 62) + 0.05, size=96)
S_(S11, "veilleur", 1500, 420, 200, LS[63] + 0.3, rot=2)
tf62 = tag(S11, 90, 430, "Ciò che è solido", LS[62] + 0.3, "acc", 56)
gone([tf62], AL("codice", 62) - 0.55)
t62 = [tag(S11, 90, 430, "Nessun codice nascosto", AL("codice", 62) - 0.5, "", 52), tag(S11, 90, 540, "Gli echi del testo", AL("echi", 62, 0) - 0.4, "acc", 52)]
gone(t62, LS[63] - 0.4)
t63 = [tag(S11, 90, 430, "Le letture sul futuro: false?", LS[63] + 0.2, "", 46), stamp(S11, 90, 570, "No", E("No", 63, 0.2, 0.9), rot=-3, size=90)]
gone(t63, LS[64] - 0.4)
t64 = [tag(S11, 90, 430, "Il primo secolo", AL("secolo", 64) - 0.5, "", 50), tag(S11, 90, 540, "La storia della Chiesa", AL("Chiesa", 64) - 0.3, "", 50), tag(S11, 90, 650, "Un periodo finale", AL("finale", 64) - 0.4, "acc", 50)]
gone(t64, LS[65] - 0.4)
t65 = [tag(S11, 90, 430, "Nessun campo da scegliere", AL("campo", 65) - 0.4, "", 52), tag(S11, 90, 540, "Il testo ≠ ciò che vi si proietta", AL("proiettato", 65) - 0.7, "acc", 46)]
gone(t65, LS[66] - 0.4)
c66 = card(S11, 90, 420, "Matteo 24,4" + BIB, "«Guardate che nessuno vi seduca»", AL("Matteo", 66) - 0.3, w=1000, size=42)
tag(S11, 90, 650, "Vigilanza, non panico", AL("vigilanza", 66) - 0.4, "acc", 52)

# =====================================================================  S12 : quando il numero fa paura (righe 67-71)
t = LS[67] - 0.4
cam(t, S12)
headline(S12, 170, ["Quando il numero fa [paura]"], t + 0.1, kicker="Applicazione", hl_t=AL("angosciate", 67) + 0.05, size=100)
S_(S12, "pere", 1500, 420, 190, LS[68] + 0.3, rot=2)
t67 = [tag(S12, 90, 430, "Paura della fine dei tempi", LS[67] + 0.4, "", 52), tag(S12, 90, 540, "Paura di «ricevere il marchio»", AL("marchio", 67) - 0.5, "acc", 48)]
gone(t67, LS[68] - 0.4)
t68 = [stamp(S12, 90, 440, "Scritto per consolare", AL("consolare", 68) - 0.4, rot=-3, size=64), tag(S12, 90, 620, "Non per terrorizzare", AL("terrorizzarli", 68) - 0.5, "acc", 52)]
gone(t68, LS[69] - 0.4)
t69a = tag(S12, 90, 430, "Una benedizione per chi legge", AL("benedizione", 69) - 0.3, "", 48)
gone([t69a], AL("asciugherà", 69) - 0.5)
c69 = card(S12, 90, 420, "Apocalisse 21,4" + BIB, "«Iddio asciugherà ogni lagrima dagli occhi loro»", AL("asciugherà", 69) - 0.3, w=1000, size=42)
gone([c69], LS[70] - 0.4)
t70 = [tag(S12, 90, 430, "Una persona cara", AL("persona", 70) - 0.3, "", 52), tag(S12, 90, 540, "Un pastore", AL("pastore", 70) - 0.3, "", 52), tag(S12, 90, 650, "Un professionista della salute", AL("professionista", 70) - 0.4, "acc", 52),
       stamp(S12, 90, 770, "Non è mancanza di fede", AL("fede", 70) - 0.5, rot=-3, size=52)]
gone(t70, LS[71] - 0.4)
tq = tag(S12, 90, 430, "Quale timore vi ha segnato?", LS[71] + 0.4, "acc", 50)
cta = put(S12, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Ditelo nei commenti', "cta")
blur_in(cta, AL("commenti", 71) - 1.0, 14)
sfx("click", AL("commenti", 71) - 1.0, 0.8)
gone([tq, cta], LS[72] - 0.3)

# =====================================================================  S13 : conclusione (righe 72-77)
t = LS[72] - 0.4
cam(t, S13)
headline(S13, 170, ["Tanto [falso] sul 666"], t + 0.1, kicker="La risposta", hl_t=AL("false", 72) + 0.05, size=100)
S_(S13, "scribe", 1500, 420, 190, LS[75] + 0.3, rot=2)
t72 = tag(S13, 90, 430, "Perché tante cose false?", LS[72] + 0.3, "acc", 56)
gone([t72], LS[73] - 0.4)
t73 = [tag(S13, 90, 430, "Un numero misterioso", AL("misterioso", 73) - 0.4, "", 52), tag(S13, 90, 540, "Le paure di ogni epoca", AL("paure", 73) - 0.4, "acc", 50)]
gone(t73, LS[74] - 0.4)
tf74 = tag(S13, 90, 430, "Il testo è più sobrio", LS[74] + 0.3, "", 52)
gone([tf74], AL("uomo", 74) - 0.45)
t74 = [tag(S13, 90, 430, "Un numero d\'uomo", AL("uomo", 74) - 0.3, "", 52), tag(S13, 90, 540, "Un nome da calcolare", AL("calcolare", 74) - 0.3, "", 52), tag(S13, 90, 650, "Un marchio: a chi si appartiene", AL("marchio", 74) - 0.3, "acc", 48)]
gone(t74, LS[75] - 0.4)
t75 = [stamp(S13, 90, 440, "Non un codice da temere", AL("codice", 75) - 0.4, rot=-3, size=60), tag(S13, 90, 620, "Una fedeltà dovuta solo a Dio", AL("fedeltà", 75) - 0.6, "acc", 46)]
gone(t75, LS[76] - 0.4)
t76 = [tag(S13, 90, 430, "Chi è il destinatario?", AL("destinatario", 76) - 0.3, "", 52), tag(S13, 90, 540, "Qual è il contesto?", AL("contesto", 76) - 0.3, "", 52), tag(S13, 90, 650, "Che cosa dice il versetto?", AL("versetto", 76) - 0.3, "acc", 52)]
gone(t76, LS[77] - 0.3)

t_end = AL("Ogni", 77) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(AL("Ogni", 77) - 0.8, DUR_)]
build(
    chapters=[("01", "Il mito", 0, LS[9]), ("02", "Il testo", LS[9], LS[29]), ("03", "Nerone", LS[29], LS[52]), ("04", "Il sei", LS[52], LS[67]), ("05", "Per voi", LS[67], DUR_)],
    suppress=supp,
    endcard={"kicker": "Ogni settimana", "title": "La Bibbia<br />[Semplice]", "button": "Iscriviti",
             "stickers": [("scribe", 150, 560, 280, -6), ("jesus-portrait", 1550, 330, 230, 5)]},
    endcard_t=AL("Ogni", 77) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
