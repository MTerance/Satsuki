using Godot;
using Satsuki.Interfaces;
using System;

namespace Satsuki.Scenes
{
	/// <summary>
	/// Menu principal du jeu apres selection "Start Game" depuis Title
	/// Permet de choisir entre differents modes de jeu
	/// </summary>
	public partial class MainMenu : Node, IScene
	{
		private DateTime _sceneStartTime;
		private int _menuItemIndex = 0;
		private Button[] _menuButtons;
		private Label _titleLabel;
		private bool _isAnimating = false;
		private float _titleAnimationTime = 0.0f;
		private readonly string[] _menuItems = { "Solo Play", "Multiplayer", "Mini-Games", "Back to Title" };

		#region Signals
		[Signal]
		public delegate void SoloPlayRequestedEventHandler();
		
		[Signal]
		public delegate void MultiplayerRequestedEventHandler();
		
		[Signal]
		public delegate void MiniGamesRequestedEventHandler();
		
		[Signal]
		public delegate void BackToTitleRequestedEventHandler();
		#endregion

		public override void _Ready()
		{
			_sceneStartTime = DateTime.UtcNow;
			GD.Print("MainMenu: Initialisation du menu principal...");

			CreateUI();
			
			GD.Print($"MainMenu: Menu initialise avec {_menuButtons.Length} options");
		}

		private void CreateUI()
		{
			var canvasLayer = new CanvasLayer();
			AddChild(canvasLayer);

			// Titre du menu principal
			_titleLabel = new Label
			{
				Text = "MAIN MENU",
				HorizontalAlignment = HorizontalAlignment.Center,
				VerticalAlignment = VerticalAlignment.Top
			};
			_titleLabel.AddThemeFontSizeOverride("font_size", 64);
			_titleLabel.AddThemeColorOverride("font_color", new Color(0.2f, 0.8f, 1.0f));
			canvasLayer.AddChild(_titleLabel);
			_titleLabel.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.TopWide);
			_titleLabel.OffsetTop = 80;
			_titleLabel.OffsetBottom = 180;

			// Container du menu
			var menuContainer = new VBoxContainer
			{
				Alignment = BoxContainer.AlignmentMode.Center
			};
			canvasLayer.AddChild(menuContainer);
			menuContainer.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.Center);
			menuContainer.GrowHorizontal = Control.GrowDirection.Both;
			menuContainer.GrowVertical = Control.GrowDirection.Both;

			// Creation des boutons
			_menuButtons = new Button[_menuItems.Length];
			for (int i = 0; i < _menuItems.Length; i++)
			{
				var button = new Button
				{
					Text = _menuItems[i],
					CustomMinimumSize = new Vector2(350, 70)
				};
				button.AddThemeFontSizeOverride("font_size", 26);
				
				int index = i;
				button.Pressed += () => OnMenuItemSelected(index);
				button.MouseEntered += () => OnMenuItemHover(index);
				
				menuContainer.AddChild(button);
				_menuButtons[i] = button;
			}

			UpdateMenuSelection();
			GD.Print("MainMenu: UI creee avec succes");
		}

		private void UpdateMenuSelection()
		{
			for (int i = 0; i < _menuButtons.Length; i++)
			{
				if (i == _menuItemIndex)
				{
					_menuButtons[i].GrabFocus();
					_menuButtons[i].AddThemeColorOverride("font_color", new Color(0.2f, 0.8f, 1.0f));
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
			GD.Print($"MainMenu hover: {_menuButtons[index].Text}");
		}

		private void OnMenuItemSelected(int index)
		{
			_menuItemIndex = index;
			UpdateMenuSelection();
			GD.Print($"MainMenu selectionne: {_menuButtons[index].Text}");
			
			switch (_menuButtons[index].Text)
			{
				case "Solo Play":
					StartSoloPlay();
					break;
				case "Multiplayer":
					StartMultiplayer();
					break;
				case "Mini-Games":
					OpenMiniGames();
					break;
				case "Back to Title":
					BackToTitle();
					break;
			}
		}

		private void StartSoloPlay()
		{
			GD.Print("MainMenu: Demande de demarrage Solo Play...");
			var finalState = GetSceneState();
			GD.Print($"MainMenu: Etat de la scene: {System.Text.Json.JsonSerializer.Serialize(finalState)}");
			
			EmitSignal(SignalName.SoloPlayRequested);
			GD.Print("MainMenu: Signal SoloPlayRequested emis");
		}

		private void StartMultiplayer()
		{
			GD.Print("MainMenu: Demande de demarrage Multiplayer...");
			EmitSignal(SignalName.MultiplayerRequested);
			GD.Print("MainMenu: Signal MultiplayerRequested emis");
		}

		private void OpenMiniGames()
		{
			GD.Print("MainMenu: Ouverture des Mini-Games...");
			EmitSignal(SignalName.MiniGamesRequested);
			GD.Print("MainMenu: Signal MiniGamesRequested emis");
		}

		private void BackToTitle()
		{
			GD.Print("MainMenu: Retour au menu titre...");
			var finalState = GetSceneState();
			GD.Print($"MainMenu: Etat final: {System.Text.Json.JsonSerializer.Serialize(finalState)}");
			
			EmitSignal(SignalName.BackToTitleRequested);
			GD.Print("MainMenu: Signal BackToTitleRequested emis");
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
						BackToTitle();
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

			_titleLabel.AddThemeColorOverride("font_color", Colors.Cyan);
			await ToSignal(GetTree().CreateTimer(0.5), SceneTreeTimer.SignalName.Timeout);
			
			if (_titleLabel != null && IsInstanceValid(_titleLabel))
			{
				_titleLabel.AddThemeColorOverride("font_color", new Color(0.2f, 0.8f, 1.0f));
			}
			
			_isAnimating = false;
			_titleAnimationTime = 0.0f;
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
					SceneType = "GameModeSelection",
					StartTime = _sceneStartTime,
					ElapsedTime = Math.Round(elapsedTime, 2),
					ElapsedTimeFormatted = FormatElapsedTime(elapsedTime)
				},
				Menu = new
				{
					SelectedIndex = _menuItemIndex,
					SelectedOption = _menuItems[_menuItemIndex]
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
