using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
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

        /// <summary>
        /// Indique si le message est actuellement crypté
        /// </summary>
        public bool IsEncrypted => _isEncrypted;

        public Message(string content)
        {
            _content = content;
            _isEncrypted = false;
            Timestamp = DateTime.Now;
        }

        /// <summary>
        /// Constructeur pour créer un message avec un statut de cryptage spécifique
        /// </summary>
        /// <param name="content">Contenu du message</param>
        /// <param name="isEncrypted">Indique si le contenu est déjà crypté</param>
        internal Message(string content, bool isEncrypted)
        {
            _content = content;
            _isEncrypted = isEncrypted;
            Timestamp = DateTime.Now;
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
                Console.WriteLine("Message déjà crypté");
                return false;
            }

            try
            {
                string encrypted = MessageCrypto.Encrypt(_content, key, iv);
                if (!string.IsNullOrEmpty(encrypted) && encrypted != _content)
                {
                    _content = encrypted;
                    _isEncrypted = true;
                    return true;
                }
                return false;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur lors du cryptage du message: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Décrypte le contenu du message
        /// </summary>
        /// <param name="key">Clé de décryptage (optionnel)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel)</param>
        /// <returns>True si le décryptage a réussi</returns>
        public bool Decrypt(byte[] key = null, byte[] iv = null)
        {
            if (!_isEncrypted)
            {
                Console.WriteLine("Message non crypté");
                return false;
            }

            try
            {
                string decrypted = MessageCrypto.Decrypt(_content, key, iv);
                if (!string.IsNullOrEmpty(decrypted) && decrypted != _content)
                {
                    _content = decrypted;
                    _isEncrypted = false;
                    return true;
                }
                return false;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur lors du décryptage du message: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Obtient le contenu décrypté sans modifier l'état du message
        /// </summary>
        /// <param name="key">Clé de décryptage (optionnel)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel)</param>
        /// <returns>Contenu décrypté ou contenu original si non crypté</returns>
        public string GetDecryptedContent(byte[] key = null, byte[] iv = null)
        {
            if (!_isEncrypted)
                return _content;

            try
            {
                return MessageCrypto.Decrypt(_content, key, iv);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur lors du décryptage: {ex.Message}");
                return _content; // Retourne le contenu crypté en cas d'erreur
            }
        }

        /// <summary>
        /// Crée une copie cryptée du message sans modifier l'original
        /// </summary>
        /// <param name="key">Clé de cryptage (optionnel)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel)</param>
        /// <returns>Nouveau message crypté</returns>
        public Message CreateEncryptedCopy(byte[] key = null, byte[] iv = null)
        {
            if (_isEncrypted)
                return new Message(_content, true) { Timestamp = this.Timestamp };

            string encryptedContent = MessageCrypto.Encrypt(_content, key, iv);
            return new Message(encryptedContent, true) { Timestamp = this.Timestamp };
        }

        /// <summary>
        /// Crée une copie décryptée du message sans modifier l'original
        /// </summary>
        /// <param name="key">Clé de décryptage (optionnel)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel)</param>
        /// <returns>Nouveau message décrypté</returns>
        public Message CreateDecryptedCopy(byte[] key = null, byte[] iv = null)
        {
            if (!_isEncrypted)
                return new Message(_content, false) { Timestamp = this.Timestamp };

            string decryptedContent = MessageCrypto.Decrypt(_content, key, iv);
            return new Message(decryptedContent, false) { Timestamp = this.Timestamp };
        }

        public override string ToString()
        {
            string status = _isEncrypted ? "[CRYPTÉ]" : "[CLAIR]";
            return $"{status} [{Timestamp:HH:mm:ss.fff}] {(_isEncrypted ? "***CONTENU_CRYPTÉ***" : _content)}";
        }
    }
}
