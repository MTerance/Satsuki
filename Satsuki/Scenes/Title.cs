using Godot;
using Satsuki.Interfaces;
using System;

namespace Satsuki.Scenes
{
	public partial class Title : Node, IScene
	{
		private DateTime _sceneStartTime;
		private Label _titleLabel;
		private bool _isAnimating = false;
		private float _titleAnimationTime = 0.0f;

		#region Signals
		[Signal]
		public delegate void StartGameRequestedEventHandler();
		
		[Signal]
		public delegate void OptionsRequestedEventHandler();
		
		[Signal]
		public delegate void CreditsRequestedEventHandler();
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

			// Titre uniquement
			_titleLabel = new Label
			{
				Text = "SATSUKI",
				HorizontalAlignment = HorizontalAlignment.Center,
				VerticalAlignment = VerticalAlignment.Center
			};
			_titleLabel.AddThemeFontSizeOverride("font_size", 96);
			_titleLabel.AddThemeColorOverride("font_color", new Color(1.0f, 0.5f, 0.0f));
			canvasLayer.AddChild(_titleLabel);
			_titleLabel.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.Center);

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
			// Appuyer sur n'importe quelle touche ou clic pour demarrer
			if (@event is InputEventKey keyEvent && keyEvent.Pressed)
			{
				if (keyEvent.Keycode == Key.Escape)
				{
					QuitGame();
				}
				else
				{
					StartGame();
				}
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
			_titleAnimationTime += (float)delta;
			
			if (!_isAnimating && _titleAnimationTime >= 2.0f)
			{
				_isAnimating = true;
				AnimateTitle();
			}
		}

		private async void AnimateTitle()
		{
			if (_titleLabel == null || !IsInstanceValid(_titleLabel))
				return;

			_titleLabel.AddThemeColorOverride("font_color", Colors.Yellow);
			await ToSignal(GetTree().CreateTimer(0.5), SceneTreeTimer.SignalName.Timeout);
			
			if (_titleLabel != null && IsInstanceValid(_titleLabel))
			{
				_titleLabel.AddThemeColorOverride("font_color", new Color(1.0f, 0.5f, 0.0f));
			}
			
			_isAnimating = false;
			_titleAnimationTime = 0.0f;
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
				Animation = new
				{
					IsAnimating = _isAnimating,
					AnimationTime = Math.Round(_titleAnimationTime, 2)
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
