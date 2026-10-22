# La Bible Simple — production vidéo

Dépôt de production des vidéos de la chaîne YouTube « La Bible Simple » (explications bibliques claires, en français). Les échanges avec l'utilisateur se font en français.

## Déroulé pour chaque vidéo

L'utilisateur précise à chaque fois s'il s'agit d'un **short** (1 min à 1 min 10, 9:16) ou d'une **vidéo longue** (16:9).

1. **Titre** : l'utilisateur fournit le titre et le format.
2. **Script** : générer le script avec `prompts/script-short.md` ou `prompts/script-video-longue.md`. Le livrer dans un bloc de texte, ligne par ligne, prêt à copier. Attendre la validation de l'utilisateur.
3. **Prompts d'images** (dès que le script est validé) : prompts en anglais, prêts à copier-coller dans Nano Banana, chacun avec le bloc de style complet (voir plus bas). L'utilisateur génère les images pendant qu'il prépare la voix off.
4. **Voix off** : l'utilisateur la génère ailleurs et l'envoie.
5. **Transcription** : Whisper `whisper-large-v3` via l'API Groq (`https://api.groq.com/openai/v1/audio/transcriptions`), `language=fr`, `response_format=verbose_json`, avec horodatages par mot (`timestamp_granularities[]=word`) pour les sous-titres. La clé est un secret réseau de l'environnement : le proxy ajoute l'en-tête `Authorization: Bearer …` aux requêtes vers `api.groq.com`, donc appeler l'API **sans** en-tête d'autorisation. Si l'appel renvoie 401, le secret manque : demander de l'ajouter dans les réglages de l'environnement. Ne jamais demander de coller une clé dans le chat. Repli sans clé : transcription locale `npx hyperframes transcribe assets/voix.wav -m large-v3 -l fr --json -d .` (environ 4 min par minute d'audio) ; si `whisper-cli` plante (SIGILL, selon la machine), utiliser `montage/transcribe_pt.py` (faster-whisper `large-v3` en int8, installé dans un venv ; environ 100 s pour 62 s d'audio ; le pipeline transformers en float32 ou bfloat16 dépasse 14 Go et se fait tuer). Il recolle les mots coupés aux apostrophes. Corriger ensuite l'orthographe des noms propres d'après le script validé (Whisper écrit « Amman », « Mardoché », « Pourim » pour « Haman », « Mardochée », « Purim »). Whisper confond les homophones (« seau » pour « sceau », « leur front » pour « leurs fronts ») : corriger d'après le script validé.
6. **Vérification des images** : absence de texte, de lettres et de chiffres ; pas d'anachronisme ; résolution d'origine (pas de captures d'écran). Signaler ce qui est à refaire, avec un prompt de remplacement.
7. **Découpe** : copier les originaux dans `assets/source/` sous des noms descriptifs, extraire chaque élément des planches en PNG transparent dans `assets/elements/` (détection des composantes sur fond blanc, contrôle visuel sur une planche de contrôle).
8. **Montage** : projet HyperFrames dans `montage/<nom-video>/`, suivre la skill `hyperframes` (puis `general-video` et `hyperframes-core`). `npx hyperframes check` doit passer, puis rendu brouillon (`-q draft`) envoyé pour validation et contrôle d'images clés.
9. **Finalisation** : rendu en qualité `delivery`, puis `titre-description-tags.md` dans le format de `montage/short-666/titre-description-tags.md` (titre, 5 titres courts avec nombre de caractères, description SEO, crédits audio, tags sous 500 caractères).

Committer et pousser à chaque étape qui produit des fichiers.

## Règles éditoriales

- Distinguer ce que dit le texte biblique, la tradition, le consensus historique et les hypothèses. Une hypothèse (ex. Néron = 666) est présentée comme telle.
- Pas de numérologie inventée, pas de clickbait, pas d'événement biblique inventé.
- Citations bibliques complètes en Louis Segond 1910 (domaine public), nommée à la première citation.
- Hébreu et grec : toujours en HTML, jamais dans une image ; faire relire par quelqu'un qui lit la langue avant publication.

## Styles visuels

- **Style 01 « Parchemin aquarelle »** : style des quatre premiers shorts, figé dans `styles/style-01-parchemin-aquarelle.md`. Ne pas le modifier pour tester un autre style : créer un nouveau fichier `styles/style-NN-<nom>.md`, un gabarit séparé et un dossier de projet distinct.
- **Style 02 « Explainer à autocollants »** (inspiré de PaperClip) : **style par défaut des nouvelles vidéos**, sauf si l'utilisateur demande le style 01. Détail dans `styles/style-02-autocollants-explainer.md`. Photos réelles détourées à liseré blanc, personnages aquarelle en autocollants, grande toile et caméra continue, infographies exactes, accent orange unique. Modèle : `montage/short-esther-02/` (`build.py` + `template.tpl`).

### Déroulé propre au style 02 (remplace les étapes 3, 6 et 7 du déroulé général)

Les images viennent de trois sources :
1. **Générées par l'utilisateur (Nano Banana), sur prompts fournis** : seulement ce qu'aucune photo réelle ne montre, surtout les personnages (en général une seule planche de 6 personnages, en pied et en gros plan, dans le style aquarelle du style 01 pour garder une identité constante), parfois une scène précise. Pas de décors : le fond est la toile claire à grille de points.
2. **Cherchées sur internet par Claude** : photos d'objets et de lieux réels (pièces, sceaux, manuscrits, reliefs, sites), uniquement en domaine public ou licence libre compatible avec un usage commercial (Met Open Access `/public/collection/v1.1/search?...&isPublicDomain=true`, autres musées en accès ouvert, Wikimedia Commons). Vérifier la licence de chaque image une par une et la noter dans `CREDITS.md` (titre, institution, lien, licence). Jamais d'image sans licence claire, jamais de marque ni de personne réelle identifiable. Détourage (`npx hyperframes remove-background`, ou par couleur de fond pour les fonds studio unis), puis liseré blanc et ombre. **Montrer la sélection à l'utilisateur avant le montage.**
3. **Fabriquées par Claude** : cartes (fond Natural Earth, domaine public ; tracés historiques annoncés « schématiques »), chronologies, compteurs, schémas, grilles, tableaux.

Ordre : titre et format → script validé → en parallèle, prompts des personnages pour l'utilisateur et recherche des photos par Claude (sélection montrée) → voix off → transcription → détourage et autocollants → montage → brouillon → finalisation.

Si une collection en ligne est inaccessible depuis l'environnement, le dire et passer à une autre. Pour les sujets abstraits (grâce, prière), prévoir plus d'infographies et de personnages, moins de photos.

## Charte visuelle du style 01 (détail dans `design.md`)

- Aquarelle et encre sur parchemin, bords déchirés, vignette bleu nuit.
- Palette : parchemin `#EFE3C8`, sépia `#8B5E34`, ocre `#C8963E`, bleu nuit `#1E2A44`, encre `#1A1410`, rouille `#8B2E1F`, or `#E8B955`.
- Polices (OFL, fichiers locaux) : Cormorant Garamond (titres), EB Garamond (petites capitales, références), Frank Ruhl Libre (hébreu).
- Tout le texte à l'écran est en HTML, sur des cartes de parchemin déchiré, à l'encre.
- Bloc de style des prompts Nano Banana : `Watercolor and ink illustration, hand-drawn pen lines, aged cream and sepia tones, ochre accents, small navy and rust details ... No text, no letters, no numbers, no writing, no watermark, no photorealism.` Planches : fond blanc uni, éléments isolés et espacés. Décors : sans personnages.

## Règles de montage

- Shorts : 9:16 (1080 × 1920), zones hautes et basses dégagées pour l'interface YouTube.
- Vidéos longues : 16:9, **20 plans au maximum**, qui reviennent pendant la vidéo avec un état différent ; changement d'état toutes les 7 à 20 secondes (mouvement de caméra lent, apparitions en plusieurs temps, alternance décor / gros plan).
- Images d'éléments : toujours `width` et `height` explicites en pixels (une largeur `auto` change de taille d'un worker de rendu à l'autre).
- Effets sonores : utiliser la bibliothèque intégrée à HyperFrames (`.agents/skills/media-use/audio/assets/sfx/`, licence Pixabay : usage commercial, aucune attribution obligatoire). `Short(..., lib_sfx=True)` dans `montage/common.py` superpose pour chaque impact `impact-bass-2` + `pop` + `whoosh-short`, car les impacts et la montée de la bibliothèque sont presque uniquement sous 150 Hz (inaudibles sur un haut-parleur de téléphone). Le fichier `riser.mp3` n'a de son que de 0 à 4,5 s (sommet vers 3,5 à 4,3 s) malgré ce que dit son manifeste. Pas plus de 10 à 12 événements par short, impacts seulement sur les mots-clés, « whoosh » seulement aux changements de plan importants. Niveaux : chaque effet environ 10 dB sous la voix (voix seule environ -19 LUFS).
- Musique : générée en local avec MusicGen (`musicgen-small`) via `montage/gen_music.py` (venv Python avec `torch`, `transformers`, `scipy` ; PyTorch s'installe depuis PyPI car download.pytorch.org est bloqué ; environ 160 à 200 s de calcul pour 30 s de musique). Post-traitement : filtre passe-haut 110 Hz, compression légère, fondus, `loudnorm` à -16 LUFS, puis `data-volume` d'environ 0,15 pour rester environ 13 à 15 dB sous la voix. **Licence** : les poids de `musicgen-small` sont en CC-BY-NC 4.0 (non commercial) ; l'usage de l'audio généré dans une vidéo monétisée n'est pas clairement tranché. À signaler à l'utilisateur dans le `CREDITS.md` de chaque vidéo. Alternative : un fichier fourni par l'utilisateur.

## Consignes de rétention (à appliquer à chaque nouvelle vidéo)

Avant le montage
- Première phrase du script : une tension (chiffre, contraste, question), moins de 2,5 s. Premier plan plein cadre dès la première image, jamais une carte vide.
- Une phrase = une image : pas deux idées dans la même phrase.
- Liste de 5 à 8 mots-clés visuels par script, affichés en carte à l'écran au moment exact où le mot est prononcé (horodatage mot par mot).
- Voix off : énergie, pauses courtes, débit un peu plus rapide (5 à 10 %), pas de silence de plus de 0,5 s.
- Images : pleine résolution (au moins 2048 px), avec des personnages en pied et des mains ou objets clés en plus des bustes, pour alterner plans larges et gros plans.

Au montage
- Un seul texte lisible à la fois : sous-titres mot par mot sur une bande sombre ; des cartes seulement pour un mot-clé ou une référence biblique, jamais la même phrase deux fois.
- Un événement visuel toutes les 2 à 3 secondes (anneau doré, tampon « Hypothèse », zoom « coup de poing », flash) ; rien de statique plus de 3 secondes.
- Zones de sécurité : 150 px en haut, 380 px en bas, 140 px à droite (interface YouTube).
- Son : musique discrète sous la voix, quelques impacts sur les mots-clés, effets assez bas pour ne jamais couvrir la voix (voix seule environ -19 LUFS, extras environ 10 dB sous la voix). Vérifier les niveaux élément par élément (mesure `ebur128` après `atrim` et `volume`) : le rendu semble normaliser le total, donc comparer le mix final à la voix seule ne prouve rien.
- Signature de chaîne : mêmes gestes d'une vidéo à l'autre (cartes parchemin, anneau doré, tampon rouge).
- Ne pas boucler la fin du short sur son début (choix de l'utilisateur).

Après la publication
- Suivre dans YouTube Studio la part des spectateurs qui restent au-delà de 3 s et la courbe de rétention ; tester deux accroches sur deux shorts voisins ; envisager une série récurrente. Ce sont des bonnes pratiques, à confirmer par les courbes de la chaîne.

## Repères

- `montage/short-666/` : premier short complet (version 1 publiée ; la version 2 de `build.py` est écrite mais pas rendue).
- `montage/short-marque-sceau/` : deuxième short ; la version 2 (style rétention) a un rendu brouillon.
- `montage/short-noe/` : troisième short ; version complète avec effets de la bibliothèque et musique MusicGen (modèle de référence pour le son).
- `montage/common.py`, `montage/template-short.tpl`, `montage/gen_music.py` (musique), `montage/synth_audio.py` (anciens sons synthétisés, graves inaudibles sur téléphone : à éviter) : base proposée pour les prochains montages (constructeur de plans calés sur la transcription, gabarit commun, sons synthétisés sans droits). Essayée seulement sur le brouillon v2 de « marque et sceau » : la relire avant de s'en servir.
- `montage/short-esther-02/` : short Esther en style 02 (version 2 avec toutes les améliorations) ; modèle de référence du style 02.
- `kit-style-02/` : kit complet et réutilisable du style 02 (guide `GUIDE.md`, moteur `moteur/style02.py` + gabarit paramétré, outils, prompts, exemple Esther qui régénère le même `index.html`). Point de départ des prochains montages en style 02 : `bash kit-style-02/outils/nouveau_projet.sh montage/<nom>`.
- `montage/test-short-9x16/` : tests de style (v1 à v3).
