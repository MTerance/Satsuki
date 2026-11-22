
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;
using AkibaQuiz.Infrastructure.Database;
using Dapper;
using Microsoft.Extensions.Logging;

namespace AkibaQuiz.Infrastructure.Repositories;

public sealed class QuestionCatalogRepository(
    SqliteConnectionFactory factory,
    ILogger<QuestionCatalogRepository> logger)
    : IQuestionCatalogRepository
{
    public async Task<QuestionCatalogPage> SearchAsync(
        QuestionCatalogQuery query,
        CancellationToken ct)
    {
        // Défense supplémentaire : normalement le service
        // applicatif a déjà validé ces paramètres.
        if (query.Kind is not
            ("All" or "QuestionAnswer" or "QCM"))
        {
            throw new ArgumentException(
                "Type de question invalide.",
                nameof(query));
        }

        if (query.Page < 1 ||
            query.PageSize is < 1 or > 100)
        {
            throw new ArgumentOutOfRangeException(
                nameof(query),
                "Pagination invalide.");
        }

        string? textPattern = string.IsNullOrWhiteSpace(query.Text)
            ? null
            : "%" + EscapeLike(query.Text.Trim()) + "%";

        bool hasText = textPattern is not null;
        bool hasCategory = query.CategoryId.HasValue;
        bool hasTag = query.TagId.HasValue;

        // Les fragments proviennent exclusivement du code,
        // jamais directement de chaînes saisies par l'utilisateur.
        string qaWhere = BuildWhere(
            "qa",
            "IdQuestionAnswer",
            hasText,
            hasCategory,
            hasTag);

        string qcmWhere = BuildWhere(
            "qcm",
            "IdQCM",
            hasText,
            hasCategory,
            hasTag);

        var selectParts = new List<string>();
        var countParts = new List<string>();

        // ==========================================
        // 1. QUESTIONANSWERS
        // ==========================================

        if (query.Kind is "All" or "QuestionAnswer")
        {
            countParts.Add($"""
                (SELECT COUNT(*)
                 FROM QuestionsAnswers qa
                 {qaWhere})
                """);

            selectParts.Add($"""
                SELECT
                    qa.Id,
                    'QuestionAnswer' AS Type,
                    qa.Question,
                    qa.IdCategory,
                    c.Name AS CategoryName
                FROM QuestionsAnswers qa
                INNER JOIN Categories c
                    ON c.Id = qa.IdCategory
                {qaWhere}
                """);
        }

        // ==========================================
        // 2. QCM
        // ==========================================

        if (query.Kind is "All" or "QCM")
        {
            countParts.Add($"""
                (SELECT COUNT(*)
                 FROM QCMQuestion qcm
                 {qcmWhere})
                """);

            selectParts.Add($"""
                SELECT
                    qcm.Id,
                    'QCM' AS Type,
                    qcm.Question,
                    qcm.IdCategory,
                    c.Name AS CategoryName
                FROM QCMQuestion qcm
                INNER JOIN Categories c
                    ON c.Id = qcm.IdCategory
                {qcmWhere}
                """);
        }

        // ==========================================
        // 3. REQUÊTE DE COMPTAGE
        // ==========================================

        string countSql =
            "SELECT " + string.Join(" + ", countParts) + ";";

        // ==========================================
        // 4. REQUÊTE PAGINÉE
        // ==========================================

        string candidatesSql = string.Join(
            "\nUNION ALL\n",
            selectParts);

        string pageSql = $"""
            SELECT
                catalog.Id,
                catalog.Type,
                catalog.Question,
                catalog.IdCategory,
                catalog.CategoryName,

                CASE
                    WHEN catalog.Type = 'QCM' THEN (
                        SELECT COUNT(*)
                        FROM QCMQuizz a
                        WHERE a.IdQCMQuestion = catalog.Id
                    )
                    ELSE 0
                END AS AnswerCount

            FROM (
                {candidatesSql}
            ) AS catalog

            ORDER BY
                catalog.Id DESC,
                catalog.Type ASC

            LIMIT @PageSize
            OFFSET @Offset;
            """;

        var parameters = new
        {
            query.CategoryId,
            query.TagId,
            TextPattern = textPattern,
            query.PageSize,
            Offset = ((long)query.Page - 1) * query.PageSize
        };

        // ==========================================
        // 5. EXÉCUTION AVEC MÉTRIQUES
        // ==========================================

        await using var db = await factory.OpenAsync(ct);

        var sw = Stopwatch.StartNew();

        long count = await db.ExecuteScalarAsync<long>(
            new CommandDefinition(
                countSql,
                parameters,
                cancellationToken: ct));

        sw.Stop();
        double countMs = sw.Elapsed.TotalMilliseconds;

        sw.Restart();

        var items = (await db.QueryAsync<QuestionCatalogItem>(
            new CommandDefinition(
                pageSql,
                parameters,
                cancellationToken: ct)))
            .ToList();

        sw.Stop();
        double pageMs = sw.Elapsed.TotalMilliseconds;

        logger.LogInformation(
            "CATALOG PERF Kind={Kind} Category={Category} " +
            "Tag={Tag} HasText={HasText} Total={Total} " +
            "CountMs={CountMs:F2} PageMs={PageMs:F2}",
            query.Kind,
            query.CategoryId,
            query.TagId,
            hasText,
            count,
            countMs,
            pageMs);

        return new QuestionCatalogPage
        {
            Items = items,
            TotalCount = count,
            Page = query.Page,
            PageSize = query.PageSize
        };
    }

    // ==========================================
    // CONSTRUCTION DES FILTRES
    // ==========================================

    private static string BuildWhere(
        string alias,
        string tagColumn,
        bool hasText,
        bool hasCategory,
        bool hasTag)
    {
        var clauses = new List<string>();

        if (hasCategory)
        {
            clauses.Add(
                $"{alias}.IdCategory = @CategoryId");
        }

        if (hasText)
        {
            clauses.Add(
                $@"{alias}.Question LIKE @TextPattern ESCAPE '\'");
        }

        if (hasTag)
        {
            clauses.Add($"""
                {alias}.Id IN (
                    SELECT tq.{tagColumn}
                    FROM TagQuizz tq
                    WHERE tq.IdTag = @TagId
                      AND tq.{tagColumn} IS NOT NULL
                )
                """);
        }

        return clauses.Count == 0
            ? ""
            : "WHERE " + string.Join(
                "\nAND ",
                clauses);
    }


    public async Task<IReadOnlyList<QuestionLabelModel>>
        GetLabelsByIdsAsync(
            IEnumerable<long> questionIds,
            IEnumerable<long> qcmIds,
            CancellationToken ct)
    {

        var qaIds = questionIds
            .Where(id => id > 0)
            .Distinct()
            .ToArray();

        var qcmIdsArray = qcmIds
            .Where(id => id > 0)
            .Distinct()
            .ToArray();

        if (qaIds.Length == 0 && qcmIdsArray.Length == 0)
            return [];

        var result = new List<QuestionLabelModel>();

        await using var db = await factory.OpenAsync(ct);

        if (qaIds.Length > 0)
        {
            const string sql = """
            SELECT
                Id,
                'QuestionAnswer' AS Type,
                Question
            FROM QuestionsAnswers
            WHERE Id IN @Ids;
            """;

            var rows = await db.QueryAsync<QuestionLabelModel>(
                new CommandDefinition(
                    sql,
                    new { Ids = qaIds },
                    cancellationToken: ct));

            result.AddRange(rows);
        }

        if (qcmIdsArray.Length > 0)
        {
            const string sql = """
            SELECT
                Id,
                'QCM' AS Type,
                Question
            FROM QCMQuestion
            WHERE Id IN @Ids;
            """;

            var rows = await db.QueryAsync<QuestionLabelModel>(
                new CommandDefinition(
                    sql,
                    new { Ids = qcmIdsArray },
                    cancellationToken: ct));

            result.AddRange(rows);
        }

        return result;
    }


    // ==========================================
    // RECHERCHE LITTÉRALE SQL LIKE
    // ==========================================

    private static string EscapeLike(string value)
    {
        return value
            .Replace(@"\", @"\\")
            .Replace("%", @"\%")
            .Replace("_", @"\_");
    }
}
