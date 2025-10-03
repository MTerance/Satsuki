# 🚀 Scripts de Déploiement - City Block Generator v7.0.0

Ce dossier contient plusieurs méthodes pour déployer automatiquement l'addon City Block Generator vers votre installation Blender.

## 📁 Fichiers de Déploiement

### 🎯 **deploy_addon.bat** (Recommandé pour Windows)
```batch
# Double-cliquez pour lancer le déploiement automatique
# Copie tous les fichiers Python vers Blender 4.5
```

### ⚡ **deploy_addon.ps1** (PowerShell avancé)
```powershell
# Script PowerShell avec options avancées
# Usage:
.\deploy_addon.ps1                    # Déploiement standard
.\deploy_addon.ps1 -Backup           # Avec sauvegarde
.\deploy_addon.ps1 -Force             # Forcer l'écrasement
```

### 🐍 **deploy_addon.py** (Python universel)
```python
# Script Python multi-plateforme
python deploy_addon.py
```

### 🔄 **Bouton "Déployer Addon"** (Depuis Blender)
- Disponible dans l'interface de l'addon
- Copie automatiquement depuis l'addon actuel
- Idéal pour les mises à jour rapides

## 🎯 Chemins de Déploiement

**Source :**
```
C:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator
```

**Destination :**
```
C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.5\scripts\addons\city_block_generator
```

## 📋 Fichiers Copiés

Les scripts copient automatiquement :
- ✅ `__init__.py` - Configuration principale
- ✅ `generator.py` - Logique de génération de ville
- ✅ `operators.py` - Opérateurs Blender et propriétés
- ✅ `ui.py` - Interface utilisateur
- ✅ `reload_addon.py` - Utilitaire de rechargement

## 🔄 Workflow de Développement

### 1. **Modification du Code**
- Éditez les fichiers Python dans le répertoire source
- Testez vos modifications

### 2. **Déploiement**
- **Option A :** Double-cliquez sur `deploy_addon.bat`
- **Option B :** Utilisez le bouton "Déployer Addon" dans Blender
- **Option C :** Exécutez le script PowerShell/Python

### 3. **Activation des Changements**
- Dans Blender, utilisez "Rechargement Rapide" ou "Rechargement Complet"
- L'addon sera mis à jour avec vos modifications

## 🛠️ Fonctionnalités des Scripts

### ✅ **Vérifications de Sécurité**
- Vérification de l'existence des fichiers source
- Création automatique du répertoire de destination
- Validation des tailles de fichiers après copie

### 💾 **Sauvegarde Automatique**
- Option de sauvegarde de l'addon existant
- Horodatage des sauvegardes
- Protection contre la perte de données

### 📊 **Rapport Détaillé**
- Statistiques de copie (réussies/échouées)
- Messages d'erreur détaillés
- Instructions post-déploiement

### 🎨 **Interface Colorée**
- Codes couleur pour le statut (✅ ❌ ⚠️)
- Messages structurés et lisibles
- Feedback en temps réel

## 🔧 Dépannage

### **Erreur de Permissions**
```powershell
# Exécuter PowerShell en tant qu'administrateur
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### **Répertoire de Destination Introuvable**
- Vérifiez que Blender 4.5 est installé
- Créez manuellement le dossier si nécessaire

### **Fichiers Non Copiés**
- Vérifiez les permissions en écriture
- Fermez Blender pendant le déploiement
- Utilisez l'option `-Force` si nécessaire

## 🎯 Avantages du Système

### 🚀 **Développement Rapide**
- Déploiement en un clic
- Pas de manipulation manuelle de fichiers
- Workflow automatisé

### 🔒 **Sécurisé**
- Sauvegardes automatiques
- Vérifications d'intégrité
- Gestion d'erreurs robuste

### 📈 **Évolutif**
- Scripts facilement modifiables
- Support de versions multiples de Blender
- Extensible pour d'autres addons

## 📞 Support

En cas de problème :
1. Vérifiez les chemins dans les scripts
2. Consultez les logs d'erreur détaillés
3. Utilisez l'option de sauvegarde avant déploiement
4. Testez avec le mode administrateur si nécessaire

---

**Version :** 7.0.0  
**Dernière mise à jour :** Septembre 2025  
**Compatibilité :** Blender 4.0+, Windows 10/11
