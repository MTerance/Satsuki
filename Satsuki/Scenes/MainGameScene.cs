using Godot;
using Satsuki.Interfaces;
using Satsuki.Scenes.Locations;
using Satsuki.Systems;
using Satsuki.Manager;
using System;

/// <summary>
/// Scène principale du jeu - Orchestrateur simplifié
/// Gère Credits, Title et délègue locations au LocationManager
/// </summary>
public partial class MainGameScene : Node, IScene
{
	#region Private Fields
	private GameServerHandler _gameServerHandler;
	private LocationManager _locationManager;
	private bool _hasLoadedCredits = false;
	private bool _debugMode = true;
	
	// Référence rapide pour IScene (peut être Title ou Credits)
	private IScene _currentScene;
	private Node _currentSceneNode;
	#endregion

	#region Public Properties
	/// <summary>
	/// Location courante (délégué au LocationManager)
	/// </summary>
	public ILocation CurrentLocation => _locationManager?.CurrentLocation;
	
	/// <summary>
	/// Scène UI courante (Title ou Credits)
	/// </summary>
	public IScene CurrentScene => _currentScene;
	
	/// <summary>
	/// Handler du serveur de jeu
	/// </summary>
	public GameServerHandler ServerHandler => _gameServerHandler;
	#endregion

	#region Godot Lifecycle
	public override void _Ready()
	{
		GD.Print("?? MainGameScene: Initialisation...");
		
		// Initialiser les managers
		_gameServerHandler = new GameServerHandler();
		AddChild(_gameServerHandler);
		
		_locationManager = new LocationManager();
		AddChild(_locationManager);
		
		// Événements LocationManager
		_locationManager.LocationLoaded += OnLocationLoaded;
		_locationManager.LocationLoadFailed += OnLocationLoadFailed;
		
		// Événements Server
		_gameServerHandler.ServerStarted += OnServerStarted;
		_gameServerHandler.ServerStopped += OnServerStopped;
		_gameServerHandler.ServerError += OnServerError;
		_gameServerHandler.ClientConnected += OnClientConnected;
		_gameServerHandler.ClientDisconnected += OnClientDisconnected;
		_gameServerHandler.MessageReceived += OnMessageReceived;

		GD.Print("? MainGameScene: Initialisée");
		
		// Démarrer par les crédits
		CallDeferred(nameof(LoadCredits));
	}

	public override void _ExitTree()
	{
		// Décharger la scène UI
		UnloadCurrentScene();
		
		// Déconnecter événements
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
		
		GD.Print("?? MainGameScene: Nettoyage terminé");
	}
	#endregion

	#region Scene Management
	/// <summary>
	/// Charge Credits
	/// </summary>
	public void LoadCredits()
	{
		if (_hasLoadedCredits) return;
		
		try
		{
			GD.Print("?? MainGameScene: Chargement Credits...");
			
			UnloadCurrentScene();
			
			var credits = new Credits();
			AddChild(credits);
			_currentSceneNode = credits;
			_currentScene = credits;
			
			// Connecter événements Credits
			credits.CreditsCompleted += () => LoadTitle();
			credits.LoadTitleSceneRequested += () => LoadTitle();
			credits.SetFadeSpeed(2.0f);
			
			_hasLoadedCredits = true;
			GD.Print("? Credits chargé");
		}
		catch (Exception ex)
		{
			GD.PrintErr($"? Erreur chargement Credits: {ex.Message}");
		}
	}

	/// <summary>
	/// Charge Title + Restaurant en arrière-plan
	/// </summary>
	public void LoadTitle()
	{
		try
		{
			GD.Print("?? MainGameScene: Chargement Title...");
			
			UnloadCurrentScene();
			
			var title = new Satsuki.Scenes.Title();
			AddChild(title);
			_currentSceneNode = title;
			_currentScene = title;
			
			GD.Print("? Title chargé");
			
			// Charger Restaurant en arrière-plan avec caméra Title
			CallDeferred(nameof(LoadRestaurant));
		}
		catch (Exception ex)
		{
			GD.PrintErr($"? Erreur chargement Title: {ex.Message}");
		}
	}

	/// <summary>
	/// Charge Restaurant et active la caméra Title
	/// </summary>
	private void LoadRestaurant()
	{
		try
		{
			const string restaurantPath = "res://Scenes/Locations/Restaurant.tscn";
			
			bool success = _locationManager.LoadLocationFromScene(restaurantPath, useCache: true);
			
			if (success && _locationManager.CurrentLocation != null)
			{
				GD.Print("? Restaurant chargé");
				
				// Activer caméra Title
				_locationManager.CurrentLocation.SetActiveCamera(CameraType.Title);
				GD.Print("?? Caméra Title activée");
			}
			else
			{
				GD.PrintErr("? Échec chargement Restaurant");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"? Erreur chargement Restaurant: {ex.Message}");
		}
	}

	/// <summary>
	/// Décharge la scène UI courante
	/// </summary>
	private void UnloadCurrentScene()
	{
		if (_currentSceneNode == null) return;

		GD.Print($"??? Déchargement {_currentSceneNode.GetType().Name}");

		// Déconnecter événements si Credits
		if (_currentSceneNode is Credits credits)
		{
			credits.CreditsCompleted -= () => LoadTitle();
			credits.LoadTitleSceneRequested -= () => LoadTitle();
		}

		RemoveChild(_currentSceneNode);
		_currentSceneNode.QueueFree();
		_currentSceneNode = null;
		_currentScene = null;
		
		GD.Print("? Déchargement terminé");
	}
	#endregion

	#region LocationManager Event Handlers
	private void OnLocationLoaded(ILocation location)
	{
		GD.Print($"??? Location '{location.LocationName}' chargée");
	}

	private void OnLocationLoadFailed(string identifier, string reason)
	{
		GD.PrintErr($"? Échec chargement '{identifier}': {reason}");
	}
	#endregion

	#region Server Event Handlers
	private void OnServerStarted()
	{
		GD.Print("?? MainGameScene: Serveur démarré");
	}

	private void OnServerStopped()
	{
		GD.Print("?? MainGameScene: Serveur arrêté");
	}

	private void OnServerError(string error)
	{
		GD.PrintErr($"? MainGameScene: Erreur serveur - {error}");
	}

	private void OnClientConnected(string clientId)
	{
		GD.Print($"?? MainGameScene: Client connecté - {clientId}");
	}

	private void OnClientDisconnected(string clientId)
	{
		GD.Print($"?? MainGameScene: Client déconnecté - {clientId}");
	}

	private void OnMessageReceived(string clientId, string content)
	{
		if (_debugMode)
		{
			GD.Print($"?? MainGameScene: Message de {clientId}: {content}");
		}
	}
	#endregion

	#region IScene Implementation
	/// <summary>
	/// Retourne l'état global de MainGameScene
	/// </summary>
	public object GetSceneState()
	{
		return new
		{
			MainGameScene = new
			{
				SceneName = "MainGameScene",
				HasLoadedCredits = _hasLoadedCredits,
				CurrentScene = _currentSceneNode?.GetType().Name ?? "None",
				CurrentLocation = CurrentLocation?.LocationName ?? "None",
				ConnectedClients = _gameServerHandler?.GetConnectedClientCount() ?? 0
			},
			UIScene = _currentScene?.GetSceneState(),
			Location = CurrentLocation?.GetLocationState(),
			Timestamp = DateTime.UtcNow
		};
	}

	/// <summary>
	/// Alias pour compatibilité
	/// </summary>
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
				GD.Print($"?? Mode debug: {(_debugMode ? "ON" : "OFF")}");
				break;
			case Key.F11:
				LoadCredits();
				break;
			case Key.F12:
				LoadTitle();
				break;
		}
	}
	#endregion
}
