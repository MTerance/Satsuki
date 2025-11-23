# ?? DecorManager - Points d'apparition des joueurs

**Date** : 22 novembre 2025  
**Fonctionnalité** : Placement interactif des spawn points avec sauvegarde JSON

---

## ?? Vue d'ensemble

Le DecorManager permet maintenant de définir des **points d'apparition pour les joueurs** directement en cliquant dans la scène 3D. Chaque point peut être de type **Standard_Idle** ou **Seated_Idle**, et toute la configuration est sauvegardée dans un fichier JSON.

---

## ? Nouvelles fonctionnalités

### 1. Mode placement interactif
- ? Checkbox pour activer/désactiver le mode placement
- ? Cliquez dans la scène 3D pour placer un point
- ? Marqueurs visuels (sphères vertes ou bleues)

### 2. Types de spawn points
- ?? **Standard_Idle** : Joueur debout (sphère verte)
- ?? **Seated_Idle** : Joueur assis (sphère bleue)

### 3. Gestion des points
- ? Liste des points enregistrés
- ? Suppression d'un point spécifique
- ? Effacement de tous les points
- ? Sauvegarde en JSON

### 4. Sauvegarde automatique
- ? Fichier JSON généré dans `Configs/`
- ? Nom : `[NomDeLaScene]_config.json`
- ? Chargement automatique au reload

---

## ?? Utilisation

### Étape 1 : Charger une scène

```
1. Ouvrir Godot
2. Activer le plugin "Decor Manager"
3. Dans le dock Decor Manager :
   - Saisir : res://Scenes/Locations/Restaurant.tscn
   - Cliquer : "Charger la scene"
```

### Étape 2 : Activer le mode placement

```
1. Cocher : ? "Mode placement actif"
2. Le status devient vert : "Mode placement actif - Cliquez dans la scene 3D"
```

### Étape 3 : Choisir le type de spawn

```
1. Dans le dropdown "Type:" choisir :
   - Standard_Idle (pour joueur debout) ??
   - Seated_Idle (pour joueur assis) ??
```

### Étape 4 : Placer les points

```
1. Cliquer dans la vue 3D de la scène
2. Un marqueur visuel apparaît (sphère verte ou bleue)
3. Le point est ajouté à la liste
4. Répéter pour chaque point désiré
```

### Étape 5 : Sauvegarder

```
1. Cliquer : "Sauvegarder configuration JSON"
2. Fichier créé : Configs/Restaurant_config.json
3. Status : "Configuration sauvegardee: Restaurant_config.json"
```

---

## ?? Interface utilisateur

```
??????????????????????????????????????
?  Points d'apparition des joueurs   ? (vert)
??????????????????????????????????????
?  ? Mode placement actif            ?
?     (cliquez dans la scene 3D)     ?
??????????????????????????????????????
?  Type: [Standard_Idle ?]           ?
??????????????????????????????????????
?  Points enregistres:               ?
?  ????????????????????????????????  ?
?  ? 0: Standard_Idle - (1.2, 0, 3)?  ?
?  ? 1: Seated_Idle - (-2, 0, 5)  ?  ?
?  ? 2: Standard_Idle - (4, 0, -1)?  ?
?  ????????????????????????????????  ?
??????????????????????????????????????
?  [Supprimer selectionne] [Tout...]?
?  [Sauvegarder configuration JSON]  ?
??????????????????????????????????????
```

---

## ?? Format du fichier JSON

### Exemple : `Restaurant_config.json`

```json
{
  "ScenePath": "res://Scenes/Locations/Restaurant.tscn",
  "SceneName": "Restaurant",
  "SpawnPoints": [
    {
      "Position": {
        "x": 1.234,
        "y": 0.0,
        "z": 3.456
      },
      "Type": 0,
      "Index": 0
    },
    {
      "Position": {
        "x": -2.5,
        "y": 0.0,
        "z": 5.2
      },
      "Type": 1,
      "Index": 1
    },
    {
      "Position": {
        "x": 4.1,
        "y": 0.0,
        "z": -1.3
      },
      "Type": 0,
      "Index": 2
    }
  ],
  "SavedAt": "2025-11-22T14:30:00Z"
}
```

### Structure des données

| Champ | Type | Description |
|-------|------|-------------|
| `ScenePath` | string | Chemin complet de la scène |
| `SceneName` | string | Nom de la scène (sans extension) |
| `SpawnPoints` | array | Liste des points d'apparition |
| `SavedAt` | DateTime | Date/heure de sauvegarde |

### Structure d'un SpawnPoint

| Champ | Type | Description |
|-------|------|-------------|
| `Position` | Vector3 | Position 3D (x, y, z) |
| `Type` | enum | 0 = Standard_Idle, 1 = Seated_Idle |
| `Index` | int | Numéro d'ordre du point |

---

## ?? Types de spawn points

### Standard_Idle (Type 0)

**Usage** : Joueur debout  
**Couleur** : ?? Vert  
**Animation** : Idle debout  

**Exemples d'utilisation** :
- Hall d'entrée
- Couloirs
- Zones de passage
- Près des comptoirs

### Seated_Idle (Type 1)

**Usage** : Joueur assis  
**Couleur** : ?? Bleu  
**Animation** : Idle assis  

**Exemples d'utilisation** :
- Chaises
- Bancs
- Tables
- Sièges de bar

---

## ?? Fonctionnalités techniques

### Détection du clic 3D

```csharp
public override int _Forward3DGuiInput(Camera3D camera, InputEvent @event)
{
    if (!_isSpawnPointMode) return Pass;
    
    if (@event is InputEventMouseButton mouseButton && mouseButton.Pressed)
    {
        var from = camera.ProjectRayOrigin(mouseButton.Position);
        var to = from + camera.ProjectRayNormal(mouseButton.Position) * 1000;
        
        var spaceState = camera.GetWorld3D().DirectSpaceState;
        var query = PhysicsRayQueryParameters3D.Create(from, to);
        var result = spaceState.IntersectRay(query);
        
        if (result.Count > 0)
        {
            var position = (Vector3)result["position"];
            AddSpawnPoint(position);
        }
    }
}
```

### Création du marqueur visuel

```csharp
private void CreateSpawnPointMarker(SpawnPointData spawnPoint)
{
    var marker = new MeshInstance3D();
    marker.Name = $"SpawnPoint_{spawnPoint.Index}_{spawnPoint.Type}";
    
    var sphereMesh = new SphereMesh();
    sphereMesh.Radius = 0.3f;
    
    var material = new StandardMaterial3D();
    material.AlbedoColor = spawnPoint.Type == Standard_Idle ? Green : Blue;
    material.EmissionEnabled = true;
    
    marker.GlobalPosition = spawnPoint.Position;
    _loadedScene.AddChild(marker);
}
```

### Chargement automatique

```csharp
private void LoadExistingConfiguration()
{
    var jsonPath = Path.Combine("res://", "Configs", $"{sceneName}_config.json");
    
    if (File.Exists(jsonPath))
    {
        var json = File.ReadAllText(jsonPath);
        var config = JsonSerializer.Deserialize<DecorConfiguration>(json);
        
        _spawnPoints.AddRange(config.SpawnPoints);
        
        foreach (var sp in _spawnPoints)
        {
            CreateSpawnPointMarker(sp);
        }
    }
}
```

---

## ?? Workflow complet

### Scénario : Configurer le Restaurant

```
1. Charger Restaurant.tscn
   ? Caméras détectées
   ? Configuration existante chargée (si existe)

2. Activer mode placement
   ? Status : Mode actif

3. Placer 3 points Standard_Idle (debout)
   ? Près de l'entrée : (1.5, 0, 3)
   ? Près du comptoir : (4, 0, -1)
   ? Dans le coin : (-2, 0, 5)

4. Changer type ? Seated_Idle

5. Placer 2 points Seated_Idle (assis)
   ? Chaise table 1 : (2, 0, 2)
   ? Chaise table 2 : (-3, 0, 4)

6. Vérifier la liste
   ? 5 points au total
   ? 3 verts, 2 bleus

7. Sauvegarder
   ? Restaurant_config.json créé
   ? Status : Configuration sauvegardee
```

---

## ?? Bonnes pratiques

### Placement des points

1. **Espacement** : Laisser au moins 1-2 mètres entre les points
2. **Hauteur** : Y = 0 pour le sol (ajusté automatiquement)
3. **Accessibilité** : Éviter les zones bloquées ou inaccessibles
4. **Visibilité** : Placer où les joueurs seront visibles

### Types de points

1. **Standard_Idle** :
   - Zones de circulation
   - Devant les objets interactifs
   - Points de rencontre

2. **Seated_Idle** :
   - Sur les chaises (bien centré)
   - Bancs (plusieurs points alignés)
   - Tables (autour de la table)

### Organisation

1. **Numérotation** : Les points sont numérotés automatiquement
2. **Groupage** : Garder les points similaires ensemble
3. **Documentation** : Noter l'usage de chaque zone dans un fichier séparé

---

## ?? Résolution de problèmes

### Le clic ne place pas de point

**Causes** :
- Mode placement non activé
- Clic sur une zone sans collision
- Scène 3D pas chargée

**Solutions** :
```
1. Vérifier que ? Mode placement est coché
2. Cliquer sur un objet avec collision (sol, murs, meubles)
3. Recharger la scène si nécessaire
```

### Les marqueurs ne s'affichent pas

**Causes** :
- Caméra trop éloignée
- Marqueurs hors du champ de vision
- Matériaux non appliqués

**Solutions** :
```
1. Zoomer sur la zone
2. Vérifier l'arborescence : SpawnPoint_0_Standard_Idle
3. Sélectionner le marqueur pour le voir
```

### La sauvegarde échoue

**Causes** :
- Dossier Configs inexistant
- Permissions d'écriture
- Chemin de scène invalide

**Solutions** :
```
1. Le dossier Configs/ est créé automatiquement
2. Vérifier les permissions du dossier projet
3. Recharger la scène pour définir le chemin
```

### Les points ne se rechargent pas

**Causes** :
- Nom de fichier incorrect
- JSON corrompu
- Conversion Vector3 échouée

**Solutions** :
```
1. Vérifier : Configs/[NomScene]_config.json existe
2. Valider le JSON dans un éditeur
3. Supprimer le JSON et recréer
```

---

## ?? Statistiques d'utilisation

### Limites recommandées

| Décor | Points Standard | Points Seated | Total |
|-------|-----------------|---------------|-------|
| **Restaurant** | 5-8 | 8-12 | 15-20 |
| **Hall** | 10-15 | 2-5 | 12-20 |
| **Salle de jeu** | 3-5 | 10-15 | 13-20 |
| **Extérieur** | 15-20 | 5-8 | 20-28 |

### Performance

- **Marqueurs** : Légers (sphères simples)
- **Fichier JSON** : < 10 KB pour 50 points
- **Chargement** : Instantané

---

## ?? Résumé

### Ce que vous pouvez faire maintenant

- ? Placer des spawn points en cliquant dans la 3D
- ? Choisir entre Standard (debout) et Seated (assis)
- ? Voir les marqueurs visuels (?? vert / ?? bleu)
- ? Gérer la liste (ajouter/supprimer)
- ? Sauvegarder en JSON automatiquement
- ? Charger la config existante au reload

### Fichiers générés

```
Satsuki/
??? Configs/
    ??? Restaurant_config.json
    ??? Hall_config.json
    ??? SalleDeJeu_config.json
```

### Prochaines étapes

1. Configurer chaque décor avec ses spawn points
2. Tester en jeu l'apparition des joueurs
3. Ajuster les positions si nécessaire
4. Documenter l'usage de chaque zone

---

*Date de création : 22 novembre 2025*  
*Version : 1.1*  
*Build : ? Réussi*
