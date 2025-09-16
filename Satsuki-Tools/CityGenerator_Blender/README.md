# City Block Generator - Scripts de Packaging

Ce dossier contient plusieurs scripts pour packager automatiquement l'addon Blender "City Block Generator".

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
   - Créer un nouveau `city_block_generator_6_12.zip`
   - Afficher les instructions d'installation

## 📦 Installation dans Blender

1. Ouvrez Blender
2. `Edit > Preferences > Add-ons`
3. Cliquez `Install...`
4. Sélectionnez `city_block_generator_6_12.zip`
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
city_block_generator_6_12/
├── __init__.py          # Point d'entrée de l'addon
├── operators.py         # Opérateurs Blender (génération, etc.)
├── ui.py               # Interface utilisateur (panneau CityGen)
└── generator.py        # Logique de génération des quartiers
```

## 🛠️ Développement

Pour modifier l'addon :
1. Éditez les fichiers dans `city_block_generator_6_12/`
2. Relancez un script de packaging
3. Réinstallez dans Blender

## 📞 Support

Si l'addon ne fonctionne pas :
1. Vérifiez que Blender est en mode "Object"
2. Utilisez le bouton "Réinitialiser Paramètres" si l'interface est vide
3. Consultez la console Blender (Window > Toggle System Console) pour les erreurs

---
*City Block Generator v6.12.7 - Générateur de quartiers urbains procéduraux pour Blender*
