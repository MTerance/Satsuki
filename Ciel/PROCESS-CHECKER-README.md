# Service de Vérification de Processus Satsuki

Ce service permet de vérifier si le programme `Satsuki.exe` est en cours d'exécution sur le système. Il est basé sur une architecture modulaire Electron avec une interface Vue.js.

## 🏗️ Architecture

### Structure des Fichiers

```
Ciel/
├── electron/
│   ├── modules/
│   │   ├── process-checker.cjs        # Module Electron principal
│   │   └── index.cjs                  # Export du module
│   ├── main.cjs                       # Handlers IPC
│   ├── preload.js                     # Exposition de l'API
│   └── types/
│       └── electron.d.ts              # Types TypeScript
├── src/
│   ├── services/
│   │   └── processService.js          # Service Vue.js
│   ├── components/
│   │   └── ProcessCheckerDemo.vue     # Composant de démonstration
│   └── types/
│       └── electron.d.ts              # Types TypeScript
```

### Flux de Données

1. **Electron Main Process** (`process-checker.cjs`) - Exécute les commandes système
2. **IPC Handlers** (`main.cjs`) - Communication inter-processus
3. **Preload Script** (`preload.js`) - Exposition sécurisée de l'API
4. **Vue Service** (`processService.js`) - Interface réactive
5. **Vue Component** (`ProcessCheckerDemo.vue`) - Interface utilisateur

## 🚀 Fonctionnalités

### Module Electron (process-checker.cjs)

#### Méthodes Principales

- **`checkSatsukiProcess()`** - Vérification basique du processus
- **`getDetailedProcessInfo()`** - Informations détaillées (Windows uniquement)
- **`getAllSatsukiProcesses()`** - Liste de tous les processus Satsuki
- **`startMonitoring()`** - Surveillance périodique avec callback

#### Compatibilité Multiplateforme

- **Windows** : Utilise `tasklist` et `wmic`
- **Unix/Linux/macOS** : Utilise `pgrep`

### Service Vue (processService.js)

#### États Réactifs

```javascript
const processService = new ProcessService();

// États principaux
processService.isRunning.value        // boolean - Processus en cours ?
processService.processInfo.value      // Object - Informations du processus
processService.lastCheck.value        // string - Dernière vérification (ISO)
processService.error.value            // string - Dernière erreur
processService.isChecking.value       // boolean - Vérification en cours ?
processService.monitoring.value       // boolean - Surveillance active ?

// Statistiques
processService.stats = {
  totalChecks: 0,                     // Nombre total de vérifications
  successfulChecks: 0,                // Vérifications réussies
  failedChecks: 0,                    // Vérifications échouées
  uptimeChecks: 0,                    // Vérifications où Satsuki était actif
  lastSuccessfulCheck: null,          // Dernière vérification réussie
  averageCheckDuration: 0             // Temps moyen de vérification (ms)
}

// Configuration
processService.config = {
  checkInterval: 5000,                // Intervalle de surveillance (ms)
  autoStart: false,                   // Démarrage automatique
  enableDetailedInfo: true            // Informations détaillées
}
```

#### Méthodes d'API

```javascript
// Vérification unique
const result = await processService.checkSatsukiProcess();

// Informations détaillées
const detailed = await processService.getDetailedProcessInfo();

// Tous les processus
const allProcesses = await processService.getAllSatsukiProcesses();

// Surveillance
processService.startMonitoring(5000, (result) => {
  console.log('Satsuki est', result.running ? 'actif' : 'inactif');
});

processService.stopMonitoring();

// État actuel
const state = processService.getCurrentState();

// Diagnostic
const diagnostic = processService.getDiagnosticInfo();
```

## 📊 Format des Données

### Résultat de Vérification

```typescript
interface ProcessCheckResult {
  running: boolean;              // Processus en cours d'exécution
  processInfo: ProcessInfo | null;  // Informations du processus
  error: string | null;          // Message d'erreur éventuel
}
```

### Informations de Processus (Windows)

```typescript
interface ProcessInfo {
  imageName?: string;            // "Satsuki.exe"
  pid?: number;                  // ID du processus
  sessionName?: string;          // "Console" ou "Services"
  sessionNumber?: number;        // Numéro de session
  memoryUsage?: string;          // "1,234 K"
  creationDate?: string;         // Date de création (wmic)
  pageFileUsage?: string;        // Utilisation fichier de pagination
  workingSetSize?: string;       // Taille du working set
}
```

### Informations de Processus (Unix)

```typescript
interface ProcessInfo {
  pid: number;                   // ID du processus
  processName: string;           // "Satsuki.exe"
  count?: number;                // Nombre d'instances
}
```

## 🔧 Utilisation

### Dans un Composant Vue

```vue
<template>
  <div>
    <p>Satsuki est {{ processService.isRunning.value ? 'actif' : 'inactif' }}</p>
    <button @click="check">Vérifier</button>
    <button @click="toggleMonitoring">
      {{ processService.monitoring.value ? 'Arrêter' : 'Démarrer' }} surveillance
    </button>
  </div>
</template>

<script>
import processService from '@/services/processService.js';

export default {
  setup() {
    const check = async () => {
      await processService.checkSatsukiProcess();
    };

    const toggleMonitoring = () => {
      if (processService.monitoring.value) {
        processService.stopMonitoring();
      } else {
        processService.startMonitoring(3000, (result) => {
          console.log('État Satsuki:', result.running ? 'ON' : 'OFF');
        });
      }
    };

    return {
      processService,
      check,
      toggleMonitoring
    };
  }
};
</script>
```

### Surveillance Avancée

```javascript
// Callback personnalisé
const onProcessChange = (result) => {
  if (result.running) {
    console.log(`Satsuki détecté (PID: ${result.processInfo?.pid})`);
    // Logique quand Satsuki démarre
  } else {
    console.log('Satsuki arrêté');
    // Logique quand Satsuki s'arrête
  }
};

// Démarrer la surveillance
processService.startMonitoring(2000, onProcessChange);

// Ajouter des callbacks supplémentaires
processService.addMonitoringCallback((result) => {
  // Envoyer des métriques
  analytics.track('satsuki_status', { running: result.running });
});
```

## ⚙️ Configuration

### Paramètres du Service

```javascript
// Modifier la configuration
processService.updateConfig({
  checkInterval: 3000,           // Vérifier toutes les 3 secondes
  enableDetailedInfo: false,     // Désactiver les infos détaillées
  autoStart: true               // Démarrage automatique de la surveillance
});

// Configuration par défaut
const defaultConfig = {
  checkInterval: 5000,          // 5 secondes
  autoStart: false,            // Pas de démarrage auto
  enableDetailedInfo: true     // Infos détaillées activées
};
```

## 🐛 Gestion d'Erreurs

### Types d'Erreurs Communes

1. **API non disponible** - L'application n'est pas dans Electron
2. **Commande échouée** - Erreur système lors de l'exécution
3. **Parse erreur** - Impossible de parser la sortie de la commande
4. **Permissions** - Accès insuffisant pour exécuter les commandes

### Diagnostic

```javascript
// Informations de diagnostic complètes
const diagnostic = processService.getDiagnosticInfo();
console.log('Diagnostic:', diagnostic);

// Vérification de l'API
if (!window.processChecker) {
  console.error('API processChecker non disponible - vérifiez que vous êtes dans Electron');
}

// Vérification des erreurs récentes
if (processService.error.value) {
  console.error('Dernière erreur:', processService.error.value);
}
```

## 🧪 Tests et Développement

### Test Manuel

1. Ouvrir le composant `ProcessCheckerDemo.vue`
2. Utiliser les boutons de test pour vérifier les fonctionnalités
3. Surveiller le journal des événements
4. Vérifier les statistiques

### Commandes Système Utilisées

#### Windows
```cmd
# Vérification basique
tasklist /FI "IMAGENAME eq Satsuki.exe" /FO CSV

# Informations détaillées
wmic process where "ProcessId=[PID]" get Name,ProcessId,PageFileUsage,WorkingSetSize,CreationDate /format:csv
```

#### Unix/Linux/macOS
```bash
# Vérification basique
pgrep -f Satsuki.exe
```

## 🔮 Extensions Futures

### Fonctionnalités Prévues

- **Alertes** - Notifications quand Satsuki démarre/s'arrête
- **Historique** - Stockage de l'historique des états
- **Métriques** - Graphiques de disponibilité
- **Contrôles** - Démarrer/arrêter Satsuki depuis l'interface
- **Multi-processus** - Surveillance de plusieurs applications
- **Logs système** - Intégration avec les logs système

### API Extensions

```javascript
// Futures fonctionnalités
processService.startSatsuki();           // Démarrer Satsuki
processService.stopSatsuki();            // Arrêter Satsuki
processService.restartSatsuki();         // Redémarrer Satsuki
processService.getProcessHistory();      // Historique des états
processService.exportLogs();             // Exporter les logs
```

## 📝 Notes Techniques

### Sécurité

- Utilisation de `contextBridge` pour l'exposition sécurisée des APIs
- Validation des entrées côté Electron
- Pas d'accès direct aux APIs Node.js depuis le renderer

### Performance

- Cache des résultats pour éviter les appels système répétés
- Surveillance non-bloquante avec intervalles configurables
- Parsing optimisé des sorties de commandes système

### Limitations

- Les informations détaillées ne sont disponibles que sur Windows
- Nécessite des permissions pour exécuter les commandes système
- Les processus en arrière-plan peuvent ne pas être détectés sur certains systèmes

## 🏁 Conclusion

Ce service fournit une solution complète pour surveiller l'état du processus Satsuki.exe avec :
- ✅ Interface réactive Vue.js
- ✅ Backend Electron sécurisé
- ✅ Compatibilité multiplateforme
- ✅ Surveillance en temps réel
- ✅ Statistiques détaillées
- ✅ Configuration flexible
- ✅ Gestion d'erreurs robuste