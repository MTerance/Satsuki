# 🔧 GUIDE DE RÉSOLUTION : Propriétés manquantes

## 🎯 Problème identifié
Les erreurs "property not found: CityGenProperties.xxxx" indiquent que les propriétés ne sont pas correctement enregistrées ou accessibles.

## ✅ Corrections appliquées

### 1. Ordre d'enregistrement corrigé
**Problème** : `CityGenProperties` était enregistré en dernier  
**Solution** : Déplacé en premier dans la liste des classes

```python
# AVANT
classes = [CITYGEN_OT_Generate, ..., CityGenProperties]

# APRÈS  
classes = [CityGenProperties, CITYGEN_OT_Generate, ...]
```

### 2. Validation améliorée dans ResetProperties
**Ajout** : Vérification de l'existence de `CityGenProperties` avant utilisation

## 🚀 PROCÉDURE DE RÉSOLUTION

### Étape 1 : Réinstallation complète
1. **Désinstaller** l'ancienne version
2. **Redémarrer Blender** 
3. **Installer** `city_block_generator.zip` (nouvelle version)
4. **Activer** l'addon

### Étape 2 : Test diagnostic
Copier dans la console Blender (`test_ordre_enregistrement.py`) :
```python
import bpy
if hasattr(bpy.types, 'CityGenProperties'):
    print("✅ CityGenProperties trouvé")
else:
    print("❌ CityGenProperties manquant - Redémarrer Blender")
```

### Étape 3 : Correction manuelle (si nécessaire)
Copier dans la console Blender (`correction_proprietes_blender.py`) :
```python
# Force la recréation des propriétés
if hasattr(bpy.types.Scene, 'citygen_props'):
    del bpy.types.Scene.citygen_props
bpy.types.Scene.citygen_props = bpy.props.PointerProperty(type=bpy.types.CityGenProperties)
```

### Étape 4 : Utilisation du bouton intégré
1. **Ouvrir** le panneau CityGen (touche N → onglet CityGen)
2. **Cliquer** sur "Réinitialiser Paramètres"
3. **Vérifier** que les propriétés apparaissent

## 🧪 Scripts de diagnostic fournis

### 1. `test_ordre_enregistrement.py`
- **Usage** : Diagnostic complet de l'ordre d'enregistrement
- **Vérifie** : Classes, propriétés, accessibilité
- **Recommandations** : Solutions spécifiques

### 2. `correction_proprietes_blender.py` 
- **Usage** : Correction manuelle des propriétés
- **Actions** : Suppression et recréation forcée
- **Test** : Vérification de l'accessibilité

## 📋 Vérification finale

Après correction, vous devriez avoir :
- ✅ Pas d'erreur "property not found" dans la console
- ✅ Panneau CityGen avec tous les paramètres
- ✅ Valeurs par défaut visibles :
  - Largeur: 5
  - Longueur: 5  
  - Étages max: 8
  - etc.

## 🚨 Si le problème persiste

### Solution 1 : Rechargement complet
```python
# Dans la console Blender
import addon_utils
addon_utils.disable("city_block_generator")
addon_utils.enable("city_block_generator", default_set=True)
```

### Solution 2 : Réinitialisation Blender
1. **Sauvegarder** votre projet
2. **Fermer Blender**
3. **Supprimer** le cache des addons :
   `%APPDATA%\Blender Foundation\Blender\4.x\scripts\addons\__pycache__`
4. **Relancer Blender**
5. **Réinstaller** l'addon

### Solution 3 : Mode sans échec
1. **Lancer Blender** avec `--factory-startup`
2. **Installer** l'addon dans cet environnement propre
3. **Tester** si les propriétés fonctionnent

## 💡 Prévention

Pour éviter ce problème à l'avenir :
1. **Toujours** redémarrer Blender après désinstallation
2. **Ne pas** modifier l'addon pendant qu'il est activé
3. **Utiliser** "Rechargement Rapide" pour les modifications de développement

---

**Version corrigée** : 6.21.1 (Ordre d'enregistrement fixé)  
**Date** : 09/04/2025  
**Statut** : ✅ **PROPRIÉTÉS CORRIGÉES**
