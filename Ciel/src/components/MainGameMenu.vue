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
        <div class="modal-container quiz-modal" @click.stop>
            <div class="modal-header">
                <h3 class="modal-title">Ajouter un Quiz</h3>
                <button class="modal-close" @click="closeQuizModal">×</button>
            </div>
            
            <!-- Onglets pour les différentes méthodes -->
            <div class="quiz-tabs">
                <button 
                    class="tab-button" 
                    :class="{ active: activeQuizTab === 'manual' }"
                    @click="activeQuizTab = 'manual'"
                >
                    📝 Manuel
                </button>
                <button 
                    class="tab-button" 
                    :class="{ active: activeQuizTab === 'xml' }"
                    @click="activeQuizTab = 'xml'"
                >
                    📄 Fichier XML
                </button>
                <button 
                    class="tab-button" 
                    :class="{ active: activeQuizTab === 'toshokan' }"
                    @click="activeQuizTab = 'toshokan'"
                >
                    🌐 Toshokan API
                </button>
            </div>
            
            <div class="modal-body">
                <!-- Onglet Manuel (formulaire existant) -->
                <div v-if="activeQuizTab === 'manual'" class="tab-content">
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
                
                <!-- Onglet XML -->
                <div v-if="activeQuizTab === 'xml'" class="tab-content">
                    <div class="xml-upload-section">
                        <div class="upload-zone" :class="{ 'dragover': isDragOver }" 
                             @drop="handleFileDrop" 
                             @dragover.prevent="isDragOver = true" 
                             @dragleave="isDragOver = false">
                            <div class="upload-icon">📄</div>
                            <p class="upload-text">
                                Glissez-déposez un fichier XML ici ou 
                                <label class="upload-link">
                                    cliquez pour parcourir
                                    <input 
                                        type="file" 
                                        ref="xmlFileInput"
                                        @change="handleFileSelect" 
                                        accept=".xml"
                                        style="display: none;"
                                    />
                                </label>
                            </p>
                            <p class="upload-hint">Formats acceptés: .xml</p>
                        </div>
                        
                        <div v-if="selectedXMLFile" class="file-preview">
                            <div class="file-info">
                                <span class="file-name">{{ selectedXMLFile.name }}</span>
                                <span class="file-size">({{ formatFileSize(selectedXMLFile.size) }})</span>
                                <button @click="removeSelectedFile" class="remove-file">×</button>
                            </div>
                            
                            <div v-if="xmlQuizData" class="xml-preview">
                                <h4>Aperçu du quiz :</h4>
                                <div class="preview-info">
                                    <p><strong>Titre:</strong> {{ xmlQuizData.title }}</p>
                                    <p v-if="xmlQuizData.description"><strong>Description:</strong> {{ xmlQuizData.description }}</p>
                                    <p><strong>Questions:</strong> {{ xmlQuizData.questions.length }}</p>
                                    <p v-if="xmlQuizData.category"><strong>Catégorie:</strong> {{ xmlQuizData.category }}</p>
                                    <p v-if="xmlQuizData.difficulty"><strong>Difficulté:</strong> {{ xmlQuizData.difficulty }}</p>
                                </div>
                            </div>
                            
                            <div v-if="xmlParseError" class="error-message">
                                <p><strong>Erreur de parsing:</strong> {{ xmlParseError }}</p>
                            </div>
                        </div>
                        
                        <div class="form-actions">
                            <button type="button" @click="closeQuizModal" class="btn-cancel">
                                Annuler
                            </button>
                            <button 
                                type="button" 
                                @click="submitXMLQuiz" 
                                class="btn-submit" 
                                :disabled="!xmlQuizData"
                            >
                                Importer Quiz XML
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Onglet Toshokan API -->
                <div v-if="activeQuizTab === 'toshokan'" class="tab-content">
                    <div class="toshokan-search-section">
                        <div class="search-form">
                            <div class="form-group">
                                <label class="form-label">Rechercher des quiz sur Toshokan</label>
                                <div class="search-input-group">
                                    <input 
                                        v-model="toshokanSearchQuery" 
                                        type="text" 
                                        class="form-input"
                                        placeholder="Tapez des mots-clés pour rechercher..."
                                        @keyup.enter="searchToshokanQuizzes"
                                    />
                                    <button 
                                        type="button" 
                                        @click="searchToshokanQuizzes" 
                                        class="search-button"
                                        :disabled="isSearchingToshokan"
                                    >
                                        {{ isSearchingToshokan ? '🔄' : '🔍' }}
                                    </button>
                                </div>
                            </div>
                            
                            <div class="search-filters">
                                <select v-model="toshokanFilters.difficulty" class="filter-select">
                                    <option value="">Toutes difficultés</option>
                                    <option value="easy">Facile</option>
                                    <option value="medium">Moyen</option>
                                    <option value="hard">Difficile</option>
                                </select>
                                
                                <select v-model="toshokanFilters.category" class="filter-select">
                                    <option value="">Toutes catégories</option>
                                    <option value="history">Histoire</option>
                                    <option value="science">Science</option>
                                    <option value="geography">Géographie</option>
                                    <option value="literature">Littérature</option>
                                    <option value="general">Culture générale</option>
                                </select>
                            </div>
                        </div>
                        
                        <div v-if="isSearchingToshokan" class="loading-indicator">
                            <div class="spinner"></div>
                            <p>Recherche en cours...</p>
                        </div>
                        
                        <div v-if="toshokanSearchError" class="error-message">
                            <p><strong>Erreur:</strong> {{ toshokanSearchError }}</p>
                        </div>
                        
                        <div v-if="toshokanResults.length > 0" class="search-results">
                            <h4>Résultats de recherche ({{ toshokanResults.length }})</h4>
                            <div class="results-list">
                                <div 
                                    v-for="session in toshokanResults" 
                                    :key="session.id"
                                    class="result-item"
                                    :class="{ selected: selectedToshokanSession?.id === session.id }"
                                    @click="selectToshokanSession(session)"
                                >
                                    <div class="result-header">
                                        <h5 class="result-title">{{ session.title }}</h5>
                                        <span class="badge" :class="session.difficulty">{{ getDifficultyLabel(session.difficulty) }}</span>
                                    </div>
                                    <p v-if="session.description" class="result-description">{{ session.description }}</p>
                                    <div class="result-meta">
                                        <span class="meta-item">📝 {{ session.questionCount }} questions</span>
                                        <span v-if="session.category" class="meta-item">🏷️ {{ session.category }}</span>
                                        <span v-if="session.author" class="meta-item">👤 {{ session.author }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="form-actions">
                            <button type="button" @click="closeQuizModal" class="btn-cancel">
                                Annuler
                            </button>
                            <button 
                                type="button" 
                                @click="submitToshokanQuiz" 
                                class="btn-submit" 
                                :disabled="!selectedToshokanSession"
                            >
                                Importer Quiz Toshokan
                            </button>
                        </div>
                    </div>
                </div>
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

// Variables pour les onglets du modal quiz
const activeQuizTab = ref<'manual' | 'xml' | 'toshokan'>('manual');

// Variables pour le chargement XML
const selectedXMLFile = ref<File | null>(null);
const xmlQuizData = ref<XMLQuizData | null>(null);
const xmlParseError = ref<string>('');
const isDragOver = ref<boolean>(false);
const xmlFileInput = ref<HTMLInputElement | null>(null);

// Variables pour Toshokan API
const toshokanSearchQuery = ref<string>('');
const toshokanResults = ref<ToshokanSession[]>([]);
const selectedToshokanSession = ref<ToshokanSession | null>(null);
const isSearchingToshokan = ref<boolean>(false);
const toshokanSearchError = ref<string>('');
const toshokanFilters = ref({
    difficulty: '',
    category: ''
});

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
    // Réinitialiser les données des nouvelles fonctionnalités
    resetQuizModal();
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

// Fonctions pour le chargement XML
const handleFileSelect = (event: Event): void => {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
        handleXMLFile(input.files[0]);
    }
};

const handleFileDrop = (event: DragEvent): void => {
    event.preventDefault();
    isDragOver.value = false;
    
    if (event.dataTransfer?.files && event.dataTransfer.files.length > 0) {
        handleXMLFile(event.dataTransfer.files[0]);
    }
};

const handleXMLFile = async (file: File): Promise<void> => {
    if (!file.name.toLowerCase().endsWith('.xml')) {
        xmlParseError.value = 'Seuls les fichiers XML sont autorisés';
        return;
    }
    
    selectedXMLFile.value = file;
    xmlParseError.value = '';
    
    try {
        const content = await file.text();
        xmlQuizData.value = parseXMLQuiz(content);
    } catch (error) {
        xmlParseError.value = `Erreur lors de la lecture du fichier: ${error}`;
        xmlQuizData.value = null;
    }
};

const parseXMLQuiz = (xmlContent: string): XMLQuizData => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(xmlContent, 'text/xml');
    
    // Vérifier s'il y a des erreurs de parsing
    const parserError = doc.querySelector('parsererror');
    if (parserError) {
        throw new Error('XML invalide');
    }
    
    // Extraire les informations du quiz
    const quizElement = doc.querySelector('quiz');
    if (!quizElement) {
        throw new Error('Élément <quiz> non trouvé');
    }
    
    // Extraire le nom du quiz
    const titleElement = doc.querySelector('quiz_name') || doc.querySelector('title');
    const title = titleElement?.textContent || 'Quiz sans titre';
    
    // Extraire les informations du summary
    const questionCountElement = doc.querySelector('number_of_questions') || doc.querySelector('question_count');
    const expectedQuestionCount = questionCountElement ? parseInt(questionCountElement.textContent || '0') : 0;
    
    // Extraire les questions
    const questionElements = doc.querySelectorAll('question');
    const questions: XMLQuestion[] = Array.from(questionElements).map((qElement, index) => {
        const questionText = qElement.querySelector('text')?.textContent || `Question ${index + 1}`;
        const category = qElement.querySelector('category')?.textContent || '';
        const difficulty = qElement.getAttribute('difficulty') || 'medium';
        
        // Extraire les options de réponse
        const optionElements = qElement.querySelectorAll('choices option');
        const answers = Array.from(optionElements).map(option => option.textContent || '');
        
        // Trouver l'index de la réponse correcte
        let correctAnswer = 0;
        Array.from(optionElements).forEach((option, idx) => {
            if (option.getAttribute('correct') === 'true') {
                correctAnswer = idx;
            }
        });
        
        return {
            question: questionText,
            answers,
            correctAnswer,
            difficulty: mapDifficultyFromXML(difficulty),
            category
        };
    });
    
    if (questions.length === 0) {
        throw new Error('Aucune question trouvée dans le fichier XML');
    }
    
    // Déterminer la difficulté globale basée sur la moyenne des questions
    const difficultyStats = questions.reduce((stats, q) => {
        stats[q.difficulty || 'medium'] = (stats[q.difficulty || 'medium'] || 0) + 1;
        return stats;
    }, {} as Record<string, number>);
    
    const dominantDifficulty = Object.keys(difficultyStats).reduce((a, b) => 
        difficultyStats[a] > difficultyStats[b] ? a : b
    );
    
    // Déterminer la catégorie dominante
    const categoryStats = questions.reduce((stats, q) => {
        const cat = q.category || 'Général';
        stats[cat] = (stats[cat] || 0) + 1;
        return stats;
    }, {} as Record<string, number>);
    
    const dominantCategory = Object.keys(categoryStats).reduce((a, b) => 
        categoryStats[a] > categoryStats[b] ? a : b
    );
    
    return {
        title,
        description: `Quiz importé avec ${questions.length} questions`,
        category: dominantCategory,
        difficulty: dominantDifficulty as 'easy' | 'medium' | 'hard',
        questions
    };
};

// Fonction utilitaire pour mapper les difficultés XML vers notre format
const mapDifficultyFromXML = (xmlDifficulty: string): 'easy' | 'medium' | 'hard' => {
    const mapping: Record<string, 'easy' | 'medium' | 'hard'> = {
        'facile': 'easy',
        'easy': 'easy',
        'moyen': 'medium',
        'medium': 'medium',
        'moyenne': 'medium',
        'difficile': 'hard',
        'hard': 'hard',
        'dur': 'hard'
    };
    
    return mapping[xmlDifficulty.toLowerCase()] || 'medium';
};

const removeSelectedFile = (): void => {
    selectedXMLFile.value = null;
    xmlQuizData.value = null;
    xmlParseError.value = '';
    if (xmlFileInput.value) {
        xmlFileInput.value.value = '';
    }
};

const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const submitXMLQuiz = async (): Promise<void> => {
    if (!xmlQuizData.value) {
        alert('Aucun quiz XML valide sélectionné');
        return;
    }
    
    const xmlContent = selectedXMLFile.value ? await selectedXMLFile.value.text() : undefined;
    
    const newQuiz: Quiz = {
        id: quizIdCounter++,
        title: xmlQuizData.value.title,
        description: xmlQuizData.value.description || '',
        questionCount: xmlQuizData.value.questions.length,
        difficulty: (xmlQuizData.value.difficulty as 'easy' | 'medium' | 'hard') || 'medium',
        category: xmlQuizData.value.category || '',
        source: 'xml',
        xmlContent
    };
    
    quizzes.value.push(newQuiz);
    sendQuizAdded(newQuiz);
    closeQuizModal();
    
    // Réinitialiser les données XML
    removeSelectedFile();
};

// Fonctions pour Toshokan API
const searchToshokanQuizzes = async (): Promise<void> => {
    if (!toshokanSearchQuery.value.trim()) {
        toshokanSearchError.value = 'Veuillez entrer des mots-clés de recherche';
        return;
    }
    
    isSearchingToshokan.value = true;
    toshokanSearchError.value = '';
    toshokanResults.value = [];
    
    try {
        const searchParams = new URLSearchParams({
            q: toshokanSearchQuery.value,
            ...(toshokanFilters.value.difficulty && { difficulty: toshokanFilters.value.difficulty }),
            ...(toshokanFilters.value.category && { category: toshokanFilters.value.category }),
            limit: '20'
        });
        
        const response = await fetch(`https://toshokan.satsuki.azelakara.net/api/quiz/search?${searchParams}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        
        const data: ToshokanSearchResponse = await response.json();
        toshokanResults.value = data.sessions || [];
        
        if (toshokanResults.value.length === 0) {
            toshokanSearchError.value = 'Aucun quiz trouvé avec ces critères';
        }
        
    } catch (error) {
        console.error('Erreur lors de la recherche Toshokan:', error);
        toshokanSearchError.value = `Erreur de connexion à l'API Toshokan: ${error}`;
    } finally {
        isSearchingToshokan.value = false;
    }
};

const selectToshokanSession = (session: ToshokanSession): void => {
    selectedToshokanSession.value = session;
};

const getDifficultyLabel = (difficulty: string): string => {
    const labels = {
        'easy': 'Facile',
        'medium': 'Moyen',
        'hard': 'Difficile'
    };
    return labels[difficulty as keyof typeof labels] || difficulty;
};

const submitToshokanQuiz = (): void => {
    if (!selectedToshokanSession.value) {
        alert('Aucun quiz Toshokan sélectionné');
        return;
    }
    
    const session = selectedToshokanSession.value;
    const newQuiz: Quiz = {
        id: quizIdCounter++,
        title: session.title,
        description: session.description || '',
        questionCount: session.questionCount,
        difficulty: session.difficulty,
        category: session.category,
        source: 'toshokan',
        toshokanId: session.id
    };
    
    quizzes.value.push(newQuiz);
    sendQuizAdded(newQuiz);
    closeQuizModal();
    
    // Réinitialiser la sélection
    selectedToshokanSession.value = null;
    toshokanSearchQuery.value = '';
    toshokanResults.value = [];
};

// Réinitialiser l'onglet et les données lors de l'ouverture du modal
const resetQuizModal = (): void => {
    activeQuizTab.value = 'manual';
    // removeSelectedFile(); // Sera appelé dans les fonctions correspondantes
    selectedToshokanSession.value = null;
    toshokanSearchQuery.value = '';
    toshokanResults.value = [];
    toshokanSearchError.value = '';
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