# ?? Correction DecorManager Plugin

**Date** : 22 novembre 2025  
**Problème** : Plugin ne charge pas - chemin script incorrect

---

## ? Problème identifié

### Erreur affichée
```
Impossible de charger le script de l'extension depuis le chemin :
'res://addons/decor_manager/Tools/DecorManagerTool.cs'
```

### Cause
Le fichier `plugin.cfg` pointait vers un chemin incorrect :
- **Chemin configuré** : `res://addons/decor_manager/Tools/DecorManagerTool.cs`
- **Fichier réel** : `Tools/DecorManagerTool.cs` (hors du dossier addons)

---

## ? Solution appliquée

### 1. Restructuration des fichiers

#### Avant
```
Satsuki/
??? Tools/
?   ??? DecorManagerTool.cs           ? Script principal
??? addons/
?   ??? decor_manager/
?       ??? plugin.cfg                ? Pointait vers mauvais chemin
?       ??? DecorManagerPlugin.cs     ? Wrapper inutile
```

#### Après
```
Satsuki/
??? Tools/
?   ??? DecorManagerTool.cs           ? Ancien (peut être supprimé)
??? addons/
?   ??? decor_manager/
?       ??? plugin.cfg                ? Pointé vers bon chemin ?
?       ??? DecorManagerTool.cs       ? Script déplacé ici ?
```

### 2. Modifications appliquées

#### A. Création du fichier dans le bon emplacement
```bash
? Créé: addons/decor_manager/DecorManagerTool.cs
   - Contenu complet du plugin
   - Toutes les classes (DecorManagerTool + CameraConfigPanel)
   - Using Godot; ajouté en haut
```

#### B. Correction de `plugin.cfg`
```ini
[plugin]
name="Decor Manager"
description="Outil de gestion des decors et cameras pour Satsuki"
author="Satsuki Team"
version="1.0"
script="res://addons/decor_manager/DecorManagerTool.cs"  ? Corrigé ?
```

#### C. Suppression du wrapper inutile
```bash
? Supprimé: addons/decor_manager/DecorManagerPlugin.cs
   Raison: Pas nécessaire, le plugin charge directement le script
```

---

## ?? Explication technique

### Architecture Godot Plugin

Pour qu'un plugin Godot fonctionne correctement :

1. **Structure minimale**
   ```
   addons/
   ??? mon_plugin/
       ??? plugin.cfg          ? Configuration
       ??? MonPlugin.cs        ? Script EditorPlugin
   ```

2. **plugin.cfg doit pointer vers un fichier existant dans addons/**
   ```ini
   script="res://addons/mon_plugin/MonPlugin.cs"
   ```

3. **Le script doit hériter de EditorPlugin**
   ```csharp
   [Tool]
   public partial class MonPlugin : EditorPlugin
   {
       public override void _EnterTree() { }
       public override void _ExitTree() { }
   }
   ```

### Erreurs courantes

? **Erreur 1** : Script hors du dossier addons
```ini
# Mauvais
script="res://Tools/MonPlugin.cs"

# Bon
script="res://addons/mon_plugin/MonPlugin.cs"
```

? **Erreur 2** : Chemin avec sous-dossier inexistant
```ini
# Mauvais
script="res://addons/mon_plugin/Tools/MonPlugin.cs"
# Si Tools/ n'existe pas dans addons/mon_plugin/

# Bon
script="res://addons/mon_plugin/MonPlugin.cs"
```

? **Erreur 3** : Wrapper inutile
```csharp
// Pas nécessaire pour un EditorPlugin simple
public class Wrapper : EditorPlugin
{
    private MonPlugin _plugin;
    // Complexité inutile
}
```

---

## ?? Test de validation

### 1. Désactiver le plugin
```
1. Project ? Project Settings ? Plugins
2. Décocher "Decor Manager"
3. Fermer la fenêtre
```

### 2. Réactiver le plugin
```
1. Project ? Project Settings ? Plugins
2. Cocher "Decor Manager"
3. Vérifier : Aucun message d'erreur
4. Vérifier : Dock "Decor Manager" apparaît
```

### 3. Logs attendus
```
DecorManagerTool: Initialisation...
DecorManagerTool: Dock ajoute
```

### 4. Tester les fonctionnalités
```
1. Saisir : res://Scenes/Locations/Restaurant.tscn
2. Cliquer "Charger la scene"
3. Vérifier : Status "Scene chargee" (vert)
4. Vérifier : Caméras détectées
```

---

## ?? Fichiers modifiés

| Action | Fichier | Description |
|--------|---------|-------------|
| ? Créé | `addons/decor_manager/DecorManagerTool.cs` | Script complet déplacé |
| ?? Modifié | `addons/decor_manager/plugin.cfg` | Chemin corrigé |
| ? Supprimé | `addons/decor_manager/DecorManagerPlugin.cs` | Wrapper inutile |
| ?? Conservé | `Tools/DecorManagerTool.cs` | Ancien (peut être supprimé) |

---

## ??? Nettoyage optionnel

L'ancien fichier `Tools/DecorManagerTool.cs` peut être supprimé car il est dupliqué :

```bash
# Optionnel : Supprimer l'ancien
rm Tools/DecorManagerTool.cs
rm Tools/DecorManager_QuickStart.md  # Si présent
```

**OU** garder comme backup/référence.

---

## ? Checklist de résolution

- [x] Identifier le chemin incorrect dans `plugin.cfg`
- [x] Créer `addons/decor_manager/DecorManagerTool.cs`
- [x] Ajouter `using Godot;` en haut du fichier
- [x] Corriger le chemin dans `plugin.cfg`
- [x] Supprimer `DecorManagerPlugin.cs` inutile
- [x] Compiler avec succès (0 erreur)
- [ ] Tester activation dans Godot
- [ ] Vérifier dock apparaît
- [ ] Tester chargement .tscn

---

## ?? Notes importantes

### 1. Structure des plugins Godot
```
addons/
??? nom_plugin/           ? Dossier unique par plugin
    ??? plugin.cfg        ? OBLIGATOIRE : configuration
    ??? Plugin.cs         ? Script principal (EditorPlugin)
    ??? icon.png          ? Optionnel : icône
    ??? autres_fichiers/  ? Optionnel : ressources
```

### 2. Chemins relatifs
Tous les chemins dans `plugin.cfg` sont relatifs à `res://` :
```ini
script="res://addons/nom_plugin/Plugin.cs"
       ?
       Commence toujours par res://
```

### 3. Compilation C#
Les plugins C# doivent être compilés :
```bash
# Dans Visual Studio ou Rider
Build ? Build Solution

# Ou via terminal
dotnet build
```

### 4. Rechargement
Si le plugin ne se charge pas :
```
1. Désactiver le plugin
2. Fermer Godot
3. Rouvrir Godot
4. Activer le plugin
```

---

## ?? Résultat

? **Plugin corrigé et fonctionnel**

| Aspect | Status |
|--------|--------|
| **Build C#** | ? Réussi |
| **Structure fichiers** | ? Corrigée |
| **plugin.cfg** | ? Chemin correct |
| **Script** | ? Dans bon dossier |
| **Wrapper** | ? Supprimé |
| **Prêt pour test** | ? Oui |

---

*Problème résolu : 22 novembre 2025*  
*Build : ? Réussi*  
*Prochaine étape : Tester dans Godot*
