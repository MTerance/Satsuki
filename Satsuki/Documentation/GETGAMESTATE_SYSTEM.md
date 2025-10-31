# ?? Syst�me GetGameState avec GetSceneState Dynamique

## Vue d'ensemble

Le syst�me `GetGameState()` dans `MainGameScene` a �t� am�lior� pour inclure l'�tat de la sc�ne actuelle via une m�thode `GetSceneState()` appel�e dynamiquement par r�flexion.

## ?? Fonctionnalit�s

### MainGameScene.GetGameState()

La m�thode `GetGameState()` retourne maintenant :
- **Informations serveur** (running, clients connect�s, etc.)
- **Informations de cryptage** (activ�, cl�, IV)
- **Liste des clients** avec leurs types
- **Informations de debug**
- **?? Informations de sc�ne** incluant :
  - Nom de la sc�ne actuelle
  - Chemin de la sc�ne
  - **�tat de la sc�ne** via `GetSceneState()`

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
            // �tat retourn� par GetSceneState() de la sc�ne
        }
    }
}
```

## ?? Impl�mentation de GetSceneState() dans une Sc�ne

### Exemple 1: Sc�ne de Quiz

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
    /// Retourne l'�tat actuel de la sc�ne de quiz
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

**R�sultat GetGameState() avec cette sc�ne :**

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

### Exemple 2: Sc�ne de Gameplay

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

### Exemple 3: Sc�ne de Menu (Simple)

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

## ?? Comment �a Fonctionne

### 1. Appel Dynamique par R�flexion

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

Si la sc�ne n'impl�mente pas `GetSceneState()` :
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

### Sc�ne avec GetSceneState()
```
? �tat de la sc�ne QuizScene r�cup�r�
```

### Sc�ne sans GetSceneState()
```
?? La sc�ne MenuScene n'impl�mente pas GetSceneState()
```

### Erreur
```
? Erreur lors de la r�cup�ration de l'�tat de la sc�ne: NullReferenceException...
```

## ?? Cas d'Usage

### 1. Monitoring du Serveur
Un client BACKEND peut r�cup�rer l'�tat complet du serveur incluant l'�tat de la sc�ne actuelle :

```csharp
// C�t� serveur
var gameState = mainGameScene.GetGameState();
await network.SendMessageToClient(backendClientId, JsonSerializer.Serialize(gameState));
```

### 2. Sauvegarde de Partie
```csharp
var gameState = mainGameScene.GetGameState();
var sceneState = gameState.Scene.SceneState;

// Sauvegarder l'�tat dans un fichier
File.WriteAllText("save.json", JsonSerializer.Serialize(sceneState));
```

### 3. Debug et Analytics
```csharp
// Logger l'�tat p�riodiquement
var timer = new Timer();
timer.Timeout += () =>
{
    var state = mainGameScene.GetGameState();
    GD.Print($"Scene: {state.Scene.CurrentScene}");
    GD.Print($"Players: {state.Server.ConnectedClients}");
};
```

## ??? Bonnes Pratiques

### 1. M�thode GetSceneState() Publique
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

### 4. G�rer les Valeurs Nulles
```csharp
return new
{
    PlayerName = _playerName ?? "Unknown",  // ? Null-coalescing
    Health = _playerHealth.HasValue ? _playerHealth.Value : 0
};
```

## ?? Exemples de Sc�nes Compl�tes

Les fichiers suivants ont �t� cr��s comme exemples :

1. **`Scenes/Quizz/QuizScene.cs`**
   - Sc�ne de quiz avec progression
   - Tracking des joueurs
   - Score et questions

2. **`Scenes/GameplayScene.cs`**
   - Sc�ne de gameplay compl�te
   - Health, ennemis, inventaire
   - Statistiques de session

## ?? Utilisation Avanc�e

### Enrichir GetGameState() avec Plus d'Informations

```csharp
public object GetGameState()
{
    var baseState = base.GetGameState(); // Si h�ritage

    return new
    {
        // �tats de base
        Server = baseState.Server,
        Clients = baseState.Clients,
        
        // �tat personnalis� de la sc�ne
        Scene = new
        {
            CurrentScene = GetTree().CurrentScene?.Name,
            ScenePath = GetTree().CurrentScene?.SceneFilePath,
            SceneState = GetCurrentSceneState(),
            
            // ?? Informations suppl�mentaires
            SceneLoadTime = Time.GetTicksMsec(),
            NodeCount = GetTree().GetNodeCount(),
            PhysicsFrames = Engine.GetPhysicsFrames()
        }
    };
}
```

## ?? Interface pour GetSceneState

Cr�er une interface commune (optionnel) :

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

Le syst�me `GetGameState()` avec `GetSceneState()` dynamique permet :
- ? Monitoring complet du serveur
- ? �tat de sc�ne personnalis�
- ? Sauvegarde de partie
- ? Debug et analytics
- ? Flexibilit� totale (sc�nes avec ou sans GetSceneState)

**Tous les clients BACKEND peuvent maintenant r�cup�rer l'�tat complet du jeu, incluant l'�tat d�taill� de la sc�ne active !** ??
