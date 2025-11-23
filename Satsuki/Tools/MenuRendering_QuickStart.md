# ?? Quick Start - Menu Rendering

**Afficher vos menus UI sur des surfaces 3D en 2 minutes !**

---

## ? Démarrage rapide

### 1?? Charger une scène (20 sec)

```
Godot ? Decor Manager dock
Chemin: res://Scenes/Locations/Restaurant.tscn
? "Charger la scene"
```

### 2?? Activer le mode (5 sec)

```
? "Mode selection actif (cliquez sur une surface)"
Status devient rose ??
```

### 3?? Choisir le type de menu (5 sec)

```
Menu: [Title ?]
- Title      ? Écran titre
- MainMenu   ? Menu principal  
- Game       ? Interface jeu
```

### 4?? Sélectionner la surface (10 sec)

```
? Cliquer sur un écran/panneau dans la vue 3D
   Status: "Surface selectionnee: TV_Screen" ?
```

### 5?? Choisir la texture (30 sec)

```
Texture: res://Assets/Textures/title_screen.png
? Cliquer "..." pour browser
```

### 6?? Configurer émission (15 sec)

```
Emission: [Blanc] ??
Energy: 1.5 ?
```

### 7?? Appliquer (5 sec)

```
? "Appliquer menu sur surface selectionnee"
   Menu apparaît avec effet lumineux ?
```

### 8?? Sauvegarder (10 sec)

```
? "Sauvegarder dans JSON"
   Fichier: Configs/Restaurant_config.json ?
```

---

## ?? Résultat JSON

```json
{
  "MenuRenderSurfaces": [
    {
      "SurfaceName": "TV_Screen",
      "TexturePath": "res://Assets/Textures/title_screen.png",
      "MenuType": "Title",
      "EmissionColor": { "r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0 },
      "EmissionEnergy": 1.5
    }
  ]
}
```

---

## ?? Types de menu

| Type | Usage | Exemple |
|------|-------|---------|
| **Title** | Écran titre | Logo + Start/Quit |
| **MainMenu** | Menu principal | Navigation + Options |
| **Game** | Interface jeu | HUD + Score + Vie |

---

## ?? Exemples de textures

```
res://Assets/Textures/title_screen.png     ? Logo + boutons
res://Assets/Textures/main_menu.png        ? Navigation
res://Assets/Textures/game_hud.png         ? Interface jeu
```

---

## ?? Paramètres recommandés

| Menu | Emission Color | Energy |
|------|----------------|--------|
| **Title** | Blanc | 1.5 |
| **MainMenu** | Cyan/Bleu | 1.2 |
| **Game** | Blanc | 1.0 |

---

## ? Checklist

- [ ] Scène chargée
- [ ] Mode selection ?
- [ ] Type menu choisi
- [ ] Surface cliquée
- [ ] Texture choisie
- [ ] Émission configurée
- [ ] Menu appliqué
- [ ] JSON sauvegardé

---

## ?? Utilisation en jeu

```csharp
using Satsuki.Tools;

// Charger config
var config = DecorLoader.LoadConfiguration("res://Scenes/Locations/Restaurant.tscn");

// Afficher selon type
foreach (var menu in config.MenuRenderSurfaces)
{
    switch (menu.MenuType)
    {
        case "Title":
            DisplayTitleMenu(menu.SurfaceName);
            break;
        case "MainMenu":
            DisplayMainMenu(menu.SurfaceName);
            break;
        case "Game":
            DisplayGameUI(menu.SurfaceName);
            break;
    }
}
```

---

## ?? Astuce pro

```
Pour un écran réaliste:
- Menu: Title
- Texture: 1920x1080 PNG
- Emission: Blanc (1.0, 1.0, 1.0)
- Energy: 1.5
- Design: Boutons grands et lisibles
```

---

*Guide complet : [DecorManager_MenuRendering_Guide.md](../Documentation/DecorManager_MenuRendering_Guide.md)*
