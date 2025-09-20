# Documentation du Syst�me de Messages Multithread

## Vue d'ensemble

Le syst�me de messages multithread est compos� de trois �l�ments principaux qui travaillent ensemble pour g�rer la r�ception, le stockage et le traitement des messages r�seau de mani�re asynchrone.

## Architecture

### 1. **Message** (Class1.cs)
```csharp
public class Message
{
    public string Content { get; set; }
    public DateTime Timestamp { get; set; }
}
```
- **R�le** : Structure de donn�es repr�sentant un message
- **Propri�t�s** :
  - `Content` : Le contenu textuel du message
  - `Timestamp` : Horodatage automatique de cr�ation du message

### 2. **MessageHandler** (Networks/MessageHandler.cs)
```csharp
public class MessageHandler : SingletonBase<MessageHandler>, IDisposable
```
- **R�le** : Gestionnaire multithread pour la collecte et le tri des messages
- **Caract�ristiques** :
  - **Thread-safe** : Utilise `ConcurrentQueue<Message>` pour le stockage s�curis�
  - **Singleton** : Une seule instance dans toute l'application
  - **Asynchrone** : Traitement en arri�re-plan avec `Task` et `SemaphoreSlim`

#### M�thodes principales :
- `StartMessageProcessing()` : D�marre le traitement en arri�re-plan
- `AddReceivedMessage(string content)` : Ajoute un nouveau message � la queue
- `GetMessagesByTimestamp()` : R�cup�re tous les messages tri�s par timestamp
- `GetMessagesByTimestamp(int maxCount)` : R�cup�re un nombre limit� de messages
- `HasPendingMessages()` : V�rifie s'il y a des messages en attente
- `GetPendingMessageCount()` : Retourne le nombre de messages en attente

### 3. **Network** (Networks/Network.cs)
```csharp
public class Network : SingletonBase<Network>, INetwork, IDisposable
```
- **R�le** : Gestionnaire de connexions TCP et r�ception des messages
- **Nouvelles fonctionnalit�s** :
  - **�coute asynchrone** : `ListenForMessages()` en arri�re-plan
  - **Int�gration MessageHandler** : Envoi automatique des messages re�us
  - **Gestion des d�connexions** : D�tection et gestion des clients d�connect�s

### 4. **MainGameScene** (Scenes/MainGameScene.cs)
```csharp
public partial class MainGameScene : Node
```
- **R�le** : Consommateur principal des messages pour la logique de jeu
- **M�canisme** :
  - **Timer Godot** : Traitement p�riodique des messages (100ms)
  - **Tri automatique** : Messages r�cup�r�s par ordre chronologique
  - **Dispatch** : R�partition des messages selon leur contenu

## Flux de donn�es

```
Client TCP ? Network.ListenForMessages() 
    ?
MessageHandler.AddReceivedMessage()
    ?
ConcurrentQueue<Message> (stockage thread-safe)
    ?
MainGameScene.ProcessIncomingMessages() (Timer 100ms)
    ?
MessageHandler.GetMessagesByTimestamp() (tri par timestamp)
    ?
HandleMessage() ? Traitement sp�cifique selon le type
```

## Avantages du syst�me

### 1. **Performance**
- **Non-bloquant** : La r�ception r�seau n'impacte pas le thread principal de Godot
- **Traitement par lots** : Plusieurs messages trait�s ensemble
- **Limite configurable** : �vite la surcharge avec `GetMessagesByTimestamp(maxCount)`

### 2. **Fiabilit�**
- **Thread-safe** : `ConcurrentQueue` �vite les conditions de course
- **Ordre garanti** : Messages trait�s par ordre chronologique
- **Gestion d'erreurs** : Exceptions captur�es et logg�es

### 3. **Extensibilit�**
- **Pattern Singleton** : Acc�s global facile
- **D�couplage** : Network et MainGameScene ind�pendants
- **Types de messages** : Facilement extensible (PLAYER_MOVE, CHAT, GAME_STATE, etc.)

## Utilisation

### D�marrage du syst�me
```csharp
// Dans votre code de d�marrage
Network.GetInstance.Start(); // D�marre automatiquement le MessageHandler
```

### R�cup�ration des messages dans MainGameScene
```csharp
// R�cup�ration de tous les messages
List<Message> messages = MessageHandler.GetInstance.GetMessagesByTimestamp();

// R�cup�ration limit�e (recommand�e pour les performances)
List<Message> messages = MessageHandler.GetInstance.GetMessagesByTimestamp(10);

// V�rification avant r�cup�ration
if (MessageHandler.GetInstance.HasPendingMessages())
{
    // Traiter les messages...
}
```

### Ajout de nouveaux types de messages
```csharp
private void HandleMessage(Message message)
{
    if (message.Content.StartsWith("NEW_TYPE:"))
    {
        HandleNewMessageType(message.Content);
    }
    // ... autres types
}

private void HandleNewMessageType(string content)
{
    // Votre logique personnalis�e
}
```

## Configuration

### Fr�quence de traitement
Modifiez la propri�t� `WaitTime` du timer dans MainGameScene :
```csharp
_messageProcessingTimer.WaitTime = 0.05; // 50ms pour plus de r�activit�
_messageProcessingTimer.WaitTime = 0.2;  // 200ms pour moins de charge CPU
```

### Taille du buffer r�seau
Modifiez la taille du buffer dans `Network.ListenForMessages()` :
```csharp
byte[] buffer = new byte[8192]; // Buffer plus grand pour gros messages
```

## Nettoyage des ressources

Le syst�me g�re automatiquement le nettoyage :
- **MessageHandler** : Impl�mente `IDisposable` avec arr�t propre des t�ches
- **Network** : Ferme les connexions et lib�re les ressources
- **MainGameScene** : Lib�re le timer dans `_ExitTree()`

## Notes de d�veloppement

- **Thread principal** : Seul MainGameScene s'ex�cute sur le thread principal de Godot
- **S�curit�** : Toutes les collections sont thread-safe
- **Performance** : Le tri par timestamp est optimis� avec LINQ
- **Debug** : Messages de console int�gr�s pour le suivi des op�rations