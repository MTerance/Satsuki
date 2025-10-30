# ?? R�sum� - Syst�me de Routing JSON

## ? Objectif Atteint

Impl�mentation d'un syst�me de routing des messages JSON avec distinction `target` (Game/Scene) et `order`/`request` (BACKEND/Client).

---

## ?? Fichiers Modifi�s/Cr��s

```
Scenes/
??? MainGameScene.cs                    ? Modifi�
??? Examples/
    ??? NetworkQuizScene.cs             ? Cr�� (exemple)

Interfaces/
??? INetworkScene.cs                    ? Cr��

Documentation/
??? MESSAGE_ROUTING_SYSTEM.md           ? Cr��
```

---

## ?? Nouveau Format de Message

### Structure de Base

```json
{
    "target": "Game" | "Scene",
    "order": "...",       // Si BACKEND
    "request": "...",     // Si Client
    "...": "donn�es"
}
```

---

## ?? Target: Game

### Orders BACKEND Disponibles

| Order | Description | Exemple |
|-------|-------------|---------|
| **GetGameState** | R�cup�re l'�tat complet | `{"target": "Game", "order": "GetGameState"}` |
| **DisconnectClient** | D�connecte un client | `{"target": "Game", "order": "DisconnectClient", "targetClientId": "Client_2"}` |
| **BroadcastMessage** | Diffuse un message | `{"target": "Game", "order": "BroadcastMessage", "message": "..."}` |
| **SetDebugMode** | Active/d�sactive debug | `{"target": "Game", "order": "SetDebugMode", "enabled": true}` |

### Requests Client Disponibles

| Request | Description | Exemple |
|---------|-------------|---------|
| **GetServerInfo** | Infos du serveur | `{"target": "Game", "request": "GetServerInfo"}` |
| **Ping** | Ping le serveur | `{"target": "Game", "request": "Ping"}` |

---

## ?? Target: Scene

### Impl�mentation dans une Sc�ne

```csharp
using Satsuki.Interfaces;

public partial class MyScene : Node, INetworkScene
{
    // IScene
    public object GetSceneState() { ... }
    
    // INetworkScene
    public void HandleSceneOrder(string clientId, string order, string jsonData)
    {
        // Traiter les orders BACKEND
    }
    
    public void HandleSceneRequest(string clientId, string request, string jsonData)
    {
        // Traiter les requests clients
    }
}
```

---

## ?? Flux de Traitement

### Message vers Game

```
Client ? JSON
    ?
MainGameScene.HandleMessage()
    ?
HandleJsonMessage()
    ?
"target": "Game" ?
    ?
HandleGameMessage()
    ?
"order" ou "request" ?
    ?
HandleGameOrder() | HandleGameRequest()
    ?
Traitement
    ?
R�ponse au client
```

### Message vers Scene

```
Client ? JSON
    ?
MainGameScene.HandleMessage()
    ?
HandleJsonMessage()
    ?
"target": "Scene" ?
    ?
HandleSceneMessage()
    ?
GetTree().CurrentScene
    ?
InvokeSceneMethod() (r�flexion)
    ?
HandleSceneOrder() | HandleSceneRequest()
    ?
Traitement par la sc�ne
```

---

## ?? M�thodes Ajout�es � MainGameScene

| M�thode | Description |
|---------|-------------|
| **HandleGameMessage** | Route les messages Game |
| **HandleGameOrder** | Traite les orders BACKEND pour Game |
| **HandleGameRequest** | Traite les requests clients pour Game |
| **HandleSceneMessage** | Route les messages Scene |
| **InvokeSceneMethod** | Appelle les m�thodes de la sc�ne par r�flexion |

---

## ?? Interface INetworkScene

```csharp
public interface INetworkScene : IScene
{
    void HandleSceneOrder(string clientId, string order, string jsonData);
    void HandleSceneRequest(string clientId, string request, string jsonData);
}
```

**H�ritage** :
- ? `IScene` : Pour `GetSceneState()`
- ? M�thodes de traitement r�seau

---

## ?? Exemples d'Utilisation

### 1. Client BACKEND R�cup�re l'�tat

**Envoi** :
```json
{
    "target": "Game",
    "order": "GetGameState"
}
```

**R�ception** :
```json
{
    "Server": {...},
    "Scene": {
        "CurrentScene": "QuizScene",
        "SceneState": {...}
    }
}
```

### 2. Client Soumet une R�ponse

**Envoi** :
```json
{
    "target": "Scene",
    "request": "SubmitAnswer",
    "questionId": 5,
    "answer": "Paris"
}
```

**Traitement** :
```csharp
public void HandleSceneRequest(string clientId, string request, string jsonData)
{
    if (request == "SubmitAnswer")
    {
        // Parser JSON
        // V�rifier r�ponse
        // Renvoyer r�sultat
    }
}
```

### 3. BACKEND Pause un Quiz

**Envoi** :
```json
{
    "target": "Scene",
    "order": "PauseQuiz"
}
```

**Traitement** :
```csharp
public void HandleSceneOrder(string clientId, string order, string jsonData)
{
    if (order == "PauseQuiz")
    {
        _isPaused = true;
        // Notifier tous les joueurs
    }
}
```

---

## ?? Gestion des Erreurs

### Sc�ne sans M�thode

**Log** :
```
?? La sc�ne QuizScene n'impl�mente pas HandleSceneOrder
```

**Response** :
```json
{
    "target": "Scene",
    "error": "Method HandleSceneOrder not implemented",
    "sceneName": "QuizScene"
}
```

### Erreur d'Ex�cution

**Log** :
```
? Erreur lors de l'invocation de HandleSceneRequest: Exception...
```

**Response** :
```json
{
    "target": "Scene",
    "error": "Exception message...",
    "method": "HandleSceneRequest"
}
```

---

## ?? Comparaison Order vs Request

| Aspect | Order (BACKEND) | Request (Client) |
|--------|-----------------|------------------|
| **Source** | Client authentifi� BACKEND | Tout client |
| **Permissions** | Administrateur | Standard |
| **S�curit�** | ? Mot de passe | ? Pas de v�rification |
| **Usage** | Administration, contr�le | Gameplay, interaction |
| **Exemples** | PauseGame, KickPlayer | SubmitAnswer, GetInfo |

---

## ?? Exemple Complet: NetworkQuizScene

**Fichier** : `Scenes/Examples/NetworkQuizScene.cs`

**Impl�mente** :
- ? `INetworkScene`
- ? `GetSceneState()`
- ? `HandleSceneOrder()` (6 orders)
- ? `HandleSceneRequest()` (4 requests)

**Orders Support�s** :
- StartQuiz
- PauseQuiz
- ResumeQuiz
- StopQuiz
- SkipQuestion
- GetQuizState

**Requests Support�s** :
- SubmitAnswer
- RequestHint
- GetCurrentQuestion
- JoinQuiz

---

## ?? R�trocompatibilit�

L'ancien format (authentification) est toujours support� :

```json
{
    "order": "ClientTypeResponse",
    "clientType": "PLAYER"
}
```

---

## ?? Avantages du Syst�me

? **Routing Intelligent**
- Messages dirig�s vers le bon destinataire
- S�paration Game/Scene claire

? **Distinction Order/Request**
- S�curit� : Orders = BACKEND only
- Flexibilit� : Requests = tous clients

? **Extensibilit�**
- Facile d'ajouter de nouveaux orders/requests
- Chaque sc�ne d�finit ses propres commandes

? **Gestion d'Erreurs**
- Erreurs captur�es et renvoy�es
- Logs d�taill�s

? **Type-Safe avec Interfaces**
- `INetworkScene` d�finit le contrat
- Intellisense et v�rification � la compilation

---

## ?? Statistiques

### Lignes de Code Ajout�es

- **MainGameScene.cs** : ~200 lignes
- **INetworkScene.cs** : 10 lignes
- **NetworkQuizScene.cs** : 300 lignes (exemple)
- **Documentation** : 400+ lignes

### M�thodes Cr��es

- MainGameScene : 6 nouvelles m�thodes
- INetworkScene : 2 m�thodes d'interface
- NetworkQuizScene : 15+ m�thodes

---

## ? Build Status

**Compilation** : ? R�ussie  
**Erreurs** : ? Aucune  
**Warnings** : ? Aucun  
**Tests** : ? Pas d'erreurs  

---

## ?? Conclusion

Le syst�me de routing JSON est maintenant op�rationnel :

- ? **Routing Game/Scene** impl�ment�
- ? **Orders/Requests** distinction claire
- ? **Interface INetworkScene** cr��e
- ? **Exemple complet** fourni (NetworkQuizScene)
- ? **Documentation** compl�te
- ? **Gestion d'erreurs** robuste
- ? **R�trocompatibilit�** maintenue

**Les messages peuvent maintenant �tre rout�s intelligemment vers MainGameScene ou la sc�ne actuelle avec un syst�me flexible, s�curis� et extensible !** ????

---

## ?? Fichiers de Documentation

1. **MESSAGE_ROUTING_SYSTEM.md** : Documentation compl�te du syst�me
2. **Ce fichier** : R�sum� et vue d'ensemble

**Le syst�me est pr�t pour l'int�gration dans les sc�nes de quiz et autres sc�nes r�seau !** ??
