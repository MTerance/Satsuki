const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');
const cors = require('cors');

class SocketServer {
    constructor(port = 3001) {
        this.port = port;
        this.app = express();
        this.server = createServer(this.app);
        this.io = new Server(this.server, {
            cors: {
                origin: ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
                methods: ["GET", "POST"],
                credentials: true
            },
            transports: ['websocket', 'polling']
        });

        this.setupMiddleware();
        this.setupRoutes();
        this.setupSocketHandlers();
        
        // État du serveur
        this.connectedClients = new Map();
        this.activeQuizzes = new Map();
        this.quizParticipants = new Map();
        this.sharedModels = new Map();
    }

    setupMiddleware() {
        this.app.use(cors({
            origin: ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
            credentials: true
        }));
        this.app.use(express.json());
        this.app.use(express.static('public'));
    }

    setupRoutes() {
        this.app.get('/', (req, res) => {
            res.json({
                message: 'Serveur Socket.IO pour Quiz 3D',
                status: 'running',
                connections: this.connectedClients.size,
                activeQuizzes: this.activeQuizzes.size,
                timestamp: new Date().toISOString()
            });
        });

        this.app.get('/status', (req, res) => {
            res.json({
                connectedClients: this.connectedClients.size,
                activeQuizzes: Array.from(this.activeQuizzes.keys()),
                participants: Object.fromEntries(this.quizParticipants),
                sharedModels: Array.from(this.sharedModels.keys())
            });
        });
    }

    setupSocketHandlers() {
        this.io.on('connection', (socket) => {
            console.log(`✅ Client connecté: ${socket.id}`);
            
            // Stocker les informations du client
            this.connectedClients.set(socket.id, {
                id: socket.id,
                connectedAt: new Date(),
                userName: null,
                currentQuiz: null,
                rooms: new Set()
            });

            // Événements de base
            this.setupBasicEvents(socket);
            
            // Événements du quiz 3D
            this.setupQuizEvents(socket);
            
            // Événements de synchronisation 3D
            this.setup3DEvents(socket);
            
            // Gestion de la déconnexion
            socket.on('disconnect', (reason) => {
                console.log(`❌ Client déconnecté: ${socket.id} (${reason})`);
                this.handleDisconnect(socket);
            });
        });
    }

    setupBasicEvents(socket) {
        // Rejoindre une room
        socket.on('join_room', (data) => {
            const { room, user } = data;
            socket.join(room);
            
            const client = this.connectedClients.get(socket.id);
            if (client) {
                client.rooms.add(room);
                if (user) {
                    client.userName = user.name || user.userName;
                }
            }
            
            socket.to(room).emit('participant:joined', {
                participant: { id: socket.id, name: client?.userName },
                room,
                timestamp: new Date().toISOString()
            });
            
            console.log(`👥 ${socket.id} a rejoint la room: ${room}`);
        });

        // Quitter une room
        socket.on('leave_room', (data) => {
            const { room } = data;
            socket.leave(room);
            
            const client = this.connectedClients.get(socket.id);
            if (client) {
                client.rooms.delete(room);
            }
            
            socket.to(room).emit('participant:left', {
                participant: { id: socket.id, name: client?.userName },
                room,
                timestamp: new Date().toISOString()
            });
            
            console.log(`👋 ${socket.id} a quitté la room: ${room}`);
        });
    }

    setupQuizEvents(socket) {
        // Démarrer un quiz
        socket.on('quiz:start', (data) => {
            const { quizId, userName } = data;
            console.log(`🎯 Démarrage du quiz ${quizId} pour ${userName}`);
            
            // Créer ou rejoindre le quiz
            if (!this.activeQuizzes.has(quizId)) {
                this.activeQuizzes.set(quizId, {
                    id: quizId,
                    startedAt: new Date(),
                    participants: new Map(),
                    currentQuestion: 0,
                    questions: this.generateSampleQuestions()
                });
            }

            const quiz = this.activeQuizzes.get(quizId);
            const roomName = `quiz_${quizId}`;
            
            // Ajouter le participant
            quiz.participants.set(socket.id, {
                id: socket.id,
                name: userName,
                score: 0,
                answers: [],
                joinedAt: new Date()
            });

            // Rejoindre la room du quiz
            socket.join(roomName);
            
            // Mettre à jour les informations du client
            const client = this.connectedClients.get(socket.id);
            if (client) {
                client.userName = userName;
                client.currentQuiz = quizId;
                client.rooms.add(roomName);
            }

            // Notifier le client du démarrage
            socket.emit('quiz:started', {
                quiz: {
                    id: quizId,
                    participantCount: quiz.participants.size
                },
                participant: quiz.participants.get(socket.id)
            });

            // Envoyer la première question
            this.sendNextQuestion(socket, quiz);

            // Notifier les autres participants
            socket.to(roomName).emit('participant:joined', {
                participant: { id: socket.id, name: userName }
            });
        });

        // Soumettre une réponse
        socket.on('quiz:submit_answer', (data) => {
            const { questionId, answer, timeTaken } = data;
            const client = this.connectedClients.get(socket.id);
            
            if (!client?.currentQuiz) {
                socket.emit('quiz:error', { message: 'Aucun quiz actif' });
                return;
            }

            const quiz = this.activeQuizzes.get(client.currentQuiz);
            const participant = quiz?.participants.get(socket.id);
            
            if (!quiz || !participant) {
                socket.emit('quiz:error', { message: 'Quiz ou participant introuvable' });
                return;
            }

            // Vérifier la réponse
            const question = quiz.questions.find(q => q.id === questionId);
            const isCorrect = question && answer === question.correctAnswer;
            const points = isCorrect ? Math.max(10 - Math.floor(timeTaken / 3), 1) : 0;

            // Enregistrer la réponse
            const answerRecord = {
                questionId,
                answer,
                isCorrect,
                points,
                timeTaken,
                timestamp: new Date()
            };

            participant.answers.push(answerRecord);
            participant.score += points;

            // Envoyer le résultat
            socket.emit('quiz:answer_result', {
                ...answerRecord,
                correctAnswer: question?.correctAnswer,
                explanation: question?.explanation
            });

            // Envoyer la question suivante ou terminer
            if (participant.answers.length < quiz.questions.length) {
                setTimeout(() => {
                    this.sendNextQuestion(socket, quiz);
                }, 2000);
            } else {
                this.finishQuizForParticipant(socket, quiz);
            }

            // Mettre à jour le leaderboard
            this.updateLeaderboard(client.currentQuiz);

            console.log(`📝 ${participant.name} a répondu: ${answer} (${isCorrect ? 'correct' : 'incorrect'}) - ${points} points`);
        });
    }

    setup3DEvents(socket) {
        // Synchronisation de caméra 3D
        socket.on('3d:sync_camera', (data) => {
            const { position, rotation, timestamp } = data;
            const client = this.connectedClients.get(socket.id);
            
            // Diffuser à tous les clients connectés sauf l'expéditeur
            socket.broadcast.emit('3d:camera_sync', {
                userId: socket.id,
                userName: client?.userName,
                position,
                rotation,
                timestamp
            });

            console.log(`📷 Synchronisation caméra 3D de ${client?.userName || socket.id}`);
        });

        // Chargement de modèle 3D partagé
        socket.on('3d:load_model', (data) => {
            const { modelPath, modelData, timestamp } = data;
            const client = this.connectedClients.get(socket.id);
            
            // Stocker le modèle partagé
            this.sharedModels.set(modelPath, {
                path: modelPath,
                data: modelData,
                loadedBy: socket.id,
                userName: client?.userName,
                timestamp: new Date()
            });

            // Diffuser à tous les clients
            this.io.emit('3d:model_loaded', {
                modelPath,
                modelData,
                loadedBy: socket.id,
                userName: client?.userName,
                timestamp
            });

            console.log(`🎨 Modèle 3D chargé: ${modelPath} par ${client?.userName || socket.id}`);
        });
    }

    generateSampleQuestions() {
        return [
            {
                id: 1,
                text: "Combien de faces a un cube ?",
                type: "3d-object",
                options: ["4", "6", "8", "12"],
                correctAnswer: "6",
                explanation: "Un cube a 6 faces carrées identiques.",
                model3D: "/models/cube.glb"
            },
            {
                id: 2,
                text: "Quelle est la forme géométrique avec le plus de côtés parmi ces options ?",
                type: "3d-object",
                options: ["Triangle", "Carré", "Pentagone", "Hexagone"],
                correctAnswer: "Hexagone",
                explanation: "Un hexagone a 6 côtés, plus que les autres formes proposées.",
                model3D: "/models/polygon.glb"
            },
            {
                id: 3,
                text: "Dans un repère 3D, quel axe représente généralement la hauteur ?",
                type: "3d-scene",
                options: ["X", "Y", "Z", "W"],
                correctAnswer: "Y",
                explanation: "L'axe Y représente généralement la hauteur dans un repère 3D standard.",
                model3D: "/models/axes.glb"
            }
        ];
    }

    sendNextQuestion(socket, quiz) {
        const participant = quiz.participants.get(socket.id);
        const questionIndex = participant.answers.length;
        
        if (questionIndex < quiz.questions.length) {
            const question = quiz.questions[questionIndex];
            socket.emit('quiz:question', {
                question: {
                    id: question.id,
                    text: question.text,
                    type: question.type,
                    options: question.options,
                    model3D: question.model3D
                },
                questionNumber: questionIndex + 1,
                totalQuestions: quiz.questions.length
            });
        }
    }

    finishQuizForParticipant(socket, quiz) {
        const participant = quiz.participants.get(socket.id);
        const client = this.connectedClients.get(socket.id);
        
        socket.emit('quiz:finished', {
            finalScore: participant.score,
            totalQuestions: quiz.questions.length,
            answers: participant.answers,
            completedAt: new Date()
        });

        console.log(`🏁 Quiz terminé pour ${participant.name} - Score: ${participant.score}`);
    }

    updateLeaderboard(quizId) {
        const quiz = this.activeQuizzes.get(quizId);
        if (!quiz) return;

        const leaderboard = Array.from(quiz.participants.values())
            .sort((a, b) => b.score - a.score)
            .map((participant, index) => ({
                rank: index + 1,
                id: participant.id,
                name: participant.name,
                score: participant.score,
                answersCount: participant.answers.length
            }));

        const roomName = `quiz_${quizId}`;
        this.io.to(roomName).emit('quiz:leaderboard', { leaderboard });
    }

    handleDisconnect(socket) {
        const client = this.connectedClients.get(socket.id);
        
        if (client) {
            // Notifier les rooms de la déconnexion
            for (const room of client.rooms) {
                socket.to(room).emit('participant:left', {
                    participant: { id: socket.id, name: client.userName }
                });
            }

            // Retirer des quiz actifs
            if (client.currentQuiz) {
                const quiz = this.activeQuizzes.get(client.currentQuiz);
                if (quiz) {
                    quiz.participants.delete(socket.id);
                    if (quiz.participants.size === 0) {
                        this.activeQuizzes.delete(client.currentQuiz);
                        console.log(`🗑️ Quiz ${client.currentQuiz} supprimé (aucun participant)`);
                    } else {
                        this.updateLeaderboard(client.currentQuiz);
                    }
                }
            }
        }

        this.connectedClients.delete(socket.id);
    }

    start() {
        this.server.listen(this.port, () => {
            console.log(`🚀 Serveur Socket.IO démarré sur le port ${this.port}`);
            console.log(`📡 Interface web: http://localhost:${this.port}`);
            console.log(`🔌 Socket.IO endpoint: ws://localhost:${this.port}`);
        });
    }

    stop() {
        this.server.close(() => {
            console.log('🛑 Serveur Socket.IO arrêté');
        });
    }
}

// Démarrer le serveur si ce fichier est exécuté directement
if (require.main === module) {
    const server = new SocketServer(3001);
    server.start();

    // Gérer l'arrêt propre
    process.on('SIGINT', () => {
        console.log('\n🛑 Arrêt du serveur...');
        server.stop();
        process.exit(0);
    });
}

module.exports = SocketServer;