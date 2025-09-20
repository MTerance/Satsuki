const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');

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
            
            // Gestion de la déconnexion
            socket.on('disconnect', (reason) => {
                console.log(`❌ Client déconnecté: ${socket.id} (${reason})`);
                this.connectedClients.delete(socket.id);
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