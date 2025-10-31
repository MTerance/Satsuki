# ?? Sc�nario d'Utilisation - Credits avec IScene

## Sc�nario: Monitoring des Cr�dits par un Client BACKEND

### ?? Contexte
Un administrateur se connecte en tant que client BACKEND pendant que les cr�dits sont affich�s. Il souhaite surveiller la progression et les interactions utilisateur.

---

## ?? Flux Complet

### 1. D�marrage des Cr�dits
```
Joueur lance les cr�dits
    ?
Credits._Ready()
    ?? _sceneStartTime = DateTime.UtcNow
    ?? SplashScreenManager cr��
    ?? 3 splash screens configur�s
    ?? StartSequence()
```

**�tat Initial :**
```json
{
    "SceneInfo": {
        "SceneName": "Credits",
        "ElapsedTime": 0.05,
        "ElapsedTimeFormatted": "00:00"
    },
    "SplashScreens": {
        "TotalScreens": 3,
        "CurrentIndex": 0,
        "Progress": 0.0
    },
    "UserInteraction": {
        "TotalSkips": 0,
        "SkipRate": 0.0
    }
}
```

---

### 2. Client BACKEND se Connecte

```
Admin ouvre l'application BACKEND
    ?
Client BACKEND se connecte au serveur
    ?
ServerManager.HandleClientConnected("Client_1")
    ?
RequestClientType envoy�
    ?
Client r�pond: BACKEND + password
    ?
Authentification r�ussie
    ?
mainGameScene.GetGameState() appel�
    ?
GetTree().CurrentScene = Credits
    ?
Credits.GetSceneState() invoqu� par r�flexion
    ?
�tat envoy� au client BACKEND
```

**Message re�u par le client BACKEND :**
```json
{
    "Server": {
        "IsRunning": true,
        "ConnectedClients": 1
    },
    "Scene": {
        "CurrentScene": "Credits",
        "ScenePath": "res://Scenes/Credits.tscn",
        "SceneState": {
            "SceneInfo": {
                "SceneName": "Credits",
                "ElapsedTime": 1.23,
                "ElapsedTimeFormatted": "00:01"
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
                "IsActive": true
            }
        }
    }
}
```

---

### 3. Progression des Cr�dits

#### T = 0s - Premier Splash Screen
```
?? Affichage: "SATSUKI" (2.5s)
Progress: 0%
```

#### T = 1.5s - Joueur Skip
```
?? Joueur appuie sur Espace
    ?
_splashScreenManager.Skip()
    ?
_totalSkips++ (= 1)
    ?
FadeOut() ? FadeIn() prochain screen
```

**�tat mis � jour :**
```json
{
    "SplashScreens": {
        "CurrentIndex": 1,
        "Progress": 33.33
    },
    "UserInteraction": {
        "TotalSkips": 1,
        "SkipRate": 40.0  // 1 skip / 1.5s * 60
    }
}
```

#### T = 3.5s - Deuxi�me Splash Screen
```
?? Affichage: "D�velopp� par\nMTerance" (2.0s)
Progress: 33.33%
```

#### T = 5.5s - Auto-transition
```
? Splash screen 2/3 termin�
    ?
FadeOut() ? FadeIn() prochain screen
```

**�tat mis � jour :**
```json
{
    "SplashScreens": {
        "CurrentIndex": 2,
        "Progress": 66.67
    },
    "SceneInfo": {
        "ElapsedTime": 5.5,
        "ElapsedTimeFormatted": "00:05"
    }
}
```

#### T = 7.5s - Dernier Splash Screen
```
?? Affichage: "Merci d'avoir jou�!" (2.0s)
Progress: 66.67%
```

#### T = 9.5s - Fin des Cr�dits
```
? Splash screen 3/3 termin�
    ?
OnAllSplashScreensCompleted()
    ?
�tat final logu�
    ?
Timer 1s
    ?
ChangeSceneToFile("MainGameScene.tscn")
```

**�tat final :**
```json
{
    "SceneInfo": {
        "ElapsedTime": 9.5,
        "ElapsedTimeFormatted": "00:09"
    },
    "SplashScreens": {
        "CurrentIndex": 3,
        "RemainingScreens": 0,
        "Progress": 100.0
    },
    "UserInteraction": {
        "TotalSkips": 1,
        "SkipRate": 6.32  // 1 skip / 9.5s * 60
    },
    "Status": {
        "IsCompleted": true
    }
}
```

---

## ?? Dashboard Client BACKEND

### Interface Affich�e

```
?????????????????????????????????????????????????????????????
?              SATSUKI - BACKEND DASHBOARD                  ?
?????????????????????????????????????????????????????????????
? Serveur: ? RUNNING                                       ?
? Clients Connect�s: 1                                      ?
?????????????????????????????????????????????????????????????
? Sc�ne Actuelle: Credits                                   ?
? Type: SplashScreen                                        ?
?????????????????????????????????????????????????????????????
? ?? PROGRESSION DES CR�DITS                               ?
?                                                            ?
? Progression: ???????????????? 66.67%                     ?
?                                                            ?
? Splash Actuel: 2 / 3                                     ?
? Restants: 1                                               ?
?                                                            ?
? Temps �coul�: 00:05                                       ?
?????????????????????????????????????????????????????????????
? ?? INTERACTIONS UTILISATEUR                               ?
?                                                            ?
? Skips Totaux: 1                                           ?
? Taux de Skip: 18.46 /min                                  ?
?????????????????????????????????????????????????????????????
? ?? STATUT                                                 ?
?                                                            ?
? Compl�t�: ?                                              ?
? Actif: ?                                                 ?
? Timestamp: 14:35:05                                       ?
?????????????????????????????????????????????????????????????
```

---

## ?? Exemple Code Client BACKEND

### Python Client
```python
import socket
import json
from datetime import datetime

class BackendClient:
    def __init__(self, host='127.0.0.1', port=80):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        
    def authenticate(self):
        # Attendre RequestClientType
        data = self.socket.recv(4096).decode('utf-8')
        request = json.loads(data)
        
        # R�pondre avec BACKEND + password
        response = {
            'order': 'ClientTypeResponse',
            'clientType': 'BACKEND',
            'password': '***Satsuk1***',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        self.socket.send(json.dumps(response).encode('utf-8'))
        
    def receive_game_state(self):
        data = self.socket.recv(8192).decode('utf-8')
        
        if data.startswith("GAME_STATE:"):
            json_data = data[11:]  # Remove "GAME_STATE:" prefix
            game_state = json.loads(json_data)
            
            return game_state
            
    def display_credits_state(self, game_state):
        scene = game_state['Scene']
        
        if scene['CurrentScene'] == 'Credits':
            state = scene['SceneState']
            
            print("?????????????????????????????????????????")
            print("?      CREDITS MONITORING               ?")
            print("?????????????????????????????????????????")
            
            # Scene Info
            info = state['SceneInfo']
            print(f"? Temps �coul�: {info['ElapsedTimeFormatted']}")
            
            # Splash Screens
            splash = state['SplashScreens']
            progress_bar = self.create_progress_bar(splash['Progress'])
            print(f"? Progression: {progress_bar} {splash['Progress']}%")
            print(f"? Screen: {splash['CurrentIndex']}/{splash['TotalScreens']}")
            
            # User Interaction
            user = state['UserInteraction']
            print(f"? Skips: {user['TotalSkips']}")
            print(f"? Skip Rate: {user['SkipRate']} /min")
            
            # Status
            status = state['Status']
            completed = "?" if status['IsCompleted'] else "?"
            print(f"? Compl�t�: {completed}")
            
            print("?????????????????????????????????????????")
            
    def create_progress_bar(self, progress, width=20):
        filled = int(progress / 100 * width)
        bar = "?" * filled + "?" * (width - filled)
        return bar

# Utilisation
client = BackendClient()
client.authenticate()

game_state = client.receive_game_state()
client.display_credits_state(game_state)
```

**Sortie Console :**
```
?????????????????????????????????????????
?      CREDITS MONITORING               ?
?????????????????????????????????????????
? Temps �coul�: 00:05
? Progression: ???????????????????? 66.67%
? Screen: 2/3
? Skips: 1
? Skip Rate: 18.46 /min
? Compl�t�: ?
?????????????????????????????????????????
```

---

## ?? Analytics et M�triques

### M�triques Collect�es
```csharp
// Dans OnAllSplashScreensCompleted
var finalState = GetSceneState();

Analytics.Track("credits_completed", new
{
    elapsed_time = finalState.SceneInfo.ElapsedTime,
    total_skips = finalState.UserInteraction.TotalSkips,
    skip_rate = finalState.UserInteraction.SkipRate,
    completed_naturally = finalState.UserInteraction.TotalSkips == 0
});
```

### Rapport Statistique
```
???????????????????????????????????????
 CREDITS SESSION REPORT
???????????????????????????????????????
 Session ID: CS_20240115_143000
 Date: 2024-01-15 14:30:00 UTC
???????????????????????????????????????
 Dur�e Totale: 00:09
 Splash Screens: 3
 
 Interactions:
  - Skips: 1
  - Skip Rate: 6.32/min
  - Compl�t�: ?
  
 Comportement:
  - Patient Viewer: ? (1 skip)
  - Speed Runner: ? (pas tous skipp�s)
  - Normal Viewer: ?
???????????????????????????????????????
```

---

## ?? Achievements Potentiels

### 1. "Patient Viewer" ??
```csharp
if (state.Status.IsCompleted && state.UserInteraction.TotalSkips == 0)
{
    AchievementManager.Unlock("patient_viewer");
    // Regarde tous les cr�dits sans skip
}
```

### 2. "Speed Runner" ?
```csharp
if (state.SceneInfo.ElapsedTime < 3.0 && state.Status.IsCompleted)
{
    AchievementManager.Unlock("speed_runner");
    // Termine les cr�dits en moins de 3 secondes
}
```

### 3. "First Time Viewer" ??
```csharp
if (!PlayerPrefs.HasKey("credits_seen"))
{
    PlayerPrefs.SetBool("credits_seen", true);
    AchievementManager.Unlock("first_time_viewer");
}
```

---

## ?? Conclusion

Ce sc�nario d�montre :
- ? Monitoring en temps r�el des cr�dits
- ? Tracking des interactions utilisateur
- ? Int�gration compl�te BACKEND
- ? Analytics et m�triques d�taill�es

**Les administrateurs peuvent maintenant surveiller pr�cis�ment comment les joueurs interagissent avec les cr�dits !** ??
