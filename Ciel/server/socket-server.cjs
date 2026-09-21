const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');
const cors = require('cors');

// Cibles d'ordre reconnues (miroir de Satsuki/Systems/ServerManager.cs - DispatchOrderRequest)
const OrderTarget = Object.freeze({
    SYSTEM: 'System',
    SCENE: 'Scene',
    QUIZZ: 'Quizz'
});

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
        this.app.use(cors());
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

    // === LOGIQUE MÉTIER (réutilisée par les événements bruts et les OrderRequest) ===

    handlePlayerAdded(socket, playerData) {
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
    }

    handlePlayerRemoved(socket, removeData) {
        console.log(`🗑️ Suppression joueur ID:`, removeData.id);

        const removedPlayer = this.gamePlayers.get(removeData.id);

        if (removedPlayer) {
            this.gamePlayers.delete(removeData.id);

            socket.emit('player_removed_response', {
                success: true,
                message: `Joueur ${removedPlayer.name} supprimé avec succès`,
                playerId: removeData.id,
                totalPlayers: this.gamePlayers.size
            });

            socket.broadcast.emit('player_left', {
                playerId: removeData.id,
                playerName: removedPlayer.name,
                totalPlayers: this.gamePlayers.size
            });

            console.log(`📊 Total joueurs: ${this.gamePlayers.size}`);
        } else {
            socket.emit('player_removed_response', {
                success: false,
                message: `Joueur avec ID ${removeData.id} non trouvé`,
                playerId: removeData.id
            });
        }
    }

    handleQuizAdded(socket, quizData) {
        console.log(`📝 Nouveau quiz ajouté:`, quizData);

        this.gameQuizzes.set(quizData.id, {
            ...quizData,
            createdBy: socket.id,
            createdAt: new Date().toISOString()
        });

        socket.emit('quiz_added_response', {
            success: true,
            message: `Quiz "${quizData.title}" créé avec succès`,
            quiz: quizData,
            totalQuizzes: this.gameQuizzes.size
        });

        socket.broadcast.emit('quiz_created', {
            quiz: quizData,
            createdBy: this.connectedClients.get(socket.id)?.name || 'Utilisateur anonyme',
            totalQuizzes: this.gameQuizzes.size
        });

        console.log(`📊 Total quiz: ${this.gameQuizzes.size}`);
    }

    handleQuizRemoved(socket, removeData) {
        console.log(`🗑️ Suppression quiz ID:`, removeData.id);

        const removedQuiz = this.gameQuizzes.get(removeData.id);

        if (removedQuiz) {
            this.gameQuizzes.delete(removeData.id);

            socket.emit('quiz_removed_response', {
                success: true,
                message: `Quiz "${removedQuiz.title}" supprimé avec succès`,
                quizId: removeData.id,
                totalQuizzes: this.gameQuizzes.size
            });

            socket.broadcast.emit('quiz_deleted', {
                quizId: removeData.id,
                quizTitle: removedQuiz.title,
                deletedBy: this.connectedClients.get(socket.id)?.name || 'Utilisateur anonyme',
                totalQuizzes: this.gameQuizzes.size
            });

            console.log(`📊 Total quiz: ${this.gameQuizzes.size}`);
        } else {
            socket.emit('quiz_removed_response', {
                success: false,
                message: `Quiz avec ID ${removeData.id} non trouvé`,
                quizId: removeData.id
            });
        }
    }

    handleGetPlayers(socket) {
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
    }

    // === DISPATCH DES ORDERREQUEST (format Satsuki) ===

    /**
     * Dispatch un OrderRequest selon sa Target et son Order.
     * Format : { ClientId, Target, Order, JsonData }
     * (cf. Satsuki/Models/OrderRequest.cs et Satsuki/Systems/ServerManager.cs)
     */
    dispatchOrderRequest(socket, orderRequest) {
        const { ClientId, Target, Order, JsonData } = orderRequest;

        if (!Order || !Target) {
            console.warn(`⚠️ OrderRequest invalide reçu de ${socket.id}:`, orderRequest);
            socket.emit('order_error', {
                success: false,
                message: 'OrderRequest invalide: Target et Order sont requis',
                orderRequest
            });
            return;
        }

        // JsonData est une chaîne JSON (cf. sérialisation côté Satsuki)
        let data = {};
        if (JsonData) {
            try {
                data = JSON.parse(JsonData);
            } catch (error) {
                console.error(`❌ Impossible de désérialiser JsonData pour l'ordre '${Order}':`, error.message);
                socket.emit('order_error', {
                    success: false,
                    message: `JsonData invalide pour l'ordre '${Order}': ${error.message}`,
                    orderRequest
                });
                return;
            }
        }

        console.log(`📨 Order '${Order}' reçu de ${ClientId} pour target '${Target}'`);

        switch (Target) {
            case OrderTarget.QUIZZ:
                this.dispatchQuizzOrder(socket, Order, data);
                break;
            case OrderTarget.SCENE:
                this.dispatchSceneOrder(socket, Order, data);
                break;
            case OrderTarget.SYSTEM:
                this.dispatchSystemOrder(socket, Order, data);
                break;
            default:
                console.error(`❌ Target inconnue '${Target}' pour l'ordre '${Order}'`);
                socket.emit('order_error', {
                    success: false,
                    message: `Target inconnue '${Target}' pour l'ordre '${Order}'`,
                    orderRequest
                });
        }
    }

    dispatchQuizzOrder(socket, order, data) {
        switch (order) {
            case 'player_added':
                this.handlePlayerAdded(socket, data);
                break;
            case 'player_removed':
                this.handlePlayerRemoved(socket, data);
                break;
            case 'quiz_added':
                this.handleQuizAdded(socket, data);
                break;
            case 'quiz_removed':
                this.handleQuizRemoved(socket, data);
                break;
            case 'get_players':
                this.handleGetPlayers(socket);
                break;
            default:
                console.warn(`⚠️ Ordre Quizz non géré: '${order}'`);
                socket.emit('order_error', {
                    success: false,
                    message: `Ordre Quizz non géré: '${order}'`
                });
        }
    }

    dispatchSceneOrder(socket, order, data) {
        // Les ordres de scène sont retransmis à tous les clients
        console.log(`🎬 Ordre de scène: '${order}'`, data);
        this.io.emit('scene_order', { order, data, timestamp: new Date().toISOString() });
    }

    dispatchSystemOrder(socket, order, data) {
        switch (order) {
            case 'ping':
                socket.emit('pong', { timestamp: new Date().toISOString() });
                break;
            case 'get_status':
                socket.emit('server_status', {
                    connections: this.connectedClients.size,
                    players: this.gamePlayers.size,
                    quizzes: this.gameQuizzes.size,
                    timestamp: new Date().toISOString()
                });
                break;
            default:
                console.warn(`⚠️ Ordre System non géré: '${order}'`);
                socket.emit('order_error', {
                    success: false,
                    message: `Ordre System non géré: '${order}'`
                });
        }
    }

    // === GESTION DES CONNEXIONS SOCKET.IO ===

    setupSocketHandlers() {
        this.io.on('connection', (socket) => {
            console.log(`✅ Client connecté: ${socket.id}`);

            this.connectedClients.set(socket.id, {
                id: socket.id,
                connectedAt: new Date()
            });

            socket.emit('welcome', { message: 'Bienvenue sur le serveur Socket.IO!' });

            // === CANAL ORDERREQUEST (format Satsuki) ===
            socket.on('order_request', (orderRequest) => {
                this.dispatchOrderRequest(socket, orderRequest);
            });

            // === ÉVÉNEMENTS BRUTS (compatibilité descendante) ===
            socket.on('player_added', (playerData) => this.handlePlayerAdded(socket, playerData));
            socket.on('player_removed', (removeData) => this.handlePlayerRemoved(socket, removeData));
            socket.on('quiz_added', (quizData) => this.handleQuizAdded(socket, quizData));
            socket.on('quiz_removed', (removeData) => this.handleQuizRemoved(socket, removeData));
            socket.on('get_players', () => this.handleGetPlayers(socket));
            
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