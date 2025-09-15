# GUIDE DE TEST PRATIQUE TOKYO SIMPLE V2.1

## 🎯 VALIDATION COMPLÈTE DANS BLENDER

### ÉTAPE 1: INSTALLATION
```
1. Ouvrir Blender 4.0+
2. Edit → Preferences → Add-ons
3. Install... → tokyo_simple_v2_1.zip
4. Activer "Tokyo City Generator v2.1 SIMPLE"
5. Sidebar (N) → Onglet "Tokyo"
```

### ÉTAPE 2: INTERFACE - VALIDATION
- ✅ **1 seul panneau** "Tokyo City Generator"
- ✅ **4 paramètres** visibles et clairs:
  - City Size (3-10)
  - Building Style (Low/Mixed/High) 
  - Density (slider)
  - Better Materials (checkbox)
- ✅ **2 boutons** bien visibles:
  - 🏗️ "Generate Tokyo City" (gros bouton)
  - 🗑️ "Clear City"

### ÉTAPE 3: TEST GÉNÉRATION RAPIDE
**Paramètres test**:
- City Size: **5**
- Building Style: **Mixed**
- Density: **70%**
- Better Materials: **ON**

**Cliquer "Generate Tokyo City"**

**Vérifications attendues**:
1. ⏱️ **Génération < 5 secondes**
2. 🛣️ **Routes grises** en grille régulière
3. 🏢 **Bâtiments variés** (hauteurs différentes)
4. 🚫 **Pas de chevauchement** routes/bâtiments
5. 🎨 **Couleurs variées** (pas uniformes)
6. ✅ **Message succès** "Tokyo city generated!"

### ÉTAPE 4: TEST VARIÉTÉ
**Regénérer 3 fois** avec mêmes paramètres:
- Cliquer "Generate" → Observer
- Cliquer "Generate" → Observer  
- Cliquer "Generate" → Observer

**Vérifications**:
- 🎲 **Positions différentes** des bâtiments
- 📏 **Hauteurs variées** à chaque fois
- 🌈 **Couleurs changeantes**
- 🏙️ **Aspect "vivant"** non-répétitif

### ÉTAPE 5: TEST STYLES
**Test Low Rise**:
- Building Style: **Low**
- Generate → **Bâtiments bas** (maisons)

**Test High Rise**:
- Building Style: **High** 
- Generate → **Gratte-ciels** + effet fenêtres

### ÉTAPE 6: TEST NETTOYAGE
- Cliquer **"Clear City"**
- ✅ **Tous objets Tokyo** disparaissent
- ✅ **Message confirmation** affiché
- ✅ **Scène propre** prête pour nouveau test

---

## 🚨 PROBLÈMES POSSIBLES

### Si l'addon ne s'installe pas:
- Vérifier Blender 4.0+
- ZIP bien téléchargé (6.4KB)
- Redémarrer Blender

### Si erreurs à la génération:
- Vérifier console Blender (Window → Toggle System Console)
- Noter les messages d'erreur Python
- Tester avec paramètres minimums (City Size: 3)

### Si bâtiments sur routes:
- BUG confirmé - Noter les paramètres utilisés
- Tester différentes tailles de ville

---

## ✅ CRITÈRES DE SUCCÈS

**Interface**: Simple, 4 paramètres, 2 boutons
**Performance**: Génération < 5 secondes  
**Qualité**: Routes séparées, bâtiments variés
**Stabilité**: Pas d'erreur, nettoyage fonctionne
**Expérience**: "Enfin quelque chose qui marche!"

---

**OBJECTIF**: Prouver que Tokyo v2.1 Simple est l'opposé total de v2.0 "impossible à utiliser"