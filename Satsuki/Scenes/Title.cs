using Godot;
using Satsuki.Interfaces;
using Satsuki.Interfaces.Models;
using System;

namespace Satsuki.Scenes
{
	public partial class Title : Node, IScene
	{
		private DateTime _sceneStartTime;
		private TextureRect _logoRect;

		#region Signals
		[Signal]
		public delegate void StartGameRequestedEventHandler();
		#endregion

		public override void _Ready()
		{
			_sceneStartTime = DateTime.UtcNow;
			GD.Print("Title: Initialisation de l'ecran titre...");
			CreateUI();
			GD.Print("Title: Ecran titre initialise");
		}

		private void CreateUI()
		{
			var canvasLayer = new CanvasLayer();
			AddChild(canvasLayer);

			var logoTexture = GD.Load<Texture2D>("res://Assets/Img/overlay_logo_small_placeholder.png");
			if (logoTexture != null)
			{
				_logoRect = new TextureRect
				{
					Texture = logoTexture,
					ExpandMode = TextureRect.ExpandModeEnum.KeepSize,
					StretchMode = TextureRect.StretchModeEnum.KeepAspectCentered
				};
				canvasLayer.AddChild(_logoRect);
				_logoRect.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.Center);
			}
			else
			{
				GD.PrintErr("Title: Logo introuvable a res://Assets/Img/overlay_logo_small_placeholder.png");
			}

			GD.Print("Title: UI creee avec succes");
		}

		private string FormatElapsedTime(double seconds)
		{
			int minutes = (int)(seconds / 60);
			int secs = (int)(seconds % 60);
			return $"{minutes:D2}:{secs:D2}";
		}

		public override void _Input(InputEvent @event)
		{
			if (@event is InputEventKey keyEvent && keyEvent.Pressed)
			{
				if (keyEvent.Keycode == Key.Escape)
					QuitGame();
				else
					StartGame();
			}
			else if (@event is InputEventMouseButton mouseEvent && mouseEvent.Pressed)
			{
				StartGame();
			}
		}

        private void StartGame()
		{
			GD.Print("Title: Demande de demarrage du jeu...");
			EmitSignal(SignalName.StartGameRequested);
			GD.Print("Title: Signal StartGameRequested emis");
		}

		private void QuitGame()
		{
			GD.Print("Title: Fermeture du jeu...");
			GetTree().Quit();
		}

		public override void _Process(double delta)
		{
		}

		public override void _ExitTree()
		{
			GD.Print("Title: Nettoyage de la scene titre");
		}

		public object GetSceneState()
		{
			var elapsedTime = (DateTime.UtcNow - _sceneStartTime).TotalSeconds;

			return new
			{
				SceneInfo = new
				{
					SceneName = "Title",
					SceneType = "TitleScreen",
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
