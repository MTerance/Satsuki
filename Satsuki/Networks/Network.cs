using Godot;
using Satsuki.Utils;
using Satsuki.Networks;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

public class Network : SingletonBase<Network>, INetwork, IDisposable
{
	private TcpListener _server;
	private bool _isRunning = false;
	private CancellationTokenSource _cancellationTokenSource;
	private Task _serverListeningTask;
	
	// Dictionnaire pour stocker les types de clients
	private readonly ConcurrentDictionary<string, string> _clientTypes;

	// Événement déclenché quand un nouveau client se connecte
	public event Action<string> OnClientConnected;

	public Network()
	{
		_server = null;
		_cancellationTokenSource = new CancellationTokenSource();
		_clientTypes = new ConcurrentDictionary<string, string>();
	}

	public void Dispose()
	{
		Stop();
		_cancellationTokenSource?.Dispose();
	}

	public bool Stop()
	{
		if (_isRunning)
		{
			_isRunning = false;
			_cancellationTokenSource?.Cancel();
			
			// Arrête le récepteur de messages
			MessageReceiver.GetInstance.Stop().Wait(TimeSpan.FromSeconds(5));
			
			// Nettoie les types de clients
			_clientTypes.Clear();
		}

		if (_server != null)
		{
			_server.Stop();
			_server = null;
		}
		
		Console.WriteLine("🛑 Network: Serveur arrêté");
		return true;
	}

	public bool Start()	
	{
		if (_isRunning)
			return true;

		try
		{
			_server = new TcpListener(IPAddress.Parse("127.0.0.1"), 80);
			_server.Start();
			_isRunning = true;
			
			Console.WriteLine("✅ Server has started on {0}:{1}, Waiting for connections…", "127.0.0.1", 80);

			// Démarre le système de réception des messages
			MessageReceiver.GetInstance.Start();

			// Démarre l'écoute des nouvelles connexions en arrière-plan
			_serverListeningTask = Task.Run(AcceptClientsLoop, _cancellationTokenSource.Token);
			
			return true;
		}
		catch (Exception ex)
		{
			Console.WriteLine($"❌ Erreur lors du démarrage du serveur: {ex.Message}");
			return false;
		}
	}

	/// <summary>
	/// Boucle d'acceptation des nouveaux clients
	/// </summary>
	private async Task AcceptClientsLoop()
	{
		try
		{
			while (_isRunning && !_cancellationTokenSource.Token.IsCancellationRequested)
			{
				try
				{
					// Accepte une nouvelle connexion (bloquant)
					var tcpClient = await AcceptTcpClientAsync(_server, _cancellationTokenSource.Token);
					
					if (tcpClient != null)
					{
						Console.WriteLine($"🔌 Nouveau client connecté: {tcpClient.Client.RemoteEndPoint}");
						
						// Ajoute le client au système de réception de messages
						string clientId = MessageReceiver.GetInstance.AddClient(tcpClient);
						
						if (clientId != null)
						{
							Console.WriteLine($"✅ Client assigné avec l'ID: {clientId}");
							
							// Initialiser le type de client comme "UNKNOWN"
							_clientTypes.TryAdd(clientId, "UNKNOWN");
							
							LogConnectionStats();
							
							// Déclencher l'événement de connexion client
							OnClientConnected?.Invoke(clientId);
						}
						else
						{
							Console.WriteLine("❌ Échec de l'ajout du client au MessageReceiver");
							tcpClient.Close();
						}
					}
				}
				catch (ObjectDisposedException)
				{
					// Serveur fermé, sortie normale
					break;
				}
				catch (Exception ex)
				{
					Console.WriteLine($"❌ Erreur lors de l'acceptation d'un client: {ex.Message}");
					await Task.Delay(1000, _cancellationTokenSource.Token); // Attendre avant de réessayer
				}
			}
		}
		catch (OperationCanceledException)
		{
			Console.WriteLine("🛑 Boucle d'acceptation des clients annulée");
		}
	}

	/// <summary>
	/// Version asynchrone de AcceptTcpClient avec support d'annulation
	/// </summary>
	private async Task<TcpClient> AcceptTcpClientAsync(TcpListener listener, CancellationToken cancellationToken)
	{
		try
		{
			return await Task.Run(() =>
			{
				cancellationToken.ThrowIfCancellationRequested();
				return listener.AcceptTcpClient();
			}, cancellationToken);
		}
		catch (OperationCanceledException)
		{
			return null;
		}
	}

	/// <summary>
	/// Définit le type d'un client
	/// </summary>
	public bool SetClientType(string clientId, string clientType)
	{
		if (_clientTypes.ContainsKey(clientId))
		{
			_clientTypes[clientId] = clientType;
			Console.WriteLine($"🏷️ Type de client {clientId} défini: {clientType}");
			return true;
		}
		return false;
	}

	/// <summary>
	/// Obtient le type d'un client
	/// </summary>
	public string GetClientType(string clientId)
	{
		return _clientTypes.TryGetValue(clientId, out string clientType) ? clientType : null;
	}

	/// <summary>
	/// Obtient tous les clients d'un type spécifique
	/// </summary>
	public List<string> GetClientsByType(string clientType)
	{
		var clients = new List<string>();
		foreach (var kvp in _clientTypes)
		{
			if (kvp.Value == clientType)
			{
				clients.Add(kvp.Key);
			}
		}
		return clients;
	}

	/// <summary>
	/// Obtient tous les types de clients avec leurs IDs
	/// </summary>
	public Dictionary<string, string> GetAllClientTypes()
	{
		return new Dictionary<string, string>(_clientTypes);
	}

	/// <summary>
	/// Affiche les statistiques de connexion
	/// </summary>
	private void LogConnectionStats()
	{
		var stats = MessageReceiver.GetInstance.GetStatistics();
		Console.WriteLine($"📊 Statistiques: {stats.connectedClients} clients connectés, {stats.pendingMessages} messages en attente");
	}

	/// <summary>
	/// Envoie un message à un client spécifique
	/// </summary>
	/// <param name="clientId">ID du client</param>
	/// <param name="message">Message à envoyer</param>
	public async Task<bool> SendMessageToClient(string clientId, string message)
	{
		return await MessageReceiver.GetInstance.SendMessageToClient(clientId, message);
	}

	/// <summary>
	/// Diffuse un message à tous les clients connectés
	/// </summary>
	/// <param name="message">Message à diffuser</param>
	public async Task BroadcastMessage(string message)
	{
		await MessageReceiver.GetInstance.BroadcastMessage(message);
	}

	/// <summary>
	/// Diffuse un message à tous les clients d'un type spécifique
	/// </summary>
	/// <param name="message">Message à diffuser</param>
	/// <param name="clientType">Type de clients ciblés (BACKEND, PLAYER, OTHER)</param>
	public async Task BroadcastMessageToType(string message, string clientType)
	{
		var targetClients = GetClientsByType(clientType);
		foreach (var clientId in targetClients)
		{
			await SendMessageToClient(clientId, message);
		}
		Console.WriteLine($"📢 Message diffusé à {targetClients.Count} clients de type {clientType}");
	}

	/// <summary>
	/// Obtient la liste des clients connectés
	/// </summary>
	public List<string> GetConnectedClients()
	{
		return MessageReceiver.GetInstance.GetConnectedClientIds();
	}

	/// <summary>
	/// Obtient les statistiques du réseau
	/// </summary>
	public (int connectedClients, int pendingMessages, bool serverRunning) GetNetworkStatistics()
	{
		var receiverStats = MessageReceiver.GetInstance.GetStatistics();
		return (receiverStats.connectedClients, receiverStats.pendingMessages, _isRunning);
	}

	/// <summary>
	/// Déconnecte un client spécifique
	/// </summary>
	/// <param name="clientId">ID du client à déconnecter</param>
	public async Task DisconnectClient(string clientId)
	{
		await MessageReceiver.GetInstance.RemoveClient(clientId);
		_clientTypes.TryRemove(clientId, out _);
		Console.WriteLine($"🔌 Client {clientId} déconnecté");
	}
}
