using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts;
using AkibaQuiz.Infrastructure.Database;
using Dapper;
using Microsoft.Data.Sqlite;
namespace AkibaQuiz.Infrastructure.Repositories;

public sealed class GameRepository(SqliteConnectionFactory factory) : IGameRepository
{
    private sealed class GameRow { public long Id { get; set; } public string Name { get; set; } = ""; public string Author { get; set; } = ""; public string? CreationDate { get; set; } }
    private sealed class RoundRow { public long Id { get; set; } public long Position { get; set; } }
    private sealed class QuestionRow { public long Id { get; set; } public long Position { get; set; } public long? IdQuestionAnswer { get; set; } public long? IdQCMQuestion { get; set; } public long? IdListQuestionsAnswers { get; set; } }
    public async Task<List<GameDto>> All(CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);
        var ids = await db.QueryAsync<long>(new CommandDefinition("SELECT Id FROM Games ORDER BY Id", cancellationToken: ct));
        var list = new List<GameDto>();
        foreach (var id in ids)
            list.Add((await Load(db, id, ct))!);
        return list;
    }
    public async Task<GameDto?> Get(long id, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);
        return await Load(db, id, ct);
    }

    private static async Task<GameDto?> Load(SqliteConnection db, long id, CancellationToken ct)
    {
        var g = await db.QuerySingleOrDefaultAsync<GameRow>(new CommandDefinition("SELECT Id,Name,Author,CreationDate FROM Games WHERE Id=@id", new { id }, cancellationToken: ct)); if (g is null) return null;
        var rounds = await db.QueryAsync<RoundRow>(new CommandDefinition("SELECT Id,Position FROM GameRounds WHERE IdGame=@id ORDER BY Position,Id", new { id }, cancellationToken: ct));
        var list = new List<RoundDto>(); foreach (var r in rounds)
        {
            var rows = await db.QueryAsync<QuestionRow>(new CommandDefinition("SELECT Id,Position,IdQuestionAnswer,IdQCMQuestion,IdListQuestionsAnswers FROM RoundQuestions WHERE IdGameRound=@rid ORDER BY Position,Id", new { rid = r.Id }, cancellationToken: ct));
            list.Add(new RoundDto(r.Id, r.Position, rows.Select(q => new RoundQuestionDto(q.Id, q.Position, q.IdQuestionAnswer, q.IdQCMQuestion, q.IdListQuestionsAnswers)).ToList()));
        }
        return new GameDto(g.Id, g.Name, g.Author, g.CreationDate, list);
    }
    private static async Task ValidateQuestions(SqliteConnection db, System.Data.IDbTransaction tx, GameWrite value, CancellationToken ct)
    {
        foreach (var r in value.Rounds) foreach (var q in r.Questions)
        {
            if (q.IdQuestionAnswer is long qa) await SqlHelpers.Require(db, tx, "QuestionsAnswers", qa, ct);
            if (q.IdQCMQuestion is long qcm) await SqlHelpers.Require(db, tx, "QCMQuestion", qcm, ct);
        }
    }
    public async Task<long> Save(long? id, GameWrite value, string author, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct); await using var tx = await db.BeginTransactionAsync(ct);
        await ValidateQuestions(db, tx, value, ct);
        long key;
        if (id.HasValue)
        {
            key = id.Value;
            var n = await db.ExecuteAsync(new CommandDefinition("UPDATE Games SET Name=@name WHERE Id=@key", new { name = value.Name.Trim(), key }, tx, cancellationToken: ct)); if (n == 0) throw new KeyNotFoundException("Game introuvable");
            await db.ExecuteAsync(new CommandDefinition("DELETE FROM RoundQuestions WHERE IdGameRound IN(SELECT Id FROM GameRounds WHERE IdGame=@key);DELETE FROM GameRounds WHERE IdGame=@key", new { key }, tx, cancellationToken: ct));
        }
        else
        {
            key = await db.ExecuteScalarAsync<long>(new CommandDefinition("INSERT INTO Games(Name,Author,CreationDate) VALUES(@name,@author,@now) RETURNING Id", new { name = value.Name.Trim(), author, now = SqlHelpers.Now() }, tx, cancellationToken: ct));
        }
        foreach (var r in value.Rounds.OrderBy(r => r.Position))
        {
            var rid = await db.ExecuteScalarAsync<long>(new CommandDefinition("INSERT INTO GameRounds(Position,IdGame) VALUES(@position,@key) RETURNING Id", new { position = r.Position, key }, tx, cancellationToken: ct));
            foreach (var q in r.Questions.OrderBy(q => q.Position)) await db.ExecuteAsync(new CommandDefinition("INSERT INTO RoundQuestions(Position,IdGameRound,IdQuestionAnswer,IdQCMQuestion,IdListQuestionsAnswers) VALUES(@position,@rid,@qa,@qcm,NULL)", new { position = q.Position, rid, qa = q.IdQuestionAnswer, qcm = q.IdQCMQuestion }, tx, cancellationToken: ct));
        }
        await tx.CommitAsync(ct); return key;
    }
    public async Task<bool> Delete(long id, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);
        await using var tx = await db.BeginTransactionAsync(ct);
        var n = await db.ExecuteScalarAsync<long>(new CommandDefinition("SELECT COUNT(*) FROM Games WHERE Id=@id", new { id }, tx, cancellationToken: ct)); if (n == 0) return false;
        await db.ExecuteAsync(new CommandDefinition("DELETE FROM RoundQuestions WHERE IdGameRound IN(SELECT Id FROM GameRounds WHERE IdGame=@id);DELETE FROM GameRounds WHERE IdGame=@id;DELETE FROM Games WHERE Id=@id", new { id }, tx, cancellationToken: ct));
        await tx.CommitAsync(ct); return true;
    }
}
