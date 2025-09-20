using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

namespace Satsuki.Utils
{
    /// <summary>
    /// Utilitaire de cryptage AES pour les messages réseau
    /// </summary>
    public static class MessageCrypto
    {
        // Clé AES de 256 bits (32 bytes) - En production, cette clé devrait être générée de manière sécurisée
        private static readonly byte[] DefaultKey = Encoding.UTF8.GetBytes("MySecretKey123456789012345678901"); // 32 bytes
        
        // IV (Initialization Vector) de 128 bits (16 bytes)
        private static readonly byte[] DefaultIV = Encoding.UTF8.GetBytes("MyInitVector1234"); // 16 bytes

        /// <summary>
        /// Crypte un message en utilisant AES-256
        /// </summary>
        /// <param name="plainText">Texte à crypter</param>
        /// <param name="key">Clé de cryptage (optionnel, utilise la clé par défaut si null)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel, utilise l'IV par défaut si null)</param>
        /// <returns>Message crypté encodé en Base64</returns>
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
        /// Décrypte un message crypté en AES-256
        /// </summary>
        /// <param name="encryptedText">Texte crypté encodé en Base64</param>
        /// <param name="key">Clé de décryptage (optionnel, utilise la clé par défaut si null)</param>
        /// <param name="iv">Vecteur d'initialisation (optionnel, utilise l'IV par défaut si null)</param>
        /// <returns>Message décrypté en texte clair</returns>
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
                Console.WriteLine($"Erreur lors du décryptage: {ex.Message}");
                return encryptedText; // Retourne le texte crypté en cas d'erreur
            }
        }

        /// <summary>
        /// Génère une nouvelle clé AES-256 aléatoire
        /// </summary>
        /// <returns>Clé de 32 bytes</returns>
        public static byte[] GenerateRandomKey()
        {
            using var aes = Aes.Create();
            aes.GenerateKey();
            return aes.Key;
        }

        /// <summary>
        /// Génère un nouveau vecteur d'initialisation aléatoire
        /// </summary>
        /// <returns>IV de 16 bytes</returns>
        public static byte[] GenerateRandomIV()
        {
            using var aes = Aes.Create();
            aes.GenerateIV();
            return aes.IV;
        }

        /// <summary>
        /// Convertit une clé/IV en string pour affichage ou stockage
        /// </summary>
        /// <param name="bytes">Bytes à convertir</param>
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
        /// Vérifie si une string est un message crypté valide (Base64)
        /// </summary>
        /// <param name="text">Texte à vérifier</param>
        /// <returns>True si le texte semble être crypté</returns>
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