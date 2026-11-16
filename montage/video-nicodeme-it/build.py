"""Video lunga « Nicodemo : l'uomo che visitava Gesù di notte, fino al giorno in cui non ebbe più paura » (La Bibbia Semplice) — stile 02, 16:9. Versione italiana di montage/video-nicodeme/.

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

THEME = {"brand": "La Bibbia Semplice", "title": "La Bibbia Semplice - Nicodemo - style 02", "lang": "it",
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
    for _t in re.split(r"[\s'’]+", _l):
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
# S1 : l'uomo della notte (righe 1-7)
cam(0, S1)
headline(S1, 170, ["Nicodemo, l\'uomo della [notte]"], 0.0, kicker="Vangelo di Giovanni", hl_t=AL("notte", 1) + 0.05, size=96)
S_(S1, "veilleur", 1500, 420, 200, 0.0, rot=2, instant=True)
t1 = tag(S1, 90, 430, "Gli altri : in pieno giorno", AL("pieno", 1) - 0.2, "", 50)
gone([t1], AL("Lui", 1) - 0.3)
tl = tag(S1, 90, 540, "Lui : di notte", AL("Lui", 1) - 0.2, "acc", 56)
gone([tl], LS[2] - 0.4)
t2 = [tag(S1, 90, 430, "Ricco di sapere", AL("ricco", 2) - 0.1, "", 52), tag(S1, 90, 540, "Rispettato", AL("rispettato", 2) - 0.1, "", 52), tag(S1, 90, 650, "Legato al suo rango", AL("rango", 2) - 0.4, "acc", 52)]
gone(t2, LS[3] - 0.4)
t3 = tag(S1, 90, 430, "Bussare in segreto alla porta di Gesù", AL("segreto", 3) - 0.4, "acc", 48)
gone([t3], LS[4] - 0.4)
t4 = [tag(S1, 90, 430, "Chi è quest\'uomo ?", AL("Chi", 4) - 0.1, "", 52), tag(S1, 90, 540, "Perché di notte ?", AL("Perché", 4) - 0.1, "", 52), tag(S1, 90, 650, "Che cosa gli succede ?", AL("succede", 4) - 0.3, "acc", 52)]
gone(t4, LS[5] - 0.4)
t5 = [tag(S1, 90, 430, "Una visita di notte", AL("visita", 5) - 0.2, "", 52), tag(S1, 90, 540, "Una frase in pieno consiglio", AL("consiglio", 5) - 0.4, "", 50), tag(S1, 90, 650, "Una sepoltura", AL("sepoltura", 5) - 0.3, "acc", 52)]
gone(t5, LS[6] - 0.4)
c6 = card(S1, 90, 420, "Un ritratto proprio di Giovanni", "Giovanni 3 · Giovanni 7 · Giovanni 19", AL("Giovanni", 6) - 0.3, w=900, size=52)
gone([c6], LS[7] - 0.4)
tag(S1, 90, 430, "Tra la prima scena e l\'ultima…", LS[7] + 0.3, "acc", 46)
tag(S1, 90, 540, "…qualcosa cambia", E("cambia", 7, 0.4, 3.0), "", 52)

# =====================================================================  S2 : il contesto, chi è Nicodemo (righe 8-14)
t = LS[8] - 0.4
cam(t, S2)
headline(S2, 170, ["[Gerusalemme], la Pasqua"], t + 0.1, kicker="Nel primo secolo", hl_t=AL("Gerusalemme", 8) + 0.05, size=104)
vi = S_(S2, "ville", 1450, 420, 300, LS[8] + 0.2, rot=2)
fade(vi, AL("pellegrini", 10) - 0.4)
t9 = [tag(S2, 90, 430, "Scaccia i mercanti dal tempio", AL("mercanti", 9) - 0.3, "", 46), tag(S2, 90, 540, "Compie segni", AL("segni", 9) - 0.3, "acc", 52)]
gone(t9, LS[10] - 0.4)
fo = S_(S2, "foule", 1100, 560, 300, AL("pellegrini", 10) - 0.3, rot=-2)
t10 = tag(S2, 90, 430, "Chi è questo Galileo ?", AL("Galileo", 10) - 0.4, "acc", 52)
gone([t10, fo], LS[11] - 0.4)
S_(S2, "nicodeme-tete", 1500, 420, 190, E("Nicodemo", 11, 0.3, 0.3), rot=2)
c11 = card(S2, 90, 420, "Giovanni 3.1" + BIB, "« un uomo tra i Farisei, chiamato Nicodemo, un capo dei Giudei »", E("Farisei", 11, 0.5, 0.4), w=1000, size=40)
gone([c11], LS[12] - 0.4)
t12 = [tag(S2, 90, 430, "I farisei", AL("farisei", 12) - 0.2, "", 52), tag(S2, 90, 540, "La legge di Mosè, ogni giorno", AL("Mosè", 12) - 0.3, "acc", 46)]
gone(t12, LS[13] - 0.4)
t13 = [tag(S2, 90, 430, "Capo dei Giudei", AL("Capo", 13) - 0.1, "", 52), tag(S2, 90, 540, "Il consiglio : il Sinedrio", AL("Sinedrio", 13) - 0.4, "acc", 50), tag(S2, 90, 650, "Un notabile, prudente", AL("notabile", 13) - 0.2, "", 50)]
gone(t13, LS[14] - 0.4)
c14 = card(S2, 90, 420, "Un nome greco", "Nicodemo : « vincitore del popolo »", AL("vincitore", 14) - 0.5, w=900, size=46)

# =====================================================================  S3 : perché di notte ? (righe 15-21)
t = LS[15] - 0.4
cam(t, S3)
headline(S3, 170, ["Perché [di notte] ?"], t + 0.1, kicker="Giovanni 3.2", hl_t=AL("notte", 16) + 0.05, size=104)
t15 = tag(S3, 90, 430, "Viene a cercare Gesù", LS[15] + 0.2, "acc", 52)
gone([t15], LS[16] - 0.4)
t16 = tag(S3, 90, 430, "Il testo non lo dice", AL("dice", 16) - 0.8, "", 56)
gone([t16], LS[17] - 0.4)
t17 = [tag(S3, 90, 430, "Paura dello sguardo dei colleghi ?", AL("temesse", 17) - 0.3, "", 46), tag(S3, 90, 540, "Una conversazione tranquilla ?", AL("tranquilla", 17) - 0.4, "", 46), tag(S3, 90, 650, "Un simbolo ?", AL("simbolo", 17) - 0.3, "acc", 50)]
gone(t17, LS[18] - 0.4)
sh = stamp(S3, 90, 440, "Delle ipotesi", AL("ipotesi", 18) - 0.4, rot=-3, size=70)
sn = S_(S3, "nicodeme", 1500, 420, 190, LS[18] + 0.3, rot=2)
gone([sh, sn], LS[19] - 0.4)
f19 = tag(S3, 90, 430, "In Giovanni : luce e tenebre", LS[19] + 0.3, "acc", 50)
kq(S3, 90, 420, "Giovanni 1.5" + BIB, "« La luce splende nelle tenebre, e le tenebre non l\'hanno ricevuta. »", 19, "luce", n=1, width=900, size=42, fade_at=LS[20] - 0.4)
f20 = tag(S3, 90, 430, "Giuda lascia la tavola", LS[20] + 0.3, "", 52)
fade(f19, AL("luce", 19, 1) - 0.3)
kq(S3, 90, 420, "Giovanni 13.30" + BIB, "« Ed era notte. »", 20, "Ed", width=600, size=54, last=AL("notte", 20) + 0.6, fade_at=AL("notte", 20) + 1.2)
fade(f20, AL("Ed", 20) - 0.3)
tag(S3, 90, 660, "La notte : uno stato del cuore ?", AL("cuore", 20) - 0.5, "acc", 46)

# =====================================================================  S4 : Rabbì (righe 22-24)
t = LS[22] - 0.4
cam(t, S4)
headline(S4, 170, ["« [Rabbì], noi sappiamo »"], t + 0.1, kicker="Giovanni 3.2", hl_t=AL("Rabbì", 22) + 0.05, size=100)
S_(S4, "christ-nicodeme-dessin", 1500, 420, 250, LS[22] + 0.4, rot=2)
kq(S4, 90, 420, "Giovanni 3.2" + BIB, "« Rabbì, noi sappiamo che tu sei un dottore venuto da Dio; perché nessuno può fare questi miracoli che tu fai, se Dio non è con lui. »", 22, "Rabbì", width=950, size=36, fade_at=LS[23] - 0.4)
t23 = [tag(S4, 90, 430, "« Noi » : altri con lui", AL("noi", 23) - 0.3, "acc", 50), tag(S4, 90, 540, "Persone impressionate, nell\'élite", AL("élite", 23) - 0.5, "", 44)]
gone(t23, LS[24] - 0.4)
t24 = [tag(S4, 90, 430, "Rabbì : « mio maestro »", AL("maestro", 24) - 0.5, "", 52), tag(S4, 90, 540, "Un notabile davanti a un artigiano", AL("artigiano", 24) - 0.4, "acc", 48)]

# =====================================================================  S5 : nascere di nuovo (righe 25-28)
t = LS[25] - 0.4
cam(t, S5)
headline(S5, 170, ["Nascere [di nuovo]"], t + 0.1, kicker="Giovanni 3.3-4", hl_t=AL("nuovo", 25) + 0.05, size=104)
S_(S5, "jesus-pied", 1500, 420, 220, LS[25] + 0.3, rot=2)
kq(S5, 90, 420, "Giovanni 3.3" + BIB, "« In verità, in verità ti dico che se uno non è nato di nuovo, non può vedere il regno di Dio. »", 25, "In", width=950, size=40, fade_at=LS[26] - 0.4)
c26 = put(S5, 90, 420, "<small>Parola greca</small><span style=\'font-size:84px\'>ἄνωθεν</span> anōthen", "card", "width:900px;font-size:66px")
blur_in(c26, AL("anōthen", 26) - 0.3, 14)
t26 = [tag(S5, 90, 700, "« di nuovo »", AL("nuovo", 26) - 0.3, "", 52), tag(S5, 560, 700, "« dall\'alto »", AL("alto", 26) - 0.3, "acc", 52)]
gone([c26] + t26, LS[27] - 0.4)
kq(S5, 90, 420, "Giovanni 3.4" + BIB, "« Come può un uomo nascere quando è vecchio? Può egli entrare una seconda volta nel seno di sua madre e nascere? »", 27, "Come", width=950, size=38, fade_at=LS[28] - 0.4)
t28 = [tag(S5, 90, 430, "Prende le parole sul serio", AL("serio", 28) - 0.4, "", 50), stamp(S5, 90, 620, "La parola è ambigua", AL("ambigua", 28) - 0.3, rot=-3, size=64)]

# =====================================================================  S6 : acqua, Spirito, vento (righe 29-35)
t = LS[29] - 0.4
cam(t, S6)
headline(S6, 170, ["Lo [Spirito] e il vento"], t + 0.1, kicker="Giovanni 3.5-10", hl_t=AL("Spirito", 32) + 0.05, size=104)
c29 = card(S6, 90, 420, "Gesù precisa", "Nascere d\'acqua e di Spirito", E("precisa", 29, 0.2, 0.3), w=900, size=48)
gone([c29], LS[30] - 0.4)
c30 = card(S6, 90, 420, "Una nascita", "ricevuta, come un dono, e non guadagnata", E("dono", 30, 0.6, 0.4), w=900, size=46)
gone([c30], LS[31] - 0.4)
c31 = card(S6, 90, 420, "Poi aggiunge un\'immagine", "Il vento", E("immagine", 31, 0.3, 0.4), w=800, size=56)
gone([c31], AL("pneuma", 32) - 0.4)
c32 = card(S6, 90, 420, "Parola greca", "<b>pneuma</b> : vento · Spirito", AL("pneuma", 32) - 0.3, w=800, size=52)
t32 = tag(S6, 90, 640, "Come la parola ebraica ruach", AL("ruach", 32) - 0.5, "acc", 46)
gone([c32, t32], LS[33] - 0.4)
c33 = card(S6, 90, 420, "Nicodemo, sconcertato", "« Come può essere ciò ? »", AL("Come", 33) - 0.4, w=900, size=46)
gone([c33], LS[34] - 0.4)
ti34 = tag(S6, 90, 430, "Con una punta di ironia", E("ironia", 34, 0.3, 0.4), "acc", 50)
gone([ti34], AL("Tu", 34) - 0.35)
kq(S6, 90, 420, "Giovanni 3.10" + BIB, "« Tu sei il dottor d\'Israele, e non sai queste cose? »", 34, "Tu", width=900, size=44, fade_at=LS[35] - 0.4)
stamp(S6, 90, 440, "Uno shock", AL("shock", 35) - 0.3, rot=-4, size=84)
tag(S6, 90, 640, "Ciò che credeva di dominare gli sfugge", AL("sfugge", 35) - 0.8, "acc", 46)

# =====================================================================  S7 : il serpente, Giovanni 3.16 (righe 36-39)
t = LS[36] - 0.4
cam(t, S7)
headline(S7, 170, ["Il serpente [innalzato]"], t + 0.1, kicker="Giovanni 3.14-16 · Numeri 21", hl_t=AL("serpente", 36) + 0.05, size=104)
se = S_(S7, "serpent-airain", 1500, 420, 200, AL("serpente", 37) - 0.3, rot=2)
t36 = tag(S7, 90, 430, "Una frase che molti conoscono", E("frase", 36, 0.3, 0.5), "acc", 50)
gone([t36], AL("come", 36) - 0.35)
kq(S7, 90, 420, "Giovanni 3.14-15" + BIB, "« E come Mosè innalzò il serpente nel deserto, così bisogna che sia innalzato il Figliuol dell\'uomo, affinché chiunque crede in lui abbia vita eterna. »", 36, "come", width=1000, size=36, fade_at=LS[37] - 0.4)
t37 = [tag(S7, 90, 430, "Numeri 21", AL("Numeri", 37) - 0.2, "", 52), tag(S7, 90, 540, "Un serpente di bronzo su un\'asta", AL("asta", 37) - 0.8, "acc", 46)]
gone(t37, LS[38] - 0.4)
kq(S7, 90, 420, "Giovanni 3.16" + BIB, "« Poiché Iddio ha tanto amato il mondo, che ha dato il suo unigenito Figliuolo, affinché chiunque crede in lui non perisca, ma abbia vita eterna. »", 38, "Poiché", width=1000, size=36, fade_at=LS[39] - 0.4)
tag(S7, 90, 430, "Dove finisce la parola di Gesù ?", AL("finisca", 39) - 0.4, "", 48)
tag(S7, 90, 540, "Il senso generale resta lo stesso", AL("senso", 39) - 0.3, "acc", 48)

# =====================================================================  S8 : il silenzio (righe 40-42)
t = LS[40] - 0.4
cam(t, S8)
headline(S8, 170, ["Un [silenzio]"], t + 0.1, kicker="Fine della scena", hl_t=AL("Niente", 40) + 0.05, size=110)
t40 = [tag(S8, 90, 430, "Non dice che crede", E("crede", 40, 0.3, 0.5), "", 50), tag(S8, 90, 540, "Né che rifiuta", AL("rifiuta", 40) - 0.3, "", 50), tag(S8, 90, 650, "Né che se ne va", AL("va", 40) - 0.3, "acc", 50)]
gone(t40, LS[41] - 0.4)
t41 = [stamp(S8, 90, 440, "Nessuna conversione", E("conversione", 41, 0.5, 0.4), rot=-3, size=70), tag(S8, 90, 650, "Finisce con un silenzio", AL("silenzio", 41) - 0.5, "acc", 50)]
gone(t41, LS[42] - 0.4)
tag(S8, 90, 430, "Mesi, forse anni", E("anni", 42, 0.8, 0.4), "", 50)

# =====================================================================  S9 : Giovanni 7, la difesa (righe 43-53)
t = LS[43] - 0.4
cam(t, S9)
headline(S9, 170, ["Prende [la parola]"], t + 0.1, kicker="Giovanni 7 · la festa delle Capanne", hl_t=AL("Nicodemo", 46) + 0.05, size=104)
t43 = tag(S9, 90, 430, "Giovanni 7 · la festa delle Capanne", LS[43] + 0.3, "acc", 52)
gone([t43], LS[44] - 0.4)
lv = S_(S9, "levite", 1500, 420, 190, AL("guardie", 44) - 0.3, rot=2)
kq(S9, 90, 420, "Giovanni 7.46" + BIB, "« Mai uomo parlò come parla quest\'uomo! »", 44, "Mai", width=900, size=48, fade_at=LS[45] - 0.4)
fade(lv, LS[45] - 0.4)
pr = S_(S9, "pretre", 1500, 420, 180, LS[45] + 0.3, rot=-2)
kq(S9, 90, 420, "Giovanni 7.49" + BIB, "« Ma questa folla che non conosce la legge, è maledetta. »", 45, "Ma", width=900, size=42, fade_at=LS[46] - 0.4)
fade(pr, LS[46] - 0.4)
S_(S9, "nicodeme", 1500, 420, 190, LS[46] + 0.3, rot=2)
kq(S9, 90, 420, "Giovanni 7.50" + BIB, "« Nicodemo, quel che era venuto di notte a Gesù, ed era uno di loro »", 46, "Nicodemo", width=950, size=38, fade_at=LS[47] - 0.4)
kq(S9, 90, 420, "Giovanni 7.51" + BIB, "« La nostra legge condanna ella un uomo prima che sia stato udito e che si sappia quello che ha fatto? »", 47, "La", width=950, size=40, fade_at=LS[48] - 0.4)
t48 = [tag(S9, 90, 430, "Non ancora una dichiarazione di fede", AL("dichiarazione", 48) - 0.4, "", 46), tag(S9, 90, 540, "Un principio : ascoltare prima di giudicare", AL("principio", 48) - 0.4, "acc", 46)]
gone(t48, LS[49] - 0.4)
t49 = [tag(S9, 90, 430, "Davanti ai suoi colleghi", AL("colleghi", 49) - 0.3, "", 52), stamp(S9, 90, 620, "Un atto coraggioso", AL("coraggioso", 49) - 0.8, rot=-3, size=64)]
gone(t49, LS[50] - 0.4)
kq(S9, 90, 420, "Giovanni 7.52" + BIB, "« Sei anche tu di Galilea? Esamina, e vedi che dalla Galilea non è mai sorto profeta. »", 50, "Sei", width=950, size=40, fade_at=LS[51] - 0.4)
t51 = tag(S9, 90, 430, "Il prezzo della parola : il disprezzo", AL("disprezzo", 51) - 0.8, "acc", 50)
gone([t51], LS[52] - 0.4)
t52 = [tag(S9, 90, 430, "2 Re : Giona, di Gat-Efer", AL("Giona", 52) - 0.5, "", 48), tag(S9, 90, 540, "In Galilea", AL("Galilea", 52) - 0.3, "acc", 52)]
gone(t52, LS[53] - 0.4)
tag(S9, 90, 430, "La seduta è tolta", AL("seduta", 53) - 0.3, "", 52)
tag(S9, 90, 540, "Ma lui ha parlato", AL("parlato", 53) - 0.4, "acc", 56)

# =====================================================================  S10 : dalla notte al giorno (righe 54-55)
t = LS[54] - 0.4
cam(t, S10)
headline(S10, 170, ["Dalla notte al [giorno]"], t + 0.1, kicker="Primo cambiamento", hl_t=AL("giorno", 54) + 0.05, size=104)
t54 = [tag(S10, 90, 430, "Non più solo un visitatore discreto", E("discreto", 54, 0.5, 0.4), "", 46), tag(S10, 90, 540, "Difende un uomo che si vuole condannare", AL("condannare", 54) - 0.6, "acc", 44)]
gone(t54, LS[55] - 0.4)
stamp(S10, 90, 440, "Il più rischioso", E("rischioso", 55, 0.5, 0.4), rot=-3, size=76)

# =====================================================================  S11 : Giovanni 19, gli aromi (righe 56-62)
t = LS[56] - 0.4
cam(t, S11)
headline(S11, 170, ["Ai piedi della [croce]"], t + 0.1, kicker="Giovanni 19", hl_t=AL("diciannove", 56) + 0.05, size=104)
t56 = [tag(S11, 90, 430, "Capitolo diciannove", LS[56] + 0.3, "", 52), tag(S11, 90, 540, "Gesù crocifisso sotto Ponzio Pilato", AL("Pilato", 56) - 0.5, "", 46), tag(S11, 90, 650, "I discepoli dispersi", AL("dispersi", 56) - 0.4, "acc", 50)]
gone(t56, LS[57] - 0.4)
f57 = tag(S11, 90, 430, "Giuseppe d\'Arimatea", LS[57] + 0.3, "acc", 52)
fade(f57, AL("discepolo", 57) - 0.4)
jo = S_(S11, "pere", 1500, 420, 190, AL("Giuseppe", 57) - 0.3, rot=2)
kq(S11, 90, 420, "Giovanni 19.38" + BIB, "« discepolo di Gesù, ma occulto per timore de\' Giudei »", 57, "discepolo", width=900, size=44, fade_at=LS[58] - 0.4)
t58 = [tag(S11, 90, 430, "Giuseppe : la paura, detta dal testo", AL("paura", 58) - 0.4, "", 46), tag(S11, 90, 540, "Nicodemo : nemmeno una parola sulla paura", AL("Nicodemo", 58) - 0.3, "acc", 46)]
gone(t58, LS[59] - 0.4)
fade(jo, LS[59] - 0.4)
S_(S11, "nicodeme", 1500, 420, 190, LS[59] + 0.3, rot=2)
kq(S11, 90, 420, "Giovanni 19.39" + BIB, "« Venne anche Nicodemo, quello che da prima era andato di notte da Gesù, portando una mistura di mirra e d\'aloe di circa cento libbre. »", 59, "Venne", width=1000, size=36, fade_at=LS[60] - 0.4)
c60 = card(S11, 90, 420, "Cento libbre romane", "più di 30 chili di profumi e di aromi", AL("trenta", 60) - 0.6, w=900, size=44)
gone([c60], LS[61] - 0.4)
t61 = [tag(S11, 90, 430, "Due uomini, due paure possibili", AL("paure", 61) - 0.5, "", 46), tag(S11, 90, 540, "Lo stesso gesto, insieme", AL("stesso", 61) - 0.4, "acc", 52)]
gone(t61, LS[62] - 0.4)
tag(S11, 90, 430, "Funerale regale ? Un\'interpretazione comune", AL("interpretazione", 62) - 0.8, "", 42)
tag(S11, 90, 540, "Non una certezza", AL("certezza", 62) - 0.4, "acc", 52)

# =====================================================================  S12 : in pieno giorno (righe 63-70)
t = LS[63] - 0.4
cam(t, S12)
headline(S12, 170, ["In [pieno giorno]"], t + 0.1, kicker="Giovanni 19.39-42", hl_t=AL("scena", 63) + 0.05, size=108)
tomb = S_(S12, "mise-au-tombeau-relief", 1100, 420, 330, AL("Immagina", 63) - 0.2, rot=-2)
fade(tomb, LS[66] - 0.4)
t63 = [tag(S12, 90, 430, "Un membro del Sinedrio", AL("Sinedrio", 63) - 0.4, "", 52), tag(S12, 90, 540, "Un uomo ricco, un notabile", AL("notabile", 63) - 0.4, "", 50), tag(S12, 90, 650, "Si occupa del suo corpo", AL("corpo", 63) - 0.4, "acc", 52)]
gone(t63, LS[64] - 0.4)
t64 = tag(S12, 90, 430, "Rischiare reputazione e posizione…", AL("reputazione", 64) - 0.5, "acc", 44)
gone([t64], LS[65] - 0.4)
t65 = [tag(S12, 90, 430, "Fasce e aromi", AL("aromi", 65) - 0.4, "", 50), tag(S12, 90, 540, "Un sepolcro nuovo, in un giardino", AL("giardino", 65) - 0.5, "acc", 48)]
gone(t65, LS[66] - 0.4)
s66 = stamp(S12, 90, 440, "Dalla notte al pieno giorno", E("pieno", 66, 0.4, 0.4), rot=-3, size=62)
gone([s66], LS[67] - 0.4)
c67 = card(S12, 90, 420, "Giovanni 19.39", "« che da prima era andato di notte »", E("evangelista", 67, 0.3, 0.4), w=900, size=44)
gone([c67], LS[68] - 0.4)
t68 = [tag(S12, 90, 430, "Mai scritto : « è diventato discepolo »", E("discepolo", 68, 0.5, 0.4), "", 46), tag(S12, 90, 540, "Gli Atti non lo menzionano", AL("Atti", 68) - 0.3, "acc", 46)]
gone(t68, LS[69] - 0.4)
c69 = [card(S12, 90, 420, "La tradizione", "Lo ha considerato un credente", AL("tradizione", 69) - 0.2, w=900, size=44), stamp(S12, 90, 680, "Apocrifo tardivo · non la Bibbia", AL("apocrifo", 69) - 0.3, rot=-3, size=50)]
gone(c69, LS[70] - 0.4)
tag(S12, 90, 430, "Una notte", E("notte", 70, 0.3, 0.4), "", 56)
tag(S12, 90, 540, "Una parola", AL("parola", 70) - 0.3, "", 56)
tag(S12, 90, 650, "Un gesto", AL("gesto", 70) - 0.3, "acc", 56)

# =====================================================================  S13 : per te (righe 71-79)
t = LS[71] - 0.4
cam(t, S13)
headline(S13, 170, ["Che cosa ci [dice] questa storia"], t + 0.1, kicker="Applicazione", hl_t=AL("dice", 71) + 0.05, size=96)
t71 = [tag(S13, 90, 430, "Avvicinare Gesù con i propri dubbi", E("dubbi", 71, 0.6, 0.4), "", 46), tag(S13, 90, 540, "Se ne va con un enigma", AL("enigma", 71) - 0.4, "", 48), tag(S13, 90, 650, "Gesù non lo scaccia", AL("scaccia", 71) - 0.3, "acc", 50)]
gone(t71, LS[72] - 0.4)
t72 = [tag(S13, 90, 430, "La fede può essere lenta", AL("lenta", 72) - 0.3, "", 52), tag(S13, 90, 540, "Una visita · una difesa · un atto", AL("tappe", 72) - 0.6, "acc", 46)]
gone(t72, LS[73] - 0.4)
t73 = tag(S13, 90, 430, "Il coraggio cresce a piccoli passi", E("piccoli", 73, 0.5, 0.4), "acc", 48)
gone([t73], LS[74] - 0.4)
t74 = [tag(S13, 90, 430, "Non giudica chi avanza nell\'ombra", AL("ombra", 74) - 0.7, "", 44), tag(S13, 90, 540, "Non lo lascia dove si trova", AL("lascia", 74) - 0.3, "acc", 46)]
gone(t74, LS[75] - 0.4)
t75 = [tag(S13, 90, 430, "La paura dello sguardo degli altri", AL("sguardo", 75) - 0.3, "", 50), tag(S13, 90, 540, "Una persona di fiducia", AL("fiducia", 75) - 0.3, "", 50), tag(S13, 90, 650, "O un professionista", AL("professionista", 75) - 0.3, "acc", 50)]
gone(t75, LS[76] - 0.4)
tq = tag(S13, 90, 430, "Quale piccolo passo questa settimana ?", LS[76] + 0.4, "acc", 52)
cta = put(S13, 90, 620, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Dillo nei commenti', "cta")
blur_in(cta, AL("commenti", 76) - 1.0, 14)
sfx("click", AL("commenti", 76) - 1.0, 0.8)
gone([tq, cta], LS[77] - 0.3)
S_(S13, "veilleur", 1500, 420, 200, LS[77] + 0.3, rot=2)
t77 = tag(S13, 90, 430, "La notte di Nicodemo", AL("notte", 77) - 0.3, "", 56)
gone([t77], LS[78] - 0.4)
t78 = [tag(S13, 90, 430, "Gli aromi, davanti a tutti", AL("aromi", 78) - 0.3, "", 52), tag(S13, 90, 540, "La paura ha ceduto, a poco a poco", AL("ceduto", 78) - 0.3, "acc", 52)]

t_end = AL("Ogni", 79) - 0.2
cam(t_end, "all")

_af = os.path.join(HERE, "autofade.json")
if os.path.exists(_af):
    for _id, _t in json.load(open(_af)):
        fade(_id, _t)

supp = list(SUPP) + [(AL("Ogni", 79) - 0.8, DUR_)]
build(
    chapters=[("01", "La notte", 0, LS[22]), ("02", "La conversazione", LS[22], LS[43]), ("03", "Il consiglio e la croce", LS[43], LS[71]), ("04", "Per te", LS[71], DUR_)],
    suppress=supp,
    endcard={"kicker": "Ogni settimana", "title": "La Bibbia<br />[Semplice]", "button": "Iscriviti",
             "stickers": [("nicodeme", 150, 560, 280, -6), ("jesus-portrait", 1550, 330, 230, 5)]},
    endcard_t=AL("Ogni", 79) - 0.1,
    music_volume=0.075,
    pulse_volume=0.05,
    retention=True,
)
print("MANQUES:", MANQUES)
