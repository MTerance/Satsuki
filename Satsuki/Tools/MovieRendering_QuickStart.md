# ?? Quick Start - Movie Rendering

**Appliquer une texture vidéo sur une surface en 2 minutes !**

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

### 3?? Sélectionner la surface (10 sec)

```
? Cliquer sur un mur/écran dans la vue 3D
   Status: "Surface selectionnee: [Nom]" ?
```

### 4?? Choisir la texture (30 sec)

```
Texture: res://Assets/Videos/movie.ogv
? Cliquer "..." pour browser
   
Ou image:
Texture: res://Assets/Images/screen.png
```

### 5?? Configurer émission (15 sec)

```
Emission: [Blanc] ??
Energy: 1.5 ?
? Boucle video
```

### 6?? Appliquer (5 sec)

```
? "Appliquer texture sur surface selectionnee"
   Texture apparaît avec effet lumineux ?
```

### 7?? Sauvegarder (5 sec)

```
Ctrl+S dans Godot
Scène sauvegardée ?
```

---

## ?? Résultat

```
Surface: TV_Screen
Texture: movie.ogv (vidéo qui boucle)
Émission: Blanc brillant
Energy: 1.5
? Écran TV lumineux avec vidéo !
```

---

## ?? Paramètres rapides

| Usage | Emission Color | Energy |
|-------|----------------|--------|
| **Écran TV** | Blanc | 1.0-1.5 |
| **Projecteur** | Blanc chaud | 3.0-5.0 |
| **Panneau holo** | Cyan/Bleu | 1.2-2.0 |
| **Enseigne** | Couleur vive | 2.0-4.0 |
| **Monitor** | Vert/Bleu | 0.8-1.2 |

---

## ?? Types de texture

- ??? **Vidéo** : .ogv, .webm (boucle automatique)
- ??? **Image** : .png, .jpg (statique)

---

## ?? Exemples de chemins

```
res://Assets/Videos/restaurant_ad.ogv
res://Assets/Images/menu_digital.png
res://Assets/Videos/hologram.webm
res://Assets/Images/billboard.jpg
```

---

## ? Checklist

- [ ] Scène chargée
- [ ] Mode selection ?
- [ ] Surface cliquée
- [ ] Texture choisie
- [ ] Émission configurée
- [ ] Appliqué
- [ ] Sauvegardé (Ctrl+S)

---

## ?? Gestion

| Action | Comment |
|--------|---------|
| **Sélectionner surface** | Clic dans la 3D (mode actif) |
| **Retirer texture** | Liste ? Sélectionner ? "Retirer" |
| **Tout effacer** | "Tout effacer" |
| **Modifier** | Re-sélectionner surface ? Appliquer |

---

## ?? Astuce pro

```
Pour un écran réaliste:
- Emission: Blanc légèrement bleuté
- Energy: 1.2-1.5
- Texture: Vidéo 1920x1080
- Loop: ?
```

---

*Guide complet : [DecorManager_MovieRendering_Guide.md](../Documentation/DecorManager_MovieRendering_Guide.md)*
