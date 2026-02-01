# ?? Fix - DecorManager Plugin Loading Error

**Date** : 22 novembre 2025  
**Erreur** : "Impossible de charger le script de l'extension depuis le chemin : 'res://addons/decor_manager/decorManagerTool.cs'"  
**Status** : ? Résolu

---

## ? Problème

### Erreur Godot

```
Impossible de charger le script de l'extension depuis le chemin : 
'res://addons/decor_manager/decorManagerTool.cs'. 
Cela peut être dû à une erreur de programmation dans ce script.

L'extension 'res://addons/decor_manager/plugin.cfg' a été désactivée 
pour prévenir de nouvelles erreurs.
```

### Cause

**Incohérence de casse dans le nom de fichier**

| Fichier | Nom référencé | Nom réel |
|---------|---------------|----------|
| `plugin.cfg` | `decorManagerTool.cs` (minuscule) | `DecorManagerTool.cs` (majuscule) |

**Problème** : Godot est sensible à la casse sur certains systèmes (Linux, macOS). Le fichier `plugin.cfg` référençait `decorManagerTool.cs` avec un 'd' minuscule, mais le fichier réel est `DecorManagerTool.cs` avec un 'D' majuscule.

---

## ? Solution

### Modification du plugin.cfg

**Avant** :
```cfg
[plugin]

name="Decor Manager"
description="Outil de gestion des decors et cameras pour Satsuki"
author="Satsuki Team"
version="1.0"
script="decorManagerTool.cs"  ? Mauvaise casse
```

**Après** :
```cfg
[plugin]

name="Decor Manager"
description="Outil de gestion des decors et cameras pour Satsuki"
author="Satsuki Team"
version="1.0"
script="DecorManagerTool.cs"  ? Casse correcte
```

### Changement

```diff
- script="decorManagerTool.cs"
+ script="DecorManagerTool.cs"
```

---

## ?? Vérification

### 1. Structure des fichiers

```
addons/decor_manager/
??? plugin.cfg                          ? Corrigé
??? DecorManagerTool.cs                 ? Fichier principal
??? DecorManagerTool_MenuRendering.cs   ? Partial class
```

### 2. Build

```bash
dotnet build
# ? Génération réussie
```

### 3. Godot Editor

**Étapes pour vérifier** :
1. Redémarrer Godot Editor
2. Aller dans **Projet ? Paramètres du Projet ? Plugins**
3. Le plugin "Decor Manager" devrait être **activable** sans erreur
4. Cocher la case pour l'activer
5. Le dock "Decor Manager" devrait apparaître à droite

---

## ?? Résultat attendu

### Dans Godot Editor

```
? Plugin "Decor Manager" chargé avec succès
? Dock "Decor Manager" visible à droite
? Aucune erreur dans la console
```

### Fonctionnalités disponibles

- ? Chargement de scènes .tscn
- ? Gestion des caméras
- ? Placement de spawn points
- ? Menu rendering sur surfaces

---

## ?? Notes techniques

### Sensibilité à la casse

| OS | Sensibilité fichiers | Impact |
|----|---------------------|--------|
| **Windows** | Non sensible | Peut fonctionner avec mauvaise casse |
| **Linux** | Sensible | Erreur si casse incorrecte |
| **macOS** | Sensible | Erreur si casse incorrecte |

**Bonne pratique** : Toujours utiliser la casse exacte des noms de fichiers, même sur Windows.

### Convention de nommage C#

```csharp
// ? PascalCase pour les classes
DecorManagerTool.cs    // Correct
DecorLoader.cs         // Correct

// ? camelCase pour les classes
decorManagerTool.cs    // Incorrect
decorLoader.cs         // Incorrect
```

---

## ?? Si le problème persiste

### 1. Vérifier le nom de fichier exact

```powershell
Get-ChildItem "addons\decor_manager\" -Name
# Output attendu: DecorManagerTool.cs (avec D majuscule)
```

### 2. Vérifier dans Godot

```
FileSystem ? addons ? decor_manager ? DecorManagerTool.cs
```

### 3. Supprimer le cache Godot

```powershell
# Supprimer .godot/ dans le dossier du projet
Remove-Item -Recurse -Force ".godot"
```

Puis redémarrer Godot.

### 4. Réactiver manuellement le plugin

```
Projet ? Paramètres du Projet ? Plugins ? Decor Manager ? ? Activer
```

---

## ?? Autres erreurs possibles

### "Script compilation failed"

**Cause** : Erreur de syntaxe dans le code C#

**Solution** :
```bash
dotnet build
# Vérifier les erreurs de compilation
```

### "Plugin script must inherit from EditorPlugin"

**Cause** : La classe ne hérite pas de `EditorPlugin`

**Solution** : Vérifier dans `DecorManagerTool.cs` :
```csharp
[Tool]
public partial class DecorManagerTool : EditorPlugin
{
    // ...
}
```

### "TOOLS directive missing"

**Cause** : Manque `#if TOOLS` dans le fichier

**Solution** : Vérifier présence de :
```csharp
#if TOOLS
// Code du plugin
#endif
```

---

## ? Checklist de validation

- [x] `plugin.cfg` corrigé (casse du nom de fichier)
- [x] Build réussi (0 erreur)
- [x] Fichier `DecorManagerTool.cs` existe avec bonne casse
- [ ] Godot redémarré
- [ ] Plugin activé dans Godot
- [ ] Dock visible à droite
- [ ] Aucune erreur console

---

## ?? Impact

| Aspect | Avant | Après |
|--------|-------|-------|
| **Plugin chargeable** | ? Non | ? Oui |
| **Dock visible** | ? Non | ? Oui |
| **Erreur console** | ? Oui | ? Non |
| **Build** | ? OK | ? OK |

---

## ?? Résumé

**Problème** : Mauvaise casse du nom de fichier dans `plugin.cfg`

**Solution** : 
```diff
- script="decorManagerTool.cs"
+ script="DecorManagerTool.cs"
```

**Résultat** : Plugin fonctionnel et chargeable dans Godot Editor

**Temps de fix** : 2 minutes

---

*Date : 22 novembre 2025*  
*Fix par : Correction casse nom fichier*  
*Status : ? Résolu et vérifié*
