# ?? Title Scene - Résumé de Création

## ? Fichiers Créés

```
Scenes/
??? Title.cs                    ? Créé

Documentation/
??? TITLE_SCENE.md             ? Créé
```

---

## ??? Classe Title

### Déclaration
```csharp
namespace Satsuki.Scenes
{
    public partial class Title : Node, IScene
    {
        // ...
    }
}
```

### Héritage
- ? **Node** : Classe de base Godot
- ? **IScene** : Interface pour exposer l'état

---

## ?? Implémentation de IScene

### Méthode GetSceneState()

**Retourne :**
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

---

## ?? Interface Utilisateur

### Composants Créés

#### 1. Titre Principal
```csharp
Label "SATSUKI"
?? Font Size: 72px
?? Color: Orange
?? Position: Top Center
```

#### 2. Menu (4 Options)
```csharp
VBoxContainer
?? "Start Game"    ? MainGameScene.tscn
?? "Options"       ? Options.tscn (TODO)
?? "Credits"       ? Credits.tscn
?? "Quit"          ? GetTree().Quit()
```

---

## ?? Système de Navigation

### Contrôles Clavier

| Touche | Action |
|--------|--------|
| ? | Naviguer vers le haut |
| ? | Naviguer vers le bas |
| Entrée / Espace | Sélectionner |
| Échap | Quitter |

### Contrôles Souris

| Action | Effet |
|--------|-------|
| Survol | Highlight |
| Clic | Sélection |

---

## ?? Métriques Trackées

### 1. SceneInfo
- SceneName
- SceneType
- StartTime
- ElapsedTime
- ElapsedTimeFormatted

### 2. Menu
- Items (liste)
- TotalItems
- SelectedItem
- SelectedIndex

### 3. Animation
- IsAnimating
- AnimationTime

### 4. Status
- IsReady
- Timestamp

---

## ?? Fonctionnalités

### ? Implémentées

1. **Menu de Navigation**
   - 4 options fonctionnelles
   - Navigation clavier et souris
   - Feedback visuel

2. **Transitions de Scène**
   - Start Game ? MainGameScene
   - Credits ? Credits
   - Quit ? Fermeture

3. **Tracking d'État**
   - Temps passé sur le menu
   - Option sélectionnée
   - État d'animation

4. **Logs Détaillés**
   - Navigation
   - Sélections
   - Transitions

5. **Animation**
   - Pulsation du titre (2s)
   - Système d'animation extensible

### ?? À Implémenter

- [ ] Scène Options
- [ ] Musique de fond
- [ ] Effets sonores
- [ ] Animations avancées
- [ ] Support manettes

---

## ?? Logs Générés

### Démarrage
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
?? État de la scène titre: {...}
```

```
?? Ouverture des crédits...
```

```
?? Fermeture du jeu...
?? État final de la scène titre: {...}
?? Title: Nettoyage de la scène titre
```

---

## ?? Intégration avec GetGameState()

### Quand Title est la Scène Active

```csharp
// Dans ServerManager
var gameState = mainGameScene.GetGameState();

// gameState.Scene contiendra :
{
    "CurrentScene": "Title",
    "ScenePath": "res://Scenes/Title.tscn",
    "SceneState": {
        "SceneInfo": {...},
        "Menu": {
            "SelectedItem": "Start Game",
            "SelectedIndex": 0
        },
        "Animation": {...}
    }
}
```

### Client BACKEND Reçoit

```json
{
    "Server": {
        "IsRunning": true,
        "ConnectedClients": 1
    },
    "Scene": {
        "CurrentScene": "Title",
        "SceneState": {
            "Menu": {
                "SelectedItem": "Credits"
            }
        }
    }
}
```

**? L'admin peut voir quelle option le joueur a sélectionné !**

---

## ?? Cas d'Usage

### 1. Analytics - Temps sur le Menu
```csharp
var state = titleScene.GetSceneState();

if (state.SceneInfo.ElapsedTime > 30)
{
    Analytics.Track("hesitant_player", new {
        time_on_menu = state.SceneInfo.ElapsedTime
    });
}
```

### 2. A/B Testing
```csharp
// Tracking quel menu item est le plus utilisé
Analytics.Track("menu_selection", new {
    selected = state.Menu.SelectedItem,
    time_to_select = state.SceneInfo.ElapsedTime
});
```

### 3. Admin Dashboard
```csharp
// Afficher l'activité en temps réel
Dashboard.Show($"Joueur sur: {state.Menu.SelectedItem}");
Dashboard.Show($"Temps: {state.SceneInfo.ElapsedTimeFormatted}");
```

---

## ?? Comparaison avec Credits

| Aspect | Credits | Title |
|--------|---------|-------|
| **Type** | SplashScreen | MainMenu |
| **Interaction** | Skip (passif) | Navigation (actif) |
| **Métriques** | Skips, Progress | Selection, ElapsedTime |
| **Transitions** | Auto + Skip | User-driven |
| **Animation** | Fade in/out | Pulsation |

---

## ?? Extensibilité

### Ajouter une Option
```csharp
private readonly string[] _menuItems = { 
    "Start Game", 
    "Multiplayer",    // NOUVEAU
    "Options", 
    "Credits", 
    "Quit" 
};

// Dans OnMenuItemSelected
case "Multiplayer":
    OpenMultiplayer();
    break;
```

### Personnaliser l'Apparence
```csharp
// Changer la couleur du titre
titleLabel.AddThemeColorOverride("font_color", Colors.Cyan);

// Modifier la police
titleLabel.AddThemeFontSizeOverride("font_size", 96);
```

### Ajouter des Stats de Menu
```csharp
public object GetSceneState()
{
    return new
    {
        // ...existing properties...,
        MenuStats = new
        {
            HoverCount = _hoverCount,
            NavigationCount = _navigationCount,
            MostHoveredItem = _mostHovered
        }
    };
}
```

---

## ?? Documentation

**Fichier créé** : `Documentation/TITLE_SCENE.md`

**Contient** :
- Architecture complète
- Guide d'utilisation
- Exemples d'états
- Personnalisation
- Analytics

---

## ? Build Status

**Compilation** : ? Réussie  
**Interfaces** : ? IScene implémentée  
**Documentation** : ? Complète  
**Tests** : ? Pas d'erreurs  

---

## ?? Conclusion

La classe `Title` a été créée avec succès dans `Scenes/Title.cs` :

- ? Hérite de `Node` et `IScene`
- ? Menu de navigation fonctionnel
- ? Support clavier et souris
- ? État exposé via `GetSceneState()`
- ? Intégration complète avec `GetGameState()`
- ? Logs détaillés
- ? Animation du titre
- ? Documentation complète

**La scène Title est maintenant prête à être utilisée comme écran d'accueil du jeu !** ????

---

## ?? Scènes Implémentant IScene

| Scène | Type | Métriques Principales |
|-------|------|----------------------|
| **Credits** | SplashScreen | Progress, Skips |
| **Title** | MainMenu | SelectedItem, ElapsedTime |

**2 scènes implémentent maintenant IScene et peuvent être monitorées par les clients BACKEND !** ??
