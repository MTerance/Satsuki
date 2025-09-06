# Guide de Dépannage - City Block Generator

## Problème : Le panneau ne s'affiche plus dans Blender

### ✅ Vérifications Rapides

1. **Addon activé ?**
   - Allez dans `Edit > Preferences > Add-ons`
   - Recherchez "City Block Generator"
   - Vérifiez que la case est cochée ✅

2. **Sidebar ouverte ?**
   - Dans la vue 3D, appuyez sur `N` pour ouvrir/fermer la sidebar
   - Cherchez l'onglet "CityGen" dans la sidebar

3. **Bon espace de travail ?**
   - Assurez-vous d'être dans un espace de travail 3D (Modeling, Layout, etc.)
   - Le panneau n'apparaît que dans la vue 3D

### 🔧 Solutions Étape par Étape

#### Solution 1: Réinstallation Propre
```
1. Edit > Preferences > Add-ons
2. Recherchez "City Block Generator"
3. Cliquez sur la flèche à côté du nom
4. Cliquez "Remove" (si présent)
5. Redémarrez Blender
6. Réinstallez le ZIP
7. Activez l'addon
```

#### Solution 2: Vérification Console
```
1. Window > Toggle System Console (Windows)
2. Réactivez l'addon
3. Recherchez les messages d'erreur en rouge
4. Si erreurs: notez-les et suivez Solution 3
```

#### Solution 3: Réinitialisation Force
```
1. Désactivez l'addon
2. Fermez Blender complètement
3. Supprimez le cache:
   - Windows: %APPDATA%\Blender Foundation\Blender\4.x\scripts\addons\
   - Supprimez le dossier city_block_generator_6_12 s'il existe
4. Redémarrez Blender
5. Réinstallez depuis le ZIP
```

#### Solution 4: Mode Debug
```
1. Dans Blender, allez dans Edit > Preferences
2. Interface > Developer Extras: ✅ Activé
3. Redémarrez Blender
4. Réactivez l'addon
5. Vérifiez la console pour plus de détails
```

### 🐛 Messages d'Erreur Courants

#### "Module not found"
- **Cause**: Installation incomplète
- **Solution**: Réinstallation propre (Solution 1)

#### "PropertyGroup not registered"  
- **Cause**: Ordre d'enregistrement incorrect
- **Solution**: Redémarrage Blender + réactivation

#### "Panel not visible"
- **Cause**: Cache Blender corrompu
- **Solution**: Nettoyage cache (Solution 3)

### 🎯 Vérification Post-Installation

Après activation réussie, vous devriez voir:
```
✅ Onglet "CityGen" dans la sidebar (N)
✅ Panneau "City Block Generator" 
✅ Paramètres modifiables (largeur, longueur, etc.)
✅ Bouton "Générer Quartier"
```

### 🆘 Debugging Avancé

Si le problème persiste:

1. **Test dans un nouveau fichier Blender**
   ```
   File > New > General
   N (ouvrir sidebar)
   Vérifier onglet CityGen
   ```

2. **Console Python**
   ```
   Window > Toggle System Console
   Taper dans la console Python:
   >>> import bpy
   >>> bpy.context.scene.citygen_props
   ```

3. **Force reload**
   ```
   Dans la console Python:
   >>> import importlib
   >>> import sys
   >>> if 'city_block_generator_6_12' in sys.modules:
   ...     importlib.reload(sys.modules['city_block_generator_6_12'])
   ```

### 📋 Informations de Support

**Version Addon**: 6.20.5
**Blender Compatible**: 4.0+
**Emplacement**: View3D > Sidebar > CityGen Tab

Si aucune solution ne fonctionne:
1. Notez votre version de Blender (Help > About)
2. Notez votre OS (Windows/Mac/Linux)
3. Joignez les messages de la console
4. Décrivez étape par étape ce que vous avez essayé

### 🚀 Test Final

Pour vérifier que l'addon fonctionne:
```
1. Ouvrez un nouveau fichier Blender
2. Supprimez le cube par défaut (X > Delete)
3. Sidebar (N) > Onglet CityGen
4. Paramètres: Largeur=3, Longueur=3
5. Cliquez "Générer Quartier"
6. Vous devriez voir apparaître des bâtiments verts et des routes roses
```

Si cette séquence fonctionne, l'addon est correctement installé ! 🎉
