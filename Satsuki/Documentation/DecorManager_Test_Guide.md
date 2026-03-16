# ? DecorManager - Guide de test après correction

**Date** : 22 novembre 2025  
**Version** : 1.0 (Corrigée)

---

## ?? Étapes de test

### 1?? Réactiver le plugin

1. **Désactiver** (si déjà activé)
   ```
   Project ? Project Settings ? Plugins
   ? Décocher "Decor Manager"
   ? OK
   ```

2. **Fermer Godot complètement**
   ```
   Fichier ? Quitter
   ```

3. **Rouvrir Godot**
   ```
   Ouvrir le projet Satsuki
   ```

4. **Activer le plugin**
   ```
   Project ? Project Settings ? Plugins
   ? Cocher "Decor Manager"
   ? OK
   ```

### Résultat attendu
- ? Aucun message d'erreur
- ? Le dock "Decor Manager" apparaît à droite
- ? Console affiche : "DecorManagerTool: Initialisation..."

---

### 2?? Vérifier l'interface

**Ce que vous devez voir** :

```
???????????????????????????????
?  DECOR MANAGER              ?
???????????????????????????????
?  Charger une scene          ?
?  Chemin .tscn: [_________] ?
?  [Charger la scene]         ?
???????????????????????????????
?  Status: Aucune scene...    ?
???????????????????????????????
?  Title_Camera3D (Non...)    ?
?  [Creer]                    ?
???????????????????????????????
?  Lobby_Camera3D (Non...)    ?
?  [Creer]                    ?
???????????????????????????????
?  Game_Camera3D (Non...)     ?
?  [Creer]                    ?
???????????????????????????????
```

### Vérifications
- [ ] Titre "DECOR MANAGER" visible
- [ ] Champ de saisie présent
- [ ] Bouton "..." (browse) visible
- [ ] Bouton "Charger la scene" visible
- [ ] 3 sections de caméras visibles
- [ ] Tous les boutons "Creer" visibles

---

### 3?? Tester le chargement d'une scène

1. **Saisir le chemin**
   ```
   Chemin .tscn: res://Scenes/Locations/Restaurant.tscn
   ```

2. **Cliquer "Charger la scene"**

3. **Vérifier les logs**
   ```
   Status: Scene chargee: res://Scenes/Locations/Restaurant.tscn
   Camera trouvee: Title_Camera3D
   Camera trouvee: Lobby_Camera3D
   ```

4. **Vérifier l'interface**
   ```
   Title_Camera3D (Trouvee) ? Vert
   Position: X: [4.61] Y: [6.13] Z: [58.77]
   [Appliquer] ? Activé
   ```

### Checklist
- [ ] Status affiche "Scene chargee" en vert
- [ ] Title_Camera3D affiche "(Trouvee)" en vert
- [ ] Lobby_Camera3D affiche "(Trouvee)" en vert
- [ ] Positions affichées correctement
- [ ] Boutons "Appliquer" activés
- [ ] Boutons "Creer" masqués

---

### 4?? Tester la modification d'une caméra

1. **Sélectionner Title_Camera3D**

2. **Modifier la position Y**
   ```
   Y: [6.13] ? [8.0]
   ```

3. **Cliquer "Appliquer"**

4. **Vérifier**
   ```
   Status: Camera Title_Camera3D mise a jour ?
   ```

5. **Dans l'arborescence Godot**
   ```
   Restaurant ? Title_Camera3D
   ? Vérifier Transform : Y = 8.0
   ```

### Checklist
- [ ] Status affiche "mise a jour" en vert
- [ ] Scène marquée comme modifiée (*)
- [ ] Position Y changée dans l'éditeur
- [ ] Caméra toujours sélectionnable

---

### 5?? Tester la création d'une caméra

1. **Si Game_Camera3D n'existe pas**
   ```
   Game_Camera3D (Non trouvee) ? Gris
   [Creer] ? Visible
   ```

2. **Cliquer "Creer"**

3. **Vérifier**
   ```
   Status: Camera Game_Camera3D creee ?
   Game_Camera3D (Trouvee) ? Vert
   [Appliquer] ? Activé
   ```

4. **Dans l'arborescence**
   ```
   Restaurant ? Game_Camera3D ? Nouveau nœud
   ```

### Checklist
- [ ] Status affiche "creee" en vert
- [ ] Panel passe de "Non trouvee" à "Trouvee"
- [ ] Bouton "Creer" masqué
- [ ] Bouton "Appliquer" visible
- [ ] Caméra ajoutée à l'arborescence

---

### 6?? Tester le bouton Browse

1. **Cliquer sur "..."**

2. **Vérifier**
   ```
   EditorFileDialog s'ouvre
   Filtre : *.tscn
   ```

3. **Naviguer vers une scène**
   ```
   Scenes ? Locations ? Restaurant.tscn
   ```

4. **Sélectionner**

5. **Vérifier**
   ```
   Chemin rempli automatiquement
   res://Scenes/Locations/Restaurant.tscn
   ```

### Checklist
- [ ] Dialogue de fichiers s'ouvre
- [ ] Seuls les .tscn visibles
- [ ] Chemin inséré après sélection
- [ ] Bouton "Charger" activé

---

## ?? Tests d'erreurs

### Test 1 : Chemin vide
```
1. Vider le champ "Chemin .tscn"
2. Cliquer "Charger la scene"
3. Vérifier : Status "Erreur: Chemin vide" (rouge)
```

### Test 2 : Fichier inexistant
```
1. Saisir : res://inexistant.tscn
2. Cliquer "Charger la scene"
3. Vérifier : Status "Erreur: Fichier introuvable" (rouge)
```

### Test 3 : Extension incorrecte
```
1. Saisir : res://Scenes/Title.cs
2. Cliquer "Charger la scene"
3. Vérifier : Erreur de chargement
```

---

## ?? Tableau de validation

| Test | Description | Status |
|------|-------------|--------|
| 1 | Activation plugin | ? À tester |
| 2 | Interface visible | ? À tester |
| 3 | Chargement .tscn | ? À tester |
| 4 | Détection caméras | ? À tester |
| 5 | Modification position | ? À tester |
| 6 | Création caméra | ? À tester |
| 7 | Bouton browse | ? À tester |
| 8 | Sauvegarde scène | ? À tester |
| 9 | Erreur chemin vide | ? À tester |
| 10 | Erreur fichier absent | ? À tester |

---

## ? Critères de succès

Le plugin est considéré comme fonctionnel si :

- [x] ? Build C# réussi (0 erreur)
- [ ] ? Plugin s'active sans erreur
- [ ] ? Dock visible dans l'éditeur
- [ ] ? Chargement .tscn fonctionne
- [ ] ? Détection des 3 caméras OK
- [ ] ? Modification de position fonctionne
- [ ] ? Création de caméra fonctionne
- [ ] ? Sauvegarde marque la scène (*)
- [ ] ? Messages d'erreur clairs
- [ ] ? Aucun crash

---

## ?? En cas de problème

### Plugin ne s'active pas
```
1. Vérifier que le fichier existe :
   addons/decor_manager/DecorManagerTool.cs
2. Vérifier plugin.cfg :
   script="res://addons/decor_manager/DecorManagerTool.cs"
3. Recompiler : dotnet build
4. Redémarrer Godot
```

### Dock n'apparaît pas
```
1. Désactiver puis réactiver le plugin
2. Fermer et rouvrir Godot
3. Vérifier les logs de console
4. Vérifier EditorPlugin.AddControlToDock() appelé
```

### Caméras non détectées
```
1. Vérifier les noms exacts :
   - Title_Camera3D
   - Lobby_Camera3D
   - Game_Camera3D
2. Vérifier le type : Camera3D (pas Camera2D)
3. Vérifier que la scène est chargée
4. Observer logs : "Camera trouvee: ..."
```

### Erreur de compilation
```
1. Vérifier using Godot; en haut du fichier
2. Vérifier #if TOOLS ... #endif
3. Build ? Rebuild Solution
4. Nettoyer et recompiler
```

---

## ?? Notes de test

### Environnement
- Godot version : 4.x
- .NET version : 8.0
- OS : Windows/Linux/Mac

### Scènes de test recommandées
1. `res://Scenes/Locations/Restaurant.tscn` (complet)
2. Créer une scène test avec 1 seule caméra
3. Créer une scène test sans caméra

### Données de test
```
Position test : (10.5, 5.0, 20.3)
Rotation test : (15, 45, 0) degrés
Nom test : TestCamera_3D
```

---

## ?? Validation finale

Une fois tous les tests passés :

1. **Créer un commit Git**
   ```bash
   git add addons/decor_manager/
   git commit -m "fix: Correction chemin DecorManager plugin"
   ```

2. **Documenter dans README**
   ```markdown
   ## Outils
   - DecorManager : Outil de gestion des décors ? Fonctionnel
   ```

3. **Tester en conditions réelles**
   ```
   - Éditer plusieurs scènes
   - Créer de nouvelles caméras
   - Modifier des décors existants
   ```

---

*Date : 22 novembre 2025*  
*Version testée : 1.0*  
*Status : ? Prêt pour tests*
