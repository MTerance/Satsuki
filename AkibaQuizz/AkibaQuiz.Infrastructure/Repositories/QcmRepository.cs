using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Infrastructure.Database;
using AkibaQuiz.Contracts.Entities;
using AkibaQuiz.Contracts.Requests;
using Dapper;
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using System.Linq;
using System.Text;

namespace AkibaQuiz.Infrastructure.Repositories
{
    public sealed class QcmRepository(SqliteConnectionFactory factory) : IQcmRepository
    {
        public async Task<long> CreateAsync(SaveQcmRequest request, string author, CancellationToken ct = default)
        {
            await using var db = await factory.OpenAsync(ct);
            await using var tx = await db.BeginTransactionAsync(ct);

            var now = DateTimeOffset.UtcNow.ToString("O");

            var id = await db.ExecuteScalarAsync<long>(
                new CommandDefinition(
                    """
                INSERT INTO QCMQuestion
                    (Question, CreationDate, LastUpdatedTDate,
                     Author, IdCategory)
                VALUES
                    (@Question, @Now, @Now, @Author, @IdCategory)
                RETURNING Id;
                """,
                    new
                    {
                        Question = request.Question.Trim(),
                        Now = now,
                        Author = author,
                        request.IdCategory
                    },
                    tx,
                    cancellationToken: ct));

            foreach (var answer in request.Answers)
            {
                var answerId = await db.ExecuteScalarAsync<long>(
                    new CommandDefinition(
                        """
                    INSERT INTO QCMAnswer (Answer)
                    VALUES (@Answer)
                    RETURNING Id;
                    """,
                        new { Answer = answer.Answer.Trim() },
                        tx,
                        cancellationToken: ct));

                await db.ExecuteAsync(
                    new CommandDefinition(
                        """
                    INSERT INTO QCMQuizz
                        (IdQCMQuestion, IdQCMAnswer, IsTrue)
                    VALUES (@QcmId, @AnswerId, @IsTrue);
                    """,
                        new
                        {
                            QcmId = id,
                            AnswerId = answerId,
                            IsTrue = answer.IsTrue ? "TRUE" : "FALSE"
                        },
                        tx,
                        cancellationToken: ct));
            }

            foreach (var tagId in request.TagIds.Distinct())
            {
                await db.ExecuteAsync(new CommandDefinition(
                    """
                INSERT INTO TagQuizz (IdTag, IdQCM)
                VALUES (@tagId, @id);
                """,
                    new { tagId, id }, tx, cancellationToken: ct));
            }

            foreach (var media in request.Medias)
            {
                await db.ExecuteAsync(new CommandDefinition(
                    """
                INSERT INTO MediaQuizz
                    (IdQCMQuestion, IdMedia, TypeDisplay)
                VALUES (@id, @IdMedia, @TypeDisplay);
                """,
                    new
                    {
                        id,
                        media.IdMedia,
                        media.TypeDisplay
                    }, tx, cancellationToken: ct));
            }

            await tx.CommitAsync(ct);
            return id;
        }

        public async Task<bool> DeleteAsync(long id, CancellationToken ct = default)
        {
            await using var db = await factory.OpenAsync(ct);
            await using var tx = await db.BeginTransactionAsync(ct);

            var exists = await db.ExecuteScalarAsync<long>(
                new CommandDefinition(
                    "SELECT COUNT(*) FROM QCMQuestion WHERE Id = @id;",
                    new { id }, tx, cancellationToken: ct));

            if (exists == 0)
                return false;

            var answerIds = (await db.QueryAsync<long>(
                new CommandDefinition(
                    """
                SELECT IdQCMAnswer FROM QCMQuizz
                WHERE IdQCMQuestion = @id;
                """,
                    new { id }, tx, cancellationToken: ct))).ToList();

            await db.ExecuteAsync(new CommandDefinition(
                "DELETE FROM QCMQuizz WHERE IdQCMQuestion = @id;",
                new { id }, tx, cancellationToken: ct));

            await db.ExecuteAsync(new CommandDefinition(
                "DELETE FROM TagQuizz WHERE IdQCM = @id;",
                new { id }, tx, cancellationToken: ct));

            await db.ExecuteAsync(new CommandDefinition(
                "DELETE FROM MediaQuizz WHERE IdQCMQuestion = @id;",
                new { id }, tx, cancellationToken: ct));

            // Si le QCM est utilisé dans RoundQuestions,
            // la clé étrangère empêche sa suppression.
            await db.ExecuteAsync(new CommandDefinition(
                "DELETE FROM QCMQuestion WHERE Id = @id;",
                new { id }, tx, cancellationToken: ct));

            foreach (var answerId in answerIds.Distinct())
            {
                await db.ExecuteAsync(new CommandDefinition(
                    """
                DELETE FROM QCMAnswer
                WHERE Id = @answerId
                  AND NOT EXISTS (
                    SELECT 1 FROM QCMQuizz
                    WHERE IdQCMAnswer = @answerId
                  );
                """,
                    new { answerId }, tx, cancellationToken: ct));
            }

            await tx.CommitAsync(ct);
            return true;
        }

        public async Task<IReadOnlyList<QcmQuestionEntity>> GetAllAsync(CancellationToken ct = default)
        {
            await using var db = await factory.OpenAsync(ct);

            var rows = await db.QueryAsync<QcmQuestionEntity>(
                new CommandDefinition(
                    "SELECT * FROM QCMQuestion ORDER BY Id;",
                    cancellationToken: ct));

            return rows.ToList();
        }

        public async Task<QcmQuestionEntity?> GetQuestionAsync(long id, CancellationToken ct = default)
        {
            await using var db = await factory.OpenAsync(ct);

            return await db.QuerySingleOrDefaultAsync<QcmQuestionEntity>(
                new CommandDefinition(
                    "SELECT * FROM QCMQuestion WHERE Id = @id;",
                    new { id },
                    cancellationToken: ct));
        }

        public async Task<IReadOnlyList<QcmAnswerRow>> GetAnswersAsync(long id, CancellationToken ct = default)
        {
            await using var db = await factory.OpenAsync(ct);

            var rows = await db.QueryAsync<QcmAnswerRow>(
                new CommandDefinition(
                    """
                SELECT
                    qq.Id,
                    qq.IdQCMAnswer,
                    a.Answer,
                    qq.IsTrue
                FROM QCMQuizz qq
                INNER JOIN QCMAnswer a
                    ON a.Id = qq.IdQCMAnswer
                WHERE qq.IdQCMQuestion = @id
                ORDER BY qq.Id;
                """,
                    new { id },
                    cancellationToken: ct));

            return rows.ToList();

        }

        public async Task<bool> UpdateAsync(long id, SaveQcmRequest request, CancellationToken ct = default)
        {
            await using var db = await factory.OpenAsync(ct);
            await using var tx = await db.BeginTransactionAsync(ct);

            var affected = await db.ExecuteAsync(
                new CommandDefinition(
                    """
                UPDATE QCMQuestion
                SET Question = @Question,
                    IdCategory = @IdCategory,
                    LastUpdatedTDate = @Now
                WHERE Id = @id;
                """,
                    new
                    {
                        id,
                        Question = request.Question.Trim(),
                        request.IdCategory,
                        Now = DateTimeOffset.UtcNow.ToString("O")
                    }, tx, cancellationToken: ct));

            if (affected == 0)
            {
                await tx.RollbackAsync(ct);
                return false;
            }

            var oldAnswerIds = (await db.QueryAsync<long>(
                new CommandDefinition(
                    """
                SELECT IdQCMAnswer FROM QCMQuizz
                WHERE IdQCMQuestion = @id;
                """,
                    new { id }, tx, cancellationToken: ct))).ToList();

            await db.ExecuteAsync(new CommandDefinition(
                "DELETE FROM QCMQuizz WHERE IdQCMQuestion = @id;",
                new { id }, tx, cancellationToken: ct));

            await db.ExecuteAsync(new CommandDefinition(
                "DELETE FROM TagQuizz WHERE IdQCM = @id;",
                new { id }, tx, cancellationToken: ct));

            await db.ExecuteAsync(new CommandDefinition(
                "DELETE FROM MediaQuizz WHERE IdQCMQuestion = @id;",
                new { id }, tx, cancellationToken: ct));

            foreach (var answer in request.Answers)
            {
                var answerId = await db.ExecuteScalarAsync<long>(
                    new CommandDefinition(
                        """
                    INSERT INTO QCMAnswer (Answer)
                    VALUES (@Answer) RETURNING Id;
                    """,
                        new { Answer = answer.Answer.Trim() },
                        tx, cancellationToken: ct));

                await db.ExecuteAsync(new CommandDefinition(
                    """
                INSERT INTO QCMQuizz
                    (IdQCMQuestion, IdQCMAnswer, IsTrue)
                VALUES (@id, @answerId, @isTrue);
                """,
                    new
                    {
                        id,
                        answerId,
                        isTrue = answer.IsTrue ? "TRUE" : "FALSE"
                    }, tx, cancellationToken: ct));
            }

            foreach (var tagId in request.TagIds.Distinct())
            {
                await db.ExecuteAsync(new CommandDefinition(
                    "INSERT INTO TagQuizz (IdTag, IdQCM) VALUES (@tagId, @id);",
                    new { tagId, id }, tx, cancellationToken: ct));
            }

            foreach (var media in request.Medias)
            {
                await db.ExecuteAsync(new CommandDefinition(
                    """
                INSERT INTO MediaQuizz
                    (IdQCMQuestion, IdMedia, TypeDisplay)
                VALUES (@id, @IdMedia, @TypeDisplay);
                """,
                    new { id, media.IdMedia, media.TypeDisplay },
                    tx, cancellationToken: ct));
            }

            foreach (var oldId in oldAnswerIds.Distinct())
            {
                await db.ExecuteAsync(new CommandDefinition(
                    """
                DELETE FROM QCMAnswer
                WHERE Id = @oldId
                  AND NOT EXISTS (
                    SELECT 1 FROM QCMQuizz
                    WHERE IdQCMAnswer = @oldId
                  );
                """,
                    new { oldId }, tx, cancellationToken: ct));
            }

            await tx.CommitAsync(ct);
            return true;
        }
    }
}
