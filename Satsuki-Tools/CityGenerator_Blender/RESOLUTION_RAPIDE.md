# 🚀 City Block Generator - Guide de Résolution Rapide

## ❌ Problème: "Le menu ne s'affiche plus et l'addon n'est pas pris en compte par Blender"

### 🎯 Solutions Rapides (dans l'ordre)

#### 1️⃣ Vérification de Base (30 secondes)
```
✅ Dans Blender: Edit > Preferences > Add-ons
✅ Recherchez "City Block Generator" 
✅ Vérifiez que la case est cochée ✅
✅ Appuyez sur N dans la vue 3D pour ouvrir la sidebar
✅ Cherchez l'onglet "CityGen"
```

#### 2️⃣ Réinstallation Propre (2 minutes)
```
1. Edit > Preferences > Add-ons
2. Trouvez "City Block Generator"
3. Cliquez la flèche pour déplier
4. Cliquez "Remove" 
5. Fermez Blender COMPLÈTEMENT
6. Rouvrez Blender
7. Edit > Preferences > Add-ons > Install
8. Sélectionnez city_block_generator_6_12.zip
9. Activez l'addon (case cochée)
10. Appuyez N dans la vue 3D > Onglet CityGen
```

#### 3️⃣ Diagnostic Intégré (si l'addon se charge partiellement)
Si vous voyez un panneau avec erreurs:
```
1. Cliquez le bouton "Diagnostic" 
2. Regardez la console (Window > Toggle System Console)
3. Cliquez "Réinitialiser Paramètres"
4. Si ça ne marche pas: fermez Blender et recommencez
```

#### 4️⃣ Nettoyage Cache (si problème persiste)
```
Windows:
1. Fermez Blender
2. Allez dans: %APPDATA%\Blender Foundation\Blender\4.x\scripts\addons\
3. Supprimez le dossier "city_block_generator_6_12" (s'il existe)
4. Rouvrez Blender
5. Réinstallez le ZIP

Mac:
~/Library/Application Support/Blender/4.x/scripts/addons/

Linux:
~/.config/blender/4.x/scripts/addons/
```

### 🆘 Si Rien ne Fonctionne

1. **Testez dans un NOUVEAU fichier Blender:**
   - File > New > General
   - Supprimez le cube (X)
   - N pour la sidebar > CityGen

2. **Vérifiez votre version Blender:**
   - Help > About
   - Nécessite Blender 4.0+

3. **Console Python (pour debug):**
   ```python
   import bpy
   print(dir(bpy.types))  # Cherchez CITYGEN dans la liste
   ```

### 🎉 Test de Fonctionnement

Une fois l'addon activé:
```
1. Nouveau fichier Blender
2. Supprimez le cube par défaut
3. Sidebar (N) > Onglet CityGen
4. Largeur = 3, Longueur = 3
5. Cliquez "Générer Quartier"
6. ✅ Vous devez voir des bâtiments verts et routes roses!
```

### 📋 Informations Support

- **Version Addon**: 6.20.6 (avec diagnostic intégré)
- **Blender Requis**: 4.0+
- **Emplacement**: View3D > Sidebar > CityGen Tab

---

### 🔧 Améliorations Version 6.20.6

- ✅ Import cyclique supprimé
- ✅ Gestion d'erreur renforcée  
- ✅ Interface de secours améliorée
- ✅ Bouton diagnostic intégré
- ✅ Réinitialisation forcée des propriétés
- ✅ Messages d'erreur plus clairs
- ✅ Compatibilité Blender 4.x optimisée

**Si cette version ne fonctionne toujours pas, le problème vient probablement de votre installation Blender ou d'un conflit avec un autre addon.** 

Essayez avec une installation Blender propre pour confirmer.
