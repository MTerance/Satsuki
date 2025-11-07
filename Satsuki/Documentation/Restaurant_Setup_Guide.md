# ??? Configuration Restaurant.tscn - Guide Complet

## ? Problème Identifié

```
ERROR: ? LocationManager: La scène 'res://Scenes/Locations/Restaurant.tscn' n'implémente pas ILocation
ERROR: ? MainGameScene: Échec de chargement de 'res://Scenes/Locations/Restaurant.tscn': Not an ILocation
ERROR: ? MainGameScene: Échec du chargement de Restaurant.tscn
```

**Cause** : Le fichier `Restaurant.tscn` n'a pas de script C# attaché qui hérite de `LocationModel`.

## ? Solution

### **Fichier Créé : `Restaurant.cs`**

Classe C# qui hérite de `LocationModel` et implémente `ILocation` :

```csharp
namespace Satsuki.Scenes.Locations
{
    public partial class Restaurant : LocationModel
    {
        public override string LocationName => "Restaurant";
        public override LocationType Type => LocationType.Social;
        public override string Description => "Restaurant principal - Environnement 3D pour le menu";
        
        // Overrides pour personnalisation...
    }
}
```

---

## ?? Étapes pour Attacher le Script dans Godot

### **1. Ouvrir Restaurant.tscn dans Godot**

1. Lancer Godot Engine
2. Dans le FileSystem, naviguer vers : `res://Scenes/Locations/`
3. Double-cliquer sur `Restaurant.tscn` pour l'ouvrir dans l'éditeur

---

### **2. Sélectionner le Node Racine**

1. Dans la Scene Tree (arbre de scène), cliquer sur le **node racine** de Restaurant
   - Généralement nommé `Restaurant` ou `Node3D`
2. Ce node racine doit être de type **Node3D** (ou un type compatible)

---

### **3. Attacher le Script C#**

#### **Méthode A : Via l'Inspector**

1. Avec le node racine sélectionné, aller dans l'**Inspector** (panneau de droite)
2. Chercher la section **Script**
3. Cliquer sur le bouton **[??]** à côté de "Script"
4. Dans le dialogue qui s'ouvre :
   - **Script Path** : Cliquer sur "Load" et naviguer vers `res://Scenes/Locations/Restaurant.cs`
   - Ou taper directement : `res://Scenes/Locations/Restaurant.cs`
5. Cliquer sur **Load**

#### **Méthode B : Drag & Drop**

1. Dans le FileSystem, localiser `Restaurant.cs`
2. Glisser-déposer `Restaurant.cs` sur le **node racine** dans la Scene Tree
3. Godot attachera automatiquement le script

#### **Méthode C : Via le Menu Contextuel**

1. Clic droit sur le **node racine** dans la Scene Tree
2. Sélectionner **Attach Script**
3. Dans le dialogue :
   - **Template** : Laisser "Empty"
   - **Path** : Changer vers `res://Scenes/Locations/Restaurant.cs`
   - **Language** : C#
4. Cliquer sur **Load** (ne pas "Create", car le fichier existe déjà)

---

### **4. Vérifier l'Attachement**

1. Le node racine devrait maintenant avoir une **icône de script** ?? à côté de son nom
2. Dans l'Inspector, la section **Script** devrait afficher :
   ```
   Script: res://Scenes/Locations/Restaurant.cs
   ```
3. Cliquer sur le script dans l'Inspector pour l'ouvrir et vérifier qu'il s'agit bien de `Restaurant.cs`

---

### **5. Configurer le Type du Node (Si Nécessaire)**

Pour que `Restaurant.cs` fonctionne correctement, le node racine **doit être de type Node3D** (ou compatible), car `LocationModel` hérite de `Node3D`.

#### **Vérifier le Type**

1. Sélectionner le node racine
2. Dans l'Inspector, vérifier le **type** en haut
3. Si ce n'est pas **Node3D** :
   - Clic droit sur le node ? **Change Type**
   - Chercher et sélectionner **Node3D**
   - Confirmer

---

### **6. Sauvegarder la Scène**

1. **Ctrl+S** ou **File ? Save Scene**
2. Vérifier que le fichier `Restaurant.tscn` a été modifié (astérisque * disparaît)

---

### **7. Vérifier dans le Code .tscn**

Optionnel : Vérifier que le script est bien attaché en ouvrant `Restaurant.tscn` dans un éditeur de texte.

Le fichier devrait contenir une ligne comme :

```gdscript
[node name="Restaurant" type="Node3D"]
script = ExtResource("1_xxxxx")  # ou un ID similaire

# Plus bas dans le fichier
[ext_resource type="Script" path="res://Scenes/Locations/Restaurant.cs" id="1_xxxxx"]
```

---

## ?? Structure Finale de Restaurant.tscn

```
Restaurant (Node3D) ?? Restaurant.cs
    ??? Camera3D
    ??? DirectionalLight3D
    ??? Floor (MeshInstance3D)
    ??? Table (MeshInstance3D)
    ??? Chair1 (MeshInstance3D)
    ??? Chair2 (MeshInstance3D)
    ??? MediaScreen (MeshInstance3D)  [Optionnel]
    ??? SpawnMarker1 (Marker3D)       [Optionnel]
```

**Essentiel** :
- ? Le node racine est de type **Node3D**
- ? Le script **Restaurant.cs** est attaché au node racine
- ? La scène est sauvegardée

---

## ?? Test de Vérification

### **Dans Godot**

1. Sélectionner le node Restaurant
2. Vérifier que l'Inspector affiche :
   ```
   Node: Restaurant
   Type: Node3D
   Script: res://Scenes/Locations/Restaurant.cs
   ```

### **Au Runtime (Jeu)**

Lors du lancement du jeu, les logs devraient afficher :

```
??? Restaurant: Initialisation de la location...
??? LocationModel: Initialisation de Restaurant...
?? Restaurant: Initialisation...
?? Restaurant: Initialisation des points de spawn...
?? Restaurant: Initialisation des sorties...
?? Restaurant: Chargement...
?? Restaurant: Chargement des ressources...
? Restaurant: Activation...
? Restaurant: Chargé
? Restaurant: Location initialisée
```

Et plus d'erreur **"Not an ILocation"** !

---

## ?? Propriétés de Restaurant.cs

### **Overrides Disponibles**

```csharp
public partial class Restaurant : LocationModel
{
    // Propriétés
    public override string LocationName => "Restaurant";
    public override LocationType Type => LocationType.Social;
    public override string Description => "Restaurant principal";
    
    // Navigation
    public override Vector3[] GetSpawnPoints() { }
    public override Vector3 GetDefaultSpawnPoint() { }
    public override Dictionary<string, string> GetExits() { }
    
    // Lifecycle
    protected override void InitializeSpawnPoints() { }
    protected override void InitializeExits() { }
    protected override void LoadResources() { }
    
    // Players
    protected override void OnPlayerEnterSpecific(string playerId) { }
    protected override void OnPlayerExitSpecific(string playerId) { }
    
    // Configuration
    protected override void ApplyAmbianceSettings(object settings) { }
    protected override void ApplyGameplaySettings(object settings) { }
}
```

---

## ?? Héritage et Interfaces

```
Restaurant.cs
    ? hérite de
LocationModel
    ? hérite de
Node3D (Godot)
    
Restaurant.cs
    ? implémente (via LocationModel)
ILocation
IScene
```

**Résultat** :
- ? `Restaurant` est un **Node3D** (compatible Godot)
- ? `Restaurant` implémente **ILocation** (requis par LocationManager)
- ? `Restaurant` implémente **IScene** (compatible MainGameScene)

---

## ?? Workflow Complet

### **1. Créer la Scène Godot**

1. Dans Godot : **Scene ? New Scene**
2. Ajouter un **Node3D** comme root
3. Renommer en "Restaurant"
4. Ajouter les éléments 3D (caméra, lumières, meshes)
5. Sauvegarder : `res://Scenes/Locations/Restaurant.tscn`

### **2. Créer le Script C#**

1. Dans Visual Studio ou Rider : créer `Scenes/Locations/Restaurant.cs`
2. Hériter de `LocationModel`
3. Override les propriétés et méthodes nécessaires
4. Build le projet C#

### **3. Attacher le Script**

1. Dans Godot : ouvrir `Restaurant.tscn`
2. Sélectionner le node racine
3. Attacher `Restaurant.cs` via l'Inspector
4. Sauvegarder la scène

### **4. Tester**

1. Lancer le jeu
2. Vérifier les logs
3. Confirmer que Restaurant est chargé sans erreur

---

## ? Validation

### **Checklist**

- ? `Restaurant.cs` créé et compile
- ? `Restaurant` hérite de `LocationModel`
- ? `Restaurant.tscn` existe avec un Node3D racine
- ? `Restaurant.cs` attaché au node racine
- ? Scène sauvegardée
- ? Pas d'erreur "Not an ILocation" au runtime

### **Tests Fonctionnels**

```csharp
// Test de chargement
var manager = LocationManager.Instance;
bool success = manager.LoadLocationFromScene("res://Scenes/Locations/Restaurant.tscn");

// Devrait retourner true
Assert.IsTrue(success);

// Vérifier la location chargée
Assert.IsNotNull(manager.CurrentLocation);
Assert.AreEqual("Restaurant", manager.CurrentLocation.LocationName);
Assert.AreEqual(LocationType.Social, manager.CurrentLocation.Type);
```

---

## ?? Utilisation dans MainGameScene

Une fois configuré, Restaurant sera automatiquement chargé lors du chargement de Title :

```csharp
// Dans LoadTitleSpecialized()
LoadTitleScene();
    ?
CallDeferred(LoadRestaurantLocation);
    ?
LocationManager.LoadLocationFromScene("Restaurant.tscn");
    ?
? Restaurant chargé dans CurrentLocation
```

**Résultat** :
- Title dans **CurrentScene** (UI)
- Restaurant dans **CurrentLocation** (3D Environment)

---

## ?? Conclusion

Après avoir attaché `Restaurant.cs` à `Restaurant.tscn` dans Godot, le LocationManager pourra charger la scène correctement et Restaurant apparaîtra comme environnement 3D derrière le menu Title ! ????

**N'oubliez pas** : Cette opération doit être faite **dans l'éditeur Godot**, pas dans le code C#. Le fichier `.tscn` doit référencer le script `.cs` pour que Godot instancie la bonne classe au runtime.
