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
		
		GD.Print("Credits: Initialisation...");
		
		_splashScreenManager = new SplashScreenManager();
		AddChild(_splashScreenManager);
		
		_splashScreenManager.SplashScreenCompleted += OnSplashScreenCompleted;
		_splashScreenManager.AllSplashScreensCompleted += OnAllSplashScreensCompleted;
		_splashScreenManager.SplashScreenSkipped += OnSplashScreenSkipped;
		_splashScreenManager.SequenceStarted += OnSequenceStarted;
		
		_splashScreenManager.SetupCustomCredits();
		_splashScreenManager.StartSequence();
		
		GD.Print("Credits: SplashScreenManager configure et demarre");
	}
	
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
	
	private string FormatElapsedTime(double seconds)
	{
		int minutes = (int)(seconds / 60);
		int secs = (int)(seconds % 60);
		return $"{minutes:D2}:{secs:D2}";
	}
	
	private void OnSplashScreenCompleted()
	{
		int current = _splashScreenManager.GetCurrentIndex();
		int total = _splashScreenManager.GetSplashScreenCount();
		GD.Print($"Splash screen {current}/{total} termine");
	}
	
	private void OnSplashScreenSkipped(int screenIndex)
	{
		GD.Print($"Splash screen {screenIndex + 1} saute (Total skips: {_splashScreenManager.GetTotalSkips()})");
	}
	
	private void OnSequenceStarted(int totalScreens)
	{
		GD.Print($"Sequence de credits demarree: {totalScreens} ecrans");
	}
	
	private void OnAllSplashScreensCompleted()
	{
		GD.Print("Tous les credits ont ete affiches");
		
		var finalState = GetSceneState();
		GD.Print($"Etat final des credits: {System.Text.Json.JsonSerializer.Serialize(finalState)}");
		
		EmitSignal(SignalName.CreditsCompleted);
		
		GetTree().CreateTimer(1.0f).Timeout += () =>
		{
			GD.Print("Credits: Demande de chargement de la scene Title via SceneNavigationManager...");
			
			var navigationManager = GetNode<Satsuki.Manager.SceneNavigationManager>("/root/SceneNavigationManager");
			if (navigationManager != null)
			{
				navigationManager.NotifyCreditsCompleted();
			}
			else
			{
				GD.Print("SceneNavigationManager non trouve, chargement direct");
				EmitSignal(SignalName.LoadTitleSceneRequested);
				GetTree().ChangeSceneToFile("res://Scenes/Title.tscn");
			}
		};
	}
	
	public void CompleteCredits()
	{
		GD.Print("Credits: Completion manuelle demandee");
		
		_splashScreenManager?.SkipAll();
		
		EmitSignal(SignalName.CreditsCompleted);
		EmitSignal(SignalName.LoadTitleSceneRequested);
	}
	
	public override void _Input(InputEvent @event)
	{
		_splashScreenManager?.HandleInput(@event);
	}
	
	public void SkipToNext()
	{
		_splashScreenManager?.Skip();
	}
	
	public void SkipAll()
	{
		_splashScreenManager?.SkipAll();
	}
	
	public void SetFadeSpeed(float speed)
	{
		_splashScreenManager?.SetFadeSpeed(speed);
	}
	
	public void RestartCredits()
	{
		if (_splashScreenManager != null)
		{
			_splashScreenManager.SetupCustomCredits();
			_splashScreenManager.StartSequence();
			GD.Print("Credits redemarres");
		}
	}
	
	public override void _ExitTree()
	{
		if (_splashScreenManager != null)
		{
			_splashScreenManager.SplashScreenCompleted -= OnSplashScreenCompleted;
			_splashScreenManager.AllSplashScreensCompleted -= OnAllSplashScreensCompleted;
			_splashScreenManager.SplashScreenSkipped -= OnSplashScreenSkipped;
			_splashScreenManager.SequenceStarted -= OnSequenceStarted;
		}
		
		GD.Print("Credits: Nettoyage termine");
	}
}
