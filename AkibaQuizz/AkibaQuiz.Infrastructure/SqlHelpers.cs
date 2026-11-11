using AkibaQuiz.Contracts;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;
using Dapper;
using Microsoft.Data.Sqlite;
using System.Data;

namespace AkibaQuiz.Infrastructure;

// Helpers SQL internes à l'Infrastructure ; aucun DTO HTTP.
internal static class SqlHelpers
{
    public static string Now() => DateTimeOffset.UtcNow.ToString("O");

    public static async Task Require(SqliteConnection db, IDbTransaction tx, string table, long id, CancellationToken ct)
    {
        if (id <= 0) throw new ApiValidationException($"Identifiant incorrect : {table}/{id}");
        string[] allowed = ["Categories", "Tags", "Medias", "QuestionsAnswers", "QCMQuestion"];
        if (!allowed.Contains(table)) throw new InvalidOperationException("Table non autorisée");
        var n = await db.ExecuteScalarAsync<long>(new CommandDefinition(
            $"SELECT COUNT(*) FROM {table} WHERE Id=@id", new { id }, tx, cancellationToken: ct));
        if (n == 0) throw new ApiValidationException($"Référence inexistante : {table}/{id}");
    }

    public static async Task ValidateLinks(
        SqliteConnection db, IDbTransaction tx, long category,
        IEnumerable<long> tags, IEnumerable<SaveMediaAssociationRequest> medias, CancellationToken ct)
    {
        await Require(db, tx, "Categories", category, ct);
        foreach (var tag in tags.Distinct())
            await Require(db, tx, "Tags", tag, ct);
        foreach (var media in medias)
        {
            await Require(db, tx, "Medias", media.IdMedia, ct);
            if (string.IsNullOrWhiteSpace(media.TypeDisplay))
                throw new ApiValidationException("TypeDisplay obligatoire.");
        }
    }

    public static async Task ReplaceLinks(
        SqliteConnection db, IDbTransaction tx, long id, bool qcm,
        IEnumerable<long> tags, IEnumerable<SaveMediaAssociationRequest> medias, CancellationToken ct)
    {
        string tagField = qcm ? "IdQCM" : "IdQuestionAnswer";
        string mediaField = qcm ? "IdQCMQuestion" : "IdQuestionAnswer";
        await db.ExecuteAsync(new CommandDefinition(
            $"DELETE FROM TagQuizz WHERE {tagField}=@id", new { id }, tx, cancellationToken: ct));
        await db.ExecuteAsync(new CommandDefinition(
            $"DELETE FROM MediaQuizz WHERE {mediaField}=@id", new { id }, tx, cancellationToken: ct));
        foreach (var tag in tags.Distinct())
            await db.ExecuteAsync(new CommandDefinition(
                $"INSERT INTO TagQuizz(IdTag,{tagField}) VALUES(@tag,@id)",
                new { tag, id }, tx, cancellationToken: ct));
        foreach (var media in medias)
            await db.ExecuteAsync(new CommandDefinition(
                $"INSERT INTO MediaQuizz(IdMedia,{mediaField},TypeDisplay) VALUES(@IdMedia,@id,@TypeDisplay)",
                new { media.IdMedia, id, media.TypeDisplay }, tx, cancellationToken: ct));
    }

    public static async Task<List<TagModel>> Tags(SqliteConnection db, long id, bool qcm, CancellationToken ct)
    {
        string field = qcm ? "IdQCM" : "IdQuestionAnswer";
        var result = await db.QueryAsync<TagModel>(new CommandDefinition(
            $"SELECT t.Id,t.Name,t.Color FROM Tags t JOIN TagQuizz l ON l.IdTag=t.Id WHERE l.{field}=@id ORDER BY t.Id",
            new { id }, cancellationToken: ct));
        return result.ToList();
    }

    public static async Task<List<QuizMediaModel>> Medias(SqliteConnection db, long id, bool qcm, CancellationToken ct)
    {
        string field = qcm ? "IdQCMQuestion" : "IdQuestionAnswer";
        var result = await db.QueryAsync<QuizMediaModel>(new CommandDefinition(
            $"SELECT l.Id,l.IdMedia,m.Filename,m.IdTypeMedia,tm.Name AS TypeMediaName,l.TypeDisplay " +
            $"FROM MediaQuizz l JOIN Medias m ON m.Id=l.IdMedia JOIN TypeMedia tm ON tm.Id=m.IdTypeMedia " +
            $"WHERE l.{field}=@id ORDER BY l.Id", new { id }, cancellationToken: ct));
        return result.ToList();
    }

    public static async Task CheckUnused(SqliteConnection db, IDbTransaction tx, long id, bool qcm, CancellationToken ct)
    {
        string field = qcm ? "IdQCMQuestion" : "IdQuestionAnswer";
        var n = await db.ExecuteScalarAsync<long>(new CommandDefinition(
            $"SELECT COUNT(*) FROM RoundQuestions WHERE {field}=@id", new { id }, tx, cancellationToken: ct));
        if (n > 0) throw new ApiConflictException("Cette question est utilisée dans une manche.");
    }
}
