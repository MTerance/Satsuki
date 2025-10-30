# ?? Guide des Emojis - Logs du Projet Satsuki

## Vue d'ensemble

Ce document répertorie tous les emojis utilisés dans les logs du projet pour maintenir une cohérence visuelle et faciliter la lecture des logs.

---

## ?? Scènes et Gameplay

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Initialisation de scène, démarrage de jeu | `"?? Title: Initialisation..."` |
| ?? | Crédits, cinématiques | `"?? Credits: Initialisation..."` |
| ?? | Quiz, apprentissage | `"?? QuizScene initialisée"` |
| ?? | Achievements, succès | `"?? Achievement débloqué"` |
| ?? | Pause | `"?? Jeu mis en pause"` |
| ?? | Play, reprise | `"?? Jeu repris"` |
| ?? | Stop | `"?? Jeu arrêté"` |

---

## ?? Réseau et Serveur

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Serveur, réseau | `"?? Serveur actif"` |
| ?? | Connexion/déconnexion | `"?? Client déconnecté"` |
| ?? | Message reçu | `"?? [GAME] Order reçu"` |
| ?? | Message envoyé | `"?? Message envoyé"` |
| ?? | Broadcast | `"?? Message diffusé"` |
| ?? | Ping/Pong | `"?? Ping de Client_1"` |
| ?? | Clients connectés | `"?? Clients connectés: 3"` |
| ?? | Joueur spécifique | `"?? Alice a rejoint"` |

---

## ?? Sécurité et Cryptage

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Cryptage activé | `"?? Cryptage: ACTIVÉ"` |
| ?? | Clé de cryptage | `"?? Clé par défaut: ..."` |
| ?? | Décryptage | `"?? Message décrypté"` |
| ?? | Erreur de sécurité | `"?? Erreur réseau"` |

---

## ?? Interface Utilisateur

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Menu, liste | `"?? Menu initialisé"` |
| ? | Succès, validation | `"? UI initialisée"` |
| ? | Erreur | `"? Erreur de connexion"` |
| ?? | Avertissement | `"?? Attention: ..."` |
| ??? | Souris, hover | `"??? Menu hover: Credits"` |
| ?? | Navigation haut | `"?? Menu: Options"` |
| ?? | Navigation bas | `"?? Menu: Start Game"` |
| ?? | Navigation gauche | `"?? Page précédente"` |
| ?? | Navigation droite | `"?? Page suivante"` |

---

## ?? Données et État

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Statistiques, état | `"?? État du jeu: ..."` |
| ?? | Texte, configuration | `"?? 3 splash screens configurés"` |
| ?? | Sauvegarde | `"?? Partie sauvegardée"` |
| ?? | Fichier | `"?? Fichier chargé"` |
| ??? | Suppression | `"??? Données effacées"` |

---

## ?? Actions et Commandes

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Skip, suivant | `"?? Skip vers le suivant"` |
| ? | Retour | `"? Retour en arrière"` |
| ?? | Reload, refresh | `"?? Rechargement..."` |
| ?? | Loop, répétition | `"?? Boucle active"` |
| ?? | Mélange, random | `"?? Questions mélangées"` |
| ?? | Fermeture, au revoir | `"?? Fermeture du jeu"` |
| ?? | Sortie | `"?? Sortie de la scène"` |

---

## ?? Communication

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Chat, message | `"?? Chat de Client_1"` |
| ?? | Message générique | `"?? Message reçu"` |
| ?? | Indice, astuce | `"?? Indice envoyé"` |
| ? | Question | `"? Question envoyée"` |
| ? | Exclamation, important | `"? Message important"` |

---

## ?? Développement et Debug

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Configuration, setup | `"?? Système initialisé"` |
| ?? | Debug | `"?? Mode debug: ACTIVÉ"` |
| ? | Performance, rapide | `"? Traitement haute fréquence"` |
| ?? | Style, UI | `"?? Thème appliqué"` |
| ?? | Test | `"?? Test unitaire OK"` |

---

## ? Animations et Effets

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ? | Animation, effet spécial | `"? Effet appliqué"` |
| ?? | Highlight, star | `"?? Nouvelle fonctionnalité"` |
| ?? | Transition | `"?? Transition en cours"` |
| ?? | Effet visuel important | `"?? Victory animation"` |

---

## ?? Quiz et Réponses

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ? | Réponse correcte | `"? Bonne réponse!"` |
| ? | Réponse incorrecte | `"? Mauvaise réponse"` |
| ?? | Score parfait | `"?? Score parfait!"` |
| ?? | Score, points | `"?? Score: 42 points"` |

---

## ?? Temps et Durée

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Temps écoulé | `"?? Temps: 00:42"` |
| ? | Timer, alarme | `"? Temps écoulé!"` |
| ?? | Horloge | `"?? Heure: 14:30"` |

---

## ?? Exemples par Fichier

### MainGameScene.cs
```csharp
Console.WriteLine("?? MainGameScene: Système initialisé");
Console.WriteLine("?? Test du système de cryptage...");
Console.WriteLine("? Système de cryptage opérationnel");
Console.WriteLine("?? Serveur actif: true");
Console.WriteLine("?? Clients connectés: 3");
Console.WriteLine("?? [GAME] Order reçu");
Console.WriteLine("? État du jeu envoyé");
```

### Title.cs
```csharp
GD.Print("?? Title: Initialisation de l'écran titre...");
GD.Print("?? Menu initialisé avec 4 options");
GD.Print("? UI initialisée");
GD.Print("??? Menu hover: Credits");
GD.Print("?? Menu: Options");
GD.Print("?? Menu: Start Game");
GD.Print("?? Ouverture des crédits...");
GD.Print("?? Fermeture du jeu...");
```

### Credits.cs
```csharp
GD.Print("?? Credits: Initialisation...");
GD.Print("?? 3 splash screens configurés");
GD.Print("? Splash screen 1/3 terminé");
GD.Print("?? Skip vers le suivant");
GD.Print("?? Tous les crédits affichés");
GD.Print("?? Retour au menu principal...");
```

### NetworkQuizScene.cs
```csharp
GD.Print("?? NetworkQuizScene initialisée");
GD.Print("?? [NetworkQuizScene] Order: StartQuiz");
GD.Print("?? Quiz démarré");
GD.Print("?? Quiz mis en pause");
GD.Print("? Réponse correcte");
GD.Print("?? Indice envoyé");
GD.Print("? Question envoyée");
```

### ServerManager.cs
```csharp
GD.Print("?? ServerManager: Serveur démarré");
GD.Print("?? Client connecté: Client_1");
GD.Print("?? Client BACKEND authentifié");
GD.Print("?? Message envoyé à Client_1");
GD.Print("?? Client déconnecté: Client_2");
```

---

## ?? Règles de Style

### 1. Cohérence
- Utilisez toujours le même emoji pour le même type de message
- Un emoji par ligne de log au début du message

### 2. Lisibilité
- L'emoji doit clarifier le type de message
- Ne surchargez pas avec trop d'emojis

### 3. Priorité
- ? Succès (vert mentalement)
- ? Erreur (rouge mentalement)
- ?? Avertissement (jaune mentalement)

### 4. Structure
```csharp
// Format standard
GD.Print("?? [Contexte]: Message descriptif");

// Exemples
GD.Print("?? Title: Initialisation...");
GD.Print("?? [GAME] Order de Client_1: GetGameState");
GD.Print("? Message envoyé avec succès");
```

---

## ?? Recherche Rapide

Pour trouver un type de log spécifique dans les fichiers :

| Type | Emoji à rechercher |
|------|-------------------|
| Erreurs | `?` |
| Succès | `?` |
| Réseau | `?? ?? ??` |
| Sécurité | `?? ??` |
| UI | `??? ?? ??` |
| Gameplay | `?? ?? ??` |

---

## ?? Références

Ce guide est basé sur les conventions établies dans :
- MainGameScene.cs
- Title.cs
- Credits.cs
- NetworkQuizScene.cs
- ServerManager.cs

**Maintenir ce guide à jour lors de l'ajout de nouveaux types de logs !** ???
