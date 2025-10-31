# ?? Credits Scene - Impl�mentation IScene

## Vue d'ensemble

La sc�ne `Credits` impl�mente l'interface `IScene` pour exposer son �tat via `GetSceneState()`, permettant au syst�me `GetGameState()` de r�cup�rer des informations d�taill�es sur les cr�dits en cours.

## ?? Structure de l'�tat Retourn�

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

## ?? Impl�mentation

### D�claration de la Classe
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

### M�thode GetSceneState()
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

## ?? M�triques Track�es

### 1. **SceneInfo**
- **SceneName** : Nom de la sc�ne ("Credits")
- **SceneType** : Type de sc�ne ("SplashScreen")
- **StartTime** : Heure de d�marrage (UTC)
- **ElapsedTime** : Temps �coul� en secondes
- **ElapsedTimeFormatted** : Temps formatt� (MM:SS)

### 2. **SplashScreens**
- **TotalScreens** : Nombre total de splash screens
- **CurrentIndex** : Index actuel dans la s�quence
- **RemainingScreens** : Nombre de screens restants
- **Progress** : Pourcentage de progression (0-100)

### 3. **UserInteraction**
- **TotalSkips** : Nombre total de skips effectu�s
- **SkipRate** : Taux de skip par minute

### 4. **Status**
- **IsCompleted** : Si tous les screens sont termin�s
- **IsActive** : Si le SplashScreenManager est actif
- **Timestamp** : Horodatage actuel

## ?? Utilisation

### R�cup�rer l'�tat depuis le Serveur

#### Client BACKEND r�cup�re l'�tat
```csharp
// Dans ServerManager apr�s connexion du premier client BACKEND
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

### Monitoring en Temps R�el
```csharp
// Timer pour surveiller l'avancement des cr�dits
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

## ?? Exemples d'�tat

### �tat Initial (D�but des Cr�dits)
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

### �tat en Cours (50% Progression)
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

### �tat Final (Cr�dits Termin�s)
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

## ?? Logs G�n�r�s

### Au D�marrage
```
?? Credits: Initialisation...
?? 3 splash screens configur�s
```

### Pendant l'Ex�cution
```
? Splash screen 1/3 termin�
?? Skip vers le splash screen suivant
? Splash screen 2/3 termin�
```

### � la Fin
```
?? Tous les cr�dits ont �t� affich�s
?? �tat final des cr�dits: {"SceneInfo":{...},"SplashScreens":{...}}
?? Retour au menu principal...
```

## ?? Cas d'Usage Avanc�s

### 1. Analytics des Cr�dits
```csharp
var state = creditsScene.GetSceneState();

// Combien de joueurs skip les cr�dits ?
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
// D�bloquer si l'utilisateur regarde tous les cr�dits sans skip
if (state.Status.IsCompleted && state.UserInteraction.TotalSkips == 0)
{
    AchievementManager.Unlock("patient_viewer");
}
```

### 3. Admin Dashboard
```csharp
// Afficher les stats en temps r�el pour les admins
var state = GetGameState();
var credits = state.Scene.SceneState;

Dashboard.Display($"Credits Progress: {credits.SplashScreens.Progress}%");
Dashboard.Display($"Skips: {credits.UserInteraction.TotalSkips}");
```

## ?? Personnalisation

### Ajouter Plus de M�triques
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

### Tracking des Interactions D�taill�es
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

## ?? Int�gration avec MainGameScene

Lorsqu'un client BACKEND se connecte et que `Credits` est la sc�ne active :

```csharp
// Dans ServerManager.HandleClientConnected
var gameState = mainGameScene.GetGameState();

// Envoi au client BACKEND
await network.SendMessageToClient(backendClientId, 
    JsonSerializer.Serialize(gameState));
```

Le client BACKEND re�oit :
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

La sc�ne `Credits` impl�mente maintenant `IScene`, permettant :
- ? Monitoring de la progression des cr�dits
- ? Tracking des interactions utilisateur
- ? Analytics d�taill�es
- ? Int�gration compl�te avec le syst�me `GetGameState()`

**Les administrateurs peuvent maintenant surveiller en temps r�el l'avancement des cr�dits !** ??
