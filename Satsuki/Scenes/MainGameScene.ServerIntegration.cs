using Godot;
using Satsuki.Systems;

/// <summary>
/// Partie ServerIntegration de MainGameScene
/// Gère GameServerHandler, événements réseau, UI et commandes debug
/// </summary>
public partial class MainGameScene
{
	#region Server Event Handlers
	private void OnServerStarted()
	{
		GD.Print("?? MainGameScene: Serveur démarré avec succès!");
		SetNetworkUIEnabled(true);
	}

	private void OnServerStopped()
	{
		GD.Print("?? MainGameScene: Serveur arrêté");
		SetNetworkUIEnabled(false);
	}

	private void OnServerError(string error)
	{
		GD.PrintErr($"?? MainGameScene: Erreur serveur - {error}");
		ShowNetworkError(error);
	}

	private void OnClientConnected(string clientId)
	{
		GD.Print($"?? MainGameScene: Client connecté - {clientId}");
		UpdateClientList();
	}

	private void OnClientDisconnected(string clientId)
	{
		GD.Print($"?? MainGameScene: Client déconnecté - {clientId}");
		UpdateClientList();
	}

	private void OnMessageReceived(string clientId, string content)
	{
		if (_debugMode)
		{
			GD.Print($"?? MainGameScene: Message reçu de {clientId}: {content}");
		}
	}
	#endregion

	#region UI Management
	private void SetNetworkUIEnabled(bool enabled)
	{
		GD.Print($"?? Interface réseau: {(enabled ? "Activée" : "Désactivée")}");
	}

	private void ShowNetworkError(string error)
	{
		GD.PrintErr($"?? Erreur réseau: {error}");
	}

	private void UpdateClientList()
	{
		if (_gameServerHandler != null)
		{
			int clientCount = _gameServerHandler.GetConnectedClientCount();
			GD.Print($"?? Nombre de clients connectés: {clientCount}");
		}
	}
	#endregion

	#region Public API for Server Access
	public GameServerHandler GetServerHandler()
	{
		return _gameServerHandler;
	}

	public void SendMessageToClient(string clientId, string message, bool encrypt = true)
	{
		_gameServerHandler?.SendMessageToClient(clientId, message, encrypt);
	}

	public void BroadcastMessage(string message, bool encrypt = true)
	{
		_gameServerHandler?.BroadcastToAllClients(message, encrypt);
	}

	public int GetConnectedClientCount()
	{
		return _gameServerHandler?.GetConnectedClientCount() ?? 0;
	}
	#endregion

	#region Input Handling (Debug Commands)
	public override void _Input(InputEvent @event)
	{
		if (_currentSceneNode != null)
		{
			_currentSceneNode._Input(@event);
		}

		if (@event is InputEventKey keyEvent && keyEvent.Pressed && _gameServerHandler != null)
		{
			switch (keyEvent.Keycode)
			{
				case Key.F1:
					_gameServerHandler.BroadcastToAllClients("SERVER_BROADCAST:Message de test crypté du serveur", encrypt: true);
					break;
				case Key.F2:
					GD.Print("?? Affichage des statistiques serveur...");
					break;
				case Key.F3:
					_gameServerHandler.ListConnectedClients();
					break;
				case Key.F4:
					_debugMode = !_debugMode;
					_gameServerHandler.ToggleDebugMode();
					GD.Print($"?? Mode debug MainGameScene: {(_debugMode ? "ACTIVÉ" : "DÉSACTIVÉ")}");
					break;
				case Key.F5:
					_gameServerHandler.BroadcastToAllClients("CHAT:SERVER:Message crypté du serveur à tous les joueurs", encrypt: true);
					break;
				case Key.F6:
					_gameServerHandler.ProcessMessagesHighFrequency();
					break;
				case Key.F7:
					_gameServerHandler.ProcessLimitedMessages(5);
					break;
				case Key.F8:
					_gameServerHandler.ToggleEncryption();
					break;
				case Key.F9:
					_gameServerHandler.GenerateNewEncryptionKey();
					break;
				case Key.F10:
					var gameState = _gameServerHandler.GetCompleteGameState();
					GD.Print("?? État complet du jeu récupéré");
					break;
				case Key.F11:
					if (!_hasLoadedCredits)
					{
						LoadCreditsScene();
					}
					else
					{
						GD.Print("?? Credits déjà chargés");
					}
					break;
				case Key.F12:
					LoadTitleScene();
					break;
				case Key.Delete:
					UnloadCurrentScene();
					GD.Print("??? CurrentScene déchargée");
					break;
				case Key.Home:
					LoadLocationByClassName("LocationModel");
					GD.Print("??? LocationModel chargée dans CurrentLocation");
					break;
				case Key.End:
					UnloadCurrentLocation();
					GD.Print("??? CurrentLocation déchargée");
					break;
				case Key.Menu:
					var locationInfo = GetCurrentLocationInfo();
					GD.Print($"??? Info CurrentLocation: {System.Text.Json.JsonSerializer.Serialize(locationInfo)}");
					break;
				case Key.Minus:
					PlayerEnterCurrentLocation("TestPlayer");
					GD.Print("?? TestPlayer entre dans CurrentLocation");
					break;
				case Key.Equal:
					var players = GetPlayersInCurrentLocation();
					GD.Print($"?? Joueurs dans CurrentLocation: {string.Join(", ", players)}");
					break;
				case Key.Backspace:
					var interactables = GetCurrentLocationInteractables();
					GD.Print($"?? Interactables dans CurrentLocation: {interactables.Length}");
					foreach (var interactable in interactables)
					{
						GD.Print($"  - {interactable.DisplayName} ({interactable.InteractableId})");
					}
					break;
			}
		}
	}
	#endregion
}
