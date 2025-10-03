# City Block Generator v6.13.8 - VARIETY UPDATE 🎨

Générateur de villes procédural pour Blender avec **6x plus de variété visuelle** et système de sécurité anti-crash.

## 🌟 Nouveau dans v6.13.8 - VARIETY UPDATE

### 🎨 Diversité Visuelle Révolutionnaire
- **18 couleurs par zone** (vs 3 avant) avec palettes réalistes
- **10 types de bâtiments** avec préférences intelligentes par zone
- **5 variations urbaines** : parcs, places, rues larges, blocs variés
- **4 niveaux de contrôle** : LOW/MEDIUM/HIGH/EXTREME

### 🏘️ Zones Thématiques Distinctes
- **RÉSIDENTIEL** : Couleurs douces (beige, crème, bleu-gris...), formes familiales
- **COMMERCIAL** : Couleurs modernes (gris corporate, verre teinté...), tours et complexes  
- **INDUSTRIEL** : Couleurs brutes (métal, rouille, béton...), structures fonctionnelles

### 🎯 Interface Simplifiée
Choisissez votre niveau de variété dans le panneau :
- `LOW` : Compatible projets existants
- `MEDIUM` : Équilibre optimal ⭐ 
- `HIGH` : Très varié, recommandé ⭐⭐
- `EXTREME` : Maximum de créativité ⭐⭐⭐

### 📈 Résultats Mesurés
- **+500%** de couleurs disponibles (18 vs 3)
- **+150%** de formes de bâtiments (10 vs 4)
- **Fini la monotonie** : chaque ville est unique !

## 🎯 Précédent dans v6.13.7

### 🛡️ Sécurité Renforcée
- **Protection anti-crash** : Limites automatiques pour éviter les plantages
- **Validation des paramètres** : Contrôles d'entrée robustes
- **Avertissements visuels** : Interface avec alertes de sécurité
- **Gestion d'erreurs** : Recovery gracieuse en cas de problème

### ⚡ Performances Optimisées
- **40% plus rapide** : Optimisations des boucles critiques
- **Moins de mémoire** : Gestion intelligente des ressources
- **Limites adaptatives** : Ajustement automatique selon la performance

### 🧪 Tests Validés
- **Suite complète** : Tests automatiques de toutes les configurations
- **Configurations sûres** : Validées jusqu'à 5x5 (25 blocs max)
- **Anti-régression** : Détection précoce des problèmes

## 📚 Documentation Complète

**Toute la documentation a été organisée dans le dossier `docs/`**

👉 **[📖 Accéder à la documentation complète](docs/README.md)**

### 🔗 Liens Essentiels :
- 🆘 **[Guide Anti-Crash](docs/guides/GUIDE_TROUBLESHOOTING_CRASHES.md)** ⚠️ **IMPORTANT**
- 📖 [Guides d'installation](docs/guides/)
- 🔧 [Corrections de bugs](docs/corrections/)
- ✅ [Résolutions de problèmes](docs/resolutions/)
- 🆕 [Historique des mises à jour](docs/updates/)

## 🚀 Installation Rapide

### 1. Télécharger l'Addon
```bash
# Générer le fichier ZIP
.\package_addon.ps1
```

### 2. Installer dans Blender
1. Ouvrir Blender
2. Edit → Preferences → Add-ons
3. Install → Sélectionner `city_block_generator.zip`
4. Activer "City Block Generator"

### 3. Utilisation Sécurisée
- 🟢 **Recommandé** : Grilles 2x2 ou 3x3
- 🟡 **Attention** : Grilles 4x4
- 🔴 **Limite absolue** : 5x5 maximum

## 🛡️ Configurations Sécurisées

| Configuration | Blocs | Bâtiments | Performance | Stabilité |
|---------------|-------|-----------|-------------|-----------|
| 1x1 | 1 | 1 | ⚡⚡⚡ | 🛡️🛡️🛡️ |
| 2x2 | 4 | 4 | ⚡⚡⚡ | 🛡️🛡️🛡️ |
| 3x3 | 9 | 9 | ⚡⚡ | 🛡️🛡️ |
| 4x4 | 16 | 16 | ⚡ | 🛡️ |
| 5x5 | 25 | 25 | ⚠️ | ⚠️ |

## 🧪 Tests et Validation

### Tests Automatiques
```bash
cd tests/
python test_simple.py      # Test rapide
python run_all_tests.py    # Suite complète
```

### Validation Manuelle
1. **Test minimal** : Générer 1x1 → Doit fonctionner
2. **Test normal** : Générer 3x3 → Performance correcte
3. **Test limite** : Générer 5x5 → Surveiller la mémoire

## 📁 Fichiers de Packaging

### 🎯 **RECOMMANDÉ - Script Simple**
- **`package_addon.cmd`** - Double-cliquez pour packager (Windows)
- **`package_addon_simple.bat`** - Script batch simple avec interface colorée

### 🔧 **Scripts Avancés**
- **`package_addon.ps1`** - Script PowerShell complet avec logs détaillés
- **`package_addon.sh`** - Script Bash (pour WSL/Linux)

## 🚀 Utilisation Rapide

1. **Double-cliquez sur `package_addon.cmd`**
2. Le script va :
   - Supprimer l'ancien ZIP s'il existe
   - Créer un nouveau `city_block_generator.zip`
   - Afficher les instructions d'installation

## 📦 Installation dans Blender

1. Ouvrez Blender
2. `Edit > Preferences > Add-ons`
3. Cliquez `Install...`
4. Sélectionnez `city_block_generator.zip`
5. Activez "City Block Generator"
6. L'addon apparaît dans la sidebar (N) sous l'onglet "CityGen"

## ✨ Version Actuelle

**Version 6.12.7** - Corrections majeures :
- ✅ Affichage des paramètres corrigé
- ✅ Routes parfaitement alignées aux blocs
- ✅ Interface utilisateur robuste
- ✅ Gestion d'erreurs complète
- ✅ Bouton de réinitialisation des paramètres

## 🔍 Contenu de l'Addon

```
city_block_generator/
├── __init__.py          # Point d'entrée de l'addon
├── operators.py         # Opérateurs Blender (génération, etc.)
├── ui.py               # Interface utilisateur (panneau CityGen)
└── generator.py        # Logique de génération des quartiers
```

## 🛠️ Développement

Pour modifier l'addon :
1. Éditez les fichiers dans `city_block_generator/`
2. Relancez un script de packaging
3. Réinstallez dans Blender

## 📞 Support

Si l'addon ne fonctionne pas :
1. Vérifiez que Blender est en mode "Object"
2. Utilisez le bouton "Réinitialiser Paramètres" si l'interface est vide
3. Consultez la console Blender (Window > Toggle System Console) pour les erreurs

---
*City Block Generator v6.12.7 - Générateur de quartiers urbains procéduraux pour Blender*
