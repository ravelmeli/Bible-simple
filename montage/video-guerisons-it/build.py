"""Video lunga « Ogni guarigione di Gesù, classificata per tipo di malattia » (La Bibbia Semplice) — style 02, 16:9, 674.7 s. Versione italiana di montage/video-guerisons/.

Construit avec le moteur du kit (kit-style-02/moteur/style02.py), option retention, thème beige.
Règles de mise en page (contrôlées par kit-style-02/outils/audit_chevauchements.js après chaque build) :
  - contenu à partir de y = 420 (sous le titre), colonne gauche x = 90, colonne droite x >= 1100, autocollants hauts à x = 1500 ;
  - une citation occupe sa zone seule : tout ce qui s'y trouvait disparaît avant, elle disparaît à la fin de la ligne ;
  - le contenu s'arrête avant les sous-titres (bas d'écran).
Les mots grecs et araméens (lepra, sôzô, Effatà, Talità kum) sont écrits en HTML : à faire relire avant publication.
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

THEME = {"brand": "La Bibbia Semplice", "title": "La Bibbia Semplice - Le guarigioni di Gesù - style 02", "lang": "it",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
DUR_ = 674.7
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
    keys = {style02.norm(pre + word) for pre in ("", "l", "d", "j", "n", "s", "qu", "c", "m", "t", "dell", "nell", "all", "dall", "sull", "un", "v", "quest", "nel", "sant", "tutt")}
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




S1, S2, S3, S4, S5 = (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)
S6, S7, S8, S9, S10 = (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)
S11 = (0, 2)

html.append('<style>'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')
WEB = " · Riveduta"

# S1: la porta di Cafarnao (righe 1-9)
cam(0, S1)
headline(S1, 170, ["Una città intera a [una porta]"], 0.0, kicker="Marco 1,32-33", hl_t=AL("porta", 1) + 0.05, size=88)
f0 = S_(S1, "foule", 1100, 420, 330, 0.0, rot=-3, instant=True)
fade(f0, AL("Marco", 3) - 0.7)
f3 = tag(S1, 90, 430, "Marco racconta la scena", LS[3] + 0.2, "acc", 52)
fade(f3, AL("Poi", 3) - 0.7)
t2 = [tag(S1, 90, 430, "Cafarnao", AL("Cafarnao", 2) - 0.2, "", 52), tag(S1, 90, 540, "Il lago di Galilea", AL("Galilea", 2) - 0.2, "", 52)]
gone(t2, LS[3] - 0.5)
kq(S1, 90, 420, "Marco 1,32-33" + WEB,
   "«Poi, fattosi sera, tramontato il sole, gli menavano tutti i malati e gli indemoniati. E tutta la città era raunata dinanzi alla porta.»",
   3, "Poi", width=900, size=36, fade_at=LS[4] - 0.4)
S_(S1, "jesus-pied", 1500, 420, 210, AL("porta", 3) - 0.5, rot=2)
t4 = tag(S1, 90, 430, "Gesù guarisce… molti", AL("molti", 4) - 0.8, "acc", 52)
gone([t4], LS[5] - 0.5)
s5 = stamp(S1, 90, 440, "Quante?", AL("quante", 5) - 0.1, rot=-4, size=84)
gone([s5], LS[6] - 0.5)
c6 = counter(S1, 90, 420, 0, 20, AL("ventina", 6) - 1.6, 2.4, unit=" racconti", size=130)
t6 = tag(S1, 90, 640, "Il testo non dà nessun totale", AL("totale", 6) - 1.0, "acc", 44)
gone([c6, t6], LS[7] - 0.5)
t7 = [tag(S1, 90, 430, "La pelle", AL("pelle", 7) - 0.2, "", 42), tag(S1, 90, 530, "Gli occhi", AL("occhi", 7) - 0.2, "", 42),
      tag(S1, 90, 630, "Orecchie e parola", AL("orecchie", 7) - 0.2, "", 42), tag(S1, 90, 730, "Il movimento", AL("movimento", 7) - 0.2, "", 42),
      tag(S1, 800, 430, "Febbre e sangue", AL("febbre", 7) - 0.2, "", 42), tag(S1, 800, 530, "Gli spiriti", AL("spiriti", 7) - 0.2, "", 42),
      tag(S1, 800, 630, "La morte", AL("morte", 7) - 0.2, "acc", 42)]
s8 = stamp(S1, 700, 760, "I gesti cambiano", AL("gesti", 8) - 0.6, rot=-3, size=44)
gone(t7 + [s8], LS[9] - 0.5)
c9 = card(S1, 90, 420, "Il metodo", "Un racconto = una persona guarita, con la sua storia", AL("metodo", 9) - 0.3, w=900, size=38)
t9 = tag(S1, 90, 700, "Le folle guarite in blocco: sommari", AL("folle", 9) - 0.2, "", 42)
gone([c9, t9], LS[10] - 0.5)

# S2: la pelle (righe 10-18)
t = LS[10] - 0.4
cam(t, S2)
headline(S2, 170, ["La [pelle]"], t + 0.1, kicker="La lebbra", hl_t=AL("pelle", 10) + 0.05, size=110)
t10 = tag(S2, 90, 430, "La più temuta dell'epoca", AL("temuta", 10) - 0.4, "acc", 52)
gone([t10], LS[11] - 0.5)
c11 = card(S2, 90, 420, "La parola greca", "<b>lepra</b>: un insieme di affezioni della pelle", AL("lepra", 11) - 0.3, w=900, size=40)
t11 = [tag(S2, 90, 640, "Levitico 13", AL("Levitico", 11) - 0.2, "", 46), tag(S2, 90, 750, "Non per forza la lebbra di oggi", AL("forza", 11) - 0.5, "acc", 38)]
gone([c11] + t11, LS[12] - 0.5)
f12 = tag(S2, 90, 430, "Il malato vive in disparte", LS[12] + 0.2, "", 50)
fade(f12, AL("Impuro", 12) - 0.7)
s12 = stamp(S2, 90, 440, "Impuro!", AL("Impuro", 12) - 0.1, rot=-4, size=84)
t12 = tag(S2, 90, 640, "Un'esclusione, oltre che una malattia", AL("esclusione", 12) - 0.6, "acc", 46)
S_(S2, "lepreux", 1500, 420, 170, AL("malattia", 12) - 0.3, rot=-2)
gone([s12, t12], LS[13] - 0.5)
kq(S2, 90, 420, "Marco 1,40" + WEB, "«Se vuoi, tu puoi mondarmi.»", 13, "Se", width=900, size=44, fade_at=LS[14] - 0.4)
c14 = card(S2, 90, 420, "Marco 1,41", "«mosso a compassione»", AL("compassione", 14) - 0.5, w=800, size=44)
t14 = [tag(S2, 90, 620, "Alcuni manoscritti: «adirato»", AL("adirato", 14) - 0.4, "", 40), tag(S2, 90, 730, "Gli specialisti ne discutono", AL("discutono", 14) - 0.6, "acc", 40)]
gone([c14] + t14, LS[15] - 0.5)
s15 = stamp(S2, 90, 440, "Lo tocca", AL("Toccare", 15) - 0.1, rot=-4, size=72)
fade(s15, AL("sacerdote", 15) - 1.4)
c15 = card(S2, 90, 620, "Dice", "«Lo voglio, sii mondato.»", AL("voglio", 15) - 0.4, w=800, size=44, accent=True)
t15 = tag(S2, 90, 440, "Va' a presentarti al sacerdote", AL("sacerdote", 15) - 0.8, "", 46)
gone([c15, t15], LS[16] - 0.5)
c16 = card(S2, 90, 420, "Luca 17", "Dieci lebbrosi, da lontano: purificati lungo la strada", AL("dieci", 16) - 0.2, w=900, size=38)
t16 = tag(S2, 90, 650, "Gesù non li tocca", AL("tocca", 16) - 0.3, "", 46)
gone([c16, t16], LS[17] - 0.5)
S_(S2, "samaritain", 1100, 420, 260, AL("Samaritano", 17) - 0.8, rot=2)
t17 = [tag(S2, 90, 430, "Uno solo torna", AL("torna", 17) - 0.3, "", 52), tag(S2, 90, 540, "Un Samaritano, uno straniero", AL("Samaritano", 17) - 0.6, "acc", 50)]
gone(t17, LS[18] - 0.5)
teaser(S2, 90, 440, "Il seguito, sulla stessa linea", LS[18] + 0.3, hold=4.4)

# S3: la vista (righe 19-24)
t = LS[19] - 0.4
cam(t, S3)
headline(S3, 170, ["La [vista]"], t + 0.1, kicker="Seconda categoria", hl_t=AL("vista", 19) + 0.05, size=110)
t19 = tag(S3, 90, 430, "Una delle più frequenti", AL("frequenti", 19) - 0.6, "acc", 52)
gone([t19], LS[20] - 0.5)
jr = S_(S3, "jericho", 1100, 420, 380, AL("Gerico", 20) - 0.2, rot=2)
fade(jr, LS[21] - 0.5)
kq(S3, 90, 420, "Marco 10,47 · Bartimeo a Gerico", "«Figliuol di Davide, abbi pietà di me!»", 20, "Figliuol", width=800, size=40, fade_at=LS[21] - 0.4)
t20 = [tag(S3, 90, 700, "La folla gli dice di tacere", AL("tacere", 20) - 0.8, "", 44), tag(S3, 90, 800, "Grida più forte", AL("forte", 20) - 0.4, "acc", 46)]
gone(t20, LS[21] - 0.5)
S_(S3, "bartimee", 1500, 420, 190, AL("mantello", 21) - 0.4, rot=-2)
t21 = [tag(S3, 90, 430, "Getta via il mantello", AL("mantello", 21) - 0.4, "", 52), stamp(S3, 90, 580, "Vedere", AL("vedere", 21) - 0.4, rot=-4, size=96)]
S_(S3, "bartimee-portrait", 1100, 420, 280, AL("vedere", 21) - 0.3, rot=2)
gone(t21, LS[22] - 0.5)
kq(S3, 90, 420, "Marco 10,52" + WEB, "«Va', la tua fede ti ha salvato.»", 22, "Va", width=800, size=44, fade_at=LS[23] - 0.4)
c22 = card(S3, 90, 690, "Greco", "<b>sozo</b>: salvare e guarire", AL("sôzô", 22) - 0.3, w=800, size=40)
gone([c22], LS[23] - 0.5)
t23 = tag(S3, 90, 430, "Betsaida: in due tempi", AL("Betsaida", 23) - 0.3, "acc", 50)
fade(t23, AL("Vedo", 23) - 0.7)
c23 = card(S3, 90, 420, "Marco 8,24", "«Vedo gli uomini, perché li vedo camminare simili ad alberi.»", AL("Vedo", 23) - 0.4, w=800, size=40)
gone([c23], LS[24] - 0.5)
t24 = tag(S3, 90, 430, "Una guarigione per tappe", AL("tappe", 24) - 0.9, "acc", 56)
gone([t24], LS[25] - 0.5)

# S4: il cieco nato (righe 25-27)
t = LS[25] - 0.4
cam(t, S4)
headline(S4, 170, ["Il [cieco] nato"], t + 0.1, kicker="Giovanni 9", hl_t=AL("cieco", 25) + 0.05, size=96)
elg = S_(S4, "el-greco-aveugle", 1100, 420, 470, AL("cieco", 25) + 0.2, rot=2)
fade(elg, LS[26] - 0.5)
c25 = card(S4, 90, 420, "I discepoli chiedono", "Chi ha peccato, lui o i suoi genitori?", AL("peccato", 25) - 0.8, w=800, size=40)
s25 = stamp(S4, 90, 620, "Né l'uno né gli altri", AL("risponde", 25) - 0.3, rot=-3, size=56)
gone([c25, s25], LS[26] - 0.5)
t26 = [tag(S4, 90, 430, "Fango, saliva", AL("fango", 26) - 0.3, "", 48), tag(S4, 90, 540, "La piscina di Siloe", AL("Siloe", 26) - 0.3, "acc", 48),
       tag(S4, 90, 650, "Siloe: «mandato»", AL("mandato", 26) - 0.6, "", 48)]
S_(S4, "siloe", 1100, 420, 430, AL("Siloe", 26) - 0.3, rot=-2)
gone(t26, LS[27] - 0.5)
c27 = card(S4, 90, 420, "La sua sola risposta", "«Ero cieco, e ora ci vedo»", AL("ripete", 27) - 0.3, w=800, size=44)
t27 = tag(S4, 90, 700, "I genitori tacciono", AL("genitori", 27) - 0.3, "", 44)

# S5: udito e parola (righe 28-32)
t = LS[28] - 0.4
cam(t, S5)
headline(S5, 170, ["[Udito] e parola"], t + 0.1, kicker="Terza categoria", hl_t=AL("udito", 28) + 0.05, size=96)
t28 = tag(S5, 90, 430, "Sentire, parlare", AL("parola", 28) - 0.6, "acc", 52)
gone([t28], LS[29] - 0.5)
S_(S5, "villageois", 1500, 420, 250, AL("sordo", 29) - 0.3, rot=2)
t29 = [tag(S5, 90, 430, "La Decapoli", AL("Decapoli", 29) - 0.3, "", 52), tag(S5, 90, 540, "In disparte, lontano dalla folla", AL("disparte", 29) - 0.3, "", 46),
       tag(S5, 90, 650, "Dita, saliva, un sospiro", AL("saliva", 29) - 0.3, "acc", 46)]
gone(t29, LS[30] - 0.5)
c30 = card(S5, 90, 420, "Una parola aramaica", "<b>Effatà</b>: «apriti»", AL("Effatà", 30) - 0.6, w=800, size=48)
burst(S5, 1000, 520, AL("Effatà", 30) - 0.2)
gone([c30], LS[31] - 0.5)
kq(S5, 90, 420, "Marco 7,37" + WEB, "«Egli ha fatto bene ogni cosa; fa udire i sordi e parlare i muti.»", 31, "Egli", width=900, size=42, fade_at=LS[32] - 0.4)
tag(S5, 90, 430, "Un muto", AL("muto", 32) - 0.3, "", 52)
tag(S5, 90, 540, "Uno spirito cattivo, scacciato", AL("spirito", 32) - 0.3, "", 46)
tag(S5, 90, 650, "Parla", AL("parla", 32) - 0.3, "acc", 52)

# S6: il movimento (righe 33-39)
t = LS[33] - 0.4
cam(t, S6)
headline(S6, 170, ["Il [movimento]"], t + 0.1, kicker="Quarta categoria", hl_t=AL("movimento", 33) + 0.05, size=104)
f33 = tag(S6, 90, 430, "Paralitici · mani · schiene", LS[33] + 0.4, "acc", 52)
fade(f33, LS[34] - 0.5)
p34 = S_(S6, "porteurs", 90, 420, 480, AL("quattro", 34) - 0.3, rot=-2)
t34 = [tag(S6, 700, 430, "Quattro uomini", AL("quattro", 34) - 0.3, "", 50), tag(S6, 700, 540, "Il tetto scoperchiato", AL("tetto", 34) - 0.3, "acc", 50)]
gone([p34] + t34, LS[35] - 0.5)
pd = S_(S6, "paralytique-dessin", 1100, 420, 420, AL("fede", 35) - 0.3, rot=2)
fade(pd, LS[36] - 0.5)
kq(S6, 90, 420, "Marco 2,5" + WEB, "«Figliuolo, i tuoi peccati ti sono rimessi.»", 35, "Figliuolo", width=800, size=44, fade_at=LS[36] - 0.4)
t35 = [tag(S6, 90, 700, "Alcuni scribi si indignano", AL("scribi", 35) - 0.3, "", 44), tag(S6, 90, 800, "Ordina: alzati", AL("ordina", 35) - 0.3, "acc", 44)]
gone(t35, LS[36] - 0.5)
c36 = card(S6, 90, 420, "Betesda · Giovanni 5", "Malato da trentotto anni", AL("trentotto", 36) - 0.6, w=800, size=44)
t36 = tag(S6, 90, 620, "«Vuoi tu esser guarito?»", AL("Vuoi", 36) - 0.3, "acc", 52)
bd = S_(S6, "bethesda-dessin", 1100, 420, 420, AL("Betesda", 36) - 0.5, rot=-2)
fade(bd, LS[38] - 0.5)
gone([c36, t36], LS[37] - 0.5)
t37 = [tag(S6, 90, 430, "Una moltitudine di malati", AL("moltitudine", 37) - 0.3, "", 52), tag(S6, 90, 540, "Una sola guarigione raccontata", AL("soltanto", 37) - 0.3, "acc", 46)]
gone(t37, LS[38] - 0.5)
f38 = tag(S6, 90, 430, "Una mano inaridita", LS[38] + 0.2, "acc", 52)
fade(f38, AL("Stendi", 38) - 1.2)
c38 = card(S6, 90, 420, "Di sabato", "«Stendi la mano»", AL("Stendi", 38) - 0.8, w=800, size=48)
t38 = tag(S6, 90, 620, "E la discussione comincia", AL("discussione", 38) - 0.3, "", 44)
gone([c38, t38], LS[39] - 0.5)
S_(S6, "femme-courbee", 1500, 420, 215, AL("curva", 39) - 0.3, rot=2)
tag(S6, 90, 430, "Diciotto anni", AL("diciotto", 39) - 0.3, "", 56)
tag(S6, 90, 540, "«Figliuola d'Abramo»", AL("Abramo", 39) - 0.6, "acc", 52)
tag(S6, 90, 650, "Si raddrizza", AL("raddrizza", 39) - 0.3, "", 48)

# S7: febbre e sangue (righe 40-46)
t = LS[40] - 0.4
cam(t, S7)
headline(S7, 170, ["La [febbre] e il sangue"], t + 0.1, kicker="Quinta categoria", hl_t=AL("febbre", 40) + 0.05, size=96)
f40 = tag(S7, 90, 430, "Febbre e sangue", LS[40] + 0.3, "acc", 52)
fade(f40, LS[41] - 0.5)
t41 = [tag(S7, 90, 430, "La suocera di Pietro", AL("suocera", 41) - 0.3, "", 50), tag(S7, 90, 540, "La prende per la mano", AL("mano", 41) - 0.3, "", 46),
       tag(S7, 90, 650, "Si mette a servirli", AL("servirli", 41) - 0.5, "acc", 46)]
gone(t41, LS[42] - 0.5)
f42 = [tag(S7, 90, 430, "Un ufficiale del re", LS[42] + 0.3, "", 52), tag(S7, 90, 540, "Suo figlio sta morendo", AL("morendo", 42) - 0.4, "", 50)]
gone(f42, AL("Va", 42) - 0.8)
kq(S7, 90, 420, "Giovanni 4,50" + WEB, "«Va', tuo figlio vive.»", 42, "Va", width=700, size=48, fade_at=LS[43] - 0.4)
t42 = tag(S7, 90, 700, "A distanza: la stessa ora", AL("ora", 42) - 0.5, "acc", 44)
gone([t42], LS[43] - 0.5)
ce = S_(S7, "centurion", 1500, 420, 190, AL("centurione", 43) - 0.3, rot=2)
t43 = [tag(S7, 90, 430, "Un centurione romano", AL("centurione", 43) - 0.3, "", 50), tag(S7, 90, 540, "Basta una parola", AL("basta", 43) - 0.4, "acc", 52),
       tag(S7, 90, 650, "Guarito a distanza", AL("distanza", 43) - 0.3, "", 48)]
gone([ce] + t43, LS[44] - 0.5)
S_(S7, "femme-sang", 1100, 420, 380, AL("speso", 44) - 1.2, rot=-2)
t44 = [tag(S7, 90, 430, "Dodici anni", AL("Poi", 44) - 0.1, "", 56), tag(S7, 90, 540, "Nessun sollievo", AL("sollievo", 44) - 0.8, "acc", 44)]
pr = S_(S7, "pince-romaine", 90, 660, 330, AL("speso", 44) - 0.5, rot=-3)
gone(t44 + [pr], LS[45] - 0.5)
c45 = card(S7, 90, 420, "Si dice", "«Se tocco soltanto le sue vesti, sarò guarita.»", AL("tocco", 45) - 1.0, w=800, size=36)
t45a = tag(S7, 90, 700, "Il flusso si ferma", AL("flusso", 45) - 0.3, "acc", 50)
fade(t45a, AL("Chi", 45) - 0.7)
t45 = [t45a, tag(S7, 90, 700, "«Chi mi ha toccato le vesti?»", AL("Chi", 45) - 0.3, "", 42)]
gone([c45] + t45, LS[46] - 0.5)
kq(S7, 90, 420, "Marco 5,34" + WEB, "«Figliuola, la tua fede ti ha salvata; vattene in pace, e sii guarita dal tuo male.»", 46, "figliuola", width=800, size=40, fade_at=LS[47] - 0.4)

# S8: gli spiriti (righe 47-52)
t = LS[47] - 0.4
cam(t, S8)
headline(S8, 170, ["Gli [spiriti]"], t + 0.1, kicker="Sesta categoria", hl_t=AL("spiriti", 47) + 0.05, size=104)
f47 = tag(S8, 90, 430, "Spiriti immondi", LS[47] + 0.3, "acc", 52)
fade(f47, AL("distinguono", 47) - 0.9)
t47 = [tag(S8, 90, 430, "Malattia o spirito immondo", AL("distinguono", 47) - 0.6, "", 52), tag(S8, 90, 540, "Spesso distinti", AL("legati", 47) - 0.9, "acc", 52)]
gone(t47, LS[48] - 0.5)
f48 = tag(S8, 90, 430, "Un vecchio dibattito", LS[48] + 0.3, "", 52)
fade(f48, AL("diagnosi", 48) - 1.3)
c48 = card(S8, 90, 420, "Gli specialisti ne discutono", "Nessuna diagnosi medica nel testo", AL("diagnosi", 48) - 0.9, w=900, size=40)
s48 = stamp(S8, 90, 640, "Nessuna diagnosi", AL("diagnosi", 48) - 0.3, rot=-3, size=60)
gone([c48, s48], LS[49] - 0.5)
S_(S8, "jesus-pied", 1500, 420, 210, AL("sinagoga", 49) - 0.3, rot=2)
kq(S8, 90, 420, "Marco 1,24" + WEB, "«Io so chi sei: il Santo di Dio.»", 49, "Io", width=900, size=44, fade_at=LS[50] - 0.4)
t49 = [tag(S8, 90, 700, "Ordina di uscire", AL("ordina", 49) - 0.3, "", 44), tag(S8, 90, 800, "Parla con autorità", AL("autorità", 49) - 0.6, "acc", 44)]
gone(t49, LS[50] - 0.5)
t50 = [tag(S8, 90, 430, "Il paese dei Geraseni", AL("Geraseni", 50) - 0.3, "", 50), tag(S8, 90, 540, "Fra le tombe", AL("tombe", 50) - 0.3, "", 48),
       tag(S8, 90, 650, "Seduto, vestito, in senno", AL("senno", 50) - 0.8, "acc", 44)]
gone(t50, LS[51] - 0.5)
pf = S_(S8, "pere-fils", 1100, 420, 165, AL("padre", 51) - 0.3, rot=-2)
kq(S8, 90, 420, "Marco 9,23" + WEB, "«Ogni cosa è possibile a chi crede.»", 51, "Ogni", width=800, size=42, fade_at=LS[52] - 0.4)
c51 = card(S8, 90, 690, "Il padre risponde", "«Io credo; aiuta la mia incredulità!»", AL("incredulità", 51) - 0.8, w=800, size=36)
gone([pf, c51], LS[52] - 0.5)
t52 = [tag(S8, 90, 430, "Una madre cananea", AL("cananea", 52) - 0.3, "", 52), tag(S8, 90, 540, "Una straniera", AL("straniera", 52) - 0.3, "", 48)]
kq(S8, 90, 650, "Matteo 15,28" + WEB, "«O donna, grande è la tua fede!»", 52, "O", width=800, size=44)

# S9: la morte (righe 53-57)
t = LS[53] - 0.4
cam(t, S9)
headline(S9, 170, ["La [morte]"], t + 0.1, kicker="Ultima categoria", hl_t=AL("morte", 53) + 0.05, size=110)
t53 = tag(S9, 90, 430, "Tre volte, restituisce la vita", LS[53] + 0.3, "acc", 52)
gone([t53], LS[54] - 0.5)
fj = S_(S9, "fille-jairus", 1500, 420, 150, AL("figlia", 54) - 0.3, rot=2)
t54 = tag(S9, 90, 430, "La figlia di Iairo · dodici anni", AL("figlia", 54) - 0.3, "", 52)
c54 = card(S9, 90, 560, "In aramaico", "<b>Talità kum</b>: «fanciulla, alzati»", AL("Talità", 54) - 0.3, w=800, size=40)
gone([fj, t54, c54], LS[55] - 0.5)
vc = S_(S9, "veuve-cortege", 90, 420, 520, AL("Nain", 55) - 0.3, rot=-2)
t55 = [tag(S9, 760, 430, "Nain", AL("Nain", 55) - 0.3, "", 52), tag(S9, 760, 540, "Il figlio unico di una vedova", AL("vedova", 55) - 0.3, "", 46),
       tag(S9, 760, 650, "«Alzati»", AL("Alzati", 55) - 0.3, "acc", 52)]
gone([vc] + t55, LS[56] - 0.5)
lz = S_(S9, "lazare", 1500, 420, 220, AL("Lazzaro", 56) - 0.3, rot=2)
lg = S_(S9, "lazare-gravure", 1000, 420, 400, AL("Lazzaro", 56) - 0.2, rot=-2)
t56 = [tag(S9, 90, 430, "Morto da quattro giorni", AL("quattro", 56) - 0.3, "", 50), tag(S9, 90, 540, "Gesù piange", AL("piange", 56) - 0.3, "", 52),
       tag(S9, 90, 650, "«Lazzaro, vieni fuori!»", AL("grida", 56) - 0.4, "acc", 52)]
gone([lg] + t56, LS[57] - 0.5)
c57 = card(S9, 90, 420, "Tradizione cristiana", "Segni che annunciano la risurrezione di Gesù", AL("segni", 57) - 0.4, w=900, size=38)
t57 = tag(S9, 90, 690, "Lettura abituale: poi morti di nuovo", AL("morte", 57) - 0.9, "", 40)

# S10: il quadro d'insieme (righe 58-64)
t = LS[58] - 0.4
cam(t, S10)
headline(S10, 170, ["Il quadro [d'insieme]"], t + 0.1, kicker="Che cosa hanno in comune", hl_t=AL("insieme", 58) + 0.05, size=96)
t58 = [tag(S10, 90, 430, "In comune?", AL("comune", 58) - 0.4, "", 52), tag(S10, 90, 540, "Differenze?", AL("differiscono", 58) - 0.3, "acc", 52)]
gone(t58, LS[59] - 0.5)
g59 = [card(S10, 90, 420, "Un gesto", "Una parola", AL("parola", 59) - 0.3, w=400, size=32),
       card(S10, 580, 420, "Un gesto", "Un contatto", AL("contatto", 59) - 0.3, w=400, size=32),
       card(S10, 90, 640, "Un gesto", "Fango, saliva", AL("fango", 59) - 0.3, w=400, size=32),
       card(S10, 580, 640, "Un gesto", "A distanza", AL("distanza", 59) - 0.3, w=400, size=32, accent=True)]
gone(g59, LS[60] - 0.5)
f60 = tag(S10, 90, 430, "La fede: spesso, non sempre", LS[60] + 0.3, "acc", 52)
fade(f60, AL("malato", 60) - 0.7)
g60 = [card(S10, 90, 420, "La fede", "Quella del malato", AL("malato", 60) - 0.3, w=400, size=32),
       card(S10, 580, 420, "La fede", "Quella dei suoi amici", AL("amici", 60) - 0.3, w=400, size=32),
       card(S10, 90, 640, "La fede", "Di un padre, di un centurione", AL("centurione", 60) - 0.3, w=400, size=32),
       card(S10, 580, 640, "La fede", "A volte, non si dice nulla", AL("cieco", 60) - 0.6, w=400, size=32, accent=True)]
gone(g60, LS[61] - 0.5)
t61 = tag(S10, 90, 430, "Non guarisce sempre", LS[61] + 0.3, "acc", 52)
fade(t61, AL("poté", 61) - 0.7)
kq(S10, 90, 420, "Marco 6,5" + WEB, "«non poté far quivi alcun miracolo, salvo che, imposte le mani a pochi infermi, li guarì.»", 61, "poté", width=950, size=38,
   fade_at=LS[62] - 0.4)
f62 = tag(S10, 90, 430, "La risposta a Giovanni Battista", LS[62] + 0.3, "acc", 52)
fade(f62, AL("ciechi", 62) - 0.8)
kq(S10, 90, 420, "Matteo 11,5" + WEB,
   "«i ciechi ricuperano la vista, gli zoppi camminano, i lebbrosi son mondati, i sordi odono, i morti risuscitano, e a' poveri è annunziata la buona novella.»",
   62, "ciechi", width=950, size=38, fade_at=LS[63] - 0.4)
f63 = tag(S10, 90, 430, "Nota bene", LS[63] + 0.1, "acc", 52)
fade(f63, AL("categorie", 63) - 0.8)
s63 = stamp(S10, 90, 440, "Le nostre categorie", AL("categorie", 63) - 0.5, rot=-3, size=60)
c63 = card(S10, 90, 620, "Isaia 35 · Isaia 61", "Un'eco delle promesse di Isaia", AL("Isaia", 63) - 0.3, w=800, size=38)
gone([s63, c63], LS[64] - 0.5)
f64 = tag(S10, 90, 430, "Non solo sollievi", LS[64] + 0.2, "", 46)
fade(f64, AL("sollievi", 64) - 0.7)
S_(S10, "cent-florins", 1100, 420, 470, AL("segni", 64) - 0.5, rot=-2)
tag(S10, 90, 430, "Non solo sollievi", AL("sollievi", 64) - 0.5, "", 46)
tag(S10, 90, 540, "In Giovanni: segni", AL("segni", 64) - 0.3, "acc", 50)
tag(S10, 90, 650, "Comincia qualcosa di nuovo", AL("nuovo", 64) - 0.4, "", 44)

# S11: quando la guarigione non arriva (righe 65-69)
t = LS[65] - 0.4
cam(t, S11)
headline(S11, 170, ["Quando la guarigione [non arriva]"], t + 0.1, kicker="Il Nuovo Testamento", hl_t=AL("guarigione", 67) + 0.05, size=84)
f65 = tag(S11, 90, 430, "Malati non guariti", LS[65] + 0.3, "", 48)
fade(f65, AL("spina", 65) - 0.9)
pa = S_(S11, "paul", 1500, 420, 160, AL("Paolo", 65) - 0.3, rot=-2)
fade(pa, LS[66] - 0.5)
t65 = [tag(S11, 90, 430, "Paolo: una spina nella carne", AL("spina", 65) - 0.5, "", 48), tag(S11, 90, 540, "Chiede tre volte", AL("tre", 65) - 0.3, "acc", 48)]
gone(t65, AL("risposta", 65) - 0.7)
kq(S11, 90, 420, "2 Corinzi 12,9" + WEB, "«La mia grazia ti basta, perché la mia potenza si compie nella debolezza.»", 65, "La", n=2, width=900, size=42, fade_at=LS[66] - 0.4)
f66 = tag(S11, 90, 430, "In un'altra lettera", LS[66] + 0.3, "", 52)
fade(f66, AL("Trofimo", 66) - 0.7)
t66 = tag(S11, 90, 430, "Trofimo, malato a Mileto", AL("Trofimo", 66) - 0.3, "", 52)
gone([t66], LS[67] - 0.5)
c67 = card(S11, 90, 420, "Se preghi per una guarigione", "I testi non dicono che ti manca la fede", LS[67] + 0.3, w=900, size=38)
t67 = tag(S11, 90, 640, "Né che la tua sofferenza non conti", AL("conti", 67) - 1.6, "acc", 40)
gone([c67, t67], LS[68] - 0.5)
f68 = tag(S11, 90, 430, "Se sei malato", LS[68] + 0.3, "acc", 52)
fade(f68, AL("medico", 68) - 0.8)
S_(S11, "mains-lampe", 1500, 420, 300, AL("medico", 68) - 0.3, rot=2)
t68 = [tag(S11, 90, 430, "Consultare un medico", AL("medico", 68) - 0.3, "", 52), tag(S11, 90, 540, "Non si oppone alla fede", AL("oppone", 68) - 0.3, "acc", 50),
       tag(S11, 90, 650, "Luca, «il medico diletto»", AL("diletto", 68) - 0.5, "", 46)]
gone(t68, LS[69] - 0.5)
t69 = tag(S11, 90, 430, "Quale ti tocca di più?", AL("quale", 69) - 0.3, "acc", 56)
cta = put(S11, 90, 600, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Dillo nei commenti', "cta")
blur_in(cta, AL("commenti", 69) - 1.2, 14)
sfx("click", AL("commenti", 69) - 1.2, 0.8)

# S1 rivisitata: conclusione (righe 70-73)
cam(LS[70] - 2.0, "all")
wipe(S1, LS[70] - 2.1)
t = LS[70] - 0.4
cam(t, S1)
headline(S1, 170, ["Davanti a ognuna, [si ferma]"], t + 0.1, kicker="Cafarnao", hl_t=AL("ferma", 71) + 0.05, size=88)
S_(S1, "foule", 1500, 420, 300, AL("porta", 70) - 0.3, rot=2)
kq(S1, 90, 420, "Marco 1,34" + WEB, "«Egli ne guarì molti che soffrivano di varie malattie.»", 70, "Egli", width=900, size=44, fade_at=LS[71] - 0.4)
t71 = [tag(S1, 90, 430, "La pelle", AL("pelle", 71) - 0.1, "", 50), tag(S1, 90, 540, "Gli occhi", AL("occhi", 71) - 0.1, "", 50), tag(S1, 90, 650, "La voce", AL("voce", 71) - 0.1, "", 50),
       tag(S1, 800, 430, "Le gambe", AL("gambe", 71) - 0.1, "", 50), tag(S1, 800, 540, "Il sangue", AL("sangue", 71) - 0.1, "", 50), tag(S1, 800, 650, "La morte", AL("morte", 71) - 0.1, "", 50)]
gone(t71, LS[72] - 0.5)
t72 = [tag(S1, 90, 430, "Troppo lontano", AL("lontano", 72) - 0.1, "", 52), tag(S1, 90, 540, "Troppo impuro", AL("impuro", 72) - 0.1, "", 52),
       tag(S1, 90, 650, "Troppo malato", AL("malato", 72) - 0.1, "", 52), tag(S1, 90, 760, "Troppo morto", AL("morto", 72) - 0.1, "", 52),
       stamp(S1, 800, 540, "Si ferma", AL("fermi", 72) - 0.3, rot=-3, size=84)]
gone(t72, LS[73] - 0.3)

t_end = AL("Altri", 73) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(LS[70] - 2.8, LS[70] - 0.5), (AL("Altri", 73) - 0.8, DUR_)]
build(
    chapters=[("01", "La porta di Cafarnao", 0, LS[10]), ("02", "La pelle", LS[10], LS[19]), ("03", "La vista", LS[19], LS[28]), ("04", "Udito e movimento", LS[28], LS[40]),
              ("05", "Febbre, spiriti, morte", LS[40], LS[58]), ("06", "Il quadro d'insieme", LS[58], DUR_)],
    suppress=supp,
    endcard={"kicker": "Ogni settimana", "title": "La Bibbia<br />[Semplice]", "button": "Iscriviti",
             "stickers": [("jesus-portrait", 150, 560, 300, -6), ("bartimee-portrait", 1550, 330, 220, 5)]},
    endcard_t=AL("Altri", 73) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
