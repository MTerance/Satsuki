using Godot;
using Satsuki.Manager;

public partial class Credits : Node
{
	private SplashScreenManager _splashScreenManager;
	
	public override void _Ready()
	{
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
			}
			// Appuyer sur Echap pour tout sauter
			else if (keyEvent.Keycode == Key.Escape)
			{
				GD.Print("???? Skip de tous les crédits");
				_splashScreenManager.SkipAll();
			}
		}
		
		// Clic de souris pour passer au suivant
		if (@event is InputEventMouseButton mouseEvent && mouseEvent.Pressed)
		{
			GD.Print("??? Clic souris: Skip vers le splash screen suivant");
			_splashScreenManager.Skip();
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
