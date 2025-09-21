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
                <!-- Section joueurs -->
                <div class="card players-section">
                    <div class="card-header">
                        <h3 class="card-title">Joueurs</h3>
                        <button class="btn-base btn-primary add-player-button" @click="openPlayerModal">
                            + Add Player
                        </button>
                    </div>
                    
                    <!-- Liste des joueurs -->
                    <div class="items-list players-list">
                        <div 
                            v-for="(player, index) in players" 
                            :key="player.id"
                            class="item player-item"
                            :style="{ color: player.color }"
                        >
                            <div class="item-info">
                                <div class="item-main">
                                    <span class="color-dot player-color-dot" :style="{ backgroundColor: player.color }"></span>
                                    <span class="item-title player-name">{{ player.name }}</span>
                                </div>
                            </div>
                            <button 
                                class="action-button remove remove-player-button" 
                                @click="removePlayer(index)"
                                title="Supprimer le joueur"
                            >
                                ×
                            </button>
                        </div>
                        <div v-if="players.length === 0" class="empty-state">
                            Aucun joueur ajouté
                        </div>
                    </div>
                </div>

                <!-- Section Quiz -->
                <div class="card quiz-section">
                    <div class="card-header">
                        <h3 class="card-title">Quiz</h3>
                        <button class="btn-base btn-secondary add-quiz-button" @click="openQuizModal">
                            + Add Quiz
                        </button>
                    </div>
                    
                    <!-- Liste des quiz -->
                    <div class="items-list quiz-list">
                        <div 
                            v-for="(quiz, index) in quizzes" 
                            :key="quiz.id"
                            class="item quiz-item"
                        >
                            <div class="item-info">
                                <div class="item-main">
                                    <span class="item-title quiz-title-text">{{ quiz.title }}</span>
                                    <span class="badge quiz-difficulty" :class="quiz.difficulty">
                                        {{ quiz.difficulty === 'easy' ? 'Facile' : quiz.difficulty === 'medium' ? 'Moyen' : 'Difficile' }}
                                    </span>
                                </div>
                                <div class="item-details quiz-details">
                                    <span class="quiz-questions">{{ quiz.questionCount }} questions</span>
                                    <span v-if="quiz.category" class="badge-secondary quiz-category">{{ quiz.category }}</span>
                                </div>
                                <p v-if="quiz.description" class="item-description quiz-description">{{ quiz.description }}</p>
                            </div>
                            <button 
                                class="action-button remove remove-quiz-button" 
                                @click="removeQuiz(index)"
                                title="Supprimer le quiz"
                            >
                                ×
                            </button>
                        </div>
                        <div v-if="quizzes.length === 0" class="empty-state">
                            Aucun quiz créé
                        </div>
                    </div>
                </div>

                <button class="btn-base btn-success start-button" :disabled="players.length === 0">
                    Start
                </button>
            </div>
        </div>

        <!-- Modal d'ajout de joueur -->
        <div v-if="isPlayerModalOpen" class="modal-overlay" @click="closePlayerModal">
            <div class="modal-container" @click.stop>
                <div class="modal-header">
                    <h3 class="modal-title">Ajouter un joueur</h3>
                    <button class="modal-close" @click="closePlayerModal">×</button>
                </div>
                
                <form @submit.prevent="submitPlayer" class="player-form">
                    <div class="form-group">
                        <label for="playerName" class="form-label">Nom du joueur</label>
                        <input 
                            id="playerName"
                            v-model="newPlayerForm.name"
                            type="text" 
                            class="form-input"
                            placeholder="Entrez le nom du joueur"
                            required
                            maxlength="20"
                        />
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Sexe</label>
                        <div class="gender-options">
                            <label class="gender-option">
                                <input 
                                    v-model="newPlayerForm.gender" 
                                    type="radio" 
                                    value="male"
                                    class="gender-radio"
                                />
                                <span class="gender-label">
                                    <span class="gender-icon">👨</span>
                                    Masculin
                                </span>
                            </label>
                            <label class="gender-option">
                                <input 
                                    v-model="newPlayerForm.gender" 
                                    type="radio" 
                                    value="female"
                                    class="gender-radio"
                                />
                                <span class="gender-label">
                                    <span class="gender-icon">👩</span>
                                    Féminin
                                </span>
                            </label>
                        </div>
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" @click="closePlayerModal" class="btn-cancel">
                            Annuler
                        </button>
                        <button type="submit" class="btn-submit" :disabled="!newPlayerForm.name.trim() || !newPlayerForm.gender">
                            Ajouter
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Modal pour ajouter un quiz -->
    <div v-if="isQuizModalOpen" class="modal-overlay" @click="closeQuizModal">
        <div class="modal-container" @click.stop>
            <div class="modal-header">
                <h3 class="modal-title">Ajouter un Quiz</h3>
                <button class="modal-close" @click="closeQuizModal">×</button>
            </div>
            <div class="modal-body">
                <form @submit.prevent="submitQuizForm" class="quiz-form">
                    <div class="form-group">
                        <label class="form-label">Titre du quiz *</label>
                        <input 
                            v-model="newQuizForm.title" 
                            type="text" 
                            class="form-input"
                            placeholder="Entrez le titre du quiz"
                            maxlength="100"
                            required
                        />
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Description</label>
                        <textarea 
                            v-model="newQuizForm.description" 
                            class="form-textarea"
                            placeholder="Description du quiz (optionnel)"
                            maxlength="500"
                            rows="3"
                        ></textarea>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group form-group-half">
                            <label class="form-label">Nombre de questions</label>
                            <input 
                                v-model.number="newQuizForm.questionCount" 
                                type="number" 
                                class="form-input"
                                min="1"
                                max="50"
                                required
                            />
                        </div>
                        
                        <div class="form-group form-group-half">
                            <label class="form-label">Catégorie</label>
                            <input 
                                v-model="newQuizForm.category" 
                                type="text" 
                                class="form-input"
                                placeholder="Ex: Histoire, Science..."
                                maxlength="50"
                            />
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Difficulté *</label>
                        <div class="difficulty-options">
                            <label class="difficulty-option">
                                <input 
                                    v-model="newQuizForm.difficulty" 
                                    type="radio" 
                                    value="easy"
                                    class="difficulty-radio"
                                />
                                <span class="difficulty-label easy">
                                    <span class="difficulty-icon">🟢</span>
                                    Facile
                                </span>
                            </label>
                            <label class="difficulty-option">
                                <input 
                                    v-model="newQuizForm.difficulty" 
                                    type="radio" 
                                    value="medium"
                                    class="difficulty-radio"
                                />
                                <span class="difficulty-label medium">
                                    <span class="difficulty-icon">🟡</span>
                                    Moyen
                                </span>
                            </label>
                            <label class="difficulty-option">
                                <input 
                                    v-model="newQuizForm.difficulty" 
                                    type="radio" 
                                    value="hard"
                                    class="difficulty-radio"
                                />
                                <span class="difficulty-label hard">
                                    <span class="difficulty-icon">🔴</span>
                                    Difficile
                                </span>
                            </label>
                        </div>
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" @click="closeQuizModal" class="btn-cancel">
                            Annuler
                        </button>
                        <button type="submit" class="btn-submit" :disabled="!newQuizForm.title.trim() || !newQuizForm.difficulty">
                            Créer Quiz
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

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
}

// Interface pour le formulaire de quiz
interface QuizForm {
    title: string;
    description: string;
    questionCount: number;
    difficulty: 'easy' | 'medium' | 'hard' | '';
    category: string;
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
const isPlayerModalOpen = ref<boolean>(false);
const newPlayerForm = ref<PlayerForm>({
    name: '',
    gender: ''
});
let playerIdCounter = 1;

// État réactif pour les quiz
const quizzes = ref<Quiz[]>([]);
const isQuizModalOpen = ref<boolean>(false);
const newQuizForm = ref<QuizForm>({
    title: '',
    description: '',
    questionCount: 5,
    difficulty: '',
    category: ''
});
let quizIdCounter = 1;

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

// Fonctions pour les quiz
const openQuizModal = (): void => {
    isQuizModalOpen.value = true;
    // Réinitialiser le formulaire
    newQuizForm.value = {
        title: '',
        description: '',
        questionCount: 5,
        difficulty: '',
        category: ''
    };
};

const closeQuizModal = (): void => {
    isQuizModalOpen.value = false;
    newQuizForm.value = {
        title: '',
        description: '',
        questionCount: 5,
        difficulty: '',
        category: ''
    };
};

const submitQuizForm = (): void => {
    if (!newQuizForm.value.title.trim()) {
        alert('Le titre du quiz est requis');
        return;
    }

    if (!newQuizForm.value.difficulty) {
        alert('La difficulté du quiz est requise');
        return;
    }

    const newQuiz: Quiz = {
        id: quizIdCounter++,
        title: newQuizForm.value.title.trim(),
        description: newQuizForm.value.description.trim(),
        questionCount: newQuizForm.value.questionCount,
        difficulty: newQuizForm.value.difficulty as 'easy' | 'medium' | 'hard',
        category: newQuizForm.value.category.trim()
    };

    quizzes.value.push(newQuiz);
    
    // Envoyer au serveur
    sendQuizAdded(newQuiz);
    
    closeQuizModal();
};

const removeQuiz = (index: number): void => {
    const quizToRemove = quizzes.value[index];
    const quizId = quizToRemove.id;
    
    // Supprimer le quiz de la liste
    quizzes.value.splice(index, 1);
    
    // Envoyer au serveur
    sendQuizRemoved(quizId);
};

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