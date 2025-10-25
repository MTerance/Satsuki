using Godot;
using Satsuki.Networks;
using Satsuki.Utils;
using System;
using System.Text.Json;
using System.Threading.Tasks;

public partial class ServerManager : Node
{
	private Network _network;
	private bool _isServerRunning = false;
	private MainGameScene _mainGameScene;
	private bool _hasHadFirstClient = false;
	
	// Mot de passe pour les clients BACKEND
	private const string BACKEND_PASSWORD = "***Satsuk1***";

	[Signal] public delegate void ServerStartedEventHandler();
	[Signal] public delegate void ServerStoppedEventHandler();
	[Signal] public delegate void ServerErrorEventHandler(string error);
	[Signal] public delegate void ClientConnectedEventHandler(string clientId);
	[Signal] public delegate void ClientTypeReceivedEventHandler(string clientId, string clientType);
	[Signal] public delegate void BackendAuthenticationFailedEventHandler(string clientId, string reason);

	public override void _Ready()
	{
		GD.Print("?? Server Manager: Initialisation du serveur Satsuki...");
		
		// Tenter de récupérer MainGameScene
		_mainGameScene = GetNodeOrNull<MainGameScene>("/root/MainGameScene");
		if (_mainGameScene == null)
		{
			GD.PrintErr("?? ServerManager: MainGameScene non trouvé, GetGameState ne sera pas disponible");
		}
		
		// Demarrer le serveur automatiquement au lancement du jeu
		CallDeferred(nameof(StartServerAsync));
		
		// Gerer la fermeture propre du serveur
		GetTree().AutoAcceptQuit = false;
	}

	private async void StartServerAsync()
	{
		try
		{
			GD.Print("?? Demarrage du serveur reseau...");
			
			_network = Network.GetInstance;
			
			// S'abonner aux événements de connexion de clients
			_network.OnClientConnected += HandleClientConnected;
			
			if (_network.Start())
			{
				_isServerRunning = true;
				GD.Print("? Serveur Satsuki demarre avec succes!");
				GD.Print("?? Serveur TCP: 127.0.0.1:80");
				GD.Print("?? Systeme de cryptage: Active");
				GD.Print("?? Authentification BACKEND: Active");
				
				EmitSignal(SignalName.ServerStarted);
				
				// Envoyer un message d'etat initial aux clients connectes
				await Task.Delay(1000); // Attendre que le serveur soit completement initialise
				await _network.BroadcastMessage("SERVER_READY: Serveur Satsuki en ligne");
			}
			else
			{
				var error = "? Echec du demarrage du serveur reseau";
				GD.PrintErr(error);
				EmitSignal(SignalName.ServerError, error);
			}
		}
		catch (Exception ex)
		{
			var error = $"? Erreur lors du demarrage du serveur: {ex.Message}";
			GD.PrintErr(error);
			EmitSignal(SignalName.ServerError, error);
		}
	}

	/// <summary>
	/// Gère la première connexion d'un client
	/// </summary>
	private async void HandleClientConnected(string clientId)
	{
		GD.Print($"?? ServerManager: Nouveau client connecté - {clientId}");
		
		// Émettre le signal
		EmitSignal(SignalName.ClientConnected, clientId);
		
		// Demander le type du client
		await RequestClientType(clientId);
		
		// Si c'est le premier client, appeler GetGameState
		if (!_hasHadFirstClient)
		{
			_hasHadFirstClient = true;
			GD.Print("?? Premier client connecté - Récupération de l'état du jeu...");
			
			if (_mainGameScene != null)
			{
				try
				{
					var gameState = _mainGameScene.GetGameState();
					GD.Print("?? État du jeu récupéré:");
					
					// Convertir l'objet en JSON pour l'affichage
					string gameStateJson = System.Text.Json.JsonSerializer.Serialize(gameState);
					GD.Print($"   {gameStateJson}");
					
					// Envoyer l'état du jeu au client
					await SendGameStateToClient(clientId, gameStateJson);
				}
				catch (Exception ex)
				{
					GD.PrintErr($"? Erreur lors de la récupération de l'état du jeu: {ex.Message}");
				}
			}
			else
			{
				GD.PrintErr("?? MainGameScene non disponible, impossible de récupérer l'état du jeu");
			}
		}
	}

	/// <summary>
	/// Demande au client de s'identifier avec son type
	/// </summary>
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
				GD.Print($"?? Demande de type envoyée au client {clientId}");
			}
			else
			{
				GD.PrintErr($"? Échec de l'envoi de la demande de type au client {clientId}");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"? Erreur lors de la demande de type client: {ex.Message}");
		}
	}

	/// <summary>
	/// Traite la réponse du client concernant son type avec validation du mot de passe pour BACKEND
	/// </summary>
	public async void HandleClientTypeResponse(string clientId, string clientType, string password = null)
	{
		GD.Print($"?? Type de client reçu - {clientId}: {clientType}");
		
		// Si c'est un client BACKEND, vérifier le mot de passe
		if (clientType == "BACKEND")
		{
			if (string.IsNullOrEmpty(password))
			{
				GD.PrintErr($"?? Client {clientId} tente de se connecter en tant que BACKEND sans mot de passe");
				await RejectBackendClient(clientId, "PASSWORD_MISSING");
				return;
			}
			
			if (password != BACKEND_PASSWORD)
			{
				GD.PrintErr($"?? Client {clientId} a fourni un mot de passe BACKEND invalide");
				await RejectBackendClient(clientId, "PASSWORD_INVALID");
				return;
			}
			
			GD.Print($"?? Client {clientId} authentifié en tant que BACKEND avec succès");
		}
		
		// Valider le type de client
		if (IsValidClientType(clientType))
		{
			// Émettre le signal
			EmitSignal(SignalName.ClientTypeReceived, clientId, clientType);
			
			// Enregistrer le type de client
			_network.SetClientType(clientId, clientType);
			
			// Envoyer la confirmation au client
			await SendClientTypeConfirmation(clientId, clientType, true);
			
			GD.Print($"? Client {clientId} enregistré en tant que {clientType}");
		}
		else
		{
			GD.PrintErr($"?? Type de client invalide reçu de {clientId}: {clientType}");
			await SendClientTypeConfirmation(clientId, clientType, false, "INVALID_TYPE");
		}
	}

	/// <summary>
	/// Rejette un client BACKEND avec mot de passe invalide
	/// </summary>
	private async Task RejectBackendClient(string clientId, string reason)
	{
		// Envoyer un message d'erreur au client
		var errorMessage = new
		{
			order = "ClientTypeRejected",
			clientId = clientId,
			reason = reason,
			timestamp = DateTime.UtcNow.ToString("o")
		};
		
		string jsonMessage = JsonSerializer.Serialize(errorMessage);
		await _network.SendMessageToClient(clientId, jsonMessage);
		
		// Émettre le signal d'échec d'authentification
		EmitSignal(SignalName.BackendAuthenticationFailed, clientId, reason);
		
		// Déconnecter le client après un court délai
		await Task.Delay(2000);
		await _network.DisconnectClient(clientId);
		
		GD.Print($"?? Client {clientId} déconnecté pour authentification BACKEND échouée ({reason})");
	}

	/// <summary>
	/// Envoie la confirmation du type de client
	/// </summary>
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
		
		GD.Print($"?? Confirmation de type envoyée au client {clientId}: {(success ? "ACCEPTÉ" : "REJETÉ")}");
	}

	/// <summary>
	/// Valide que le type de client est autorisé
	/// </summary>
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

	/// <summary>
	/// Envoie l'état du jeu à un client spécifique
	/// </summary>
	private async Task SendGameStateToClient(string clientId, string gameStateJson)
	{
		try
		{
			string message = $"GAME_STATE:{gameStateJson}";
			
			bool success = await _network.SendMessageToClient(clientId, message);
			if (success)
			{
				GD.Print($"? État du jeu envoyé au client {clientId}");
			}
			else
			{
				GD.PrintErr($"? Échec de l'envoi de l'état du jeu au client {clientId}");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"? Erreur lors de l'envoi de l'état du jeu: {ex.Message}");
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
		GD.Print("?? Arret du serveur en cours...");
		
		if (_isServerRunning && _network != null)
		{
			try
			{
				// Se désabonner des événements
				_network.OnClientConnected -= HandleClientConnected;
				
				// Notifier les clients de la fermeture
				await _network.BroadcastMessage("SERVER_SHUTDOWN: Le serveur Satsuki va se fermer");
				await Task.Delay(2000); // Attendre que les messages soient envoyes
				
				_network.Stop();
				_isServerRunning = false;
				EmitSignal(SignalName.ServerStopped);
				
				GD.Print("? Serveur arrete proprement");
			}
			catch (Exception ex)
			{
				GD.PrintErr($"? Erreur lors de l'arret du serveur: {ex.Message}");
			}
		}
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
			GD.Print($"?? Statut serveur - Clients: {stats.connectedClients}, Messages en attente: {stats.pendingMessages}");
		}
	}

	public override void _ExitTree()
	{
		// Se désabonner des événements lors de la destruction
		if (_network != null)
		{
			_network.OnClientConnected -= HandleClientConnected;
		}
	}
}
