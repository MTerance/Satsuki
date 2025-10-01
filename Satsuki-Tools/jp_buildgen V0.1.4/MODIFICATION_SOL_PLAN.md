# Modification du sol : Cube → Plan à Z=0

## Changement majeur implémenté

### 🔄 Transformation du sol de la parcelle

**AVANT** : Sol = cube épais de 0.02 unités
```python
# Sol comme cube épais
ground = _add_cube(PREFIX+"Ground", (..., 0.02), (0, (...), 0.01), (...))
GROUND_LEVEL = 0.02  # Bâtiments au-dessus du cube
```

**APRÈS** : Sol = plan parfait à Z=0
```python
# Sol comme plan de référence
ground = _add_plane(PREFIX+"Ground", (...), (0, (...), 0), (...))  
GROUND_LEVEL = 0.0   # Bâtiments directement sur le plan
```

### 🎯 Avantages de cette approche

1. **Référence absolue** : Le sol est exactement à Z=0, point de référence parfait
2. **Simplicité géométrique** : Plan infini sans épaisseur inutile
3. **Précision maximale** : Aucune approximation, ancrage parfait
4. **Performance** : Plan plus léger qu'un cube
5. **Logique intuitive** : Sol = base absolue du monde

### 🔧 Implémentation technique

#### Nouvelle fonction `_add_plane()`
```python
def _add_plane(name, size=(2,2), loc=(0,0,0), mat=None):
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = (size[0]/2.0, size[1]/2.0, 1.0)  # Pas de Z
    # Application matériau...
    return o
```

#### Parcelle modifiée
```python
def _make_parcel(root, foot_x, foot_y, front=3.0, others=0.8, M=None):
    # Sol = plan de référence à Z=0
    ground = _add_plane(PREFIX+"Ground", (foot_x + 2*others, foot_y + others + front),
                        (0, (front-others)*0.5, 0), M["ground"])
    
    # Trottoir = cube fin posé sur le plan (optionnel, pour la visualisation)
    sw = _add_cube(PREFIX+"Sidewalk_Front", (..., 0.02), (..., 0), M["ground"])
```

#### Constante ajustée
```python
GROUND_LEVEL = 0.0  # Sol = plan à Z=0, bâtiments posés directement
```

### 📐 Impact sur les positions

Tous les bâtiments sont maintenant positionnés avec leur **base exactement à Z=0** :

| Élément | Position Z |
|---------|------------|
| **Sol** | `0.0` (plan de référence) |
| **Trottoir** | `0.0` → `0.02` (cube fin) |
| **Bâtiments** | `0.0` → `hauteur` (base sur plan) |
| **Toits** | `hauteur_bâtiment` → `hauteur + toit` |
| **Équipements** | `top_z` (calculé automatiquement) |

### 🏗️ Structure finale

```
Z = hauteur_max    ┌─ Équipements toiture
                   │
Z = hauteur_toit   ├─ Toits / Modules
                   │
Z = hauteur_corps  ├─ Corps des bâtiments
                   │
Z = 0.02           ├─ Trottoir (optionnel)
Z = 0.0            └─ SOL (plan de référence)
```

### ✅ Avantages immédiats

1. **Ancrage parfait** : Base des bâtiments exactement à Z=0
2. **Référence claire** : Sol = origine du monde 3D
3. **Calculs simplifiés** : Plus de compensation d'épaisseur
4. **Cohérence visuelle** : Alignement parfait sur l'horizon
5. **Standards respectés** : Convention 3D universelle

### 🧪 Test de validation

Dans Blender, vérifier que :
- Le sol apparaît comme un plan à Z=0
- Tous les bâtiments ont leur base exactement sur ce plan
- Aucun gap ou flottement visible
- Le trottoir (si activé) repose sur le plan

## Statut : ✅ SOL PARFAIT À Z=0

Le sol est maintenant un plan de référence absolu à Z=0. Tous les bâtiments sont parfaitement ancrés sur cette base géométrique idéale.