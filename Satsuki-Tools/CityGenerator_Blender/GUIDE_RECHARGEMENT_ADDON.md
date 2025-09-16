# 🔄 Guide du Rechargement d'Addon dans Blender

## 📖 Comment Recharger l'Addon depuis un Bouton

L'addon City Block Generator propose **2 types de rechargement** accessibles directement depuis l'interface :

### 🚀 **Rechargement Rapide** (Recommandé)
**Bouton**: `Rechargement Rapide` ⚡

**Ce qu'il fait**:
- Recharge uniquement les modules Python modifiés
- **Conserve** les propriétés et paramètres actuels
- **Rapide** et sûr
- Idéal pour tester des modifications de code

**Utilisation**:
```
1. Modifiez le code Python de l'addon
2. Dans Blender > Sidebar (N) > CityGen
3. Cliquez "Rechargement Rapide"
4. ✅ Les modifications sont prises en compte
```

### 🔧 **Rechargement Complet**
**Bouton**: `Rechargement Complet` 🔄

**Ce qu'il fait**:
- **Désenregistre** complètement l'addon
- Recharge tous les modules
- **Ré-enregistre** l'addon
- Sauvegarde et restaure les propriétés

**Utilisation**:
```
1. Pour des changements majeurs (nouvelles classes, etc.)
2. Dans Blender > Sidebar (N) > CityGen  
3. Cliquez "Rechargement Complet"
4. ✅ Rechargement complet effectué
```

## 🛠️ Code des Opérateurs

### Rechargement Rapide
```python
class CITYGEN_OT_QuickReload(bpy.types.Operator):
    bl_idname = "citygen.quick_reload"
    bl_label = "Rechargement Rapide"
    
    def execute(self, context):
        import importlib
        import sys
        
        # Recharger les modules sans désenregistrement
        modules = [
            "city_block_generator_6_12.generator",
            "city_block_generator_6_12.operators", 
            "city_block_generator_6_12.ui"
        ]
        
        for module_name in modules:
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
        
        # Mise à jour interface
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'UI':
                        region.tag_redraw()
        
        return {'FINISHED'}
```

### Rechargement Complet
```python
class CITYGEN_OT_ReloadAddon(bpy.types.Operator):
    bl_idname = "citygen.reload_addon"
    bl_label = "Recharger Addon"
    
    def execute(self, context):
        import importlib
        import sys
        
        # 1. Sauvegarder les propriétés
        current_props = {}
        if hasattr(context.scene, 'citygen_props'):
            props = context.scene.citygen_props
            current_props = {
                'width': props.width,
                'length': props.length,
                # ... autres propriétés
            }
        
        # 2. Désenregistrer l'addon
        addon_module = sys.modules["city_block_generator_6_12"]
        addon_module.unregister()
        
        # 3. Recharger tous les modules
        for module_name in sys.modules:
            if module_name.startswith("city_block_generator_6_12"):
                importlib.reload(sys.modules[module_name])
        
        # 4. Ré-enregistrer l'addon
        addon_module.register()
        
        # 5. Restaurer les propriétés
        if current_props and hasattr(context.scene, 'citygen_props'):
            props = context.scene.citygen_props
            for key, value in current_props.items():
                setattr(props, key, value)
        
        return {'FINISHED'}
```

## 🎯 Quand Utiliser Chaque Type ?

### 🚀 Rechargement Rapide
- ✅ Modification de fonctions existantes
- ✅ Changement d'algorithmes 
- ✅ Correction de bugs
- ✅ Ajustement d'interface
- ✅ Développement quotidien

### 🔧 Rechargement Complet
- ✅ Ajout de nouvelles classes
- ✅ Modification des PropertyGroups
- ✅ Changement des bl_info
- ✅ Problèmes de registre
- ✅ Après modifications majeures

## 🚨 Dépannage

### Problème: "Module non trouvé"
```python
# Solution: Vérifier le nom du module
print(list(sys.modules.keys()))  # Liste tous les modules
```

### Problème: "Propriétés perdues"
```python
# Les propriétés sont automatiquement sauvegardées
# Si problème, utilisez "Réinitialiser Paramètres"
```

### Problème: "Interface ne se met pas à jour"
```python
# Force la mise à jour manuelle
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for region in area.regions:
            if region.type == 'UI':
                region.tag_redraw()
```

## 📋 Console de Debug

Pour voir les détails du rechargement:
```
1. Window > Toggle System Console
2. Effectuez le rechargement
3. Observez les messages:
   ✅ Module xyz rechargé
   ⚠️ Attention: xyz
   ❌ Erreur: xyz
```

## 🎮 Raccourcis de Développement

Pour les développeurs d'addons, vous pouvez créer des raccourcis:

```python
# Dans la console Python de Blender
import bpy
bpy.ops.citygen.quick_reload()  # Rechargement rapide
bpy.ops.citygen.reload_addon()  # Rechargement complet
```

---

**💡 Conseil**: Pendant le développement, utilisez principalement le **Rechargement Rapide**. Passez au **Rechargement Complet** uniquement si nécessaire ou en cas de problème.
