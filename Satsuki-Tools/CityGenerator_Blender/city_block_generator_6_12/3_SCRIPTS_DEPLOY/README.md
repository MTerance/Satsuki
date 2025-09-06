# 🚀 SCRIPTS DE DÉPLOIEMENT

## 📦 **Scripts d'Installation**

### 🎯 **Script Principal**
- `DEPLOY_ADDON_CLEAN_V6_14_0.py` - **RECOMMANDÉ** Déploie l'addon nettoyé

### 🔧 **Scripts Alternatifs**
- `FORCE_INSTALL_ROBUSTE_V6_13_7.py` - Installation robuste v6.13.7
- `FORCE_COURBES_VISIBLES_V6_13_7.py` - Patch courbes visibles
- `FORCE_INSTALL_V6_12_9.py` - Installation basique

### ⚙️ **Scripts Utilitaires**
- `*reload*.py` - Scripts de rechargement
- `*deploy*.py` - Scripts de déploiement legacy
- `*install*.py` - Scripts d'installation divers

### 🎯 **Processus Recommandé**

1. **Nettoyage**: L'addon a déjà été nettoyé
2. **Déploiement**: Exécuter `DEPLOY_ADDON_CLEAN_V6_14_0.py`
3. **Installation Blender**: 
   - Redémarrer Blender
   - Edit > Preferences > Add-ons
   - Supprimer ancien addon
   - Install > Sélectionner nouveau dossier
   - Activer addon

### 📊 **Destinations**
- **Addon Clean**: `C:\Users\sshom\Documents\assets\Tools\city_block_generator_6_14_clean`
- **Addon Legacy**: `C:\Users\sshom\Documents\assets\Tools\city_block_generator_6_12`

### ⚡ **Instructions**
```bash
cd 3_SCRIPTS_DEPLOY
python DEPLOY_ADDON_CLEAN_V6_14_0.py
```
