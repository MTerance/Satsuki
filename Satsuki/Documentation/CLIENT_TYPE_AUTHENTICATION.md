# ?? Syst�me d'Authentification des Types de Clients

## Vue d'ensemble

Le syst�me de gestion des types de clients avec authentification permet au serveur de cat�goriser les clients et de s�curiser l'acc�s aux r�les administratifs.

## ??? Types de Clients

| Type | Description | Authentification | Utilisation |
|------|-------------|------------------|-------------|
| **BACKEND** | Administrateur | ? **Mot de passe requis** | Gestion serveur, administration |
| **PLAYER** | Joueur | ? Aucune | Joueurs du jeu |
| **OTHER** | Autre | ? Aucune | Observateurs, spectateurs |
| **UNKNOWN** | Non d�fini | - | �tat initial |

## ?? Authentification BACKEND

### Mot de Passe
```
***Satsuk1***
```

?? **S�curit�**: Seuls les clients avec le mot de passe correct peuvent devenir BACKEND.

## ?? Protocole de Communication

### 1?? Demande du Serveur
```json
{
    "order": "RequestClientType",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "clientId": "Client_1",
    "requiresPassword": ["BACKEND"]
}
```

### 2?? R�ponse Client PLAYER
```json
{
    "order": "ClientTypeResponse",
    "clientType": "PLAYER",
    "timestamp": "2024-01-15T10:30:01.000Z"
}
```

### 3?? R�ponse Client BACKEND
```json
{
    "order": "ClientTypeResponse",
    "clientType": "BACKEND",
    "password": "***Satsuk1***",
    "timestamp": "2024-01-15T10:30:01.000Z"
}
```

### 4?? Confirmation Succ�s
```json
{
    "order": "ClientTypeConfirmation",
    "clientId": "Client_1",
    "clientType": "BACKEND",
    "success": true,
    "timestamp": "2024-01-15T10:30:02.000Z"
}
```

### 5?? Rejet (mot de passe invalide)
```json
{
    "order": "ClientTypeRejected",
    "clientId": "Client_1",
    "reason": "PASSWORD_INVALID",
    "timestamp": "2024-01-15T10:30:02.000Z"
}
```

## ?? Codes de Rejet

| Code | Description | Action |
|------|-------------|--------|
| `PASSWORD_MISSING` | Pas de mot de passe fourni | D�connexion automatique |
| `PASSWORD_INVALID` | Mot de passe incorrect | D�connexion automatique |
| `INVALID_TYPE` | Type non valide | Message d'erreur |

## ?? Exemples d'Impl�mentation

### Client C# BACKEND
```csharp
private async Task SendBackendAuthentication()
{
    var response = new
    {
        order = "ClientTypeResponse",
        clientType = "BACKEND",
        password = "***Satsuk1***",
        timestamp = DateTime.UtcNow.ToString("o")
    };
    
    string json = JsonSerializer.Serialize(response);
    await SendMessage(json);
}
```

### Client Python BACKEND
```python
def send_backend_authentication(self):
    response = {
        'order': 'ClientTypeResponse',
        'clientType': 'BACKEND',
        'password': '***Satsuk1***',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    self.socket.send(json.dumps(response).encode('utf-8'))
```

## ?? Logs Serveur

### ? Succ�s BACKEND
```
?? Type de client re�u de Client_1: BACKEND
?? Mot de passe fourni par Client_1 pour authentification BACKEND
?? Client Client_1 authentifi� en tant que BACKEND avec succ�s
? Client Client_1 enregistr� en tant que BACKEND
```

### ? �chec Mot de Passe
```
?? Type de client re�u de Client_2: BACKEND
?? Mot de passe fourni par Client_2 pour authentification BACKEND
?? Client Client_2 a fourni un mot de passe BACKEND invalide
?? Client Client_2 d�connect� pour authentification BACKEND �chou�e (PASSWORD_INVALID)
```

### ? Mot de Passe Manquant
```
?? Type de client re�u de Client_3: BACKEND
?? Client Client_3 tente de se connecter en tant que BACKEND sans mot de passe
?? Client Client_3 d�connect� pour authentification BACKEND �chou�e (PASSWORD_MISSING)
```

## ??? Recommandations de S�curit�

### ?? Production
1. **Ne pas hardcoder** le mot de passe
2. **Utiliser des variables d'environnement**
3. **Impl�menter TLS/SSL**
4. **Hash + Salt** pour le stockage
5. **Token JWT** pour l'authentification
6. **Rotation r�guli�re** du mot de passe

### ?? Am�liorations Futures
- [ ] Timeout authentification
- [ ] Limite tentatives �chou�es
- [ ] Bannissement automatique
- [ ] Authentification 2FA
- [ ] Logs d'audit d�taill�s
- [ ] Chiffrement des mots de passe

## ?? API Serveur

### Signaux
```csharp
[Signal] public delegate void ClientTypeReceivedEventHandler(string clientId, string clientType);
[Signal] public delegate void BackendAuthenticationFailedEventHandler(string clientId, string reason);
```

### M�thodes
```csharp
// Authentification avec mot de passe
public void HandleClientTypeResponse(string clientId, string clientType, string password = null)

// Rejet client BACKEND
private async Task RejectBackendClient(string clientId, string reason)
```

## ?? Tests

### Test F3
```
?? Clients connect�s:
   - Client_1: BACKEND (authentifi�)
   - Client_2: PLAYER
```

## ? Conclusion

Le syst�me d'authentification BACKEND garantit que seuls les administrateurs autoris�s peuvent acc�der aux fonctionnalit�s sensibles du serveur Satsuki.
