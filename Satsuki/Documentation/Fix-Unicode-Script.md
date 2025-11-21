# Script de maintenance Unicode

## ?? `fix-unicode.ps1`

Script PowerShell pour maintenir la conformité ASCII du code C# du projet Satsuki.

### ?? Objectif

Supprimer automatiquement :
- Les caractères accentués français (à, é, è, ê, ç, etc.)
- Les emojis dans les commentaires
- Tout en préservant les opérateurs C# (?, ??, etc.)

### ?? Utilisation

```powershell
# Depuis le répertoire racine du projet
.\fix-unicode.ps1
```

### ? Caractères corrigés

| Avant | Après | Type |
|-------|-------|------|
| à, â, ä | a | Voyelle |
| é, è, ê, ë | e | Voyelle |
| î, ï | i | Voyelle |
| ô, ö | o | Voyelle |
| ù, û, ü | u | Voyelle |
| ç | c | Consonne |
| ???????? | (supprimé) | Emojis |

### ?? Sortie du script

```
=== Correction Unicode pour Satsuki ===

Fichiers a analyser: 35

  [OK] LocationManager.cs
  [OK] Network.cs
  [OK] SingletonBase.cs

=== Resultat ===
Total: 3 fichier(s) corrige(s)

Verification recommandee:
  dotnet build Satsuki.csproj
```

### ?? Vérification post-correction

Après exécution, vérifiez toujours que le build fonctionne :

```powershell
dotnet build Satsuki.csproj
```

### ?? Avertissements

- ? **Safe** : Préserve tous les opérateurs C#
- ? **Testé** : Build réussi après correction
- ?? **Backup** : Utilisez Git pour revenir en arrière si nécessaire

### ?? Historique

- **Création** : 2024
- **Dernière vérification** : Build réussi, 0 erreur
- **Fichiers corrigés** : 30+ fichiers C#

### ?? Documentation associée

- `Documentation/Unicode_Audit_Report.md` - Rapport d'audit initial
- `Documentation/Unicode_Fix_Complete_Report.md` - Rapport final détaillé

---

**Note** : Ce script est uniquement nécessaire si de nouveaux fichiers avec des accents sont ajoutés au projet.
