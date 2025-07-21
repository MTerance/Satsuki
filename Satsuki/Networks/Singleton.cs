using Godot;
using System;
using System.Net;
using System.Net.Sockets;

public interface INetwork
{
	bool Start();
	bool Stop();
}

public abstract class SingletonBase<T>
	where T : SingletonBase<T>, new()
{
    static private T _instance = null;

    static public T GetInstance
    {
        get 
        {  
            if (_instance == null)
                _instance = new T();
            return _instance; 
        }   
    }
}

public class Network : SingletonBase<Network>, INetwork, IDisposable
{
    private TcpListener _server;
    private TcpClient _client;
    private NetworkStream _stream;

    public Network()
    {
        _server = null;
        _client = null;
        _stream = null;
    }

    public void Dispose()
    {
        _stream?.Close();
        _stream?.Dispose();

        _server?.Stop();
        _server?.Dispose();
    }

    public bool Stop()
    {
        if (_stream != null)
        {
            _stream.Close();
            _stream.Dispose();
            _stream = null;
        }
        if (_client != null)
        {
            _client.Close();
            _client.Dispose();
            _client = null;
        }
        if (_server != null)
        {
            _server.Stop();
            _server = null;
        }
        return true;
    }

    public bool Start()
    {
        _server = new TcpListener(IPAddress.Parse("127.0.0.1"), 80);
        _server.Start();
        Console.WriteLine("Server has started on {0}:{1}, Waiting for a connection…", "127.0.0.1", 80);

        _client = _server.AcceptTcpClient();
        Console.WriteLine("A client connected.");

        _stream = _client.GetStream();

        return true;
    }
}
