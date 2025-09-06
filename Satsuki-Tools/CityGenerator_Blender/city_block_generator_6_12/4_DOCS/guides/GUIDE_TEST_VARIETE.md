# GUIDE DE TEST - CITY BLOCK GENERATOR 6.12.6 AVEC VARIÉTÉ DE BÂTIMENTS

## 🎯 NOUVELLES FONCTIONNALITÉS À TESTER

### 1. RECHARGEMENT FORCÉ DE L'ADDON
```
Dans Blender > Text Editor > Coller le contenu de reload_variety.py > Exécuter
```

### 2. TESTS DES NOUVELLES PROPRIÉTÉS

#### A) Bâtiments multiples par bloc
- **Propriété**: "Bâtiments par bloc" (1-9)
- **Test 1**: Mettre 1 → un bâtiment par bloc (ancien comportement)
- **Test 2**: Mettre 2-3 → subdivision intelligente des blocs
- **Test 3**: Mettre 4+ → petits bâtiments densément packés
- **Résultat attendu**: Blocs subdivisés avec espacement intelligent

#### B) Routes collées (sans espaces)
- **Propriété**: "Routes collées" (checkbox)
- **Test 1**: Décoché → routes avec trottoirs (ancien comportement)
- **Test 2**: Coché → routes directement collées aux bâtiments
- **Résultat attendu**: Plus d'espaces entre routes et blocs quand coché

#### C) Variété des formes de bâtiments
- **Propriété**: "Variété des bâtiments" (dropdown)
- **Test LOW**: Principalement rectangulaires simples
- **Test MEDIUM**: Mix équilibré de formes
- **Test HIGH**: Maximum de variété (L, U, T, Croix, Tours)
- **Test MODERN**: Tours et gratte-ciels dominants
- **Test CREATIVE**: Formes artistiques et complexes
- **Résultat attendu**: Formes visiblement différentes selon le niveau

#### D) Variation des hauteurs
- **Propriété**: "Variation hauteur" (0.0-1.0)
- **Test 0.0**: Hauteurs uniformes
- **Test 0.5**: Variation modérée
- **Test 1.0**: Hauteurs très variées
- **Résultat attendu**: Skyline plus ou moins varié

### 3. TESTS DE COMBINAISONS

#### Configuration Recommandée pour Test Complet
```
Largeur: 4
Longueur: 4
Étages max: 12
Largeur routes: 4.0
Bâtiments par bloc: 3
Routes collées: ✓ Coché
Variété: HIGH
Variation hauteur: 0.8
```

#### Test de Performance
```
Grille 6x6 avec 5 bâtiments par bloc
→ Devrait générer 180 bâtiments variés rapidement
```

### 4. VÉRIFICATIONS VISUELLES

#### À Observer dans la Vue 3D:
1. **Formes variées**: L, U, T, Croix, Tours selon la variété choisie
2. **Hauteurs différentes**: Skyline non-uniforme avec variation > 0
3. **Blocs subdivisés**: Plusieurs bâtiments par bloc bien espacés
4. **Routes collées**: Pas d'espace entre routes et bâtiments si coché
5. **Disposition intelligente**: Pas de chevauchements, espacement logique

#### Problèmes Potentiels:
- Bâtiments qui se chevauchent → Problème de subdivision
- Routes avec espaces malgré "collées" → Problème de sidewalk_width
- Toutes les formes identiques → Problème de variety selection
- Hauteurs uniformes → Problème de height_variation

### 5. TESTS SPÉCIALISÉS

#### Test Variété LOW vs HIGH
```
1. Générer avec LOW → Noter les formes obtenues
2. Supprimer la génération
3. Générer avec HIGH → Comparer les formes
4. Résultat: HIGH doit avoir beaucoup plus de variété
```

#### Test Bâtiments Multiples
```
1. Générer avec 1 bâtiment par bloc
2. Supprimer, générer avec 4 bâtiments par bloc
3. Résultat: Blocs subdivisés en 4 sections avec un bâtiment chacune
```

#### Test Routes Collées
```
1. Générer avec routes collées décoché
2. Mesurer distance route-bâtiment
3. Regenerer avec routes collées coché
4. Résultat: Distance doit être réduite à zéro
```

## 🎯 SUCCÈS ATTENDU
- Interface enrichie avec 4 nouvelles options
- Génération de villes beaucoup plus variées et réalistes
- Performance maintenue même avec complexité accrue
- Contrôle fin de l'apparence urbaine

## 🚨 SI PROBLÈMES
1. Exécuter reload_variety.py dans Blender
2. Vérifier que toutes les propriétés sont visibles dans l'UI
3. Tester d'abord avec grille 2x2 pour déboguer
4. Vérifier la console Blender pour erreurs Python

Version: 6.12.6 - Système de variété intelligent avec sélection pondérée
