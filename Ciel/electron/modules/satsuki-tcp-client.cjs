const net = require('net');
const crypto = require('crypto');

/**
 * Client TCP pour le serveur Satsuki (Godot).
 *
 * Protocole :
 *  - Transport : TCP brut, messages JSON UTF-8 délimités par '\n'
 *  - Cryptage  : AES-256-CBC / PKCS7, sortie Base64
 *  - Handshake : serveur -> {order:"RequestClientType"} ; client -> type+password
 *  - Ordres    : OrderRequest { ClientId, Target, Order, JsonData }
 *
 * Le serveur crypte par défaut ses messages sortants avec les clés ci-dessous.
 * On tente un décryptage ; si le message est en clair on le garde tel quel.
 */

// Clés par défaut (cf. Satsuki/Utils/MessageCryptoSystem.cs).
// La chaîne source fait 34 caractères, ce qui est invalide pour AES-256 (32 bytes).
// Côté serveur (MessageCryptoSystem.cs), Encoding.UTF8.GetBytes() direct avec 34 bytes
// lève une CryptographicException, attrapée silencieusement → Encrypt/Decrypt renvoient
// le texte inchangé. En l'état, le serveur envoie donc EN CLAIR et ne peut pas décrypter.
//
// Stratégie client :
//  - Réception : tolérer clair ET crypté (détection looksEncrypted + tentative decrypt)
//  - Émission : SHA-256 de la chaîne = 32 bytes déterministes, à aligner avec un serveur
//    corrigé (MessageCrypto doit alors utiliser SHA256 de la même chaîne).
//  - Mode adaptatif : si le serveur envoie en clair (bug actuel), on lui renvoie en clair
//    pour que ProcessMessage puisse désérialiser ; sinon on crypte.
const KEY_SOURCE = 'SatsukiGameServer2024Key1234567890';
const IV_SOURCE = 'SatsukiInitVect1';

// Clé 32 bytes via SHA-256 (déterministe, toute longueur d'entrée)
const DEFAULT_KEY = crypto.createHash('sha256').update(KEY_SOURCE, 'utf8').digest();
// IV 16 bytes : la chaîne source fait exactement 16 caractères
const DEFAULT_IV = Buffer.from(IV_SOURCE, 'utf8');

const BACKEND_PASSWORD = '***Satsuk1***'; // cf. Satsuki/Systems/ServerManager.cs

function encrypt(plainText, key = DEFAULT_KEY, iv = DEFAULT_IV) {
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  let encrypted = cipher.update(plainText, 'utf8', 'base64');
  encrypted += cipher.final('base64');
  return encrypted;
}

function decrypt(base64Text, key = DEFAULT_KEY, iv = DEFAULT_IV) {
  const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
  let decrypted = decipher.update(base64Text, 'base64', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

// Détecte si une chaîne ressemble à du Base64 AES-CBC (longueur multiple de 16 bytes décodée)
function looksEncrypted(text) {
  if (!text || /[{[]/.test(text[0])) return false; // commence par { ou [ => JSON clair
  if (!/^[A-Za-z0-9+/=]+$/.test(text)) return false;
  try {
    const buf = Buffer.from(text, 'base64');
    return buf.length > 0 && buf.length % 16 === 0;
  } catch {
    return false;
  }
}

class SatsukiTcpClient {
  constructor() {
    this.socket = null;
    this.mainWindow = null;
    this.connected = false;
    this.clientId = null;
    this.clientType = null;
    this.buffer = ''; // accumulateur pour délimiter les messages par '\n'
    this.host = '127.0.0.1';
    this.port = 3002;
    // Dernier état de jeu reçu via GAME_STATE: (cf. ServerManager.SendGameStateToClient)
    this.gameState = null;
    // Mode adaptatif : le serveur actuel (clé invalide) envoie en clair — on s'aligne.
    // Dès qu'un message serveur crypté est détecté, on repasse en crypté.
    this.serverEncrypts = false;
  }

  setMainWindow(win) {
    this.mainWindow = win;
  }

  // Envoie un événement vers le renderer
  _notify(channel, payload) {
    if (this.mainWindow && !this.mainWindow.isDestroyed()) {
      this.mainWindow.webContents.send(channel, payload);
    }
  }

  _setStatus(status) {
    this._notify('satsuki-status', status);
  }

  /**
   * Connecte au serveur Satsuki.
   * @param {object} opts { host, port, clientType, password }
   */
  connect(opts = {}) {
    const {
      host = '127.0.0.1',
      port = 3002,
      clientType = 'BACKEND',
      password = BACKEND_PASSWORD
    } = opts;

    this.host = host;
    this.port = port;

    return new Promise((resolve) => {
      try {
        this.disconnect();

        this.socket = new net.Socket();
        this.socket.setNoDelay(true);
        this.buffer = '';

        const onConnectTimeout = setTimeout(() => {
          if (!this.connected) {
            this.socket.destroy();
            resolve({ success: false, message: 'Connection timeout' });
          }
        }, 10000);

        this.socket.connect(port, host, () => {
          clearTimeout(onConnectTimeout);
          this.connected = true;
          this.clientType = clientType;
          this._pendingPassword = password;
          console.log(`[SatsukiTCP] Connecté à ${host}:${port}`);
          this._setStatus({ connected: true, host, port });
          resolve({ success: true, message: `Connecté à ${host}:${port}` });
        });

        this.socket.on('data', (data) => this._onData(data));

        this.socket.on('error', (err) => {
          clearTimeout(onConnectTimeout);
          console.error('[SatsukiTCP] Erreur:', err.message);
          this._notify('satsuki-error', err.message);
          if (!this.connected) {
            resolve({ success: false, message: err.message });
          }
        });

        this.socket.on('close', () => {
          console.log('[SatsukiTCP] Connexion fermée');
          this.connected = false;
          this.clientId = null;
          this._setStatus({ connected: false });
        });
      } catch (err) {
        resolve({ success: false, message: err.message });
      }
    });
  }

  // Réception : accumulation + split par ligne, décryptage si nécessaire.
  // Le serveur n'ajoute PAS toujours '\n' (handshake crypté envoyé sans terminateur) :
  // on traite donc aussi le buffer résiduel s'il forme un message Base64/JSON complet.
  _onData(data) {
    this.buffer += data.toString('utf8');
    this._flushBuffer();
  }

  _flushBuffer() {
    // 1) Traiter toutes les lignes terminées par '\n'
    let idx;
    while ((idx = this.buffer.indexOf('\n')) !== -1) {
      const rawLine = this.buffer.slice(0, idx).replace(/\r$/, '');
      this.buffer = this.buffer.slice(idx + 1);
      if (rawLine.trim().length > 0) {
        this._handleLine(rawLine.trim());
      }
    }

    // 2) Buffer résiduel SANS '\n' : si c'est un message Base64 AES complet
    //    (longueur décodée multiple de 16) ou du JSON complet, le traiter tout de suite.
    const rest = this.buffer.trim();
    if (rest.length > 0 && (looksEncrypted(rest) || this._isCompleteJson(rest))) {
      this.buffer = '';
      this._handleLine(rest);
    }
  }

  // Détecte un objet JSON complet (accolades équilibrées, fin sur '}')
  _isCompleteJson(text) {
    if (!text.startsWith('{') || !text.endsWith('}')) return false;
    let depth = 0, inString = false, escape = false;
    for (const ch of text) {
      if (escape) { escape = false; continue; }
      if (ch === '\\') { escape = true; continue; }
      if (ch === '"') { inString = !inString; continue; }
      if (inString) continue;
      if (ch === '{') depth++;
      else if (ch === '}') { depth--; if (depth < 0) return false; }
    }
    return depth === 0;
  }

  _handleLine(line) {
    let message = line;

    // Tente un décryptage si la ligne ressemble à du Base64 AES.
    if (looksEncrypted(line)) {
      try {
        message = decrypt(line);
        // Le serveur crypte réellement → aligner nos envois
        if (!this.serverEncrypts) {
          this.serverEncrypts = true;
          console.log('[SatsukiTCP] Serveur en mode crypté détecté');
        }
      } catch {
        message = line; // garde le brut si échec
      }
    }

    // Message d'état de jeu : "GAME_STATE:{json}" (cf. ServerManager.SendGameStateToClient)
    if (message.startsWith('GAME_STATE:')) {
      this._handleGameState(message.slice('GAME_STATE:'.length));
      return;
    }

    let parsed = null;
    try {
      parsed = JSON.parse(message);
    } catch {
      // pas du JSON : on relaie en texte brut
    }

    // État de jeu en JSON direct (réponse à GetGameState, sans préfixe GAME_STATE:)
    // Détecté via la présence de CurrentStateScene.CurrentScene (PascalCase).
    if (parsed && parsed.CurrentStateScene && parsed.CurrentStateScene.CurrentScene !== undefined) {
      this._storeGameState(parsed);
      return;
    }

    // Handshake : le serveur demande le type de client
    if (parsed && parsed.order === 'RequestClientType') {
      this.clientId = parsed.clientId || this.clientId;
      this._sendClientType();
    }

    // Confirmation de type
    if (parsed && parsed.order === 'ClientTypeConfirmation') {
      if (parsed.success) {
        console.log(`[SatsukiTCP] Type confirmé: ${parsed.clientType}`);
      } else {
        console.warn(`[SatsukiTCP] Type rejeté: ${parsed.reason}`);
        this._notify('satsuki-error', `ClientType rejeté: ${parsed.reason}`);
      }
    }

    // Relaie le message (parsé ou brut) au renderer
    this._notify('satsuki-message', { raw: message, data: parsed });
  }

  // Parse et stocke l'état de jeu reçu via "GAME_STATE:{json}", puis le relaie au renderer
  _handleGameState(json) {
    let state = null;
    try {
      state = JSON.parse(json);
    } catch (err) {
      console.warn('[SatsukiTCP] GAME_STATE invalide:', err.message);
      return;
    }
    this._storeGameState(state);
  }

  // Stocke un état de jeu (objet déjà parsé) et le relaie au renderer
  _storeGameState(state) {
    this.gameState = state;
    const scene = state?.CurrentStateScene?.CurrentScene ?? null;
    console.log(`[SatsukiTCP] État de jeu reçu — scène: ${scene ?? 'inconnue'}`);

    this._notify('satsuki-game-state', { scene, state });
    // Relaie aussi comme message standard avec un order exploitable par clientService.onOrder
    this._notify('satsuki-message', {
      raw: JSON.stringify(state),
      data: { order: 'GameStateUpdate', scene, state }
    });
  }

  // Demande l'état courant au serveur (ordre Scene, traité par MainGameScene)
  requestGameState() {
    return this.sendOrder({
      ClientId: this.clientId || 'ciel-client',
      Target: 'Scene',
      Order: 'GetGameState',
      JsonData: '{}'
    });
  }

  // Répond au handshake RequestClientType
  _sendClientType() {
    const payload = {
      order: 'ClientTypeResponse',
      clientId: this.clientId,
      clientType: this.clientType,
      password: this.clientType === 'BACKEND' ? this._pendingPassword : undefined,
      timestamp: new Date().toISOString()
    };
    this._sendJson(payload);
  }

  // Sérialise et envoie un objet JSON, terminé par '\n'.
  // Crypté uniquement si le serveur crypte ses propres envois (mode adaptatif) :
  // le serveur Satsuki actuel ne peut pas décrypter (clé invalide) → envoi en clair.
  _sendJson(obj) {
    if (!this.connected || !this.socket) {
      return { success: false, message: 'Non connecté au serveur Satsuki' };
    }
    try {
      const json = JSON.stringify(obj);
      const payload = (this.serverEncrypts ? encrypt(json) : json) + '\n';
      this.socket.write(payload, 'utf8');
      return { success: true, message: 'Message envoyé' };
    } catch (err) {
      console.error('[SatsukiTCP] Erreur envoi:', err.message);
      return { success: false, message: err.message };
    }
  }

  /**
   * Envoie un OrderRequest au serveur.
   * @param {object} orderRequest { ClientId?, Target, Order, JsonData }
   */
  sendOrder(orderRequest) {
    const req = {
      ClientId: orderRequest.ClientId || this.clientId || 'ciel-client',
      Target: orderRequest.Target,
      Order: orderRequest.Order,
      JsonData: typeof orderRequest.JsonData === 'string'
        ? orderRequest.JsonData
        : JSON.stringify(orderRequest.JsonData || {})
    };
    return this._sendJson(req);
  }

  // Envoie un objet JSON brut (déjà formé)
  sendRaw(obj) {
    return this._sendJson(obj);
  }

  disconnect() {
    if (this.socket) {
      try { this.socket.destroy(); } catch { /* ignore */ }
      this.socket = null;
    }
    this.connected = false;
    this.clientId = null;
    return { success: true, message: 'Déconnecté' };
  }

  getStatus() {
    return {
      connected: this.connected,
      host: this.host,
      port: this.port,
      clientId: this.clientId,
      clientType: this.clientType,
      gameState: this.gameState,
      currentScene: this.gameState?.CurrentStateScene?.CurrentScene ?? null
    };
  }
}

module.exports = new SatsukiTcpClient();
