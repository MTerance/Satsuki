# TOKYO SIMPLE v2.1 - RETOUR AUX SOURCES

**Date**: Décembre 2024  
**Version**: 2.1.0 SIMPLE  
**Statut**: BACK TO BASICS QUI MARCHENT !  

## 🎯 OBJECTIF

Retourner à un générateur **SIMPLE ET EFFICACE** après l'échec de complexité de la v2.0.

L'utilisateur a dit: *"c'est impossible à utiliser, le résultat n'est pas celui attendu... l'interface est un bordel sans nom"*

**SOLUTION**: Reprendre les bases qui marchaient (v1.6.0) avec une interface ultra-simple.

---

## ✨ PRINCIPE v2.1 SIMPLE

### Interface Ultra-Simple
- **4 paramètres SEULEMENT** (vs 20+ dans v2.0)
- **1 algorithme** efficace (Tokyo style)
- **1 bouton** principal "Generate Tokyo City"
- **Panneau unique** dans la sidebar

### Paramètres Essentiels
1. **City Size** (3-10) - Taille de la grille
2. **Building Style** (Low/Mixed/High) - Style architectural
3. **Density** (0.3-1.0) - Densité de construction
4. **Better Materials** (On/Off) - Matériaux améliorés

### Génération Intelligente
- **Routes d'abord** - Créées AVANT les bâtiments
- **Bâtiments après** - Placés dans les espaces libres
- **Pas de chevauchement** - Routes et bâtiments bien séparés
- **Variété automatique** - Hauteurs et couleurs variées

---

## 🏗️ ARCHITECTURE SIMPLE

```
TOKYO_SIMPLE_V2_1/
└── __init__.py (tout en un fichier - 350 lignes)
    ├── TokyoSimpleProperties (4 propriétés)
    ├── TOKYO_SIMPLE_OT_generate (générateur principal)
    ├── TOKYO_SIMPLE_OT_clear (nettoyage)
    └── TOKYO_SIMPLE_PT_panel (interface simple)
```

### Algorithme Principal
1. **Nettoyer** les objets Tokyo existants
2. **Créer réseau de routes** (horizontal + vertical)
3. **Générer bâtiments** dans les blocs libres
4. **Appliquer matériaux** selon la hauteur
5. **Finir** - Retour utilisateur simple

---

## 🎨 MATÉRIAUX INTELLIGENTS

### Selon la Hauteur
- **Maisons** (< 10m): Brun chaleureux, peu réfléchissant
- **Appartements** (10-20m): Beige résidentiel
- **Bureaux** (20-35m): Gris professionnel
- **Gratte-ciels** (> 35m): Bleu moderne + émission fenêtres

### Anti-Uniformité
- **Variation de couleur** automatique (±15%)
- **Hauteurs variées** selon le style choisi
- **Effet centre-ville** (plus haut au centre)

---

## 📦 INSTALLATION SIMPLE

```bash
# Créer le ZIP final
tokyo_simple_v2_1.zip
└── tokyo_simple_v2_1/
    └── __init__.py
```

Dans Blender:
1. Edit > Preferences > Add-ons
2. Install... > Sélectionner tokyo_simple_v2_1.zip
3. Activer "Tokyo City Generator v2.1 SIMPLE"
4. Aller dans View3D > Sidebar (N) > Onglet "Tokyo"

---

## 🎯 DIFFÉRENCES vs v2.0

| Aspect | v2.0 COMPLEX | v2.1 SIMPLE |
|--------|--------------|-------------|
| **Interface** | 3 panneaux, 20+ options | 1 panneau, 4 options |
| **Algorithmes** | 3 (Tokyo/Organic/Grid) | 1 (Tokyo optimisé) |
| **Fichiers** | 5 fichiers modulaires | 1 fichier tout-en-un |
| **Génération** | Complexe, bugs | Simple, fiable |
| **Installation** | Structure complexe | ZIP direct |
| **Utilisation** | "Bordel sans nom" | Intuitif et direct |

---

## ✅ TESTS DE VALIDATION

### Test 1: Interface
- [ ] Panneau visible dans sidebar "Tokyo"
- [ ] 4 paramètres clairement visibles
- [ ] Bouton "Generate" bien visible et utilisable

### Test 2: Génération
- [ ] Ville 5x5 générée en < 5 secondes
- [ ] Routes bien alignées et continues
- [ ] Bâtiments séparés des routes (pas de chevauchement)
- [ ] Hauteurs variées selon le style choisi

### Test 3: Matériaux
- [ ] Couleurs variées (pas tous identiques)
- [ ] Matériaux différents selon la hauteur
- [ ] Gratte-ciels avec effet fenêtres éclairées

### Test 4: Nettoyage
- [ ] Bouton "Clear City" supprime tous les objets Tokyo
- [ ] Nouvelle génération remplace l'ancienne

---

## 🚀 PROCHAINES ÉTAPES

1. **Créer le ZIP** tokyo_simple_v2_1.zip
2. **Installer dans Blender** et tester
3. **Valider interface** ultra-simple
4. **Confirmer génération** sans bugs
5. **Livrer** à l'utilisateur

**OBJECTIF**: Que l'utilisateur dise "Enfin quelque chose qui marche !" au lieu de "C'est un bordel".