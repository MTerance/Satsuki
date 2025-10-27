# ?? Title Scene - Documentation

## Vue d'ensemble

La sc�ne `Title` est l'�cran titre principal du jeu. Elle impl�mente l'interface `IScene` et fournit un menu de navigation avec plusieurs options.

## ??? Architecture

### H�ritage
```csharp
public partial class Title : Node, IScene
```

- **Node** : Classe de base Godot
- **IScene** : Interface pour exposer l'�tat de la sc�ne

### Namespace
```csharp
namespace Satsuki.Scenes
```

## ?? �tat de la Sc�ne (GetSceneState)

### Structure Retourn�e
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

### �l�ments UI

#### 1. Titre Principal
```csharp
Label "SATSUKI"
?? Taille: 72px
?? Couleur: Orange (1.0, 0.5, 0.0)
?? Position: (0, 100)
?? Alignement: Centr� en haut
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
| **Start Game** | D�marre le jeu | `MainGameScene.tscn` |
| **Options** | Ouvre les options | `Options.tscn` (TODO) |
| **Credits** | Affiche les cr�dits | `Credits.tscn` |
| **Quit** | Quitte le jeu | `GetTree().Quit()` |

## ?? Contr�les

### Clavier

| Touche | Action |
|--------|--------|
| **?** (Up) | Naviguer vers le haut |
| **?** (Down) | Naviguer vers le bas |
| **Entr�e** / **Espace** | S�lectionner l'option |
| **�chap** | Quitter le jeu |

### Souris

| Action | Effet |
|--------|-------|
| **Survol** | Met en surbrillance l'option |
| **Clic** | S�lectionne l'option |

## ?? M�triques Track�es

### SceneInfo
- **SceneName** : "Title"
- **SceneType** : "MainMenu"
- **StartTime** : Heure de d�marrage (UTC)
- **ElapsedTime** : Temps pass� sur l'�cran titre (secondes)
- **ElapsedTimeFormatted** : Temps formatt� (MM:SS)

### Menu
- **Items** : Liste des options du menu
- **TotalItems** : Nombre d'options (4)
- **SelectedItem** : Option actuellement s�lectionn�e
- **SelectedIndex** : Index de l'option (0-3)

### Animation
- **IsAnimating** : Animation en cours
- **AnimationTime** : Temps d'animation accumul�

### Status
- **IsReady** : Sc�ne pr�te
- **Timestamp** : Horodatage actuel

## ?? M�thodes Principales

### Publiques

#### GetSceneState()
```csharp
public object GetSceneState()
```
Retourne l'�tat actuel de la sc�ne titre incluant les informations du menu et les animations.

### Priv�es

#### InitializeUI()
```csharp
private void InitializeUI()
```
Cr�e l'interface utilisateur (titre + menu).

#### OnMenuItemHover(int index)
```csharp
private void OnMenuItemHover(int index)
```
Callback quand la souris survole un �l�ment du menu.

#### OnMenuItemSelected(int index)
```csharp
private void OnMenuItemSelected(int index)
```
Callback quand un �l�ment du menu est s�lectionn�.

#### StartGame()
```csharp
private void StartGame()
```
D�marre le jeu et charge `MainGameScene.tscn`.

#### OpenOptions()
```csharp
private void OpenOptions()
```
Ouvre le menu des options (� impl�menter).

#### OpenCredits()
```csharp
private void OpenCredits()
```
Charge la sc�ne `Credits.tscn`.

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

## ?? Logs G�n�r�s

### Au D�marrage
```
?? Title: Initialisation de l'�cran titre...
? UI initialis�e
?? Menu initialis� avec 4 options
```

### Navigation
```
??? Menu hover: Credits
?? Menu: Options
?? Menu: Start Game
? Menu s�lectionn�: Start Game
```

### Actions
```
?? D�marrage du jeu...
?? �tat de la sc�ne titre: {"SceneInfo":{...}}
```

```
?? Ouverture des cr�dits...
```

```
?? Fermeture du jeu...
?? �tat final de la sc�ne titre: {"SceneInfo":{...}}
```

## ?? Utilisation avec GetGameState()

### R�cup�ration depuis un Client BACKEND

```csharp
// Dans ServerManager apr�s connexion BACKEND
var gameState = mainGameScene.GetGameState();

// Si Title est la sc�ne actuelle
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

## ?? Exemples d'�tats

### �tat Initial
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

### Apr�s Navigation
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

## ?? Am�liorations Futures

- [ ] Musique de fond
- [ ] Animations de particules
- [ ] Mode multijoueur dans le menu
- [ ] Sauvegarde de la derni�re option s�lectionn�e
- [ ] Easter eggs (Konami Code)
- [ ] Support des manettes
- [ ] Th�mes personnalisables

## ?? Conclusion

La sc�ne `Title` fournit :
- ? Menu de navigation complet
- ? Support clavier et souris
- ? �tat expos� via `IScene`
- ? Int�gration avec `GetGameState()`
- ? Logs d�taill�s
- ? Base extensible pour futurs menus

**Les clients BACKEND peuvent maintenant surveiller l'activit� des joueurs sur l'�cran titre !** ????
