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
        /// Indique si le message est actuellement crypt�
        /// </summary>
        public bool IsEncrypted => _isEncrypted;
        
        private static int _sequenceCounter = 0;

        public Message(string content)
        {
            _content = content;
            _isEncrypted = false;
            Timestamp = DateTime.Now;
            SequenceNumber = System.Threading.Interlocked.Increment(ref _sequenceCounter);
        }

        /// <summary>
        /// Constructeur pour cr�er un message avec un statut de cryptage sp�cifique
        /// </summary>
        /// <param name="content">Contenu du message</param>
        /// <param name="isEncrypted">Indique si le contenu est d�j� crypt�</param>
        internal Message(string content, bool isEncrypted)
        {
            _content = content;
            _isEncrypted = isEncrypted;
            Timestamp = DateTime.Now;
            SequenceNumber = System.Threading.Interlocked.Increment(ref _sequenceCounter);
        }

        /// <summary>
        /// Crypte le contenu du message
        /// </summary>
        /// <param name="key">Cl� de cryptage (optionnel)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel)</param>
        /// <returns>True si le cryptage a r�ussi</returns>
        public bool Encrypt(byte[] key = null, byte[] iv = null)
        {
            if (_isEncrypted)
            {
                Console.WriteLine("?? Message d�j� crypt�");
                return false;
            }

            try
            {
                string encrypted = MessageCrypto.Encrypt(_content, key, iv);
                if (!string.IsNullOrEmpty(encrypted) && encrypted != _content)
                {
                    _content = encrypted;
                    _isEncrypted = true;
                    Console.WriteLine($"?? Message #{SequenceNumber} crypt�");
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
        /// D�crypte le contenu du message
        /// </summary>
        /// <param name="key">Cl� de d�cryptage (optionnel)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel)</param>
        /// <returns>True si le d�cryptage a r�ussi</returns>
        public bool Decrypt(byte[] key = null, byte[] iv = null)
        {
            if (!_isEncrypted)
            {
                Console.WriteLine("?? Message non crypt�");
                return false;
            }

            try
            {
                string decrypted = MessageCrypto.Decrypt(_content, key, iv);
                if (!string.IsNullOrEmpty(decrypted) && decrypted != _content)
                {
                    _content = decrypted;
                    _isEncrypted = false;
                    Console.WriteLine($"?? Message #{SequenceNumber} d�crypt�");
                    return true;
                }
                return false;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"? Erreur lors du d�cryptage du message #{SequenceNumber}: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Obtient le contenu d�crypt� sans modifier l'�tat du message
        /// </summary>
        /// <param name="key">Cl� de d�cryptage (optionnel)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel)</param>
        /// <returns>Contenu d�crypt� ou contenu original si non crypt�</returns>
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
                Console.WriteLine($"? Erreur lors du d�cryptage: {ex.Message}");
                return _content; // Retourne le contenu crypt� en cas d'erreur
            }
        }

        /// <summary>
        /// Cr�e une copie crypt�e du message sans modifier l'original
        /// </summary>
        /// <param name="key">Cl� de cryptage (optionnel)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel)</param>
        /// <returns>Nouveau message crypt�</returns>
        public Message CreateEncryptedCopy(byte[] key = null, byte[] iv = null)
        {
            if (_isEncrypted)
                return new Message(_content, true) { Timestamp = this.Timestamp };

            string encryptedContent = MessageCrypto.Encrypt(_content, key, iv);
            return new Message(encryptedContent, true) { Timestamp = this.Timestamp };
        }

        /// <summary>
        /// Cr�e une copie d�crypt�e du message sans modifier l'original
        /// </summary>
        /// <param name="key">Cl� de d�cryptage (optionnel)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel)</param>
        /// <returns>Nouveau message d�crypt�</returns>
        public Message CreateDecryptedCopy(byte[] key = null, byte[] iv = null)
        {
            if (!_isEncrypted)
                return new Message(_content, false) { Timestamp = this.Timestamp };

            string decryptedContent = MessageCrypto.Decrypt(_content, key, iv);
            return new Message(decryptedContent, false) { Timestamp = this.Timestamp };
        }

        public override string ToString()
        {
            string status = _isEncrypted ? "[??CRYPT�]" : "[??CLAIR]";
            string content = _isEncrypted ? "***CONTENU_CRYPT�***" : _content;
            return $"{status} [{Timestamp:HH:mm:ss.fff}] #{SequenceNumber}: {content}";
        }
    }
}