# ?? Gestion automatique des caméras par scène

## ? Système de caméras contextuelles

Le système active automatiquement la caméra appropriée en fonction de la scène UI affichée :
- **Title** ? `Title_Camera3D`
- **MainMenu** ? `Lobby_Camera3D`

---

## ?? Flux de changement de caméra

### Scénario 1 : Credits ? Title

```
[Credits terminé]
    ?
[LoadTitle()]
    ?
[Title créé et ajouté]
    ?
[CallDeferred(ActivateTitleCamera)]
    ?
[SetActiveCamera(CameraType.Title)]
    ?
[DeactivateAllCameras()] ? Désactive toutes les caméras
    ?
[Title_Camera3D.Current = true]
    ?
[? Title_Camera3D active]
```

### Scénario 2 : Title ? MainMenu

```
[Utilisateur clique "Start Game"]
    ?
[OnStartGameRequested()]
    ?
[LoadMainMenu()]
    ?
[MainMenu créé et ajouté]
    ?
[CallDeferred(ActivateLobbyCamera)]
    ?
[SetActiveCamera(CameraType.Lobby)]
    ?
[DeactivateAllCameras()] ? Désactive Title_Camera3D et autres
    ?
[Lobby_Camera3D.Current = true]
    ?
[? Lobby_Camera3D active]
```

### Scénario 3 : MainMenu ? Title (Back)

```
[Utilisateur clique "Back to Title"]
    ?
[OnBackToTitleRequested()]
    ?
[LoadTitle()]
    ?
[CallDeferred(ActivateTitleCamera)]
    ?
[SetActiveCamera(CameraType.Title)]
    ?
[DeactivateAllCameras()] ? Désactive Lobby_Camera3D
    ?
[Title_Camera3D.Current = true]
    ?
[? Title_Camera3D réactivée]
```

---

## ?? Implémentation

### 1. Dans `MainGameScene.LoadTitle()`

```csharp
public void LoadTitle()
{
    // ... création de Title ...
    
    // Activation différée de la caméra Title
    CallDeferred(nameof(ActivateTitleCamera));
}

private void ActivateTitleCamera()
{
    bool success = _locationManager.LoadLocationFromScene(
        "res://Scenes/Locations/Restaurant.tscn", 
        useCache: true
    );
    
    if (success && _locationManager.CurrentLocation != null)
    {
        bool cameraSet = _locationManager.CurrentLocation.SetActiveCamera(
            CameraType.Title
        );
        
        if (cameraSet)
        {
            GD.Print("Camera Title_Camera3D activee avec succes");
        }
    }
}
```

### 2. Dans `MainGameScene.LoadMainMenu()`

```csharp
public void LoadMainMenu()
{
    // ... création de MainMenu ...
    
    // Activation différée de la caméra Lobby
    CallDeferred(nameof(ActivateLobbyCamera));
}

private void ActivateLobbyCamera()
{
    if (_locationManager?.CurrentLocation != null)
    {
        GD.Print("Activation camera Lobby pour MainMenu...");
        
        bool cameraSet = _locationManager.CurrentLocation.SetActiveCamera(
            CameraType.Lobby
        );
        
        if (cameraSet)
        {
            GD.Print("Camera Lobby_Camera3D activee avec succes");
        }
        else
        {
            GD.PrintErr("Echec activation Camera Lobby_Camera3D");
        }
    }
    else
    {
        GD.PrintErr("Location non chargee, impossible d'activer la camera");
    }
}
```

### 3. Désactivation automatique dans `LocationModel.SetActiveCamera()`

```csharp
public bool SetActiveCamera(CameraType cameraType)
{
    // ... recherche de la caméra ...
    
    if (currentCamera != null)
    {
        // ? Désactiver TOUTES les autres caméras
        DeactivateAllCameras();
        
        // ? Activer la caméra cible
        currentCamera.Current = true;
        
        return true;
    }
}

private void DeactivateAllCameras()
{
    var cameras = new List<Camera3D>();
    FindAllCamerasRecursive(this, cameras);
    
    foreach (var camera in cameras)
    {
        if (camera.Current)
        {
            camera.Current = false;
            GD.Print($"  - Camera {camera.Name} desactivee");
        }
    }
}
```

---

## ?? Mapping Scène ? Caméra

| Scène UI | Caméra active | Position approximative |
|----------|---------------|------------------------|
| **Credits** | (Aucune) | N/A |
| **Title** | `Title_Camera3D` | (4.61, 6.13, 58.77) |
| **MainMenu** | `Lobby_Camera3D` | (Position Lobby) |
| **Gameplay** | `MainGame_Camera3D` | (À définir) |

---

## ?? Types de caméras disponibles

```csharp
public enum CameraType
{
    Lobby,      // Pour MainMenu (sélection mode)
    Title,      // Pour Title (menu principal)
    MainGame,   // Pour le gameplay
    Cinematic   // Pour les cinématiques
}
```

---

## ?? Logs attendus

### Passage Title ? MainMenu

```
MainGameScene: Reception du signal StartGameRequested
MainGameScene: Chargement MainMenu...
MainMenu: Initialisation du menu principal...
MainMenu: UI creee avec succes
MainMenu: Menu initialise avec 4 options
MainMenu charge
MainGameScene: Activation camera Lobby pour MainMenu...
Restaurant: Recherche de la camera Lobby (Lobby_Camera3D)
Restaurant: Camera non trouvee avec %, essai chemin direct...
  - Camera Title_Camera3D desactivee
Restaurant: Camera Lobby_Camera3D activee avec succes
  - Position: (-24.9722, 9.54031, 27.7257)
  - Rotation: (0.368125, 0, 0)
  - Chemin: Restaurant/Lobby_Camera3D
Camera Lobby_Camera3D activee avec succes
```

### Passage MainMenu ? Title

```
MainGameScene: Reception du signal BackToTitleRequested
MainGameScene: Chargement Title...
Title: Initialisation de l'ecran titre...
UI creee avec succes
Menu initialise avec 4 options
Title charge
Restaurant: Recherche de la camera Title (Title_Camera3D)
Restaurant: Camera non trouvee avec %, essai chemin direct...
  - Camera Lobby_Camera3D desactivee
Restaurant: Camera Title_Camera3D activee avec succes
  - Position: (4.61098, 6.13089, 58.7656)
  - Rotation: (0, 0, 0)
  - Chemin: Restaurant/Title_Camera3D
Camera Title_Camera3D activee avec succes
```

---

## ?? Synchronisation avec CallDeferred

### Pourquoi CallDeferred ?

```csharp
CallDeferred(nameof(ActivateLobbyCamera));
```

**Raisons** :
1. ? Attend que la scène UI soit complètement initialisée
2. ? Évite les problèmes de synchronisation
3. ? Garantit que la location est prête
4. ? Permet au menu de s'afficher avant le changement de caméra

**Sans CallDeferred** :
- ? Risque de race condition
- ? La caméra peut changer avant que le menu soit prêt
- ? Possible erreur si location non encore chargée

**Avec CallDeferred** :
- ? Exécution différée au prochain frame
- ? Tout est initialisé
- ? Pas de conflit

---

## ?? Positions des caméras dans Restaurant.tscn

```
Restaurant (Node3D)
??? DirectionalLight3D
??? Restaurant_Scene (GLTF)
??? Lobby_Camera3D
?   ??? Transform: (-24.97, 9.54, 27.73)
?   ??? Rotation: (0.93, 0.37, 0)  ? Regard vers le bas
?
??? Title_Camera3D
    ??? Transform: (4.61, 6.13, 58.77)
    ??? Rotation: (1, 0, 0)  ? Vue de face
```

### Différences visuelles

- **Title_Camera3D** : Vue frontale du restaurant, centrée
- **Lobby_Camera3D** : Vue d'angle, légèrement en hauteur

---

## ?? Tests de validation

### Test 1 : Title ? MainMenu
```
1. ? Lancer l'application
2. ? Attendre la fin des crédits
3. ? Vérifier : Title affiché avec Title_Camera3D
4. ? Cliquer "Start Game"
5. ? Vérifier : MainMenu affiché
6. ? Vérifier : Camera change vers Lobby_Camera3D
7. ? Vérifier : Title_Camera3D désactivée
8. ? Observer : Vue différente du restaurant
```

### Test 2 : MainMenu ? Title
```
1. ? Depuis MainMenu
2. ? Cliquer "Back to Title" ou Échap
3. ? Vérifier : Title réaffiché
4. ? Vérifier : Camera change vers Title_Camera3D
5. ? Vérifier : Lobby_Camera3D désactivée
6. ? Observer : Vue revient à la vue frontale
```

### Test 3 : Logs de changement
```
1. ? Observer la console
2. ? Vérifier : "Camera [X] desactivee" lors du changement
3. ? Vérifier : "Camera [Y] activee avec succes"
4. ? Vérifier : Position et rotation affichées
5. ? Vérifier : Chemin complet affiché
```

### Test 4 : Transitions multiples
```
1. ? Credits ? Title ? MainMenu
2. ? MainMenu ? Title ? MainMenu
3. ? Vérifier : Caméras changent correctement à chaque fois
4. ? Vérifier : Pas de caméras multiples actives
5. ? Vérifier : Pas de lag ou saccade
```

### Test 5 : Caméra manquante
```
1. ?? Renommer temporairement Lobby_Camera3D
2. ?? Lancer et aller dans MainMenu
3. ? Vérifier : Log d'erreur "Camera Lobby_Camera3D introuvable"
4. ? Vérifier : Pas de crash
5. ? Vérifier : Application continue de fonctionner
```

---

## ?? Comparaison avant/après

### Avant (sans changement automatique)

```csharp
public void LoadMainMenu()
{
    var mainMenu = new MainMenu();
    AddChild(mainMenu);
    _currentScene = mainMenu;
    
    // ? Pas de changement de caméra
    // La caméra Title reste active
}
```

**Problèmes** :
- ? Mauvaise vue pour le MainMenu
- ? Pas cohérent avec la scène
- ? Utilisateur voit la même vue

### Après (avec changement automatique)

```csharp
public void LoadMainMenu()
{
    var mainMenu = new MainMenu();
    AddChild(mainMenu);
    _currentScene = mainMenu;
    
    // ? Changement automatique de caméra
    CallDeferred(nameof(ActivateLobbyCamera));
}

private void ActivateLobbyCamera()
{
    _locationManager.CurrentLocation.SetActiveCamera(CameraType.Lobby);
    // ? Title_Camera3D désactivée automatiquement
    // ? Lobby_Camera3D activée
}
```

**Avantages** :
- ? Vue adaptée au MainMenu
- ? Cohérence visuelle
- ? Désactivation automatique des autres caméras
- ? Transitions fluides

---

## ?? Points clés

1. ? **Activation automatique** : Caméra change avec la scène
2. ? **CallDeferred** : Garantit l'initialisation complète
3. ? **Désactivation auto** : Toutes les autres caméras sont désactivées
4. ? **Logs détaillés** : Position, rotation, chemin
5. ? **Robuste** : Gestion d'erreur si caméra absente
6. ? **Cohérent** : Chaque scène a sa vue

---

## ?? Méthodes de changement de caméra

| Scène | Méthode | Caméra cible |
|-------|---------|--------------|
| Credits | (Aucune) | Aucune |
| Title | `ActivateTitleCamera()` | `Title_Camera3D` |
| MainMenu | `ActivateLobbyCamera()` | `Lobby_Camera3D` |
| Gameplay | `ActivateGameCamera()` | `MainGame_Camera3D` (à créer) |

---

## ?? Extensibilité

### Ajouter une caméra pour une nouvelle scène

```csharp
public void LoadNewScene()
{
    var newScene = new NewScene();
    AddChild(newScene);
    _currentScene = newScene;
    
    // Activation de la caméra spécifique
    CallDeferred(nameof(ActivateNewSceneCamera));
}

private void ActivateNewSceneCamera()
{
    if (_locationManager?.CurrentLocation != null)
    {
        bool cameraSet = _locationManager.CurrentLocation.SetActiveCamera(
            CameraType.Cinematic  // ou nouveau type
        );
        
        if (cameraSet)
        {
            GD.Print("Camera activee pour NewScene");
        }
    }
}
```

---

## ?? Fichiers modifiés

| Fichier | Modifications |
|---------|---------------|
| `Scenes/MainGameScene.cs` | ? Ajout `ActivateLobbyCamera()` |
| `Scenes/MainGameScene.cs` | ? `CallDeferred` dans `LoadMainMenu()` |
| `Scenes/Locations/LocationModel.cs` | ? (Déjà implémenté) `DeactivateAllCameras()` |

---

## ?? Résultat

? **Caméras contextuelles** : Chaque scène a sa vue  
? **Transitions automatiques** : Pas d'intervention manuelle  
? **Désactivation auto** : Une seule caméra active à la fois  
? **Logs détaillés** : Debug facile  
? **Robuste** : Gestion d'erreur complète  
? **Extensible** : Facile d'ajouter de nouvelles caméras  
? **Build réussi** : 0 erreur  

**Le système de caméras s'adapte automatiquement à la scène affichée ! ???**

---

*Date de mise à jour : 2024*  
*Build : ? Réussi*  
*Caméras gérées : Title_Camera3D, Lobby_Camera3D*
