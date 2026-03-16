# ?? Quick Start - DecorLoader

**Charger un décor + JSON en 1 ligne !**

---

## ? Usage basique

```csharp
using Satsuki.Tools;

// Charger décor + configuration
var (scene, config) = DecorLoader.LoadDecorWithConfig("res://Scenes/Locations/Restaurant.tscn");

// Ajouter au jeu
if (scene != null)
{
    AddChild(scene);
}

// Utiliser la configuration
if (config != null)
{
    GD.Print($"{config.SceneName}: {config.SpawnPoints.Count} spawn points");
}
```

---

## ?? Cas d'usage courants

### 1. Spawn de joueur

```csharp
var spawnPoint = DecorLoader.GetRandomSpawnPoint(
    "res://Scenes/Locations/Restaurant.tscn",
    SpawnPointType.Standard_Idle
);

player.GlobalPosition = spawnPoint.Position;
```

### 2. Liste des points assis

```csharp
var chairs = DecorLoader.GetSpawnPointsByType(
    decorPath, 
    SpawnPointType.Seated_Idle
);
```

### 3. Vérifier config existe

```csharp
if (DecorLoader.HasConfiguration(decorPath))
{
    // Charger la config
}
```

### 4. Tous les spawn points

```csharp
var allPoints = DecorLoader.GetSpawnPoints(decorPath);
```

---

## ?? Données retournées

```csharp
// DecorConfiguration
config.ScenePath     // "res://Scenes/Locations/Restaurant.tscn"
config.SceneName     // "Restaurant"
config.SpawnPoints   // List<SpawnPointData>
config.SavedAt       // DateTime

// SpawnPointData
spawnPoint.Position  // Vector3
spawnPoint.Type      // SpawnPointType (Standard_Idle / Seated_Idle)
spawnPoint.Index     // int
```

---

## ?? Fichiers

```
Configs/
??? Restaurant_config.json    ? Chargé automatiquement
??? Hall_config.json
??? [Decor]_config.json
```

---

## ? Checklist

- [ ] `using Satsuki.Tools;` en haut du fichier
- [ ] Chemin .tscn correct (`res://...`)
- [ ] Fichier JSON existe dans `Configs/`
- [ ] Vérifier `scene != null` et `config != null`

---

## ?? Méthodes essentielles

| Méthode | Usage |
|---------|-------|
| `LoadDecorWithConfig` | Charger décor + JSON |
| `GetRandomSpawnPoint` | Spawn point aléatoire |
| `GetSpawnPointsByType` | Filtrer par type |
| `HasConfiguration` | Vérifier si JSON existe |

---

*Guide complet : [DecorLoader_Guide.md](../Documentation/DecorLoader_Guide.md)*
