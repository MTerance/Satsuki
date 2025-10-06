<template>
  <div class="socket-demo-container">
    <div class="connection-status">
      <h2>État de la connexion Socket.IO</h2>
      <div class="status-indicator" :class="connectionStatusClass">
        <span class="status-dot"></span>
        <span class="status-text">{{ connectionStatusText }}</span>
      </div>
      <div class="connection-info" v-if="connectionStats">
        <p><strong>Socket ID:</strong> {{ connectionStats.id || 'Non connecté' }}</p>
        <p><strong>Transport:</strong> {{ connectionStats.transport || 'N/A' }}</p>
        <p><strong>Upgraded:</strong> {{ connectionStats.upgraded ? 'Oui' : 'Non' }}</p>
      </div>
    </div>

    <div class="connection-controls">
      <h3>Contrôles de connexion</h3>
      <div class="controls-group">
        <input 
          v-model="serverUrl" 
          placeholder="URL du serveur (ex: http://localhost:3001)"
          class="url-input"
        />
        <button @click="handleConnect" :disabled="isConnected" class="btn btn-connect">
          Se connecter
        </button>
        <button @click="handleDisconnect" :disabled="!isConnected" class="btn btn-disconnect">
          Se déconnecter
        </button>
      </div>
    </div>

    <div class="quiz-controls" v-if="isConnected">
      <h3>Contrôles du Quiz 3D</h3>
      <div class="quiz-section">
        <div class="quiz-join">
          <input 
            v-model="userName" 
            placeholder="Votre nom"
            class="name-input"
          />
          <input 
            v-model="quizId" 
            placeholder="ID du quiz"
            class="quiz-input"
          />
          <button @click="startQuiz" class="btn btn-quiz">
            Rejoindre le quiz
          </button>
        </div>

        <div class="quiz-state" v-if="quizState.isActive">
          <h4>Quiz en cours</h4>
          <div class="current-question" v-if="quizState.currentQuestion">
            <h5>Question actuelle:</h5>
            <p>{{ quizState.currentQuestion.text }}</p>
            <div class="question-options" v-if="quizState.currentQuestion.options">
              <button 
                v-for="(option, index) in quizState.currentQuestion.options"
                :key="index"
                @click="submitAnswer(quizState.currentQuestion.id, option)"
                class="option-btn"
              >
                {{ option }}
              </button>
            </div>
          </div>

          <div class="participants" v-if="quizState.participants.length > 0">
            <h5>Participants ({{ quizState.participants.length }}):</h5>
            <ul>
              <li v-for="participant in quizState.participants" :key="participant.id">
                {{ participant.name }}
              </li>
            </ul>
          </div>

          <div class="leaderboard" v-if="quizState.leaderboard.length > 0">
            <h5>Classement:</h5>
            <ol>
              <li v-for="player in quizState.leaderboard" :key="player.id">
                {{ player.name }} - {{ player.score }} points
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>

    <div class="sync-3d-controls" v-if="isConnected">
      <h3>Synchronisation 3D</h3>
      <div class="sync-section">
        <div class="camera-sync">
          <h4>Synchronisation de caméra</h4>
          <div class="camera-controls">
            <div class="position-controls">
              <label>Position:</label>
              <input v-model.number="cameraPosition.x" placeholder="X" type="number" step="0.1" />
              <input v-model.number="cameraPosition.y" placeholder="Y" type="number" step="0.1" />
              <input v-model.number="cameraPosition.z" placeholder="Z" type="number" step="0.1" />
            </div>
            <div class="rotation-controls">
              <label>Rotation:</label>
              <input v-model.number="cameraRotation.x" placeholder="RX" type="number" step="0.1" />
              <input v-model.number="cameraRotation.y" placeholder="RY" type="number" step="0.1" />
              <input v-model.number="cameraRotation.z" placeholder="RZ" type="number" step="0.1" />
            </div>
            <button @click="syncCameraPosition" class="btn btn-sync">
              Synchroniser caméra
            </button>
          </div>
        </div>

        <div class="model-sync">
          <h4>Modèles 3D partagés</h4>
          <div class="model-controls">
            <input 
              v-model="modelPath" 
              placeholder="Chemin du modèle 3D"
              class="model-input"
            />
            <button @click="loadSharedModel" class="btn btn-load">
              Charger modèle partagé
            </button>
          </div>
          <div class="loaded-models" v-if="sync3DState.loadedModels.length > 0">
            <h5>Modèles chargés:</h5>
            <ul>
              <li v-for="model in sync3DState.loadedModels" :key="model.timestamp">
                {{ model.path }} (par {{ model.loadedBy }})
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="events-log">
      <h3>Journal des événements</h3>
      <div class="log-container">
        <div 
          v-for="(event, index) in eventLog" 
          :key="index"
          class="log-entry"
          :class="event.type"
        >
          <span class="timestamp">{{ formatTime(event.timestamp) }}</span>
          <span class="event-type">{{ event.event }}</span>
          <span class="event-data">{{ event.data }}</span>
        </div>
      </div>
      <button @click="clearLog" class="btn btn-clear">Vider le journal</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useQuizSocket, use3DSync } from '../composables/useSocket.js';

// Utiliser les composables
const quizSocket = useQuizSocket();
const sync3D = use3DSync();

// États locaux
const serverUrl = ref('http://localhost:3001');
const userName = ref('');
const quizId = ref('');
const modelPath = ref('/models/example.glb');
const eventLog = ref([]);

// Caméra 3D
const cameraPosition = ref({ x: 0, y: 0, z: 5 });
const cameraRotation = ref({ x: 0, y: 0, z: 0 });

// États calculés
const isConnected = computed(() => quizSocket.isConnected.value);
const connectionStatus = computed(() => quizSocket.connectionStatus.value);
const quizState = computed(() => quizSocket.quizState.value);
const sync3DState = computed(() => sync3D.sync3DState.value);

const connectionStatusClass = computed(() => {
  return {
    'status-connected': connectionStatus.value === 'connected',
    'status-connecting': connectionStatus.value === 'reconnecting',
    'status-disconnected': connectionStatus.value === 'disconnected',
    'status-error': connectionStatus.value === 'error'
  };
});

const connectionStatusText = computed(() => {
  const statusMap = {
    'connected': 'Connecté',
    'disconnected': 'Déconnecté',
    'reconnecting': 'Reconnexion...',
    'error': 'Erreur',
    'failed': 'Échec'
  };
  return statusMap[connectionStatus.value] || 'Inconnu';
});

const connectionStats = computed(() => quizSocket.getConnectionStats());

// Méthodes de connexion
const handleConnect = () => {
  try {
    quizSocket.setServerUrl(serverUrl.value);
    quizSocket.connect();
    addLogEntry('info', 'connect_attempt', `Tentative de connexion à ${serverUrl.value}`);
  } catch (error) {
    addLogEntry('error', 'connect_error', error.message);
  }
};

const handleDisconnect = () => {
  quizSocket.disconnect();
  addLogEntry('info', 'disconnect', 'Déconnexion manuelle');
};

// Méthodes du quiz
const startQuiz = () => {
  if (userName.value && quizId.value) {
    quizSocket.startQuiz(quizId.value, userName.value);
    addLogEntry('info', 'quiz_start', `Démarrage du quiz ${quizId.value} pour ${userName.value}`);
  }
};

const submitAnswer = (questionId, answer) => {
  const timeTaken = Math.floor(Math.random() * 30) + 5; // Simulation du temps
  quizSocket.submitAnswer(questionId, answer, timeTaken);
  addLogEntry('info', 'answer_submit', `Réponse: ${answer} en ${timeTaken}s`);
};

// Méthodes de synchronisation 3D
const syncCameraPosition = () => {
  sync3D.syncCamera(cameraPosition.value, cameraRotation.value);
  addLogEntry('info', '3d_camera_sync', `Position: ${JSON.stringify(cameraPosition.value)}`);
};

const loadSharedModel = () => {
  if (modelPath.value) {
    sync3D.loadSharedModel(modelPath.value, { shared: true });
    addLogEntry('info', '3d_model_load', `Modèle: ${modelPath.value}`);
  }
};

// Utilitaires
const addLogEntry = (type, event, data) => {
  eventLog.value.unshift({
    type,
    event,
    data,
    timestamp: new Date()
  });
  
  // Limiter le journal à 50 entrées
  if (eventLog.value.length > 50) {
    eventLog.value = eventLog.value.slice(0, 50);
  }
};

const clearLog = () => {
  eventLog.value = [];
};

const formatTime = (timestamp) => {
  return timestamp.toLocaleTimeString();
};

// Configuration des écouteurs d'événements
onMounted(() => {
  // Écouter tous les événements pour le journal
  const logEvents = [
    'connect', 'disconnect', 'connect_error', 'reconnect',
    'quiz:started', 'quiz:question', 'quiz:answer_result', 'quiz:finished',
    'participant:joined', 'participant:left',
    '3d:camera_sync', '3d:model_loaded'
  ];

  logEvents.forEach(event => {
    quizSocket.on(event, (data) => {
      addLogEntry('event', event, JSON.stringify(data));
    });
  });
});
</script>

<style scoped>
.socket-demo-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.connection-status {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #dc3545;
}

.status-connected .status-dot {
  background: #28a745;
}

.status-connecting .status-dot {
  background: #ffc107;
  animation: pulse 1s infinite;
}

.status-error .status-dot {
  background: #dc3545;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.connection-info {
  background: white;
  padding: 10px;
  border-radius: 4px;
  font-size: 14px;
}

.controls-group {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.url-input, .name-input, .quiz-input, .model-input {
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
}

.url-input {
  min-width: 300px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-connect {
  background: #28a745;
  color: white;
}

.btn-connect:hover:not(:disabled) {
  background: #218838;
}

.btn-disconnect {
  background: #dc3545;
  color: white;
}

.btn-quiz, .btn-sync, .btn-load {
  background: #007bff;
  color: white;
}

.btn-clear {
  background: #6c757d;
  color: white;
}

.quiz-controls, .sync-3d-controls {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.quiz-section, .sync-section {
  display: grid;
  gap: 20px;
}

.option-btn {
  background: #e9ecef;
  border: 1px solid #ced4da;
  padding: 10px 15px;
  margin: 5px;
  border-radius: 4px;
  cursor: pointer;
}

.option-btn:hover {
  background: #dee2e6;
}

.camera-controls {
  display: grid;
  gap: 10px;
}

.position-controls, .rotation-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.position-controls input, .rotation-controls input {
  width: 80px;
}

.events-log {
  background: #343a40;
  color: white;
  border-radius: 8px;
  padding: 20px;
}

.log-container {
  max-height: 300px;
  overflow-y: auto;
  background: #212529;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
}

.log-entry {
  display: flex;
  gap: 10px;
  padding: 4px 0;
  border-bottom: 1px solid #495057;
  font-family: monospace;
  font-size: 12px;
}

.log-entry.error {
  color: #ff6b6b;
}

.log-entry.info {
  color: #74c0fc;
}

.log-entry.event {
  color: #51cf66;
}

.timestamp {
  color: #adb5bd;
  min-width: 80px;
}

.event-type {
  color: #ffd43b;
  min-width: 120px;
}

.event-data {
  color: #e9ecef;
  word-break: break-all;
}
</style>