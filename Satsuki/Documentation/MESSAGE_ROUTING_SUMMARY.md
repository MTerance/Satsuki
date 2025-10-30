# ?? Résumé - Système de Routing JSON

## ? Objectif Atteint

Implémentation d'un système de routing des messages JSON avec distinction `target` (Game/Scene) et `order`/`request` (BACKEND/Client).

---

## ?? Fichiers Modifiés/Créés

```
Scenes/
??? MainGameScene.cs                    ? Modifié
??? Examples/
    ??? NetworkQuizScene.cs             ? Créé (exemple)

Interfaces/
??? INetworkScene.cs                    ? Créé

Documentation/
??? MESSAGE_ROUTING_SYSTEM.md           ? Créé
```

---

## ?? Nouveau Format de Message

### Structure de Base

```json
{
    "target": "Game" | "Scene",
    "order": "...",       // Si BACKEND
    "request": "...",     // Si Client
    "...": "données"
}
```

---

## ?? Target: Game

### Orders BACKEND Disponibles

| Order | Description | Exemple |
|-------|-------------|---------|
| **GetGameState** | Récupère l'état complet | `{"target": "Game", "order": "GetGameState"}` |
| **DisconnectClient** | Déconnecte un client | `{"target": "Game", "order": "DisconnectClient", "targetClientId": "Client_2"}` |
| **BroadcastMessage** | Diffuse un message | `{"target": "Game", "order": "BroadcastMessage", "message": "..."}` |
| **SetDebugMode** | Active/désactive debug | `{"target": "Game", "order": "SetDebugMode", "enabled": true}` |

### Requests Client Disponibles

| Request | Description | Exemple |
|---------|-------------|---------|
| **GetServerInfo** | Infos du serveur | `{"target": "Game", "request": "GetServerInfo"}` |
| **Ping** | Ping le serveur | `{"target": "Game", "request": "Ping"}` |

---

## ?? Target: Scene

### Implémentation dans une Scène

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
Réponse au client
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
InvokeSceneMethod() (réflexion)
    ?
HandleSceneOrder() | HandleSceneRequest()
    ?
Traitement par la scène
```

---

## ?? Méthodes Ajoutées à MainGameScene

| Méthode | Description |
|---------|-------------|
| **HandleGameMessage** | Route les messages Game |
| **HandleGameOrder** | Traite les orders BACKEND pour Game |
| **HandleGameRequest** | Traite les requests clients pour Game |
| **HandleSceneMessage** | Route les messages Scene |
| **InvokeSceneMethod** | Appelle les méthodes de la scène par réflexion |

---

## ?? Interface INetworkScene

```csharp
public interface INetworkScene : IScene
{
    void HandleSceneOrder(string clientId, string order, string jsonData);
    void HandleSceneRequest(string clientId, string request, string jsonData);
}
```

**Héritage** :
- ? `IScene` : Pour `GetSceneState()`
- ? Méthodes de traitement réseau

---

## ?? Exemples d'Utilisation

### 1. Client BACKEND Récupère l'État

**Envoi** :
```json
{
    "target": "Game",
    "order": "GetGameState"
}
```

**Réception** :
```json
{
    "Server": {...},
    "Scene": {
        "CurrentScene": "QuizScene",
        "SceneState": {...}
    }
}
```

### 2. Client Soumet une Réponse

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
        // Vérifier réponse
        // Renvoyer résultat
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

### Scène sans Méthode

**Log** :
```
?? La scène QuizScene n'implémente pas HandleSceneOrder
```

**Response** :
```json
{
    "target": "Scene",
    "error": "Method HandleSceneOrder not implemented",
    "sceneName": "QuizScene"
}
```

### Erreur d'Exécution

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
| **Source** | Client authentifié BACKEND | Tout client |
| **Permissions** | Administrateur | Standard |
| **Sécurité** | ? Mot de passe | ? Pas de vérification |
| **Usage** | Administration, contrôle | Gameplay, interaction |
| **Exemples** | PauseGame, KickPlayer | SubmitAnswer, GetInfo |

---

## ?? Exemple Complet: NetworkQuizScene

**Fichier** : `Scenes/Examples/NetworkQuizScene.cs`

**Implémente** :
- ? `INetworkScene`
- ? `GetSceneState()`
- ? `HandleSceneOrder()` (6 orders)
- ? `HandleSceneRequest()` (4 requests)

**Orders Supportés** :
- StartQuiz
- PauseQuiz
- ResumeQuiz
- StopQuiz
- SkipQuestion
- GetQuizState

**Requests Supportés** :
- SubmitAnswer
- RequestHint
- GetCurrentQuestion
- JoinQuiz

---

## ?? Rétrocompatibilité

L'ancien format (authentification) est toujours supporté :

```json
{
    "order": "ClientTypeResponse",
    "clientType": "PLAYER"
}
```

---

## ?? Avantages du Système

? **Routing Intelligent**
- Messages dirigés vers le bon destinataire
- Séparation Game/Scene claire

? **Distinction Order/Request**
- Sécurité : Orders = BACKEND only
- Flexibilité : Requests = tous clients

? **Extensibilité**
- Facile d'ajouter de nouveaux orders/requests
- Chaque scène définit ses propres commandes

? **Gestion d'Erreurs**
- Erreurs capturées et renvoyées
- Logs détaillés

? **Type-Safe avec Interfaces**
- `INetworkScene` définit le contrat
- Intellisense et vérification à la compilation

---

## ?? Statistiques

### Lignes de Code Ajoutées

- **MainGameScene.cs** : ~200 lignes
- **INetworkScene.cs** : 10 lignes
- **NetworkQuizScene.cs** : 300 lignes (exemple)
- **Documentation** : 400+ lignes

### Méthodes Créées

- MainGameScene : 6 nouvelles méthodes
- INetworkScene : 2 méthodes d'interface
- NetworkQuizScene : 15+ méthodes

---

## ? Build Status

**Compilation** : ? Réussie  
**Erreurs** : ? Aucune  
**Warnings** : ? Aucun  
**Tests** : ? Pas d'erreurs  

---

## ?? Conclusion

Le système de routing JSON est maintenant opérationnel :

- ? **Routing Game/Scene** implémenté
- ? **Orders/Requests** distinction claire
- ? **Interface INetworkScene** créée
- ? **Exemple complet** fourni (NetworkQuizScene)
- ? **Documentation** complète
- ? **Gestion d'erreurs** robuste
- ? **Rétrocompatibilité** maintenue

**Les messages peuvent maintenant être routés intelligemment vers MainGameScene ou la scène actuelle avec un système flexible, sécurisé et extensible !** ????

---

## ?? Fichiers de Documentation

1. **MESSAGE_ROUTING_SYSTEM.md** : Documentation complète du système
2. **Ce fichier** : Résumé et vue d'ensemble

**Le système est prêt pour l'intégration dans les scènes de quiz et autres scènes réseau !** ??
