
using AkibaQuiz.Contracts;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.Data.Sqlite;
using Microsoft.Extensions.Logging;

namespace AkibaQuiz.Api.Security
{
    public sealed class AdminApiKeyFilter
        : IAsyncAuthorizationFilter
    {
        private readonly ILogger<AdminApiKeyFilter> _logger;

        public AdminApiKeyFilter(
            ILogger<AdminApiKeyFilter> logger)
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

            var expectedAdminKey =
                ApiKeySecurity.GetAdminKey();

            var expectedCielKey =
                ApiKeySecurity.GetCielKey();

            // Échec fermé si la configuration Admin
            // est absente ou invalide.
            if (!ApiKeySecurity.IsConfigured(
                expectedAdminKey))
            {
                _logger.LogError(
                    "La clé API Admin n'est pas configurée " +
                    "ou est invalide.");

                context.Result =
                    new StatusCodeResult(503);

                return Task.CompletedTask;
            }

            // Les deux clients doivent posséder
            // des secrets distincts.
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

            // Une requête Admin ne doit jamais
            // contenir d'en-tête Ciel.
            if (headers.ContainsKey(
                ApiKeySecurity.CielHeader))
            {
                context.Result =
                    new UnauthorizedResult();

                return Task.CompletedTask;
            }

            if (!headers.TryGetValue(
                ApiKeySecurity.AdminHeader,
                out var supplied))
            {
                context.Result =
                    new UnauthorizedResult();

                return Task.CompletedTask;
            }

            if (!ApiKeySecurity.Matches(
                expectedAdminKey,
                supplied))
            {
                context.Result =
                    new UnauthorizedResult();

                return Task.CompletedTask;
            }

            // Marquer uniquement un client
            // effectivement authentifié.
            if (context.Result is null)
            {
                http.Items[
                    HttpAuditActorProvider
                        .VerifiedApiClientKey] = "admin";
            }

            return Task.CompletedTask;
        }
    }

    public sealed class ApiExceptionFilter
        : IExceptionFilter
    {
        public void OnException(
            ExceptionContext context)
        {
            var (status, message) =
                context.Exception switch
                {
                    ApiValidationException e =>
                        (400, e.Message),

                    ApiConflictException e =>
                        (409, e.Message),

                    KeyNotFoundException e =>
                        (404, e.Message),

                    SqliteException e
                        when e.SqliteErrorCode == 19 =>
                        (
                            409,
                            "Contrainte d'intégrité SQLite " +
                            "non respectée."
                        ),

                    _ => (0, "")
                };

            if (status == 0)
                return;

            context.Result = new ObjectResult(
                new { error = message })
            {
                StatusCode = status
            };

            context.ExceptionHandled = true;
        }
    }
}
