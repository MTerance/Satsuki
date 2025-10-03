# 🚨 Guide de Résolution - Addon Invisible dans Blender

## ❌ Problème: "L'addon n'est plus pris en compte par Blender et aucun message de debug"

### 🔍 **Diagnostic Effectué**
Le problème a été identifié et corrigé dans la version 6.21.1 :

**Problèmes trouvés :**
1. ❌ Décorateur `@bpy.app.handlers.persistent` manquant/incorrect
2. ❌ Import `bpy` manquant dans `__init__.py`
3. ❌ Gestion des erreurs lors de l'enregistrement

**Solutions appliquées :**
1. ✅ Décorateur `persistent` appliqué de manière conditionnelle
2. ✅ Import `bpy` ajouté dans `__init__.py`
3. ✅ Gestion robuste des erreurs d'enregistrement

---

## 🎯 **Solution Immédiate** 

### Étape 1: Installation de la Version Corrigée
```
1. Téléchargez: city_block_generator.zip (dernière version)
2. Dans Blender: Edit > Preferences > Add-ons
3. Si "City Block Generator" existe déjà:
   - Trouvez-le dans la liste
   - Cliquez la flèche pour déplier
   - Cliquez "Remove"
4. Redémarrez Blender complètement
5. Edit > Preferences > Add-ons > Install
6. Sélectionnez le nouveau ZIP
7. Activez "City Block Generator"
```

### Étape 2: Vérification
```
✅ Dans la vue 3D, appuyez sur N
✅ Cherchez l'onglet "CityGen" dans la sidebar
✅ Le panneau devrait afficher tous les paramètres
✅ Test: Changez Largeur=3, Longueur=3, cliquez "Générer Quartier"
```

---

## 🧪 **Diagnostic Avancé** (Si le problème persiste)

### Script de Test Rapide
Copiez/collez ce code dans la console Python de Blender:

```python
import bpy
import sys

print("=== DIAGNOSTIC ADDON CITY BLOCK GENERATOR ===")

# Vérifier si l'addon est chargé
addon_name = "city_block_generator_6_12"
if addon_name in sys.modules:
    print(f"✅ Module {addon_name}: CHARGÉ")
    addon_module = sys.modules[addon_name]
    
    # Vérifier bl_info
    if hasattr(addon_module, 'bl_info'):
        bl_info = addon_module.bl_info
        print(f"✅ bl_info: {bl_info['name']} v{bl_info['version']}")
    else:
        print("❌ bl_info: MANQUANT")
    
    # Vérifier les propriétés
    if hasattr(bpy.context.scene, 'citygen_props'):
        print("✅ Propriétés: PRÉSENTES")
        props = bpy.context.scene.citygen_props
        print(f"   • Largeur: {props.width}")
        print(f"   • Longueur: {props.length}")
    else:
        print("❌ Propriétés: MANQUANTES")
    
    # Vérifier le panneau
    if hasattr(bpy.types, 'CITYGEN_PT_Panel'):
        print("✅ Panneau UI: ENREGISTRÉ")
    else:
        print("❌ Panneau UI: NON ENREGISTRÉ")
        
else:
    print(f"❌ Module {addon_name}: NON CHARGÉ")

print("=== FIN DIAGNOSTIC ===")
```

### Console de Debug
Pour voir les messages d'erreur:
```
Windows: Window > Toggle System Console
Mac: Terminal > Applications/Blender.app/Contents/MacOS/Blender
Linux: Lancez Blender depuis le terminal
```

---

## 🔧 **Problèmes Courants et Solutions**

### 1. "Module non trouvé"
**Cause**: Installation ZIP incorrecte
**Solution**: 
```
- Vérifiez que le ZIP contient le dossier city_block_generator/
- Ne pas extraire le ZIP avant installation
- Utiliser "Install" pas "Install from File"
```

### 2. "Propriétés manquantes"
**Cause**: Enregistrement incomplet
**Solution**:
```
1. Dans le panneau CityGen, cliquez "Diagnostic"
2. Puis "Réinitialiser Paramètres"
3. Si ça ne marche pas: redémarrez Blender
```

### 3. "Panneau invisible"
**Cause**: Cache Blender ou conflit
**Solution**:
```
1. Appuyez N pour afficher/masquer la sidebar
2. Vérifiez que vous êtes dans un espace 3D
3. Désactivez tous les autres addons temporairement
```

### 4. "Erreur persistent handler"
**Cause**: Version Blender incompatible ou cache
**Solution**:
```
1. Blender 4.0+ requis
2. Nettoyez le cache: %APPDATA%\Blender Foundation\
3. Installation Blender propre pour test
```

---

## 📋 **Informations Techniques**

### Version Corrigée: 6.21.1
**Corrections apportées:**
- ✅ Décorateur `@bpy.app.handlers.persistent` appliqué dynamiquement
- ✅ Import `bpy` ajouté dans tous les modules requis
- ✅ Gestion d'erreur robuste pour `bpy.data.scenes`
- ✅ Gestion de variable `init_citygen_props` corrigée
- ✅ Tests de compatibilité Blender 4.x

### Structure de l'Addon
```
city_block_generator_6_12/
├── __init__.py          # Module principal avec bl_info
├── operators.py         # 8 opérateurs + PropertyGroup
├── ui.py               # Panneau interface utilisateur
└── generator.py        # Logique de génération
```

### Classes Principales
- `CITYGEN_OT_Generate` - Génération quartier
- `CITYGEN_OT_ResetProperties` - Réinitialisation
- `CITYGEN_OT_Diagnostic` - Diagnostic intégré
- `CITYGEN_PT_Panel` - Interface utilisateur
- `CityGenProperties` - Propriétés de l'addon

---

## 🎉 **Test Final**

Une fois l'addon installé et activé:

1. **Nouveau fichier Blender** (File > New)
2. **Supprimez le cube** (X > Delete)
3. **Ouvrez la sidebar** (N)
4. **Onglet CityGen** (doit être visible)
5. **Paramètres**: Largeur=3, Longueur=3
6. **Cliquez "Générer Quartier"**
7. **Résultat**: Bâtiments verts + routes roses

Si cette séquence fonctionne : **🎯 Addon corrigé et fonctionnel !**

---

**💡 Support**: Si le problème persiste après ces étapes, il s'agit probablement d'un conflit avec votre installation Blender ou un autre addon.
