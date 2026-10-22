# Style 02 « Explainer à autocollants » — guide complet pour le reproduire

Ce kit permet de refaire à l'identique le style du short « Esther » (`montage/short-esther-02/`) sur n'importe quelle chaîne YouTube. Tout ce qui est propre à « La Bible Simple » (nom, couleur, chapitres, carte de fin) se règle en un seul endroit.

Contenu du dossier `kit-style-02/` :

| Dossier | Contenu |
| --- | --- |
| `GUIDE.md` | ce guide |
| `moteur/style02.py` | moteur de montage : primitives, caméra, sous-titres, son, assemblage |
| `moteur/template.tpl` | gabarit HTML/CSS (couleurs, marque et langue en paramètres) |
| `exemple-esther/` | le short Esther réécrit avec le moteur : il régénère **exactement** le même `index.html` que l'original |
| `outils/` | recherche de photos (Met), découpe de planche, autocollants, carte, musique, transcription, niveaux sonores, création de projet |
| `prompts/` | prompt de script générique, prompts de personnages pour Nano Banana |

---

## 1. Le concept

- **Une seule grande toile** de 3 × 5 écrans en 9:16 (soit 3240 × 9600 px), parcourue par **une caméra continue** : panoramiques et zooms aux accélérations longues, sans coupe ni fondu.
- Chaque écran de la toile est une **station** : un moment du récit, de 3 à 7 secondes.
- Chaque phrase de la voix fait entrer un nouvel élément : autocollant, étiquette, titre, compteur ou carte.
- **Ton** : sérieux, précis, factuel. Infographies exactes : barres à l'échelle, vrais chiffres, sources citées à l'écran.
- **Inspiration** : les vidéos explicatives de PaperClip (回形针). On reprend le langage visuel, jamais la marque ni les noms de série d'un autre créateur.

## 2. Signature visuelle

### Palette (thème par défaut, `THEME_DEFAUT` dans `moteur/style02.py`)

| Rôle | Clé | Valeur |
| --- | --- | --- |
| Accent unique (mot surligné, chiffre clé, trait de caméra, bouton) | `acc` | `#F85830` |
| Toile claire | `bg` | `#E9EDF1` |
| Encre (texte, contours) et fond du mode sombre | `ink` | `#1B242E` |
| Gris des sous-lignes | `grey` | `#6B7785` |
| Gris en mode sombre et flèches | `grey2` | `#8A97A6` |
| Bordure des références et côtes de la carte | `line` | `#AEB8C3` |
| Cases éteintes des grilles | `tile` | `#CBD3DC` |
| Terres de la carte | `land` | `#D3DAE2` |

Une seule couleur vive à l'écran : l'accent. Tout le reste est gris-bleu.

### Fond

- Toile `#E9EDF1` avec une grille de points : `radial-gradient(circle, rgba(ink, .16) 2px, transparent 2.6px)`, pas de 40 px.
- Grain léger par-dessus, opacité 0,05, en bruit SVG animé.
- **Mode sombre** pour la révélation finale : fond `#1B242E`, textes clairs.

### Typographie

- **Inter**, licence OFL, fichier local `assets/fonts/Inter.ttf` (variable, graisses 100 à 900).
- Grand titre : graisse 800, interlettrage −1,5 px, interligne 1,08, de 88 à 124 px selon la longueur (200 px pour une question finale très courte).
- Surtitre (« kicker ») : 26 px, capitales, interlettrage de 5 px, gris, précédé d'un carré d'accent de 18 px.
- Mot clé : souligné par un trait d'accent épais (0,26 em) qui s'étire de gauche à droite (`[mot]` dans `headline`).
- Étiquette : titre de 36 px en gras et sous-ligne grise de 24 px, avec un trait d'accent de 4 px à gauche.
- Bandeau (`tag`) : fond blanc, bordure d'encre de 3 px, ombre décalée de 6 px, ou version pleine en couleur d'accent.
- Référence (`ref`) : 24 px, capitales espacées, gris, cadre fin.
- Pour l'hébreu, le grec et l'arabe : Noto Sans Hebrew, Greek ou Arabic, toujours en HTML et jamais dans une image.

### Autocollants

- Photos réelles **détourées**, avec un **liseré blanc** uniforme et une ombre douce : `drop-shadow(0 18px 22px rgba(ink,.28)) drop-shadow(0 3px 4px rgba(ink,.18))`.
- Épaisseur du liseré selon l'élément :

  | Élément | Liseré |
  | --- | --- |
  | Photo | 12 px |
  | Personnage | 16 px |
  | Petit objet affiché petit | 14 px |

- Les personnages dessinés (aquarelle ou autre style constant) deviennent eux aussi des autocollants. Ils humanisent le récit à côté des photos de musée.
- Légère rotation de −6° à +6°. Entrée en « pop » : échelle 0,55 → 1 avec rebond (`back.out(1.9)`), plus un petit son « pop ».

### Habillage fixe (ne bouge pas avec la caméra)

- **En haut, à 160 px** : la signature de la chaîne (carré d'accent et nom en capitales), puis la **barre de chapitres** (4 chapitres, par exemple Danger · Décision · Retournement · Leçon). Chaque chapitre a sa barre de progression, et le chapitre en cours est en pleine opacité.
- **Sous-titres à 1440 px** : boîte blanche à bordure d'encre, 56 px en gras, au plus 4 mots à la fois. Le mot prononcé passe en couleur d'accent.
- **Carte de fin** : fond sombre, surtitre (« Abonne-toi »), nom de la chaîne avec un mot souligné, bouton plein en couleur d'accent qui pulse, et deux autocollants qui montent.

## 3. Mise en page d'une station (9:16, 1080 × 1920)

| Zone | Contenu |
| --- | --- |
| 0 à 150 px | réservé (interface YouTube) |
| 160 à 260 px | signature et chapitres (fixes) |
| 280 à 480 px | titre de la station (`headline`, y ≈ 280–300) |
| **560 à 1400 px** | **contenu** : autocollants, carte, schéma, compteurs |
| 1250 à 1320 px | bandeau d'accent et référence, en bas du contenu |
| 1440 à 1540 px | sous-titres (fixes) |
| 1540 à 1920 px | réservé (interface YouTube : 380 px en bas) |
| 140 px à droite | réservés (boutons YouTube) : rien d'important au-delà de x = 940 |

En 16:9 (vidéo longue), le moteur passe automatiquement en 1920 × 1080. Les sous-titres montent alors à 880 px et la barre de chapitres à 60 px. Il faut recaler les positions des éléments dans chaque station.

## 4. Mouvement (valeurs exactes)

| Geste | Réglage |
| --- | --- |
| Déplacement de caméra | 0,75 s, `power3.inOut` ; vue d'ensemble 0,95 s |
| Flou de mouvement | 5 px en aller-retour pendant le déplacement (2 px vers ou depuis la vue d'ensemble) |
| Trait de caméra | ligne d'accent de 10 px tracée de la station quittée à la suivante (à 62 % de la hauteur), effacée 0,3 s après l'arrivée |
| Dérive | zoom lent de 1 à 1,035 sur toute la durée où l'on reste sur une station |
| Entrée de texte | défloutage : flou 14 px → 0, montée de 24 px, 0,55 s, `power3.out` |
| Autocollant | pop 0,6 s `back.out(1.9)` ; ou `instant=True` (visible dès la 1re image, zoom 1,14 → 1) pour l'accroche |
| Ligne de rappel | tracé en 0,4 s, puis point d'accent qui apparaît |
| Bandeau | s'ouvre de gauche à droite en 0,35 s |
| Compteur | défile en `power2.out`, avec un tic-tac si la durée dépasse 0,5 s |
| Vue d'ensemble | zoom arrière sur toute la toile au retournement (milieu de la vidéo) et à la fin |
| Rythme | un nouvel état toutes les 1 à 3 s, jamais plus de 3 s immobiles |

## 5. Son

| Élément | Source | Volume (`data-volume`) | Cible |
| --- | --- | --- | --- |
| Voix | voix off | 1 | environ −19 LUFS |
| Musique | MusicGen, prompt « tech explainer » | 0,15 | 13 à 15 dB sous la voix (−33,8 LUFS dans Esther) |
| Souffle (déplacement de caméra) | `whoosh-short` | 0,10 × 0,9 | environ 10 dB sous la voix |
| Clic (étiquette, case) | `click-soft` | 0,22 × 0,5 à 0,8 | idem |
| Pop (autocollant) | `pop` | 0,28 × 0,32 | idem |
| Temps fort (`hit`) | `impact-bass-2` 0,07 + `pop` 0,28 × 1,4 | | l'impact seul est inaudible sur téléphone (graves sous 150 Hz), d'où le pop superposé |
| Compteur | `typing` | 0,12 × 0,25 | |
| Éclat | `sparkle` | 0,06 | |

- **Effets** : bibliothèque intégrée à HyperFrames (`.agents/skills/media-use/audio/assets/sfx/`), licence Pixabay : usage commercial, aucune attribution obligatoire.
- Temps forts seulement sur les mots-clés : de 6 à 10 par short.
- **Musique** : `outils/gen_music.py`. Post-traitement :
  ```
  ffmpeg -i brut.wav -af "highpass=f=110,acompressor=threshold=0.08:ratio=3:attack=80:release=600:makeup=1,afade=t=in:d=1.5,afade=t=out:st=<durée-2>:d=2,loudnorm=I=-16:TP=-2:LRA=4" assets/audio/music.wav
  ```
  `build()` ajoute ensuite la piste à 0,15 si `assets/audio/music.wav` existe.
- **Vérifier les niveaux élément par élément** avec `outils/mesure_niveaux.sh` (découpe et volume appliqués avant la mesure). Le rendu semble normaliser le total, donc comparer le mix final à la voix seule ne prouve rien.

## 6. Déroulé complet d'une vidéo

1. **Titre et format.** Short 9:16 (1 min à 1 min 10) ou vidéo longue 16:9.
2. **Script.** Utiliser `prompts/script-short.md`. Il est livré ligne par ligne et validé, avec 5 à 8 mots-clés visuels.
3. **Images, en parallèle**, selon trois sources (section 7) :
   - prompts de personnages pour Nano Banana (`prompts/personnages-nano-banana.md`) ;
   - recherche de photos libres ;
   - liste des infographies à fabriquer.

   **Montrer la sélection de photos avant le montage.**
4. **Voix off.** Énergique, pauses courtes, débit 5 à 10 % plus rapide qu'une lecture normale, jamais plus de 0,5 s de silence.
5. **Transcription mot par mot** vers `transcript.json` (section 9).
6. **Corriger la transcription** d'après le script validé : noms propres, homophones, apostrophes.
7. **Découpe et autocollants.** Utiliser `outils/decouper_planche.py` puis `outils/make_sticker.py`. Contrôler sur la planche de contrôle.
8. **Montage.**
   - Créer le projet : `bash outils/nouveau_projet.sh ../montage/<nom>`.
   - Écrire les stations dans `build.py` (section 8).
   - Lancer `python3 build.py`, puis `npx hyperframes check`, qui doit passer sans erreur.
9. **Brouillon.**
   - Rendu : `npx hyperframes render -q draft -o renders/<nom>-draft.mp4`.
   - Contrôle visuel des images clés : `npx hyperframes snapshot --at 0,5,12,30,61`.
10. **Finalisation.**
    - Rendu final : `npx hyperframes render -q delivery`.
    - Fichier `titre-description-tags.md` : titre, 5 titres courts avec leur nombre de caractères, description SEO, crédits audio, tags sous 500 caractères.
    - Fichier `CREDITS.md` complet.

## 7. Les trois sources d'images

### 7.1 Générées (Nano Banana) : seulement ce qu'aucune photo ne montre

- Surtout les personnages, sur une planche de 6 en général. Le personnage principal y figure en pied et en gros plan.
- Pas de décors : le fond est la toile.
- Fond blanc uni et éléments espacés, pour que la découpe automatique fonctionne.
- Jamais de texte, de lettres ni de chiffres dans l'image. Vérifier aussi l'absence d'anachronisme.

### 7.2 Cherchées sur internet : photos réelles en domaine public ou sous licence libre commerciale

- **Met Open Access** (CC0) : `python3 -I outils/met_search.py chercher "Achaemenid gold" "Persepolis relief"`, puis `telecharger <ids>`. Le script revérifie `isPublicDomain` objet par objet et prépare les lignes de crédits.
  - Recherche : `/public/collection/v1.1/search?q=…&hasImages=true&isPublicDomain=true&limit=25`. L'ancienne route `/v1/search` répond 410.
  - Détail d'un objet : `/public/collection/v1/objects/{id}` (champs `isPublicDomain`, `primaryImage`, `objectURL`, `creditLine`). Ignorer les objets qui répondent 404.
- **Autres musées en accès ouvert** : Art Institute of Chicago, Rijksmuseum, Smithsonian Open Access, Cleveland Museum of Art, Getty, Paris Musées. Pour chacun, ne garder que les images marquées CC0 ou domaine public.
- **Wikimedia Commons** : licence à vérifier fichier par fichier. Accepter seulement le domaine public, CC0, CC BY ou CC BY-SA ; les deux dernières imposent l'attribution, et CC BY-SA son partage à l'identique. **Refuser** NC (non commercial) et ND (pas de modification, or le détourage est une modification).
- **Interdits** : image sans licence claire, marque, personne réelle identifiable.
- **Crédits** : noter chaque image dans le `CREDITS.md` de la vidéo (titre, institution, lien, licence, ligne de crédit).
- **Détourage** :
  - cas général : `npx hyperframes remove-background photo.jpg -o cut.png` ;
  - objet sur fond studio uni : `make_sticker.py --fond-uni 24` (tolérance de 22 à 28).
- Si une collection est inaccessible depuis l'environnement, le dire et passer à une autre.

### 7.3 Fabriquées : infographies exactes

| Infographie | Comment la fabriquer |
| --- | --- |
| Carte | `outils/make_map.py` avec un fichier de réglages (voir `exemple-esther/carte-esther.json`), puis `map_svg()` dans le montage. Fond Natural Earth (domaine public). Toute zone tracée à la main est annoncée à l'écran comme « tracé schématique ». |
| Chronologie | ligne verticale qui se trace, points et étiquettes (station S9 de l'exemple) |
| Compteur | `counter()` |
| Barres à l'échelle | `bar_to_scale()`, avec l'échelle écrite dans l'étiquette (« ≈ 22 m, même échelle ») |
| Schéma de décision | boîtes `.box` et flèches SVG (station S4) |
| Cases d'étapes ou de jours | `boxes()` |

Pour un sujet abstrait, prévoir plus d'infographies et de personnages, et moins de photos.

## 8. Écrire le montage avec le moteur

Point de départ : `exemple-esther/build.py`, copié par `nouveau_projet.sh`. Garder la structure et remplacer les stations.

```python
import style02 as s
THEME = {"brand": "Ma Chaîne", "title": "Ma Chaîne - Sujet", "lang": "fr", "acc": "#F85830"}
s.setup(here=HERE, duration=61.0, cols=3, rows=5, theme=THEME)   # fmt="16:9" pour une vidéo longue
from style02 import *          # après setup

S1, S2, S3 = (0, 0), (1, 0), (2, 0)    # stations : (colonne, rangée) ; parcours en serpentin
cam(0, S1)                                                        # la caméra est sur S1 au départ
sticker(S1, "objet-cle", 50, 600, 640, 0.0, rot=-4, instant=True) # accroche visible dès la 1re image
headline(S1, 300, ["Première ligne", "avec un [mot clé]"], 0.0, kicker="Explication · Sujet", hl_t=T("clé") + 0.2)
tag(S1, 60, 1250, "= le chiffre choc", T("choc"), "acc", 64)
hit(T("choc"))
cam(T("ensuite") - 0.2, S2)                                       # passage à la station suivante
...
cam(34.7, "all")                                                  # vue d'ensemble au retournement
dark_mode(50.6)                                                   # révélation en mode sombre
cam(59.65, "all")                                                 # vue d'ensemble finale
build(chapters=[("01", "Contexte", 0, 17.8), ("02", "…", 17.8, 34.8), ("03", "…", 34.8, 50.6), ("04", "…", 50.6, DUR)],
      suppress=[(59.6, DUR)],
      endcard={"kicker": "Abonne-toi", "title": "Ma<br />[Chaîne]", "button": "S'abonner",
               "stickers": [("objet-cle", 40, 1180, 380, -6), ("personnage", 790, 1060, 240, 5)]},
      endcard_t=60.2)
```

### Primitives

| Fonction | Rôle |
| --- | --- |
| `T("mot", n)` | début de la n-ième occurrence d'un mot (insensible à la ponctuation et à la casse) : tout se cale dessus |
| `sticker(station, nom, x, y, largeur, t, rot, label=, sub=, instant=)` | autocollant, avec étiquette et ligne de rappel facultatives |
| `headline(station, y, lignes, t, kicker=, sub=, size=, dark=, hl_t=)` | grand titre ; `[mot]` souligné à `hl_t` |
| `label_box(station, x, y, titre, sous_titre, t, dark=)` | étiquette |
| `tag(station, x, y, texte, t, "acc" ou "" ou "dark", taille)` | bandeau |
| `ref(station, x, y, texte, t)` | référence de source |
| `counter(station, x, y, de, à, t, durée, unité, taille, "small" ou "dark")` | compteur |
| `boxes(station, x, y, libellés, t)` | cases qui s'allument une à une |
| `bar_to_scale(station, x, base_y, hauteur, t, width=, acc=, dur=)` | barre à l'échelle |
| `map_svg(station, x, y, "assets/map.json", t_affichage, t_tracé)` | carte |
| `leader(station, a, b, t)` | ligne de rappel seule |
| `put(station, x, y, html, classe)` + `blur_in(id, t)` / `pop(id, t)` / `tween(sel, de, vers, t)` | élément libre |
| `cam(t, station ou "all")` | caméra |
| `dark_mode(t)` | passage au fond sombre |
| `sfx(type, t, facteur)` / `hit(t, facteur)` | effets sonores |
| `build(chapters, suppress, endcard, endcard_t, music_volume=0.15)` | assemble `index.html` |

Les coordonnées x et y sont **relatives à l'écran de la station** (0 à 1080, 0 à 1920).

### Règles de rythme et de rétention

- Accroche en moins de 2,5 s. Première image pleine, jamais vide : un autocollant `instant=True` et le titre.
- Une phrase = une image ; un événement toutes les 2 à 3 s.
- Un seul texte lisible à la fois. Pendant une citation affichée en grand, couper les sous-titres (`suppress`).
- Mots-clés soulignés ou en bandeau au moment exact où ils sont prononcés.
- Un temps fort unique vers 60 à 75 % de la durée. Image finale tenue de 0,8 à 1,2 s.
- Ne pas faire boucler la fin sur le début.
- Images d'éléments toujours avec `width` et `height` en pixels (le moteur le fait).

## 9. Installation des outils

| Outil | Installation |
| --- | --- |
| Node 22 et HyperFrames | `npx hyperframes --version` ; compétences pour l'agent : `npx skills add heygen-com/hyperframes` |
| Python 3 | `pip install pillow numpy` (moteur et outils d'image) |
| ffmpeg | requis pour la transcription locale et la mesure des niveaux |
| Musique | venv avec `torch`, `transformers`, `scipy`. PyTorch s'installe depuis PyPI si download.pytorch.org est bloqué. Compter 160 à 200 s de calcul par tranche de 30 s. |
| Transcription locale | venv avec `faster-whisper`, puis `python3 outils/transcribe_pt.py assets/voix.wav transcript.json` (environ 100 s pour 1 min d'audio, recolle les mots coupés aux apostrophes) |

**Transcription par l'API Groq**, la plus rapide : `whisper-large-v3`, `language=<langue>`, `response_format=verbose_json`, `timestamp_granularities[]=word`.

- La clé se met en **secret réseau de l'environnement**, jamais dans le chat.
- Sans clé, utiliser en priorité `npx hyperframes transcribe assets/voix.wav -m large-v3 -l fr --json -d .`.
- Si cette commande plante (SIGILL), passer à `transcribe_pt.py`.

Format attendu de `transcript.json` : `[{"text": "mot", "start": 0.12, "end": 0.40}, ...]`.

## 10. Licences : ce qui est sûr et ce qui ne l'est pas

| Élément | Licence | Usage commercial |
| --- | --- | --- |
| Photos Met Open Access | CC0 | oui, sans attribution (la citer quand même dans `CREDITS.md`) |
| Natural Earth | domaine public | oui |
| Effets HyperFrames | Pixabay Content License | oui, sans attribution |
| Police Inter | SIL OFL 1.1 | oui (joindre `OFL-Inter.txt`) |
| GSAP | licence GSAP « Standard » (gratuite) | oui |
| **Musique MusicGen** | poids de `musicgen-small` en **CC-BY-NC 4.0** | **pas clairement tranché pour une vidéo monétisée** : le signaler dans `CREDITS.md`, ou utiliser une musique dont la licence est claire |
| Images Nano Banana | conditions de Google | vérifier les conditions en vigueur au moment de la publication |

## 11. Adapter le kit à une autre chaîne : liste de contrôle

1. Dans `THEME` : `brand`, `title`, `lang`, et éventuellement `acc` (une seule couleur vive, bien contrastée sur `#E9EDF1` et sur `#1B242E`).
2. Les libellés des 4 chapitres dans `build(chapters=…)`.
3. La carte de fin (`endcard`) : surtitre, nom de la chaîne avec un mot entre crochets, bouton, deux autocollants.
4. Le bloc de style des personnages, choisi une fois puis gardé (`prompts/personnages-nano-banana.md`).
5. Le prompt de script (`prompts/script-short.md`) : nom, thème, langue, règles d'exactitude du domaine.
6. Le prompt de musique (`PROMPT` dans `outils/gen_music.py`) : garder « modern minimal tech explainer underscore, soft plucked synth arpeggio, warm pad, light steady pulse » et changer seulement la couleur (« subtle ancient middle-eastern color » pour la Bible).
7. Les sources de photos propres au thème : musées et collections du domaine.
8. Ne pas toucher aux valeurs de mouvement, de mise en page et de son : ce sont elles qui font le style.

## 12. Contrôles avant publication

- [ ] `npx hyperframes check` sans erreur. Les avertissements « line_unread » sur les sous-titres calés sur la voix sont normaux.
- [ ] Première image pleine (accroche visible), aucune image noire ou vide de plus de 0,3 s.
- [ ] Rien d'important dans les zones réservées (haut 150 px, bas 380 px, droite 140 px).
- [ ] Aucun texte, lettre ni chiffre dans les images générées ; pas d'anachronisme.
- [ ] Chiffres et échelles exacts, sources à l'écran, hypothèses annoncées comme telles.
- [ ] Niveaux : voix environ −19 LUFS, effets environ 10 dB dessous, musique 13 à 15 dB dessous ; rendu final autour de −16 LUFS.
- [ ] `CREDITS.md` complet (chaque photo avec sa licence, carte, musique avec sa réserve, effets, police).
- [ ] `titre-description-tags.md` prêt.
