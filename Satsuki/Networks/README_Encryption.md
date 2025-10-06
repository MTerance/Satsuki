# Documentation du Syst�me de Cryptage des Messages

## Vue d'ensemble

Le syst�me de cryptage utilise l'algorithme **AES-256** (Advanced Encryption Standard) pour s�curiser tous les messages �chang�s entre les clients et le serveur. Le cryptage est int�gr� de mani�re transparente dans le syst�me de messages existant.

## Architecture du Cryptage

### 1. **MessageCrypto** (Utils/MessageCrypto.cs)
Classe utilitaire statique qui g�re les op�rations de cryptage/d�cryptage.

#### Caract�ristiques :
- **Algorithme** : AES-256 en mode CBC
- **Cl�** : 256 bits (32 bytes)
- **IV** : 128 bits (16 bytes)
- **Encodage** : Base64 pour le transport
- **Padding** : PKCS7

#### M�thodes principales :
```csharp
// Cryptage/D�cryptage
string Encrypt(string plainText, byte[] key = null, byte[] iv = null)
string Decrypt(string encryptedText, byte[] key = null, byte[] iv = null)

// G�n�ration de cl�s
byte[] GenerateRandomKey()
byte[] GenerateRandomIV()

// Utilitaires
bool IsEncrypted(string text)
string BytesToBase64(byte[] bytes)
byte[] Base64ToBytes(string base64String)
```

### 2. **Message** (Class1.cs) - Am�lior�
La classe Message a �t� �tendue pour supporter le cryptage natif.

#### Nouvelles propri�t�s :
- `bool IsEncrypted` : Indique si le message est crypt�
- Gestion interne de l'�tat de cryptage

#### Nouvelles m�thodes :
```csharp
// Cryptage/D�cryptage in-place
bool Encrypt(byte[] key = null, byte[] iv = null)
bool Decrypt(byte[] key = null, byte[] iv = null)

// Acc�s au contenu sans modification
string GetDecryptedContent(byte[] key = null, byte[] iv = null)

// Cr�ation de copies
Message CreateEncryptedCopy(byte[] key = null, byte[] iv = null)
Message CreateDecryptedCopy(byte[] key = null, byte[] iv = null)
```

### 3. **MessageHandler** (Networks/MessageHandler.cs) - �tendu
Gestion centralis�e du cryptage avec configuration flexible.

#### Configuration du cryptage :
```csharp
// Configuration
void ConfigureEncryption(bool enabled, byte[] key = null, byte[] iv = null)
void GenerateNewEncryptionKey()
(bool enabled, string keyBase64, string ivBase64) GetEncryptionInfo()

// Ajout de messages
void AddReceivedMessage(string content)        // Auto-cryptage si activ�
void AddEncryptedMessage(string encryptedContent) // Message d�j� crypt�

// R�cup�ration
List<Message> GetMessagesByTimestamp(bool decryptMessages = true)
List<Message> GetEncryptedMessagesByTimestamp() // Sans d�cryptage
```

### 4. **Network** (Networks/Network.cs) - S�curis�
Transport s�curis� des messages avec d�tection automatique.

#### Fonctionnalit�s :
```csharp
// Envoi avec cryptage
Task<bool> SendMessage(string message, bool encrypt = true)
Task<bool> SendMessage(Message message, bool sendEncrypted = true)

// Configuration
void ConfigureEncryption(bool enabled, bool generateNewKey = false)
(bool enabled, string keyInfo, string ivInfo) GetEncryptionStatus()
```

#### D�tection automatique :
- Messages entrants : D�tection Base64 pour identifier les messages crypt�s
- Messages sortants : Cryptage automatique selon configuration

### 5. **MainGameScene** (Scenes/MainGameScene.cs) - Interface
Interface utilisateur pour la gestion du cryptage.

#### Fonctionnalit�s de debug :
- **F1** : Test du cryptage
- **F2** : Affichage des informations de cryptage
- **F3** : G�n�ration d'une nouvelle cl�
- **F4** : Basculer cryptage activ�/d�sactiv�

## Flux de Cryptage

### R�ception de messages :
```
Client ? Network.ListenForMessages()
    ?
D�tection automatique (crypt�/clair)
    ?
MessageHandler.AddReceivedMessage() ou AddEncryptedMessage()
    ?
Stockage en queue (�tat pr�serv�)
    ?
MainGameScene.ProcessIncomingMessages()
    ?
GetMessagesByTimestamp(decryptMessages: true)
    ?
D�cryptage automatique ? HandleMessage()
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

## Configuration et S�curit�

### Cl�s par d�faut :
```csharp
// ATTENTION: En production, utilisez des cl�s g�n�r�es al�atoirement
private static readonly byte[] DefaultKey = "MySecretKey123456789012345678901"; // 32 bytes
private static readonly byte[] DefaultIV = "MyInitVector1234"; // 16 bytes
```

### G�n�ration de cl�s s�curis�es :
```csharp
// G�n�re une nouvelle cl� al�atoire pour la session
MessageHandler.GetInstance.GenerateNewEncryptionKey();

// R�cup�re les informations pour partage s�curis�
var encInfo = MessageHandler.GetInstance.GetEncryptionInfo();
Console.WriteLine($"Cl�: {encInfo.keyBase64}");
Console.WriteLine($"IV: {encInfo.ivBase64}");
```

### Recommandations de s�curit� :
1. **Cl�s uniques** : G�n�rez des cl�s al�atoires pour chaque session
2. **Rotation des cl�s** : Changez les cl�s p�riodiquement
3. **Transport s�curis�** : �changez les cl�s via un canal s�curis� s�par�
4. **Effacement m�moire** : Les cl�s sont automatiquement effac�es lors du Dispose()

## Modes d'utilisation

### Mode automatique (recommand�) :
```csharp
// Au d�marrage
MessageHandler.GetInstance.ConfigureEncryption(enabled: true);

// Les messages sont automatiquement crypt�s/d�crypt�s
List<Message> messages = MessageHandler.GetInstance.GetMessagesByTimestamp();
```

### Mode manuel :
```csharp
// Cr�ation et cryptage manuel
var message = new Message("Message secret");
message.Encrypt();

// Envoi avec contr�le
await Network.GetInstance.SendMessage(message, sendEncrypted: true);
```

### Mode debug :
```csharp
// R�cup�ration sans d�cryptage pour debug
List<Message> encryptedMessages = MessageHandler.GetInstance.GetEncryptedMessagesByTimestamp();

// V�rification du cryptage
foreach (var msg in encryptedMessages)
{
    Console.WriteLine($"Crypt�: {msg.IsEncrypted}");
}
```

## Tests et Validation

### Test int�gr� dans MainGameScene :
Appuyez sur **F1** pour lancer le test automatique qui valide :
- Cryptage d'un message test
- D�cryptage du message crypt�
- V�rification de l'int�grit�

### Commandes de debug :
- **F2** : Affiche les cl�s actuelles
- **F3** : G�n�re de nouvelles cl�s
- **F4** : Active/d�sactive le cryptage

### Messages de commande :
Envoyez des messages sp�ciaux pour contr�ler le cryptage :
```
ENCRYPT_CMD:ENABLE   - Active le cryptage
ENCRYPT_CMD:DISABLE  - D�sactive le cryptage
ENCRYPT_CMD:NEW_KEY  - G�n�re une nouvelle cl�
```

## Performance

### Impact sur les performances :
- **Cryptage** : ~0.1ms par message (d�pend de la taille)
- **D�cryptage** : ~0.1ms par message
- **M�moire** : +32 bytes par message pour les m�tadonn�es
- **R�seau** : +33% de taille due � l'encodage Base64

### Optimisations :
- Cryptage asynchrone en arri�re-plan
- R�utilisation des objets AES
- Effacement s�curis� de la m�moire
- Traitement par lots des messages

## D�pannage

### Erreurs courantes :

1. **"Message d�j� crypt�"** : Tentative de cryptage d'un message d�j� crypt�
2. **"Message non crypt�"** : Tentative de d�cryptage d'un message en clair
3. **"Erreur lors du d�cryptage"** : Cl�/IV incorrect ou donn�es corrompues

### Logging :
Tous les �v�nements de cryptage sont logg�s dans la console avec le pr�fixe appropri�.

### Mode de r�cup�ration :
En cas d'erreur de cryptage/d�cryptage, le syst�me retourne gracieusement le contenu original sans planter.

## Extensibilit�

Le syst�me est con�u pour �tre facilement �tendu :

### Autres algorithmes :
Modifiez `MessageCrypto` pour supporter d'autres algorithmes (RSA, ChaCha20, etc.)

### Authentification :
Ajoutez HMAC pour l'authentification des messages

### Compression :
Int�grez la compression avant cryptage pour r�duire la taille

### �change de cl�s :
Impl�mentez Diffie-Hellman pour l'�change s�curis� de cl�s