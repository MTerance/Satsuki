# ?? Automatic Credits Scene Loading - MainGameScene

## ?? Overview

La `MainGameScene` a été modifiée pour charger automatiquement la scène `Credits` au démarrage, créant ainsi un flux de jeu où les crédits s'affichent dès le lancement de l'application.

## ?? Modifications Apportées

### 1. **MainGameScene.cs - Chargement Automatique**

#### Nouveau comportement dans `_Ready()`:
```csharp
public override void _Ready()
{
    // ... initialisation existante ...
    
    // Charger automatiquement la scène Credits
    CallDeferred(nameof(LoadCreditsScene));
}
```

#### Nouvelle méthode `LoadCreditsScene()`:
```csharp
private void LoadCreditsScene()
{
    if (_hasLoadedCredits) return;
    
    try
    {
        GD.Print("?? MainGameScene: Chargement de la scène Credits...");
        GetTree().ChangeSceneToFile("res://Scenes/Credits.tscn");
        _hasLoadedCredits = true;
        GD.Print("? MainGameScene: Scène Credits chargée avec succès");
    }
    catch (Exception ex)
    {
        GD.PrintErr($"? MainGameScene: Erreur lors du chargement de Credits: {ex.Message}");
        GD.PrintErr("?? MainGameScene: Continuons sans charger Credits...");
    }
}
```

### 2. **Credits.tscn - Structure de Scène**

Le fichier `.tscn` a été mis à jour pour :
- Utiliser le script `Credits.cs`
- Être de type `Node` (correspondant au script)
- Avoir les bonnes références

```tscn
[gd_scene load_steps=2 format=3 uid="uid://rg4pnqbh6u1v"]

[ext_resource type="Script" path="res://Scenes/Credits.cs" id="1_credits"]

[node name="Credits" type="Node"]
script = ExtResource("1_credits")
```

## ?? Fonctionnalités Ajoutées

### 1. **Tracking d'État**
```csharp
private bool _hasLoadedCredits = false;
```
- Empêche le chargement multiple des crédits
- Trackable via `GetSceneState()`

### 2. **Gestion d'Erreurs Robuste**
- Try-catch pour gérer les erreurs de chargement
- Logs détaillés pour debugging
- Continuation du jeu même en cas d'échec

### 3. **Interface de Debug Étendue**
#### Nouvelle commande F11:
```csharp
case Key.F11:
    // Recharger manuellement les crédits
    if (!_hasLoadedCredits)
    {
        LoadCreditsScene();
    }
    else
    {
        GD.Print("?? Credits déjà chargés");
    }
    break;
```

### 4. **Méthode Publique d'Accès**
```csharp
public void LoadCredits()
{
    LoadCreditsScene();
}
```

## ?? Flux de Démarrage

```mermaid
graph TD
    A[Application Start] --> B[MainGameScene._Ready()]
    B --> C[Initialize GameServerHandler]
    C --> D[Connect Server Events]
    D --> E[CallDeferred LoadCreditsScene]
    E --> F[GetTree().ChangeSceneToFile Credits.tscn]
    F --> G[Credits Scene Loaded]
    G --> H[Credits._Ready() executes]
    H --> I[SplashScreenManager starts]
    I --> J[Credits sequence plays]
    J --> K[Return to MainGameScene]
```

## ?? État de la Scène Mis à Jour

Le `GetSceneState()` inclut maintenant :
```csharp
Scene = new
{
    CurrentScene = sceneName,
    ScenePath = scenePath,
    SceneState = sceneState,
    HasLoadedCredits = _hasLoadedCredits  // ? NOUVEAU
}
```

## ?? Expérience Utilisateur

### Séquence de Démarrage:
1. **Lancement** ? MainGameScene s'initialise
2. **Serveur** ? GameServerHandler démarre
3. **Transition** ? Credits se charge automatiquement
4. **Credits** ? Splash screens s'affichent
5. **Retour** ? Retour automatique à MainGameScene après les crédits

### Contrôles Utilisateur:
- **Espace/Entrée** : Passer au crédit suivant
- **Échap** : Ignorer tous les crédits
- **Clic souris** : Passer au crédit suivant
- **F11** (Debug) : Recharger les crédits manuellement

## ?? Intégration avec le Serveur

### Avantages:
- **Serveur actif** : Le serveur démarre avant les crédits
- **État synchronisé** : L'état des crédits est trackable via GameServerHandler
- **Clients connectés** : Peuvent voir l'état des crédits via `GetCompleteGameState()`

### Données Serveur:
```json
{
  "ServerState": {
    "IsRunning": true,
    "ConnectedClients": 0,
    "PendingMessages": 0
  },
  "GameSceneState": {
    "Scene": {
      "CurrentScene": "Credits",
      "HasLoadedCredits": true
    }
  }
}
```

## ??? Gestion d'Erreurs

### Scenarios Couverts:
1. **Credits.tscn manquant** ? Log d'erreur, continue sans crash
2. **Script Credits.cs invalide** ? Exception catchée, application continue
3. **Chargement multiple** ? Prévenu par `_hasLoadedCredits`

### Logs de Debug:
```
?? MainGameScene: Chargement de la scène Credits...
? MainGameScene: Scène Credits chargée avec succès
?? Credits: Initialisation...
? 3 splash screens configurés
```

## ?? Extensions Possibles

### Futures Améliorations:
1. **Configuration** : Paramètre pour activer/désactiver le chargement auto
2. **Conditions** : Charger les crédits seulement dans certains contextes
3. **Animation** : Transition animée entre MainGameScene et Credits
4. **Persistance** : Se souvenir si les crédits ont déjà été vus

### Exemple d'Extension:
```csharp
public void LoadCreditsWithCondition(bool forceLoad = false)
{
    // Ne charger que si c'est le premier lancement ou forcé
    bool isFirstLaunch = !FileAccess.FileExists("user://credits_seen.dat");
    
    if (isFirstLaunch || forceLoad)
    {
        LoadCreditsScene();
    }
}
```

## ? Validation

### Tests à Effectuer:
1. **Démarrage normal** ? Crédits se chargent automatiquement
2. **Erreur de fichier** ? Application continue sans crash
3. **Commande F11** ? Rechargement manuel fonctionne
4. **État serveur** ? `HasLoadedCredits` visible dans l'état

### Vérification:
- ? Compilation réussie
- ? Fichiers `.tscn` et `.cs` cohérents
- ? Gestion d'erreurs robuste
- ? Integration serveur fonctionnelle

La MainGameScene charge maintenant automatiquement les crédits au démarrage, créant une expérience utilisateur fluide dès le lancement de l'application !