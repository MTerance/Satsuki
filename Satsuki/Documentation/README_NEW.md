# ?? Documentation Satsuki - Index Organisé

**Dernière mise à jour** : 22 novembre 2025  
**Version** : 2.0 (Réorganisée)

---

## ?? Structure de la Documentation

```
Documentation/
??? 01_Architecture/      # Architecture système et interfaces
??? 02_Features/          # Fonctionnalités du jeu
??? 03_Tools/             # Outils et utilitaires
??? 04_Fixes/             # Corrections et solutions
??? 05_Systems/           # Systèmes techniques
??? 06_Guides/            # Guides d'implémentation
??? 07_Reports/           # Rapports et analyses
??? Archive/              # Documentation obsolète
??? README.md             # Ce fichier
```

---

## ??? 01 - Architecture

Documentation de l'architecture système et des interfaces principales.

| Document | Description |
|----------|-------------|
| [MainGameScene_Complete_Architecture.md](01_Architecture/MainGameScene_Complete_Architecture.md) | Architecture complète de la scène principale |
| [ServerArchitecture.md](01_Architecture/ServerArchitecture.md) | Architecture du serveur réseau |
| [ILocation_Interface.md](01_Architecture/ILocation_Interface.md) | Interface des locations |
| [GETGAMESTATE_SYSTEM.md](01_Architecture/GETGAMESTATE_SYSTEM.md) | Système d'état du jeu |

---

## ? 02 - Features

Fonctionnalités et systèmes de gameplay.

### Decor Manager

| Document | Description |
|----------|-------------|
| [DecorManager_SpawnPoints_Feature.md](02_Features/DecorManager_SpawnPoints_Feature.md) | Système de placement des spawn points |
| [DecorManager_MenuRendering_Guide.md](02_Features/DecorManager_MenuRendering_Guide.md) | Affichage des menus UI sur surfaces 3D |

### Caméras

| Document | Description |
|----------|-------------|
| [Camera_Context_System.md](02_Features/Camera_Context_System.md) | Système de contexte caméra |

### Crédits

| Document | Description |
|----------|-------------|
| [Credits_AutoLoad.md](02_Features/Credits_AutoLoad.md) | Système de chargement automatique |
| [CREDITS_ISCENE_IMPLEMENTATION.md](02_Features/CREDITS_ISCENE_IMPLEMENTATION.md) | Implémentation IScene |
| [CREDITS_SCENARIO.md](02_Features/CREDITS_SCENARIO.md) | Scénario des crédits |

---

## ??? 03 - Tools

Outils de développement et utilitaires.

### Decor Manager Tool

| Document | Description |
|----------|-------------|
| [DecorManagerTool_Guide.md](03_Tools/DecorManagerTool_Guide.md) | Guide complet de l'outil |
| [DecorManagerTool_Summary.md](03_Tools/DecorManagerTool_Summary.md) | Résumé de l'outil |

### Decor Loader

| Document | Description |
|----------|-------------|
| [DecorLoader_Guide.md](03_Tools/DecorLoader_Guide.md) | Guide d'utilisation |
| [DecorLoader_Summary.md](03_Tools/DecorLoader_Summary.md) | Résumé fonctionnel |

### Location Manager

| Document | Description |
|----------|-------------|
| [LocationManager.md](03_Tools/LocationManager.md) | Gestionnaire de locations |

### Quick Start (dans Tools/)

| Document | Description |
|----------|-------------|
| [../Tools/DecorManager_Plugin_QuickFix.md](../Tools/DecorManager_Plugin_QuickFix.md) | Fix rapide plugin |
| [../Tools/SpawnPoints_QuickStart.md](../Tools/SpawnPoints_QuickStart.md) | Démarrage rapide spawn points |
| [../Tools/MenuRendering_QuickStart.md](../Tools/MenuRendering_QuickStart.md) | Démarrage rapide menu rendering |
| [../Tools/DecorLoader_QuickStart.md](../Tools/DecorLoader_QuickStart.md) | Démarrage rapide decor loader |

---

## ?? 04 - Fixes

Solutions aux problèmes et corrections de bugs.

### Decor Manager

| Document | Description |
|----------|-------------|
| [DecorManager_Plugin_Loading_Fix.md](04_Fixes/DecorManager_Plugin_Loading_Fix.md) | Fix erreur chargement plugin |
| [DecorManager_Final_Solution.md](04_Fixes/DecorManager_Final_Solution.md) | Solution finale problèmes |

### UI & Display

| Document | Description |
|----------|-------------|
| [Application_Close_Fix.md](04_Fixes/Application_Close_Fix.md) | Fix fermeture application |
| [SplashScreen_Fade_Fix.md](04_Fixes/SplashScreen_Fade_Fix.md) | Fix animation fade splash screen |
| [Title_Menu_Display_Fix.md](04_Fixes/Title_Menu_Display_Fix.md) | Fix affichage menu titre |

### Caméras

| Document | Description |
|----------|-------------|
| [Camera_System_Improvement.md](04_Fixes/Camera_System_Improvement.md) | Améliorations système caméra |
| [Title_Camera_Activation.md](04_Fixes/Title_Camera_Activation.md) | Fix activation caméra titre |

### Encoding

| Document | Description |
|----------|-------------|
| [Unicode_Fix_Complete_Report.md](04_Fixes/Unicode_Fix_Complete_Report.md) | Rapport complet fix Unicode |

---

## ?? 05 - Systems

Systèmes techniques et fonctionnels.

| Document | Description |
|----------|-------------|
| [CLIENT_TYPE_AUTHENTICATION.md](05_Systems/CLIENT_TYPE_AUTHENTICATION.md) | Authentification par type client |
| [CryptageSystem.md](05_Systems/CryptageSystem.md) | Système de cryptage |
| [LocationManager_Integration.md](05_Systems/LocationManager_Integration.md) | Intégration location manager |
| [LocationManager_Resume.md](05_Systems/LocationManager_Resume.md) | Résumé location manager |

---

## ?? 06 - Guides

Guides d'implémentation et tutoriels.

| Document | Description |
|----------|-------------|
| [MainMenu_Complete_Implementation.md](06_Guides/MainMenu_Complete_Implementation.md) | Implémentation complète MainMenu |
| [Credits_Title_Navigation.md](06_Guides/Credits_Title_Navigation.md) | Navigation Credits/Title |
| [DecorLoader_MainGameScene_Example.md](06_Guides/DecorLoader_MainGameScene_Example.md) | Exemple d'intégration |

---

## ?? 07 - Reports

Rapports de maintenance et analyses.

| Document | Description |
|----------|-------------|
| [Cleanup_Obsolete_Docs_Report.md](07_Reports/Cleanup_Obsolete_Docs_Report.md) | Rapport nettoyage docs obsolètes |
| [Cleanup_Scripts_Report.md](07_Reports/Cleanup_Scripts_Report.md) | Rapport nettoyage scripts |
| [Documentation_Cleanup_Report.md](07_Reports/Documentation_Cleanup_Report.md) | Rapport nettoyage documentation |

---

## ??? Archive

Documentation obsolète conservée pour référence historique.

<details>
<summary>Cliquez pour voir la liste</summary>

| Document | Raison archivage |
|----------|------------------|
| DecorManager_Fix.md | Remplacé par Final_Solution |
| DecorManager_MovieRendering_*.md | Renommé en MenuRendering |
| DecorManager_Path_Fix.md | Problème résolu |
| Restaurant_*.md | Anciennes versions |
| SplashScreen_Debug_Guide.md | Debug temporaire |
| SubViewport_Fix.md | Intégré au code |
| Title_LobbyEx_Integration.md | Version obsolète |

</details>

---

## ?? Recherche rapide

### Par composant

- **Decor Manager** : [02_Features](02_Features/), [03_Tools](03_Tools/), [04_Fixes](04_Fixes/)
- **Caméras** : [02_Features](02_Features/), [04_Fixes](04_Fixes/)
- **Locations** : [01_Architecture](01_Architecture/), [03_Tools](03_Tools/), [05_Systems](05_Systems/)
- **UI/Menus** : [02_Features](02_Features/), [04_Fixes](04_Fixes/), [06_Guides](06_Guides/)
- **Réseau** : [01_Architecture](01_Architecture/), [05_Systems](05_Systems/)

### Par type

- **Guides complets** : [03_Tools](03_Tools/), [06_Guides](06_Guides/)
- **Fixes** : [04_Fixes](04_Fixes/)
- **Quick Start** : [../Tools/](../Tools/)
- **Architecture** : [01_Architecture](01_Architecture/)

---

## ?? Documentation externe

### Networks/

| Document | Description |
|----------|-------------|
| [Networks/README_Encryption.md](../Networks/README_Encryption.md) | Système de cryptage réseau |
| [Networks/README_MessageReceiver.md](../Networks/README_MessageReceiver.md) | Réception de messages |
| [Networks/README_MessageSystem.md](../Networks/README_MessageSystem.md) | Système de messagerie |

### Interfaces/

| Document | Description |
|----------|-------------|
| [Interfaces/README.md](../Interfaces/README.md) | Documentation des interfaces |
| [Interfaces/SUMMARY.md](../Interfaces/SUMMARY.md) | Résumé des interfaces |

---

## ?? Démarrage rapide

### Pour développeurs

1. **Architecture** ? Commencer par [01_Architecture](01_Architecture/)
2. **Outils** ? Voir [03_Tools](03_Tools/)
3. **Quick Start** ? Voir [../Tools/](../Tools/)

### Pour résoudre un problème

1. Consulter [04_Fixes](04_Fixes/)
2. Vérifier [07_Reports](07_Reports/)
3. Chercher dans [Archive](Archive/)

### Pour implémenter une fonctionnalité

1. Lire [02_Features](02_Features/)
2. Suivre [06_Guides](06_Guides/)
3. Utiliser [03_Tools](03_Tools/)

---

## ?? Maintenance

### Scripts disponibles

| Script | Fonction |
|--------|----------|
| `reorganize-documentation.ps1` | Réorganise la structure |
| `cleanup-obsolete-docs.ps1` | Nettoie les fichiers obsolètes |

### Contribution

Lors de l'ajout de nouvelle documentation :

1. Choisir le bon dossier (01-07)
2. Suivre la convention de nommage
3. Mettre à jour ce README.md
4. Ajouter au .csproj si nécessaire

---

## ?? Statistiques

| Catégorie | Nombre de docs |
|-----------|----------------|
| Architecture | 4 |
| Features | 6 |
| Tools | 5 |
| Fixes | 8 |
| Systems | 4 |
| Guides | 3 |
| Reports | 3 |
| Archive | 13 |
| **Total** | **46** |

---

## ?? Liens utiles

- [Godot Documentation](https://docs.godotengine.org/)
- [C# .NET 8 Documentation](https://docs.microsoft.com/en-us/dotnet/csharp/)
- [GitHub Repository](https://github.com/MTerance/Satsuki)

---

**Documentation maintenue par l'équipe Satsuki**  
*Dernière réorganisation : 22 novembre 2025*
