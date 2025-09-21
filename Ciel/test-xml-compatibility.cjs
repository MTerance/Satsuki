// Test de compatibilité pour parseXMLQuiz
const fs = require('fs');

// Simuler DOMParser pour Node.js
const { DOMParser } = require('xmldom');
global.DOMParser = DOMParser;

// Fonction parseXMLQuiz mise à jour
const parseXMLQuiz = (xmlContent) => {
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
    
    // Extraire le nom du quiz (NOUVEAU: title au lieu de nom_du_quizz)
    const titleElement = doc.querySelector('title');
    const title = titleElement?.textContent || 'Quiz sans titre';
    
    // Extraire les informations du summary (NOUVEAU: question_count au lieu de nombre_de_questions)
    const questionCountElement = doc.querySelector('question_count');
    const expectedQuestionCount = questionCountElement ? parseInt(questionCountElement.textContent || '0') : 0;
    
    // Extraire les questions
    const questionElements = doc.querySelectorAll('question');
    const questions = Array.from(questionElements).map((qElement, index) => {
        const questionText = qElement.querySelector('text')?.textContent || `Question ${index + 1}`; // NOUVEAU: text au lieu de texte
        const category = qElement.querySelector('category')?.textContent || ''; // NOUVEAU: category au lieu de categorie
        const difficulty = qElement.getAttribute('difficulty') || 'medium'; // NOUVEAU: difficulty au lieu de difficulte
        
        // Extraire les options de réponse (NOUVEAU: choices au lieu de choix)
        const optionElements = qElement.querySelectorAll('choices option');
        const answers = Array.from(optionElements).map(option => option.textContent || '');
        
        // Trouver l'index de la réponse correcte (NOUVEAU: correct au lieu de correcte)
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
    
    return {
        title,
        description: `Quiz importé avec ${questions.length} questions`,
        questions
    };
};

// Fonction utilitaire pour mapper les difficultés XML vers notre format
const mapDifficultyFromXML = (xmlDifficulty) => {
    const mapping = {
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

// Test avec notre fichier XML
try {
    const xmlContent = fs.readFileSync('src/assets/fule_quizz_exemple.xml', 'utf8');
    console.log('🔍 Test de compatibilité XML...\n');
    
    const result = parseXMLQuiz(xmlContent);
    
    console.log('✅ Parsing réussi !');
    console.log('📊 Résultats:');
    console.log(`   Titre: ${result.title}`);
    console.log(`   Description: ${result.description}`);
    console.log(`   Nombre de questions: ${result.questions.length}`);
    
    console.log('\n🎯 Questions trouvées:');
    result.questions.forEach((q, i) => {
        console.log(`   ${i + 1}. [${q.category}] ${q.question.substring(0, 50)}...`);
        console.log(`      Difficulté: ${q.difficulty}`);
        console.log(`      Réponses: ${q.answers.length}`);
        console.log(`      Réponse correcte: ${q.answers[q.correctAnswer]}`);
    });
    
} catch (error) {
    console.error('❌ Erreur lors du test:', error.message);
    process.exit(1);
}