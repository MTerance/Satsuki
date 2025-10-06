import { ref, onMounted, onUnmounted, computed } from 'vue';
import socketClient from '../services/socketClient.js';

export function useSocket() {
    // États réactifs
    const isConnected = computed(() => socketClient.isConnected.value);
    const connectionStatus = computed(() => socketClient.connectionStatus.value);
    const events = ref({});
    const listeners = ref(new Map());

    // Connecter au serveur Socket.IO
    const connect = (url = null, options = {}) => {
        try {
            return socketClient.connect(url, options);
        } catch (error) {
            console.error('Erreur de connexion Socket.IO:', error);
            throw error;
        }
    };

    // Déconnecter
    const disconnect = () => {
        socketClient.disconnect();
    };

    // Émettre un événement
    const emit = (event, data = {}) => {
        socketClient.emit(event, data);
    };

    // Écouter un événement avec nettoyage automatique
    const on = (event, callback) => {
        socketClient.on(event, callback);
        
        // Stocker le listener pour le nettoyage
        if (!listeners.value.has(event)) {
            listeners.value.set(event, []);
        }
        listeners.value.get(event).push(callback);
    };

    // Arrêter d'écouter un événement
    const off = (event, callback = null) => {
        socketClient.off(event, callback);
        
        if (callback && listeners.value.has(event)) {
            const eventListeners = listeners.value.get(event);
            const index = eventListeners.indexOf(callback);
            if (index > -1) {
                eventListeners.splice(index, 1);
            }
        }
    };

    // Rejoindre une room
    const joinRoom = (roomName, userData = {}) => {
        socketClient.joinRoom(roomName, userData);
    };

    // Quitter une room
    const leaveRoom = (roomName) => {
        socketClient.leaveRoom(roomName);
    };

    // Méthodes spécifiques au quiz 3D
    const quiz = {
        start: (quizId, userName) => {
            socketClient.startQuiz(quizId, userName);
        },
        
        submitAnswer: (questionId, answer, timeTaken) => {
            socketClient.submitAnswer(questionId, answer, timeTaken);
        },
        
        onStarted: (callback) => {
            on('quiz:started', callback);
        },
        
        onQuestion: (callback) => {
            on('quiz:question', callback);
        },
        
        onAnswerResult: (callback) => {
            on('quiz:answer_result', callback);
        },
        
        onFinished: (callback) => {
            on('quiz:finished', callback);
        },
        
        onLeaderboard: (callback) => {
            on('quiz:leaderboard', callback);
        }
    };

    // Méthodes pour la synchronisation 3D
    const sync3D = {
        camera: (cameraData) => {
            socketClient.syncCamera3D(cameraData);
        },
        
        loadModel: (modelPath, modelData) => {
            socketClient.loadModel3D(modelPath, modelData);
        },
        
        onCameraSync: (callback) => {
            on('3d:camera_sync', callback);
        },
        
        onModelLoaded: (callback) => {
            on('3d:model_loaded', callback);
        }
    };

    // Obtenir les statistiques de connexion
    const getConnectionStatus = () => {
        return socketClient.getConnectionStatus();
    };

    const getConnectionStats = () => {
        return socketClient.getConnectionStats();
    };

    // Configurer l'URL du serveur
    const setServerUrl = (url) => {
        socketClient.setServerUrl(url);
    };

    // Nettoyage automatique lors du démontage du composant
    onUnmounted(() => {
        // Nettoyer tous les listeners enregistrés
        for (const [event, callbacks] of listeners.value.entries()) {
            for (const callback of callbacks) {
                socketClient.off(event, callback);
            }
        }
        listeners.value.clear();
    });

    return {
        // États
        isConnected,
        connectionStatus,
        events,
        
        // Méthodes de base
        connect,
        disconnect,
        emit,
        on,
        off,
        joinRoom,
        leaveRoom,
        
        // Méthodes spécialisées
        quiz,
        sync3D,
        
        // Utilitaires
        getConnectionStatus,
        getConnectionStats,
        setServerUrl
    };
}

// Composable pour les événements de quiz spécifiquement
export function useQuizSocket() {
    const socket = useSocket();
    
    const quizState = ref({
        currentQuiz: null,
        currentQuestion: null,
        participants: [],
        leaderboard: [],
        userAnswers: [],
        isActive: false
    });

    // Démarrer un quiz
    const startQuiz = async (quizId, userName) => {
        socket.quiz.start(quizId, userName);
        quizState.value.isActive = true;
    };

    // Soumettre une réponse
    const submitAnswer = (questionId, answer, timeTaken) => {
        socket.quiz.submitAnswer(questionId, answer, timeTaken);
        
        // Ajouter la réponse à l'historique local
        quizState.value.userAnswers.push({
            questionId,
            answer,
            timeTaken,
            timestamp: new Date()
        });
    };

    // Configurer les écouteurs d'événements du quiz
    onMounted(() => {
        socket.quiz.onStarted((data) => {
            quizState.value.currentQuiz = data.quiz;
            quizState.value.isActive = true;
            console.log('Quiz démarré:', data);
        });

        socket.quiz.onQuestion((data) => {
            quizState.value.currentQuestion = data.question;
            console.log('Nouvelle question:', data);
        });

        socket.quiz.onAnswerResult((data) => {
            console.log('Résultat de la réponse:', data);
            // Mettre à jour l'état local avec le résultat
            const lastAnswer = quizState.value.userAnswers[quizState.value.userAnswers.length - 1];
            if (lastAnswer) {
                lastAnswer.result = data;
            }
        });

        socket.quiz.onFinished((data) => {
            quizState.value.isActive = false;
            quizState.value.currentQuestion = null;
            console.log('Quiz terminé:', data);
        });

        socket.quiz.onLeaderboard((data) => {
            quizState.value.leaderboard = data.leaderboard;
            console.log('Leaderboard mis à jour:', data);
        });

        // Écouter les événements des participants
        socket.on('participant:joined', (data) => {
            quizState.value.participants.push(data.participant);
        });

        socket.on('participant:left', (data) => {
            const index = quizState.value.participants.findIndex(p => p.id === data.participant.id);
            if (index > -1) {
                quizState.value.participants.splice(index, 1);
            }
        });
    });

    return {
        ...socket,
        quizState,
        startQuiz,
        submitAnswer
    };
}

// Composable pour la synchronisation 3D
export function use3DSync() {
    const socket = useSocket();
    
    const sync3DState = ref({
        connectedUsers: [],
        sharedCamera: null,
        loadedModels: [],
        interactions: []
    });

    // Synchroniser la caméra 3D
    const syncCamera = (position, rotation, zoom = 1) => {
        const cameraData = {
            position: { x: position.x, y: position.y, z: position.z },
            rotation: { x: rotation.x, y: rotation.y, z: rotation.z },
            zoom,
            timestamp: Date.now()
        };
        
        socket.sync3D.camera(cameraData);
    };

    // Charger un modèle 3D partagé
    const loadSharedModel = (modelPath, metadata = {}) => {
        const modelData = {
            path: modelPath,
            metadata,
            loadedBy: socket.getConnectionStatus().socketId,
            timestamp: Date.now()
        };
        
        socket.sync3D.loadModel(modelPath, modelData);
    };

    // Configurer les écouteurs 3D
    onMounted(() => {
        socket.sync3D.onCameraSync((data) => {
            sync3DState.value.sharedCamera = data;
            console.log('Caméra synchronisée:', data);
        });

        socket.sync3D.onModelLoaded((data) => {
            sync3DState.value.loadedModels.push(data);
            console.log('Modèle 3D chargé:', data);
        });
    });

    return {
        ...socket,
        sync3DState,
        syncCamera,
        loadSharedModel
    };
}