using Godot;
using Satsuki;
using Satsuki.Networks;
using Satsuki.Utils;
using System;
using System.Collections.Generic;

public partial class MainGameScene : Node
{
	private ServerManager _serverManager;
	private bool _debugMode = true;
	
	public override void _Ready()
	{
		//currentScene = GetNode<Node>("QuestionAnswerQuizzScene");
		
		// Essayer de récupérer le ServerManager via AutoLoad
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
		
		// Récupérer le serveur global (démarré automatiquement)
		_serverManager = GetNode<ServerManager>("/root/ServerManager");
		
		if (_serverManager != null)
		{
			// Écouter les événements du serveur
			_serverManager.ServerStarted += OnServerStarted;
			_serverManager.ServerStopped += OnServerStopped;
			_serverManager.ServerError += OnServerError;
			
			GD.Print("🎮 MainGameScene: Connecté au ServerManager");
		}
		else
		{
			GD.PrintErr("❌ ServerManager non trouvé! Vérifiez la configuration AutoLoad.");
		}
		
		// Teste le système de cryptage au démarrage
		TestCryptographySystem();
		/*
		// Configure un timer pour traiter les messages périodiquement
		_messageProcessingTimer = new Timer();
		_messageProcessingTimer.WaitTime = 0.1; // Traite les messages toutes les 100ms
		_messageProcessingTimer.Timeout += ProcessIncomingMessages;
		_messageProcessingTimer.Autostart = true;
		AddChild(_messageProcessingTimer);

		// Timer pour afficher les statistiques
		_statisticsTimer = new Timer();
		_statisticsTimer.WaitTime = 5.0; // Affiche les stats toutes les 5 secondes
		_statisticsTimer.Timeout += DisplayStatistics;
		_statisticsTimer.Autostart = true;
		AddChild(_statisticsTimer);
		*/
		Console.WriteLine("?? MainGameScene: Système de réception multithread initialisé avec cryptage");
	}

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
	/// Traite les messages entrants du MessageReceiver avec décryptage automatique
	/// </summary>
	private void ProcessIncomingMessages()
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
	/// Traite les messages un par un avec décryptage automatique
	/// </summary>
	private void ProcessNextMessage()
	{
		Message nextMessage = MessageReceiver.GetInstance.GetNextMessage(decryptMessage: true);
		if (nextMessage != null)
		{
			HandleMessage(nextMessage);
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
		if (content.StartsWith("PLAYER_MOVE:"))
		{
			HandlePlayerMovement(clientId, content);
		}
		else if (content.StartsWith("CHAT:"))
		{
			HandleChatMessage(clientId, content);
		}
		else if (content.StartsWith("GAME_STATE:"))
		{
			HandleGameStateUpdate(clientId, content);
		}
		else if (content.StartsWith("CLIENT_INFO:"))
		{
			HandleClientInfo(clientId, content);
		}
		else if (content.StartsWith("PING"))
		{
			HandlePingMessage(clientId, content);
		}
		else if (content.StartsWith("CRYPTO_TEST:"))
		{
			HandleCryptoTestMessage(clientId, content);
		}
		else
		{
			HandleGenericMessage(clientId, content);
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
		Console.WriteLine($"?? Client {clientId} déconnecté par le serveur");
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
					// Liste des clients connectés
					var clients = MessageReceiver.GetInstance.GetConnectedClientIds();
					Console.WriteLine($"?? Clients connectés: {string.Join(", ", clients)}");
					break;
				case Key.F4:
					// Bascule le mode debug
					_debugMode = !_debugMode;
					Console.WriteLine($"?? Mode debug: {(_debugMode ? "ACTIVÉ" : "DÉSACTIVÉ")}");
					break;
				case Key.F5:
					// Simule un message de chat crypté du serveur
					BroadcastToAllClients("CHAT:SERVER:Message crypté du serveur à tous les joueurs", encrypt: true);
					break;
				case Key.F6:
					// Traite les messages en mode haute fréquence
					ProcessMessagesHighFrequency();
					Console.WriteLine("? Traitement haute fréquence exécuté");
					break;
				case Key.F7:
					// Traite seulement les 5 prochains messages
					ProcessLimitedMessages(5);
					Console.WriteLine("?? Traitement limité à 5 messages");
					break;
				case Key.F8:
					// Bascule le cryptage on/off
					var encInfo = MessageReceiver.GetInstance.GetEncryptionInfo();
					MessageReceiver.GetInstance.ConfigureEncryption(!encInfo.enabled);
					Console.WriteLine($"?? Cryptage basculé: {(!encInfo.enabled ? "ACTIVÉ" : "DÉSACTIVÉ")}");
					break;
				case Key.F9:
					// Génère une nouvelle clé de cryptage
					MessageReceiver.GetInstance.GenerateNewEncryptionKey();
					Console.WriteLine("?? Nouvelle clé de cryptage générée");
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
	}
}
