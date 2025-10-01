# Correction du problème de flottement des bâtiments

## Problème identifié
Les bâtiments générés par jp_buildgen flottaient au-dessus du sol au lieu d'être correctement posés sur la parcelle.

## Cause du problème
Le sol de la parcelle avait une épaisseur de `0.02` unités (définie dans `_make_parcel`), mais tous les bâtiments étaient positionnés à partir de `z=0` au lieu de `z=0.02`, ce qui créait un gap visible entre le sol et la base des bâtiments.

## Solution implémentée

### 1. Constante globale
Ajout de `GROUND_LEVEL = 0.02` pour centraliser la valeur de l'épaisseur du sol.

### 2. Corrections par type de bâtiment

#### Office
- **Avant** : `(0,0,podium_h/2)` 
- **Après** : `(0,0,GROUND_LEVEL + podium_h/2)`

#### Mall  
- **Avant** : `(0,0,podium_h/2)`
- **Après** : `(0,0,GROUND_LEVEL + podium_h/2)`

#### Restaurant
- **Avant** : `(0,0,total_h/2)`
- **Après** : `(0,0,GROUND_LEVEL + total_h/2)`

#### Konbini
- **Avant** : `(0,0,total_h/2)`
- **Après** : `(0,0,GROUND_LEVEL + total_h/2)`

#### Apartment
- **Avant** : `(0,0,total_h/2)`
- **Après** : `(0,0,GROUND_LEVEL + total_h/2)`
- **Balcons** : `z = GROUND_LEVEL + f*fh - fh*0.35`

#### House
- **Avant** : `(0,0,h/2)`
- **Après** : `(0,0,GROUND_LEVEL + h/2)`
- **Toit** : `ridge_z = GROUND_LEVEL + h + 0.8`

### 3. Éléments décoratifs corrigés
- **Enseignes** : Positionnement relatif au `GROUND_LEVEL`
- **Auvents** : Position relative au sol
- **Équipements de toiture** : Calcul automatique correct grâce au repositionnement des bâtiments

## Résultat attendu
- Tous les bâtiments sont maintenant correctement posés sur le sol de la parcelle
- Aucun gap visible entre le sol et la base des bâtiments
- Les proportions et l'alignement des éléments sont préservés
- Les équipements de toiture suivent automatiquement la nouvelle hauteur des bâtiments

## Test recommandé
1. Générer chaque type de bâtiment (Office, Mall, Restaurant, Konbini, Apartment, House)
2. Vérifier visuellement que la base du bâtiment touche bien le sol
3. Confirmer que les enseignes et éléments décoratifs sont correctement positionnés
4. Valider que les équipements de toiture apparaissent au bon niveau