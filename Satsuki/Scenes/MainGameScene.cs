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
	private bool _debugMode = true;
	
	public override void _Ready()
	{
		// Teste le syst�me de cryptage au d�marrage
		TestCryptographySystem();
		
		// Configure un timer pour traiter les messages p�riodiquement
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

		Console.WriteLine("?? MainGameScene: Syst�me de r�ception multithread initialis� avec cryptage");
	}

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
	/// Traite les messages entrants du MessageReceiver avec d�cryptage automatique
	/// </summary>
	private void ProcessIncomingMessages()
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
	/// Traite les messages un par un avec d�cryptage automatique
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
		
		// Traitement bas� sur le contenu du message
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
	/// Obtient le nombre de clients connect�s
	/// </summary>
	public int GetConnectedClientCount()
	{
		return MessageReceiver.GetInstance.GetConnectedClientIds().Count;
	}

	/// <summary>
	/// D�connecte un client sp�cifique
	/// </summary>
	public async void DisconnectClient(string clientId)
	{
		await MessageReceiver.GetInstance.RemoveClient(clientId);
		Console.WriteLine($"?? Client {clientId} d�connect� par le serveur");
	}

	/// <summary>
	/// M�thode alternative pour r�cup�rer un nombre limit� de messages
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
	/// Traite les messages en mode haute fr�quence
	/// </summary>
	private void ProcessMessagesHighFrequency()
	{
		// Traite tous les messages disponibles imm�diatement
		while (MessageReceiver.GetInstance.HasPendingMessages())
		{
			ProcessNextMessage();
		}
	}

	/// <summary>
	/// Commandes Input pour tests et debug avec fonctionnalit�s de cryptage
	/// </summary>
	public override void _Input(InputEvent @event)
	{
		if (@event is InputEventKey keyEvent && keyEvent.Pressed)
		{
			switch (keyEvent.Keycode)
			{
				case Key.F1:
					// Test d'envoi de message crypt� � tous les clients
					BroadcastToAllClients("SERVER_BROADCAST:Message de test crypt� du serveur", encrypt: true);
					break;
				case Key.F2:
					// Affiche les statistiques avec informations de cryptage
					DisplayStatistics();
					break;
				case Key.F3:
					// Liste des clients connect�s
					var clients = MessageReceiver.GetInstance.GetConnectedClientIds();
					Console.WriteLine($"?? Clients connect�s: {string.Join(", ", clients)}");
					break;
				case Key.F4:
					// Bascule le mode debug
					_debugMode = !_debugMode;
					Console.WriteLine($"?? Mode debug: {(_debugMode ? "ACTIV�" : "D�SACTIV�")}");
					break;
				case Key.F5:
					// Simule un message de chat crypt� du serveur
					BroadcastToAllClients("CHAT:SERVER:Message crypt� du serveur � tous les joueurs", encrypt: true);
					break;
				case Key.F6:
					// Traite les messages en mode haute fr�quence
					ProcessMessagesHighFrequency();
					Console.WriteLine("? Traitement haute fr�quence ex�cut�");
					break;
				case Key.F7:
					// Traite seulement les 5 prochains messages
					ProcessLimitedMessages(5);
					Console.WriteLine("?? Traitement limit� � 5 messages");
					break;
				case Key.F8:
					// Bascule le cryptage on/off
					var encInfo = MessageReceiver.GetInstance.GetEncryptionInfo();
					MessageReceiver.GetInstance.ConfigureEncryption(!encInfo.enabled);
					Console.WriteLine($"?? Cryptage bascul�: {(!encInfo.enabled ? "ACTIV�" : "D�SACTIV�")}");
					break;
				case Key.F9:
					// G�n�re une nouvelle cl� de cryptage
					MessageReceiver.GetInstance.GenerateNewEncryptionKey();
					Console.WriteLine("?? Nouvelle cl� de cryptage g�n�r�e");
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
		// Nettoie les ressources quand la sc�ne se ferme
		_messageProcessingTimer?.QueueFree();
		_statisticsTimer?.QueueFree();
		Console.WriteLine("?? MainGameScene: Nettoyage des ressources de cryptage");
	}
}
