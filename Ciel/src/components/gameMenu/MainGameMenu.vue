<template>
    <div class="main-game-menu">
        <div class="page-container">
            <!-- En-tête du menu -->
            <div class="page-header">
                <h1 class="page-title">Satsuki</h1>
                <p class="page-subtitle">Menu Principal</p>
            </div>

            <!-- Options du menu principal -->
            <div class="menu-options">
                <PlayerSection @player-added="onPlayerAdded" @player-removed="onPlayerRemoved" />
                <GameSection @quiz-added="sendQuizAdded" @quiz-removed="sendQuizRemoved" />
                <button class="btn-base btn-success start-button" :disabled="players.length === 0">
                    Start
                </button>
            </div>
        </div>
    </div>    
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import PlayerSection from './playersSection/PlayerSection.vue';
import GameSection from './gameSection/gameSection.vue';

// Interface pour un joueur
interface Player {
    id: number;
    name: string;
    color: string;
    gender: 'male' | 'female';
}

// Interface pour le formulaire
interface PlayerForm {
    name: string;
    gender: 'male' | 'female' | '';
}

// Interface pour un quiz
interface Quiz {
    id: number;
    title: string;
    description: string;
    questionCount: number;
    difficulty: 'easy' | 'medium' | 'hard';
    category: string;
    source?: 'manual' | 'xml' | 'toshokan'; // Source du quiz
    xmlContent?: string; // Contenu XML original
    toshokanId?: string; // ID Toshokan si applicable
}

// Interface pour le formulaire de quiz
interface QuizForm {
    title: string;
    description: string;
    questionCount: number;
    difficulty: 'easy' | 'medium' | 'hard' | '';
    category: string;
}

// Interface pour les données XML du quiz
interface XMLQuestion {
    question: string;
    answers: string[];
    correctAnswer: number;
    difficulty?: string;
    category?: string;
}

interface XMLQuizData {
    title: string;
    description?: string;
    category?: string;
    difficulty?: string;
    questions: XMLQuestion[];
}

// Interface pour l'API Toshokan
interface ToshokanSession {
    id: string;
    title: string;
    description?: string;
    questionCount: number;
    difficulty: 'easy' | 'medium' | 'hard';
    category: string;
    author?: string;
    createdAt: string;
    tags?: string[];
}

interface ToshokanSearchResponse {
    sessions: ToshokanSession[];
    total: number;
    page: number;
    limit: number;
}

// Couleurs prédéfinies pour les joueurs
const playerColors = [
    '#FF6B6B', // Rouge
    '#4ECDC4', // Turquoise
    '#45B7D1', // Bleu
    '#96CEB4', // Vert
    '#FFEAA7', // Jaune
    '#DDA0DD', // Violet
    '#FFB347', // Orange
    '#98D8C8'  // Vert menthe
];

// État réactif
const players = ref<Player[]>([]);
/* TEMP: modal/form/id logic moved to PlayerSection.vue — commented out here during migration
const isPlayerModalOpen = ref<boolean>(false);
const newPlayerForm = ref<PlayerForm>({
    name: '',
    gender: ''
});
let playerIdCounter = 1;
*/

// Quiz section moved to GameSection component (gameSection/GameSection.vue)

// Variables pour la communication avec le socket existant
let isSocketConnected = false;

// Fonctions de communication avec le socket existant
const emitToSocket = (eventName: string, data: any): void => {
    // Émettre un événement personnalisé que MainStatusNavBar peut écouter
    window.dispatchEvent(new CustomEvent('game-socket-emit', {
        detail: { eventName, data }
    }));
};

const sendPlayerAdded = (player: Player): void => {
    if (isSocketConnected) {
        const playerData = {
            id: player.id,
            name: player.name,
            gender: player.gender,
            color: player.color,
            timestamp: new Date().toISOString()
        };

        emitToSocket('player_added', playerData);
        console.log('📤 Joueur envoyé au serveur:', playerData);
    } else {
        console.warn('⚠️ Socket non connecté, impossible d\'envoyer les données du joueur');
    }
};

const sendPlayerRemoved = (playerId: number): void => {
    if (isSocketConnected) {
        const removeData = {
            id: playerId,
            timestamp: new Date().toISOString()
        };

        emitToSocket('player_removed', removeData);
        console.log('📤 Suppression joueur envoyée au serveur:', removeData);
    } else {
        console.warn('⚠️ Socket non connecté, impossible d\'envoyer la suppression du joueur');
    }
};

// Handlers for PlayerSection emits — update local state and forward to socket/store
const onPlayerAdded = (player: Player): void => {
    // Keep parent list in sync
    players.value.push(player);
    // Forward to socket/store
    sendPlayerAdded(player);
};

const onPlayerRemoved = (playerId: number): void => {
    // Remove locally if present
    const idx = players.value.findIndex(p => p.id === playerId);
    if (idx !== -1) {
        players.value.splice(idx, 1);
        // Reassign colors
        players.value.forEach((p, i) => {
            p.color = playerColors[i];
        });
    }

    // Forward removal to socket/store regardless
    sendPlayerRemoved(playerId);
};

// Écouter les événements de statut de connexion
const handleSocketStatus = (event: CustomEvent) => {
    const { connected } = event.detail;
    isSocketConnected = connected;
    console.log('🔌 Statut socket dans GameMenu:', connected ? 'Connecté' : 'Déconnecté');
};

// Écouter les réponses du serveur
const handleSocketResponse = (event: CustomEvent) => {
    const { eventName, data } = event.detail;
    
    if (eventName === 'player_added_response') {
        console.log('✅ Réponse serveur - Joueur ajouté:', data);
    } else if (eventName === 'player_removed_response') {
        console.log('✅ Réponse serveur - Joueur supprimé:', data);
    } else if (eventName === 'quiz_added_response') {
        console.log('✅ Réponse serveur - Quiz ajouté:', data);
    } else if (eventName === 'quiz_removed_response') {
        console.log('✅ Réponse serveur - Quiz supprimé:', data);
    }
};

// Fonctions
/* TEMP: player modal and manual add/remove functions moved to PlayerSection.vue. Commented out here while
   the new component takes responsibility. Keeping parent handlers `onPlayerAdded`/`onPlayerRemoved` that
   synchronize `players` and forward to the socket. If rollback needed, uncomment this block.

const openPlayerModal = (): void => {
    isPlayerModalOpen.value = true;
    // Réinitialiser le formulaire
    newPlayerForm.value = {
        name: '',
        gender: ''
    };
};

const closePlayerModal = (): void => {
    isPlayerModalOpen.value = false;
    newPlayerForm.value = {
        name: '',
        gender: ''
    };
};

const submitPlayer = (): void => {
    if (!newPlayerForm.value.name.trim() || !newPlayerForm.value.gender) {
        return;
    }

    if (players.value.length >= playerColors.length) {
        alert(`Maximum ${playerColors.length} joueurs autorisés`);
        return;
    }

    const newPlayer: Player = {
        id: playerIdCounter++,
        name: newPlayerForm.value.name.trim(),
        color: playerColors[players.value.length],
        gender: newPlayerForm.value.gender as 'male' | 'female'
    };

    players.value.push(newPlayer);
    
    // Envoyer au serveur
    sendPlayerAdded(newPlayer);
    
    closePlayerModal();
};

const addPlayer = (): void => {
    if (players.value.length >= playerColors.length) {
        alert(`Maximum ${playerColors.length} joueurs autorisés`);
        return;
    }

    const newPlayer: Player = {
        id: playerIdCounter++,
        name: `Joueur ${players.value.length + 1}`,
        color: playerColors[players.value.length],
        gender: 'male' // Par défaut
    };

    players.value.push(newPlayer);
};

const removePlayer = (index: number): void => {
    const playerToRemove = players.value[index];
    const playerId = playerToRemove.id;
    
    // Supprimer le joueur de la liste
    players.value.splice(index, 1);
    
    // Envoyer au serveur
    sendPlayerRemoved(playerId);
    
    // Réassigner les couleurs après suppression
    players.value.forEach((player, idx) => {
        player.color = playerColors[idx];
    });
};

*/

// Quiz logic moved to GameSection component; parent keeps only socket forwarding helpers below

const sendQuizAdded = (quiz: Quiz): void => {
    if (isSocketConnected) {
        const quizData = {
            id: quiz.id,
            title: quiz.title,
            description: quiz.description,
            questionCount: quiz.questionCount,
            difficulty: quiz.difficulty,
            category: quiz.category,
            timestamp: new Date().toISOString()
        };

        emitToSocket('quiz_added', quizData);
        console.log('📤 Quiz envoyé au serveur:', quizData);
    } else {
        console.warn('⚠️ Socket non connecté, impossible d\'envoyer les données du quiz');
    }
};

const sendQuizRemoved = (quizId: number): void => {
    if (isSocketConnected) {
        const removeData = {
            id: quizId,
            timestamp: new Date().toISOString()
        };

        emitToSocket('quiz_removed', removeData);
        console.log('📤 Suppression quiz envoyée au serveur:', removeData);
    } else {
        console.warn('⚠️ Socket non connecté, impossible d\'envoyer la suppression du quiz');
    }
};

// Lifecycle hooks
onMounted(() => {
    console.log('🎮 MainGameMenu monté - Écoute des événements socket');
    
    // Écouter le statut de connexion du socket
    window.addEventListener('socket-status-change', handleSocketStatus as EventListener);
    
    // Écouter les réponses du serveur via MainStatusNavBar
    window.addEventListener('socket-response', handleSocketResponse as EventListener);
});

onUnmounted(() => {
    console.log('🎮 MainGameMenu démonté - Nettoyage des écouteurs');
    
    // Supprimer les écouteurs d'événements
    window.removeEventListener('socket-status-change', handleSocketStatus as EventListener);
    window.removeEventListener('socket-response', handleSocketResponse as EventListener);
});

</script>

<style scoped>
/* ========== STYLES SPÉCIFIQUES À MAINGAMEMENU ========== */

.main-game-menu {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-lg);
    background: var(--bg-gradient);
}

.menu-options {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xl);
}

.start-button {
    font-size: 1.2rem;
    padding: var(--spacing-lg) var(--spacing-2xl);
    margin-top: var(--spacing-lg);
}

/* ========== STYLES SPÉCIFIQUES AUX FORMULAIRES ========== */
.form-row {
    display: flex;
    gap: var(--spacing-lg);
}

.form-group-half {
    flex: 1;
}

/* ========== OPTIONS DE GENRE ========== */
.gender-options {
    display: flex;
    gap: var(--spacing-md);
    flex-wrap: wrap;
}

.gender-option {
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: 0;
}

.gender-radio {
    display: none;
}

.gender-label {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: 12px 20px;
    border: 2px solid #e2e8f0;
    border-radius: var(--border-radius-md);
    transition: all var(--transition-normal);
    font-weight: 500;
    min-width: 120px;
    justify-content: center;
}

.gender-label:hover {
    border-color: #3b82f6;
    background: rgba(59, 130, 246, 0.05);
}

.gender-radio:checked + .gender-label {
    border-color: #3b82f6;
    background: rgba(59, 130, 246, 0.1);
    color: #2563eb;
}

.gender-icon {
    font-size: 1.2rem;
}

/* ========== OPTIONS DE DIFFICULTÉ ========== */
.difficulty-options {
    display: flex;
    gap: var(--spacing-md);
    flex-wrap: wrap;
}

.difficulty-option {
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: 0;
}

.difficulty-radio {
    display: none;
}

.difficulty-label {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: 12px 20px;
    border: 2px solid #e2e8f0;
    border-radius: var(--border-radius-md);
    transition: all var(--transition-normal);
    font-weight: 500;
    min-width: 120px;
    justify-content: center;
}

.difficulty-label:hover {
    border-color: #8b5cf6;
    background: rgba(139, 92, 246, 0.05);
}

.difficulty-radio:checked + .difficulty-label {
    border-color: #8b5cf6;
    background: rgba(139, 92, 246, 0.1);
    color: #6d28d9;
}

.difficulty-label.easy .difficulty-icon {
    color: #10b981;
}

.difficulty-label.medium .difficulty-icon {
    color: #f59e0b;
}

.difficulty-label.hard .difficulty-icon {
    color: #ef4444;
}

.difficulty-icon {
    font-size: 1.2rem;
}

/* ========== STYLES SPÉCIFIQUES AUX BADGES DE DIFFICULTÉ ========== */
.quiz-difficulty.easy {
    background: rgba(16, 185, 129, 0.15);
    color: #059669;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.quiz-difficulty.medium {
    background: rgba(245, 158, 11, 0.15);
    color: #d97706;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.quiz-difficulty.hard {
    background: rgba(239, 68, 68, 0.15);
    color: #dc2626;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

/* ========== STYLES POUR LES QUESTIONS ========== */
.quiz-questions {
    font-size: 0.9rem;
    color: var(--text-secondary);
    font-weight: 500;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
    .form-row {
        flex-direction: column;
    }
    
    .gender-options,
    .difficulty-options {
        flex-direction: column;
    }
    
    .gender-label,
    .difficulty-label {
        min-width: auto;
        width: 100%;
    }
}
</style>