# 🚀 SCRIPTS DE DÉPLOIEMENT

## 📦 **Scripts d'Installation**

### 🎯 **Script Principal**
- `DEPLOY_ADDON_V6_14_1_CORRECTION_DIAGONALES.py` - **RECOMMANDÉ** v6.14.1 avec correction
- `deploy_v6_14_1_correction.ps1` - **PowerShell** v6.14.1 avec correction
- `DEPLOY_ADDON_CLEAN_V6_14_0.py` - Déploie l'addon nettoyé v6.14.0

### 🔧 **Scripts Alternatifs**
- `FORCE_INSTALL_ROBUSTE_V6_13_7.py` - Installation robuste v6.13.7
- `FORCE_COURBES_VISIBLES_V6_13_7.py` - Patch courbes visibles
- `FORCE_INSTALL_V6_12_9.py` - Installation basique

### ⚙️ **Scripts Utilitaires**
- `*reload*.py` - Scripts de rechargement
- `*deploy*.py` - Scripts de déploiement legacy
- `*install*.py` - Scripts d'installation divers

### 🎯 **Processus Recommandé V6.14.1**

1. **Correction Applied**: Routes diagonales éliminées
2. **Déploiement**: Exécuter `DEPLOY_ADDON_V6_14_1_CORRECTION_DIAGONALES.py`
3. **Installation Blender**: 
   - Redémarrer Blender
   - Edit > Preferences > Add-ons
   - Supprimer ancien addon
   - Install > Sélectionner nouveau dossier
   - Activer addon

### 📊 **Destinations V6.14.1**
- **Assets**: `C:\Users\sshom\Documents\assets\Tools\city_block_generator_6_14_1`
- **Blender**: `C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.5\scripts\addons\city_block_generator_6_14_1`
- **Addon Legacy**: `C:\Users\sshom\Documents\assets\Tools\city_block_generator_6_12`

### ⚡ **Instructions**
```bash
cd 3_SCRIPTS_DEPLOY
python DEPLOY_ADDON_CLEAN_V6_14_0.py
```
