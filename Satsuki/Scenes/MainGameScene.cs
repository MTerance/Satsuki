using Godot;
using Satsuki.Interfaces;
using Satsuki.Systems;
using System;
using System.Reflection;
using System.Threading.Tasks;

public partial class MainGameScene : Node, IScene
{
	private GameServerHandler _gameServerHandler;
	private bool _debugMode = true;

	public override void _Ready()
	{
		GD.Print("🎮 MainGameScene: Initialisation...");
		
		// Créer et ajouter le gestionnaire de serveur
		_gameServerHandler = new GameServerHandler();
		AddChild(_gameServerHandler);
		
		// Connecter aux événements du gestionnaire de serveur
		_gameServerHandler.ServerStarted += OnServerStarted;
		_gameServerHandler.ServerStopped += OnServerStopped;
		_gameServerHandler.ServerError += OnServerError;
		_gameServerHandler.ClientConnected += OnClientConnected;
		_gameServerHandler.ClientDisconnected += OnClientDisconnected;
		_gameServerHandler.MessageReceived += OnMessageReceived;

		GD.Print("✅ MainGameScene: Initialisée avec GameServerHandler");
	}

	#region IScene Implementation
	/// <summary>
	/// Retourne l'état actuel de la scène de jeu (sans les données serveur)
	/// </summary>
	/// <returns>Un objet contenant l'état de la scène de jeu</returns>
	public object GetSceneState()
	{
		// Récupérer la scène actuelle
		var currentScene = GetTree().CurrentScene;
		string sceneName = currentScene?.Name ?? "Unknown";
		string scenePath = currentScene?.SceneFilePath ?? "Unknown";

		// Essayer d'obtenir l'état de la scène si elle a une méthode GetSceneState
		object sceneState = null;
		if (currentScene != null && currentScene != this)
		{
			// Utiliser la réflexion pour appeler GetSceneState si elle existe
			var sceneType = currentScene.GetType();
			var getSceneStateMethod = sceneType.GetMethod("GetSceneState",
				BindingFlags.Public | BindingFlags.Instance);

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
			Scene = new
			{
				CurrentScene = sceneName,
				ScenePath = scenePath,
				SceneState = sceneState
			},
			Debug = new
			{
				DebugMode = _debugMode,
				Timestamp = DateTime.UtcNow
			}
		};
	}

	/// <summary>
	/// Méthode publique pour obtenir l'état de la scène de jeu (utilisée par GameServerHandler)
	/// </summary>
	/// <returns>Un objet contenant l'état de la scène de jeu</returns>
	public object GetGameSceneState()
	{
		return GetSceneState();
	}
	#endregion

	#region Server Event Handlers
	private void OnServerStarted()
	{
		GD.Print("🎮 MainGameScene: Serveur démarré avec succès!");
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
		ShowNetworkError(error);
	}

	private void OnClientConnected(string clientId)
	{
		GD.Print($"🎮 MainGameScene: Client connecté - {clientId}");
		// Logique UI pour afficher la connexion d'un client
		UpdateClientList();
	}

	private void OnClientDisconnected(string clientId)
	{
		GD.Print($"🎮 MainGameScene: Client déconnecté - {clientId}");
		// Logique UI pour afficher la déconnexion d'un client
		UpdateClientList();
	}

	private void OnMessageReceived(string clientId, string content)
	{
		if (_debugMode)
		{
			GD.Print($"🎮 MainGameScene: Message reçu de {clientId}: {content}");
		}
		// Logique UI pour afficher les messages si nécessaire
	}
	#endregion

	#region UI Management
	private void SetNetworkUIEnabled(bool enabled)
	{
		// Activer/désactiver les éléments UI liés au réseau
		// Par exemple, boutons multijoueur, indicateurs de statut, etc.
		GD.Print($"📡 Interface réseau: {(enabled ? "Activée" : "Désactivée")}");
		
		// Ici vous pourriez mettre à jour des éléments UI spécifiques
		// Exemple : GetNode<Button>("MultiplayerButton").Disabled = !enabled;
	}

	private void ShowNetworkError(string error)
	{
		// Afficher une notification d'erreur réseau dans l'UI
		GD.PrintErr($"🚨 Erreur réseau: {error}");
		
		// Ici vous pourriez afficher un popup d'erreur ou une notification
		// Exemple : GetNode<AcceptDialog>("ErrorDialog").DialogText = $"Erreur réseau: {error}";
		// Exemple : GetNode<AcceptDialog>("ErrorDialog").PopupCentered();
	}

	private void UpdateClientList()
	{
		// Mettre à jour l'affichage de la liste des clients connectés
		if (_gameServerHandler != null)
		{
			int clientCount = _gameServerHandler.GetConnectedClientCount();
			GD.Print($"📊 Nombre de clients connectés: {clientCount}");
			
			// Ici vous pourriez mettre à jour un label ou une liste dans l'UI
			// Exemple : GetNode<Label>("ClientCountLabel").Text = $"Clients: {clientCount}";
		}
	}
	#endregion

	#region Input Handling (Debug Commands)
	/// <summary>
	/// Commandes Input pour tests et debug - délègue au GameServerHandler
	/// </summary>
	public override void _Input(InputEvent @event)
	{
		if (@event is InputEventKey keyEvent && keyEvent.Pressed && _gameServerHandler != null)
		{
			switch (keyEvent.Keycode)
			{
				case Key.F1:
					// Test d'envoi de message crypté à tous les clients
					_gameServerHandler.BroadcastToAllClients("SERVER_BROADCAST:Message de test crypté du serveur", encrypt: true);
					break;
				case Key.F2:
					// Affiche les statistiques avec informations de cryptage (via GameServerHandler)
					GD.Print("📊 Affichage des statistiques serveur...");
					break;
				case Key.F3:
					// Liste des clients connectés
					_gameServerHandler.ListConnectedClients();
					break;
				case Key.F4:
					// Bascule le mode debug
					_debugMode = !_debugMode;
					_gameServerHandler.ToggleDebugMode();
					GD.Print($"🐛 Mode debug MainGameScene: {(_debugMode ? "ACTIVÉ" : "DÉSACTIVÉ")}");
					break;
				case Key.F5:
					// Simule un message de chat crypté du serveur
					_gameServerHandler.BroadcastToAllClients("CHAT:SERVER:Message crypté du serveur à tous les joueurs", encrypt: true);
					break;
				case Key.F6:
					// Traite tous les messages disponibles immédiatement
					_gameServerHandler.ProcessMessagesHighFrequency();
					break;
				case Key.F7:
					// Traite seulement les 5 prochains messages
					_gameServerHandler.ProcessLimitedMessages(5);
					break;
				case Key.F8:
					// Bascule le cryptage on/off
					_gameServerHandler.ToggleEncryption();
					break;
				case Key.F9:
					// Génère une nouvelle clé de cryptage
					_gameServerHandler.GenerateNewEncryptionKey();
					break;
				case Key.F10:
					// Obtient l'état complet du jeu
					var gameState = _gameServerHandler.GetCompleteGameState();
					GD.Print("🎮 État complet du jeu récupéré");
					break;
			}
		}
	}
	#endregion

	#region Scene Management
	public void ChangeScene(string scenePath = "res://Scenes/OtherScene.tscn")
	{
		GetTree().ChangeSceneToFile(scenePath);
	}

	/// <summary>
	/// Méthode pour obtenir des informations sur la scène actuelle
	/// </summary>
	/// <returns>Informations sur la scène actuelle</returns>
	public object GetCurrentSceneInfo()
	{
		var currentScene = GetTree().CurrentScene;
		return new
		{
			Name = currentScene?.Name ?? "Unknown",
			Path = currentScene?.SceneFilePath ?? "Unknown",
			Type = currentScene?.GetType().Name ?? "Unknown",
			IsMainGameScene = currentScene == this
		};
	}
	#endregion

	#region Public API for Server Access
	/// <summary>
	/// Obtient une référence au gestionnaire de serveur
	/// </summary>
	/// <returns>Instance du GameServerHandler</returns>
	public GameServerHandler GetServerHandler()
	{
		return _gameServerHandler;
	}

	/// <summary>
	/// Envoie un message à un client spécifique via le gestionnaire de serveur
	/// </summary>
	/// <param name="clientId">ID du client</param>
	/// <param name="message">Message à envoyer</param>
	/// <param name="encrypt">Si true, crypte le message</param>
	public void SendMessageToClient(string clientId, string message, bool encrypt = true)
	{
		_gameServerHandler?.SendMessageToClient(clientId, message, encrypt);
	}

	/// <summary>
	/// Diffuse un message à tous les clients via le gestionnaire de serveur
	/// </summary>
	/// <param name="message">Message à diffuser</param>
	/// <param name="encrypt">Si true, crypte le message</param>
	public void BroadcastMessage(string message, bool encrypt = true)
	{
		_gameServerHandler?.BroadcastToAllClients(message, encrypt);
	}

	/// <summary>
	/// Obtient le nombre de clients connectés
	/// </summary>
	/// <returns>Nombre de clients connectés</returns>
	public int GetConnectedClientCount()
	{
		return _gameServerHandler?.GetConnectedClientCount() ?? 0;
	}
	#endregion

	#region Cleanup
	public override void _ExitTree()
	{
		// Déconnecter les événements du gestionnaire de serveur
		if (_gameServerHandler != null)
		{
			_gameServerHandler.ServerStarted -= OnServerStarted;
			_gameServerHandler.ServerStopped -= OnServerStopped;
			_gameServerHandler.ServerError -= OnServerError;
			_gameServerHandler.ClientConnected -= OnClientConnected;
			_gameServerHandler.ClientDisconnected -= OnClientDisconnected;
			_gameServerHandler.MessageReceived -= OnMessageReceived;
		}
		
		GD.Print("🧹 MainGameScene: Nettoyage terminé");
	}
	#endregion
}
