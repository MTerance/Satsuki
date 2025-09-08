# GUIDE COMPLET - SYSTÈME DE TEXTURES TOKYO v1.3.0

## 🎨 COMMENT ACCÉDER AU SYSTÈME DE TEXTURES

### 🚀 ÉTAPE 1: Vérifier que l'addon v1.3.0 est actif

1. **⚙️ Edit > Preferences > Add-ons**
2. **🔍 Cherchez "Tokyo City Generator"**
3. **✅ Vérifiez que vous voyez "1.3.0 TEXTURE SYSTEM"**
4. **✅ L'addon doit être coché (activé)**

### 🎯 ÉTAPE 2: Accéder à l'interface

1. **📐 Ouvrez la Vue 3D** (3D Viewport)
2. **📋 Appuyez sur `N`** pour ouvrir la sidebar
3. **🔍 Cherchez l'onglet "Tokyo"** dans la sidebar
4. **🎛️ Cliquez sur l'onglet "Tokyo"**

### 🎨 ÉTAPE 3: Activer le système de textures

Dans le panneau Tokyo, vous verrez:

```
┌─────────────────────────────────┐
│ Tokyo City Generator            │
├─────────────────────────────────┤
│ Grid Size: [3]                  │
│ Block Size: [25.0]              │
│ Building Density: [0.8]         │
│                                 │
│ ✅ Advanced Textures            │ ← NOUVEAU!
│ Texture Base Path: [Browse...]  │ ← NOUVEAU!
│                                 │
│ [Generate Tokyo City]           │
└─────────────────────────────────┘
```

### ⚙️ ÉTAPE 4: Configuration du système

#### A. Activer les textures avancées
- **✅ Cochez "Advanced Textures"**
- Cette option active le système intelligent

#### B. Configurer le chemin des textures
- **📁 Cliquez sur "Texture Base Path"**
- **🎯 Sélectionnez:** `C:\Users\sshom\Documents\assets\Tools\tokyo_textures`
- **💡 OU** n'importe quel dossier contenant vos textures

---

## 📁 STRUCTURE DES DOSSIERS DE TEXTURES

Le système recherche cette hiérarchie:

```
📁 tokyo_textures/
├── 📂 skyscrapers/          # Gratte-ciels (>15 étages)
│   ├── 📂 facade/
│   ├── 📂 roof/
│   ├── 📂 details/
│   └── 📂 materials/
├── 📂 commercial/           # Commercial (8-15 étages)
│   ├── 📂 facade/
│   ├── 📂 roof/
│   ├── 📂 details/
│   └── 📂 materials/
├── 📂 midrise/             # Moyenne hauteur (4-8 étages)
│   ├── 📂 facade/
│   ├── 📂 roof/
│   ├── 📂 details/
│   └── 📂 materials/
├── 📂 residential/         # Résidentiel (2-4 étages)
│   ├── 📂 facade/
│   ├── 📂 roof/
│   ├── 📂 details/
│   └── 📂 materials/
└── 📂 lowrise/            # Petits bâtiments (1-2 étages)
    ├── 📂 facade/
    ├── 📂 roof/
    ├── 📂 details/
    └── 📂 materials/
```

---

## 🎮 UTILISATION PRATIQUE

### 🏗️ Génération avec textures automatiques

1. **🧹 Supprimez le cube par défaut** (sélectionnez + Delete)
2. **🎛️ Dans le panneau Tokyo:**
   - **Grid Size:** 3 (pour une ville 3x3)
   - **Block Size:** 25.0 (taille des blocs)
   - **✅ Advanced Textures:** COCHÉ
   - **📁 Texture Base Path:** Votre dossier de textures
3. **🚀 Cliquez "Generate Tokyo City"**

### 🎨 Résultat magique

Le système va automatiquement:
- 📏 **Analyser chaque bâtiment** (hauteur/largeur)
- 🏢 **Catégoriser:** Gratte-ciel, commercial, résidentiel, etc.
- 🎲 **Sélectionner au hasard** une texture appropriée
- 🎭 **Appliquer le matériau** avec toutes les propriétés

### 📊 Intelligence du système

```
🏢 Gratte-ciel (>15 étages)    → textures métalliques, verre
🏬 Commercial (8-15 étages)    → textures modernes, enseignes
🏘️ Moyenne hauteur (4-8)       → textures urbaines standards
🏠 Résidentiel (2-4 étages)    → textures chaleureuses, briques
🏪 Petits bâtiments (1-2)      → textures locales, boutiques
```

---

## 🛠️ CONFIGURATION AVANCÉE

### 📁 Créer automatiquement la structure de dossiers

Exécutez ce script pour créer tous les dossiers:

```python
# Dans Blender, Scripting workspace:
import bpy
bpy.ops.mesh.tokyo_setup_textures()
```

### 🎨 Ajouter vos propres textures

1. **📂 Placez vos images** dans les bons dossiers:
   - **facade/:** `building_01.jpg`, `wall_concrete.png`
   - **roof/:** `roof_tiles.jpg`, `rooftop_metal.png`
   - **details/:** `windows.png`, `balcony.jpg`
   - **materials/:** `metal.jpg`, `glass.png`

2. **🔄 Formats supportés:** `.jpg`, `.png`, `.tga`, `.bmp`, `.tiff`

3. **📏 Résolutions recommandées:** 1024x1024 ou 2048x2048

### ⚙️ Paramètres du matériau automatique

Le système crée automatiquement:
- **🎨 Base Color:** Texture principale
- **🔧 Roughness:** Rugosité réaliste
- **💎 Metallic:** Selon le type de bâtiment
- **🗺️ Normal Map:** Si disponible
- **📐 UV Mapping:** Automatique et proportionnel

---

## 🔍 DÉPANNAGE

### ❌ "Advanced Textures" n'apparaît pas
**Solution:** L'addon n'est pas en version 1.3.0
- Vérifiez la version dans Add-ons
- Redémarrez Blender
- Utilisez le script de force refresh

### ❌ Pas de textures appliquées
**Solutions:**
1. **📁 Vérifiez le chemin:** Texture Base Path correct?
2. **📂 Vérifiez la structure:** Dossiers créés?
3. **🖼️ Vérifiez les images:** Fichiers présents?

### ❌ Textures incorrectes
**Solution:** Le système prend au hasard
- C'est normal! Relancez pour d'autres textures
- Ajoutez plus de variétés dans vos dossiers

### 🔍 Console de debug
Dans Blender, ouvrez `Window > Toggle System Console` pour voir:
```
🎨 Tokyo Texture System: Analyzing building...
📏 Building: height=45.2, width=12.8
🏢 Category: skyscrapers
🎲 Selected: glass_tower_03.jpg
✅ Material applied: TokyoMat_Skyscraper_001
```

---

## 🎉 ASTUCES AVANCÉES

### 🎲 Génération multiple
- Relancez plusieurs fois pour des variations
- Chaque génération = nouvelles textures aléatoires

### 🎨 Mix de styles
- Mélangez différents types de textures dans les dossiers
- Le système adaptera automatiquement

### 📊 Performances
- Plus de textures = plus de variété
- Résolutions élevées = plus beau mais plus lourd

### 🔄 Mise à jour en temps réel
- Modifiez le chemin → nouvelles textures appliquées
- Ajoutez des fichiers → plus de variété disponible

---

## ✅ RÉSUMÉ RAPIDE

1. **✅ Activez "Advanced Textures"**
2. **📁 Configurez "Texture Base Path"**
3. **🚀 Générez votre ville**
4. **🎉 Profitez des textures automatiques!**

Le système de textures v1.3.0 transforme vos villes génériques en métropoles réalistes avec un seul clic! 🌆
