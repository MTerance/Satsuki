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
}
