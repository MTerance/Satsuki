# ?? MainMenu.cs - Documentation complète

## ? Implémentation complète

Le fichier `MainMenu.cs` a été entièrement créé avec toutes les méthodes nécessaires.

---

## ?? Rôle

`MainMenu` est le **menu de sélection des modes de jeu** affiché après que l'utilisateur clique sur "Start Game" depuis le menu Title.

---

## ??? Architecture

### Héritage
```csharp
public partial class MainMenu : Node, IScene
```

### Options du menu (4)
1. **Solo Play** - Mode solo
2. **Multiplayer** - Mode multijoueur
3. **Mini-Games** - Mini-jeux
4. **Back to Title** - Retour au menu titre

---

## ?? Champs privés

```csharp
private DateTime _sceneStartTime;          // Temps de démarrage
private int _menuItemIndex = 0;            // Index sélection
private Button[] _menuButtons;             // Boutons du menu
private Label _titleLabel;                 // Label "MAIN MENU"
private bool _isAnimating = false;         // Flag animation
private float _titleAnimationTime = 0.0f;  // Timer animation
private readonly string[] _menuItems;      // Noms des options
```

---

## ?? Signaux

### Déclaration
```csharp
[Signal] public delegate void SoloPlayRequestedEventHandler();
[Signal] public delegate void MultiplayerRequestedEventHandler();
[Signal] public delegate void MiniGamesRequestedEventHandler();
[Signal] public delegate void BackToTitleRequestedEventHandler();
```

### Émission
| Signal | Émis par | Reçu par |
|--------|----------|----------|
| `SoloPlayRequested` | `StartSoloPlay()` | `MainGameScene.OnSoloPlayRequested()` |
| `MultiplayerRequested` | `StartMultiplayer()` | `MainGameScene.OnMultiplayerRequested()` |
| `MiniGamesRequested` | `OpenMiniGames()` | `MainGameScene.OnMiniGamesRequested()` |
| `BackToTitleRequested` | `BackToTitle()` | `MainGameScene.OnBackToTitleRequested()` |

---

## ?? Création de l'UI (`CreateUI()`)

### Structure hiérarchique
```
MainMenu (Node)
??? CanvasLayer
    ??? _titleLabel (Label)
    ?   ??? "MAIN MENU" (64px, cyan)
    ?
    ??? menuContainer (VBoxContainer)
        ??? Button "Solo Play"
        ??? Button "Multiplayer"
        ??? Button "Mini-Games"
        ??? Button "Back to Title"
```

### Style visuel

#### Titre
- **Texte** : "MAIN MENU"
- **Police** : 64px
- **Couleur** : Cyan (0.2, 0.8, 1.0)
- **Position** : En haut, centré
- **Offsets** : Top=80, Bottom=180

#### Boutons
- **Taille** : 350x70 pixels
- **Police** : 26px
- **Couleur normale** : Blanc
- **Couleur sélection** : Cyan (0.2, 0.8, 1.0)
- **Position** : Centrés verticalement

---

## ?? Méthodes principales

### Gestion du menu

#### `UpdateMenuSelection()`
```csharp
Met à jour la sélection visuelle :
- Bouton sélectionné ? Focus + Couleur cyan
- Autres boutons ? Couleur blanche
```

#### `OnMenuItemHover(int index)`
```csharp
Gère le survol souris :
1. Change l'index de sélection
2. Met à jour l'affichage
3. Log l'option survolée
```

#### `OnMenuItemSelected(int index)`
```csharp
Gère le clic/validation :
1. Met à jour la sélection
2. Log l'option choisie
3. Appelle la méthode correspondante
```

### Actions du menu

#### `StartSoloPlay()`
```csharp
Action : Démarre le mode solo
1. Log l'action
2. Sérialise l'état de la scène
3. Émet SoloPlayRequested
```

#### `StartMultiplayer()`
```csharp
Action : Démarre le mode multijoueur
1. Log l'action
2. Émet MultiplayerRequested
```

#### `OpenMiniGames()`
```csharp
Action : Ouvre les mini-jeux
1. Log l'action
2. Émet MiniGamesRequested
```

#### `BackToTitle()`
```csharp
Action : Retour au menu titre
1. Log l'action
2. Sérialise l'état final
3. Émet BackToTitleRequested
```

---

## ?? Contrôles

### Navigation clavier
| Touche | Action |
|--------|--------|
| ? | Sélection précédente |
| ? | Sélection suivante |
| Entrée / Espace | Valider la sélection |
| Échap | Retour au Title |

### Navigation souris
- **Survol** : Change la sélection
- **Clic** : Valide l'option

---

## ?? Animation du titre

### `AnimateTitle()`
```csharp
Animation toutes les 2 secondes :
1. Cyan ? Cyan clair (0.5s)
2. Pause
3. Cyan clair ? Cyan (0.5s)
4. Recommence
```

---

## ?? Flux de navigation

```
[Title - Start Game]
         ?
[MainMenu affiché]
         ?
    ??????????????????????????????
    ?    ?    ?       ?          ?
[Solo][Multi][Mini][Back]   [Échap]
    ?    ?    ?       ?          ?
[Game][Game][Games][Title]  [Title]
```

---

## ?? Interface IScene

### `GetSceneState()`
Retourne un objet avec :

```json
{
  "SceneInfo": {
    "SceneName": "MainMenu",
    "SceneType": "GameModeSelection",
    "StartTime": "2024-...",
    "ElapsedTime": 12.34,
    "ElapsedTimeFormatted": "00:12"
  },
  "Menu": {
    "SelectedIndex": 0,
    "SelectedOption": "Solo Play"
  },
  "Animation": {
    "IsAnimating": false,
    "AnimationTime": 1.5
  },
  "Status": {
    "IsReady": true,
    "Timestamp": "2024-..."
  }
}
```

---

## ?? Intégration avec MainGameScene

### Chargement
```csharp
// Dans MainGameScene.LoadMainMenu()
var mainMenu = new MainMenu();
AddChild(mainMenu);
_currentScene = mainMenu;

// Connexion des signaux
mainMenu.SoloPlayRequested += OnSoloPlayRequested;
mainMenu.MultiplayerRequested += OnMultiplayerRequested;
mainMenu.MiniGamesRequested += OnMiniGamesRequested;
mainMenu.BackToTitleRequested += OnBackToTitleRequested;
```

### Déchargement
```csharp
// Dans MainGameScene.UnloadCurrentScene()
if (_currentScene is MainMenu mainMenu)
{
    mainMenu.SoloPlayRequested -= OnSoloPlayRequested;
    mainMenu.MultiplayerRequested -= OnMultiplayerRequested;
    mainMenu.MiniGamesRequested -= OnMiniGamesRequested;
    mainMenu.BackToTitleRequested -= OnBackToTitleRequested;
}
```

### Handlers dans MainGameScene
```csharp
private void OnSoloPlayRequested()
{
    // TODO: Charger la scène de jeu solo
}

private void OnMultiplayerRequested()
{
    // TODO: Charger la scène multijoueur
}

private void OnMiniGamesRequested()
{
    // TODO: Charger la scène des mini-jeux
}

private void OnBackToTitleRequested()
{
    LoadTitle(); // ? Implémenté
}
```

---

## ?? Tests de validation

### Test 1 : Affichage du menu
```
1. ? Depuis Title, cliquer "Start Game"
2. ? Vérifier : "MAIN MENU" affiché
3. ? Vérifier : 4 boutons visibles
4. ? Vérifier : Premier bouton sélectionné (cyan)
```

### Test 2 : Navigation clavier
```
1. ? Appuyer sur ?
2. ? Vérifier : Sélection change (couleur cyan se déplace)
3. ? Appuyer sur ?
4. ? Vérifier : Sélection revient
5. ? Appuyer sur Entrée
6. ? Vérifier : Signal émis, log affiché
```

### Test 3 : Navigation souris
```
1. ? Survoler "Multiplayer"
2. ? Vérifier : Bouton s'illumine en cyan
3. ? Cliquer
4. ? Vérifier : Signal MultiplayerRequested émis
```

### Test 4 : Retour au Title
```
1. ? Cliquer "Back to Title"
2. ? Vérifier : Signal BackToTitleRequested émis
3. ? Vérifier : Title rechargé
4. ? Ou appuyer sur Échap ? Même résultat
```

### Test 5 : Animation du titre
```
1. ? Observer le titre "MAIN MENU"
2. ? Attendre 2 secondes
3. ? Vérifier : Couleur change vers cyan clair
4. ? Attendre 0.5s
5. ? Vérifier : Couleur revient au cyan
```

---

## ?? Logs attendus

### Au chargement
```
MainGameScene: Chargement MainMenu...
MainMenu: Initialisation du menu principal...
MainMenu: UI creee avec succes
MainMenu: Menu initialise avec 4 options
MainMenu charge
```

### Lors d'une sélection
```
MainMenu hover: Solo Play
MainMenu selectionne: Solo Play
MainMenu: Demande de demarrage Solo Play...
MainMenu: Etat de la scene: {...}
MainMenu: Signal SoloPlayRequested emis
MainGameScene: Reception du signal SoloPlayRequested
MainGameScene: Demarrage du mode Solo Play...
```

### Retour au Title
```
MainMenu selectionne: Back to Title
MainMenu: Retour au menu titre...
MainMenu: Etat final: {...}
MainMenu: Signal BackToTitleRequested emis
MainGameScene: Reception du signal BackToTitleRequested
MainGameScene: Chargement Title...
```

---

## ?? Points d'extension

### 1. Implémentation des modes de jeu
```csharp
private void OnSoloPlayRequested()
{
    LoadGameplaySolo(); // À créer
}

private void OnMultiplayerRequested()
{
    LoadGameplayMulti(); // À créer
}

private void OnMiniGamesRequested()
{
    LoadMiniGamesMenu(); // À créer
}
```

### 2. Sous-menus
Ajouter des sous-menus pour chaque option :
- Solo Play ? Choix du niveau
- Multiplayer ? Créer/Rejoindre partie
- Mini-Games ? Liste des mini-jeux

### 3. Animations avancées
- Transitions entre menus
- Effets de particules
- Sons de sélection

---

## ?? Comparaison avec Title

| Aspect | Title | MainMenu |
|--------|-------|----------|
| **Titre** | "SATSUKI" (72px, orange) | "MAIN MENU" (64px, cyan) |
| **Options** | 4 (Start, Options, Credits, Quit) | 4 (Solo, Multi, Mini, Back) |
| **Boutons** | 300x60px, 24px | 350x70px, 26px |
| **Animation** | Orange ? Jaune | Cyan ? Cyan clair |
| **Signaux** | 3 + Quit | 4 |
| **Échap** | Quit | Back to Title |

---

## ? Résumé

| Aspect | État |
|--------|------|
| **Compilation** | ? Réussi |
| **Méthodes** | ? Toutes implémentées |
| **Signaux** | ? Tous déclarés et émis |
| **UI** | ? Créée dynamiquement |
| **Navigation** | ? Clavier + souris |
| **Animation** | ? Fonctionnelle |
| **IScene** | ? Implémentée |
| **Documentation** | ? Complète |

---

## ?? Conclusion

**MainMenu.cs est complet et fonctionnel.**

- ? Toutes les méthodes créées
- ? UI dynamique avec 4 options
- ? Signaux connectés à MainGameScene
- ? Navigation clavier et souris
- ? Animation du titre
- ? Retour au Title fonctionnel
- ? Prêt pour extension (Solo/Multi/Mini)

---

*Date de création : 2024*  
*Build : ? Réussi*  
*Architecture : ? Cohérente avec Title.cs*
