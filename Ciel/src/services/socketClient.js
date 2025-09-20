import { io } from 'socket.io-client';
import { ref, reactive } from 'vue';

class SocketClient {
    constructor() {
        this.socket = null;
        this.isConnected = ref(false);
        this.connectionStatus = ref('disconnected');
        this.events = reactive({});
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        
        // Configuration par défaut
        this.config = {
            url: 'http://localhost:3001',
            options: {
                autoConnect: false,
                reconnection: true,
                reconnectionDelay: 1000,
                reconnectionDelayMax: 5000,
                maxReconnectionAttempts: 5,
                timeout: 20000,
                forceNew: true
            }
        };
    }

    // Initialiser la connexion Socket.IO
    connect(url = null, options = {}) {
        try {
            const serverUrl = url || this.config.url;
            const socketOptions = { ...this.config.options, ...options };
            
            console.log(`Tentative de connexion au serveur Socket.IO: ${serverUrl}`);
            
            this.socket = io(serverUrl, socketOptions);
            
            this.setupEventListeners();
            this.socket.connect();
            
            return this.socket;
        } catch (error) {
            console.error('Erreur lors de la connexion Socket.IO:', error);
            this.connectionStatus.value = 'error';
            throw error;
        }
    }

    // Configurer les écouteurs d'événements de base
    setupEventListeners() {
        if (!this.socket) return;

        // Événements de connexion
        this.socket.on('connect', () => {
            console.log('✅ Connecté au serveur Socket.IO');
            this.isConnected.value = true;
            this.connectionStatus.value = 'connected';
            this.reconnectAttempts = 0;
            this.emit('client:connected', { socketId: this.socket.id });
        });

        this.socket.on('disconnect', (reason) => {
            console.log('❌ Déconnecté du serveur Socket.IO:', reason);
            this.isConnected.value = false;
            this.connectionStatus.value = 'disconnected';
            this.emit('client:disconnected', { reason });
        });

        this.socket.on('connect_error', (error) => {
            console.error('❌ Erreur de connexion Socket.IO:', error);
            this.connectionStatus.value = 'error';
            this.handleReconnection();
        });

        // Événements de reconnexion
        this.socket.on('reconnect', (attemptNumber) => {
            console.log(`✅ Reconnecté après ${attemptNumber} tentatives`);
            this.isConnected.value = true;
            this.connectionStatus.value = 'connected';
            this.reconnectAttempts = 0;
        });

        this.socket.on('reconnect_attempt', (attemptNumber) => {
            console.log(`🔄 Tentative de reconnexion #${attemptNumber}`);
            this.connectionStatus.value = 'reconnecting';
        });

        this.socket.on('reconnect_error', (error) => {
            console.error('❌ Erreur de reconnexion:', error);
            this.connectionStatus.value = 'error';
        });

        this.socket.on('reconnect_failed', () => {
            console.error('❌ Échec de toutes les tentatives de reconnexion');
            this.connectionStatus.value = 'failed';
        });

        // Événements personnalisés pour le quiz 3D
        this.setupQuiz3DEvents();
    }

    // Événements spécifiques au quiz 3D
    setupQuiz3DEvents() {
        if (!this.socket) return;

        // Événements du quiz
        this.socket.on('quiz:started', (data) => {
            console.log('Quiz démarré:', data);
            this.emit('quiz:started', data);
        });

        this.socket.on('quiz:question', (data) => {
            console.log('Nouvelle question reçue:', data);
            this.emit('quiz:question', data);
        });

        this.socket.on('quiz:answer_result', (data) => {
            console.log('Résultat de la réponse:', data);
            this.emit('quiz:answer_result', data);
        });

        this.socket.on('quiz:finished', (data) => {
            console.log('Quiz terminé:', data);
            this.emit('quiz:finished', data);
        });

        this.socket.on('quiz:leaderboard', (data) => {
            console.log('Leaderboard mis à jour:', data);
            this.emit('quiz:leaderboard', data);
        });

        // Événements des participants
        this.socket.on('participant:joined', (data) => {
            console.log('Nouveau participant:', data);
            this.emit('participant:joined', data);
        });

        this.socket.on('participant:left', (data) => {
            console.log('Participant parti:', data);
            this.emit('participant:left', data);
        });

        // Événements 3D
        this.socket.on('3d:model_loaded', (data) => {
            console.log('Modèle 3D chargé:', data);
            this.emit('3d:model_loaded', data);
        });

        this.socket.on('3d:camera_sync', (data) => {
            console.log('Synchronisation caméra 3D:', data);
            this.emit('3d:camera_sync', data);
        });
    }

    // Gérer la reconnexion manuelle
    handleReconnection() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`🔄 Tentative de reconnexion ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
            
            setTimeout(() => {
                if (this.socket && !this.isConnected.value) {
                    this.socket.connect();
                }
            }, this.reconnectDelay * this.reconnectAttempts);
        } else {
            console.error('❌ Nombre maximum de tentatives de reconnexion atteint');
            this.connectionStatus.value = 'failed';
        }
    }

    // Émettre un événement
    emit(event, data = {}) {
        if (this.socket && this.isConnected.value) {
            this.socket.emit(event, data);
            console.log(`📤 Événement émis: ${event}`, data);
        } else {
            console.warn(`⚠️ Impossible d'émettre l'événement ${event}: socket non connecté`);
        }
    }

    // Écouter un événement
    on(event, callback) {
        if (this.socket) {
            this.socket.on(event, callback);
            console.log(`👂 Écoute de l'événement: ${event}`);
        }
    }

    // Arrêter d'écouter un événement
    off(event, callback = null) {
        if (this.socket) {
            if (callback) {
                this.socket.off(event, callback);
            } else {
                this.socket.off(event);
            }
            console.log(`🔇 Arrêt de l'écoute: ${event}`);
        }
    }

    // Rejoindre une room
    joinRoom(roomName, userData = {}) {
        this.emit('join_room', { 
            room: roomName, 
            user: userData,
            timestamp: new Date().toISOString()
        });
    }

    // Quitter une room
    leaveRoom(roomName) {
        this.emit('leave_room', { 
            room: roomName,
            timestamp: new Date().toISOString()
        });
    }

    // Méthodes spécifiques au quiz 3D
    startQuiz(quizId, userName) {
        this.emit('quiz:start', {
            quizId,
            userName,
            timestamp: new Date().toISOString()
        });
    }

    submitAnswer(questionId, answer, timeTaken) {
        this.emit('quiz:submit_answer', {
            questionId,
            answer,
            timeTaken,
            timestamp: new Date().toISOString()
        });
    }

    syncCamera3D(cameraData) {
        this.emit('3d:sync_camera', {
            position: cameraData.position,
            rotation: cameraData.rotation,
            timestamp: new Date().toISOString()
        });
    }

    loadModel3D(modelPath, modelData) {
        this.emit('3d:load_model', {
            modelPath,
            modelData,
            timestamp: new Date().toISOString()
        });
    }

    // Déconnecter le socket
    disconnect() {
        if (this.socket) {
            console.log('🔌 Déconnexion du serveur Socket.IO');
            this.socket.disconnect();
            this.isConnected.value = false;
            this.connectionStatus.value = 'disconnected';
        }
    }

    // Obtenir l'état de la connexion
    getConnectionStatus() {
        return {
            isConnected: this.isConnected.value,
            status: this.connectionStatus.value,
            socketId: this.socket?.id || null,
            reconnectAttempts: this.reconnectAttempts
        };
    }

    // Configurer l'URL du serveur
    setServerUrl(url) {
        this.config.url = url;
    }

    // Obtenir les statistiques de connexion
    getConnectionStats() {
        if (!this.socket) return null;

        return {
            connected: this.socket.connected,
            id: this.socket.id,
            transport: this.socket.io.engine?.transport?.name,
            upgraded: this.socket.io.engine?.upgraded,
            readyState: this.socket.io.engine?.readyState
        };
    }
}

// Créer une instance singleton
const socketClient = new SocketClient();

// Exporter l'instance et la classe
export default socketClient;
export { SocketClient };