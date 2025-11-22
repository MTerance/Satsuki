# ?? Index de la Documentation - Projet Satsuki

## ?? Maintenance & Outils

| Document | Description |
|----------|-------------|
| [Fix-Unicode-Script.md](Fix-Unicode-Script.md) | Script de correction Unicode |
| [Unicode_Fix_Complete_Report.md](Unicode_Fix_Complete_Report.md) | Rapport complet de correction Unicode |
| [Cleanup_Scripts_Report.md](Cleanup_Scripts_Report.md) | Rapport de nettoyage des scripts |

## ?? Scènes & Navigation

### Title & MainMenu
| Document | Description |
|----------|-------------|
| [Title_Menu_Display_Fix.md](Title_Menu_Display_Fix.md) | Correction affichage menu Title |
| [MainMenu_Complete_Implementation.md](MainMenu_Complete_Implementation.md) | Implémentation complète MainMenu |
| [Credits_AutoLoad.md](Credits_AutoLoad.md) | Chargement auto des crédits |
| [Credits_Title_Navigation.md](Credits_Title_Navigation.md) | Navigation Credits/Title |

### Crédits
| Document | Description |
|----------|-------------|
| [CREDITS_SCENARIO.md](CREDITS_SCENARIO.md) | Scénario des crédits |
| [CREDITS_ISCENE_IMPLEMENTATION.md](CREDITS_ISCENE_IMPLEMENTATION.md) | Implémentation IScene |

## ?? SplashScreen

| Document | Description |
|----------|-------------|
| [SplashScreen_Fade_Fix.md](SplashScreen_Fade_Fix.md) | Correction fade in/out |
| [SplashScreen_Debug_Guide.md](SplashScreen_Debug_Guide.md) | Guide de debug |

## ?? Système de Caméras

| Document | Description |
|----------|-------------|
| [Camera_Context_System.md](Camera_Context_System.md) | Système de caméras contextuelles |
| [Camera_System_Improvement.md](Camera_System_Improvement.md) | Améliorations système caméras |
| [Title_Camera_Activation.md](Title_Camera_Activation.md) | Activation Title_Camera3D |

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
| [MainGameScene_Complete_Architecture.md](MainGameScene_Complete_Architecture.md) | Architecture complète (? RÉCENT) |

## ?? Réseau & Serveur

| Document | Description |
|----------|-------------|
| [ServerArchitecture.md](ServerArchitecture.md) | Architecture serveur |
| [CLIENT_TYPE_AUTHENTICATION.md](CLIENT_TYPE_AUTHENTICATION.md) | Authentification clients |
| [CryptageSystem.md](CryptageSystem.md) | Système de cryptage |
| [MESSAGE_ROUTING_SYSTEM.md](MESSAGE_ROUTING_SYSTEM.md) | Système de routage messages |
| [MESSAGE_ROUTING_SUMMARY.md](MESSAGE_ROUTING_SUMMARY.md) | Résumé routage messages |

## ?? Corrections Techniques

| Document | Description |
|----------|-------------|
| [SubViewport_Fix.md](SubViewport_Fix.md) | Correction SubViewport |
| [GETGAMESTATE_SYSTEM.md](GETGAMESTATE_SYSTEM.md) | Système GetGameState |
| [Application_Close_Fix.md](Application_Close_Fix.md) | Correction fermeture app |
| [UTF8_ENCODING_FIX.md](UTF8_ENCODING_FIX.md) | Correction encodage UTF-8 |

## ?? Guides

| Document | Description |
|----------|-------------|
| [EMOJI_LOG_GUIDE.md](EMOJI_LOG_GUIDE.md) | Guide des emojis dans les logs |

---

## ?? Comment utiliser cette documentation

### Pour les développeurs
- Consultez les sections par fonctionnalité
- Les documents "Complete" donnent une vue d'ensemble complète
- Les guides "Setup" et "Integration" sont pratiques pour l'implémentation

### Pour la maintenance
- `Fix-Unicode-Script.md` pour les corrections Unicode
- `Cleanup_Scripts_Report.md` pour l'historique de nettoyage
- Documents "Fix" pour les corrections spécifiques

### Structure recommandée
```
Documentation/
??? Maintenance (Unicode, Scripts, Cleanup)
??? Architecture (MainGameScene, LocationManager)
??? Scènes (Title, MainMenu, Credits, Restaurant)
??? Systèmes (SplashScreen, Camera, Network)
??? Corrections (SubViewport, Encoding, Close)
```

---

## ??? Nettoyage récent (22/11/2025)

### Documents supprimés (obsolètes/doublons)
- ? MainGameScene_Refactorisation.md
- ? MainGameScene_Simplification.md
- ? MainGameScene_Migration_Summary.md
- ? MainGameScene_CurrentLocation_Property.md
- ? MainGameScene_CurrentScene_Property.md
- ? Camera_Management_System.md
- ? TITLE_SCENE.md
- ? TITLE_SCENE_SUMMARY.md
- ? SPLASHSCREEN_MANAGER.md
- ? SplashScreenManager_Refactor.md
- ? SESSION_SUMMARY.md
- ? Changements_Retires_LobbyEx.md
- ? Suppression_Lobby.md
- ? Specialized_LoadUnload_Methods.md

**Total** : 14 fichiers obsolètes supprimés

### Documents conservés (à jour)
- ? MainGameScene_Complete_Architecture.md (architecture complète)
- ? Camera_Context_System.md (système de caméras)
- ? Title_Menu_Display_Fix.md (menu Title)
- ? MainMenu_Complete_Implementation.md (MainMenu)
- ? SplashScreen_Fade_Fix.md (fade in/out)
- ? Application_Close_Fix.md (fermeture app)

---

*Dernière mise à jour : 22/11/2025*  
*Fichiers actifs : 33*  
*Fichiers supprimés : 14*
