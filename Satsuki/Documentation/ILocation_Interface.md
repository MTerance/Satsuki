# ??? Interface ILocation - Architecture des Locations

## ?? Overview

Création de l'interface `ILocation` pour standardiser et structurer toutes les locations du jeu. Cette interface définit un contrat complet pour les fonctionnalités que chaque location doit implémenter, incluant la gestion des joueurs, des interactions, de la navigation et de la configuration.

## ?? Objectifs de ILocation

### **Standardisation**
- Contrat uniforme pour toutes les locations
- API cohérente pour l'interaction avec les locations
- Structure prévisible pour les développeurs

### **Fonctionnalités Complètes**
- Gestion du cycle de vie (load/unload)
- Système de joueurs (enter/exit)
- Objets interactables
- Navigation et spawn points
- Configuration dynamique

### **Intégration avec IScene**
- Compatible avec l'architecture existante
- Utilisable dans MainGameScene.CurrentScene
- État accessible via GetSceneState()

## ??? Structure de l'Interface ILocation

### 1. **Identification et Métadonnées**
```csharp
string LocationName { get; }          // Nom unique
LocationType Type { get; }            // Type de location
string Description { get; }           // Description
string LocationId { get; }            // ID unique
```

#### **Énumération LocationType**
```csharp
public enum LocationType
{
    Interior,    // Intérieur (maison, bâtiment)
    Exterior,    // Extérieur (rue, parc)
    Special,     // Spécial (donjon, zone secrète)
    Transition,  // Transition (couloir, ascenseur)
    Combat,      // Zone de combat
    Social,      // Zone sociale (café, place)
    Shop,        // Magasin/commerce
    Home         // Base/refuge du joueur
}
```

### 2. **État et Statut**
```csharp
bool IsLoaded { get; }               // Location chargée et prête
bool IsAccessible { get; }           // Accessible au joueur
object GetLocationState();           // État complet
```

### 3. **Cycle de Vie**
```csharp
void Initialize();                   // Initialisation
void LoadLocation();                 // Chargement ressources
void UnloadLocation();               // Déchargement
void ActivateLocation();             // Activation (visible, systèmes)
void DeactivateLocation();           // Désactivation
```

### 4. **Gestion des Joueurs**
```csharp
void OnPlayerEnter(string playerId);        // Joueur entre
void OnPlayerExit(string playerId);         // Joueur sort
string[] GetPlayersInLocation();            // Liste des joueurs
```

### 5. **Système d'Interactions**
```csharp
IInteractable[] GetInteractables();                              // Objets interactables
void ProcessInteraction(string playerId, string interactionId,  // Traitement interaction
                       object data = null);
```

### 6. **Navigation**
```csharp
Vector3[] GetSpawnPoints();                              // Points d'apparition
Vector3 GetDefaultSpawnPoint();                         // Point par défaut
Dictionary<string, string> GetExits();                  // Sorties disponibles
```

### 7. **Configuration**
```csharp
void Configure(ILocationConfig config);        // Configuration dynamique
object SaveLocationState();                    // Sauvegarde état
void RestoreLocationState(object stateData);   // Restauration état
```

### 8. **Événements**
```csharp
event Action<ILocation> LocationLoaded;                    // Location chargée
event Action<ILocation> LocationUnloaded;                  // Location déchargée
event Action<ILocation, string> PlayerEntered;             // Joueur entré
event Action<ILocation, string> PlayerExited;              // Joueur sorti
event Action<ILocation, string, string> InteractionOccurred; // Interaction
```

## ?? Interface IInteractable

### **Propriétés des objets interactables**
```csharp
public interface IInteractable
{
    string InteractableId { get; }         // ID unique
    string DisplayName { get; }            // Nom affiché
    string InteractionDescription { get; }  // Description interaction
    bool IsInteractable { get; }           // Disponible
    Vector3 Position { get; }              // Position dans location
    
    object Interact(string playerId, object data = null);  // Exécuter interaction
    event Action<IInteractable, string> Interacted;        // Événement
}
```

### **Exemple : MediaScreenInteractable**
```csharp
public class MediaScreenInteractable : IInteractable
{
    private readonly MeshInstance3D _mediaScreen;

    public string InteractableId => $"MediaScreen_{_mediaScreen.GetInstanceId()}";
    public string DisplayName => "Écran Média";
    public string InteractionDescription => "Interagir avec l'écran média";
    public bool IsInteractable => _mediaScreen?.IsInsideTree() ?? false;
    public Vector3 Position => _mediaScreen?.GlobalPosition ?? Vector3.Zero;

    public object Interact(string playerId, object data = null)
    {
        // Logique d'interaction avec l'écran
        return new { Success = true, Action = "MediaScreenInteraction" };
    }
}
```

## ??? Interface ILocationConfig

### **Configuration complète des locations**
```csharp
public interface ILocationConfig
{
    object AmbianceSettings { get; }     // Ambiance (éclairage, son)
    object GameplaySettings { get; }     // Paramètres de gameplay
    string[] PreloadResources { get; }   // Ressources à précharger
    bool AutoSave { get; }              // Sauvegarde automatique
    int MaxPlayers { get; }             // Capacité maximale
}
```

## ?? Implémentation LocationModel

### **Classe de base complète**
```csharp
public partial class LocationModel : Node3D, ILocation, IScene
{
    // Implémente ILocation ET IScene
    // Préserve le code MediaScreen existant
    // Ajoute toutes les fonctionnalités ILocation
}
```

### **Fonctionnalités ajoutées**
- ? **Gestion des joueurs** : Liste, entrée/sortie, événements
- ? **Objets interactables** : Collection, recherche, interaction
- ? **Navigation** : Spawn points, sorties, points d'intérêt
- ? **Configuration** : Paramètres dynamiques, sauvegarde/restauration
- ? **Événements** : Signaling complet pour intégration externe

### **Code MediaScreen préservé**
- ? **InitializeMediaScreen()** : Code existant intact
- ? **SetupMediaScreenWithFallback()** : Fonctionnalité complète
- ? **SubViewport integration** : Recherche et setup automatique
- ? **MediaScreenInteractable** : MediaScreen comme objet interactable

## ?? Intégration avec MainGameScene

### **Utilisation dans CurrentScene**
```csharp
// Dans MainGameScene
public void LoadLocationInCurrentScene(Type locationType)
{
    if (typeof(ILocation).IsAssignableFrom(locationType))
    {
        LoadSceneInProperty("", locationType);
        
        // La location est maintenant accessible via CurrentScene
        if (CurrentScene is ILocation location)
        {
            // Utilisation de l'API ILocation
            location.OnPlayerEnter("Player1");
            var interactables = location.GetInteractables();
            var state = location.GetLocationState();
        }
    }
}
```

### **Méthodes spécialisées pour les locations**
```csharp
private void LoadLocationSpecialized(ILocation location)
{
    // Configuration spécifique aux locations
    location.LocationLoaded += OnLocationLoaded;
    location.PlayerEntered += OnPlayerEnteredLocation;
    location.InteractionOccurred += OnLocationInteraction;
    
    // Activer si pas déjà fait
    if (!location.IsLoaded)
    {
        location.LoadLocation();
    }
}

private void UnloadLocationSpecialized(ILocation location)
{
    // Déconnexion des événements
    location.LocationLoaded -= OnLocationLoaded;
    location.PlayerEntered -= OnPlayerEnteredLocation;
    location.InteractionOccurred -= OnLocationInteraction;
    
    // Décharger proprement
    location.UnloadLocation();
}
```

## ?? État de Location

### **GetLocationState() enrichi**
```csharp
return new
{
    Location = new
    {
        Id = LocationId,
        Name = LocationName,
        Type = Type.ToString(),
        Description = Description,
        IsLoaded = _isLoaded,
        IsAccessible = _isAccessible
    },
    Players = new
    {
        Count = _playersInLocation.Count,
        PlayerIds = _playersInLocation.ToArray()
    },
    Interactables = new
    {
        Count = _interactables.Count,
        Available = _interactables.Count(i => i.IsInteractable)
    },
    Navigation = new
    {
        SpawnPoints = GetSpawnPoints().Length,
        DefaultSpawn = GetDefaultSpawnPoint(),
        ExitCount = GetExits().Count
    }
};
```

### **Intégration IScene**
```csharp
// IScene.GetSceneState() délègue à ILocation.GetLocationState()
public object GetSceneState()
{
    return GetLocationState();
}
```

## ?? Exemples d'Usage

### **Création d'une location spécialisée**
```csharp
public partial class CafeLocation : LocationModel
{
    public override LocationType Type => LocationType.Social;
    public override string Description => "Café convivial du centre-ville";

    protected override void InitializeInteractables()
    {
        base.InitializeInteractables(); // MediaScreen automatique
        
        // Ajouter comptoir, tables, etc.
        _interactables.Add(new CounterInteractable());
        _interactables.Add(new MenuInteractable());
    }

    protected override void OnPlayerEnterSpecific(string playerId)
    {
        // Musique d'ambiance café
        PlayAmbianceSound("cafe_ambiance.ogg");
        
        // Notification aux autres joueurs
        BroadcastToOtherClients(playerId, $"{playerId} entre dans le café");
    }
}
```

### **Interaction avec une location**
```csharp
// Depuis GameServerHandler ou autre système
public void HandlePlayerMovement(string playerId, Vector3 newPosition)
{
    // Détecter changement de location
    var newLocation = GetLocationAtPosition(newPosition);
    var currentLocation = GetPlayerCurrentLocation(playerId);
    
    if (newLocation != currentLocation)
    {
        // Sortir de l'ancienne location
        currentLocation?.OnPlayerExit(playerId);
        
        // Entrer dans la nouvelle location
        newLocation?.OnPlayerEnter(playerId);
        
        // Mettre à jour le tracking
        UpdatePlayerLocation(playerId, newLocation);
    }
}
```

### **Configuration dynamique**
```csharp
var locationConfig = new LocationConfig
{
    AmbianceSettings = new { 
        LightIntensity = 0.8f, 
        SoundVolume = 0.6f 
    },
    GameplaySettings = new { 
        PvPEnabled = false, 
        TradeEnabled = true 
    },
    PreloadResources = new[] { 
        "cafe_textures.tres", 
        "cafe_sounds.ogg" 
    },
    AutoSave = true,
    MaxPlayers = 20
};

myLocation.Configure(locationConfig);
```

## ??? Avantages de l'Architecture

### ? **Standardisation**
- **API uniforme** : Toutes les locations se comportent de manière prévisible
- **Intégration facile** : Compatible avec MainGameScene.CurrentScene
- **Documentation claire** : Interface bien définie et documentée

### ? **Extensibilité**
- **Nouvelles locations** : Simple à créer en implémentant ILocation
- **Fonctionnalités modulaires** : Ajout facile de nouveaux types d'interactions
- **Configuration flexible** : Paramètres adaptables par location

### ? **Maintenabilité**
- **Code organisé** : Séparation claire des responsabilités
- **Réutilisabilité** : Composants réutilisables (IInteractable, ILocationConfig)
- **Testing** : Interface facilite les tests unitaires

### ? **Performance**
- **Chargement optimisé** : Load/unload selon les besoins
- **Gestion mémoire** : Déchargement propre des ressources
- **Activation sélective** : Systèmes activés seulement si nécessaire

## ?? Extensions Futures

### **Système de portails**
```csharp
public interface IPortal : IInteractable
{
    string DestinationLocationId { get; }
    Vector3 DestinationSpawnPoint { get; }
    bool IsPortalActive { get; }
    
    void ActivatePortal();
    void DeactivatePortal();
}
```

### **Zones dynamiques**
```csharp
public interface IDynamicZone : ILocation
{
    void GenerateContent();
    void RegenerateContent();
    bool IsGenerated { get; }
    float GenerationProgress { get; }
}
```

### **Système de quêtes par location**
```csharp
public interface IQuestLocation : ILocation
{
    IQuest[] GetAvailableQuests(string playerId);
    void StartQuest(string playerId, string questId);
    void CompleteQuestObjective(string playerId, string questId, string objectiveId);
}
```

## ? Validation

### **Tests effectués**
- ? **Compilation réussie** : Interface et implémentation valides
- ? **LocationModel** : Implémente ILocation et préserve MediaScreen
- ? **Intégration IScene** : Compatible avec MainGameScene.CurrentScene
- ? **MediaScreenInteractable** : MediaScreen automatiquement interactable
- ? **États accessibles** : GetLocationState() fonctionne

### **Fonctionnalités testées**
1. **Création location** : LocationModel instancie et initialise
2. **Gestion joueurs** : OnPlayerEnter/Exit avec événements
3. **Objets interactables** : MediaScreen détecté automatiquement
4. **Navigation** : Spawn points et sorties configurables
5. **État complet** : GetLocationState() retourne données complètes

L'interface `ILocation` fournit maintenant une architecture complète et standardisée pour toutes les locations du jeu, avec une intégration parfaite dans l'écosystème existant ! ????