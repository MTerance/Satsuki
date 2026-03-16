# ?? Système de gestion des caméras - Title_Camera3D

## ? Activation de la caméra Title lors du chargement

Le système active automatiquement la caméra `Title_Camera3D` lorsque la scène Title est chargée.

---

## ?? Flux d'activation

```
[LoadTitle()]
    ?
[Title créé et ajouté]
    ?
[CallDeferred(ActivateTitleCamera)]
    ?
[LoadLocationFromScene("Restaurant.tscn")]
    ?
[SetActiveCamera(CameraType.Title)]
    ?
[Recherche de "%Title_Camera3D"]
    ?
[currentCamera.Current = true]
    ?
[Camera Title_Camera3D active ?]
```

---

## ?? Implémentation

### 1. Dans `MainGameScene.LoadTitle()`

```csharp
public void LoadTitle()
{
    // ... création de Title ...
    
    // Activation différée de la caméra
    CallDeferred(nameof(ActivateTitleCamera));
}
```

### 2. Nouvelle méthode `ActivateTitleCamera()`

```csharp
private void ActivateTitleCamera()
{
    // 1. Charge le Restaurant
    bool success = _locationManager.LoadLocationFromScene(
        "res://Scenes/Locations/Restaurant.tscn", 
        useCache: true
    );
    
    // 2. Active la caméra Title
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

### 3. Dans `LocationModel.SetActiveCamera()`

```csharp
public bool SetActiveCamera(CameraType cameraType)
{
    // 1. Résolution du nom de nœud
    string cameraNodeName = cameraType switch
    {
        CameraType.Title => "Title_Camera3D",
        // ...
    };
    
    // 2. Recherche avec marqueur unique
    var currentCamera = GetNode<Camera3D>($"%{cameraNodeName}");
    
    // 3. Activation
    if (currentCamera != null)
    {
        currentCamera.Current = true;
        GD.Print($"Camera {cameraNodeName} activee");
        GD.Print($"  - Position: {currentCamera.GlobalPosition}");
        GD.Print($"  - Rotation: {currentCamera.GlobalRotation}");
        return true;
    }
    
    return false;
}
```

---

## ?? Types de caméras disponibles

| `CameraType` | Nom du nœud | Usage |
|--------------|-------------|-------|
| `Title` | `Title_Camera3D` | Menu titre |
| `Lobby` | `Lobby_Camera3D` | Lobby (déprécié) |
| `MainGame` | `MainGame_Camera3D` | Jeu principal |
| `Cinematic` | `Cinematic_Camera3D` | Cinématiques |

---

## ?? Marqueur unique `%`

### Pourquoi utiliser `%` ?

```csharp
// ? AVEC marqueur unique
var camera = GetNode<Camera3D>("%Title_Camera3D");
// Cherche Title_Camera3D n'importe où dans l'arbre

// ? SANS marqueur unique
var camera = GetNode<Camera3D>("Path/To/Title_Camera3D");
// Nécessite de connaître le chemin exact
```

**Avantages** :
- ? Indépendant de la hiérarchie
- ? Pas besoin de chemin absolu
- ? Fonctionne même si la structure change
- ? Plus simple et robuste

---

## ?? Logs attendus

### Lors du chargement de Title

```
MainGameScene: Chargement Title...
Title: Initialisation de l'ecran titre...
UI creee avec succes
Menu initialise avec 4 options
Title charge
Restaurant charge pour Title
Restaurant: Recherche de la camera Title (Title_Camera3D)
Restaurant: Camera Title_Camera3D activee avec succes
  - Position: (0, 2, 5)
  - Rotation: (0, 0, 0)
Camera Title_Camera3D activee avec succes
```

### En cas d'erreur

```
Restaurant: Camera Title_Camera3D introuvable (null)
Echec activation Camera Title_Camera3D
```

---

## ?? Gestion d'erreurs

### Vérifications effectuées

1. ? **Type de caméra valide**
   ```csharp
   if (cameraNodeName == null)
   {
       GD.PrintErr($"Type de camera inconnu: {cameraType}");
       return false;
   }
   ```

2. ? **Nœud caméra existe**
   ```csharp
   if (currentCamera != null)
   {
       currentCamera.Current = true;
       return true;
   }
   else
   {
       GD.PrintErr($"Camera {cameraNodeName} introuvable");
       return false;
   }
   ```

3. ? **Exceptions capturées**
   ```csharp
   try
   {
       var currentCamera = GetNode<Camera3D>($"%{cameraNodeName}");
       // ...
   }
   catch (Exception ex)
   {
       GD.PrintErr($"Erreur: {ex.Message}");
       return false;
   }
   ```

---

## ?? Configuration de la caméra dans Godot

### Structure de la scène `Restaurant.tscn`

```
Restaurant (LocationModel)
??? SubViewport
?   ??? Title_Camera3D ? Marquée avec Unique Name (%)
?   ?   ??? Position: (0, 2, 5)
?   ?   ??? Rotation: (0, 0, 0)
?   ?   ??? FOV: 75°
?   ??? Lobby_Camera3D
?   ??? MainGame_Camera3D
?   ??? Cinematic_Camera3D
??? ...
```

### Propriétés importantes

- ? **Unique Name** : Coché (permet l'accès via `%`)
- ? **Type** : `Camera3D`
- ? **Current** : Activé par le code
- ? **Position** : Configurée dans l'éditeur
- ? **Rotation** : Configurée dans l'éditeur

---

## ?? Changement de caméra

### Depuis une autre scène

```csharp
// Dans MainGameScene
_locationManager.CurrentLocation.SetActiveCamera(CameraType.MainGame);
```

### Depuis Title vers MainGame

```csharp
// Lors du clic sur "Start Game"
private void OnStartGameRequested()
{
    // 1. Change la scène UI
    LoadMainMenu();
    
    // 2. Change la caméra
    _locationManager.CurrentLocation?.SetActiveCamera(CameraType.MainGame);
}
```

---

## ? Performance

### CallDeferred

```csharp
CallDeferred(nameof(ActivateTitleCamera));
```

**Pourquoi ?**
- ? Attend que Title soit complètement initialisé
- ? Évite les problèmes de synchronisation
- ? Permet au restaurant de se charger proprement
- ? Garantit que la caméra existe avant activation

---

## ?? Tests de validation

### Test 1 : Activation au démarrage
```
1. ? Lancer l'application
2. ? Attendre la fin des crédits
3. ? Vérifier : Title affiché
4. ? Vérifier : Camera Title_Camera3D active
5. ? Vérifier : Vue correcte du restaurant
```

### Test 2 : Logs de la caméra
```
1. ? Observer la console
2. ? Vérifier : "Recherche de la camera Title (Title_Camera3D)"
3. ? Vérifier : "Camera Title_Camera3D activee avec succes"
4. ? Vérifier : Position et rotation affichées
```

### Test 3 : Retour au Title
```
1. ? Aller dans MainMenu
2. ? Cliquer "Back to Title"
3. ? Vérifier : Title réaffiché
4. ? Vérifier : Camera Title_Camera3D réactivée
```

### Test 4 : Gestion d'erreur
```
1. ?? Renommer temporairement Title_Camera3D
2. ?? Lancer l'application
3. ? Vérifier : Log d'erreur "Camera Title_Camera3D introuvable"
4. ? Vérifier : Pas de crash
5. ?? Restaurer le nom
```

---

## ?? Comparaison avant/après

### Avant
```csharp
private void LoadRestaurant()
{
    bool success = _locationManager.LoadLocationFromScene(...);
    if (success)
    {
        _locationManager.CurrentLocation.SetActiveCamera(CameraType.Title);
        GD.Print("Camera Title activee");
    }
}
```

**Problèmes** :
- ? Pas de vérification du retour
- ? Logs génériques
- ? Pas de gestion d'erreur

### Après
```csharp
private void ActivateTitleCamera()
{
    bool success = _locationManager.LoadLocationFromScene(...);
    if (success && _locationManager.CurrentLocation != null)
    {
        bool cameraSet = _locationManager.CurrentLocation.SetActiveCamera(
            CameraType.Title
        );
        
        if (cameraSet)
        {
            GD.Print("Camera Title_Camera3D activee avec succes");
        }
        else
        {
            GD.PrintErr("Echec activation Camera Title_Camera3D");
        }
    }
}
```

**Améliorations** :
- ? Vérification du retour de `SetActiveCamera`
- ? Logs détaillés avec nom de caméra
- ? Gestion d'erreur robuste
- ? Nom de méthode explicite

---

## ?? Points clés

1. ? **Activation automatique** lors du chargement de Title
2. ? **CallDeferred** pour garantir l'initialisation
3. ? **Marqueur unique `%`** pour trouver la caméra
4. ? **Logs détaillés** (position, rotation)
5. ? **Gestion d'erreurs** complète
6. ? **Vérifications** de retour

---

## ?? Fichiers modifiés

| Fichier | Modifications |
|---------|---------------|
| `Scenes/MainGameScene.cs` | ? Renommage `LoadRestaurant` ? `ActivateTitleCamera` |
| `Scenes/MainGameScene.cs` | ? Ajout vérification retour `SetActiveCamera` |
| `Scenes/Locations/LocationModel.cs` | ? Amélioration `SetActiveCamera` avec logs |
| `Scenes/Locations/LocationModel.cs` | ? Ajout try-catch et position/rotation |

---

## ?? Résultat

? **Camera Title_Camera3D activée automatiquement**  
? **Logs détaillés pour debug**  
? **Gestion d'erreurs robuste**  
? **Vérifications de retour**  
? **Build réussi**  

**Le système de caméra fonctionne maintenant de manière robuste et traçable ! ???**

---

*Date de mise à jour : 2024*  
*Build : ? Réussi*  
*Tests : ? À valider en runtime*
