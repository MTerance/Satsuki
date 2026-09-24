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
// On normalise à 32 bytes (troncature) pour rester compatible si .NET tronque,
// et le client reste tolérant aux messages en clair.
function normalizeKey(input, length) {
  const buf = Buffer.from(input, 'utf8');
  if (buf.length === length) return buf;
  if (buf.length > length) return buf.subarray(0, length);
  return Buffer.concat([buf, Buffer.alloc(length - buf.length, 0)]);
}

const DEFAULT_KEY = normalizeKey('SatsukiGameServer2024Key1234567890', 32); // AES-256
const DEFAULT_IV = normalizeKey('SatsukiInitVect1', 16); // 16 bytes

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

  // Réception : accumulation + split par ligne, décryptage si nécessaire
  _onData(data) {
    this.buffer += data.toString('utf8');

    let idx;
    while ((idx = this.buffer.indexOf('\n')) !== -1) {
      const rawLine = this.buffer.slice(0, idx).replace(/\r$/, '');
      this.buffer = this.buffer.slice(idx + 1);
      if (rawLine.trim().length > 0) {
        this._handleLine(rawLine.trim());
      }
    }
  }

  _handleLine(line) {
    let message = line;

    // Le serveur préfixe parfois par "[clientId] " dans ses logs, mais envoie le JSON pur.
    // Tente un décryptage si la ligne ressemble à du Base64 AES.
    if (looksEncrypted(line)) {
      try {
        message = decrypt(line);
      } catch {
        message = line; // garde le brut si échec
      }
    }

    let parsed = null;
    try {
      parsed = JSON.parse(message);
    } catch {
      // pas du JSON : on relaie en texte brut
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

  // Sérialise et envoie un objet JSON (crypté), terminé par '\n'
  _sendJson(obj) {
    if (!this.connected || !this.socket) {
      return { success: false, message: 'Non connecté au serveur Satsuki' };
    }
    try {
      const json = JSON.stringify(obj);
      const payload = encrypt(json) + '\n';
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
      clientType: this.clientType
    };
  }
}

module.exports = new SatsukiTcpClient();
