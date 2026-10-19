# La Bible Simple — production vidéo

Dépôt de production des vidéos de la chaîne YouTube « La Bible Simple » (explications bibliques claires, en français). Les échanges avec l'utilisateur se font en français.

## Déroulé pour chaque vidéo

L'utilisateur précise à chaque fois s'il s'agit d'un **short** (1 min à 1 min 10, 9:16) ou d'une **vidéo longue** (16:9).

1. **Titre** : l'utilisateur fournit le titre et le format.
2. **Script** : générer le script avec `prompts/script-short.md` ou `prompts/script-video-longue.md`. Le livrer dans un bloc de texte, ligne par ligne, prêt à copier. Attendre la validation de l'utilisateur.
3. **Prompts d'images** (dès que le script est validé) : prompts en anglais, prêts à copier-coller dans Nano Banana, chacun avec le bloc de style complet (voir plus bas). L'utilisateur génère les images pendant qu'il prépare la voix off.
4. **Voix off** : l'utilisateur la génère ailleurs et l'envoie.
5. **Transcription** : Whisper `whisper-large-v3` via l'API Groq (`https://api.groq.com/openai/v1/audio/transcriptions`), `language=fr`, `response_format=verbose_json`, avec horodatages par mot (`timestamp_granularities[]=word`) pour les sous-titres. Clé lue dans la variable d'environnement `GROQ_API_KEY`. Ne jamais demander de coller une clé dans le chat ; si elle manque, demander de l'ajouter dans les réglages de l'environnement.
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

## Charte visuelle (détail dans `design.md`)

- Aquarelle et encre sur parchemin, bords déchirés, vignette bleu nuit.
- Palette : parchemin `#EFE3C8`, sépia `#8B5E34`, ocre `#C8963E`, bleu nuit `#1E2A44`, encre `#1A1410`, rouille `#8B2E1F`, or `#E8B955`.
- Polices (OFL, fichiers locaux) : Cormorant Garamond (titres), EB Garamond (petites capitales, références), Frank Ruhl Libre (hébreu).
- Tout le texte à l'écran est en HTML, sur des cartes de parchemin déchiré, à l'encre.
- Bloc de style des prompts Nano Banana : `Watercolor and ink illustration, hand-drawn pen lines, aged cream and sepia tones, ochre accents, small navy and rust details ... No text, no letters, no numbers, no writing, no watermark, no photorealism.` Planches : fond blanc uni, éléments isolés et espacés. Décors : sans personnages.

## Règles de montage

- Shorts : 9:16 (1080 × 1920), zones hautes et basses dégagées pour l'interface YouTube.
- Vidéos longues : 16:9, **20 plans au maximum**, qui reviennent pendant la vidéo avec un état différent ; changement d'état toutes les 7 à 20 secondes (mouvement de caméra lent, apparitions en plusieurs temps, alternance décor / gros plan).
- Images d'éléments : toujours `width` et `height` explicites en pixels (une largeur `auto` change de taille d'un worker de rendu à l'autre).
- Effets sonores : 5 à 6 par minute au maximum, sous licence libre (`npx hyperframes media-use resolve --type sfx`), crédits notés dans `CREDITS.md` et dans la description.
- Musique : discrète, environ 20 dB sous la voix, libre de droits pour YouTube. La recherche automatique demande `HEYGEN_API_KEY` dans l'environnement (la connexion OAuth HeyGen ne fonctionne pas depuis le cloud) ; sinon l'utilisateur fournit le fichier.

## Repères

- `montage/short-666/` : premier short complet, modèle de référence (`build.py` génère `index.html` depuis `template.tpl`).
- `montage/test-short-9x16/` : tests de style (v1 à v3).
