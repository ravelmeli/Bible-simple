# Règles pour générer les images avec Nano Banana (version économe)

Rôle : tu prépares les prompts d'images d'une vidéo explicative en style « autocollants » (photos réelles détourées + personnages dessinés, sur une toile claire). Le but : **une seule génération par vidéo**, réutilisable, sans retouche.

## 1. Ne générer que ce qu'aucune photo libre ne montre
- Les objets, lieux, monnaies, manuscrits, sites : chercher d'abord des photos en domaine public (Met Open Access, autres musées en CC0, Wikimedia Commons avec licence vérifiée).
- Les cartes, chronologies, compteurs, schémas : les fabriquer en code, jamais en image générée.
- Ne générer que : les personnages, quelques animaux, une scène d'action précise, un objet symbolique sans équivalent réel.
- **Jamais de décor ni de paysage** : le fond de la vidéo est la toile claire.

## 2. Une seule planche par vidéo
- **Une image carrée 2048 × 2048 avec 6 éléments** (grille 3 × 2), ou 4 éléments (2 × 2) si les éléments sont grands.
- Le personnage principal apparaît **deux fois** : en pied (plans larges) et en gros plan tête et épaules (moments forts).
- Compléter avec : les personnages secondaires, une scène d'action, un groupe, un animal ou un objet clé (ex. une main qui tient quelque chose).
- Décrire chaque case par sa position : « top left, … ; top middle, … ; bottom right, … ».

## 3. Une planche facile à découper automatiquement
- « Pure white background », « each one isolated with no overlap and no background behind it », « generous spacing ».
- « no shadows on the background » (une ombre au sol gêne le détourage).
- Les éléments ne doivent pas se toucher : sinon la découpe les mélange.

## 4. Un bloc de style identique à chaque vidéo
- Choisir **une fois** le bloc de style de la chaîne et ne plus le changer : c'est l'identité visuelle, et les personnages restent réutilisables d'une vidéo à l'autre.
- Exemple (aquarelle) : « Watercolor and ink illustration, hand-drawn pen lines, aged cream and sepia tones, ochre accents, small navy and rust details. »
- Toujours finir par : « No text, no letters, no numbers, no writing, no watermark, no shadows on the background, no photorealism. »

## 5. Éviter les erreurs qui obligent à regénérer
- **Aucun texte** dans l'image : rouleaux vierges, pièces sans inscription, pierres lisses (« blank », « no symbols », « no engraving »). Les vrais textes viennent des photos ou sont écrits en HTML.
- **Pas d'anachronisme** : préciser l'époque et la matière (« 9th century BC », « scale armor made of small overlapping bronze scales », « simple brown wool robe »). Sinon l'IA dessine des armures romaines, des kippas, des turbans modernes.
- **Pas de personne réelle identifiable**, pas de marque ; un personnage moderne (ex. archéologue) est vu de dos ou de trois quarts, visage caché.
- Sujets sensibles (blessé, sacrifice) : « not bloody, not graphic », « no animal visible on the altar ».
- Le même personnage doit garder la même tenue dans ses deux cases : décrire la tenue une fois, puis écrire « the same [personnage] ».

## 6. Réutiliser avant de générer
- Tenir une bibliothèque des éléments déjà découpés (personnages, animaux, objets) et la consulter avant chaque vidéo.
- Un personnage récurrent (Jésus, Moïse, Noé…) n'est généré qu'une fois et repris ensuite.

## 7. Si une case est ratée
- Ne pas regénérer la planche entière : regénérer **une seule case** avec un prompt court « A single full-body character, isolated, no background: … » + le même bloc de style.

## Modèle de prompt (à remplir)

```
[BLOC DE STYLE]. Pure white background, 2048 x 2048 square. Six separate elements arranged in a 3 x 2 grid with generous spacing, each one isolated with no overlap and no background behind it: top left, [personnage principal, en pied, époque, tenue, objet tenu, attitude]; top middle, head-and-shoulders portrait of the same [personnage], [expression]; top right, [personnage secondaire, en pied]; bottom left, [groupe ou scène d'action]; bottom middle, [animal ou objet clé, sans inscription]; bottom right, [gros plan d'une main ou d'un objet symbolique]. No text, no letters, no numbers, no writing, no watermark, no shadows on the background, no photorealism.
```

## Contrôle à la réception
1. Aucun texte, lettre ou chiffre visible.
2. Rien d'anachronique.
3. Résolution d'origine (pas de capture d'écran), au moins 2000 px.
4. Éléments bien séparés sur fond blanc.
Si un point échoue : regénérer seulement la case concernée (règle 7).
