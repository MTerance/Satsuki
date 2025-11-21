# ?? SplashScreenManager - Documentation

## Vue d'ensemble

Le `SplashScreenManager` est un système de gestion de splash screens (écrans de transition) pour Godot, permettant d'afficher des séquences d'écrans avec des transitions fade in/out.

## ?? Fonctionnalités

? **Types de Splash Screens**
- ?? Splash screens texte avec couleurs personnalisables
- ??? Splash screens image (PNG, JPG, etc.)

? **Transitions**
- Fade in/out automatiques
- Vitesse de transition configurable
- Transitions fluides entre les écrans

? **Contrôles**
- ?? Skip splash screen actuel (Espace, Entrée, Clic souris)
- ???? Skip toute la séquence (Échap)
- ?? Durées personnalisables par splash screen

? **Événements**
- Signal `SplashScreenCompleted` : Émis après chaque splash screen
- Signal `AllSplashScreensCompleted` : Émis à la fin de toute la séquence

## ?? Installation

Le `SplashScreenManager` est créé dynamiquement dans votre scène :

```csharp
private SplashScreenManager _splashScreenManager;

public override void _Ready()
{
    _splashScreenManager = new SplashScreenManager();
    AddChild(_splashScreenManager);
}
```

## ?? Utilisation de Base

### 1. Ajouter des Splash Screens

#### Splash Screen Texte
```csharp
// Texte simple (durée par défaut: 3 secondes)
_splashScreenManager.AddTextSplash("Bienvenue!");

// Avec durée personnalisée
_splashScreenManager.AddTextSplash("Mon Jeu", 2.5f);

// Avec couleur personnalisée
_splashScreenManager.AddTextSplash("Crédits", 2.0f, Colors.Cyan);

// Texte multiligne
_splashScreenManager.AddTextSplash("Développé par\nMTerance", 3.0f);
```

#### Splash Screen Image
```csharp
// Image avec durée par défaut (3 secondes)
_splashScreenManager.AddImageSplash("res://Assets/logo.png");

// Avec durée personnalisée
_splashScreenManager.AddImageSplash("res://Assets/splash.png", 4.0f);
```

### 2. Démarrer la Séquence

```csharp
_splashScreenManager.StartSequence();
```

### 3. S'abonner aux Événements

```csharp
_splashScreenManager.SplashScreenCompleted += OnSplashCompleted;
_splashScreenManager.AllSplashScreensCompleted += OnAllCompleted;

private void OnSplashCompleted()
{
    GD.Print("Un splash screen est terminé");
}

private void OnAllCompleted()
{
    GD.Print("Tous les splash screens sont terminés");
    // Charger la scène suivante
    GetTree().ChangeSceneToFile("res://Scenes/MainMenu.tscn");
}
```

## ?? Exemple Complet (Credits.cs)

```csharp
using Godot;
using Satsuki.Manager;

public partial class Credits : Node
{
    private SplashScreenManager _splashScreenManager;
    
    public override void _Ready()
    {
        // Créer le manager
        _splashScreenManager = new SplashScreenManager();
        AddChild(_splashScreenManager);
        
        // Événements
        _splashScreenManager.AllSplashScreensCompleted += OnCompleted;
        
        // Ajouter les splash screens
        _splashScreenManager.AddTextSplash("SATSUKI", 2.5f, Colors.Orange);
        _splashScreenManager.AddTextSplash("Développé par\nMTerance", 2.0f, Colors.Cyan);
        _splashScreenManager.AddImageSplash("res://Assets/logo.png", 3.0f);
        _splashScreenManager.AddTextSplash("Merci d'avoir joué!", 2.0f, Colors.LightGreen);
        
        // Démarrer
        _splashScreenManager.StartSequence();
    }
    
    private void OnCompleted()
    {
        GetTree().ChangeSceneToFile("res://Scenes/MainMenu.tscn");
    }
    
    public override void _Input(InputEvent @event)
    {
        if (@event is InputEventKey key && key.Pressed)
        {
            if (key.Keycode == Key.Space)
                _splashScreenManager.Skip();      // Skip actuel
            else if (key.Keycode == Key.Escape)
                _splashScreenManager.SkipAll();   // Skip tout
        }
    }
}
```

## ?? API Détaillée

### Méthodes Principales

#### AddTextSplash
```csharp
void AddTextSplash(string text, float duration = 3.0f, Color? textColor = null)
```
Ajoute un splash screen texte.

**Paramètres:**
- `text`: Le texte à afficher
- `duration`: Durée d'affichage en secondes (défaut: 3.0)
- `textColor`: Couleur du texte (défaut: blanc)

#### AddImageSplash
```csharp
void AddImageSplash(string imagePath, float duration = 3.0f)
```
Ajoute un splash screen image.

**Paramètres:**
- `imagePath`: Chemin vers l'image (ex: "res://Assets/logo.png")
- `duration`: Durée d'affichage en secondes (défaut: 3.0)

#### StartSequence
```csharp
void StartSequence()
```
Démarre la séquence de splash screens.

#### Skip
```csharp
void Skip()
```
Passe au splash screen suivant.

#### SkipAll
```csharp
void SkipAll()
```
Saute toute la séquence et émet `AllSplashScreensCompleted`.

#### SetFadeSpeed
```csharp
void SetFadeSpeed(float speed)
```
Configure la vitesse des transitions fade (défaut: 2.0).

**Paramètres:**
- `speed`: Vitesse de transition (minimum: 0.1)

#### Clear
```csharp
void Clear()
```
Efface tous les splash screens de la liste.

#### GetSplashScreenCount
```csharp
int GetSplashScreenCount()
```
Retourne le nombre total de splash screens.

#### GetCurrentIndex
```csharp
int GetCurrentIndex()
```
Retourne l'index du splash screen actuel.

## ?? Contrôles par Défaut

Dans l'exemple `Credits.cs`, les contrôles suivants sont implémentés :

| Touche/Action | Effet |
|---------------|-------|
| **Espace** | Passe au splash screen suivant |
| **Entrée** | Passe au splash screen suivant |
| **Échap** | Saute toute la séquence |
| **Clic souris** | Passe au splash screen suivant |

## ?? Signaux (Events)

### SplashScreenCompleted
```csharp
[Signal]
public delegate void SplashScreenCompletedEventHandler();
```
Émis après chaque splash screen terminé.

### AllSplashScreensCompleted
```csharp
[Signal]
public delegate void AllSplashScreensCompletedEventHandler();
```
Émis quand tous les splash screens sont terminés.

## ?? Personnalisation

### Modifier la Vitesse de Transition
```csharp
// Transition plus rapide (fade en 0.5 seconde)
_splashScreenManager.SetFadeSpeed(4.0f);

// Transition plus lente (fade en 2 secondes)
_splashScreenManager.SetFadeSpeed(1.0f);
```

### Changer la Taille de Police
Modifiez directement dans `SplashScreenManager.cs` :
```csharp
_textDisplay.AddThemeFontSizeOverride("font_size", 64); // Plus grand
_textDisplay.AddThemeFontSizeOverride("font_size", 32); // Plus petit
```

### Ajouter un Fond de Couleur
```csharp
// Dans _Ready() du SplashScreenManager
var background = new ColorRect
{
    Color = new Color(0.1f, 0.1f, 0.15f), // Bleu foncé
    AnchorsPreset = (int)Control.LayoutPreset.FullRect
};
AddChild(background);
MoveChild(background, 0); // Mettre en premier
```

## ?? Configuration Avancée

### Séquence avec Mix Texte et Images
```csharp
_splashScreenManager.AddTextSplash("Présente", 1.5f);
_splashScreenManager.AddImageSplash("res://Assets/studio_logo.png", 3.0f);
_splashScreenManager.AddTextSplash("Un Jeu de", 1.5f);
_splashScreenManager.AddImageSplash("res://Assets/game_logo.png", 3.0f);
_splashScreenManager.AddTextSplash("Appuyez pour commencer", 0.0f); // Infini
```

### Affichage Infini
Pour un splash screen qui reste jusqu'au clic :
```csharp
_splashScreenManager.AddTextSplash("Appuyez pour continuer", 999.0f);
```

## ?? Dépannage

### Problème: Image ne s'affiche pas
**Cause**: Chemin d'accès incorrect ou image non chargée

**Solution**:
```csharp
// Vérifier que le chemin est correct
_splashScreenManager.AddImageSplash("res://Assets/Images/logo.png", 3.0f);

// Vérifier dans la sortie Godot si l'erreur apparaît :
// "? Impossible de charger l'image: ..."
```

### Problème: Texte trop petit/grand
**Solution**: Modifier la taille de police dans `SplashScreenManager.cs` ligne ~45

### Problème: Transitions trop rapides/lentes
**Solution**:
```csharp
_splashScreenManager.SetFadeSpeed(2.0f); // Ajuster la valeur
```

## ?? Notes

- ? Les splash screens sont affichés dans l'ordre d'ajout
- ?? Les transitions sont automatiques avec fade in/out
- ?? Le texte est centré horizontalement et verticalement
- ??? Les images sont mises à l'échelle en conservant le ratio (KeepAspectCentered)
- ?? La durée minimale de transition est de 1 seconde (0.5s fade in + 0.5s fade out)

## ?? Améliorations Futures

- [ ] Support des animations personnalisées
- [ ] Support des effets de particules
- [ ] Support audio (musique de fond)
- [ ] Transitions personnalisables (slide, zoom, etc.)
- [ ] Support des vidéos
- [ ] Boutons "Skip" visuels
- [ ] Barre de progression

## ?? Voir Aussi

- [Documentation Godot Tween](https://docs.godotengine.org/en/stable/classes/class_tween.html)
- [Documentation Godot Signals](https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html)

## ?? Conclusion

Le `SplashScreenManager` offre une solution simple et efficace pour créer des séquences de splash screens dans vos projets Godot. Utilisez-le pour vos crédits, intros de jeu, ou tutoriels !
