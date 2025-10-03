# GUIDE MODE DISTRICT - City Block Generator v6.13.0

## 🏙️ Mode District Activé

Le mode district est maintenant **ACTIVÉ PAR DÉFAUT** dans cette version. Il crée des zones urbaines distinctes avec des caractéristiques visuelles et architecturales différenciées.

## 🎯 Comment utiliser le mode district

### 1. Installation et Activation
1. Installez l'addon `city_block_generator.zip` dans Blender
2. Activez l'addon dans les préférences
3. Le mode district est maintenant activé par défaut (case cochée)

### 2. Configuration des Paramètres

#### Paramètres de Base
- **Grille** : Recommandé 6x6 à 8x8 pour voir les effets de district
- **Variété** : HIGH ou EXTREME pour maximiser les différences
- **Taille de base** : 12-15 unités pour des blocs variés

#### Ratios des Zones (Mode District)
- **Commercial** (0.2-0.4) : Zones d'affaires avec grands bâtiments
- **Résidentiel** (0.4-0.6) : Zones d'habitation avec hauteurs variées  
- **Industriel** (0.1-0.3) : Zones industrielles avec bâtiments bas et larges

### 3. Caractéristiques Visuelles par Zone

#### 🏢 Zone Commerciale (Bleu)
- Bâtiments **50% plus grands** que la normale
- Hauteurs **importantes** (jusqu'à 150% du max)
- Matériau **bleu distinctif**
- Formes plus **imposantes**

#### 🏠 Zone Résidentielle (Vert)
- Tailles de blocs **normales**
- Hauteurs **variées** (30% de chance d'être plus hauts)
- Matériau **vert distinctif**
- Densité **équilibrée**

#### 🏭 Zone Industrielle (Orange)
- Blocs **2x plus larges**
- Bâtiments **bas** (1-2 étages seulement)
- Matériau **orange distinctif**
- Aspect **étalé et fonctionnel**

## 🔧 Configuration Recommandée pour la Démonstration

```
Largeur/Longueur : 7x7
Étages max : 15
Variété : HIGH
Taille de base : 12.0
Mode district : ✓ ACTIVÉ

Ratios :
- Commercial : 0.35
- Résidentiel : 0.45  
- Industriel : 0.20
```

## 🎨 Identification Visuelle

### Matériaux Distinctifs
Chaque zone a maintenant son propre matériau coloré :
- **Bleu** = Commercial (centres d'affaires)
- **Vert** = Résidentiel (quartiers d'habitation)
- **Orange** = Industriel (zones d'activité)

### Analyse du Résultat
Après génération, vérifiez :
1. **Répartition** : Les zones sont-elles bien distribuées ?
2. **Tailles** : Les blocs commerciaux sont-ils plus grands ?
3. **Hauteurs** : Les bâtiments industriels sont-ils plus bas ?
4. **Couleurs** : Les matériaux reflètent-ils les zones ?

## 🧪 Script de Test

Pour tester le mode district dans Blender, copiez ce code dans l'éditeur de texte :

```python
import bpy

# Configuration optimale pour test
props = bpy.context.scene.citygen_props
props.width = 7
props.length = 7
props.max_floors = 15
props.block_variety = 'HIGH'
props.base_block_size = 12.0
props.district_mode = True
props.commercial_ratio = 0.35
props.residential_ratio = 0.45
props.industrial_ratio = 0.20

# Générer le quartier
bpy.ops.citygen.generate_city()
```

## 🔍 Dépannage

### Le mode district ne semble pas actif
- Vérifiez que la case "Mode quartiers" est cochée
- Assurez-vous que les ratios totalisent 1.0
- Utilisez une grille suffisamment grande (6x6 minimum)

### Les zones ne sont pas visibles
- Regardez les couleurs des matériaux (bleu/vert/orange)
- Vérifiez les tailles relatives des blocs
- Observez les hauteurs des bâtiments

### Les ratios ne fonctionnent pas
- Les ratios doivent totaliser 1.0 (ajustement automatique)
- Grilles trop petites peuvent ne pas respecter les ratios exacts
- Essayez avec une grille 8x8 ou plus grande

## 📊 Messages de Débogage

Dans la console Blender, vous verrez :
```
Districts générés - Commercial: X/49, Résidentiel: Y/49, Industriel: Z/49
Génération bâtiment N de type rectangular (zone: COMMERCIAL)
Application du matériau de district COMMERCIAL au bâtiment N
```

Ces messages confirment le bon fonctionnement du mode district.

## 🚀 Prochaines Étapes

1. **Tester** différentes configurations de ratios
2. **Observer** l'impact sur la répartition urbaine
3. **Expérimenter** avec différentes tailles de grille
4. **Comparer** avec le mode district désactivé

Le mode district transforme votre génération procédurale en véritable planification urbaine !
