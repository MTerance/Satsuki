# ?? Decor Manager Tool - Documentation

## ?? Vue d'ensemble

**Decor Manager** est un outil Godot personnalisé pour gérer les décors et les caméras dans le projet Satsuki. Il permet de :
- ? Charger des fichiers `.tscn` directement dans l'éditeur
- ? Visualiser et éditer les caméras (Title_Camera3D, Lobby_Camera3D, Game_Camera3D)
- ? Modifier les positions et rotations des caméras
- ? Créer de nouvelles caméras si elles n'existent pas
- ? Renommer les caméras

---

## ?? Structure des fichiers

```
Satsuki/
??? Tools/
?   ??? DecorManagerTool.cs          ? Outil principal
??? addons/
?   ??? decor_manager/
?       ??? plugin.cfg               ? Configuration plugin
?       ??? DecorManagerPlugin.cs    ? Script d'activation
```

---

## ?? Installation

### 1. Activer le plugin dans Godot

1. Ouvrir Godot
2. Aller dans **Project ? Project Settings ? Plugins**
3. Activer **"Decor Manager"**
4. Le dock apparaît dans le panneau de droite

### 2. Vérification

- ? Onglet "Decor Manager" visible dans le dock droit
- ? Logs : "DecorManagerTool: Initialisation..."
- ? Interface chargée avec sections

---

## ?? Interface utilisateur

### Vue d'ensemble

```
???????????????????????????????
?  DECOR MANAGER              ?
???????????????????????????????
?  Charger une scene          ?
?  ?????????????????????????? ?
?  ? Chemin .tscn: [......] ? ?
?  ?????????????????????????? ?
?  [Charger la scene]         ?
???????????????????????????????
?  Status: Aucune scene...    ?
???????????????????????????????
?  Title_Camera3D (Trouvee)   ?
?  Nom: [Title_Camera3D]      ?
?  Position:                  ?
?    X: [0.0] Y: [0.0] Z: [0] ?
?  Rotation (degres):         ?
?    X: [0] Y: [0] Z: [0]     ?
?  [Appliquer]                ?
???????????????????????????????
?  Lobby_Camera3D (Non...)    ?
?  ...                        ?
?  [Creer]                    ?
???????????????????????????????
?  Game_Camera3D (Non...)     ?
?  ...                        ?
?  [Creer]                    ?
???????????????????????????????
```

---

## ?? Utilisation

### 1. Charger une scène

#### Option A : Saisie manuelle
```
1. Taper le chemin dans "Chemin .tscn:"
   Exemple: res://Scenes/Locations/Restaurant.tscn
2. Cliquer "Charger la scene"
```

#### Option B : Navigateur de fichiers
```
1. Cliquer sur le bouton "..." (Browse)
2. Sélectionner un fichier .tscn
3. Cliquer "Charger la scene"
```

**Résultat** :
- ? La scène est chargée dans l'éditeur
- ? Les caméras sont détectées automatiquement
- ? Les panels de caméras sont mis à jour
- ? Status : "Scene chargee: [chemin]" (vert)

---

### 2. Éditer une caméra existante

#### Exemple : Title_Camera3D

```
1. La caméra apparaît avec "(Trouvee)" en vert
2. Modifier le nom (optionnel)
   Nom: [Title_Camera3D] ? [NewTitle_Camera3D]
3. Modifier la position
   X: [4.61]
   Y: [6.13]
   Z: [58.77]
4. Modifier la rotation (en degrés)
   X: [0]
   Y: [0]
   Z: [0]
5. Cliquer "Appliquer"
```

**Résultat** :
- ? La caméra est mise à jour dans la scène
- ? La scène est marquée comme modifiée (*)
- ? Status : "Camera Title_Camera3D mise a jour" (vert)

---

### 3. Créer une nouvelle caméra

#### Si une caméra n'existe pas

```
1. Le panel affiche "(Non trouvee)" en gris
2. Le bouton "Creer" est visible
3. Cliquer sur "Creer"
```

**Résultat** :
- ? Une nouvelle Camera3D est créée
- ? Position par défaut : (0, 0, 0)
- ? Rotation par défaut : (0, 0, 0)
- ? Le panel passe à "Trouvee" avec bouton "Appliquer"
- ? Status : "Camera [nom] creee" (vert)

---

## ?? Couleurs des caméras

| Caméra | Couleur | Usage |
|--------|---------|-------|
| **Title_Camera3D** | ?? Orange | Menu principal |
| **Lobby_Camera3D** | ?? Cyan | Sélection mode |
| **Game_Camera3D** | ?? Vert | Gameplay |

---

## ?? Fonctionnalités détaillées

### Chargement de scène

```csharp
private void OnLoadScenePressed()
{
    // 1. Validation du chemin
    if (!ResourceLoader.Exists(scenePath))
        ? Erreur: "Fichier introuvable"
    
    // 2. Déchargement de la scène précédente
    if (_loadedScene != null)
        ? _loadedScene.QueueFree()
    
    // 3. Chargement de la nouvelle scène
    var scene = GD.Load<PackedScene>(scenePath);
    _loadedScene = scene.Instantiate<Node3D>();
    
    // 4. Ajout à l'arbre de l'éditeur
    editedSceneRoot.AddChild(_loadedScene);
    
    // 5. Scan des caméras
    ScanCameras(_loadedScene);
    
    // 6. Mise à jour des panels
    UpdateCameraPanels();
}
```

### Scan des caméras

```csharp
private void ScanCameras(Node node)
{
    // Recherche récursive
    if (node is Camera3D camera)
    {
        // Filtrage par nom
        if (name == "Title_Camera3D" || 
            name == "Lobby_Camera3D" || 
            name == "Game_Camera3D")
        {
            _cameras[name] = camera;
        }
    }
    
    // Parcours des enfants
    foreach (Node child in node.GetChildren())
        ScanCameras(child);
}
```

### Application des changements

```csharp
public void ApplyCameraChanges(
    string cameraName, 
    string newName, 
    Vector3 position, 
    Vector3 rotation)
{
    var camera = _cameras[cameraName];
    
    // 1. Renommage (si nécessaire)
    if (newName != cameraName)
    {
        camera.Name = newName;
        _cameras.Remove(cameraName);
        _cameras[newName] = camera;
    }
    
    // 2. Positionnement
    camera.GlobalPosition = position;
    camera.GlobalRotation = rotation;
    
    // 3. Marquer comme modifié
    editorInterface.MarkSceneAsUnsaved();
}
```

### Création de caméra

```csharp
public void CreateCamera(string cameraName)
{
    // 1. Création
    var newCamera = new Camera3D();
    newCamera.Name = cameraName;
    newCamera.GlobalPosition = Vector3.Zero;
    newCamera.GlobalRotation = Vector3.Zero;
    
    // 2. Ajout à la scène
    _loadedScene.AddChild(newCamera);
    newCamera.Owner = _loadedScene;
    
    // 3. Enregistrement
    _cameras[cameraName] = newCamera;
    
    // 4. Mise à jour UI
    UpdateCameraPanels();
    
    // 5. Marquer comme modifié
    editorInterface.MarkSceneAsUnsaved();
}
```

---

## ?? États des caméras

### Caméra trouvée

```
Title_Camera3D (Trouvee) ? Texte vert
Nom: [Title_Camera3D]
Position: X: [4.61] Y: [6.13] Z: [58.77]
Rotation: X: [0] Y: [0] Z: [0]
[Appliquer] ? Activé
```

### Caméra non trouvée

```
Title_Camera3D (Non trouvee) ? Texte gris
Nom: []
Position: X: [0] Y: [0] Z: [0]
Rotation: X: [0] Y: [0] Z: [0]
[Creer] ? Visible
```

---

## ?? Workflow typique

### Scénario 1 : Éditer un décor existant

```
1. Ouvrir Godot
2. Activer le plugin "Decor Manager"
3. Dans le dock Decor Manager:
   ? Chemin: res://Scenes/Locations/Restaurant.tscn
   ? Cliquer "Charger la scene"
4. Les caméras sont détectées
5. Modifier Title_Camera3D:
   ? Position Y: 6.13 ? 8.0
   ? Rotation X: 0 ? 15
6. Cliquer "Appliquer"
7. Sauvegarder la scène (Ctrl+S)
```

### Scénario 2 : Créer une nouvelle caméra

```
1. Charger une scène
2. Game_Camera3D affiche "(Non trouvee)"
3. Cliquer "Creer" sur Game_Camera3D
4. La caméra est créée à (0, 0, 0)
5. Modifier sa position:
   ? X: 10, Y: 5, Z: 20
6. Cliquer "Appliquer"
7. Sauvegarder
```

### Scénario 3 : Renommer une caméra

```
1. Charger une scène avec Lobby_Camera3D
2. Modifier le nom:
   ? Nom: [Lobby_Camera3D] ? [Menu_Camera3D]
3. Cliquer "Appliquer"
4. La caméra est renommée
5. Sauvegarder
```

---

## ?? Paramètres des SpinBox

### Position

| Axe | Min | Max | Step | Unité |
|-----|-----|-----|------|-------|
| X | -1000 | 1000 | 0.1 | mètres |
| Y | -1000 | 1000 | 0.1 | mètres |
| Z | -1000 | 1000 | 0.1 | mètres |

### Rotation

| Axe | Min | Max | Step | Unité |
|-----|-----|-----|------|-------|
| X | -180 | 180 | 0.1 | degrés |
| Y | -180 | 180 | 0.1 | degrés |
| Z | -180 | 180 | 0.1 | degrés |

**Note** : La rotation est convertie automatiquement en radians pour Godot.

---

## ?? Logs de debug

### Initialisation
```
DecorManagerTool: Initialisation...
DecorManagerTool: Dock ajoute
```

### Chargement de scène
```
Fichier selectionne: res://Scenes/Locations/Restaurant.tscn
Camera trouvee: Title_Camera3D
Camera trouvee: Lobby_Camera3D
Status: Scene chargee: res://Scenes/Locations/Restaurant.tscn
```

### Application de changements
```
Status: Camera Title_Camera3D mise a jour
```

### Création de caméra
```
Status: Camera Game_Camera3D creee
```

### Erreurs
```
Status: Erreur: Fichier introuvable - [chemin]
Status: Erreur: Camera [nom] non trouvee
Status: Erreur de chargement: [message]
```

---

## ?? Résolution de problèmes

### Le dock n'apparaît pas

**Solutions** :
1. Vérifier que le plugin est activé
   - Project ? Project Settings ? Plugins
   - Cocher "Decor Manager"
2. Redémarrer Godot
3. Vérifier les logs pour les erreurs

### Les caméras ne sont pas détectées

**Causes possibles** :
1. Noms incorrects (sensible à la casse)
   - Doit être exactement : `Title_Camera3D`, `Lobby_Camera3D`, `Game_Camera3D`
2. Caméras dans des sous-nœuds trop profonds
   - Le scan est récursif, donc devrait fonctionner
3. Type de nœud incorrect
   - Doit être `Camera3D`, pas `Camera2D`

**Solution** :
```
1. Ouvrir la scène dans l'arborescence Godot
2. Vérifier les noms des caméras
3. Vérifier le type (Camera3D)
4. Recharger la scène dans Decor Manager
```

### Les changements ne sont pas sauvegardés

**Solution** :
1. Vérifier que la scène est marquée (*) dans l'éditeur
2. Sauvegarder explicitement (Ctrl+S)
3. Si le problème persiste, vérifier les permissions d'écriture

### Erreur "Fichier introuvable"

**Causes** :
1. Chemin incorrect
2. Fichier supprimé ou déplacé
3. Extension manquante

**Solution** :
```
1. Utiliser le bouton "..." pour naviguer
2. Vérifier que le chemin commence par "res://"
3. Vérifier l'extension ".tscn"
```

---

## ?? Extensibilité

### Ajouter un nouveau type de caméra

```csharp
// Dans ScanCameras()
if (cameraName == "Title_Camera3D" || 
    cameraName == "Lobby_Camera3D" || 
    cameraName == "Game_Camera3D" ||
    cameraName == "Cinematic_Camera3D") // ? Nouvelle
{
    _cameras[cameraName] = camera;
}

// Dans CreateDockPanel()
_cinematicCameraPanel = CreateCameraConfigPanel(
    "Cinematic_Camera3D", 
    new Color(1.0f, 0.0f, 1.0f) // Magenta
);
_mainContainer.AddChild(_cinematicCameraPanel);
```

### Ajouter des propriétés de caméra

Exemple : FOV (Field of View)

```csharp
// Dans CameraConfigPanel
private SpinBox _fovInput;

// Dans CreateUI()
_fovInput = CreateSpinBox("FOV:", 10, 120);
fovContainer.AddChild(_fovInput);

// Dans UpdateFromCamera()
if (camera != null)
    _fovInput.Value = camera.Fov;

// Dans OnApplyPressed()
_camera.Fov = (float)_fovInput.Value;
```

---

## ?? Checklist d'utilisation

### Avant utilisation
- [ ] Plugin "Decor Manager" activé
- [ ] Dock visible dans le panneau de droite
- [ ] Fichier .tscn préparé

### Pendant utilisation
- [ ] Chemin .tscn correct
- [ ] Scène chargée avec succès
- [ ] Caméras détectées
- [ ] Modifications appliquées
- [ ] Scène marquée comme modifiée (*)

### Après utilisation
- [ ] Scène sauvegardée (Ctrl+S)
- [ ] Changements vérifiés dans l'éditeur
- [ ] Tests en jeu effectués

---

## ?? Résumé des fonctionnalités

| Fonctionnalité | Description | Status |
|----------------|-------------|--------|
| **Chargement .tscn** | Charger des scènes de décor | ? |
| **Scan automatique** | Détection des caméras | ? |
| **Édition position** | Modifier X, Y, Z | ? |
| **Édition rotation** | Modifier angles en degrés | ? |
| **Renommage** | Changer le nom des caméras | ? |
| **Création** | Créer des caméras manquantes | ? |
| **Interface claire** | Panels avec codes couleur | ? |
| **Sauvegarde auto** | Marquer scène modifiée | ? |

---

*Date de création : 22 novembre 2025*  
*Version : 1.0*  
*Build : ? Réussi*
