import { ref, computed } from 'vue';

// Types de client reconnus par le serveur Satsuki (cf. ServerManager.IsValidClientType)
export const ClientType = {
    BACKEND: 'BACKEND',
    PLAYER: 'PLAYER',
    OTHER: 'OTHER'
};

// Cibles d'ordre (cf. ServerManager.DispatchOrderRequest)
export const OrderTarget = {
    SYSTEM: 'System',
    SCENE: 'Scene',
    QUIZZ: 'Quizz'
};

/**
 * Service renderer qui enveloppe window.satsuki (client TCP du main Electron)
 * pour dialoguer avec le serveur Satsuki (Godot).
 *
 * Le handshake (RequestClientType -> ClientTypeResponse) est géré par le main
 * process. Ce service expose un état réactif et une API simple d'envoi d'ordres.
 */
class ClientService {
    constructor() {
        this.isConnected = ref(false);
        this.status = ref('disconnected'); // disconnected | connecting | connected | error
        this.clientId = ref(null);
        this.clientType = ref(null);
        this._listenersBound = false;
        this._messageHandlers = new Map(); // order -> Set<callback>
    }

    // L'API preload est-elle disponible (contexte Electron) ?
    get available() {
        return typeof window !== 'undefined' && !!window.satsuki;
    }

    _bindIpcListeners() {
        if (this._listenersBound || !this.available) return;
        this._listenersBound = true;

        window.satsuki.onStatus((s) => {
            this.isConnected.value = !!s.connected;
            this.status.value = s.connected ? 'connected' : 'disconnected';
            if (s.clientId !== undefined) this.clientId.value = s.clientId;
            if (s.clientType !== undefined) this.clientType.value = s.clientType;
        });

        window.satsuki.onError((err) => {
            console.error('[ClientService] Erreur Satsuki:', err);
            this.status.value = 'error';
        });

        window.satsuki.onMessage((payload) => this._routeMessage(payload));
    }

    // Route un message entrant vers les handlers enregistrés selon son "order"
    _routeMessage(payload) {
        const data = payload?.data;
        if (data && typeof data === 'object' && data.order) {
            const set = this._messageHandlers.get(data.order);
            if (set) for (const cb of set) cb(data);
        }
        // Handler générique (tous messages)
        const all = this._messageHandlers.get('*');
        if (all) for (const cb of all) cb(payload);
    }

    /**
     * Connecte au serveur Satsuki.
     * @param {object} opts { host, port, clientType, password }
     */
    async connect(opts = {}) {
        if (!this.available) {
            console.warn('[ClientService] window.satsuki indisponible (hors Electron)');
            this.status.value = 'error';
            return { success: false, message: 'API satsuki indisponible' };
        }
        this._bindIpcListeners();
        this.status.value = 'connecting';
        const res = await window.satsuki.connect({
            host: opts.host || '127.0.0.1',
            port: opts.port || 3002,
            clientType: opts.clientType || ClientType.BACKEND,
            password: opts.password
        });
        if (!res.success) this.status.value = 'error';
        return res;
    }

    async disconnect() {
        if (!this.available) return { success: false, message: 'indisponible' };
        const res = await window.satsuki.disconnect();
        this.isConnected.value = false;
        this.status.value = 'disconnected';
        this.clientId.value = null;
        return res;
    }

    /**
     * Envoie un OrderRequest au serveur Satsuki.
     * @param {string} order - nom de l'ordre
     * @param {object|string} data - données (sérialisées dans JsonData)
     * @param {string} target - OrderTarget
     */
    async sendOrder(order, data = {}, target = OrderTarget.QUIZZ) {
        if (!this.available) {
            console.warn('[ClientService] window.satsuki indisponible');
            return { success: false, message: 'indisponible' };
        }
        if (!this.isConnected.value) {
            console.warn('[ClientService] Non connecté, ordre ignoré:', order);
            return { success: false, message: 'non connecté' };
        }
        return window.satsuki.sendOrder({
            ClientId: this.clientId.value || 'ciel-client',
            Target: target,
            Order: order,
            JsonData: typeof data === 'string' ? data : JSON.stringify(data)
        });
    }

    /**
     * Enregistre un handler pour un ordre entrant (ex: 'ClientTypeConfirmation').
     * Utiliser '*' pour tous les messages.
     */
    onOrder(order, callback) {
        if (!this._messageHandlers.has(order)) this._messageHandlers.set(order, new Set());
        this._messageHandlers.get(order).add(callback);
        return () => this.offOrder(order, callback);
    }

    offOrder(order, callback) {
        this._messageHandlers.get(order)?.delete(callback);
    }

    async getStatus() {
        if (!this.available) return { connected: false };
        return window.satsuki.getStatus();
    }
}

const clientService = new ClientService();
export default clientService;
