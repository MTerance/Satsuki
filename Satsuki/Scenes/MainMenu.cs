using Godot;
using Satsuki.Interfaces;
using System;

namespace Satsuki.Scenes
{
	public partial class MainMenu : Node, IScene
	{
		private DateTime _sceneStartTime;

		#region Signals
		[Signal]
		public delegate void GoToLobbyRequestedEventHandler();

		[Signal]
		public delegate void MiniGamesRequestedEventHandler();

		[Signal]
		public delegate void BackToTitleRequestedEventHandler();
		#endregion

		public override void _Ready()
		{
			_sceneStartTime = DateTime.UtcNow;
			GD.Print("MainMenu: Initialisation du menu principal...");
			GD.Print("MainMenu: Menu initialise");
		}

		private string FormatElapsedTime(double seconds)
		{
			int minutes = (int)(seconds / 60);
			int secs = (int)(seconds % 60);
			return $"{minutes:D2}:{secs:D2}";
		}

		public override void _Process(double delta)
		{
		}

		public override void _ExitTree()
		{
			GD.Print("MainMenu: Nettoyage de la scene menu principal");
		}

		public object GetSceneState()
		{
			var elapsedTime = (DateTime.UtcNow - _sceneStartTime).TotalSeconds;

			return new
			{
				SceneInfo = new
				{
					SceneName = "MainMenu",
					SceneType = "MenuSelection",
					StartTime = _sceneStartTime,
					ElapsedTime = Math.Round(elapsedTime, 2),
					ElapsedTimeFormatted = FormatElapsedTime(elapsedTime)
				},
				Status = new
				{
					IsReady = true,
					Timestamp = DateTime.UtcNow
				}
			};
		}
	}
}
