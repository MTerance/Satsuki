<template>
  <div />
</template>

<script setup lang="ts">
</script>

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
</script>
