"""Vidéo longue « Pourquoi Proverbes 1 est une clé pour lire toute la Bible » — style 02, 16:9, 411,9 s (6 min 52).

Construit avec le moteur du kit (kit-style-02/moteur/style02.py), option retention. 18 stations, 21 arrêts de caméra,
trois stations revisitées avec un état différent (wipe). Chaque élément est calé sur transcript.json.
Les mots hébreux sont en lettres latines (translittération), écrits en HTML : à faire relire avant publication.
Lancer : python3 build.py   (puis npx hyperframes check et npx hyperframes render -q draft)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kit-style-02", "moteur"))
import style02 as s  # noqa: E402

THEME = {"brand": "La Bible Simple", "title": "La Bible Simple - Proverbes 1, une clé de lecture - style 02", "lang": "fr",
         "bg": "#EFE4CC", "ink": "#2B2118", "grey": "#7A6C58", "grey2": "#B3A58D", "line": "#CDBFA3", "tile": "#DDD0B6", "land": "#E2D6BB"}
s.setup(here=HERE, duration=411.9, cols=5, rows=4, fmt="16:9", theme=THEME, bpm=96,
         zoom=1.15, xmap=(190, 0.8539), ymap=(208, 0.85))
from style02 import *  # noqa: E402,F401,F403
import style02  # noqa: E402

N = " "


MANQUES = []


def A(word, after=0.0, n=0):
    """Début du n-ième mot `word` prononcé à partir de `after` secondes."""
    hits = [w["start"] for w in style02.words if style02.norm(w["text"]) == style02.norm(word) and w["start"] >= after - 0.01]
    if len(hits) <= n:
        MANQUES.append((word, after, n))
        return max(after, 1.0) + 0.5
    return hits[n]


def S_(station, name, x, y, w, t, **kw):
    """sticker() avec contrôle de débordement (zone utile : y < 860)."""
    i, h = sticker(station, name, x, y, w, t, **kw)
    if y + h > 862:
        print(f"ATTENTION {name} déborde : bas à {y + h}")
    return i


# stations (colonne, rangée) : rangées 0 → 3, serpent
MARCHE, CLE, SALOMON, EZECHIAS, EGYPTE = (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)
PROLOGUE, HOKHMAH, MOUSSAR, YIRAH, CENTRE = (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)
PERE, BANDE, CHEMINS, SAGESSE, FRISE = (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)
NT, LECTURES, APPEL = (4, 3), (3, 3), (2, 3)

html.append('<style>'
            '.box.wide{text-align:left;font-weight:700;line-height:1.3}'
            f'.word{{font-weight:900;letter-spacing:-3px;line-height:1.05;color:{INK};border-bottom:16px solid {ACC};display:inline-block}}'
            '.node.card{background:#fff;border:3px solid ' + INK + ';padding:22px 28px 26px;box-sizing:border-box;font-weight:700;line-height:1.3;'
            'box-shadow:8px 8px 0 rgba(43,33,24,.15)}'
            '.card small{display:block;font-size:24px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:' + THEME["grey"] + ';margin-bottom:8px}'
            '</style>')


def quote(station, x, y, ref_txt, text, t, width=1000, size=40):
    i = put(station, x, y, f"<small>{ref_txt}</small>{text}", "box wide", f"width:{width}px;font-size:{size}px")
    blur_in(i, t, 14)
    return i


# =====================================================================  MARCHÉ (0 → 18,3) : la Sagesse crie
cam(0, MARCHE)
S_(MARCHE, "sagesse-pied", 130, 370, 270, 0.0, rot=-3, instant=True)
S_(MARCHE, "etal", 1300, 380, 400, A("marché"), rot=3)
headline(MARCHE, 170, ["Une femme [crie] en plein marché"], 0.0, kicker="Proverbes 1", hl_t=A("crie") + 0.05, size=88)
tag(MARCHE, 560, 430, "Pas d'échoppe", A("échoppe") - 0.1, "", 54)
tag(MARCHE, 560, 540, "Pas d'armée", A("armée") - 0.1, "", 54)
tag(MARCHE, 560, 650, "Pas de titre", A("titre") - 0.1, "acc", 54)
burst(MARCHE, 700, 280, A("crie") + 0.05)
teaser(MARCHE, 560, 770, "Qui est cette femme ?", 8.4, hold=3.6)
label_box(MARCHE, 1000, 700, "La Sagesse", "Proverbes 1.20", A("sagesse") - 0.2)
ring(MARCHE, 265, 480, A("sagesse"), size=300)
hit(A("sagesse"), 0.8)

# =====================================================================  CLÉ (18,3 → 36,7) : par où commencer ?
t = A("question") - 0.5
cam(t, CLE)
headline(CLE, 170, ["Par où [commencer] ?"], t + 0.1, kicker="La question", hl_t=A("commencer") + 0.05, size=100)
S_(CLE, "panneau", 130, 340, 400, A("commencer") - 0.2, rot=-2)
tag(CLE, 640, 400, "On garde la sensation", A("sensation") - 0.2, "", 52)
tag(CLE, 640, 520, "qu'il manque une clé", A("manque") - 0.1, "acc", 60)
S_(CLE, "cle", 1500, 260, 230, A("clé", 20.0), rot=8)
label_box(CLE, 640, 680, "Proverbes 1", "une clé de lecture", A("Proverbes", 26.0))
tag(CLE, 640, 800, "Pas la seule clé", A("seule") - 0.1, "", 48)
hit(A("clé", 20.0), 0.8)
ring(CLE, 1610, 420, A("clé", 20.0) + 0.1, size=260)

# =====================================================================  SALOMON (36,7 → 54,3) : le contexte
t = A("Commençons") - 0.3
cam(t, SALOMON)
headline(SALOMON, 170, ["Le [contexte]"], t + 0.1, kicker="Proverbes 1.1", hl_t=A("contexte") + 0.05, size=100)
quote(SALOMON, 90, 400, "Proverbes 1.1 · Louis Segond 1910", "« Proverbes de Salomon, fils de David, roi d'Israël. »",
      A("Proverbes", 38.0), width=1050, size=44)
S_(SALOMON, "salomon", 1450, 260, 260, A("Salomon", 38.0) - 0.1, rot=3)
tag(SALOMON, 90, 640, "Xe siècle avant notre ère", A("dixième") - 0.2, "acc", 56)
tag(SALOMON, 90, 760, "Le roi le plus sage de son temps", A("sage") - 0.5, "", 44)
ring(SALOMON, 1580, 360, A("Salomon", 46.0), size=240)
burst(SALOMON, 1000, 690, A("dixième") + 0.1)

# =====================================================================  ÉZÉCHIAS (54,3 → 66,9) : forme actuelle plus tard
t = A("historiens") - 0.5
cam(t, EZECHIAS)
headline(EZECHIAS, 170, ["Un livre [mis en forme] plus tard"], t + 0.1, kicker="Les historiens pensent", hl_t=A("forme") + 0.05, size=84)
S_(EZECHIAS, "scribe", 90, 380, 430, A("chapitre", 54.0) - 0.3, rot=-2)
tag(EZECHIAS, 560, 430, "Les hommes du roi Ézéchias", A("Ézéchias") - 0.2, "", 50)
tag(EZECHIAS, 560, 540, "recopient d'autres proverbes", A("recopié") - 0.1, "acc", 50)
label_box(EZECHIAS, 560, 660, "Proverbes 25.1", "le texte lui-même le laisse entendre", A("laisse"))
S_(EZECHIAS, "sceau-anse-jarre", 1300, 360, 440, A("recopié") + 0.2, rot=3)
label_box(EZECHIAS, 1300, 700, "Anse de jarre à sceau", "Israël, VIIIe-VIIe s. av. J.-C. · The Met", A("recopié") + 0.6)

# =====================================================================  ÉGYPTE (66,9 → 85,1) : un langage commun
t = A("spécialistes") - 0.5
cam(t, EGYPTE)
headline(EGYPTE, 170, ["Un langage [commun]"], t + 0.1, kicker="Ressemblances avec l'Égypte", hl_t=A("commun") + 0.05, size=96)
map_svg(EGYPTE, 70, 330, "assets/map.json", t + 0.3, A("d'Amenemopé") - 0.2, width=690)
S_(EGYPTE, "papyrus-hieratique", 1010, 330, 520, A("Instruction") - 0.1, rot=3)
label_box(EGYPTE, 1010, 500, "Lettre sur papyrus en hiératique", "Égypte, vers 1470 av. J.-C. · The Met", A("d'Amenemopé") + 0.2)
tag(EGYPTE, 1010, 640, "La sagesse, langage commun", A("commun") - 0.1, "acc", 42)
S_(EGYPTE, "palette-scribe", 1760, 250, 100, A("ancien") - 0.2, rot=4)
S_(EGYPTE, "lampe", 1500, 720, 160, A("reste") - 0.3, rot=-3)
tag(EGYPTE, 1010, 760, "Un passage à la fois", A("passage") - 0.1, "", 44)
burst(EGYPTE, 1230, 450, A("d'Amenemopé") + 0.15)

# =====================================================================  PROLOGUE (85,1 → 110,4) : ce que veut faire ce livre
t = A("Mais") - 0.4
cam(t, PROLOGUE)
headline(PROLOGUE, 170, ["Ce que veut faire [ce livre]"], t + 0.1, kicker="Proverbes 1.2-4", hl_t=A("livre", 85.0) + 0.05, size=88)
teaser(PROLOGUE, 1100, 190, "Trois mots hébreux à retenir", 103.0, hold=2.6)
q = quote(PROLOGUE, 90, 360, "Proverbes 1.2-4 · Louis Segond 1910",
          "« Pour connaître la sagesse et l'instruction, pour comprendre les paroles de l'intelligence ; pour recevoir des leçons de "
          "bon sens, de justice, d'équité et de droiture ; pour donner aux simples de la prudence, au jeune homme de la science "
          "et de la réflexion. »", A("Pour", 90.0), width=1080, size=40)
S_(PROLOGUE, "rouleau", 1330, 380, 440, A("Pour", 90.0) + 0.3, rot=3)
for k, (txt, w_, cl) in enumerate([("Sagesse", "sagesse", ""), ("Instruction", "l'instruction", ""), ("Intelligence", "l'intelligence", ""),
                                   ("Justice", "justice", "acc"), ("Équité", "d'équité", ""), ("Droiture", "droiture", "acc")]):
    tag(PROLOGUE, 90 + (k % 3) * 360, 720 + (k // 3) * 100, txt, A(w_, 91.0) - 0.15, cl, 44)
burst(PROLOGUE, 1550, 600, A("manuel", 100.0) + 0.1) if False else None

# =====================================================================  HOKHMAH (110,4 → 132,5)
t = A("hébreux") - 0.9
cam(t, HOKHMAH)
headline(HOKHMAH, 170, ["Trois mots [hébreux]"], t + 0.1, kicker="1 · Sagesse", hl_t=A("hébreux") + 0.05, size=96)
w1 = put(HOKHMAH, 90, 330, "ḥokhmah", "word", "font-size:190px")
blur_in(w1, A("premier", 110.0) + 0.1, 20)
tag(HOKHMAH, 90, 600, "« sagesse »", A("traduit") - 0.1, "", 56)
S_(HOKHMAH, "betsaleel", 1330, 280, 300, A("Betsaleel") - 0.3, rot=3)
tag(HOKHMAH, 90, 700, "L'habileté d'un artisan", A("l'habileté") - 0.1, "", 50)
tag(HOKHMAH, 90, 800, "Savoir faire, savoir vivre", A("faire") - 0.2, "acc", 50)
label_box(HOKHMAH, 1000, 720, "Betsaleel", "Exode 31.1-6", A("Betsaleel") + 0.1)
burst(HOKHMAH, 1480, 300, A("Betsaleel") + 0.1)

# =====================================================================  MOUSSAR (132,5 → 139,9)
t = A("deuxième") - 0.4
cam(t, MOUSSAR)
headline(MOUSSAR, 170, ["Le deuxième mot"], t + 0.1, kicker="2 · Instruction", size=96)
w2 = put(MOUSSAR, 90, 330, "moussar", "word", "font-size:190px")
blur_in(w2, A("moussar") - 0.1, 20)
S_(MOUSSAR, "tablette-ecole", 1000, 340, 780, A("moussar") + 0.2, rot=-2)
label_box(MOUSSAR, 1000, 700, "Tablette d'écolier", "Égypte, vers 1900 av. J.-C. · The Met", A("discipline") - 0.3)
tag(MOUSSAR, 90, 620, "« instruction »", A("instruction", 132.0) - 0.1, "", 52)
tag(MOUSSAR, 90, 720, "ou « discipline »", A("discipline") - 0.1, "acc", 52)

# =====================================================================  YIRʾAH (139,9 → 167,0)
t = A("troisième") - 0.4
cam(t, YIRAH)
headline(YIRAH, 170, ["Le troisième mot"], t + 0.1, kicker="3 · Crainte", size=96)
w3 = put(YIRAH, 90, 300, "yirʾah", "word", "font-size:190px")
blur_in(w3, 142.4, 20)
tag(YIRAH, 90, 560, "« la crainte »", 143.9, "acc", 56)
q = quote(YIRAH, 90, 650, "Proverbes 1.7 · Louis Segond 1910",
          "« La crainte de l'Éternel est le commencement de la science ; les insensés méprisent la sagesse et l'instruction. »",
          A("Voici", 144.0), width=1100, size=38)
tag(YIRAH, 1300, 300, "Pas seulement la peur", A("peur") - 0.2, "", 44)
tag(YIRAH, 1300, 400, "Le respect", A("respect") - 0.1, "", 50)
tag(YIRAH, 1300, 500, "L'émerveillement", A("l'émerveillement") - 0.1, "", 50)
tag(YIRAH, 1300, 600, "Qui est Dieu", A("conscience") + 0.4, "acc", 50)
tag(YIRAH, 1300, 700, "Et qui nous sommes", A("sommes") - 0.4, "acc", 50)
ring(YIRAH, 1000, 700, A("peut", 154.0), size=0) if False else None

# =====================================================================  CENTRE (167,0 → 185,8) : un ordre
t = A("ordre") - 0.6
cam(t, CENTRE)
headline(CENTRE, 170, ["Un [ordre]"], t + 0.1, kicker="Proverbes 1.7", hl_t=A("ordre") + 0.05, size=110)
tag(CENTRE, 90, 400, "Pas au centre", A("centre") - 0.2, "", 56)
tag(CENTRE, 90, 520, "Dieu à sa place", A("place") - 0.3, "acc", 56)
S_(CENTRE, "cle", 1620, 200, 190, A("clé", 174.0) - 0.2, rot=6)
stamp(CENTRE, 560, 440, "La clé", A("clé", 174.0) + 0.1, rot=-5, size=84)
bA = put(CENTRE, 90, 660, "« Sois intelligent, et tu trouveras Dieu »", "card", "width:700px;font-size:34px;color:" + THEME["grey"])
blur_in(bA, A("Sois") - 0.2, 14)
bB = put(CENTRE, 880, 660, "« Reconnais Dieu, et l'intelligence commencera »", "card", "width:720px;font-size:34px;border-color:" + ACC)
blur_in(bB, A("reconnais") - 0.2, 14)
arrow(CENTRE, (800, 760), (870, 760), A("reconnais") - 0.1)

# =====================================================================  PÈRE (185,8 → 202,8) : première scène
t = A("prologue") - 0.5
cam(t, PERE)
headline(PERE, 170, ["Deux [scènes]"], t + 0.1, kicker="Proverbes 1.8-33", hl_t=A("scènes") + 0.05, size=104)
c1 = put(PERE, 90, 340, "<small>Scène 1</small>Versets 8 à 19 : un père parle à son fils", "card", "width:820px;font-size:38px")
blur_in(c1, A("Première") - 0.1, 14)
S_(PERE, "pere", 1230, 250, 290, A("père", 190.0) - 0.2, rot=-2)
S_(PERE, "fils", 1590, 280, 190, A("fils", 190.0) - 0.1, rot=3)
quote(PERE, 90, 520, "Proverbes 1.8 · Louis Segond 1910", "« Écoute, mon fils, l'instruction de ton père, et ne rejette pas l'enseignement de ta mère. »",
      A("Écoute"), width=820, size=36)

# =====================================================================  BANDE (202,8 → 219,0) : les hommes qui séduisent
t = A("l'avertit") - 0.7
cam(t, BANDE)
headline(BANDE, 170, ["Des hommes qui veulent te [séduire]"], t + 0.1, kicker="Proverbes 1.10-19", hl_t=A("suivre") + 0.05, size=84)
S_(BANDE, "bande", 1000, 330, 700, A("hommes", 203.0) - 0.2, rot=-2)
tag(BANDE, 90, 400, "Une part du butin", A("butin") - 0.2, "", 54)
tag(BANDE, 90, 510, "Une bourse commune", A("bourse") - 0.2, "", 54)
tag(BANDE, 90, 680, "Le piège se referme sur eux", A("pièges", 212.0) - 0.4, "acc", 52)
burst(BANDE, 600, 440, A("butin") + 0.1)
burst(BANDE, 1000, 700, A("referment") + 0.1)
arrow(BANDE, (850, 760), (1050, 640), A("referment") - 0.1)

# =====================================================================  CHEMINS (219,0 → 226,5) : deux chemins
t = A("Voilà") - 0.5
cam(t, CHEMINS)
headline(CHEMINS, 170, ["Deux [chemins]"], t + 0.1, kicker="Le premier choix du livre", hl_t=A("chemins") + 0.05, size=110)
S_(CHEMINS, "panneau", 800, 330, 420, A("chemins") + 0.2, rot=-2)
tag(CHEMINS, 90, 440, "Celui qui promet vite", A("vite") - 0.3, "", 54)
tag(CHEMINS, 1240, 560, "Celui qui construit lentement", A("lentement") - 0.4, "acc", 50)
hit(A("chemins") + 0.1, 0.7)

# =====================================================================  SAGESSE (226,5 → 274,1) : scène 2
t = A("Seconde") - 0.4
cam(t, SAGESSE)
headline(SAGESSE, 170, ["La Sagesse [prend la parole]"], t + 0.1, kicker="Scène 2 · versets 20-33", hl_t=A("parole") + 0.05, size=88)
S_(SAGESSE, "sagesse-pied", 100, 360, 290, A("Seconde") + 0.3, rot=-3)
q1 = quote(SAGESSE, 520, 380, "Proverbes 1.20-21 · Louis Segond 1910",
           "« La sagesse crie dans les rues, elle élève sa voix dans les places ; elle crie à l'entrée des lieux bruyants ; "
           "aux portes, dans la ville, elle dit ses paroles. »", A("sagesse", 232.0), width=1100, size=38)
fade(q1, A("Une", 242.0) - 0.2)
S_(SAGESSE, "etal", 1560, 360, 300, A("Une", 242.0) + 0.1, rot=3)
tg1 = tag(SAGESSE, 520, 400, "Pas cachée au sommet d'une montagne", A("sommet") - 0.5, "", 42)
tg2 = tag(SAGESSE, 520, 510, "Pas réservée à une élite", A("élite") - 0.5, "", 42)
tg3 = tag(SAGESSE, 520, 640, "Offerte à tous, au milieu du bruit", A("offerte") - 0.2, "acc", 44)
tg4 = tag(SAGESSE, 520, 760, "Mais elle se heurte à un refus", A("refus") - 0.6, "", 42)
for _i in (tg1, tg2, tg3, tg4):
    fade(_i, A("promesse") + 0.1)
burst(SAGESSE, 1640, 380, A("bruit") + 0.1)
q2 = quote(SAGESSE, 520, 380, "Proverbes 1.33 · Louis Segond 1910",
           "« Mais celui qui m'écoute reposera avec assurance ; il vivra tranquille, sans craindre aucun mal. »",
           A("promesse") + 0.3, width=1100, size=42)
S_(SAGESSE, "sagesse-portrait", 1480, 520, 300, A("promesse") + 0.4, rot=3)

# =====================================================================  FRISE (274,1 → 313,4) : trois livres, même base
t = A("Alors,") - 0.3
cam(t, FRISE)
headline(FRISE, 170, ["Une [clé] qui traverse la Bible"], t + 0.1, kicker="Trois livres, la même base", hl_t=A("clé", 274.0) + 0.05, size=88)
quote(FRISE, 70, 360, "Psaume 111.10 · LSG", "« La crainte de l'Éternel est le commencement de la sagesse. »", A("Psaume") - 0.1, width=480, size=30)
quote(FRISE, 650, 360, "Job 28.28 · LSG", "« Voici, la crainte du Seigneur, c'est la sagesse ; s'éloigner du mal, c'est l'intelligence. »",
      A("Voici", 295.0) - 0.4, width=480, size=30)
quote(FRISE, 1230, 360, "Ecclésiaste 12.13 · LSG", "« Crains Dieu, et observe ses commandements. C'est là ce que doit faire tout homme. »",
      A("Crains") - 0.2, width=480, size=30)
S_(FRISE, "or-ornement", 760, 650, 100, A("l'or") - 0.4, rot=-4)
label_box(FRISE, 880, 740, "Comme on cherche de l'or", "ornement en or, Chypre, vers 1200 av. J.-C. · The Met", A("l'or") - 0.2)
burst(FRISE, 350, 720, A("mêmes") + 0.1)
hit(A("mêmes") + 0.1, 0.6)

# =====================================================================  NT (313,4 → 330,7)
t = A("Ensuite") - 0.4
cam(t, NT)
headline(NT, 170, ["Le Nouveau Testament reprend ce [langage]"], t + 0.1, kicker="Matthieu · 1 Corinthiens · Jacques", hl_t=A("langage") + 0.05, size=76)
S_(NT, "jesus-pied", 90, 340, 190, A("Jésus", 313.0) - 0.2, rot=-3)
S_(NT, "salomon", 330, 345, 165, A("Salomon", 313.0) - 0.3, rot=3)
label_box(NT, 90, 790, "Matthieu 12.42", "« plus que Salomon »", A("plus") - 0.1)
S_(NT, "paul-portrait", 700, 350, 300, A("Paul", 313.0) - 0.2, rot=-2)
label_box(NT, 700, 790, "1 Corinthiens 1.24", "« puissance de Dieu et sagesse de Dieu »", A("puissance") - 0.2)
S_(NT, "lettre-papyrus-grec", 1300, 330, 260, A("Jacques", 320.0) - 0.2, rot=3)
label_box(NT, 1300, 790, "Jacques 1.5", "« qu'il la demande à Dieu »", A("demande") - 0.3)
ring(NT, 200, 540, A("Jésus", 313.0), size=300)

# =====================================================================  LECTURES (330,7 → 352,4) : soyons honnêtes
t = A("honnêtes") - 0.6
cam(t, LECTURES)
headline(LECTURES, 170, ["Deux [lectures]"], t + 0.1, kicker="Soyons honnêtes", hl_t=A("lecture", 330.0) + 0.05, size=104)
stamp(LECTURES, 1020, 190, "Tradition chrétienne", A("chrétienne") - 0.2, rot=-4, size=40)
tag(LECTURES, 90, 400, "Jésus = la sagesse de Dieu", A("sagesse", 330.0, 1) - 0.4, "acc", 50)
tag(LECTURES, 90, 520, "Une lecture chrétienne", A("chrétienne") - 0.1, "", 50)
tag(LECTURES, 90, 640, "Pas celle des lecteurs juifs", A("juifs") - 0.2, "", 50)
cA = put(LECTURES, 90, 740, "<small>Ce que dit le texte</small>La sagesse commence par la relation avec Dieu, et elle appelle chacun",
         "card", "width:830px;font-size:30px")
blur_in(cA, A("Ce", 340.0) - 0.1, 14)
cB = put(LECTURES, 1000, 330, "<small>Ce que la tradition chrétienne ajoute</small>Cette sagesse a pris un visage",
         "card", "width:830px;font-size:34px;border-color:" + ACC)
blur_in(cB, A("tradition", 341.0) - 0.2, 14)
S_(LECTURES, "jesus-portrait", 1450, 470, 270, A("visage") - 0.2, rot=3)

# =====================================================================  CLÉ (revisite) 352,4 → 369,0 : une clé de lecture
cam(A("Alors,", 352.0) - 1.8, "all")
wipe(CLE, A("Alors,", 352.0) - 1.9)
t = A("Alors,", 352.0) - 0.4
cam(t, CLE)
headline(CLE, 170, ["Une clé de [lecture]"], t + 0.1, kicker="La réponse", hl_t=A("lecture", 353.0) + 0.05, size=104)
S_(CLE, "cle", 1500, 190, 215, A("lecture", 353.0), rot=-6)
stamp(CLE, 90, 400, "Une clé de lecture", A("clé", 355.0) + 0.4, rot=-4, size=72)
tag(CLE, 90, 600, "Avec humilité", A("humilité") - 0.2, "", 56)
tag(CLE, 90, 700, "Vivre ce que l'on comprend", A("vivre", 360.0) - 0.2, "acc", 56)
tag(CLE, 90, 800, "Plutôt que collectionner des informations", A("collectionner") - 0.4, "", 44)
burst(CLE, 1570, 400, A("lire") + 0.1)

# =====================================================================  CHEMINS (revisite) 369,0 → 382,2 : ton carrefour
wipe(CHEMINS, 368.3)
t = A("Cette", 369.0) - 0.4
cam(t, CHEMINS)
headline(CHEMINS, 170, ["Ton [carrefour]"], t + 0.1, kicker="Cette semaine", hl_t=A("carrefour") + 0.05, size=110)
S_(CHEMINS, "panneau", 1380, 320, 380, A("carrefour") - 0.3, rot=2)
label_box(CHEMINS, 90, 400, "Relis lentement", "les sept premiers versets de Proverbes 1", A("lentement", 369.0) - 0.3)
tag(CHEMINS, 90, 560, "À quel carrefour ?", A("carrefour") - 0.1, "acc", 64)
tag(CHEMINS, 90, 680, "Qu'est-ce que j'entends déjà ?", A("j'entends") - 0.3, "", 52)
ring(CHEMINS, 1570, 460, A("carrefour") + 0.1, size=300)

# =====================================================================  APPEL (382,2 → 392,3) : question de réflexion
t = A("Y", 382.0) - 0.3
cam(t, APPEL)
headline(APPEL, 170, ["Un verset t'a déjà [guidé] ?"], t + 0.1, kicker="À ton tour", hl_t=A("guidé") + 0.05, size=96)
S_(APPEL, "sagesse-portrait", 1380, 300, 360, t + 0.5, rot=3)
label_box(APPEL, 90, 420, "Ou une décision", "pour laquelle tu cherches encore la sagesse ?", A("décision") - 0.2)
cta = put(APPEL, 90, 640, '<svg viewBox="0 0 120 100"><path d="M10 12 h100 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-58 l-22 20 v-20 h-20 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/></svg>Écris-le en commentaire', "cta")
blur_in(cta, A("Écris-le") - 0.2, 14)
sfx("click", A("Écris-le") - 0.2, 0.8)
tag(APPEL, 90, 790, "Sans pression : nous lisons tous ensemble", A("pression") - 0.2, "", 44)

# =====================================================================  MARCHÉ (revisite) 392,3 → fin : la femme crie toujours
cam(A("La", 392.0) - 1.8, "all")
wipe(MARCHE, A("La", 392.0) - 1.9)
t = A("La", 392.0) - 0.4
cam(t, MARCHE)
headline(MARCHE, 170, ["Elle crie [toujours]"], t + 0.1, kicker="Conclusion", hl_t=A("toujours") + 0.05, size=104)
S_(MARCHE, "sagesse-portrait", 1300, 330, 420, A("toujours") - 0.2, rot=-3)
tag(MARCHE, 90, 400, "Pas pour te faire honte", A("honte") - 0.3, "", 56)
tag(MARCHE, 90, 520, "Elle sait où mènent les deux chemins", A("chemins", 393.0) - 0.8, "acc", 50)
tag(MARCHE, 90, 700, "Commencer au bon endroit", A("commencer", 398.0) - 0.2, "acc", 56)
tag(MARCHE, 90, 800, "Reconnaître Dieu à sa place", A("reconnaître") - 0.2, "", 50)
hit(A("reconnaître"), 0.8)

t_end = A("Chaque") - 0.3
cam(t_end, "all")

build(
    chapters=[("01", "Le contexte", 0, 85.1), ("02", "Les trois mots", 85.1, 185.8), ("03", "Les deux scènes", 185.8, 274.1),
              ("04", "Dans toute la Bible", 274.1, 352.4), ("05", "Comment lire", 352.4, 411.9)],
    suppress=[(A("Proverbes", 38.0) + 0.1, 46.2), (A("Pour", 90.0) - 0.1, 109.5), (A("Voici", 144.0) + 0.2, 153.6),
              (A("Écoute") - 0.1, 202.3), (A("La", 232.0) - 0.1, 241.9), (A("Mais", 262.0) - 0.1, 273.8),
              (A("Psaume") + 0.2, 286.0), (A("Voici", 295.0) - 0.2, 301.8), (A("Crains") - 0.1, 312.6),
              (A("Alors,", 352.0) - 1.9, A("Alors,", 352.0) - 0.5), (A("La", 392.0) - 1.9, A("La", 392.0) - 0.5),
              (A("Chaque") - 0.8, 411.9)],
    endcard={"kicker": "Chaque semaine", "title": "La Bible<br />[Simple]", "button": "S'abonner",
             "stickers": [("sagesse-portrait", 150, 560, 330, -6), ("salomon", 1500, 330, 240, 5)]},
    endcard_t=A("Chaque") - 0.1,
    music_volume=0.14,
    retention=True,
)
print("MANQUES:", MANQUES)
