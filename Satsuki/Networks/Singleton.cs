using Godot;
using System;
using System.Net.Sockets;

public interface ISingleton 
{
	
}

public abstract  ASingleton : ISingleton 
{
	 
}

public class Network
{
	static public Network GetInstance()
	{
	 if (_instance == null)
		_instance = new Network();	
	return _instance;
	}
	
	static private Network _instance = null;
	
	private TcpListener _server;
	private TcpClient _client;
	private NetworkStream _stream;
	
	private Network()
	{
		Start();
	}
	
	public void Start()
	{
		_server = new TcpListener(IPAdress.parse("127.0.0.1"),80);
		_server.Start();
		Console.WriteLine("Server has started on {0}:{1}, Waiting for a connection…", "127.0.0.1", 80);

		_client = _server.AcceptTcpClient();
		Console.WriteLine("A client connected.");

		_stream = _client.GetStream();
	}
	
	
	
}
