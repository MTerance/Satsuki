# Correction de l'erreur de packaging ZIP

## Problème identifié
Lors de l'installation de l'addon dans Blender, l'erreur suivante apparaissait :
```
ZIP packaged incorrectly; __init__.py should be in a directory, not at top-level
```

## Cause du problème
Les scripts de packaging compressaient les fichiers **directement à la racine** du ZIP au lieu de les placer dans un sous-dossier `jp_buildgen/`.

### Structure incorrecte (AVANT)
```
jp_buildgen_v0.1.3.zip
├── __init__.py          ❌ À la racine
├── core.py              ❌ À la racine  
├── operators.py         ❌ À la racine
├── panels.py            ❌ À la racine
├── properties.py        ❌ À la racine
├── README.md            ❌ À la racine
└── textures/            ❌ À la racine
```

### Structure correcte (APRÈS)
```
jp_buildgen_v0.1.3.zip
└── jp_buildgen/         ✅ Dossier addon
    ├── __init__.py      ✅ Dans le dossier
    ├── core.py          ✅ Dans le dossier
    ├── operators.py     ✅ Dans le dossier
    ├── panels.py        ✅ Dans le dossier
    ├── properties.py    ✅ Dans le dossier
    ├── README.md        ✅ Dans le dossier
    └── textures/        ✅ Dans le dossier
```

## Solution implémentée

### Modification de `package_simple.bat`
```bat
# AVANT - Compression directe
powershell -command "Compress-Archive -Path '__init__.py','core.py',... -DestinationPath '%ZIP_NAME%' -Force"

# APRÈS - Création de structure temporaire
mkdir "%TEMP_DIR%\jp_buildgen"
copy "*.py" "%TEMP_DIR%\jp_buildgen\" 
xcopy "textures" "%TEMP_DIR%\jp_buildgen\textures" /e /i /q
powershell -command "Compress-Archive -Path '%TEMP_DIR%\jp_buildgen' -DestinationPath '%ZIP_NAME%' -Force"
```

### Étapes de correction
1. **Créer un répertoire temporaire** avec la structure correcte
2. **Copier tous les fichiers** dans `TEMP_DIR/jp_buildgen/`
3. **Compresser le dossier parent** contenant `jp_buildgen/`
4. **Nettoyer** le répertoire temporaire

## Scripts corrigés

### ✅ `package_simple.bat` 
- Script le plus simple et fiable
- Structure temporaire automatique
- Nettoyage après compression

### ✅ `package_addon.bat`
- Déjà utilisait la bonne logique
- Pas de modification nécessaire

### ⚠️ `package_addon.ps1`
- Problèmes d'encodage à résoudre
- Utiliser les scripts .bat en attendant

## Test de validation

Après correction, la structure du ZIP est vérifiée :
```powershell
Expand-Archive -Path 'jp_buildgen_v0.1.3.zip' -DestinationPath 'test'
# Résultat : test/jp_buildgen/[tous les fichiers]
```

## Installation dans Blender

Le ZIP corrigé s'installe maintenant sans erreur :
1. Edit > Preferences > Add-ons
2. Install... > Sélectionner `jp_buildgen_v0.1.3.zip`
3. Activer "JP Building Generator"
4. Interface disponible dans View3D > Sidebar > JPBuild

## Statut : ✅ RÉSOLU

L'erreur de packaging est maintenant corrigée. Les scripts `package_simple.bat` et `package_addon.bat` créent la structure ZIP correcte attendue par Blender.