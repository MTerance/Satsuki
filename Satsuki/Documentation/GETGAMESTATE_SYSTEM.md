# ?? Système GetGameState avec GetSceneState Dynamique

## Vue d'ensemble

Le système `GetGameState()` dans `MainGameScene` a été amélioré pour inclure l'état de la scène actuelle via une méthode `GetSceneState()` appelée dynamiquement par réflexion.

## ?? Fonctionnalités

### MainGameScene.GetGameState()

La méthode `GetGameState()` retourne maintenant :
- **Informations serveur** (running, clients connectés, etc.)
- **Informations de cryptage** (activé, clé, IV)
- **Liste des clients** avec leurs types
- **Informations de debug**
- **?? Informations de scène** incluant :
  - Nom de la scène actuelle
  - Chemin de la scène
  - **État de la scène** via `GetSceneState()`

## ?? Structure de Retour

```json
{
    "Server": {
        "IsRunning": true,
        "IsServerManagerActive": true,
        "ConnectedClients": 2,
        "PendingMessages": 0
    },
    "Encryption": {
        "Enabled": true,
        "KeyPreview": "...",
        "IVPreview": "..."
    },
    "Clients": [
        {
            "Id": "Client_1",
            "Status": "Connected",
            "Type": "PLAYER"
        }
    ],
    "Debug": {
        "DebugMode": true,
        "Timestamp": "2024-01-15T14:30:00Z"
    },
    "Scene": {
        "CurrentScene": "QuizScene",
        "ScenePath": "res://Scenes/Quizz/QuizScene.tscn",
        "SceneState": {
            // État retourné par GetSceneState() de la scène
        }
    }
}
```

## ?? Implémentation de GetSceneState() dans une Scène

### Exemple 1: Scène de Quiz

```csharp
using Godot;
using System;

public partial class QuizScene : Node
{
    private string _quizTitle = "Quiz de Test";
    private int _currentQuestionIndex = 0;
    private int _totalQuestions = 10;
    private int _score = 0;
    private bool _isActive = false;
    
    /// <summary>
    /// Retourne l'état actuel de la scène de quiz
    /// </summary>
    public object GetSceneState()
    {
        return new
        {
            QuizInfo = new
            {
                Title = _quizTitle,
                IsActive = _isActive,
                CurrentQuestion = _currentQuestionIndex + 1,
                TotalQuestions = _totalQuestions,
                Progress = _totalQuestions > 0 ? 
                    (float)_currentQuestionIndex / _totalQuestions * 100 : 0
            },
            PlayerStats = new
            {
                CurrentScore = _score
            },
            Timing = new
            {
                Timestamp = DateTime.UtcNow
            }
        };
    }
}
```

**Résultat GetGameState() avec cette scène :**

```json
{
    "Scene": {
        "CurrentScene": "QuizScene",
        "ScenePath": "res://Scenes/Quizz/QuizScene.tscn",
        "SceneState": {
            "QuizInfo": {
                "Title": "Quiz de Test",
                "IsActive": true,
                "CurrentQuestion": 5,
                "TotalQuestions": 10,
                "Progress": 50.0
            },
            "PlayerStats": {
                "CurrentScore": 42
            },
            "Timing": {
                "Timestamp": "2024-01-15T14:30:00Z"
            }
        }
    }
}
```

### Exemple 2: Scène de Gameplay

```csharp
using Godot;
using System;
using System.Collections.Generic;

public partial class GameplayScene : Node
{
    private string _levelName = "Level 1";
    private int _playerHealth = 100;
    private int _enemiesKilled = 0;
    private float _playTime = 0.0f;
    
    public object GetSceneState()
    {
        return new
        {
            Level = new
            {
                Name = _levelName,
                EnemiesKilled = _enemiesKilled
            },
            Player = new
            {
                Health = _playerHealth,
                IsAlive = _playerHealth > 0
            },
            Session = new
            {
                PlayTime = Math.Round(_playTime, 2),
                StartTime = DateTime.UtcNow.AddSeconds(-_playTime)
            }
        };
    }
}
```

### Exemple 3: Scène de Menu (Simple)

```csharp
using Godot;

public partial class MenuScene : Node
{
    private string _selectedMenuItem = "Main Menu";
    
    public object GetSceneState()
    {
        return new
        {
            Menu = new
            {
                CurrentSelection = _selectedMenuItem,
                MenuType = "MainMenu"
            }
        };
    }
}
```

## ?? Comment ça Fonctionne

### 1. Appel Dynamique par Réflexion

```csharp
var currentScene = GetTree().CurrentScene;
var sceneType = currentScene.GetType();
var getSceneStateMethod = sceneType.GetMethod("GetSceneState", 
    System.Reflection.BindingFlags.Public | 
    System.Reflection.BindingFlags.Instance);

if (getSceneStateMethod != null)
{
    sceneState = getSceneStateMethod.Invoke(currentScene, null);
}
```

### 2. Gestion des Erreurs

Si la scène n'implémente pas `GetSceneState()` :
```json
{
    "SceneState": {
        "Info": "Scene does not implement GetSceneState()"
    }
}
```

Si une erreur survient :
```json
{
    "SceneState": {
        "Error": "Failed to get scene state",
        "Message": "Error details..."
    }
}
```

## ?? Logs

### Scène avec GetSceneState()
```
? État de la scène QuizScene récupéré
```

### Scène sans GetSceneState()
```
?? La scène MenuScene n'implémente pas GetSceneState()
```

### Erreur
```
? Erreur lors de la récupération de l'état de la scène: NullReferenceException...
```

## ?? Cas d'Usage

### 1. Monitoring du Serveur
Un client BACKEND peut récupérer l'état complet du serveur incluant l'état de la scène actuelle :

```csharp
// Côté serveur
var gameState = mainGameScene.GetGameState();
await network.SendMessageToClient(backendClientId, JsonSerializer.Serialize(gameState));
```

### 2. Sauvegarde de Partie
```csharp
var gameState = mainGameScene.GetGameState();
var sceneState = gameState.Scene.SceneState;

// Sauvegarder l'état dans un fichier
File.WriteAllText("save.json", JsonSerializer.Serialize(sceneState));
```

### 3. Debug et Analytics
```csharp
// Logger l'état périodiquement
var timer = new Timer();
timer.Timeout += () =>
{
    var state = mainGameScene.GetGameState();
    GD.Print($"Scene: {state.Scene.CurrentScene}");
    GD.Print($"Players: {state.Server.ConnectedClients}");
};
```

## ??? Bonnes Pratiques

### 1. Méthode GetSceneState() Publique
```csharp
public object GetSceneState()  // ? Public
{
    // ...
}
```

### 2. Retourner des Objets Anonymes
```csharp
return new  // ? Objet anonyme
{
    Property1 = value1,
    Property2 = value2
};
```

### 3. Inclure un Timestamp
```csharp
return new
{
    // ...existing properties...,
    Timestamp = DateTime.UtcNow  // ? Pour tracking temporel
};
```

### 4. Gérer les Valeurs Nulles
```csharp
return new
{
    PlayerName = _playerName ?? "Unknown",  // ? Null-coalescing
    Health = _playerHealth.HasValue ? _playerHealth.Value : 0
};
```

## ?? Exemples de Scènes Complètes

Les fichiers suivants ont été créés comme exemples :

1. **`Scenes/Quizz/QuizScene.cs`**
   - Scène de quiz avec progression
   - Tracking des joueurs
   - Score et questions

2. **`Scenes/GameplayScene.cs`**
   - Scène de gameplay complète
   - Health, ennemis, inventaire
   - Statistiques de session

## ?? Utilisation Avancée

### Enrichir GetGameState() avec Plus d'Informations

```csharp
public object GetGameState()
{
    var baseState = base.GetGameState(); // Si héritage

    return new
    {
        // États de base
        Server = baseState.Server,
        Clients = baseState.Clients,
        
        // État personnalisé de la scène
        Scene = new
        {
            CurrentScene = GetTree().CurrentScene?.Name,
            ScenePath = GetTree().CurrentScene?.SceneFilePath,
            SceneState = GetCurrentSceneState(),
            
            // ?? Informations supplémentaires
            SceneLoadTime = Time.GetTicksMsec(),
            NodeCount = GetTree().GetNodeCount(),
            PhysicsFrames = Engine.GetPhysicsFrames()
        }
    };
}
```

## ?? Interface pour GetSceneState

Créer une interface commune (optionnel) :

```csharp
public interface ISceneWithState
{
    object GetSceneState();
}

public partial class QuizScene : Node, ISceneWithState
{
    public object GetSceneState()
    {
        // Implementation
    }
}
```

## ?? Conclusion

Le système `GetGameState()` avec `GetSceneState()` dynamique permet :
- ? Monitoring complet du serveur
- ? État de scène personnalisé
- ? Sauvegarde de partie
- ? Debug et analytics
- ? Flexibilité totale (scènes avec ou sans GetSceneState)

**Tous les clients BACKEND peuvent maintenant récupérer l'état complet du jeu, incluant l'état détaillé de la scène active !** ??
