# Style 02 — « Explainer à autocollants » (inspiré de PaperClip / 回形针)

Style en test. Le style 01 « Parchemin aquarelle » reste la référence (`styles/style-01-parchemin-aquarelle.md`) et ne doit pas être modifié pour ce style.

Source : une vidéo de référence de 10 s (16:9) et le prompt qui l'a produite, fournis par l'utilisateur. On reprend le langage visuel, jamais la marque de l'auteur (pas de « GEWU LAB », pas de nom de série copié).

## Principe

Une seule grande toile (par exemple 6000 × 3000 px en 16:9, ou 2400 × 6000 px en 9:16) parcourue par une caméra continue : panoramiques et zooms aux accélérations longues, sans coupe ni fondu. Chaque phrase de la voix fait entrer un nouvel élément visuel. Le ton est sérieux, précis, factuel.

## Signature visuelle (à respecter)

- **Autocollants** : photos réelles détourées, liseré blanc uniforme de 8 à 12 px, ombre douce. Le liseré harmonise des images de sources différentes.
- **Fond** : gris-bleu très pâle (`#E9EDF1`) avec une fine grille de points. Fin en mode sombre (`#1B242E`) pour la révélation.
- **Couleurs** : 2 ou 3 couleurs plus un seul accent vif (orange-rouge, environ `#F85830`), réservé au mot surligné, aux éléments importants et au chiffre clé.
- **Typographie** : sans-serif régulière (OFL, fichier local : Inter ou Manrope ; Noto Sans Hebrew pour l'hébreu). Grand titre en gras sur deux lignes, petite étiquette en capitales espacées au-dessus, sous-ligne grise en dessous, mot clé souligné d'un trait épais orange.
- **Infographies exactes** : étiquettes reliées aux objets par des lignes fines, grilles qui s'allument case par case, compteurs, barres à l'échelle, cartes avec arcs qui se dessinent, chronologies.
- **Navigation** : fil de chapitres en bas (01 Contexte · 02 Texte · 03 Histoire · 04 Leçon), chapitre en cours souligné en orange ; signature de la chaîne en bas à gauche.
- **Mouvement** : un nouvel état toutes les 1 à 2 s, flou de mouvement sur les déplacements rapides de caméra, texte qui se « défloute » à l'entrée, zoom arrière final.

## Transposition biblique

- Grilles : les 22 lettres hébraïques et leur valeur (gématrie), les 12 tribus, les livres de la Bible, les rois et empires.
- Cartes : empires (Perse, Rome), lieux (Patmos, Suse, Jérusalem), routes.
- Compteurs : 666, 300 coudées, 8 personnes, 3 jours.
- Chronologies : dates de règnes, périodes de rédaction.
- Autocollants : objets archéologiques réels (sceaux, monnaies, tablettes, manuscrits, sites).
- Les règles éditoriales de `CLAUDE.md` s'appliquent sans changement (hypothèse présentée comme telle, citations Louis Segond 1910, hébreu relu).

## Images : sources et licences

- Priorité aux photos d'objets de musées publiées en **CC0 / domaine public** (collections en accès ouvert). Vérifier la licence de chaque photo une par une et la noter dans `CREDITS.md` (titre, institution, lien, licence).
- Les éléments aquarelle déjà découpés peuvent servir d'autocollants en dépannage (liseré blanc ajouté), mais le style est plus fidèle avec des photos.
- Jamais de marque réelle ni de visage de personne réelle identifiable.

## Exigences de fabrication (reprises du prompt d'origine)

- Accroche dans la première demi-seconde, jamais plus de 0,3 s d'écran vide ou noir.
- Une montée, un temps fort unique vers 60 à 75 % de la durée, une image finale tenue 0,8 à 1,2 s avec un léger mouvement.
- Une feuille de rythme unique (temps forts) partagée par l'image et le son.
- Rendu déterministe (chaque image ne dépend que du temps), comme HyperFrames.
- Son : nappe sobre de type « explainer tech », clics d'interface, tic-tac pendant les compteurs, souffle doux sur les mouvements de caméra.
- Contrôles finaux : durée, résolution, fps, volume (environ -14 LUFS pour une vidéo sans voix, -16 avec voix), aucune image noire, aucune police de secours, aucun élément coupé au bord.
