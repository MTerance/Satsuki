
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.Extensions.Logging;

namespace AkibaQuiz.Api.Security
{
    public sealed class CielCatalogApiKeyFilter
        : IAsyncAuthorizationFilter
    {
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
            var http = context.HttpContext;
            var headers = http.Request.Headers;

            http.Response.Headers["Cache-Control"] =
                "no-store";

            var expectedCielKey =
                ApiKeySecurity.GetCielKey();

            var expectedAdminKey =
                ApiKeySecurity.GetAdminKey();

            if (!ApiKeySecurity.IsConfigured(
                expectedCielKey))
            {
                _logger.LogError(
                    "La clé API Ciel n'est pas configurée " +
                    "ou est invalide.");

                context.Result =
                    new StatusCodeResult(503);

                return Task.CompletedTask;
            }

            if (ApiKeySecurity.AreIdentical(
                expectedAdminKey,
                expectedCielKey))
            {
                _logger.LogError(
                    "Les clés API Admin et Ciel " +
                    "doivent être distinctes.");

                context.Result =
                    new StatusCodeResult(503);

                return Task.CompletedTask;
            }

            bool hasCielHeader = headers.TryGetValue(
                ApiKeySecurity.CielHeader,
                out var suppliedCiel);

            bool hasAdminHeader = headers.TryGetValue(
                ApiKeySecurity.AdminHeader,
                out var suppliedAdmin);

            // Rejeter les requêtes sans identification
            // ou avec deux identifications simultanées.
            if (hasCielHeader == hasAdminHeader)
            {
                context.Result =
                    new UnauthorizedResult();

                return Task.CompletedTask;
            }

            // Accès normal du client Ciel.
            if (hasCielHeader)
            {
                if (!ApiKeySecurity.Matches(
                    expectedCielKey,
                    suppliedCiel))
                {
                    context.Result =
                        new UnauthorizedResult();
                }

                return Task.CompletedTask;
            }

            // Compatibilité historique avec les
            // outils d'administration existants.
            if (!ApiKeySecurity.Matches(
                expectedAdminKey,
                suppliedAdmin))
            {
                context.Result =
                    new UnauthorizedResult();
            }

            return Task.CompletedTask;
        }
    }
}
