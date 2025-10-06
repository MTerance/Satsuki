using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

namespace Satsuki.Utils
{
    /// <summary>
    /// Classe utilitaire pour le cryptage et d�cryptage AES des messages r�seau
    /// </summary>
    public static class MessageCrypto
    {
        // Cl� AES de 256 bits (32 bytes) - En production, utilisez une cl� g�n�r�e de mani�re s�curis�e
        private static readonly byte[] DefaultKey = Encoding.UTF8.GetBytes("SatsukiGameServer2024Key1234567890"); // 32 bytes
        
        // IV (Initialization Vector) de 128 bits (16 bytes)
        private static readonly byte[] DefaultIV = Encoding.UTF8.GetBytes("SatsukiInitVect1"); // 16 bytes

        /// <summary>
        /// Crypte un message en utilisant AES-256-CBC
        /// </summary>
        /// <param name="plainText">Texte en clair � crypter</param>
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
        /// D�crypte un message crypt� en AES-256-CBC
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

        /// <summary>
        /// Crypte un message avec une nouvelle cl� al�atoire
        /// </summary>
        /// <param name="plainText">Texte � crypter</param>
        /// <returns>Tuple contenant le message crypt� et les cl�s utilis�es</returns>
        public static (string encryptedMessage, byte[] key, byte[] iv) EncryptWithRandomKey(string plainText)
        {
            var key = GenerateRandomKey();
            var iv = GenerateRandomIV();
            var encrypted = Encrypt(plainText, key, iv);
            return (encrypted, key, iv);
        }

        /// <summary>
        /// Teste le syst�me de cryptage avec un message de test
        /// </summary>
        /// <returns>True si le test r�ussit</returns>
        public static bool TestEncryption()
        {
            try
            {
                string testMessage = "Message de test pour v�rifier le cryptage";
                Console.WriteLine($"?? Test de cryptage - Message original: {testMessage}");

                // Test avec cl�s par d�faut
                string encrypted = Encrypt(testMessage);
                Console.WriteLine($"?? Message crypt�: {encrypted}");

                string decrypted = Decrypt(encrypted);
                Console.WriteLine($"?? Message d�crypt�: {decrypted}");

                bool success = testMessage == decrypted;
                Console.WriteLine($"? Test de cryptage: {(success ? "R�USSI" : "�CHEC")}");

                // Test avec cl�s al�atoires
                var (encryptedRandom, key, iv) = EncryptWithRandomKey(testMessage);
                string decryptedRandom = Decrypt(encryptedRandom, key, iv);
                bool successRandom = testMessage == decryptedRandom;
                Console.WriteLine($"?? Test cryptage cl�s al�atoires: {(successRandom ? "R�USSI" : "�CHEC")}");

                return success && successRandom;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"? Erreur lors du test de cryptage: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Obtient les informations sur les cl�s par d�faut
        /// </summary>
        /// <returns>Informations sur les cl�s</returns>
        public static (string keyBase64, string ivBase64) GetDefaultKeyInfo()
        {
            return (BytesToBase64(DefaultKey), BytesToBase64(DefaultIV));
        }

        /// <summary>
        /// Nettoie les cl�s de la m�moire pour la s�curit�
        /// </summary>
        /// <param name="key">Cl� � nettoyer</param>
        /// <param name="iv">IV � nettoyer</param>
        public static void ClearKeys(byte[] key, byte[] iv)
        {
            if (key != null)
                Array.Clear(key, 0, key.Length);
            if (iv != null)
                Array.Clear(iv, 0, iv.Length);
        }
    }
}