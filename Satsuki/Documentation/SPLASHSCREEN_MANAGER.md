# ?? SplashScreenManager - Documentation

## Vue d'ensemble

Le `SplashScreenManager` est un syst�me de gestion de splash screens (�crans de transition) pour Godot, permettant d'afficher des s�quences d'�crans avec des transitions fade in/out.

## ?? Fonctionnalit�s

? **Types de Splash Screens**
- ?? Splash screens texte avec couleurs personnalisables
- ??? Splash screens image (PNG, JPG, etc.)

? **Transitions**
- Fade in/out automatiques
- Vitesse de transition configurable
- Transitions fluides entre les �crans

? **Contr�les**
- ?? Skip splash screen actuel (Espace, Entr�e, Clic souris)
- ???? Skip toute la s�quence (�chap)
- ?? Dur�es personnalisables par splash screen

? **�v�nements**
- Signal `SplashScreenCompleted` : �mis apr�s chaque splash screen
- Signal `AllSplashScreensCompleted` : �mis � la fin de toute la s�quence

## ?? Installation

Le `SplashScreenManager` est cr�� dynamiquement dans votre sc�ne :

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
// Texte simple (dur�e par d�faut: 3 secondes)
_splashScreenManager.AddTextSplash("Bienvenue!");

// Avec dur�e personnalis�e
_splashScreenManager.AddTextSplash("Mon Jeu", 2.5f);

// Avec couleur personnalis�e
_splashScreenManager.AddTextSplash("Cr�dits", 2.0f, Colors.Cyan);

// Texte multiligne
_splashScreenManager.AddTextSplash("D�velopp� par\nMTerance", 3.0f);
```

#### Splash Screen Image
```csharp
// Image avec dur�e par d�faut (3 secondes)
_splashScreenManager.AddImageSplash("res://Assets/logo.png");

// Avec dur�e personnalis�e
_splashScreenManager.AddImageSplash("res://Assets/splash.png", 4.0f);
```

### 2. D�marrer la S�quence

```csharp
_splashScreenManager.StartSequence();
```

### 3. S'abonner aux �v�nements

```csharp
_splashScreenManager.SplashScreenCompleted += OnSplashCompleted;
_splashScreenManager.AllSplashScreensCompleted += OnAllCompleted;

private void OnSplashCompleted()
{
    GD.Print("Un splash screen est termin�");
}

private void OnAllCompleted()
{
    GD.Print("Tous les splash screens sont termin�s");
    // Charger la sc�ne suivante
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
        // Cr�er le manager
        _splashScreenManager = new SplashScreenManager();
        AddChild(_splashScreenManager);
        
        // �v�nements
        _splashScreenManager.AllSplashScreensCompleted += OnCompleted;
        
        // Ajouter les splash screens
        _splashScreenManager.AddTextSplash("SATSUKI", 2.5f, Colors.Orange);
        _splashScreenManager.AddTextSplash("D�velopp� par\nMTerance", 2.0f, Colors.Cyan);
        _splashScreenManager.AddImageSplash("res://Assets/logo.png", 3.0f);
        _splashScreenManager.AddTextSplash("Merci d'avoir jou�!", 2.0f, Colors.LightGreen);
        
        // D�marrer
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

## ?? API D�taill�e

### M�thodes Principales

#### AddTextSplash
```csharp
void AddTextSplash(string text, float duration = 3.0f, Color? textColor = null)
```
Ajoute un splash screen texte.

**Param�tres:**
- `text`: Le texte � afficher
- `duration`: Dur�e d'affichage en secondes (d�faut: 3.0)
- `textColor`: Couleur du texte (d�faut: blanc)

#### AddImageSplash
```csharp
void AddImageSplash(string imagePath, float duration = 3.0f)
```
Ajoute un splash screen image.

**Param�tres:**
- `imagePath`: Chemin vers l'image (ex: "res://Assets/logo.png")
- `duration`: Dur�e d'affichage en secondes (d�faut: 3.0)

#### StartSequence
```csharp
void StartSequence()
```
D�marre la s�quence de splash screens.

#### Skip
```csharp
void Skip()
```
Passe au splash screen suivant.

#### SkipAll
```csharp
void SkipAll()
```
Saute toute la s�quence et �met `AllSplashScreensCompleted`.

#### SetFadeSpeed
```csharp
void SetFadeSpeed(float speed)
```
Configure la vitesse des transitions fade (d�faut: 2.0).

**Param�tres:**
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

## ?? Contr�les par D�faut

Dans l'exemple `Credits.cs`, les contr�les suivants sont impl�ment�s :

| Touche/Action | Effet |
|---------------|-------|
| **Espace** | Passe au splash screen suivant |
| **Entr�e** | Passe au splash screen suivant |
| **�chap** | Saute toute la s�quence |
| **Clic souris** | Passe au splash screen suivant |

## ?? Signaux (Events)

### SplashScreenCompleted
```csharp
[Signal]
public delegate void SplashScreenCompletedEventHandler();
```
�mis apr�s chaque splash screen termin�.

### AllSplashScreensCompleted
```csharp
[Signal]
public delegate void AllSplashScreensCompletedEventHandler();
```
�mis quand tous les splash screens sont termin�s.

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
    Color = new Color(0.1f, 0.1f, 0.15f), // Bleu fonc�
    AnchorsPreset = (int)Control.LayoutPreset.FullRect
};
AddChild(background);
MoveChild(background, 0); // Mettre en premier
```

## ?? Configuration Avanc�e

### S�quence avec Mix Texte et Images
```csharp
_splashScreenManager.AddTextSplash("Pr�sente", 1.5f);
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

## ?? D�pannage

### Probl�me: Image ne s'affiche pas
**Cause**: Chemin d'acc�s incorrect ou image non charg�e

**Solution**:
```csharp
// V�rifier que le chemin est correct
_splashScreenManager.AddImageSplash("res://Assets/Images/logo.png", 3.0f);

// V�rifier dans la sortie Godot si l'erreur appara�t :
// "? Impossible de charger l'image: ..."
```

### Probl�me: Texte trop petit/grand
**Solution**: Modifier la taille de police dans `SplashScreenManager.cs` ligne ~45

### Probl�me: Transitions trop rapides/lentes
**Solution**:
```csharp
_splashScreenManager.SetFadeSpeed(2.0f); // Ajuster la valeur
```

## ?? Notes

- ? Les splash screens sont affich�s dans l'ordre d'ajout
- ?? Les transitions sont automatiques avec fade in/out
- ?? Le texte est centr� horizontalement et verticalement
- ??? Les images sont mises � l'�chelle en conservant le ratio (KeepAspectCentered)
- ?? La dur�e minimale de transition est de 1 seconde (0.5s fade in + 0.5s fade out)

## ?? Am�liorations Futures

- [ ] Support des animations personnalis�es
- [ ] Support des effets de particules
- [ ] Support audio (musique de fond)
- [ ] Transitions personnalisables (slide, zoom, etc.)
- [ ] Support des vid�os
- [ ] Boutons "Skip" visuels
- [ ] Barre de progression

## ?? Voir Aussi

- [Documentation Godot Tween](https://docs.godotengine.org/en/stable/classes/class_tween.html)
- [Documentation Godot Signals](https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html)

## ?? Conclusion

Le `SplashScreenManager` offre une solution simple et efficace pour cr�er des s�quences de splash screens dans vos projets Godot. Utilisez-le pour vos cr�dits, intros de jeu, ou tutoriels !
