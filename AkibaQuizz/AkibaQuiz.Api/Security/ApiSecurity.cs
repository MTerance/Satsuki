using AkibaQuiz.Contracts;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using System;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;

namespace AkibaQuiz.Api.Security
{
    public sealed class AdminApiKeyFilter : IAsyncAuthorizationFilter
    {
        public Task OnAuthorizationAsync(AuthorizationFilterContext context)
        {
            var expected = Environment.GetEnvironmentVariable("AKIBA_ADMIN_API_KEY");
            var supplied = context.HttpContext.Request.Headers["X-Akiba-Admin-Key"].ToString();
            if (string.IsNullOrWhiteSpace(expected) || string.IsNullOrWhiteSpace(supplied)) context.Result = new UnauthorizedResult();
            else if (!CryptographicOperations.FixedTimeEquals(Encoding.UTF8.GetBytes(expected), Encoding.UTF8.GetBytes(supplied))) context.Result = new UnauthorizedResult();
            return Task.CompletedTask;
        }
    }
    public sealed class ApiExceptionFilter : IExceptionFilter
    {
        public void OnException(ExceptionContext context)
        {
            var (status, message) = context.Exception switch
            {
                ApiValidationException e => (400, e.Message),
                ApiConflictException e => (409, e.Message),
                KeyNotFoundException e => (404, e.Message),
                Microsoft.Data.Sqlite.SqliteException e when e.SqliteErrorCode == 19 => (409, "Contrainte d'intégrité SQLite non respectée."),
                _ => (0, "")
            };
            if (status == 0) return;
            context.Result = new ObjectResult(new { error = message }) { StatusCode = status }; context.ExceptionHandled = true;
        }
    }
}
