using Godot;
using Satsuki.Interfaces;
using Satsuki.Scenes;
using Satsuki.Scenes.Locations;
using Satsuki.Systems;
using Satsuki.Manager;
using Satsuki.Interfaces.Models;
using Satsuki.Interfaces.GameMode;
using System;
using Satsuki.Scenes.GameModes;
using Satsuki.Scenes.Abstract;
using Satsuki.Models;
using System.Text.Json;

/// <summary>
/// Scene principale du jeu - Orchestrateur simplifie
/// Gere Credits, Title et delegue locations au LocationManager
/// </summary>
public partial class MainGameScene : GameScene, IScene, IGameRecordUser
{

	#region Signals

	[Signal]
	delegate void GameModeRequestedEventHandler(string newGameMode);

	#endregion

	#region Private Fields
	private ServerManager _serverManager;
	private LocationManager _locationManager;
	private GameModeLoader _gameModeLoader;
	private bool _hasLoadedCredits = false;
	private bool _debugMode = true;

	//**/
	private IGameRecord _currentGameRecord;
	//**/


	private Node _currentScene;
	#endregion

	#region Public Properties
	public ILocation CurrentLocation => 
		_locationManager?.CurrentLocation;
	public IScene CurrentScene => 
		_currentScene as IScene;
	public ServerManager Server => 
		_serverManager;
	#endregion

	#region Godot Lifecycle
	public override void _Ready()
	{
		GD.Print("MainGameScene: Initialisation...");

		_serverManager = GetNodeOrNull<ServerManager>("/root/ServerManager");
		if (_serverManager == null)
		{
			GD.PrintErr("MainGameScene: ServerManager introuvable en AutoLoad");
		}

		_gameModeLoader = new GameModeLoader();

		_locationManager = new LocationManager();
		AddChild(_locationManager);

		_locationManager.LocationLoaded += OnLocationLoaded;
		_locationManager.LocationLoadFailed += OnLocationLoadFailed;

		if (_serverManager != null)
		{
			_serverManager.ServerStarted += OnServerStarted;
			_serverManager.ServerStopped += OnServerStopped;
			_serverManager.ServerError += OnServerError;
			_serverManager.ClientConnected += OnClientConnected;
			_serverManager.ClientTypeReceived += OnClientTypeReceived;
			_serverManager.SystemOrderReceived += OnSystemOrderReceived;
			_serverManager.SceneOrderReceived += OnSceneOrderReceived;
			_serverManager.QuizzOrderReceived += OnQuizzOrderReceived;
		}

		GD.Print("MainGameScene: Initialisee");

		CallDeferred(nameof(LoadCredits));
	}

	public override void _ExitTree()
	{
		UnloadCurrentScene();

		if (_locationManager != null)
		{
			_locationManager.LocationLoaded -= OnLocationLoaded;
			_locationManager.LocationLoadFailed -= OnLocationLoadFailed;
		}

		if (_serverManager != null)
		{
			_serverManager.ServerStarted -= OnServerStarted;
			_serverManager.ServerStopped -= OnServerStopped;
			_serverManager.ServerError -= OnServerError;
			_serverManager.ClientConnected -= OnClientConnected;
			_serverManager.ClientTypeReceived -= OnClientTypeReceived;
			_serverManager.SystemOrderReceived -= OnSystemOrderReceived;
			_serverManager.SceneOrderReceived -= OnSceneOrderReceived;
			_serverManager.QuizzOrderReceived -= OnQuizzOrderReceived;
		}

		GD.Print("MainGameScene: Nettoyage termine");
	}
	
	public override void _Notification(int what)
	{
		if (what == NotificationWMCloseRequest)
		{
			GD.Print("MainGameScene: Demande de fermeture recue");
			// Le ServerManager va gerer l'arret propre et quitter l'application
		}
	}
	#endregion

	#region Scene Management
	public void LoadCredits()
	{
		try
		{
			GD.Print("MainGameScene: Chargement Credits...");
			
			UnloadCurrentScene();
			
			var credits = new Credits();
			AddChild(credits);
			_currentScene = credits;
			
			credits.CreditsCompleted += OnCreditsCompleted;
			credits.LoadTitleSceneRequested += OnLoadTitleRequested;
			credits.SetFadeSpeed(2.0f);
			
			_hasLoadedCredits = true;
			GD.Print("Credits charge");
		}
		catch (Exception ex)
		{
			GD.PrintErr($"Erreur chargement Credits: {ex.Message}");
			_hasLoadedCredits = false;
		}
	}

	public void LoadTitle()
	{
		try
		{
			GD.Print("MainGameScene: Chargement Title...");
			
			UnloadCurrentScene();
			
			var title = new Title();
			AddChild(title);
			_currentScene = title;
			
			title.StartGameRequested += OnStartGameRequested;
			
			GD.Print("Title charge");
			
			CallDeferred(nameof(ActivateTitleCamera));
		}
		catch (Exception ex)
		{
			GD.PrintErr($"Erreur chargement Title: {ex.Message}");
		}
	}
	
	private void ActivateTitleCamera()
	{
		try
		{
			const string restaurantPath = "res://Scenes/Locations/Restaurant.tscn";
			
			bool success = _locationManager.LoadLocationFromScene(restaurantPath, useCache: true);
			
			if (success && _locationManager.CurrentLocation != null)
			{
				GD.Print("Restaurant charge pour Title");
				
				bool cameraSet = _locationManager.CurrentLocation.SetActiveCamera(CameraType.Title);
				if (cameraSet)
				{
					GD.Print("Camera Title_Camera3D activee avec succes");
				}
				else
				{
					GD.PrintErr("Echec activation Camera Title_Camera3D");
				}
			}
			else
			{
				GD.PrintErr("Echec chargement Restaurant pour Title");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"Erreur activation camera Title: {ex.Message}");
		}
	}

	public void LoadMainMenu()
	{
		try
		{
			GD.Print("MainGameScene: Chargement MainMenu...");
			
			UnloadCurrentScene();
			
			var mainMenu = new MainMenu();
			AddChild(mainMenu);
			_currentScene = mainMenu;
			
			mainMenu.GoToLobbyRequested += OnGoToLobbyRequested;
			mainMenu.MiniGamesRequested += OnMiniGamesRequested;
			mainMenu.BackToTitleRequested += OnBackToTitleRequested;
			
			GD.Print("MainMenu charge");
			
			CallDeferred(nameof(ActivateLobbyCamera));
		}
		catch (Exception ex)
		{
			GD.PrintErr($"Erreur chargement MainMenu: {ex.Message}");
		}
	}
	
	private void ActivateLobbyCamera()
	{
		try
		{
			if (_locationManager?.CurrentLocation != null)
			{
				GD.Print("MainGameScene: Activation camera Lobby pour MainMenu...");
				
				bool cameraSet = _locationManager.CurrentLocation.SetActiveCamera(CameraType.Lobby);
				if (cameraSet)
				{
					GD.Print("Camera Lobby_Camera3D activee avec succes");
				}
				else
				{
					GD.PrintErr("Echec activation Camera Lobby_Camera3D");
				}
			}
			else
			{
				GD.PrintErr("Location non chargee, impossible d'activer la camera Lobby");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"Erreur activation camera Lobby: {ex.Message}");
		}
	}

	public void LoadLobby()
	{
		try
		{
			GD.Print("MainGameScene: Chargement Lobby...");

			UnloadCurrentScene();

			var lobby = new Lobby();
			AddChild(lobby);
			_currentScene = lobby;

			GD.Print("Lobby charge");

			CallDeferred(nameof(ActivateLobbyCamera));
		}
		catch (Exception ex)
		{
			GD.PrintErr($"Erreur chargement Lobby: {ex.Message}");
		}
	}


	public void LoadGameMode(string gamemodeName)
	{
		try
		{
			GD.Print($"MainGameScene: Chargement GameMode '{gamemodeName}'...");
			UnloadCurrentScene();
			var gameModeScene = _gameModeLoader.LoadGameMode(gamemodeName);
			if (gameModeScene != null)
			{
				AddChild(gameModeScene);
				_currentScene = gameModeScene;
				if (_currentScene is IGameMode gameMode)
				{
					this.GameModeRequested += OnGameModeRequested;
				}
				GD.Print($"GameMode '{gamemodeName}' charge");
			}
			else
			{
				GD.PrintErr($"Echec chargement GameMode '{gamemodeName}'");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"Erreur chargement GameMode '{gamemodeName}': {ex.Message}");
		}
	}

	private void OnGameModeRequested(string newGameMode)
	{
		LoadGameMode(newGameMode);
	}

	private void UnloadCurrentScene()
	{
		if (_currentScene == null) return;

		GD.Print($"Dechargement {_currentScene.GetType().Name}");

		if (_currentScene is Credits credits)
		{
			credits.CreditsCompleted -= OnCreditsCompleted;
			credits.LoadTitleSceneRequested -= OnLoadTitleRequested;
		}
		
		if (_currentScene is Title title)
		{
			title.StartGameRequested -= OnStartGameRequested;
		}
		
		if (_currentScene is MainMenu mainMenu)
		{
			mainMenu.GoToLobbyRequested -= OnGoToLobbyRequested;
			mainMenu.MiniGamesRequested -= OnMiniGamesRequested;
			mainMenu.BackToTitleRequested -= OnBackToTitleRequested;
		}

		RemoveChild(_currentScene);
		_currentScene.QueueFree();
		_currentScene = null;
		
		GD.Print("Dechargement termine");
	}

	private void OnCreditsCompleted()
	{
		LoadTitle();
	}

	private void OnLoadTitleRequested()
	{
		LoadTitle();
	}
	
	private void OnStartGameRequested()
	{
		GD.Print("MainGameScene: Reception du signal StartGameRequested");
		LoadLobby();
	}
	
	private void OnGoToLobbyRequested()
	{
		GD.Print("MainGameScene: Reception du signal GoToLobbyRequested");
		// TODO: Ajouter la logique pour aller au Lobby
	}
	
	private void OnMiniGamesRequested()
	{
		GD.Print("MainGameScene: Reception du signal MiniGamesRequested");
		// TODO: Charger la scene des mini-jeux
		GD.Print("MainGameScene: Ouverture des Mini-Games...");
	}
	
	private void OnBackToTitleRequested()
	{
		GD.Print("MainGameScene: Reception du signal BackToTitleRequested");
		LoadTitle();
	}
	#endregion

	#region LocationManager Event Handlers
	private void OnLocationLoaded(ILocation location)
	{
		GD.Print($"Location '{location.LocationName}' chargee");
	}

	private void OnLocationLoadFailed(string identifier, string reason)
	{
		GD.PrintErr($"Echec chargement '{identifier}': {reason}");
	}
	#endregion

	#region Server Event Handlers
	private void OnServerStarted()
	{
		GD.Print("MainGameScene: Serveur demarre");
	}

	private void OnServerStopped()
	{
		GD.Print("MainGameScene: Serveur arrete");
	}

	private void OnServerError(string error)
	{
		GD.PrintErr($"MainGameScene: Erreur serveur - {error}");
	}

	private void OnClientConnected(string clientId)
	{
		GD.Print($"MainGameScene: Client connecte - {clientId}");
	}

	private void OnClientDisconnected(string clientId)
	{
		GD.Print($"MainGameScene: Client deconnecte - {clientId}");
	}

	private void OnMessageReceived(string clientId, string content)
	{
		if (_debugMode)
		{
			GD.Print($"MainGameScene: Message de {clientId}: {content}");
		}
	}

	private void OnClientTypeReceived(string clientId, string clientType)
	{
		GD.Print($"MainGameScene: Client {clientId} enregistre comme {clientType}");
	}

	private void OnSystemOrderReceived(string orderRequestJson)
	{
		try
		{
			var orderRequest = JsonSerializer.Deserialize<OrderRequest>(orderRequestJson);
			if (_debugMode)
			{
				GD.Print($"MainGameScene: Ordre systeme '{orderRequest.Order}'");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"MainGameScene: Erreur parsing ordre systeme: {ex.Message}");
		}
	}

	private void OnSceneOrderReceived(string orderRequestJson)
	{
		try
		{
			var orderRequest = JsonSerializer.Deserialize<OrderRequest>(orderRequestJson);
			if (_debugMode)
			{
				GD.Print($"MainGameScene: Ordre scene '{orderRequest.Order}'");
			}
			OnMessageReceived(orderRequest.ClientId, orderRequestJson);
		}
		catch (Exception ex)
		{
			GD.PrintErr($"MainGameScene: Erreur parsing ordre scene: {ex.Message}");
		}
	}

	private void OnQuizzOrderReceived(string orderRequestJson)
	{
		try
		{
			var orderRequest = JsonSerializer.Deserialize<OrderRequest>(orderRequestJson);
			if (_debugMode)
			{
				GD.Print($"MainGameScene: Ordre quizz '{orderRequest.Order}'");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"MainGameScene: Erreur parsing ordre quizz: {ex.Message}");
		}
	}
	#endregion

	#region IScene Implementation
	public object GetSceneState()
	{
		return new
		{
			MainGameScene = new
			{
				SceneName = "MainGameScene",
				HasLoadedCredits = _hasLoadedCredits,
				CurrentScene = _currentScene?.GetType().Name ?? "None",
				CurrentLocation = CurrentLocation?.LocationName ?? "None",
				ConnectedClients = _serverManager?.GetConnectedClientsCount() ?? 0
			},
			UIScene = CurrentScene?.GetSceneState(),
			Location = CurrentLocation?.GetLocationState(),
			Timestamp = DateTime.UtcNow
		};
	}

	public object GetGameSceneState() => GetSceneState();

	public IGameRecord LoadCurrentGameRecord()
	{
		return _currentGameRecord;
	}

	public void SetGameRecord(IGameRecord gameRecord)
	{
		_currentGameRecord = gameRecord;
	}
	#endregion

	#region Input Handling (Debug)
	public override void _Input(InputEvent @event)
	{
		if (@event is not InputEventKey keyEvent || !keyEvent.Pressed) return;

		switch (keyEvent.Keycode)
		{
			case Key.F1:
				_serverManager?.SendServerMessage("SERVER_BROADCAST:Test");
				break;
			case Key.F3:
				_serverManager?.LogServerStatus();
				break;
			case Key.F4:
				_debugMode = !_debugMode;
				GD.Print($"Mode debug: {(_debugMode ? "ON" : "OFF")}");
				break;
			case Key.F11:
				_hasLoadedCredits = false;
				LoadCredits();
				break;
			case Key.F12:
				LoadTitle();
				break;
		}
	}
	#endregion
}
