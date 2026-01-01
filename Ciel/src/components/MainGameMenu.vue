<script lang="ts">
import MainGameMenu from './gameMenu/MainGameMenu.vue';
export default MainGameMenu;
</script>

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