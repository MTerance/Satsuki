# TOKYO CITY GENERATOR v1.6.0 - SYSTÈME MULTI-ÉTAGES
## Guide d'installation et test du nouveau système de textures

### 🆕 NOUVEAUTÉS v1.6.0

**SYSTÈME DE TEXTURES MULTI-ÉTAGES :**
- ✅ Chaque fichier texture contient 4 étages
- ✅ Répétition automatique selon la hauteur du bâtiment
- ✅ Calcul intelligent : hauteur ÷ 3m par étage ÷ 4 étages par texture
- ✅ Mapping UV optimisé pour façades réalistes
- ✅ Support tous types de bâtiments (residential, commercial, skyscrapers, etc.)

### 📦 INSTALLATION

1. **Désinstaller l'ancienne version :**
   - Blender > Edit > Preferences > Add-ons
   - Chercher "Tokyo City Generator"
   - Cliquer sur la flèche ▼ puis "Remove"

2. **Installer la nouvelle version :**
   - Install from disk > Sélectionner `tokyo_addon_v1_6_0_multi_floors.zip`
   - ✅ Activer l'addon "Tokyo City Generator"

3. **Configuration des textures :**
   - Aller dans le panneau Tokyo City Generator (sidebar N)
   - ✅ Cocher "Advanced Textures"
   - 📁 Définir le chemin : `C:\Users\sshom\Documents\assets\Tools\tokyo_textures`

### 🏗️ STRUCTURE DES TEXTURES

Vos textures doivent être organisées ainsi :
```
tokyo_textures/
├── residential/        # Maisons (< 20m)
├── commercial/         # Centres commerciaux (10-50m, large)
├── skyscrapers/        # Gratte-ciels (> 50m)
├── midrise/           # Immeubles moyens (20-50m, étroit)
└── lowrise/           # Petits bâtiments (< 10m)
```

**Format des fichiers texture :**
- 📏 Chaque fichier = **4 étages empilés verticalement**
- 🔄 Le système répète automatiquement selon la hauteur
- 📐 Exemple : bâtiment 24m = 8 étages = 2x répétitions de texture

### 🧪 TEST RAPIDE

1. **Générer une ville :**
   - Créer une grille 3x3
   - ✅ "Advanced Textures" activé
   - Générer

2. **Vérifier l'affichage :**
   - Passer en mode **Material Preview** (3ème sphère)
   - Ou appuyer **Z** puis **3**

3. **Résultats attendus :**
   - 🏢 Gratte-ciels : textures répétées 15x (≈60 étages)
   - 🏪 Commercial : textures répétées 2x (≈8 étages)
   - 🏠 Residential : textures répétées 1x (≈4 étages)

### 🔍 DIAGNOSTIC EN CAS DE PROBLÈME

Si les textures n'apparaissent pas, copier dans la console Blender :

```python
import bpy
import os

scene = bpy.context.scene
print(f"Chemin configuré: {scene.tokyo_texture_base_path}")

# Vérifier les dossiers
for cat in ['residential', 'commercial', 'skyscrapers']:
    path = os.path.join(scene.tokyo_texture_base_path, cat)
    if os.path.exists(path):
        files = os.listdir(path)
        images = [f for f in files if f.lower().endswith(('.png', '.jpg'))]
        print(f"{cat}: {len(images)} images trouvées")
    else:
        print(f"{cat}: DOSSIER MANQUANT")
```

### 🎯 FONCTIONNALITÉS AVANCÉES

**Calcul automatique des répétitions :**
- Bâtiment 12m = 4 étages = 1.0x répétition
- Bâtiment 24m = 8 étages = 2.0x répétition  
- Bâtiment 60m = 20 étages = 5.0x répétition

**Types de matériaux :**
- 🏢 Skyscrapers : Métallique brillant (Metallic: 0.8)
- 🏪 Commercial : Semi-brillant (Metallic: 0.3)
- 🏠 Residential : Mat (Metallic: 0.1)

### 📞 SUPPORT

Si vous rencontrez des problèmes :
1. Vérifiez que le mode d'affichage est en "Material"
2. Confirmez que vos textures sont bien organisées par dossier
3. Testez le diagnostic ci-dessus

**Version : 1.6.0 Multi-Floors**
**Date : 9 septembre 2025**
