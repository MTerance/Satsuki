using Godot;
using Satsuki.Interfaces;
using Satsuki.Scenes.Locations;
using System;
using System.Reflection;

/// <summary>
/// Partie LocationManagement de MainGameScene
/// Gère le chargement/déchargement des locations et leurs configurations
/// </summary>
public partial class MainGameScene
{
	#region Location Loading Core
	public void LoadLocationInProperty(Type locationType)
	{
		try
		{
			GD.Print($"??? MainGameScene: Chargement de {locationType.Name} dans CurrentLocation...");
			
			if (!typeof(ILocation).IsAssignableFrom(locationType))
			{
				GD.PrintErr($"? MainGameScene: {locationType.Name} n'implémente pas ILocation");
				return;
			}

			UnloadCurrentLocationSpecialized();

			var locationInstance = Activator.CreateInstance(locationType) as Node;
			if (locationInstance is ILocation location)
			{
				AddChild(locationInstance);
				_currentLocationNode = locationInstance;
				_currentLocation = location;
				
				if (locationInstance is IScene scene)
				{
					_currentSceneNode = locationInstance;
					_currentScene = scene;
					GD.Print($"?? MainGameScene: {locationType.Name} est aussi une IScene");
				}
				
				LoadLocationSpecialized(location, locationType);
				GD.Print($"? MainGameScene: {locationType.Name} chargée dans CurrentLocation");
			}
			else
			{
				GD.PrintErr($"? MainGameScene: Impossible de créer l'instance de {locationType.Name}");
				locationInstance?.QueueFree();
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"? MainGameScene: Erreur lors du chargement de {locationType.Name}: {ex.Message}");
		}
	}

	private void LoadLocationSpecialized(ILocation location, Type locationType)
	{
		GD.Print($"??? MainGameScene: Configuration spécialisée pour location {locationType.Name}...");

		location.LocationLoaded += OnLocationLoaded;
		location.LocationUnloaded += OnLocationUnloaded;
		location.PlayerEntered += OnPlayerEnteredLocation;
		location.PlayerExited += OnPlayerExitedLocation;
		location.InteractionOccurred += OnLocationInteractionOccurred;

		if (!location.IsLoaded)
		{
			location.Initialize();
			location.LoadLocation();
		}

		location.ActivateLocation();

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

		GD.Print($"?? MainGameScene: Configuration location {locationType.Name} appliquée");
	}

	private void UnloadCurrentLocationSpecialized()
	{
		if (_currentLocationNode == null || _currentLocation == null) return;

		GD.Print($"??? MainGameScene: Déchargement spécialisé de la location {_currentLocationNode.GetType().Name}");

		_currentLocation.LocationLoaded -= OnLocationLoaded;
		_currentLocation.LocationUnloaded -= OnLocationUnloaded;
		_currentLocation.PlayerEntered -= OnPlayerEnteredLocation;
		_currentLocation.PlayerExited -= OnPlayerExitedLocation;
		_currentLocation.InteractionOccurred -= OnLocationInteractionOccurred;

		_currentLocation.DeactivateLocation();
		_currentLocation.UnloadLocation();

		RemoveChild(_currentLocationNode);
		_currentLocationNode.QueueFree();
		_currentLocationNode = null;
		_currentLocation = null;

		if (_currentSceneNode == _currentLocationNode)
		{
			_currentSceneNode = null;
			_currentScene = null;
		}

		GD.Print("? MainGameScene: Déchargement location spécialisé terminé");
	}
	#endregion

	#region Location Event Handlers
	private void OnLocationLoaded(ILocation location)
	{
		GD.Print($"??? MainGameScene: Location {location.LocationName} chargée");
	}

	private void OnLocationUnloaded(ILocation location)
	{
		GD.Print($"??? MainGameScene: Location {location.LocationName} déchargée");
	}

	private void OnPlayerEnteredLocation(ILocation location, string playerId)
	{
		GD.Print($"?? MainGameScene: Joueur {playerId} entre dans {location.LocationName}");
		_gameServerHandler?.BroadcastToAllClients($"LOCATION_ENTER:{playerId}:{location.LocationId}", true);
	}

	private void OnPlayerExitedLocation(ILocation location, string playerId)
	{
		GD.Print($"?? MainGameScene: Joueur {playerId} sort de {location.LocationName}");
		_gameServerHandler?.BroadcastToAllClients($"LOCATION_EXIT:{playerId}:{location.LocationId}", true);
	}

	private void OnLocationInteractionOccurred(ILocation location, string playerId, string interactionId)
	{
		GD.Print($"?? MainGameScene: Interaction {interactionId} par {playerId} dans {location.LocationName}");
		_gameServerHandler?.BroadcastToAllClients($"LOCATION_INTERACTION:{playerId}:{location.LocationId}:{interactionId}", true);
	}
	#endregion

	#region Location Configuration Methods
	private void ConfigureInteriorLocation(ILocation location)
	{
		GD.Print($"?? MainGameScene: Configuration location intérieur {location.LocationName}");
	}

	private void ConfigureExteriorLocation(ILocation location)
	{
		GD.Print($"?? MainGameScene: Configuration location extérieur {location.LocationName}");
	}

	private void ConfigureCombatLocation(ILocation location)
	{
		GD.Print($"?? MainGameScene: Configuration location combat {location.LocationName}");
	}

	private void ConfigureSocialLocation(ILocation location)
	{
		GD.Print($"?? MainGameScene: Configuration location sociale {location.LocationName}");
	}

	private void ConfigureShopLocation(ILocation location)
	{
		GD.Print($"?? MainGameScene: Configuration location magasin {location.LocationName}");
	}

	private void ConfigureDefaultLocation(ILocation location)
	{
		GD.Print($"??? MainGameScene: Configuration par défaut location {location.LocationName}");
	}
	#endregion

	#region Public Location API
	public void UnloadCurrentLocation()
	{
		UnloadCurrentLocationSpecialized();
	}

	public void LoadCustomLocation(Type locationType)
	{
		if (locationType.IsSubclassOf(typeof(Node)) && typeof(ILocation).IsAssignableFrom(locationType))
		{
			LoadLocationInProperty(locationType);
		}
		else
		{
			GD.PrintErr($"? MainGameScene: {locationType.Name} doit être un Node et implémenter ILocation");
		}
	}

	public void LoadLocationByClassName(string locationClassName)
	{
		try
		{
			var assembly = Assembly.GetExecutingAssembly();
			var locationType = assembly.GetType(locationClassName);
			
			if (locationType == null)
			{
				locationType = assembly.GetType($"Satsuki.Scenes.Locations.{locationClassName}");
			}

			if (locationType != null && typeof(ILocation).IsAssignableFrom(locationType))
			{
				LoadLocationInProperty(locationType);
			}
			else
			{
				GD.PrintErr($"? MainGameScene: Type de location '{locationClassName}' non trouvé ou n'implémente pas ILocation");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"? MainGameScene: Erreur lors du chargement de la location '{locationClassName}': {ex.Message}");
		}
	}

	public void PlayerEnterCurrentLocation(string playerId)
	{
		if (_currentLocation != null)
		{
			_currentLocation.OnPlayerEnter(playerId);
		}
		else
		{
			GD.PrintErr("? MainGameScene: Aucune location courante pour faire entrer le joueur");
		}
	}

	public void PlayerExitCurrentLocation(string playerId)
	{
		if (_currentLocation != null)
		{
			_currentLocation.OnPlayerExit(playerId);
		}
		else
		{
			GD.PrintErr("? MainGameScene: Aucune location courante pour faire sortir le joueur");
		}
	}

	public void ProcessLocationInteraction(string playerId, string interactionId, object data = null)
	{
		if (_currentLocation != null)
		{
			_currentLocation.ProcessInteraction(playerId, interactionId, data);
		}
		else
		{
			GD.PrintErr("? MainGameScene: Aucune location courante pour traiter l'interaction");
		}
	}

	public string[] GetPlayersInCurrentLocation()
	{
		return _currentLocation?.GetPlayersInLocation() ?? new string[0];
	}

	public IInteractable[] GetCurrentLocationInteractables()
	{
		return _currentLocation?.GetInteractables() ?? new IInteractable[0];
	}

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
}
