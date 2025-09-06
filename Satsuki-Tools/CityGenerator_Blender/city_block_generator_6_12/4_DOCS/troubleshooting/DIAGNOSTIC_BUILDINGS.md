# 🔍 Guide de Diagnostic - Bâtiments Non Visibles

## 🎯 Version de Diagnostic Déployée (v7.0.3)

Cette version inclut des **logs détaillés** pour identifier exactement pourquoi les bâtiments ne sont pas visibles.

## 🚀 Procédure de Test

### Étape 1: Redémarrage Obligatoire
**IMPORTANT**: Redémarrez complètement Blender pour charger la nouvelle version avec les logs.

### Étape 2: Activer la Console
1. **Window > Toggle System Console** (pour voir les logs en temps réel)
2. Gardez cette console visible pendant le test

### Étape 3: Configuration de Test Simple
Dans le panneau CityGen, utilisez ces paramètres exacts :
```
Largeur: 2
Longueur: 2  
Étages max: 6
Mode quartiers: ✅ (doit être coché)
Type de district: RESIDENTIAL
```

### Étape 4: Génération avec Surveillance
1. Cliquez **"Générer Quartier"**
2. **OBSERVEZ LA CONSOLE** - vous devriez voir des messages détaillés

## 🔍 Messages à Surveiller

### Messages Normaux (Bonne Génération)
```
🏗️ DÉBUT génération bâtiment 1
   Paramètres: pos=(5.0,5.0), taille=(8.0x8.0x9.0)
   ➡️ Appel generate_rectangular_building...
🏢 DÉBUT generate_rectangular_building #1
   ➡️ Appel create_cube_with_center_bottom_origin...
   ✅ Cube créé: Cube
   📍 Position: (5.0, 5.0, 0.0)
   🏷️ Nom assigné: batiment_rectangular_1
   🎨 Matériau appliqué: BuildingMat
✅ generate_rectangular_building #1 TERMINÉ avec succès
✅ Bâtiment 1 créé avec succès: batiment_rectangular_1
```

### Messages d'Erreur à Identifier
```
❌ ERREUR: Paramètres de bâtiment invalides: w=0, d=0, h=0
❌ ERREUR: Matériau invalide pour le bâtiment
❌ Échec de création du cube pour le bâtiment
❌ ÉCHEC: Bâtiment X - Objet None retourné
```

## 🛠️ Diagnostic Selon les Messages

### Cas 1: "Paramètres invalides"
**Problème**: Hauteur = 0 ou dimensions = 0
**Solution**: 
- Vérifier que "Étages max" > 0
- Vérifier que "Mode quartiers" est activé

### Cas 2: "Matériau invalide"  
**Problème**: Matériaux non créés
**Solution**:
- Cliquer "Mettre à jour Couleurs"
- Redémarrer Blender

### Cas 3: "Échec de création du cube"
**Problème**: Problème avec l'API Blender
**Solution**:
- Vérifier que vous êtes en mode Object
- Aucun objet sélectionné en mode Edit

### Cas 4: Bâtiments créés mais invisibles
**Signes**: Messages de succès mais rien visible
**Vérifications**:
1. **Outliner**: Chercher objets nommés "batiment_rectangular_X"
2. **View Layers**: Vérifier que les objets ne sont pas masqués
3. **Collections**: Vérifier la visibilité des collections

## 🔧 Actions de Dépannage

### Si Aucun Message de Bâtiment
1. **Mode quartiers non activé** → Cocher la case
2. **max_floors = 0** → Mettre à 4-8
3. **Grille trop petite** → Essayer 3x3

### Si Messages d'Erreur Matériau
1. Cliquer **"Mettre à jour Couleurs"**
2. Si échec: **"Rechargement Complet"**
3. Si échec: Redémarrer Blender

### Si Messages de Succès mais Pas de Bâtiments
1. **Vérifier l'Outliner** (chercher "batiment_")
2. **Changer la vue** (Numpad 7 pour vue dessus)
3. **Zoom Out** (molette souris)
4. **Vérifier les layers** (touche ~ ou collection visibility)

## 📊 Informations Additionnelles Logs

Les nouveaux logs montrent aussi :
- **Position exacte** de chaque bâtiment
- **Échelle finale** appliquée  
- **État de visibilité** (viewport/render)
- **Collections** utilisées
- **Validation des mesh** données

## 🆘 Si le Problème Persiste

Après le test avec les logs, si le problème persiste :

1. **Copier les messages de la console** 
2. **Noter la configuration exacte** utilisée
3. **Vérifier l'Outliner** pour les objets "batiment_"
4. **Tester une vue différente** (caméra, perspective)

## 💡 Test Rapide Manuel

Dans la console Python de Blender, testez :
```python
# Vérifier les objets créés
objects = [obj for obj in bpy.context.scene.objects if 'batiment' in obj.name]
print(f"Bâtiments trouvés: {len(objects)}")
for obj in objects:
    print(f"- {obj.name}: pos={obj.location}, visible={not obj.hide_viewport}")
```

Cette version de diagnostic devrait nous dire exactement où est le problème dans la chaîne de génération des bâtiments !
