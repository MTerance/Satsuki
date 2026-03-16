# ?? Decor Manager - Godot Addon

**Version** : 1.0  
**Godot** : 4.x  
**Projet** : Satsuki

---

## ?? Description

Addon Godot pour la gestion des décors, caméras et points d'apparition dans le projet Satsuki.

---

## ? Fonctionnalités

- ?? Chargement de scènes .tscn
- ?? Gestion des caméras (Title, Lobby, Game)
- ?? Placement de spawn points
- ??? Menu rendering sur surfaces 3D
- ?? Sauvegarde en configuration JSON

---

## ?? Structure

```
addons/decor_manager/
??? plugin.cfg                          # Configuration du plugin
??? DecorManagerTool.cs                 # Script principal
??? DecorManagerTool_MenuRendering.cs   # Extension menu rendering
??? LobbyInfoContainer.cs               # Conteneur info lobby
??? Scenes/
?   ??? control.tscn                    # Interface personnalisée
??? Assets/
?   ??? spawn_point_marker.png          # Marqueur spawn point
??? README.md                           # Ce fichier
```

---

## ?? Installation

1. Copier le dossier `decor_manager` dans `addons/`
2. Ouvrir Godot
3. Projet ? Paramètres du Projet ? Plugins
4. Activer "Decor Manager"

---

## ?? Documentation

Voir [DecorManagerTool_Guide.md](../../Documentation/DecorManagerTool_Guide.md)

---

## ?? Crédits

### Icônes

| Source | Auteur | Lien | Licence |
|--------|--------|------|---------|
| **Smashicons** | Smashicons | [https://smashicons.com/](https://smashicons.com/) | Voir site |

Les icônes utilisées dans cet addon (spawn_point_marker.png, etc.) proviennent de **Smashicons**.

### Développement

- **Équipe Satsuki** - Développement de l'addon
- **Godot Engine** - Moteur de jeu

---

## ?? Licence

Cet addon fait partie du projet Satsuki.

### Icônes tierces

Les icônes de **Smashicons** sont utilisées conformément à leur licence.
Veuillez consulter [https://smashicons.com/](https://smashicons.com/) pour les conditions d'utilisation.

---

## ?? Liens

- **Smashicons** : [https://smashicons.com/](https://smashicons.com/)
- **Godot Engine** : [https://godotengine.org/](https://godotengine.org/)
- **Projet Satsuki** : [https://github.com/MTerance/Satsuki](https://github.com/MTerance/Satsuki)

---

*© 2025 Satsuki Team*
