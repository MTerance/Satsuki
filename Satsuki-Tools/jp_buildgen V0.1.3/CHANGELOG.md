# JP Building Generator - CHANGELOG

## Version 0.1.4 (Octobre 2025)

### 🔧 Corrections majeures
- ✅ **RÉSOLU** : Problème de flottement des bâtiments
  - Modification de `_add_cube()` pour origine au bottom center
  - Recalcul de toutes les positions Z
  - Ancrage parfait de tous les éléments

- ✅ **RÉSOLU** : Erreur de packaging ZIP
  - Structure ZIP corrigée : `jp_buildgen/[fichiers]`
  - Installation Blender sans erreur

### 🏗️ Améliorations techniques
- 🆕 **Sol transformé** : Cube épais → Plan de référence à Z=0.0
- 🆕 **Fonction `_add_plane()`** : Création de plans pour le sol
- 🔧 **Calcul équipements toiture** : Corrigé pour bottom center
- 🔧 **Modules Mall** : Repositionnés sur toit du podium
- 🔧 **Toits en pente** : Position du faîte ajustée

### 📦 Système de packaging
- ✅ **`package_simple.bat`** : Script fiable avec structure correcte
- ✅ **`package_addon.bat`** : Interface complète
- 📝 **Documentation** : Guides complets de packaging et utilisation

### 🎯 Nouveautés
- **Référence absolue** : Sol à Z=0 comme base géométrique parfaite
- **Ancrage précis** : Tous les bâtiments parfaitement posés
- **Performance** : Sol en plan plus léger qu'un cube
- **Simplicité** : Calculs de position simplifiés

---

## Version 0.1.3 (Développement)

### 🚀 Fonctionnalités initiales
- **6 types de bâtiments** : Office, Mall, Restaurant, Konbini, Apartment, House
- **30 textures incluses** : 6 catégories × 5 types (concrete, glass, roof, ground, signage)
- **Génération procédurale** : Seed, dimensions, étages configurables
- **Système de matériaux** : Projection automatique, fallback procédural
- **Interface intuitive** : Panneau dédié dans View3D > Sidebar > JPBuild

### 🏗️ Architecture technique
- **Système modulaire** : properties, operators, panels, core
- **Gestion des textures** : Cache d'images, mapping Box
- **Éléments décoratifs** : Balcons, enseignes, équipements toiture
- **Parcelle complète** : Sol, trottoir, marges configurables

---

## Installation

### Prérequis
- **Blender** : Version 4.5.0 ou supérieure
- **Python** : Version intégrée dans Blender

### Procédure
1. Télécharger `jp_buildgen_v0.1.4.zip`
2. Ouvrir Blender > Edit > Preferences > Add-ons
3. Cliquer "Install..." et sélectionner le ZIP
4. Activer "JP Building Generator"
5. Interface disponible : View3D > Sidebar > JPBuild

## Support

### Compatibilité testée
- ✅ **Windows** : PowerShell, Command Prompt
- ✅ **Blender** : 4.5.0+
- 🔄 **macOS/Linux** : Compatible (non testé)

### Documentation
- `README.md` : Guide d'utilisation
- `GUIDE_PACKAGING.md` : Scripts de packaging
- `RÉSUMÉ_FINAL_COMPLET.md` : Documentation technique complète

---

**Version actuelle : 0.1.4 - PRODUCTION READY** ✅