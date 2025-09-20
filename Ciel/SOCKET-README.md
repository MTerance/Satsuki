# 🔌 Client Socket.IO pour Quiz 3D

Ce module fournit un client Socket.IO complet pour votre application de quiz 3D avec synchronisation en temps réel.

## 📁 Structure des fichiers

```
src/
├── services/
│   └── socketClient.js          # Client Socket.IO principal
├── composables/
│   └── useSocket.js             # Composables Vue pour Socket.IO
├── components/
│   └── SocketDemo.vue           # Composant de démonstration
└── config/
    └── socketConfig.js          # Configuration Socket.IO

server/
└── socket-server.js             # Serveur Socket.IO de développement
```

## 🚀 Démarrage rapide

### 1. Démarrer le serveur Socket.IO

```bash
# Terminal 1 : Démarrer le serveur Socket.IO
npm run socket-server

# Ou démarrer l'application complète avec Socket.IO
npm run web-with-socket
```

### 2. Utiliser le client dans un composant Vue

```vue
<script setup>
import { useSocket } from '@/composables/useSocket.js';

const socket = useSocket();

// Se connecter au serveur
const connect = () => {
  socket.connect('http://localhost:3001');
};

// Écouter les événements
socket.on('quiz:started', (data) => {
  console.log('Quiz démarré:', data);
});

// Émettre des événements
const startQuiz = () => {
  socket.emit('quiz:start', {
    quizId: 'quiz-123',
    userName: 'MonNom'
  });
};
</script>
```

## 🎯 Fonctionnalités

### 🔗 Connexion Socket.IO
- Connexion automatique avec reconnexion
- Gestion des états de connexion
- Statistiques de connexion en temps réel

### 🎮 Quiz 3D
- Création et gestion de quiz en temps réel
- Soumission de réponses avec timer
- Classement en temps réel (leaderboard)
- Support des modèles 3D

### 🌐 Synchronisation 3D
- Synchronisation de caméra 3D entre utilisateurs
- Chargement partagé de modèles 3D
- Interactions 3D collaboratives

## 📡 API du Client Socket.IO

### Classe SocketClient

#### Méthodes principales

```javascript
// Connexion
connect(url, options)          // Se connecter au serveur
disconnect()                   // Se déconnecter
emit(event, data)             // Émettre un événement
on(event, callback)           // Écouter un événement
off(event, callback)          // Arrêter d'écouter

// Rooms
joinRoom(roomName, userData)   // Rejoindre une room
leaveRoom(roomName)           // Quitter une room

// Quiz
startQuiz(quizId, userName)   // Démarrer un quiz
submitAnswer(questionId, answer, timeTaken)  // Soumettre une réponse

// 3D
syncCamera3D(cameraData)      // Synchroniser la caméra 3D
loadModel3D(modelPath, data)  // Charger un modèle 3D
```

#### États réactifs (Vue)

```javascript
isConnected.value             // État de connexion (boolean)
connectionStatus.value        // Statut détaillé ('connected', 'disconnected', etc.)
```

### Composables Vue

#### useSocket()
Composable de base pour Socket.IO

```javascript
const {
  isConnected,
  connectionStatus,
  connect,
  disconnect,
  emit,
  on,
  off,
  joinRoom,
  leaveRoom
} = useSocket();
```

#### useQuizSocket()
Composable spécialisé pour les quiz

```javascript
const {
  quizState,
  startQuiz,
  submitAnswer
} = useQuizSocket();

// quizState contient :
// - currentQuiz
// - currentQuestion  
// - participants
// - leaderboard
// - userAnswers
// - isActive
```

#### use3DSync()
Composable pour la synchronisation 3D

```javascript
const {
  sync3DState,
  syncCamera,
  loadSharedModel
} = use3DSync();

// sync3DState contient :
// - connectedUsers
// - sharedCamera
// - loadedModels
// - interactions
```

## 🎮 Événements Quiz

### Événements émis par le client

```javascript
// Démarrer un quiz
socket.emit('quiz:start', {
  quizId: 'quiz-123',
  userName: 'MonNom'
});

// Soumettre une réponse
socket.emit('quiz:submit_answer', {
  questionId: 1,
  answer: 'Option A',
  timeTaken: 15 // secondes
});
```

### Événements reçus du serveur

```javascript
// Quiz démarré
socket.on('quiz:started', (data) => {
  // data.quiz: informations du quiz
  // data.participant: informations du participant
});

// Nouvelle question
socket.on('quiz:question', (data) => {
  // data.question: question avec options
  // data.questionNumber: numéro de la question
  // data.totalQuestions: nombre total de questions
});

// Résultat d'une réponse
socket.on('quiz:answer_result', (data) => {
  // data.isCorrect: boolean
  // data.points: points gagnés
  // data.correctAnswer: bonne réponse
  // data.explanation: explication
});

// Quiz terminé
socket.on('quiz:finished', (data) => {
  // data.finalScore: score final
  // data.answers: toutes les réponses
});

// Classement mis à jour
socket.on('quiz:leaderboard', (data) => {
  // data.leaderboard: array des participants classés
});
```

## 🌐 Événements 3D

### Synchronisation de caméra

```javascript
// Envoyer la position de la caméra
socket.syncCamera3D({
  position: { x: 0, y: 5, z: 10 },
  rotation: { x: 0, y: 0, z: 0 }
});

// Recevoir les mises à jour de caméra
socket.on('3d:camera_sync', (data) => {
  // data.userId: ID de l'utilisateur
  // data.position: nouvelle position
  // data.rotation: nouvelle rotation
});
```

### Modèles 3D partagés

```javascript
// Charger un modèle partagé
socket.loadModel3D('/models/cube.glb', {
  name: 'Cube',
  shared: true
});

// Modèle chargé par un autre utilisateur
socket.on('3d:model_loaded', (data) => {
  // data.modelPath: chemin du modèle
  // data.loadedBy: ID de l'utilisateur qui l'a chargé
  // data.userName: nom de l'utilisateur
});
```

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env` :

```env
SOCKET_SERVER_URL=http://localhost:3001
SOCKET_DEBUG=true
QUIZ_TIME_LIMIT=30
MAX_PARTICIPANTS=50
```

### Configuration personnalisée

```javascript
import { getSocketConfig } from '@/config/socketConfig.js';

// Configuration pour développement
const config = getSocketConfig('development');

// Configuration pour production
const configProd = getSocketConfig('production');
```

## 🔧 Scripts NPM

```bash
# Démarrer uniquement le serveur Socket.IO
npm run socket-server

# Démarrer l'app complète avec Socket.IO
npm run web-with-socket

# Démarrer l'app sans Socket.IO
npm run web
```

## 🐛 Débogage

### Activer les logs détaillés

```javascript
const socket = useSocket();
socket.connect('http://localhost:3001', {
  debug: true
});
```

### Vérifier l'état de connexion

```javascript
const stats = socket.getConnectionStats();
console.log('Statistiques de connexion:', stats);

const status = socket.getConnectionStatus();
console.log('État de connexion:', status);
```

### Interface de débogage

Utilisez le composant `SocketDemo.vue` pour une interface complète de test :

```vue
<template>
  <SocketDemo />
</template>

<script setup>
import SocketDemo from '@/components/SocketDemo.vue';
</script>
```

## 📊 Monitoring

Le serveur expose une API REST pour le monitoring :

```bash
# État du serveur
curl http://localhost:3001/

# Statistiques détaillées
curl http://localhost:3001/status
```

## 🔐 Sécurité

### CORS
Le serveur est configuré pour accepter les connexions depuis :
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000`
- `http://127.0.0.1:5173`

### Validation des données
Toutes les données sont validées côté client et serveur :

```javascript
import { validateData } from '@/config/socketConfig.js';

// Valider un nom d'utilisateur
const isValid = validateData('userName', 'MonNom123');
```

## 🚀 Déploiement

### Pour un serveur de production

1. Modifier l'URL dans `socketConfig.js`
2. Configurer HTTPS/WSS
3. Ajouter l'authentification si nécessaire
4. Configurer un reverse proxy (nginx, Apache)

### Variables d'environnement production

```env
NODE_ENV=production
SOCKET_SERVER_URL=wss://your-domain.com
ALLOWED_ORIGINS=https://your-app.com
```

## 📚 Exemples complets

Voir le fichier `SocketDemo.vue` pour des exemples complets d'utilisation de toutes les fonctionnalités.

## 🤝 Contribution

Pour contribuer au développement :

1. Créer une branche pour votre fonctionnalité
2. Tester avec le serveur de développement
3. Documenter les nouvelles fonctionnalités
4. Soumettre une pull request

## 📞 Support

En cas de problème :

1. Vérifier que le serveur Socket.IO est démarré
2. Contrôler les logs du navigateur et du serveur
3. Tester avec le composant `SocketDemo.vue`
4. Vérifier la configuration réseau/firewall