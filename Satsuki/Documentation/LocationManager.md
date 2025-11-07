# ??? LocationManager - Gestionnaire de Locations Godot

## ?? Overview

**LocationManager** est un gestionnaire centralisé qui s'occupe du chargement et déchargement des scènes Godot qui sont des `LocationModel`. Il simplifie la gestion des locations en fournissant une API unifiée et un système de cache.

## ?? Responsabilités

### ? **Chargement de Locations**
- Charger depuis un fichier `.tscn` (scène Godot)
- Charger par type (création programmatique)
- Charger par nom de type

### ? **Gestion du Cycle de Vie**
- Initialisation automatique
- Activation/désactivation
- Déchargement propre

### ? **Système de Cache**
- Cache des `PackedScene` pour performances
- Préchargement possible
- Gestion mémoire optimisée

### ? **Enregistrement des Types**
- Auto-découverte des locations disponibles
- Enregistrement manuel possible
- Liste des types enregistrés

### ? **Événements**
- `LocationLoaded` : Quand une location est chargée
- `LocationUnloaded` : Quand une location est déchargée
- `LocationLoadFailed` : Quand le chargement échoue

## ??? Architecture

### **Pattern Singleton**
```csharp
public partial class LocationManager : Node
{
    private static LocationManager _instance;
    public static LocationManager Instance => _instance;
}
```

**Accès** :
```csharp
LocationManager.Instance.LoadLocationFromScene("res://Scenes/Locations/MyLocation.tscn");
```

### **Champs Privés**
```csharp
private ILocation _currentLocation;                              // Location courante
private Node _currentLocationNode;                               // Node Godot de la location
private Dictionary<string, PackedScene> _cachedScenes;          // Cache de scènes
private Dictionary<string, Type> _registeredLocationTypes;      // Types enregistrés
```

## ?? Méthodes Principales

### **1. Chargement depuis Scène Godot**

#### **LoadLocationFromScene(scenePath, useCache)**
Charge une location depuis un fichier `.tscn`.

```csharp
bool success = LocationManager.Instance.LoadLocationFromScene(
    "res://Scenes/Locations/Lobby.tscn",
    useCache: true
);

if (success)
{
    GD.Print("Location chargée avec succès !");
}
```

**Paramètres** :
- `scenePath` : Chemin vers le fichier `.tscn`
- `useCache` : Utiliser le cache de scènes (défaut: `true`)

**Retour** : `bool` - `true` si succès, `false` sinon

**Processus** :
1. Décharge la location courante
2. Charge la `PackedScene` (depuis cache ou disque)
3. Instancie la scène
4. Vérifie que c'est une `ILocation`
5. Ajoute à l'arbre de scène
6. Connecte les événements
7. Initialise et active

---

### **2. Chargement par Type**

#### **LoadLocationByType(locationType)**
Charge une location par création d'instance programmatique.

```csharp
bool success = LocationManager.Instance.LoadLocationByType(typeof(LocationModel));
```

**Paramètres** :
- `locationType` : Type de la location à instancier

**Retour** : `bool` - `true` si succès, `false` sinon

**Processus** :
1. Vérifie que le type implémente `ILocation`
2. Vérifie que le type hérite de `Node`
3. Décharge la location courante
4. Crée une instance via `Activator.CreateInstance`
5. Ajoute à l'arbre et initialise

---

#### **LoadLocationByTypeName(typeName)**
Charge une location par son nom de type.

```csharp
// Depuis les types enregistrés
bool success = LocationManager.Instance.LoadLocationByTypeName("LocationModel");

// Ou avec namespace complet
success = LocationManager.Instance.LoadLocationByTypeName("Satsuki.Scenes.Locations.MyLocation");
```

**Paramètres** :
- `typeName` : Nom du type (court ou complet)

**Retour** : `bool` - `true` si succès, `false` sinon

**Recherche** :
1. Dans les types enregistrés
2. Dans l'assembly courant
3. Dans le namespace `Satsuki.Scenes.Locations`

---

### **3. Déchargement**

#### **UnloadCurrentLocation()**
Décharge la location courante de manière propre.

```csharp
LocationManager.Instance.UnloadCurrentLocation();
```

**Processus** :
1. Déconnecte les événements
2. Désactive la location
3. Décharge la location
4. Émet l'événement `LocationUnloaded`
5. Supprime le node de l'arbre
6. Nettoie les références

---

### **4. Gestion du Cache**

#### **PreloadScene(scenePath)**
Précharge une scène dans le cache pour chargement rapide ultérieur.

```csharp
LocationManager.Instance.PreloadScene("res://Scenes/Locations/BigLocation.tscn");
```

#### **ClearCache()**
Vide le cache de scènes.

```csharp
LocationManager.Instance.ClearCache();
```

#### **GetCachedSceneCount()**
Obtient le nombre de scènes en cache.

```csharp
int count = LocationManager.Instance.GetCachedSceneCount();
GD.Print($"Scènes en cache: {count}");
```

---

### **5. Enregistrement des Types**

#### **RegisterLocationType(name, type)**
Enregistre manuellement un type de location.

```csharp
LocationManager.Instance.RegisterLocationType("MyCustomLocation", typeof(MyCustomLocation));
```

#### **GetRegisteredLocationTypes()**
Obtient la liste des types enregistrés.

```csharp
string[] types = LocationManager.Instance.GetRegisteredLocationTypes();
foreach (var type in types)
{
    GD.Print($"Type disponible: {type}");
}
```

---

### **6. Gestion des Joueurs (Shortcuts)**

#### **PlayerEnter(playerId)**
```csharp
LocationManager.Instance.PlayerEnter("Player1");
```

#### **PlayerExit(playerId)**
```csharp
LocationManager.Instance.PlayerExit("Player1");
```

#### **GetPlayersInCurrentLocation()**
```csharp
string[] players = LocationManager.Instance.GetPlayersInCurrentLocation();
GD.Print($"Joueurs: {string.Join(", ", players)}");
```

---

### **7. Informations**

#### **GetCurrentLocationInfo()**
Obtient les informations complètes sur la location courante.

```csharp
var info = LocationManager.Instance.GetCurrentLocationInfo();
GD.Print($"Location: {info.LocationName}");
GD.Print($"Type: {info.LocationType}");
GD.Print($"Joueurs: {info.PlayersCount}");
```

**Retour** :
```json
{
  "HasLocation": true,
  "LocationName": "Lobby",
  "LocationId": "Lobby_12345",
  "LocationType": "Social",
  "LocationDescription": "Lobby principal",
  "IsLoaded": true,
  "IsAccessible": true,
  "LocationState": { /* ... */ },
  "NodePath": "/root/MainGameScene/LocationManager/Lobby",
  "IsReady": true,
  "PlayersCount": 2,
  "InteractablesCount": 3,
  "SpawnPointsCount": 9
}
```

## ?? Utilisation Pratique

### **Scénario 1 : Charger une Location depuis .tscn**

```csharp
// Dans un script
public override void _Ready()
{
    // Charger le Lobby depuis sa scène Godot
    bool success = LocationManager.Instance.LoadLocationFromScene(
        "res://Scenes/Locations/Lobby.tscn"
    );
    
    if (success)
    {
        GD.Print("Lobby chargé !");
        
        // Faire entrer un joueur
        LocationManager.Instance.PlayerEnter("Player1");
    }
}
```

### **Scénario 2 : Charger une Location Programmatiquement**

```csharp
// Charger LocationModel sans fichier .tscn
bool success = LocationManager.Instance.LoadLocationByType(typeof(LocationModel));

// Ou par nom
success = LocationManager.Instance.LoadLocationByTypeName("LocationModel");
```

### **Scénario 3 : Préchargement pour Performance**

```csharp
// Au démarrage du jeu, précharger les locations fréquentes
public override void _Ready()
{
    var manager = LocationManager.Instance;
    
    // Précharger
    manager.PreloadScene("res://Scenes/Locations/Lobby.tscn");
    manager.PreloadScene("res://Scenes/Locations/Arena.tscn");
    manager.PreloadScene("res://Scenes/Locations/Shop.tscn");
    
    GD.Print($"Scènes préchargées: {manager.GetCachedSceneCount()}");
}

// Plus tard, chargement instantané depuis le cache
public void GoToLobby()
{
    // Très rapide car déjà en cache
    LocationManager.Instance.LoadLocationFromScene("res://Scenes/Locations/Lobby.tscn");
}
```

### **Scénario 4 : Écouter les Événements**

```csharp
public override void _Ready()
{
    var manager = LocationManager.Instance;
    
    // S'abonner aux événements
    manager.LocationLoaded += OnLocationLoaded;
    manager.LocationUnloaded += OnLocationUnloaded;
    manager.LocationLoadFailed += OnLocationLoadFailed;
}

private void OnLocationLoaded(ILocation location)
{
    GD.Print($"? Location chargée: {location.LocationName}");
    
    // Configurer l'UI
    UpdateLocationUI(location);
    
    // Spawn le joueur
    SpawnPlayerInLocation(location);
}

private void OnLocationUnloaded(ILocation location)
{
    GD.Print($"??? Location déchargée: {location.LocationName}");
    
    // Nettoyer l'UI
    ClearLocationUI();
}

private void OnLocationLoadFailed(string identifier, string reason)
{
    GD.PrintErr($"? Échec de chargement: {identifier}");
    GD.PrintErr($"   Raison: {reason}");
    
    // Afficher un message d'erreur à l'utilisateur
    ShowErrorDialog($"Impossible de charger la location: {reason}");
}
```

### **Scénario 5 : Transition entre Locations**

```csharp
public async void TransitionToLocation(string scenePath)
{
    GD.Print($"?? Transition vers {scenePath}...");
    
    // Fade out
    await FadeOut();
    
    // Décharger l'ancienne location
    LocationManager.Instance.UnloadCurrentLocation();
    
    // Charger la nouvelle
    bool success = LocationManager.Instance.LoadLocationFromScene(scenePath);
    
    if (success)
    {
        // Fade in
        await FadeIn();
        
        // Spawn le joueur
        LocationManager.Instance.PlayerEnter("Player1");
    }
    else
    {
        GD.PrintErr("Échec de la transition");
    }
}
```

## ?? Intégration avec MainGameScene

Le LocationManager peut remplacer la logique de gestion des locations dans `MainGameScene.LocationManagement.cs` :

### **Avant (MainGameScene.LocationManagement.cs)**
```csharp
public void LoadLocationInProperty(Type locationType)
{
    // ~50 lignes de code de chargement
    // Gestion manuelle de l'arbre de scène
    // Gestion manuelle des événements
    // ...
}
```

### **Après (avec LocationManager)**
```csharp
public void LoadLocationInProperty(Type locationType)
{
    // Déléguer au LocationManager
    bool success = LocationManager.Instance.LoadLocationByType(locationType);
    
    if (success)
    {
        _currentLocation = LocationManager.Instance.CurrentLocation;
        _currentLocationNode = LocationManager.Instance.CurrentLocationNode;
    }
}
```

**Simplification** :
- ? Moins de code dans MainGameScene
- ? Logique centralisée
- ? Réutilisable ailleurs
- ? Plus facile à tester

## ?? Propriétés Publiques

```csharp
// Location courante
ILocation CurrentLocation { get; }

// Node Godot de la location
Node CurrentLocationNode { get; }

// Indique si une location est chargée
bool HasLocation { get; }
```

## ?? Événements

```csharp
// Quand une location est chargée avec succès
event Action<ILocation> LocationLoaded;

// Quand une location est déchargée
event Action<ILocation> LocationUnloaded;

// Quand le chargement échoue (identifier, raison)
event Action<string, string> LocationLoadFailed;
```

## ?? Auto-Découverte des Types

Au démarrage, le LocationManager scanne automatiquement l'assembly pour trouver tous les types qui :
- ? Implémentent `ILocation`
- ? Sont des classes (pas abstraites)
- ? Héritent de `Node`

**Types auto-découverts** :
```
?? LocationManager: Enregistrement des types de locations...
  ? LocationModel
  ? Lobby
  ? Arena
  ? Shop
  ? MyCustomLocation
? LocationManager: 5 types de locations enregistrés
```

## ?? Exemple Complet d'Utilisation

```csharp
using Godot;
using Satsuki.Manager;
using Satsuki.Interfaces;

public partial class GameController : Node
{
    private LocationManager _locationManager;
    
    public override void _Ready()
    {
        _locationManager = LocationManager.Instance;
        
        // S'abonner aux événements
        _locationManager.LocationLoaded += OnLocationLoaded;
        _locationManager.LocationLoadFailed += OnLocationLoadFailed;
        
        // Précharger les locations principales
        PreloadCommonLocations();
        
        // Charger la location de départ
        LoadStartingLocation();
    }
    
    private void PreloadCommonLocations()
    {
        _locationManager.PreloadScene("res://Scenes/Locations/Lobby.tscn");
        _locationManager.PreloadScene("res://Scenes/Locations/Arena.tscn");
        _locationManager.PreloadScene("res://Scenes/Locations/Shop.tscn");
        
        GD.Print($"? {_locationManager.GetCachedSceneCount()} locations préchargées");
    }
    
    private void LoadStartingLocation()
    {
        bool success = _locationManager.LoadLocationFromScene(
            "res://Scenes/Locations/Lobby.tscn"
        );
        
        if (!success)
        {
            GD.PrintErr("Impossible de charger la location de départ !");
        }
    }
    
    private void OnLocationLoaded(ILocation location)
    {
        GD.Print($"?? Location prête: {location.LocationName}");
        
        // Spawn le joueur au point de spawn par défaut
        var spawnPoint = location.GetDefaultSpawnPoint();
        SpawnPlayer(spawnPoint);
        
        // Faire entrer le joueur dans la location
        _locationManager.PlayerEnter("Player1");
        
        // Mettre à jour l'UI
        UpdateLocationNameLabel(location.LocationName);
    }
    
    private void OnLocationLoadFailed(string identifier, string reason)
    {
        GD.PrintErr($"? Échec: {identifier} - {reason}");
        ShowErrorDialog($"Impossible de charger la location.\nRaison: {reason}");
    }
    
    // Exemple de transition
    public void GoToArena()
    {
        CallDeferred(nameof(LoadArena));
    }
    
    private void LoadArena()
    {
        _locationManager.LoadLocationFromScene("res://Scenes/Locations/Arena.tscn");
    }
    
    // Exemple d'information
    public void ShowLocationInfo()
    {
        var info = _locationManager.GetCurrentLocationInfo();
        
        if (info.HasLocation)
        {
            GD.Print($"?? Location: {info.LocationName}");
            GD.Print($"   Type: {info.LocationType}");
            GD.Print($"   Joueurs: {info.PlayersCount}");
            GD.Print($"   Interactables: {info.InteractablesCount}");
        }
        else
        {
            GD.Print("Aucune location chargée");
        }
    }
    
    private void SpawnPlayer(Vector3 position)
    {
        // Logique de spawn du joueur
    }
    
    private void UpdateLocationNameLabel(string locationName)
    {
        // Mettre à jour l'UI
    }
    
    private void ShowErrorDialog(string message)
    {
        // Afficher un dialogue d'erreur
    }
}
```

## ? Avantages du LocationManager

### ? **Centralisation**
- Une seule source de vérité pour les locations
- Logique unifiée
- Facile à maintenir

### ? **Performance**
- Système de cache intelligent
- Préchargement possible
- Gestion mémoire optimisée

### ? **Facilité d'Utilisation**
- API claire et simple
- Gestion automatique du cycle de vie
- Événements pour réactivité

### ? **Flexibilité**
- Charger depuis `.tscn` ou par code
- Système de cache optionnel
- Auto-découverte des types

### ? **Robustesse**
- Gestion d'erreurs complète
- Événements d'échec
- Nettoyage automatique

## ?? Extensions Futures Possibles

### **Transitions Animées**
```csharp
public async Task LoadLocationWithTransition(string scenePath, TransitionType transition)
{
    await PlayTransitionOut(transition);
    bool success = LoadLocationFromScene(scenePath);
    if (success) await PlayTransitionIn(transition);
}
```

### **Chargement Asynchrone**
```csharp
public async Task<bool> LoadLocationAsync(string scenePath)
{
    // Chargement en arrière-plan
    // Évite les freezes
}
```

### **Pool de Locations**
```csharp
// Garde certaines locations en mémoire pour switch instantané
public void AddToPool(string scenePath) { }
public void RemoveFromPool(string scenePath) { }
```

Le **LocationManager** est maintenant prêt à être utilisé pour gérer toutes vos locations Godot de manière centralisée et efficace ! ????
