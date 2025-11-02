using Godot;
using System;

namespace Satsuki.Manager
{
	/// <summary>
	/// Gestionnaire global de navigation entre les scènes
	/// Singleton AutoLoad pour gérer les transitions entre Credits, Title, etc.
	/// </summary>
	public partial class SceneNavigationManager : Node
	{
		private static SceneNavigationManager _instance;
		
		public static SceneNavigationManager Instance => _instance;
		
		#region Signals
		[Signal]
		public delegate void SceneChangeRequestedEventHandler(string scenePath);
		
		[Signal] 
		public delegate void CreditsCompletedEventHandler();
		
		[Signal]
		public delegate void TitleSceneRequestedEventHandler();
		#endregion
		
		public override void _Ready()
		{
			_instance = this;
			GD.Print("?? SceneNavigationManager: Initialisé");
		}
		
		/// <summary>
		/// Demande le chargement de la scène Title
		/// </summary>
		public void RequestTitleScene()
		{
			GD.Print("?? SceneNavigationManager: Demande de chargement Title");
			EmitSignal(SignalName.TitleSceneRequested);
			LoadScene("res://Scenes/Title.tscn");
		}
		
		/// <summary>
		/// Notifie que les crédits sont terminés
		/// </summary>
		public void NotifyCreditsCompleted()
		{
			GD.Print("?? SceneNavigationManager: Crédits terminés");
			EmitSignal(SignalName.CreditsCompleted);
			
			// Automatiquement charger la scène Title après les crédits
			CallDeferred(nameof(RequestTitleScene));
		}
		
		/// <summary>
		/// Charge une scène spécifique
		/// </summary>
		public void LoadScene(string scenePath)
		{
			try
			{
				if (ResourceLoader.Exists(scenePath))
				{
					GD.Print($"?? SceneNavigationManager: Chargement de {scenePath}");
					EmitSignal(SignalName.SceneChangeRequested, scenePath);
					GetTree().ChangeSceneToFile(scenePath);
				}
				else
				{
					GD.PrintErr($"? SceneNavigationManager: Scène non trouvée: {scenePath}");
				}
			}
			catch (Exception ex)
			{
				GD.PrintErr($"? SceneNavigationManager: Erreur chargement {scenePath}: {ex.Message}");
			}
		}
		
		/// <summary>
		/// Charge la scène MainGameScene
		/// </summary>
		public void LoadMainGame()
		{
			LoadScene("res://Scenes/MainGameScene.tscn");
		}
		
		/// <summary>
		/// Charge la scène Credits
		/// </summary>
		public void LoadCredits()
		{
			LoadScene("res://Scenes/Credits.tscn");
		}
		
		/// <summary>
		/// Charge la scène Title
		/// </summary>
		public void LoadTitle()
		{
			LoadScene("res://Scenes/Title.tscn");
		}
		
		public override void _ExitTree()
		{
			GD.Print("?? SceneNavigationManager: Nettoyage");
		}
	}
}