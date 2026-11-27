using Microsoft.Extensions.Primitives;
using System;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;

namespace AkibaQuiz.Api.Security
{
    internal static class ApiKeySecurity
    {
        public const string AdminHeader =
            "X-Akiba-Admin-Key";

        public const string CielHeader =
            "X-Akiba-Ciel-Key";

        public const string AdminEnvironmentVariable =
            "AKIBA_ADMIN_API_KEY";

        public const string CielEnvironmentVariable =
            "AKIBA_CIEL_READ_API_KEY";

        public const int MaxKeyLength = 256;

        public static string? GetAdminKey()
        {
            return Environment.GetEnvironmentVariable(
                AdminEnvironmentVariable);
        }

        public static string? GetCielKey()
        {
            return Environment.GetEnvironmentVariable(
                CielEnvironmentVariable);
        }

        public static bool IsConfigured(string? key)
        {
            return !string.IsNullOrWhiteSpace(key)
                && key.Length <= MaxKeyLength;
        }

        public static bool Matches(
            string? expected,
            StringValues supplied)
        {
            if (!IsConfigured(expected))
                return false;

            if (supplied.Count != 1)
                return false;

            var actual = supplied[0];

            if (!IsConfigured(actual))
                return false;

            return FixedTimeEquals(expected!, actual!);
        }

        public static bool AreIdentical(
            string? first,
            string? second)
        {
            if (!IsConfigured(first) ||
                !IsConfigured(second))
            {
                return false;
            }

            return FixedTimeEquals(first!, second!);
        }

        private static bool FixedTimeEquals(
            string first,
            string second)
        {
            byte[] firstHash = SHA256.HashData(
                Encoding.UTF8.GetBytes(first));

            byte[] secondHash = SHA256.HashData(
                Encoding.UTF8.GetBytes(second));

            return CryptographicOperations.FixedTimeEquals(
                firstHash,
                secondHash);
        }
    }
}
