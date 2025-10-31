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
	/// Gestionnaire d�di� aux fonctionnalit�s serveur du jeu
	/// Centralise toute la logique de communication r�seau, traitement des messages et gestion des clients
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
		
		// R�f�rence � la sc�ne principale pour obtenir l'�tat du jeu
		private MainGameScene _mainGameScene;
		#endregion

		#region Initialization
		public override void _Ready()
		{
			GD.Print("?? GameServerHandler: Initialisation...");
			
			// Obtenir la r�f�rence � la MainGameScene
			_mainGameScene = GetParent<MainGameScene>();
			
			InitializeServer();
			SetupMessageProcessing();
			TestCryptographySystem();
			
			GD.Print("? GameServerHandler: Pr�t");
		}

		private void InitializeServer()
		{
			// R�cup�rer le ServerManager via AutoLoad
			_serverManager = GetNodeOrNull<ServerManager>("/root/ServerManager");

			if (_serverManager == null)
			{
				GD.PrintErr("? ServerManager non trouv� via AutoLoad! D�marrage manuel...");
				StartManualServer();
			}
			else
			{
				// Configurer la r�f�rence au GameServerHandler dans le ServerManager
				_serverManager.SetGameServerHandler(this);
				
				// Connecter les �v�nements du ServerManager
				_serverManager.ServerStarted += OnServerStarted;
				_serverManager.ServerStopped += OnServerStopped;
				_serverManager.ServerError += OnServerError;

				GD.Print("?? GameServerHandler: Connect� au ServerManager");
			}
		}

		private void StartManualServer()
		{
			try
			{
				var network = Network.GetInstance;
				if (network.Start())
				{
					GD.Print("? Serveur d�marr� manuellement avec succ�s!");
					EmitSignal(SignalName.ServerStarted);
				}
				else
				{
					GD.PrintErr("? �chec du d�marrage manuel du serveur");
					EmitSignal(SignalName.ServerError, "�chec du d�marrage manuel du serveur");
				}
			}
			catch (System.Exception ex)
			{
				GD.PrintErr($"? Erreur lors du d�marrage manuel: {ex.Message}");
				EmitSignal(SignalName.ServerError, ex.Message);
			}
		}

		private void SetupMessageProcessing()
		{
			// Configure un timer pour traiter les messages p�riodiquement
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

			Console.WriteLine("?? GameServerHandler: Syst�me de r�ception multithread initialis� avec cryptage");
		}
		#endregion

		#region Cryptography System
		/// <summary>
		/// Teste le syst�me de cryptage au d�marrage
		/// </summary>
		private void TestCryptographySystem()
		{
			Console.WriteLine("?? Test du syst�me de cryptage...");
			bool testResult = MessageCrypto.TestEncryption();

			if (testResult)
			{
				Console.WriteLine("? Syst�me de cryptage op�rationnel");
			}
			else
			{
				Console.WriteLine("? Probl�me avec le syst�me de cryptage");
			}

			// Affiche les informations sur les cl�s par d�faut
			var keyInfo = MessageCrypto.GetDefaultKeyInfo();
			Console.WriteLine($"?? Cl� par d�faut: {keyInfo.keyBase64.Substring(0, 10)}...");
			Console.WriteLine($"?? IV par d�faut: {keyInfo.ivBase64.Substring(0, 10)}...");
		}

		/// <summary>
		/// Bascule le cryptage on/off
		/// </summary>
		public void ToggleEncryption()
		{
			var encInfo = MessageReceiver.GetInstance.GetEncryptionInfo();
			MessageReceiver.GetInstance.ConfigureEncryption(!encInfo.enabled);
			Console.WriteLine($"?? Cryptage bascul�: {(!encInfo.enabled ? "ACTIV�" : "D�SACTIV�")}");
		}

		/// <summary>
		/// G�n�re une nouvelle cl� de cryptage
		/// </summary>
		public void GenerateNewEncryptionKey()
		{
			MessageReceiver.GetInstance.GenerateNewEncryptionKey();
			Console.WriteLine("?? Nouvelle cl� de cryptage g�n�r�e");
		}
		#endregion

		#region Message Processing
		/// <summary>
		/// Traite les messages entrants du MessageReceiver avec d�cryptage automatique
		/// </summary>
		/// <param name="maxMessages">Nombre maximum de messages � traiter (0 = tous)</param>
		private void ProcessIncomingMessages(int maxMessages = 0)
		{
			if (MessageReceiver.GetInstance.HasPendingMessages())
			{
				// R�cup�re tous les messages dans l'ordre d'arriv�e avec d�cryptage automatique
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
		/// Traite un message individuel (d�j� d�crypt�)
		/// </summary>
		/// <param name="message">Message � traiter</param>
		private void HandleMessage(Message message)
		{
			if (_debugMode)
			{
				Console.WriteLine($"[S�q#{message.SequenceNumber}] [{message.Timestamp:HH:mm:ss.fff}] {message.Content}");
			}

			// Extrait l'ID du client du message (format: [ClientId] contenu)
			string clientId = ExtractClientId(message.Content);
			string content = ExtractMessageContent(message.Content);

			// �mettre le signal pour notifier la r�ception du message
			EmitSignal(SignalName.MessageReceived, clientId, content);

			// V�rifier si c'est une r�ponse JSON (commence par '{')
			if (content.TrimStart().StartsWith("{"))
			{
				HandleJsonMessage(clientId, content);
				return;
			}

			// Traitement bas� sur le contenu du message
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
		/// D�termine le type de message bas� sur son contenu
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

				// V�rifier si c'est une r�ponse de type client
				if (root.TryGetProperty("order", out JsonElement orderElement))
				{
					string order = orderElement.GetString();

					if (order == "ClientTypeResponse" && root.TryGetProperty("clientType", out JsonElement typeElement))
					{
						string clientType = typeElement.GetString();
						Console.WriteLine($"?? Type de client re�u de {clientId}: {clientType}");

						// R�cup�rer le mot de passe si pr�sent (pour les clients BACKEND)
						string password = null;
						if (root.TryGetProperty("password", out JsonElement passwordElement))
						{
							password = passwordElement.GetString();
							Console.WriteLine($"?? Mot de passe fourni par {clientId} pour authentification BACKEND");
						}

						// Transf�rer au ServerManager pour traitement avec le mot de passe
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
			// Retransmet le mouvement aux autres clients (crypt�)
			BroadcastToOtherClients(clientId, content, encrypt: true);
		}

		/// <summary>
		/// Traite les messages de chat
		/// </summary>
		private void HandleChatMessage(string clientId, string content)
		{
			Console.WriteLine($"?? Chat de {clientId}: {content}");
			// Retransmet le message de chat � tous les clients (crypt�)
			BroadcastToAllClients($"CHAT_RELAY:{clientId}:{content}", encrypt: true);
		}

		/// <summary>
		/// Traite les mises � jour d'�tat de jeu
		/// </summary>
		private void HandleGameStateUpdate(string clientId, string content)
		{
			Console.WriteLine($"?? Mise � jour d'�tat de {clientId}: {content}");
			// Traite la mise � jour d'�tat du jeu...
		}

		/// <summary>
		/// Traite les informations du client
		/// </summary>
		private void HandleClientInfo(string clientId, string content)
		{
			Console.WriteLine($"?? Informations du client {clientId}: {content}");
			// R�pond avec les informations du serveur (crypt�)
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
			// R�pond avec un pong (crypt�)
			SendMessageToClient(clientId, "PONG", encrypt: true);
		}

		/// <summary>
		/// Traite les messages de test de cryptage
		/// </summary>
		private void HandleCryptoTestMessage(string clientId, string content)
		{
			Console.WriteLine($"?? Test de cryptage de {clientId}: {content}");
			// R�pond avec un message de test crypt�
			SendMessageToClient(clientId, "CRYPTO_RESPONSE:Message de test crypt� du serveur", encrypt: true);
		}

		/// <summary>
		/// Traite les messages g�n�riques
		/// </summary>
		private void HandleGenericMessage(string clientId, string content)
		{
			Console.WriteLine($"?? Message g�n�rique de {clientId}: {content}");
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
		/// Envoie un message � un client sp�cifique avec cryptage optionnel
		/// </summary>
		/// <param name="clientId">ID du client</param>
		/// <param name="message">Message � envoyer</param>
		/// <param name="encrypt">Si true, crypte le message avant envoi</param>
		public async void SendMessageToClient(string clientId, string message, bool encrypt = true)
		{
			bool success = await MessageReceiver.GetInstance.SendMessageToClient(clientId, message, encrypt);
			if (_debugMode && !success)
			{
				Console.WriteLine($"? �chec envoi message � {clientId}");
			}
			else if (_debugMode && encrypt)
			{
				Console.WriteLine($"?? Message crypt� envoy� � {clientId}");
			}
		}

		/// <summary>
		/// Diffuse un message � tous les clients avec cryptage optionnel
		/// </summary>
		/// <param name="message">Message � diffuser</param>
		/// <param name="encrypt">Si true, crypte le message avant envoi</param>
		public async void BroadcastToAllClients(string message, bool encrypt = true)
		{
			await MessageReceiver.GetInstance.BroadcastMessage(message, encrypt);
			if (_debugMode)
			{
				string status = encrypt ? "crypt�" : "clair";
				Console.WriteLine($"?? Message {status} diffus�: {message}");
			}
		}

		/// <summary>
		/// Diffuse un message � tous les clients sauf l'exp�diteur
		/// </summary>
		/// <param name="senderClientId">ID de l'exp�diteur � exclure</param>
		/// <param name="message">Message � diffuser</param>
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
				string status = encrypt ? "crypt�" : "clair";
				Console.WriteLine($"?? Message {status} diffus� � {clients.Count - 1} autres clients");
			}
		}

		/// <summary>
		/// D�connecte un client sp�cifique
		/// </summary>
		public async void DisconnectClient(string clientId)
		{
			await MessageReceiver.GetInstance.RemoveClient(clientId);
			Console.WriteLine($"?? Client {clientId} d�connect� par le serveur");
			EmitSignal(SignalName.ClientDisconnected, clientId);
		}
		#endregion

		#region Server Information
		/// <summary>
		/// Obtient le nombre de clients connect�s
		/// </summary>
		public int GetConnectedClientCount()
		{
			return MessageReceiver.GetInstance.GetConnectedClientIds().Count;
		}

		/// <summary>
		/// Obtient l'�tat complet du serveur incluant les informations r�seau et clients
		/// </summary>
		/// <returns>Un objet contenant l'�tat du serveur</returns>
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
		/// Obtient l'�tat complet du jeu depuis la MainGameScene
		/// </summary>
		/// <returns>Un objet contenant l'�tat complet du jeu</returns>
		public object GetCompleteGameState()
		{
			var serverState = GetServerState();
			object gameSceneState = null;

			// Obtenir l'�tat de la sc�ne de jeu depuis la MainGameScene
			if (_mainGameScene != null)
			{
				try
				{
					gameSceneState = _mainGameScene.GetGameSceneState();
				}
				catch (Exception ex)
				{
					Console.WriteLine($"? Erreur lors de la r�cup�ration de l'�tat de la sc�ne: {ex.Message}");
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
		/// Affiche les statistiques du syst�me avec informations de cryptage
		/// </summary>
		private void DisplayStatistics()
		{
			if (_debugMode)
			{
				var stats = MessageReceiver.GetInstance.GetStatistics();
				var encInfo = MessageReceiver.GetInstance.GetEncryptionInfo();

				Console.WriteLine($"=== STATISTIQUES R�SEAU ===");
				Console.WriteLine($"?? Serveur actif: {stats.isRunning}");
				Console.WriteLine($"?? Clients connect�s: {stats.connectedClients}");
				Console.WriteLine($"?? Messages en attente: {stats.pendingMessages}");
				Console.WriteLine($"?? Cryptage: {(stats.encryptionEnabled ? "ACTIV�" : "D�SACTIV�")}");
				Console.WriteLine($"?? Mode: Ordre d'arriv�e (FIFO)");
				if (stats.encryptionEnabled)
				{
					Console.WriteLine($"?? Cl�: {encInfo.keyBase64.Substring(0, 10)}...");
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
			Console.WriteLine($"?? Mode debug: {(_debugMode ? "ACTIV�" : "D�SACTIV�")}");
		}

		/// <summary>
		/// Traite les messages en mode haute fr�quence
		/// </summary>
		public void ProcessMessagesHighFrequency()
		{
			// Traite tous les messages disponibles imm�diatement
			while (MessageReceiver.GetInstance.HasPendingMessages())
			{
				ProcessNextMessage();
			}
			Console.WriteLine("? Traitement haute fr�quence ex�cut�");
		}

		/// <summary>
		/// M�thode alternative pour r�cup�rer un nombre limit� de messages
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
			Console.WriteLine($"?? Traitement limit� � {maxMessages} messages");
		}

		/// <summary>
		/// Affiche la liste des clients connect�s
		/// </summary>
		public void ListConnectedClients()
		{
			var clients = MessageReceiver.GetInstance.GetConnectedClientIds();
			Console.WriteLine($"?? Clients connect�s: {string.Join(", ", clients)}");
		}
		#endregion

		#region Server Event Handlers
		private void OnServerStarted()
		{
			GD.Print("?? GameServerHandler: Serveur d�marr� avec succ�s!");
			EmitSignal(SignalName.ServerStarted);
		}

		private void OnServerStopped()
		{
			GD.Print("?? GameServerHandler: Serveur arr�t�");
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
			// D�connecter les �v�nements du serveur
			if (_serverManager != null)
			{
				_serverManager.ServerStarted -= OnServerStarted;
				_serverManager.ServerStopped -= OnServerStopped;
				_serverManager.ServerError -= OnServerError;
			}
			
			Console.WriteLine("?? GameServerHandler: Nettoyage des ressources de cryptage");
			
			// Nettoie les ressources quand la sc�ne se ferme
			_messageProcessingTimer?.QueueFree();
			_statisticsTimer?.QueueFree();
			
			Console.WriteLine("?? GameServerHandler: Nettoyage termin�");
		}
		#endregion
	}
}