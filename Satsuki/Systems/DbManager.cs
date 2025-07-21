using Godot;
using System;
using Microsoft.Data.Sqlite;
using System.IO;

public interface IDbManager : IDisposable
{
    void OpenConnection();
    void CloseConnection();
    SqliteConnection GetConnection();
}

public class SqliteDbManager : IDbManager
{
    private SqliteConnection _connection;
    private readonly string _dbPath;
    private bool _disposed = false;

    public SqliteDbManager()
    {
        var dbDirectory = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "database");
        if (!Directory.Exists(dbDirectory))
            Directory.CreateDirectory(dbDirectory);
        _dbPath = Path.Combine(dbDirectory, "SatsukiDB.sqlite");
        _connection = new SqliteConnection($"Data Source={_dbPath}");
    }

    public void OpenConnection()
    {
        if (_connection.State != System.Data.ConnectionState.Open)
            _connection.Open();
    }

    public void CloseConnection()
    {
        if (_connection.State != System.Data.ConnectionState.Closed)
            _connection.Close();
    }

    public SqliteConnection GetConnection()
    {
        return _connection;
    }

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

    protected virtual void Dispose(bool disposing)
    {
        if (!_disposed)
        {
            if (disposing)
            {
                if (_connection != null)
                {
                    _connection.Dispose();
                    _connection = null;
                }
            }
            _disposed = true;
        }
    }
}
