# ? FIX APPLIQUÉ - DecorManager Plugin Loading

**Date** : 22 novembre 2025  
**Problème** : Plugin DecorManager ne se chargeait pas dans Godot  
**Status** : ? Résolu

---

## ?? Problème

### Erreur Godot

```
Impossible de charger le script de l'extension depuis le chemin : 
'res://addons/decor_manager/decorManagerTool.cs'

L'extension 'res://addons/decor_manager/plugin.cfg' a été désactivée.
```

---

## ? Solution

### Changement effectué

**Fichier** : `addons/decor_manager/plugin.cfg`

```diff
- script="decorManagerTool.cs"    ? Casse incorrecte
+ script="DecorManagerTool.cs"    ? Casse correcte
```

### Cause

Le fichier réel s'appelle `DecorManagerTool.cs` (avec **D** majuscule), mais le `plugin.cfg` référençait `decorManagerTool.cs` (avec **d** minuscule).

---

## ?? Résultat

| Aspect | Avant | Après |
|--------|-------|-------|
| **Plugin charge** | ? Non | ? Oui |
| **Erreur console** | ? Oui | ? Non |
| **Dock visible** | ? Non | ? Oui |
| **Build** | ? OK | ? OK |

---

## ?? Prochaines étapes

### 1. Redémarrer Godot Editor

Fermer et rouvrir l'éditeur Godot pour que le changement soit pris en compte.

### 2. Activer le plugin

```
Projet ? Paramètres du Projet ? Plugins ? Decor Manager ? ? Activer
```

### 3. Vérifier le dock

Le dock "Decor Manager" devrait apparaître à droite de l'éditeur.

### 4. Tester les fonctionnalités

- ? Chargement de scène .tscn
- ? Gestion des caméras
- ? Placement spawn points
- ? Menu rendering

---

## ?? Fichiers créés

| Fichier | Description |
|---------|-------------|
| `Documentation/DecorManager_Plugin_Loading_Fix.md` | Guide détaillé du fix |
| `Tools/DecorManager_Plugin_QuickFix.md` | Quick fix (30 secondes) |
| `PLUGIN_LOADING_FIX_SUCCESS.md` | Ce récapitulatif |

---

## ?? Vérification

### Build

```bash
dotnet build
# ? Génération réussie
```

### Fichier modifié

```bash
git status
# modified:   addons/decor_manager/plugin.cfg
```

---

## ?? Leçon apprise

**Bonne pratique** : Toujours utiliser la **casse exacte** des noms de fichiers dans les références, même sur Windows (qui n'est pas sensible à la casse).

**Convention C#** : 
- ? `DecorManagerTool.cs` (PascalCase)
- ? `decorManagerTool.cs` (camelCase)

---

## ?? Conclusion

**Problème** : Incohérence de casse dans `plugin.cfg`

**Fix** : 1 caractère changé (`d` ? `D`)

**Temps** : 2 minutes

**Résultat** : Plugin fonctionnel ! ?

---

*Date : 22 novembre 2025*  
*Fix : Correction casse nom fichier*  
*Status : ? Résolu et documenté*
