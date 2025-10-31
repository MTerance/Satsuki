# ?? Système de Routing des Messages JSON

## Vue d'ensemble

Le système de routing des messages permet de diriger les messages JSON vers le bon destinataire : `MainGameScene` (Game) ou la scène actuelle (Scene).

## ?? Architecture du Routing

### Format du Message JSON

```json
{
    "target": "Game" | "Scene",
    "order": "CommandName",      // Si message BACKEND
    "request": "RequestName",    // Si message client
    "...": "autres données"
}
```

---

## ?? Target: Game

Messages destinés au `MainGameScene` pour la gestion du serveur et du jeu global.

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

Messages destinés à la scène actuellement active.

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

Récupère l'état complet du jeu.

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

Déconnecte un client spécifique.

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
? Client Client_2 déconnecté
```

---

### 3. BroadcastMessage

Diffuse un message à tous les clients.

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
? Message diffusé
```

---

### 4. SetDebugMode

Active/désactive le mode debug.

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
? Mode debug: ACTIVÉ
```

---

## ?? Requests Game (Clients)

### 1. GetServerInfo

Récupère les informations du serveur.

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

### Implémentation dans une Scène

Pour qu'une scène puisse recevoir des messages, elle doit implémenter `INetworkScene` :

```csharp
using Godot;
using Satsuki.Interfaces;
using System.Text.Json;

public partial class QuizScene : Node, INetworkScene
{
    public object GetSceneState()
    {
        // Implémentation IScene
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
Vérifie "target": "Game"
    ?
HandleGameMessage()
    ?
Vérifie "order" ou "request"
    ?
HandleGameOrder() ou HandleGameRequest()
    ?
Traite le message
    ?
Renvoie la réponse au client
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
Vérifie "target": "Scene"
    ?
HandleSceneMessage()
    ?
Récupère GetTree().CurrentScene
    ?
Vérifie "order" ou "request"
    ?
InvokeSceneMethod("HandleSceneOrder" ou "HandleSceneRequest")
    ?
Appelle la méthode sur la scène par réflexion
    ?
La scène traite le message
```

---

## ?? Gestion des Erreurs

### Scène sans Méthode

Si la scène n'implémente pas `HandleSceneOrder` ou `HandleSceneRequest` :

**Log :**
```
?? La scène QuizScene n'implémente pas HandleSceneOrder
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

### Erreur d'Exécution

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

### Exemple 1: Client BACKEND Récupère l'État du Jeu

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
? État du jeu envoyé à Client_1
```

**Client reçoit :**
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

### Exemple 2: Client PLAYER Soumet une Réponse

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
? Méthode HandleSceneRequest invoquée sur QuizScene
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
        
        // Vérifier la réponse
        bool isCorrect = CheckAnswer(questionId, answer);
        
        // Renvoyer le résultat
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
? Méthode HandleSceneOrder invoquée sur QuizScene
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
- ? Contrat clair pour les scènes réseau
- ? Héritage de `IScene` (GetSceneState)
- ? Séparation Orders/Requests

---

## ?? Rétrocompatibilité

L'ancien format (sans `target`) est toujours supporté :

```json
{
    "order": "ClientTypeResponse",
    "clientType": "PLAYER"
}
```

Ce format sera traité comme avant pour l'authentification des clients.

---

## ?? Comparaison Order vs Request

| Aspect | Order (BACKEND) | Request (Client) |
|--------|-----------------|------------------|
| **Source** | Client BACKEND authentifié | Tout client |
| **Permissions** | Administrateur | Standard |
| **Exemples** | PauseGame, KickPlayer | SubmitAnswer, GetInfo |
| **Sécurité** | ? Mot de passe requis | ? Pas d'authentification |

---

## ?? Extensibilité

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

Le système de routing JSON offre :
- ? Routing intelligent Game/Scene
- ? Distinction Order/Request
- ? Gestion d'erreurs robuste
- ? Extensibilité facile
- ? Rétrocompatibilité
- ? Interface claire (INetworkScene)

**Les messages peuvent maintenant être routés précisément vers le bon destinataire avec un système flexible et extensible !** ??
