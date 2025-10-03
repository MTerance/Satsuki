# City Block Generator v6.13.0 - Système de Blocs Variés

## 🎉 **NOUVELLES FONCTIONNALITÉS MAJEURES**

### 🏗️ **VARIÉTÉ DES BLOCS**

Le système permet maintenant de générer des blocs de superficies très différentes avec 6 modes de variation :

#### **Modes de Variété :**
- **🔲 Uniforme** : Tous les blocs ont exactement la même taille
- **📐 Faible** : Variation de 80% à 120% (±20%)
- **📊 Moyenne** : Variation de 60% à 140% (±40%) - *Par défaut*
- **📈 Élevée** : Variation de 40% à 160% (±60%)
- **🎲 Extrême** : Variation de 25% à 200% (-75% à +100%)
- **🏘️ Quartiers** : Zones distinctes avec tailles cohérentes

### 🏙️ **MODE DISTRICTS**

Quand activé, ce mode crée des zones urbaines réalistes avec des caractéristiques distinctes :

#### **Types de Zones :**
- **🏢 Commercial** (20% par défaut)
  - Blocs 50% plus grands
  - Bâtiments plus hauts (4+ étages)
  - Formes préférées : Rectangle, L, U

- **🏠 Résidentiel** (60% par défaut)
  - Taille normale des blocs
  - Hauteur variable (1-8+ étages)
  - Formes préférées : Rectangle, L, T

- **🏭 Industriel** (20% par défaut)
  - Blocs double taille
  - Bâtiments bas (1-2 étages)
  - Formes préférées : Rectangle, L

### ⚙️ **NOUVEAUX PARAMÈTRES**

#### **Paramètres de Base :**
- **Taille de bloc de base** : 2-50 unités Blender
- **Mode quartiers** : Activé/Désactivé

#### **Ratios des Zones :**
- **Ratio commercial** : 0-100%
- **Ratio résidentiel** : 0-100%
- **Ratio industriel** : 0-100%

*Note : Les ratios sont automatiquement normalisés*

### 🛠️ **AMÉLIORATIONS TECHNIQUES**

#### **Structure de Données Enrichie :**
- Chaque bloc contient maintenant :
  - Taille (largeur, profondeur)
  - Type de zone
  - Informations de zone
  - Variation de base

#### **Génération Intelligente :**
- **Zones cohérentes** : Les blocs similaires sont regroupés
- **Centres de zones** : Algorithme de proximité pour les districts
- **Variation contextuelle** : Tailles basées sur la position et le type

#### **Compatibilité :**
- Support de l'ancienne structure de données
- Migration transparente des projets existants
- Interface enrichie avec nouveaux contrôles

## 🎯 **UTILISATION PRATIQUE**

### **Pour une ville moderne variée :**
1. Mode : **Élevée** ou **Extrême**
2. Districts : **Activé**
3. Commercial : **30%**, Résidentiel : **50%**, Industriel : **20%**

### **Pour un quartier résidentiel uniforme :**
1. Mode : **Uniforme** ou **Faible**
2. Districts : **Désactivé**
3. Taille de base : **8-12 unités**

### **Pour une zone industrielle :**
1. Mode : **Moyenne**
2. Districts : **Activé**
3. Industriel : **80%**, Autres : **20%**

## 📦 **INSTALLATION**

1. **Installez** `city_block_generator.zip` dans Blender
2. **Activez** l'addon dans les Préférences
3. **Trouvez** le panneau "CityGen" dans la sidebar (N)
4. **Explorez** les nouveaux paramètres sous "Variété des blocs"

## 🔄 **COMPATIBILITÉ**

- **Blender 4.0+** requis
- **Compatible** avec les projets existants
- **Migration automatique** des anciennes données
- **Préservation** des routes et alignements corrigés

---

**Version 6.13.0** - Système de génération de blocs de superficies différentes pour des villes plus réalistes et variées ! 🏙️✨
