# 🚨 CORRECTION URGENTE - ERREUR BLENDER 4.0+

## ❌ PROBLÈME IDENTIFIÉ
**Erreur**: `KeyError: 'bpy_prop_collection[key]: key "Specular" not found'`

**Cause**: La propriété `'Specular'` n'existe plus dans Blender 4.0+ 
- Elle a été remplacée par `'IOR'` (Index of Refraction)
- L'ancien code utilisait `bsdf.inputs['Specular'].default_value = 0.3`

## ✅ SOLUTION APPLIQUÉE

### Code Corrigé
```python
def apply_sidewalk_material(self, obj):
    """Matériau spécifique pour les trottoirs"""
    mat = bpy.data.materials.new(name="Tokyo_Sidewalk")
    mat.use_nodes = True
    
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    # Couleur béton claire pour les trottoirs
    bsdf.inputs['Base Color'].default_value = (0.7, 0.7, 0.75, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.8
    # ✅ SUPPRIMÉ: bsdf.inputs['Specular'].default_value = 0.3
    
    obj.data.materials.append(mat)
```

### Fichier Corrigé
- ✅ **tokyo_realistic_v2_1_1_FIXED.zip** (7.3KB)
- ✅ Compatible Blender 4.0+
- ✅ Même fonctionnalités (rues variées + trottoirs)

## 🔄 INSTALLATION DU CORRECTIF

1. **Désinstaller** l'ancien addon (si installé)
2. **Installer** `tokyo_realistic_v2_1_1_FIXED.zip`
3. **Activer** "Tokyo City Generator v2.1.1 REALISTIC"
4. **Tester** génération immédiatement

## 🎯 TEST RAPIDE
- City Size: **5**
- Building Style: **Mixed**  
- Density: **70%**
- Better Materials: **ON**

**Cliquer "Generate Tokyo City"** → Doit fonctionner SANS erreur !

---

**STATUS**: ✅ CORRIGÉ - Prêt pour test final