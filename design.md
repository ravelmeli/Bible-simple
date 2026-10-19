# Charte visuelle — La Bible Simple

Référence de style pour les vidéos de la chaîne « La Bible Simple ». Les couleurs et polices ci-dessous sont des estimations tirées des visuels de référence : à valider sur les fichiers originaux avant publication.

## Principe

Un manuscrit ancien qu'on explique à la lumière d'une lampe. Le papier, l'encre et la plume sont les matières de base. Le ton reste sobre, lisible et respectueux, sans effets spectaculaires.

## Matières et styles d'image

Deux familles, à ne pas mélanger dans une même scène :

1. **Illustration aquarelle et encre** (dominante) : traits à la plume, lavis, bords de papier irréguliers, vignette bleu nuit sur les bords. Pour les scènes historiques, les lieux et les personnages.
2. **Infographie sur parchemin** (texte, schémas, tableaux) : parchemin crème craquelé, cadre à double filet, lettrage serif. Pour les chiffres, les équations, les listes et les comparaisons.

**À éviter :** les photographies réalistes (ex. fragments sur ardoise avec loupe), les fonds blancs purs, les personnages en 3D.

## Palette

| Rôle | Nom | Hex (estimé) | Usage |
| --- | --- | --- | --- |
| Fond principal | Parchemin | `#EFE3C8` | Fonds de scène, cartes |
| Papier vieilli | Vieux papier | `#D9C49A` | Bords, fragments |
| Sépia | Sépia | `#8B5E34` | Cadres, traits secondaires |
| Ocre | Ocre | `#C8963E` | Accents, ornements |
| Bleu nuit | Nuit | `#1E2A44` | Vignettes, scènes sombres |
| Encre | Encre | `#1A1410` | Texte principal, traits |
| Brun rouille | Rouille | `#8B2E1F` | Mise en valeur (ex. « 666 », nœuds) |
| Terre cuite | Terre | `#C4623F` | Médaillons, nœuds de schéma |
| Or | Or | `#E8B955` | Chiffres, lumière, filets dorés |

**Règle :** un seul accent fort par plan (rouille *ou* or). Le bleu nuit ne sert qu'aux vignettes et aux plans dramatiques.

## Typographie

| Usage | Police suggérée | Remarque |
| --- | --- | --- |
| Titres | Cormorant Garamond (Google Fonts) | Capitales et petites capitales |
| Titres manuscrits | Caveat ou Cormorant Italic | Pour les légendes de carnet |
| Corps de texte | EB Garamond (Google Fonts) | Lisibilité à l'écran |
| Hébreu | Frank Ruhl Libre ou Noto Serif Hebrew | Toujours en HTML, jamais dans une image |
| Grec / latin | EB Garamond | Vérifier la présence des glyphes |

Taille minimale du texte à l'écran : 36 px en 1920 × 1080, 48 px en 1080 × 1920.

## Texte

- **Tout le texte est en HTML**, y compris les titres, les légendes, les chiffres, l'hébreu, le grec et le latin.
- Les visuels générés ne contiennent aucun texte. Les images existantes avec du texte intégré (gématrie, « La séduction », légendes) sont à régénérer sans texte ou à recouvrir.
- Les caractères hébreux, grecs et latins doivent être vérifiés par une personne qui les lit avant publication.

## Cadres et formats

- **16:9** (YouTube long) : zone de sécurité de 5 % sur chaque bord.
- **9:16** (shorts) : texte à au moins 8 % du haut et du bas (zones d'interface).
- Les visuels de référence sont verticaux (environ 2:3). Pour le 16:9, prévoir un recadrage ou un visuel horizontal dédié, pas un étirement.

## Mouvement

- Zoom lent (1,00 → 1,05 sur la durée du plan), parallaxe légère entre fond et premier plan.
- Texte et schémas apparaissent par fondu ou tracé de trait (2 à 4 secondes), jamais par effet rebondissant.
- Transitions : fondu au noir ou fondu sur le parchemin. Pas de balayage rapide.

## Fond sonore et rythme

Voir le plan vidéo une fois la structure créée. Ce fichier ne couvre que l'image.

## Éléments réutilisables (kit)

- Fond parchemin avec bords déchirés (2048 × 2048 à générer, sans texte).
- Cadre à double filet pour les infographies.
- Médaillons et nœuds terre cuite pour les schémas.
- Personnages et objets extraits : voir `elements_666` (18 PNG transparents).

## Cohérence

Une vidéo doit garder la même palette, le même type de papier et la même police de titre. Les nouveaux visuels doivent être comparés à ce fichier avant d'être ajoutés.
