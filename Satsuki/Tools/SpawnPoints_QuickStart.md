# ?? Quick Start - Spawn Points

**Placement des points d'apparition en 5 minutes**

---

## ? Démarrage rapide

### 1?? Charger une scène (30 sec)

```
Godot ? Decor Manager dock
Chemin: res://Scenes/Locations/Restaurant.tscn
? "Charger la scene"
```

### 2?? Activer le mode (5 sec)

```
? "Mode placement actif"
Status devient vert ?
```

### 3?? Placer des points (2 min)

**Points debout (?? vert)** :
```
Type: Standard_Idle
? Cliquer dans la scène 3D (entrée, couloirs)
? Sphères vertes apparaissent
```

**Points assis (?? bleu)** :
```
Type: Seated_Idle  
? Cliquer sur les chaises/bancs
? Sphères bleues apparaissent
```

### 4?? Sauvegarder (10 sec)

```
? "Sauvegarder configuration JSON"
Fichier créé: Configs/Restaurant_config.json ?
```

---

## ?? Résultat

```json
{
  "ScenePath": "res://Scenes/Locations/Restaurant.tscn",
  "SceneName": "Restaurant",
  "SpawnPoints": [
    { "Position": { "x": 1.2, "y": 0, "z": 3.4 }, "Type": 0 },
    { "Position": { "x": -2.5, "y": 0, "z": 5.2 }, "Type": 1 }
  ]
}
```

---

## ?? Raccourcis

| Action | Comment |
|--------|---------|
| **Placer point** | Clic gauche dans la 3D |
| **Changer type** | Dropdown "Type" |
| **Supprimer** | Sélectionner + "Supprimer" |
| **Tout effacer** | "Tout effacer" |
| **Sauvegarder** | "Sauvegarder JSON" |

---

## ?? Types

- ?? **Standard_Idle** = Debout (entrée, couloirs, zones)
- ?? **Seated_Idle** = Assis (chaises, bancs, tables)

---

## ?? Fichiers

```
Configs/
??? Restaurant_config.json
??? Hall_config.json
??? [VotreScene]_config.json
```

---

## ? Checklist

- [ ] Scène chargée
- [ ] Mode actif ?
- [ ] Points placés (?? + ??)
- [ ] JSON sauvegardé
- [ ] Marqueurs visibles

---

*Guide complet : [DecorManager_SpawnPoints_Feature.md](../Documentation/DecorManager_SpawnPoints_Feature.md)*
