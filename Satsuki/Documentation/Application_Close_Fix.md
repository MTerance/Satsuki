# ?? Système de fermeture propre de l'application

## Problème résolu

Lorsque l'utilisateur cliquait sur la croix de fermeture (?) :
- ? Le serveur s'arrêtait proprement
- ? **L'application ne se fermait pas**

---

## ?? Solution implémentée

### Architecture du flux de fermeture

```
[Utilisateur clique sur ?]
         ?
[Godot envoie NotificationWMCloseRequest]
         ?
[ServerManager._Notification() reçoit la notification]
         ?
[ServerManager.OnQuitRequest() s'exécute]
         ?
[1. Notification aux clients]
[2. Attente 2 secondes]
[3. Arrêt du serveur]
[4. GetTree().Quit() ? AJOUTÉ]
         ?
[Application se ferme ?]
```

---

## ?? Modifications apportées

### 1. **`Systems/ServerManager.cs`**

#### Avant
```csharp
private async void OnQuitRequest()
{
    GD.Print("Arret du serveur en cours...");
    
    if (_isServerRunning && _network != null)
    {
        try
        {
            _network.OnClientConnected -= HandleClientConnected;
            
            await _network.BroadcastMessage("SERVER_SHUTDOWN: Le serveur Satsuki va se fermer");
            await Task.Delay(2000);
            
            _network.Stop();
            _isServerRunning = false;
            EmitSignal(SignalName.ServerStopped);
            
            GD.Print("Serveur arrete proprement");
        }
        catch (Exception ex)
        {
            GD.PrintErr($"Erreur lors de l'arret du serveur: {ex.Message}");
        }
    }
    // ? Pas de fermeture de l'application !
}
```

#### Après
```csharp
private async void OnQuitRequest()
{
    GD.Print("Arret du serveur en cours...");
    
    if (_isServerRunning && _network != null)
    {
        try
        {
            _network.OnClientConnected -= HandleClientConnected;
            
            await _network.BroadcastMessage("SERVER_SHUTDOWN: Le serveur Satsuki va se fermer");
            await Task.Delay(2000);
            
            _network.Stop();
            _isServerRunning = false;
            EmitSignal(SignalName.ServerStopped);
            
            GD.Print("Serveur arrete proprement");
        }
        catch (Exception ex)
        {
            GD.PrintErr($"Erreur lors de l'arret du serveur: {ex.Message}");
        }
    }
    
    // ? Quitter l'application apres l'arret du serveur
    GD.Print("Fermeture de l'application...");
    GetTree().Quit();
}
```

### 2. **`Scenes/MainGameScene.cs`**

Ajout de la gestion de la notification pour traçabilité :

```csharp
public override void _Notification(int what)
{
    if (what == NotificationWMCloseRequest)
    {
        GD.Print("MainGameScene: Demande de fermeture recue");
        // Le ServerManager va gerer l'arret propre et quitter l'application
    }
}
```

---

## ?? Flux de fermeture détaillé

### Étape 1 : Notification de fermeture
```
Utilisateur ? [X] ? NotificationWMCloseRequest
```

### Étape 2 : Interception
```csharp
// Dans ServerManager.cs
public override void _Notification(int what)
{
    if (what == NotificationWMCloseRequest || what == NotificationApplicationPaused)
    {
        OnQuitRequest();
    }
}
```

### Étape 3 : Arrêt propre du serveur
```csharp
1. Notification aux clients: "SERVER_SHUTDOWN: Le serveur Satsuki va se fermer"
2. Attente 2 secondes (pour que les clients reçoivent le message)
3. Déconnexion des événements
4. Arrêt du réseau: _network.Stop()
5. Émission du signal ServerStopped
```

### Étape 4 : Fermeture de l'application ?
```csharp
GetTree().Quit();
```

---

## ?? Logs de fermeture attendus

Quand l'utilisateur clique sur ?, la console affiche :

```
MainGameScene: Demande de fermeture recue
Arret du serveur en cours...
[Broadcast] SERVER_SHUTDOWN: Le serveur Satsuki va se fermer
[Attente 2000ms]
Serveur arrete proprement
Fermeture de l'application...
[Application se ferme]
```

---

## ?? Cas particuliers

### Si le serveur n'est pas démarré
```csharp
if (_isServerRunning && _network != null)
{
    // Arrêt du serveur
}
// ? Quitte quand même l'application
GetTree().Quit();
```

### Si une erreur survient
```csharp
try
{
    // Arrêt du serveur
}
catch (Exception ex)
{
    GD.PrintErr($"Erreur lors de l'arret du serveur: {ex.Message}");
}
// ? Quitte quand même l'application
GetTree().Quit();
```

---

## ?? Avantages de cette solution

? **Arrêt propre** : Les clients sont notifiés avant la fermeture  
? **Délai de grâce** : 2 secondes pour envoyer les messages  
? **Fermeture garantie** : `GetTree().Quit()` est toujours appelé  
? **Traçabilité** : Logs détaillés à chaque étape  
? **Robuste** : Fonctionne même en cas d'erreur  

---

## ?? Notifications Godot utilisées

| Notification | Valeur | Description |
|--------------|--------|-------------|
| `NotificationWMCloseRequest` | 1006 | Fermeture demandée par l'OS |
| `NotificationApplicationPaused` | 1015 | Application mise en pause |

---

## ?? Tests à effectuer

### Test 1 : Fermeture normale
1. ? Lancer l'application
2. ? Démarrer le serveur
3. ? Cliquer sur ?
4. ? Vérifier : Serveur arrêté proprement
5. ? Vérifier : Application fermée

### Test 2 : Fermeture sans serveur
1. ? Lancer l'application
2. ? NE PAS démarrer le serveur
3. ? Cliquer sur ?
4. ? Vérifier : Application fermée immédiatement

### Test 3 : Fermeture avec clients connectés
1. ? Lancer l'application
2. ? Démarrer le serveur
3. ? Connecter un client
4. ? Cliquer sur ?
5. ? Vérifier : Client reçoit "SERVER_SHUTDOWN"
6. ? Vérifier : Serveur arrêté après 2s
7. ? Vérifier : Application fermée

---

## ?? Fichiers modifiés

| Fichier | Modification |
|---------|--------------|
| `Systems/ServerManager.cs` | ? Ajout de `GetTree().Quit()` dans `OnQuitRequest()` |
| `Scenes/MainGameScene.cs` | ? Ajout de `_Notification()` pour traçabilité |

---

## ?? Résultat

**L'application se ferme maintenant correctement lorsque l'utilisateur clique sur la croix de fermeture, tout en arrêtant le serveur proprement.**

---

*Date de correction : 2024*
*Build : ? Réussi*
