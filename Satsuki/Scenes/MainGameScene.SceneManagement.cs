using Godot;
using Satsuki.Interfaces;
using Satsuki.Scenes.Locations;
using System;

/// <summary>
/// Partie SceneManagement de MainGameScene
/// Gère le chargement/déchargement des scènes (Credits, Title, etc.)
/// </summary>
public partial class MainGameScene
{
	#region Scene Loading Core
	/// <summary>
	/// Charge une scène dans la propriété CurrentScene avec gestion spécialisée par type
	/// </summary>
	private void LoadSceneInProperty(string scenePath, Type sceneType)
	{
		try
		{
			GD.Print($"📦 MainGameScene: Chargement de {sceneType.Name} dans CurrentScene...");
			
			UnloadCurrentSceneSpecialized();

			var sceneInstance = Activator.CreateInstance(sceneType) as Node;
			if (sceneInstance is IScene scene)
			{
				AddChild(sceneInstance);
				_currentSceneNode = sceneInstance;
				_currentScene = scene;
				
				if (sceneInstance is ILocation location)
				{
					_currentLocationNode = sceneInstance;
					_currentLocation = location;
					GD.Print($"🏗️ MainGameScene: {sceneType.Name} est aussi une ILocation");
				}
				
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
	/// Méthode spécialisée pour charger différents types de scènes
	/// </summary>
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
	/// Décharge la scène courante avec méthode spécialisée
	/// </summary>
	private void UnloadCurrentSceneSpecialized()
	{
		if (_currentSceneNode == null) return;

		GD.Print($"🗑️ MainGameScene: Déchargement spécialisé de {_currentSceneNode.GetType().Name}");

		switch (_currentSceneNode.GetType().Name)
		{
			case nameof(Credits):
				UnloadCreditsSpecialized(_currentSceneNode as Credits);
				break;
			case "Title":
				UnloadTitleSpecialized(_currentSceneNode as Satsuki.Scenes.Title);
				break;
			default:
				if (_currentSceneNode is ILocation)
				{
					return;
				}
				else
				{
					UnloadDefaultSceneSpecialized(_currentSceneNode as IScene);
				}
				break;
		}

		if (!(_currentSceneNode is ILocation))
		{
			RemoveChild(_currentSceneNode);
			_currentSceneNode.QueueFree();
			_currentSceneNode = null;
			_currentScene = null;
		}

		GD.Print("✅ MainGameScene: Déchargement spécialisé terminé");
	}
	#endregion

	#region Credits Specialized
	private void LoadCreditsSpecialized(Credits credits)
	{
		if (credits == null) return;

		GD.Print("🎬 MainGameScene: Configuration spécialisée Credits...");

		credits.CreditsCompleted += OnCreditsCompleted;
		credits.LoadTitleSceneRequested += OnLoadTitleSceneRequested;
		credits.SetFadeSpeed(2.0f);

		GD.Print("🔗 MainGameScene: Signaux Credits connectés");
		GD.Print("⚙️ MainGameScene: Configuration Credits appliquée");
	}

	private void UnloadCreditsSpecialized(Credits credits)
	{
		if (credits == null) return;

		GD.Print("🎬 MainGameScene: Déchargement spécialisé Credits...");

		credits.CreditsCompleted -= OnCreditsCompleted;
		credits.LoadTitleSceneRequested -= OnLoadTitleSceneRequested;

		GD.Print("🧹 MainGameScene: Credits déchargé avec nettoyage spécialisé");
	}

	private void OnCreditsCompleted()
	{
		GD.Print("🎉 MainGameScene: Crédits terminés - transition vers Title");
	}

	private void OnLoadTitleSceneRequested()
	{
		GD.Print("🎯 MainGameScene: Demande de chargement de Title reçue");
		LoadTitleScene();
	}
	#endregion

	#region Title Specialized
	private void LoadTitleSpecialized(Satsuki.Scenes.Title title)
	{
		if (title == null) return;

		GD.Print("🎯 MainGameScene: Configuration spécialisée Title...");
		
		// Charger automatiquement Restaurant.tscn via LocationManager
		GD.Print("🍽️ MainGameScene: Chargement de Restaurant.tscn en CurrentLocation...");
		CallDeferred(nameof(LoadRestaurantLocation));
		
		GD.Print("⚙️ MainGameScene: Configuration Title appliquée");
	}

	private void UnloadTitleSpecialized(Satsuki.Scenes.Title title)
	{
		if (title == null) return;

		GD.Print("🎯 MainGameScene: Déchargement spécialisé Title...");
		
		// Décharger la location Restaurant si elle est chargée
		if (_locationManager != null && _locationManager.HasLocation)
		{
			GD.Print("🍽️ MainGameScene: Déchargement de Restaurant.tscn...");
			_locationManager.UnloadCurrentLocation();
		}
		
		GD.Print("🧹 MainGameScene: Title déchargé avec nettoyage spécialisé");
	}
	
	/// <summary>
	/// Charge Restaurant.tscn via LocationManager (appelé en CallDeferred)
	/// </summary>
	private void LoadRestaurantLocation()
	{
		try
		{
			const string restaurantPath = "res://Scenes/Locations/Restaurant.tscn";
			
			bool success = _locationManager.LoadLocationFromScene(restaurantPath, useCache: true);
			
			if (success)
			{
				GD.Print($"✅ MainGameScene: Restaurant chargé dans CurrentLocation via LocationManager");
			}
			else
			{
				GD.PrintErr($"❌ MainGameScene: Échec du chargement de Restaurant.tscn");
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"❌ MainGameScene: Erreur lors du chargement de Restaurant: {ex.Message}");
		}
	}
	#endregion

	#region Default Scene Specialized
	private void LoadDefaultSceneSpecialized(IScene scene)
	{
		if (scene == null) return;

		GD.Print($"📦 MainGameScene: Configuration par défaut pour {scene.GetType().Name}...");
		GD.Print("⚙️ MainGameScene: Configuration par défaut appliquée");
	}

	private void UnloadDefaultSceneSpecialized(IScene scene)
	{
		if (scene == null) return;

		GD.Print($"📦 MainGameScene: Déchargement par défaut pour {scene.GetType().Name}...");
		GD.Print("🧹 MainGameScene: Déchargement par défaut terminé");
	}
	#endregion

	#region Specific Scene Loading Methods
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
	#endregion

	#region Public Scene API
	public void UnloadCurrentScene()
	{
		UnloadCurrentSceneSpecialized();
	}

	public void LoadCredits()
	{
		LoadCreditsScene();
	}

	public void LoadTitle()
	{
		LoadTitleScene();
	}

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

	public void ChangeScene(string scenePath = "res://Scenes/OtherScene.tscn")
	{
		GetTree().ChangeSceneToFile(scenePath);
	}

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
	#endregion
}
