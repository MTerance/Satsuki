# ?? Guide des Emojis - Logs du Projet Satsuki

## Vue d'ensemble

Ce document r�pertorie tous les emojis utilis�s dans les logs du projet pour maintenir une coh�rence visuelle et faciliter la lecture des logs.

---

## ?? Sc�nes et Gameplay

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Initialisation de sc�ne, d�marrage de jeu | `"?? Title: Initialisation..."` |
| ?? | Cr�dits, cin�matiques | `"?? Credits: Initialisation..."` |
| ?? | Quiz, apprentissage | `"?? QuizScene initialis�e"` |
| ?? | Achievements, succ�s | `"?? Achievement d�bloqu�"` |
| ?? | Pause | `"?? Jeu mis en pause"` |
| ?? | Play, reprise | `"?? Jeu repris"` |
| ?? | Stop | `"?? Jeu arr�t�"` |

---

## ?? R�seau et Serveur

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Serveur, r�seau | `"?? Serveur actif"` |
| ?? | Connexion/d�connexion | `"?? Client d�connect�"` |
| ?? | Message re�u | `"?? [GAME] Order re�u"` |
| ?? | Message envoy� | `"?? Message envoy�"` |
| ?? | Broadcast | `"?? Message diffus�"` |
| ?? | Ping/Pong | `"?? Ping de Client_1"` |
| ?? | Clients connect�s | `"?? Clients connect�s: 3"` |
| ?? | Joueur sp�cifique | `"?? Alice a rejoint"` |

---

## ?? S�curit� et Cryptage

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Cryptage activ� | `"?? Cryptage: ACTIV�"` |
| ?? | Cl� de cryptage | `"?? Cl� par d�faut: ..."` |
| ?? | D�cryptage | `"?? Message d�crypt�"` |
| ?? | Erreur de s�curit� | `"?? Erreur r�seau"` |

---

## ?? Interface Utilisateur

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Menu, liste | `"?? Menu initialis�"` |
| ? | Succ�s, validation | `"? UI initialis�e"` |
| ? | Erreur | `"? Erreur de connexion"` |
| ?? | Avertissement | `"?? Attention: ..."` |
| ??? | Souris, hover | `"??? Menu hover: Credits"` |
| ?? | Navigation haut | `"?? Menu: Options"` |
| ?? | Navigation bas | `"?? Menu: Start Game"` |
| ?? | Navigation gauche | `"?? Page pr�c�dente"` |
| ?? | Navigation droite | `"?? Page suivante"` |

---

## ?? Donn�es et �tat

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Statistiques, �tat | `"?? �tat du jeu: ..."` |
| ?? | Texte, configuration | `"?? 3 splash screens configur�s"` |
| ?? | Sauvegarde | `"?? Partie sauvegard�e"` |
| ?? | Fichier | `"?? Fichier charg�"` |
| ??? | Suppression | `"??? Donn�es effac�es"` |

---

## ?? Actions et Commandes

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Skip, suivant | `"?? Skip vers le suivant"` |
| ? | Retour | `"? Retour en arri�re"` |
| ?? | Reload, refresh | `"?? Rechargement..."` |
| ?? | Loop, r�p�tition | `"?? Boucle active"` |
| ?? | M�lange, random | `"?? Questions m�lang�es"` |
| ?? | Fermeture, au revoir | `"?? Fermeture du jeu"` |
| ?? | Sortie | `"?? Sortie de la sc�ne"` |

---

## ?? Communication

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Chat, message | `"?? Chat de Client_1"` |
| ?? | Message g�n�rique | `"?? Message re�u"` |
| ?? | Indice, astuce | `"?? Indice envoy�"` |
| ? | Question | `"? Question envoy�e"` |
| ? | Exclamation, important | `"? Message important"` |

---

## ?? D�veloppement et Debug

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Configuration, setup | `"?? Syst�me initialis�"` |
| ?? | Debug | `"?? Mode debug: ACTIV�"` |
| ? | Performance, rapide | `"? Traitement haute fr�quence"` |
| ?? | Style, UI | `"?? Th�me appliqu�"` |
| ?? | Test | `"?? Test unitaire OK"` |

---

## ? Animations et Effets

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ? | Animation, effet sp�cial | `"? Effet appliqu�"` |
| ?? | Highlight, star | `"?? Nouvelle fonctionnalit�"` |
| ?? | Transition | `"?? Transition en cours"` |
| ?? | Effet visuel important | `"?? Victory animation"` |

---

## ?? Quiz et R�ponses

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ? | R�ponse correcte | `"? Bonne r�ponse!"` |
| ? | R�ponse incorrecte | `"? Mauvaise r�ponse"` |
| ?? | Score parfait | `"?? Score parfait!"` |
| ?? | Score, points | `"?? Score: 42 points"` |

---

## ?? Temps et Dur�e

| Emoji | Usage | Exemple |
|-------|-------|---------|
| ?? | Temps �coul� | `"?? Temps: 00:42"` |
| ? | Timer, alarme | `"? Temps �coul�!"` |
| ?? | Horloge | `"?? Heure: 14:30"` |

---

## ?? Exemples par Fichier

### MainGameScene.cs
```csharp
Console.WriteLine("?? MainGameScene: Syst�me initialis�");
Console.WriteLine("?? Test du syst�me de cryptage...");
Console.WriteLine("? Syst�me de cryptage op�rationnel");
Console.WriteLine("?? Serveur actif: true");
Console.WriteLine("?? Clients connect�s: 3");
Console.WriteLine("?? [GAME] Order re�u");
Console.WriteLine("? �tat du jeu envoy�");
```

### Title.cs
```csharp
GD.Print("?? Title: Initialisation de l'�cran titre...");
GD.Print("?? Menu initialis� avec 4 options");
GD.Print("? UI initialis�e");
GD.Print("??? Menu hover: Credits");
GD.Print("?? Menu: Options");
GD.Print("?? Menu: Start Game");
GD.Print("?? Ouverture des cr�dits...");
GD.Print("?? Fermeture du jeu...");
```

### Credits.cs
```csharp
GD.Print("?? Credits: Initialisation...");
GD.Print("?? 3 splash screens configur�s");
GD.Print("? Splash screen 1/3 termin�");
GD.Print("?? Skip vers le suivant");
GD.Print("?? Tous les cr�dits affich�s");
GD.Print("?? Retour au menu principal...");
```

### NetworkQuizScene.cs
```csharp
GD.Print("?? NetworkQuizScene initialis�e");
GD.Print("?? [NetworkQuizScene] Order: StartQuiz");
GD.Print("?? Quiz d�marr�");
GD.Print("?? Quiz mis en pause");
GD.Print("? R�ponse correcte");
GD.Print("?? Indice envoy�");
GD.Print("? Question envoy�e");
```

### ServerManager.cs
```csharp
GD.Print("?? ServerManager: Serveur d�marr�");
GD.Print("?? Client connect�: Client_1");
GD.Print("?? Client BACKEND authentifi�");
GD.Print("?? Message envoy� � Client_1");
GD.Print("?? Client d�connect�: Client_2");
```

---

## ?? R�gles de Style

### 1. Coh�rence
- Utilisez toujours le m�me emoji pour le m�me type de message
- Un emoji par ligne de log au d�but du message

### 2. Lisibilit�
- L'emoji doit clarifier le type de message
- Ne surchargez pas avec trop d'emojis

### 3. Priorit�
- ? Succ�s (vert mentalement)
- ? Erreur (rouge mentalement)
- ?? Avertissement (jaune mentalement)

### 4. Structure
```csharp
// Format standard
GD.Print("?? [Contexte]: Message descriptif");

// Exemples
GD.Print("?? Title: Initialisation...");
GD.Print("?? [GAME] Order de Client_1: GetGameState");
GD.Print("? Message envoy� avec succ�s");
```

---

## ?? Recherche Rapide

Pour trouver un type de log sp�cifique dans les fichiers :

| Type | Emoji � rechercher |
|------|-------------------|
| Erreurs | `?` |
| Succ�s | `?` |
| R�seau | `?? ?? ??` |
| S�curit� | `?? ??` |
| UI | `??? ?? ??` |
| Gameplay | `?? ?? ??` |

---

## ?? R�f�rences

Ce guide est bas� sur les conventions �tablies dans :
- MainGameScene.cs
- Title.cs
- Credits.cs
- NetworkQuizScene.cs
- ServerManager.cs

**Maintenir ce guide � jour lors de l'ajout de nouveaux types de logs !** ???
