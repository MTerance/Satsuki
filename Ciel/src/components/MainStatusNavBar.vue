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
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { io, type Socket } from 'socket.io-client';

// Types
type ConnectionStatus = 'disconnected' | 'connecting' | 'connected' | 'error' | 'reconnecting';

// États locaux
const socket = ref<Socket | null>(null);
const isConnected = ref<boolean>(false);
const isConnecting = ref<boolean>(false);
const connectionStatus = ref<ConnectionStatus>('disconnected');

// Configuration
const SERVER_URL: string = 'http://localhost:3002';

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

// Méthodes de connexion
const handleConnect = async () => {
    try {
        isConnecting.value = true;
        connectionStatus.value = 'connecting';
        
        // Créer la connexion Socket.IO
        socket.value = io(SERVER_URL, {
            autoConnect: false,
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            reconnectionAttempts: 5,
            timeout: 20000
        });
        
        // Configurer les écouteurs d'événements
        setupSocketListeners();
        
        // Se connecter
        socket.value.connect();
        
    } catch (error) {
        console.error('Erreur de connexion Socket.IO:', error);
        isConnecting.value = false;
        connectionStatus.value = 'error';
    }
};

const handleDisconnect = () => {
    if (socket.value) {
        socket.value.disconnect();
        socket.value = null;
    }
    isConnected.value = false;
    isConnecting.value = false;
    connectionStatus.value = 'disconnected';
};

const setupSocketListeners = () => {
    if (!socket.value) return;
    
    socket.value.on('connect', () => {
        console.log('✅ Socket.IO connecté:', socket?.value?.id);
        isConnected.value = true;
        isConnecting.value = false;
        connectionStatus.value = 'connected';
        broadcastConnectionStatus();
    });
    
    socket.value.on('disconnect', (reason) => {
        console.log('❌ Socket.IO déconnecté:', reason);
        isConnected.value = false;
        isConnecting.value = false;
        connectionStatus.value = 'disconnected';
        broadcastConnectionStatus();
    });
    
    socket.value.on('connect_error', (error) => {
        console.error('❌ Erreur de connexion Socket.IO:', error);
        isConnected.value = false;
        isConnecting.value = false;
        connectionStatus.value = 'error';
        broadcastConnectionStatus();
    });
    
    socket.value.on('reconnect', (attemptNumber) => {
        console.log(`✅ Reconnecté après ${attemptNumber} tentatives`);
        isConnected.value = true;
        isConnecting.value = false;
        connectionStatus.value = 'connected';
        broadcastConnectionStatus();
    });
    
    socket.value.on('reconnect_attempt', (attemptNumber) => {
        console.log(`🔄 Tentative de reconnexion #${attemptNumber}`);
        isConnecting.value = true;
        connectionStatus.value = 'reconnecting';
    });
    
    socket.value.on('welcome', (data) => {
        console.log('📨 Message de bienvenue:', data);
    });
    
    // Écouter les événements de jeu depuis les autres composants
    socket.value.on('player_added_confirmed', (data) => {
        console.log('🎮 Joueur ajouté confirmé:', data);
        // Diffuser l'événement vers les autres composants
        window.dispatchEvent(new CustomEvent('socket-response', {
            detail: { eventName: 'player_added_confirmed', data }
        }));
    });
    
    socket.value.on('player_removed_confirmed', (data) => {
        console.log('🎮 Joueur supprimé confirmé:', data);
        // Diffuser l'événement vers les autres composants
        window.dispatchEvent(new CustomEvent('socket-response', {
            detail: { eventName: 'player_removed_confirmed', data }
        }));
    });
    
    socket.value.on('player_list_updated', (data) => {
        console.log('🎮 Liste des joueurs mise à jour:', data);
        // Diffuser l'événement vers les autres composants
        window.dispatchEvent(new CustomEvent('socket-response', {
            detail: { eventName: 'player_list_updated', data }
        }));
    });
};

// Gestionnaire pour les événements émis par d'autres composants
const handleGameSocketEmit = (event: CustomEvent) => {
    const { eventName, data } = event.detail;
    
    if (socket.value && isConnected.value) {
        console.log(`🎮 Transfert vers serveur: ${eventName}`, data);
        socket.value.emit(eventName, data);
    } else {
        console.warn('⚠️ Socket non connecté, impossible de transférer:', eventName, data);
    }
};

// Diffuser le statut de connexion vers les autres composants
const broadcastConnectionStatus = () => {
    window.dispatchEvent(new CustomEvent('socket-status-change', {
        detail: { connected: isConnected.value }
    }));
};

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
    // Supprimer les écouteurs d'événements
    window.removeEventListener('game-socket-emit', handleGameSocketEmit as EventListener);
    
    if (socket.value) {
        socket.value.disconnect();
    }
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