# 🎨 TOKYO TEXTURE SYSTEM v1.2.0 - GUIDE COMPLET

## 🎯 RÉVOLUTION TEXTURES TOKYO

Le **Tokyo City Generator** dispose maintenant d'un **système de textures intelligent** qui sélectionne automatiquement des textures selon:
- ✅ **Hauteur** du bâtiment  
- ✅ **Largeur** du bâtiment
- ✅ **Type de zone** (business/commercial/résidentiel)

## 🏗️ CATÉGORIES AUTOMATIQUES

### 🏢 GRATTE-CIELS (Skyscrapers)
- **Conditions**: Hauteur > 50m
- **Dossiers**: `skyscrapers/glass_towers/`, `skyscrapers/modern_office/`, `skyscrapers/metallic_facades/`, `skyscrapers/corporate_buildings/`
- **Style**: Façades vitrées, métalliques, bureaux modernes
- **Mapping**: Texture étirée verticalement (Scale Y=0.1)

### 🏬 CENTRES COMMERCIAUX (Commercial)
- **Conditions**: Hauteur 10-50m + Largeur > 15m
- **Dossiers**: `commercial/shopping_centers/`, `commercial/retail_facades/`, `commercial/colorful_buildings/`, `commercial/modern_stores/`
- **Style**: Façades colorées, enseignes, vitrines
- **Mapping**: Texture normale (Scale 1:1:1)

### 🏘️ IMMEUBLES MOYENS (Midrise)
- **Conditions**: Hauteur 20-50m + Largeur ≤ 15m
- **Dossiers**: `midrise/apartment_blocks/`, `midrise/office_buildings/`, `midrise/mixed_use/`, `midrise/urban_housing/`
- **Style**: Appartements, bureaux moyens
- **Mapping**: Texture standard (Scale 1.5:1.5:1.5)

### 🏠 RÉSIDENTIEL (Residential)
- **Conditions**: Hauteur 3-20m
- **Dossiers**: `residential/japanese_houses/`, `residential/modern_homes/`, `residential/traditional_buildings/`, `residential/small_apartments/`
- **Style**: Maisons japonaises, habitations modernes
- **Mapping**: Texture détaillée (Scale 2:2:2)

### 🏪 PETITS BÂTIMENTS (Lowrise)
- **Conditions**: Hauteur < 10m
- **Dossiers**: `lowrise/small_shops/`, `lowrise/cafes_restaurants/`, `lowrise/services/`, `lowrise/traditional_stores/`
- **Style**: Petits commerces, cafés, services
- **Mapping**: Texture standard (Scale 1.5:1.5:1.5)

## 📁 INSTALLATION DU SYSTÈME

### 🔧 Étape 1: Création de la structure
```python
# Exécuter dans Blender (Text Editor)
exec(open("setup_textures.py").read())
```

Ou exécuter manuellement:
```
C:/Users/sshom/Documents/Assets/Textures/Tokyo_Buildings/
├── skyscrapers/
│   ├── glass_towers/
│   ├── modern_office/
│   ├── metallic_facades/
│   └── corporate_buildings/
├── commercial/
│   ├── shopping_centers/
│   ├── retail_facades/
│   ├── colorful_buildings/
│   └── modern_stores/
├── midrise/
│   ├── apartment_blocks/
│   ├── office_buildings/
│   ├── mixed_use/
│   └── urban_housing/
├── residential/
│   ├── japanese_houses/
│   ├── modern_homes/
│   ├── traditional_buildings/
│   └── small_apartments/
└── lowrise/
    ├── small_shops/
    ├── cafes_restaurants/
    ├── services/
    └── traditional_stores/
```

### 📸 Étape 2: Ajouter vos textures
- **Formats supportés**: .jpg, .png, .exr, .hdr, .tiff, .bmp
- **Taille recommandée**: 1024x1024 pixels minimum
- **Conseil**: Utilisez des textures seamless (répétables)

### ⚙️ Étape 3: Activer dans l'addon
1. Ouvrir Blender
2. Onglet **Tokyo** (sidebar N)
3. Cocher **"Advanced Textures"**
4. Générer votre ville!

## 🎮 UTILISATION

### Interface mise à jour:
```
🗾 Tokyo City Generator 1.2.0
┌─────────────────────────────┐
│ ⚙️ Configuration            │
│ District Size: [3]          │
│ Block Density: [100%]       │
│ Building Variety: [All]     │
│ Organic Streets: [30%]      │
│ Advanced Textures: [✓]      │ ← NOUVEAU!
└─────────────────────────────┘
```

### Algorithme de sélection:
1. **Calculer dimensions** du bâtiment (hauteur, largeur_x, largeur_y)
2. **Déterminer catégorie** selon conditions
3. **Choisir dossier aléatoire** dans la catégorie
4. **Sélectionner texture aléatoire** dans le dossier
5. **Appliquer avec mapping** approprié

## 🎨 SYSTÈME DE MATÉRIAUX

### Matériaux avec texture:
- **Nœud Image Texture** avec texture chargée
- **Mapping personnalisé** selon catégorie
- **Paramètres PBR** adaptés (metallic, roughness)
- **Nommage**: `Tokyo_Advanced_{category}_{building_name}`

### Matériaux procéduraux (fallback):
- **Couleurs par catégorie** si pas de texture
- **Paramètres réalistes** metallic/roughness
- **Variation aléatoire** pour commercial

## 🔍 DÉBOGAGE ET TESTS

### Script de test:
```python
# Dans Blender Text Editor
exec(open("test_texture_system.py").read())
```

### Messages de debug:
- `🎨 Texture sélectionnée: facade_01.jpg pour skyscraper`
- `🏗️ Matériau créé: Tokyo_Advanced_skyscraper_0_0`
- `⚠️ Dossier texture inexistant: /path/to/folder`

### Vérifications:
1. **Structure dossiers** créée correctement
2. **Images présentes** dans les dossiers
3. **Propriété activée** dans l'interface
4. **Import système** réussi

## 🚀 RÉSULTATS ATTENDUS

### Ville 3x3 avec textures:
- **1 gratte-ciel** avec texture glass_towers
- **4 centres commerciaux** avec textures colorées variées  
- **4 maisons** avec textures japanese_houses
- **Tous différents** grâce à la sélection aléatoire!

### Avantages vs matériaux de base:
- ✅ **Réalisme photographique** avec vraies textures
- ✅ **Variété infinie** selon vos images
- ✅ **Adaptation automatique** selon dimensions
- ✅ **Mapping intelligent** par type de bâtiment
- ✅ **Fallback sûr** si pas de textures

## 📋 FORMATS ET CONSEILS

### Formats recommandés:
- **JPG** pour photos de façades (plus petit)
- **PNG** pour textures avec transparence
- **EXR/HDR** pour éclairage HDR avancé

### Conseils de texture:
- **Seamless**: Éviter les répétitions visibles
- **Résolution**: 1024² optimal, 2048² pour détails
- **Contraste**: Éviter trop sombre/clair
- **Perspective**: Façades droites, pas d'angle

### Nommage suggéré:
```
glass_tower_01.jpg
office_facade_modern_blue.png
shop_colorful_red_01.jpg
house_japanese_traditional_wood.jpg
```

## 🔧 PERSONNALISATION AVANCÉE

### Modifier les catégories:
Éditer `texture_system.py`:
```python
'skyscraper': {
    'height_range': (50, 200),    # Modifier seuils
    'width_range': (10, 40),
    'texture_folders': [          # Ajouter dossiers
        'skyscrapers/my_custom_folder'
    ]
}
```

### Ajouter chemins de textures:
```python
possible_paths = [
    "C:/MonDossier/Textures/",    # Ajouter ici
    "D:/Assets/Buildings/",
    # ...
]
```

## 🎯 OBJECTIF ATTEINT

**ENFIN** un système de textures qui:
- ✅ **Sélectionne automatiquement** selon dimensions
- ✅ **Supporte tous formats** image courants  
- ✅ **Organise intelligemment** par catégories
- ✅ **Variété infinie** avec vos propres textures
- ✅ **Mapping adaptatif** par type de bâtiment
- ✅ **Fallback sûr** sans erreurs

**Fini les matériaux unis !**  
**Place au réalisme photographique !** 🎨🏙️✨

---
*Tokyo Texture System v1.2.0 - Généré automatiquement*
