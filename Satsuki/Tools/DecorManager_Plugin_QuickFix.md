# ? Quick Fix - DecorManager Plugin

**Erreur** : "Impossible de charger le script de l'extension"

---

## ?? Solution rapide (30 secondes)

### 1. Ouvrir le fichier

```
addons/decor_manager/plugin.cfg
```

### 2. Changer la ligne 7

**Avant** :
```cfg
script="decorManagerTool.cs"
```

**Après** :
```cfg
script="DecorManagerTool.cs"
```

### 3. Sauvegarder (Ctrl+S)

### 4. Redémarrer Godot

### 5. Activer le plugin

```
Projet ? Paramètres ? Plugins ? Decor Manager ?
```

---

## ? Résultat

- ? Plugin chargé
- ? Dock visible à droite
- ? Aucune erreur

---

## ?? Pourquoi ?

Le fichier s'appelle `DecorManagerTool.cs` (avec **D** majuscule), pas `decorManagerTool.cs` (avec **d** minuscule).

---

*Guide complet : [DecorManager_Plugin_Loading_Fix.md](../Documentation/DecorManager_Plugin_Loading_Fix.md)*
