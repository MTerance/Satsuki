# ?? Title Scene - R�sum� de Cr�ation

## ? Fichiers Cr��s

```
Scenes/
??? Title.cs                    ? Cr��

Documentation/
??? TITLE_SCENE.md             ? Cr��
```

---

## ??? Classe Title

### D�claration
```csharp
namespace Satsuki.Scenes
{
    public partial class Title : Node, IScene
    {
        // ...
    }
}
```

### H�ritage
- ? **Node** : Classe de base Godot
- ? **IScene** : Interface pour exposer l'�tat

---

## ?? Impl�mentation de IScene

### M�thode GetSceneState()

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

### Composants Cr��s

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

## ?? Syst�me de Navigation

### Contr�les Clavier

| Touche | Action |
|--------|--------|
| ? | Naviguer vers le haut |
| ? | Naviguer vers le bas |
| Entr�e / Espace | S�lectionner |
| �chap | Quitter |

### Contr�les Souris

| Action | Effet |
|--------|-------|
| Survol | Highlight |
| Clic | S�lection |

---

## ?? M�triques Track�es

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

## ?? Fonctionnalit�s

### ? Impl�ment�es

1. **Menu de Navigation**
   - 4 options fonctionnelles
   - Navigation clavier et souris
   - Feedback visuel

2. **Transitions de Sc�ne**
   - Start Game ? MainGameScene
   - Credits ? Credits
   - Quit ? Fermeture

3. **Tracking d'�tat**
   - Temps pass� sur le menu
   - Option s�lectionn�e
   - �tat d'animation

4. **Logs D�taill�s**
   - Navigation
   - S�lections
   - Transitions

5. **Animation**
   - Pulsation du titre (2s)
   - Syst�me d'animation extensible

### ?? � Impl�menter

- [ ] Sc�ne Options
- [ ] Musique de fond
- [ ] Effets sonores
- [ ] Animations avanc�es
- [ ] Support manettes

---

## ?? Logs G�n�r�s

### D�marrage
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
?? �tat de la sc�ne titre: {...}
```

```
?? Ouverture des cr�dits...
```

```
?? Fermeture du jeu...
?? �tat final de la sc�ne titre: {...}
?? Title: Nettoyage de la sc�ne titre
```

---

## ?? Int�gration avec GetGameState()

### Quand Title est la Sc�ne Active

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

### Client BACKEND Re�oit

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

**? L'admin peut voir quelle option le joueur a s�lectionn� !**

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
// Tracking quel menu item est le plus utilis�
Analytics.Track("menu_selection", new {
    selected = state.Menu.SelectedItem,
    time_to_select = state.SceneInfo.ElapsedTime
});
```

### 3. Admin Dashboard
```csharp
// Afficher l'activit� en temps r�el
Dashboard.Show($"Joueur sur: {state.Menu.SelectedItem}");
Dashboard.Show($"Temps: {state.SceneInfo.ElapsedTimeFormatted}");
```

---

## ?? Comparaison avec Credits

| Aspect | Credits | Title |
|--------|---------|-------|
| **Type** | SplashScreen | MainMenu |
| **Interaction** | Skip (passif) | Navigation (actif) |
| **M�triques** | Skips, Progress | Selection, ElapsedTime |
| **Transitions** | Auto + Skip | User-driven |
| **Animation** | Fade in/out | Pulsation |

---

## ?? Extensibilit�

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

**Fichier cr��** : `Documentation/TITLE_SCENE.md`

**Contient** :
- Architecture compl�te
- Guide d'utilisation
- Exemples d'�tats
- Personnalisation
- Analytics

---

## ? Build Status

**Compilation** : ? R�ussie  
**Interfaces** : ? IScene impl�ment�e  
**Documentation** : ? Compl�te  
**Tests** : ? Pas d'erreurs  

---

## ?? Conclusion

La classe `Title` a �t� cr��e avec succ�s dans `Scenes/Title.cs` :

- ? H�rite de `Node` et `IScene`
- ? Menu de navigation fonctionnel
- ? Support clavier et souris
- ? �tat expos� via `GetSceneState()`
- ? Int�gration compl�te avec `GetGameState()`
- ? Logs d�taill�s
- ? Animation du titre
- ? Documentation compl�te

**La sc�ne Title est maintenant pr�te � �tre utilis�e comme �cran d'accueil du jeu !** ????

---

## ?? Sc�nes Impl�mentant IScene

| Sc�ne | Type | M�triques Principales |
|-------|------|----------------------|
| **Credits** | SplashScreen | Progress, Skips |
| **Title** | MainMenu | SelectedItem, ElapsedTime |

**2 sc�nes impl�mentent maintenant IScene et peuvent �tre monitor�es par les clients BACKEND !** ??
