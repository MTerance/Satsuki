# ?? Movie Rendering - DecorManager

**Date** : 22 novembre 2025  
**Fonctionnalité** : Application de textures vidéo/images avec émission sur des surfaces 3D  
**Status** : ? Implémenté et compilé

---

## ?? Vue d'ensemble

La fonctionnalité **Movie Rendering** permet d'appliquer des textures (images ou vidéos) avec effet d'émission sur des surfaces 3D dans vos décors. Parfait pour créer des écrans TV, projecteurs, panneaux lumineux, etc.

---

## ? Fonctionnalités

### 1. Sélection de surface interactive
- ? Checkbox pour activer le mode
- ??? Cliquez sur une surface 3D dans l'éditeur
- ? La surface sélectionnée est mise en surbrillance

### 2. Configuration de texture
- ?? Champ de chemin avec bouton browse
- ??? Support vidéo (.ogv, .webm)
- ??? Support image (.png, .jpg)

### 3. Paramètres d'émission
- ?? Color Picker pour la couleur d'émission
- ? SpinBox pour l'intensité (0-10)
- ?? Checkbox pour boucler la vidéo

### 4. Gestion des surfaces
- ?? Liste des surfaces avec texture appliquée
- ??? Retirer une texture spécifique
- ? Effacer toutes les textures

---

## ?? Utilisation

### Étape 1 : Charger une scène

```
Godot ? Decor Manager dock
Chemin: res://Scenes/Locations/Restaurant.tscn
? "Charger la scene"
```

### Étape 2 : Activer le mode Movie Rendering

```
? "Mode selection actif (cliquez sur une surface)"
Status devient rose ?
```

### Étape 3 : Sélectionner une surface

```
? Cliquer sur un mur, écran, panneau dans la vue 3D
   Status: "Surface selectionnee: [Nom]"
```

### Étape 4 : Choisir une texture

```
Texture: res://Assets/Videos/movie.ogv
? Cliquer "..." pour browser
   Filtres: Video Files (.ogv, .webm)
           Image Files (.png, .jpg)
```

### Étape 5 : Configurer l'émission

```
Emission: [Blanc] ? Choisir couleur
Energy: 1.0 ? Ajuster intensité (0-10)
? Boucle video (loop)
```

### Étape 6 : Appliquer

```
? "Appliquer texture sur surface selectionnee"
   La texture apparaît avec effet lumineux
```

---

## ?? Interface utilisateur

```
??????????????????????????????????????????????
?  Movie Rendering (Texture Video)          ? (rose)
??????????????????????????????????????????????
?  ? Mode selection actif                    ?
?     (cliquez sur une surface)              ?
??????????????????????????????????????????????
?  Texture: [res://Assets/...movie.ogv][...]?
??????????????????????????????????????????????
?  Emission: [?? Blanc]  Energy: [1.0 ??]   ?
?  ? Boucle video (loop)                     ?
??????????????????????????????????????????????
?  [Appliquer texture sur surface selectionnee]?
??????????????????????????????????????????????
?  Surfaces avec texture video:              ?
?  ??????????????????????????????????????    ?
?  ? 0: TVScreen - movie.ogv            ?    ?
?  ? 1: Billboard - ad.png              ?    ?
?  ??????????????????????????????????????    ?
??????????????????????????????????????????????
?  [Retirer texture] [Tout effacer]          ?
??????????????????????????????????????????????
```

---

## ?? Paramètres

### Emission Color (Couleur d'émission)
- **Description** : Couleur de la lumière émise par la surface
- **Défaut** : Blanc
- **Exemples** :
  - Blanc ? Écran TV naturel
  - Bleu ? Panneau holographique
  - Vert ? Écran de contrôle
  - Rouge ? Panneau d'alerte

### Emission Energy (Intensité d'émission)
- **Range** : 0.0 - 10.0
- **Défaut** : 1.0
- **Exemples** :
  - 0.5 ? Écran peu lumineux
  - 1.0 ? Écran normal
  - 2.0 ? Écran très lumineux
  - 5.0+ ? Projecteur puissant

### Loop Video
- ? **Activé** : La vidéo boucle infiniment
- ? **Désactivé** : La vidéo joue une fois

---

## ?? Cas d'usage

### 1. Écran TV dans un restaurant

```
Surface: TV_Screen
Texture: res://Assets/Videos/restaurant_ad.ogv
Emission: Blanc
Energy: 1.5
Loop: ?
```

### 2. Panneau publicitaire extérieur

```
Surface: Billboard_Mesh
Texture: res://Assets/Images/ad_poster.png
Emission: Blanc
Energy: 2.0
Loop: ?
```

### 3. Écran de sécurité

```
Surface: Security_Monitor
Texture: res://Assets/Videos/surveillance.webm
Emission: Bleu verdâtre
Energy: 0.8
Loop: ?
```

### 4. Projecteur de cinéma

```
Surface: Cinema_Screen
Texture: res://Assets/Videos/movie_trailer.ogv
Emission: Blanc chaud
Energy: 3.0
Loop: ?
```

### 5. Panneau holographique

```
Surface: Holo_Panel
Texture: res://Assets/Videos/hologram_interface.webm
Emission: Cyan
Energy: 1.2
Loop: ?
```

---

## ?? Fonctionnement technique

### Application de texture

```csharp
// 1. Trouver le MeshInstance3D
MeshInstance3D meshInstance = surface as MeshInstance3D;

// 2. Créer le matériau
var material = new StandardMaterial3D();
material.AlbedoTexture = GD.Load<Texture2D>(texturePath);

// 3. Configurer l'émission
material.EmissionEnabled = true;
material.Emission = emissionColor;
material.EmissionEnergyMultiplier = energy;
material.EmissionTexture = material.AlbedoTexture;

// 4. Appliquer
meshInstance.MaterialOverride = material;
```

### Sélection de surface

```csharp
// Raycast depuis la caméra
var from = camera.ProjectRayOrigin(mousePosition);
var to = from + camera.ProjectRayNormal(mousePosition) * 1000;

var spaceState = camera.GetWorld3D().DirectSpaceState;
var query = PhysicsRayQueryParameters3D.Create(from, to);
var result = spaceState.IntersectRay(query);

if (result.Count > 0)
{
    var surface = result["collider"].As<Node3D>();
    SelectSurface(surface);
}
```

---

## ?? Structure des données

### MovieRenderSurface

```csharp
public class MovieRenderSurface
{
    public MeshInstance3D Surface { get; set; }      // La surface 3D
    public string TexturePath { get; set; }          // Chemin de la texture
    public Color EmissionColor { get; set; }         // Couleur d'émission
    public float EmissionEnergy { get; set; }        // Intensité
    public bool Loop { get; set; }                   // Boucle vidéo
}
```

---

## ?? Conseils de design

### Choix des surfaces
- ? Surfaces planes (murs, écrans, panneaux)
- ? Surfaces avec UV mapping correct
- ?? Éviter surfaces courbes complexes

### Textures recommandées
- **Vidéos** : 1920x1080 ou 1280x720
- **Images** : 2048x2048 max pour performance
- **Format** : .ogv ou .webm pour vidéo, .png pour image

### Paramètres d'émission
- **Intérieur sombre** : Energy 1.5-3.0
- **Intérieur éclairé** : Energy 0.8-1.5
- **Extérieur** : Energy 2.0-5.0
- **Projecteur** : Energy 5.0-10.0

### Performance
- Limiter à **2-3 surfaces vidéo** par scène
- Préférer images statiques quand possible
- Utiliser résolutions appropriées

---

## ?? Résolution de problèmes

### La surface ne se sélectionne pas

**Causes** :
- Mode non activé
- Surface sans collision
- Pas de MeshInstance3D

**Solutions** :
```
1. Vérifier ? Mode selection actif
2. Ajouter CollisionShape à la surface
3. S'assurer que c'est un MeshInstance3D
```

### La texture n'apparaît pas

**Causes** :
- Chemin incorrect
- Fichier non importé
- Surface sans UV mapping

**Solutions** :
```
1. Vérifier le chemin (res://...)
2. Réimporter le fichier dans Godot
3. Vérifier UV mapping dans Blender
```

### L'émission est trop faible/forte

**Solutions** :
```
1. Ajuster Energy: 0.5 ? 3.0
2. Changer couleur d'émission
3. Vérifier éclairage ambiant de la scène
```

### La vidéo ne bouge pas

**Info** :
```
Dans l'éditeur, les vidéos sont statiques.
La lecture vidéo fonctionne en jeu (runtime).

Pour tester : Lancer le jeu (F5)
```

---

## ?? Workflow complet

### Scénario : Ajouter un écran TV au restaurant

```
1. Ouvrir Restaurant.tscn dans Decor Manager

2. Activer Movie Rendering
   ? Mode selection actif

3. Cliquer sur le mesh de la TV
   Status: "Surface selectionnee: TV_Screen"

4. Choisir la vidéo
   Texture: res://Assets/Videos/restaurant_ad.ogv
   
5. Configurer émission
   Color: Blanc
   Energy: 1.5
   Loop: ?

6. Appliquer
   ? "Appliquer texture sur surface selectionnee"
   
7. Résultat
   L'écran TV montre la vidéo avec effet lumineux
   
8. Sauvegarder la scène (Ctrl+S)
```

---

## ?? Limites et notes

### Limites actuelles
- ?? Vidéos statiques dans l'éditeur
- ?? Lecture vidéo uniquement en runtime
- ?? Pas de contrôle timeline
- ?? Une seule texture par surface

### Améliorations futures
- ?? Preview vidéo dans l'éditeur
- ?? Contrôles play/pause/stop
- ?? Support WebCam
- ??? Timeline scrubbing
- ?? Audio synchronisé

---

## ?? Galerie d'exemples

### Restaurant
- ?? Écran TV (menu digital)
- ?? Panneau publicitaire
- ?? Enseigne lumineuse

### Hall d'accueil
- ??? Écran d'informations
- ?? Tableau d'affichage
- ?? Décorations lumineuses

### Salle de jeu
- ?? Écrans de jeu
- ?? Tableau des scores
- ?? Effets lumineux

### Extérieur
- ?? Billboard animé
- ?? Panneau de signalisation
- ?? Enseignes de rue

---

## ? Checklist d'utilisation

- [ ] Scène chargée
- [ ] Mode selection actif ?
- [ ] Surface sélectionnée (visible dans status)
- [ ] Texture choisie (chemin valide)
- [ ] Émission configurée (couleur + energy)
- [ ] Loop défini (? ou ?)
- [ ] Texture appliquée (clic sur bouton)
- [ ] Scène sauvegardée (Ctrl+S)

---

## ?? Résumé

**Movie Rendering** vous permet de :
- ? Sélectionner des surfaces par clic 3D
- ? Appliquer textures vidéo/image
- ? Configurer émission (couleur + intensité)
- ? Gérer plusieurs surfaces
- ? Retirer/effacer facilement

**Parfait pour créer des décors vivants et immersifs ! ??**

---

*Date : 22 novembre 2025*  
*Fonctionnalité : Movie Rendering*  
*Status : ? Implémenté et documenté*
