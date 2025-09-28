using Godot;
using Satsuki.Networks;
using Satsuki.Utils;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;


public class WebSocketClient
{
    public string Id { get; set; }
    public WebSocket WebSocket { get; set; }
    public string ClientType { get; set; }
    public DateTime ConnectedAt { get; set; }
    public CancellationTokenSource CancellationToken { get; set; }

    public WebSocketClient(WebSocket webSocket)
    {
        Id = Guid.NewGuid().ToString();
        WebSocket = webSocket;
        ConnectedAt = DateTime.UtcNow;
        CancellationToken = new CancellationTokenSource();
    }
}


public class Network : SingletonBase<Network>, INetwork, IDisposable
{
	private TcpListener		_server;
	private HttpListener	_httpListener;
	private TcpClient		_client;
	private NetworkStream	_stream;
	private bool			_isRunning;

	private readonly ConcurrentDictionary<string,WebSocketClient> _webSocketClients = new();




    public Network()
	{
		_server = null;
		_httpListener = null;
		_client = null;
		_stream = null;
	}

	public void Dispose()
	{
		_stream?.Close();
		_stream?.Dispose();

		_httpListener?.Stop();
		_httpListener?.Close();

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
	{	// pour le serveur Websocket 
		_httpListener = new HttpListener();
		_httpListener.Prefixes.Add("http://localhost:8080/");
		_httpListener.Start();
        Console.WriteLine("webSocket Server has started on {0}, Waiting for a connection…", "http://localhost:8080/");

        // pour le serveur TCP
        _server = new TcpListener(IPAddress.Parse("127.0.0.1"), 80);
		_server.Start();
		Console.WriteLine("Tcp Server has started on {0}:{1}, Waiting for a connection…", "127.0.0.1", 80);


		_ = Task.Run(AcceptWebSocketClients);

		_client = _server.AcceptTcpClient();
		Console.WriteLine("A client connected.");

		_stream = _client.GetStream();

		return true;
	}

	public async Task SendMessage(string message)
	{
		var tasks = new List<Task<bool>>();
		foreach (var client in _webSocketClients.Values)
		{
			tasks.Add(SendWebSocketMessage( message, client));
		}
		var result = await Task.WhenAll(tasks);
	}


	private async Task<bool> SendWebSocketMessage(string message, WebSocketClient client)
	{
		if (client.WebSocket.State != WebSocketState.Open)
			return false;
		var buffer = Encoding.UTF8.GetBytes(message);
		await client.WebSocket.SendAsync(new ArraySegment<byte>(buffer),
			WebSocketMessageType.Text, true,
			client.CancellationToken.Token);
		return true;
	}

    private async Task AcceptWebSocketClients()
	{
		while (_isRunning)
		{
			var context = await _httpListener.GetContextAsync();
			if (context.Request.IsWebSocketRequest)
			{
				var wsContext = await context.AcceptWebSocketAsync(null);
				_ = Task.Run(() => 
				{ 
					var result = HandleWebSocketClient(wsContext.WebSocket);
				});
			}
		}

		return;
	}

	private async Task HandleWebSocketClient(WebSocket websocket)
	{
		var client  = new WebSocketClient(websocket);
		_webSocketClients.TryAdd(client.Id, client);
		Console.WriteLine($"Client WebSocket connecté : {0}", client.Id);
		try
		{
            // send first Message
			//
            var buffer = new byte[4096];
            while (websocket.State == WebSocketState.Open && !client.CancellationToken.Token.IsCancellationRequested)
			{
				var result = await websocket.ReceiveAsync(
					new ArraySegment<byte>(buffer),
					client.CancellationToken.Token
				);
				if (result.MessageType == WebSocketMessageType.Close)
				{
					await websocket.CloseAsync(WebSocketCloseStatus.NormalClosure,
						"Closing",
						CancellationToken.None
					);
					break;
				}
				else if (result.MessageType == WebSocketMessageType.Text) {
                    var message = Encoding.UTF8.GetString(buffer, 0, result.Count);
					// client , message
                }
			}
		}
		catch (Exception ex)
		{

		}

	}

}
