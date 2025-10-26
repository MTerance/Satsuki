using Godot;
using System;
using System.Collections.Generic;

namespace Satsuki.Manager
{
	/// <summary>
	/// Gestionnaire de splash screens avec système de transition
	/// </summary>
	public partial class SplashScreenManager : Node
	{
		private List<SplashScreenData> _splashScreens = new List<SplashScreenData>();
		private int _currentIndex = 0;
		private ColorRect _fadeOverlay;
		private TextureRect _imageDisplay;
		private Label _textDisplay;
		private Timer _displayTimer;
		private bool _isTransitioning = false;
		private float _fadeSpeed = 2.0f;

		[Signal]
		public delegate void SplashScreenCompletedEventHandler();

		[Signal]
		public delegate void AllSplashScreensCompletedEventHandler();

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

			GD.Print("? SplashScreenManager initialisé");
		}

		/// <summary>
		/// Ajoute un splash screen texte
		/// </summary>
		public void AddTextSplash(string text, float duration = 3.0f, Color? textColor = null)
		{
			var splash = new SplashScreenData
			{
				Type = SplashScreenType.Text,
				Text = text,
				Duration = duration,
				TextColor = textColor ?? Colors.White
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
			GD.Print($"?? Démarrage de la séquence de {_splashScreens.Count} splash screens");
			ShowNextSplash();
		}

		/// <summary>
		/// Affiche le splash screen suivant
		/// </summary>
		private void ShowNextSplash()
		{
			if (_currentIndex >= _splashScreens.Count)
			{
				GD.Print("? Tous les splash screens terminés");
				EmitSignal(SignalName.AllSplashScreensCompleted);
				return;
			}

			var splash = _splashScreens[_currentIndex];
			GD.Print($"??? Affichage du splash screen {_currentIndex + 1}/{_splashScreens.Count}");

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
			if (!_isTransitioning)
			{
				FadeOut();
			}
		}

		/// <summary>
		/// Passe au splash screen suivant (skip)
		/// </summary>
		public void Skip()
		{
			if (_isTransitioning)
				return;

			_displayTimer.Stop();
			FadeOut();
		}

		/// <summary>
		/// Passe directement à la fin de la séquence
		/// </summary>
		public void SkipAll()
		{
			_currentIndex = _splashScreens.Count;
			_displayTimer.Stop();
			_textDisplay.Visible = false;
			_imageDisplay.Visible = false;
			_fadeOverlay.Color = new Color(0, 0, 0, 1);

			GD.Print("?? Toute la séquence a été sautée");
			EmitSignal(SignalName.AllSplashScreensCompleted);
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
			GD.Print("??? Splash screens effacés");
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
	}
}
