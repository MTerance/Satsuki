# ?? Correction de l'affichage du menu Title

## ?? Problème identifié

Le menu Title ne s'affichait pas à l'écran.

### Cause racine

Le code de `Title.cs` tentait de récupérer des nœuds UI depuis la scène `.tscn` avec `GetNode()`, mais ces nœuds n'existaient pas dans `Title.tscn`.

---

## ? Solution appliquée

### 1. Création dynamique de l'UI dans `CreateUI()`

Au lieu de `GetNode()`, on crée tous les éléments en code :
- Titre "SATSUKI" (Label 72px orange)
- Menu VBoxContainer centré
- 4 boutons (Start Game, Options, Credits, Quit)

### 2. Ajout des signaux pour MainGameScene

```csharp
[Signal]
public delegate void StartGameRequestedEventHandler();
[Signal]
public delegate void OptionsRequestedEventHandler();
[Signal]
public delegate void CreditsRequestedEventHandler();
```

### 3. Connexion dans MainGameScene

Connexion et déconnexion propre des signaux dans `LoadTitle()` et `UnloadCurrentScene()`.

---

## ?? Navigation

| Touche | Action |
|--------|--------|
| ? / ? | Naviguer |
| Entrée / Espace | Sélectionner |
| Échap | Quitter |
| Souris | Survol et clic |

---

## ?? Fichiers modifiés

- ? `Scenes/Title.cs` - Ajout CreateUI() + signaux
- ? `Scenes/MainGameScene.cs` - Connexion signaux + LoadMainMenu()

---

## ?? Résultat

? Menu Title affiché correctement  
? Navigation fonctionnelle  
? Signaux connectés  
? Build réussi  

*Date de correction : 2024*
