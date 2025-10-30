using Godot;
using Satsuki;
using Satsuki.Networks;
using Satsuki.Utils;
using System;
using System.Collections.Generic;

public partial class MainGameScene : Node
{
	private Timer _messageProcessingTimer;
	private Timer _statisticsTimer;
	Node currentScene;
	private bool _debugMode = true;
	
	public override void _Ready()
	{
		currentScene = GetNode<Node>("QuestionAnswerQuizzScene");
		// Teste le système de cryptage au démarrage
		TestCryptographySystem();
		
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
			List<Message> messages = maxMessages > 0 
				? MessageReceiver.GetInstance.GetMessagesByArrivalOrder(maxMessages, decryptMessages: true)
				: MessageReceiver.GetInstance.GetMessagesByArrivalOrder(decryptMessages: true);
			
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
		Console.WriteLine($"🎯 Mise à jour d'état de {clientId}: {content}");
		
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
	/// Déconnecte un client spécifique
	/// </summary>
	public async void DisconnectClient(string clientId)
	{
		await MessageReceiver.GetInstance.RemoveClient(clientId);
		Console.WriteLine($"🚪 Client {clientId} déconnecté par le serveur");
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
					// Liste des clients connectés
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
		GetTree().ChangeSceneToFile(
			"res://Scenes/OtherScene.tscn"
		);
	}

	public override void _ExitTree()
	{
		// Nettoie les ressources quand la scène se ferme
		_messageProcessingTimer?.QueueFree();
		_statisticsTimer?.QueueFree();
		Console.WriteLine("🧹 MainGameScene: Nettoyage des ressources de cryptage");
	}
}
