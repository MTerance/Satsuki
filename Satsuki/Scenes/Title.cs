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

		public override void _Ready()
		{
			_sceneStartTime = DateTime.UtcNow;
			GD.Print("Title: Initialisation de l'ecran titre...");

			_titleLabel = GetNode<Label>("TitleLabel");
			var menuContainer = GetNode<VBoxContainer>("MenuContainer");
			_menuButtons = new Button[menuContainer.GetChildCount()];
			
			for (int i = 0; i < menuContainer.GetChildCount(); i++)
			{
				_menuButtons[i] = menuContainer.GetChild<Button>(i);
				int index = i;
				_menuButtons[i].Pressed += () => OnMenuItemSelected(index);
				_menuButtons[i].MouseEntered += () => OnMenuItemHover(index);
			}
			
			UpdateMenuSelection();
			GD.Print($"Menu initialise avec {_menuButtons.Length} options");
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
			GD.Print("Demarrage du jeu...");
			var finalState = GetSceneState();
			GD.Print($"Etat de la scene titre: {System.Text.Json.JsonSerializer.Serialize(finalState)}");
			
			if (ResourceLoader.Exists("res://Scenes/MainGameScene.tscn"))
				GetTree().ChangeSceneToFile("res://Scenes/MainGameScene.tscn");
			else
				GD.PrintErr("Scene MainGameScene introuvable");
		}

		private void OpenOptions()
		{
			GD.Print("Ouverture des options...");
		}

		private void OpenCredits()
		{
			GD.Print("Ouverture des credits...");
			
			if (ResourceLoader.Exists("res://Scenes/Credits.tscn"))
				GetTree().ChangeSceneToFile("res://Scenes/Credits.tscn");
			else
				GD.PrintErr("Scene Credits introuvable");
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
