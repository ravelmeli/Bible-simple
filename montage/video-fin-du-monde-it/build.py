"""Video lunga « Profezie sulla fine del mondo (2027, Nostradamus): che cosa dice la Bibbia? » (La Bibbia Semplice) — style 02, 16:9, 623.5 s. Versione italiana di montage/video-fin-du-monde/.

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

THEME = {"brand": "La Bibbia Semplice", "title": "La Bibbia Semplice - Profezie sulla fine del mondo - style 02", "lang": "it",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
DUR_ = 623.5
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
S11, S12, S13 = (0, 2), (1, 2), (2, 2)
WEB = "Riveduta"

html.append('<style>'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')

# =====================================================================  S1: date annunciate (righe 1-7)
cam(0, S1)
headline(S1, 170, ["La fine del mondo, [rimandata]"], 0.0, kicker="Annunci", hl_t=AL("rimandata", 1) + 0.05, size=88)
v0 = S_(S1, "villageois", 1100, 420, 300, 0.0, rot=-3, instant=True)
fade(v0, LS[2] - 0.2)
tg1 = [tag(S1, 90, 430, "Annunciata", AL("annunciata", 1) - 0.1, "", 56), tag(S1, 90, 540, "Rimandata", AL("rimandata", 1) - 0.1, "acc", 56)]
gone(tg1, LS[2] - 0.2)
an = S_(S1, "animateur", 1500, 420, 190, LS[2] - 0.1, rot=2)
c1 = card(S1, 90, 420, "Annuncio di Harold Camping", "21 maggio 2011", AL("Camping", 2) - 0.2, w=700, size=56)
st1 = stamp(S1, 90, 660, "Niente", AL("niente", 3) + 0.1, rot=-4, size=72)
gone([c1, st1], AL("corregge", 3) - 0.2)
c2 = card(S1, 90, 420, "Annuncio corretto", "21 ottobre 2011", AL("corregge", 3) + 0.2, w=760, size=56, accent=True)
st2 = stamp(S1, 90, 660, "Ancora niente", AL("niente", 4) + 0.1, rot=-3, size=64)
gone([c2, st2, an], LS[5] - 0.15)
cn = counter(S1, 90, 420, 2011, 2027, AL("duemilaventisette", 5) - 0.8, 2.2, size=170)
tn = [tag(S1, 800, 440, "Nostradamus", AL("Nostradamus", 5) - 0.1, "", 52), tag(S1, 800, 550, "Quartine", AL("quartine", 5) - 0.1, "acc", 52)]
gone([cn] + tn, LS[6] - 0.5)
tq = tag(S1, 90, 440, "La Bibbia dice quando?", AL("Bibbia", 6) - 0.4, "acc", 56)
v6 = S_(S1, "villageois", 1100, 420, 300, AL("credenti", 6) - 0.3, rot=2)
ring(S1, 1260, 600, AL("angoscia", 6), size=260)
gone([tq], LS[7] - 0.5)
tx = [tag(S1, 90, 430, "Il testo", AL("testo", 7) - 0.1, "", 54), tag(S1, 90, 540, "La storia", AL("storia", 7) - 0.1, "", 54),
      tag(S1, 90, 650, "La risposta di Gesù", AL("Gesù", 7) - 0.1, "acc", 54)]

# =====================================================================  S2: Nostradamus (righe 8-14)
t = LS[8] - 0.4
cam(t, S2)
headline(S2, 170, ["[Nostradamus]"], t + 0.1, kicker="Le Profezie, 1555", hl_t=AL("Nostradamus", 8) + 0.05, size=104)
S_(S2, "nostradamus-pied", 1500, 420, 160, AL("Nostradamus", 8) - 0.2, rot=-2)
t8 = tag(S2, 90, 430, "Un nome che ritorna sempre", AL("ritorna", 8) - 0.5, "", 50)
fade(t8, LS[9] - 0.5)
c9 = card(S2, 90, 420, "Michel de Nostredame", "medico e astrologo · 1503-1566", AL("Michel", 9) - 0.1, w=900, size=38)
fade(c9, LS[10] - 0.5)
n10 = counter(S2, 90, 420, 1500, 1555, AL("millecinquecentocinquantacinque", 10) - 0.2, 2.0, size=150)
t10 = [tag(S2, 90, 620, "Lione · Le Profezie", AL("Lione", 10) - 0.2, "acc", 46), tag(S2, 90, 740, "Quartine volutamente oscure", AL("oscure", 10) - 1.0, "", 40)]
ast = S_(S2, "astrolabe", 1050, 420, 260, AL("Profezie", 10) - 0.2, rot=3)
fade(ast, LS[12] - 0.5)
gone([n10] + t10, LS[11] - 0.5)
t11 = [tag(S2, 90, 430, "Versi molto vaghi", AL("vaghi", 11) - 0.3, "acc", 56), tag(S2, 90, 560, "Senso trovato a cose fatte", AL("fatte", 11) - 1.0, "", 50)]
gone(t11, LS[12] - 0.5)
c12 = card(S2, 90, 420, "Celebre quartina", "«anno millenovecentonovantanove, sette mesi»", AL("quartina", 12) - 0.1, w=900, size=36)
t12 = [tag(S2, 90, 640, "Un grande re di terrore", AL("re", 12) - 0.3, "", 46), stamp(S2, 900, 640, "Niente", AL("niente", 12), rot=-4, size=64),
       tag(S2, 90, 760, "Poi, una nuova lettura", AL("reinterpretato", 12) - 1.0, "acc", 40)]
gone([c12] + t12, LS[13] - 0.5)
s13 = stamp(S2, 90, 430, "Falsa", AL("falsa", 13) - 0.2, rot=-4, size=84)
t13 = [tag(S2, 90, 640, "Scritta negli anni Novanta da uno studente", AL("studente", 13) - 0.6, "", 40),
       tag(S2, 90, 750, "Attribuita a torto a Nostradamus", AL("vago", 13) - 1.4, "acc", 40)]
gone([s13] + t13, LS[14] - 0.5)
teaser(S2, 90, 440, "Il seguito chiarisce molte cose", AL("pazienza", 14) - 0.5, hold=4.6)

# =====================================================================  S3: la prova biblica (righe 15-19)
t = LS[15] - 0.4
cam(t, S3)
headline(S3, 170, ["La [prova] del profeta"], t + 0.1, kicker="Deuteronomio 18", hl_t=AL("test", 16) + 0.05, size=96)
t15 = tag(S3, 90, 430, "La Bibbia giudica in altro modo", AL("giudica", 15) - 0.3, "acc", 52)
fade(t15, LS[16] - 0.5)
S_(S3, "rouleau", 1500, 420, 230, AL("Deuteronomio", 16) - 0.2, rot=3)
f16 = tag(S3, 90, 430, "Dio dà un test", LS[16] + 0.5, "acc", 52)
fade(f16, AL("Quando", 16) - 0.6)
kq(S3, 90, 420, "Deuteronomio 18,22 · " + WEB,
   "«Quando ciò che il profeta avrà detto non avverrà e non si compirà, quella sarà una parola che l'Eterno non ha detta.»",
   16, "Quando", width=900, size=38, fade_at=LS[17] - 0.4)
t17 = [tag(S3, 90, 430, "Una predizione precisa", AL("precisa", 17) - 0.6, "", 52), tag(S3, 90, 540, "Non si realizza: non viene da Dio", AL("realizza", 17) - 0.3, "acc", 46)]
gone(t17, LS[18] - 0.5)
t18 = tag(S3, 90, 430, "Il profeta chiama a tornare", AL("tornare", 18) - 0.8, "acc", 52)
gone([t18], LS[19] - 0.5)
S_(S3, "jonas", 1100, 420, 220, AL("Giona", 19) - 0.3, rot=-3)
card(S3, 90, 420, "Giona 3,4", "«Ancora quaranta giorni, e Ninive sarà distrutta»", AL("Ancora", 19) - 0.2, w=760, size=36)
tag(S3, 90, 640, "La città si pente", AL("pente", 19) - 0.3, "", 46)
tag(S3, 90, 750, "Lo scopo: la conversione", AL("conversione", 19) - 0.4, "acc", 46)

# =====================================================================  S4: la domanda a Gesù (righe 20-24)
t = LS[20] - 0.4
cam(t, S4)
headline(S4, 170, ["Che cosa dice [Gesù]?"], t + 0.1, kicker="Matteo 24", hl_t=AL("Gesù", 20) + 0.05, size=96)
S_(S4, "jesus-pied", 1500, 420, 210, AL("Gesù", 20) - 0.3, rot=2)
t20 = tag(S4, 90, 430, "La data della fine?", AL("data", 20) - 0.2, "acc", 56)
fade(t20, LS[21] - 0.5)
kq(S4, 90, 420, "Matteo 24,3 · " + WEB,
   "«Dicci, quando avverranno queste cose, e quale sarà il segno della tua venuta e della fine dell'età presente?»", 21, "Dicci", width=900, size=40,
   fade_at=LS[22] - 0.4)
c22 = card(S4, 90, 420, "In greco", "<b>synteleia tou aionos</b>", AL("synteleia", 22) - 0.2, w=760, size=40)
t22 = tag(S4, 90, 600, "Il compimento di un'età", AL("compimento", 22) - 0.4, "acc", 50)
gone([c22, t22], LS[23] - 0.5)
a23 = S_(S4, "arc-titus", 90, 420, 360, AL("tempio", 23) - 0.3, rot=-2)
s23 = stamp(S4, 640, 450, "Anno 70", AL("settanta", 23) - 0.2, rot=-4, size=72)
t23 = tag(S4, 640, 610, "Il tempio distrutto", AL("distrutto", 23), "", 48)
gone([a23, s23, t23], LS[24] - 0.5)
tag(S4, 90, 430, "Lettura 1: l'anno 70", AL("parte", 24) - 0.4, "", 52)
tag(S4, 90, 560, "Lettura 2: la fine dei tempi", AL("tempi", 24) - 0.2, "acc", 52)

# =====================================================================  S5: il giorno e l'ora (righe 25-28)
t = LS[25] - 0.4
cam(t, S5)
headline(S5, 170, ["Il giorno e [l'ora]"], t + 0.1, kicker="Matteo 24,36", hl_t=AL("ora", 25) + 0.05, size=96)
S_(S5, "jesus-portrait", 1500, 420, 250, AL("Gesù", 25) - 0.3, rot=3)
kq(S5, 90, 420, "Matteo 24,36 · " + WEB,
   "«Ma quanto a quel giorno e a quell'ora nessuno li sa, neppure gli angeli de' cieli, né il Figliuolo, ma il Padre solo.»", 25, "Ma", n=1,
   width=950, size=40, fade_at=LS[26] - 0.4)
t26 = [tag(S5, 90, 430, "Marco: la stessa parola", AL("Marco", 26) - 0.2, "", 52), tag(S5, 90, 540, "Il giorno resta il segreto del Padre", AL("segreto", 26) - 0.8, "acc", 46)]
gone(t26, LS[27] - 0.5)
kq(S5, 90, 420, "Atti 1,7 · " + WEB,
   "«Non spetta a voi di sapere i tempi o i momenti che il Padre ha riservato alla sua propria autorità.»", 27, "Non", width=950, size=38,
   fade_at=LS[28] - 0.4)
stamp(S5, 90, 440, "Contraddice", AL("contraddice", 28) - 0.2, rot=-4, size=84)
tag(S5, 90, 670, "Basta rileggere Matteo", AL("rileggere", 28) - 0.6, "acc", 50)

# =====================================================================  S6: i segni (righe 29-32)
t = LS[29] - 0.4
cam(t, S6)
headline(S6, 170, ["E i [segni]?"], t + 0.1, kicker="Matteo 24,4-6", hl_t=AL("segni", 29) + 0.05, size=96)
t29 = tag(S6, 90, 430, "Guarda come comincia", AL("guarda", 29) - 0.3, "", 52)
fade(t29, LS[30] - 0.5)
S_(S6, "cavaliers", 1500, 420, 290, AL("guerre", 30) - 0.3, rot=2)
kq(S6, 90, 420, "Matteo 24,4-6 · " + WEB,
   "«Guardate che nessuno vi seduca. Perché molti verranno nel mio nome, dicendo: Io sono il Cristo; e ne sedurranno molti. "
   "Voi udrete parlare di guerre e di rumori di guerre; guardate di non turbarvi, perché bisogna che avvenga così; ma non sarà ancora la fine.»",
   30, "Guardate", width=1050, size=30, fade_at=LS[31] - 0.4)
t31 = [tag(S6, 90, 430, "Nessun calendario", AL("calendario", 31) - 0.6, "", 52), tag(S6, 90, 540, "Un avvertimento", AL("avvertimento", 31) - 0.3, "acc", 52),
       tag(S6, 90, 650, "Contro l'inganno e il panico", AL("panico", 31) - 1.2, "", 44)]
gone(t31, LS[32] - 0.5)
card(S6, 90, 420, "Gesù dice", "«non sarà ancora la fine»", AL("fine", 32, 1) - 0.2, w=780, size=48)
stamp(S6, 90, 680, "Non un conto alla rovescia", AL("conto", 32) - 0.2, rot=-3, size=48)

# =====================================================================  S7: Paolo e Pietro (righe 33-36)
t = LS[33] - 0.4
cam(t, S7)
headline(S7, 170, ["Paolo e [Pietro]"], t + 0.1, kicker="1 Tessalonicesi · 2 Pietro", hl_t=AL("Pietro", 35) + 0.05, size=96)
S_(S7, "paul", 1500, 420, 170, AL("Paolo", 33) - 0.3, rot=-2)
t33 = [tag(S7, 90, 430, "Tessalonica", AL("Tessalonica", 33) - 0.3, "", 52), tag(S7, 90, 540, "Non lasciarsi turbare", AL("turbare", 33) - 0.6, "acc", 46)]
gone(t33, LS[34] - 0.5)
kq(S7, 90, 420, "1 Tessalonicesi 5,2 · " + WEB, "«il giorno del Signore verrà come un ladro nella notte»", 34, "il", width=900, size=42,
   last=AL("notte", 34) + 0.5, fade_at=LS[35] - 0.4)
t34 = tag(S7, 90, 700, "Un ladro non avverte", AL("avverte", 34) - 0.6, "acc", 50)
gone([t34], LS[35] - 0.5)
S_(S7, "sablier", 1250, 420, 110, AL("Pietro", 35) - 0.2, rot=2)
kq(S7, 90, 420, "2 Pietro 3,8-9 · " + WEB,
   "«davanti al Signore un giorno è come mille anni, e mille anni sono come un giorno. Il Signore non ritarda l'adempimento della sua promessa, come alcuni stimano che faccia; "
   "ma è paziente verso di voi, non volendo che alcuno perisca, ma che tutti giungano al ravvedimento.»",
   35, "davanti", width=900, size=30, fade_at=LS[36] - 0.4)
tag(S7, 90, 430, "Non serve a calcolare", AL("calcolare", 36) - 0.2, "", 52)
tag(S7, 90, 540, "Pazienza, non lentezza", AL("pazienza", 36) - 0.4, "acc", 50)

# =====================================================================  S8: William Miller (righe 37-40)
t = LS[37] - 0.4
cam(t, S8)
headline(S8, 170, ["William [Miller], 1844"], t + 0.1, kicker="Ottocento", hl_t=AL("Miller", 37) + 0.05, size=96)
f37 = tag(S8, 90, 430, "Una lunga storia di date", LS[37] + 0.3, "", 52)
fade(f37, AL("Daniele", 37) - 0.6)
S_(S8, "miller", 1500, 420, 190, AL("Miller", 37) - 0.3, rot=-2)
t37 = [tag(S8, 90, 430, "Le profezie di Daniele", AL("Daniele", 37) - 0.3, "", 48), tag(S8, 90, 560, "Ritorno atteso verso il 1843", AL("milleottocentoquarantatré", 37) - 1.0, "acc", 52)]
gone(t37, LS[38] - 0.5)
c38 = card(S8, 90, 420, "Data fissata", "22 ottobre 1844", AL("ventidue", 38) - 0.4, w=720, size=52)
t38 = [tag(S8, 90, 640, "Decine di migliaia di persone", AL("Decine", 38) - 0.2, "", 42), tag(S8, 90, 750, "Campi lasciati, beni venduti", AL("campi", 38) - 0.3, "", 40)]
gone([c38] + t38, LS[39] - 0.5)
s39 = [stamp(S8, 90, 430, "Niente", AL("niente", 39) - 0.1, rot=-4, size=84),
       tag(S8, 90, 650, "La Grande Delusione", AL("Delusione", 39) - 0.6, "acc", 52)]
gone(s39, LS[40] - 0.5)
t40 = [tag(S8, 90, 430, "Chiese avventiste", AL("avventiste", 40) - 0.5, "", 48), tag(S8, 90, 540, "Niente più date", AL("rinunciato", 40) - 0.5, "acc", 48)]

# =====================================================================  S9: lo stesso schema (righe 41-45)
t = LS[41] - 0.4
cam(t, S9)
headline(S9, 170, ["Lo stesso [schema]"], t + 0.1, kicker="La storia delle date", hl_t=AL("schema", 43) + 0.05, size=104)
S_(S9, "sablier", 1500, 420, 110, AL("Europa", 41) - 0.2, rot=-2)
c41 = card(S9, 90, 420, "L'anno mille", "Panico generale? In gran parte una leggenda", AL("Europa", 41) - 0.2, w=900, size=40)
t41 = tag(S9, 90, 620, "Costruita più tardi", AL("leggenda", 41) - 0.8, "acc", 50)
gone([c41, t41], LS[42] - 0.5)
c42 = card(S9, 90, 420, "Calendario maya · 2012", "La fine di un ciclo di computo, non una predizione della fine del mondo", AL("maya", 42) - 0.5, w=900, size=38)
gone([c42], LS[43] - 0.5)
bx = [card(S9, 90, 420, "Passo 1", "Una data", AL("data", 43) - 0.3, w=400, size=34),
      card(S9, 580, 420, "Passo 2", "Una paura", AL("paura", 43) - 0.3, w=400, size=34),
      card(S9, 90, 600, "Passo 3", "Un silenzio", AL("silenzio", 43) - 0.3, w=400, size=34),
      card(S9, 580, 600, "Passo 4", "Una nuova data", AL("nuova", 43) - 0.3, w=400, size=34, accent=True)]
gone(bx, LS[44] - 0.5)
c44 = card(S9, 90, 420, "Perché?", "L'incertezza fa paura: una data dà l'impressione di riprendere il controllo", AL("Perché", 44) - 0.1, w=900, size=38)
gone([c44], LS[45] - 0.5)
g45 = [stamp(S9, 90, 440, "Non una data", AL("data", 45) - 0.3, rot=-4, size=76),
       tag(S9, 90, 620, "Un modo di vivere", AL("vivere", 45) - 0.8, "acc", 56)]
gone(g45, LS[46] - 0.5)

# =====================================================================  S10: l'Apocalisse (righe 46-52)
t = LS[46] - 0.4
cam(t, S10)
headline(S10, 170, ["L'[Apocalisse]"], t + 0.1, kicker="Il libro più citato", hl_t=AL("Apocalisse", 46) + 0.05, size=110)
f46 = tag(S10, 90, 430, "Il libro che tutti citano", LS[46] + 0.3, "acc", 52)
fade(f46, AL("apokalypsis", 47) - 0.7)
S_(S10, "cavaliers", 1500, 420, 255, AL("Apocalisse", 46) - 0.2, rot=2)
c47 = card(S10, 90, 420, "Dal greco apokalypsis", "svelamento, rivelazione", AL("apokalypsis", 47) - 0.3, w=780, size=44)
s47 = stamp(S10, 90, 620, "≠ catastrofe", AL("catastrofe", 47) - 0.3, rot=-3, size=64)
gone([c47, s47], LS[48] - 0.5)
S_(S10, "jean-pied", 1200, 420, 185, AL("Beato", 48) - 0.2, rot=-2)
kq(S10, 90, 420, "Apocalisse 1,3 · " + WEB,
   "«Beato chi legge e beati quelli che ascoltano le parole di questa profezia e fanno tesoro delle cose che vi sono scritte, perché il tempo è vicino.»",
   48, "Beato", width=900, size=36, fade_at=LS[49] - 0.4)
t49 = [tag(S10, 90, 430, "Sette Chiese ben reali", AL("sette", 49) - 0.2, "", 52), tag(S10, 90, 540, "Asia Minore · attuale Turchia", AL("Turchia", 49) - 0.7, "", 44),
       tag(S10, 90, 650, "Sotto l'Impero romano", AL("romano", 49) - 0.3, "acc", 48)]
gone(t49, LS[50] - 0.5)
cc = [card(S10, 90, 420, "Lettura 1", "Il mondo dei primi lettori", AL("primi", 50) - 0.3, w=400, size=30),
      card(S10, 580, 420, "Lettura 2", "La storia della Chiesa", AL("Chiesa", 50) - 0.3, w=400, size=30),
      card(S10, 90, 640, "Lettura 3", "Eventi ancora a venire", AL("venire", 50) - 0.3, w=400, size=30),
      card(S10, 580, 640, "Lettura 4", "Un quadro simbolico", AL("simbolico", 50) - 0.3, w=400, size=30, accent=True)]
gone(cc, LS[51] - 0.5)
c51 = card(S10, 90, 420, "Numeri", "mille anni, centoquarantaquattromila: prima di tutto simboli", AL("numeri", 51) - 0.2, w=900, size=38)
s51 = stamp(S10, 90, 690, "Non un codice", AL("codice", 51) - 0.3, rot=-4, size=64)
gone([c51, s51], LS[52] - 0.5)
kq(S10, 90, 420, "Apocalisse 22,20 · " + WEB, "«Sì, vengo presto.»", 52, "Sì", width=700, size=48, last=AL("presto", 52) + 0.5,
   fade_at=LS[53] - 0.45)
tag(S10, 90, 660, "«Vieni, Signor Gesù.»", AL("Vieni", 52) - 0.3, "acc", 56)

# =====================================================================  S11: parousia e vegliare (righe 53-56)
t = LS[53] - 0.4
cam(t, S11)
headline(S11, 170, ["La [parousia]"], t + 0.1, kicker="Presenza, arrivo", hl_t=AL("parousia", 53) + 0.05, size=104)
c53 = card(S11, 90, 420, "In greco", "<b>parousia</b>: presenza, arrivo", AL("parousia", 53) - 0.3, w=800, size=44)
t53 = tag(S11, 90, 600, "La visita ufficiale di un re", AL("re", 53) - 0.4, "", 46)
gone([c53, t53], LS[54] - 0.5)
s54 = stamp(S11, 90, 440, "Non un conto alla rovescia", AL("conto", 54) - 0.3, rot=-3, size=48)
t54 = tag(S11, 90, 600, "Un arrivo atteso", AL("arrivo", 54) - 0.4, "acc", 54)
gone([s54, t54], LS[55] - 0.5)
kq(S11, 90, 420, "Matteo 24,42 · " + WEB, "«Vegliate dunque, perché non sapete in quale giorno il vostro Signore verrà.»", 55, "Vegliate",
   width=900, size=42, fade_at=LS[56] - 0.4)
tw55 = tag(S11, 90, 740, "Vegliare = restare svegli", AL("svegli", 55) - 0.5, "acc", 46)
fade(tw55, LS[56] - 0.5)
S_(S11, "veilleur", 1500, 420, 250, AL("cielo", 56) - 0.3, rot=2)
S_(S11, "vierge-lampe", 1180, 420, 150, AL("olio", 56) - 0.3, rot=-2)
S_(S11, "pain", 760, 420, 250, AL("affamati", 56) - 0.3, rot=2)

# =====================================================================  S12: tre domande (righe 57-60)
t = LS[57] - 0.4
cam(t, S12)
headline(S12, 170, ["Tre [domande]"], t + 0.1, kicker="Davanti a una profezia", hl_t=AL("tre", 57) + 0.05, size=104)
f57 = tag(S12, 90, 430, "Tre semplici domande", LS[57] + 0.3, "acc", 56)
fade(f57, AL("data", 58) - 0.8)
card(S12, 90, 420, "Domanda 1", "Dà una data?", AL("data", 58) - 0.3, w=500, size=34)
tag(S12, 90, 650, "Contraddice Matteo 24,36", AL("contraddice", 58) - 0.2, "acc", 34)
card(S12, 690, 420, "Domanda 2", "Ti spinge alla paura?", AL("paura", 59) - 0.3, w=500, size=34)
tag(S12, 690, 650, "«guardate di non turbarvi»", AL("turbarvi", 59) - 0.5, "acc", 32)
card(S12, 1300, 420, "Domanda 3", "Ti chiede del denaro?", AL("denaro", 60) - 0.3, w=500, size=34)
tag(S12, 1300, 650, "«Guardate che nessuno vi seduca»", AL("seduca", 60) - 0.8, "acc", 32)

# =====================================================================  S13: sostegno e domanda (righe 61-62)
t = LS[61] - 0.4
cam(t, S13)
headline(S13, 170, ["Non sei [solo]"], t + 0.1, kicker="Quando l'angoscia occupa troppo spazio", hl_t=AL("solo", 61) + 0.05, size=104)
glow(S13, 1560, 540, AL("angoscia", 61), size=360, dur=8.0)
S_(S13, "mains-lampe", 1420, 420, 300, AL("angoscia", 61) - 0.2, rot=2)
t61 = [tag(S13, 90, 430, "Un medico", AL("medico", 61) - 0.1, "", 52), tag(S13, 90, 540, "Uno psicologo", AL("psicologo", 61) - 0.1, "", 52),
       tag(S13, 90, 650, "Una persona di fiducia", AL("fiducia", 61) - 0.1, "", 52), tag(S13, 90, 760, "Non toglie nulla alla fede", AL("fede", 61) - 0.9, "acc", 46)]
gone(t61, LS[62] - 0.5)
tq2 = tag(S13, 90, 430, "Una promessa che ti ha aiutato?", LS[62] + 0.4, "acc", 54)
cta = put(S13, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Condividila nei commenti', "cta")
blur_in(cta, AL("commenti", 62) - 1.0, 14)
sfx("click", AL("commenti", 62) - 1.0, 0.8)

# =====================================================================  S1 (rivisitata): conclusione (righe 63-66)
cam(LS[63] - 2.0, "all")
wipe(S1, LS[63] - 2.1)
t = LS[63] - 0.4
cam(t, S1)
headline(S1, 170, ["Il mondo era [ancora lì]"], t + 0.1, kicker="21 ottobre 2011", hl_t=AL("ancora", 63) + 0.05, size=96)
an2 = S_(S1, "animateur", 1500, 420, 190, AL("mattino", 63) - 0.3, rot=2)
fade(an2, LS[65] - 0.5)
t63 = tag(S1, 90, 430, "Il giorno e l'ora restano il segreto del Padre", AL("segreto", 63) - 1.4, "acc", 44)
gone([t63], LS[64] - 0.5)
t64 = [tag(S1, 90, 430, "Appartiene a Dio", AL("appartiene", 64) - 0.2, "", 52), tag(S1, 90, 540, "Non si calcola", AL("calcola", 64) - 0.3, "", 52),
       tag(S1, 90, 650, "La speranza non dipende da una data", AL("speranza", 64) - 0.5, "acc", 44)]
gone(t64, LS[65] - 0.5)
gH = glow(S1, 900, 600, LS[65], size=520, dur=9.0)
f65 = tag(S1, 90, 430, "Ciò che il testo ci lascia", LS[65] + 0.2, "", 54)
fade(f65, AL("vegliare", 65) - 0.6)
w65 = []
for _x, _w, _k in ((90, "vegliare", "vegliare"), (780, "amare", "amare"), (1180, "sperare", "sperare")):
    wid = put(S1, _x, 500, _w, "word", "font-size:100px")
    blur_in(wid, AL(_k, 65) - 0.1, 20)
    w65.append(wid)
gone(w65, LS[66] - 0.2)

t_end = AL("Ogni", 66) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(LS[63] - 2.8, LS[63] - 0.5), (AL("Ogni", 66) - 0.8, DUR_)]
build(
    chapters=[("01", "Date annunciate", 0, LS[8]), ("02", "Nostradamus", LS[8], LS[15]), ("03", "Che cosa dice Gesù", LS[15], LS[37]),
              ("04", "La storia delle date", LS[37], LS[46]), ("05", "L'Apocalisse", LS[46], LS[53]), ("06", "Vegliare", LS[53], DUR_)],
    suppress=supp,
    endcard={"kicker": "Ogni settimana", "title": "La Bibbia<br />[Semplice]", "button": "Iscriviti",
             "stickers": [("jean-portrait", 150, 560, 300, -6), ("vierge-lampe", 1550, 330, 180, 5)]},
    endcard_t=AL("Ogni", 66) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
