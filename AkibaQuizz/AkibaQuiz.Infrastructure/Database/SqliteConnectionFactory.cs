using Microsoft.Data.Sqlite;

namespace AkibaQuiz.Infrastructure.Database;

public sealed class SqliteConnectionFactory
{
    private readonly string connectionString;

    public SqliteConnectionFactory(string databasePath)
    {
        if (File.Exists(databasePath))
        {
           var buiilder = new SqliteConnectionStringBuilder
           {
               DataSource = databasePath,
               Mode = SqliteOpenMode.ReadWriteCreate,
               Cache = SqliteCacheMode.Shared,
               DefaultTimeout = 30,
               ForeignKeys = true,
           };
            connectionString = buiilder.ToString();
        }
        else
        {
            throw new FileNotFoundException("Database file not found.", databasePath);
        }
    }

    public async Task<SqliteConnection> OpenAsync(CancellationToken ct = default)    
    {
        var connection = new SqliteConnection(connectionString);
        await connection.OpenAsync(ct);
        return connection;
    }
}
