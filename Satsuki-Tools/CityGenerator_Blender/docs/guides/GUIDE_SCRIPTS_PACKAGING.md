# SCRIPTS DE PACKAGING -Dossier source trouve: city_block_generator
📋 Version detectee: v6.20.4
Suppression de l'ancien fichier: city_block_generator.zipty Block Generator v6.20.4

## 📦 SCRIPTS DISPONIBLES

Tous les scripts lisent automatiquement la version depuis `city_block_generator/__init__.py` et l'affichent correctement dans les logs.

### 1. `package_addon.ps1` (RECOMMANDÉ)
**Script PowerShell complet avec toutes les fonctionnalités**

```powershell
.\package_addon.ps1
```

**Fonctionnalités :**
- ✅ Lecture automatique de la version depuis `__init__.py`
- ✅ Suppression de l'ancien ZIP avec gestion d'erreurs
- ✅ Compression optimisée avec Compress-Archive
- ✅ Affichage détaillé des informations (taille, date)
- ✅ Messages colorés et informatifs
- ✅ Gestion complète des erreurs

**Sortie typique :**
```
=== PACKAGING CITY BLOCK GENERATOR ADDON ===
Dossier source trouve: city_block_generator
Version detectee: 6.20.4
Suppression de l'ancien fichier: city_block_generator.zip
   Ancien ZIP supprime avec succes
Creation du nouveau package...
SUCCES! Package cree: city_block_generator.zip
   Taille du fichier: 0.02 MB
   Cree le: 09/04/2025 01:06:39
PRET POUR L'INSTALLATION:
   5. Version: 6.20.4
```

### 2. `package_addon_advanced.bat`
**Script Batch avancé avec lecture de version**

```batch
.\package_addon_advanced.bat
```

**Fonctionnalités :**
- ✅ Lecture automatique de la version depuis `__init__.py`
- ✅ Interface utilisateur claire
- ✅ Suppression sécurisée de l'ancien ZIP
- ✅ Pause à la fin pour lecture des résultats

**Sortie typique :**
```
===============================================
    CITY BLOCK GENERATOR - PACKAGING TOOL
===============================================
[INFO] Lecture de la version depuis city_block_generator\__init__.py...
[OK] Version detectee: 6.20.4
[SUCCES] Package cree avec succes !
5. Version installee: 6.20.4
```

### 3. `package_addon_simple.bat`
**Script Batch basique (version corrigée)**

```batch
.\package_addon_simple.bat
```

**Fonctionnalités :**
- ✅ Création de ZIP simple
- ✅ Message informatif sur la version
- ✅ Instructions d'installation

### 4. Autres scripts disponibles
- `package_addon.sh` (Linux/macOS)
- `package_addon.bat` (version basique)
- `package_addon.cmd` (alias de .bat)

## 🎯 UTILISATION RECOMMANDÉE

### Pour Windows PowerShell :
```powershell
cd "C:\path\to\Tools"
.\package_addon.ps1
```

### Pour Windows Command Prompt :
```batch
cd "C:\path\to\Tools"
.\package_addon_advanced.bat
```

### Pour Linux/macOS :
```bash
cd "/path/to/Tools"
chmod +x package_addon.sh
./package_addon.sh
```

## 📊 VERSIONS SUPPORTÉES

Tous les scripts lisent la version depuis :
```python
# Dans city_block_generator/__init__.py
bl_info = {
    "version": (6, 20, 4),  # ← Version lue automatiquement
}
```

**Format de sortie :** `6.20.4`

## 🔧 FONCTIONNEMENT TECHNIQUE

### Lecture de Version
1. **PowerShell** : Regex `"version":\s*\((\d+),\s*(\d+),\s*(\d+)\)`
2. **Batch** : `findstr "version.*(" __init__.py`

### Compression
- **Méthode :** PowerShell `Compress-Archive`
- **Niveau :** Optimal
- **Format :** ZIP standard compatible Blender

### Gestion d'Erreurs
- Vérification existence dossier source
- Suppression sécurisée ancien ZIP
- Messages d'erreur détaillés
- Codes de sortie appropriés

## 📋 CHECKLIST AVANT PACKAGING

1. **Vérifier la version dans `__init__.py`**
2. **Sauvegarder les modifications**
3. **Fermer Blender** (pour éviter les conflits de fichiers)
4. **Exécuter le script** de packaging
5. **Vérifier le ZIP créé** (taille ~0.02 MB)

## 🚀 APRÈS PACKAGING

Le fichier `city_block_generator.zip` est prêt pour :
1. **Installation dans Blender**
2. **Distribution**
3. **Tests sur d'autres machines**

**Tous les scripts affichent maintenant la version correcte !** ✅
