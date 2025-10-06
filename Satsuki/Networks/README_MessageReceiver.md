# Documentation du Syst�me MessageReceiver - Ordre d'Arriv�e

## Vue d'ensemble

Le syst�me **MessageReceiver** est une impl�mentation multithread qui re�oit les messages des diff�rents clients TCP et les stocke dans une queue **par ordre d'arriv�e (FIFO - First In, First Out)**. Le MainGameScene r�cup�re ensuite ces messages dans l'ordre chronologique de r�ception.

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
- **Contenu** : Le message re�u du client
- **Timestamp** : Horodatage de cr�ation du message
- **SequenceNumber** : Num�ro de s�quence unique pour tracer l'ordre d'arriv�e

### 2. **MessageReceiver** (Networks/MessageReceiver.cs)
```csharp
public class MessageReceiver : SingletonBase<MessageReceiver>, IDisposable
```

#### Fonctionnalit�s principales :
- **Thread-Safe** : Utilise `ConcurrentQueue<Message>` pour le stockage FIFO
- **Multi-clients** : G�re plusieurs connexions TCP simultan�ment
- **Ordre d'arriv�e** : Les messages sont trait�s dans l'ordre de r�ception
- **Gestion automatique** : D�tection des d�connexions et nettoyage

#### M�thodes cl�s :
```csharp
// Gestion des clients
string AddClient(TcpClient tcpClient)
Task RemoveClient(string clientId)

// R�cup�ration des messages (FIFO)
List<Message> GetMessagesByArrivalOrder()
List<Message> GetMessagesByArrivalOrder(int maxCount)
Message GetNextMessage()

// V�rifications
bool HasPendingMessages()
int GetPendingMessageCount()
int GetConnectedClientCount()
```

### 3. **ClientConnection** (Classe interne)
Gestionnaire individuel pour chaque client TCP :
- **�coute asynchrone** : Thread d�di� par client
- **Traitement multi-messages** : Support des messages s�par�s par `\n` ou `\r`
- **Gestion d'erreurs** : D�tection automatique des d�connexions
- **Envoi bidirectionnel** : Capacit� d'envoyer des r�ponses

### 4. **Network** (Networks/Network.cs)
Serveur TCP principal qui :
- **Accepte les connexions** : Boucle d'acceptation asynchrone
- **D�l�gue au MessageReceiver** : Transfert automatique des nouveaux clients
- **Interface simplifi�e** : M�thodes pour envoi/broadcast

### 5. **MainGameScene** (Scenes/MainGameScene.cs)
Interface de traitement des messages :
- **Timer de traitement** : R�cup�ration p�riodique (100ms)
- **Ordre d'arriv�e garanti** : Messages trait�s dans l'ordre FIFO
- **Types de messages** : Dispatching par pr�fixe de contenu

## Flux de Donn�es

```
Client TCP #1 ? ClientConnection#1 ?
Client TCP #2 ? ClientConnection#2 ? MessageReceiver.ConcurrentQueue (FIFO)
Client TCP #3 ? ClientConnection#3 ?
                                    ?
MainGameScene.Timer (100ms) ? GetMessagesByArrivalOrder() ? HandleMessage()
```

### S�quence de traitement :
1. **Connexion** : Client TCP se connecte au serveur
2. **Ajout** : `Network` ajoute le client au `MessageReceiver`
3. **�coute** : `ClientConnection` d�marre un thread d'�coute
4. **R�ception** : Message re�u ? cr�� avec `SequenceNumber` croissant
5. **Stockage** : Message ajout� � la `ConcurrentQueue` (FIFO)
6. **Traitement** : `MainGameScene` r�cup�re les messages dans l'ordre d'arriv�e
7. **Dispatching** : Traitement selon le type de message

## Avantages du Syst�me

### 1. **Ordre d'Arriv�e Garanti**
- ? **FIFO strict** : Premier arriv�, premier trait�
- ? **Num�ros de s�quence** : Tra�abilit� compl�te de l'ordre
- ? **Pas de r�organisation** : Pas de tri par timestamp, traitement imm�diat

### 2. **Performance Optimis�e**
- ? **Thread par client** : Pas de blocage entre clients
- ? **Queue lock-free** : `ConcurrentQueue` haute performance
- ? **Traitement par lots** : R�cup�ration de plusieurs messages � la fois

### 3. **Robustesse**
- ? **Gestion des d�connexions** : Nettoyage automatique des clients
- ? **Gestion d'erreurs** : Exceptions captur�es et logg�es
- ? **Ressources auto-g�r�es** : `IDisposable` et cleanup automatique

### 4. **Flexibilit�**
- ? **Traitement configurable** : Timer ajustable, traitement limit�
- ? **Debug int�gr�** : Logs d�taill�s avec num�ros de s�quence
- ? **Commandes de test** : Touches F1-F7 pour diff�rents tests

## Utilisation

### D�marrage du syst�me :
```csharp
// Dans Network.Start()
MessageReceiver.GetInstance.Start();
// Le syst�me est pr�t � recevoir des clients
```

### Traitement des messages dans MainGameScene :
```csharp
// Traitement normal (toutes les 100ms)
List<Message> messages = MessageReceiver.GetInstance.GetMessagesByArrivalOrder();

// Traitement limit� (max 10 messages)
List<Message> messages = MessageReceiver.GetInstance.GetMessagesByArrivalOrder(10);

// Traitement imm�diat (message suivant)
Message nextMessage = MessageReceiver.GetInstance.GetNextMessage();
```

### Diff�rents modes de traitement :

#### Mode Standard (Timer)
```csharp
// Traitement p�riodique toutes les 100ms
_messageProcessingTimer.WaitTime = 0.1;
```

#### Mode Haute Fr�quence
```csharp
// Traite tous les messages imm�diatement
while (MessageReceiver.GetInstance.HasPendingMessages())
{
    ProcessNextMessage();
}
```

#### Mode Limit�
```csharp
// Traite maximum N messages par cycle
List<Message> messages = MessageReceiver.GetInstance.GetMessagesByArrivalOrder(maxCount);
```

## Types de Messages Support�s

### Format des messages :
```
[ClientId] COMMAND:data
```

### Types reconnus :
- **`PLAYER_MOVE:`** - Mouvements de joueur
- **`CHAT:`** - Messages de chat
- **`GAME_STATE:`** - Mises � jour d'�tat de jeu
- **`CLIENT_INFO:`** - Informations du client
- **`PING`** - Test de connectivit�
- **Autres** - Messages g�n�riques

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
private bool _debugMode = true; // Active les logs d�taill�s
```

### Commandes de test (Touches F) :
- **F1** : Broadcast message test
- **F2** : Afficher statistiques
- **F3** : Lister clients connect�s
- **F4** : Basculer mode debug
- **F5** : Message de chat du serveur
- **F6** : Traitement haute fr�quence
- **F7** : Traitement limit� (5 messages)

### Statistiques en temps r�el :
```csharp
var stats = MessageReceiver.GetInstance.GetStatistics();
Console.WriteLine($"Clients: {stats.connectedClients}");
Console.WriteLine($"Messages en attente: {stats.pendingMessages}");
```

## Gestion des Erreurs

### D�connexions clients :
- **D�tection automatique** : 0 bytes re�us = client d�connect�
- **Nettoyage automatique** : Suppression de la liste des clients
- **Notification** : Callback `OnClientDisconnected`

### Erreurs r�seau :
- **Exceptions captur�es** : Pas de crash de l'application
- **Logs d�taill�s** : Information compl�te pour debug
- **R�cup�ration gracieuse** : Continuation du service pour autres clients

### Gestion m�moire :
- **Dispose pattern** : Lib�ration propre des ressources
- **CancellationToken** : Arr�t propre des threads
- **Cleanup automatique** : Vidage des queues lors de l'arr�t

## Comparaison avec Timestamp

| Crit�re | **Ordre d'Arriv�e (FIFO)** | Ordre Timestamp |
|---------|---------------------------|-----------------|
| **Performance** | ? Tr�s rapide (pas de tri) | ?? Plus lent (tri requis) |
| **Ordre** | ?? Ordre r�seau r�el | ?? Ordre chronologique th�orique |
| **Latence** | ?? Traitement imm�diat | ?? D�lai de tri |
| **Complexit�** | ?? Simple (FIFO) | ?? Complexe (tri + timestamp) |
| **D�terminisme** | ? Ordre r�seau garanti | ? D�pend de la synchronisation |

## Cas d'Usage Id�aux

### ? Parfait pour :
- **Jeux en temps r�el** : Ordre d'arriv�e = ordre d'ex�cution
- **Chat en direct** : Messages dans l'ordre de frappe
- **Commandes utilisateur** : Respect de la s�quence d'input
- **�v�nements critiques** : Pas de r�organisation

### ?? � �viter pour :
- **Synchronisation pr�cise** : Si timing exact requis
- **Messages horodat�s** : Si ordre chronologique critique
- **Syst�mes distribu�s** : Si clients dans fuseaux diff�rents

## Extension Future

Le syst�me peut facilement �tre �tendu pour :

### Priorit�s de messages :
```csharp
public enum MessagePriority { Low, Normal, High, Critical }
// Utiliser des queues s�par�es par priorit�
```

### Filtres de messages :
```csharp
public void AddMessageFilter(Func<Message, bool> filter)
// Filtrage avant ajout � la queue
```

### M�triques avanc�es :
```csharp
public MessageMetrics GetDetailedMetrics()
// Latence, d�bit, erreurs par client
```

### Persistance :
```csharp
public void EnableMessageLogging(string filePath)
// Sauvegarde des messages pour replay/debug
```

Le syst�me **MessageReceiver** offre une solution robuste et performante pour la gestion de messages multithread avec un ordre d'arriv�e garanti, parfaitement adapt� aux applications temps r�el comme les jeux multijoueurs.