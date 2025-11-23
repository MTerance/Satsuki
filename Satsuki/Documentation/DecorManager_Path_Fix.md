# ?? Solution au problème de chemin dupliqué

**Erreur** : `Impossible de charger le script de l'extension depuis le chemin : 'res://addons/decor_manager/res://addons/decor_manager/DecorManagerTool.cs'`

---

## ? Solutions à essayer

### Solution 1 : Nettoyer le cache Godot

1. **Fermer Godot complètement**

2. **Supprimer le cache**
   ```
   C:\Users\sshom\source\repos\Satsuki\Satsuki\.godot\
   ? Supprimer ce dossier complet
   ```

3. **Rouvrir Godot**
   - Le cache sera régénéré automatiquement

4. **Réactiver le plugin**
   ```
   Project ? Project Settings ? Plugins
   ? Cocher "Decor Manager"
   ```

---

### Solution 2 : Vérifier le fichier plugin.cfg

Le fichier doit contenir **exactement** :

```ini
[plugin]

name="Decor Manager"
description="Outil de gestion des decors et cameras pour Satsuki"
author="Satsuki Team"
version="1.0"
script="res://addons/decor_manager/DecorManagerTool.cs"
```

**Points importants** :
- ? Ligne vide après `[plugin]`
- ? Pas d'espaces avant/après les `=`
- ? Guillemets doubles `"` (pas simples `'`)
- ? Chemin commence par `res://`
- ? **PAS de duplication** dans le chemin

---

### Solution 3 : Réinstaller le plugin

1. **Désactiver le plugin**
   ```
   Project Settings ? Plugins ? Décocher "Decor Manager"
   ```

2. **Supprimer le dossier**
   ```
   Satsuki/addons/decor_manager/
   ? Supprimer complètement
   ```

3. **Recréer la structure**
   ```
   addons/
   ??? decor_manager/
       ??? plugin.cfg
       ??? DecorManagerTool.cs
   ```

4. **Recopier les fichiers**
   - Plugin.cfg avec contenu correct
   - DecorManagerTool.cs

5. **Redémarrer Godot**

6. **Activer le plugin**

---

### Solution 4 : Vérifier les chemins Windows

Le problème pourrait venir de chemins Windows vs chemins Godot.

**Vérifier que le fichier existe** :
```powershell
Test-Path "C:\Users\sshom\source\repos\Satsuki\Satsuki\addons\decor_manager\DecorManagerTool.cs"
# Doit retourner : True
```

**Vérifier le contenu de plugin.cfg** :
```powershell
Get-Content "C:\Users\sshom\source\repos\Satsuki\Satsuki\addons\decor_manager\plugin.cfg"
```

---

### Solution 5 : Recréer plugin.cfg manuellement

1. **Supprimer** `plugin.cfg`

2. **Créer un nouveau fichier** avec un éditeur de texte (Notepad++)

3. **Copier exactement** :
   ```ini
   [plugin]

   name="Decor Manager"
   description="Outil de gestion des decors et cameras pour Satsuki"
   author="Satsuki Team"
   version="1.0"
   script="res://addons/decor_manager/DecorManagerTool.cs"
   ```

4. **Sauvegarder en UTF-8** (pas UTF-8 BOM)

5. **Redémarrer Godot**

---

## ?? Diagnostics

### Vérifier la structure
```
addons/
??? decor_manager/
    ??? plugin.cfg           ? Doit exister
    ??? DecorManagerTool.cs  ? Doit exister
```

### Vérifier le contenu de plugin.cfg
```powershell
# Dans PowerShell
cd "C:\Users\sshom\source\repos\Satsuki\Satsuki"
Get-Content "addons\decor_manager\plugin.cfg"
```

**Résultat attendu** :
```
[plugin]

name="Decor Manager"
description="Outil de gestion des decors et cameras pour Satsuki"
author="Satsuki Team"
version="1.0"
script="res://addons/decor_manager/DecorManagerTool.cs"
```

### Vérifier que DecorManagerTool.cs compile
```powershell
# Dans Visual Studio
Build ? Rebuild Solution
# Doit afficher : Build succeeded (0 errors)
```

---

## ?? Problèmes courants

### Problème 1 : Chemin dupliqué
```
? script="res://addons/decor_manager/res://addons/..."
? script="res://addons/decor_manager/DecorManagerTool.cs"
```

### Problème 2 : Mauvais encodage
```
Plugin.cfg doit être en UTF-8 (sans BOM)
Pas en UTF-16 ou ANSI
```

### Problème 3 : Ligne vide manquante
```
[plugin]
        ? Cette ligne vide est OBLIGATOIRE
name="..."
```

### Problème 4 : Cache Godot corrompu
```
Solution : Supprimer .godot/ et redémarrer
```

---

## ?? Checklist de résolution

- [ ] Fermer Godot
- [ ] Supprimer `.godot/` folder
- [ ] Vérifier `plugin.cfg` correct
- [ ] Vérifier `DecorManagerTool.cs` existe
- [ ] Recompiler le projet (Build ? Rebuild)
- [ ] Rouvrir Godot
- [ ] Activer le plugin
- [ ] Vérifier logs console

---

## ?? Solution recommandée

**Étapes à suivre dans l'ordre** :

1. **Fermer Godot**

2. **Nettoyer**
   ```powershell
   cd "C:\Users\sshom\source\repos\Satsuki\Satsuki"
   Remove-Item -Recurse -Force ".godot"
   ```

3. **Vérifier plugin.cfg**
   ```powershell
   Get-Content "addons\decor_manager\plugin.cfg"
   # Vérifier que le chemin est correct
   ```

4. **Recompiler**
   ```
   Visual Studio ? Build ? Rebuild Solution
   ```

5. **Rouvrir Godot**

6. **Activer plugin**
   ```
   Project Settings ? Plugins ? Activer "Decor Manager"
   ```

7. **Vérifier**
   ```
   - Aucun message d'erreur
   - Dock "Decor Manager" visible
   - Console : "DecorManagerTool: Initialisation..."
   ```

---

## ?? Si rien ne fonctionne

**Dernière solution** : Réinstallation complète

1. Sauvegarder `DecorManagerTool.cs`
2. Supprimer `addons/decor_manager/`
3. Recréer le dossier
4. Copier les fichiers
5. Redémarrer Godot

---

*Date : 22 novembre 2025*  
*Problème : Chemin dupliqué dans plugin*  
*Status : Solutions fournies*
