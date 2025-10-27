# ?? Title Scene - Documentation

## Vue d'ensemble

La scène `Title` est l'écran titre principal du jeu. Elle implémente l'interface `IScene` et fournit un menu de navigation avec plusieurs options.

## ??? Architecture

### Héritage
```csharp
public partial class Title : Node, IScene
```

- **Node** : Classe de base Godot
- **IScene** : Interface pour exposer l'état de la scène

### Namespace
```csharp
namespace Satsuki.Scenes
```

## ?? État de la Scène (GetSceneState)

### Structure Retournée
```json
{
    "SceneInfo": {
        "SceneName": "Title",
        "SceneType": "MainMenu",
        "StartTime": "2024-01-15T14:30:00Z",
        "ElapsedTime": 5.42,
        "ElapsedTimeFormatted": "00:05"
    },
    "Menu": {
        "Items": ["Start Game", "Options", "Credits", "Quit"],
        "TotalItems": 4,
        "SelectedItem": "Start Game",
        "SelectedIndex": 0
    },
    "Animation": {
        "IsAnimating": false,
        "AnimationTime": 1.23
    },
    "Status": {
        "IsReady": true,
        "Timestamp": "2024-01-15T14:30:05Z"
    }
}
```

## ?? Interface Utilisateur

### Éléments UI

#### 1. Titre Principal
```csharp
Label "SATSUKI"
?? Taille: 72px
?? Couleur: Orange (1.0, 0.5, 0.0)
?? Position: (0, 100)
?? Alignement: Centré en haut
```

#### 2. Menu Principal
```csharp
VBoxContainer
?? Position: (400, 300)
?? Taille: 400x auto
?? Boutons:
    ?? "Start Game"
    ?? "Options"
    ?? "Credits"
    ?? "Quit"
```

### Options du Menu

| Option | Action | Destination |
|--------|--------|-------------|
| **Start Game** | Démarre le jeu | `MainGameScene.tscn` |
| **Options** | Ouvre les options | `Options.tscn` (TODO) |
| **Credits** | Affiche les crédits | `Credits.tscn` |
| **Quit** | Quitte le jeu | `GetTree().Quit()` |

## ?? Contrôles

### Clavier

| Touche | Action |
|--------|--------|
| **?** (Up) | Naviguer vers le haut |
| **?** (Down) | Naviguer vers le bas |
| **Entrée** / **Espace** | Sélectionner l'option |
| **Échap** | Quitter le jeu |

### Souris

| Action | Effet |
|--------|-------|
| **Survol** | Met en surbrillance l'option |
| **Clic** | Sélectionne l'option |

## ?? Métriques Trackées

### SceneInfo
- **SceneName** : "Title"
- **SceneType** : "MainMenu"
- **StartTime** : Heure de démarrage (UTC)
- **ElapsedTime** : Temps passé sur l'écran titre (secondes)
- **ElapsedTimeFormatted** : Temps formatté (MM:SS)

### Menu
- **Items** : Liste des options du menu
- **TotalItems** : Nombre d'options (4)
- **SelectedItem** : Option actuellement sélectionnée
- **SelectedIndex** : Index de l'option (0-3)

### Animation
- **IsAnimating** : Animation en cours
- **AnimationTime** : Temps d'animation accumulé

### Status
- **IsReady** : Scène prête
- **Timestamp** : Horodatage actuel

## ?? Méthodes Principales

### Publiques

#### GetSceneState()
```csharp
public object GetSceneState()
```
Retourne l'état actuel de la scène titre incluant les informations du menu et les animations.

### Privées

#### InitializeUI()
```csharp
private void InitializeUI()
```
Crée l'interface utilisateur (titre + menu).

#### OnMenuItemHover(int index)
```csharp
private void OnMenuItemHover(int index)
```
Callback quand la souris survole un élément du menu.

#### OnMenuItemSelected(int index)
```csharp
private void OnMenuItemSelected(int index)
```
Callback quand un élément du menu est sélectionné.

#### StartGame()
```csharp
private void StartGame()
```
Démarre le jeu et charge `MainGameScene.tscn`.

#### OpenOptions()
```csharp
private void OpenOptions()
```
Ouvre le menu des options (à implémenter).

#### OpenCredits()
```csharp
private void OpenCredits()
```
Charge la scène `Credits.tscn`.

#### QuitGame()
```csharp
private void QuitGame()
```
Ferme le jeu proprement.

#### AnimateTitle()
```csharp
private async void AnimateTitle()
```
Animation de pulsation du titre toutes les 2 secondes.

## ?? Logs Générés

### Au Démarrage
```
?? Title: Initialisation de l'écran titre...
? UI initialisée
?? Menu initialisé avec 4 options
```

### Navigation
```
??? Menu hover: Credits
?? Menu: Options
?? Menu: Start Game
? Menu sélectionné: Start Game
```

### Actions
```
?? Démarrage du jeu...
?? État de la scène titre: {"SceneInfo":{...}}
```

```
?? Ouverture des crédits...
```

```
?? Fermeture du jeu...
?? État final de la scène titre: {"SceneInfo":{...}}
```

## ?? Utilisation avec GetGameState()

### Récupération depuis un Client BACKEND

```csharp
// Dans ServerManager après connexion BACKEND
var gameState = mainGameScene.GetGameState();

// Si Title est la scène actuelle
{
    "Scene": {
        "CurrentScene": "Title",
        "ScenePath": "res://Scenes/Title.tscn",
        "SceneState": {
            "SceneInfo": {
                "SceneName": "Title",
                "ElapsedTime": 12.34
            },
            "Menu": {
                "SelectedItem": "Credits",
                "SelectedIndex": 2
            }
        }
    }
}
```

## ?? Exemples d'États

### État Initial
```json
{
    "SceneInfo": {
        "SceneName": "Title",
        "SceneType": "MainMenu",
        "ElapsedTime": 0.05,
        "ElapsedTimeFormatted": "00:00"
    },
    "Menu": {
        "Items": ["Start Game", "Options", "Credits", "Quit"],
        "TotalItems": 4,
        "SelectedItem": "Start Game",
        "SelectedIndex": 0
    },
    "Animation": {
        "IsAnimating": false,
        "AnimationTime": 0.0
    }
}
```

### Après Navigation
```json
{
    "SceneInfo": {
        "ElapsedTime": 5.23,
        "ElapsedTimeFormatted": "00:05"
    },
    "Menu": {
        "SelectedItem": "Credits",
        "SelectedIndex": 2
    },
    "Animation": {
        "IsAnimating": true,
        "AnimationTime": 1.5
    }
}
```

## ?? Personnalisation

### Modifier les Options du Menu
```csharp
private readonly string[] _menuItems = { 
    "Start Game", 
    "Multiplayer",    // Nouveau
    "Options", 
    "Credits", 
    "Quit" 
};
```

### Changer les Couleurs
```csharp
// Titre
titleLabel.AddThemeColorOverride("font_color", Colors.Red);

// Boutons
button.AddThemeColorOverride("font_color", Colors.Cyan);
```

### Ajouter une Animation
```csharp
private async void AnimateTitle()
{
    var tween = CreateTween();
    tween.TweenProperty(titleLabel, "scale", Vector2.One * 1.1f, 0.3f);
    tween.TweenProperty(titleLabel, "scale", Vector2.One, 0.3f);
    
    await ToSignal(tween, Tween.SignalName.Finished);
    _isAnimating = false;
}
```

## ?? Analytics

### Tracking du Temps sur le Menu
```csharp
var state = titleScene.GetSceneState();
var elapsedTime = state.SceneInfo.ElapsedTime;

if (elapsedTime > 30.0)
{
    Analytics.Track("long_time_on_title", new {
        elapsed = elapsedTime,
        selected_item = state.Menu.SelectedItem
    });
}
```

### Tracking des Clics
```csharp
private Dictionary<string, int> _menuClicks = new();

private void OnMenuItemSelected(int index)
{
    var item = _menuItems[index];
    
    if (!_menuClicks.ContainsKey(item))
        _menuClicks[item] = 0;
    
    _menuClicks[item]++;
    
    Analytics.Track($"menu_click_{item}", new {
        clicks = _menuClicks[item]
    });
}
```

## ?? Améliorations Futures

- [ ] Musique de fond
- [ ] Animations de particules
- [ ] Mode multijoueur dans le menu
- [ ] Sauvegarde de la dernière option sélectionnée
- [ ] Easter eggs (Konami Code)
- [ ] Support des manettes
- [ ] Thèmes personnalisables

## ?? Conclusion

La scène `Title` fournit :
- ? Menu de navigation complet
- ? Support clavier et souris
- ? État exposé via `IScene`
- ? Intégration avec `GetGameState()`
- ? Logs détaillés
- ? Base extensible pour futurs menus

**Les clients BACKEND peuvent maintenant surveiller l'activité des joueurs sur l'écran titre !** ????
