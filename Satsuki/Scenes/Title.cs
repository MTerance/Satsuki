using Godot;
using Satsuki.Interfaces;
using System;

namespace Satsuki.Scenes
{
	public partial class Title : Node, IScene
	{
		private DateTime _sceneStartTime;
		private int _menuItemIndex = 0;
		private Button[] _menuButtons;
		private Label _titleLabel;
		private bool _isAnimating = false;
		private float _titleAnimationTime = 0.0f;
		private readonly string[] _menuItems = { "Start Game", "Options", "Credits", "Quit" };

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
			
			GD.Print($"Menu initialise avec {_menuButtons.Length} options");
		}

		private void CreateUI()
		{
			var canvasLayer = new CanvasLayer();
			AddChild(canvasLayer);

			_titleLabel = new Label
			{
				Text = "SATSUKI",
				HorizontalAlignment = HorizontalAlignment.Center,
				VerticalAlignment = VerticalAlignment.Top
			};
			_titleLabel.AddThemeFontSizeOverride("font_size", 72);
			_titleLabel.AddThemeColorOverride("font_color", new Color(1.0f, 0.5f, 0.0f));
			canvasLayer.AddChild(_titleLabel);
			_titleLabel.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.TopWide);
			_titleLabel.OffsetTop = 100;
			_titleLabel.OffsetBottom = 200;

			var menuContainer = new VBoxContainer
			{
				Alignment = BoxContainer.AlignmentMode.Center
			};
			canvasLayer.AddChild(menuContainer);
			menuContainer.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.Center);
			menuContainer.GrowHorizontal = Control.GrowDirection.Both;
			menuContainer.GrowVertical = Control.GrowDirection.Both;

			_menuButtons = new Button[_menuItems.Length];
			for (int i = 0; i < _menuItems.Length; i++)
			{
				var button = new Button
				{
					Text = _menuItems[i],
					CustomMinimumSize = new Vector2(300, 60)
				};
				button.AddThemeFontSizeOverride("font_size", 24);
				
				int index = i;
				button.Pressed += () => OnMenuItemSelected(index);
				button.MouseEntered += () => OnMenuItemHover(index);
				
				menuContainer.AddChild(button);
				_menuButtons[i] = button;
			}

			UpdateMenuSelection();
			GD.Print("UI creee avec succes");
		}

		private void UpdateMenuSelection()
		{
			for (int i = 0; i < _menuButtons.Length; i++)
			{
				if (i == _menuItemIndex)
				{
					_menuButtons[i].GrabFocus();
					_menuButtons[i].AddThemeColorOverride("font_color", Colors.Orange);
				}
				else
				{
					_menuButtons[i].AddThemeColorOverride("font_color", Colors.White);
				}
			}
		}

		private void OnMenuItemHover(int index)
		{
			_menuItemIndex = index;
			UpdateMenuSelection();
			GD.Print($"Menu hover: {_menuButtons[index].Text}");
		}

		private void OnMenuItemSelected(int index)
		{
			_menuItemIndex = index;
			UpdateMenuSelection();
			GD.Print($"Menu selectionne: {_menuButtons[index].Text}");
			
			switch (_menuButtons[index].Text)
			{
				case "Start Game":
					StartGame();
					break;
				case "Options":
					OpenOptions();
					break;
				case "Credits":
					OpenCredits();
					break;
				case "Quit":
					QuitGame();
					break;
			}
		}

		private void StartGame()
		{
			GD.Print("Title: Demande de demarrage du jeu...");
			var finalState = GetSceneState();
			GD.Print($"Etat de la scene titre: {System.Text.Json.JsonSerializer.Serialize(finalState)}");
			
			EmitSignal(SignalName.StartGameRequested);
			GD.Print("Title: Signal StartGameRequested emis");
		}

		private void OpenOptions()
		{
			GD.Print("Title: Demande d'ouverture des options...");
			EmitSignal(SignalName.OptionsRequested);
		}

		private void OpenCredits()
		{
			GD.Print("Title: Demande d'ouverture des credits...");
			EmitSignal(SignalName.CreditsRequested);
		}

		private void QuitGame()
		{
			GD.Print("Fermeture du jeu...");
			var finalState = GetSceneState();
			GD.Print($"Etat final de la scene titre: {System.Text.Json.JsonSerializer.Serialize(finalState)}");
			GetTree().Quit();
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
				switch (keyEvent.Keycode)
				{
					case Key.Up:
						_menuItemIndex = (_menuItemIndex - 1 + _menuButtons.Length) % _menuButtons.Length;
						UpdateMenuSelection();
						break;
					case Key.Down:
						_menuItemIndex = (_menuItemIndex + 1) % _menuButtons.Length;
						UpdateMenuSelection();
						break;
					case Key.Enter:
					case Key.Space:
						OnMenuItemSelected(_menuItemIndex);
						break;
					case Key.Escape:
						QuitGame();
						break;
				}
			}
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
					SceneType = "MainMenu",
					StartTime = _sceneStartTime,
					ElapsedTime = Math.Round(elapsedTime, 2),
					ElapsedTimeFormatted = FormatElapsedTime(elapsedTime)
				},
				Menu = new
				{
					SelectedIndex = _menuItemIndex
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
