using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Satsuki.Utils;

namespace Satsuki.Networks
{
    public class MessageHandler : SingletonBase<MessageHandler>, IDisposable
    {
        private readonly ConcurrentQueue<Message> _messageQueue;
        private readonly SemaphoreSlim _messageAvailableSemaphore;
        private readonly CancellationTokenSource _cancellationTokenSource;
        private Task _messageProcessingTask;
        private readonly object _lockObject = new object();
        private bool _isRunning;
        private bool _disposed;

        // Configuration du cryptage
        private bool _encryptionEnabled;
        private byte[] _encryptionKey;
        private byte[] _encryptionIV;

        public MessageHandler()
        {
            _messageQueue = new ConcurrentQueue<Message>();
            _messageAvailableSemaphore = new SemaphoreSlim(0);
            _cancellationTokenSource = new CancellationTokenSource();
            _isRunning = false;
            _disposed = false;
            
            // Configuration par défaut du cryptage
            _encryptionEnabled = true; // Cryptage activé par défaut
            _encryptionKey = null; // Utilise la clé par défaut de MessageCrypto
            _encryptionIV = null;  // Utilise l'IV par défaut de MessageCrypto
        }

        /// <summary>
        /// Configure le système de cryptage
        /// </summary>
        /// <param name="enabled">Active ou désactive le cryptage</param>
        /// <param name="key">Clé de cryptage personnalisée (null pour utiliser la clé par défaut)</param>
        /// <param name="iv">IV personnalisé (null pour utiliser l'IV par défaut)</param>
        public void ConfigureEncryption(bool enabled, byte[] key = null, byte[] iv = null)
        {
            lock (_lockObject)
            {
                _encryptionEnabled = enabled;
                _encryptionKey = key;
                _encryptionIV = iv;
                
                Console.WriteLine($"Cryptage des messages: {(enabled ? "ACTIVÉ" : "DÉSACTIVÉ")}" +
                    $"{(enabled && key != null ? "\nClé de cryptage personnalisée configurée" : "")}");
            }
        }

        /// <summary>
        /// Génère et configure une nouvelle clé de cryptage aléatoire
        /// </summary>
        public void GenerateNewEncryptionKey()
        {
            lock (_lockObject)
            {
                _encryptionKey = MessageCrypto.GenerateRandomKey();
                _encryptionIV = MessageCrypto.GenerateRandomIV();
                
                Console.WriteLine("Nouvelle clé de cryptage générée");
                Console.WriteLine($"Clé: {MessageCrypto.BytesToBase64(_encryptionKey)}");
                Console.WriteLine($"IV: {MessageCrypto.BytesToBase64(_encryptionIV)}");
            }
        }

        /// <summary>
        /// Obtient les informations de cryptage actuelles
        /// </summary>
        /// <returns>Tuple contenant l'état, la clé et l'IV en Base64</returns>
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
        /// Démarre le traitement des messages en arrière-plan
        /// </summary>
        public void StartMessageProcessing()
        {
            lock (_lockObject)
            {
                if (_isRunning || _disposed)
                    return;

                _isRunning = true;
                _messageProcessingTask = Task.Run(MessageProcessingLoop, _cancellationTokenSource.Token);
            }
        }

        /// <summary>
        /// Arrête le traitement des messages
        /// </summary>
        public async Task StopMessageProcessing()
        {
            lock (_lockObject)
            {
                if (!_isRunning)
                    return;

                _isRunning = false;
                _cancellationTokenSource.Cancel();
            }

            if (_messageProcessingTask != null)
            {
                await _messageProcessingTask;
                _messageProcessingTask = null;
            }
        }

        /// <summary>
        /// Ajoute un message reçu du réseau à la queue (avec cryptage automatique si activé)
        /// </summary>
        /// <param name="content">Contenu du message (supposé en clair)</param>
        public void AddReceivedMessage(string content)
        {
            if (_disposed || string.IsNullOrEmpty(content))
                return;

            var message = new Message(content);
            
            // Crypte automatiquement si le cryptage est activé
            if (_encryptionEnabled)
            {
                message.Encrypt(_encryptionKey, _encryptionIV);
            }

            _messageQueue.Enqueue(message);
            _messageAvailableSemaphore.Release();
        }

        /// <summary>
        /// Ajoute un message déjà crypté à la queue (pour messages reçus déjà cryptés)
        /// </summary>
        /// <param name="encryptedContent">Contenu crypté</param>
        public void AddEncryptedMessage(string encryptedContent)
        {
            if (_disposed || string.IsNullOrEmpty(encryptedContent))
                return;

            // Crée le message comme étant déjà crypté
            var message = new Message(encryptedContent, true);
            _messageQueue.Enqueue(message);
            _messageAvailableSemaphore.Release();
        }

        /// <summary>
        /// Ajoute un message déjà créé à la queue
        /// </summary>
        /// <param name="message">Message à ajouter</param>
        public void AddReceivedMessage(Message message)
        {
            if (_disposed || message == null)
                return;

            _messageQueue.Enqueue(message);
            _messageAvailableSemaphore.Release();
        }

        /// <summary>
        /// Récupère tous les messages disponibles triés par timestamp avec décryptage automatique
        /// </summary>
        /// <param name="decryptMessages">Si true, décrypte automatiquement les messages cryptés</param>
        /// <returns>Liste des messages triés par timestamp</returns>
        public List<Message> GetMessagesByTimestamp(bool decryptMessages = true)
        {
            var messages = new List<Message>();
            
            // Récupère tous les messages de la queue
            while (_messageQueue.TryDequeue(out Message message))
            {
                // Décrypte automatiquement si demandé et si le message est crypté
                if (decryptMessages && message.IsEncrypted)
                {
                    message.Decrypt(_encryptionKey, _encryptionIV);
                }
                
                messages.Add(message);
            }

            // Trie par timestamp (plus ancien en premier)
            return messages.OrderBy(m => m.Timestamp).ToList();
        }

        /// <summary>
        /// Récupère un nombre limité de messages triés par timestamp avec décryptage automatique
        /// </summary>
        /// <param name="maxCount">Nombre maximum de messages à récupérer</param>
        /// <param name="decryptMessages">Si true, décrypte automatiquement les messages cryptés</param>
        /// <returns>Liste des messages triés par timestamp</returns>
        public List<Message> GetMessagesByTimestamp(int maxCount, bool decryptMessages = true)
        {
            var messages = new List<Message>();
            int count = 0;
            
            // Récupère les messages jusqu'à la limite
            while (_messageQueue.TryDequeue(out Message message) && count < maxCount)
            {
                // Décrypte automatiquement si demandé et si le message est crypté
                if (decryptMessages && message.IsEncrypted)
                {
                    message.Decrypt(_encryptionKey, _encryptionIV);
                }
                
                messages.Add(message);
                count++;
            }

            // Trie par timestamp (plus ancien en premier)
            return messages.OrderBy(m => m.Timestamp).ToList();
        }

        /// <summary>
        /// Récupère les messages sans les décrypter (utile pour debug ou transfert)
        /// </summary>
        /// <returns>Liste des messages triés par timestamp (possiblement cryptés)</returns>
        public List<Message> GetEncryptedMessagesByTimestamp()
        {
            return GetMessagesByTimestamp(decryptMessages: false);
        }

        /// <summary>
        /// Vérifie s'il y a des messages en attente
        /// </summary>
        /// <returns>True s'il y a des messages disponibles</returns>
        public bool HasPendingMessages()
        {
            return !_messageQueue.IsEmpty;
        }

        /// <summary>
        /// Obtient le nombre de messages en attente
        /// </summary>
        /// <returns>Nombre de messages dans la queue</returns>
        public int GetPendingMessageCount()
        {
            return _messageQueue.Count;
        }

        /// <summary>
        /// Boucle principale de traitement des messages
        /// </summary>
        private async Task MessageProcessingLoop()
        {
            try
            {
                while (!_cancellationTokenSource.Token.IsCancellationRequested)
                {
                    // Attend qu'un message soit disponible ou que l'annulation soit demandée
                    await _messageAvailableSemaphore.WaitAsync(_cancellationTokenSource.Token);

                    if (_cancellationTokenSource.Token.IsCancellationRequested)
                        break;

                    // Logging avec information de cryptage
                    if (HasPendingMessages())
                    {
                        string encStatus = _encryptionEnabled ? "CRYPTÉ" : "CLAIR";
                        Console.WriteLine($"Messages en attente: {GetPendingMessageCount()} [{encStatus}]");
                    }
                }
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("MessageHandler: Arrêt du traitement des messages.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"MessageHandler: Erreur dans la boucle de traitement: {ex.Message}");
            }
        }

        /// <summary>
        /// Nettoie les ressources
        /// </summary>
        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        protected virtual void Dispose(bool disposing)
        {
            if (!_disposed && disposing)
            {
                // Arrête le traitement en cours
                StopMessageProcessing().Wait(TimeSpan.FromSeconds(5));
                
                _cancellationTokenSource?.Dispose();
                _messageAvailableSemaphore?.Dispose();
                
                // Vide la queue
                while (_messageQueue.TryDequeue(out _)) { }
                
                // Efface les clés de mémoire pour sécurité
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

        ~MessageHandler()
        {
            Dispose(false);
        }
    }
}