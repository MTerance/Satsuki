# 🔧 GUIDE RÉSOLUTION - TEXTURES TOKYO NE S'APPLIQUENT PAS

## 🎯 PROBLÈMES POSSIBLES ET SOLUTIONS

### 1️⃣ **PROBLÈME: Option "Advanced Textures" désactivée**

**Symptômes**:
- Les bâtiments ont des couleurs unies (gris, bleu, rouge)
- Pas de textures détaillées
- Interface Tokyo visible mais pas de chemin texture

**Solution**:
```
1. Vue 3D > Sidebar (N) > Onglet Tokyo
2. ✅ Cocher "Advanced Textures"
3. Le champ "Texture Base Path" apparaît
4. Générer un nouveau district
```

### 2️⃣ **PROBLÈME: Dossiers de textures manquants**

**Symptômes**:
- Advanced Textures coché mais matériaux basiques appliqués
- Messages d'erreur dans la console Blender
- Chemin texture configuré mais dossiers vides

**Solution**:
```python
# Dans Blender Text Editor:
exec(open('setup_textures.py').read())
```

**Ou créer manuellement**:
```
C:/Users/sshom/Documents/assets/Tools/tokyo_textures/
├── skyscrapers/
│   ├── glass_towers/
│   ├── modern_office/
│   └── metallic_facades/
├── commercial/
│   ├── shopping_centers/
│   └── retail_facades/
├── residential/
│   ├── apartment_blocks/
│   └── traditional_housing/
└── etc...
```

### 3️⃣ **PROBLÈME: Fichiers texture manquants**

**Symptômes**:
- Dossiers créés mais matériaux procéduraux appliqués
- Pas d'images dans les dossiers

**Solution**:
1. Télécharger des textures (formats: .jpg, .png, .exr, .hdr)
2. Les placer dans les dossiers appropriés
3. Noms recommandés: facade01.jpg, building_wall.png, etc.

### 4️⃣ **PROBLÈME: Mode d'affichage Blender incorrect**

**Symptômes**:
- Textures appliquées mais invisibles
- Vue 3D en mode Solid ou Wireframe

**Solution**:
```
Vue 3D > Mode d'affichage > Material Preview (icône sphère)
Ou
Vue 3D > Mode d'affichage > Rendered (icône sphère blanche)
```

### 5️⃣ **PROBLÈME: Chemin texture incorrect**

**Symptômes**:
- Interface Tokyo avec chemin affiché
- Erreurs "dossier non trouvé" dans console

**Solution**:
1. Vérifier le chemin dans l'interface Tokyo
2. Corriger vers un dossier existant
3. Utiliser des barres obliques (/) même sur Windows

### 6️⃣ **PROBLÈME: Module texture_system non chargé**

**Symptômes**:
- Advanced Textures coché mais pas d'effet
- Erreur import dans la console

**Solution**:
1. Redémarrer Blender
2. Réinstaller l'addon depuis le ZIP
3. Vérifier que tous les fichiers sont présents

## 🧪 TESTS DE DIAGNOSTIC

### Test 1: Vérification basic
```python
# Dans Blender Console/Text Editor:
exec(open('diagnostic_textures.py').read())
```

### Test 2: Test visuel simple
```python
# Dans Blender Console/Text Editor:
exec(open('test_textures_simple.py').read())
```

### Test 3: Vérification manuelle
1. Générer un district Tokyo
2. Sélectionner un bâtiment
3. Material Properties > Vérifier les matériaux
4. Shader Editor > Voir les nœuds de texture

## 🎯 SOLUTION RAPIDE ÉTAPE PAR ÉTAPE

### **MÉTHODE RAPIDE** (5 minutes):

1. **Activer Advanced Textures**:
   - Vue 3D > N > Tokyo
   - ✅ Cocher "Advanced Textures"

2. **Créer dossiers automatiquement**:
   ```python
   exec(open('setup_textures.py').read())
   ```

3. **Générer district test**:
   - Grid Size: 3x3
   - District Type: Business
   - Cliquer "Generate Tokyo District"

4. **Mode d'affichage**:
   - Vue 3D > Material Preview

5. **Si toujours pas visible**:
   - Sélectionner un bâtiment
   - Material Properties > Ajouter matériau manuellement

### **MÉTHODE COMPLÈTE** (15 minutes):

1. **Diagnostic complet**:
   ```python
   exec(open('diagnostic_textures.py').read())
   ```

2. **Corriger selon résultats**

3. **Ajouter vraies textures** (optionnel):
   - Télécharger textures de bâtiments
   - Les placer dans les dossiers créés

4. **Test final**:
   ```python
   exec(open('test_textures_simple.py').read())
   ```

## 📊 VÉRIFICATIONS FINALES

### ✅ Checklist réussite:
- [ ] Advanced Textures coché
- [ ] Chemin texture visible et correct
- [ ] Dossiers textures créés
- [ ] Mode Material Preview actif
- [ ] Matériaux avec nœuds texture visibles
- [ ] Bâtiments avec textures détaillées

### ❌ Si toujours en échec:
1. Redémarrer Blender
2. Réinstaller addon depuis ZIP corrigé
3. Vérifier version Blender (4.0+ requis)
4. Utiliser le mode Rendered pour forcer l'affichage

---
*Guide pour Tokyo City Generator v1.4.0*
*Si problème persiste: utiliser diagnostic_textures.py*
