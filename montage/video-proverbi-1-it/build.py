"""Video lunga « Perché Proverbi 1 è una chiave per leggere tutta la Bibbia » (La Bibbia Semplice) — style 02, 16:9, 381.6 s. Versione italiana di montage/video-proverbes-1/.

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

THEME = {"brand": "La Bibbia Semplice", "title": "La Bibbia Semplice - Proverbi 1, una chiave di lettura - style 02", "lang": "it",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
DUR_ = 381.6
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


S1, S2, S3, S4, S5 = (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)
S6, S7, S8, S9, S10 = (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)
S11, S12, S13, S14, S15 = (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)
S16, S17, S18 = (4, 3), (3, 3), (2, 3)

html.append('<style>'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')
RIV = " · Riveduta"

# S1: la donna nel mercato (righe 1-3)
cam(0, S1)
headline(S1, 170, ["Una donna [grida] nel mercato"], 0.0, kicker="Proverbi 1", hl_t=AL("grida", 1) + 0.05, size=88)
sp = S_(S1, "sagesse-pied", 1500, 420, 260, 0.0, rot=-3, instant=True)
fo = S_(S1, "foule", 1100, 420, 300, AL("mercato", 1) - 0.3, rot=2)
t2 = [tag(S1, 90, 430, "Nessuna bancarella", AL("bancarella", 2) - 0.2, "", 52), tag(S1, 90, 540, "Nessun esercito", AL("esercito", 2) - 0.2, "", 52),
      tag(S1, 90, 650, "Nessun titolo", AL("titolo", 2) - 0.2, "acc", 52)]
burst(S1, 800, 600, AL("grida", 1) + 0.1)
gone(t2 + [fo], LS[3] - 0.5)
s3 = stamp(S1, 90, 440, "È la Sapienza", AL("sapienza", 3) - 0.2, rot=-4, size=80)
ring(S1, 1640, 600, AL("sapienza", 3), size=300)
t3 = tag(S1, 90, 670, "Proverbi, capitolo 1", AL("capitolo", 3) - 0.2, "acc", 48)

# S2: la chiave (righe 4-5)
t = LS[4] - 0.4
cam(t, S2)
headline(S2, 170, ["Da dove [si comincia] ?"], t + 0.1, kicker="La domanda", hl_t=AL("comincia", 4) + 0.05, size=96)
f4 = tag(S2, 90, 430, "Una domanda che torna spesso", LS[4] + 0.2, "", 50)
fade(f4, AL("dove", 4) - 0.6)
t4 = [tag(S2, 90, 430, "Per capire tutto", AL("capire", 4) - 0.3, "", 52), tag(S2, 90, 540, "Manca una chiave", AL("chiave", 4) - 0.3, "acc", 56)]
gk = glow(S2, 1640, 560, AL("chiave", 4) - 0.2, size=400)
k1 = S_(S2, "cle", 1550, 420, 190, AL("chiave", 4) - 0.2, rot=8)
animate(k1, "turn", AL("chiave", 4) + 0.2)
gone(t4, LS[5] - 0.5)
S_(S2, "cma-cle-romaine", 1100, 420, 200, AL("chiave", 5) - 0.4, rot=-3)
label_box(S2, 700, 790, "Una chiave romana", "I secolo · Cleveland Museum of Art", AL("chiave", 5) + 0.1)
c5 = card(S2, 90, 420, "Proverbi 1", "Una chiave di lettura che la Bibbia stessa ci offre", AL("chiave", 5) - 0.6, w=800, size=40)
t5 = tag(S2, 90, 720, "Non l'unica chiave", AL("unica", 5) - 0.2, "", 46)

# S3: Salomone (righe 6-8)
t = LS[6] - 0.4
cam(t, S3)
headline(S3, 170, ["Il [contesto]"], t + 0.1, kicker="Proverbi 1.1", hl_t=AL("contesto", 6) + 0.05, size=104)
f6 = tag(S3, 90, 430, "Cominciamo dal contesto", LS[6] + 0.2, "acc", 52)
fade(f6, AL("proverbi", 7) - 0.6)
kq(S3, 90, 420, "Proverbi 1.1" + RIV, "«Proverbi di Salomone, figliuolo di Davide, re d'Israele.»", 7, "proverbi", width=900, size=44, fade_at=LS[8] - 0.4)
S_(S3, "salomon", 1500, 420, 215, AL("salomone", 7) - 0.1, rot=3)
t8 = [tag(S3, 90, 430, "Decimo secolo a.C.", AL("decimo", 8) - 0.2, "acc", 56), tag(S3, 90, 550, "Il re più saggio del suo tempo", AL("saggio", 8) - 0.4, "", 44)]
gc = glow(S3, 1350, 520, AL("saggio", 8) - 0.4, size=320)
S_(S3, "sym-couronne", 1150, 420, 220, AL("saggio", 8) - 0.4, rot=-6)

# S4: Ezechia (riga 9)
t = LS[9] - 0.5
cam(t, S4)
headline(S4, 170, ["Un libro [formato] più tardi"], t + 0.1, kicker="Gli storici pensano", hl_t=AL("forma", 9) + 0.05, size=84)
f9 = tag(S4, 620, 430, "Una forma più tarda", LS[9] + 0.3, "", 50)
fade(f9, AL("ezechia", 9) - 0.6)
S_(S4, "scribe", 90, 420, 330, AL("ezechia", 9) - 0.4, rot=-2)
t9 = [tag(S4, 620, 430, "Gli uomini del re Ezechia", AL("ezechia", 9) - 0.1, "", 46), tag(S4, 620, 540, "ricopiano altri proverbi", AL("ricopiato", 9) - 0.1, "acc", 44)]
S_(S4, "sceau-anse-jarre", 1500, 420, 330, AL("ricopiato", 9) + 0.3, rot=3)
label_box(S4, 620, 700, "Proverbi 25.1", "il testo stesso lo lascia intendere", AL("intendere", 9) - 0.6)

# S5: Egitto (righe 10-11)
t = LS[10] - 0.5
cam(t, S5)
headline(S5, 170, ["Un linguaggio [comune]"], t + 0.1, kicker="Echi dall'Egitto", hl_t=AL("comune", 10) + 0.05, size=96)
map_svg(S5, 90, 420, "assets/map.json", t + 0.3, AL("amenemope", 10) - 0.3, width=500)
S_(S5, "papyrus-hieratique", 760, 420, 380, AL("amenemope", 10) - 0.1, rot=3)
label_box(S5, 760, 740, "Lettera su papiro", "Egitto, c. 1470 a.C. · The Met", AL("amenemope", 10) + 0.3)
S_(S5, "cma-scribe-medthu", 1350, 420, 220, AL("egiziano", 10) - 0.2, rot=-3)
gl = glow(S5, 1690, 780, AL("resta", 11) - 0.3, size=280)
S_(S5, "lampe", 1620, 700, 160, AL("resta", 11) - 0.3, rot=-3)
tag(S5, 760, 570, "Un passo alla volta", AL("passo", 11) - 0.2, "", 44)

# S6: il prologo (righe 12-13)
t = LS[12] - 0.4
cam(t, S6)
headline(S6, 170, ["Che cosa [vuole fare] il libro"], t + 0.1, kicker="Proverbi 1.2-4", hl_t=AL("vuole", 12) + 0.05, size=84)
f12 = tag(S6, 90, 430, "Lo dice subito", LS[12] + 0.5, "acc", 52)
fade(f12, AL("per", 13) - 0.7)
ru0 = S_(S6, "rouleau", 1500, 420, 260, LS[12] + 0.3, rot=3)
animate(ru0, "unroll", LS[12] + 0.3)
fade(ru0, AL("sapienza", 13) - 0.55)
kq(S6, 90, 420, "Proverbi 1.2-4" + RIV,
   "«Per conoscere la sapienza e l'istruzione, per comprendere i detti dell'intelligenza; per ricevere ammaestramento di buon senso, di giustizia, di equità e di rettitudine; "
   "per dare accorgimento ai semplici, e conoscenza e riflessione al giovane.»", 13, "per", width=980, size=36)
slot_t = [("lampe", "sapienza", "istruzione"), ("rouleau", "istruzione", "intelligenza"), ("sym-porte", "intelligenza", "giustizia"), ("sym-balance", "giustizia", "semplici"),
          ("fils", "semplici", "giovane"), ("etudiant", "giovane", None)]
for _n, _a, _b in slot_t:
    _t0 = AL(_a, 13) - 0.1
    _s = S_(S6, _n, 1500, 420, 240, _t0, rot=2)
    fade(_s, (AL(_b, 13) - 0.55) if _b else LS[14] - 0.6)

# S7: chokhmah (righe 14-16)
t = LS[14] - 0.4
cam(t, S7)
headline(S7, 170, ["Tre parole [ebraiche]"], t + 0.1, kicker="1 · Sapienza", hl_t=AL("ebraiche", 14) + 0.05, size=96)
gh0 = glow(S7, 1640, 560, t + 0.3, size=400, dur=5.0)
lh0 = S_(S7, "lampe", 1500, 480, 260, t + 0.3, rot=-3)
fade(lh0, AL("bezaleel", 16) - 0.9)
w1 = put(S7, 90, 420, "chokhmah", "word", "font-size:170px")
blur_in(w1, AL("chokhmah", 15) - 0.1, 20)
tag(S7, 90, 670, "« sapienza »", AL("traduce", 15) - 0.1, "", 48)
t16 = tag(S7, 90, 765, "L'abilità di un artigiano", AL("artigiano", 16) - 0.4, "acc", 40)
fade(t16, LS[17] - 0.5)
gb = glow(S7, 1640, 560, AL("bezaleel", 16) - 0.3, size=400)
S_(S7, "betsaleel", 1500, 420, 230, AL("bezaleel", 16) - 0.3, rot=3)

# S8: mussar (riga 17)
t = LS[17] - 0.4
cam(t, S8)
headline(S8, 170, ["La seconda [parola]"], t + 0.1, kicker="2 · Istruzione", hl_t=AL("seconda", 17) + 0.05, size=96)
w2 = put(S8, 90, 420, "mussar", "word", "font-size:170px")
blur_in(w2, AL("mussar", 17) - 0.1, 20)
S_(S8, "tablette-ecole", 900, 420, 360, AL("mussar", 17) + 0.2, rot=-2)
label_box(S8, 900, 700, "Una tavoletta da scolaro", "Egitto, c. 1900 a.C. · The Met", AL("disciplina", 17) - 0.4)
S_(S8, "etudiant", 1500, 420, 260, AL("istruzione", 17) - 0.1, rot=3)
tag(S8, 90, 660, "« istruzione »", AL("istruzione", 17) - 0.1, "", 46)
tag(S8, 90, 750, "o « disciplina »", AL("disciplina", 17) - 0.1, "acc", 42)

# S9: yirah (righe 18-20)
t = LS[18] - 0.4
cam(t, S9)
headline(S9, 170, ["La terza [parola]"], t + 0.1, kicker="3 · Timore", hl_t=AL("terza", 18) + 0.05, size=96)
w3 = put(S9, 90, 420, "yirah", "word", "font-size:170px")
blur_in(w3, AL("yirah", 18) - 0.1, 20)
t18 = tag(S9, 90, 640, "« timore »", AL("timore", 18) - 0.1, "acc", 56)
gone([w3, t18], AL("ecco", 19) - 0.6)
kq(S9, 90, 420, "Proverbi 1.7" + RIV, "«Il timore dell'Eterno è il principio della scienza; ma gli stolti sprezzano la sapienza e l'istruzione.»", 19, "il", n=1, width=900, size=38,
   fade_at=LS[20] - 0.4)
f20 = tag(S9, 90, 540, "Una parola che sorprende", LS[20] + 0.3, "", 50)
fade(f20, AL("paura", 20) - 0.8)
tn = tag(S9, 90, 430, "Non solo paura", AL("paura", 20) - 0.5, "acc", 54)
fade(tn, AL("rispetto", 20) + 3.0)
an = S_(S9, "ancien", 1500, 420, 190, AL("rispetto", 20) - 0.3, rot=2)
fade(an, AL("stupore", 20) - 0.2)
sm_ = S_(S9, "montagne", 1100, 420, 380, AL("stupore", 20) - 0.2, rot=-2)
animate(sm_, "zoom", AL("stupore", 20) - 0.2, dur=4.0)
fade(sm_, AL("coscienza", 20) - 0.3)
gy = glow(S9, 1480, 560, AL("coscienza", 20) - 0.3, size=360, dur=5.0)
S_(S9, "mains-lampe", 1100, 420, 330, AL("coscienza", 20) - 0.3, rot=2)

# S10: un ordine (righe 21-22)
t = LS[21] - 0.5
cam(t, S10)
headline(S10, 170, ["Un [ordine]"], t + 0.1, kicker="Proverbi 1.7", hl_t=AL("ordine", 21) + 0.05, size=110)
tag(S10, 90, 430, "Non al centro", AL("centro", 21) - 0.4, "", 56)
tag(S10, 90, 540, "Dio al suo posto", AL("posto", 21) - 0.3, "acc", 56)
bal0 = S_(S10, "sym-balance", 760, 420, 200, t + 0.4, rot=0)
animate(bal0, "rock", t + 0.4, dur=7.0)
fade(bal0, AL("chiave", 22) - 0.7)
tr = S_(S10, "sym-arbre", 1100, 420, 170, AL("comincia", 21) - 0.3, rot=0)
animate(tr, "grow", AL("comincia", 21) - 0.3)
fade(tr, AL("chiave", 22) - 0.7)
gC = glow(S10, 1640, 560, AL("chiave", 22) - 0.2, size=380)
k2 = S_(S10, "cle", 1550, 420, 190, AL("chiave", 22) - 0.2, rot=6)
animate(k2, "turn", AL("chiave", 22) + 0.1)
stamp(S10, 700, 440, "La chiave", AL("chiave", 22) + 0.1, rot=-5, size=64)
bA = put(S10, 90, 650, "«Sii intelligente, e troverai Dio»", "card", "width:560px;font-size:32px;color:" + THEME["grey"])
blur_in(bA, AL("intelligente", 22) - 0.2, 14)
bB = put(S10, 770, 650, "«Riconosci Dio, e l'intelligenza comincerà»", "card", "width:560px;font-size:32px;border-color:" + ACC)
blur_in(bB, AL("riconosci", 22) - 0.2, 14)
arrow(S10, (680, 740), (760, 740), AL("riconosci", 22) - 0.1)

# S11: il padre (righe 23-25)
t = LS[23] - 0.5
cam(t, S11)
headline(S11, 170, ["Due [scene]"], t + 0.1, kicker="Proverbi 1.8-33", hl_t=AL("scene", 23) + 0.05, size=104)
f23 = tag(S11, 90, 430, "Dopo il prologo", LS[23] + 0.3, "acc", 52)
fade(f23, AL("prima", 24) - 0.5)
c1 = card(S11, 90, 420, "Scena 1", "Versetti 8-19: un padre parla a suo figlio", AL("prima", 24) - 0.1, w=820, size=38)
S_(S11, "pere", 1250, 420, 215, AL("padre", 24) - 0.2, rot=-2)
S_(S11, "fils", 1520, 420, 150, AL("figlio", 24) - 0.1, rot=3)
fade(c1, LS[25] - 0.5)
kq(S11, 90, 420, "Proverbi 1.8" + RIV, "«Ascolta, figliuol mio, l'istruzione di tuo padre, e non trascurare l'insegnamento di tua madre.»", 25, "ascolta", width=820, size=38)
ring(S11, 1360, 600, AL("ascolta", 25) - 0.1, size=260)

# S12: gli uomini (righe 26-27)
t = LS[26] - 0.6
cam(t, S12)
headline(S12, 170, ["Uomini che vogliono [attirarti]"], t + 0.1, kicker="Proverbi 1.10-19", hl_t=AL("seguirli", 26) + 0.05, size=84)
S_(S12, "bande", 1000, 420, 420, AL("uomini", 26) - 0.2, rot=-2)
tag(S12, 90, 430, "Una parte del bottino", AL("bottino", 26) - 0.3, "", 50)
tag(S12, 90, 540, "Una borsa in comune", AL("borsa", 26) - 0.3, "", 50)
S_(S12, "sym-coffre", 1560, 420, 220, AL("bottino", 26) - 0.2, rot=4)
tag(S12, 90, 650, "Le trappole si richiudono", AL("trappole", 27) - 0.5, "acc", 46)
burst(S12, 700, 440, AL("bottino", 26) + 0.1)
burst(S12, 1000, 700, AL("richiudono", 27) + 0.1)

# S13: due strade (riga 28)
t = LS[28] - 0.6
cam(t, S13)
headline(S13, 170, ["Due [strade]"], t + 0.1, kicker="La prima scelta del libro", hl_t=AL("strade", 28) + 0.05, size=110)
ch = S_(S13, "chemins", 1000, 420, 420, AL("strade", 28) + 0.1, rot=2)
animate(ch, "zoom", AL("fretta", 28) - 0.3, dur=6.0)
tag(S13, 90, 430, "Promette in fretta", AL("fretta", 28) - 0.2, "", 50)
tag(S13, 90, 540, "Costruisce lentamente", AL("lentamente", 28) - 0.3, "acc", 54)
hit(AL("strade", 28) + 0.1, 0.7)

# S14: la Sapienza parla (righe 29-33)
t = LS[29] - 0.4
cam(t, S14)
headline(S14, 170, ["La Sapienza [parla]"], t + 0.1, kicker="Scena 2 · versetti 20-33", hl_t=AL("parola", 29) + 0.05, size=96)
S_(S14, "sagesse-pied", 100, 420, 260, LS[29] + 0.3, rot=-3)
kq(S14, 520, 420, "Proverbi 1.20" + RIV, "«La sapienza grida per le strade, fa udire la sua voce sulle piazze.»", 30, "la", width=900, size=42, fade_at=LS[31] - 0.4)
old_ = [S_(S14, "porte-ville", 520, 420, 300, LS[31] + 0.1, rot=-2), S_(S14, "foule", 1000, 420, 300, AL("strade", 31) - 0.3, rot=2),
        S_(S14, "etal", 1500, 420, 250, AL("rumore", 31) - 0.9, rot=3),
        tag(S14, 520, 740, "Non è nascosta su una montagna", AL("montagna", 31) - 0.5, "", 40)]
for _i in old_:
    fade(_i, AL("rifiuto", 32) - 0.7)
burst(S14, 1650, 440, AL("rumore", 31) + 0.1)
rf = [tag(S14, 520, 430, "Chiama…", AL("rifiuto", 32) - 0.3, "", 56), tag(S14, 520, 540, "…e non la si ascolta", AL("ascolta", 32) - 0.4, "", 56),
      tag(S14, 520, 650, "Il frutto delle nostre scelte", AL("frutto", 32) - 0.3, "acc", 50)]
gone(rf, LS[33] - 0.5)
kq(S14, 520, 420, "Proverbi 1.33" + RIV, "«Ma chi mi ascolta dimorerà al sicuro, vivrà tranquillo, senza paura d'alcun male.»", 33, "ma", width=900, size=44, fade_at=LS[34] - 0.4)

# S15: altri libri (righe 34-37)
t = LS[34] - 0.5
cam(t, S15)
headline(S15, 170, ["Una chiave in tutta la [Bibbia]"], t + 0.1, kicker="Salmi · Giobbe · Ecclesiaste", hl_t=AL("bibbia", 34) + 0.05, size=84)
f34 = tag(S15, 90, 430, "Perché una chiave ?", LS[34] + 0.3, "acc", 52)
fade(f34, AL("salmo", 35) - 0.9)
sr1 = S_(S15, "rouleau", 1500, 420, 240, AL("salmo", 35) - 0.3, rot=3)
fade(sr1, LS[36] - 0.5)
kq(S15, 90, 420, "Salmo 111.10" + RIV, "«Il timore dell'Eterno è il principio della sapienza.»", 35, "il", width=900, size=44, fade_at=LS[36] - 0.4)
sr2 = S_(S15, "ancien", 1500, 420, 190, AL("giobbe", 36) - 0.3, rot=2)
fade(sr2, LS[37] - 0.5)
kq(S15, 90, 420, "Giobbe 28.28" + RIV, "«Ecco, il timor del Signore, questa è la sapienza; e fuggire il male è l'intelligenza.»", 36, "ecco", width=900, size=40, fade_at=LS[37] - 0.4)
sr3 = S_(S15, "sagesse-portrait", 1500, 420, 240, AL("ecclesiaste", 37) - 0.3, rot=-2)
kq(S15, 90, 420, "Ecclesiaste 12.13" + RIV, "«Temi Dio, e osserva i suoi comandamenti, perché questo è il tutto per l'uomo.»", 37, "temi", width=900, size=42, fade_at=LS[38] - 0.4)
fade(sr3, LS[38] - 0.5)

# S16: il Nuovo Testamento (righe 38-40)
t = LS[38] - 0.5
cam(t, S16)
headline(S16, 170, ["Il Nuovo Testamento [riprende]"], t + 0.1, kicker="Matteo · 1 Corinzi · Giacomo", hl_t=AL("riprende", 38) + 0.05, size=80)
S_(S16, "jesus-portrait", 1500, 420, 250, AL("gesù", 38) - 0.3, rot=3)
f38 = tag(S16, 90, 430, "Un linguaggio ripreso", LS[38] + 0.3, "", 52)
fade(f38, AL("salomone", 38) - 0.9)
t38 = tag(S16, 90, 430, "« più che Salomone »", AL("salomone", 38) - 0.5, "acc", 56)
gone([t38], LS[39] - 0.5)
S_(S16, "paul-portrait", 1100, 420, 220, AL("paolo", 39) - 0.3, rot=-3)
kq(S16, 90, 420, "1 Corinzi 1.24" + RIV, "«potenza di Dio e sapienza di Dio»", 39, "potenza", width=800, size=44, fade_at=LS[40] - 0.4)
kq(S16, 90, 420, "Giacomo 1.5" + RIV, "«Se qualcuno di voi manca di sapienza, la chieda a Dio.»", 40, "se", width=800, size=44)

# S17: testo e tradizione (righe 41-43)
t = LS[41] - 0.5
cam(t, S17)
headline(S17, 170, ["Testo e [tradizione]"], t + 0.1, kicker="Siamo onesti", hl_t=AL("tradizione", 42) + 0.05, size=96)
f41 = tag(S17, 90, 430, "Siamo onesti", LS[41] + 0.3, "acc", 56)
fade(f41, AL("cristiana", 41) - 0.9)
s41 = stamp(S17, 90, 440, "Lettura cristiana", AL("cristiana", 41) - 0.4, rot=-4, size=72)
t41 = tag(S17, 90, 640, "I lettori ebrei non la fanno", AL("ebrei", 41) - 0.3, "", 46)
gone([s41, t41], LS[42] - 0.5)
f42 = tag(S17, 90, 430, "Il testo, la tradizione", LS[42] + 0.3, "", 52)
fade(f42, AL("relazione", 42) - 0.9)
c42a = card(S17, 90, 420, "Il testo · Proverbi 1", "La sapienza comincia dalla relazione con Dio, e chiama ciascuno", AL("relazione", 42) - 0.4, w=850, size=36)
c42b = card(S17, 90, 650, "La tradizione cristiana", "Questa sapienza ha preso un volto", AL("tradizione", 42) - 0.4, w=850, size=36, accent=True)
gone([c42a, c42b], LS[43] - 0.5)
f43 = tag(S17, 90, 430, "Una chiave di lettura", LS[43] + 0.3, "acc", 52)
fade(f43, AL("onestamente", 43) - 1.1)
c43 = card(S17, 90, 420, "Ciò che si può affermare", "Proverbi uno offre una chiave di lettura", AL("onestamente", 43) - 0.6, w=850, size=40)
t43 = tag(S17, 90, 650, "Con umiltà, per vivere ciò che si capisce", AL("umiltà", 43) - 0.3, "acc", 42)

# S18: applicazione (righe 44-45)
t = LS[44] - 0.5
cam(t, S18)
headline(S18, 170, ["Questa [settimana]"], t + 0.1, kicker="Per te", hl_t=AL("settimana", 44) + 0.05, size=104)
S_(S18, "sagesse-portrait", 1500, 420, 240, LS[44] + 0.3, rot=2)
cn = counter(S18, 90, 420, 0, 7, AL("sette", 44) - 1.0, 2.0, unit=" versetti", size=150)
c44 = card(S18, 90, 640, "Una domanda", "A quale bivio della mia vita una voce sta gridando ?", AL("bivio", 44) - 0.6, w=900, size=38)
gone([cn, c44], LS[45] - 0.5)
t45 = tag(S18, 90, 430, "Un versetto che ti ha guidato ?", AL("versetto", 45) - 0.3, "acc", 52)
cta = put(S18, 90, 600, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Scrivilo nei commenti', "cta")
blur_in(cta, AL("commenti", 45) - 1.2, 14)
sfx("click", AL("commenti", 45) - 1.2, 0.8)

# S1 rivisitata: conclusione (righe 46-48)
cam(LS[46] - 2.0, "all")
wipe(S1, LS[46] - 2.1)
t = LS[46] - 0.4
cam(t, S1)
headline(S1, 170, ["La donna del mercato [grida ancora]"], t + 0.1, kicker="Proverbi 1", hl_t=AL("ancora", 46) + 0.05, size=84)
S_(S1, "sagesse-pied", 1500, 420, 260, LS[46] + 0.2, rot=-3)
t46 = [tag(S1, 90, 430, "Non grida per farti vergognare", AL("vergognare", 46) - 0.5, "", 46), tag(S1, 90, 540, "Sa dove portano le due strade", AL("portano", 46) - 0.4, "acc", 46)]
gone(t46, LS[47] - 0.5)
tag(S1, 90, 430, "Non aspetta che tu sappia tutto", AL("aspetta", 47) - 0.2, "", 48)
s47 = stamp(S1, 90, 560, "Il punto giusto", AL("giusto", 47) - 0.3, rot=-3, size=72)

t_end = AL("settimana", 48) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(LS[46] - 2.8, LS[46] - 0.5), (AL("settimana", 48) - 0.8, DUR_)]
build(
    chapters=[("01", "Il contesto", 0, LS[12]), ("02", "Tre parole", LS[12], LS[23]), ("03", "Due scene", LS[23], LS[34]),
              ("04", "Una chiave", LS[34], LS[44]), ("05", "Per te", LS[44], DUR_)],
    suppress=supp,
    endcard={"kicker": "Ogni settimana", "title": "La Bibbia<br />[Semplice]", "button": "Iscriviti",
             "stickers": [("sagesse-portrait", 150, 560, 300, -6), ("salomon", 1550, 330, 200, 5)]},
    endcard_t=AL("settimana", 48) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
