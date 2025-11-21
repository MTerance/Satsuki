# Diagnostic des Images de Crédits - SplashScreenManager

## État actuel

### Dossier des crédits
- **Chemin** : `C:\Users\sshom\source\repos\Satsuki\Satsuki\Assets\Img\Credits`
- **Statut** : ? Existe
- **Images trouvées** : 3 fichiers PNG
  1. `logo-Epitanime.png` (234 KB)
  2. `LogoOtakCoffee.png` (490 KB)
  3. `logo_Godot.png` (27 KB)

### Configuration actuelle de l'ImageDisplay

```csharp
_imageDisplay = new TextureRect
{
    ExpandMode = TextureRect.ExpandModeEnum.FitHeightProportional,
    StretchMode = TextureRect.StretchModeEnum.KeepAspectCentered,
    Visible = false,
    AnchorsPreset = (int)Control.LayoutPreset.FullRect
};
```

## Logs de debug ajoutés

### Dans `_Ready()`
- ? "SplashScreenManager: Debut de l'initialisation"
- ? "FadeOverlay cree"
- ? "ImageDisplay cree"
- ? "TextDisplay cree"
- ? "Timer cree"
- ? "SplashScreenManager initialise avec succes"

### Dans `FadeIn()` pour les images
- ? Type de splash (Text/Image)
- ? Chemin de l'image
- ? Taille de la texture
- ? Configuration de l'ImageDisplay (ExpandMode, StretchMode, Size, Position)
- ? État de la texture (null ou non)
- ? État de visibilité
- ? Progression du tween de fade

## Comment diagnostiquer

### 1. Lancez le jeu et vérifiez la console Godot
Cherchez les logs suivants dans l'ordre :

```
SplashScreenManager: Debut de l'initialisation
FadeOverlay cree
ImageDisplay cree
TextDisplay cree
Timer cree
SplashScreenManager initialise avec succes
Credits: Initialisation...
Splash screen image ajoute: res://Assets/Img/Credits/logo-Epitanime.png (3s)
Splash screen image ajoute: res://Assets/Img/Credits/LogoOtakCoffee.png (3s)
Splash screen image ajoute: res://Assets/Img/Credits/logo_Godot.png (3s)
3 splash screens images ajoutes depuis res://Assets/Img/Credits
Credits personnalises configures
Demarrage de la sequence de 3 splash screens
FadeIn: Debut pour type=Image
FadeIn: Configuration de l'image
  - Chemin: res://Assets/Img/Credits/...
  - Taille texture: (largeur, hauteur)
  - ImageDisplay ExpandMode: FitHeightProportional
  - ImageDisplay StretchMode: KeepAspectCentered
```

### 2. Vérifications à faire

#### Si les logs s'arrêtent avant "FadeIn: Debut pour type=Image"
- ? Problème : La séquence ne démarre pas
- Solution : Vérifier que `StartSequence()` est appelé

#### Si "Texture est null" apparaît
- ? Problème : Les images ne sont pas chargées
- Solution : Vérifier les chemins dans `res://Assets/Img/Credits/`

#### Si "FadeIn: Image configuree et visible=true" apparaît mais pas d'image visible
- ? Problème : L'image est configurée mais pas affichée
- Solutions possibles :
  1. Z-index : L'overlay noir cache l'image
  2. Taille : L'image est trop grande ou trop petite
  3. Position : L'image est hors de l'écran

## Solutions possibles

### Solution 1 : Vérifier l'ordre des couches (Z-index)
Le `_fadeOverlay` doit être au-dessus de l'image pour faire le fade.

**Ordre actuel dans `_Ready()` :**
1. `_fadeOverlay` (ajouté en premier)
2. `_imageDisplay` (ajouté en second)
3. `_textDisplay` (ajouté en troisième)

**Problème potentiel :** Si l'overlay a `MouseFilter.Ignore`, il devrait laisser passer l'affichage.

### Solution 2 : Changer le mode d'affichage
Essayer différents modes :

```csharp
// Option 1 : FitHeightProportional (actuel)
ExpandMode = TextureRect.ExpandModeEnum.FitHeightProportional

// Option 2 : KeepAspectCovered
ExpandMode = TextureRect.ExpandModeEnum.KeepAspectCovered

// Option 3 : FitWidth
ExpandMode = TextureRect.ExpandModeEnum.FitWidth
```

### Solution 3 : Forcer la mise à jour de l'affichage
Après avoir défini la texture, forcer un redessinage :

```csharp
_imageDisplay.Texture = splash.Texture;
_imageDisplay.Visible = true;
_imageDisplay.QueueRedraw(); // Forcer le redessin
```

### Solution 4 : Définir explicitement la taille
```csharp
_imageDisplay.Texture = splash.Texture;
_imageDisplay.CustomMinimumSize = new Vector2(800, 600); // Taille minimale
_imageDisplay.Visible = true;
```

## Test rapide

### Tester avec une image simple
Remplacer temporairement `SetupCustomCredits()` par :

```csharp
public void SetupCustomCredits()
{
    Clear();
    
    // Test avec un texte d'abord
    AddTextSplash("TEST AVANT IMAGE", 2.0f, Colors.Yellow, 64);
    
    // Puis une image
    AddImageSplash("res://Assets/Img/Credits/logo_Godot.png", 5.0f);
    
    // Puis un texte après
    AddTextSplash("TEST APRES IMAGE", 2.0f, Colors.Green, 64);
    
    GD.Print("Credits personnalises configures (MODE TEST)");
}
```

Si le texte avant et après s'affiche mais pas l'image, le problème est clairement dans l'affichage de l'image.

## Prochaines étapes

1. ? Lancez le jeu
2. ? Observez les logs dans la console Godot
3. ? Identifiez où le processus s'arrête
4. ? Partagez les logs pour un diagnostic plus précis
5. ? Testez les solutions proposées une par une
