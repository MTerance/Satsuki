using Godot;
using Satsuki.Networks;
using Satsuki.Utils;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;

namespace Satsuki.Systems
{
	/// <summary>
	/// Gestionnaire dédié aux fonctionnalités serveur du jeu
	/// Centralise toute la logique de communication réseau, traitement des messages et gestion des clients
	/// </summary>
	public partial class GameServerHandler : Node
	{
		#region Events
		[Signal] public delegate void ServerStartedEventHandler();
		[Signal] public delegate void ServerStoppedEventHandler();
		[Signal] public delegate void ServerErrorEventHandler(string error);
		[Signal] public delegate void ClientConnectedEventHandler(string clientId);
		[Signal] public delegate void ClientDisconnectedEventHandler(string clientId);
		[Signal] public delegate void MessageReceivedEventHandler(string clientId, string content);
		#endregion

		#region Private Fields
		private ServerManager _serverManager;
		private bool _debugMode = true;
		private Timer _messageProcessingTimer;
		private Timer _statisticsTimer;
		
		// Référence à la scène principale pour obtenir l'état du jeu
		private MainGameScene _mainGameScene;
		#endregion

		#region Initialization
		public override void _Ready()
		{
			GD.Print("?? GameServerHandler: Initialisation...");
			
			// Obtenir la référence à la MainGameScene
			_mainGameScene = GetParent<MainGameScene>();
			
			InitializeServer();
			SetupMessageProcessing();
			TestCryptographySystem();
			
			GD.Print("? GameServerHandler: Prêt");
		}

		private void InitializeServer()
		{
			// Récupérer le ServerManager via AutoLoad
			_serverManager = GetNodeOrNull<ServerManager>("/root/ServerManager");

			if (_serverManager == null)
			{
				GD.PrintErr("? ServerManager non trouvé via AutoLoad! Démarrage manuel...");
				StartManualServer();
			}
			else
			{
				// Configurer la référence au GameServerHandler dans le ServerManager
				_serverManager.SetGameServerHandler(this);
				
				// Connecter les événements du ServerManager
				_serverManager.ServerStarted += OnServerStarted;
				_serverManager.ServerStopped += OnServerStopped;
				_serverManager.ServerError += OnServerError;

				GD.Print("?? GameServerHandler: Connecté au ServerManager");
			}
		}

		private void StartManualServer()
		{
			try
			{
				var network = Network.GetInstance;
				if (network.Start())
				{
					GD.Print("? Serveur démarré manuellement avec succès!");
					EmitSignal(SignalName.ServerStarted);
				}
				else
				{
					GD.PrintErr("? Échec du démarrage manuel du serveur");
					EmitSignal(SignalName.ServerError, "Échec du démarrage manuel du serveur");
				}
			}
			catch (System.Exception ex)
			{
				GD.PrintErr($"? Erreur lors du démarrage manuel: {ex.Message}");
				EmitSignal(SignalName.ServerError, ex.Message);
			}
		}

		private void SetupMessageProcessing()
		{
			// Configure un timer pour traiter les messages périodiquement
			_messageProcessingTimer = new Timer();
			_messageProcessingTimer.WaitTime = 0.1; // Traite les messages toutes les 100ms
			_messageProcessingTimer.Timeout += () => ProcessIncomingMessages();
			_messageProcessingTimer.Autostart = true;
			AddChild(_messageProcessingTimer);

			// Timer pour afficher les statistiques
			_statisticsTimer = new Timer();
			_statisticsTimer.WaitTime = 5.0; // Affiche les stats toutes les 5 secondes
			_statisticsTimer.Timeout += DisplayStatistics;
			_statisticsTimer.Autostart = true;
			AddChild(_statisticsTimer);

			Console.WriteLine("?? GameServerHandler: Système de réception multithread initialisé avec cryptage");
		}
		#endregion

		#region Cryptography System
		/// <summary>
		/// Teste le système de cryptage au démarrage
		/// </summary>
		private void TestCryptographySystem()
		{
			Console.WriteLine("?? Test du système de cryptage...");
			bool testResult = MessageCrypto.TestEncryption();

			if (testResult)
			{
				Console.WriteLine("? Système de cryptage opérationnel");
			}
			else
			{
				Console.WriteLine("? Problème avec le système de cryptage");
			}

			// Affiche les informations sur les clés par défaut
			var keyInfo = MessageCrypto.GetDefaultKeyInfo();
			Console.WriteLine($"?? Clé par défaut: {keyInfo.keyBase64.Substring(0, 10)}...");
			Console.WriteLine($"?? IV par défaut: {keyInfo.ivBase64.Substring(0, 10)}...");
		}

		/// <summary>
		/// Bascule le cryptage on/off
		/// </summary>
		public void ToggleEncryption()
		{
			var encInfo = MessageReceiver.GetInstance.GetEncryptionInfo();
			MessageReceiver.GetInstance.ConfigureEncryption(!encInfo.enabled);
			Console.WriteLine($"?? Cryptage basculé: {(!encInfo.enabled ? "ACTIVÉ" : "DÉSACTIVÉ")}");
		}

		/// <summary>
		/// Génère une nouvelle clé de cryptage
		/// </summary>
		public void GenerateNewEncryptionKey()
		{
			MessageReceiver.GetInstance.GenerateNewEncryptionKey();
			Console.WriteLine("?? Nouvelle clé de cryptage générée");
		}
		#endregion

		#region Message Processing
		/// <summary>
		/// Traite les messages entrants du MessageReceiver avec décryptage automatique
		/// </summary>
		/// <param name="maxMessages">Nombre maximum de messages à traiter (0 = tous)</param>
		private void ProcessIncomingMessages(int maxMessages = 0)
		{
			if (MessageReceiver.GetInstance.HasPendingMessages())
			{
				// Récupère tous les messages dans l'ordre d'arrivée avec décryptage automatique
				List<Message> messages = MessageReceiver.GetInstance.GetMessagesByArrivalOrder(decryptMessages: true);

				foreach (var message in messages)
				{
					HandleMessage(message);
				}
			}
		}

		/// <summary>
		/// Traite le prochain message disponible
		/// </summary>
		private void ProcessNextMessage()
		{
			var message = MessageReceiver.GetInstance.GetNextMessage(decryptMessage: true);
			if (message != null)
			{
				HandleMessage(message);
			}
		}

		/// <summary>
		/// Traite un message individuel (déjà décrypté)
		/// </summary>
		/// <param name="message">Message à traiter</param>
		private void HandleMessage(Message message)
		{
			if (_debugMode)
			{
				Console.WriteLine($"[Séq#{message.SequenceNumber}] [{message.Timestamp:HH:mm:ss.fff}] {message.Content}");
			}

			// Extrait l'ID du client du message (format: [ClientId] contenu)
			string clientId = ExtractClientId(message.Content);
			string content = ExtractMessageContent(message.Content);

			// Émettre le signal pour notifier la réception du message
			EmitSignal(SignalName.MessageReceived, clientId, content);

			// Vérifier si c'est une réponse JSON (commence par '{')
			if (content.TrimStart().StartsWith("{"))
			{
				HandleJsonMessage(clientId, content);
				return;
			}

			// Traitement basé sur le contenu du message
			switch (GetMessageType(content))
			{
				case "PLAYER_MOVE":
					HandlePlayerMovement(clientId, content);
					break;
				case "CHAT":
					HandleChatMessage(clientId, content);
					break;
				case "GAME_STATE":
					HandleGameStateUpdate(clientId, content);
					break;
				case "CLIENT_INFO":
					HandleClientInfo(clientId, content);
					break;
				case "PING":
					HandlePingMessage(clientId, content);
					break;
				case "CRYPTO_TEST":
					HandleCryptoTestMessage(clientId, content);
					break;
				default:
					HandleGenericMessage(clientId, content);
					break;
			}
		}

		/// <summary>
		/// Détermine le type de message basé sur son contenu
		/// </summary>
		private string GetMessageType(string content)
		{
			if (content.StartsWith("PLAYER_MOVE:")) return "PLAYER_MOVE";
			if (content.StartsWith("CHAT:")) return "CHAT";
			if (content.StartsWith("GAME_STATE:")) return "GAME_STATE";
			if (content.StartsWith("CLIENT_INFO:")) return "CLIENT_INFO";
			if (content.StartsWith("PING")) return "PING";
			if (content.StartsWith("CRYPTO_TEST:")) return "CRYPTO_TEST";
			return "GENERIC";
		}

		/// <summary>
		/// Traite les messages JSON du client
		/// </summary>
		private void HandleJsonMessage(string clientId, string jsonContent)
		{
			try
			{
				using JsonDocument doc = JsonDocument.Parse(jsonContent);
				JsonElement root = doc.RootElement;

				// Vérifier si c'est une réponse de type client
				if (root.TryGetProperty("order", out JsonElement orderElement))
				{
					string order = orderElement.GetString();

					if (order == "ClientTypeResponse" && root.TryGetProperty("clientType", out JsonElement typeElement))
					{
						string clientType = typeElement.GetString();
						Console.WriteLine($"?? Type de client reçu de {clientId}: {clientType}");

						// Récupérer le mot de passe si présent (pour les clients BACKEND)
						string password = null;
						if (root.TryGetProperty("password", out JsonElement passwordElement))
						{
							password = passwordElement.GetString();
							Console.WriteLine($"?? Mot de passe fourni par {clientId} pour authentification BACKEND");
						}

						// Transférer au ServerManager pour traitement avec le mot de passe
						_serverManager?.HandleClientTypeResponse(clientId, clientType, password);
					}
				}
			}
			catch (JsonException ex)
			{
				Console.WriteLine($"? Erreur lors du parsing JSON de {clientId}: {ex.Message}");
			}
		}
		#endregion

		#region Message Type Handlers
		/// <summary>
		/// Traite les mouvements de joueur
		/// </summary>
		private void HandlePlayerMovement(string clientId, string content)
		{
			Console.WriteLine($"?? Mouvement du joueur {clientId}: {content}");
			// Retransmet le mouvement aux autres clients (crypté)
			BroadcastToOtherClients(clientId, content, encrypt: true);
		}

		/// <summary>
		/// Traite les messages de chat
		/// </summary>
		private void HandleChatMessage(string clientId, string content)
		{
			Console.WriteLine($"?? Chat de {clientId}: {content}");
			// Retransmet le message de chat à tous les clients (crypté)
			BroadcastToAllClients($"CHAT_RELAY:{clientId}:{content}", encrypt: true);
		}

		/// <summary>
		/// Traite les mises à jour d'état de jeu
		/// </summary>
		private void HandleGameStateUpdate(string clientId, string content)
		{
			Console.WriteLine($"?? Mise à jour d'état de {clientId}: {content}");
			// Traite la mise à jour d'état du jeu...
		}

		/// <summary>
		/// Traite les informations du client
		/// </summary>
		private void HandleClientInfo(string clientId, string content)
		{
			Console.WriteLine($"?? Informations du client {clientId}: {content}");
			// Répond avec les informations du serveur (crypté)
			var encInfo = MessageReceiver.GetInstance.GetEncryptionInfo();
			SendMessageToClient(clientId, $"SERVER_INFO:Version=1.0,Players={GetConnectedClientCount()},Crypto={encInfo.enabled}", encrypt: true);
		}

		/// <summary>
		/// Traite les messages de ping
		/// </summary>
		private void HandlePingMessage(string clientId, string content)
		{
			if (_debugMode)
			{
				Console.WriteLine($"?? Ping de {clientId}: {content}");
			}
			// Répond avec un pong (crypté)
			SendMessageToClient(clientId, "PONG", encrypt: true);
		}

		/// <summary>
		/// Traite les messages de test de cryptage
		/// </summary>
		private void HandleCryptoTestMessage(string clientId, string content)
		{
			Console.WriteLine($"?? Test de cryptage de {clientId}: {content}");
			// Répond avec un message de test crypté
			SendMessageToClient(clientId, "CRYPTO_RESPONSE:Message de test crypté du serveur", encrypt: true);
		}

		/// <summary>
		/// Traite les messages génériques
		/// </summary>
		private void HandleGenericMessage(string clientId, string content)
		{
			Console.WriteLine($"?? Message générique de {clientId}: {content}");
		}
		#endregion

		#region Message Utilities
		/// <summary>
		/// Extrait l'ID du client du message
		/// </summary>
		private string ExtractClientId(string messageContent)
		{
			if (messageContent.StartsWith("[") && messageContent.Contains("]"))
			{
				int endIndex = messageContent.IndexOf("]");
				return messageContent.Substring(1, endIndex - 1);
			}
			return "Unknown";
		}

		/// <summary>
		/// Extrait le contenu du message sans l'ID du client
		/// </summary>
		private string ExtractMessageContent(string messageContent)
		{
			if (messageContent.StartsWith("[") && messageContent.Contains("] "))
			{
				int startIndex = messageContent.IndexOf("] ") + 2;
				return messageContent.Substring(startIndex);
			}
			return messageContent;
		}
		#endregion

		#region Client Communication
		/// <summary>
		/// Envoie un message à un client spécifique avec cryptage optionnel
		/// </summary>
		/// <param name="clientId">ID du client</param>
		/// <param name="message">Message à envoyer</param>
		/// <param name="encrypt">Si true, crypte le message avant envoi</param>
		public async void SendMessageToClient(string clientId, string message, bool encrypt = true)
		{
			bool success = await MessageReceiver.GetInstance.SendMessageToClient(clientId, message, encrypt);
			if (_debugMode && !success)
			{
				Console.WriteLine($"? Échec envoi message à {clientId}");
			}
			else if (_debugMode && encrypt)
			{
				Console.WriteLine($"?? Message crypté envoyé à {clientId}");
			}
		}

		/// <summary>
		/// Diffuse un message à tous les clients avec cryptage optionnel
		/// </summary>
		/// <param name="message">Message à diffuser</param>
		/// <param name="encrypt">Si true, crypte le message avant envoi</param>
		public async void BroadcastToAllClients(string message, bool encrypt = true)
		{
			await MessageReceiver.GetInstance.BroadcastMessage(message, encrypt);
			if (_debugMode)
			{
				string status = encrypt ? "crypté" : "clair";
				Console.WriteLine($"?? Message {status} diffusé: {message}");
			}
		}

		/// <summary>
		/// Diffuse un message à tous les clients sauf l'expéditeur
		/// </summary>
		/// <param name="senderClientId">ID de l'expéditeur à exclure</param>
		/// <param name="message">Message à diffuser</param>
		/// <param name="encrypt">Si true, crypte le message avant envoi</param>
		public async void BroadcastToOtherClients(string senderClientId, string message, bool encrypt = true)
		{
			var clients = MessageReceiver.GetInstance.GetConnectedClientIds();
			foreach (string clientId in clients)
			{
				if (clientId != senderClientId)
				{
					await MessageReceiver.GetInstance.SendMessageToClient(clientId, message, encrypt);
				}
			}
			if (_debugMode)
			{
				string status = encrypt ? "crypté" : "clair";
				Console.WriteLine($"?? Message {status} diffusé à {clients.Count - 1} autres clients");
			}
		}

		/// <summary>
		/// Déconnecte un client spécifique
		/// </summary>
		public async void DisconnectClient(string clientId)
		{
			await MessageReceiver.GetInstance.RemoveClient(clientId);
			Console.WriteLine($"?? Client {clientId} déconnecté par le serveur");
			EmitSignal(SignalName.ClientDisconnected, clientId);
		}
		#endregion

		#region Server Information
		/// <summary>
		/// Obtient le nombre de clients connectés
		/// </summary>
		public int GetConnectedClientCount()
		{
			return MessageReceiver.GetInstance.GetConnectedClientIds().Count;
		}

		/// <summary>
		/// Obtient l'état complet du serveur incluant les informations réseau et clients
		/// </summary>
		/// <returns>Un objet contenant l'état du serveur</returns>
		public object GetServerState()
		{
			var stats = MessageReceiver.GetInstance.GetStatistics();
			var encInfo = MessageReceiver.GetInstance.GetEncryptionInfo();
			var connectedClients = MessageReceiver.GetInstance.GetConnectedClientIds();
			var network = Network.GetInstance;

			return new
			{
				Server = new
				{
					IsRunning = stats.isRunning,
					IsServerManagerActive = _serverManager?.IsServerRunning() ?? false,
					ConnectedClients = stats.connectedClients,
					PendingMessages = stats.pendingMessages
				},
				Encryption = new
				{
					Enabled = stats.encryptionEnabled,
					KeyPreview = encInfo.keyBase64?.Substring(0, Math.Min(10, encInfo.keyBase64?.Length ?? 0)) ?? "N/A",
					IVPreview = encInfo.ivBase64?.Substring(0, Math.Min(10, encInfo.ivBase64?.Length ?? 0)) ?? "N/A"
				},
				Clients = connectedClients.Select(id => new
				{
					Id = id,
					Status = "Connected",
					Type = network.GetClientType(id) ?? "UNKNOWN"
				}).ToList(),
				Debug = new
				{
					DebugMode = _debugMode,
					Timestamp = DateTime.UtcNow
				}
			};
		}

		/// <summary>
		/// Obtient l'état complet du jeu depuis la MainGameScene
		/// </summary>
		/// <returns>Un objet contenant l'état complet du jeu</returns>
		public object GetCompleteGameState()
		{
			var serverState = GetServerState();
			object gameSceneState = null;

			// Obtenir l'état de la scène de jeu depuis la MainGameScene
			if (_mainGameScene != null)
			{
				try
				{
					gameSceneState = _mainGameScene.GetGameSceneState();
				}
				catch (Exception ex)
				{
					Console.WriteLine($"? Erreur lors de la récupération de l'état de la scène: {ex.Message}");
					gameSceneState = new { Error = "Failed to get game scene state", Message = ex.Message };
				}
			}

			return new
			{
				ServerState = serverState,
				GameSceneState = gameSceneState,
				Timestamp = DateTime.UtcNow
			};
		}
		#endregion

		#region Statistics and Debug
		/// <summary>
		/// Affiche les statistiques du système avec informations de cryptage
		/// </summary>
		private void DisplayStatistics()
		{
			if (_debugMode)
			{
				var stats = MessageReceiver.GetInstance.GetStatistics();
				var encInfo = MessageReceiver.GetInstance.GetEncryptionInfo();

				Console.WriteLine($"=== STATISTIQUES RÉSEAU ===");
				Console.WriteLine($"?? Serveur actif: {stats.isRunning}");
				Console.WriteLine($"?? Clients connectés: {stats.connectedClients}");
				Console.WriteLine($"?? Messages en attente: {stats.pendingMessages}");
				Console.WriteLine($"?? Cryptage: {(stats.encryptionEnabled ? "ACTIVÉ" : "DÉSACTIVÉ")}");
				Console.WriteLine($"?? Mode: Ordre d'arrivée (FIFO)");
				if (stats.encryptionEnabled)
				{
					Console.WriteLine($"?? Clé: {encInfo.keyBase64.Substring(0, 10)}...");
				}
				Console.WriteLine($"========================");
			}
		}

		/// <summary>
		/// Bascule le mode debug
		/// </summary>
		public void ToggleDebugMode()
		{
			_debugMode = !_debugMode;
			Console.WriteLine($"?? Mode debug: {(_debugMode ? "ACTIVÉ" : "DÉSACTIVÉ")}");
		}

		/// <summary>
		/// Traite les messages en mode haute fréquence
		/// </summary>
		public void ProcessMessagesHighFrequency()
		{
			// Traite tous les messages disponibles immédiatement
			while (MessageReceiver.GetInstance.HasPendingMessages())
			{
				ProcessNextMessage();
			}
			Console.WriteLine("? Traitement haute fréquence exécuté");
		}

		/// <summary>
		/// Méthode alternative pour récupérer un nombre limité de messages
		/// </summary>
		public void ProcessLimitedMessages(int maxMessages = 10)
		{
			if (MessageReceiver.GetInstance.HasPendingMessages())
			{
				List<Message> messages = MessageReceiver.GetInstance.GetMessagesByArrivalOrder(maxMessages, decryptMessages: true);

				foreach (var message in messages)
				{
					HandleMessage(message);
				}
			}
			Console.WriteLine($"?? Traitement limité à {maxMessages} messages");
		}

		/// <summary>
		/// Affiche la liste des clients connectés
		/// </summary>
		public void ListConnectedClients()
		{
			var clients = MessageReceiver.GetInstance.GetConnectedClientIds();
			Console.WriteLine($"?? Clients connectés: {string.Join(", ", clients)}");
		}
		#endregion

		#region Server Event Handlers
		private void OnServerStarted()
		{
			GD.Print("?? GameServerHandler: Serveur démarré avec succès!");
			EmitSignal(SignalName.ServerStarted);
		}

		private void OnServerStopped()
		{
			GD.Print("?? GameServerHandler: Serveur arrêté");
			EmitSignal(SignalName.ServerStopped);
		}

		private void OnServerError(string error)
		{
			GD.PrintErr($"?? GameServerHandler: Erreur serveur - {error}");
			EmitSignal(SignalName.ServerError, error);
		}
		#endregion

		#region Cleanup
		public override void _ExitTree()
		{
			// Déconnecter les événements du serveur
			if (_serverManager != null)
			{
				_serverManager.ServerStarted -= OnServerStarted;
				_serverManager.ServerStopped -= OnServerStopped;
				_serverManager.ServerError -= OnServerError;
			}
			
			Console.WriteLine("?? GameServerHandler: Nettoyage des ressources de cryptage");
			
			// Nettoie les ressources quand la scène se ferme
			_messageProcessingTimer?.QueueFree();
			_statisticsTimer?.QueueFree();
			
			Console.WriteLine("?? GameServerHandler: Nettoyage terminé");
		}
		#endregion
	}
}