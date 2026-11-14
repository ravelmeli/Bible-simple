"""Video lunga «Aiutati, che il ciel t'aiuta» non è nella Bibbia: da dove viene? (La Bibbia Semplice) — style 02, 16:9. Versione italiana di montage/video-aide-toi/.

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

THEME = {"brand": "La Bibbia Semplice", "title": "La Bibbia Semplice - Aiutati, che il ciel t'aiuta - style 02", "lang": "it",
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


PRE = ("", "l", "d", "j", "n", "s", "qu", "c", "m", "t", "dell", "nell", "all", "dall", "sull", "un", "v", "quest", "nel", "sant", "tutt")


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

# =====================================================================  S1 : la phrase, l'enquête (lignes 1-7)
cam(0, S1)
headline(S1, 170, ["«Aiutati, che [il ciel] t'aiuta»"], 0.0, kicker="Una frase che tutti conoscono", hl_t=AL("così", 1) + 0.05, size=88)
S_(S1, "foule", 1100, 420, 330, 0.0, rot=-3, instant=True)
st1 = stamp(S1, 90, 440, "Non è nella Bibbia", AL("così", 1) - 0.1, rot=-4, size=62)
gone([st1], LS[3] - 0.3)
t3 = [tag(S1, 90, 430, "Una prova", AL("prova", 3) - 0.1, "", 52), tag(S1, 90, 540, "Un esame", AL("esame", 3) - 0.1, "", 52),
      tag(S1, 90, 650, "Quasi un versetto", AL("versetto", 3) - 0.3, "acc", 52)]
gone(t3, LS[4] - 0.4)
st4 = [stamp(S1, 90, 440, "Introvabile", AL("troverai", 4) - 0.3, rot=-3, size=80), tag(S1, 90, 650, "Dalla Genesi all'Apocalisse", AL("Apocalisse", 4) - 1.0, "", 44)]
gone(st4, LS[5] - 0.4)
t5 = [tag(S1, 90, 430, "Da dove viene?", AL("dove", 5) - 0.1, "acc", 52), tag(S1, 90, 540, "Chi l'ha detta?", AL("Chi", 5) - 0.1, "", 52),
      tag(S1, 90, 650, "È vera?", AL("vera", 5) - 0.3, "", 52)]
gone(t5, LS[6] - 0.4)
t6 = [tag(S1, 90, 430, "Francia · XVII secolo", AL("Francia", 6) - 0.2, "", 50), tag(S1, 90, 540, "Grecia antica", AL("Grecia", 6) - 0.2, "", 50),
      tag(S1, 90, 650, "Che cosa dice la Bibbia", AL("biblico", 6) - 0.4, "acc", 50)]
gone(t6, LS[7] - 0.4)
teaser(S1, 90, 440, "Un poeta francese", LS[7] + 0.3, hold=3.4)

# =====================================================================  S2 : La Fontaine (lignes 8-13)
t = LS[8] - 0.4
cam(t, S2)
headline(S2, 170, ["[La Fontaine], 1668"], t + 0.1, kicker="Favole · libro VI", hl_t=AL("Fontaine", 8) + 0.05, size=96)
liv = S_(S2, "livres", 1350, 420, 230, LS[8] + 0.4, rot=2)
f8 = tag(S2, 90, 430, "Un poeta francese", LS[8] + 0.3, "", 52)
fade(f8, AL("carrettiere", 8) - 0.6)
c8 = card(S2, 90, 420, "La favola", "Il carrettiere impantanato", AL("carrettiere", 8) - 0.3, w=900, size=52)
fade(liv, LS[9] - 0.4)
gone([c8], LS[9] - 0.4)
her = S_(S2, "hercule-statuette", 1500, 420, 150, AL("Ercole", 9) - 0.3, rot=2)
t9 = [tag(S2, 90, 430, "La ruota affonda nel fango", AL("ruota", 9) - 0.2, "", 46), tag(S2, 90, 540, "Invoca Ercole", AL("Ercole", 9) - 0.3, "acc", 50)]
gone(t9, LS[10] - 0.4)
t10 = [tag(S2, 90, 430, "Eroe della mitologia greca", AL("eroe", 10) - 0.3, "", 46), tag(S2, 90, 540, "Adorato come un semidio", AL("semidio", 10) - 0.6, "acc", 46)]
gone(t10, LS[11] - 0.4)
t11 = [tag(S2, 90, 430, "La spalla alla ruota", AL("spalla", 11) - 0.2, "", 50), tag(S2, 90, 540, "Togliere i sassi", AL("sassi", 11) - 0.2, "", 50),
       tag(S2, 90, 650, "Riempire il solco", AL("solco", 11) - 0.2, "acc", 50)]
gone(t11, LS[12] - 0.4)
c12 = card(S2, 90, 420, "La Fontaine · Il carrettiere impantanato", "«Aide-toi, le Ciel t'aidera.»", AL("Aide-toi", 12) - 0.2, w=1000, size=54, accent=True)
gone([c12], LS[13] - 0.4)
t13 = stamp(S2, 90, 430, "Non il Dio d'Israele", AL("Israele", 13) - 0.3, rot=-3, size=70)
tag(S2, 90, 660, "Un dio greco", AL("Ercole", 13) - 0.1, "acc", 54)

# =====================================================================  S3 : Ésope (lignes 14-17)
t = LS[14] - 0.4
cam(t, S3)
headline(S3, 170, ["[Esopo], Grecia antica"], t + 0.1, kicker="La fonte della favola", hl_t=AL("Esopo", 14) + 0.05, size=96)
S_(S3, "esope-statuette", 1500, 420, 140, AL("Esopo", 14) - 0.3, rot=-2)
t14 = tag(S3, 90, 430, "La Fontaine la prende in prestito", E("prestito", 14, 0.4, 0.4), "acc", 52)
gone([t14], LS[15] - 0.4)
c15 = card(S3, 90, 420, "Nella versione di Esopo", "Metti mano all'opera prima di pregare", AL("Ercole", 15) - 0.4, w=900, size=44)
gone([c15], LS[16] - 0.4)
t16 = [tag(S3, 90, 430, "Un'idea antichissima", AL("antichissima", 16) - 0.8, "", 52), tag(S3, 90, 540, "Molto prima di Gesù", AL("Gesù", 16) - 0.3, "acc", 52)]
gone(t16, LS[17] - 0.4)
stamp(S3, 90, 440, "Origine: una favola greca", AL("favola", 17) - 0.5, rot=-3, size=60)

# =====================================================================  S4 : la version anglaise (lignes 18-23)
t = LS[18] - 0.4
cam(t, S4)
headline(S4, 170, ["Versione [inglese]"], t + 0.1, kicker="Una frase che viaggia", hl_t=AL("inglese", 19) + 0.05, size=104)
teaser(S4, 90, 440, "Il seguito cambia lo sguardo", LS[18] + 0.3, hold=7.0)
c19 = card(S4, 90, 420, "In inglese", "God helps those who help themselves", E("God", 19, 0.3, 0.2), w=1000, size=48)
gone([c19], LS[20] - 0.4)
c20 = card(S4, 90, 420, "George Herbert · 1651", "«Aiutati da te, e Dio ti aiuterà.»", E("Herbert", 20, 0.3), w=1000, size=44)
gone([c20], LS[21] - 0.4)
c21 = card(S4, 90, 420, "Algernon Sidney", "fine del XVII secolo · «un proverbio»", E("Sidney", 21, 0.3), w=900, size=44)
gone([c21], LS[22] - 0.4)
fr = S_(S4, "franklin", 1500, 420, 300, AL("Franklin", 22) - 0.3, rot=2)
c22 = card(S4, 90, 420, "Benjamin Franklin", "almanacco · 1736", AL("Franklin", 22) - 0.2, w=700, size=52)
gone([c22], LS[23] - 0.4)
t23 = [tag(S4, 90, 430, "Stampatore, uomo pratico", AL("stampatore", 23) - 0.3, "", 50), stamp(S4, 90, 620, "Un proverbio, non un versetto", AL("proverbio", 23) - 0.2, rot=-3, size=54)]

# =====================================================================  S5 : du proverbe au « verset » (lignes 24-27)
t = LS[24] - 0.4
cam(t, S5)
headline(S5, 170, ["Dal proverbio al [«versetto»]"], t + 0.1, kicker="Come è sembrata biblica", hl_t=AL("biblica", 25) + 0.05, size=92)
c24 = card(S5, 90, 420, "Francia · anni Venti dell'Ottocento", "La società «Aide-toi, le ciel t'aidera»", E("società", 24, 0.3), w=1000, size=44)
gone([c24], LS[25] - 0.4)
t25 = [tag(S5, 90, 430, "Le favole", AL("favole", 25) - 0.1, "", 50), tag(S5, 90, 540, "La politica", AL("politica", 25) - 0.1, "", 50),
       tag(S5, 90, 650, "I discorsi", AL("discorsi", 25) - 0.1, "", 50), tag(S5, 800, 430, "I sermoni", AL("sermoni", 25) - 0.1, "acc", 50)]
gone(t25, LS[26] - 0.4)
t26 = tag(S5, 90, 430, "Sondaggi USA: una larga parte dei credenti", AL("sondaggi", 26) - 0.2, "", 40)
gone([t26], LS[27] - 0.4)
s27 = stamp(S5, 90, 440, "Non è nella Bibbia", AL("Riassumiamo", 27) + 0.5, rot=-4, size=76)
t27 = [tag(S5, 90, 650, "Una favola", AL("favola", 27) - 0.1, "", 48), tag(S5, 500, 650, "Un proverbio", AL("proverbio", 27) - 0.1, "", 48),
       tag(S5, 960, 650, "Morale pratica", AL("morale", 27) - 0.2, "acc", 48)]

# =====================================================================  S6 : l'aide de Dieu dans les Psaumes (lignes 28-35)
t = LS[28] - 0.4
cam(t, S6)
headline(S6, 170, ["L'aiuto di [Dio]"], t + 0.1, kicker="Che cosa dice davvero la Bibbia", hl_t=AL("aiuto", 29) + 0.05, size=104)
t28 = tag(S6, 90, 430, "Dice qualcosa di vero?", E("vero", 28, 0.4, 0.4), "acc", 54)
gone([t28], LS[29] - 0.4)
t29 = tag(S6, 90, 430, "Il testo dice quasi il contrario", E("contrario", 29, 0.9, 0.4), "", 48)
gone([t29], LS[30] - 0.4)
c30 = put(S6, 90, 420, "<small>Parola ebraica</small><span class='heb' style='font-size:92px;margin-right:18px'>עזר</span>ezer", "card", "width:800px;font-size:70px")
blur_in(c30, AL("ezer", 30) - 0.3, 14)
t30 = tag(S6, 90, 700, "«aiuto» · «soccorso»", AL("soccorso", 30) - 0.4, "acc", 52)
gone([c30, t30], LS[31] - 0.4)
f31 = tag(S6, 90, 430, "Salmo 33, versetto 20", LS[31] + 0.3, "", 52)
fade(f31, AL("anima", 31) - 0.3)
kq(S6, 90, 420, "Salmo 33,20" + BIB, "«L'anima nostra aspetta l'Eterno; egli è il nostro aiuto e il nostro scudo.»", 31, "anima", width=900, size=40, fade_at=LS[32] - 0.4)
t32 = tag(S6, 90, 430, "L'aiuto di chi non ce la fa da solo", E("solo", 32, 1.2, 0.4), "acc", 46)
gone([t32], LS[33] - 0.4)
kq(S6, 90, 420, "Salmo 121,1-2" + BIB, "«Io alzo gli occhi ai monti. Donde mi verrà l'aiuto? Il mio aiuto viene dall'Eterno, che ha fatto il cielo e la terra.»", 33, "Io", width=950, size=36, fade_at=LS[34] - 0.4)
kq(S6, 90, 420, "Salmo 46,1" + BIB, "«Dio è per noi un rifugio e una forza, un aiuto sempre pronto nelle distrette.»", 34, "Dio", width=950, size=38, fade_at=LS[35] - 0.4)
stamp(S6, 90, 440, "Nessuno dice: prima aiutati", AL("Nota", 35) + 0.3, rot=-3, size=50)
tag(S6, 90, 700, "L'aiuto viene da Dio", AL("aiuto", 35, 1) - 0.4, "acc", 52)

# =====================================================================  S7 : sans force, par la grâce (lignes 36-39)
t = LS[36] - 0.4
cam(t, S7)
headline(S7, 170, ["[Senza forza]"], t + 0.1, kicker="Romani 5 · Efesini 2", hl_t=AL("forza", 37) + 0.05, size=110)
S_(S7, "paul-pied", 1500, 420, 150, AL("Paolo", 36) - 0.3, rot=-2)
kq(S7, 90, 420, "Romani 5,6" + BIB, "«Poiché, mentre eravamo ancora senza forza, Cristo, nel tempo stabilito, è morto per gli empi.»", 36, "Poiché", width=950, size=40, fade_at=LS[37] - 0.4)
t37 = [tag(S7, 90, 430, "«Senza forza»", AL("forza", 37) - 0.3, "", 56), tag(S7, 90, 540, "Lontano da «aiutati»", AL("lontani", 37) - 0.2, "acc", 52)]
gone(t37, LS[38] - 0.4)
kq(S7, 90, 420, "Efesini 2,8-9" + BIB, "«Poiché è per grazia che siete stati salvati, mediante la fede; e ciò non viene da voi; è il dono di Dio. Non è in virtù di opere, affinché nessuno si glori.»", 38, "Poiché", width=1000, size=34, fade_at=LS[39] - 0.4)
stamp(S7, 90, 440, "La salvezza è un dono", AL("dono", 39) - 0.6, rot=-3, size=76)

# =====================================================================  S8 : l'effort n'est pas inutile (lignes 40-45)
t = LS[40] - 0.4
cam(t, S8)
headline(S8, 170, ["E [lo sforzo]?"], t + 0.1, kicker="Proverbi 6 · 2 Tessalonicesi 3", hl_t=AL("sforzo", 40) + 0.05, size=110)
S_(S8, "paul-portrait", 1500, 420, 230, AL("Paolo", 43) - 0.3, rot=2)
t40 = tag(S8, 90, 430, "Lo sforzo non è inutile", E("inutile", 40, 0.6, 0.4), "acc", 52)
gone([t40], LS[41] - 0.4)
kq(S8, 90, 420, "Proverbi 6,6" + BIB, "«Va' dalla formica, o pigro; considera le sue vie e diventa saggio.»", 41, "Va", width=900, size=42, fade_at=LS[42] - 0.4)
t42 = [tag(S8, 90, 430, "Il lavoro", AL("lavoro", 42) - 0.2, "", 52), tag(S8, 90, 540, "La previdenza", AL("previdenza", 42) - 0.2, "", 52),
       tag(S8, 90, 650, "La saggezza pratica", AL("saggezza", 42) - 0.2, "acc", 52)]
gone(t42, LS[43] - 0.4)
kq(S8, 90, 420, "2 Tessalonicesi 3,10" + BIB, "«Se qualcuno non vuol lavorare, neppure mangi.»", 43, "Se", width=900, size=42, fade_at=LS[44] - 0.4)
c44 = card(S8, 90, 420, "Lo sforzo personale", "non è proibito", AL("proibito", 44) - 0.5, w=800, size=54)
gone([c44], LS[45] - 0.4)
t45 = [tag(S8, 90, 430, "Chi rifiuta di lavorare", AL("rifiuta", 45) - 0.2, "", 46), tag(S8, 90, 540, "Non chi non può", AL("può", 45) - 0.3, "acc", 46),
       tag(S8, 90, 650, "Paolo: ha lavorato con le sue mani", AL("mani", 45) - 0.4, "", 44)]

# =====================================================================  S9 : agir ou se confier ? la mer Rouge (lignes 46-49)
t = LS[46] - 0.4
cam(t, S9)
headline(S9, 170, ["Agire o [affidarsi]?"], t + 0.1, kicker="Esodo 14", hl_t=AL("affidarci", 46) + 0.05, size=100)
t46 = [tag(S9, 90, 430, "Agire", AL("agire", 46) - 0.1, "", 56), tag(S9, 90, 540, "Affidarsi a Dio", AL("affidarci", 46) - 0.2, "", 56), tag(S9, 90, 650, "Entrambi", AL("insieme", 46) - 0.2, "acc", 56)]
gone(t46, LS[47] - 0.4)
f47 = tag(S9, 90, 430, "Primo esempio: il Mar Rosso", LS[47] + 0.3, "", 50)
fade(f47, AL("Eterno", 47) - 0.3)
mo = S_(S9, "moise", 1500, 420, 190, LS[47] + 0.4, rot=2)
fade(mo, LS[49] - 0.4)
kq(S9, 90, 420, "Esodo 14,14" + BIB, "«L'Eterno combatterà per voi, e voi ve ne starete queti.»", 47, "Eterno", width=900, size=42, fade_at=LS[48] - 0.4)
kq(S9, 90, 420, "Esodo 14,15" + BIB, "«Perché gridi a me? Di' ai figliuoli d'Israele che si mettano in cammino.»", 48, "Perché", width=900, size=42, fade_at=LS[49] - 0.4)
stamp(S9, 90, 440, "Un aiuto che chiede una risposta", E("risposta", 49, 0.8, 0.4), rot=-3, size=50)

# =====================================================================  S10 : Néhémie, Proverbes, Psaume 127 (lignes 50-57)
t = LS[50] - 0.4
cam(t, S10)
headline(S10, 170, ["[Preghiera] e vigilanza"], t + 0.1, kicker="Neemia · Proverbi · Salmo 127", hl_t=AL("Preghiera", 51) + 0.05, size=96)
nh = S_(S10, "feuillet-nehemie", 1100, 420, 270, AL("Neemia", 50) - 0.2, rot=2)
so = S_(S10, "soldat", 1500, 420, 170, AL("guardie", 50) - 0.3, rot=-2)
gone([nh, so], LS[51] - 0.3)
t50 = [tag(S10, 90, 430, "Neemia", AL("Neemia", 50) - 0.1, "", 54), tag(S10, 90, 540, "Pregano", AL("pregano", 50) - 0.2, "acc", 54), tag(S10, 90, 650, "Guardie, giorno e notte", AL("guardie", 50) - 0.2, "", 50)]
gone(t50, LS[51] - 0.3)
t51 = stamp(S10, 90, 440, "Preghiera + vigilanza", AL("Preghiera", 51) - 0.1, rot=-3, size=70)
gone([t51], LS[52] - 0.4)
kq(S10, 90, 420, "Proverbi 21,31" + BIB, "«Il cavallo è pronto per il giorno della battaglia, ma la vittoria appartiene all'Eterno.»", 52, "Il", width=900, size=40, fade_at=LS[53] - 0.4)
t53 = [tag(S10, 90, 430, "Il cavallo", AL("cavallo", 53) - 0.1, "", 50), tag(S10, 90, 540, "L'esercito", AL("esercito", 53) - 0.1, "", 50), tag(S10, 90, 650, "La vittoria", AL("vittoria", 53) - 0.2, "acc", 50)]
gone(t53, LS[54] - 0.4)
kq(S10, 90, 420, "Proverbi 16,9" + BIB, "«Il cuore dell'uomo medita la sua via, ma l'Eterno dirige i suoi passi.»", 54, "Il", width=900, size=42, fade_at=LS[55] - 0.4)
t55 = [tag(S10, 90, 430, "Pianifichi", AL("pianifichi", 55) - 0.1, "", 50), tag(S10, 90, 540, "Non controlli tutto", AL("controllare", 55) - 0.3, "acc", 50)]
gone(t55, LS[56] - 0.4)
f56 = tag(S10, 90, 430, "Salmo 127", LS[56] + 0.3, "", 52)
fade(f56, AL("Se", 56) - 0.3)
kq(S10, 90, 420, "Salmo 127,1" + BIB, "«Se l'Eterno non edifica la casa, invano si affaticano gli edificatori.»", 56, "Se", width=900, size=42, fade_at=LS[57] - 0.4)
tag(S10, 90, 430, "Costruiscono davvero", AL("costruttori", 57) - 0.4, "", 50)
tag(S10, 90, 540, "Ma lo sforzo non basta", AL("basta", 57) - 0.6, "acc", 50)

# =====================================================================  S11 : le vrai équilibre, les dangers (lignes 58-62)
t = LS[58] - 0.4
cam(t, S11)
headline(S11, 170, ["Il vero [equilibrio]"], t + 0.1, kicker="Né «agisci da solo», né «non fare nulla»", hl_t=AL("equilibrio", 58) + 0.05, size=104)
c58 = [card(S11, 90, 420, "Il testo dice", "Agisci", E("agisci", 58, 0.2, 0.4), w=420, size=56), card(S11, 700, 420, "E", "Non riporre la fiducia nella sola tua azione", E("fiducia", 58, 0.4, 1.0), w=760, size=44, accent=True)]
gone(c58, LS[59] - 0.4)
t59 = [tag(S11, 90, 430, "Non del tutto falsa", E("falsa", 59, 0.4, 0.4), "", 52), tag(S11, 90, 540, "Una parte di saggezza pratica", AL("saggezza", 59) - 0.3, "acc", 50)]
gone(t59, LS[60] - 0.4)
s60 = stamp(S11, 90, 440, "Pericolosa come legge di Dio", AL("pericolosa", 60) - 0.2, rot=-3, size=56)
gone([s60], LS[61] - 0.4)
S_(S11, "sym-balance", 1500, 420, 190, AL("meriti", 61) - 0.3, rot=2)
t61 = [tag(S11, 90, 430, "L'aiuto di Dio si merita?", E("meriti", 61, 0.3, 0.4), "", 50), tag(S11, 90, 540, "Tutta la Bibbia parla di grazia", AL("grazia", 61) - 0.4, "acc", 50)]
gone(t61, LS[62] - 0.4)
c62 = card(S11, 90, 420, "Come può suonare la frase", "«Se Dio non ti aiuta, è perché non ti aiuti abbastanza.»", AL("rimprovero", 62) - 0.3, w=1000, size=40)
t62 = tag(S11, 90, 720, "Malato · indebitato · esausto · senza lavoro", AL("esausto", 62) - 0.5, "", 40)

# =====================================================================  S12 : Job, les pauvres, les soins (lignes 63-67)
t = LS[63] - 0.4
cam(t, S12)
headline(S12, 170, ["Giobbe e [i poveri]"], t + 0.1, kicker="Giobbe 42 · Levitico 19 · Proverbi 19", hl_t=AL("poveri", 64) + 0.05, size=96)
jb = S_(S12, "job-blake", 1150, 420, 600, AL("Giobbe", 63) - 0.2, rot=-2)
fade(jb, LS[64] - 0.4)
kq(S12, 90, 420, "Giobbe 42,7" + BIB, "«Voi non avete parlato di me secondo la verità, come ha fatto il mio servo Giobbe.»", 63, "Voi", width=900, size=40, fade_at=LS[64] - 0.4)
gl = S_(S12, "glaneuses-millet", 1150, 420, 600, E("spigolature", 64, 0.3, 0.4), rot=2)
fade(gl, LS[65] - 0.4)
t64 = tag(S12, 90, 430, "Lasciare le spigolature", E("spigolature", 64, 0.3, 0.4), "acc", 52)
gone([t64], LS[65] - 0.4)
kq(S12, 90, 420, "Proverbi 19,17" + BIB, "«Chi ha pietà del povero presta all'Eterno, che gli contraccambierà l'opera buona.»", 65, "Chi", width=900, size=40, fade_at=LS[66] - 0.4)
s66 = stamp(S12, 90, 440, "Agli altri: aiutatelo", E("altri", 66, 0.5, 0.4), rot=-3, size=64)
gone([s66], LS[67] - 0.4)
f67 = tag(S12, 90, 430, "Un periodo molto pesante", LS[67] + 0.3, "", 52)
fade(f67, AL("medico", 67) - 0.4)
t67 = [tag(S12, 90, 430, "Un medico", AL("medico", 67) - 0.1, "", 52), tag(S12, 90, 540, "Uno psicologo", AL("psicologo", 67) - 0.1, "", 52), tag(S12, 90, 650, "Una persona vicina", AL("vicina", 67) - 0.1, "", 52),
       tag(S12, 90, 760, "La fede non si oppone alle cure", AL("cure", 67) - 0.6, "acc", 46)]

# =====================================================================  S13 : que faire de cette phrase ? (lignes 68-73)
t = LS[68] - 0.4
cam(t, S13)
headline(S13, 170, ["Che farne di [questa frase]?"], t + 0.1, kicker="Un proverbio, non una promessa", hl_t=AL("frase", 68) + 0.05, size=92)
t68 = [tag(S13, 90, 430, "Un proverbio di buon senso", E("proverbio", 68, 0.3, 0.4), "", 52), tag(S13, 90, 540, "Agisci · preparati", AL("agisci", 68) - 0.3, "", 52)]
gone(t68, LS[69] - 0.4)
f69 = tag(S13, 90, 430, "La promessa di Dio", LS[69] + 0.3, "", 52)
fade(f69, AL("Il", 69) - 0.3)
kq(S13, 90, 420, "Salmo 121,2" + BIB, "«Il mio aiuto viene dall'Eterno.»", 69, "Il", width=800, size=50, fade_at=LS[70] - 0.4)
tq = tag(S13, 90, 430, "Quando l'aiuto è arrivato senza meritarlo?", LS[70] + 0.4, "acc", 48)
cta = put(S13, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Dillo nei commenti', "cta")
blur_in(cta, AL("commenti", 70) - 1.0, 14)
sfx("click", AL("commenti", 70) - 1.0, 0.8)
gone([tq, cta], LS[71] - 0.3)
S_(S13, "hercule-statuette", 1500, 420, 150, LS[71] + 0.3, rot=2)
t71 = [tag(S13, 90, 430, "Spingi la ruota", AL("spingi", 71) - 0.2, "", 56), tag(S13, 90, 540, "E invoca anche", AL("invoca", 71) - 0.2, "acc", 56)]
gone(t71, LS[72] - 0.4)
stamp(S13, 90, 440, "Le due cose sono permesse", AL("due", 72) - 0.3, rot=-3, size=54)

t_end = AL("Ogni", 73) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(AL("Ogni", 73) - 0.8, DUR_)]
build(
    chapters=[("01", "La frase", 0, LS[8]), ("02", "L'origine", LS[8], LS[28]), ("03", "Che cosa dice la Bibbia", LS[28], LS[58]), ("04", "Per te", LS[58], DUR_)],
    suppress=supp,
    endcard={"kicker": "Ogni settimana", "title": "La Bibbia<br />[Semplice]", "button": "Iscriviti",
             "stickers": [("moise-portrait", 150, 560, 300, -6), ("paul-portrait", 1550, 330, 230, 5)]},
    endcard_t=AL("Ogni", 73) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
