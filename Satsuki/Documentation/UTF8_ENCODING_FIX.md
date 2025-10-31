# ?? Correction - Problème d'Encodage UTF-8 avec Godot

## ?? Problème Rencontré

### Erreur Godot

```
ERROR: Script 'res://Scenes/Title.cs' contains invalid unicode (UTF-8)
ERROR: Cannot load C# script file 'res://Scenes/Title.cs'
ERROR: Failed loading resource: res://Scenes/Title.cs
```

### Cause

Godot a des difficultés avec certains caractères UTF-8 :
- ? Emojis dans les messages GD.Print()
- ? Accents dans les commentaires XML (`é`, `è`, `à`)
- ? Caractères spéciaux

## ? Solution Appliquée

### 1. Suppression des Emojis

**Avant :**
```csharp
GD.Print("?? Title: Initialisation de l'écran titre...");
GD.Print("?? Menu initialisé avec {_menuItems.Length} options");
GD.Print("? UI initialisée");
```

**Après :**
```csharp
GD.Print("Title: Initialisation de l'ecran titre...");
GD.Print($"Menu initialise avec {_menuItems.Length} options");
GD.Print("UI initialisee");
```

### 2. Suppression des Accents

**Avant :**
```csharp
/// <summary>
/// Scène d'écran titre du jeu
/// </summary>
```

**Après :**
```csharp
/// <summary>
/// Scene d'ecran titre du jeu
/// </summary>
```

## ?? Fichiers Corrigés

### 1. Interfaces/IScene.cs

**Modifications :**
- `scènes` ? `scenes`
- `état` ? `etat`

```csharp
namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface de base pour toutes les scenes du jeu
	/// </summary>
	public interface IScene
	{
		/// <summary>
		/// Retourne l'etat actuel de la scene
		/// </summary>
		object GetSceneState();
	}
}
```

### 2. Scenes/Title.cs

**Modifications :**
- Tous les emojis supprimés des GD.Print()
- Tous les accents supprimés des commentaires
- Encodage UTF-8 sans BOM

**Exemples de changements :**

| Avant | Après |
|-------|-------|
| `écran` | `ecran` |
| `Initialisation...` avec emoji | `Initialisation...` sans emoji |
| `initialisé` | `initialise` |
| `créer` | `creer` |
| `survolé` | `survole` |
| `sélectionné` | `selectionne` |
| `Démarre` | `Demarre` |
| `état` | `etat` |
| `écoulé` | `ecoule` |

## ?? Recommandations

### Pour les Logs

Au lieu d'emojis dans GD.Print(), utilisez des préfixes texte :

```csharp
// ? Éviter
GD.Print("?? Title: Message");

// ? Préférer
GD.Print("[TITLE] Message");
GD.Print("[GAME] Message");
GD.Print("[NET] Message");
GD.Print("[OK] Message");
GD.Print("[ERR] Message");
```

### Pour les Commentaires

Évitez les accents français dans les commentaires :

```csharp
// ? Éviter
/// <summary>
/// Démarre le jeu et initialise les paramètres
/// </summary>

// ? Préférer
/// <summary>
/// Demarre le jeu et initialise les parametres
/// </summary>

// OU en anglais
/// <summary>
/// Starts the game and initializes parameters
/// </summary>
```

## ?? Vérification

### Test Godot

Après correction, Godot devrait charger le fichier sans erreur :

```
? Script loaded successfully: res://Scenes/Title.cs
? No encoding errors
```

### Build C#

```bash
dotnet build
# ? Build succeeded
```

## ?? Alternative : Emojis dans Console.WriteLine

Si vous voulez garder les emojis pour les logs console (pas Godot) :

```csharp
// Pour Godot (sans emoji)
GD.Print("[TITLE] Initialisation...");

// Pour Console (avec emoji, si nécessaire)
Console.WriteLine("?? Title: Initialisation...");
```

**Note** : Console.WriteLine() supporte mieux l'UTF-8 que GD.Print().

## ?? Système de Préfixes Proposé

Au lieu des emojis, utilisez des préfixes cohérents :

| Préfixe | Usage | Exemple |
|---------|-------|---------|
| `[INIT]` | Initialisation | `[INIT] Title scene ready` |
| `[OK]` | Succès | `[OK] UI initialized` |
| `[ERR]` | Erreur | `[ERR] Failed to load` |
| `[WARN]` | Avertissement | `[WARN] Missing config` |
| `[NET]` | Réseau | `[NET] Client connected` |
| `[GAME]` | Gameplay | `[GAME] Player moved` |
| `[DB]` | Base de données | `[DB] Query executed` |
| `[SCENE]` | Scène | `[SCENE] Changing to Menu` |

### Exemple de Code

```csharp
public override void _Ready()
{
	_sceneStartTime = DateTime.UtcNow;
	
	GD.Print("[INIT] Title: Initialisation de l'ecran titre...");
	
	InitializeUI();
	
	GD.Print($"[OK] Menu initialise avec {_menuItems.Length} options");
}

private void StartGame()
{
	GD.Print("[GAME] Demarrage du jeu...");
	
	var finalState = GetSceneState();
	GD.Print($"[INFO] Etat de la scene titre: {System.Text.Json.JsonSerializer.Serialize(finalState)}");
	
	GetTree().ChangeSceneToFile("res://Scenes/MainGameScene.tscn");
}

private void OnMenuItemHover(int index)
{
	_menuItemIndex = index;
	_selectedMenuItem = _menuItems[index];
	GD.Print($"[UI] Menu hover: {_selectedMenuItem}");
}
```

## ?? Avantages des Préfixes

? **Compatible Godot** : Pas de problèmes d'encodage  
? **Lisible** : Facile à filtrer dans les logs  
? **Cherchable** : `grep "[ERR]"` fonctionne  
? **Consistant** : Même format partout  
? **Performance** : Pas de conversion UTF-8 complexe  

## ?? Comparaison

| Aspect | Emojis | Préfixes |
|--------|--------|----------|
| **Compatibilité Godot** | ? Problèmes | ? Parfait |
| **Lisibilité Console** | ? Très visuel | ? Clair |
| **Cherchable** | ?? Difficile | ? Facile |
| **Performance** | ?? Moyenne | ? Rapide |
| **Encodage** | ? UTF-8 requis | ? ASCII |

## ? Status Actuel

**Fichiers corrigés** :
- ? `Interfaces/IScene.cs`
- ? `Scenes/Title.cs`

**Build** : ? Réussi  
**Godot** : ? Peut charger les scripts  
**Fonctionnalités** : ? Préservées  

## ?? Conclusion

Le problème d'encodage UTF-8 a été résolu en :
1. Supprimant les emojis des GD.Print()
2. Supprimant les accents des commentaires
3. Proposant un système de préfixes alternatif

**Les fichiers sont maintenant compatibles Godot tout en gardant leur lisibilité !** ?

---

**Note** : Les emojis restent utilisables dans `Console.WriteLine()` pour les logs de développement C# si nécessaire, mais pour Godot, privilégiez les préfixes texte.
