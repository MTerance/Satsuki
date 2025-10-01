# Guide de packaging - JP Building Generator

Ce dossier contient plusieurs scripts pour créer facilement un package ZIP de l'addon jp_buildgen, prêt à être installé dans Blender.

## Scripts disponibles

### 1. `package_simple.bat` ⭐ **Recommandé pour utilisation rapide** ✅ CORRIGÉ
Script batch simple et rapide.

**Utilisation :**
```bash
double-clic sur package_simple.bat
```

**Fonctionnalités :**
- Crée `jp_buildgen_v0.1.3.zip` avec la **structure correcte**
- Inclut tous les fichiers essentiels et textures dans le dossier `jp_buildgen/`
- Interface simple
- **RÉSOUT** l'erreur "ZIP packaged incorrectly"

### 2. `package_addon.bat` ✅ FONCTIONNE CORRECTEMENT
Script batch complet avec interface détaillée.

**Utilisation :**
```bash
double-clic sur package_addon.bat
```

**Fonctionnalités :**
- Création dans un répertoire temporaire propre
- Structure ZIP correcte dès le départ
- Exclusion automatique des fichiers non nécessaires
- Interface utilisateur détaillée avec messages de statut
- Instructions d'installation incluses

### 3. `package_addon.ps1` 🚀 **Le plus flexible**
Script PowerShell avancé avec options.

**Utilisation basique :**
```powershell
.\package_addon.ps1
```

**Utilisation avancée :**
```powershell
# Spécifier une version
.\package_addon.ps1 -Version "0.1.4"

# Inclure la documentation
.\package_addon.ps1 -IncludeDocs

# Spécifier un répertoire de sortie
.\package_addon.ps1 -OutputDir "C:\Packages"

# Combinaison d'options
.\package_addon.ps1 -Version "0.1.4" -IncludeDocs -OutputDir ".\releases"
```

**Fonctionnalités :**
- Interface colorée et détaillée
- Options de ligne de commande
- Vérification de l'existence des fichiers
- Gestion d'erreurs avancée
- Nettoyage automatique

## Fichiers inclus dans le package

### Fichiers essentiels (toujours inclus)
- `__init__.py` - Point d'entrée de l'addon
- `core.py` - Logique principale de génération
- `operators.py` - Opérateurs Blender 
- `panels.py` - Interface utilisateur
- `properties.py` - Propriétés et paramètres

### Dossier textures (toujours inclus)
- `textures/` - Toutes les textures par catégorie
  - `office/`, `mall/`, `restaurant/`, `konbini/`, `apartment/`, `house/`

### Documentation (optionnelle)
- `README.md` - Guide d'utilisation
- `CORRECTION_FLOTTEMENT.md` - Documentation des corrections (exclu par défaut)

## Installation dans Blender

1. **Ouvrir Blender**
2. **Aller dans Edit > Preferences > Add-ons**
3. **Cliquer sur "Install..."**
4. **Sélectionner le fichier ZIP créé**
5. **Activer l'addon "JP Building Generator"**
6. **L'interface apparaît dans View3D > Sidebar > JPBuild**

## Résolution de problèmes

### Erreur "PowerShell n'est pas reconnu"
- Utiliser `package_simple.bat` à la place
- Ou ouvrir PowerShell en tant qu'administrateur

### Erreur "Compress-Archive n'est pas reconnu"
- Mettre à jour PowerShell vers une version récente
- Ou utiliser `package_addon.bat` qui gère mieux les anciennes versions

### Fichier ZIP vide ou corrompu
- Vérifier que tous les fichiers `.py` sont présents
- Relancer le script
- Vérifier les permissions d'écriture

### L'addon ne s'installe pas dans Blender
- Vérifier que le ZIP contient bien un dossier `jp_buildgen` avec les fichiers Python
- Redémarrer Blender après installation
- Vérifier la compatibilité de version (Blender 4.5.0+)

## Structure du package final

```
jp_buildgen_v0.1.3.zip
└── jp_buildgen/
    ├── __init__.py
    ├── core.py
    ├── operators.py
    ├── panels.py
    ├── properties.py
    ├── README.md (optionnel)
    └── textures/
        ├── office/
        ├── mall/
        ├── restaurant/
        ├── konbini/
        ├── apartment/
        └── house/
```