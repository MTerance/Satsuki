# ?? Decor Manager Tool - Quick Start

## ?? Activation rapide

1. **Activer le plugin**
   ```
   Project ? Project Settings ? Plugins
   ? Cocher "Decor Manager"
   ```

2. **Ouvrir le dock**
   ```
   Le panneau "Decor Manager" apparaît à droite
   ```

---

## ?? Usage en 3 étapes

### 1?? Charger un décor

```
Chemin .tscn: res://Scenes/Locations/Restaurant.tscn
                        [Charger la scene]
```

### 2?? Éditer les caméras

```
Title_Camera3D (Trouvee) ?
Position: X: [4.61] Y: [6.13] Z: [58.77]
Rotation: X: [0] Y: [0] Z: [0]
                        [Appliquer]
```

### 3?? Sauvegarder

```
Ctrl + S pour sauvegarder la scène
```

---

## ?? Fonctionnalités principales

| Action | Description |
|--------|-------------|
| ?? **Charger** | Charge un fichier .tscn |
| ?? **Détecter** | Trouve les caméras automatiquement |
| ?? **Éditer** | Modifie position/rotation |
| ? **Créer** | Ajoute des caméras manquantes |
| ??? **Renommer** | Change le nom des caméras |

---

## ?? Caméras gérées

| Nom | Couleur | Usage |
|-----|---------|-------|
| **Title_Camera3D** | ?? Orange | Menu principal |
| **Lobby_Camera3D** | ?? Cyan | Sélection mode |
| **Game_Camera3D** | ?? Vert | Gameplay |

---

## ? Raccourcis

| Touche | Action |
|--------|--------|
| `...` | Ouvrir navigateur fichiers |
| `Charger` | Charger la scène |
| `Appliquer` | Appliquer changements caméra |
| `Creer` | Créer caméra manquante |
| `Ctrl+S` | Sauvegarder |

---

## ?? Problèmes courants

### Caméra non détectée
- ? Vérifier le nom exact : `Title_Camera3D`
- ? Type : `Camera3D` (pas Camera2D)
- ? Recharger la scène

### Changements non sauvegardés
- ? Cliquer "Appliquer" d'abord
- ? Puis `Ctrl+S` pour sauvegarder
- ? Vérifier l'astérisque (*) dans l'onglet

---

## ?? Documentation complète

Voir [DecorManagerTool_Guide.md](DecorManagerTool_Guide.md) pour :
- Guide détaillé
- Workflows complets
- Résolution de problèmes
- Extensibilité

---

*Version : 1.0*  
*Créé : 22/11/2025*
