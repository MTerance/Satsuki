# Documentation du Système de Messages Multithread

## Vue d'ensemble

Le système de messages multithread est composé de trois éléments principaux qui travaillent ensemble pour gérer la réception, le stockage et le traitement des messages réseau de manière asynchrone.

## Architecture

### 1. **Message** (Class1.cs)
```csharp
public class Message
{
    public string Content { get; set; }
    public DateTime Timestamp { get; set; }
}
```
- **Rôle** : Structure de données représentant un message
- **Propriétés** :
  - `Content` : Le contenu textuel du message
  - `Timestamp` : Horodatage automatique de création du message

### 2. **MessageHandler** (Networks/MessageHandler.cs)
```csharp
public class MessageHandler : SingletonBase<MessageHandler>, IDisposable
```
- **Rôle** : Gestionnaire multithread pour la collecte et le tri des messages
- **Caractéristiques** :
  - **Thread-safe** : Utilise `ConcurrentQueue<Message>` pour le stockage sécurisé
  - **Singleton** : Une seule instance dans toute l'application
  - **Asynchrone** : Traitement en arrière-plan avec `Task` et `SemaphoreSlim`

#### Méthodes principales :
- `StartMessageProcessing()` : Démarre le traitement en arrière-plan
- `AddReceivedMessage(string content)` : Ajoute un nouveau message à la queue
- `GetMessagesByTimestamp()` : Récupère tous les messages triés par timestamp
- `GetMessagesByTimestamp(int maxCount)` : Récupère un nombre limité de messages
- `HasPendingMessages()` : Vérifie s'il y a des messages en attente
- `GetPendingMessageCount()` : Retourne le nombre de messages en attente

### 3. **Network** (Networks/Network.cs)
```csharp
public class Network : SingletonBase<Network>, INetwork, IDisposable
```
- **Rôle** : Gestionnaire de connexions TCP et réception des messages
- **Nouvelles fonctionnalités** :
  - **Écoute asynchrone** : `ListenForMessages()` en arrière-plan
  - **Intégration MessageHandler** : Envoi automatique des messages reçus
  - **Gestion des déconnexions** : Détection et gestion des clients déconnectés

### 4. **MainGameScene** (Scenes/MainGameScene.cs)
```csharp
public partial class MainGameScene : Node
```
- **Rôle** : Consommateur principal des messages pour la logique de jeu
- **Mécanisme** :
  - **Timer Godot** : Traitement périodique des messages (100ms)
  - **Tri automatique** : Messages récupérés par ordre chronologique
  - **Dispatch** : Répartition des messages selon leur contenu

## Flux de données

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
HandleMessage() ? Traitement spécifique selon le type
```

## Avantages du système

### 1. **Performance**
- **Non-bloquant** : La réception réseau n'impacte pas le thread principal de Godot
- **Traitement par lots** : Plusieurs messages traités ensemble
- **Limite configurable** : Évite la surcharge avec `GetMessagesByTimestamp(maxCount)`

### 2. **Fiabilité**
- **Thread-safe** : `ConcurrentQueue` évite les conditions de course
- **Ordre garanti** : Messages traités par ordre chronologique
- **Gestion d'erreurs** : Exceptions capturées et loggées

### 3. **Extensibilité**
- **Pattern Singleton** : Accès global facile
- **Découplage** : Network et MainGameScene indépendants
- **Types de messages** : Facilement extensible (PLAYER_MOVE, CHAT, GAME_STATE, etc.)

## Utilisation

### Démarrage du système
```csharp
// Dans votre code de démarrage
Network.GetInstance.Start(); // Démarre automatiquement le MessageHandler
```

### Récupération des messages dans MainGameScene
```csharp
// Récupération de tous les messages
List<Message> messages = MessageHandler.GetInstance.GetMessagesByTimestamp();

// Récupération limitée (recommandée pour les performances)
List<Message> messages = MessageHandler.GetInstance.GetMessagesByTimestamp(10);

// Vérification avant récupération
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
    // Votre logique personnalisée
}
```

## Configuration

### Fréquence de traitement
Modifiez la propriété `WaitTime` du timer dans MainGameScene :
```csharp
_messageProcessingTimer.WaitTime = 0.05; // 50ms pour plus de réactivité
_messageProcessingTimer.WaitTime = 0.2;  // 200ms pour moins de charge CPU
```

### Taille du buffer réseau
Modifiez la taille du buffer dans `Network.ListenForMessages()` :
```csharp
byte[] buffer = new byte[8192]; // Buffer plus grand pour gros messages
```

## Nettoyage des ressources

Le système gère automatiquement le nettoyage :
- **MessageHandler** : Implémente `IDisposable` avec arrêt propre des tâches
- **Network** : Ferme les connexions et libère les ressources
- **MainGameScene** : Libère le timer dans `_ExitTree()`

## Notes de développement

- **Thread principal** : Seul MainGameScene s'exécute sur le thread principal de Godot
- **Sécurité** : Toutes les collections sont thread-safe
- **Performance** : Le tri par timestamp est optimisé avec LINQ
- **Debug** : Messages de console intégrés pour le suivi des opérations