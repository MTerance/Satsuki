# ?? Menu Rendering - DecorManager

**Date** : 22 novembre 2025  
**Fonctionnalité** : Affichage des menus UI (Title, MainMenu, Game) sur des surfaces 3D  
**Status** : ? Implémenté et compilé

---

## ?? Vue d'ensemble

La fonctionnalité **Menu Rendering** permet d'afficher les menus UI de votre jeu (écran titre, menu principal, interface de jeu) sur des surfaces 3D dans vos décors. Les boutons et éléments UI sont rendus sur une texture qui est ensuite appliquée sur une surface avec effet d'émission.

**Exemple** : Afficher le menu Title sur un écran TV dans un restaurant, le MainMenu sur un panneau holographique, etc.

---

## ? Fonctionnalités

### 1. Sélection de surface interactive
- ? Checkbox pour activer le mode
- ??? Cliquez sur une surface 3D dans l'éditeur
- ? La surface sélectionnée est mise en surbrillance

### 2. Configuration du menu
- ?? **Menu Type** : Title, MainMenu ou Game
- ?? **Texture** : Chemin vers la texture du menu
- ?? **Emission** : Couleur et intensité lumineuse

### 3. Sauvegarde dans JSON
- ?? Toutes les informations sauvegardées
- ?? Nom de surface, texture, type de menu, émission
- ?? Chargement automatique au reload

---

## ?? Utilisation

### Étape 1 : Charger une scène

```
Godot ? Decor Manager dock
Chemin: res://Scenes/Locations/Restaurant.tscn
? "Charger la scene"
```

### Étape 2 : Activer le mode Menu Rendering

```
? "Mode selection actif (cliquez sur une surface)"
Status devient rose ??
```

### Étape 3 : Choisir le type de menu

```
Menu: [Title ?]
Options:
- Title      ? Écran titre du jeu
- MainMenu   ? Menu principal
- Game       ? Interface de jeu
```

### Étape 4 : Sélectionner une surface

```
? Cliquer sur un écran, panneau dans la vue 3D
   Status: "Surface selectionnee: TV_Screen"
```

### Étape 5 : Choisir la texture du menu

```
Texture: res://Assets/Textures/title_menu_screen.png
? Cliquer "..." pour browser
```

### Étape 6 : Configurer l'émission

```
Emission: [Blanc] ? Choisir couleur
Energy: 1.5 ? Ajuster intensité (0-10)
```

### Étape 7 : Appliquer

```
? "Appliquer menu sur surface selectionnee"
   Le menu apparaît sur la surface avec effet lumineux
```

### Étape 8 : Sauvegarder dans JSON

```
? "Sauvegarder dans JSON"
   Fichier mis à jour: Configs/Restaurant_config.json
```

---

## ?? Interface utilisateur

```
??????????????????????????????????????????????
?  Menu Rendering (Affichage UI sur surfaces)? ??
??????????????????????????????????????????????
?  ? Mode selection actif                    ?
?     (cliquez sur une surface)              ?
??????????????????????????????????????????????
?  Menu: [Title ?]                           ?
??????????????????????????????????????????????
?  Texture: [res://Assets/...title.png][...]?
??????????????????????????????????????????????
?  Emission: [?? Blanc]  Energy: [1.5 ??]   ?
??????????????????????????????????????????????
?  [Appliquer menu sur surface selectionnee] ?
??????????????????????????????????????????????
?  Surfaces avec menu rendering:             ?
?  ??????????????????????????????????????    ?
?  ? 0: TV_Screen - Title (title.png)  ?    ?
?  ? 1: Panel - MainMenu (menu.png)    ?    ?
?  ? 2: Display - Game (game_ui.png)   ?    ?
?  ??????????????????????????????????????    ?
??????????????????????????????????????????????
?  [Retirer menu] [Tout effacer] [Sauv JSON]?
??????????????????????????????????????????????
```

---

## ?? Types de menu

### Title (Écran titre)
- **Usage** : Premier écran du jeu
- **Contient** : Logo, boutons "Start", "Options", "Quit"
- **Exemple** : Afficher sur écran TV dans hall d'entrée

### MainMenu (Menu principal)
- **Usage** : Menu après l'écran titre
- **Contient** : Navigation, sélection de mode, paramètres
- **Exemple** : Panneau holographique dans lobby

### Game (Interface de jeu)
- **Usage** : HUD et interface pendant le jeu
- **Contient** : Score, vie, mini-map, inventaire
- **Exemple** : Écrans de contrôle, tableaux d'affichage

---

## ?? Fichier JSON généré

### Structure complète

```json
{
  "ScenePath": "res://Scenes/Locations/Restaurant.tscn",
  "SceneName": "Restaurant",
  "SpawnPoints": [ /* ... */ ],
  "MenuRenderSurfaces": [
    {
      "SurfaceName": "TV_Screen",
      "TexturePath": "res://Assets/Textures/title_menu_screen.png",
      "MenuType": "Title",
      "EmissionColor": {
        "r": 1.0,
        "g": 1.0,
        "b": 1.0,
        "a": 1.0
      },
      "EmissionEnergy": 1.5
    },
    {
      "SurfaceName": "Menu_Panel",
      "TexturePath": "res://Assets/Textures/main_menu_screen.png",
      "MenuType": "MainMenu",
      "EmissionColor": {
        "r": 0.8,
        "g": 0.9,
        "b": 1.0,
        "a": 1.0
      },
      "EmissionEnergy": 1.2
    }
  ],
  "SavedAt": "2025-11-22T16:00:00Z"
}
```

### Champs MenuRenderSurfaceData

| Champ | Type | Description |
|-------|------|-------------|
| `SurfaceName` | string | Nom de la surface 3D (MeshInstance3D) |
| `TexturePath` | string | Chemin vers la texture du menu |
| `MenuType` | string | "Title", "MainMenu" ou "Game" |
| `EmissionColor` | Color | Couleur d'émission (RGBA) |
| `EmissionEnergy` | float | Intensité lumineuse (0-10) |

---

## ?? Cas d'usage

### 1. Restaurant - Écran titre sur TV

```
Surface: TV_Screen
Menu: Title
Texture: res://Assets/Textures/title_screen.png
Emission: Blanc
Energy: 1.5

Résultat: L'écran titre du jeu s'affiche sur la TV
         Les joueurs voient les boutons Start/Options/Quit
```

### 2. Hall - Menu principal sur panneau holographique

```
Surface: Holo_Panel
Menu: MainMenu
Texture: res://Assets/Textures/main_menu.png
Emission: Cyan
Energy: 1.2

Résultat: Le menu principal flotte sur le panneau holo
         Navigation et sélection de mode visibles
```

### 3. Salle de jeu - Interface sur écrans

```
Surface: Game_Monitor_1
Menu: Game
Texture: res://Assets/Textures/game_hud.png
Emission: Blanc-bleuté
Energy: 1.0

Résultat: HUD et interface de jeu affichés
         Score, vie, mini-map sur l'écran
```

---

## ?? Workflow complet

### Scénario : Configurer les menus du Restaurant

```
1. Charger Restaurant.tscn

2. Configurer écran titre
   ? Mode selection
   Menu: Title
   Cliquer sur TV_Screen
   Texture: res://Assets/Textures/title_screen.png
   Emission: Blanc, Energy: 1.5
   ? Appliquer

3. Configurer menu principal
   Menu: MainMenu
   Cliquer sur Menu_Panel
   Texture: res://Assets/Textures/main_menu.png
   Emission: Cyan, Energy: 1.2
   ? Appliquer

4. Sauvegarder
   ? "Sauvegarder dans JSON"
   Fichier: Configs/Restaurant_config.json ?

5. Résultat
   2 surfaces configurées:
   - TV_Screen affiche Title
   - Menu_Panel affiche MainMenu
```

---

## ?? Utilisation en jeu (Runtime)

### Charger et afficher les menus

```csharp
using Satsuki.Tools;

// Charger la configuration
var config = DecorLoader.LoadConfiguration("res://Scenes/Locations/Restaurant.tscn");

if (config != null && config.MenuRenderSurfaces != null)
{
    foreach (var menuSurface in config.MenuRenderSurfaces)
    {
        // Afficher le menu approprié selon le type
        switch (menuSurface.MenuType)
        {
            case "Title":
                DisplayTitleMenu(menuSurface.SurfaceName);
                break;
            case "MainMenu":
                DisplayMainMenu(menuSurface.SurfaceName);
                break;
            case "Game":
                DisplayGameUI(menuSurface.SurfaceName);
                break;
        }
    }
}
```

### Récupérer surfaces par type de menu

```csharp
// Obtenir toutes les surfaces Title
var titleSurfaces = DecorLoader.GetMenuRenderSurfacesByType(
    "res://Scenes/Locations/Restaurant.tscn",
    "Title"
);

foreach (var surface in titleSurfaces)
{
    GD.Print($"Surface Title: {surface.SurfaceName}");
    GD.Print($"Texture: {surface.TexturePath}");
}
```

---

## ?? Création des textures de menu

### Recommandations

**Résolution** :
- 1920x1080 (Full HD) pour grands écrans
- 1280x720 (HD) pour petits écrans
- 2048x2048 max pour panneaux carrés

**Format** :
- PNG avec transparence pour effets
- JPG pour fond opaque

**Design** :
- Boutons lisibles à distance
- Contraste élevé pour émission
- Couleurs qui ressortent

### Exemple de workflow Photoshop/GIMP

```
1. Créer canvas 1920x1080
2. Designer l'interface UI
   - Logo en haut
   - Boutons centrés
   - Texte lisible
3. Exporter en PNG
4. Sauvegarder dans Assets/Textures/
5. Importer dans Godot
6. Appliquer dans DecorManager
```

---

## ?? Résolution de problèmes

### La surface ne se sélectionne pas

**Solutions** :
```
1. Vérifier ? Mode selection actif
2. S'assurer que c'est un MeshInstance3D
3. Ajouter CollisionShape si nécessaire
```

### La texture n'apparaît pas

**Solutions** :
```
1. Vérifier le chemin (res://...)
2. Réimporter la texture dans Godot
3. Vérifier que la surface a un UV mapping
```

### Le menu ne se sauvegarde pas

**Solutions** :
```
1. Vérifier qu'une scène est chargée
2. Cliquer "Sauvegarder dans JSON"
3. Vérifier dossier Configs/ existe
```

### Le JSON ne se charge pas

**Solutions** :
```
1. Valider le JSON (format correct)
2. Vérifier les chemins de textures
3. Recharger la scène
```

---

## ? Performance

### Limites recommandées
- **Surfaces avec menu** : 2-4 par scène max
- **Résolution texture** : 1920x1080 max
- **Émission** : 0.8-2.0 pour performance optimale

### Optimisations
- Utiliser mipmaps pour textures
- Réduire résolution si distance éloignée
- Désactiver émission si non visible

---

## ?? Exemple complet

### Restaurant avec 3 menus

```json
{
  "ScenePath": "res://Scenes/Locations/Restaurant.tscn",
  "SceneName": "Restaurant",
  "MenuRenderSurfaces": [
    {
      "SurfaceName": "TV_Screen_Main",
      "TexturePath": "res://Assets/Textures/title_screen.png",
      "MenuType": "Title",
      "EmissionColor": { "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 },
      "EmissionEnergy": 1.5
    },
    {
      "SurfaceName": "Wall_Panel",
      "TexturePath": "res://Assets/Textures/main_menu.png",
      "MenuType": "MainMenu",
      "EmissionColor": { "r": 0.8, "g": 0.9, "b": 1.0, "a": 1.0 },
      "EmissionEnergy": 1.2
    },
    {
      "SurfaceName": "Game_Monitor",
      "TexturePath": "res://Assets/Textures/game_hud.png",
      "MenuType": "Game",
      "EmissionColor": { "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 },
      "EmissionEnergy": 1.0
    }
  ]
}
```

---

## ? Checklist

- [ ] Scène chargée
- [ ] Mode selection ?
- [ ] Type de menu choisi (Title/MainMenu/Game)
- [ ] Surface sélectionnée (clic 3D)
- [ ] Texture choisie (chemin valide)
- [ ] Émission configurée
- [ ] Menu appliqué (clic bouton)
- [ ] JSON sauvegardé
- [ ] Scène sauvegardée (Ctrl+S)

---

## ?? Résumé

**Menu Rendering** vous permet de :
- ? Afficher les menus UI sur des surfaces 3D
- ? Choisir le type de menu (Title/MainMenu/Game)
- ? Configurer texture et émission
- ? Sauvegarder dans JSON avec le type de menu
- ? Charger et afficher automatiquement en jeu

**Créez des décors immersifs où les menus font partie du monde ! ???**

---

*Date : 22 novembre 2025*  
*Fonctionnalité : Menu Rendering*  
*Status : ? Implémenté et documenté*
