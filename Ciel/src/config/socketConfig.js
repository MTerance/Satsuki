// Configuration Socket.IO pour l'application
export const socketConfig = {
    // URL du serveur Socket.IO
    serverUrl: 'http://localhost:3001',
    
    // Options de connexion Socket.IO
    options: {
        autoConnect: false,
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        maxReconnectionAttempts: 5,
        timeout: 20000,
        forceNew: true,
        transports: ['websocket', 'polling']
    },

    // Configuration pour différents environnements
    environments: {
        development: {
            serverUrl: 'http://localhost:3001',
            debug: true
        },
        production: {
            serverUrl: 'wss://your-production-server.com',
            debug: false
        },
        staging: {
            serverUrl: 'wss://staging-server.com',
            debug: true
        }
    },

    // Événements personnalisés pour le quiz 3D
    events: {
        // Événements de connexion
        CONNECTION: {
            CONNECT: 'connect',
            DISCONNECT: 'disconnect',
            CONNECT_ERROR: 'connect_error',
            RECONNECT: 'reconnect',
            RECONNECT_ATTEMPT: 'reconnect_attempt',
            RECONNECT_ERROR: 'reconnect_error',
            RECONNECT_FAILED: 'reconnect_failed'
        },

        // Événements de quiz
        QUIZ: {
            START: 'quiz:start',
            STARTED: 'quiz:started',
            QUESTION: 'quiz:question',
            SUBMIT_ANSWER: 'quiz:submit_answer',
            ANSWER_RESULT: 'quiz:answer_result',
            FINISHED: 'quiz:finished',
            LEADERBOARD: 'quiz:leaderboard',
            ERROR: 'quiz:error'
        },

        // Événements des participants
        PARTICIPANT: {
            JOINED: 'participant:joined',
            LEFT: 'participant:left'
        },

        // Événements 3D
        THREED: {
            SYNC_CAMERA: '3d:sync_camera',
            CAMERA_SYNC: '3d:camera_sync',
            LOAD_MODEL: '3d:load_model',
            MODEL_LOADED: '3d:model_loaded'
        },

        // Événements de room
        ROOM: {
            JOIN: 'join_room',
            LEAVE: 'leave_room'
        },

        // Événements client
        CLIENT: {
            CONNECTED: 'client:connected',
            DISCONNECTED: 'client:disconnected'
        }
    },

    // Configuration des rooms
    rooms: {
        quiz: (quizId) => `quiz_${quizId}`,
        sync3d: (sessionId) => `sync3d_${sessionId}`,
        general: 'general_room'
    },

    // Paramètres du quiz
    quiz: {
        defaultTimeLimit: 30, // secondes
        maxParticipants: 50,
        minParticipants: 1,
        autoStartDelay: 5000, // ms
        questionDelay: 2000, // ms entre les questions
        resultsDisplayTime: 5000 // ms
    },

    // Paramètres de synchronisation 3D
    sync3D: {
        cameraUpdateInterval: 100, // ms
        modelSyncTimeout: 5000, // ms
        maxModelsPerSession: 10,
        supportedFormats: ['.glb', '.gltf', '.obj', '.fbx']
    },

    // Messages d'erreur
    errorMessages: {
        CONNECTION_FAILED: 'Impossible de se connecter au serveur',
        QUIZ_NOT_FOUND: 'Quiz introuvable',
        INVALID_ANSWER: 'Réponse invalide',
        TIMEOUT: 'Délai de connexion dépassé',
        MAX_PARTICIPANTS: 'Nombre maximum de participants atteint',
        UNAUTHORIZED: 'Non autorisé'
    },

    // Messages de succès
    successMessages: {
        CONNECTED: 'Connexion établie avec succès',
        QUIZ_JOINED: 'Quiz rejoint avec succès',
        ANSWER_SUBMITTED: 'Réponse envoyée',
        MODEL_LOADED: 'Modèle 3D chargé'
    },

    // Validation
    validation: {
        userName: {
            minLength: 2,
            maxLength: 20,
            pattern: /^[a-zA-Z0-9_-]+$/
        },
        quizId: {
            pattern: /^[a-zA-Z0-9-]+$/
        },
        modelPath: {
            pattern: /\.(glb|gltf|obj|fbx)$/i
        }
    }
};

// Fonction pour obtenir la configuration selon l'environnement
export function getSocketConfig(environment = 'development') {
    const baseConfig = { ...socketConfig };
    const envConfig = socketConfig.environments[environment];
    
    if (envConfig) {
        baseConfig.serverUrl = envConfig.serverUrl;
        baseConfig.options.debug = envConfig.debug;
    }
    
    return baseConfig;
}

// Fonction pour valider les données
export function validateData(type, value) {
    const validation = socketConfig.validation[type];
    if (!validation) return true;
    
    if (validation.minLength && value.length < validation.minLength) return false;
    if (validation.maxLength && value.length > validation.maxLength) return false;
    if (validation.pattern && !validation.pattern.test(value)) return false;
    
    return true;
}

// Fonction pour formater les messages d'erreur
export function getErrorMessage(errorType) {
    return socketConfig.errorMessages[errorType] || 'Erreur inconnue';
}

// Fonction pour formater les messages de succès
export function getSuccessMessage(successType) {
    return socketConfig.successMessages[successType] || 'Opération réussie';
}

// Export par défaut
export default socketConfig;