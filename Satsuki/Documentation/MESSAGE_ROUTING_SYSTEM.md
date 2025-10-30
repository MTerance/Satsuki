# ?? Syst�me de Routing des Messages JSON

## Vue d'ensemble

Le syst�me de routing des messages permet de diriger les messages JSON vers le bon destinataire : `MainGameScene` (Game) ou la sc�ne actuelle (Scene).

## ?? Architecture du Routing

### Format du Message JSON

```json
{
    "target": "Game" | "Scene",
    "order": "CommandName",      // Si message BACKEND
    "request": "RequestName",    // Si message client
    "...": "autres donn�es"
}
```

---

## ?? Target: Game

Messages destin�s au `MainGameScene` pour la gestion du serveur et du jeu global.

### Format BACKEND (Order)

```json
{
    "target": "Game",
    "order": "GetGameState",
    "timestamp": "2024-01-15T14:30:00Z"
}
```

### Format Client (Request)

```json
{
    "target": "Game",
    "request": "GetServerInfo",
    "timestamp": "2024-01-15T14:30:00Z"
}
```

---

## ?? Target: Scene

Messages destin�s � la sc�ne actuellement active.

### Format BACKEND (Order)

```json
{
    "target": "Scene",
    "order": "PauseGame",
    "timestamp": "2024-01-15T14:30:00Z"
}
```

### Format Client (Request)

```json
{
    "target": "Scene",
    "request": "SubmitAnswer",
    "questionId": 42,
    "answer": "Paris",
    "timestamp": "2024-01-15T14:30:00Z"
}
```

---

## ?? Orders Game (BACKEND)

### 1. GetGameState

R�cup�re l'�tat complet du jeu.

**Request :**
```json
{
    "target": "Game",
    "order": "GetGameState"
}
```

**Response :**
```json
{
    "Server": {...},
    "Encryption": {...},
    "Clients": [...],
    "Scene": {...}
}
```

---

### 2. DisconnectClient

D�connecte un client sp�cifique.

**Request :**
```json
{
    "target": "Game",
    "order": "DisconnectClient",
    "targetClientId": "Client_2"
}
```

**Response :**
```
? Client Client_2 d�connect�
```

---

### 3. BroadcastMessage

Diffuse un message � tous les clients.

**Request :**
```json
{
    "target": "Game",
    "order": "BroadcastMessage",
    "message": "Maintenance dans 5 minutes"
}
```

**Response :**
```
? Message diffus�
```

---

### 4. SetDebugMode

Active/d�sactive le mode debug.

**Request :**
```json
{
    "target": "Game",
    "order": "SetDebugMode",
    "enabled": true
}
```

**Response :**
```
? Mode debug: ACTIV�
```

---

## ?? Requests Game (Clients)

### 1. GetServerInfo

R�cup�re les informations du serveur.

**Request :**
```json
{
    "target": "Game",
    "request": "GetServerInfo"
}
```

**Response :**
```json
{
    "IsRunning": true,
    "ConnectedClients": 3,
    "PendingMessages": 0,
    "Timestamp": "2024-01-15T14:30:00Z"
}
```

---

### 2. Ping

Envoie un ping au serveur.

**Request :**
```json
{
    "target": "Game",
    "request": "Ping"
}
```

**Response :**
```json
{
    "target": "Game",
    "response": "Pong",
    "timestamp": "2024-01-15T14:30:00Z"
}
```

---

## ?? Messages Scene

### Impl�mentation dans une Sc�ne

Pour qu'une sc�ne puisse recevoir des messages, elle doit impl�menter `INetworkScene` :

```csharp
using Godot;
using Satsuki.Interfaces;
using System.Text.Json;

public partial class QuizScene : Node, INetworkScene
{
    public object GetSceneState()
    {
        // Impl�mentation IScene
        return new { ... };
    }
    
    public void HandleSceneOrder(string clientId, string order, string jsonData)
    {
        // Traiter les orders BACKEND
        switch (order)
        {
            case "PauseQuiz":
                PauseQuiz();
                break;
                
            case "SkipQuestion":
                SkipQuestion();
                break;
                
            default:
                GD.Print($"Order inconnu: {order}");
                break;
        }
    }
    
    public void HandleSceneRequest(string clientId, string request, string jsonData)
    {
        // Traiter les requests clients
        using JsonDocument doc = JsonDocument.Parse(jsonData);
        JsonElement root = doc.RootElement;
        
        switch (request)
        {
            case "SubmitAnswer":
                if (root.TryGetProperty("answer", out JsonElement answerElement))
                {
                    string answer = answerElement.GetString();
                    HandleAnswer(clientId, answer);
                }
                break;
                
            case "RequestHint":
                SendHint(clientId);
                break;
                
            default:
                GD.Print($"Request inconnue: {request}");
                break;
        }
    }
}
```

---

## ?? Flux de Traitement

### Message vers Game

```
Client envoie JSON
    ?
MainGameScene.HandleMessage()
    ?
HandleJsonMessage()
    ?
V�rifie "target": "Game"
    ?
HandleGameMessage()
    ?
V�rifie "order" ou "request"
    ?
HandleGameOrder() ou HandleGameRequest()
    ?
Traite le message
    ?
Renvoie la r�ponse au client
```

---

### Message vers Scene

```
Client envoie JSON
    ?
MainGameScene.HandleMessage()
    ?
HandleJsonMessage()
    ?
V�rifie "target": "Scene"
    ?
HandleSceneMessage()
    ?
R�cup�re GetTree().CurrentScene
    ?
V�rifie "order" ou "request"
    ?
InvokeSceneMethod("HandleSceneOrder" ou "HandleSceneRequest")
    ?
Appelle la m�thode sur la sc�ne par r�flexion
    ?
La sc�ne traite le message
```

---

## ?? Gestion des Erreurs

### Sc�ne sans M�thode

Si la sc�ne n'impl�mente pas `HandleSceneOrder` ou `HandleSceneRequest` :

**Log :**
```
?? La sc�ne QuizScene n'impl�mente pas HandleSceneOrder
```

**Response au client :**
```json
{
    "target": "Scene",
    "error": "Method HandleSceneOrder not implemented",
    "sceneName": "QuizScene"
}
```

---

### Erreur d'Ex�cution

Si une erreur survient lors du traitement :

**Log :**
```
? Erreur lors de l'invocation de HandleSceneRequest: NullReferenceException
```

**Response au client :**
```json
{
    "target": "Scene",
    "error": "NullReferenceException: Object reference not set...",
    "method": "HandleSceneRequest"
}
```

---

## ?? Exemples Complets

### Exemple 1: Client BACKEND R�cup�re l'�tat du Jeu

**Client envoie :**
```json
{
    "target": "Game",
    "order": "GetGameState"
}
```

**Serveur traite :**
```
?? [GAME] Order de Client_1: GetGameState
? �tat du jeu envoy� � Client_1
```

**Client re�oit :**
```json
{
    "Server": {
        "IsRunning": true,
        "ConnectedClients": 2
    },
    "Scene": {
        "CurrentScene": "QuizScene",
        "SceneState": {...}
    }
}
```

---

### Exemple 2: Client PLAYER Soumet une R�ponse

**Client envoie :**
```json
{
    "target": "Scene",
    "request": "SubmitAnswer",
    "questionId": 5,
    "answer": "Paris",
    "timeTaken": 12.5
}
```

**Serveur traite :**
```
?? [SCENE] Request de Client_2 pour QuizScene: SubmitAnswer
? M�thode HandleSceneRequest invoqu�e sur QuizScene
```

**QuizScene traite :**
```csharp
public void HandleSceneRequest(string clientId, string request, string jsonData)
{
    using JsonDocument doc = JsonDocument.Parse(jsonData);
    JsonElement root = doc.RootElement;
    
    if (request == "SubmitAnswer")
    {
        int questionId = root.GetProperty("questionId").GetInt32();
        string answer = root.GetProperty("answer").GetString();
        float timeTaken = root.GetProperty("timeTaken").GetSingle();
        
        // V�rifier la r�ponse
        bool isCorrect = CheckAnswer(questionId, answer);
        
        // Renvoyer le r�sultat
        var response = new
        {
            target = "Scene",
            response = "AnswerResult",
            questionId = questionId,
            isCorrect = isCorrect,
            timeTaken = timeTaken
        };
        
        // Envoyer via MainGameScene
        SendResponseToClient(clientId, response);
    }
}
```

---

### Exemple 3: BACKEND Pause un Quiz

**Client BACKEND envoie :**
```json
{
    "target": "Scene",
    "order": "PauseQuiz",
    "reason": "Technical issue"
}
```

**Serveur traite :**
```
?? [SCENE] Order de Client_1 pour QuizScene: PauseQuiz
? M�thode HandleSceneOrder invoqu�e sur QuizScene
```

**QuizScene traite :**
```csharp
public void HandleSceneOrder(string clientId, string order, string jsonData)
{
    if (order == "PauseQuiz")
    {
        _isPaused = true;
        GD.Print("?? Quiz mis en pause par BACKEND");
        
        // Notifier tous les joueurs
        BroadcastToAllPlayers(new
        {
            target = "Scene",
            notification = "QuizPaused",
            reason = "Technical issue"
        });
    }
}
```

---

## ?? Interface INetworkScene

```csharp
namespace Satsuki.Interfaces
{
    public interface INetworkScene : IScene
    {
        void HandleSceneOrder(string clientId, string order, string jsonData);
        void HandleSceneRequest(string clientId, string request, string jsonData);
    }
}
```

**Avantages :**
- ? Contrat clair pour les sc�nes r�seau
- ? H�ritage de `IScene` (GetSceneState)
- ? S�paration Orders/Requests

---

## ?? R�trocompatibilit�

L'ancien format (sans `target`) est toujours support� :

```json
{
    "order": "ClientTypeResponse",
    "clientType": "PLAYER"
}
```

Ce format sera trait� comme avant pour l'authentification des clients.

---

## ?? Comparaison Order vs Request

| Aspect | Order (BACKEND) | Request (Client) |
|--------|-----------------|------------------|
| **Source** | Client BACKEND authentifi� | Tout client |
| **Permissions** | Administrateur | Standard |
| **Exemples** | PauseGame, KickPlayer | SubmitAnswer, GetInfo |
| **S�curit�** | ? Mot de passe requis | ? Pas d'authentification |

---

## ?? Extensibilit�

### Ajouter un Nouveau Order Game

```csharp
case "RestartServer":
    if (root.TryGetProperty("delay", out JsonElement delayElement))
    {
        int delay = delayElement.GetInt32();
        RestartServerWithDelay(delay);
    }
    break;
```

### Ajouter une Nouvelle Request Game

```csharp
case "GetPlayerList":
    var players = GetAllPlayers();
    SendMessageToClient(clientId, JsonSerializer.Serialize(players));
    break;
```

---

## ?? Conclusion

Le syst�me de routing JSON offre :
- ? Routing intelligent Game/Scene
- ? Distinction Order/Request
- ? Gestion d'erreurs robuste
- ? Extensibilit� facile
- ? R�trocompatibilit�
- ? Interface claire (INetworkScene)

**Les messages peuvent maintenant �tre rout�s pr�cis�ment vers le bon destinataire avec un syst�me flexible et extensible !** ??
