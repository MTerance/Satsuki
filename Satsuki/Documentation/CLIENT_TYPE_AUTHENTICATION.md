# ?? Système d'Authentification des Types de Clients

## Vue d'ensemble

Le système de gestion des types de clients avec authentification permet au serveur de catégoriser les clients et de sécuriser l'accès aux rôles administratifs.

## ??? Types de Clients

| Type | Description | Authentification | Utilisation |
|------|-------------|------------------|-------------|
| **BACKEND** | Administrateur | ? **Mot de passe requis** | Gestion serveur, administration |
| **PLAYER** | Joueur | ? Aucune | Joueurs du jeu |
| **OTHER** | Autre | ? Aucune | Observateurs, spectateurs |
| **UNKNOWN** | Non défini | - | État initial |

## ?? Authentification BACKEND

### Mot de Passe
```
***Satsuk1***
```

?? **Sécurité**: Seuls les clients avec le mot de passe correct peuvent devenir BACKEND.

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

### 2?? Réponse Client PLAYER
```json
{
    "order": "ClientTypeResponse",
    "clientType": "PLAYER",
    "timestamp": "2024-01-15T10:30:01.000Z"
}
```

### 3?? Réponse Client BACKEND
```json
{
    "order": "ClientTypeResponse",
    "clientType": "BACKEND",
    "password": "***Satsuk1***",
    "timestamp": "2024-01-15T10:30:01.000Z"
}
```

### 4?? Confirmation Succès
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
| `PASSWORD_MISSING` | Pas de mot de passe fourni | Déconnexion automatique |
| `PASSWORD_INVALID` | Mot de passe incorrect | Déconnexion automatique |
| `INVALID_TYPE` | Type non valide | Message d'erreur |

## ?? Exemples d'Implémentation

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

### ? Succès BACKEND
```
?? Type de client reçu de Client_1: BACKEND
?? Mot de passe fourni par Client_1 pour authentification BACKEND
?? Client Client_1 authentifié en tant que BACKEND avec succès
? Client Client_1 enregistré en tant que BACKEND
```

### ? Échec Mot de Passe
```
?? Type de client reçu de Client_2: BACKEND
?? Mot de passe fourni par Client_2 pour authentification BACKEND
?? Client Client_2 a fourni un mot de passe BACKEND invalide
?? Client Client_2 déconnecté pour authentification BACKEND échouée (PASSWORD_INVALID)
```

### ? Mot de Passe Manquant
```
?? Type de client reçu de Client_3: BACKEND
?? Client Client_3 tente de se connecter en tant que BACKEND sans mot de passe
?? Client Client_3 déconnecté pour authentification BACKEND échouée (PASSWORD_MISSING)
```

## ??? Recommandations de Sécurité

### ?? Production
1. **Ne pas hardcoder** le mot de passe
2. **Utiliser des variables d'environnement**
3. **Implémenter TLS/SSL**
4. **Hash + Salt** pour le stockage
5. **Token JWT** pour l'authentification
6. **Rotation régulière** du mot de passe

### ?? Améliorations Futures
- [ ] Timeout authentification
- [ ] Limite tentatives échouées
- [ ] Bannissement automatique
- [ ] Authentification 2FA
- [ ] Logs d'audit détaillés
- [ ] Chiffrement des mots de passe

## ?? API Serveur

### Signaux
```csharp
[Signal] public delegate void ClientTypeReceivedEventHandler(string clientId, string clientType);
[Signal] public delegate void BackendAuthenticationFailedEventHandler(string clientId, string reason);
```

### Méthodes
```csharp
// Authentification avec mot de passe
public void HandleClientTypeResponse(string clientId, string clientType, string password = null)

// Rejet client BACKEND
private async Task RejectBackendClient(string clientId, string reason)
```

## ?? Tests

### Test F3
```
?? Clients connectés:
   - Client_1: BACKEND (authentifié)
   - Client_2: PLAYER
```

## ? Conclusion

Le système d'authentification BACKEND garantit que seuls les administrateurs autorisés peuvent accéder aux fonctionnalités sensibles du serveur Satsuki.
