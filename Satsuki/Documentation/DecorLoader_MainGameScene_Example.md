# ?? Exemple : Utilisation de DecorLoader dans MainGameScene

**Date** : 22 novembre 2025  
**Fichier exemple** : `Scenes/MainGameScene.cs`

---

## ?? Objectif

Montrer comment utiliser `DecorLoader` pour charger un décor et placer les joueurs aux spawn points.

---

## ?? Code exemple complet

```csharp
using Godot;
using Satsuki.Tools;
using System.Collections.Generic;

namespace Satsuki.Scenes
{
    public partial class MainGameScene : Node
    {
        private Node3D _currentDecor;
        private DecorConfiguration _currentConfig;
        private List<Player> _players = new List<Player>();
        
        public override void _Ready()
        {
            GD.Print("MainGameScene: Initialisation");
            
            // Charger le décor initial
            LoadDecor("res://Scenes/Locations/Restaurant.tscn");
        }
        
        /// <summary>
        /// Charge un décor et sa configuration
        /// </summary>
        public void LoadDecor(string decorPath)
        {
            GD.Print($"MainGameScene: Chargement de {decorPath}");
            
            // 1. Nettoyer le décor précédent
            if (_currentDecor != null)
            {
                GD.Print("MainGameScene: Nettoyage du decor precedent");
                _currentDecor.QueueFree();
                _currentDecor = null;
            }
            
            // 2. Charger le nouveau décor avec sa configuration
            var (scene, config) = DecorLoader.LoadDecorWithConfig(decorPath);
            
            if (scene == null)
            {
                GD.PrintErr($"MainGameScene: Impossible de charger {decorPath}");
                return;
            }
            
            // 3. Ajouter la scène au jeu
            _currentDecor = scene;
            AddChild(_currentDecor);
            
            GD.Print($"MainGameScene: Decor {scene.Name} charge");
            
            // 4. Stocker la configuration
            _currentConfig = config;
            
            if (config != null)
            {
                GD.Print($"MainGameScene: Configuration chargee - {config.SpawnPoints.Count} spawn points");
                
                // 5. Afficher les infos
                DisplayDecorInfo(config);
                
                // 6. Placer les joueurs existants
                if (_players.Count > 0)
                {
                    PlacePlayersAtSpawnPoints();
                }
            }
            else
            {
                GD.Print("MainGameScene: Aucune configuration - spawn points par defaut");
            }
        }
        
        /// <summary>
        /// Affiche les informations du décor chargé
        /// </summary>
        private void DisplayDecorInfo(DecorConfiguration config)
        {
            GD.Print("=== DECOR INFO ===");
            GD.Print($"Nom: {config.SceneName}");
            GD.Print($"Chemin: {config.ScenePath}");
            GD.Print($"Spawn points totaux: {config.SpawnPoints.Count}");
            
            // Compter par type
            int standingCount = 0;
            int seatedCount = 0;
            
            foreach (var sp in config.SpawnPoints)
            {
                if (sp.Type == SpawnPointType.Standard_Idle)
                    standingCount++;
                else
                    seatedCount++;
            }
            
            GD.Print($"  - Debout: {standingCount}");
            GD.Print($"  - Assis: {seatedCount}");
            GD.Print($"Sauvegarde: {config.SavedAt}");
            GD.Print("==================");
        }
        
        /// <summary>
        /// Place les joueurs aux spawn points disponibles
        /// </summary>
        private void PlacePlayersAtSpawnPoints()
        {
            if (_currentConfig == null || _currentConfig.SpawnPoints.Count == 0)
            {
                GD.PrintErr("MainGameScene: Aucun spawn point disponible");
                return;
            }
            
            GD.Print($"MainGameScene: Placement de {_players.Count} joueurs");
            
            for (int i = 0; i < _players.Count; i++)
            {
                // Utiliser un spawn point différent pour chaque joueur (cycle si nécessaire)
                var spawnPoint = _currentConfig.SpawnPoints[i % _currentConfig.SpawnPoints.Count];
                
                _players[i].GlobalPosition = spawnPoint.Position;
                _players[i].SetIdleAnimation(spawnPoint.Type);
                
                GD.Print($"  Joueur {i} place en {spawnPoint.Type} a {spawnPoint.Position}");
            }
        }
        
        /// <summary>
        /// Ajoute un nouveau joueur et le place
        /// </summary>
        public void AddPlayer(Player player)
        {
            _players.Add(player);
            AddChild(player);
            
            GD.Print($"MainGameScene: Ajout joueur {player.Name}");
            
            // Placer le joueur à un spawn point
            PlaceNewPlayer(player);
        }
        
        /// <summary>
        /// Place un nouveau joueur à un spawn point libre
        /// </summary>
        private void PlaceNewPlayer(Player player, bool preferSeated = false)
        {
            if (_currentConfig == null || _currentConfig.SpawnPoints.Count == 0)
            {
                GD.PrintErr("MainGameScene: Aucun spawn point disponible");
                player.GlobalPosition = Vector3.Zero; // Position par défaut
                return;
            }
            
            // Récupérer un spawn point aléatoire du type préféré
            var spawnType = preferSeated ? SpawnPointType.Seated_Idle : SpawnPointType.Standard_Idle;
            var spawnPoint = GetAvailableSpawnPoint(spawnType);
            
            if (spawnPoint == null)
            {
                // Aucun point du type préféré, prendre n'importe lequel
                spawnPoint = GetAvailableSpawnPoint(null);
            }
            
            if (spawnPoint != null)
            {
                player.GlobalPosition = spawnPoint.Position;
                player.SetIdleAnimation(spawnPoint.Type);
                GD.Print($"Joueur place en {spawnPoint.Type} a {spawnPoint.Position}");
            }
            else
            {
                GD.PrintErr("Aucun spawn point disponible !");
                player.GlobalPosition = Vector3.Zero;
            }
        }
        
        /// <summary>
        /// Récupère un spawn point disponible (non occupé)
        /// </summary>
        private SpawnPointData GetAvailableSpawnPoint(SpawnPointType? preferredType)
        {
            var availablePoints = new List<SpawnPointData>();
            
            foreach (var sp in _currentConfig.SpawnPoints)
            {
                // Vérifier si le type correspond (si spécifié)
                if (preferredType.HasValue && sp.Type != preferredType.Value)
                    continue;
                
                // Vérifier si le point n'est pas déjà occupé
                bool occupied = false;
                foreach (var player in _players)
                {
                    if (player.GlobalPosition.DistanceTo(sp.Position) < 0.5f)
                    {
                        occupied = true;
                        break;
                    }
                }
                
                if (!occupied)
                {
                    availablePoints.Add(sp);
                }
            }
            
            if (availablePoints.Count == 0)
                return null;
            
            // Retourner un point aléatoire parmi les disponibles
            var random = new Random();
            return availablePoints[random.Next(availablePoints.Count)];
        }
        
        /// <summary>
        /// Change de décor avec transition
        /// </summary>
        public async void ChangeDecor(string newDecorPath)
        {
            GD.Print($"MainGameScene: Changement de decor vers {newDecorPath}");
            
            // Vérifier que le décor existe et a une configuration
            if (!ResourceLoader.Exists(newDecorPath))
            {
                GD.PrintErr($"Decor introuvable: {newDecorPath}");
                return;
            }
            
            if (!DecorLoader.HasConfiguration(newDecorPath))
            {
                GD.Print("Attention: Ce decor n'a pas de configuration de spawn points");
            }
            
            // Fade out (exemple)
            await FadeOut();
            
            // Charger le nouveau décor
            LoadDecor(newDecorPath);
            
            // Fade in
            await FadeIn();
        }
        
        /// <summary>
        /// Liste tous les décors disponibles avec configuration
        /// </summary>
        public void ListAvailableDecors()
        {
            var decors = DecorLoader.ListConfiguredDecors();
            
            GD.Print($"=== {decors.Count} DECORS DISPONIBLES ===");
            foreach (var decorPath in decors)
            {
                var config = DecorLoader.LoadConfiguration(decorPath);
                if (config != null)
                {
                    GD.Print($"- {config.SceneName}: {config.SpawnPoints.Count} spawn points");
                }
            }
            GD.Print("=====================================");
        }
        
        // Méthodes de transition (exemples)
        private async Task FadeOut()
        {
            // Votre code de fade out
            await ToSignal(GetTree().CreateTimer(0.5), SceneTreeTimer.SignalName.Timeout);
        }
        
        private async Task FadeIn()
        {
            // Votre code de fade in
            await ToSignal(GetTree().CreateTimer(0.5), SceneTreeTimer.SignalName.Timeout);
        }
    }
    
    // Classe Player exemple
    public partial class Player : CharacterBody3D
    {
        public void SetIdleAnimation(SpawnPointType type)
        {
            switch (type)
            {
                case SpawnPointType.Standard_Idle:
                    // Jouer animation debout
                    GD.Print($"{Name}: Animation Idle debout");
                    break;
                    
                case SpawnPointType.Seated_Idle:
                    // Jouer animation assis
                    GD.Print($"{Name}: Animation Idle assis");
                    break;
            }
        }
    }
}
```

---

## ?? Points clés

### 1. Chargement simple

```csharp
var (scene, config) = DecorLoader.LoadDecorWithConfig(decorPath);
AddChild(scene);
```

### 2. Placement automatique

```csharp
foreach (var player in _players)
{
    var spawnPoint = config.SpawnPoints[i % config.SpawnPoints.Count];
    player.GlobalPosition = spawnPoint.Position;
}
```

### 3. Gestion des erreurs

```csharp
if (scene == null)
{
    GD.PrintErr("Impossible de charger le decor");
    return;
}

if (config == null)
{
    GD.Print("Pas de configuration - valeurs par defaut");
}
```

### 4. Points disponibles

```csharp
private SpawnPointData GetAvailableSpawnPoint(SpawnPointType? type)
{
    // Vérifier qu'aucun joueur n'occupe déjà ce point
    // Retourner un point libre aléatoire
}
```

---

## ?? Flux de données

```
1. MainGameScene.LoadDecor(path)
   ?
2. DecorLoader.LoadDecorWithConfig(path)
   ?
3. Retour: (Node3D scene, DecorConfiguration config)
   ?
4. AddChild(scene)
   ?
5. PlacePlayersAtSpawnPoints()
   ?
6. player.GlobalPosition = spawnPoint.Position
```

---

## ? Avantages de cette approche

- ? **Simple** : Une ligne pour charger décor + config
- ? **Sûr** : Gestion automatique des erreurs
- ? **Flexible** : Supporte décors avec ou sans config
- ? **Performant** : Pas de surcharge
- ? **Maintenable** : Code clair et structuré

---

## ?? Résultat en jeu

```
MainGameScene: Chargement de res://Scenes/Locations/Restaurant.tscn
DecorLoader: Chargement de res://Scenes/Locations/Restaurant.tscn
DecorLoader: Configuration Restaurant chargee (7 spawn points)
MainGameScene: Decor Restaurant charge
MainGameScene: Configuration chargee - 7 spawn points
=== DECOR INFO ===
Nom: Restaurant
Chemin: res://Scenes/Locations/Restaurant.tscn
Spawn points totaux: 7
  - Debout: 3
  - Assis: 4
Sauvegarde: 22/11/2025 15:30:00
==================
MainGameScene: Placement de 4 joueurs
  Joueur 0 place en Standard_Idle a (1.5, 0, 3.2)
  Joueur 1 place en Standard_Idle a (4.2, 0, -1.8)
  Joueur 2 place en Seated_Idle a (2.1, 0, 2.4)
  Joueur 3 place en Seated_Idle a (2.1, 0, 3.6)
```

---

*Exemple complet et prêt à l'emploi ! ??*
