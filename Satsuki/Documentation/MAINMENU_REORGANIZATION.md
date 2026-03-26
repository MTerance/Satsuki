# ?? Reorganisation MainMenu - Simplification

## Vue d'ensemble

Le MainMenu a été réorganisé pour ne contenir qu'une seule option principale "Go to Lobby" au lieu des options "Solo Play" et "Multiplayer". Les modes de jeu seront maintenant sélectionnés depuis le Lobby lui-même.

---

## ?? Changements Apportés

### 1. MainMenu.cs

#### Avant
```csharp
private readonly string[] _menuItems = { 
    "Solo Play",      // ? Supprimé
    "Multiplayer",    // ? Supprimé  
    "Mini-Games", 
    "Back to Title" 
};
```

#### Après
```csharp
private readonly string[] _menuItems = { 
    "Go to Lobby",    // ? Nouvelle option unique
    "Mini-Games", 
    "Back to Title" 
};
```

#### Signaux Modifiés

**Avant :**
```csharp
[Signal]
public delegate void SoloPlayRequestedEventHandler();      // ? Supprimé

[Signal]
public delegate void MultiplayerRequestedEventHandler();   // ? Supprimé

[Signal]
public delegate void MiniGamesRequestedEventHandler();

[Signal]
public delegate void BackToTitleRequestedEventHandler();
```

**Après :**
```csharp
[Signal]
public delegate void GoToLobbyRequestedEventHandler();     // ? Nouveau

[Signal]
public delegate void MiniGamesRequestedEventHandler();

[Signal]
public delegate void BackToTitleRequestedEventHandler();
```

#### Méthodes Modifiées

**Supprimées :**
- `StartSoloPlay()`
- `StartMultiplayer()`

**Ajoutée :**
- `GoToLobby()`

```csharp
private void GoToLobby()
{
	GD.Print("MainMenu: Demande d'acces au Lobby...");
	var finalState = GetSceneState();
	GD.Print($"MainMenu: Etat de la scene: {System.Text.Json.JsonSerializer.Serialize(finalState)}");
	
	EmitSignal(SignalName.GoToLobbyRequested);
	GD.Print("MainMenu: Signal GoToLobbyRequested emis");
}
```

---

### 2. MainGameScene.cs

#### LoadMainMenu()

**Avant :**
```csharp
mainMenu.SoloPlayRequested += OnSoloPlayRequested;      // ? Supprimé
mainMenu.MultiplayerRequested += OnMultiplayerRequested; // ? Supprimé
mainMenu.MiniGamesRequested += OnMiniGamesRequested;
mainMenu.BackToTitleRequested += OnBackToTitleRequested;
```

**Après :**
```csharp
mainMenu.GoToLobbyRequested += OnGoToLobbyRequested;    // ? Nouveau
mainMenu.MiniGamesRequested += OnMiniGamesRequested;
mainMenu.BackToTitleRequested += OnBackToTitleRequested;
```

#### UnloadCurrentScene()

**Avant :**
```csharp
if (_currentScene is MainMenu mainMenu)
{
	mainMenu.SoloPlayRequested -= OnSoloPlayRequested;      // ? Supprimé
	mainMenu.MultiplayerRequested -= OnMultiplayerRequested; // ? Supprimé
	mainMenu.MiniGamesRequested -= OnMiniGamesRequested;
	mainMenu.BackToTitleRequested -= OnBackToTitleRequested;
}
```

**Après :**
```csharp
if (_currentScene is MainMenu mainMenu)
{
	mainMenu.GoToLobbyRequested -= OnGoToLobbyRequested;    // ? Nouveau
	mainMenu.MiniGamesRequested -= OnMiniGamesRequested;
	mainMenu.BackToTitleRequested -= OnBackToTitleRequested;
}
```

#### Event Handlers

**Supprimés :**
```csharp
private void OnSoloPlayRequested()      // ? Supprimé
{
	GD.Print("MainGameScene: Reception du signal SoloPlayRequested");
	// TODO: Charger la scene de jeu solo
	GD.Print("MainGameScene: Demarrage du mode Solo Play...");
}

private void OnMultiplayerRequested()   // ? Supprimé
{
	GD.Print("MainGameScene: Reception du signal MultiplayerRequested");
	// TODO: Charger la scene multijoueur
	GD.Print("MainGameScene: Demarrage du mode Multiplayer...");
}
```

**Ajouté :**
```csharp
private void OnGoToLobbyRequested()     // ? Nouveau
{
	GD.Print("MainGameScene: Reception du signal GoToLobbyRequested");
	// TODO: Ajouter la logique pour aller au Lobby
}
```

---

## ?? Nouvelle Architecture de Navigation

### Avant (Ancien Flux)
```
Title
  ??> Start Game
      ??> MainMenu
   ??> Solo Play     ? Lance le jeu solo
  ??> Multiplayer   ? Lance le multijoueur
      ??> Mini-Games    ? Ouvre les mini-jeux
              ??> Back to Title ? Retour au titre
```

### Après (Nouveau Flux)
```
Title
  ??> Start Game
        ??> MainMenu
        ??> Go to Lobby   ? Va au Lobby (choix Solo/Multi là-bas)
           ??> Mini-Games    ? Ouvre les mini-jeux
              ??> Back to Title ? Retour au titre
```

---

## ?? Comparaison

| Aspect | Avant | Après |
|--------|-------|-------|
| **Options MainMenu** | 4 | 3 |
| **Signaux** | 4 | 3 |
| **Méthodes** | StartSoloPlay, StartMultiplayer, OpenMiniGames, BackToTitle | GoToLobby, OpenMiniGames, BackToTitle |
| **Event Handlers** | OnSoloPlayRequested, OnMultiplayerRequested, OnMiniGamesRequested, OnBackToTitleRequested | OnGoToLobbyRequested, OnMiniGamesRequested, OnBackToTitleRequested |
| **Complexité** | Moyenne | Simplifiée |

---

## ?? Interface Utilisateur MainMenu

### Boutons Affichés

```
?????????????????????????????????????
?  MAIN MENU        ?
?????????????????????????????????????
?     ?
?      [  Go to Lobby  ]     ?
?      [  Mini-Games   ]           ?
?      [ Back to Title ]  ?
?          ?
?????????????????????????????????????
```

---

## ?? Workflow Utilisateur

### Scénario Typique

1. **Joueur lance le jeu**
   ```
   Credits ? Title
   ```

2. **Joueur clique "Start Game"**
   ```
 Title ? MainMenu (avec camera Lobby activée)
   ```

3. **Joueur clique "Go to Lobby"**
 ```
   MainMenu ? Lobby (à implémenter)
   ```

4. **Dans le Lobby, joueur choisit :**
   - Solo Play
   - Multiplayer
   - Paramètres du jeu
   - etc.

---

## ?? TODO - Implémentation du Lobby

### OnGoToLobbyRequested()

Actuellement :
```csharp
private void OnGoToLobbyRequested()
{
	GD.Print("MainGameScene: Reception du signal GoToLobbyRequested");
	// TODO: Ajouter la logique pour aller au Lobby
}
```

### À Implémenter :

```csharp
private void OnGoToLobbyRequested()
{
	GD.Print("MainGameScene: Reception du signal GoToLobbyRequested");
	LoadLobby();
}

public void LoadLobby()
{
	try
	{
		GD.Print("MainGameScene: Chargement Lobby...");
		
		UnloadCurrentScene();
		
		var lobby = new Lobby();
		AddChild(lobby);
		_currentScene = lobby;
		
		lobby.SoloPlayRequested += OnSoloPlayFromLobby;
		lobby.MultiplayerRequested += OnMultiplayerFromLobby;
		lobby.BackToMainMenuRequested += OnBackToMainMenuRequested;
		
		GD.Print("Lobby charge");
		
		// La caméra Lobby est déjà active depuis MainMenu
	}
	catch (Exception ex)
	{
		GD.PrintErr($"Erreur chargement Lobby: {ex.Message}");
	}
}
```

---

## ?? Avantages de cette Réorganisation

### 1. Séparation des Responsabilités
- ? MainMenu = Navigation simple
- ? Lobby = Configuration et sélection du mode de jeu

### 2. UX Améliorée
- ? Moins d'options sur le MainMenu
- ? Interface plus claire
- ? Lobby permet plus de paramétrage

### 3. Extensibilité
- ? Facile d'ajouter des options au Lobby
- ? MainMenu reste simple
- ? Caméra Lobby réutilisée

### 4. Logique de Jeu
- ? Le Lobby peut gérer :
  - Matchmaking
  - Configuration du jeu
  - Liste des joueurs
  - Chat pré-game
  - Etc.

---

## ?? Logs Générés

### Quand le joueur va au Lobby

```
MainMenu: Demande d'acces au Lobby...
MainMenu: Etat de la scene: {...}
MainMenu: Signal GoToLobbyRequested emis
MainGameScene: Reception du signal GoToLobbyRequested
// TODO: Logs de LoadLobby()
```

---

## ? Status

**Build** : ? Réussi  
**Erreurs** : ? Aucune  
**MainMenu** : ? Simplifié (3 options)  
**MainGameScene** : ? Adapté au nouveau flux  
**Lobby** : ? À implémenter  

---

## ?? Fichiers Modifiés

```
Scenes/
??? MainMenu.cs          ? Modifié (simplifié)
??? MainGameScene.cs         ? Modifié (nouveau signal)
```

---

## ?? Conclusion

Le MainMenu a été simplifié avec succès :
- ? Une seule option principale "Go to Lobby"
- ? Flux de navigation plus clair
- ? Prêt pour l'implémentation du Lobby
- ? Options Solo/Multiplayer déplacées au Lobby

**La prochaine étape est d'implémenter la scène Lobby avec les options de jeu !** ??
