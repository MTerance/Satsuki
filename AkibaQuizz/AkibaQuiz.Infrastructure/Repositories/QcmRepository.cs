using AkibaQuiz.Infrastructure;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;
using AkibaQuiz.Infrastructure.Database;
using Dapper;
using Microsoft.Data.Sqlite;

namespace AkibaQuiz.Infrastructure.Repositories;

public sealed class QcmRepository(SqliteConnectionFactory factory) : IQcmRepository
{
    private sealed class QcmRow
    {
        public long Id { get; set; }
        public string Question { get; set; } = "";
        public long IdCategory { get; set; }
        public string CategoryName { get; set; } = "";
        public string Author { get; set; } = "";
        public string CreationDate { get; set; } = "";
        public string LastUpdatedTDate { get; set; } = "";
    }

    private sealed class AnswerRow
    {
        public long Id { get; set; }
        public long IdQCMAnswer { get; set; }
        public string Answer { get; set; } = "";
        public string IsTrue { get; set; } = "FALSE";
    }

    public async Task<IReadOnlyList<QcmModel>> GetAllAsync(CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);
        var ids = await db.QueryAsync<long>(new CommandDefinition(
            "SELECT Id FROM QCMQuestion ORDER BY Id", cancellationToken: ct));
        var result = new List<QcmModel>();
        foreach (var id in ids)
            result.Add((await Load(db, id, ct))!);
        return result;
    }

    public async Task<QcmModel?> GetByIdAsync(long id, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);
        return await Load(db, id, ct);
    }

    private static async Task<QcmModel?> Load(SqliteConnection db, long id, CancellationToken ct)
    {
        var row = await db.QuerySingleOrDefaultAsync<QcmRow>(new CommandDefinition(
            "SELECT q.*, c.Name AS CategoryName FROM QCMQuestion q " +
            "JOIN Categories c ON c.Id=q.IdCategory WHERE q.Id=@id",
            new { id }, cancellationToken: ct));
        if (row is null) return null;

        var answers = await db.QueryAsync<AnswerRow>(new CommandDefinition(
            "SELECT l.Id,l.IdQCMAnswer,a.Answer,l.IsTrue FROM QCMQuizz l " +
            "JOIN QCMAnswer a ON a.Id=l.IdQCMAnswer " +
            "WHERE l.IdQCMQuestion=@id ORDER BY l.Id",
            new { id }, cancellationToken: ct));
        return new QcmModel
        {
            Id = row.Id, Question = row.Question, IdCategory = row.IdCategory,
            CategoryName = row.CategoryName, Author = row.Author,
            CreationDate = ParseDate(row.CreationDate),
            LastUpdatedDate = ParseDate(row.LastUpdatedTDate),
            Answers = answers.Select(a => new QcmPropositionModel
            {
                Id = a.Id, IdQCMAnswer = a.IdQCMAnswer, Answer = a.Answer,
                IsTrue = string.Equals(a.IsTrue, "TRUE", StringComparison.OrdinalIgnoreCase)
            }).ToList(),
            Tags = await SqlHelpers.Tags(db, id, true, ct),
            Medias = await SqlHelpers.Medias(db, id, true, ct)
        };
    }

    private static DateTimeOffset? ParseDate(string? date)
        => DateTimeOffset.TryParse(date, out var value) ? value : null;

    public async Task<long> SaveAsync(long? id, SaveQcmRequest value, string author, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);
        await using var tx = await db.BeginTransactionAsync(ct);
        await SqlHelpers.ValidateLinks(db, tx, value.IdCategory, value.TagIds, value.Medias, ct);
        long key;
        List<long> previous = [];
        if (id.HasValue)
        {
            key = id.Value;
            var n = await db.ExecuteAsync(new CommandDefinition(
                "UPDATE QCMQuestion SET Question=@question,IdCategory=@category,LastUpdatedTDate=@now WHERE Id=@key",
                new { question = value.Question.Trim(), category = value.IdCategory,
                    now = SqlHelpers.Now(), key }, tx, cancellationToken: ct));
            if (n == 0) throw new KeyNotFoundException("QCM introuvable");
            previous = (await db.QueryAsync<long>(new CommandDefinition(
                "SELECT IdQCMAnswer FROM QCMQuizz WHERE IdQCMQuestion=@key",
                new { key }, tx, cancellationToken: ct))).ToList();
            await db.ExecuteAsync(new CommandDefinition(
                "DELETE FROM QCMQuizz WHERE IdQCMQuestion=@key",
                new { key }, tx, cancellationToken: ct));
        }
        else
        {
            key = await db.ExecuteScalarAsync<long>(new CommandDefinition(
                "INSERT INTO QCMQuestion(Question,CreationDate,LastUpdatedTDate,Author,IdCategory) " +
                "VALUES(@question,@now,@now,@author,@category) RETURNING Id",
                new { question = value.Question.Trim(), now = SqlHelpers.Now(), author,
                    category = value.IdCategory }, tx, cancellationToken: ct));
        }
        foreach (var answer in value.Answers)
        {
            var answerId = await db.ExecuteScalarAsync<long>(new CommandDefinition(
                "INSERT INTO QCMAnswer(Answer) VALUES(@text) RETURNING Id",
                new { text = answer.Answer.Trim() }, tx, cancellationToken: ct));
            await db.ExecuteAsync(new CommandDefinition(
                "INSERT INTO QCMQuizz(IdQCMQuestion,IdQCMAnswer,IsTrue) VALUES(@key,@answerId,@truth)",
                new { key, answerId, truth = answer.IsTrue ? "TRUE" : "FALSE" }, tx, cancellationToken: ct));
        }
        await SqlHelpers.ReplaceLinks(db, tx, key, true, value.TagIds, value.Medias, ct);
        foreach (var oldId in previous.Distinct())
            await db.ExecuteAsync(new CommandDefinition(
                "DELETE FROM QCMAnswer WHERE Id=@oldId " +
                "AND NOT EXISTS(SELECT 1 FROM QCMQuizz WHERE IdQCMAnswer=@oldId)",
                new { oldId }, tx, cancellationToken: ct));
        await tx.CommitAsync(ct);
        return key;
    }

    public async Task<bool> DeleteAsync(long id, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);
        await using var tx = await db.BeginTransactionAsync(ct);
        var n = await db.ExecuteScalarAsync<long>(new CommandDefinition(
            "SELECT COUNT(*) FROM QCMQuestion WHERE Id=@id", new { id }, tx, cancellationToken: ct));
        if (n == 0) return false;
        await SqlHelpers.CheckUnused(db, tx, id, true, ct);
        var previous = (await db.QueryAsync<long>(new CommandDefinition(
            "SELECT IdQCMAnswer FROM QCMQuizz WHERE IdQCMQuestion=@id",
            new { id }, tx, cancellationToken: ct))).ToList();
        await db.ExecuteAsync(new CommandDefinition(
            "DELETE FROM QCMQuizz WHERE IdQCMQuestion=@id; " +
            "DELETE FROM TagQuizz WHERE IdQCM=@id; " +
            "DELETE FROM MediaQuizz WHERE IdQCMQuestion=@id; " +
            "DELETE FROM QCMQuestion WHERE Id=@id", new { id }, tx, cancellationToken: ct));
        foreach (var oldId in previous.Distinct())
            await db.ExecuteAsync(new CommandDefinition(
                "DELETE FROM QCMAnswer WHERE Id=@oldId " +
                "AND NOT EXISTS(SELECT 1 FROM QCMQuizz WHERE IdQCMAnswer=@oldId)",
                new { oldId }, tx, cancellationToken: ct));
        await tx.CommitAsync(ct);
        return true;
    }
}
