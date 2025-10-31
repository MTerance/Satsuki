using Godot;
using Satsuki.Manager;

public partial class Credits : Node
{
	private SplashScreenManager _splashScreenManager;
	
	public override void _Ready()
	{
		GD.Print("?? Credits: Initialisation...");
		
		// Cr�er et ajouter le SplashScreenManager
		_splashScreenManager = new SplashScreenManager();
		AddChild(_splashScreenManager);
		
		// S'abonner aux �v�nements
		_splashScreenManager.SplashScreenCompleted += OnSplashScreenCompleted;
		_splashScreenManager.AllSplashScreensCompleted += OnAllSplashScreensCompleted;
		
		// Configurer les splash screens
		SetupSplashScreens();
		
		// D�marrer la s�quence
		_splashScreenManager.StartSequence();
	}
	
	/// <summary>
	/// Configure les splash screens des cr�dits
	/// </summary>
	private void SetupSplashScreens()
	{
		// Splash screen 1: Titre du jeu
		_splashScreenManager.AddTextSplash("SATSUKI", 2.5f, new Color(1.0f, 0.5f, 0.0f));
		
		// Splash screen 2: D�velopp� par
		_splashScreenManager.AddTextSplash("D�velopp� par\nMTerance", 2.0f, Colors.Cyan);
		
		// Splash screen 3: Remerciements
		_splashScreenManager.AddTextSplash("Merci d'avoir jou�!", 2.0f, Colors.LightGreen);
		
		// Option: Ajouter des images si disponibles
		// _splashScreenManager.AddImageSplash("res://Assets/logo.png", 3.0f);
		
		GD.Print($"?? {_splashScreenManager.GetSplashScreenCount()} splash screens configur�s");
	}
	
	/// <summary>
	/// Callback quand un splash screen est termin�
	/// </summary>
	private void OnSplashScreenCompleted()
	{
		int current = _splashScreenManager.GetCurrentIndex();
		int total = _splashScreenManager.GetSplashScreenCount();
		GD.Print($"? Splash screen {current}/{total} termin�");
	}
	
	/// <summary>
	/// Callback quand tous les splash screens sont termin�s
	/// </summary>
	private void OnAllSplashScreensCompleted()
	{
		GD.Print("?? Tous les cr�dits ont �t� affich�s");
		
		// Retourner au menu principal ou fermer le jeu
		// Exemple: Retour au menu apr�s 1 seconde
		GetTree().CreateTimer(1.0f).Timeout += () =>
		{
			GD.Print("?? Retour au menu principal...");
			GetTree().ChangeSceneToFile("res://Scenes/MainGameScene.tscn");
		};
	}
	
	/// <summary>
	/// Gestion des inputs pour sauter les cr�dits
	/// </summary>
	public override void _Input(InputEvent @event)
	{
		// Appuyer sur Espace ou Entr�e pour passer au splash screen suivant
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
				GD.Print("???? Skip de tous les cr�dits");
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
		// Se d�sabonner des �v�nements
		if (_splashScreenManager != null)
		{
			_splashScreenManager.SplashScreenCompleted -= OnSplashScreenCompleted;
			_splashScreenManager.AllSplashScreensCompleted -= OnAllSplashScreensCompleted;
		}
		
		GD.Print("?? Credits: Nettoyage termin�");
	}
}
