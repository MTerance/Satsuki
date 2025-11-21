# ?? Credits Scene - Implémentation IScene

## Vue d'ensemble

La scène `Credits` implémente l'interface `IScene` pour exposer son état via `GetSceneState()`, permettant au système `GetGameState()` de récupérer des informations détaillées sur les crédits en cours.

## ?? Structure de l'État Retourné

```json
{
    "SceneInfo": {
        "SceneName": "Credits",
        "SceneType": "SplashScreen",
        "StartTime": "2024-01-15T14:30:00Z",
        "ElapsedTime": 5.42,
        "ElapsedTimeFormatted": "00:05"
    },
    "SplashScreens": {
        "TotalScreens": 3,
        "CurrentIndex": 2,
        "RemainingScreens": 1,
        "Progress": 66.67
    },
    "UserInteraction": {
        "TotalSkips": 2,
        "SkipRate": 22.14
    },
    "Status": {
        "IsCompleted": false,
        "IsActive": true,
        "Timestamp": "2024-01-15T14:30:05Z"
    }
}
```

## ?? Implémentation

### Déclaration de la Classe
```csharp
using Satsuki.Interfaces;

public partial class Credits : Node, IScene
{
    private SplashScreenManager _splashScreenManager;
    private DateTime _sceneStartTime;
    private int _totalSkips = 0;
    
    // ...
}
```

### Méthode GetSceneState()
```csharp
public object GetSceneState()
{
    var elapsedTime = (DateTime.UtcNow - _sceneStartTime).TotalSeconds;
    
    return new
    {
        SceneInfo = {...},
        SplashScreens = {...},
        UserInteraction = {...},
        Status = {...}
    };
}
```

## ?? Métriques Trackées

### 1. **SceneInfo**
- **SceneName** : Nom de la scène ("Credits")
- **SceneType** : Type de scène ("SplashScreen")
- **StartTime** : Heure de démarrage (UTC)
- **ElapsedTime** : Temps écoulé en secondes
- **ElapsedTimeFormatted** : Temps formatté (MM:SS)

### 2. **SplashScreens**
- **TotalScreens** : Nombre total de splash screens
- **CurrentIndex** : Index actuel dans la séquence
- **RemainingScreens** : Nombre de screens restants
- **Progress** : Pourcentage de progression (0-100)

### 3. **UserInteraction**
- **TotalSkips** : Nombre total de skips effectués
- **SkipRate** : Taux de skip par minute

### 4. **Status**
- **IsCompleted** : Si tous les screens sont terminés
- **IsActive** : Si le SplashScreenManager est actif
- **Timestamp** : Horodatage actuel

## ?? Utilisation

### Récupérer l'État depuis le Serveur

#### Client BACKEND récupère l'état
```csharp
// Dans ServerManager après connexion du premier client BACKEND
var gameState = mainGameScene.GetGameState();

// gameState.Scene contiendra :
{
    "CurrentScene": "Credits",
    "ScenePath": "res://Scenes/Credits.tscn",
    "SceneState": {
        "SceneInfo": {...},
        "SplashScreens": {...},
        "UserInteraction": {...},
        "Status": {...}
    }
}
```

### Monitoring en Temps Réel
```csharp
// Timer pour surveiller l'avancement des crédits
var timer = new Timer { WaitTime = 1.0 };
timer.Timeout += () =>
{
    if (GetTree().CurrentScene is Credits creditsScene)
    {
        var state = creditsScene.GetSceneState();
        var splashInfo = state.SplashScreens;
        
        GD.Print($"Progression: {splashInfo.Progress}%");
        GD.Print($"Screen: {splashInfo.CurrentIndex}/{splashInfo.TotalScreens}");
    }
};
```

## ?? Exemples d'État

### État Initial (Début des Crédits)
```json
{
    "SceneInfo": {
        "SceneName": "Credits",
        "SceneType": "SplashScreen",
        "StartTime": "2024-01-15T14:30:00Z",
        "ElapsedTime": 0.05,
        "ElapsedTimeFormatted": "00:00"
    },
    "SplashScreens": {
        "TotalScreens": 3,
        "CurrentIndex": 0,
        "RemainingScreens": 3,
        "Progress": 0.0
    },
    "UserInteraction": {
        "TotalSkips": 0,
        "SkipRate": 0.0
    },
    "Status": {
        "IsCompleted": false,
        "IsActive": true,
        "Timestamp": "2024-01-15T14:30:00Z"
    }
}
```

### État en Cours (50% Progression)
```json
{
    "SceneInfo": {
        "ElapsedTime": 3.25,
        "ElapsedTimeFormatted": "00:03"
    },
    "SplashScreens": {
        "TotalScreens": 3,
        "CurrentIndex": 1,
        "RemainingScreens": 2,
        "Progress": 33.33
    },
    "UserInteraction": {
        "TotalSkips": 1,
        "SkipRate": 18.46
    },
    "Status": {
        "IsCompleted": false,
        "IsActive": true
    }
}
```

### État Final (Crédits Terminés)
```json
{
    "SceneInfo": {
        "ElapsedTime": 6.5,
        "ElapsedTimeFormatted": "00:06"
    },
    "SplashScreens": {
        "TotalScreens": 3,
        "CurrentIndex": 3,
        "RemainingScreens": 0,
        "Progress": 100.0
    },
    "UserInteraction": {
        "TotalSkips": 0,
        "SkipRate": 0.0
    },
    "Status": {
        "IsCompleted": true,
        "IsActive": true
    }
}
```

## ?? Tracking des Skips

### Comptage des Skips
```csharp
// Chaque skip individuel
if (keyEvent.Keycode == Key.Space)
{
    _splashScreenManager.Skip();
    _totalSkips++;  // +1
}

// Skip all (compte tous les screens restants)
if (keyEvent.Keycode == Key.Escape)
{
    _splashScreenManager.SkipAll();
    _totalSkips += _splashScreenManager.GetSplashScreenCount() 
                   - _splashScreenManager.GetCurrentIndex();
}
```

### Calcul du Skip Rate
```csharp
SkipRate = _totalSkips / elapsedTime * 60  // Skips par minute
```

## ?? Logs Générés

### Au Démarrage
```
?? Credits: Initialisation...
?? 3 splash screens configurés
```

### Pendant l'Exécution
```
? Splash screen 1/3 terminé
?? Skip vers le splash screen suivant
? Splash screen 2/3 terminé
```

### À la Fin
```
?? Tous les crédits ont été affichés
?? État final des crédits: {"SceneInfo":{...},"SplashScreens":{...}}
?? Retour au menu principal...
```

## ?? Cas d'Usage Avancés

### 1. Analytics des Crédits
```csharp
var state = creditsScene.GetSceneState();

// Combien de joueurs skip les crédits ?
if (state.UserInteraction.TotalSkips > 0)
{
    Analytics.Track("credits_skipped", new {
        skips = state.UserInteraction.TotalSkips,
        elapsed_time = state.SceneInfo.ElapsedTime
    });
}
```

### 2. Achievement: "Patient Viewer"
```csharp
// Débloquer si l'utilisateur regarde tous les crédits sans skip
if (state.Status.IsCompleted && state.UserInteraction.TotalSkips == 0)
{
    AchievementManager.Unlock("patient_viewer");
}
```

### 3. Admin Dashboard
```csharp
// Afficher les stats en temps réel pour les admins
var state = GetGameState();
var credits = state.Scene.SceneState;

Dashboard.Display($"Credits Progress: {credits.SplashScreens.Progress}%");
Dashboard.Display($"Skips: {credits.UserInteraction.TotalSkips}");
```

## ?? Personnalisation

### Ajouter Plus de Métriques
```csharp
public object GetSceneState()
{
    return new
    {
        // ...existing properties...,
        
        Performance = new
        {
            FrameRate = Engine.GetFramesPerSecond(),
            MemoryUsage = OS.GetStaticMemoryUsage()
        },
        
        Audio = new
        {
            IsMusicPlaying = _backgroundMusic?.IsPlaying() ?? false,
            Volume = AudioServer.GetBusVolumeDb(0)
        }
    };
}
```

### Tracking des Interactions Détaillées
```csharp
private List<string> _interactionHistory = new();

public override void _Input(InputEvent @event)
{
    if (@event is InputEventKey keyEvent && keyEvent.Pressed)
    {
        _interactionHistory.Add($"{DateTime.UtcNow:HH:mm:ss} - Key: {keyEvent.Keycode}");
    }
}

public object GetSceneState()
{
    return new
    {
        // ...
        InteractionHistory = _interactionHistory.TakeLast(10).ToList()
    };
}
```

## ?? Intégration avec MainGameScene

Lorsqu'un client BACKEND se connecte et que `Credits` est la scène active :

```csharp
// Dans ServerManager.HandleClientConnected
var gameState = mainGameScene.GetGameState();

// Envoi au client BACKEND
await network.SendMessageToClient(backendClientId, 
    JsonSerializer.Serialize(gameState));
```

Le client BACKEND reçoit :
```json
{
    "Server": {...},
    "Encryption": {...},
    "Clients": [{...}],
    "Scene": {
        "CurrentScene": "Credits",
        "ScenePath": "res://Scenes/Credits.tscn",
        "SceneState": {
            "SceneInfo": {...},
            "SplashScreens": {
                "Progress": 33.33
            },
            "UserInteraction": {...}
        }
    }
}
```

## ?? Conclusion

La scène `Credits` implémente maintenant `IScene`, permettant :
- ? Monitoring de la progression des crédits
- ? Tracking des interactions utilisateur
- ? Analytics détaillées
- ? Intégration complète avec le système `GetGameState()`

**Les administrateurs peuvent maintenant surveiller en temps réel l'avancement des crédits !** ??
