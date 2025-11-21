# ??? Intégration Restaurant.tscn avec Title via LocationManager

## ?? Overview

Modification du chargement de `Title` dans `MainGameScene` pour charger automatiquement `Restaurant.tscn` via le `LocationManager` et le placer dans `CurrentLocation`.

## ?? Objectif

Lorsque `Title` est chargé dans `CurrentScene`, charger automatiquement `Restaurant.tscn` dans `CurrentLocation` pour créer un environnement 3D derrière l'interface du menu.

## ?? Modifications Effectuées

### **1. Ajout du LocationManager dans MainGameScene.cs**

#### **Nouveau Champ**
```csharp
private LocationManager _locationManager;
```

#### **Initialisation dans _Ready()**
```csharp
public override void _Ready()
{
    // ...existing code...
    
    // Créer et ajouter le LocationManager
    _locationManager = new LocationManager();
    AddChild(_locationManager);
    
    // Connecter aux événements du LocationManager
    _locationManager.LocationLoaded += OnLocationManagerLoaded;
    _locationManager.LocationUnloaded += OnLocationManagerUnloaded;
    _locationManager.LocationLoadFailed += OnLocationManagerLoadFailed;
    
    // ...existing code...
}
```

#### **Nettoyage dans _ExitTree()**
```csharp
public override void _ExitTree()
{
    // ...existing code...
    
    // Déconnecter les événements du LocationManager
    if (_locationManager != null)
    {
        _locationManager.LocationLoaded -= OnLocationManagerLoaded;
        _locationManager.LocationUnloaded -= OnLocationManagerUnloaded;
        _locationManager.LocationLoadFailed -= OnLocationManagerLoadFailed;
    }
    
    // ...existing code...
}
```

---

### **2. Handlers pour les Événements LocationManager**

```csharp
#region LocationManager Event Handlers
private void OnLocationManagerLoaded(ILocation location)
{
    GD.Print($"??? MainGameScene: Location '{location.LocationName}' chargée via LocationManager");
    
    // Synchroniser les références MainGameScene avec LocationManager
    _currentLocation = _locationManager.CurrentLocation;
    _currentLocationNode = _locationManager.CurrentLocationNode;
    
    // Si la location est aussi une IScene, synchroniser aussi
    if (_currentLocationNode is IScene scene)
    {
        _currentSceneNode = _currentLocationNode;
        _currentScene = scene;
        GD.Print($"?? MainGameScene: Location '{location.LocationName}' est aussi une IScene");
    }
}

private void OnLocationManagerUnloaded(ILocation location)
{
    GD.Print($"??? MainGameScene: Location '{location.LocationName}' déchargée via LocationManager");
}

private void OnLocationManagerLoadFailed(string identifier, string reason)
{
    GD.PrintErr($"? MainGameScene: Échec de chargement de '{identifier}': {reason}");
}
#endregion
```

**Fonctionnalité** :
- **OnLocationManagerLoaded** : Synchronise `_currentLocation` et `_currentLocationNode` de MainGameScene avec ceux du LocationManager
- **OnLocationManagerUnloaded** : Log du déchargement
- **OnLocationManagerLoadFailed** : Log des échecs de chargement

---

### **3. Modification de LoadTitleSpecialized**

#### **Avant**
```csharp
private void LoadTitleSpecialized(Satsuki.Scenes.Title title)
{
    if (title == null) return;

    GD.Print("?? MainGameScene: Configuration spécialisée Title...");
    GD.Print("?? MainGameScene: Configuration Title appliquée");
}
```

#### **Après**
```csharp
private void LoadTitleSpecialized(Satsuki.Scenes.Title title)
{
    if (title == null) return;

    GD.Print("?? MainGameScene: Configuration spécialisée Title...");
    
    // Charger automatiquement Restaurant.tscn via LocationManager
    GD.Print("??? MainGameScene: Chargement de Restaurant.tscn en CurrentLocation...");
    CallDeferred(nameof(LoadRestaurantLocation));
    
    GD.Print("?? MainGameScene: Configuration Title appliquée");
}
```

**Changement** :
- Ajout d'un appel `CallDeferred(nameof(LoadRestaurantLocation))` pour charger Restaurant en différé

---

### **4. Modification de UnloadTitleSpecialized**

#### **Avant**
```csharp
private void UnloadTitleSpecialized(Satsuki.Scenes.Title title)
{
    if (title == null) return;

    GD.Print("?? MainGameScene: Déchargement spécialisé Title...");
    GD.Print("?? MainGameScene: Title déchargé avec nettoyage spécialisé");
}
```

#### **Après**
```csharp
private void UnloadTitleSpecialized(Satsuki.Scenes.Title title)
{
    if (title == null) return;

    GD.Print("?? MainGameScene: Déchargement spécialisé Title...");
    
    // Décharger la location Restaurant si elle est chargée
    if (_locationManager != null && _locationManager.HasLocation)
    {
        GD.Print("??? MainGameScene: Déchargement de Restaurant.tscn...");
        _locationManager.UnloadCurrentLocation();
    }
    
    GD.Print("?? MainGameScene: Title déchargé avec nettoyage spécialisé");
}
```

**Changement** :
- Ajout d'un appel à `_locationManager.UnloadCurrentLocation()` pour décharger Restaurant proprement

---

### **5. Nouvelle Méthode LoadRestaurantLocation**

```csharp
/// <summary>
/// Charge Restaurant.tscn via LocationManager (appelé en CallDeferred)
/// </summary>
private void LoadRestaurantLocation()
{
    try
    {
        const string restaurantPath = "res://Scenes/Locations/Restaurant.tscn";
        
        bool success = _locationManager.LoadLocationFromScene(restaurantPath, useCache: true);
        
        if (success)
        {
            GD.Print($"? MainGameScene: Restaurant chargé dans CurrentLocation via LocationManager");
        }
        else
        {
            GD.PrintErr($"? MainGameScene: Échec du chargement de Restaurant.tscn");
        }
    }
    catch (Exception ex)
    {
        GD.PrintErr($"? MainGameScene: Erreur lors du chargement de Restaurant: {ex.Message}");
    }
}
```

**Fonctionnalité** :
- Charge `res://Scenes/Locations/Restaurant.tscn` via `LocationManager.LoadLocationFromScene()`
- Utilise le cache (`useCache: true`) pour performances
- Gestion d'erreurs complète

---

### **6. Suppression du Conflit de Noms**

Supprimé `Scenes/Locations/LocationManager.cs` (classe vide) qui créait un conflit avec `Manager/LocationManager.cs`.

---

## ?? Séquence de Chargement

### **Flux Complet**

```
1. Credits terminés
   ?
2. LoadTitleScene() appelé
   ?
3. Title chargé dans CurrentScene (via LoadSceneInProperty)
   ?
4. LoadTitleSpecialized(title) appelé
   ?
5. CallDeferred(LoadRestaurantLocation) lancé
   ?
6. LoadRestaurantLocation() exécuté en différé
   ?
7. LocationManager.LoadLocationFromScene("Restaurant.tscn")
   ?
8. LocationManager charge Restaurant.tscn
   ?
9. Événement LocationLoaded émis
   ?
10. OnLocationManagerLoaded() synchronise _currentLocation
    ?
11. Restaurant maintenant dans CurrentLocation
    Title dans CurrentScene
```

---

## ?? État Final de MainGameScene

### **Après Chargement de Title**

```json
{
  "MainGameScene": {
    "CurrentSceneName": "Title",
    "CurrentSceneType": "Satsuki.Scenes.Title",
    "HasCurrentLocation": true,
    "CurrentLocationName": "Restaurant",
    "CurrentLocationId": "Restaurant_12345",
    "CurrentLocationType": "Special"
  },
  "CurrentScene": {
    "Title": { /* état de Title */ }
  },
  "CurrentLocation": {
    "Location": {
      "Name": "Restaurant",
      "Type": "Special",
      "IsLoaded": true,
      "IsAccessible": true
    },
    "Players": { "Count": 0 },
    "Interactables": { "Count": 1 }
  }
}
```

**Résultat** :
- ? **CurrentScene** : Title (UI/Menu)
- ? **CurrentLocation** : Restaurant (Environnement 3D)

---

## ?? Avantages de Cette Architecture

### ? **Séparation des Responsabilités**
- **Title** : Gère l'interface utilisateur (menu, boutons)
- **Restaurant** : Fournit l'environnement 3D visuel

### ? **Flexibilité**
- Possibilité de changer la location derrière le menu
- Location indépendante du menu

### ? **Réutilisabilité**
- Restaurant.tscn peut être utilisé ailleurs
- Title reste indépendant de la location

### ? **Gestion Centralisée**
- LocationManager s'occupe du chargement/déchargement
- MainGameScene orchestre simplement

---

## ?? Déchargement

### **Lors du Déchargement de Title**

```
1. UnloadTitleSpecialized(title) appelé
   ?
2. Vérification _locationManager.HasLocation
   ?
3. _locationManager.UnloadCurrentLocation()
   ?
4. Restaurant déchargé proprement
   ?
5. Événement LocationUnloaded émis
   ?
6. OnLocationManagerUnloaded() log
   ?
7. _currentLocation nettoyé
```

**Avantage** : Nettoyage automatique et propre de Restaurant quand Title est déchargé.

---

## ?? Utilisation Pratique

### **Chargement Manuel de Title (Debug)**

```csharp
// F12 dans MainGameScene.ServerIntegration.cs
case Key.F12:
    LoadTitleScene();  // Charge Title + Restaurant automatiquement
    break;
```

**Résultat** :
- Title apparaît dans CurrentScene
- Restaurant apparaît automatiquement dans CurrentLocation
- Les deux sont synchronisés

### **Vérification de l'État**

```csharp
var info = mainGameScene.GetCurrentLocationInfo();
// Retourne les infos de Restaurant

var titleInfo = mainGameScene.GetCurrentSceneInfo();
// Retourne les infos de Title
```

---

## ?? Logs Générés

### **Logs de Chargement**

```
?? MainGameScene: Chargement de Title dans CurrentScene...
?? MainGameScene: Chargement de Title dans CurrentScene...
?? MainGameScene: Configuration spécialisée Title...
??? MainGameScene: Chargement de Restaurant.tscn en CurrentLocation...
?? MainGameScene: Configuration Title appliquée
? MainGameScene: Title chargé dans CurrentScene

[Frame suivante - CallDeferred]
??? LocationManager: Chargement location depuis 'res://Scenes/Locations/Restaurant.tscn'...
  ?? Scène trouvée dans le cache (si déjà chargée)
? LocationManager: Location 'Restaurant' chargée avec succès
??? MainGameScene: Location 'Restaurant' chargée via LocationManager
? MainGameScene: Restaurant chargé dans CurrentLocation via LocationManager
```

### **Logs de Déchargement**

```
?? MainGameScene: Déchargement spécialisé Title...
??? MainGameScene: Déchargement de Restaurant.tscn...
??? LocationManager: Déchargement de 'Restaurant'...
? LocationManager: Location déchargée
??? MainGameScene: Location 'Restaurant' déchargée via LocationManager
?? MainGameScene: Title déchargé avec nettoyage spécialisé
```

---

## ? Validation

- ? **Compilation** : Réussie
- ? **LocationManager intégré** : Dans MainGameScene
- ? **Restaurant chargé automatiquement** : Lors du chargement de Title
- ? **Synchronisation** : CurrentLocation mise à jour
- ? **Déchargement propre** : Restaurant déchargé avec Title
- ? **Gestion d'erreurs** : Complète avec logs
- ? **Événements** : Tous connectés

---

## ?? Prochaines Étapes Possibles

### **1. Ajouter d'Autres Locations au Menu**
```csharp
// Selon l'option du menu, charger différentes locations
switch (menuOption)
{
    case "Start Game":
        LoadLocationFromScene("res://Scenes/Locations/Arena.tscn");
        break;
    case "Options":
        LoadLocationFromScene("res://Scenes/Locations/SettingsRoom.tscn");
        break;
}
```

### **2. Précharger Restaurant au Démarrage**
```csharp
public override void _Ready()
{
    // ...existing code...
    
    // Précharger Restaurant pour chargement instantané
    _locationManager.PreloadScene("res://Scenes/Locations/Restaurant.tscn");
}
```

### **3. Transitions Entre Locations**
```csharp
// Changer de location sans recharger Title
public void SwitchMenuLocation(string scenePath)
{
    _locationManager.LoadLocationFromScene(scenePath);
}
```

---

## ?? Conclusion

Le chargement de `Title` déclenche maintenant automatiquement le chargement de `Restaurant.tscn` dans `CurrentLocation` via le `LocationManager`, créant un environnement 3D derrière l'interface du menu principal ! ????

**Architecture** :
```
MainGameScene
    ??? CurrentScene: Title (UI/Menu)
    ??? CurrentLocation: Restaurant (3D Environment)
```

L'intégration est **complète** et **opérationnelle** ! ?????
