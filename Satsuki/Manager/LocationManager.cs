using Godot;
using Satsuki.Interfaces;
using Satsuki.Scenes.Locations;
using System;
using System.Collections.Generic;
using System.Reflection;

namespace Satsuki.Manager
{
	/// <summary>
	/// Gestionnaire centralisé pour le chargement et déchargement des locations
	/// Gère les scènes Godot qui sont des LocationModel
	/// </summary>
	public partial class LocationManager : Node
	{
		#region Singleton
		private static LocationManager _instance;
		public static LocationManager Instance => _instance;
		#endregion

		#region Private Fields
		private ILocation _currentLocation;
		private Node _currentLocationNode;
		private Dictionary<string, PackedScene> _cachedScenes = new Dictionary<string, PackedScene>();
		private Dictionary<string, Type> _registeredLocationTypes = new Dictionary<string, Type>();
		#endregion

		#region Properties
		/// <summary>
		/// Location actuellement chargée
		/// </summary>
		public ILocation CurrentLocation => _currentLocation;

		/// <summary>
		/// Node de la location courante
		/// </summary>
		public Node CurrentLocationNode => _currentLocationNode;

		/// <summary>
		/// Indique si une location est chargée
		/// </summary>
		public bool HasLocation => _currentLocation != null;
		#endregion

		#region Events
		/// <summary>
		/// Événement déclenché quand une location est chargée
		/// </summary>
		public event Action<ILocation> LocationLoaded;

		/// <summary>
		/// Événement déclenché quand une location est déchargée
		/// </summary>
		public event Action<ILocation> LocationUnloaded;

		/// <summary>
		/// Événement déclenché quand le chargement d'une location échoue
		/// </summary>
		public event Action<string, string> LocationLoadFailed;
		#endregion

		#region Godot Lifecycle
		public override void _Ready()
		{
			if (_instance != null && _instance != this)
			{
				GD.PrintErr("?? LocationManager: Instance déjà existante, suppression de ce doublon");
				QueueFree();
				return;
			}

			_instance = this;
			GD.Print("??? LocationManager: Initialisation...");

			// Enregistrer automatiquement les types de locations disponibles
			RegisterAvailableLocationTypes();

			GD.Print("? LocationManager: Initialisé avec succès");
		}

		public override void _ExitTree()
		{
			// Décharger la location courante
			UnloadCurrentLocation();

			// Nettoyer le cache
			_cachedScenes.Clear();
			_registeredLocationTypes.Clear();

			if (_instance == this)
			{
				_instance = null;
			}

			GD.Print("?? LocationManager: Nettoyage terminé");
		}
		#endregion

		#region Location Registration
		/// <summary>
		/// Enregistre automatiquement les types de locations disponibles
		/// </summary>
		private void RegisterAvailableLocationTypes()
		{
			GD.Print("?? LocationManager: Enregistrement des types de locations...");

			var assembly = Assembly.GetExecutingAssembly();
			var locationTypes = new List<Type>();

			foreach (var type in assembly.GetTypes())
			{
				if (typeof(ILocation).IsAssignableFrom(type) && 
				    type.IsClass && 
				    !type.IsAbstract &&
				    type.IsSubclassOf(typeof(Node)))
				{
					locationTypes.Add(type);
					_registeredLocationTypes[type.Name] = type;
					GD.Print($"  ? {type.Name}");
				}
			}

			GD.Print($"? LocationManager: {locationTypes.Count} types de locations enregistrés");
		}

		/// <summary>
		/// Enregistre manuellement un type de location
		/// </summary>
		public void RegisterLocationType(string name, Type locationType)
		{
			if (!typeof(ILocation).IsAssignableFrom(locationType))
			{
				GD.PrintErr($"? LocationManager: {locationType.Name} n'implémente pas ILocation");
				return;
			}

			if (!locationType.IsSubclassOf(typeof(Node)))
			{
				GD.PrintErr($"? LocationManager: {locationType.Name} n'hérite pas de Node");
				return;
			}

			_registeredLocationTypes[name] = locationType;
			GD.Print($"? LocationManager: Type '{name}' enregistré");
		}

		/// <summary>
		/// Obtient la liste des types de locations enregistrés
		/// </summary>
		public string[] GetRegisteredLocationTypes()
		{
			var types = new List<string>(_registeredLocationTypes.Keys);
			return types.ToArray();
		}
		#endregion

		#region Location Loading - By Scene Path
		/// <summary>
		/// Charge une location depuis un chemin de scène Godot (.tscn)
		/// </summary>
		/// <param name="scenePath">Chemin vers le fichier .tscn</param>
		/// <param name="useCache">Utiliser le cache de scènes</param>
		public bool LoadLocationFromScene(string scenePath, bool useCache = true)
		{
			try
			{
				GD.Print($"??? LocationManager: Chargement location depuis '{scenePath}'...");

				// Décharger la location courante
				UnloadCurrentLocation();

				// Charger la scène
				PackedScene scene = null;

				if (useCache && _cachedScenes.ContainsKey(scenePath))
				{
					scene = _cachedScenes[scenePath];
					GD.Print("  ?? Scène trouvée dans le cache");
				}
				else
				{
					scene = GD.Load<PackedScene>(scenePath);
					if (scene == null)
					{
						GD.PrintErr($"? LocationManager: Impossible de charger la scène '{scenePath}'");
						LocationLoadFailed?.Invoke(scenePath, "Scene not found");
						return false;
					}

					if (useCache)
					{
						_cachedScenes[scenePath] = scene;
						GD.Print("  ?? Scène mise en cache");
					}
				}

				// Instancier la scène
				var instance = scene.Instantiate();
				if (instance == null)
				{
					GD.PrintErr($"? LocationManager: Impossible d'instancier la scène '{scenePath}'");
					LocationLoadFailed?.Invoke(scenePath, "Failed to instantiate");
					return false;
				}

				// Vérifier que c'est bien une ILocation
				if (instance is not ILocation location)
				{
					GD.PrintErr($"? LocationManager: La scène '{scenePath}' n'implémente pas ILocation");
					instance.QueueFree();
					LocationLoadFailed?.Invoke(scenePath, "Not an ILocation");
					return false;
				}

				// Ajouter à l'arbre de scène
				AddChild(instance);

				// Stocker les références
				_currentLocationNode = instance;
				_currentLocation = location;

				// Connecter aux événements de la location
				ConnectLocationEvents(location);

				// Initialiser et charger si nécessaire
				if (!location.IsLoaded)
				{
					location.Initialize();
					location.LoadLocation();
				}

				// Activer la location
				location.ActivateLocation();

				GD.Print($"? LocationManager: Location '{location.LocationName}' chargée avec succès");
				LocationLoaded?.Invoke(location);

				return true;
			}
			catch (Exception ex)
			{
				GD.PrintErr($"? LocationManager: Erreur lors du chargement de '{scenePath}': {ex.Message}");
				LocationLoadFailed?.Invoke(scenePath, ex.Message);
				return false;
			}
		}
		#endregion

		#region Location Loading - By Type
		/// <summary>
		/// Charge une location par son type (création d'instance programmatique)
		/// </summary>
		public bool LoadLocationByType(Type locationType)
		{
			try
			{
				GD.Print($"??? LocationManager: Chargement location de type '{locationType.Name}'...");

				if (!typeof(ILocation).IsAssignableFrom(locationType))
				{
					GD.PrintErr($"? LocationManager: {locationType.Name} n'implémente pas ILocation");
					LocationLoadFailed?.Invoke(locationType.Name, "Not an ILocation");
					return false;
				}

				if (!locationType.IsSubclassOf(typeof(Node)))
				{
					GD.PrintErr($"? LocationManager: {locationType.Name} n'hérite pas de Node");
					LocationLoadFailed?.Invoke(locationType.Name, "Not a Node");
					return false;
				}

				// Décharger la location courante
				UnloadCurrentLocation();

				// Créer une instance
				var instance = Activator.CreateInstance(locationType) as Node;
				if (instance == null)
				{
					GD.PrintErr($"? LocationManager: Impossible de créer une instance de '{locationType.Name}'");
					LocationLoadFailed?.Invoke(locationType.Name, "Failed to instantiate");
					return false;
				}

				var location = instance as ILocation;

				// Ajouter à l'arbre de scène
				AddChild(instance);

				// Stocker les références
				_currentLocationNode = instance;
				_currentLocation = location;

				// Connecter aux événements
				ConnectLocationEvents(location);

				// Initialiser et charger
				if (!location.IsLoaded)
				{
					location.Initialize();
					location.LoadLocation();
				}

				// Activer
				location.ActivateLocation();

				GD.Print($"? LocationManager: Location '{location.LocationName}' chargée avec succès");
				LocationLoaded?.Invoke(location);

				return true;
			}
			catch (Exception ex)
			{
				GD.PrintErr($"? LocationManager: Erreur lors du chargement de '{locationType.Name}': {ex.Message}");
				LocationLoadFailed?.Invoke(locationType.Name, ex.Message);
				return false;
			}
		}

		/// <summary>
		/// Charge une location par son nom de type
		/// </summary>
		public bool LoadLocationByTypeName(string typeName)
		{
			if (_registeredLocationTypes.TryGetValue(typeName, out var locationType))
			{
				return LoadLocationByType(locationType);
			}

			// Essayer de trouver le type dans l'assembly
			var assembly = Assembly.GetExecutingAssembly();
			var type = assembly.GetType(typeName);

			if (type == null)
			{
				type = assembly.GetType($"Satsuki.Scenes.Locations.{typeName}");
			}

			if (type != null)
			{
				return LoadLocationByType(type);
			}

			GD.PrintErr($"? LocationManager: Type de location '{typeName}' non trouvé");
			LocationLoadFailed?.Invoke(typeName, "Type not found");
			return false;
		}
		#endregion

		#region Location Unloading
		/// <summary>
		/// Décharge la location courante
		/// </summary>
		public void UnloadCurrentLocation()
		{
			if (_currentLocation == null || _currentLocationNode == null)
			{
				return;
			}

			GD.Print($"??? LocationManager: Déchargement de '{_currentLocation.LocationName}'...");

			// Déconnecter les événements
			DisconnectLocationEvents(_currentLocation);

			// Désactiver et décharger
			_currentLocation.DeactivateLocation();
			_currentLocation.UnloadLocation();

			// Notifier avant de supprimer
			var locationBeingUnloaded = _currentLocation;
			LocationUnloaded?.Invoke(locationBeingUnloaded);

			// Supprimer de l'arbre
			RemoveChild(_currentLocationNode);
			_currentLocationNode.QueueFree();

			// Nettoyer les références
			_currentLocationNode = null;
			_currentLocation = null;

			GD.Print("? LocationManager: Location déchargée");
		}
		#endregion

		#region Event Management
		/// <summary>
		/// Connecte les événements d'une location
		/// </summary>
		private void ConnectLocationEvents(ILocation location)
		{
			location.LocationLoaded += OnLocationLoadedEvent;
			location.LocationUnloaded += OnLocationUnloadedEvent;
			location.PlayerEntered += OnPlayerEnteredLocation;
			location.PlayerExited += OnPlayerExitedLocation;
			location.InteractionOccurred += OnLocationInteraction;
		}

		/// <summary>
		/// Déconnecte les événements d'une location
		/// </summary>
		private void DisconnectLocationEvents(ILocation location)
		{
			location.LocationLoaded -= OnLocationLoadedEvent;
			location.LocationUnloaded -= OnLocationUnloadedEvent;
			location.PlayerEntered -= OnPlayerEnteredLocation;
			location.PlayerExited -= OnPlayerExitedLocation;
			location.InteractionOccurred -= OnLocationInteraction;
		}

		private void OnLocationLoadedEvent(ILocation location)
		{
			GD.Print($"?? LocationManager: Location '{location.LocationName}' chargée");
		}

		private void OnLocationUnloadedEvent(ILocation location)
		{
			GD.Print($"?? LocationManager: Location '{location.LocationName}' déchargée");
		}

		private void OnPlayerEnteredLocation(ILocation location, string playerId)
		{
			GD.Print($"?? LocationManager: Joueur '{playerId}' entre dans '{location.LocationName}'");
		}

		private void OnPlayerExitedLocation(ILocation location, string playerId)
		{
			GD.Print($"?? LocationManager: Joueur '{playerId}' sort de '{location.LocationName}'");
		}

		private void OnLocationInteraction(ILocation location, string playerId, string interactionId)
		{
			GD.Print($"?? LocationManager: Interaction '{interactionId}' par '{playerId}' dans '{location.LocationName}'");
		}
		#endregion

		#region Cache Management
		/// <summary>
		/// Précharge une scène dans le cache
		/// </summary>
		public bool PreloadScene(string scenePath)
		{
			if (_cachedScenes.ContainsKey(scenePath))
			{
				GD.Print($"?? LocationManager: Scène '{scenePath}' déjà en cache");
				return true;
			}

			try
			{
				var scene = GD.Load<PackedScene>(scenePath);
				if (scene != null)
				{
					_cachedScenes[scenePath] = scene;
					GD.Print($"?? LocationManager: Scène '{scenePath}' mise en cache");
					return true;
				}
			}
			catch (Exception ex)
			{
				GD.PrintErr($"? LocationManager: Erreur lors du préchargement de '{scenePath}': {ex.Message}");
			}

			return false;
		}

		/// <summary>
		/// Vide le cache de scènes
		/// </summary>
		public void ClearCache()
		{
			_cachedScenes.Clear();
			GD.Print("?? LocationManager: Cache vidé");
		}

		/// <summary>
		/// Obtient le nombre de scènes en cache
		/// </summary>
		public int GetCachedSceneCount()
		{
			return _cachedScenes.Count;
		}
		#endregion

		#region Player Management Shortcuts
		/// <summary>
		/// Fait entrer un joueur dans la location courante
		/// </summary>
		public void PlayerEnter(string playerId)
		{
			if (_currentLocation != null)
			{
				_currentLocation.OnPlayerEnter(playerId);
			}
			else
			{
				GD.PrintErr("? LocationManager: Aucune location courante");
			}
		}

		/// <summary>
		/// Fait sortir un joueur de la location courante
		/// </summary>
		public void PlayerExit(string playerId)
		{
			if (_currentLocation != null)
			{
				_currentLocation.OnPlayerExit(playerId);
			}
			else
			{
				GD.PrintErr("? LocationManager: Aucune location courante");
			}
		}

		/// <summary>
		/// Obtient les joueurs dans la location courante
		/// </summary>
		public string[] GetPlayersInCurrentLocation()
		{
			return _currentLocation?.GetPlayersInLocation() ?? Array.Empty<string>();
		}
		#endregion

		#region Location Info
		/// <summary>
		/// Obtient les informations complètes sur la location courante
		/// </summary>
		public object GetCurrentLocationInfo()
		{
			if (_currentLocation == null)
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
				NodePath = _currentLocationNode?.GetPath().ToString() ?? "",
				IsReady = _currentLocationNode?.IsInsideTree() ?? false,
				PlayersCount = _currentLocation.GetPlayersInLocation().Length,
				InteractablesCount = _currentLocation.GetInteractables().Length,
				SpawnPointsCount = _currentLocation.GetSpawnPoints().Length
			};
		}
		#endregion
	}
}
