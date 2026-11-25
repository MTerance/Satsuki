using AkibaQuiz.Application.Auditing;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Infrastructure.Database;
using Dapper;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace AkibaQuiz.Infrastructure.Auditing
{
    public class SqLiteAuditEventRepository : IAuditEventReader
    {
        private readonly SqliteConnectionFactory factory;
        public SqLiteAuditEventRepository(SqliteConnectionFactory factory)
        {
            this.factory = factory;
        }

        public async Task<AuditPage> SearchAsync(AuditFilter filter, CancellationToken ct)
        {
            ArgumentNullException.ThrowIfNull(filter);

            var clauses = new List<string>();
            var p = new DynamicParameters();

            if (!string.IsNullOrWhiteSpace(filter.EntityType))
            {
                clauses.Add("a.EntityType = @EntityType");
                p.Add("EntityType", filter.EntityType);
            }

            if (filter.EntityId.HasValue)
            {
                clauses.Add("a.EntityId = @EntityId");
                p.Add("EntityId", filter.EntityId.Value);
            }

            if (!string.IsNullOrWhiteSpace(filter.Action))
            {
                clauses.Add("a.Action = @Action");
                p.Add("Action", filter.Action);
            }

            if (!string.IsNullOrWhiteSpace(filter.ActorType))
            {
                clauses.Add("a.ActorType = @ActorType");
                p.Add("ActorType", filter.ActorType);
            }

            if (!string.IsNullOrWhiteSpace(filter.ActorId))
            {
                clauses.Add("a.ActorId = @ActorId");
                p.Add("ActorId", filter.ActorId.Trim());
            }

            if (!string.IsNullOrWhiteSpace(filter.CorrelationId))
            {
                clauses.Add("a.CorrelationId = @CorrelationId");
                p.Add("CorrelationId", filter.CorrelationId.Trim());
            }

            if (filter.DateFrom.HasValue)
            {
                clauses.Add("a.OccurredAtUtc >= @FromUtc");
                p.Add("FromUtc", ToUtcStart(filter.DateFrom.Value));
            }

            if (filter.DateTo.HasValue)
            {
                // Borne supérieure exclusive :
                // couvre toute la journée sélectionnée.
                clauses.Add("a.OccurredAtUtc < @ToUtcExclusive");

                p.Add(
                    "ToUtcExclusive",
                    ToUtcStart(filter.DateTo.Value.AddDays(1)));
            }

            string whereSql = clauses.Count == 0
                ? ""
                : "WHERE " + string.Join(" AND ", clauses);

            p.Add("PageSize", filter.PageSize);
            p.Add(
                "Offset",
                ((long)filter.Page - 1) * filter.PageSize);

            // Les valeurs utilisateur ne sont jamais
            // concaténées dans le SQL.
            const string selectColumns = """
            a.Id,
            a.OccurredAtUtc,
            a.EntityType,
            a.EntityId,
            a.Action,
            a.ActorType,
            a.ActorId,
            a.CorrelationId,
            a.DetailsJson
            """;

            string sql = $"""
            SELECT COUNT(*)
            FROM AuditEvents a
            {whereSql};

            SELECT
                {selectColumns}
            FROM AuditEvents a
            {whereSql}
            ORDER BY
                a.OccurredAtUtc DESC,
                a.Id DESC
            LIMIT @PageSize OFFSET @Offset;
            """;

            await using var db = await factory.OpenAsync(ct);

            using var grid = await db.QueryMultipleAsync(
                new CommandDefinition(
                    sql,
                    p,
                    cancellationToken: ct));

            long count = await grid.ReadSingleAsync<long>();

            var events = (await grid.ReadAsync<AuditEventRow>())
                .ToList();

            return new AuditPage
            {
                Items = events,
                TotalCount = count,
                Page = filter.Page,
                PageSize = filter.PageSize
            };
        }

        private static string ToUtcStart(DateOnly date)
        {
            var start = new DateTimeOffset(
                date.ToDateTime(TimeOnly.MinValue),
                TimeSpan.Zero);

            return start.ToString("O");
        }
    }
}
