using Godot;
using Satsuki;
using Satsuki.Networks;
using Satsuki.Utils;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using Satsuki.Interfaces;

public partial class MainGameScene : Node
{
	private ServerManager _serverManager;
	private IScene _currentScene;
	private bool _debugMode = true;

	public override void _Ready()
	{
		// Récupérer le ServerManager via AutoLoad
		_serverManager = GetNodeOrNull<ServerManager>("/root/ServerManager");

		if (_serverManager == null)
		{
			GD.PrintErr("❌ ServerManager non trouvé via AutoLoad! Démarrage manuel...");
			// Démarrage manuel du serveur
			try
			{
				var network = Network.GetInstance;
				if (network.Start())
				{
					GD.Print("✅ Serveur démarré manuellement avec succès!");
				}
				else
				{
					GD.PrintErr("❌ Échec du démarrage manuel du serveur");
				}
			}
			catch (System.Exception ex)
			{
				GD.PrintErr($"❌ Erreur lors du démarrage manuel: {ex.Message}");
			}
		}
		else
		{
			// Connecter les événements du ServerManager
			_serverManager.ServerStarted += OnServerStarted;
			_serverManager.ServerStopped += OnServerStopped;
			_serverManager.ServerError += OnServerError;

			GD.Print("🎮 MainGameScene: Connecté au ServerManager");
		}

		// Teste le système de cryptage au démarrage
		TestCryptographySystem();
		/*
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

		Console.WriteLine("🔄 MainGameScene: Système de réception multithread initialisé avec cryptage");
	}

	/// <summary>
	/// Teste le système de cryptage au démarrage
	/// </summary>
	private void TestCryptographySystem()
	{
		Console.WriteLine("🔧 Test du système de cryptage...");
		bool testResult = MessageCrypto.TestEncryption();

		if (testResult)
		{
			Console.WriteLine("✅ Système de cryptage opérationnel");
		}
		else
		{
			Console.WriteLine("❌ Problème avec le système de cryptage");
		}

		// Affiche les informations sur les clés par défaut
		var keyInfo = MessageCrypto.GetDefaultKeyInfo();
		Console.WriteLine($"🔑 Clé par défaut: {keyInfo.keyBase64.Substring(0, 10)}...");
		Console.WriteLine($"🔒 IV par défaut: {keyInfo.ivBase64.Substring(0, 10)}...");
	}

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
	/// Affiche les statistiques du système avec informations de cryptage
	/// </summary>
	private void DisplayStatistics()
	{
		if (_debugMode)
		{
			var stats = MessageReceiver.GetInstance.GetStatistics();
			var encInfo = MessageReceiver.GetInstance.GetEncryptionInfo();

			Console.WriteLine($"=== STATISTIQUES RÉSEAU ===");
			Console.WriteLine($"🟢 Serveur actif: {stats.isRunning}");
			Console.WriteLine($"👥 Clients connectés: {stats.connectedClients}");
			Console.WriteLine($"📬 Messages en attente: {stats.pendingMessages}");
			Console.WriteLine($"🔐 Cryptage: {(stats.encryptionEnabled ? "ACTIVÉ" : "DÉSACTIVÉ")}");
			Console.WriteLine($"📋 Mode: Ordre d'arrivée (FIFO)");
			if (stats.encryptionEnabled)
			{
				Console.WriteLine($"🔑 Clé: {encInfo.keyBase64.Substring(0, 10)}...");
			}
			Console.WriteLine($"========================");
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
					Console.WriteLine($"📥 Type de client reçu de {clientId}: {clientType}");

					// Récupérer le mot de passe si présent (pour les clients BACKEND)
					string password = null;
					if (root.TryGetProperty("password", out JsonElement passwordElement))
					{
						password = passwordElement.GetString();
						Console.WriteLine($"🔑 Mot de passe fourni par {clientId} pour authentification BACKEND");
					}

					// Transférer au ServerManager pour traitement avec le mot de passe
					_serverManager?.HandleClientTypeResponse(clientId, clientType, password);
				}
			}
		}
		catch (JsonException ex)
		{
			Console.WriteLine($"❌ Erreur lors du parsing JSON de {clientId}: {ex.Message}");
		}
	}

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

	/// <summary>
	/// Traite les mouvements de joueur
	/// </summary>
	private void HandlePlayerMovement(string clientId, string content)
	{
		Console.WriteLine($"🎮 Mouvement du joueur {clientId}: {content}");

		// Retransmet le mouvement aux autres clients (crypté)
		BroadcastToOtherClients(clientId, content, encrypt: true);
	}

	/// <summary>
	/// Traite les messages de chat
	/// </summary>
	private void HandleChatMessage(string clientId, string content)
	{
		Console.WriteLine($"💬 Chat de {clientId}: {content}");

		// Retransmet le message de chat à tous les clients (crypté)
		BroadcastToAllClients($"CHAT_RELAY:{clientId}:{content}", encrypt: true);
	}

	/// <summary>
	/// Traite les mises à jour d'état de jeu
	/// </summary>
	private void HandleGameStateUpdate(string clientId, string content)
	{
		Console.WriteLine($"🔄 Mise à jour d'état de {clientId}: {content}");

		// Traite la mise à jour d'état du jeu...
	}

	/// <summary>
	/// Traite les informations du client
	/// </summary>
	private void HandleClientInfo(string clientId, string content)
	{
		Console.WriteLine($"ℹ️ Informations du client {clientId}: {content}");

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
			Console.WriteLine($"🏓 Ping de {clientId}: {content}");
		}

		// Répond avec un pong (crypté)
		SendMessageToClient(clientId, "PONG", encrypt: true);
	}

	/// <summary>
	/// Traite les messages de test de cryptage
	/// </summary>
	private void HandleCryptoTestMessage(string clientId, string content)
	{
		Console.WriteLine($"🔐 Test de cryptage de {clientId}: {content}");

		// Répond avec un message de test crypté
		SendMessageToClient(clientId, "CRYPTO_RESPONSE:Message de test crypté du serveur", encrypt: true);
	}

	/// <summary>
	/// Traite les messages génériques
	/// </summary>
	private void HandleGenericMessage(string clientId, string content)
	{
		Console.WriteLine($"📝 Message générique de {clientId}: {content}");
	}

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
			Console.WriteLine($"❌ Échec envoi message à {clientId}");
		}
		else if (_debugMode && encrypt)
		{
			Console.WriteLine($"🔐 Message crypté envoyé à {clientId}");
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
			Console.WriteLine($"📢 Message {status} diffusé: {message}");
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
			Console.WriteLine($"📡 Message {status} diffusé à {clients.Count - 1} autres clients");
		}
	}

	/// <summary>
	/// Obtient le nombre de clients connectés
	/// </summary>
	public int GetConnectedClientCount()
	{
		return MessageReceiver.GetInstance.GetConnectedClientIds().Count;
	}

	/// <summary>
	/// Obtient l'état complet du jeu incluant les informations serveur et clients
	/// </summary>
	/// <returns>Un objet contenant l'état du jeu</returns>
	public object GetGameState()
	{
		var stats = MessageReceiver.GetInstance.GetStatistics();
		var encInfo = MessageReceiver.GetInstance.GetEncryptionInfo();
		var connectedClients = MessageReceiver.GetInstance.GetConnectedClientIds();
		var network = Network.GetInstance;

		// Récupérer la scène actuelle
		var currentScene = GetTree().CurrentScene;
		string sceneName = currentScene?.Name ?? "Unknown";
		string scenePath = currentScene?.SceneFilePath ?? "Unknown";

		// Essayer d'obtenir l'état de la scène si elle a une méthode GetSceneState
		object sceneState = null;
		if (currentScene != null)
		{
			// Utiliser la réflexion pour appeler GetSceneState si elle existe
			var sceneType = currentScene.GetType();
			var getSceneStateMethod = sceneType.GetMethod("GetSceneState",
				System.Reflection.BindingFlags.Public |
				System.Reflection.BindingFlags.Instance);

			if (getSceneStateMethod != null)
			{
				try
				{
					sceneState = getSceneStateMethod.Invoke(currentScene, null);
					Console.WriteLine($"✅ État de la scène {sceneName} récupéré");
				}
				catch (Exception ex)
				{
					Console.WriteLine($"❌ Erreur lors de la récupération de l'état de la scène: {ex.Message}");
					sceneState = new { Error = "Failed to get scene state", Message = ex.Message };
				}
			}
			else
			{
				sceneState = new { Info = "Scene does not implement GetSceneState()" };
				Console.WriteLine($"ℹ️ La scène {sceneName} n'implémente pas GetSceneState()");
			}
		}

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
			},
			Scene = new
			{
				CurrentScene = sceneName,
				ScenePath = scenePath,
				SceneState = sceneState
			}
		};
	}

	/// <summary>
	/// Déconnecte un client spécifique
	/// </summary>
	public async void DisconnectClient(string clientId)
	{
		await MessageReceiver.GetInstance.RemoveClient(clientId);
		Console.WriteLine($"🔌 Client {clientId} déconnecté par le serveur");
	}

	/// <summary>
	/// Méthode alternative pour récupérer un nombre limité de messages
	/// </summary>
	private void ProcessLimitedMessages(int maxMessages = 10)
	{
		if (MessageReceiver.GetInstance.HasPendingMessages())
		{
			List<Message> messages = MessageReceiver.GetInstance.GetMessagesByArrivalOrder(maxMessages, decryptMessages: true);

			foreach (var message in messages)
			{
				HandleMessage(message);
			}
		}
	}

	/// <summary>
	/// Traite les messages en mode haute fréquence
	/// </summary>
	private void ProcessMessagesHighFrequency()
	{
		// Traite tous les messages disponibles immédiatement
		while (MessageReceiver.GetInstance.HasPendingMessages())
		{
			ProcessNextMessage();
		}
	}

	/// <summary>
	/// Commandes Input pour tests et debug avec fonctionnalités de cryptage
	/// </summary>
	public override void _Input(InputEvent @event)
	{
		if (@event is InputEventKey keyEvent && keyEvent.Pressed)
		{
			switch (keyEvent.Keycode)
			{
				case Key.F1:
					// Test d'envoi de message crypté à tous les clients
					BroadcastToAllClients("SERVER_BROADCAST:Message de test crypté du serveur", encrypt: true);
					break;
				case Key.F2:
					// Affiche les statistiques avec informations de cryptage
					DisplayStatistics();
					break;
				case Key.F3:
					// Liste des clients connectés avec leurs types
					var clients = MessageReceiver.GetInstance.GetConnectedClientIds();
					Console.WriteLine($"👥 Clients connectés: {string.Join(", ", clients)}");
					break;
				case Key.F4:
					// Bascule le mode debug
					_debugMode = !_debugMode;
					Console.WriteLine($"🐛 Mode debug: {(_debugMode ? "ACTIVÉ" : "DÉSACTIVÉ")}");
					break;
				case Key.F5:
					// Simule un message de chat crypté du serveur
					BroadcastToAllClients("CHAT:SERVER:Message crypté du serveur à tous les joueurs", encrypt: true);
					break;
				case Key.F6:
					// Traite tous les messages disponibles immédiatement
					while (MessageReceiver.GetInstance.HasPendingMessages())
					{
						ProcessIncomingMessages(1);
					}
					Console.WriteLine("⚡ Traitement haute fréquence exécuté");
					break;
				case Key.F7:
					// Traite seulement les 5 prochains messages
					ProcessIncomingMessages(5);
					Console.WriteLine("🔢 Traitement limité à 5 messages");
					break;
				case Key.F8:
					// Bascule le cryptage on/off
					var encInfo = MessageReceiver.GetInstance.GetEncryptionInfo();
					MessageReceiver.GetInstance.ConfigureEncryption(!encInfo.enabled);
					Console.WriteLine($"🔄 Cryptage basculé: {(!encInfo.enabled ? "ACTIVÉ" : "DÉSACTIVÉ")}");
					break;
				case Key.F9:
					// Génère une nouvelle clé de cryptage
					MessageReceiver.GetInstance.GenerateNewEncryptionKey();
					Console.WriteLine("🔑 Nouvelle clé de cryptage générée");
					break;
				case Key.F10:
					// Test de cryptage manuel
					TestCryptographySystem();
					break;
			}
		}
	}

	public async void ChangeScene()
	{
		GetTree().ChangeSceneToFile("res://Scenes/OtherScene.tscn");
	}

	private void OnServerStarted()
	{
		GD.Print("🎮 MainGameScene: Serveur démarré avec succès!");

		// Le serveur est maintenant prêt, on peut activer les fonctionnalités réseau
		SetNetworkUIEnabled(true);
	}

	private void OnServerStopped()
	{
		GD.Print("🎮 MainGameScene: Serveur arrêté");
		SetNetworkUIEnabled(false);
	}

	private void OnServerError(string error)
	{
		GD.PrintErr($"🎮 MainGameScene: Erreur serveur - {error}");
		// Optionnel: afficher une notification à l'utilisateur
		ShowNetworkError(error);
	}

	private void SetNetworkUIEnabled(bool enabled)
	{
		// Activer/désactiver les éléments UI liés au réseau
		// Par exemple, boutons multijoueur, indicateurs de statut, etc.
		GD.Print($"📡 Interface réseau: {(enabled ? "Activée" : "Désactivée")}");
	}

	private void ShowNetworkError(string error)
	{
		// Afficher une notification d'erreur réseau
		GD.PrintErr($"🚨 Erreur réseau: {error}");
	}

	public override void _ExitTree()
	{
		// Déconnecter les événements du serveur
		if (_serverManager != null)
		{
			_serverManager.ServerStarted -= OnServerStarted;
			_serverManager.ServerStopped -= OnServerStopped;
			_serverManager.ServerError -= OnServerError;
		}
		Console.WriteLine("🎮 MainGameScene: Nettoyage des ressources de cryptage");
		// Nettoie les ressources quand la scène se ferme
		_messageProcessingTimer?.QueueFree();
		_statisticsTimer?.QueueFree();
		Console.WriteLine("🧹 MainGameScene: Nettoyage des ressources de cryptage");
	}
}
