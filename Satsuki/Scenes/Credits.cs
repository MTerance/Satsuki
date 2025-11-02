using Godot;
using Satsuki.Manager;
using Satsuki.Interfaces;
using System;

public partial class Credits : Node, IScene
{
	private SplashScreenManager _splashScreenManager;
	private DateTime _sceneStartTime;
	
	#region Signals
	[Signal]
	public delegate void CreditsCompletedEventHandler();
	
	[Signal]
	public delegate void LoadTitleSceneRequestedEventHandler();
	#endregion
	
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
		_splashScreenManager.SplashScreenSkipped += OnSplashScreenSkipped;
		_splashScreenManager.SequenceStarted += OnSequenceStarted;
		
		// Configurer les splash screens (le SplashScreenManager s'occupe de tout)
		_splashScreenManager.SetupDefaultCredits();
		
		// Démarrer la séquence
		_splashScreenManager.StartSequence();
		
		GD.Print("? Credits: SplashScreenManager configuré et démarré");
	}
	
	/// <summary>
	/// Retourne l'état actuel de la scène Credits
	/// Le SplashScreenManager gère maintenant tous les détails
	/// </summary>
	public object GetSceneState()
	{
		var elapsedTime = (DateTime.UtcNow - _sceneStartTime).TotalSeconds;
		var splashState = _splashScreenManager?.GetSplashScreenState();
		
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
			SplashScreenManager = splashState,
			Status = new
			{
				IsCompleted = _splashScreenManager?.GetCurrentIndex() >= _splashScreenManager?.GetSplashScreenCount(),
				IsActive = _splashScreenManager?.IsSequenceActive() ?? false,
				ManagerLoaded = _splashScreenManager != null,
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
	/// Callback quand un splash screen est terminé
	/// </summary>
	private void OnSplashScreenCompleted()
	{
		int current = _splashScreenManager.GetCurrentIndex();
		int total = _splashScreenManager.GetSplashScreenCount();
		GD.Print($"? Splash screen {current}/{total} terminé");
	}
	
	/// <summary>
	/// Callback quand un splash screen est sauté
	/// </summary>
	private void OnSplashScreenSkipped(int screenIndex)
	{
		GD.Print($"?? Splash screen {screenIndex + 1} sauté (Total skips: {_splashScreenManager.GetTotalSkips()})");
	}
	
	/// <summary>
	/// Callback quand la séquence démarre
	/// </summary>
	private void OnSequenceStarted(int totalScreens)
	{
		GD.Print($"?? Séquence de crédits démarrée: {totalScreens} écrans");
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
		
		// Émettre le signal de completion des crédits
		EmitSignal(SignalName.CreditsCompleted);
		
		// Utiliser le SceneNavigationManager pour charger la scène Title
		GetTree().CreateTimer(1.0f).Timeout += () =>
		{
			GD.Print("?? Credits: Demande de chargement de la scène Title via SceneNavigationManager...");
			
			// Utiliser le singleton SceneNavigationManager
			var navigationManager = GetNode<Satsuki.Manager.SceneNavigationManager>("/root/SceneNavigationManager");
			if (navigationManager != null)
			{
				navigationManager.NotifyCreditsCompleted();
			}
			else
			{
				// Fallback: chargement direct
				GD.Print("?? SceneNavigationManager non trouvé, chargement direct");
				EmitSignal(SignalName.LoadTitleSceneRequested);
				GetTree().ChangeSceneToFile("res://Scenes/Title.tscn");
			}
		};
	}
	
	/// <summary>
	/// Méthode publique pour terminer manuellement les crédits
	/// </summary>
	public void CompleteCredits()
	{
		GD.Print("?? Credits: Completion manuelle demandée");
		
		// Arrêter la séquence en cours
		_splashScreenManager?.SkipAll();
		
		// Émettre les signaux
		EmitSignal(SignalName.CreditsCompleted);
		EmitSignal(SignalName.LoadTitleSceneRequested);
	}
	
	/// <summary>
	/// Gestion des inputs - délégué au SplashScreenManager
	/// </summary>
	public override void _Input(InputEvent @event)
	{
		// Le SplashScreenManager gère maintenant tous les inputs
		_splashScreenManager?.HandleInput(@event);
	}
	
	/// <summary>
	/// API publique pour contrôler les crédits
	/// </summary>
	
	/// <summary>
	/// Passe au crédit suivant
	/// </summary>
	public void SkipToNext()
	{
		_splashScreenManager?.Skip();
	}
	
	/// <summary>
	/// Ignore tous les crédits
	/// </summary>
	public void SkipAll()
	{
		_splashScreenManager?.SkipAll();
	}
	
	/// <summary>
	/// Configure la vitesse des transitions
	/// </summary>
	public void SetFadeSpeed(float speed)
	{
		_splashScreenManager?.SetFadeSpeed(speed);
	}
	
	/// <summary>
	/// Redémarre la séquence de crédits
	/// </summary>
	public void RestartCredits()
	{
		if (_splashScreenManager != null)
		{
			_splashScreenManager.SetupDefaultCredits();
			_splashScreenManager.StartSequence();
			GD.Print("?? Crédits redémarrés");
		}
	}
	
	/// <summary>
	/// Configure des crédits personnalisés
	/// </summary>
	public void SetupCustomCredits()
	{
		if (_splashScreenManager == null) return;
		
		_splashScreenManager.Clear();
		
		// Exemple de crédits personnalisés
		_splashScreenManager.AddTextSplash("SATSUKI", 2.5f, new Color(1.0f, 0.5f, 0.0f), 72);
		_splashScreenManager.AddTextSplash("Un jeu développé avec passion", 2.0f, Colors.Cyan, 36);
		_splashScreenManager.AddTextSplash("Développé par\nMTerance", 2.0f, Colors.LightBlue, 42);
		_splashScreenManager.AddTextSplash("Merci d'avoir joué!", 2.0f, Colors.LightGreen, 48);
		_splashScreenManager.AddTextSplash("Version 1.0", 1.5f, Colors.Gray, 24);
		
		GD.Print("?? Crédits personnalisés configurés");
	}
	
	public override void _ExitTree()
	{
		// Se désabonner des événements
		if (_splashScreenManager != null)
		{
			_splashScreenManager.SplashScreenCompleted -= OnSplashScreenCompleted;
			_splashScreenManager.AllSplashScreensCompleted -= OnAllSplashScreensCompleted;
			_splashScreenManager.SplashScreenSkipped -= OnSplashScreenSkipped;
			_splashScreenManager.SequenceStarted -= OnSequenceStarted;
		}
		
		GD.Print("?? Credits: Nettoyage terminé");
	}
}
