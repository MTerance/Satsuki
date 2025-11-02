using Godot;
using Satsuki.Interfaces;
using Satsuki.Systems;
using Satsuki.Scenes.Locations;
using System;
using System.Reflection;
using System.Threading.Tasks;

public partial class MainGameScene : Node, IScene
{
	private GameServerHandler _gameServerHandler;
	private bool _debugMode = true;
	private bool _hasLoadedCredits = false;
	
	// Propriété IScene pour gérer la scène courante chargée
	private IScene _currentScene;
	private Node _currentSceneNode;
	
	// Propriété ILocation pour gérer la location courante
	private ILocation _currentLocation;
	private Node _currentLocationNode;

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
		
		// Charger automatiquement la scène Credits dans la propriété IScene
		CallDeferred(nameof(LoadCreditsScene));
	}

	#region Current Scene Management
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

	/// <summary>
	/// Charge une scène dans la propriété CurrentScene avec gestion spécialisée par type
	/// </summary>
	/// <param name="scenePath">Chemin vers la scène à charger</param>
	/// <param name="sceneType">Type de la classe de scène</param>
	private void LoadSceneInProperty(string scenePath, Type sceneType)
	{
		try
		{
			GD.Print($"📦 MainGameScene: Chargement de {sceneType.Name} dans CurrentScene...");
			
			// Décharger la scène précédente avec méthode spécialisée
			UnloadCurrentSceneSpecialized();

			// Créer une nouvelle instance de la scène
			var sceneInstance = Activator.CreateInstance(sceneType) as Node;
			if (sceneInstance is IScene scene)
			{
				// Ajouter comme enfant
				AddChild(sceneInstance);
				
				// Assigner aux propriétés
				_currentSceneNode = sceneInstance;
				_currentScene = scene;
				
				// Vérifier si c'est aussi une ILocation
				if (sceneInstance is ILocation location)
				{
					_currentLocationNode = sceneInstance;
					_currentLocation = location;
					GD.Print($"🏗️ MainGameScene: {sceneType.Name} est aussi une ILocation");
				}
				
				// Appeler la méthode de chargement spécialisée selon le type
				LoadSceneSpecialized(sceneInstance, sceneType);
				
				GD.Print($"✅ MainGameScene: {sceneType.Name} chargée dans CurrentScene");
			}
			else
			{
				GD.PrintErr($"❌ MainGameScene: {sceneType.Name} n'implémente pas IScene");
				sceneInstance?.QueueFree();
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"❌ MainGameScene: Erreur lors du chargement de {sceneType.Name}: {ex.Message}");
		}
	}

	/// <summary>
	/// Charge une location dans la propriété CurrentLocation
	/// </summary>
	/// <param name="locationType">Type de la location à charger</param>
	public void LoadLocationInProperty(Type locationType)
	{
		try
		{
			GD.Print($"🏗️ MainGameScene: Chargement de {locationType.Name} dans CurrentLocation...");
			
			// Vérifier que le type implémente ILocation
			if (!typeof(ILocation).IsAssignableFrom(locationType))
			{
				GD.PrintErr($"❌ MainGameScene: {locationType.Name} n'implémente pas ILocation");
				return;
			}

			// Décharger la location précédente
			UnloadCurrentLocationSpecialized();

			// Créer une nouvelle instance de la location
			var locationInstance = Activator.CreateInstance(locationType) as Node;
			if (locationInstance is ILocation location)
			{
				// Ajouter comme enfant
				AddChild(locationInstance);
				
				// Assigner aux propriétés
				_currentLocationNode = locationInstance;
				_currentLocation = location;
				
				// Vérifier si c'est aussi une IScene
				if (locationInstance is IScene scene)
				{
					_currentSceneNode = locationInstance;
					_currentScene = scene;
					GD.Print($"📦 MainGameScene: {locationType.Name} est aussi une IScene");
				}
				
				// Appeler la méthode de chargement spécialisée pour les locations
				LoadLocationSpecialized(location, locationType);
				
				GD.Print($"✅ MainGameScene: {locationType.Name} chargée dans CurrentLocation");
			}
			else
			{
				GD.PrintErr($"❌ MainGameScene: Impossible de créer l'instance de {locationType.Name}");
				locationInstance?.QueueFree();
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"❌ MainGameScene: Erreur lors du chargement de {locationType.Name}: {ex.Message}");
		}
	}

	/// <summary>
	/// Méthode spécialisée pour charger différents types de locations
	/// </summary>
	/// <param name="location">Instance de la location</param>
	/// <param name="locationType">Type de la location</param>
	private void LoadLocationSpecialized(ILocation location, Type locationType)
	{
		GD.Print($"🏗️ MainGameScene: Configuration spécialisée pour location {locationType.Name}...");

		// Connecter aux événements de la location
		location.LocationLoaded += OnLocationLoaded;
		location.LocationUnloaded += OnLocationUnloaded;
		location.PlayerEntered += OnPlayerEnteredLocation;
		location.PlayerExited += OnPlayerExitedLocation;
		location.InteractionOccurred += OnLocationInteractionOccurred;

		// Initialiser et charger la location si nécessaire
		if (!location.IsLoaded)
		{
			location.Initialize();
			location.LoadLocation();
		}

		// Activer la location
		location.ActivateLocation();

		// Configuration spécifique selon le type de location
		switch (location.Type)
		{
			case LocationType.Interior:
				ConfigureInteriorLocation(location);
				break;
			case LocationType.Exterior:
				ConfigureExteriorLocation(location);
				break;
			case LocationType.Combat:
				ConfigureCombatLocation(location);
				break;
			case LocationType.Social:
				ConfigureSocialLocation(location);
				break;
			case LocationType.Shop:
				ConfigureShopLocation(location);
				break;
			default:
				ConfigureDefaultLocation(location);
				break;
		}

		GD.Print($"⚙️ MainGameScene: Configuration location {locationType.Name} appliquée");
	}

	/// <summary>
	/// Décharge la location courante avec méthode spécialisée
	/// </summary>
	private void UnloadCurrentLocationSpecialized()
	{
		if (_currentLocationNode == null || _currentLocation == null) return;

		GD.Print($"🗑️ MainGameScene: Déchargement spécialisé de la location {_currentLocationNode.GetType().Name}");

		// Déconnecter les événements de la location
		_currentLocation.LocationLoaded -= OnLocationLoaded;
		_currentLocation.LocationUnloaded -= OnLocationUnloaded;
		_currentLocation.PlayerEntered -= OnPlayerEnteredLocation;
		_currentLocation.PlayerExited -= OnPlayerExitedLocation;
		_currentLocation.InteractionOccurred -= OnLocationInteractionOccurred;

		// Désactiver et décharger la location
		_currentLocation.DeactivateLocation();
		_currentLocation.UnloadLocation();

		// Nettoyage commun
		RemoveChild(_currentLocationNode);
		_currentLocationNode.QueueFree();
		_currentLocationNode = null;
		_currentLocation = null;

		// Si la location était aussi la CurrentScene, nettoyer aussi
		if (_currentSceneNode == _currentLocationNode)
		{
			_currentSceneNode = null;
			_currentScene = null;
		}

		GD.Print("✅ MainGameScene: Déchargement location spécialisé terminé");
	}

	/// <summary>
	/// Méthode spécialisée pour charger différents types de scènes
	/// </summary>
	/// <param name="sceneInstance">Instance de la scène</param>
	/// <param name="sceneType">Type de la scène</param>
	private void LoadSceneSpecialized(Node sceneInstance, Type sceneType)
	{
		switch (sceneType.Name)
		{
			case nameof(Credits):
				LoadCreditsSpecialized(sceneInstance as Credits);
				break;
			case "Title":
				LoadTitleSpecialized(sceneInstance as Satsuki.Scenes.Title);
				break;
			case "LocationModel":
				// Si c'est une LocationModel, elle sera gérée par LoadLocationSpecialized
				if (sceneInstance is ILocation location)
				{
					LoadLocationSpecialized(location, sceneType);
				}
				else
				{
					LoadDefaultSceneSpecialized(sceneInstance as IScene);
				}
				break;
			default:
				// Vérifier si c'est une location
				if (sceneInstance is ILocation loc)
				{
					LoadLocationSpecialized(loc, sceneType);
				}
				else
				{
					LoadDefaultSceneSpecialized(sceneInstance as IScene);
				}
				break;
		}
	}

	/// <summary>
	/// Chargement spécialisé pour la scène Credits
	/// </summary>
	/// <param name="credits">Instance de Credits</param>
	private void LoadCreditsSpecialized(Credits credits)
	{
		if (credits == null) return;

		GD.Print("🎬 MainGameScene: Configuration spécialisée Credits...");

		// Connecter aux événements spécifiques de Credits
		credits.CreditsCompleted += OnCreditsCompleted;
		credits.LoadTitleSceneRequested += OnLoadTitleSceneRequested;

		// Configuration spécifique pour Credits
		// Ajuster la vitesse de fade si nécessaire
		credits.SetFadeSpeed(2.0f);

		// Log spécifique
		GD.Print("🔗 MainGameScene: Signaux Credits connectés");
		GD.Print("⚙️ MainGameScene: Configuration Credits appliquée");
	}

	/// <summary>
	/// Déchargement spécialisé pour la scène Credits
	/// </summary>
	/// <param name="credits">Instance de Credits</param>
	private void UnloadCreditsSpecialized(Credits credits)
	{
		if (credits == null) return;

		GD.Print("🎬 MainGameScene: Déchargement spécialisé Credits...");

		// Déconnecter les événements spécifiques
		credits.CreditsCompleted -= OnCreditsCompleted;
		credits.LoadTitleSceneRequested -= OnLoadTitleSceneRequested;

		// Logique de nettoyage spécifique à Credits
		// Par exemple : sauvegarder que les crédits ont été vus
		// PlayerData.SetCreditsViewed(true);

		GD.Print("🧹 MainGameScene: Credits déchargé avec nettoyage spécialisé");
	}

	/// <summary>
	/// Chargement spécialisé pour la scène Title
	/// </summary>
	/// <param name="title">Instance de Title</param>
	private void LoadTitleSpecialized(Satsuki.Scenes.Title title)
	{
		if (title == null) return;

		GD.Print("🎯 MainGameScene: Configuration spécialisée Title...");

		// Configuration spécifique pour Title
		// Par exemple : configurer les éléments UI, charger les données de sauvegarde, etc.

		// Si Title a des événements spécifiques, les connecter ici
		// title.GameStartRequested += OnGameStartRequested;
		// title.OptionsRequested += OnOptionsRequested;

		// Configuration du menu selon l'état du jeu
		// title.SetMenuState(GetMenuState());

		// Charger automatiquement LobbyEx dans CurrentLocation lors de l'initialisation de Title
		CallDeferred(nameof(LoadLobbyExForTitle));

		GD.Print("⚙️ MainGameScene: Configuration Title appliquée");
	}

	/// <summary>
	/// Charge LobbyEx dans CurrentLocation pour l'écran Title
	/// </summary>
	private void LoadLobbyExForTitle()
	{
		try
		{
			GD.Print("🏛️ MainGameScene: Chargement automatique de LobbyEx pour Title...");
			
			// Charger LobbyEx dans CurrentLocation
			LoadLocationByClassName("LobbyEx");
			
			// Vérifier que le chargement a réussi
			if (_currentLocation != null && _currentLocation.LocationName == "LobbyEx")
			{
				GD.Print("✅ MainGameScene: LobbyEx chargé avec succès pour Title");
				
				// Configurer LobbyEx pour l'écran titre
				ConfigureLobbyExForTitle();
			}
			else
			{
				GD.PrintErr("❌ MainGameScene: Échec du chargement de LobbyEx");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"❌ MainGameScene: Erreur lors du chargement de LobbyEx: {ex.Message}");
		}
	}

	/// <summary>
	/// Configure LobbyEx spécifiquement pour l'écran titre
	/// </summary>
	private void ConfigureLobbyExForTitle()
	{
		if (_currentLocation is Satsuki.Scenes.Locations.LobbyEx lobbyEx)
		{
			GD.Print("⚙️ MainGameScene: Configuration LobbyEx pour Title...");
			
			// Configuration spécifique du lobby pour l'écran titre
			// Par exemple : masquer certains éléments, activer mode "preview", etc.
			
			// Ajouter un message d'activité pour indiquer que le lobby est en mode titre
			lobbyEx.CallDeferred("UpdateLobbyActivity", "Lobby activé pour l'écran titre");
			
			GD.Print("✅ MainGameScene: LobbyEx configuré pour Title");
		}
	}
	/// <summary>
	/// Déchargement spécialisé pour la scène Title
	/// </summary>
	/// <param name="title">Instance de Title</param>
	private void UnloadTitleSpecialized(Satsuki.Scenes.Title title)
	{
		if (title == null) return;

		GD.Print("🎯 MainGameScene: Déchargement spécialisé Title...");

		// Déconnecter les événements spécifiques si ils existent
		// title.GameStartRequested -= OnGameStartRequested;
		// title.OptionsRequested -= OnOptionsRequested;

		// Décharger LobbyEx si il était chargé avec Title
		if (_currentLocation != null && _currentLocation.LocationName == "LobbyEx")
		{
			GD.Print("🏛️ MainGameScene: Déchargement de LobbyEx avec Title...");
			UnloadCurrentLocation();
		}

		// Logique de nettoyage spécifique à Title
		// Par exemple : sauvegarder les préférences du menu

		GD.Print("🧹 MainGameScene: Title déchargé avec nettoyage spécialisé");
	}

	/// <summary>
	/// Chargement par défaut pour les scènes non spécialisées
	/// </summary>
	/// <param name="scene">Instance de la scène</param>
	private void LoadDefaultSceneSpecialized(IScene scene)
	{
		if (scene == null) return;

		GD.Print($"📦 MainGameScene: Configuration par défaut pour {scene.GetType().Name}...");

		// Configuration générique pour toutes les scènes IScene
		// Par exemple : enregistrer la scène pour monitoring, initialiser des systèmes communs, etc.

		GD.Print("⚙️ MainGameScene: Configuration par défaut appliquée");
	}

	/// <summary>
	/// Déchargement par défaut pour les scènes non spécialisées
	/// </summary>
	/// <param name="scene">Instance de la scène</param>
	private void UnloadDefaultSceneSpecialized(IScene scene)
	{
		if (scene == null) return;

		GD.Print($"📦 MainGameScene: Déchargement par défaut pour {scene.GetType().Name}...");

		// Nettoyage générique pour toutes les scènes IScene
		// Par exemple : désenregistrer du monitoring, nettoyer les ressources communes, etc.

		GD.Print("🧹 MainGameScene: Déchargement par défaut terminé");
	}

	/// <summary>
	/// Décharge la scène courante avec méthode spécialisée
	/// </summary>
	private void UnloadCurrentSceneSpecialized()
	{
		if (_currentSceneNode == null) return;

		GD.Print($"🗑️ MainGameScene: Déchargement spécialisé de {_currentSceneNode.GetType().Name}");

		// Appeler la méthode de déchargement spécialisée selon le type
		switch (_currentSceneNode.GetType().Name)
		{
			case nameof(Credits):
				UnloadCreditsSpecialized(_currentSceneNode as Credits);
				break;
			case "Title":
				UnloadTitleSpecialized(_currentSceneNode as Satsuki.Scenes.Title);
				break;
			default:
				// Si c'est une location, elle sera gérée par UnloadCurrentLocationSpecialized
				if (_currentSceneNode is ILocation)
				{
					// Ne pas décharger ici, sera géré par UnloadCurrentLocationSpecialized
					return;
				}
				else
				{
					UnloadDefaultSceneSpecialized(_currentSceneNode as IScene);
				}
				break;
		}

		// Nettoyage commun seulement si ce n'est pas une location
		if (!(_currentSceneNode is ILocation))
		{
			RemoveChild(_currentSceneNode);
			_currentSceneNode.QueueFree();
			_currentSceneNode = null;
			_currentScene = null;
		}

		GD.Print("✅ MainGameScene: Déchargement spécialisé terminé");
	}

	/// <summary>
	/// Charge la scène Credits dans CurrentScene
	/// </summary>
	private void LoadCreditsScene()
	{
		if (_hasLoadedCredits) return;
		
		try
		{
			GD.Print("🎬 MainGameScene: Chargement de Credits dans CurrentScene...");
			
			LoadSceneInProperty("res://Scenes/Credits.tscn", typeof(Credits));
			_hasLoadedCredits = true;
			
			GD.Print("✅ MainGameScene: Credits chargé dans CurrentScene");
		}
		catch (Exception ex)
		{
			GD.PrintErr($"❌ MainGameScene: Erreur lors du chargement de Credits: {ex.Message}");
		}
	}

	/// <summary>
	/// Charge la scène Title dans CurrentScene
	/// </summary>
	private void LoadTitleScene()
	{
		try
		{
			GD.Print("🎯 MainGameScene: Chargement de Title dans CurrentScene...");
			
			LoadSceneInProperty("res://Scenes/Title.tscn", typeof(Satsuki.Scenes.Title));
			
			GD.Print("✅ MainGameScene: Title chargé dans CurrentScene");
		}
		catch (Exception ex)
		{
			GD.PrintErr($"❌ MainGameScene: Erreur lors du chargement de Title: {ex.Message}");
		}
	}

	/// <summary>
	/// Décharge la scène courante (API publique)
	/// </summary>
	public void UnloadCurrentScene()
	{
		UnloadCurrentSceneSpecialized();
	}

	/// <summary>
	/// Décharge la location courante (API publique)
	/// </summary>
	public void UnloadCurrentLocation()
	{
		UnloadCurrentLocationSpecialized();
	}

	/// <summary>
	/// Obtient des informations sur la scène courante
	/// </summary>
	/// <returns>Informations détaillées sur la CurrentScene</returns>
	public object GetCurrentSceneInfo()
	{
		if (_currentScene == null || _currentSceneNode == null)
		{
			return new
			{
				HasScene = false,
				SceneName = "None",
				SceneType = "None"
			};
		}

		return new
		{
			HasScene = true,
			SceneName = _currentSceneNode.GetType().Name,
			SceneType = _currentSceneNode.GetType().FullName,
			SceneState = _currentScene.GetSceneState(),
			NodePath = _currentSceneNode.GetPath().ToString(),
			IsReady = _currentSceneNode.IsInsideTree()
		};
	}

	/// <summary>
	/// Obtient des informations sur la location courante
	/// </summary>
	/// <returns>Informations détaillées sur la CurrentLocation</returns>
	public object GetCurrentLocationInfo()
	{
		if (_currentLocation == null || _currentLocationNode == null)
		{
			return new
			{
				HasLocation = false,
				LocationName = "None",
				LocationId = "None",
				LocationType = "None"
			};
		}

		return new
		{
			HasLocation = true,
			LocationName = _currentLocation.LocationName,
			LocationId = _currentLocation.LocationId,
			LocationType = _currentLocation.Type.ToString(),
			LocationDescription = _currentLocation.Description,
			IsLoaded = _currentLocation.IsLoaded,
			IsAccessible = _currentLocation.IsAccessible,
			LocationState = _currentLocation.GetLocationState(),
			NodePath = _currentLocationNode.GetPath().ToString(),
			IsReady = _currentLocationNode.IsInsideTree(),
			PlayersInLocation = _currentLocation.GetPlayersInLocation(),
			InteractablesCount = _currentLocation.GetInteractables().Length,
			SpawnPointsCount = _currentLocation.GetSpawnPoints().Length
		};
	}
	#endregion

	#region Location Event Handlers
	/// <summary>
	/// Callback quand une location est chargée
	/// </summary>
	private void OnLocationLoaded(ILocation location)
	{
		GD.Print($"🏗️ MainGameScene: Location {location.LocationName} chargée");
		
		// Logique additionnelle lors du chargement d'une location
		// Par exemple : mettre à jour l'UI, notifier les clients, etc.
	}

	/// <summary>
	/// Callback quand une location est déchargée
	/// </summary>
	private void OnLocationUnloaded(ILocation location)
	{
		GD.Print($"🗑️ MainGameScene: Location {location.LocationName} déchargée");
		
		// Logique additionnelle lors du déchargement d'une location
	}

	/// <summary>
	/// Callback quand un joueur entre dans une location
	/// </summary>
	private void OnPlayerEnteredLocation(ILocation location, string playerId)
	{
		GD.Print($"👤 MainGameScene: Joueur {playerId} entre dans {location.LocationName}");
		
		// Notifier le serveur et les autres clients
		_gameServerHandler?.BroadcastToAllClients($"LOCATION_ENTER:{playerId}:{location.LocationId}", true);
	}

	/// <summary>
	/// Callback quand un joueur sort d'une location
	/// </summary>
	private void OnPlayerExitedLocation(ILocation location, string playerId)
	{
		GD.Print($"👤 MainGameScene: Joueur {playerId} sort de {location.LocationName}");
		
		// Notifier le serveur et les autres clients
		_gameServerHandler?.BroadcastToAllClients($"LOCATION_EXIT:{playerId}:{location.LocationId}", true);
	}

	/// <summary>
	/// Callback quand une interaction se produit dans une location
	/// </summary>
	private void OnLocationInteractionOccurred(ILocation location, string playerId, string interactionId)
	{
		GD.Print($"🤝 MainGameScene: Interaction {interactionId} par {playerId} dans {location.LocationName}");
		
		// Notifier le serveur et les autres clients
		_gameServerHandler?.BroadcastToAllClients($"LOCATION_INTERACTION:{playerId}:{location.LocationId}:{interactionId}", true);
	}
	#endregion

	#region Location Configuration Methods
	/// <summary>
	/// Configure une location d'intérieur
	/// </summary>
	private void ConfigureInteriorLocation(ILocation location)
	{
		GD.Print($"🏠 MainGameScene: Configuration location intérieur {location.LocationName}");
		// Configuration spécifique aux intérieurs
	}

	/// <summary>
	/// Configure une location d'extérieur
	/// </summary>
	private void ConfigureExteriorLocation(ILocation location)
	{
		GD.Print($"🌳 MainGameScene: Configuration location extérieur {location.LocationName}");
		// Configuration spécifique aux extérieurs
	}

	/// <summary>
	/// Configure une location de combat
	/// </summary>
	private void ConfigureCombatLocation(ILocation location)
	{
		GD.Print($"⚔️ MainGameScene: Configuration location combat {location.LocationName}");
		// Configuration spécifique aux zones de combat
	}

	/// <summary>
	/// Configure une location sociale
	/// </summary>
	private void ConfigureSocialLocation(ILocation location)
	{
		GD.Print($"👥 MainGameScene: Configuration location sociale {location.LocationName}");
		// Configuration spécifique aux zones sociales
	}

	/// <summary>
	/// Configure une location de magasin
	/// </summary>
	private void ConfigureShopLocation(ILocation location)
	{
		GD.Print($"🏪 MainGameScene: Configuration location magasin {location.LocationName}");
		// Configuration spécifique aux magasins
	}

	/// <summary>
	/// Configuration par défaut pour une location
	/// </summary>
	private void ConfigureDefaultLocation(ILocation location)
	{
		GD.Print($"🏗️ MainGameScene: Configuration par défaut location {location.LocationName}");
		// Configuration générique
	}
	#endregion

	/// <summary>
	/// Callback quand les crédits sont terminés
	/// </summary>
	private void OnCreditsCompleted()
	{
		GD.Print("🎉 MainGameScene: Crédits terminés - transition vers Title");
		
		// Ici vous pouvez ajouter de la logique supplémentaire
		// Par exemple : sauvegarder que les crédits ont été vus
		// PlayerData.SetCreditsViewed(true);
	}

	/// <summary>
	/// Callback pour charger la scène Title
	/// </summary>
	private void OnLoadTitleSceneRequested()
	{
		GD.Print("🎯 MainGameScene: Demande de chargement de Title reçue");
		LoadTitleScene();
	}

	#region IScene Implementation
	/// <summary>
	/// Retourne l'état actuel de la scène de jeu incluant la CurrentScene et CurrentLocation
	/// </summary>
	/// <returns>Un objet contenant l'état de la scène de jeu, CurrentScene et CurrentLocation</returns>
	public object GetSceneState()
	{
		// Récupérer l'état de la CurrentScene si elle existe
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

		// Récupérer l'état de la CurrentLocation si elle existe
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
	/// <returns>Un objet contenant l'état de la scène de jeu</returns>
	public object GetGameSceneState()
	{
		return GetSceneState();
	}
	#endregion

	#region Scene Management
	public void ChangeScene(string scenePath = "res://Scenes/OtherScene.tscn")
	{
		GetTree().ChangeSceneToFile(scenePath);
	}

	/// <summary>
	/// Charge la scène Credits manuellement dans CurrentScene
	/// </summary>
	public void LoadCredits()
	{
		LoadCreditsScene();
	}

	/// <summary>
	/// Charge la scène Title manuellement dans CurrentScene
	/// </summary>
	public void LoadTitle()
	{
		LoadTitleScene();
	}

	/// <summary>
	/// Charge une scène personnalisée dans CurrentScene
	/// </summary>
	/// <param name="sceneType">Type de la scène à charger</param>
	public void LoadCustomScene(Type sceneType)
	{
		if (sceneType.IsSubclassOf(typeof(Node)) && typeof(IScene).IsAssignableFrom(sceneType))
		{
			LoadSceneInProperty("", sceneType);
		}
		else
		{
			GD.PrintErr($"❌ MainGameScene: {sceneType.Name} doit être un Node et implémenter IScene");
		}
	}

	/// <summary>
	/// Charge une location personnalisée dans CurrentLocation
	/// </summary>
	/// <param name="locationType">Type de la location à charger</param>
	public void LoadCustomLocation(Type locationType)
	{
		if (locationType.IsSubclassOf(typeof(Node)) && typeof(ILocation).IsAssignableFrom(locationType))
		{
			LoadLocationInProperty(locationType);
		}
		else
		{
			GD.PrintErr($"❌ MainGameScene: {locationType.Name} doit être un Node et implémenter ILocation");
		}
	}

	/// <summary>
	/// Charge une location par nom de classe
	/// </summary>
	/// <param name="locationClassName">Nom de la classe de location</param>
	public void LoadLocationByClassName(string locationClassName)
	{
		try
		{
			// Rechercher le type dans l'assembly actuel
			var assembly = System.Reflection.Assembly.GetExecutingAssembly();
			var locationType = assembly.GetType(locationClassName);
			
			if (locationType == null)
			{
				// Essayer avec le namespace Satsuki.Scenes.Locations
				locationType = assembly.GetType($"Satsuki.Scenes.Locations.{locationClassName}");
			}

			if (locationType != null && typeof(ILocation).IsAssignableFrom(locationType))
			{
				LoadLocationInProperty(locationType);
			}
			else
			{
				GD.PrintErr($"❌ MainGameScene: Type de location '{locationClassName}' non trouvé ou n'implémente pas ILocation");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"❌ MainGameScene: Erreur lors du chargement de la location '{locationClassName}': {ex.Message}");
		}
	}

	/// <summary>
	/// Fait entrer un joueur dans la location courante
	/// </summary>
	/// <param name="playerId">ID du joueur</param>
	public void PlayerEnterCurrentLocation(string playerId)
	{
		if (_currentLocation != null)
		{
			_currentLocation.OnPlayerEnter(playerId);
		}
		else
		{
			GD.PrintErr("❌ MainGameScene: Aucune location courante pour faire entrer le joueur");
		}
	}

	/// <summary>
	/// Fait sortir un joueur de la location courante
	/// </summary>
	/// <param name="playerId">ID du joueur</param>
	public void PlayerExitCurrentLocation(string playerId)
	{
		if (_currentLocation != null)
		{
			_currentLocation.OnPlayerExit(playerId);
		}
		else
		{
			GD.PrintErr("❌ MainGameScene: Aucune location courante pour faire sortir le joueur");
		}
	}

	/// <summary>
	/// Traite une interaction dans la location courante
	/// </summary>
	/// <param name="playerId">ID du joueur</param>
	/// <param name="interactionId">ID de l'interaction</param>
	/// <param name="data">Données additionnelles</param>
	public void ProcessLocationInteraction(string playerId, string interactionId, object data = null)
	{
		if (_currentLocation != null)
		{
			_currentLocation.ProcessInteraction(playerId, interactionId, data);
		}
		else
		{
			GD.PrintErr("❌ MainGameScene: Aucune location courante pour traiter l'interaction");
		}
	}

	/// <summary>
	/// Obtient les joueurs présents dans la location courante
	/// </summary>
	/// <returns>Array des IDs des joueurs ou array vide si pas de location</returns>
	public string[] GetPlayersInCurrentLocation()
	{
		return _currentLocation?.GetPlayersInLocation() ?? new string[0];
	}

	/// <summary>
	/// Obtient les objets interactables de la location courante
	/// </summary>
	/// <returns>Array des interactables ou array vide si pas de location</returns>
	public IInteractable[] GetCurrentLocationInteractables()
	{
		return _currentLocation?.GetInteractables() ?? new IInteractable[0];
	}
	#endregion

	#region Input Handling (Debug Commands)
	/// <summary>
	/// Commandes Input pour tests et debug - délègue au GameServerHandler, CurrentScene et CurrentLocation
	/// </summary>
	public override void _Input(InputEvent @event)
	{
		// Déléguer les inputs à la CurrentScene d'abord
		if (_currentSceneNode != null)
		{
			_currentSceneNode._Input(@event);
		}

		// Puis traiter les commandes debug de MainGameScene
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
				case Key.F11:
					// Recharger manuellement les crédits
					if (!_hasLoadedCredits)
					{
						LoadCreditsScene();
					}
					else
					{
						GD.Print("🎬 Credits déjà chargés");
					}
					break;
				case Key.F12:
					// Charger la scène Title manuellement (debug)
					LoadTitleScene();
					break;
				case Key.Delete:
					// Décharger la CurrentScene (debug)
					UnloadCurrentScene();
					GD.Print("🗑️ CurrentScene déchargée");
					break;
				case Key.Home:
					// Charger une location de test (LocationModel)
					LoadLocationByClassName("LocationModel");
					GD.Print("🏗️ LocationModel chargée dans CurrentLocation");
					break;
				case Key.End:
					// Décharger la CurrentLocation (debug)
					UnloadCurrentLocation();
					GD.Print("🗑️ CurrentLocation déchargée");
					break;
				case Key.Menu:
					// Afficher les infos de la CurrentLocation
					var locationInfo = GetCurrentLocationInfo();
					GD.Print($"🏗️ Info CurrentLocation: {System.Text.Json.JsonSerializer.Serialize(locationInfo)}");
					break;
				case Key.Minus:
					// Simuler l'entrée d'un joueur dans la location courante
					PlayerEnterCurrentLocation("TestPlayer");
					GD.Print("👤 TestPlayer entre dans CurrentLocation");
					break;
				case Key.Equal:
					// Afficher les joueurs dans la location courante
					var players = GetPlayersInCurrentLocation();
					GD.Print($"👥 Joueurs dans CurrentLocation: {string.Join(", ", players)}");
					break;
				case Key.Backspace:
					// Afficher les interactables de la location courante
					var interactables = GetCurrentLocationInteractables();
					GD.Print($"🤝 Interactables dans CurrentLocation: {interactables.Length}");
					foreach (var interactable in interactables)
					{
						GD.Print($"  - {interactable.DisplayName} ({interactable.InteractableId})");
					}
					break;
				case Key.L:
					// Charger LobbyEx manuellement (debug)
					LoadLocationByClassName("LobbyEx");
					GD.Print("🏛️ LobbyEx chargé manuellement");
					break;
				case Key.T:
					// Tester la configuration Title + LobbyEx (debug)
					LoadTitleScene();
					GD.Print("🎯 Title + LobbyEx chargés ensemble");
					break;
			}
		}
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
		// Décharger la CurrentLocation
		UnloadCurrentLocation();

		// Décharger la CurrentScene
		UnloadCurrentScene();

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
