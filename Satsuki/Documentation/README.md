# ?? Index de la Documentation - Projet Satsuki

## ?? Maintenance & Outils

| Document | Description |
|----------|-------------|
| [Fix-Unicode-Script.md](Fix-Unicode-Script.md) | Script de correction Unicode |
| [Unicode_Fix_Complete_Report.md](Unicode_Fix_Complete_Report.md) | Rapport complet de correction Unicode |

## ?? Scènes & Navigation

| Document | Description |
|----------|-------------|
| [TITLE_SCENE.md](TITLE_SCENE.md) | Documentation de la scène Title |
| [TITLE_SCENE_SUMMARY.md](TITLE_SCENE_SUMMARY.md) | Résumé de Title |
| [Title_LobbyEx_Integration.md](Title_LobbyEx_Integration.md) | Intégration Title/LobbyEx |
| [CREDITS_SCENARIO.md](CREDITS_SCENARIO.md) | Scénario des crédits |
| [CREDITS_ISCENE_IMPLEMENTATION.md](CREDITS_ISCENE_IMPLEMENTATION.md) | Implémentation IScene |
| [Credits_AutoLoad.md](Credits_AutoLoad.md) | Chargement auto des crédits |
| [Credits_Title_Navigation.md](Credits_Title_Navigation.md) | Navigation Credits/Title |

## ?? SplashScreen

| Document | Description |
|----------|-------------|
| [SPLASHSCREEN_MANAGER.md](SPLASHSCREEN_MANAGER.md) | Manager des splash screens |
| [SplashScreenManager_Refactor.md](SplashScreenManager_Refactor.md) | Refactorisation |
| [SplashScreen_Debug_Guide.md](SplashScreen_Debug_Guide.md) | Guide de debug |

## ?? Locations

| Document | Description |
|----------|-------------|
| [ILocation_Interface.md](ILocation_Interface.md) | Interface ILocation |
| [LocationManager.md](LocationManager.md) | Gestionnaire de locations |
| [LocationManager_Integration.md](LocationManager_Integration.md) | Intégration du manager |
| [LocationManager_Resume.md](LocationManager_Resume.md) | Résumé du système |
| [Restaurant_Setup_Guide.md](Restaurant_Setup_Guide.md) | Guide setup Restaurant |
| [Restaurant_Title_Integration.md](Restaurant_Title_Integration.md) | Intégration Restaurant/Title |
| [Restaurant_Fix_Summary.md](Restaurant_Fix_Summary.md) | Résumé des corrections |

## ?? MainGameScene

| Document | Description |
|----------|-------------|
| [MainGameScene_Refactorisation.md](MainGameScene_Refactorisation.md) | Refactorisation |
| [MainGameScene_Simplification.md](MainGameScene_Simplification.md) | Simplification |
| [MainGameScene_Migration_Summary.md](MainGameScene_Migration_Summary.md) | Résumé migration |
| [MainGameScene_CurrentLocation_Property.md](MainGameScene_CurrentLocation_Property.md) | Propriété CurrentLocation |
| [MainGameScene_CurrentScene_Property.md](MainGameScene_CurrentScene_Property.md) | Propriété CurrentScene |
| [Specialized_LoadUnload_Methods.md](Specialized_LoadUnload_Methods.md) | Méthodes Load/Unload |

## ?? Réseau & Serveur

| Document | Description |
|----------|-------------|
| [ServerArchitecture.md](ServerArchitecture.md) | Architecture serveur |
| [CLIENT_TYPE_AUTHENTICATION.md](CLIENT_TYPE_AUTHENTICATION.md) | Authentification clients |
| [CryptageSystem.md](CryptageSystem.md) | Système de cryptage |

## ?? Changements & Suppressions

| Document | Description |
|----------|-------------|
| [Changements_Retires_LobbyEx.md](Changements_Retires_LobbyEx.md) | Retrait de LobbyEx |
| [Suppression_Lobby.md](Suppression_Lobby.md) | Suppression du lobby |

## ?? Corrections Techniques

| Document | Description |
|----------|-------------|
| [SubViewport_Fix.md](SubViewport_Fix.md) | Correction SubViewport |
| [Camera_Management_System.md](Camera_Management_System.md) | Gestion des caméras |
| [GETGAMESTATE_SYSTEM.md](GETGAMESTATE_SYSTEM.md) | Système GetGameState |

---

## ?? Comment utiliser cette documentation

### Pour les développeurs
- Consultez les sections par fonctionnalité
- Les documents "Summary" et "Resume" donnent une vue d'ensemble
- Les guides "Setup" et "Integration" sont pratiques pour l'implémentation

### Pour la maintenance
- `Fix-Unicode-Script.md` pour les corrections Unicode
- `Unicode_Fix_Complete_Report.md` pour l'historique complet

### Structure recommandée
```
Documentation/
??? Maintenance (Unicode, Scripts)
??? Architecture (MainGameScene, LocationManager)
??? Scènes (Title, Credits, Restaurant)
??? Systèmes (SplashScreen, Camera, Network)
??? Historique (Changements, Suppressions)
```

---

*Dernière mise à jour : 2024*
