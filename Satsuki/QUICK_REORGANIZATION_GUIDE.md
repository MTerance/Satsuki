# ? Guide d'Exécution Rapide - Réorganisation Documentation

**Temps estimé** : 5 minutes  
**Difficulté** : Facile  
**Réversible** : Oui (backup automatique)

---

## ?? En 3 étapes

### 1?? Créer un backup (30 sec)

```powershell
cd "C:\Users\sshom\source\repos\Satsuki\Satsuki"
Copy-Item -Path "Documentation" -Destination "Documentation_BACKUP_$(Get-Date -Format 'yyyyMMdd_HHmmss')" -Recurse
```

? **Résultat** : Dossier `Documentation_BACKUP_20251122_HHMMSS` créé

---

### 2?? Exécuter le script (2 min)

```powershell
.\reorganize-documentation.ps1
```

? **Résultat** : 
- 8 dossiers créés
- 46 fichiers déplacés
- Rapport affiché

---

### 3?? Activer le nouveau README (1 min)

```powershell
# Sauvegarder ancien README
Move-Item "Documentation\README.md" "Documentation\README_OLD.md" -Force

# Activer nouveau README
Move-Item "Documentation\README_NEW.md" "Documentation\README.md" -Force
```

? **Résultat** : README.md structuré actif

---

## ?? Vérification (1 min)

### Vérifier la structure

```powershell
Get-ChildItem "Documentation" -Directory
```

**Attendu** :
```
01_Architecture
02_Features
03_Tools
04_Fixes
05_Systems
06_Guides
07_Reports
Archive
```

### Vérifier les fichiers déplacés

```powershell
Get-ChildItem "Documentation\01_Architecture" -Name
```

**Attendu** :
```
MainGameScene_Complete_Architecture.md
ServerArchitecture.md
ILocation_Interface.md
GETGAMESTATE_SYSTEM.md
```

---

## ? Si tout est OK

### Commit Git

```bash
git add Documentation/
git commit -m "docs: reorganize documentation structure"
git push origin sho/dev/createlobby
```

---

## ? Si problème

### Restaurer le backup

```powershell
# Supprimer Documentation actuel
Remove-Item "Documentation" -Recurse -Force

# Restaurer backup
Copy-Item -Path "Documentation_BACKUP_*" -Destination "Documentation" -Recurse
```

---

## ?? Résultat final

```
Documentation/
??? 01_Architecture/          ? 4 docs
??? 02_Features/              ? 6 docs
??? 03_Tools/                 ? 5 docs
??? 04_Fixes/                 ? 8 docs
??? 05_Systems/               ? 4 docs
??? 06_Guides/                ? 3 docs
??? 07_Reports/               ? 3 docs
??? Archive/                  ? 13 docs
??? README.md                 ? Nouveau
??? README_OLD.md             ? Ancien (backup)
??? REORGANIZATION_REPORT.md  ? Rapport
```

---

## ?? C'est fait !

**Navigation** : Ouvrir `Documentation/README.md`

**Recherche** : Utiliser les catégories 01-07

**Archive** : Consulter `Archive/` si besoin

---

*Temps total : 5 minutes*  
*Réorganisation : ? Terminée*  
*Documentation : ?? Structurée*
