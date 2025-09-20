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
		// Configure le cryptage au démarrage
		InitializeEncryption();
		
		// Configure un timer pour traiter les messages périodiquement
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
		// Active le cryptage avec génération d'une nouvelle clé
		MessageHandler.GetInstance.ConfigureEncryption(enabled: true);
		
		// Optionnel: génère une nouvelle clé aléatoire pour cette session
		// MessageHandler.GetInstance.GenerateNewEncryptionKey();
		
		Console.WriteLine("MainGameScene: Système de cryptage initialisé");
	}

	/// <summary>
	/// Affiche les informations de cryptage actuelles
	/// </summary>
	private void DisplayEncryptionInfo()
	{
		var encInfo = MessageHandler.GetInstance.GetEncryptionInfo();
		Console.WriteLine("=== INFORMATIONS DE CRYPTAGE ===");
		Console.WriteLine($"Statut: {(encInfo.enabled ? "ACTIVÉ" : "DÉSACTIVÉ")}");
		Console.WriteLine($"Clé: {encInfo.keyBase64}");
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
			// Récupère tous les messages triés par timestamp avec décryptage automatique
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
	/// <param name="message">Message à traiter</param>
	private void HandleMessage(Message message)
	{
		if (_debugEncryption)
		{
			Console.WriteLine($"[{message.Timestamp:HH:mm:ss.fff}] Message traité: {message.Content}");
			Console.WriteLine($"État du message: {(message.IsEncrypted ? "CRYPTÉ" : "DÉCRYPTÉ")}");
		}
		
		// Traitement basé sur le contenu du message (maintenant décrypté)
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
		Console.WriteLine($"Commande de cryptage reçue: {content}");
		
		// Exemple de commandes:
		// ENCRYPT_CMD:ENABLE - Active le cryptage
		// ENCRYPT_CMD:DISABLE - Désactive le cryptage
		// ENCRYPT_CMD:NEW_KEY - Génère une nouvelle clé
		
		string[] parts = content.Split(':');
		if (parts.Length >= 2)
		{
			switch (parts[1].ToUpper())
			{
				case "ENABLE":
					MessageHandler.GetInstance.ConfigureEncryption(true);
					Console.WriteLine("Cryptage activé via commande");
					break;
				case "DISABLE":
					MessageHandler.GetInstance.ConfigureEncryption(false);
					Console.WriteLine("Cryptage désactivé via commande");
					break;
				case "NEW_KEY":
					MessageHandler.GetInstance.GenerateNewEncryptionKey();
					Console.WriteLine("Nouvelle clé de cryptage générée via commande");
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
		Console.WriteLine($"Mouvement de joueur reçu (décrypté): {content}");
		// Traitement du mouvement...
	}

	/// <summary>
	/// Traite les messages de chat
	/// </summary>
	private void HandleChatMessage(string content)
	{
		Console.WriteLine($"Message de chat reçu (décrypté): {content}");
		// Affichage du chat...
	}

	/// <summary>
	/// Traite les mises à jour d'état de jeu
	/// </summary>
	private void HandleGameStateUpdate(string content)
	{
		Console.WriteLine($"Mise à jour d'état reçue (décrypté): {content}");
		// Mise à jour de l'état du jeu...
	}

	/// <summary>
	/// Traite les messages génériques
	/// </summary>
	private void HandleGenericMessage(string content)
	{
		Console.WriteLine($"Message générique reçu (décrypté): {content}");
	}

	/// <summary>
	/// Envoie un message crypté via Network
	/// </summary>
	/// <param name="messageContent">Contenu du message à envoyer</param>
	/// <param name="encrypt">Force le cryptage (true par défaut)</param>
	public async void SendEncryptedMessage(string messageContent, bool encrypt = true)
	{
		if (Network.GetInstance != null)
		{
			bool success = await Network.GetInstance.SendMessage(messageContent, encrypt);
			if (success)
			{
				Console.WriteLine($"Message envoyé {(encrypt ? "crypté" : "en clair")}: {messageContent}");
			}
			else
			{
				Console.WriteLine("Échec de l'envoi du message");
			}
		}
	}

	/// <summary>
	/// Exemple de méthodes utilitaires pour tester le cryptage
	/// </summary>
	private void TestEncryption()
	{
		Console.WriteLine("=== TEST DE CRYPTAGE ===");
		
		// Test direct avec MessageCrypto
		string testMessage = "Message de test secret";
		string encrypted = MessageCrypto.Encrypt(testMessage);
		string decrypted = MessageCrypto.Decrypt(encrypted);
		
		Console.WriteLine($"Original: {testMessage}");
		Console.WriteLine($"Crypté: {encrypted}");
		Console.WriteLine($"Décrypté: {decrypted}");
		Console.WriteLine($"Succès: {testMessage == decrypted}");
		
		// Test avec objet Message
		var message = new Message("Test avec objet Message");
		Console.WriteLine($"Avant cryptage: {message}");
		
		message.Encrypt();
		Console.WriteLine($"Après cryptage: {message}");
		
		message.Decrypt();
		Console.WriteLine($"Après décryptage: {message}");
		
		Console.WriteLine("=== FIN TEST ===");
	}

	/// <summary>
	/// Méthode alternative pour récupérer un nombre limité de messages
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
	/// Active/désactive le debug de cryptage
	/// </summary>
	/// <param name="enabled">État du debug</param>
	public void SetEncryptionDebug(bool enabled)
	{
		_debugEncryption = enabled;
		Console.WriteLine($"Debug de cryptage: {(enabled ? "ACTIVÉ" : "DÉSACTIVÉ")}");
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
					Console.WriteLine($"Cryptage basculé: {(!encInfo.enabled ? "ACTIVÉ" : "DÉSACTIVÉ")}");
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
		Console.WriteLine("MainGameScene: Nettoyage des ressources de cryptage");
	}
}
