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
    /// Classe multithread qui gère la réception de messages de multiples clients
    /// et les stocke dans une queue triée par timestamp
    /// </summary>
    public class MultiThreadMessageReceiver : SingletonBase<MultiThreadMessageReceiver>, IDisposable
    {
        private readonly ConcurrentQueue<Message> _messageQueue;
        private readonly ConcurrentDictionary<string, ClientHandler> _clients;
        private readonly SemaphoreSlim _messageAvailableSemaphore;
        private readonly CancellationTokenSource _cancellationTokenSource;
        private readonly object _lockObject = new object();
        private bool _isRunning;
        private bool _disposed;
        private int _clientIdCounter;

        public MultiThreadMessageReceiver()
        {
            _messageQueue = new ConcurrentQueue<Message>();
            _clients = new ConcurrentDictionary<string, ClientHandler>();
            _messageAvailableSemaphore = new SemaphoreSlim(0);
            _cancellationTokenSource = new CancellationTokenSource();
            _isRunning = false;
            _disposed = false;
            _clientIdCounter = 0;
        }

        /// <summary>
        /// Démarre le système de réception multithread
        /// </summary>
        public void Start()
        {
            lock (_lockObject)
            {
                if (_isRunning || _disposed)
                    return;

                _isRunning = true;
                Console.WriteLine("MultiThreadMessageReceiver: Démarré");
            }
        }

        /// <summary>
        /// Arrête le système de réception
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

            // Arrête tous les clients
            var stopTasks = _clients.Values.Select(client => client.StopAsync()).ToArray();
            await Task.WhenAll(stopTasks);

            _clients.Clear();
            Console.WriteLine("MultiThreadMessageReceiver: Arrêté");
        }

        /// <summary>
        /// Ajoute un nouveau client à gérer
        /// </summary>
        /// <param name="tcpClient">Client TCP connecté</param>
        /// <returns>ID unique du client</returns>
        public string AddClient(TcpClient tcpClient)
        {
            if (!_isRunning || _disposed || tcpClient == null)
                return null;

            string clientId = $"Client_{Interlocked.Increment(ref _clientIdCounter)}";
            var clientHandler = new ClientHandler(clientId, tcpClient, OnMessageReceived, OnClientDisconnected);
            
            if (_clients.TryAdd(clientId, clientHandler))
            {
                clientHandler.StartListening(_cancellationTokenSource.Token);
                Console.WriteLine($"MultiThreadMessageReceiver: Client {clientId} ajouté");
                return clientId;
            }

            return null;
        }

        /// <summary>
        /// Supprime un client
        /// </summary>
        /// <param name="clientId">ID du client à supprimer</param>
        public async Task RemoveClient(string clientId)
        {
            if (_clients.TryRemove(clientId, out ClientHandler clientHandler))
            {
                await clientHandler.StopAsync();
                Console.WriteLine($"MultiThreadMessageReceiver: Client {clientId} supprimé");
            }
        }

        /// <summary>
        /// Obtient le nombre de clients connectés
        /// </summary>
        public int GetConnectedClientCount()
        {
            return _clients.Count;
        }

        /// <summary>
        /// Obtient la liste des IDs des clients connectés
        /// </summary>
        public List<string> GetConnectedClientIds()
        {
            return _clients.Keys.ToList();
        }

        /// <summary>
        /// Récupère tous les messages triés par timestamp
        /// </summary>
        /// <returns>Liste des messages triés</returns>
        public List<Message> GetMessagesByTimestamp()
        {
            var messages = new List<Message>();
            
            while (_messageQueue.TryDequeue(out Message message))
            {
                messages.Add(message);
            }

            return messages.OrderBy(m => m.Timestamp).ToList();
        }

        /// <summary>
        /// Récupère un nombre limité de messages triés par timestamp
        /// </summary>
        /// <param name="maxCount">Nombre maximum de messages</param>
        /// <returns>Liste des messages triés</returns>
        public List<Message> GetMessagesByTimestamp(int maxCount)
        {
            var messages = new List<Message>();
            int count = 0;
            
            while (_messageQueue.TryDequeue(out Message message) && count < maxCount)
            {
                messages.Add(message);
                count++;
            }

            return messages.OrderBy(m => m.Timestamp).ToList();
        }

        /// <summary>
        /// Vérifie s'il y a des messages en attente
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
        /// Envoie un message à un client spécifique
        /// </summary>
        /// <param name="clientId">ID du client</param>
        /// <param name="message">Message à envoyer</param>
        public async Task<bool> SendMessageToClient(string clientId, string message)
        {
            if (_clients.TryGetValue(clientId, out ClientHandler clientHandler))
            {
                return await clientHandler.SendMessageAsync(message);
            }
            return false;
        }

        /// <summary>
        /// Envoie un message à tous les clients connectés
        /// </summary>
        /// <param name="message">Message à envoyer</param>
        public async Task BroadcastMessage(string message)
        {
            var sendTasks = _clients.Values.Select(client => client.SendMessageAsync(message)).ToArray();
            await Task.WhenAll(sendTasks);
            Console.WriteLine($"Message diffusé à {sendTasks.Length} clients");
        }

        /// <summary>
        /// Callback appelé quand un message est reçu d'un client
        /// </summary>
        private void OnMessageReceived(string clientId, string messageContent)
        {
            var message = new Message($"[{clientId}] {messageContent}");
            _messageQueue.Enqueue(message);
            _messageAvailableSemaphore.Release();
            
            Console.WriteLine($"Message reçu de {clientId}: {messageContent}");
        }

        /// <summary>
        /// Callback appelé quand un client se déconnecte
        /// </summary>
        private async void OnClientDisconnected(string clientId)
        {
            await RemoveClient(clientId);
        }

        /// <summary>
        /// Obtient les statistiques du système
        /// </summary>
        public (int clients, int pendingMessages, bool running) GetStatistics()
        {
            return (_clients.Count, _messageQueue.Count, _isRunning);
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
                
                _disposed = true;
            }
        }

        ~MultiThreadMessageReceiver()
        {
            Dispose(false);
        }
    }

    /// <summary>
    /// Gestionnaire pour un client TCP individuel
    /// </summary>
    internal class ClientHandler
    {
        private readonly string _clientId;
        private readonly TcpClient _tcpClient;
        private readonly NetworkStream _stream;
        private readonly Action<string, string> _onMessageReceived;
        private readonly Action<string> _onDisconnected;
        private Task _listeningTask;
        private bool _isListening;

        public ClientHandler(string clientId, TcpClient tcpClient, Action<string, string> onMessageReceived, Action<string> onDisconnected)
        {
            _clientId = clientId;
            _tcpClient = tcpClient;
            _stream = tcpClient.GetStream();
            _onMessageReceived = onMessageReceived;
            _onDisconnected = onDisconnected;
            _isListening = false;
        }

        /// <summary>
        /// Démarre l'écoute des messages pour ce client
        /// </summary>
        public void StartListening(CancellationToken cancellationToken)
        {
            if (_isListening)
                return;

            _isListening = true;
            _listeningTask = Task.Run(() => ListenForMessages(cancellationToken), cancellationToken);
        }

        /// <summary>
        /// Arrête l'écoute pour ce client
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
        /// Envoie un message à ce client
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
                Console.WriteLine($"Erreur envoi message à {_clientId}: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Boucle d'écoute des messages
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
                            _onMessageReceived?.Invoke(_clientId, message);
                        }
                        else
                        {
                            // Client déconnecté
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
                // Arrêt normal
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur écoute {_clientId}: {ex.Message}");
            }
            finally
            {
                _onDisconnected?.Invoke(_clientId);
            }
        }
    }
}