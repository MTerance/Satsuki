using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Satsuki.Utils;
using Satsuki;

namespace Satsuki.Networks
{
    /// <summary>
    /// Classe multithread qui re�oit les messages des diff�rents clients
    /// et les stocke dans une queue par ordre d'arriv�e avec support du cryptage
    /// </summary>
    public class MessageReceiver : SingletonBase<MessageReceiver>, IDisposable
    {
        private readonly ConcurrentQueue<Message> _messageQueue;
        private readonly ConcurrentDictionary<string, ClientConnection> _clients;
        private readonly SemaphoreSlim _messageAvailableSemaphore;
        private readonly CancellationTokenSource _cancellationTokenSource;
        private readonly object _lockObject = new object();
        private bool _isRunning;
        private bool _disposed;
        private int _clientIdCounter;

        // Configuration du cryptage
        private bool _encryptionEnabled;
        private byte[] _encryptionKey;
        private byte[] _encryptionIV;

        public MessageReceiver()
        {
            _messageQueue = new ConcurrentQueue<Message>();
            _clients = new ConcurrentDictionary<string, ClientConnection>();
            _messageAvailableSemaphore = new SemaphoreSlim(0);
            _cancellationTokenSource = new CancellationTokenSource();
            _isRunning = false;
            _disposed = false;
            _clientIdCounter = 0;

            // Configuration par d�faut du cryptage
            _encryptionEnabled = true; // Cryptage activ� par d�faut
            _encryptionKey = null; // Utilise la cl� par d�faut
            _encryptionIV = null;  // Utilise l'IV par d�faut
        }

        /// <summary>
        /// Configure le syst�me de cryptage
        /// </summary>
        /// <param name="enabled">Active ou d�sactive le cryptage</param>
        /// <param name="key">Cl� de cryptage personnalis�e (null pour utiliser la cl� par d�faut)</param>
        /// <param name="iv">IV personnalis� (null pour utiliser l'IV par d�faut)</param>
        public void ConfigureEncryption(bool enabled, byte[] key = null, byte[] iv = null)
        {
            lock (_lockObject)
            {
                _encryptionEnabled = enabled;
                _encryptionKey = key;
                _encryptionIV = iv;
                
                Console.WriteLine($"?? Cryptage des messages: {(enabled ? "ACTIV�" : "D�SACTIV�")}");
                if (enabled && key != null)
                {
                    Console.WriteLine("?? Cl� de cryptage personnalis�e configur�e");
                }
            }
        }

        /// <summary>
        /// G�n�re et configure une nouvelle cl� de cryptage al�atoire
        /// </summary>
        public void GenerateNewEncryptionKey()
        {
            lock (_lockObject)
            {
                _encryptionKey = MessageCrypto.GenerateRandomKey();
                _encryptionIV = MessageCrypto.GenerateRandomIV();
                
                Console.WriteLine("?? Nouvelle cl� de cryptage g�n�r�e");
                Console.WriteLine($"?? Cl�: {MessageCrypto.BytesToBase64(_encryptionKey)}");
                Console.WriteLine($"?? IV: {MessageCrypto.BytesToBase64(_encryptionIV)}");
            }
        }

        /// <summary>
        /// Obtient les informations de cryptage actuelles
        /// </summary>
        /// <returns>Tuple contenant l'�tat, la cl� et l'IV en Base64</returns>
        public (bool enabled, string keyBase64, string ivBase64) GetEncryptionInfo()
        {
            lock (_lockObject)
            {
                string keyB64 = _encryptionKey != null ? MessageCrypto.BytesToBase64(_encryptionKey) : "DEFAULT";
                string ivB64 = _encryptionIV != null ? MessageCrypto.BytesToBase64(_encryptionIV) : "DEFAULT";
                return (_encryptionEnabled, keyB64, ivB64);
            }
        }

        /// <summary>
        /// D�marre le syst�me de r�ception des messages
        /// </summary>
        public void Start()
        {
            lock (_lockObject)
            {
                if (_isRunning || _disposed)
                    return;

                _isRunning = true;
                Console.WriteLine("?? MessageReceiver: D�marr� - R�ception des messages par ordre d'arriv�e");
                
                var encInfo = GetEncryptionInfo();
                Console.WriteLine($"?? Cryptage: {(encInfo.enabled ? "ACTIV�" : "D�SACTIV�")}");
            }
        }

        /// <summary>
        /// Arr�te le syst�me de r�ception
        /// </summary>
        public async Task Stop()
        {
            lock (_lockObject)
            {
                if (!_isRunning)
                    return;

                _isRunning = false;
                _cancellationTokenSource.Cancel();
            }

            // Arr�te tous les clients
            var stopTasks = _clients.Values.Select(client => client.StopAsync()).ToArray();
            await Task.WhenAll(stopTasks);

            _clients.Clear();
            Console.WriteLine("?? MessageReceiver: Arr�t�");
        }

        /// <summary>
        /// Ajoute un nouveau client TCP � surveiller
        /// </summary>
        /// <param name="tcpClient">Client TCP connect�</param>
        /// <returns>ID unique attribu� au client</returns>
        public string AddClient(TcpClient tcpClient)
        {
            if (!_isRunning || _disposed || tcpClient == null)
                return null;

            string clientId = $"Client_{Interlocked.Increment(ref _clientIdCounter)}";
            var clientConnection = new ClientConnection(clientId, tcpClient, OnMessageReceived, OnClientDisconnected);
            
            if (_clients.TryAdd(clientId, clientConnection))
            {
                clientConnection.StartListening(_cancellationTokenSource.Token);
                Console.WriteLine($"?? MessageReceiver: Client {clientId} ajout� ({tcpClient.Client.RemoteEndPoint})");
                LogConnectionStats();
                return clientId;
            }

            return null;
        }

        /// <summary>
        /// Supprime un client de la surveillance
        /// </summary>
        /// <param name="clientId">ID du client � supprimer</param>
        public async Task RemoveClient(string clientId)
        {
            if (_clients.TryRemove(clientId, out ClientConnection clientConnection))
            {
                await clientConnection.StopAsync();
                Console.WriteLine($"? MessageReceiver: Client {clientId} supprim�");
                LogConnectionStats();
            }
        }

        /// <summary>
        /// R�cup�re tous les messages dans l'ordre d'arriv�e avec d�cryptage automatique
        /// </summary>
        /// <param name="decryptMessages">Si true, d�crypte automatiquement les messages crypt�s</param>
        /// <returns>Liste des messages dans l'ordre d'arriv�e</returns>
        public List<Message> GetMessagesByArrivalOrder(bool decryptMessages = true)
        {
            var messages = new List<Message>();
            
            // R�cup�re tous les messages de la queue dans l'ordre FIFO
            while (_messageQueue.TryDequeue(out Message message))
            {
                // D�crypte automatiquement si demand� et si le message est crypt�
                if (decryptMessages && message.IsEncrypted)
                {
                    message.Decrypt(_encryptionKey, _encryptionIV);
                }
                
                messages.Add(message);
            }

            return messages; // D�j� dans l'ordre d'arriv�e gr�ce � ConcurrentQueue
        }

        /// <summary>
        /// R�cup�re un nombre limit� de messages dans l'ordre d'arriv�e avec d�cryptage automatique
        /// </summary>
        /// <param name="maxCount">Nombre maximum de messages � r�cup�rer</param>
        /// <param name="decryptMessages">Si true, d�crypte automatiquement les messages crypt�s</param>
        /// <returns>Liste des messages dans l'ordre d'arriv�e</returns>
        public List<Message> GetMessagesByArrivalOrder(int maxCount, bool decryptMessages = true)
        {
            var messages = new List<Message>();
            int count = 0;
            
            // R�cup�re les messages jusqu'� la limite dans l'ordre FIFO
            while (_messageQueue.TryDequeue(out Message message) && count < maxCount)
            {
                // D�crypte automatiquement si demand� et si le message est crypt�
                if (decryptMessages && message.IsEncrypted)
                {
                    message.Decrypt(_encryptionKey, _encryptionIV);
                }
                
                messages.Add(message);
                count++;
            }

            return messages;
        }

        /// <summary>
        /// R�cup�re le prochain message disponible avec d�cryptage optionnel
        /// </summary>
        /// <param name="decryptMessage">Si true, d�crypte automatiquement si le message est crypt�</param>
        /// <returns>Le prochain message ou null si aucun disponible</returns>
        public Message GetNextMessage(bool decryptMessage = true)
        {
            if (_messageQueue.TryDequeue(out Message message))
            {
                // D�crypte automatiquement si demand� et si le message est crypt�
                if (decryptMessage && message.IsEncrypted)
                {
                    message.Decrypt(_encryptionKey, _encryptionIV);
                }
                return message;
            }
            return null;
        }

        /// <summary>
        /// R�cup�re les messages sans les d�crypter (utile pour debug ou transfert)
        /// </summary>
        /// <returns>Liste des messages dans l'ordre d'arriv�e (possiblement crypt�s)</returns>
        public List<Message> GetEncryptedMessagesByArrivalOrder()
        {
            return GetMessagesByArrivalOrder(decryptMessages: false);
        }

        /// <summary>
        /// V�rifie s'il y a des messages en attente
        /// </summary>
        public bool HasPendingMessages()
        {
            return !_messageQueue.IsEmpty;
        }

        /// <summary>
        /// Obtient le nombre de messages en attente
        /// </summary>
        public int GetPendingMessageCount()
        {
            return _messageQueue.Count;
        }

        /// <summary>
        /// Obtient le nombre de clients connect�s
        /// </summary>
        public int GetConnectedClientCount()
        {
            return _clients.Count;
        }

        /// <summary>
        /// Obtient la liste des IDs des clients connect�s
        /// </summary>
        public List<string> GetConnectedClientIds()
        {
            return _clients.Keys.ToList();
        }

        /// <summary>
        /// Envoie un message � un client sp�cifique (avec cryptage optionnel)
        /// </summary>
        /// <param name="clientId">ID du client</param>
        /// <param name="message">Message � envoyer</param>
        /// <param name="encrypt">Si true, crypte le message avant envoi</param>
        public async Task<bool> SendMessageToClient(string clientId, string message, bool encrypt = true)
        {
            if (_clients.TryGetValue(clientId, out ClientConnection clientConnection))
            {
                string messageToSend = message;
                
                // Crypte le message si demand� et si le cryptage est activ�
                if (encrypt && _encryptionEnabled)
                {
                    messageToSend = MessageCrypto.Encrypt(message, _encryptionKey, _encryptionIV);
                    Console.WriteLine($"?? Message crypt� envoy� � {clientId}");
                }
                
                return await clientConnection.SendMessageAsync(messageToSend);
            }
            return false;
        }

        /// <summary>
        /// Diffuse un message � tous les clients connect�s (avec cryptage optionnel)
        /// </summary>
        /// <param name="message">Message � diffuser</param>
        /// <param name="encrypt">Si true, crypte le message avant envoi</param>
        public async Task BroadcastMessage(string message, bool encrypt = true)
        {
            string messageToSend = message;
            
            // Crypte le message si demand� et si le cryptage est activ�
            if (encrypt && _encryptionEnabled)
            {
                messageToSend = MessageCrypto.Encrypt(message, _encryptionKey, _encryptionIV);
                Console.WriteLine($"?? Message de broadcast crypt�");
            }
            
            var sendTasks = _clients.Values.Select(client => client.SendMessageAsync(messageToSend)).ToArray();
            await Task.WhenAll(sendTasks);
            Console.WriteLine($"?? Message diffus� � {sendTasks.Length} clients");
        }

        /// <summary>
        /// Callback appel� quand un message est re�u d'un client
        /// </summary>
        private void OnMessageReceived(string clientId, string messageContent)
        {
            // Cr�e le message avec pr�fixe client
            var message = new Message($"[{clientId}] {messageContent}");
            
            // D�tecte automatiquement si le message est crypt� et le marque comme tel
            if (MessageCrypto.IsEncrypted(messageContent))
            {
                // Remplace le contenu par le message crypt� original (sans pr�fixe client)
                message = new Message(messageContent, true);
                // Puis ajoute le pr�fixe client apr�s d�cryptage
                string decryptedContent = MessageCrypto.Decrypt(messageContent, _encryptionKey, _encryptionIV);
                message = new Message($"[{clientId}] {decryptedContent}");
                Console.WriteLine($"?? Message crypt� re�u de {clientId}");
            }
            
            _messageQueue.Enqueue(message);
            _messageAvailableSemaphore.Release();
            
            Console.WriteLine($"?? Message #{message.SequenceNumber} re�u de {clientId}");
        }

        /// <summary>
        /// Callback appel� quand un client se d�connecte
        /// </summary>
        private async void OnClientDisconnected(string clientId)
        {
            await RemoveClient(clientId);
        }

        /// <summary>
        /// Affiche les statistiques de connexion
        /// </summary>
        private void LogConnectionStats()
        {
            var clientCount = _clients.Count;
            var messageCount = _messageQueue.Count;
            var encStatus = _encryptionEnabled ? "CRYPT�" : "CLAIR";
            Console.WriteLine($"?? Stats: {clientCount} clients, {messageCount} messages en attente [{encStatus}]");
        }

        /// <summary>
        /// Obtient les statistiques compl�tes du syst�me
        /// </summary>
        public (int connectedClients, int pendingMessages, bool isRunning, bool encryptionEnabled) GetStatistics()
        {
            return (_clients.Count, _messageQueue.Count, _isRunning, _encryptionEnabled);
        }

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        protected virtual void Dispose(bool disposing)
        {
            if (!_disposed && disposing)
            {
                Stop().Wait(TimeSpan.FromSeconds(5));
                
                _cancellationTokenSource?.Dispose();
                _messageAvailableSemaphore?.Dispose();
                
                // Vide la queue
                while (_messageQueue.TryDequeue(out _)) { }
                
                // Efface les cl�s de m�moire pour s�curit�
                if (_encryptionKey != null)
                {
                    Array.Clear(_encryptionKey, 0, _encryptionKey.Length);
                }
                if (_encryptionIV != null)
                {
                    Array.Clear(_encryptionIV, 0, _encryptionIV.Length);
                }
                
                _disposed = true;
            }
        }

        ~MessageReceiver()
        {
            Dispose(false);
        }
    }

    // La classe ClientConnection reste inchang�e
    /// <summary>
    /// Gestionnaire pour une connexion client individuelle
    /// </summary>
    internal class ClientConnection
    {
        private readonly string _clientId;
        private readonly TcpClient _tcpClient;
        private readonly NetworkStream _stream;
        private readonly Action<string, string> _onMessageReceived;
        private readonly Action<string> _onDisconnected;
        private Task _listeningTask;
        private bool _isListening;

        public ClientConnection(string clientId, TcpClient tcpClient, Action<string, string> onMessageReceived, Action<string> onDisconnected)
        {
            _clientId = clientId;
            _tcpClient = tcpClient;
            _stream = tcpClient.GetStream();
            _onMessageReceived = onMessageReceived;
            _onDisconnected = onDisconnected;
            _isListening = false;
        }

        /// <summary>
        /// D�marre l'�coute des messages pour ce client
        /// </summary>
        public void StartListening(CancellationToken cancellationToken)
        {
            if (_isListening)
                return;

            _isListening = true;
            _listeningTask = Task.Run(() => ListenForMessages(cancellationToken), cancellationToken);
        }

        /// <summary>
        /// Arr�te l'�coute pour ce client
        /// </summary>
        public async Task StopAsync()
        {
            _isListening = false;

            if (_listeningTask != null)
            {
                await _listeningTask;
                _listeningTask = null;
            }

            _stream?.Close();
            _tcpClient?.Close();
        }

        /// <summary>
        /// Envoie un message � ce client
        /// </summary>
        public async Task<bool> SendMessageAsync(string message)
        {
            if (!_isListening || _stream == null || !_stream.CanWrite)
                return false;

            try
            {
                byte[] data = Encoding.UTF8.GetBytes(message);
                await _stream.WriteAsync(data, 0, data.Length);
                await _stream.FlushAsync();
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"? Erreur envoi message � {_clientId}: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Boucle d'�coute des messages pour ce client
        /// </summary>
        private async Task ListenForMessages(CancellationToken cancellationToken)
        {
            byte[] buffer = new byte[4096];
            
            try
            {
                while (_isListening && !cancellationToken.IsCancellationRequested && _tcpClient.Connected)
                {
                    if (_stream.CanRead)
                    {
                        int bytesRead = await _stream.ReadAsync(buffer, 0, buffer.Length, cancellationToken);
                        
                        if (bytesRead > 0)
                        {
                            string message = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                            
                            // Traite les messages multiples s�par�s par des retours � la ligne
                            string[] messages = message.Split(new[] { '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
                            foreach (string msg in messages)
                            {
                                if (!string.IsNullOrWhiteSpace(msg))
                                {
                                    _onMessageReceived?.Invoke(_clientId, msg.Trim());
                                }
                            }
                        }
                        else
                        {
                            // Client d�connect�
                            Console.WriteLine($"?? Client {_clientId} d�connect� (0 bytes)");
                            break;
                        }
                    }
                    else
                    {
                        await Task.Delay(10, cancellationToken);
                    }
                }
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine($"?? �coute {_clientId} annul�e");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"? Erreur �coute {_clientId}: {ex.Message}");
            }
            finally
            {
                Console.WriteLine($"?? Fin �coute pour {_clientId}");
                _onDisconnected?.Invoke(_clientId);
            }
        }
    }
}