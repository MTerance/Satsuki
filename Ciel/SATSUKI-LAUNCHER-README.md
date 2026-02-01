# Satsuki Launcher - Gestionnaire Multi-Écrans

Une interface complète pour détecter, lancer et gérer les instances de Satsuki.exe sur plusieurs écrans.

## 🎯 Fonctionnalités

### 🔍 Détection Automatique
- **Vérification du processus** : Détecte si Satsuki.exe est déjà en cours d'exécution
- **Surveillance temps réel** : Mise à jour automatique du statut toutes les 10 secondes
- **Informations détaillées** : PID, mémoire utilisée, session (Windows)

### 🖥️ Gestion Multi-Écrans
- **Détection automatique** : Trouve tous les écrans connectés au système
- **Informations complètes** : Résolution, position, DPI, écran tactile
- **Lancement ciblé** : Lance Satsuki sur l'écran de votre choix

### 🚀 Options de Lancement

#### Lancement Rapide
- **Meilleur écran** : Sélectionne automatiquement l'écran optimal
- **Écran principal** : Lance sur l'écran principal du système

#### Lancement Personnalisé
- **Sélection manuelle** : Choisissez l'écran spécifique
- **Chemin personnalisé** : Spécifiez l'emplacement de Satsuki.exe
- **Préférences** : Configurez vos critères de sélection d'écran

### 🔌 Connexion aux Instances
- **Détection d'instances** : Affiche toutes les instances Satsuki en cours
- **Connexion directe** : Se connecter à une instance existante
- **Gestion multiple** : Support de plusieurs instances simultanées

## 🏗️ Architecture Technique

### Backend Electron
```
electron/modules/
├── process-checker.cjs     # Détection de processus
├── screen-manager.cjs      # Gestion d'écrans
└── index.cjs              # Exports centralisés
```

### Frontend Vue
```
src/
├── views/SatsukiLauncher.vue    # Interface principale
├── services/processService.js   # Service de processus
└── types/electron.d.ts         # Types TypeScript
```

### Communication IPC
- **Sécurisée** : Utilise contextBridge d'Electron
- **Typée** : Interfaces TypeScript complètes
- **Robuste** : Gestion d'erreurs avancée

## 📊 Interface Utilisateur

### États Principaux

#### 🔴 Satsuki Arrêté
```
📱 Écrans Détectés
┌─────────────────────────┐ ┌─────────────────────────┐
│    Écran Principal      │ │    Écran Secondaire     │
│      1920×1080         │ │       2560×1440         │
│   🚀 Lancer sur cet    │ │   🚀 Lancer sur cet    │
│         écran          │ │         écran          │
└─────────────────────────┘ └─────────────────────────┘

⚡ Lancement Rapide
┌─────────────────┐ ┌─────────────────────┐
│  Meilleur Écran │ │   Écran Principal   │
└─────────────────┘ └─────────────────────┘
```

#### 🟢 Satsuki En Cours
```
✅ Satsuki est en cours d'exécution
   2 instance(s) détectée(s)

┌──────────────────────────────────────────┐
│ 🔌 Se connecter à cette instance de jeu │
└──────────────────────────────────────────┘

Instances Actives:
┌─────────────┐ ┌─────────────┐
│ PID: 12345  │ │ PID: 67890  │
│ Satsuki.exe │ │ Satsuki.exe │
│ 256 MB      │ │ 312 MB      │
└─────────────┘ └─────────────┘
```

### Informations Système
- **Écrans totaux** : Nombre d'écrans connectés
- **Écrans tactiles** : Support tactile disponible
- **Haute résolution** : Écrans avec DPI élevé
- **Surface totale** : Pixels disponibles combinés

## ⚙️ Configuration

### Préférences de Lancement
```javascript
const preferences = {
  preferPrimary: false,        // Préférer l'écran principal
  preferLargeScreen: true,     // Préférer les grands écrans
  preferHighDPI: false,        // Préférer haute résolution
  minWidth: 1024,             // Largeur minimale
  minHeight: 768              // Hauteur minimale
};
```

### Chemins de Recherche Automatique
Le système recherche Satsuki.exe dans :
1. Chemin personnalisé (si spécifié)
2. `C:\Program Files\Satsuki\`
3. `C:\Program Files (x86)\Satsuki\`
4. `C:\Games\Satsuki\`
5. Bureau utilisateur
6. Dossier Documents/Satsuki

## 🔧 APIs Disponibles

### Process Checker
```javascript
// Vérification simple
const result = await window.processChecker.checkSatsuki();

// Informations détaillées
const detailed = await window.processChecker.getDetailedInfo();

// Toutes les instances
const all = await window.processChecker.getAllSatsukiProcesses();
```

### Screen Manager
```javascript
// Liste des écrans
const displays = await window.screenManager.getAllDisplays();

// Lancer sur écran spécifique
const result = await window.screenManager.launchSatsukiOnDisplay(
  displayId, 
  'C:\Path\To\Satsuki.exe'
);

// Obtenir le meilleur écran
const best = await window.screenManager.getBestDisplay({
  preferLargeScreen: true
});
```

## 🎨 Design System

### Couleurs de Statut
- **🟢 Vert** : Satsuki en cours d'exécution
- **🔴 Rouge** : Satsuki arrêté
- **🟡 Jaune** : En cours de lancement
- **🔵 Bleu** : Surveillance active

### Animation & Feedback
- **Pulse** : Statut de surveillance active
- **Shimmer** : Chargement en cours
- **Hover Effects** : Survol des cartes d'écran
- **Transitions** : Changements d'état fluides

## 🚦 États et Transitions

```
┌─────────────┐    checkSatsuki()    ┌────────────────┐
│ Initialise  │ ────────────────────▶│ Satsuki Arrêté │
└─────────────┘                     └────────────────┘
                                             │
                                    launchSatsuki()
                                             ▼
┌─────────────┐    processFound()    ┌────────────────┐
│ En Cours    │◄────────────────────── │ En Lancement   │
└─────────────┘                     └────────────────┘
       │                                      │
       │                             launchFailed()
       │                                      ▼
       │            processStopped()   ┌────────────────┐
       └──────────────────────────────▶│ Erreur         │
                                      └────────────────┘
```

## 📱 Responsive Design

### Desktop (1024px+)
- Grille 3 colonnes pour les écrans
- Interface complète avec tous les contrôles
- Sidebar avec informations détaillées

### Tablet (768px-1024px)
- Grille 2 colonnes pour les écrans
- Interface condensée
- Contrôles groupés

### Mobile (< 768px)
- Liste verticale des écrans
- Interface simplifiée
- Navigation par onglets

## 🔍 Debugging & Logs

### Console Logs
```javascript
// Activation des logs détaillés
localStorage.setItem('satsuki-launcher-debug', 'true');

// Désactivation
localStorage.removeItem('satsuki-launcher-debug');
```

### Informations de Diagnostic
```javascript
// Dans la console du navigateur
console.log(processService.getDiagnosticInfo());
```

## 🚀 Utilisation

### Accès Direct
Visitez : `http://localhost:5173/satsuki-launcher`

### Navigation
Dans l'application : Menu → "🎮 Satsuki Launcher"

### Premier Lancement
1. L'interface vérifie automatiquement si Satsuki est en cours
2. Détecte tous les écrans disponibles
3. Affiche les options appropriées selon l'état

### Lancement Simple
1. Si Satsuki n'est pas lancé, cliquez "Lancer sur le meilleur écran"
2. Le système sélectionne automatiquement l'écran optimal
3. Lance Satsuki avec les paramètres appropriés

### Lancement Avancé
1. Sélectionnez un écran spécifique dans la grille
2. Optionnel : Spécifiez un chemin personnalisé
3. Cliquez "Lancer sur cet écran"

### Connexion aux Instances
1. Si Satsuki est déjà en cours, le système l'affiche
2. Cliquez "Se connecter à cette instance de jeu"
3. La connexion s'établit automatiquement

## 🔐 Sécurité

- **Isolation** : Processus Electron isolé du renderer
- **Validation** : Tous les paramètres sont validés
- **Sandbox** : Exécution dans un environnement sécurisé
- **Permissions** : Accès limité aux APIs système

## 🎯 Limitations Connues

1. **Windows Uniquement** : Les informations détaillées ne sont disponibles que sur Windows
2. **Positioning** : Le positionnement de fenêtre dépend du support par Satsuki.exe
3. **Permissions** : Nécessite les droits d'exécution des commandes système
4. **Détection** : Les processus en arrière-plan peuvent ne pas être détectés

## 🔄 Mises à Jour Futures

- **Historique** : Stockage de l'historique des lancements
- **Profils** : Sauvegarde de configurations d'écran
- **Notifications** : Alertes système pour les changements d'état
- **Contrôle** : Arrêt/redémarrage des instances depuis l'interface
- **Métriques** : Statistiques d'utilisation et performance