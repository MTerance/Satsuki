# ??? Propriété CurrentLocation dans MainGameScene

## ?? Overview

Ajout de la propriété `ILocation CurrentLocation` dans `MainGameScene` pour gérer spécifiquement les locations en complément de la propriété `CurrentScene` existante. Cette architecture permet une gestion granulaire des scènes (via `IScene`) et des locations (via `ILocation`) de manière indépendante ou combinée.

## ?? Objectifs de CurrentLocation

### **Gestion Dual Scene/Location**
- `CurrentScene` : Gestion générale des scènes (Credits, Title, Game, etc.)
- `CurrentLocation` : Gestion spécifique des locations (Intérieur, Extérieur, Combat, etc.)
- **Compatible** : Une même instance peut être les deux (LocationModel implémente IScene ET ILocation)

### **Architecture Flexible**
- Chargement indépendant de locations
- Gestion spécialisée des événements de location
- API dédiée aux fonctionnalités spatiales (joueurs, interactions, navigation)

## ??? Nouvelle Architecture MainGameScene

### **Double Propriété**
```csharp
public partial class MainGameScene : Node, IScene
{
    // Gestion générale des scènes
    private IScene _currentScene;
    private Node _currentSceneNode;
    
    // Gestion spécifique des locations
    private ILocation _currentLocation;
    private Node _currentLocationNode;
    
    public IScene CurrentScene { get => _currentScene; }
    public ILocation CurrentLocation { get => _currentLocation; }
}
```

### **Cas d'Usage Possibles**
1. **Scene seule** : Credits, Title (IScene uniquement)
2. **Location seule** : Chargement direct d'une location (ILocation uniquement)
3. **Scene + Location** : LocationModel (implémente les deux interfaces)

## ?? Méthodes de Gestion des Locations

### **1. Chargement de Location**
```csharp
/// <summary>
/// Charge une location dans la propriété CurrentLocation
/// </summary>
public void LoadLocationInProperty(Type locationType)
{
    // Vérification que le type implémente ILocation
    if (!typeof(ILocation).IsAssignableFrom(locationType))
        return;

    // Déchargement de la location précédente
    UnloadCurrentLocationSpecialized();

    // Création et ajout de la nouvelle location
    var locationInstance = Activator.CreateInstance(locationType) as Node;
    if (locationInstance is ILocation location)
    {
        AddChild(locationInstance);
        _currentLocationNode = locationInstance;
        _currentLocation = location;
        
        // Si c'est aussi une IScene, l'assigner aussi
        if (locationInstance is IScene scene)
        {
            _currentSceneNode = locationInstance;
            _currentScene = scene;
        }
        
        LoadLocationSpecialized(location, locationType);
    }
}
```

### **2. Configuration Spécialisée par Type de Location**
```csharp
private void LoadLocationSpecialized(ILocation location, Type locationType)
{
    // Connexion automatique des événements
    location.LocationLoaded += OnLocationLoaded;
    location.PlayerEntered += OnPlayerEnteredLocation;
    location.InteractionOccurred += OnLocationInteractionOccurred;

    // Initialisation et chargement
    if (!location.IsLoaded)
    {
        location.Initialize();
        location.LoadLocation();
    }

    // Configuration selon le type de location
    switch (location.Type)
    {
        case LocationType.Interior:
            ConfigureInteriorLocation(location);
            break;
        case LocationType.Combat:
            ConfigureCombatLocation(location);
            break;
        // ... autres types
    }
}
```

### **3. Méthodes de Configuration par Type**
```csharp
private void ConfigureInteriorLocation(ILocation location)
{
    GD.Print($"?? Configuration location intérieur {location.LocationName}");
    // Paramètres spécifiques aux intérieurs
}

private void ConfigureCombatLocation(ILocation location)
{
    GD.Print($"?? Configuration location combat {location.LocationName}");
    // Paramètres spécifiques au combat
}

// ConfigureExteriorLocation, ConfigureSocialLocation, ConfigureShopLocation...
```

## ?? Gestion des Événements de Location

### **Événements Connectés Automatiquement**
```csharp
// Lors du chargement d'une location
location.LocationLoaded += OnLocationLoaded;
location.LocationUnloaded += OnLocationUnloaded;
location.PlayerEntered += OnPlayerEnteredLocation;
location.PlayerExited += OnPlayerExitedLocation;
location.InteractionOccurred += OnLocationInteractionOccurred;
```

### **Callbacks d'Événements**
```csharp
private void OnPlayerEnteredLocation(ILocation location, string playerId)
{
    GD.Print($"?? Joueur {playerId} entre dans {location.LocationName}");
    
    // Notifier le serveur et les autres clients
    _gameServerHandler?.BroadcastToAllClients(
        $"LOCATION_ENTER:{playerId}:{location.LocationId}", true);
}

private void OnLocationInteractionOccurred(ILocation location, string playerId, string interactionId)
{
    GD.Print($"?? Interaction {interactionId} par {playerId} dans {location.LocationName}");
    
    // Notifier le serveur
    _gameServerHandler?.BroadcastToAllClients(
        $"LOCATION_INTERACTION:{playerId}:{location.LocationId}:{interactionId}", true);
}
```

## ?? État Enrichi avec CurrentLocation

### **GetSceneState() Mis à Jour**
```csharp
public object GetSceneState()
{
    // État CurrentScene (existant)
    object currentSceneState = _currentScene?.GetSceneState();
    
    // État CurrentLocation (nouveau)
    object currentLocationState = _currentLocation?.GetLocationState();

    return new
    {
        MainGameScene = new
        {
            // Info Scene
            HasCurrentScene = _currentScene != null,
            CurrentSceneName = currentSceneName,
            
            // Info Location (nouveau)
            HasCurrentLocation = _currentLocation != null,
            CurrentLocationName = _currentLocation?.LocationName ?? "None",
            CurrentLocationId = _currentLocation?.LocationId ?? "None",
            CurrentLocationType = _currentLocation?.Type.ToString() ?? "None"
        },
        CurrentScene = currentSceneState,
        CurrentLocation = currentLocationState,  // Nouveau
        Debug = { DebugMode, Timestamp }
    };
}
```

### **Exemple d'État Retourné**
```json
{
  "MainGameScene": {
    "HasCurrentScene": true,
    "CurrentSceneName": "LocationModel",
    "HasCurrentLocation": true,
    "CurrentLocationName": "LocationModel",
    "CurrentLocationId": "LocationModel_12345",
    "CurrentLocationType": "Special"
  },
  "CurrentScene": {
    "SceneInfo": { /* État IScene */ }
  },
  "CurrentLocation": {
    "Location": {
      "Name": "LocationModel",
      "Type": "Special",
      "IsLoaded": true,
      "IsAccessible": true
    },
    "Players": {
      "Count": 1,
      "PlayerIds": ["TestPlayer"]
    },
    "Interactables": {
      "Count": 1,
      "Available": 1
    }
  }
}
```

## ?? API Publique pour Locations

### **Gestion des Joueurs**
```csharp
/// <summary>
/// Fait entrer un joueur dans la location courante
/// </summary>
public void PlayerEnterCurrentLocation(string playerId)

/// <summary>
/// Fait sortir un joueur de la location courante
/// </summary>
public void PlayerExitCurrentLocation(string playerId)

/// <summary>
/// Obtient les joueurs présents dans la location courante
/// </summary>
public string[] GetPlayersInCurrentLocation()
```

### **Gestion des Interactions**
```csharp
/// <summary>
/// Traite une interaction dans la location courante
/// </summary>
public void ProcessLocationInteraction(string playerId, string interactionId, object data = null)

/// <summary>
/// Obtient les objets interactables de la location courante
/// </summary>
public IInteractable[] GetCurrentLocationInteractables()
```

### **Chargement et Information**
```csharp
/// <summary>
/// Charge une location personnalisée
/// </summary>
public void LoadCustomLocation(Type locationType)

/// <summary>
/// Charge une location par nom de classe
/// </summary>
public void LoadLocationByClassName(string locationClassName)

/// <summary>
/// Obtient des informations détaillées sur la location courante
/// </summary>
public object GetCurrentLocationInfo()

/// <summary>
/// Décharge la location courante
/// </summary>
public void UnloadCurrentLocation()
```

## ?? Commandes Debug Étendues

### **Nouvelles Commandes Clavier**
```csharp
Key.Home    // Charger LocationModel de test
Key.End     // Décharger CurrentLocation
Key.Menu    // Afficher infos CurrentLocation
Key.Minus   // Faire entrer TestPlayer
Key.Equal   // Lister joueurs présents
Key.Backspace // Lister interactables
```

### **Exemples d'Usage Debug**
```
[Home]      ??? LocationModel chargée dans CurrentLocation
[Minus]     ?? TestPlayer entre dans CurrentLocation
[Equal]     ?? Joueurs dans CurrentLocation: TestPlayer
[Backspace] ?? Interactables dans CurrentLocation: 1
            - Écran Média (MediaScreen_12345)
[Menu]      ??? Info CurrentLocation: { "HasLocation": true, ... }
[End]       ??? CurrentLocation déchargée
```

## ?? Flux d'Utilisation

### **Cas 1 : Scene + Location Combinée (LocationModel)**
```
LoadSceneInProperty(typeof(LocationModel))
    ?
LocationModel créée ? Ajouter comme enfant
    ?
Assigner à CurrentScene (IScene) ET CurrentLocation (ILocation)
    ?
LoadSceneSpecialized() détecte que c'est aussi ILocation
    ?
LoadLocationSpecialized() configure la location
    ?
Événements connectés, location initialisée et activée
```

### **Cas 2 : Location Seule**
```
LoadLocationInProperty(typeof(MyLocation))
    ?
MyLocation créée ? Ajouter comme enfant
    ?
Assigner à CurrentLocation uniquement
    ?
LoadLocationSpecialized() configure la location
    ?
Location prête pour joueurs et interactions
```

### **Cas 3 : Transition Scene ? Location**
```
Credits terminés ? LoadTitleScene()
    ?
Title chargé dans CurrentScene
    ?
Utilisateur démarre jeu ? LoadLocationByClassName("GameLocation")
    ?
GameLocation chargé dans CurrentLocation
    ?
CurrentScene (Title) + CurrentLocation (GameLocation) actifs
```

## ??? Gestion des Cas Edge

### **Location = Scene (LocationModel)**
```csharp
// Dans LoadSceneInProperty
if (sceneInstance is ILocation location)
{
    _currentLocationNode = sceneInstance;
    _currentLocation = location;
    GD.Print($"??? {sceneType.Name} est aussi une ILocation");
}

// Dans UnloadCurrentSceneSpecialized
if (_currentSceneNode is ILocation)
{
    // Ne pas décharger ici, sera géré par UnloadCurrentLocationSpecialized
    return;
}
```

### **Nettoyage Synchronisé**
```csharp
private void UnloadCurrentLocationSpecialized()
{
    // Déconnexion des événements location
    _currentLocation.LocationLoaded -= OnLocationLoaded;
    
    // Si la location était aussi la CurrentScene
    if (_currentSceneNode == _currentLocationNode)
    {
        _currentSceneNode = null;
        _currentScene = null;
    }
    
    // Nettoyage de la location
    _currentLocationNode = null;
    _currentLocation = null;
}
```

### **Cleanup Complet**
```csharp
public override void _ExitTree()
{
    // Ordre important : Location puis Scene
    UnloadCurrentLocation();
    UnloadCurrentScene();
    
    // Puis serveur
    // Déconnexion gestionnaire serveur...
}
```

## ?? Avantages de l'Architecture

### ? **Séparation des Responsabilités**
- **CurrentScene** : Gestion générale (UI, menus, workflows)
- **CurrentLocation** : Gestion spatiale (joueurs, interactions, navigation)

### ? **Flexibilité Maximale**
- Chargement indépendant ou combiné
- API spécialisée pour chaque usage
- Configuration adaptée par type

### ? **Compatibilité Rétroactive**
- CurrentScene continue de fonctionner
- LocationModel fonctionne dans les deux systèmes
- API existante préservée

### ? **Extensibilité**
- Facile d'ajouter de nouveaux types de locations
- Configuration spécialisée par LocationType
- Événements pour intégration externe

## ?? Extensions Futures

### **Gestion Multi-Location**
```csharp
private Dictionary<string, ILocation> _loadedLocations = new();

public void LoadLocationInBackground(string locationId, Type locationType)
{
    // Charger sans activer
    var location = CreateLocationInstance(locationType);
    location.Initialize();
    location.LoadLocation();
    _loadedLocations[locationId] = location;
}

public void SwitchToLoadedLocation(string locationId)
{
    // Transition instantanée
    if (_loadedLocations.TryGetValue(locationId, out var location))
    {
        UnloadCurrentLocation();
        _currentLocation = location;
        location.ActivateLocation();
    }
}
```

### **Système de Portails**
```csharp
public void HandlePortalTraversal(string playerId, string destinationLocationId)
{
    // Sortir de la location actuelle
    _currentLocation?.OnPlayerExit(playerId);
    
    // Charger la destination
    LoadLocationByClassName(destinationLocationId);
    
    // Entrer dans la nouvelle location
    _currentLocation?.OnPlayerEnter(playerId);
}
```

### **Streaming de Locations**
```csharp
public async Task<ILocation> LoadLocationAsync(Type locationType)
{
    // Chargement asynchrone avec callback
    var location = await Task.Run(() => CreateLocationInstance(locationType));
    CallDeferred(nameof(ActivateLoadedLocation), location);
    return location;
}
```

## ? Validation

### **Tests effectués**
- ? **Compilation réussie** : Toutes les méthodes compilent
- ? **CurrentLocation fonctionnelle** : Propriété accessible
- ? **LoadLocationInProperty** : Chargement spécialisé
- ? **Événements connectés** : Callbacks automatiques
- ? **API publique** : Méthodes de gestion des joueurs/interactions
- ? **Commandes debug** : Home, End, Menu, etc. fonctionnelles
- ? **État enrichi** : GetSceneState() inclut CurrentLocation

### **Scénarios testés**
1. **LocationModel** : Chargé comme Scene ET Location
2. **Location seule** : Via LoadLocationInProperty()
3. **Gestion joueurs** : Entrée/sortie avec événements
4. **Interactions** : Traitement via CurrentLocation
5. **Debug** : Commandes clavier pour tests
6. **Cleanup** : Déchargement propre des deux propriétés

La propriété `CurrentLocation` est maintenant pleinement intégrée dans `MainGameScene`, offrant une gestion granulaire et spécialisée des locations tout en conservant la compatibilité avec le système `CurrentScene` existant ! ??????