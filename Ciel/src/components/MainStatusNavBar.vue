<template>
    <nav class="status-navbar">
        <div class="navbar-content">
            <div class="navbar-left">
                <h1 class="status-title">Status Bar</h1>
            </div>
            
            <div class="navbar-right">
                <!-- Témoin de connexion Socket.IO -->
                <div class="connection-indicator" :class="connectionClass">
                    <div class="status-dot" :class="statusDotClass"></div>
                    <span class="status-text">{{ connectionText }}</span>
                </div>
                
                <!-- Bouton de connexion/déconnexion -->
                <button 
                    v-if="!isConnected" 
                    @click="handleConnect" 
                    class="connect-btn"
                    :disabled="isConnecting"
                >
                    {{ isConnecting ? 'Connexion...' : 'Se connecter' }}
                </button>
                
                <button 
                    v-else 
                    @click="handleDisconnect" 
                    class="disconnect-btn"
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
        console.log('✅ Socket.IO connecté:', socket.value.id);
        isConnected.value = true;
        isConnecting.value = false;
        connectionStatus.value = 'connected';
    });
    
    socket.value.on('disconnect', (reason) => {
        console.log('❌ Socket.IO déconnecté:', reason);
        isConnected.value = false;
        isConnecting.value = false;
        connectionStatus.value = 'disconnected';
    });
    
    socket.value.on('connect_error', (error) => {
        console.error('❌ Erreur de connexion Socket.IO:', error);
        isConnected.value = false;
        isConnecting.value = false;
        connectionStatus.value = 'error';
    });
    
    socket.value.on('reconnect', (attemptNumber) => {
        console.log(`✅ Reconnecté après ${attemptNumber} tentatives`);
        isConnected.value = true;
        isConnecting.value = false;
        connectionStatus.value = 'connected';
    });
    
    socket.value.on('reconnect_attempt', (attemptNumber) => {
        console.log(`🔄 Tentative de reconnexion #${attemptNumber}`);
        isConnecting.value = true;
        connectionStatus.value = 'reconnecting';
    });
    
    socket.value.on('welcome', (data) => {
        console.log('📨 Message de bienvenue:', data);
    });
};

// Configuration au montage
onMounted(() => {
    // Tentative de connexion automatique au démarrage
    setTimeout(() => {
        handleConnect();
    }, 1000);
});

// Nettoyage au démontage
onUnmounted(() => {
    if (socket.value) {
        socket.value.disconnect();
    }
});
</script>

<style scoped>
.status-navbar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-bottom: 2px solid #e5e7eb;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 0.75rem 1.5rem;
    min-height: 60px;
}

.navbar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 100%;
    width: 100%;
}

.navbar-left {
    flex: 1;
}

.status-title {
    color: white;
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.navbar-right {
    display: flex;
    align-items: center;
    gap: 1rem;
}

/* Indicateur de connexion */
.connection-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 600;
    transition: all 0.3s ease;
    min-width: 130px;
    justify-content: center;
}

.connection-indicator.connected {
    background: rgba(34, 197, 94, 0.2);
    border: 2px solid #22c55e;
    color: #16a34a;
    box-shadow: 0 0 10px rgba(34, 197, 94, 0.3);
}

.connection-indicator.disconnected {
    background: rgba(239, 68, 68, 0.2);
    border: 2px solid #ef4444;
    color: #dc2626;
    box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
}

.connection-indicator.connecting {
    background: rgba(251, 191, 36, 0.2);
    border: 2px solid #fbbf24;
    color: #d97706;
    box-shadow: 0 0 10px rgba(251, 191, 36, 0.3);
}

/* Points de statut */
.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    transition: all 0.3s ease;
}

.status-dot.dot-connected {
    background: #22c55e;
    box-shadow: 0 0 8px rgba(34, 197, 94, 0.6);
}

.status-dot.dot-disconnected {
    background: #ef4444;
    box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
}

.status-dot.dot-connecting {
    background: #fbbf24;
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

/* Boutons de connexion */
.connect-btn, .disconnect-btn {
    padding: 0.5rem 1rem;
    border-radius: 8px;
    border: none;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    min-width: 120px;
}

.connect-btn {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
}

.connect-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #059669, #047857);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(16, 185, 129, 0.4);
}

.connect-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

.disconnect-btn {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
}

.disconnect-btn:hover {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(239, 68, 68, 0.4);
}

/* Responsive */
@media (max-width: 768px) {
    .navbar-content {
        flex-direction: column;
        gap: 0.75rem;
        align-items: stretch;
    }
    
    .navbar-right {
        justify-content: space-between;
    }
    
    .connection-indicator {
        min-width: auto;
        flex: 1;
    }
    
    .connect-btn, .disconnect-btn {
        min-width: auto;
        flex: 1;
    }
}

@media (max-width: 480px) {
    .status-navbar {
        padding: 0.5rem 1rem;
    }
    
    .status-title {
        font-size: 1rem;
    }
    
    .connection-indicator, .connect-btn, .disconnect-btn {
        font-size: 0.75rem;
        padding: 0.4rem 0.8rem;
    }
}
</style>

<style scoped>
.status-navbar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-bottom: 2px solid #e5e7eb;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 0.75rem 1.5rem;
    min-height: 60px;
}

.navbar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 100%;
    width: 100%;
}

.navbar-left {
    flex: 1;
}

.status-title {
    color: white;
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.navbar-right {
    display: flex;
    align-items: center;
    gap: 1rem;
}

/* Indicateur de connexion */
.connection-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 600;
    transition: all 0.3s ease;
    min-width: 130px;
    justify-content: center;
}

.connection-indicator.connected {
    background: rgba(34, 197, 94, 0.2);
    border: 2px solid #22c55e;
    color: #16a34a;
    box-shadow: 0 0 10px rgba(34, 197, 94, 0.3);
}

.connection-indicator.disconnected {
    background: rgba(239, 68, 68, 0.2);
    border: 2px solid #ef4444;
    color: #dc2626;
    box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
}

.connection-indicator.connecting {
    background: rgba(251, 191, 36, 0.2);
    border: 2px solid #fbbf24;
    color: #d97706;
    box-shadow: 0 0 10px rgba(251, 191, 36, 0.3);
}

/* Points de statut */
.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    transition: all 0.3s ease;
}

.status-dot.dot-connected {
    background: #22c55e;
    box-shadow: 0 0 8px rgba(34, 197, 94, 0.6);
}

.status-dot.dot-disconnected {
    background: #ef4444;
    box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
}

.status-dot.dot-connecting {
    background: #fbbf24;
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

/* Boutons de connexion */
.connect-btn, .disconnect-btn {
    padding: 0.5rem 1rem;
    border-radius: 8px;
    border: none;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    min-width: 120px;
}

.connect-btn {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
}

.connect-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #059669, #047857);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(16, 185, 129, 0.4);
}

.connect-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

.disconnect-btn {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
}

.disconnect-btn:hover {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(239, 68, 68, 0.4);
}

/* Responsive */
@media (max-width: 768px) {
    .navbar-content {
        flex-direction: column;
        gap: 0.75rem;
        align-items: stretch;
    }
    
    .navbar-right {
        justify-content: space-between;
    }
    
    .connection-indicator {
        min-width: auto;
        flex: 1;
    }
    
    .connect-btn, .disconnect-btn {
        min-width: auto;
        flex: 1;
    }
}

@media (max-width: 480px) {
    .status-navbar {
        padding: 0.5rem 1rem;
    }
    
    .status-title {
        font-size: 1rem;
    }
    
    .connection-indicator, .connect-btn, .disconnect-btn {
        font-size: 0.75rem;
        padding: 0.4rem 0.8rem;
    }
}
</style>