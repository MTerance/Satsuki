# GUIDE RÉSOLUTION ERREURS TOKYO v1.3.0

## 🚨 PROBLÈME: Version 1.0.8 encore visible dans Blender

### ✅ SOLUTION APPLIQUÉE
La version 1.3.0 a été forcée avec succès! L'installation a réussi.

---

## 🔧 ÉTAPES À SUIVRE MAINTENANT

### 1. 🔄 REDÉMARRAGE COMPLET DE BLENDER
```
⚠️ IMPORTANT: FERMEZ Blender COMPLÈTEMENT
🚀 Redémarrez Blender (nouveau processus)
```

### 2. 🧹 NETTOYAGE ADDON DANS BLENDER
1. `Edit > Preferences > Add-ons`
2. Cherchez `Tokyo` dans la barre de recherche
3. **SI vous voyez l'ancienne version 1.0.8:**
   - ❌ DÉSACTIVEZ l'addon (décochez)
   - 🗑️ Cliquez sur `Remove` pour supprimer
   - 🔄 Cliquez sur `Refresh` pour actualiser la liste

### 3. ✅ ACTIVATION NOUVELLE VERSION
1. Dans `Add-ons`, cherchez `Tokyo City Generator`
2. Vous devriez voir: `Tokyo City Generator 1.3.0 TEXTURE SYSTEM`
3. ✅ ACTIVEZ cet addon (cochez la case)
4. 💾 Sauvegardez les préférences si demandé

### 4. 🎯 VÉRIFICATION INTERFACE
1. Ouvrez la `Vue 3D`
2. Appuyez sur `N` pour ouvrir la sidebar
3. Cherchez l'onglet `Tokyo`
4. Vous devriez voir **l'option "Advanced Textures"** (NOUVEAU!)

---

## 🔍 DIAGNOSTIC DES ERREURS

### Si vous avez encore des erreurs:

#### A. 📋 COPIEZ LE SCRIPT DE DIAGNOSTIC
```python
# Copiez le contenu du fichier: diagnostic_errors_blender.py
# Et exécutez-le dans Blender (Scripting workspace)
```

#### B. 🖥️ OUVREZ LA CONSOLE BLENDER
```
Windows > Toggle System Console
```
Les erreurs s'afficheront ici en détail.

#### C. 🧪 TEST SIMPLE
1. Créez un nouveau projet Blender
2. Supprimez le cube par défaut
3. Allez dans l'onglet `Tokyo` (sidebar N)
4. **Grid Size**: 2
5. **Block Size**: 20
6. ✅ Cochez `Advanced Textures` (NOUVEAU!)
7. Cliquez sur `Generate Tokyo City`

---

## 🎨 NOUVEAU SYSTÈME DE TEXTURES

### Configuration automatique des dossiers:
```
📁 C:\Users\sshom\Documents\assets\Tools\tokyo_textures\
├── 📂 skyscrapers/        # Gratte-ciels (>15 étages)
├── 📂 commercial/         # Commercial (8-15 étages)
├── 📂 midrise/           # Moyenne hauteur (4-8 étages)
├── 📂 residential/       # Résidentiel (2-4 étages)
└── 📂 lowrise/          # Petits bâtiments (1-2 étages)
```

### Chaque catégorie a 4 sous-dossiers:
- `facade/` - Textures de façade
- `roof/` - Textures de toit  
- `details/` - Détails architecturaux
- `materials/` - Matériaux spéciaux

---

## ❌ ERREURS COMMUNES ET SOLUTIONS

### Erreur: "Module not found"
**Solution**: Redémarrez Blender complètement

### Erreur: "Operator not found"
**Solution**: 
1. Désactivez l'addon
2. Réactivez l'addon
3. Redémarrez Blender

### Erreur: "Properties not found"
**Solution**: L'addon n'est pas correctement enregistré
1. Vérifiez que la version 1.3.0 est active
2. Pas de conflit avec d'autres addons

### Interface Tokyo non visible
**Solution**:
1. Vue 3D > Sidebar (N)
2. Scroll dans les onglets pour trouver "Tokyo"
3. Si pas là: addon pas activé correctement

---

## 🚀 VERSION 1.3.0 - NOUVELLES FONCTIONNALITÉS

### ✨ Système de Textures Intelligent
- Sélection automatique basée sur la hauteur du bâtiment
- 5 catégories de bâtiments avec textures appropriées
- Matériaux avancés avec normal maps

### 🎛️ Nouveaux Contrôles
- `Advanced Textures` - Active le système intelligent
- `Texture Base Path` - Chemin vers vos textures
- Paramètres de densité améliorés

### 📊 Optimisations
- Génération plus rapide
- Moins d'utilisation mémoire
- Meilleure stabilité

---

## 📞 SI LE PROBLÈME PERSISTE

### 🔍 Collectez ces informations:
1. Version de Blender exacte
2. Message d'erreur complet (depuis la console)
3. Résultat du script de diagnostic
4. Système d'exploitation

### 🧪 Test de derniers recours:
```python
# Dans la console Python de Blender:
import sys
print("Python paths:")
for path in sys.path:
    print(f"  {path}")

import bpy
print(f"Blender version: {bpy.app.version}")
print(f"Addons directory: {bpy.utils.user_resource('SCRIPTS', 'addons')}")
```

---

## ✅ RÉSULTAT ATTENDU

Après avoir suivi ces étapes, vous devriez avoir:
- ✅ Tokyo City Generator 1.3.0 actif
- ✅ Onglet "Tokyo" visible dans la sidebar
- ✅ Option "Advanced Textures" disponible
- ✅ Génération de villes avec textures intelligentes
- ✅ Aucune erreur dans la console

🎉 **La version 1.3.0 avec système de textures est prête!**
