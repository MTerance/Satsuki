using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

namespace Satsuki.Utils
{
    /// <summary>
    /// Utilitaire de cryptage AES pour les messages r�seau
    /// </summary>
    public static class MessageCrypto
    {
        // Cl� AES de 256 bits (32 bytes) - En production, cette cl� devrait �tre g�n�r�e de mani�re s�curis�e
        private static readonly byte[] DefaultKey = Encoding.UTF8.GetBytes("MySecretKey123456789012345678901"); // 32 bytes
        
        // IV (Initialization Vector) de 128 bits (16 bytes)
        private static readonly byte[] DefaultIV = Encoding.UTF8.GetBytes("MyInitVector1234"); // 16 bytes

        /// <summary>
        /// Crypte un message en utilisant AES-256
        /// </summary>
        /// <param name="plainText">Texte � crypter</param>
        /// <param name="key">Cl� de cryptage (optionnel, utilise la cl� par d�faut si null)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel, utilise l'IV par d�faut si null)</param>
        /// <returns>Message crypt� encod� en Base64</returns>
        public static string Encrypt(string plainText, byte[] key = null, byte[] iv = null)
        {
            if (string.IsNullOrEmpty(plainText))
                return string.Empty;

            key ??= DefaultKey;
            iv ??= DefaultIV;

            try
            {
                using var aes = Aes.Create();
                aes.Key = key;
                aes.IV = iv;
                aes.Mode = CipherMode.CBC;
                aes.Padding = PaddingMode.PKCS7;

                using var encryptor = aes.CreateEncryptor();
                using var memoryStream = new MemoryStream();
                using var cryptoStream = new CryptoStream(memoryStream, encryptor, CryptoStreamMode.Write);
                using var writer = new StreamWriter(cryptoStream);

                writer.Write(plainText);
                writer.Flush();
                cryptoStream.FlushFinalBlock();

                byte[] encryptedBytes = memoryStream.ToArray();
                return Convert.ToBase64String(encryptedBytes);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur lors du cryptage: {ex.Message}");
                return plainText; // Retourne le texte original en cas d'erreur
            }
        }

        /// <summary>
        /// D�crypte un message crypt� en AES-256
        /// </summary>
        /// <param name="encryptedText">Texte crypt� encod� en Base64</param>
        /// <param name="key">Cl� de d�cryptage (optionnel, utilise la cl� par d�faut si null)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel, utilise l'IV par d�faut si null)</param>
        /// <returns>Message d�crypt� en texte clair</returns>
        public static string Decrypt(string encryptedText, byte[] key = null, byte[] iv = null)
        {
            if (string.IsNullOrEmpty(encryptedText))
                return string.Empty;

            key ??= DefaultKey;
            iv ??= DefaultIV;

            try
            {
                byte[] encryptedBytes = Convert.FromBase64String(encryptedText);

                using var aes = Aes.Create();
                aes.Key = key;
                aes.IV = iv;
                aes.Mode = CipherMode.CBC;
                aes.Padding = PaddingMode.PKCS7;

                using var decryptor = aes.CreateDecryptor();
                using var memoryStream = new MemoryStream(encryptedBytes);
                using var cryptoStream = new CryptoStream(memoryStream, decryptor, CryptoStreamMode.Read);
                using var reader = new StreamReader(cryptoStream);

                return reader.ReadToEnd();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur lors du d�cryptage: {ex.Message}");
                return encryptedText; // Retourne le texte crypt� en cas d'erreur
            }
        }

        /// <summary>
        /// G�n�re une nouvelle cl� AES-256 al�atoire
        /// </summary>
        /// <returns>Cl� de 32 bytes</returns>
        public static byte[] GenerateRandomKey()
        {
            using var aes = Aes.Create();
            aes.GenerateKey();
            return aes.Key;
        }

        /// <summary>
        /// G�n�re un nouveau vecteur d'initialisation al�atoire
        /// </summary>
        /// <returns>IV de 16 bytes</returns>
        public static byte[] GenerateRandomIV()
        {
            using var aes = Aes.Create();
            aes.GenerateIV();
            return aes.IV;
        }

        /// <summary>
        /// Convertit une cl�/IV en string pour affichage ou stockage
        /// </summary>
        /// <param name="bytes">Bytes � convertir</param>
        /// <returns>String en Base64</returns>
        public static string BytesToBase64(byte[] bytes)
        {
            return Convert.ToBase64String(bytes);
        }

        /// <summary>
        /// Convertit une string Base64 en bytes
        /// </summary>
        /// <param name="base64String">String en Base64</param>
        /// <returns>Array de bytes</returns>
        public static byte[] Base64ToBytes(string base64String)
        {
            return Convert.FromBase64String(base64String);
        }

        /// <summary>
        /// V�rifie si une string est un message crypt� valide (Base64)
        /// </summary>
        /// <param name="text">Texte � v�rifier</param>
        /// <returns>True si le texte semble �tre crypt�</returns>
        public static bool IsEncrypted(string text)
        {
            if (string.IsNullOrEmpty(text))
                return false;

            try
            {
                Convert.FromBase64String(text);
                return true;
            }
            catch
            {
                return false;
            }
        }
    }
}