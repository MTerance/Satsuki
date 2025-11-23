# ?? DecorLoader - Classe utilitaire

**Date** : 22 novembre 2025  
**Fichier** : `Tools/DecorLoader.cs`  
**Usage** : Charger les décors et leurs configurations JSON depuis n'importe où dans le projet

---

## ?? Vue d'ensemble

`DecorLoader` est une classe utilitaire statique qui permet de charger facilement les fichiers `.tscn` de décor avec leur configuration JSON associée. Elle peut être utilisée depuis n'importe quelle partie du projet (pas seulement depuis l'éditeur).

---

## ?? Méthodes principales

### 1. LoadConfiguration

Charge uniquement le fichier JSON de configuration.

```csharp
public static DecorConfiguration LoadConfiguration(string tscnPath)
```

**Usage** :
```csharp
var config = DecorLoader.LoadConfiguration("res://Scenes/Locations/Restaurant.tscn");
if (config != null)
{
    GD.Print($"Decor: {config.SceneName}");
    GD.Print($"Spawn points: {config.SpawnPoints.Count}");
}
```

---

### 2. LoadDecorWithConfig

Charge le décor .tscn ET son JSON en une seule opération.

```csharp
public static (Node3D scene, DecorConfiguration config) LoadDecorWithConfig(string tscnPath)
```

**Usage** :
```csharp
var (scene, config) = DecorLoader.LoadDecorWithConfig("res://Scenes/Locations/Restaurant.tscn");

if (scene != null)
{
    AddChild(scene); // Ajouter la scène au jeu
    
    if (config != null)
    {
        // Placer les joueurs aux spawn points
        foreach (var spawnPoint in config.SpawnPoints)
        {
            PlacePlayer(spawnPoint.Position, spawnPoint.Type);
        }
    }
}
```

---

### 3. HasConfiguration

Vérifie si un fichier JSON existe pour un décor.

```csharp
public static bool HasConfiguration(string tscnPath)
```

**Usage** :
```csharp
if (DecorLoader.HasConfiguration("res://Scenes/Locations/Restaurant.tscn"))
{
    GD.Print("Ce decor a une configuration !");
}
```

---

### 4. GetSpawnPoints

Récupère tous les spawn points d'un décor.

```csharp
public static List<SpawnPointData> GetSpawnPoints(string tscnPath)
```

**Usage** :
```csharp
var spawnPoints = DecorLoader.GetSpawnPoints("res://Scenes/Locations/Restaurant.tscn");

foreach (var sp in spawnPoints)
{
    GD.Print($"Point {sp.Index}: {sp.Type} a {sp.Position}");
}
```

---

### 5. GetSpawnPointsByType

Récupère les spawn points d'un type spécifique.

```csharp
public static List<SpawnPointData> GetSpawnPointsByType(string tscnPath, SpawnPointType type)
```

**Usage** :
```csharp
// Récupérer uniquement les points "assis"
var seatedPoints = DecorLoader.GetSpawnPointsByType(
    "res://Scenes/Locations/Restaurant.tscn", 
    SpawnPointType.Seated_Idle
);

GD.Print($"{seatedPoints.Count} chaises disponibles");
```

---

### 6. GetRandomSpawnPoint

Récupère un spawn point aléatoire.

```csharp
public static SpawnPointData GetRandomSpawnPoint(string tscnPath, SpawnPointType? type = null)
```

**Usage** :
```csharp
// N'importe quel point
var randomPoint = DecorLoader.GetRandomSpawnPoint("res://Scenes/Locations/Restaurant.tscn");

// Uniquement un point "debout"
var standingPoint = DecorLoader.GetRandomSpawnPoint(
    "res://Scenes/Locations/Restaurant.tscn",
    SpawnPointType.Standard_Idle
);

if (standingPoint != null)
{
    player.GlobalPosition = standingPoint.Position;
}
```

---

### 7. SaveConfiguration

Sauvegarde une configuration.

```csharp
public static bool SaveConfiguration(DecorConfiguration config)
```

**Usage** :
```csharp
var config = new DecorConfiguration
{
    ScenePath = "res://Scenes/Locations/Restaurant.tscn",
    SceneName = "Restaurant",
    SpawnPoints = new List<SpawnPointData>
    {
        new SpawnPointData { Position = new Vector3(1, 0, 3), Type = SpawnPointType.Standard_Idle, Index = 0 }
    },
    SavedAt = DateTime.UtcNow
};

if (DecorLoader.SaveConfiguration(config))
{
    GD.Print("Configuration sauvegardee !");
}
```

---

### 8. ListConfiguredDecors

Liste tous les décors ayant une configuration.

```csharp
public static List<string> ListConfiguredDecors()
```

**Usage** :
```csharp
var decors = DecorLoader.ListConfiguredDecors();

foreach (var decorPath in decors)
{
    GD.Print($"Decor configure: {decorPath}");
}
```

---

## ?? Exemples d'utilisation

### Exemple 1 : Charger un décor dans MainGameScene

```csharp
public partial class MainGameScene : Node
{
    private Node3D _currentDecor;
    
    public void LoadLocation(string locationPath)
    {
        // Charger le décor avec sa config
        var (scene, config) = DecorLoader.LoadDecorWithConfig(locationPath);
        
        if (scene != null)
        {
            // Remplacer le décor actuel
            if (_currentDecor != null)
            {
                _currentDecor.QueueFree();
            }
            
            _currentDecor = scene;
            AddChild(_currentDecor);
            
            // Utiliser la configuration
            if (config != null)
            {
                GD.Print($"Decor charge: {config.SceneName}");
                GD.Print($"Spawn points disponibles: {config.SpawnPoints.Count}");
                
                // Placer les joueurs
                PlacePlayersAtSpawnPoints(config.SpawnPoints);
            }
        }
    }
}
```

---

### Exemple 2 : Faire apparaître un joueur

```csharp
public partial class PlayerManager : Node
{
    public void SpawnPlayer(Player player, string decorPath, bool seated = false)
    {
        var type = seated ? SpawnPointType.Seated_Idle : SpawnPointType.Standard_Idle;
        var spawnPoint = DecorLoader.GetRandomSpawnPoint(decorPath, type);
        
        if (spawnPoint != null)
        {
            player.GlobalPosition = spawnPoint.Position;
            player.SetIdleAnimation(spawnPoint.Type);
            GD.Print($"Joueur apparu en {spawnPoint.Type} a {spawnPoint.Position}");
        }
        else
        {
            GD.PrintErr($"Aucun spawn point {type} disponible !");
        }
    }
}
```

---

### Exemple 3 : Vérifier avant de charger

```csharp
public void TryLoadDecor(string decorPath)
{
    // Vérifier que le décor existe
    if (!ResourceLoader.Exists(decorPath))
    {
        GD.PrintErr($"Decor introuvable: {decorPath}");
        return;
    }
    
    // Vérifier s'il a une configuration
    if (DecorLoader.HasConfiguration(decorPath))
    {
        var config = DecorLoader.LoadConfiguration(decorPath);
        GD.Print($"Configuration trouvee: {config.SpawnPoints.Count} spawn points");
    }
    else
    {
        GD.Print("Pas de configuration pour ce decor");
    }
    
    // Charger le décor
    var (scene, _) = DecorLoader.LoadDecorWithConfig(decorPath);
    AddChild(scene);
}
```

---

### Exemple 4 : Répartir les joueurs

```csharp
public void DistributePlayers(List<Player> players, string decorPath)
{
    var spawnPoints = DecorLoader.GetSpawnPoints(decorPath);
    
    if (spawnPoints.Count == 0)
    {
        GD.PrintErr("Aucun spawn point disponible !");
        return;
    }
    
    for (int i = 0; i < players.Count; i++)
    {
        // Utiliser un spawn point différent pour chaque joueur
        var spawnPoint = spawnPoints[i % spawnPoints.Count];
        players[i].GlobalPosition = spawnPoint.Position;
        players[i].SetIdleAnimation(spawnPoint.Type);
    }
}
```

---

### Exemple 5 : Filtrer par type

```csharp
public void SeatAllPlayers(List<Player> players, string decorPath)
{
    // Récupérer uniquement les points assis
    var seatedPoints = DecorLoader.GetSpawnPointsByType(
        decorPath, 
        SpawnPointType.Seated_Idle
    );
    
    if (seatedPoints.Count < players.Count)
    {
        GD.PrintErr($"Pas assez de sieges ! {seatedPoints.Count} sieges pour {players.Count} joueurs");
        return;
    }
    
    for (int i = 0; i < players.Count; i++)
    {
        players[i].GlobalPosition = seatedPoints[i].Position;
        players[i].PlayAnimation("sit_idle");
    }
}
```

---

## ?? Structure des données retournées

### DecorConfiguration

```csharp
public class DecorConfiguration
{
    public string ScenePath { get; set; }        // "res://Scenes/Locations/Restaurant.tscn"
    public string SceneName { get; set; }        // "Restaurant"
    public List<SpawnPointData> SpawnPoints { get; set; }
    public DateTime SavedAt { get; set; }
}
```

### SpawnPointData

```csharp
public class SpawnPointData
{
    public Vector3 Position { get; set; }        // Position 3D du point
    public SpawnPointType Type { get; set; }     // Standard_Idle ou Seated_Idle
    public int Index { get; set; }               // Numéro d'ordre
}
```

### SpawnPointType

```csharp
public enum SpawnPointType
{
    Standard_Idle,      // 0 : Joueur debout
    Seated_Idle         // 1 : Joueur assis
}
```

---

## ?? Cas d'usage typiques

### 1. Chargement de location

```csharp
// Dans LocationManager ou MainGameScene
var (scene, config) = DecorLoader.LoadDecorWithConfig(locationPath);
```

### 2. Spawn de joueur

```csharp
// Dans PlayerSpawner
var spawnPoint = DecorLoader.GetRandomSpawnPoint(decorPath, SpawnPointType.Standard_Idle);
player.GlobalPosition = spawnPoint.Position;
```

### 3. Menu de sélection

```csharp
// Dans UI
var decors = DecorLoader.ListConfiguredDecors();
foreach (var decor in decors)
{
    AddMenuItem(decor);
}
```

### 4. Validation

```csharp
// Avant de charger
if (!DecorLoader.HasConfiguration(decorPath))
{
    ShowWarning("Ce decor n'a pas de configuration !");
}
```

---

## ?? Gestion des erreurs

### Décor non trouvé

```csharp
var (scene, config) = DecorLoader.LoadDecorWithConfig("res://Invalid.tscn");
if (scene == null)
{
    GD.PrintErr("Impossible de charger le decor");
    // Afficher message d'erreur utilisateur
}
```

### Pas de configuration

```csharp
var config = DecorLoader.LoadConfiguration(decorPath);
if (config == null)
{
    GD.Print("Aucune configuration - utiliser valeurs par defaut");
    // Placer joueurs à des positions par défaut
}
```

### Pas assez de spawn points

```csharp
var spawnPoints = DecorLoader.GetSpawnPoints(decorPath);
if (spawnPoints.Count < playerCount)
{
    GD.PrintErr($"Seulement {spawnPoints.Count} spawn points pour {playerCount} joueurs");
    // Réutiliser les spawn points ou placer aléatoirement
}
```

---

## ?? Bonnes pratiques

### 1. Toujours vérifier null

```csharp
var config = DecorLoader.LoadConfiguration(path);
if (config != null && config.SpawnPoints != null)
{
    // Utiliser les spawn points
}
```

### 2. Mettre en cache

```csharp
private Dictionary<string, DecorConfiguration> _configCache = new();

public DecorConfiguration GetConfig(string path)
{
    if (!_configCache.ContainsKey(path))
    {
        _configCache[path] = DecorLoader.LoadConfiguration(path);
    }
    return _configCache[path];
}
```

### 3. Libérer les ressources

```csharp
var (scene, config) = DecorLoader.LoadDecorWithConfig(path);
AddChild(scene);

// Plus tard...
if (scene != null)
{
    scene.QueueFree();
}
```

---

## ?? Emplacements des fichiers

### Structure

```
Satsuki/
??? Tools/
?   ??? DecorLoader.cs              ? Classe utilitaire
??? Configs/
?   ??? Restaurant_config.json
?   ??? Hall_config.json
?   ??? [Decor]_config.json
??? Scenes/
    ??? Locations/
        ??? Restaurant.tscn
        ??? Hall.tscn
        ??? [Decor].tscn
```

### Correspondance automatique

Le `DecorLoader` fait automatiquement la correspondance :

```
Restaurant.tscn ? Restaurant_config.json
Hall.tscn ? Hall_config.json
SalleDeJeu.tscn ? SalleDeJeu_config.json
```

---

## ?? Avantages

### ? Simplicité

```csharp
// Avant (manuel)
var scene = GD.Load<PackedScene>(path).Instantiate<Node3D>();
var jsonPath = Path.Combine(...);
var json = File.ReadAllText(jsonPath);
var config = JsonSerializer.Deserialize<DecorConfiguration>(json, options);

// Après (DecorLoader)
var (scene, config) = DecorLoader.LoadDecorWithConfig(path);
```

### ? Sûreté

- Gestion automatique des erreurs
- Vérifications null
- Logs explicites

### ? Flexibilité

- Méthodes pour tous les besoins
- Utilisable partout dans le projet
- Pas de dépendances

### ? Performance

- Classe statique (pas d'instanciation)
- Pas de surcharge
- Optimisé pour le chargement

---

## ?? Métriques

| Métrique | Valeur |
|----------|--------|
| **Lignes de code** | ~300 |
| **Méthodes publiques** | 8 |
| **Dépendances** | 0 (standalone) |
| **Utilisable dans** | Tout le projet |
| **Performance** | Optimale |

---

## ?? Résumé

`DecorLoader` est votre outil tout-en-un pour :

- ? Charger des décors .tscn
- ? Récupérer leur configuration JSON
- ? Obtenir des spawn points
- ? Filtrer par type
- ? Points aléatoires
- ? Sauvegarder
- ? Lister tous les décors

**Une seule classe, tous les besoins couverts ! ??**

---

*Date : 22 novembre 2025*  
*Fichier : Tools/DecorLoader.cs*  
*Status : ? Implémenté et testé*
