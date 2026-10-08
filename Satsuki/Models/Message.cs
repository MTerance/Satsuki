using System;
using Satsuki.Utils;

namespace Satsuki
{
    public class Message
    {
        private string _content;
        private bool _isEncrypted;

        public string Content 
        { 
            get => _content;
            set 
            {
                _content = value;
                _isEncrypted = false; // Reset encryption status when content changes
            }
        }

        public DateTime Timestamp { get; set; }
        public int SequenceNumber { get; private set; }

        /// <summary>
        /// ID du client qui a envoyé le message
        /// </summary>
        public string ClientId { get; set; }

        /// <summary>
        /// Indique si le message est actuellement crypté
        /// </summary>
        public bool IsEncrypted => _isEncrypted;

        private static int _sequenceCounter = 0;

        public Message(string content, string clientId = null)
        {
            _content = content;
            _isEncrypted = false;
            ClientId = clientId;
            Timestamp = DateTime.Now;
            SequenceNumber = System.Threading.Interlocked.Increment(ref _sequenceCounter);
        }

        /// <summary>
        /// Constructeur pour créer un message avec un statut de cryptage spécifique
        /// </summary>
        /// <param name="content">Contenu du message</param>
        /// <param name="isEncrypted">Indique si le contenu est déjà crypté</param>
        /// <param name="clientId">ID du client</param>
        internal Message(string content, bool isEncrypted, string clientId = null)
        {
            _content = content;
            _isEncrypted = isEncrypted;
            ClientId = clientId;
            Timestamp = DateTime.Now;
            SequenceNumber = System.Threading.Interlocked.Increment(ref _sequenceCounter);
        }

        /// <summary>
        /// Crypte le contenu du message
        /// </summary>
        /// <param name="key">Clé de cryptage (optionnel)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel)</param>
        /// <returns>True si le cryptage a réussi</returns>
        public bool Encrypt(byte[] key = null, byte[] iv = null)
        {
            if (_isEncrypted)
            {
                Console.WriteLine("?? Message déjà crypté");
                return false;
            }

            try
            {
                string encrypted = MessageCrypto.Encrypt(_content, key, iv);
                if (!string.IsNullOrEmpty(encrypted) && encrypted != _content)
                {
                    _content = encrypted;
                    _isEncrypted = true;
                    Console.WriteLine($"?? Message #{SequenceNumber} crypté");
                    return true;
                }
                return false;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"? Erreur lors du cryptage du message #{SequenceNumber}: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Décrypte le contenu du message
        /// </summary>
        /// <param name="key">Clé de cryptage (optionnel)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel)</param>
        /// <returns>True si le décryptage a réussi</returns>
        public bool Decrypt(byte[] key = null, byte[] iv = null)
        {
            if (!_isEncrypted)
            {
                Console.WriteLine("?? Message déjà en clair");
                return false;
            }

            try
            {
                string decrypted = MessageCrypto.Decrypt(_content, key, iv);
                if (!string.IsNullOrEmpty(decrypted) && decrypted != _content)
                {
                    _content = decrypted;
                    _isEncrypted = false;
                    Console.WriteLine($"?? Message #{SequenceNumber} décrypté");
                    return true;
                }
                return false;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"? Erreur lors du décryptage du message #{SequenceNumber}: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Obtient le contenu, en le décryptant si nécessaire
        /// </summary>
        public string GetContent(byte[] key = null, byte[] iv = null)
        {
            if (_isEncrypted)
            {
                Decrypt(key, iv);
            }
            return _content;
        }

        /// <summary>
        /// Vérifie si le contenu semble crypté (format Base64 valide)
        /// </summary>
        public bool IsContentEncrypted()
        {
            return MessageCrypto.IsEncrypted(_content);
        }

        /// <summary>
        /// Retourne une représentation string du message
        /// </summary>
        public override string ToString()
        {
            string encStatus = _isEncrypted ? "[CRYPTÉ]" : "[CLAIR]";
            string clientInfo = !string.IsNullOrEmpty(ClientId) ? $"[{ClientId}] " : "";
            return $"#{SequenceNumber} {encStatus} {clientInfo}{Timestamp:HH:mm:ss.fff}: {(_content?.Length > 50 ? _content.Substring(0, 50) + "..." : _content)}";
        }
    }
}
