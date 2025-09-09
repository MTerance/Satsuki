# 🔧 GUIDE DÉPANNAGE TOKYO CITY GENERATOR v1.6.0

## 🚨 PROBLÈME: "addon_utils.disable: tokyo_city_generator not loaded"

### ✅ SOLUTION COMPLÈTE

#### ÉTAPE 1: DÉSINSTALLATION PROPRE
```
1. Blender > Edit > Preferences > Add-ons
2. Chercher "tokyo" ou "city"
3. Si trouvé: Cliquer sur ▼ puis "Remove"
4. Redémarrer Blender complètement
```

#### ÉTAPE 2: INSTALLATION NOUVELLE VERSION
```
1. Installer depuis: tokyo_addon_v1_6_0_FIXED.zip
2. ✅ Activer l'addon "Tokyo City Generator 1.6.0"
3. Vérifier que l'onglet "Tokyo" apparaît dans le sidebar (N)
```

#### ÉTAPE 3: TEST DE CHARGEMENT
Copier dans la console Blender pour diagnostic :

```python
import bpy
import sys

# Vérifier addon
addons = [addon.module for addon in bpy.context.preferences.addons]
tokyo_addons = [a for a in addons if 'tokyo' in a.lower()]
print(f"Addons Tokyo: {tokyo_addons}")

# Vérifier modules
tokyo_modules = [name for name in sys.modules.keys() if 'tokyo' in name.lower()]
print(f"Modules Tokyo: {tokyo_modules}")

# Test import
try:
    import tokyo_city_generator
    print("✅ Import OK")
    print(f"Texture system: {hasattr(tokyo_city_generator, 'tokyo_texture_system')}")
except Exception as e:
    print(f"❌ Erreur: {e}")
```

### 🔍 DIAGNOSTICS POSSIBLES

#### Si l'addon ne s'active pas:
1. **Vérifier la version Blender**: Nécessite Blender 4.0+
2. **Vérifier les droits**: Installer en tant qu'administrateur
3. **Nettoyer le cache**: Supprimer le dossier `__pycache__` dans les addons

#### Si l'onglet Tokyo n'apparaît pas:
1. Appuyer **N** pour ouvrir le sidebar
2. Chercher l'onglet "Tokyo" en bas
3. Si absent: Redémarrer Blender

#### Si "Texture system not available":
1. Vérifier que `texture_system.py` est dans le ZIP
2. Réinstaller l'addon complet
3. Redémarrer Blender

### 📁 STRUCTURE REQUISE

L'addon doit contenir ces fichiers:
```
tokyo_city_generator/
├── __init__.py         (Fichier principal)
├── texture_system.py   (Système de textures)
└── operators.py        (Si présent)
```

### 🎯 VERSIONS

- **v1.6.0 FIXED**: Version corrigée du système multi-étages
- **Fichier**: `tokyo_addon_v1_6_0_FIXED.zip` (91,648 bytes)
- **Nouveautés**: Textures 4 étages par fichier avec répétition automatique

### 🆘 SI RIEN NE FONCTIONNE

**Option 1: Réinstallation complète**
```
1. Fermer Blender
2. Supprimer manuellement le dossier addon dans:
   %APPDATA%\Blender Foundation\Blender\4.x\scripts\addons\
3. Redémarrer Blender
4. Réinstaller tokyo_addon_v1_6_0_FIXED.zip
```

**Option 2: Installation manuelle**
```
1. Extraire le ZIP
2. Copier le dossier dans:
   %APPDATA%\Blender Foundation\Blender\4.x\scripts\addons\
3. Redémarrer Blender
4. Activer dans Preferences > Add-ons
```

### 📞 SUPPORT

Si le problème persiste:
1. Copier les messages d'erreur de la console Blender
2. Vérifier la version exacte de Blender
3. Tester avec un nouveau fichier Blender vide

**Dernière mise à jour: 9 septembre 2025**
