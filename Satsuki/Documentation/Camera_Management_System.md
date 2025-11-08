# ?? Système de Gestion de Caméras - LocationModel

## ?? Overview

Le système de gestion de caméras dans `LocationModel` permet de basculer entre différentes caméras prédéfinies dans une location en utilisant l'enum `CameraType`.

## ?? Enum CameraType

```csharp
public enum CameraType
{
    Lobby,       // Caméra du lobby
    Title,       // Caméra du menu titre
    MainGame,    // Caméra de jeu principale
    Cinematic    // Caméra cinématique
}
```

## ?? Méthode SetActiveCamera

### **Signature**

```csharp
public bool SetActiveCamera(CameraType cameraType)
```

### **Fonctionnalité**

1. **Mapping** : Convertit le `CameraType` en nom de node Godot
2. **Recherche** : Trouve la caméra correspondante via `GetNode<Camera3D>($"%{cameraNodeName}")`
3. **Activation** : Définit `camera.Current = true` pour activer la caméra
4. **Retour** : `true` si succès

### **Implémentation**

```csharp
public bool SetActiveCamera(CameraType cameraType)
{
    string cameraNodeName = cameraType switch
    {
        CameraType.Lobby => "Lobby_Camera3D",
        CameraType.Title => "Title_Camera3D",
        CameraType.MainGame => "MainGame_Camera3D",
        CameraType.Cinematic => "Cinematic_Camera3D",
        _ => null
    };
    
    GD.Print($"?? {LocationName}: Changement de caméra vers {cameraType} ({cameraNodeName})");
    
    var currentCamera = GetNode<Camera3D>($"%{cameraNodeName}");
    if (currentCamera is not null)
        currentCamera.Current = true;

    return true;
}
```

### **Convention de Nommage**

Les caméras dans Godot doivent suivre cette convention :
- `CameraType.Lobby` ? Node : `Lobby_Camera3D`
- `CameraType.Title` ? Node : `Title_Camera3D`
- `CameraType.MainGame` ? Node : `MainGame_Camera3D`
- `CameraType.Cinematic` ? Node : `Cinematic_Camera3D`

**Important** : Utiliser le préfixe `%` dans `GetNode` permet de chercher le node de manière unique même s'il est profond dans la hiérarchie.

---

## ?? Utilisation dans MainGameScene

### **Lors du Chargement de Restaurant pour Title**

```csharp
private void LoadRestaurantLocation()
{
    const string restaurantPath = "res://Scenes/Locations/Restaurant.tscn";
    
    bool success = _locationManager.LoadLocationFromScene(restaurantPath, useCache: true);
    
    if (success)
    {
        GD.Print($"? MainGameScene: Restaurant chargé dans CurrentLocation via LocationManager");

        // Activer la caméra Title
        if (_locationManager.CurrentLocation != null)
        {
            GD.Print($"?? MainGameScene: Activation de la caméra Title...");
            
            // Utiliser l'enum CameraType
            bool cameraSet = _locationManager.CurrentLocation.SetActiveCamera(CameraType.Title);
            
            if (cameraSet)
            {
                GD.Print($"? MainGameScene: Caméra Title activée avec succès");
            }
            else
            {
                GD.PrintErr($"? MainGameScene: Impossible d'activer la caméra Title");
            }
        }
    }
}
```

---

## ?? Séquence d'Activation

```
1. LoadTitleScene() appelé
   ?
2. Title chargé dans CurrentScene
   ?
3. CallDeferred(LoadRestaurantLocation)
   ?
4. LocationManager.LoadLocationFromScene("Restaurant.tscn")
   ?
5. Restaurant chargé avec toutes ses caméras
   ?
6. SetActiveCamera(CameraType.Title) appelé
   ?
7. Mapping: Title ? "Title_Camera3D"
   ?
8. GetNode<Camera3D>("%Title_Camera3D") recherche la caméra
   ?
9. camera.Current = true (activation)
   ?
10. Caméra Title devient la vue active du jeu
```

---

## ??? Configuration dans Godot

### **Structure de Restaurant.tscn**

```
Restaurant (Node3D) ?? LocationModel
    ??? Lobby_Camera3D (Camera3D)
    ??? Title_Camera3D (Camera3D)       ? Caméra pour le menu Title
    ??? MainGame_Camera3D (Camera3D)
    ??? Cinematic_Camera3D (Camera3D)
    ??? Environment
    ??? Lighting
    ??? Meshes
```

### **Configuration des Caméras**

#### **1. Title_Camera3D**
- **Type** : Camera3D
- **Position** : Vue appropriée pour le menu
- **Unique Name** : ? Activé (via % prefix)
- **Current** : False (sera activé par code)

**Propriétés** :
```
Transform:
    Position: (x, y, z)  // Position de vue du menu
    Rotation: (x, y, z)  // Orientation vers la scène

Camera:
    Fov: 75
    Near: 0.05
    Far: 4000
```

---

## ?? Exemples d'Utilisation

### **1. Changer de Caméra Manuellement**

```csharp
// Dans n'importe quelle classe ayant accès à ILocation
var location = LocationManager.Instance.CurrentLocation;

// Basculer vers la caméra du lobby
location.SetActiveCamera(CameraType.Lobby);

// Basculer vers la caméra de jeu
location.SetActiveCamera(CameraType.MainGame);

// Basculer vers la caméra cinématique
location.SetActiveCamera(CameraType.Cinematic);
```

### **2. Changer de Caméra lors d'un Événement**

```csharp
public void OnStartGameButtonPressed()
{
    // Passer de la caméra Title à la caméra MainGame
    _locationManager.CurrentLocation?.SetActiveCamera(CameraType.MainGame);
    
    // Lancer le jeu
    StartGame();
}
```

### **3. Séquence Cinématique**

```csharp
public async void PlayIntroSequence()
{
    // Activer la caméra cinématique
    _locationManager.CurrentLocation?.SetActiveCamera(CameraType.Cinematic);
    
    // Jouer l'animation
    await PlayCinematicAnimation();
    
    // Revenir à la caméra de jeu
    _locationManager.CurrentLocation?.SetActiveCamera(CameraType.MainGame);
}
```

### **4. Transition de Caméra Smooth**

```csharp
public async void TransitionToCamera(CameraType targetType)
{
    // Fade out
    await FadeOut(0.5f);
    
    // Changer de caméra
    _locationManager.CurrentLocation?.SetActiveCamera(targetType);
    
    // Fade in
    await FadeIn(0.5f);
}
```

---

## ?? Logs Générés

### **Logs Réussis**

```
?? MainGameScene: Activation de la caméra Title...
?? Restaurant: Changement de caméra vers Title (Title_Camera3D)
? MainGameScene: Caméra Title activée avec succès
```

### **Logs d'Erreur (si caméra introuvable)**

```
?? MainGameScene: Activation de la caméra Title...
?? Restaurant: Changement de caméra vers Title (Title_Camera3D)
? MainGameScene: Impossible d'activer la caméra Title
```

**Cause possible** :
- Le node `Title_Camera3D` n'existe pas dans Restaurant.tscn
- Le nom du node ne correspond pas exactement
- Le node n'est pas de type `Camera3D`

---

## ?? Debugging

### **Vérifier les Caméras Disponibles**

```csharp
// Lister toutes les caméras dans la location
var location = LocationManager.Instance.CurrentLocation as LocationModel;
if (location != null)
{
    var cameras = location.GetAllCameras();  // Utiliser méthode helper si ajoutée
    foreach (var cam in cameras)
    {
        GD.Print($"?? Caméra trouvée: {cam.Name}, Current: {cam.Current}");
    }
}
```

### **Tester Manuellement dans Godot**

1. Ouvrir `Restaurant.tscn`
2. Sélectionner `Title_Camera3D`
3. Dans l'Inspector, activer **Preview**
4. Vérifier que la vue est correcte pour le menu

### **Vérifier Unique Name**

1. Sélectionner `Title_Camera3D` dans la Scene Tree
2. Dans l'Inspector, vérifier **Access as Unique Name** (icône %)
3. Si pas activé, l'activer et sauvegarder la scène

---

## ?? Avantages du Système

### ? **Type-Safe**
- Utilisation d'enum `CameraType` évite les erreurs de typage
- IntelliSense suggère les valeurs possibles

### ? **Maintenable**
- Noms de caméras centralisés dans le switch
- Facile de modifier le mapping

### ? **Flexible**
- Ajout de nouveaux types de caméras simple
- Pas besoin de modifier l'interface `ILocation`

### ? **Découplé**
- MainGameScene n'a pas besoin de connaître les noms exacts des caméras
- Utilise l'abstraction `CameraType`

---

## ?? Extensions Futures

### **1. Transitions Animées**

```csharp
public async Task SetActiveCameraWithTransition(CameraType targetType, float duration = 1.0f)
{
    // Interpoler position/rotation entre caméra actuelle et cible
    // Utiliser Tween pour smooth transition
}
```

### **2. Stack de Caméras**

```csharp
private Stack<CameraType> _cameraStack = new();

public void PushCamera(CameraType type)
{
    _cameraStack.Push(_currentCameraType);
    SetActiveCamera(type);
}

public void PopCamera()
{
    if (_cameraStack.Count > 0)
    {
        var previousType = _cameraStack.Pop();
        SetActiveCamera(previousType);
    }
}
```

### **3. Événements de Changement de Caméra**

```csharp
public event Action<CameraType, CameraType> CameraChanged;

public bool SetActiveCamera(CameraType cameraType)
{
    var oldType = _currentCameraType;
    // ... changement de caméra ...
    CameraChanged?.Invoke(oldType, cameraType);
    return true;
}
```

---

## ?? Cas d'Usage par Caméra

| CameraType | Usage | Scènes Typiques |
|------------|-------|-----------------|
| **Lobby** | Vue du lobby d'attente | Multiplayer lobby, salle d'attente |
| **Title** | Vue du menu principal | Menu titre, options, crédits |
| **MainGame** | Vue de jeu normale | Gameplay actif, exploration |
| **Cinematic** | Cutscenes, animations | Intros, transitions, dialogues |

---

## ? Checklist de Configuration

Pour ajouter une nouvelle caméra dans une location :

- [ ] Créer un node `Camera3D` dans Godot
- [ ] Nommer selon convention : `{Type}_Camera3D`
- [ ] Activer **Access as Unique Name** (%)
- [ ] Positionner et orienter la caméra
- [ ] Configurer FOV, Near, Far
- [ ] Ajouter le type dans l'enum `CameraType` (si nouveau)
- [ ] Ajouter le mapping dans le `switch` de `SetActiveCamera`
- [ ] Tester avec `SetActiveCamera(CameraType.NouveauType)`

---

## ?? Conclusion

Le système de gestion de caméras via `CameraType` et `SetActiveCamera()` offre une solution simple, type-safe et maintenable pour contrôler les vues dans les locations du jeu.

**Avantages clés** :
- ?? Type-safe avec enum
- ?? Facile à étendre
- ?? Découplé et maintenable
- ?? Intégration transparente avec Godot

Le système est maintenant prêt pour gérer toutes les transitions de caméras du jeu ! ???
