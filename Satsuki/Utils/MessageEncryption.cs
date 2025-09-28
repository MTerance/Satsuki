using System;
using System.Security.Cryptography;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Utils
{
    public static class MessageEncryption
    {
        private static readonly byte[] Key = Encoding.UTF8.GetBytes("SatsukiKey1234567890123456789012"); // 32 bytes
        private static readonly byte[] IV = Encoding.UTF8.GetBytes("SatsukiIV1234567"); // 16 bytes

        public static string Encrypt(string plaintext)
        {
            using var aes = Aes.Create();
            aes.Key = Key;
            aes.IV = IV;

            using var encryptor = aes.CreateEncryptor();
            var plaintextBytes = Encoding.UTF8.GetBytes(plaintext);
            var ciphertextBytes = encryptor.TransformFinalBlock(plaintextBytes, 0, plaintextBytes.Length);

            return Convert.ToBase64String(ciphertextBytes);
        }

        public static string Decrypt(string ciphertext)
        {
            using var aes = Aes.Create();
            aes.Key = Key;
            aes.IV = IV;

            using var decryptor = aes.CreateDecryptor();
            var ciphertextBytes = Convert.FromBase64String(ciphertext);
            var plaintextBytes = decryptor.TransformFinalBlock(ciphertextBytes, 0, ciphertextBytes.Length);

            return Encoding.UTF8.GetString(plaintextBytes);
        }
    }
}
