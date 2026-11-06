using Microsoft.Data.Sqlite;

namespace AkibaQuiz.Infrastructure.Database;

public sealed class SqliteConnectionFactory(string connectionString)
{
    public async Task<SqliteConnection> OpenAsync(CancellationToken ct = default)    
    {
        var connection = new SqliteConnection(connectionString);

        await connection.OpenAsync(ct);

        await using var command = connection.CreateCommand();
        command.CommandText = """
            PRAGMA foreign_keys = ON;
            PRAGMA busy_timeout = 5000;
            PRAGMA journal_mode = WAL;
            """;
        await command.ExecuteNonQueryAsync(ct);
        return connection;
    }
}
