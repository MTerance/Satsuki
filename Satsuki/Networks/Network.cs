using Godot;
using Satsuki.Utils;
using Satsuki.Networks;
using System;
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

    public Network()
	{
		_server = null;
		_cancellationTokenSource = new CancellationTokenSource();
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
			
			// Arr�te le r�cepteur de messages
			MessageReceiver.GetInstance.Stop().Wait(TimeSpan.FromSeconds(5));
		}

		if (_server != null)
		{
			_server.Stop();
			_server = null;
		}
		
		Console.WriteLine("Network: Serveur arr�t�");
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
			
			Console.WriteLine("Server has started on {0}:{1}, Waiting for connections�", "127.0.0.1", 80);

			// D�marre le syst�me de r�ception des messages
			MessageReceiver.GetInstance.Start();

			// D�marre l'�coute des nouvelles connexions en arri�re-plan
			_serverListeningTask = Task.Run(AcceptClientsLoop, _cancellationTokenSource.Token);
			
			return true;
		}
		catch (Exception ex)
		{
			Console.WriteLine($"Erreur lors du d�marrage du serveur: {ex.Message}");
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
						Console.WriteLine($"Nouveau client connect�: {tcpClient.Client.RemoteEndPoint}");
						
						// Ajoute le client au syst�me de r�ception de messages
						string clientId = MessageReceiver.GetInstance.AddClient(tcpClient);
						
						if (clientId != null)
						{
							Console.WriteLine($"Client assign� avec l'ID: {clientId}");
							LogConnectionStats();
						}
						else
						{
							Console.WriteLine("�chec de l'ajout du client au MessageReceiver");
							tcpClient.Close();
						}
					}
				}
				catch (ObjectDisposedException)
				{
					// Serveur ferm�, sortie normale
					break;
				}
				catch (Exception ex)
				{
					Console.WriteLine($"Erreur lors de l'acceptation d'un client: {ex.Message}");
					await Task.Delay(1000, _cancellationTokenSource.Token); // Attendre avant de r�essayer
				}
			}
		}
		catch (OperationCanceledException)
		{
			Console.WriteLine("Boucle d'acceptation des clients annul�e");
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
	/// Affiche les statistiques de connexion
	/// </summary>
	private void LogConnectionStats()
	{
		var stats = MessageReceiver.GetInstance.GetStatistics();
		Console.WriteLine($"Statistiques: {stats.connectedClients} clients connect�s, {stats.pendingMessages} messages en attente");
	}

	/// <summary>
	/// Envoie un message � un client sp�cifique
	/// </summary>
	/// <param name="clientId">ID du client</param>
	/// <param name="message">Message � envoyer</param>
	public async Task<bool> SendMessageToClient(string clientId, string message)
	{
		return await MessageReceiver.GetInstance.SendMessageToClient(clientId, message);
	}

	/// <summary>
	/// Diffuse un message � tous les clients connect�s
	/// </summary>
	/// <param name="message">Message � diffuser</param>
	public async Task BroadcastMessage(string message)
	{
		await MessageReceiver.GetInstance.BroadcastMessage(message);
	}

	/// <summary>
	/// Obtient la liste des clients connect�s
	/// </summary>
	public List<string> GetConnectedClients()
	{
		return MessageReceiver.GetInstance.GetConnectedClientIds();
	}

	/// <summary>
	/// Obtient les statistiques du r�seau
	/// </summary>
	public (int connectedClients, int pendingMessages, bool serverRunning) GetNetworkStatistics()
	{
		var receiverStats = MessageReceiver.GetInstance.GetStatistics();
		return (receiverStats.connectedClients, receiverStats.pendingMessages, _isRunning);
	}

	/// <summary>
	/// D�connecte un client sp�cifique
	/// </summary>
	/// <param name="clientId">ID du client � d�connecter</param>
	public async Task DisconnectClient(string clientId)
	{
		await MessageReceiver.GetInstance.RemoveClient(clientId);
		Console.WriteLine($"Client {clientId} d�connect�");
	}
}