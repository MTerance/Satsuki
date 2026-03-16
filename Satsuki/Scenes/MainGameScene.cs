using Godot;
using Satsuki.Interfaces;
using Satsuki.Scenes;
using Satsuki.Scenes.Locations;
using Satsuki.Systems;
using Satsuki.Manager;
using System;

/// <summary>
/// Scene principale du jeu - Orchestrateur simplifie
/// Gere Credits, Title et delegue locations au LocationManager
/// </summary>
public partial class MainGameScene : Node, IScene
{
	#region Private Fields
	private GameServerHandler _gameServerHandler;
	private LocationManager _locationManager;
	private bool _hasLoadedCredits = false;
	private bool _debugMode = true;
	
	private Node _currentScene;
	#endregion

	#region Public Properties
	public ILocation CurrentLocation => 
		_locationManager?.CurrentLocation;
	public IScene CurrentScene => 
		_currentScene as IScene;
	public GameServerHandler ServerHandler => 
		_gameServerHandler;
	#endregion

	#region Godot Lifecycle
	public override void _Ready()
	{
		GD.Print("MainGameScene: Initialisation...");
		
		_gameServerHandler = new GameServerHandler();
		AddChild(_gameServerHandler);
		
		_locationManager = new LocationManager();
		AddChild(_locationManager);
		
		_locationManager.LocationLoaded += OnLocationLoaded;
		_locationManager.LocationLoadFailed += OnLocationLoadFailed;
		
		_gameServerHandler.ServerStarted += OnServerStarted;
		_gameServerHandler.ServerStopped += OnServerStopped;
		_gameServerHandler.ServerError += OnServerError;
		_gameServerHandler.ClientConnected += OnClientConnected;
		_gameServerHandler.ClientDisconnected += OnClientDisconnected;
		_gameServerHandler.MessageReceived += OnMessageReceived;

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

		if (_gameServerHandler != null)
		{
			_gameServerHandler.ServerStarted -= OnServerStarted;
			_gameServerHandler.ServerStopped -= OnServerStopped;
			_gameServerHandler.ServerError -= OnServerError;
			_gameServerHandler.ClientConnected -= OnClientConnected;
			_gameServerHandler.ClientDisconnected -= OnClientDisconnected;
			_gameServerHandler.MessageReceived -= OnMessageReceived;
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
			title.OptionsRequested += OnOptionsRequested;
			title.CreditsRequested += OnCreditsRequestedFromTitle;
			
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
			
			mainMenu.SoloPlayRequested += OnSoloPlayRequested;
			mainMenu.MultiplayerRequested += OnMultiplayerRequested;
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
			title.OptionsRequested -= OnOptionsRequested;
			title.CreditsRequested -= OnCreditsRequestedFromTitle;
		}
		
		if (_currentScene is MainMenu mainMenu)
		{
			mainMenu.SoloPlayRequested -= OnSoloPlayRequested;
			mainMenu.MultiplayerRequested -= OnMultiplayerRequested;
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
		LoadMainMenu();
	}
	
	private void OnOptionsRequested()
	{
		GD.Print("MainGameScene: Reception du signal OptionsRequested");
	}
	
	private void OnCreditsRequestedFromTitle()
	{
		GD.Print("MainGameScene: Reception du signal CreditsRequested");
		LoadCredits();
	}
	
	private void OnSoloPlayRequested()
	{
		GD.Print("MainGameScene: Reception du signal SoloPlayRequested");
		// TODO: Charger la scene de jeu solo
		GD.Print("MainGameScene: Demarrage du mode Solo Play...");
	}
	
	private void OnMultiplayerRequested()
	{
		GD.Print("MainGameScene: Reception du signal MultiplayerRequested");
		// TODO: Charger la scene multijoueur
		GD.Print("MainGameScene: Demarrage du mode Multiplayer...");
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
				ConnectedClients = _gameServerHandler?.GetConnectedClientCount() ?? 0
			},
			UIScene = CurrentScene?.GetSceneState(),
			Location = CurrentLocation?.GetLocationState(),
			Timestamp = DateTime.UtcNow
		};
	}

	public object GetGameSceneState() => GetSceneState();
	#endregion

	#region Input Handling (Debug)
	public override void _Input(InputEvent @event)
	{
		if (@event is not InputEventKey keyEvent || !keyEvent.Pressed) return;

		switch (keyEvent.Keycode)
		{
			case Key.F1:
				_gameServerHandler?.BroadcastToAllClients("SERVER_BROADCAST:Test", encrypt: true);
				break;
			case Key.F3:
				_gameServerHandler?.ListConnectedClients();
				break;
			case Key.F4:
				_debugMode = !_debugMode;
				_gameServerHandler?.ToggleDebugMode();
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
