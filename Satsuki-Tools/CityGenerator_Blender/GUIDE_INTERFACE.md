# 🎛️ GUIDE INTERFACE - City Block Generator v6.13.2

## 📍 Où Changer de Mode dans l'Interface

### 🔍 Localisation des Options

L'interface du City Block Generator est organisée en **4 sections principales** :

```
┌─ ⚙️ Paramètres:
│  ├─ Largeur: [5]           ← Nombre de colonnes
│  ├─ Longueur: [5]          ← Nombre de rangées  
│  ├─ Étages max: [8]        ← Hauteur maximale
│  └─ Forme: [AUTO]          ← Style des bâtiments
│
├─ 🏗️ Variété des blocs:
│  ├─ Taille de base: [10.0] ← Taille standard
│  ├─ Variété: [MEDIUM]      ← Variation des tailles
│  │
│  ├─ 🏙️ Mode quartiers:     ← *** C'EST ICI ! ***
│  │  └─ ☑️ Activer les zones distinctes
│  │
│  └─ ⚙️ Configuration des zones: (si mode activé)
│     ├─ 🏢 Commercial: [0.35] ← Zones d'affaires
│     ├─ 🏠 Résidentiel: [0.45] ← Zones d'habitation
│     └─ 🏭 Industriel: [0.20]  ← Zones d'activité
│
├─ ▶️ Actions:
│  ├─ 🏗️ Générer Quartier    ← Création complète
│  ├─ 🛣️ Régénérer Routes     ← Routes seulement
│  └─ 🔄 Réinitialiser       ← Valeurs par défaut
│
└─ 💡 Conseils:
   ├─ Grilles > 10x10 = lent
   └─ Sauvegardez avant génér...
```

## 🎯 Comment Activer le Mode District

### 1. Trouver la Section "Variété des blocs"
- Déroulez le panneau CityGen dans la vue 3D
- Localisez la section avec l'icône 🏗️
- C'est la **2ème section** de l'interface

### 2. Activer le Mode Quartiers
- Cherchez "🏙️ Mode quartiers:"
- **Cochez la case** "☑️ Activer les zones distinctes"
- Les options de configuration apparaissent automatiquement

### 3. Configurer les Zones
Une fois le mode activé, vous verrez :
```
⚙️ Configuration des zones:
🏢 Commercial:   [█████████░] 35%
🏠 Résidentiel:  [████████░░] 45%  
🏭 Industriel:   [████░░░░░░] 20%
```

## 🎨 Types de Zones Disponibles

### 🏢 Zone Commerciale (Bleu)
- **Caractéristiques** : Bâtiments grands et hauts
- **Ratio recommandé** : 20-40%
- **Matériau** : Bleu distinctif
- **Usage** : Centres d'affaires, commerces

### 🏠 Zone Résidentielle (Vert)  
- **Caractéristiques** : Taille normale, hauteur variée
- **Ratio recommandé** : 40-60%
- **Matériau** : Vert distinctif
- **Usage** : Quartiers d'habitation

### 🏭 Zone Industrielle (Orange)
- **Caractéristiques** : Large et bas, aspect fonctionnel
- **Ratio recommandé** : 10-30%
- **Matériau** : Orange distinctif
- **Usage** : Zones d'activité, entrepôts

## ⚙️ Autres Options de Variété

### Variété des Tailles
Dans la même section, vous pouvez aussi modifier :

- **UNIFORM** : Tous les blocs identiques
- **LOW** : Légère variation (±20%)
- **MEDIUM** : Variation modérée (±40%) 
- **HIGH** : Grande variation (±60%)
- **EXTREME** : Variation maximale (-75% à +100%)

### Taille de Base
- **Min** : 2.0 unités (blocs très petits)
- **Max** : 50.0 unités (blocs énormes)
- **Recommandé** : 10-15 unités

## 🚀 Utilisation Pratique

### Configuration Rapide Districts
```
1. Mode quartiers : ☑️ ACTIVÉ
2. Variété : HIGH ou EXTREME
3. Taille de base : 12.0
4. Ratios : C=35%, R=45%, I=20%
5. Grille : 7x7 (optimal)
```

### Configuration Test Simple
```
1. Mode quartiers : ☐ DÉSACTIVÉ  
2. Variété : UNIFORM
3. Taille de base : 10.0
4. Grille : 3x3 (test rapide)
```

## 💡 Conseils Interface

### ✅ Bonnes Pratiques
- **Sauvegardez** votre scène avant génération
- **Testez** avec des petites grilles d'abord
- **Activez** le mode district pour plus de réalisme
- **Variez** les ratios selon vos besoins

### ⚠️ Points d'Attention
- Les ratios totalisent automatiquement 100%
- Grilles > 10x10 peuvent être lentes
- Le mode district nécessite Blender en mode Object
- Sauvegardez avant d'expérimenter

## 🎯 Résumé

**Le mode district se trouve dans la section "Variété des blocs", sous forme d'une case à cocher "Activer les zones distinctes". Une fois activé, les sliders de configuration des zones apparaissent automatiquement !**

---

*Guide Interface v6.13.2 - Mode District Accessible*
