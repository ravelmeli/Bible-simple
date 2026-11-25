"""Video lunga « Avvento: da dove viene questa festa? Che cosa dice davvero la Bibbia » (La Bibbia Semplice) — stile 02, 16:9. Versione italiana di montage/video-avent/.
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

THEME = {"brand": "La Bibbia Semplice", "title": "La Bibbia Semplice - Avvento - style 02", "lang": "it",
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
# =====================================================================  S1 : apertura (righe 1-6)
cam(0, S1)
headline(S1, 170, ["«[Avvento]» non è nella Bibbia"], 0.0, kicker="Non una parola biblica", hl_t=AL("Avvento", 1) + 0.05, size=96)
S_(S1, "livres", 1500, 420, 200, 0.0, rot=2, instant=True)
t1 = tag(S1, 90, 430, "Da nessuna parte nella Bibbia", 0.3, "acc", 52)
gone([t1], LS[2] - 0.4)
t2 = [tag(S1, 90, 430, "Una prima candela", AL("candela", 2) - 0.3, "", 52), tag(S1, 90, 540, "Un calendario dell\'Avvento", AL("calendario", 2) - 0.3, "", 52), tag(S1, 90, 650, "Aspettare il Natale", AL("Natale", 2) - 0.5, "acc", 52)]
gone(t2, LS[3] - 0.4)
t3 = [tag(S1, 90, 430, "Da dove viene questa abitudine?", LS[3] + 0.2, "", 50), tag(S1, 90, 540, "Che cosa dice la Bibbia dell\'attesa?", AL("attesa", 3) - 0.4, "", 46), tag(S1, 90, 650, "Che cosa hanno aggiunto i secoli?", AL("secoli", 3) - 0.5, "acc", 48)]
gone(t3, LS[4] - 0.4)
t4 = [tag(S1, 90, 430, "Ciò che dice il testo", E("testo", 4, 0.4, 0.6), "", 52), tag(S1, 90, 540, "Ciò che dice la tradizione", AL("tradizione", 4) - 0.3, "", 52), tag(S1, 90, 650, "Un\'abitudine moderna", AL("moderna", 4) - 0.4, "acc", 52)]
gone(t4, LS[5] - 0.4)
tag(S1, 90, 430, "Il futuro quanto il passato", E("futuro", 5, 0.3, 0.6), "acc", 50)

# =====================================================================  S2 : adventus, parousia (righe 7-13)
t = LS[7] - 0.4
cam(t, S2)
headline(S2, 170, ["Una parola da [imperatore]"], t + 0.1, kicker="Adventus · parousia", hl_t=AL("imperatore", 8) + 0.05, size=104)
S_(S2, "soldat", 1500, 420, 150, LS[8] + 0.3, rot=2)
c7 = card(S2, 90, 420, "Latino: adventus", "«arrivo», «venuta»", E("arrivo", 7, 0.3, 0.6), w=900, size=52)
gone([c7], LS[8] - 0.4)
t8 = [tag(S2, 90, 430, "L\'ingresso solenne di un imperatore", AL("imperatore", 8) - 0.4, "", 46), tag(S2, 90, 540, "La città si addobba", AL("feste", 8) - 1.2, "acc", 52)]
gone(t8, LS[9] - 0.4)
c9 = card(S2, 90, 420, "Greco: parousia", "«presenza», «venuta»", AL("parousia", 9) - 0.3, w=900, size=52)
t9 = tag(S2, 90, 640, "Anche la visita di un re", AL("visita", 9) - 0.4, "acc", 52)
gone([c9, t9], LS[10] - 0.4)
t10 = tag(S2, 90, 430, "Il vocabolario di un sovrano", AL("vocabolario", 10) - 0.5, "", 52)
gone([t10], LS[11] - 0.4)
t11 = [stamp(S2, 90, 440, "Viene un altro re", E("re", 11, 0.4, 0.8), rot=-3, size=70)]
gone(t11, LS[12] - 0.4)
c12 = card(S2, 90, 420, "Greco: epiphaneia", "«apparizione»", AL("epiphaneia", 12) - 0.3, w=800, size=52)
gone([c12], LS[13] - 0.4)
tag(S2, 90, 430, "Non un conto alla rovescia di regali", AL("regali", 13) - 0.6, "", 46)
tag(S2, 90, 540, "L\'arrivo di un re", AL("re", 13) - 0.5, "acc", 56)

# =====================================================================  S3 : quattro settimane, una tradizione (righe 14-18)
t = LS[14] - 0.4
cam(t, S3)
headline(S3, 170, ["Quattro settimane: una [tradizione]"], t + 0.1, kicker="Non nella Bibbia", hl_t=AL("tradizione", 15) + 0.05, size=92)
S_(S3, "rouleau", 1500, 420, 220, LS[16] + 0.3, rot=2)
t14 = tag(S3, 90, 430, "Nessun periodo di 4 settimane", E("sorpresa", 14, 0.3, 0.6), "acc", 50)
gone([t14], LS[15] - 0.4)
t15 = tag(S3, 90, 430, "Costruita a poco a poco dalla Chiesa", E("poco", 15, 0.6, 0.8), "", 46)
gone([t15], LS[16] - 0.4)
t16 = [tag(S3, 90, 430, "IV secolo · Spagna", AL("Spagna", 16) - 0.3, "", 50), tag(S3, 90, 540, "V secolo · Gallia: 40 giorni", AL("Gallia", 16) - 0.3, "", 50)]
gone(t16, LS[17] - 0.4)
t17 = [tag(S3, 90, 430, "VI secolo · Roma: 4 settimane", AL("Roma", 17) - 0.3, "", 50), tag(S3, 90, 540, "L\'Oriente: altre usanze", AL("Oriente", 17) - 0.3, "acc", 50)]
gone(t17, LS[18] - 0.4)
tag(S3, 90, 430, "Ortodossi: 40 giorni dal 15 novembre", AL("novembre", 18) - 0.5, "", 44)
tag(S3, 90, 540, "Protestanti: pratiche varie", AL("protestanti", 18) - 0.3, "acc", 46)

# =====================================================================  S4 : il 25 dicembre (righe 19-24)
t = LS[19] - 0.4
cam(t, S4)
headline(S4, 170, ["Il [25 dicembre]"], t + 0.1, kicker="Non nella Bibbia nemmeno lui", hl_t=AL("dicembre", 19) + 0.05, size=112)
S_(S4, "sym-balance", 1450, 420, 260, LS[21] + 0.3, rot=2)
t19 = tag(S4, 90, 430, "La data non è nella Bibbia", LS[19] + 0.3, "acc", 50)
gone([t19], LS[20] - 0.4)
t20 = [tag(S4, 90, 430, "I Vangeli: nessuna data", AL("Vangeli", 20) - 0.3, "", 50), tag(S4, 90, 540, "Prima traccia: Roma, IV secolo", AL("Roma", 20) - 0.5, "acc", 48)]
gone(t20, LS[21] - 0.4)
t21 = [stamp(S4, 90, 440, "Due ipotesi", AL("ipotesi", 21) - 0.3, rot=-3, size=70), tag(S4, 90, 620, "Feste pagane del sole?", AL("sole", 21) - 0.6, "", 48), tag(S4, 90, 730, "Calcolata dalla morte di Gesù?", AL("morte", 21) - 0.5, "", 46)]
gone(t21, LS[22] - 0.4)
t22 = [tag(S4, 90, 430, "Gli storici non concordano", AL("storici", 22) - 0.3, "", 50), stamp(S4, 90, 560, "Nessuna certezza", AL("certezza", 22) - 0.6, rot=-3, size=64)]
gone(t22, LS[23] - 0.4)
c23 = card(S4, 90, 420, "Prima rivelazione", "Una tradizione bella, non una prescrizione", AL("rivelazione", 23) - 0.4, w=1000, size=48)
gone([c23], LS[24] - 0.4)
tag(S4, 90, 430, "Restate: la corona, il calendario", LS[24] + 0.3, "acc", 48)

# =====================================================================  S5 : le promesse (righe 25-32)
t = LS[25] - 0.4
cam(t, S5)
headline(S5, 170, ["Secoli di [attesa]"], t + 0.1, kicker="Isaia · Michea", hl_t=AL("attesa", 25) + 0.05, size=104)
S_(S5, "scribe", 1500, 420, 190, LS[27] + 0.3, rot=2)
t25 = tag(S5, 90, 430, "Parla molto di attesa", LS[25] + 0.3, "acc", 50)
gone([t25], LS[26] - 0.4)
t26 = [tag(S5, 90, 430, "Un re", AL("re", 26) - 0.3, "", 56), tag(S5, 90, 540, "Un salvatore", AL("salvatore", 26) - 0.3, "", 56), tag(S5, 90, 650, "Un liberatore", AL("liberatore", 26) - 0.3, "acc", 56)]
gone(t26, LS[27] - 0.4)
c27 = card(S5, 90, 420, "Isaia 9" + BIB, "«un fanciullo ci è nato, un figliuolo ci è stato dato»", AL("fanciullo", 27) - 0.5, w=1000, size=44)
gone([c27], LS[28] - 0.4)
c28 = card(S5, 90, 420, "Michea 5", "Betlemme, «piccola tra le migliaia di Giuda»", AL("Betlemme", 28) - 0.4, w=1000, size=44)
gone([c28], LS[29] - 0.4)
c29 = card(S5, 90, 420, "Isaia 7" + BIB, "«la vergine concepirà… Emmanuele»", AL("vergine", 29) - 0.5, w=1000, size=44)
gone([c29], LS[30] - 0.4)
c30 = put(S5, 90, 420, "<small>Parola ebraica</small><span style='font-size:84px'>almah</span> «giovane donna»", "card", "width:900px;font-size:58px")
blur_in(c30, AL("almah", 30) - 0.3, 14)
gone([c30], LS[31] - 0.4)
c31 = put(S5, 90, 420, "<small>Settanta · greco</small><span style='font-size:84px'>parthenos</span> «vergine»", "card", "width:900px;font-size:58px")
blur_in(c31, AL("parthenos", 31) - 0.3, 14)
gone([c31], LS[32] - 0.4)
stamp(S5, 90, 440, "Emmanuele: «Dio con noi»", AL("Emmanuele", 32) - 0.4, rot=-3, size=56)

# =====================================================================  S6 : promessa tra le rovine (righe 33-38)
t = LS[33] - 0.4
cam(t, S6)
headline(S6, 170, ["Una promessa tra le [rovine]"], t + 0.1, kicker="Isaia 11 · Geremia 33 · Isaia 40", hl_t=AL("rovine", 36) + 0.05, size=96)
S_(S6, "ville", 1450, 420, 300, LS[34] + 0.3, rot=2)
tf33 = tag(S6, 90, 430, "Tre testi, epoche buie", LS[33] + 0.3, "acc", 50)
gone([tf33], AL("ramo", 33) - 0.5)
c33 = card(S6, 90, 420, "Isaia 11" + BIB, "«Un ramo uscirà dal tronco d\'Isai»", AL("ramo", 33) - 0.4, w=1000, size=44)
gone([c33], LS[34] - 0.4)
c34 = card(S6, 90, 420, "Geremia 33", "Dio adempie la sua buona parola", AL("promette", 34) - 0.6, w=1000, size=44)
t34 = tag(S6, 90, 650, "Promessa fatta durante l\'esilio", AL("esilio", 34) - 0.4, "acc", 48)
gone([c34, t34], LS[35] - 0.4)
c35 = card(S6, 90, 420, "Isaia 40" + BIB, "«Consolate, consolate il mio popolo»", AL("Consolate", 35) - 0.3, w=1000, size=46)
gone([c35], LS[36] - 0.4)
t36 = [tag(S6, 90, 430, "Epoche buie", E("buie", 36, 0.3, 0.6), "", 52), tag(S6, 90, 540, "Una promessa sussurrata", AL("rovine", 36) - 0.6, "acc", 52)]
gone(t36, LS[37] - 0.4)
c37 = card(S6, 90, 420, "Periodo intertestamentario", "≈ 4 secoli di silenzio", AL("intertestamentario", 37) - 0.5, w=900, size=48)
gone([c37], LS[38] - 0.4)
tag(S6, 90, 430, "Nessun profeta riconosciuto", AL("profeta", 38) - 0.3, "", 50)
tag(S6, 90, 540, "Un popolo sotto dominio straniero", AL("dominio", 38) - 0.3, "", 50)
tag(S6, 90, 650, "Un\'attesa dolorosa", AL("dolorosa", 38) - 0.5, "acc", 50)

# =====================================================================  S7 : preparare la via (righe 39-41)
t = LS[39] - 0.4
cam(t, S7)
headline(S7, 170, ["Preparare la [via]"], t + 0.1, kicker="Luca 3", hl_t=AL("Preparate", 39) + 0.05, size=112)
S_(S7, "veilleur", 1500, 420, 200, LS[39] + 0.5, rot=2)
c39 = card(S7, 90, 420, "Luca 3" + BIB, "«Preparate la via del Signore, raddrizzate i suoi sentieri»", AL("Preparate", 39) - 0.3, w=1000, size=42)
gone([c39], LS[40] - 0.4)
t40 = [tag(S7, 90, 430, "Il cuore dell\'Avvento", E("cuore", 40, 0.5, 0.8), "acc", 56), tag(S7, 90, 540, "Si riparavano le strade prima di un re", AL("strade", 40) - 0.4, "", 46)]
gone(t40, LS[41] - 0.4)
tag(S7, 90, 430, "Preparare il cuore come una strada", AL("strada", 41) - 0.8, "acc", 50)

# =====================================================================  S8 : le persone di Luca (righe 42-54)
t = LS[42] - 0.4
cam(t, S8)
headline(S8, 170, ["Quelli che [aspettano]"], t + 0.1, kicker="Vangelo di Luca", hl_t=AL("aspettano", 42) + 0.05, size=104)
S_(S8, "ancien", 1500, 420, 190, LS[43] + 0.3, rot=2)
t42 = tag(S8, 90, 430, "Persone che aspettano", LS[42] + 0.3, "acc", 48)
gone([t42], LS[43] - 0.4)
t43 = [tag(S8, 90, 430, "Zaccaria, sacerdote anziano", AL("Zaccaria", 43) - 0.3, "", 50), tag(S8, 90, 540, "Dubita, perde la parola", AL("parola", 43) - 0.5, "acc", 48)]
gone(t43, LS[44] - 0.4)
t44 = [stamp(S8, 90, 440, "Nove mesi di silenzio", AL("silenzio", 44) - 0.5, rot=-3, size=60)]
gone(t44, LS[45] - 0.4)
c45 = card(S8, 90, 420, "Luca 1" + BIB, "«Ecco la serva del Signore»", AL("serva", 45) - 0.4, w=1000, size=44)
gone([c45], LS[46] - 0.4)
c46 = card(S8, 90, 420, "Il Magnificat", "«L\'anima mia magnifica il Signore»", AL("magnifica", 46) - 0.5, w=1000, size=46)
gone([c46], LS[47] - 0.4)
t47 = [tag(S8, 90, 430, "Giuseppe: un sogno", AL("sogno", 47) - 0.3, "", 52), tag(S8, 90, 540, "Esita, poi accoglie", AL("accoglie", 47) - 0.4, "acc", 50)]
gone(t47, LS[48] - 0.4)
t48 = [tag(S8, 90, 430, "Editto di Augusto: un censimento", AL("censimento", 48) - 0.5, "", 48), tag(S8, 90, 540, "Giuseppe e Maria salgono a Betlemme", AL("Betlemme", 48) - 0.3, "", 44)]
gone(t48, LS[49] - 0.4)
c49 = card(S8, 90, 420, "Luca 2" + BIB, "«la pose a giacere in una mangiatoia»", AL("mangiatoia", 49) - 0.7, w=1000, size=46)
gone([c49], LS[50] - 0.4)
c50 = put(S8, 90, 420, "<small>Parola greca</small><span style='font-size:84px'>kataluma</span> una stanza per gli ospiti", "card", "width:1000px;font-size:50px")
blur_in(c50, AL("kataluma", 50) - 0.3, 14)
gone([c50], LS[51] - 0.4)
s51 = stamp(S8, 90, 440, "Un luogo umile", AL("umile", 51) - 0.5, rot=-3, size=70)
gone([s51], LS[52] - 0.4)
t52 = [tag(S8, 90, 430, "Dubbio · fiducia", AL("dubbio", 52) - 0.3, "", 50), tag(S8, 90, 540, "Silenzio · decisione", AL("decisione", 52) - 0.5, "", 50)]
gone(t52, LS[53] - 0.4)
t53 = [tag(S8, 90, 430, "Simeone: «la consolazione d\'Israele»", AL("Simeone", 53) - 0.3, "", 46), tag(S8, 90, 540, "Anna, una profetessa", AL("Anna", 53) - 0.3, "acc", 52)]
gone(t53, LS[54] - 0.4)
tag(S8, 90, 430, "Un\'attesa ricompensata", AL("ricompensata", 54) - 0.5, "acc", 52)

# =====================================================================  S9 : due venute (righe 55-62)
t = LS[55] - 0.4
cam(t, S9)
headline(S9, 170, ["Due [venute]"], t + 0.1, kicker="Betlemme e la fine dei tempi", hl_t=AL("seconda", 56) + 0.05, size=112)
S_(S9, "porte-ville", 1450, 420, 300, LS[56] + 0.3, rot=2)
t55 = tag(S9, 90, 430, "L\'Avvento non parla solo di Betlemme", LS[55] + 0.3, "acc", 46)
gone([t55], LS[56] - 0.4)
t56 = [tag(S9, 90, 430, "1ª venuta: il bambino di Betlemme", AL("prima", 56) - 0.3, "", 48), tag(S9, 90, 540, "2ª venuta: la fine dei tempi", AL("seconda", 56) - 0.3, "acc", 48)]
gone(t56, LS[57] - 0.4)
c57 = card(S9, 90, 420, "Matteo 24" + BIB, "«Vegliate dunque…»", AL("Vegliate", 57) - 0.3, w=900, size=52)
gone([c57], LS[58] - 0.4)
c58 = card(S9, 90, 420, "Apocalisse 22" + BIB, "«Vieni, Signor Gesù!»", AL("Vieni", 58) - 0.5, w=900, size=52)
gone([c58], LS[59] - 0.4)
c59 = put(S9, 90, 420, "<small>Parola aramaica · 1 Corinzi 16</small><span style='font-size:84px'>maranatha</span>", "card", "width:1000px;font-size:46px")
blur_in(c59, AL("maranatha", 59) - 0.3, 14)
gone([c59], LS[60] - 0.4)
t60 = [tag(S9, 90, 430, "«Signore nostro, vieni!»", AL("modi", 60) - 0.2, "", 52), tag(S9, 90, 540, "«Il Signore nostro viene.»", AL("oppure", 60) - 0.3, "acc", 52)]
gone(t60, LS[61] - 0.4)
s61 = stamp(S9, 90, 440, "Una preghiera: Vieni", AL("preghiera", 61) - 0.4, rot=-3, size=70)
gone([s61], LS[62] - 0.4)
tag(S9, 90, 620, "Guardare indietro, guardare avanti", AL("strano", 62) - 0.5, "acc", 44)

# =====================================================================  S10 : corona e calendario (righe 63-67)
t = LS[63] - 0.4
cam(t, S10)
headline(S10, 170, ["Corona e [calendario]"], t + 0.1, kicker="Ciò che si è aggiunto", hl_t=AL("corona", 63) + 0.05, size=104)
S_(S10, "livres", 1500, 420, 200, LS[65] + 0.3, rot=2)
t63 = tag(S10, 90, 430, "La corona: abbastanza recente", AL("corona", 63) - 0.3, "acc", 50)
gone([t63], LS[64] - 0.4)
t64 = [tag(S10, 90, 430, "Ottocento · Germania", LS[64] + 0.3, "", 50), tag(S10, 90, 540, "Wichern, pastore ad Amburgo", AL("Wichern", 64) - 0.3, "acc", 48)]
gone(t64, LS[65] - 0.4)
t65 = [tag(S10, 90, 430, "Il calendario: anche dalla Germania", AL("calendario", 65) - 0.3, "", 46), tag(S10, 90, 540, "Piccole finestrelle", AL("finestrelle", 65) - 0.3, "", 52)]
gone(t65, LS[66] - 0.4)
t66 = [tag(S10, 90, 430, "4 candele: speranza, pace, gioia, amore", AL("speranza", 66) - 0.3, "", 42), stamp(S10, 90, 560, "Nomi variabili", AL("fissa", 66) - 0.6, rot=-3, size=60)]
gone(t66, LS[67] - 0.4)
tag(S10, 90, 430, "Gesti della Chiesa, non comandamenti", AL("gesti", 67) - 0.3, "acc", 46)

# =====================================================================  S11 : che cosa conservare (righe 68-76)
t = LS[68] - 0.4
cam(t, S11)
headline(S11, 170, ["Che cosa [conservare]"], t + 0.1, kicker="Oggi", hl_t=AL("conservare", 68) + 0.05, size=104)
S_(S11, "veilleur", 1500, 420, 200, LS[69] + 0.3, rot=2)
t68 = tag(S11, 90, 430, "Che cosa tenere dell\'Avvento?", LS[68] + 0.2, "acc", 52)
gone([t68], LS[69] - 0.4)
t69 = [tag(S11, 90, 430, "1. L\'attesa", AL("attesa", 69) - 0.3, "", 56), tag(S11, 90, 540, "Un atto di resistenza", AL("resistenza", 69) - 0.5, "acc", 50)]
gone(t69, LS[70] - 0.4)
t70 = [tag(S11, 90, 430, "2. La preparazione", AL("preparazione", 70) - 0.3, "", 56), tag(S11, 90, 540, "Rallentare", AL("rallentare", 70) - 0.3, "acc", 56)]
gone(t70, LS[71] - 0.4)
t71 = [tag(S11, 90, 430, "3. La speranza", AL("speranza", 71) - 0.3, "", 56), tag(S11, 90, 540, "Dio mantiene le promesse", AL("promesse", 71) - 0.4, "acc", 50)]
gone(t71, LS[72] - 0.4)
c72 = put(S11, 90, 420, "<small>Parola ebraica</small><span style='font-size:84px'>tiqvah</span> «speranza»", "card", "width:900px;font-size:56px")
blur_in(c72, AL("tiqvah", 72) - 0.3, 14)
t72 = tag(S11, 90, 700, "Radice qavah: aspettare, tendere verso", AL("qavah", 72) - 0.4, "acc", 46)
gone([c72, t72], LS[73] - 0.4)
c73 = card(S11, 90, 420, "Giosuè 2" + BIB, "tiqvah = anche una corda (il cordone scarlatto)", AL("corda", 73) - 0.5, w=1000, size=44)
gone([c73], LS[74] - 0.4)
t74 = [stamp(S11, 90, 440, "Una lettura, non un fatto", AL("lettura", 74) - 0.5, rot=-3, size=58), tag(S11, 90, 620, "Una corda tesa: un\'attesa che tiene", AL("corda", 74) - 0.4, "", 44)]
gone(t74, LS[75] - 0.4)
c75 = put(S11, 90, 420, "<small>Gaudete · Filippesi 4</small><span style='font-size:70px'>«Rallegratevi sempre nel Signore»</span>", "card", "width:1000px;font-size:46px")
blur_in(c75, AL("Gaudete", 75) - 0.3, 14)
gone([c75], LS[76] - 0.4)
tag(S11, 90, 430, "Una gioia che sa che la strada avanza", AL("stanchezza", 76) - 0.5, "acc", 44)

# =====================================================================  S12 : periodo difficile (righe 77-81)
t = LS[77] - 0.4
cam(t, S12)
headline(S12, 170, ["Quando la festa è [difficile]"], t + 0.1, kicker="Applicazione", hl_t=AL("difficoltà", 77) + 0.05, size=96)
S_(S12, "pere", 1500, 420, 190, LS[79] + 0.3, rot=2)
t77 = tag(S12, 90, 430, "Un periodo difficile per molti", LS[77] + 0.3, "acc", 46)
gone([t77], LS[78] - 0.4)
t78 = [tag(S12, 90, 430, "Solitudine", AL("solitudine", 78) - 0.3, "", 52), tag(S12, 90, 540, "Lutto", AL("lutto", 78) - 0.3, "", 52), tag(S12, 90, 650, "Ai margini delle feste", AL("margini", 78) - 0.6, "acc", 48)]
gone(t78, LS[79] - 0.4)
t79 = [tag(S12, 90, 430, "Non siete soli", AL("soli", 79) - 0.3, "acc", 56), tag(S12, 90, 540, "Anna, madre di Samuele: piangeva", AL("piangeva", 79) - 0.8, "", 44)]
gone(t79, LS[80] - 0.4)
t80 = [tag(S12, 90, 430, "Una persona cara", AL("persona", 80) - 0.3, "", 52), tag(S12, 90, 540, "Un pastore", AL("pastore", 80) - 0.3, "", 52), tag(S12, 90, 650, "Un professionista della salute", AL("professionista", 80) - 0.4, "acc", 52),
       stamp(S12, 90, 770, "Non è mancanza di fede", AL("fede", 80) - 0.5, rot=-3, size=52)]
gone(t80, LS[81] - 0.4)
tq = tag(S12, 90, 430, "Che cosa aspettate davvero?", LS[81] + 0.4, "acc", 46)
cta = put(S12, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Ditelo nei commenti', "cta")
blur_in(cta, AL("commenti", 81) - 1.0, 14)
sfx("click", AL("commenti", 81) - 1.0, 0.8)
gone([tq, cta], LS[82] - 0.3)

# =====================================================================  S13 : conclusione (righe 82-87)
t = LS[82] - 0.4
cam(t, S13)
headline(S13, 170, ["Avvento, [attendere] un re"], t + 0.1, kicker="La risposta", hl_t=AL("domanda", 82) + 0.05, size=100)
S_(S13, "scribe", 1500, 420, 190, LS[85] + 0.3, rot=2)
t82 = tag(S13, 90, 430, "Non nella Bibbia, eppure…", LS[82] + 0.3, "acc", 50)
gone([t82], LS[83] - 0.4)
t83 = [tag(S13, 90, 430, "Una parola da imperatori", AL("imperatori", 83) - 0.4, "", 52), tag(S13, 90, 540, "Ripresa per dire: viene un altro re", AL("altro", 83) - 0.4, "acc", 46)]
gone(t83, LS[84] - 0.4)
t84 = [tag(S13, 90, 430, "Settimane, candele, finestrelle", AL("candele", 84) - 0.4, "", 46), tag(S13, 90, 540, "Bello, non obbligatorio", AL("obbligatorio", 84) - 0.5, "acc", 52)]
gone(t84, LS[85] - 0.4)
t85 = [tag(S13, 90, 430, "Preparare la propria strada", E("messaggio", 85, 0.3, 0.6), "", 52), tag(S13, 90, 540, "Vegliare", AL("vegliare", 85) - 0.3, "", 52), tag(S13, 90, 650, "Sperare", AL("sperare", 85) - 0.3, "acc", 56)]
gone(t85, LS[86] - 0.4)
t86 = [stamp(S13, 90, 440, "La prima candela", AL("candela", 86) - 0.5, rot=-3, size=64), tag(S13, 90, 620, "Che cosa significa, e che cosa no", AL("significa", 86) - 0.5, "acc", 44)]
gone(t86, LS[87] - 0.3)

t_end = AL("Ogni", 87) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(AL("Ogni", 87) - 0.8, DUR_)]
build(
    chapters=[("01", "La parola", 0, LS[14]), ("02", "La tradizione", LS[14], LS[25]), ("03", "L\'attesa biblica", LS[25], LS[55]), ("04", "Oggi", LS[55], DUR_)],
    suppress=supp,
    endcard={"kicker": "Ogni settimana", "title": "La Bibbia<br />[Semplice]", "button": "Iscriviti",
             "stickers": [("scribe", 150, 560, 280, -6), ("jesus-portrait", 1550, 330, 230, 5)]},
    endcard_t=AL("Ogni", 87) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
