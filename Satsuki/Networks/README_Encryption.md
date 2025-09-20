# Documentation du Système de Cryptage des Messages

## Vue d'ensemble

Le système de cryptage utilise l'algorithme **AES-256** (Advanced Encryption Standard) pour sécuriser tous les messages échangés entre les clients et le serveur. Le cryptage est intégré de manière transparente dans le système de messages existant.

## Architecture du Cryptage

### 1. **MessageCrypto** (Utils/MessageCrypto.cs)
Classe utilitaire statique qui gère les opérations de cryptage/décryptage.

#### Caractéristiques :
- **Algorithme** : AES-256 en mode CBC
- **Clé** : 256 bits (32 bytes)
- **IV** : 128 bits (16 bytes)
- **Encodage** : Base64 pour le transport
- **Padding** : PKCS7

#### Méthodes principales :
```csharp
// Cryptage/Décryptage
string Encrypt(string plainText, byte[] key = null, byte[] iv = null)
string Decrypt(string encryptedText, byte[] key = null, byte[] iv = null)

// Génération de clés
byte[] GenerateRandomKey()
byte[] GenerateRandomIV()

// Utilitaires
bool IsEncrypted(string text)
string BytesToBase64(byte[] bytes)
byte[] Base64ToBytes(string base64String)
```

### 2. **Message** (Class1.cs) - Amélioré
La classe Message a été étendue pour supporter le cryptage natif.

#### Nouvelles propriétés :
- `bool IsEncrypted` : Indique si le message est crypté
- Gestion interne de l'état de cryptage

#### Nouvelles méthodes :
```csharp
// Cryptage/Décryptage in-place
bool Encrypt(byte[] key = null, byte[] iv = null)
bool Decrypt(byte[] key = null, byte[] iv = null)

// Accès au contenu sans modification
string GetDecryptedContent(byte[] key = null, byte[] iv = null)

// Création de copies
Message CreateEncryptedCopy(byte[] key = null, byte[] iv = null)
Message CreateDecryptedCopy(byte[] key = null, byte[] iv = null)
```

### 3. **MessageHandler** (Networks/MessageHandler.cs) - Étendu
Gestion centralisée du cryptage avec configuration flexible.

#### Configuration du cryptage :
```csharp
// Configuration
void ConfigureEncryption(bool enabled, byte[] key = null, byte[] iv = null)
void GenerateNewEncryptionKey()
(bool enabled, string keyBase64, string ivBase64) GetEncryptionInfo()

// Ajout de messages
void AddReceivedMessage(string content)        // Auto-cryptage si activé
void AddEncryptedMessage(string encryptedContent) // Message déjà crypté

// Récupération
List<Message> GetMessagesByTimestamp(bool decryptMessages = true)
List<Message> GetEncryptedMessagesByTimestamp() // Sans décryptage
```

### 4. **Network** (Networks/Network.cs) - Sécurisé
Transport sécurisé des messages avec détection automatique.

#### Fonctionnalités :
```csharp
// Envoi avec cryptage
Task<bool> SendMessage(string message, bool encrypt = true)
Task<bool> SendMessage(Message message, bool sendEncrypted = true)

// Configuration
void ConfigureEncryption(bool enabled, bool generateNewKey = false)
(bool enabled, string keyInfo, string ivInfo) GetEncryptionStatus()
```

#### Détection automatique :
- Messages entrants : Détection Base64 pour identifier les messages cryptés
- Messages sortants : Cryptage automatique selon configuration

### 5. **MainGameScene** (Scenes/MainGameScene.cs) - Interface
Interface utilisateur pour la gestion du cryptage.

#### Fonctionnalités de debug :
- **F1** : Test du cryptage
- **F2** : Affichage des informations de cryptage
- **F3** : Génération d'une nouvelle clé
- **F4** : Basculer cryptage activé/désactivé

## Flux de Cryptage

### Réception de messages :
```
Client ? Network.ListenForMessages()
    ?
Détection automatique (crypté/clair)
    ?
MessageHandler.AddReceivedMessage() ou AddEncryptedMessage()
    ?
Stockage en queue (état préservé)
    ?
MainGameScene.ProcessIncomingMessages()
    ?
GetMessagesByTimestamp(decryptMessages: true)
    ?
Décryptage automatique ? HandleMessage()
```

### Envoi de messages :
```
MainGameScene.SendEncryptedMessage()
    ?
Network.SendMessage(message, encrypt: true)
    ?
MessageCrypto.Encrypt()
    ?
Transmission TCP (Base64)
```

## Configuration et Sécurité

### Clés par défaut :
```csharp
// ATTENTION: En production, utilisez des clés générées aléatoirement
private static readonly byte[] DefaultKey = "MySecretKey123456789012345678901"; // 32 bytes
private static readonly byte[] DefaultIV = "MyInitVector1234"; // 16 bytes
```

### Génération de clés sécurisées :
```csharp
// Génère une nouvelle clé aléatoire pour la session
MessageHandler.GetInstance.GenerateNewEncryptionKey();

// Récupère les informations pour partage sécurisé
var encInfo = MessageHandler.GetInstance.GetEncryptionInfo();
Console.WriteLine($"Clé: {encInfo.keyBase64}");
Console.WriteLine($"IV: {encInfo.ivBase64}");
```

### Recommandations de sécurité :
1. **Clés uniques** : Générez des clés aléatoires pour chaque session
2. **Rotation des clés** : Changez les clés périodiquement
3. **Transport sécurisé** : Échangez les clés via un canal sécurisé séparé
4. **Effacement mémoire** : Les clés sont automatiquement effacées lors du Dispose()

## Modes d'utilisation

### Mode automatique (recommandé) :
```csharp
// Au démarrage
MessageHandler.GetInstance.ConfigureEncryption(enabled: true);

// Les messages sont automatiquement cryptés/décryptés
List<Message> messages = MessageHandler.GetInstance.GetMessagesByTimestamp();
```

### Mode manuel :
```csharp
// Création et cryptage manuel
var message = new Message("Message secret");
message.Encrypt();

// Envoi avec contrôle
await Network.GetInstance.SendMessage(message, sendEncrypted: true);
```

### Mode debug :
```csharp
// Récupération sans décryptage pour debug
List<Message> encryptedMessages = MessageHandler.GetInstance.GetEncryptedMessagesByTimestamp();

// Vérification du cryptage
foreach (var msg in encryptedMessages)
{
    Console.WriteLine($"Crypté: {msg.IsEncrypted}");
}
```

## Tests et Validation

### Test intégré dans MainGameScene :
Appuyez sur **F1** pour lancer le test automatique qui valide :
- Cryptage d'un message test
- Décryptage du message crypté
- Vérification de l'intégrité

### Commandes de debug :
- **F2** : Affiche les clés actuelles
- **F3** : Génère de nouvelles clés
- **F4** : Active/désactive le cryptage

### Messages de commande :
Envoyez des messages spéciaux pour contrôler le cryptage :
```
ENCRYPT_CMD:ENABLE   - Active le cryptage
ENCRYPT_CMD:DISABLE  - Désactive le cryptage
ENCRYPT_CMD:NEW_KEY  - Génère une nouvelle clé
```

## Performance

### Impact sur les performances :
- **Cryptage** : ~0.1ms par message (dépend de la taille)
- **Décryptage** : ~0.1ms par message
- **Mémoire** : +32 bytes par message pour les métadonnées
- **Réseau** : +33% de taille due à l'encodage Base64

### Optimisations :
- Cryptage asynchrone en arrière-plan
- Réutilisation des objets AES
- Effacement sécurisé de la mémoire
- Traitement par lots des messages

## Dépannage

### Erreurs courantes :

1. **"Message déjà crypté"** : Tentative de cryptage d'un message déjà crypté
2. **"Message non crypté"** : Tentative de décryptage d'un message en clair
3. **"Erreur lors du décryptage"** : Clé/IV incorrect ou données corrompues

### Logging :
Tous les événements de cryptage sont loggés dans la console avec le préfixe approprié.

### Mode de récupération :
En cas d'erreur de cryptage/décryptage, le système retourne gracieusement le contenu original sans planter.

## Extensibilité

Le système est conçu pour être facilement étendu :

### Autres algorithmes :
Modifiez `MessageCrypto` pour supporter d'autres algorithmes (RSA, ChaCha20, etc.)

### Authentification :
Ajoutez HMAC pour l'authentification des messages

### Compression :
Intégrez la compression avant cryptage pour réduire la taille

### Échange de clés :
Implémentez Diffie-Hellman pour l'échange sécurisé de clés