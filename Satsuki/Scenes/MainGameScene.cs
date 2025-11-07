using Godot;
using Satsuki.Interfaces;
using Satsuki.Systems;
using Satsuki.Scenes.Locations;
using Satsuki.Manager;
using System;

/// <summary>
/// Scène principale du jeu - Orchestrateur central
/// Divisée en classes partielles pour meilleure maintenabilité:
/// - MainGameScene.cs: Initialisation et état
/// - MainGameScene.SceneManagement.cs: Gestion des scènes
/// - MainGameScene.LocationManagement.cs: Gestion des locations
/// - MainGameScene.ServerIntegration.cs: Gestion serveur et debug
/// </summary>
public partial class MainGameScene : Node, IScene
{
	#region Private Fields
	private GameServerHandler _gameServerHandler;
	private LocationManager _locationManager;
	private bool _debugMode = true;
	private bool _hasLoadedCredits = false;
	
	private IScene _currentScene;
	private Node _currentSceneNode;
	
	private ILocation _currentLocation;
	private Node _currentLocationNode;
	#endregion

	#region Public Properties
	/// <summary>
	/// Propriété publique pour accéder à la scène courante
	/// </summary>
	public IScene CurrentScene 
	{ 
		get => _currentScene; 
		private set => _currentScene = value; 
	}

	/// <summary>
	/// Propriété publique pour accéder à la location courante
	/// </summary>
	public ILocation CurrentLocation 
	{ 
		get => _currentLocation; 
		private set => _currentLocation = value; 
	}
	#endregion

	#region Godot Lifecycle
	public override void _Ready()
	{
		GD.Print("🎮 MainGameScene: Initialisation...");
		
		// Créer et ajouter le gestionnaire de serveur
		_gameServerHandler = new GameServerHandler();
		AddChild(_gameServerHandler);
		
		// Créer et ajouter le LocationManager
		_locationManager = new LocationManager();
		AddChild(_locationManager);
		
		// Connecter aux événements du LocationManager
		_locationManager.LocationLoaded += OnLocationManagerLoaded;
		_locationManager.LocationUnloaded += OnLocationManagerUnloaded;
		_locationManager.LocationLoadFailed += OnLocationManagerLoadFailed;
		
		// Connecter aux événements du gestionnaire de serveur
		_gameServerHandler.ServerStarted += OnServerStarted;
		_gameServerHandler.ServerStopped += OnServerStopped;
		_gameServerHandler.ServerError += OnServerError;
		_gameServerHandler.ClientConnected += OnClientConnected;
		_gameServerHandler.ClientDisconnected += OnClientDisconnected;
		_gameServerHandler.MessageReceived += OnMessageReceived;

		GD.Print("✅ MainGameScene: Initialisée avec GameServerHandler et LocationManager");
		
		// Charger automatiquement la scène Credits
		CallDeferred(nameof(LoadCreditsScene));
	}

	public override void _ExitTree()
	{
		// Décharger la CurrentLocation
		UnloadCurrentLocation();

		// Décharger la CurrentScene
		UnloadCurrentScene();
		
		// Déconnecter les événements du LocationManager
		if (_locationManager != null)
		{
			_locationManager.LocationLoaded -= OnLocationManagerLoaded;
			_locationManager.LocationUnloaded -= OnLocationManagerUnloaded;
			_locationManager.LocationLoadFailed -= OnLocationManagerLoadFailed;
		}

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

	#region LocationManager Event Handlers
	private void OnLocationManagerLoaded(ILocation location)
	{
		GD.Print($"🏗️ MainGameScene: Location '{location.LocationName}' chargée via LocationManager");
		
		// Synchroniser les références MainGameScene avec LocationManager
		_currentLocation = _locationManager.CurrentLocation;
		_currentLocationNode = _locationManager.CurrentLocationNode;
		
		// Si la location est aussi une IScene, synchroniser aussi
		if (_currentLocationNode is IScene scene)
		{
			_currentSceneNode = _currentLocationNode;
			_currentScene = scene;
			GD.Print($"📦 MainGameScene: Location '{location.LocationName}' est aussi une IScene");
		}
	}

	private void OnLocationManagerUnloaded(ILocation location)
	{
		GD.Print($"🗑️ MainGameScene: Location '{location.LocationName}' déchargée via LocationManager");
	}

	private void OnLocationManagerLoadFailed(string identifier, string reason)
	{
		GD.PrintErr($"❌ MainGameScene: Échec de chargement de '{identifier}': {reason}");
	}
	#endregion

	#region IScene Implementation
	/// <summary>
	/// Retourne l'état actuel de la scène de jeu incluant CurrentScene et CurrentLocation
	/// </summary>
	public object GetSceneState()
	{
		object currentSceneState = null;
		string currentSceneName = "None";
		string currentSceneType = "None";

		if (_currentScene != null)
		{
			try
			{
				currentSceneState = _currentScene.GetSceneState();
				currentSceneName = _currentSceneNode?.GetType().Name ?? "Unknown";
				currentSceneType = _currentSceneNode?.GetType().FullName ?? "Unknown";
				GD.Print($"✅ État de CurrentScene {currentSceneName} récupéré");
			}
			catch (Exception ex)
			{
				GD.PrintErr($"❌ Erreur lors de la récupération de l'état de CurrentScene: {ex.Message}");
				currentSceneState = new { Error = "Failed to get current scene state", Message = ex.Message };
			}
		}

		object currentLocationState = null;
		string currentLocationName = "None";
		string currentLocationId = "None";
		string currentLocationType = "None";

		if (_currentLocation != null)
		{
			try
			{
				currentLocationState = _currentLocation.GetLocationState();
				currentLocationName = _currentLocation.LocationName ?? "Unknown";
				currentLocationId = _currentLocation.LocationId ?? "Unknown";
				currentLocationType = _currentLocation.Type.ToString();
				GD.Print($"✅ État de CurrentLocation {currentLocationName} récupéré");
			}
			catch (Exception ex)
			{
				GD.PrintErr($"❌ Erreur lors de la récupération de l'état de CurrentLocation: {ex.Message}");
				currentLocationState = new { Error = "Failed to get current location state", Message = ex.Message };
			}
		}

		return new
		{
			MainGameScene = new
			{
				SceneName = "MainGameScene",
				HasLoadedCredits = _hasLoadedCredits,
				HasCurrentScene = _currentScene != null,
				CurrentSceneName = currentSceneName,
				CurrentSceneType = currentSceneType,
				HasCurrentLocation = _currentLocation != null,
				CurrentLocationName = currentLocationName,
				CurrentLocationId = currentLocationId,
				CurrentLocationType = currentLocationType
			},
			CurrentScene = currentSceneState,
			CurrentLocation = currentLocationState,
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
	public object GetGameSceneState()
	{
		return GetSceneState();
	}
	#endregion
}
