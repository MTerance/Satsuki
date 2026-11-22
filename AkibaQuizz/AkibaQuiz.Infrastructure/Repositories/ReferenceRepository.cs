using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Infrastructure.Database;
using Dapper;

namespace AkibaQuiz.Infrastructure.Repositories;

public sealed class ReferenceRepository(SqliteConnectionFactory factory) : IReferenceRepository
{
    public async Task<IReadOnlyList<CategoryModel>> GetCategoriesAsync(CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);
        return (await db.QueryAsync<CategoryModel>(new CommandDefinition(
            "SELECT Id,Name FROM Categories ORDER BY Id", cancellationToken: ct))).ToList();
    }

    public async Task<IReadOnlyList<TagModel>> GetTagsAsync(CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);
        return (await db.QueryAsync<TagModel>(new CommandDefinition(
            "SELECT Id,Name,Color FROM Tags ORDER BY Id", cancellationToken: ct))).ToList();
    }

    public async Task<long?> CreateCategoryAsync(
    string name, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);

        return await db.ExecuteScalarAsync<long?>(
            new CommandDefinition(
                """
            INSERT INTO Categories (Name)
            SELECT @Name
            WHERE NOT EXISTS (
                SELECT 1 FROM Categories
                WHERE Name = @Name COLLATE NOCASE
            )
            RETURNING Id;
            """,
                new { Name = name },
                cancellationToken: ct));
    }

    public async Task<bool> RenameCategoryAsync(
        long id, string name, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);

        var affected = await db.ExecuteAsync(
            new CommandDefinition(
                """
            UPDATE Categories
            SET Name = @Name
            WHERE Id = @Id
              AND NOT EXISTS (
                  SELECT 1 FROM Categories
                  WHERE Name = @Name COLLATE NOCASE
                    AND Id <> @Id
              );
            """,
                new { Id = id, Name = name },
                cancellationToken: ct));

        return affected == 1;
    }

    public async Task<bool> DeleteCategoryAsync(
        long id, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);

        var affected = await db.ExecuteAsync(
            new CommandDefinition(
                """
            DELETE FROM Categories
            WHERE Id = @Id
              AND NOT EXISTS (
                  SELECT 1 FROM QuestionsAnswers
                  WHERE IdCategory = @Id
              )
              AND NOT EXISTS (
                  SELECT 1 FROM QCMQuestion
                  WHERE IdCategory = @Id
              );
            """,
                new { Id = id },
                cancellationToken: ct));

        return affected == 1;
    }

    public async Task<long?> CreateTagAsync(
        string name, string? color, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);

        return await db.ExecuteScalarAsync<long?>(
            new CommandDefinition(
                """
            INSERT INTO Tags (Name, Color)
            SELECT @Name, @Color
            WHERE NOT EXISTS (
                SELECT 1 FROM Tags
                WHERE Name = @Name COLLATE NOCASE
            )
            RETURNING Id;
            """,
                new { Name = name, Color = color },
                cancellationToken: ct));
    }

    public async Task<bool> UpdateTagAsync(
        long id, string name, string? color,
        CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);

        var affected = await db.ExecuteAsync(
            new CommandDefinition(
                """
            UPDATE Tags
            SET Name = @Name,
                Color = @Color
            WHERE Id = @Id
              AND NOT EXISTS (
                  SELECT 1 FROM Tags
                  WHERE Name = @Name COLLATE NOCASE
                    AND Id <> @Id
              );
            """,
                new
                {
                    Id = id,
                    Name = name,
                    Color = color
                },
                cancellationToken: ct));

        return affected == 1;
    }

    public async Task<bool> DeleteTagAsync(
        long id, CancellationToken ct)
    {
        await using var db = await factory.OpenAsync(ct);

        var affected = await db.ExecuteAsync(
            new CommandDefinition(
                """
            DELETE FROM Tags
            WHERE Id = @Id
              AND NOT EXISTS (
                  SELECT 1 FROM TagQuizz
                  WHERE IdTag = @Id
              );
            """,
                new { Id = id },
                cancellationToken: ct));

        return affected == 1;
    }
}
