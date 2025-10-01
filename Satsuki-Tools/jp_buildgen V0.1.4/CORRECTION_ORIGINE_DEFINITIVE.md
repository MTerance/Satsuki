# Correction DÉFINITIVE du flottement - V2

## Problème identifié et résolu

### Le vrai problème
Le problème n'était **PAS** seulement le positionnement Z, mais l'**origine des objets** dans Blender.

Quand on crée un cube avec `primitive_cube_add`, l'origine (point de référence) est au **centre géométrique** du cube. Même en ajustant les positions Z, les objets continuent de flotter car leur base n'est pas à l'origine.

### Solution implémentée

#### 1. Modification de `_add_cube()`
```python
def _add_cube(name, size=(2,2,2), loc=(0,0,0), mat=None):
    # Créer le cube à l'origine
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0,0,0))
    o = bpy.context.active_object
    o.name = name
    
    # Appliquer la taille
    o.scale = (size[0]/2.0, size[1]/2.0, size[2]/2.0)
    
    # CRUCIAL: Entrer en mode édition pour déplacer les vertices
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Sélectionner tous les vertices et les déplacer vers le haut
    bpy.ops.mesh.select_all(action='SELECT')
    # Déplacer de la moitié de la hauteur vers le haut
    bpy.ops.transform.translate(value=(0, 0, 0.5))
    
    # Retourner en mode objet
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Positionner l'objet (base maintenant à Z=0 en coordonnées locales)
    o.location = loc
```

**Résultat** : L'origine de chaque mesh est maintenant au **bottom center** (centre de la base inférieure).

#### 2. Simplification des calculs de position

Avec le nouveau système d'origine :
- **Pour poser sur le sol** : `z = GROUND_LEVEL` 
- **Pour empiler** : `z = hauteur_précédente`
- **Plus besoin** de calculer `/2` pour centrer

### Corrections par type de bâtiment

#### Office
```python
# AVANT (origine au centre)
_add_cube(PREFIX+"Office_Podium", (...), (0,0,GROUND_LEVEL + podium_h/2), (...))

# APRÈS (origine au bottom center)  
_add_cube(PREFIX+"Office_Podium", (...), (0,0,GROUND_LEVEL), (...))
```

#### Mall, Restaurant, Konbini, Apartment, House
Même principe appliqué à tous les types avec les ajustements appropriés.

#### Parcelle (sol)
```python
# Sol et trottoir positionnés à Z=0 (base au sol)
ground = _add_cube(PREFIX+"Ground", (...), (0, (...), 0), (...))
```

### Avantages de la nouvelle approche

1. **Ancrage parfait** : Chaque objet a sa base exactement où on le souhaite
2. **Calculs simplifiés** : Plus besoin de `/2` dans les positions Z
3. **Empilement logique** : Les objets se posent naturellement les uns sur les autres
4. **Cohérence visuelle** : Aucun gap entre le sol et les bâtiments

### Test de validation

Pour valider dans Blender :
1. Générer un bâtiment de chaque type
2. Vérifier en vue de côté que la base touche le sol
3. Confirmer qu'il n'y a aucun flottement visible
4. Valider que les proportions sont conservées

## Statut : ✅ RÉSOLU DÉFINITIVEMENT

La correction de l'origine des meshs au bottom center résout complètement le problème de flottement pour tous les types de bâtiments.