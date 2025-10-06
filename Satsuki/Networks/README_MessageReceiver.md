# Documentation du Système MessageReceiver - Ordre d'Arrivée

## Vue d'ensemble

Le système **MessageReceiver** est une implémentation multithread qui reçoit les messages des différents clients TCP et les stocke dans une queue **par ordre d'arrivée (FIFO - First In, First Out)**. Le MainGameScene récupère ensuite ces messages dans l'ordre chronologique de réception.

## Architecture

### 1. **Message** (Models/Message.cs)
```csharp
public class Message
{
    public string Content { get; set; }
    public DateTime Timestamp { get; set; }
    public int SequenceNumber { get; private set; }
}
```
- **Contenu** : Le message reçu du client
- **Timestamp** : Horodatage de création du message
- **SequenceNumber** : Numéro de séquence unique pour tracer l'ordre d'arrivée

### 2. **MessageReceiver** (Networks/MessageReceiver.cs)
```csharp
public class MessageReceiver : SingletonBase<MessageReceiver>, IDisposable
```

#### Fonctionnalités principales :
- **Thread-Safe** : Utilise `ConcurrentQueue<Message>` pour le stockage FIFO
- **Multi-clients** : Gère plusieurs connexions TCP simultanément
- **Ordre d'arrivée** : Les messages sont traités dans l'ordre de réception
- **Gestion automatique** : Détection des déconnexions et nettoyage

#### Méthodes clés :
```csharp
// Gestion des clients
string AddClient(TcpClient tcpClient)
Task RemoveClient(string clientId)

// Récupération des messages (FIFO)
List<Message> GetMessagesByArrivalOrder()
List<Message> GetMessagesByArrivalOrder(int maxCount)
Message GetNextMessage()

// Vérifications
bool HasPendingMessages()
int GetPendingMessageCount()
int GetConnectedClientCount()
```

### 3. **ClientConnection** (Classe interne)
Gestionnaire individuel pour chaque client TCP :
- **Écoute asynchrone** : Thread dédié par client
- **Traitement multi-messages** : Support des messages séparés par `\n` ou `\r`
- **Gestion d'erreurs** : Détection automatique des déconnexions
- **Envoi bidirectionnel** : Capacité d'envoyer des réponses

### 4. **Network** (Networks/Network.cs)
Serveur TCP principal qui :
- **Accepte les connexions** : Boucle d'acceptation asynchrone
- **Délègue au MessageReceiver** : Transfert automatique des nouveaux clients
- **Interface simplifiée** : Méthodes pour envoi/broadcast

### 5. **MainGameScene** (Scenes/MainGameScene.cs)
Interface de traitement des messages :
- **Timer de traitement** : Récupération périodique (100ms)
- **Ordre d'arrivée garanti** : Messages traités dans l'ordre FIFO
- **Types de messages** : Dispatching par préfixe de contenu

## Flux de Données

```
Client TCP #1 ? ClientConnection#1 ?
Client TCP #2 ? ClientConnection#2 ? MessageReceiver.ConcurrentQueue (FIFO)
Client TCP #3 ? ClientConnection#3 ?
                                    ?
MainGameScene.Timer (100ms) ? GetMessagesByArrivalOrder() ? HandleMessage()
```

### Séquence de traitement :
1. **Connexion** : Client TCP se connecte au serveur
2. **Ajout** : `Network` ajoute le client au `MessageReceiver`
3. **Écoute** : `ClientConnection` démarre un thread d'écoute
4. **Réception** : Message reçu ? créé avec `SequenceNumber` croissant
5. **Stockage** : Message ajouté à la `ConcurrentQueue` (FIFO)
6. **Traitement** : `MainGameScene` récupère les messages dans l'ordre d'arrivée
7. **Dispatching** : Traitement selon le type de message

## Avantages du Système

### 1. **Ordre d'Arrivée Garanti**
- ? **FIFO strict** : Premier arrivé, premier traité
- ? **Numéros de séquence** : Traçabilité complète de l'ordre
- ? **Pas de réorganisation** : Pas de tri par timestamp, traitement immédiat

### 2. **Performance Optimisée**
- ? **Thread par client** : Pas de blocage entre clients
- ? **Queue lock-free** : `ConcurrentQueue` haute performance
- ? **Traitement par lots** : Récupération de plusieurs messages à la fois

### 3. **Robustesse**
- ? **Gestion des déconnexions** : Nettoyage automatique des clients
- ? **Gestion d'erreurs** : Exceptions capturées et loggées
- ? **Ressources auto-gérées** : `IDisposable` et cleanup automatique

### 4. **Flexibilité**
- ? **Traitement configurable** : Timer ajustable, traitement limité
- ? **Debug intégré** : Logs détaillés avec numéros de séquence
- ? **Commandes de test** : Touches F1-F7 pour différents tests

## Utilisation

### Démarrage du système :
```csharp
// Dans Network.Start()
MessageReceiver.GetInstance.Start();
// Le système est prêt à recevoir des clients
```

### Traitement des messages dans MainGameScene :
```csharp
// Traitement normal (toutes les 100ms)
List<Message> messages = MessageReceiver.GetInstance.GetMessagesByArrivalOrder();

// Traitement limité (max 10 messages)
List<Message> messages = MessageReceiver.GetInstance.GetMessagesByArrivalOrder(10);

// Traitement immédiat (message suivant)
Message nextMessage = MessageReceiver.GetInstance.GetNextMessage();
```

### Différents modes de traitement :

#### Mode Standard (Timer)
```csharp
// Traitement périodique toutes les 100ms
_messageProcessingTimer.WaitTime = 0.1;
```

#### Mode Haute Fréquence
```csharp
// Traite tous les messages immédiatement
while (MessageReceiver.GetInstance.HasPendingMessages())
{
    ProcessNextMessage();
}
```

#### Mode Limité
```csharp
// Traite maximum N messages par cycle
List<Message> messages = MessageReceiver.GetInstance.GetMessagesByArrivalOrder(maxCount);
```

## Types de Messages Supportés

### Format des messages :
```
[ClientId] COMMAND:data
```

### Types reconnus :
- **`PLAYER_MOVE:`** - Mouvements de joueur
- **`CHAT:`** - Messages de chat
- **`GAME_STATE:`** - Mises à jour d'état de jeu
- **`CLIENT_INFO:`** - Informations du client
- **`PING`** - Test de connectivité
- **Autres** - Messages génériques

### Exemple de traitement :
```csharp
private void HandleMessage(Message message)
{
    string clientId = ExtractClientId(message.Content);    // "Client_1"
    string content = ExtractMessageContent(message.Content); // "CHAT:Hello World"
    
    if (content.StartsWith("CHAT:"))
    {
        HandleChatMessage(clientId, content);
    }
}
```

## Configuration et Debug

### Variables de debug :
```csharp
private bool _debugMode = true; // Active les logs détaillés
```

### Commandes de test (Touches F) :
- **F1** : Broadcast message test
- **F2** : Afficher statistiques
- **F3** : Lister clients connectés
- **F4** : Basculer mode debug
- **F5** : Message de chat du serveur
- **F6** : Traitement haute fréquence
- **F7** : Traitement limité (5 messages)

### Statistiques en temps réel :
```csharp
var stats = MessageReceiver.GetInstance.GetStatistics();
Console.WriteLine($"Clients: {stats.connectedClients}");
Console.WriteLine($"Messages en attente: {stats.pendingMessages}");
```

## Gestion des Erreurs

### Déconnexions clients :
- **Détection automatique** : 0 bytes reçus = client déconnecté
- **Nettoyage automatique** : Suppression de la liste des clients
- **Notification** : Callback `OnClientDisconnected`

### Erreurs réseau :
- **Exceptions capturées** : Pas de crash de l'application
- **Logs détaillés** : Information complète pour debug
- **Récupération gracieuse** : Continuation du service pour autres clients

### Gestion mémoire :
- **Dispose pattern** : Libération propre des ressources
- **CancellationToken** : Arrêt propre des threads
- **Cleanup automatique** : Vidage des queues lors de l'arrêt

## Comparaison avec Timestamp

| Critère | **Ordre d'Arrivée (FIFO)** | Ordre Timestamp |
|---------|---------------------------|-----------------|
| **Performance** | ? Très rapide (pas de tri) | ?? Plus lent (tri requis) |
| **Ordre** | ?? Ordre réseau réel | ?? Ordre chronologique théorique |
| **Latence** | ?? Traitement immédiat | ?? Délai de tri |
| **Complexité** | ?? Simple (FIFO) | ?? Complexe (tri + timestamp) |
| **Déterminisme** | ? Ordre réseau garanti | ? Dépend de la synchronisation |

## Cas d'Usage Idéaux

### ? Parfait pour :
- **Jeux en temps réel** : Ordre d'arrivée = ordre d'exécution
- **Chat en direct** : Messages dans l'ordre de frappe
- **Commandes utilisateur** : Respect de la séquence d'input
- **Événements critiques** : Pas de réorganisation

### ?? À éviter pour :
- **Synchronisation précise** : Si timing exact requis
- **Messages horodatés** : Si ordre chronologique critique
- **Systèmes distribués** : Si clients dans fuseaux différents

## Extension Future

Le système peut facilement être étendu pour :

### Priorités de messages :
```csharp
public enum MessagePriority { Low, Normal, High, Critical }
// Utiliser des queues séparées par priorité
```

### Filtres de messages :
```csharp
public void AddMessageFilter(Func<Message, bool> filter)
// Filtrage avant ajout à la queue
```

### Métriques avancées :
```csharp
public MessageMetrics GetDetailedMetrics()
// Latence, débit, erreurs par client
```

### Persistance :
```csharp
public void EnableMessageLogging(string filePath)
// Sauvegarde des messages pour replay/debug
```

Le système **MessageReceiver** offre une solution robuste et performante pour la gestion de messages multithread avec un ordre d'arrivée garanti, parfaitement adapté aux applications temps réel comme les jeux multijoueurs.