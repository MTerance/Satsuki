<template>
    <nav class="navbar-primary">
        <div class="container">
            <div class="navbar-left">
                <h1 class="title-gradient">Status Bar</h1>
            </div>
            
            <div class="navbar-right">
                <!-- Témoin de connexion Socket.IO -->
                <div class="status-indicator" :class="connectionClass">
                    <div class="status-dot" :class="statusDotClass"></div>
                    <span class="status-text">{{ connectionText }}</span>
                </div>
                
                <!-- Bouton de connexion/déconnexion -->
                <button 
                    v-if="!isConnected" 
                    @click="handleConnect"
                    class="btn-base btn-success"
                    :disabled="isConnecting"
                >
                    {{ isConnecting ? 'Connexion...' : 'Se connecter' }}
                </button>
                <button 
                    v-else 
                    @click="handleDisconnect" 
                    class="btn-base btn-danger"
                >
                    Se déconnecter
                </button>
            </div>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { computed, watch, onMounted, onUnmounted } from 'vue';
import socketClient from '../services/socketClient.js';

// États réactifs délégués au service SocketClient (singleton partagé)
const isConnected = socketClient.isConnected;
const connectionStatus = socketClient.connectionStatus;
const isConnecting = computed(() =>
    connectionStatus.value === 'connecting' || connectionStatus.value === 'reconnecting'
);

// Événements serveur retransmis vers les autres composants via 'socket-response'
const SERVER_EVENTS: string[] = [
    'welcome',
    'player_added_response',
    'player_removed_response',
    'quiz_added_response',
    'quiz_removed_response',
    'players_list'
];

// Classes CSS dynamiques
const connectionClass = computed(() => ({
    'connected': isConnected.value,
    'disconnected': !isConnected.value && !isConnecting.value,
    'connecting': isConnecting.value
}));

const statusDotClass = computed(() => ({
    'dot-connected': isConnected.value,
    'dot-disconnected': !isConnected.value && !isConnecting.value,
    'dot-connecting': isConnecting.value
}));

// Texte du statut
const connectionText = computed(() => {
    if (isConnecting.value) return 'Connexion...';
    return isConnected.value ? 'Connecté' : 'Non connecté';
});

// Connexion / déconnexion déléguées au service SocketClient
const handleConnect = () => {
    if (isConnected.value || isConnecting.value) return;

    try {
        socketClient.connect();
        registerServerEventListeners();
    } catch (error) {
        console.error('Erreur de connexion Socket.IO:', error);
    }
};

const handleDisconnect = () => {
    socketClient.disconnect();
};

// Abonne le socket aux événements du serveur et les retransmet aux autres composants
const registerServerEventListeners = () => {
    for (const eventName of SERVER_EVENTS) {
        socketClient.on(eventName, (data: unknown) => {
            console.log(`📨 Événement serveur reçu: ${eventName}`, data);
            window.dispatchEvent(new CustomEvent('socket-response', {
                detail: { eventName, data }
            }));
        });
    }
};

// Transfère les événements de jeu (MainGameMenu) vers le serveur au format OrderRequest
const handleGameSocketEmit = (event: CustomEvent) => {
    const { eventName, data } = event.detail;

    if (isConnected.value) {
        console.log(`🎮 Envoi d'un ordre au serveur: ${eventName}`, data);
        socketClient.sendOrder(eventName, data);
    } else {
        console.warn('⚠️ Socket non connecté, impossible de transférer:', eventName, data);
    }
};

// Diffuse le statut de connexion vers les autres composants
watch(isConnected, (connected) => {
    window.dispatchEvent(new CustomEvent('socket-status-change', {
        detail: { connected }
    }));
});

// Configuration au montage
onMounted(() => {
    // Écouter les événements de jeu depuis MainGameMenu
    window.addEventListener('game-socket-emit', handleGameSocketEmit as EventListener);

    // Tentative de connexion automatique au démarrage
    setTimeout(() => {
        handleConnect();
    }, 1000);
});

// Nettoyage au démontage
onUnmounted(() => {
    window.removeEventListener('game-socket-emit', handleGameSocketEmit as EventListener);
    // Le socket est un singleton partagé : on ne le déconnecte pas ici.
});
</script>

<style scoped>
/* ========== STYLES SPÉCIFIQUES À MAINSTATUSNAVBAR ========== */

.navbar-left {
    flex: 1;
}

.navbar-right {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
}

/* ========== INDICATEUR DE STATUT ========== */
.status-indicator {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-xs) var(--spacing-md);
    border-radius: var(--border-radius-pill);
    font-size: 0.875rem;
    font-weight: 600;
    transition: all var(--transition-normal);
    min-width: 130px;
    justify-content: center;
    border: 2px solid;
}

.status-indicator.connected {
    background: rgba(34, 197, 94, 0.2);
    border-color: var(--color-success);
    color: var(--color-success);
    box-shadow: 0 0 10px rgba(34, 197, 94, 0.3);
}

.status-indicator.disconnected {
    background: rgba(239, 68, 68, 0.2);
    border-color: var(--color-danger);
    color: var(--color-danger);
    box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
}

.status-indicator.connecting {
    background: rgba(251, 191, 36, 0.2);
    border-color: var(--color-warning);
    color: var(--color-warning);
    box-shadow: 0 0 10px rgba(251, 191, 36, 0.3);
}

/* ========== POINTS DE STATUT ========== */
.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    transition: all var(--transition-normal);
}

.status-dot.dot-connected {
    background: var(--color-success);
    box-shadow: 0 0 8px rgba(34, 197, 94, 0.6);
}

.status-dot.dot-disconnected {
    background: var(--color-danger);
    box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
}

.status-dot.dot-connecting {
    background: var(--color-warning);
    box-shadow: 0 0 8px rgba(251, 191, 36, 0.6);
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
        opacity: 1;
    }
    50% {
        transform: scale(1.2);
        opacity: 0.7;
    }
}

.status-text {
    font-weight: 600;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
    .container {
        flex-direction: column;
        gap: var(--spacing-sm);
        align-items: stretch;
    }
    
    .navbar-right {
        justify-content: space-between;
    }
    
    .status-indicator {
        min-width: auto;
        flex: 1;
    }
    
    .btn-base {
        min-width: auto;
        flex: 1;
    }
}

@media (max-width: 480px) {
    .navbar-primary {
        padding: var(--spacing-xs) var(--spacing-md);
    }
    
    .title-gradient {
        font-size: 1rem;
    }
    
    .status-indicator, .btn-base {
        font-size: 0.75rem;
        padding: 0.4rem 0.8rem;
    }
}
</style>