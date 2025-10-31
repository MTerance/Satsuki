# ?? Architecture Serveur Refactoris�e - Satsuki

## ?? Vue d'ensemble

Cette refactorisation s�pare clairement les responsabilit�s entre la gestion de l'interface utilisateur et la gestion du serveur dans le projet Satsuki.

## ??? Nouvelle Architecture

### ?? Structure des Classes

```
MainGameScene.cs (UI & Scene Management)
??? GameServerHandler.cs (Server Logic)
?   ??? MessageReceiver
?   ??? MessageCrypto
?   ??? Network
??? ServerManager.cs (Server Lifecycle)
```

## ?? S�paration des Responsabilit�s

### ?? MainGameScene.cs
**Responsabilit�** : Gestion de l'interface utilisateur et de la logique de sc�ne

**Fonctionnalit�s** :
- ? Gestion des �v�nements UI
- ? Affichage des notifications r�seau
- ? Mise � jour des indicateurs de statut
- ? Gestion des changements de sc�ne
- ? Impl�mentation de `IScene`
- ? D�l�gation des commandes serveur

**Ce qui a �t� d�plac�** :
- ? Traitement des messages r�seau
- ? Gestion du cryptage
- ? Communication avec les clients
- ? Statistiques serveur

### ?? GameServerHandler.cs
**Responsabilit�** : Gestion compl�te du serveur de jeu

**Fonctionnalit�s** :
- ? Traitement des messages entrants
- ? Gestion du syst�me de cryptage
- ? Communication avec les clients
- ? Statistiques et debug serveur
- ? Gestion des types de messages
- ? Broadcasting de messages

**�v�nements �mis** :
- `ServerStarted`
- `ServerStopped` 
- `ServerError`
- `ClientConnected`
- `ClientDisconnected`
- `MessageReceived`

### ?? ServerManager.cs
**Responsabilit�** : Gestion du cycle de vie du serveur

**Fonctionnalit�s** :
- ? D�marrage/arr�t du serveur
- ? Authentification des clients BACKEND
- ? Gestion des types de clients
- ? AutoLoad Godot
- ? Interface avec GameServerHandler

## ?? Flux de Communication

```mermaid
graph TD
    A[Client] --> B[Network]
    B --> C[MessageReceiver]
    C --> D[GameServerHandler]
    D --> E[MainGameScene]
    E --> F[UI Update]
    
    G[ServerManager] --> D
    D --> H[Message Processing]
    H --> I[Client Response]
```

## ?? API Publique

### MainGameScene

```csharp
// Acc�s au gestionnaire serveur
GameServerHandler GetServerHandler()

// Communication simplifi�e
void SendMessageToClient(string clientId, string message, bool encrypt = true)
void BroadcastMessage(string message, bool encrypt = true)
int GetConnectedClientCount()

// Gestion des sc�nes
object GetSceneState()
object GetGameSceneState()
void ChangeScene(string scenePath)
```

### GameServerHandler

```csharp
// Communication r�seau
void SendMessageToClient(string clientId, string message, bool encrypt = true)
void BroadcastToAllClients(string message, bool encrypt = true)
void BroadcastToOtherClients(string senderClientId, string message, bool encrypt = true)
void DisconnectClient(string clientId)

// Gestion du cryptage
void ToggleEncryption()
void GenerateNewEncryptionKey()

// Traitement des messages
void ProcessMessagesHighFrequency()
void ProcessLimitedMessages(int maxMessages = 10)

// Informations
object GetServerState()
object GetCompleteGameState()
int GetConnectedClientCount()

// Debug
void ToggleDebugMode()
void ListConnectedClients()
```

## ?? Utilisation

### Depuis MainGameScene

```csharp
// Obtenir le gestionnaire serveur
var serverHandler = GetServerHandler();

// Envoyer un message
serverHandler.SendMessageToClient("Client_1", "Hello!", encrypt: true);

// Obtenir les statistiques
var state = serverHandler.GetCompleteGameState();

// API simplifi�e
SendMessageToClient("Client_1", "Hello!");
BroadcastMessage("Server announcement!");
```

### Depuis d'autres classes

```csharp
// R�cup�rer MainGameScene
var mainGameScene = GetNode<MainGameScene>("/root/MainGameScene");

// Acc�der au serveur
var serverHandler = mainGameScene.GetServerHandler();

// Utiliser les fonctionnalit�s serveur
serverHandler.BroadcastToAllClients("Global message");
```

## ?? Touches de Debug (F1-F10)

| Touche | Action | Classe responsable |
|--------|--------|-------------------|
| F1 | Test broadcast crypt� | GameServerHandler |
| F2 | Afficher statistiques | GameServerHandler |
| F3 | Lister clients | GameServerHandler |
| F4 | Toggle debug mode | MainGameScene + GameServerHandler |
| F5 | Message chat serveur | GameServerHandler |
| F6 | Traitement haute fr�quence | GameServerHandler |
| F7 | Traitement limit� (5 msg) | GameServerHandler |
| F8 | Toggle cryptage | GameServerHandler |
| F9 | Nouvelle cl� crypto | GameServerHandler |
| F10 | �tat complet du jeu | GameServerHandler |

## ?? Configuration

### AutoLoad (dans Godot)

```
ServerManager -> /root/ServerManager (Systems/ServerManager.cs)
```

### Initialisation automatique

1. `MainGameScene` se charge
2. Cr�e et ajoute `GameServerHandler` en tant qu'enfant
3. `GameServerHandler` configure `ServerManager`
4. Le serveur d�marre automatiquement

## ?? Avantages de cette Architecture

### ? S�paration des responsabilit�s
- UI et logique m�tier s�par�es
- Code plus maintenable
- Tests plus faciles

### ? R�utilisabilit�
- `GameServerHandler` peut �tre utilis� dans d'autres sc�nes
- API claire et document�e
- Modularit� am�lior�e

### ? Extensibilit�
- Facile d'ajouter de nouveaux types de messages
- Gestion d'�v�nements flexible
- Architecture orient�e �v�nements

### ? Debugging am�lior�
- Logs s�par�s par responsabilit�
- Statistiques centralis�es
- Debug commands organis�es

## ?? Points d'attention

### Migration du code existant
- V�rifier les appels directs � `MessageReceiver` ou `Network`
- Utiliser l'API de `GameServerHandler` ou `MainGameScene`
- Mettre � jour les tests unitaires

### Performance
- Les �v�nements ajoutent une l�g�re surcharge
- Les appels sont maintenant asynchrones
- Surveiller la m�moire avec les �v�nements

### D�pendances
- `GameServerHandler` d�pend de `MainGameScene` pour l'�tat
- `ServerManager` d�pend de `GameServerHandler`
- Cycle de vie g�r� automatiquement

## ?? �volutions futures

### Possibilit�s d'extension
- Plugin system pour les types de messages
- Syst�me de middleware pour le traitement
- Interface web d'administration
- Monitoring en temps r�el

### Optimisations pr�vues
- Pool d'objets pour les messages
- Compression des donn�es
- Load balancing
- Clustering multi-serveurs