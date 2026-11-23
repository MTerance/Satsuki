using Microsoft.AspNetCore.Http;
using AkibaQuiz.Application.Auditing;
using AkibaQuiz.Application.Interfaces;
using System;
using System.Collections.Generic;
using System.Text;
using System.Diagnostics.CodeAnalysis;
using System.Security.Claims;

namespace AkibaQuiz.Api.Security
{
    public sealed class HttpAuditActorProvider : IAuditActorProvider
    {
        private readonly IHttpContextAccessor _httpContextAccessor;
        public const string VerifiedApiClientKey = "AkibaQuiz.VerifiedApiClient";

        public HttpAuditActorProvider(IHttpContextAccessor httpContextAccessor)
        {
            _httpContextAccessor = httpContextAccessor;
        }

        public AuditActor GetCurrent()
        {
            var http = _httpContextAccessor.HttpContext;

            if (http is null)
            {
                return new AuditActor(
                    ActorType: "System",
                    ActorId: "background-job",
                    CorrelationId: null);
            }

            var requestId = http.TraceIdentifier;

            if (http.Items.TryGetValue(VerifiedApiClientKey, out var client) 
                && Equals(client,"admin"))
            {
                return new AuditActor(
                    ActorType: "AdminApi",
                    ActorId: "admin-api-key",
                    CorrelationId: requestId);
            }

            if (http.User.Identity?.IsAuthenticated == true)
            {
                string? userId = http.User.FindFirst(ClaimTypes.NameIdentifier)?.Value;

                userId ??= http.User.Identity.Name;

                if (string.IsNullOrWhiteSpace(userId))
                {
                    throw new InvalidOperationException("Authenticated user has no identifier.");
                }
                return new AuditActor(
                    ActorType: "OrchardUser",
                    ActorId: userId,
                    CorrelationId: requestId);
            }
            throw new InvalidOperationException("No authenticated user or verified API client found.");
        }       
    }
}
