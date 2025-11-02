using Godot;
using System;
using System.Collections.Generic;

namespace Satsuki.Manager
{
	/// <summary>
	/// Gestionnaire de splash screens avec système de transition
	/// Gère complètement l'affichage des crédits et séquences d'images
	/// </summary>
	public partial class SplashScreenManager : Node
	{
		#region Private Fields
		private List<SplashScreenData> _splashScreens = new List<SplashScreenData>();
		private int _currentIndex = 0;
		private ColorRect _fadeOverlay;
		private TextureRect _imageDisplay;
		private Label _textDisplay;
		private Timer _displayTimer;
		private bool _isTransitioning = false;
		private float _fadeSpeed = 2.0f;
		
		// Statistiques et tracking
		private DateTime _sequenceStartTime;
		private int _totalSkips = 0;
		private bool _isSequenceActive = false;
		#endregion

		#region Signals
		[Signal]
		public delegate void SplashScreenCompletedEventHandler();

		[Signal]
		public delegate void AllSplashScreensCompletedEventHandler();
		
		[Signal]
		public delegate void SplashScreenSkippedEventHandler(int screenIndex);
		
		[Signal]
		public delegate void SequenceStartedEventHandler(int totalScreens);
		#endregion

		#region Initialization
		public override void _Ready()
		{
			// Créer l'overlay de fade
			_fadeOverlay = new ColorRect
			{
				Color = new Color(0, 0, 0, 0),
				MouseFilter = Control.MouseFilterEnum.Ignore,
				AnchorsPreset = (int)Control.LayoutPreset.FullRect
			};
			AddChild(_fadeOverlay);

			// Créer l'affichage d'image
			_imageDisplay = new TextureRect
			{
				ExpandMode = TextureRect.ExpandModeEnum.IgnoreSize,
				StretchMode = TextureRect.StretchModeEnum.KeepAspectCentered,
				Visible = false,
				AnchorsPreset = (int)Control.LayoutPreset.FullRect
			};
			AddChild(_imageDisplay);

			// Créer l'affichage de texte
			_textDisplay = new Label
			{
				HorizontalAlignment = HorizontalAlignment.Center,
				VerticalAlignment = VerticalAlignment.Center,
				Visible = false,
				AnchorsPreset = (int)Control.LayoutPreset.FullRect
			};
			_textDisplay.AddThemeColorOverride("font_color", Colors.White);
			_textDisplay.AddThemeFontSizeOverride("font_size", 48);
			AddChild(_textDisplay);

			// Timer pour la durée d'affichage
			_displayTimer = new Timer();
			_displayTimer.OneShot = true;
			_displayTimer.Timeout += OnDisplayTimerTimeout;
			AddChild(_displayTimer);

			GD.Print("?? SplashScreenManager initialisé");
		}
		#endregion

		#region Public API - Configuration
		/// <summary>
		/// Ajoute un splash screen texte
		/// </summary>
		public void AddTextSplash(string text, float duration = 3.0f, Color? textColor = null, int fontSize = 48)
		{
			var splash = new SplashScreenData
			{
				Type = SplashScreenType.Text,
				Text = text,
				Duration = duration,
				TextColor = textColor ?? Colors.White,
				FontSize = fontSize
			};
			_splashScreens.Add(splash);
			GD.Print($"?? Splash screen texte ajouté: {text} ({duration}s)");
		}

		/// <summary>
		/// Ajoute un splash screen image
		/// </summary>
		public void AddImageSplash(string imagePath, float duration = 3.0f)
		{
			var texture = GD.Load<Texture2D>(imagePath);
			if (texture == null)
			{
				GD.PrintErr($"? Impossible de charger l'image: {imagePath}");
				return;
			}

			var splash = new SplashScreenData
			{
				Type = SplashScreenType.Image,
				ImagePath = imagePath,
				Texture = texture,
				Duration = duration
			};
			_splashScreens.Add(splash);
			GD.Print($"??? Splash screen image ajouté: {imagePath} ({duration}s)");
		}

		/// <summary>
		/// Configure automatiquement les crédits par défaut
		/// </summary>
		public void SetupDefaultCredits()
		{
			Clear();
			
			// Splash screen 1: Titre du jeu
			AddTextSplash("SATSUKI", 2.5f, new Color(1.0f, 0.5f, 0.0f), 64);
			
			// Splash screen 2: Développé par
			AddTextSplash("Développé par\nMTerance", 2.0f, Colors.Cyan, 36);
			
			// Splash screen 3: Remerciements
			AddTextSplash("Merci d'avoir joué!", 2.0f, Colors.LightGreen, 42);
			
			// Option: Ajouter des images si disponibles
			TryAddImageIfExists("res://Assets/logo.png", 3.0f);
			TryAddImageIfExists("res://Assets/studio_logo.png", 2.5f);
			
			GD.Print($"?? {GetSplashScreenCount()} splash screens de crédits configurés");
		}

		/// <summary>
		/// Tente d'ajouter une image si elle existe
		/// </summary>
		private void TryAddImageIfExists(string imagePath, float duration)
		{
			if (ResourceLoader.Exists(imagePath))
			{
				AddImageSplash(imagePath, duration);
			}
		}

		/// <summary>
		/// Configure la vitesse de transition
		/// </summary>
		public void SetFadeSpeed(float speed)
		{
			_fadeSpeed = Mathf.Max(0.1f, speed);
		}

		/// <summary>
		/// Nettoie tous les splash screens
		/// </summary>
		public void Clear()
		{
			_splashScreens.Clear();
			_currentIndex = 0;
			_totalSkips = 0;
			_isSequenceActive = false;
			GD.Print("??? Splash screens effacés");
		}
		#endregion

		#region Public API - Contrôle de séquence
		/// <summary>
		/// Démarre la séquence de splash screens
		/// </summary>
		public void StartSequence()
		{
			if (_splashScreens.Count == 0)
			{
				GD.PrintErr("?? Aucun splash screen à afficher");
				EmitSignal(SignalName.AllSplashScreensCompleted);
				return;
			}

			_currentIndex = 0;
			_totalSkips = 0;
			_sequenceStartTime = DateTime.UtcNow;
			_isSequenceActive = true;
			
			GD.Print($"?? Démarrage de la séquence de {_splashScreens.Count} splash screens");
			EmitSignal(SignalName.SequenceStarted, _splashScreens.Count);
			
			ShowNextSplash();
		}

		/// <summary>
		/// Passe au splash screen suivant (skip)
		/// </summary>
		public void Skip()
		{
			if (_isTransitioning || !_isSequenceActive)
				return;

			_displayTimer.Stop();
			_totalSkips++;
			
			GD.Print($"?? Skip vers le splash screen suivant (Total skips: {_totalSkips})");
			EmitSignal(SignalName.SplashScreenSkipped, _currentIndex);
			
			FadeOut();
		}

		/// <summary>
		/// Passe directement à la fin de la séquence
		/// </summary>
		public void SkipAll()
		{
			if (!_isSequenceActive) return;

			int remainingScreens = _splashScreens.Count - _currentIndex;
			_totalSkips += remainingScreens;
			_currentIndex = _splashScreens.Count;
			_displayTimer.Stop();
			_textDisplay.Visible = false;
			_imageDisplay.Visible = false;
			_fadeOverlay.Color = new Color(0, 0, 0, 1);
			_isSequenceActive = false;

			GD.Print($"???? Toute la séquence a été sautée (Total skips: {_totalSkips})");
			EmitSignal(SignalName.AllSplashScreensCompleted);
		}

		/// <summary>
		/// Gère les inputs utilisateur pour la navigation
		/// </summary>
		public void HandleInput(InputEvent @event)
		{
			if (!_isSequenceActive) return;

			// Appuyer sur Espace ou Entrée pour passer au splash screen suivant
			if (@event is InputEventKey keyEvent && keyEvent.Pressed)
			{
				if (keyEvent.Keycode == Key.Space || keyEvent.Keycode == Key.Enter)
				{
					Skip();
				}
				// Appuyer sur Échap pour tout sauter
				else if (keyEvent.Keycode == Key.Escape)
				{
					SkipAll();
				}
			}
			
			// Clic de souris pour passer au suivant
			if (@event is InputEventMouseButton mouseEvent && mouseEvent.Pressed)
			{
				Skip();
			}
		}
		#endregion

		#region Public API - État et statistiques
		/// <summary>
		/// Obtient l'état complet du SplashScreenManager
		/// </summary>
		public object GetSplashScreenState()
		{
			var elapsedTime = _isSequenceActive ? (DateTime.UtcNow - _sequenceStartTime).TotalSeconds : 0;
			
			return new
			{
				Sequence = new
				{
					TotalScreens = GetSplashScreenCount(),
					CurrentIndex = GetCurrentIndex(),
					RemainingScreens = Math.Max(0, GetSplashScreenCount() - GetCurrentIndex()),
					Progress = GetSplashScreenCount() > 0 
						? Math.Round((float)GetCurrentIndex() / GetSplashScreenCount() * 100, 2) 
						: 0,
					IsActive = _isSequenceActive,
					IsTransitioning = _isTransitioning
				},
				Timing = new
				{
					StartTime = _sequenceStartTime,
					ElapsedTime = Math.Round(elapsedTime, 2),
					ElapsedTimeFormatted = FormatElapsedTime(elapsedTime)
				},
				UserInteraction = new
				{
					TotalSkips = _totalSkips,
					SkipRate = elapsedTime > 0 ? Math.Round(_totalSkips / elapsedTime * 60, 2) : 0 // Skips per minute
				},
				Status = new
				{
					IsCompleted = GetCurrentIndex() >= GetSplashScreenCount(),
					FadeSpeed = _fadeSpeed,
					Timestamp = DateTime.UtcNow
				},
				CurrentSplash = _currentIndex < _splashScreens.Count 
					? new {
						Index = _currentIndex,
						Type = _splashScreens[_currentIndex].Type.ToString(),
						Text = _splashScreens[_currentIndex].Text,
						Duration = _splashScreens[_currentIndex].Duration
					}
					: null
			};
		}

		/// <summary>
		/// Obtient le nombre total de splash screens
		/// </summary>
		public int GetSplashScreenCount()
		{
			return _splashScreens.Count;
		}

		/// <summary>
		/// Obtient l'index actuel
		/// </summary>
		public int GetCurrentIndex()
		{
			return _currentIndex;
		}

		/// <summary>
		/// Obtient le nombre total de skips
		/// </summary>
		public int GetTotalSkips()
		{
			return _totalSkips;
		}

		/// <summary>
		/// Vérifie si la séquence est active
		/// </summary>
		public bool IsSequenceActive()
		{
			return _isSequenceActive;
		}

		/// <summary>
		/// Formate le temps écoulé en format lisible
		/// </summary>
		private string FormatElapsedTime(double seconds)
		{
			int minutes = (int)(seconds / 60);
			int secs = (int)(seconds % 60);
			return $"{minutes:D2}:{secs:D2}";
		}
		#endregion

		#region Private - Logique d'affichage
		/// <summary>
		/// Affiche le splash screen suivant
		/// </summary>
		private void ShowNextSplash()
		{
			if (_currentIndex >= _splashScreens.Count)
			{
				_isSequenceActive = false;
				GD.Print("? Tous les splash screens terminés");
				
				// Log des statistiques finales
				var finalState = GetSplashScreenState();
				GD.Print($"?? État final: {System.Text.Json.JsonSerializer.Serialize(finalState)}");
				
				EmitSignal(SignalName.AllSplashScreensCompleted);
				return;
			}

			var splash = _splashScreens[_currentIndex];
			GD.Print($"?? Affichage du splash screen {_currentIndex + 1}/{_splashScreens.Count}: {splash.Text ?? splash.ImagePath}");

			_isTransitioning = true;

			// Fade in
			FadeIn(splash);
		}

		/// <summary>
		/// Transition fade in
		/// </summary>
		private async void FadeIn(SplashScreenData splash)
		{
			// Préparer le contenu
			if (splash.Type == SplashScreenType.Text)
			{
				_textDisplay.Text = splash.Text;
				_textDisplay.AddThemeColorOverride("font_color", splash.TextColor);
				_textDisplay.AddThemeFontSizeOverride("font_size", splash.FontSize);
				_textDisplay.Visible = true;
				_imageDisplay.Visible = false;
			}
			else if (splash.Type == SplashScreenType.Image)
			{
				_imageDisplay.Texture = splash.Texture;
				_imageDisplay.Visible = true;
				_textDisplay.Visible = false;
			}

			// Fade overlay de noir vers transparent
			var tween = CreateTween();
			tween.TweenProperty(_fadeOverlay, "color:a", 0.0f, 1.0f / _fadeSpeed);
			await ToSignal(tween, Tween.SignalName.Finished);

			_isTransitioning = false;

			// Démarrer le timer d'affichage
			_displayTimer.Start(splash.Duration);
		}

		/// <summary>
		/// Transition fade out
		/// </summary>
		private async void FadeOut()
		{
			_isTransitioning = true;

			// Fade overlay de transparent vers noir
			var tween = CreateTween();
			tween.TweenProperty(_fadeOverlay, "color:a", 1.0f, 1.0f / _fadeSpeed);
			await ToSignal(tween, Tween.SignalName.Finished);

			// Cacher tout le contenu
			_textDisplay.Visible = false;
			_imageDisplay.Visible = false;

			EmitSignal(SignalName.SplashScreenCompleted);

			_currentIndex++;
			ShowNextSplash();
		}

		/// <summary>
		/// Callback du timer d'affichage
		/// </summary>
		private void OnDisplayTimerTimeout()
		{
			if (!_isTransitioning && _isSequenceActive)
			{
				FadeOut();
			}
		}
		#endregion
	}

	/// <summary>
	/// Type de splash screen
	/// </summary>
	public enum SplashScreenType
	{
		Text,
		Image
	}

	/// <summary>
	/// Données d'un splash screen
	/// </summary>
	public class SplashScreenData
	{
		public SplashScreenType Type { get; set; }
		public string Text { get; set; }
		public string ImagePath { get; set; }
		public Texture2D Texture { get; set; }
		public float Duration { get; set; }
		public Color TextColor { get; set; } = Colors.White;
		public int FontSize { get; set; } = 48;
	}
}
