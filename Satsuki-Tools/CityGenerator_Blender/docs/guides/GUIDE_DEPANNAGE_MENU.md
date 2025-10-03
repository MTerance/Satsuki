# GUIDE DÉPANNAGE - Menu Non Accessible v6.20.2

## 🔍 DIAGNOSTIC COMPLET

Le menu City Block Generator peut ne pas être accessible pour plusieurs raisons. Voici la procédure de diagnostic et résolution.

## 🛠️ ÉTAPES DE RÉSOLUTION

### Étape 1 : Vérification Basique

1. **Ouvrir le panneau latéral :**
   - Appuyez sur la touche `N` dans la vue 3D
   - L'onglet `CityGen` devrait apparaître à droite

2. **Si l'onglet CityGen n'apparaît pas :**
   - Faites un clic droit sur les onglets du panneau
   - Vérifiez si "CityGen" est dans la liste

### Étape 2 : Diagnostic avec Script

1. **Ouvrir l'éditeur de texte dans Blender**
2. **Coller ce script de diagnostic :**

```python
import bpy

print("=== DIAGNOSTIC CITY BLOCK GENERATOR ===")

# Vérifier si l'addon est activé
addon_found = False
for addon in bpy.context.preferences.addons:
    if "city_block" in addon.module.lower():
        print(f"✅ Addon trouvé: {addon.module}")
        addon_found = True
        break

if not addon_found:
    print("❌ Addon non trouvé ou non activé")

# Vérifier les classes enregistrées
if hasattr(bpy.types, 'CITYGEN_PT_Panel'):
    print("✅ Panneau UI enregistré")
else:
    print("❌ Panneau UI non enregistré")

# Vérifier les propriétés
if hasattr(bpy.context.scene, 'citygen_props'):
    print("✅ Propriétés disponibles")
else:
    print("❌ Propriétés non disponibles")

# Tenter de réinitialiser les propriétés
try:
    bpy.ops.citygen.reset_properties()
    print("✅ Propriétés réinitialisées")
except:
    print("❌ Impossible de réinitialiser les propriétés")

print("=== FIN DIAGNOSTIC ===")
```

3. **Exécuter le script** (bouton Run)
4. **Vérifier les résultats** dans la console

### Étape 3 : Solutions par Problème

#### Si "Addon non trouvé ou non activé"
1. Aller dans `Edit > Preferences > Add-ons`
2. Rechercher "City Block Generator"
3. Si trouvé : Cocher la case pour l'activer
4. Si non trouvé : Cliquer "Install" et sélectionner le ZIP

#### Si "Panneau UI non enregistré"
1. Désactiver l'addon dans Preferences
2. Redémarrer Blender complètement
3. Réactiver l'addon
4. Ou réinstaller le ZIP version 6.20.2

#### Si "Propriétés non disponibles"
1. Dans la vue 3D, appuyer `N` pour ouvrir le panneau
2. Chercher l'onglet "CityGen"
3. Cliquer "Initialiser les propriétés" si visible
4. Ou exécuter dans la console : `bpy.ops.citygen.reset_properties()`

### Étape 4 : Réinstallation Complète

Si rien ne fonctionne :

1. **Supprimer l'ancien addon :**
   - Edit > Preferences > Add-ons
   - Rechercher "City Block"
   - Cliquer sur la flèche puis "Remove"

2. **Redémarrer Blender**

3. **Installer la nouvelle version :**
   - Edit > Preferences > Add-ons > Install
   - Sélectionner `city_block_generator.zip` (dernière version)
   - Activer l'addon

4. **Forcer l'initialisation :**
   ```python
   # Dans la console Python de Blender
   import bpy
   bpy.ops.citygen.reset_properties()
   ```

### Étape 5 : Test de Fonctionnement

1. **Ouvrir le panneau :** Touche `N` en vue 3D
2. **Chercher l'onglet :** "CityGen" 
3. **Vérifier les paramètres :**
   - Largeur, Longueur doivent être modifiables
   - Tous les sliders doivent fonctionner
4. **Test de génération :**
   - Modifier un paramètre (ex: Largeur = 3)
   - Cliquer "Générer Quartier"
   - Vérifier qu'une grille 3x3 est créée

## 🎯 EMPLACEMENTS DU PANNEAU

Le panneau City Block Generator devrait apparaître :

- **Espace :** Vue 3D (3D Viewport)
- **Région :** Panneau latéral (Sidebar)
- **Onglet :** CityGen
- **Accès :** Touche `N` ou View > Sidebar

## 📋 VALEURS DE TEST

Pour vérifier que l'interface fonctionne :

```
Paramètres de test :
- Largeur: 3
- Longueur: 4  
- Étages max: 6
- Largeur routes: 3.0
- Mode quartiers: Activé ✓
- Commercial: 0.4
```

## 🚨 PROBLÈMES CONNUS

### Interface figée
- **Solution :** Redémarrer Blender
- **Prévention :** Sauvegarder avant modifications

### Propriétés vides
- **Solution :** Cliquer "Réinitialiser Paramètres"
- **Prévention :** Ne pas modifier les fichiers de l'addon

### Onglet CityGen invisible
- **Solution :** Réinstaller l'addon complètement
- **Vérification :** Script de diagnostic ci-dessus

## ✅ CRITÈRES DE SUCCÈS

Le menu est accessible quand :
- ✅ L'onglet "CityGen" est visible dans le panneau latéral
- ✅ Tous les paramètres sont modifiables (champs non grisés)
- ✅ Le bouton "Générer Quartier" est cliquable
- ✅ Les sliders des ratios fonctionnent (si mode quartiers activé)
- ✅ Aucun message d'erreur dans la console

Si tous ces critères sont remplis, l'addon est correctement installé et fonctionnel !
