# ??? Intégration LobbyEx + Title dans MainGameScene

## ?? Overview

Implémentation de l'intégration automatique entre l'écran Title et la location LobbyEx. Quand Title est chargé dans `CurrentScene`, LobbyEx est automatiquement chargé dans `CurrentLocation`, créant une expérience combinée où l'écran titre coexiste avec un lobby social interactif.

## ?? Objectifs de l'Intégration

### **Expérience Utilisateur Enrichie**
- **Écran titre** : Navigation, options, menus
- **Lobby en arrière-plan** : Ambiance sociale, activités, interactions
- **Seamless** : Transition fluide entre les deux expériences

### **Architecture Dual**
- `CurrentScene` = Title (interface, navigation)
- `CurrentLocation` = LobbyEx (lieu social, interactions)
- **Synchronisation** : Chargement/déchargement automatique

## ??? Architecture Implémentée

### **Flux de Chargement Automatique**
```
LoadTitleSpecialized(title)
    ?
Configuration Title standard
    ?
CallDeferred(nameof(LoadLobbyExForTitle))
    ?
LoadLobbyExForTitle()
    ?
LoadLocationByClassName("LobbyEx")
    ?
ConfigureLobbyExForTitle()
    ?
Title + LobbyEx actifs simultanément
```

### **Flux de Déchargement Automatique**
```
UnloadTitleSpecialized(title)
    ?
Vérification si LobbyEx est chargé
    ?
if (CurrentLocation.LocationName == "LobbyEx")
    ?
UnloadCurrentLocation()
    ?
Nettoyage Title standard
```

## ?? Méthodes d'Intégration Ajoutées

### **1. Chargement Title avec LobbyEx**
```csharp
private void LoadTitleSpecialized(Satsuki.Scenes.Title title)
{
    if (title == null) return;

    GD.Print("?? MainGameScene: Configuration spécialisée Title...");

    // Configuration Title standard
    // title.GameStartRequested += OnGameStartRequested;
    // title.OptionsRequested += OnOptionsRequested;

    // NOUVEAU: Chargement automatique LobbyEx
    CallDeferred(nameof(LoadLobbyExForTitle));

    GD.Print("?? MainGameScene: Configuration Title appliquée");
}
```

### **2. Chargement Automatique LobbyEx**
```csharp
private void LoadLobbyExForTitle()
{
    try
    {
        GD.Print("??? MainGameScene: Chargement automatique de LobbyEx pour Title...");
        
        // Charger LobbyEx dans CurrentLocation
        LoadLocationByClassName("LobbyEx");
        
        // Vérifier le succès du chargement
        if (_currentLocation != null && _currentLocation.LocationName == "LobbyEx")
        {
            GD.Print("? MainGameScene: LobbyEx chargé avec succès pour Title");
            
            // Configuration spécifique
            ConfigureLobbyExForTitle();
        }
        else
        {
            GD.PrintErr("? MainGameScene: Échec du chargement de LobbyEx");
        }
    }
    catch (Exception ex)
    {
        GD.PrintErr($"? MainGameScene: Erreur lors du chargement de LobbyEx: {ex.Message}");
    }
}
```

### **3. Configuration Spécialisée LobbyEx**
```csharp
private void ConfigureLobbyExForTitle()
{
    if (_currentLocation is Satsuki.Scenes.Locations.LobbyEx lobbyEx)
    {
        GD.Print("?? MainGameScene: Configuration LobbyEx pour Title...");
        
        // Configuration spécifique du lobby pour l'écran titre
        // Mode "preview" ou "background"
        
        // Ajouter activité pour indiquer le mode titre
        lobbyEx.CallDeferred("UpdateLobbyActivity", "Lobby activé pour l'écran titre");
        
        GD.Print("? MainGameScene: LobbyEx configuré pour Title");
    }
}
```

### **4. Déchargement Synchronisé**
```csharp
private void UnloadTitleSpecialized(Satsuki.Scenes.Title title)
{
    if (title == null) return;

    GD.Print("?? MainGameScene: Déchargement spécialisé Title...");

    // NOUVEAU: Décharger LobbyEx si présent
    if (_currentLocation != null && _currentLocation.LocationName == "LobbyEx")
    {
        GD.Print("??? MainGameScene: Déchargement de LobbyEx avec Title...");
        UnloadCurrentLocation();
    }

    // Nettoyage Title standard
    GD.Print("?? MainGameScene: Title déchargé avec nettoyage spécialisé");
}
```

## ??? Classe LobbyEx Créée

### **Hérite de LocationModel**
```csharp
public partial class LobbyEx : LocationModel
{
    public override string LocationName => "LobbyEx";
    public override LocationType Type => LocationType.Social;
    public override string Description => "Lobby étendu - Zone sociale principale du jeu";
}
```

### **Fonctionnalités Spécialisées**
- ? **Activités de lobby** : Liste des activités récentes
- ? **Messages de bienvenue** : Accueil personnalisé des joueurs
- ? **Interactables spécialisés** : Tableau d'affichage, terminal de jeux
- ? **Configuration Title** : Mode spécial pour écran titre

### **Interactables LobbyEx**
```csharp
// Tableau d'affichage du lobby
public class LobbyBoardInteractable : IInteractable
{
    public string InteractableId => "LobbyBoard_Main";
    public string DisplayName => "Tableau d'Affichage";
    public string InteractionDescription => "Consulter les annonces et informations du lobby";
    
    public object Interact(string playerId, object data = null)
    {
        return new {
            Content = new {
                Announcements = new[] {
                    "Bienvenue dans LobbyEx!",
                    "Nouvelles salles de jeu disponibles", 
                    "Événement spécial ce weekend"
                }
            }
        };
    }
}

// Terminal de jeux du lobby
public class GameTerminalInteractable : IInteractable
{
    public string InteractableId => "GameTerminal_Main";
    public string DisplayName => "Terminal de Jeux";
    
    public object Interact(string playerId, object data = null)
    {
        return new {
            AvailableGames = new[] {
                "Quiz Game", "Billiard Game", "Card Games", "Puzzle Games"
            }
        };
    }
}
```

## ?? Gestion des Activités LobbyEx

### **Système d'Activités**
```csharp
private List<string> _lobbyActivities = new List<string>();

public void UpdateLobbyActivity(string activity)
{
    _lobbyActivities.Insert(0, $"[{DateTime.UtcNow:HH:mm:ss}] {activity}");
    
    // Garder seulement les 10 dernières activités
    if (_lobbyActivities.Count > 10)
    {
        _lobbyActivities.RemoveAt(_lobbyActivities.Count - 1);
    }
}
```

### **Exemples d'Activités**
```
[14:23:15] Lobby activé pour l'écran titre
[14:23:20] TestPlayer a rejoint le lobby
[14:23:25] TestPlayer a consulté le tableau d'affichage
[14:23:30] TestPlayer a utilisé le terminal de jeux
[14:23:35] TestPlayer a quitté le lobby
```

## ?? État Combiné Title + LobbyEx

### **GetSceneState() Enrichi**
```json
{
  "MainGameScene": {
    "HasCurrentScene": true,
    "CurrentSceneName": "Title",
    "HasCurrentLocation": true,
    "CurrentLocationName": "LobbyEx",
    "CurrentLocationId": "LobbyEx_12345",
    "CurrentLocationType": "Social"
  },
  "CurrentScene": {
    "Title": {
      "SceneName": "Title",
      "TitleAnimationTime": 5.2,
      "ElapsedTime": 15.8
    }
  },
  "CurrentLocation": {
    "BaseLocation": {
      "Location": {
        "Name": "LobbyEx",
        "Type": "Social",
        "IsLoaded": true,
        "IsAccessible": true
      },
      "Players": {
        "Count": 1,
        "PlayerIds": ["TestPlayer"]
      },
      "Interactables": {
        "Count": 3,
        "Available": 3
      }
    },
    "LobbyEx": {
      "LobbySpecific": {
        "IsLobbyReady": true,
        "ElapsedTimeMinutes": 2.5
      },
      "Activities": {
        "Count": 3,
        "Recent": [
          "[14:23:35] TestPlayer a quitté le lobby",
          "[14:23:30] TestPlayer a utilisé le terminal de jeux",
          "[14:23:25] TestPlayer a consulté le tableau d'affichage"
        ]
      }
    }
  }
}
```

## ?? Commandes Debug Étendues

### **Nouvelles Commandes**
```csharp
case Key.L:
    // Charger LobbyEx manuellement
    LoadLocationByClassName("LobbyEx");
    GD.Print("??? LobbyEx chargé manuellement");
    break;

case Key.T:
    // Tester Title + LobbyEx ensemble
    LoadTitleScene();
    GD.Print("?? Title + LobbyEx chargés ensemble");
    break;
```

### **Utilisation Debug**
```
[F12]  ? Charger Title (charge automatiquement LobbyEx)
[L]    ? Charger LobbyEx seul
[T]    ? Tester Title + LobbyEx ensemble
[Minus]? Faire entrer TestPlayer dans LobbyEx
[Menu] ? Voir infos LobbyEx détaillées
[End]  ? Décharger LobbyEx
```

## ?? Flux d'Utilisation Utilisateur

### **Séquence Automatique**
```
Application démarre
    ?
Credits jouent automatiquement
    ?
Credits terminés ? Signal LoadTitleSceneRequested
    ?
Title chargé dans CurrentScene
    ?
AUTOMATIQUE: LobbyEx chargé dans CurrentLocation
    ?
Utilisateur voit Title screen + Lobby background
```

### **Interactions Possibles**
```
Title Screen (CurrentScene):
- Navigation menu principal
- Options de jeu
- Paramètres
- Quitter

LobbyEx (CurrentLocation):
- Voir activités récentes
- Interagir avec tableau d'affichage
- Utiliser terminal de jeux
- Observer autres joueurs (si multi-joueur)
```

## ?? Avantages de l'Intégration

### ? **Expérience Riche**
- **Double interface** : Menu + environnement social
- **Immersion** : Lobby vivant pendant navigation
- **Activité** : Ambiance sociale dès l'écran titre

### ? **Architecture Flexible**
- **Indépendant** : Title et LobbyEx peuvent fonctionner seuls
- **Combiné** : Expérience enrichie quand ensemble
- **Modulaire** : Facile d'ajouter d'autres combinaisons

### ? **Performance Optimisée**
- **Chargement déféré** : CallDeferred pour éviter blocage
- **Gestion erreurs** : Try/catch pour robustesse
- **Nettoyage automatique** : Synchronisation déchargement

### ? **Extensibilité**
- **Autres locations** : Facilement adaptable
- **Nouvelles combinaisons** : Pattern réutilisable
- **Configuration** : Mode spécialisé par contexte

## ?? Extensions Futures

### **Mode Preview Interactif**
```csharp
private void ConfigureLobbyExForTitle()
{
    if (_currentLocation is LobbyEx lobbyEx)
    {
        // Mode prévisualisation du lobby
        lobbyEx.SetPreviewMode(true);
        
        // Animer des joueurs virtuels
        lobbyEx.SpawnVirtualPlayers(3);
        
        // Activités simulées
        lobbyEx.StartSimulatedActivities();
    }
}
```

### **Transition Fluide vers Jeu**
```csharp
private void OnGameStartRequested()
{
    // Title disparaît en fade
    FadeOutTitle();
    
    // LobbyEx reste et devient pleinement interactif
    if (_currentLocation is LobbyEx lobbyEx)
    {
        lobbyEx.SetInteractiveMode(true);
        lobbyEx.WelcomeRealPlayer();
    }
}
```

### **Système de Notifications**
```csharp
public void ShowLobbyNotification(string message)
{
    // Afficher notification dans Title screen
    // provenant d'activités LobbyEx
    
    var notification = new Notification {
        Text = $"??? LobbyEx: {message}",
        Duration = 3.0f
    };
    
    ShowNotificationOnTitle(notification);
}
```

## ? Validation

### **Tests effectués**
- ? **Compilation réussie** : LobbyEx + MainGameScene modifications
- ? **Chargement automatique** : F12 charge Title + LobbyEx
- ? **Configuration spécialisée** : ConfigureLobbyExForTitle appelée
- ? **Déchargement synchronisé** : Title décharge LobbyEx
- ? **États combinés** : GetSceneState() inclut les deux
- ? **Commandes debug** : L et T fonctionnelles

### **Fonctionnalités validées**
1. **Auto-load** : Title charge automatiquement LobbyEx
2. **Configuration** : Mode spécial Title pour LobbyEx
3. **Activités** : Système de suivi d'activités fonctionnel
4. **Interactables** : Tableau d'affichage + terminal de jeux
5. **États** : Informations complètes dans GetSceneState()
6. **Debug** : Commandes L/T pour tests manuels

L'intégration Title + LobbyEx est maintenant opérationnelle, offrant une expérience enrichie où l'écran titre coexiste harmonieusement avec un lobby social interactif ! ??????