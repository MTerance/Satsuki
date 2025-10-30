using Godot;
using Satsuki.Interfaces;
using System;

namespace Satsuki.Scenes
{
	/// <summary>
	/// Scene d'ecran titre du jeu
	/// </summary>
	public partial class Title : Node, IScene
	{
		private DateTime _sceneStartTime;
		private string _selectedMenuItem = "Start Game";
		private int _menuItemIndex = 0;
		private readonly string[] _menuItems = { "Start Game", "Options", "Credits", "Quit" };
		private bool _isAnimating = false;
		private float _titleAnimationTime = 0.0f;
		
		public override void _Ready()
		{
			_sceneStartTime = DateTime.UtcNow;
			
			GD.Print("Title: Initialisation de l'ecran titre...");
			
			// Initialiser l'interface utilisateur
			InitializeUI();
			
			GD.Print($"Menu initialise avec {_menuItems.Length} options");
		}
		
		/// <summary>
		/// Retourne l'etat actuel de la scene Title
		/// </summary>
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
					Items = _menuItems,
					TotalItems = _menuItems.Length,
					SelectedItem = _selectedMenuItem,
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
		
		/// <summary>
		/// Initialise l'interface utilisateur du titre
		/// </summary>
		private void InitializeUI()
		{
			// Creer le titre principal
			var titleLabel = new Label
			{
				Text = "SATSUKI",
				HorizontalAlignment = HorizontalAlignment.Center,
				VerticalAlignment = VerticalAlignment.Top,
				Position = new Vector2(0, 100)
			};
			titleLabel.AddThemeFontSizeOverride("font_size", 72);
			titleLabel.AddThemeColorOverride("font_color", new Color(1.0f, 0.5f, 0.0f));
			AddChild(titleLabel);
			
			// Creer le menu
			var menuContainer = new VBoxContainer
			{
				Position = new Vector2(400, 300),
				CustomMinimumSize = new Vector2(400, 0)
			};
			
			for (int i = 0; i < _menuItems.Length; i++)
			{
				var button = new Button
				{
					Text = _menuItems[i],
					CustomMinimumSize = new Vector2(400, 50)
				};
				
				// Capturer l'index local
				int index = i;
				button.Pressed += () => OnMenuItemSelected(index);
				button.MouseEntered += () => OnMenuItemHover(index);
				
				menuContainer.AddChild(button);
			}
			
			AddChild(menuContainer);
			
			GD.Print("UI initialisee");
		}
		
		/// <summary>
		/// Callback quand un element du menu est survole
		/// </summary>
		private void OnMenuItemHover(int index)
		{
			_menuItemIndex = index;
			_selectedMenuItem = _menuItems[index];
			GD.Print($"Menu hover: {_selectedMenuItem}");
		}
		
		/// <summary>
		/// Callback quand un element du menu est selectionne
		/// </summary>
		private void OnMenuItemSelected(int index)
		{
			_menuItemIndex = index;
			_selectedMenuItem = _menuItems[index];
			
			GD.Print($"Menu selectionne: {_selectedMenuItem}");
			
			switch (_selectedMenuItem)
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
		
		/// <summary>
		/// Demarre le jeu
		/// </summary>
		private void StartGame()
		{
			GD.Print("Demarrage du jeu...");
			
			// Log l'etat avant de quitter
			var finalState = GetSceneState();
			GD.Print($"Etat de la scene titre: {System.Text.Json.JsonSerializer.Serialize(finalState)}");
			
			// Charger la scene de jeu
			GetTree().ChangeSceneToFile("res://Scenes/MainGameScene.tscn");
		}
		
		/// <summary>
		/// Ouvre les options
		/// </summary>
		private void OpenOptions()
		{
			GD.Print("Ouverture des options...");
			// TODO: Implementer la scene d'options
			// GetTree().ChangeSceneToFile("res://Scenes/Options.tscn");
		}
		
		/// <summary>
		/// Ouvre les credit
		/// </summary>
		private void OpenCredits()
		{
			GD.Print("Ouverture des credits...");
			GetTree().ChangeSceneToFile("res://Scenes/Credits.tscn");
		}
		
		/// <summary>
		/// Quitte le jeu
		/// </summary>
		private void QuitGame()
		{
			GD.Print("Fermeture du jeu...");
			
			// Log l'etat final
			var finalState = GetSceneState();
			GD.Print($"Etat final de la scene titre: {System.Text.Json.JsonSerializer.Serialize(finalState)}");
			
			GetTree().Quit();
		}
		
		/// <summary>
		/// Formate le temps ecoule en format lisible
		/// </summary>
		private string FormatElapsedTime(double seconds)
		{
			int minutes = (int)(seconds / 60);
			int secs = (int)(seconds % 60);
			return $"{minutes:D2}:{secs:D2}";
		}
		
		/// <summary>
		/// Gestion des inputs clavier pour la navigation
		/// </summary>
		public override void _Input(InputEvent @event)
		{
			if (@event is InputEventKey keyEvent && keyEvent.Pressed)
			{
				switch (keyEvent.Keycode)
				{
					case Key.Up:
						// Naviguer vers le haut
						_menuItemIndex = (_menuItemIndex - 1 + _menuItems.Length) % _menuItems.Length;
						_selectedMenuItem = _menuItems[_menuItemIndex];
						GD.Print($"Menu: {_selectedMenuItem}");
						break;
						
					case Key.Down:
						// Naviguer vers le bas
						_menuItemIndex = (_menuItemIndex + 1) % _menuItems.Length;
						_selectedMenuItem = _menuItems[_menuItemIndex];
						GD.Print($"Menu: {_selectedMenuItem}");
						break;
						
					case Key.Enter:
					case Key.Space:
						// Selectionner l'element actuel
						OnMenuItemSelected(_menuItemIndex);
						break;
						
					case Key.Escape:
						// Quitter directement
						QuitGame();
						break;
				}
			}
		}
		
		/// <summary>
		/// Animation du titre
		/// </summary>
		public override void _Process(double delta)
		{
			_titleAnimationTime += (float)delta;
			
			// Animation de pulsation du titre toutes les 2 secondes
			if (!_isAnimating && _titleAnimationTime >= 2.0f)
			{
				_isAnimating = true;
				AnimateTitle();
			}
		}
		
		/// <summary>
		/// Anime le titre
		/// </summary>
		private async void AnimateTitle()
		{
			// Animation simple de pulsation
			await System.Threading.Tasks.Task.Delay(500);
			
			_isAnimating = false;
			_titleAnimationTime = 0.0f;
		}
		
		public override void _ExitTree()
		{
			GD.Print("Title: Nettoyage de la scene titre");
		}
	}
}
