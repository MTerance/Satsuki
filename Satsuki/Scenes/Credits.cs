using Godot;
using Satsuki.Manager;
using Satsuki.Interfaces;
using System;

public partial class Credits : Node, IScene
{
	private SplashScreenManager _splashScreenManager;
	private DateTime _sceneStartTime;
	private int _totalSkips = 0;
	
	public override void _Ready()
	{
		_sceneStartTime = DateTime.UtcNow;
		
		GD.Print("?? Credits: Initialisation...");
		
		// Créer et ajouter le SplashScreenManager
		_splashScreenManager = new SplashScreenManager();
		AddChild(_splashScreenManager);
		
		// S'abonner aux événements
		_splashScreenManager.SplashScreenCompleted += OnSplashScreenCompleted;
		_splashScreenManager.AllSplashScreensCompleted += OnAllSplashScreensCompleted;
		
		// Configurer les splash screens
		SetupSplashScreens();
		
		// Démarrer la séquence
		_splashScreenManager.StartSequence();
	}
	
	/// <summary>
	/// Retourne l'état actuel de la scène Credits
	/// </summary>
	public object GetSceneState()
	{
		var elapsedTime = (DateTime.UtcNow - _sceneStartTime).TotalSeconds;
		
		return new
		{
			SceneInfo = new
			{
				SceneName = "Credits",
				SceneType = "SplashScreen",
				StartTime = _sceneStartTime,
				ElapsedTime = Math.Round(elapsedTime, 2),
				ElapsedTimeFormatted = FormatElapsedTime(elapsedTime)
			},
			SplashScreens = new
			{
				TotalScreens = _splashScreenManager?.GetSplashScreenCount() ?? 0,
				CurrentIndex = _splashScreenManager?.GetCurrentIndex() ?? 0,
				RemainingScreens = (_splashScreenManager?.GetSplashScreenCount() ?? 0) - (_splashScreenManager?.GetCurrentIndex() ?? 0),
				Progress = _splashScreenManager != null && _splashScreenManager.GetSplashScreenCount() > 0
					? Math.Round((float)_splashScreenManager.GetCurrentIndex() / _splashScreenManager.GetSplashScreenCount() * 100, 2)
					: 0
			},
			UserInteraction = new
			{
				TotalSkips = _totalSkips,
				SkipRate = elapsedTime > 0 ? Math.Round(_totalSkips / elapsedTime * 60, 2) : 0 // Skips per minute
			},
			Status = new
			{
				IsCompleted = (_splashScreenManager?.GetCurrentIndex() ?? 0) >= (_splashScreenManager?.GetSplashScreenCount() ?? 0),
				IsActive = _splashScreenManager != null,
				Timestamp = DateTime.UtcNow
			}
		};
	}
	
	/// <summary>
	/// Formate le temps écoulé en format lisible
	/// </summary>
	private string FormatElapsedTime(double seconds)
	{
		int minutes = (int)(seconds / 60);
		int secs = (int)(seconds % 60);
		return $"{minutes:D2}:{secs:D2}";
	}
	
	/// <summary>
	/// Configure les splash screens des crédits
	/// </summary>
	private void SetupSplashScreens()
	{
		// Splash screen 1: Titre du jeu
		_splashScreenManager.AddTextSplash("SATSUKI", 2.5f, new Color(1.0f, 0.5f, 0.0f));
		
		// Splash screen 2: Développé par
		_splashScreenManager.AddTextSplash("Développé par\nMTerance", 2.0f, Colors.Cyan);
		
		// Splash screen 3: Remerciements
		_splashScreenManager.AddTextSplash("Merci d'avoir joué!", 2.0f, Colors.LightGreen);
		
		// Option: Ajouter des images si disponibles
		// _splashScreenManager.AddImageSplash("res://Assets/logo.png", 3.0f);
		
		GD.Print($"?? {_splashScreenManager.GetSplashScreenCount()} splash screens configurés");
	}
	
	/// <summary>
	/// Callback quand un splash screen est terminé
	/// </summary>
	private void OnSplashScreenCompleted()
	{
		int current = _splashScreenManager.GetCurrentIndex();
		int total = _splashScreenManager.GetSplashScreenCount();
		GD.Print($"? Splash screen {current}/{total} terminé");
	}
	
	/// <summary>
	/// Callback quand tous les splash screens sont terminés
	/// </summary>
	private void OnAllSplashScreensCompleted()
	{
		GD.Print("?? Tous les crédits ont été affichés");
		
		// Log l'état final
		var finalState = GetSceneState();
		GD.Print($"?? État final des crédits: {System.Text.Json.JsonSerializer.Serialize(finalState)}");
		
		// Retourner au menu principal ou fermer le jeu
		// Exemple: Retour au menu après 1 seconde
		GetTree().CreateTimer(1.0f).Timeout += () =>
		{
			GD.Print("?? Retour au menu principal...");
			GetTree().ChangeSceneToFile("res://Scenes/MainGameScene.tscn");
		};
	}
	
	/// <summary>
	/// Gestion des inputs pour sauter les crédits
	/// </summary>
	public override void _Input(InputEvent @event)
	{
		// Appuyer sur Espace ou Entrée pour passer au splash screen suivant
		if (@event is InputEventKey keyEvent && keyEvent.Pressed)
		{
			if (keyEvent.Keycode == Key.Space || keyEvent.Keycode == Key.Enter)
			{
				GD.Print("?? Skip vers le splash screen suivant");
				_splashScreenManager.Skip();
				_totalSkips++;
			}
			// Appuyer sur Echap pour tout sauter
			else if (keyEvent.Keycode == Key.Escape)
			{
				GD.Print("???? Skip de tous les crédits");
				_splashScreenManager.SkipAll();
				_totalSkips += _splashScreenManager.GetSplashScreenCount() - _splashScreenManager.GetCurrentIndex();
			}
		}
		
		// Clic de souris pour passer au suivant
		if (@event is InputEventMouseButton mouseEvent && mouseEvent.Pressed)
		{
			GD.Print("??? Clic souris: Skip vers le splash screen suivant");
			_splashScreenManager.Skip();
			_totalSkips++;
		}
	}
	
	public override void _ExitTree()
	{
		// Se désabonner des événements
		if (_splashScreenManager != null)
		{
			_splashScreenManager.SplashScreenCompleted -= OnSplashScreenCompleted;
			_splashScreenManager.AllSplashScreensCompleted -= OnAllSplashScreensCompleted;
		}
		
		GD.Print("?? Credits: Nettoyage terminé");
	}
}
