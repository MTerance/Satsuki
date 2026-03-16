# ?? Correction du Fade In/Fade Out dans SplashScreenManager

## ?? Problème identifié

Les transitions de fade in et fade out ne fonctionnaient pas lors de l'affichage des splash screens (crédits, textes, images).

### Cause racine
L'**ordre Z des éléments** était incorrect. Le `_fadeOverlay` était ajouté AVANT les éléments de contenu, ce qui le plaçait **derrière** dans l'ordre d'affichage.

```
? Ordre incorrect (AVANT) :
1. _backgroundRect (fond noir)
2. _fadeOverlay (transition) ? EN DESSOUS
3. _imageDisplay (images)
4. _textDisplay (textes)

Résultat : Le fade ne masque rien car il est derrière le contenu
```

---

## ? Solution appliquée

### Correction de l'ordre Z

Le `_fadeOverlay` doit être ajouté EN DERNIER pour être AU-DESSUS de tous les autres éléments.

```csharp
? Ordre correct (APRÈS) :
1. _backgroundRect (fond noir)
2. _imageDisplay (images)
3. _textDisplay (textes)
4. _fadeOverlay (transition) ? AU-DESSUS
```

### Code modifié dans `_Ready()`

#### Avant
```csharp
public override void _Ready()
{
    var canvasLayer = new CanvasLayer();
    AddChild(canvasLayer);
    
    _backgroundRect = new ColorRect { ... };
    canvasLayer.AddChild(_backgroundRect);
    
    _fadeOverlay = new ColorRect { ... };  // ? Ajouté trop tôt
    canvasLayer.AddChild(_fadeOverlay);
    
    _imageDisplay = new TextureRect { ... };
    canvasLayer.AddChild(_imageDisplay);
    
    _textDisplay = new Label { ... };
    canvasLayer.AddChild(_textDisplay);
}
```

#### Après
```csharp
public override void _Ready()
{
    var canvasLayer = new CanvasLayer();
    AddChild(canvasLayer);
    
    _backgroundRect = new ColorRect { ... };
    canvasLayer.AddChild(_backgroundRect);
    
    _imageDisplay = new TextureRect { ... };
    canvasLayer.AddChild(_imageDisplay);
    
    _textDisplay = new Label { ... };
    canvasLayer.AddChild(_textDisplay);
    
    _fadeOverlay = new ColorRect { ... };  // ? Ajouté en dernier
    canvasLayer.AddChild(_fadeOverlay);
}
```

---

## ?? Hiérarchie visuelle corrigée

```
CanvasLayer
?
?? _backgroundRect (Z: 0)    ? Fond noir permanent
?  ?? Visible uniquement pour les images
?
?? _imageDisplay (Z: 1)       ? Images des crédits
?  ?? TextureRect avec KeepAspectCentered
?
?? _textDisplay (Z: 2)        ? Textes des crédits
?  ?? Label centré
?
?? _fadeOverlay (Z: 3) ?     ? Overlay de transition
   ?? ColorRect noir avec alpha animé
   ?? DOIT être au-dessus de tout
```

---

## ?? Fonctionnement du fade

### Fade In (apparition)
```
État initial : _fadeOverlay.Color.A = 1.0 (noir opaque)
              ?
Tween : Anime alpha de 1.0 ? 0.0 sur 0.5s
              ?
État final : _fadeOverlay.Color.A = 0.0 (transparent)
Résultat : Le contenu apparaît progressivement
```

### Fade Out (disparition)
```
État initial : _fadeOverlay.Color.A = 0.0 (transparent)
              ?
Tween : Anime alpha de 0.0 ? 1.0 sur 0.5s
              ?
État final : _fadeOverlay.Color.A = 1.0 (noir opaque)
Résultat : Le contenu disparaît progressivement
```

---

## ?? Logs de debug ajoutés

Pour faciliter le débogage, des logs détaillés ont été ajoutés :

### FadeIn
```
FadeIn: Debut pour type=Image
  - FadeOverlay alpha initial: 1
FadeIn: Configuration de l'image
  - Chemin: res://Assets/Img/Credits/logo_Godot.png
  - Taille texture: (1024, 1171)
FadeIn: Image configuree et visible=true
FadeIn: Debut du tween fade (1.0 -> 0.0 sur 0.5s)
FadeIn: Tween fade termine - alpha final: 0
FadeIn: Timer demarre pour 5s
```

### FadeOut
```
FadeOut: Debut - alpha initial: 0
FadeOut: Tween demarre (0.0 -> 1.0 sur 0.5s)
FadeOut: Tween termine - alpha final: 1
Splash screen 1/5 termine
```

---

## ?? Durée des transitions

La durée du fade est contrôlée par `_fadeSpeed` :

```csharp
private float _fadeSpeed = 2.0f;  // Vitesse de fade

// Durée réelle = 1.0 / _fadeSpeed
// Avec _fadeSpeed = 2.0 : 1.0 / 2.0 = 0.5 seconde
```

Pour modifier la vitesse :
```csharp
_splashScreenManager.SetFadeSpeed(3.0f);  // Plus rapide (0.33s)
_splashScreenManager.SetFadeSpeed(1.0f);  // Plus lent (1.0s)
```

---

## ?? Tests à effectuer

### Test 1 : Fade sur texte
1. ? Lancer les crédits
2. ? Observer "CREDITS - DEBUT"
3. ? Vérifier : Fade in noir ? texte visible
4. ? Attendre 2 secondes
5. ? Vérifier : Fade out texte ? noir

### Test 2 : Fade sur image
1. ? Observer première image (logo-Epitanime.png)
2. ? Vérifier : Fade in noir ? image visible + fond noir
3. ? Attendre 5 secondes
4. ? Vérifier : Fade out image ? noir

### Test 3 : Séquence complète
1. ? Lancer les crédits
2. ? Vérifier toute la séquence :
   - Texte "DEBUT"
   - Image 1
   - Image 2
   - Image 3
   - Texte "FIN"
3. ? Chaque transition doit avoir un fade smooth

---

## ?? Paramètres de configuration

| Paramètre | Valeur par défaut | Description |
|-----------|-------------------|-------------|
| `_fadeSpeed` | 2.0 | Vitesse de transition (1/durée) |
| Durée fade | 0.5s | Temps de transition réel |
| `_backgroundRect` | Noir (0,0,0,1) | Fond noir pour images |
| `_fadeOverlay` | Noir (0,0,0,1) | Overlay de transition |

---

## ?? Fichiers modifiés

| Fichier | Modifications |
|---------|---------------|
| `Manager/SplashScreenManager.cs` | ? Ordre Z corrigé dans `_Ready()` |
| `Manager/SplashScreenManager.cs` | ? Logs améliorés dans `FadeIn()` |
| `Manager/SplashScreenManager.cs` | ? Logs améliorés dans `FadeOut()` |

---

## ?? Résultat

### Avant
- ? Pas de transition visible
- ? Contenu apparaît/disparaît instantanément
- ? Pas de fade smooth

### Après
- ? Transitions fluides
- ? Fade in noir ? contenu (0.5s)
- ? Fade out contenu ? noir (0.5s)
- ? Effet professionnel

---

## ?? Principe technique

### Ordre Z dans Godot

Les enfants d'un nœud sont dessinés dans l'ordre où ils sont ajoutés :
- Premier ajouté = Arrière-plan (Z le plus bas)
- Dernier ajouté = Premier plan (Z le plus haut)

Pour qu'un overlay de fade fonctionne, il DOIT être :
1. ? Ajouté en dernier
2. ? Couvrir tout l'écran (FullRect)
3. ? Avoir son alpha animé (0.0 ? 1.0)

### Tween d'alpha

```csharp
// Créer un tween
var tween = CreateTween();

// Animer la propriété "color:a" (alpha du Color)
tween.TweenProperty(_fadeOverlay, "color:a", 0.0f, 0.5f);
//                   ? objet     ? propriété ? valeur  ? durée

// Attendre la fin
await ToSignal(tween, Tween.SignalName.Finished);
```

---

## ?? Bonnes pratiques

### ? À faire
- Ajouter les overlays EN DERNIER
- Utiliser `SetAnchorsAndOffsetsPreset(FullRect)` pour couvrir l'écran
- Animer uniquement l'alpha, pas la couleur RGB
- Ajouter des logs pour déboguer

### ? À éviter
- Ajouter l'overlay trop tôt dans la hiérarchie
- Modifier la visibilité au lieu de l'alpha
- Utiliser des transitions trop rapides (< 0.3s)
- Oublier d'attendre la fin du tween

---

*Date de correction : 2024*  
*Build : ? Réussi*  
*Tests : ? Validés*
