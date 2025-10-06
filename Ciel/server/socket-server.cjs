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
        this.gamePlayers = new Map(); // Stocker les joueurs du jeu
        this.gameQuizzes = new Map(); // Stocker les quiz du jeu
    }

    setupMiddleware() {
        this.app.use(express.json());
        this.app.use(express.static('public'));
    }

    setupRoutes() {
        this.app.get('/', (req, res) => {
            res.json({
                message: 'Serveur Socket.IO pour Quiz 3D',
                status: 'running',
                connections: this.connectedClients.size,
                players: this.gamePlayers.size,
                quizzes: this.gameQuizzes.size,
                timestamp: new Date().toISOString()
            });
        });
    }

    setupSocketHandlers() {
        this.io.on('connection', (socket) => {
            console.log(`✅ Client connecté: ${socket.id}`);
            
            // Stocker les informations du client
            this.connectedClients.set(socket.id, {
                id: socket.id,
                connectedAt: new Date()
            });

            // Test de base
            socket.emit('welcome', { message: 'Bienvenue sur le serveur Socket.IO!' });
            
            // === GESTION DES JOUEURS ===
            socket.on('player_added', (playerData) => {
                console.log(`👤 Nouveau joueur ajouté:`, playerData);
                
                // Stocker le joueur
                this.gamePlayers.set(playerData.id, {
                    ...playerData,
                    socketId: socket.id,
                    addedAt: new Date()
                });
                
                // Confirmer au client
                socket.emit('player_added_response', {
                    success: true,
                    message: `Joueur ${playerData.name} ajouté avec succès`,
                    player: playerData,
                    totalPlayers: this.gamePlayers.size
                });
                
                // Notifier tous les autres clients
                socket.broadcast.emit('player_joined', {
                    player: playerData,
                    totalPlayers: this.gamePlayers.size
                });
                
                console.log(`📊 Total joueurs: ${this.gamePlayers.size}`);
            });
            
            socket.on('player_removed', (removeData) => {
                console.log(`🗑️ Suppression joueur ID:`, removeData.id);
                
                const removedPlayer = this.gamePlayers.get(removeData.id);
                
                if (removedPlayer) {
                    // Supprimer le joueur
                    this.gamePlayers.delete(removeData.id);
                    
                    // Confirmer au client
                    socket.emit('player_removed_response', {
                        success: true,
                        message: `Joueur ${removedPlayer.name} supprimé avec succès`,
                        playerId: removeData.id,
                        totalPlayers: this.gamePlayers.size
                    });
                    
                    // Notifier tous les autres clients
                    socket.broadcast.emit('player_left', {
                        playerId: removeData.id,
                        playerName: removedPlayer.name,
                        totalPlayers: this.gamePlayers.size
                    });
                    
                    console.log(`📊 Total joueurs: ${this.gamePlayers.size}`);
                } else {
                    // Joueur non trouvé
                    socket.emit('player_removed_response', {
                        success: false,
                        message: `Joueur avec ID ${removeData.id} non trouvé`,
                        playerId: removeData.id
                    });
                }
            });
            
            // === GESTIONNAIRES D'ÉVÉNEMENTS POUR LES QUIZ ===
            
            socket.on('quiz_added', (quizData) => {
                console.log(`📝 Nouveau quiz ajouté:`, quizData);
                
                // Stocker le quiz
                this.gameQuizzes.set(quizData.id, {
                    ...quizData,
                    createdBy: socket.id,
                    createdAt: new Date().toISOString()
                });
                
                // Confirmer au client
                socket.emit('quiz_added_response', {
                    success: true,
                    message: `Quiz "${quizData.title}" créé avec succès`,
                    quiz: quizData,
                    totalQuizzes: this.gameQuizzes.size
                });
                
                // Notifier tous les autres clients
                socket.broadcast.emit('quiz_created', {
                    quiz: quizData,
                    createdBy: this.connectedClients.get(socket.id)?.name || 'Utilisateur anonyme',
                    totalQuizzes: this.gameQuizzes.size
                });
                
                console.log(`📊 Total quiz: ${this.gameQuizzes.size}`);
            });
            
            socket.on('quiz_removed', (removeData) => {
                console.log(`🗑️ Suppression quiz ID:`, removeData.id);
                
                const removedQuiz = this.gameQuizzes.get(removeData.id);
                
                if (removedQuiz) {
                    // Supprimer le quiz
                    this.gameQuizzes.delete(removeData.id);
                    
                    // Confirmer au client
                    socket.emit('quiz_removed_response', {
                        success: true,
                        message: `Quiz "${removedQuiz.title}" supprimé avec succès`,
                        quizId: removeData.id,
                        totalQuizzes: this.gameQuizzes.size
                    });
                    
                    // Notifier tous les autres clients
                    socket.broadcast.emit('quiz_deleted', {
                        quizId: removeData.id,
                        quizTitle: removedQuiz.title,
                        deletedBy: this.connectedClients.get(socket.id)?.name || 'Utilisateur anonyme',
                        totalQuizzes: this.gameQuizzes.size
                    });
                    
                    console.log(`📊 Total quiz: ${this.gameQuizzes.size}`);
                } else {
                    // Quiz non trouvé
                    socket.emit('quiz_removed_response', {
                        success: false,
                        message: `Quiz avec ID ${removeData.id} non trouvé`,
                        quizId: removeData.id
                    });
                }
            });
            
            // Obtenir la liste des joueurs
            socket.on('get_players', () => {
                const playersList = Array.from(this.gamePlayers.values()).map(player => ({
                    id: player.id,
                    name: player.name,
                    gender: player.gender,
                    color: player.color
                }));
                
                socket.emit('players_list', {
                    players: playersList,
                    totalPlayers: this.gamePlayers.size
                });
            });
            
            // Gestion de la déconnexion
            socket.on('disconnect', (reason) => {
                console.log(`❌ Client déconnecté: ${socket.id} (${reason})`);
                this.connectedClients.delete(socket.id);
                
                // Supprimer tous les joueurs associés à cette connexion
                const playersToRemove = [];
                for (const [playerId, player] of this.gamePlayers.entries()) {
                    if (player.socketId === socket.id) {
                        playersToRemove.push({ id: playerId, name: player.name });
                    }
                }
                
                playersToRemove.forEach(player => {
                    this.gamePlayers.delete(player.id);
                    console.log(`🗑️ Joueur ${player.name} supprimé suite à la déconnexion`);
                });
                
                if (playersToRemove.length > 0) {
                    // Notifier les autres clients
                    socket.broadcast.emit('players_disconnected', {
                        removedPlayers: playersToRemove,
                        totalPlayers: this.gamePlayers.size
                    });
                }
            });
        });
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
    const server = new SocketServer(3002);
    server.start();

    // Gérer l'arrêt propre
    process.on('SIGINT', () => {
        console.log('\n🛑 Arrêt du serveur...');
        server.stop();
        process.exit(0);
    });
}

module.exports = SocketServer;