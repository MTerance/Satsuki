using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Primitives;
using System;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;

namespace AkibaQuiz.Api.Security
{
    public class CielCatalogApiKeyFilter : IAsyncAuthorizationFilter
    {
        private const string CielHeader =
        "X-Akiba-Ciel-Key";

        private const string AdminHeader =
            "X-Akiba-Admin-Key";

        private readonly ILogger<CielCatalogApiKeyFilter>
            _logger;

        public CielCatalogApiKeyFilter(
            ILogger<CielCatalogApiKeyFilter> logger)
        {
            _logger = logger;
        }

        public Task OnAuthorizationAsync(
            AuthorizationFilterContext context)
        {
            var headers =
                context.HttpContext.Request.Headers;

            // Le catalogue ne doit pas être mis en cache
            // dans des caches HTTP partagés.
            context.HttpContext.Response.Headers[
                "Cache-Control"] = "no-store";

            string? expectedCielKey =
                Environment.GetEnvironmentVariable(
                    "AKIBA_CIEL_READ_API_KEY");

            if (string.IsNullOrWhiteSpace(expectedCielKey))
            {
                _logger.LogError(
                    "La clé API de lecture Ciel n'est pas configurée.");

                // Échec fermé : aucun accès au catalogue.
                context.Result = new StatusCodeResult(503);
                return Task.CompletedTask;
            }

            bool hasCielHeader = headers.TryGetValue(
                CielHeader, out var suppliedCiel);

            bool hasAdminHeader = headers.TryGetValue(
                AdminHeader, out var suppliedAdmin);

            // Interdire deux mécanismes d'identification
            // simultanés dans la même requête.
            if (hasCielHeader && hasAdminHeader)
            {
                context.Result = new UnauthorizedResult();
                return Task.CompletedTask;
            }

            // ========================================
            // 1. ACCÈS CIEL : LECTURE DU CATALOGUE
            // ========================================

            if (hasCielHeader)
            {
                if (!Matches(
                    expectedCielKey,
                    suppliedCiel))
                {
                    context.Result = new UnauthorizedResult();
                }

                return Task.CompletedTask;
            }

            // ========================================
            // 2. COMPATIBILITÉ TEMPORAIRE
            //    AVEC L'ANCIENNE CLÉ ADMIN
            // ========================================

            if (hasAdminHeader)
            {
                string? expectedAdminKey =
                    Environment.GetEnvironmentVariable(
                        "AKIBA_ADMIN_API_KEY");

                if (!Matches(
                    expectedAdminKey,
                    suppliedAdmin))
                {
                    context.Result = new UnauthorizedResult();
                }

                return Task.CompletedTask;
            }

            context.Result = new UnauthorizedResult();
            return Task.CompletedTask;
        }

        private static bool Matches(
            string? expected,
            StringValues supplied)
        {
            if (string.IsNullOrWhiteSpace(expected))
                return false;

            // Une seule valeur d'en-tête est acceptée.
            if (supplied.Count != 1)
                return false;

            var actual = supplied[0];

            if (string.IsNullOrWhiteSpace(actual))
                return false;

            // Éviter les valeurs anormalement longues.
            if (actual.Length > 256)
                return false;

            byte[] expectedHash = SHA256.HashData(
                Encoding.UTF8.GetBytes(expected));

            byte[] suppliedHash = SHA256.HashData(
                Encoding.UTF8.GetBytes(actual));

            return CryptographicOperations.FixedTimeEquals(
                expectedHash,
                suppliedHash);
        }
    }
}
