# Style 01 — « Parchemin aquarelle » (style actuel de la chaîne)

Style utilisé pour les shorts « 666 », « Marque et sceau », « Noé » et « Esther ». Figé ici pour pouvoir y revenir à l'identique pendant qu'on teste d'autres styles.

Dernier commit de référence : `a758343` (branche `claude/clever-goodall-ssie1g`).

## Images (génération Nano Banana)

- Aquarelle et encre sur parchemin, traits à la plume, bords irréguliers, vignette bleu nuit.
- Bloc de style à coller dans chaque prompt :
  `Watercolor and ink illustration, hand-drawn pen lines, aged cream and sepia tones, ochre accents, small navy and rust details. ... No text, no letters, no numbers, no writing, no watermark, no photorealism.`
- Planches : fond blanc uni, éléments isolés et espacés (6 personnages en 3 × 2, 12 objets en 4 × 3). Décors : verticaux 9:16, sans personnage, tiers supérieur calme pour les cartes.
- Découpe en PNG transparents dans `assets/elements/`, originaux dans `assets/source/`.

## Palette

| Rôle | Hex |
| --- | --- |
| Parchemin | `#EFE3C8` |
| Vieux papier | `#D9C49A` |
| Sépia | `#8B5E34` |
| Ocre | `#C8963E` |
| Bleu nuit | `#1E2A44` |
| Encre | `#1A1410` |
| Rouille | `#8B2E1F` |
| Or | `#E8B955` / `#F6D77F` |

## Typographie (fichiers OFL locaux)

- Titres et mots-clés : Cormorant Garamond (gras, italique pour les cartes).
- Références et petites capitales : EB Garamond.
- Hébreu : Frank Ruhl Libre.

## Montage

- Cartes de parchemin déchiré (`clip-path` irrégulier, texture `parchemin.jpg`), mots-clés « héros » en grand avec contour encre, anneaux dorés, tampon rouge, flash doré, zoom « coup de poing ».
- Sous-titres mot par mot sur une bande sombre, mot en cours en doré.
- Barre de progression dorée, grain de film, poussières dorées, vignette.
- Code : `montage/common.py` (constructeur de plans calés sur la transcription), `montage/template-short.tpl` (gabarit HTML/CSS), `build.py` de chaque short.

## Son

- Effets de la bibliothèque HyperFrames (Pixabay), impacts superposés à un « pop » pour être audibles sur téléphone.
- Musique : MusicGen small en local, ou fichier fourni.

## Vidéos de référence

- `montage/short-noe/` : modèle complet pour le son.
- `montage/short-esther/` : modèle complet le plus récent.
- `montage/short-marque-sceau/` et `montage/short-666/` : versions antérieures du même style.

## Pour y revenir

Ne pas modifier `montage/template-short.tpl` ni `montage/common.py` pour un autre style : créer un gabarit séparé (par exemple `montage/template-short-02.tpl`) et un dossier de projet distinct.
