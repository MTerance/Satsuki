using Godot;
using Satsuki.Networks;
using Satsuki.Utils;
using Satsuki.Systems;
using System;
using System.Text.Json;
using System.Threading.Tasks;

public partial class ServerManager : Node
{
	private Network _network;
	private bool _isServerRunning = false;
	private GameServerHandler _gameServerHandler;
	private bool _hasHadFirstClient = false;
	
	private const string BACKEND_PASSWORD = "***Satsuk1***";

	[Signal] public delegate void ServerStartedEventHandler();
	[Signal] public delegate void ServerStoppedEventHandler();
	[Signal] public delegate void ServerErrorEventHandler(string error);
	[Signal] public delegate void ClientConnectedEventHandler(string clientId);
	[Signal] public delegate void ClientTypeReceivedEventHandler(string clientId, string clientType);
	[Signal] public delegate void BackendAuthenticationFailedEventHandler(string clientId, string reason);

	public override void _Ready()
	{
		GD.Print("Server Manager: Initialisation du serveur Satsuki...");
		
		CallDeferred(nameof(StartServerAsync));
		
		GetTree().AutoAcceptQuit = false;
	}

	public void SetGameServerHandler(GameServerHandler gameServerHandler)
	{
		_gameServerHandler = gameServerHandler;
		GD.Print("ServerManager: GameServerHandler configure");
	}

	private async void StartServerAsync()
	{
		try
		{
			GD.Print("Demarrage du serveur reseau...");
			
			_network = Network.GetInstance;
			
			_network.OnClientConnected += HandleClientConnected;
			
			if (_network.Start())
			{
				_isServerRunning = true;
				GD.Print("Serveur Satsuki demarre avec succes!");
				GD.Print("Serveur TCP: 127.0.0.1:80");
				GD.Print("Systeme de cryptage: Active");
				GD.Print("Authentification BACKEND: Active");
				
				EmitSignal(SignalName.ServerStarted);
				
				await Task.Delay(1000);
				await _network.BroadcastMessage("SERVER_READY: Serveur Satsuki en ligne");
			}
			else
			{
				var error = "Echec du demarrage du serveur reseau";
				GD.PrintErr(error);
				EmitSignal(SignalName.ServerError, error);
			}
		}
		catch (Exception ex)
		{
			var error = $"Erreur lors du demarrage du serveur: {ex.Message}";
			GD.PrintErr(error);
			EmitSignal(SignalName.ServerError, error);
		}
	}

	private async void HandleClientConnected(string clientId)
	{
		GD.Print($"ServerManager: Nouveau client connecte - {clientId}");
		
		EmitSignal(SignalName.ClientConnected, clientId);
		
		await RequestClientType(clientId);
		
		if (!_hasHadFirstClient)
		{
			_hasHadFirstClient = true;
			GD.Print("Premier client connecte - Recuperation de l'etat du jeu...");
			
			if (_gameServerHandler != null)
			{
				try
				{
					var gameState = _gameServerHandler.GetCompleteGameState();
					GD.Print("Etat du jeu recupere:");
					
					string gameStateJson = System.Text.Json.JsonSerializer.Serialize(gameState);
					GD.Print($"   {gameStateJson}");
					
					await SendGameStateToClient(clientId, gameStateJson);
				}
				catch (Exception ex)
				{
					GD.PrintErr($"Erreur lors de la recuperation de l'etat du jeu: {ex.Message}");
				}
			}
			else
			{
				GD.PrintErr("GameServerHandler non disponible, impossible de recuperer l'etat du jeu");
			}
		}
	}

	private async Task RequestClientType(string clientId)
	{
		try
		{
			var requestMessage = new
			{
				order = "RequestClientType",
				timestamp = DateTime.UtcNow.ToString("o"),
				clientId = clientId,
				requiresPassword = new[] { "BACKEND" }
			};

			string jsonMessage = JsonSerializer.Serialize(requestMessage);
			bool success = await _network.SendMessageToClient(clientId, jsonMessage);

			if (success)
			{
				GD.Print($"Demande de type envoyee au client {clientId}");
			}
			else
			{
				GD.PrintErr($"Echec de l'envoi de la demande de type au client {clientId}");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"Erreur lors de la demande de type client: {ex.Message}");
		}
	}

	public async void HandleClientTypeResponse(string clientId, string clientType, string password = null)
	{
		GD.Print($"Type de client recu - {clientId}: {clientType}");
		
		if (clientType == "BACKEND")
		{
			if (string.IsNullOrEmpty(password))
			{
				GD.PrintErr($"Client {clientId} tente de se connecter en tant que BACKEND sans mot de passe");
				await RejectBackendClient(clientId, "PASSWORD_MISSING");
				return;
			}
			
			if (password != BACKEND_PASSWORD)
			{
				GD.PrintErr($"Client {clientId} a fourni un mot de passe BACKEND invalide");
				await RejectBackendClient(clientId, "PASSWORD_INVALID");
				return;
			}
			
			GD.Print($"Client {clientId} authentifie en tant que BACKEND avec succes");
		}
		
		if (IsValidClientType(clientType))
		{
			EmitSignal(SignalName.ClientTypeReceived, clientId, clientType);
			
			_network.SetClientType(clientId, clientType);
			
			await SendClientTypeConfirmation(clientId, clientType, true);
			
			GD.Print($"Client {clientId} enregistre en tant que {clientType}");
		}
		else
		{
			GD.PrintErr($"Type de client invalide recu de {clientId}: {clientType}");
			await SendClientTypeConfirmation(clientId, clientType, false, "INVALID_TYPE");
		}
	}

	private async Task RejectBackendClient(string clientId, string reason)
	{
		var errorMessage = new
		{
			order = "ClientTypeRejected",
			clientId = clientId,
			reason = reason,
			timestamp = DateTime.UtcNow.ToString("o")
		};
		
		string jsonMessage = JsonSerializer.Serialize(errorMessage);
		await _network.SendMessageToClient(clientId, jsonMessage);
		
		EmitSignal(SignalName.BackendAuthenticationFailed, clientId, reason);
		
		await Task.Delay(2000);
		await _network.DisconnectClient(clientId);
		
		GD.Print($"Client {clientId} deconnecte pour authentification BACKEND echouee ({reason})");
	}

	private async Task SendClientTypeConfirmation(string clientId, string clientType, bool success, string reason = null)
	{
		var confirmationMessage = new
		{
			order = "ClientTypeConfirmation",
			clientId = clientId,
			clientType = clientType,
			success = success,
			reason = reason,
			timestamp = DateTime.UtcNow.ToString("o")
		};
		
		string jsonMessage = JsonSerializer.Serialize(confirmationMessage);
		await _network.SendMessageToClient(clientId, jsonMessage);
		
		GD.Print($"Confirmation de type envoyee au client {clientId}: {(success ? "ACCEPTE" : "REJETE")}");
	}

	private bool IsValidClientType(string clientType)
	{
		return clientType switch
		{
			"BACKEND" => true,
			"PLAYER" => true,
			"OTHER" => true,
			_ => false
		};
	}

	private async Task SendGameStateToClient(string clientId, string gameStateJson)
	{
		try
		{
			string message = $"GAME_STATE:{gameStateJson}";
			
			bool success = await _network.SendMessageToClient(clientId, message);
			if (success)
			{
				GD.Print($"Etat du jeu envoye au client {clientId}");
			}
			else
			{
				GD.PrintErr($"Echec de l'envoi de l'etat du jeu au client {clientId}");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"Erreur lors de l'envoi de l'etat du jeu: {ex.Message}");
		}
	}

	public override void _Notification(int what)
	{
		if (what == NotificationWMCloseRequest || what == NotificationApplicationPaused)
		{
			OnQuitRequest();
		}
	}

	private async void OnQuitRequest()
	{
		GD.Print("Arret du serveur en cours...");
		
		if (_isServerRunning && _network != null)
		{
			try
			{
				_network.OnClientConnected -= HandleClientConnected;
				
				await _network.BroadcastMessage("SERVER_SHUTDOWN: Le serveur Satsuki va se fermer");
				await Task.Delay(2000);
				
				_network.Stop();
				_isServerRunning = false;
				EmitSignal(SignalName.ServerStopped);
				
				GD.Print("Serveur arrete proprement");
			}
			catch (Exception ex)
			{
				GD.PrintErr($"Erreur lors de l'arret du serveur: {ex.Message}");
			}
		}
		
		// Quitter l'application apres l'arret du serveur
		GD.Print("Fermeture de l'application...");
		GetTree().Quit();
	}

	public bool IsServerRunning()
	{
		return _isServerRunning;
	}

	public Network GetNetwork()
	{
		return _network;
	}

	public async Task<bool> SendServerMessage(string message)
	{
		if (_network != null && _isServerRunning)
		{
			await _network.BroadcastMessage(message);
			return true;
		}
		return false;
	}

	public int GetConnectedClientsCount()
	{
		if (_network != null)
		{
			var stats = _network.GetNetworkStatistics();
			return stats.connectedClients;
		}
		return 0;
	}

	public void LogServerStatus()
	{
		if (_network != null)
		{
			var stats = _network.GetNetworkStatistics();
			GD.Print($"Statut serveur - Clients: {stats.connectedClients}, Messages en attente: {stats.pendingMessages}");
		}
	}

	public override void _ExitTree()
	{
		if (_network != null)
		{
			_network.OnClientConnected -= HandleClientConnected;
		}
	}
}
