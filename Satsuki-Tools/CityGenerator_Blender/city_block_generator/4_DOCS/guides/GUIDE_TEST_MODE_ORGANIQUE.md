# 🌿 GUIDE TEST MODE ORGANIQUE - CITY BLOCK GENERATOR v7.8.0

## ✅ **CORRECTION DU BUG APPLIQUÉE**

Le bug a été résolu ! La fonction `generate_organic_city_layout()` a été mise à jour pour:
- Accepter le bon nombre de paramètres (context au lieu de 6 paramètres séparés)
- Utiliser les fonctions existantes de l'addon (`safe_delete_objects`, `generate_building`)
- Créer les matériaux correctement avec `create_material()`
- Retourner un booléen comme attendu par l'opérateur

## 🚀 **COMMENT TESTER LE MODE ORGANIQUE**

### 1. **Installation**
```
1. Ouvrez Blender
2. Edit > Preferences > Add-ons
3. Install... > Sélectionnez le dossier city_block_generator
4. Activez "City Block Generator"
5. Appuyez N pour ouvrir la sidebar, trouvez l'onglet "CityGen"
```

### 2. **Test Mode Standard (référence)**
```
✅ Désactivez "Mode Organique" (case décochée)
✅ Configurez: Grille 3x3, Bâtiments par bloc: 1
✅ Cliquez "Générer Quartier"
✅ Observez: Grille rectangulaire régulière
```

### 3. **Test Mode Organique (nouveau)**
```
🌿 Activez "Mode Organique" (case cochée)
🌿 Ajustez les paramètres:
   - Côtés Min: 4, Côtés Max: 6
   - Intensité Courbes: 0.7
   - Variation Blocs: 0.4
🌿 Cliquez "Générer Quartier"
🌿 Observez: Blocs polygonaux + routes courbes!
```

## 🔧 **PARAMÈTRES ORGANIQUES EXPLIQUÉS**

| Paramètre | Description | Effet |
|-----------|-------------|-------|
| **Mode Organique** | Active/désactive le layout organique | ON = polygones + courbes, OFF = grille standard |
| **Côtés Min/Max** | Nombre de côtés des blocs polygonaux | 3-8 côtés possibles (triangles à octogones) |
| **Intensité Courbes** | Probabilité de routes courbes | 0.0 = toutes droites, 1.0 = toutes courbes |
| **Variation Blocs** | Variation de taille des blocs | 0.0 = uniforme, 1.0 = très varié |

## 🎯 **TESTS RECOMMANDÉS**

### Test 1: Blocs Polygonaux Variés
```
Côtés Min: 3, Côtés Max: 8
Variation Blocs: 0.8
Intensité Courbes: 0.0
→ Résultat: Blocs de 3 à 8 côtés, tailles variables, routes droites
```

### Test 2: Routes Courbes Maximum
```
Côtés Min: 4, Côtés Max: 4  
Variation Blocs: 0.0
Intensité Courbes: 1.0
→ Résultat: Carrés uniformes, toutes routes courbes
```

### Test 3: Chaos Organique Total
```
Côtés Min: 3, Côtés Max: 8
Variation Blocs: 1.0
Intensité Courbes: 0.8
→ Résultat: Maximum de variété et chaos naturel
```

### Test 4: Subtilité Organique
```
Côtés Min: 5, Côtés Max: 6
Variation Blocs: 0.2
Intensité Courbes: 0.3
→ Résultat: Léger aspect organique, plus réaliste
```

## 🐛 **RÉSOLUTION DU BUG**

**Problème original:**
```
Error: generate_organic_city_layout() missing 5 required positional arguments: 
'length', 'road_width', 'road_mat', 'side_mat', and 'build_mat'
```

**Solution appliquée:**
```python
# AVANT (cassé)
def generate_organic_city_layout(width, length, road_width, road_mat, side_mat, build_mat):

# APRÈS (fonctionnel)  
def generate_organic_city_layout(context):
    # Récupère tous les paramètres depuis context.scene
    scene = context.scene
    width = safe_int(getattr(scene, 'citygen_width', 5), 5)
    road_mat = create_material("RoadMat_Organic", (1.0, 0.75, 0.8))
    # etc...
```

## 🎉 **RÉSULTAT ATTENDU**

Avec le mode organique activé, vous devriez voir:
- ✅ Blocs de formes polygonales variées (pas seulement des rectangles)
- ✅ Routes avec angles et courbes naturelles
- ✅ Variation de taille entre les blocs
- ✅ Bâtiments adaptés aux blocs polygonaux
- ✅ Aspect plus naturel et moins géométrique qu'une grille standard

## 📊 **DÉBOGAGE**

Si ça ne marche pas:
1. Vérifiez la console Blender (Window > Toggle System Console)
2. Recherchez les messages commençant par "🌿" (mode organique)
3. Les erreurs Python seront visibles dans la console
4. Rechargez l'addon (F3 > "Reload Scripts")

**Version déployée:** 7.8.0
**Statut:** ✅ Bug corrigé, prêt pour les tests!
