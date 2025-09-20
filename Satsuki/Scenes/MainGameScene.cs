using Godot;
using Satsuki;
using Satsuki.Networks;
using Satsuki.Utils;
using System;
using System.Collections.Generic;

public partial class MainGameScene : Node
{
	private Timer _messageProcessingTimer;
	private bool _debugEncryption = true; // Active les logs de debug pour le cryptage
	
	public override void _Ready()
	{
		// Configure le cryptage au d�marrage
		InitializeEncryption();
		
		// Configure un timer pour traiter les messages p�riodiquement
		_messageProcessingTimer = new Timer();
		_messageProcessingTimer.WaitTime = 0.1; // Traite les messages toutes les 100ms
		_messageProcessingTimer.Timeout += ProcessIncomingMessages;
		_messageProcessingTimer.Autostart = true;
		AddChild(_messageProcessingTimer);

		// Affiche les informations de cryptage
		DisplayEncryptionInfo();
	}

	/// <summary>
	/// Initialise la configuration de cryptage
	/// </summary>
	private void InitializeEncryption()
	{
		// Active le cryptage avec g�n�ration d'une nouvelle cl�
		MessageHandler.GetInstance.ConfigureEncryption(enabled: true);
		
		// Optionnel: g�n�re une nouvelle cl� al�atoire pour cette session
		// MessageHandler.GetInstance.GenerateNewEncryptionKey();
		
		Console.WriteLine("MainGameScene: Syst�me de cryptage initialis�");
	}

	/// <summary>
	/// Affiche les informations de cryptage actuelles
	/// </summary>
	private void DisplayEncryptionInfo()
	{
		var encInfo = MessageHandler.GetInstance.GetEncryptionInfo();
		Console.WriteLine("=== INFORMATIONS DE CRYPTAGE ===");
		Console.WriteLine($"Statut: {(encInfo.enabled ? "ACTIV�" : "D�SACTIV�")}");
		Console.WriteLine($"Cl�: {encInfo.keyBase64}");
		Console.WriteLine($"IV: {encInfo.ivBase64}");
		Console.WriteLine("===============================");
	}

	/// <summary>
	/// Traite les messages entrants du MessageHandler
	/// </summary>
	private void ProcessIncomingMessages()
	{
		if (MessageHandler.GetInstance.HasPendingMessages())
		{
			// R�cup�re tous les messages tri�s par timestamp avec d�cryptage automatique
			List<Message> messages = MessageHandler.GetInstance.GetMessagesByTimestamp(decryptMessages: true);
			
			foreach (var message in messages)
			{
				HandleMessage(message);
			}
		}
	}

	/// <summary>
	/// Traite un message individuel
	/// </summary>
	/// <param name="message">Message � traiter</param>
	private void HandleMessage(Message message)
	{
		if (_debugEncryption)
		{
			Console.WriteLine($"[{message.Timestamp:HH:mm:ss.fff}] Message trait�: {message.Content}");
			Console.WriteLine($"�tat du message: {(message.IsEncrypted ? "CRYPT�" : "D�CRYPT�")}");
		}
		
		// Traitement bas� sur le contenu du message (maintenant d�crypt�)
		if (message.Content.StartsWith("PLAYER_MOVE:"))
		{
			HandlePlayerMovement(message.Content);
		}
		else if (message.Content.StartsWith("CHAT:"))
		{
			HandleChatMessage(message.Content);
		}
		else if (message.Content.StartsWith("GAME_STATE:"))
		{
			HandleGameStateUpdate(message.Content);
		}
		else if (message.Content.StartsWith("ENCRYPT_CMD:"))
		{
			HandleEncryptionCommand(message.Content);
		}
		else
		{
			HandleGenericMessage(message.Content);
		}
	}

	/// <summary>
	/// Traite les commandes de cryptage
	/// </summary>
	private void HandleEncryptionCommand(string content)
	{
		Console.WriteLine($"Commande de cryptage re�ue: {content}");
		
		// Exemple de commandes:
		// ENCRYPT_CMD:ENABLE - Active le cryptage
		// ENCRYPT_CMD:DISABLE - D�sactive le cryptage
		// ENCRYPT_CMD:NEW_KEY - G�n�re une nouvelle cl�
		
		string[] parts = content.Split(':');
		if (parts.Length >= 2)
		{
			switch (parts[1].ToUpper())
			{
				case "ENABLE":
					MessageHandler.GetInstance.ConfigureEncryption(true);
					Console.WriteLine("Cryptage activ� via commande");
					break;
				case "DISABLE":
					MessageHandler.GetInstance.ConfigureEncryption(false);
					Console.WriteLine("Cryptage d�sactiv� via commande");
					break;
				case "NEW_KEY":
					MessageHandler.GetInstance.GenerateNewEncryptionKey();
					Console.WriteLine("Nouvelle cl� de cryptage g�n�r�e via commande");
					DisplayEncryptionInfo();
					break;
				default:
					Console.WriteLine($"Commande de cryptage inconnue: {parts[1]}");
					break;
			}
		}
	}

	/// <summary>
	/// Traite les mouvements de joueur
	/// </summary>
	private void HandlePlayerMovement(string content)
	{
		Console.WriteLine($"Mouvement de joueur re�u (d�crypt�): {content}");
		// Traitement du mouvement...
	}

	/// <summary>
	/// Traite les messages de chat
	/// </summary>
	private void HandleChatMessage(string content)
	{
		Console.WriteLine($"Message de chat re�u (d�crypt�): {content}");
		// Affichage du chat...
	}

	/// <summary>
	/// Traite les mises � jour d'�tat de jeu
	/// </summary>
	private void HandleGameStateUpdate(string content)
	{
		Console.WriteLine($"Mise � jour d'�tat re�ue (d�crypt�): {content}");
		// Mise � jour de l'�tat du jeu...
	}

	/// <summary>
	/// Traite les messages g�n�riques
	/// </summary>
	private void HandleGenericMessage(string content)
	{
		Console.WriteLine($"Message g�n�rique re�u (d�crypt�): {content}");
	}

	/// <summary>
	/// Envoie un message crypt� via Network
	/// </summary>
	/// <param name="messageContent">Contenu du message � envoyer</param>
	/// <param name="encrypt">Force le cryptage (true par d�faut)</param>
	public async void SendEncryptedMessage(string messageContent, bool encrypt = true)
	{
		if (Network.GetInstance != null)
		{
			bool success = await Network.GetInstance.SendMessage(messageContent, encrypt);
			if (success)
			{
				Console.WriteLine($"Message envoy� {(encrypt ? "crypt�" : "en clair")}: {messageContent}");
			}
			else
			{
				Console.WriteLine("�chec de l'envoi du message");
			}
		}
	}

	/// <summary>
	/// Exemple de m�thodes utilitaires pour tester le cryptage
	/// </summary>
	private void TestEncryption()
	{
		Console.WriteLine("=== TEST DE CRYPTAGE ===");
		
		// Test direct avec MessageCrypto
		string testMessage = "Message de test secret";
		string encrypted = MessageCrypto.Encrypt(testMessage);
		string decrypted = MessageCrypto.Decrypt(encrypted);
		
		Console.WriteLine($"Original: {testMessage}");
		Console.WriteLine($"Crypt�: {encrypted}");
		Console.WriteLine($"D�crypt�: {decrypted}");
		Console.WriteLine($"Succ�s: {testMessage == decrypted}");
		
		// Test avec objet Message
		var message = new Message("Test avec objet Message");
		Console.WriteLine($"Avant cryptage: {message}");
		
		message.Encrypt();
		Console.WriteLine($"Apr�s cryptage: {message}");
		
		message.Decrypt();
		Console.WriteLine($"Apr�s d�cryptage: {message}");
		
		Console.WriteLine("=== FIN TEST ===");
	}

	/// <summary>
	/// M�thode alternative pour r�cup�rer un nombre limit� de messages
	/// </summary>
	private void ProcessLimitedMessages(int maxMessages = 10)
	{
		if (MessageHandler.GetInstance.HasPendingMessages())
		{
			List<Message> messages = MessageHandler.GetInstance.GetMessagesByTimestamp(maxMessages, decryptMessages: true);
			
			foreach (var message in messages)
			{
				HandleMessage(message);
			}
		}
	}

	/// <summary>
	/// Active/d�sactive le debug de cryptage
	/// </summary>
	/// <param name="enabled">�tat du debug</param>
	public void SetEncryptionDebug(bool enabled)
	{
		_debugEncryption = enabled;
		Console.WriteLine($"Debug de cryptage: {(enabled ? "ACTIV�" : "D�SACTIV�")}");
	}

	/// <summary>
	/// Commande Input pour tester le cryptage (appelable depuis Godot)
	/// </summary>
	public override void _Input(InputEvent @event)
	{
		if (@event is InputEventKey keyEvent && keyEvent.Pressed)
		{
			switch (keyEvent.Keycode)
			{
				case Key.F1:
					TestEncryption();
					break;
				case Key.F2:
					DisplayEncryptionInfo();
					break;
				case Key.F3:
					MessageHandler.GetInstance.GenerateNewEncryptionKey();
					DisplayEncryptionInfo();
					break;
				case Key.F4:
					var encInfo = MessageHandler.GetInstance.GetEncryptionInfo();
					MessageHandler.GetInstance.ConfigureEncryption(!encInfo.enabled);
					Console.WriteLine($"Cryptage bascul�: {(!encInfo.enabled ? "ACTIV�" : "D�SACTIV�")}");
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
		Console.WriteLine("MainGameScene: Nettoyage des ressources de cryptage");
	}
}
