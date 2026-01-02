<template>
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
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Quiz {
    id: number;
    title: string;
    description: string;
    questionCount: number;
    difficulty: 'easy' | 'medium' | 'hard';
    category: string;
    source?: 'manual' | 'xml' | 'toshokan';
    xmlContent?: string;
    toshokanId?: string;
}

interface QuizForm {
    title: string;
    description: string;
    questionCount: number;
    difficulty: 'easy' | 'medium' | 'hard' | '';
    category: string;
}

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

const quizzes = ref<Quiz[]>([]);
const isQuizModalOpen = ref<boolean>(false);
const newQuizForm = ref<QuizForm>({ title: '', description: '', questionCount: 5, difficulty: '', category: '' });
let quizIdCounter = 1;

const activeQuizTab = ref<'manual' | 'xml' | 'toshokan'>('manual');

const selectedXMLFile = ref<File | null>(null);
const xmlQuizData = ref<XMLQuizData | null>(null);
const xmlParseError = ref<string>('');
const isDragOver = ref<boolean>(false);
const xmlFileInput = ref<HTMLInputElement | null>(null);

const toshokanSearchQuery = ref<string>('');
const toshokanResults = ref<ToshokanSession[]>([]);
const selectedToshokanSession = ref<ToshokanSession | null>(null);
const isSearchingToshokan = ref<boolean>(false);
const toshokanSearchError = ref<string>('');
const toshokanFilters = ref({ difficulty: '', category: '' });

// Emits for parent to handle socket/store
const emit = defineEmits<{
  (e: 'quiz-added', payload: Quiz): void;
  (e: 'quiz-removed', id: number): void;
}>();

const openQuizModal = (): void => {
    isQuizModalOpen.value = true;
    newQuizForm.value = { title: '', description: '', questionCount: 5, difficulty: '', category: '' };
    resetQuizModal();
};

const closeQuizModal = (): void => {
    isQuizModalOpen.value = false;
    newQuizForm.value = { title: '', description: '', questionCount: 5, difficulty: '', category: '' };
};

const submitQuizForm = (): void => {
    if (!newQuizForm.value.title.trim()) { alert('Le titre du quiz est requis'); return; }
    if (!newQuizForm.value.difficulty) { alert('La difficulté du quiz est requise'); return; }

    const newQuiz: Quiz = {
        id: quizIdCounter++,
        title: newQuizForm.value.title.trim(),
        description: newQuizForm.value.description.trim(),
        questionCount: newQuizForm.value.questionCount,
        difficulty: newQuizForm.value.difficulty as 'easy' | 'medium' | 'hard',
        category: newQuizForm.value.category.trim()
    };

    quizzes.value.push(newQuiz);
    emit('quiz-added', newQuiz);
    closeQuizModal();
};

const removeQuiz = (index: number): void => {
    const quizToRemove = quizzes.value[index];
    const quizId = quizToRemove.id;
    quizzes.value.splice(index, 1);
    emit('quiz-removed', quizId);
};

// XML helpers
const handleFileSelect = (event: Event): void => {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) handleXMLFile(input.files[0]);
};

const handleFileDrop = (event: DragEvent): void => {
    event.preventDefault();
    isDragOver.value = false;
    if (event.dataTransfer?.files && event.dataTransfer.files.length > 0) handleXMLFile(event.dataTransfer.files[0]);
};

const handleXMLFile = async (file: File): Promise<void> => {
    if (!file.name.toLowerCase().endsWith('.xml')) { xmlParseError.value = 'Seuls les fichiers XML sont autorisés'; return; }
    selectedXMLFile.value = file;
    xmlParseError.value = '';
    try { const content = await file.text(); xmlQuizData.value = parseXMLQuiz(content); } catch (error) { xmlParseError.value = `Erreur lors de la lecture du fichier: ${error}`; xmlQuizData.value = null; }
};

const parseXMLQuiz = (xmlContent: string): XMLQuizData => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(xmlContent, 'text/xml');
    const parserError = doc.querySelector('parsererror');
    if (parserError) throw new Error('XML invalide');
    const quizElement = doc.querySelector('quiz');
    if (!quizElement) throw new Error('Élément <quiz> non trouvé');
    const titleElement = doc.querySelector('quiz_name') || doc.querySelector('title');
    const title = titleElement?.textContent || 'Quiz sans titre';
    const questionElements = doc.querySelectorAll('question');
    const questions: XMLQuestion[] = Array.from(questionElements).map((qElement, index) => {
        const questionText = qElement.querySelector('text')?.textContent || `Question ${index + 1}`;
        const category = qElement.querySelector('category')?.textContent || '';
        const difficulty = qElement.getAttribute('difficulty') || 'medium';
        const optionElements = qElement.querySelectorAll('choices option');
        const answers = Array.from(optionElements).map(option => option.textContent || '');
        let correctAnswer = 0;
        Array.from(optionElements).forEach((option, idx) => { if (option.getAttribute('correct') === 'true') correctAnswer = idx; });
        return { question: questionText, answers, correctAnswer, difficulty: mapDifficultyFromXML(difficulty), category };
    });
    if (questions.length === 0) throw new Error('Aucune question trouvée dans le fichier XML');
    const difficultyStats = questions.reduce((stats, q) => { stats[q.difficulty || 'medium'] = (stats[q.difficulty || 'medium'] || 0) + 1; return stats; }, {} as Record<string, number>);
    const dominantDifficulty = Object.keys(difficultyStats).reduce((a, b) => difficultyStats[a] > difficultyStats[b] ? a : b);
    const categoryStats = questions.reduce((stats, q) => { const cat = q.category || 'Général'; stats[cat] = (stats[cat] || 0) + 1; return stats; }, {} as Record<string, number>);
    const dominantCategory = Object.keys(categoryStats).reduce((a, b) => categoryStats[a] > categoryStats[b] ? a : b);
    return { title, description: `Quiz importé avec ${questions.length} questions`, category: dominantCategory, difficulty: dominantDifficulty as 'easy' | 'medium' | 'hard', questions };
};

const mapDifficultyFromXML = (xmlDifficulty: string): 'easy' | 'medium' | 'hard' => {
    const mapping: Record<string, 'easy' | 'medium' | 'hard'> = { 'facile': 'easy', 'easy': 'easy', 'moyen': 'medium', 'medium': 'medium', 'moyenne': 'medium', 'difficile': 'hard', 'hard': 'hard', 'dur': 'hard' };
    return mapping[xmlDifficulty.toLowerCase()] || 'medium';
};

const removeSelectedFile = (): void => { selectedXMLFile.value = null; xmlQuizData.value = null; xmlParseError.value = ''; if (xmlFileInput.value) xmlFileInput.value.value = ''; };

const formatFileSize = (bytes: number): string => { if (bytes === 0) return '0 Bytes'; const k = 1024; const sizes = ['Bytes', 'KB', 'MB', 'GB']; const i = Math.floor(Math.log(bytes) / Math.log(k)); return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]; };

const submitXMLQuiz = async (): Promise<void> => {
    if (!xmlQuizData.value) { alert('Aucun quiz XML valide sélectionné'); return; }
    const xmlContent = selectedXMLFile.value ? await selectedXMLFile.value.text() : undefined;
    const newQuiz: Quiz = { id: quizIdCounter++, title: xmlQuizData.value.title, description: xmlQuizData.value.description || '', questionCount: xmlQuizData.value.questions.length, difficulty: (xmlQuizData.value.difficulty as 'easy' | 'medium' | 'hard') || 'medium', category: xmlQuizData.value.category || '', source: 'xml', xmlContent };
    quizzes.value.push(newQuiz);
    emit('quiz-added', newQuiz);
    closeQuizModal();
    removeSelectedFile();
};

const searchToshokanQuizzes = async (): Promise<void> => {
    if (!toshokanSearchQuery.value.trim()) { toshokanSearchError.value = 'Veuillez entrer des mots-clés de recherche'; return; }
    isSearchingToshokan.value = true; toshokanSearchError.value = ''; toshokanResults.value = [];
    try {
        const searchParams = new URLSearchParams({ q: toshokanSearchQuery.value, ...(toshokanFilters.value.difficulty && { difficulty: toshokanFilters.value.difficulty }), ...(toshokanFilters.value.category && { category: toshokanFilters.value.category }), limit: '20' });
        const response = await fetch(`https://toshokan.satsuki.azelakara.net/api/quiz/search?${searchParams}`, { method: 'GET', headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' } });
        if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);
        const data: ToshokanSearchResponse = await response.json();
        toshokanResults.value = data.sessions || [];
        if (toshokanResults.value.length === 0) toshokanSearchError.value = 'Aucun quiz trouvé avec ces critères';
    } catch (error) { console.error('Erreur lors de la recherche Toshokan:', error); toshokanSearchError.value = `Erreur de connexion à l'API Toshokan: ${error}`; } finally { isSearchingToshokan.value = false; }
};

const selectToshokanSession = (session: ToshokanSession): void => { selectedToshokanSession.value = session; };

const getDifficultyLabel = (difficulty: string): string => { const labels = { 'easy': 'Facile', 'medium': 'Moyen', 'hard': 'Difficile' }; return labels[difficulty as keyof typeof labels] || difficulty; };

const submitToshokanQuiz = (): void => {
    if (!selectedToshokanSession.value) { alert('Aucun quiz Toshokan sélectionné'); return; }
    const session = selectedToshokanSession.value;
    const newQuiz: Quiz = { id: quizIdCounter++, title: session.title, description: session.description || '', questionCount: session.questionCount, difficulty: session.difficulty, category: session.category, source: 'toshokan', toshokanId: session.id };
    quizzes.value.push(newQuiz);
    emit('quiz-added', newQuiz);
    closeQuizModal();
    selectedToshokanSession.value = null; toshokanSearchQuery.value = ''; toshokanResults.value = [];
};

const resetQuizModal = (): void => { activeQuizTab.value = 'manual'; selectedToshokanSession.value = null; toshokanSearchQuery.value = ''; toshokanResults.value = []; toshokanSearchError.value = ''; };
</script>

<style scoped>
/* keep styling inherited from parent */
</style>

