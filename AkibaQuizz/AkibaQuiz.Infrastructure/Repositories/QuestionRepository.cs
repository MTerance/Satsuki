using AkibaQuiz.Infrastructure;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Infrastructure.Auditing;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;
using AkibaQuiz.Infrastructure.Database;
using Dapper;
using Microsoft.Data.Sqlite;

namespace AkibaQuiz.Infrastructure.Repositories;

public sealed class QuestionRepository(SqliteConnectionFactory factory, AuditTrail auditTrail) : IQuestionRepository
{
    private sealed class QuestionRow
    {
        public long Id { get; set; }
        public string Question { get; set; } = "";
        public string Answer { get; set; } = "";
        public long IdCategory { get; set; }
        public string CategoryName { get; set; } = "";
        public string Author { get; set; } = "";
        public string CreationDate { get; set; } = "";
        public string LastUpdateDate { get; set; } = "";
    }

    public async Task<IReadOnlyList<QuestionAnswerModel>> GetAllAsync(CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);
        var ids = await db.QueryAsync<long>(new CommandDefinition(
            "SELECT Id FROM QuestionsAnswers ORDER BY Id", cancellationToken: ct));
        var list = new List<QuestionAnswerModel>();
        foreach (var id in ids)
            list.Add((await Load(db, id, ct))!);
        return list;
    }

    public async Task<QuestionAnswerModel?> GetByIdAsync(long id, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);
        return await Load(db, id, ct);
    }

    private static async Task<QuestionAnswerModel?> Load(SqliteConnection db, long id, CancellationToken ct)
    {
        var row = await db.QuerySingleOrDefaultAsync<QuestionRow>(new CommandDefinition(
            "SELECT q.*, c.Name AS CategoryName FROM QuestionsAnswers q " +
            "JOIN Categories c ON c.Id=q.IdCategory WHERE q.Id=@id",
            new { id }, cancellationToken: ct));
        if (row is null) return null;
        return new QuestionAnswerModel
        {
            Id = row.Id,
            Question = row.Question,
            Answer = row.Answer,
            IdCategory = row.IdCategory,
            CategoryName = row.CategoryName,
            Author = row.Author,
            CreationDate = row.CreationDate,
            LastUpdateDate = row.LastUpdateDate,
            Tags = await SqlHelpers.Tags(db, id, false, ct),
            Medias = await SqlHelpers.Medias(db, id, false, ct)
        };
    }

    public async Task<long> SaveAsync(long? id, SaveQuestionAnswerRequest value, string author, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);
        await using var tx = await db.BeginTransactionAsync(ct);

        long? oldCategoryId = null;
        long[] oldTagIds = [];

        var before = await auditTrail.CaptureAsync(db, tx, AuditEntityType.QuestionAnswer, id, ct);
        if (id.HasValue && before is null)
        {
            throw new KeyNotFoundException("Question introuvable");
        }

        await SqlHelpers.ValidateLinks(db, tx, value.IdCategory, value.TagIds, value.Medias, ct);
        long key;
        if (id.HasValue)
        {
            oldCategoryId =
        await db.QuerySingleOrDefaultAsync<long?>(
            new CommandDefinition(
                """
                SELECT IdCategory
                FROM QuestionsAnswers
                WHERE Id = @id;
                """,
                new { id = id.Value },
                tx,
                cancellationToken: ct));

            oldTagIds = (await db.QueryAsync<long>(
                new CommandDefinition(
                    """
            SELECT DISTINCT IdTag
            FROM TagQuizz
            WHERE IdQuestionAnswer = @id;
            """,
                    new { id = id.Value },
                    tx,
                    cancellationToken: ct)))
                .ToArray();


            key = id.Value;
            var n = await db.ExecuteAsync(new CommandDefinition(
                "UPDATE QuestionsAnswers SET Question=@Question,Answer=@Answer,IdCategory=@IdCategory,LastUpdateDate=@now WHERE Id=@key",
                new
                {
                    Question = value.Question.Trim(),
                    Answer = value.Answer.Trim(),
                    value.IdCategory,
                    now = SqlHelpers.Now(),
                    key
                }, tx, cancellationToken: ct));
            if (n == 0) throw new KeyNotFoundException("Question introuvable");
        }
        else
        {
            key = await db.ExecuteScalarAsync<long>(new CommandDefinition(
                "INSERT INTO QuestionsAnswers(Question,Answer,IdCategory,CreationDate,LastUpdateDate,Author) " +
                "VALUES(@Question,@Answer,@IdCategory,@now,@now,@author) RETURNING Id",
                new
                {
                    Question = value.Question.Trim(),
                    Answer = value.Answer.Trim(),
                    value.IdCategory,
                    now = SqlHelpers.Now(),
                    author
                }, tx, cancellationToken: ct));
        }
        await SqlHelpers.ReplaceLinks(db, tx, key, false, value.TagIds, value.Medias, ct);
        var auditDetails = AuditDetailsFactory.ForQuestion(
            oldCategoryId,
            value.IdCategory,
            oldTagIds,
            value.TagIds);

        var after = await auditTrail.CaptureAsync(
            db,
            tx,
            AuditEntityType.QuestionAnswer,
            key,
            ct);

        await auditTrail.RecordAsync(
            db,
            tx,
            AuditEntityType.QuestionAnswer,
            key,
            id.HasValue
                ? AuditOperation.Update
                : AuditOperation.Create,
            before,
            after,
            ct);

        await tx.CommitAsync(ct);
        return key;
    }

    public async Task<bool> DeleteAsync(long id, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);
        await using var tx = await db.BeginTransactionAsync(ct);
        var before = await auditTrail.CaptureAsync(db, tx, AuditEntityType.QuestionAnswer, id, ct);

        if (before is null)
            return false;

        await SqlHelpers.CheckUnused(db, tx, id, false, ct);

        long? oldCategoryId = null;
        long[] oldTagIds = [];

        oldCategoryId =
    await db.QuerySingleOrDefaultAsync<long?>(
        new CommandDefinition(
            """
                SELECT IdCategory
                FROM QuestionsAnswers
                WHERE Id = @id;
                """,
            new { id = id },
            tx,
            cancellationToken: ct));

        oldTagIds = (await db.QueryAsync<long>(
            new CommandDefinition(
                """
            SELECT DISTINCT IdTag
            FROM TagQuizz
            WHERE IdQuestionAnswer = @id;
            """,
                new { id = id },
                tx,
                cancellationToken: ct)))
            .ToArray();


        await db.ExecuteAsync(new CommandDefinition(
            "DELETE FROM TagQuizz WHERE IdQuestionAnswer=@id; " +
            "DELETE FROM MediaQuizz WHERE IdQuestionAnswer=@id; " +
            "DELETE FROM QuestionsAnswers WHERE Id=@id", new { id }, tx, cancellationToken: ct));

        await auditTrail.RecordAsync(db, tx, AuditEntityType.QuestionAnswer, id, AuditOperation.Delete, before, null, ct);


        await tx.CommitAsync(ct);
        return true;
    }
}
