# Prompts Nano Banana — personnages du style 02

Dans le style 02, on ne génère **que ce qu'aucune photo réelle ne montre**, surtout les personnages, en général une seule planche de 6 par vidéo. Pas de décor : le fond est la toile claire à grille de points.

Le style de dessin des personnages doit rester **le même d'une vidéo à l'autre** : c'est l'identité de la chaîne. Choisir un bloc de style une fois pour toutes et ne plus le changer.

## Bloc de style (celui de « La Bible Simple »)

```
Watercolor and ink illustration, hand-drawn pen lines, aged cream and sepia tones, ochre accents, small navy and rust details.
```

Pour une autre chaîne, on peut garder ce bloc ou le remplacer. Exemple pour une chaîne d'histoire au ton plus moderne :

```
Clean flat vector illustration, soft gradients, muted colors, thin dark outlines, friendly proportions.
```

Le choix fait, il ne change plus.

## Modèle : planche de 6 personnages

```
[BLOC DE STYLE] Pure white background, 2048 x 2048 square. Six separate characters arranged in a 3 x 2 grid with generous spacing, each one isolated with no overlap and no background behind it: top left, [PERSONNAGE 1, en pied, posture, objet tenu]; top middle, head-and-shoulders portrait of [PERSONNAGE 1, expression]; top right, [PERSONNAGE 2, en pied]; bottom left, [PERSONNAGE 3, en pied]; bottom middle, [PERSONNAGE 4, en pied, avec un objet clé dans la main]; bottom right, [GROUPE ou FOULE, 3 ou 4 personnes d'âges différents]. No text, no letters, no numbers, no writing, no watermark, no shadows on the background, no photorealism.
```

### Règles

- Le personnage principal apparaît deux fois sur la planche : **en pied** pour les plans larges, **en gros plan** pour les moments forts.
- Chaque personnage porte un attribut qui l'identifie sans texte : sceptre, rouleau, outil, vêtement.
- Les vêtements et objets sont ceux de l'époque. Vérifier l'absence d'anachronisme.
- Jamais de lettres, de chiffres ni de symboles écrits. Ce qui doit être lu à l'écran est ajouté en HTML.
- Images en 2048 px au moins. Garder les originaux, pas de captures d'écran.

### Exemple rempli (sujet Esther)

Pour le short Esther, les personnages ont été repris de la planche du short Esther en style 01 : `esther-pied`, `esther-portrait`, `mardochee`, `roi-sceptre`, `haman`, `peuple-jeune`, plus l'objet `sac-cendres`. Le prompt ci-dessous montre comment remplir le modèle pour obtenir une planche équivalente.

```
Watercolor and ink illustration, hand-drawn pen lines, aged cream and sepia tones, ochre accents, small navy and rust details. Pure white background, 2048 x 2048 square. Six separate characters arranged in a 3 x 2 grid with generous spacing, each one isolated with no overlap and no background behind it: top left, a young Persian queen standing full body in an embroidered blue and gold robe with a light veil and a small crown, calm and determined; top middle, head-and-shoulders portrait of the same queen, eyes lowered, resolute; top right, an older Jewish man in sackcloth with ashes, full body, hands open; bottom left, a Persian king seated on a throne holding out a long golden scepter; bottom middle, a proud Persian minister in a red embroidered robe holding a rolled decree; bottom right, a small group of four Jewish people of different ages in plain robes, praying together. No text, no letters, no numbers, no writing, no watermark, no shadows on the background, no photorealism.
```

## Après la génération

1. Découper la planche avec `outils/decouper_planche.py`, en donnant les noms dans l'ordre de lecture, puis vérifier `_controle.png`.
2. Transformer chaque élément en autocollant avec `outils/make_sticker.py`, liseré de 16 px pour un personnage.
