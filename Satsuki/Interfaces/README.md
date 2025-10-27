# ?? Interfaces - Documentation

## Vue d'ensemble

Le dossier `Interfaces` contient toutes les interfaces du projet Satsuki, définissant les contrats que doivent respecter les différentes implémentations.

## ?? Interfaces Disponibles

### 1. **IScene** - Scènes de jeu
```csharp
public interface IScene
{
    object GetSceneState();
}
```

**Utilisation :**
- Toutes les scènes qui veulent exposer leur état doivent implémenter cette interface
- Permet au système `GetGameState()` de récupérer l'état dynamiquement

**Exemple :**
```csharp
public partial class QuizScene : Node, IScene
{
    public object GetSceneState()
    {
        return new
        {
            QuizInfo = {...},
            PlayerStats = {...}
        };
    }
}
```

---

### 2. **INetwork** - Serveur réseau
```csharp
public interface INetwork
{
    bool Start();
    bool Stop();
}
```

**Utilisation :**
- Implémentée par la classe `Network`
- Définit les opérations de base du serveur

---

### 3. **IMessageHandler** - Gestion des messages
```csharp
public interface IMessageHandler
{
    Task HandleMessage(string clientId, string message);
    Task<bool> SendMessage(string clientId, string message, bool encrypt = true);
    Task BroadcastMessage(string message, bool encrypt = true);
}
```

**Utilisation :**
- Pour les systèmes qui traitent les messages réseau
- Standardise la communication client-serveur

---

### 4. **ICryptoSystem** - Cryptographie
```csharp
public interface ICryptoSystem
{
    string Encrypt(string plainText);
    string Decrypt(string cipherText);
    bool Test();
    void GenerateNewKey();
}
```

**Utilisation :**
- Pour les systèmes de cryptage/décryptage
- Implémentée par `MessageCrypto`

---

### 5. **IClientManager** - Gestion des clients
```csharp
public interface IClientManager
{
    string GetClientType(string clientId);
    bool SetClientType(string clientId, string clientType);
    List<string> GetClientsByType(string clientType);
    List<string> GetAllClients();
    void DisconnectClient(string clientId);
}
```

**Utilisation :**
- Pour gérer les clients connectés
- Types de clients: BACKEND, PLAYER, OTHER

---

### 6. **IDatabase** - Base de données
```csharp
public interface IDatabase
{
    bool Initialize(string connectionString);
    void Close();
    bool IsConnected();
    int ExecuteQuery(string query);
}
```

**Utilisation :**
- Pour les systèmes de gestion de base de données
- Implémentée par `DbManager`

---

## ?? Bonnes Pratiques

### 1. Nommage
- ? Préfixe `I` pour toutes les interfaces
- ? Nom descriptif et clair
- ? Namespace `Satsuki.Interfaces`

### 2. Documentation
```csharp
/// <summary>
/// Description de l'interface
/// </summary>
public interface IMyInterface
{
    /// <summary>
    /// Description de la méthode
    /// </summary>
    /// <param name="param">Description du paramètre</param>
    /// <returns>Description du retour</returns>
    ReturnType MethodName(ParamType param);
}
```

### 3. Implémentation
```csharp
using Satsuki.Interfaces;

public class MyClass : IMyInterface
{
    public ReturnType MethodName(ParamType param)
    {
        // Implementation
    }
}
```

---

## ?? Exemple d'Utilisation Complète

### Définir une Interface
```csharp
// Interfaces/IPlayerManager.cs
namespace Satsuki.Interfaces
{
    public interface IPlayerManager
    {
        void AddPlayer(string playerId, string playerName);
        void RemovePlayer(string playerId);
        List<string> GetAllPlayers();
    }
}
```

### Implémenter l'Interface
```csharp
// Manager/PlayerManager.cs
using Satsuki.Interfaces;

public class PlayerManager : IPlayerManager
{
    private Dictionary<string, string> _players = new();
    
    public void AddPlayer(string playerId, string playerName)
    {
        _players[playerId] = playerName;
    }
    
    public void RemovePlayer(string playerId)
    {
        _players.Remove(playerId);
    }
    
    public List<string> GetAllPlayers()
    {
        return new List<string>(_players.Keys);
    }
}
```

### Utiliser via l'Interface
```csharp
IPlayerManager playerManager = new PlayerManager();
playerManager.AddPlayer("P1", "Alice");
playerManager.AddPlayer("P2", "Bob");

var players = playerManager.GetAllPlayers();
// players = ["P1", "P2"]
```

---

## ?? Avantages des Interfaces

### 1. **Abstraction**
- Sépare le contrat de l'implémentation
- Facilite les tests unitaires (mocking)

### 2. **Flexibilité**
- Permet plusieurs implémentations
- Facilite le remplacement d'implémentations

### 3. **Polymorphisme**
```csharp
INetwork network = new Network();
INetwork mockNetwork = new MockNetwork(); // Pour les tests
```

### 4. **Injection de Dépendances**
```csharp
public class GameManager
{
    private readonly INetwork _network;
    private readonly IDatabase _database;
    
    public GameManager(INetwork network, IDatabase database)
    {
        _network = network;
        _database = database;
    }
}
```

---

## ?? Interfaces à Créer (Suggestions)

### IQuiz
```csharp
public interface IQuiz
{
    void Start();
    void Stop();
    void NextQuestion();
    object GetQuizState();
}
```

### IPlayer
```csharp
public interface IPlayer
{
    string GetPlayerId();
    string GetPlayerName();
    int GetScore();
    void AddScore(int points);
}
```

### IAuthenticator
```csharp
public interface IAuthenticator
{
    bool Authenticate(string username, string password);
    bool ValidateToken(string token);
    string GenerateToken(string username);
}
```

---

## ?? Vérification des Implémentations

### Compiler Time
```csharp
public class MyClass : IScene
{
    // Erreur de compilation si GetSceneState() n'est pas implémenté
    public object GetSceneState()
    {
        return new { };
    }
}
```

### Runtime
```csharp
if (scene is IScene sceneWithState)
{
    var state = sceneWithState.GetSceneState();
}
```

---

## ?? Conclusion

Le dossier `Interfaces` centralise tous les contrats du projet, permettant :
- ? Code plus maintenable
- ? Tests plus faciles
- ? Architecture plus flexible
- ? Meilleure séparation des responsabilités

**Toutes les nouvelles fonctionnalités importantes devraient commencer par définir une interface !** ??
