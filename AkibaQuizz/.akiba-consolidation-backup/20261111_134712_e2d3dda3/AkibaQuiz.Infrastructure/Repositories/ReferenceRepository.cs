using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts;
using AkibaQuiz.Infrastructure.Database;
using Dapper;
namespace AkibaQuiz.Infrastructure.Repositories;
public sealed class ReferenceRepository(SqliteConnectionFactory factory):IReferenceRepository 
{
 public async Task<List<CategoryDto>> Categories(CancellationToken ct)
    {
        await using var db=await factory.OpenAsync(ct);
        return (await db.QueryAsync<CategoryDto>(new CommandDefinition("SELECT Id,Name FROM Categories ORDER BY Id",cancellationToken:ct))).ToList();
    }
 public async Task<List<TagDto>> Tags(CancellationToken ct)
    {
        await using var db=await factory.OpenAsync(ct);
        return (await db.QueryAsync<TagDto>(new CommandDefinition("SELECT Id,Name,Color FROM Tags ORDER BY Id",cancellationToken:ct))).ToList();
    }
}
