using AkibaQuiz.Application.Interfaces;
using Dapper;
using Microsoft.Data.Sqlite;
using System;
using System.Collections.Generic;
using System.Data;
using System.Text;

namespace AkibaQuiz.Infrastructure.Auditing
{
    public enum AuditEntityType
    {
        QuestionAnswer,
        QCM,
        Game,
        Category,
        Tag
    }

    public enum AuditOperation
    {
        Create,
        Update,
        Delete
    }

    public sealed record AuditSnapshot(
        long Id,
        long? CategoryId,
        string? Name,
        string? Color,
        IReadOnlyList<long> TagIds);

    public sealed class AuditTrail(
        IAuditActorProvider actorProvider)
    {
        private sealed class SnapshotRow
        {
            public long Id { get; set; }
            public long? IdCategory { get; set; }
            public string? Name { get; set; }
            public string? Color { get; set; }
        }

        // =========================================
        // CAPTURE DE L'ÉTAT ACTUEL
        // =========================================

        public async Task<AuditSnapshot?> CaptureAsync(
            SqliteConnection db,
            IDbTransaction tx,
            AuditEntityType entity,
            long? id,
            CancellationToken ct)
        {
            if (id is null)
                return null;

            if (id <= 0)
                throw new ArgumentOutOfRangeException(nameof(id));

            // Tous les fragments SQL proviennent
            // de cette liste fermée.
            var (sql, tagColumn) = entity switch
            {
                AuditEntityType.QuestionAnswer => (
                    """
                SELECT Id, IdCategory
                FROM QuestionsAnswers
                WHERE Id = @id
                """,
                    "IdQuestionAnswer"),

                AuditEntityType.QCM => (
                    """
                SELECT Id, IdCategory
                FROM QCMQuestion
                WHERE Id = @id
                """,
                    "IdQCM"),

                AuditEntityType.Category => (
                    """
                SELECT Id, Name
                FROM Categories
                WHERE Id = @id
                """,
                    (string?)null),

                AuditEntityType.Tag => (
                    """
                SELECT Id, Name, Color
                FROM Tags
                WHERE Id = @id
                """,
                    (string?)null),

                AuditEntityType.Game => (
                    """
                SELECT Id, Name
                FROM Games
                WHERE Id = @id
                """,
                    (string?)null),

                _ => throw new ArgumentOutOfRangeException(
                    nameof(entity))
            };

            var row = await db
                .QuerySingleOrDefaultAsync<SnapshotRow>(
                    new CommandDefinition(
                        sql,
                        new { id },
                        tx,
                        cancellationToken: ct));

            if (row is null)
                return null;

            long[] tagIds = [];

            // Les catégories, les tags et les Games
            // ne possèdent pas cette association.
            if (tagColumn is not null)
            {
                string tagSql = $"""
                SELECT DISTINCT IdTag
                FROM TagQuizz
                WHERE {tagColumn} = @id
                ORDER BY IdTag
                """;

                tagIds = (await db.QueryAsync<long>(
                    new CommandDefinition(
                        tagSql,
                        new { id },
                        tx,
                        cancellationToken: ct)))
                    .ToArray();
            }

            return new AuditSnapshot(
                row.Id,
                row.IdCategory,
                row.Name,
                row.Color,
                tagIds);
        }

        // =========================================
        // ENREGISTREMENT DE L'ÉVÉNEMENT
        // =========================================

        public async Task RecordAsync(
            SqliteConnection db,
            IDbTransaction tx,
            AuditEntityType entity,
            long id,
            AuditOperation operation,
            AuditSnapshot? before,
            AuditSnapshot? after,
            CancellationToken ct)
        {
            if (id <= 0)
                throw new ArgumentOutOfRangeException(nameof(id));

            if (before is not null && before.Id != id ||
                after is not null && after.Id != id)
            {
                throw new InvalidOperationException(
                    "L'identifiant du snapshot ne correspond " +
                    "pas à l'entité auditée.");
            }

            bool valid = operation switch
            {
                AuditOperation.Create =>
                    after is not null,

                AuditOperation.Update =>
                    before is not null && after is not null,

                AuditOperation.Delete =>
                    before is not null && after is null,

                _ => false
            };

            if (!valid)
                throw new InvalidOperationException(
                    "Snapshots incompatibles avec " +
                    "l'opération d'audit.");

            string detailsJson = entity switch
            {
                AuditEntityType.QuestionAnswer or
                AuditEntityType.QCM =>
                    AuditDetailsFactory.ForQuestion(
                        before?.CategoryId,
                        after?.CategoryId,
                        before?.TagIds ?? Array.Empty<long>(),
                        after?.TagIds ?? Array.Empty<long>()),

                AuditEntityType.Tag =>
                    AuditDetailsFactory.ForTag(
                        before?.Name,
                        before?.Color,
                        after?.Name,
                        after?.Color),

                AuditEntityType.Category or
                AuditEntityType.Game =>
                    AuditDetailsFactory.ForCategory(
                        before?.Name,
                        after?.Name),

                _ => throw new ArgumentOutOfRangeException(
                    nameof(entity))
            };

            await AuditSqlWriter.WriteAsync(
                db,
                tx,
                actorProvider.GetCurrent(),
                entity.ToString(),
                id,
                operation.ToString(), ct,
                detailsJson);
        }

        public async Task RecordChangeAsync(SqliteConnection db, IDbTransaction tx,
            AuditEntityType entity, long id, AuditOperation operation,
            AuditSnapshot? before, CancellationToken ct)
        {
            // L'état après une suppression est nécessairement absent.
            AuditSnapshot? after =
                operation == AuditOperation.Delete
                    ? null
                    : await CaptureAsync(db, tx, entity, id, ct);
            await RecordAsync(db, tx, entity, id, operation, before, after, ct);
        }
    }
}
