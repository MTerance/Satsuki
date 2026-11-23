using AkibaQuiz.Application.Auditing;
using Dapper;
using Microsoft.Data.Sqlite;
using System;
using System.Collections.Generic;
using System.Data;
using System.Text;

namespace AkibaQuiz.Infrastructure.Auditing
{
    internal static class AuditSqlWriter
    {
        public static async Task WriteAsync(SqliteConnection db, IDbTransaction transaction, AuditActor actor, string entityType, long entityId, string action, string? detailsJson = null, CancellationToken ct)
        {
            ArgumentNullException.ThrowIfNull(actor);
            if (actor.ActorType is not "OrchardUser" or "AdminApi" or "System")
            {
                throw new InvalidOperationException(
                    $"Type d'auteur inconnu : {actor.ActorType}");
            }

            if (entityId <= 0)
                throw new ArgumentOutOfRangeException(
                    nameof(entityId));

            if (string.IsNullOrWhiteSpace(actor.ActorId)
                || actor.ActorId.Length > 128)
            {
                throw new InvalidOperationException(
                    "Identifiant d'auteur invalide.");
            }
            if (detailsJson is not null)
            {
                if (detailsJson.Length > 8192)
                {
                    throw new InvalidOperationException(
                        "Les détails d'audit dépassent 8192 caractères.");
                }

                try
                {
                    using var document =
                        System.Text.Json.JsonDocument.Parse(
                            detailsJson);
                }
                catch (System.Text.Json.JsonException ex)
                {
                    throw new InvalidOperationException(
                        "Le JSON d'audit est invalide.", ex);
                }
            }
            const string sql = """
    INSERT INTO AuditEvents
    (
        OccurredAtUtc,
        EntityType,
        EntityId,
        Action,
        ActorType,
        ActorId,
        CorrelationId,
        DetailsJson
    )
    VALUES
    (
        @OccurredAtUtc,
        @EntityType,
        @EntityId,
        @Action,
        @ActorType,
        @ActorId,
        @CorrelationId,
        @DetailsJson
    );
    """;

            var parameters = new
            {
                OccurredAtUtc =
            DateTimeOffset.UtcNow.ToString("O"),

                EntityType = entityType,
                EntityId = entityId,
                Action = action,

                ActorType = actor.ActorType,
                ActorId = actor.ActorId,
                CorrelationId = actor.CorrelationId,

                DetailsJson = detailsJson
            };

            if (parameters.ActorType is not
                ("OrchardUser" or "AdminApi" or "System"))
            {
                throw new InvalidOperationException(
                    $"Audit ActorType invalide : " +
                    $"'{parameters.ActorType}'");
            }

            var diagnostic = await db.QuerySingleAsync<(
    string ActorType,
    string ActorTypeQuoted)>(
    new CommandDefinition(
        """
        SELECT
            @ActorType AS ActorType,
            quote(@ActorType) AS ActorTypeQuoted;
        """,
        parameters,
        transaction,
        cancellationToken: ct));

            System.Diagnostics.Debug.WriteLine(
                $"AUDIT DIAGNOSTIC : {diagnostic.ActorTypeQuoted}");

            await db.ExecuteAsync(
                new CommandDefinition(
                    sql,
                    parameters,
                    transaction,
                    cancellationToken: ct));
        }
    }
}
