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
			
			GD.Print("Title charge");
			
			CallDeferred(nameof(LoadRestaurant));
		}
		catch (Exception ex)
		{
			GD.PrintErr($"Erreur chargement Title: {ex.Message}");
		}
	}

	private void LoadRestaurant()
	{
		try
		{
			const string restaurantPath = "res://Scenes/Locations/Restaurant.tscn";
			
			bool success = _locationManager.LoadLocationFromScene(restaurantPath, useCache: true);
			
			if (success && _locationManager.CurrentLocation != null)
			{
				GD.Print("Restaurant charge");
				
				_locationManager.CurrentLocation.SetActiveCamera(CameraType.Title);
				GD.Print("Camera Title activee");
			}
			else
			{
				GD.PrintErr("Echec chargement Restaurant");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"Erreur chargement Restaurant: {ex.Message}");
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
