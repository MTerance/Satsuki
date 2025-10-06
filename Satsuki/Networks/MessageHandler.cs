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
            
            // Configuration par d�faut du cryptage
            _encryptionEnabled = true; // Cryptage activ� par d�faut
            _encryptionKey = null; // Utilise la cl� par d�faut de MessageCrypto
            _encryptionIV = null;  // Utilise l'IV par d�faut de MessageCrypto
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
                
                Console.WriteLine($"Cryptage des messages: {(enabled ? "ACTIV�" : "D�SACTIV�")}" +
                    $"{(enabled && key != null ? "\nCl� de cryptage personnalis�e configur�e" : "")}");
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
                
                Console.WriteLine("Nouvelle cl� de cryptage g�n�r�e");
                Console.WriteLine($"Cl�: {MessageCrypto.BytesToBase64(_encryptionKey)}");
                Console.WriteLine($"IV: {MessageCrypto.BytesToBase64(_encryptionIV)}");
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
        /// D�marre le traitement des messages en arri�re-plan
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
        /// Arr�te le traitement des messages
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
        /// Ajoute un message re�u du r�seau � la queue (avec cryptage automatique si activ�)
        /// </summary>
        /// <param name="content">Contenu du message (suppos� en clair)</param>
        public void AddReceivedMessage(string content)
        {
            if (_disposed || string.IsNullOrEmpty(content))
                return;

            var message = new Message(content);
            
            // Crypte automatiquement si le cryptage est activ�
            if (_encryptionEnabled)
            {
                message.Encrypt(_encryptionKey, _encryptionIV);
            }

            _messageQueue.Enqueue(message);
            _messageAvailableSemaphore.Release();
        }

        /// <summary>
        /// Ajoute un message d�j� crypt� � la queue (pour messages re�us d�j� crypt�s)
        /// </summary>
        /// <param name="encryptedContent">Contenu crypt�</param>
        public void AddEncryptedMessage(string encryptedContent)
        {
            if (_disposed || string.IsNullOrEmpty(encryptedContent))
                return;

            // Cr�e le message comme �tant d�j� crypt�
            var message = new Message(encryptedContent, true);
            _messageQueue.Enqueue(message);
            _messageAvailableSemaphore.Release();
        }

        /// <summary>
        /// Ajoute un message d�j� cr�� � la queue
        /// </summary>
        /// <param name="message">Message � ajouter</param>
        public void AddReceivedMessage(Message message)
        {
            if (_disposed || message == null)
                return;

            _messageQueue.Enqueue(message);
            _messageAvailableSemaphore.Release();
        }

        /// <summary>
        /// R�cup�re tous les messages disponibles tri�s par timestamp avec d�cryptage automatique
        /// </summary>
        /// <param name="decryptMessages">Si true, d�crypte automatiquement les messages crypt�s</param>
        /// <returns>Liste des messages tri�s par timestamp</returns>
        public List<Message> GetMessagesByTimestamp(bool decryptMessages = true)
        {
            var messages = new List<Message>();
            
            // R�cup�re tous les messages de la queue
            while (_messageQueue.TryDequeue(out Message message))
            {
                // D�crypte automatiquement si demand� et si le message est crypt�
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
        /// R�cup�re un nombre limit� de messages tri�s par timestamp avec d�cryptage automatique
        /// </summary>
        /// <param name="maxCount">Nombre maximum de messages � r�cup�rer</param>
        /// <param name="decryptMessages">Si true, d�crypte automatiquement les messages crypt�s</param>
        /// <returns>Liste des messages tri�s par timestamp</returns>
        public List<Message> GetMessagesByTimestamp(int maxCount, bool decryptMessages = true)
        {
            var messages = new List<Message>();
            int count = 0;
            
            // R�cup�re les messages jusqu'� la limite
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

            // Trie par timestamp (plus ancien en premier)
            return messages.OrderBy(m => m.Timestamp).ToList();
        }

        /// <summary>
        /// R�cup�re les messages sans les d�crypter (utile pour debug ou transfert)
        /// </summary>
        /// <returns>Liste des messages tri�s par timestamp (possiblement crypt�s)</returns>
        public List<Message> GetEncryptedMessagesByTimestamp()
        {
            return GetMessagesByTimestamp(decryptMessages: false);
        }

        /// <summary>
        /// V�rifie s'il y a des messages en attente
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
                    // Attend qu'un message soit disponible ou que l'annulation soit demand�e
                    await _messageAvailableSemaphore.WaitAsync(_cancellationTokenSource.Token);

                    if (_cancellationTokenSource.Token.IsCancellationRequested)
                        break;

                    // Logging avec information de cryptage
                    if (HasPendingMessages())
                    {
                        string encStatus = _encryptionEnabled ? "CRYPT�" : "CLAIR";
                        Console.WriteLine($"Messages en attente: {GetPendingMessageCount()} [{encStatus}]");
                    }
                }
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("MessageHandler: Arr�t du traitement des messages.");
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
                // Arr�te le traitement en cours
                StopMessageProcessing().Wait(TimeSpan.FromSeconds(5));
                
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

        ~MessageHandler()
        {
            Dispose(false);
        }
    }
}