using Godot;
using System;
using System.Collections.Generic;

namespace Satsuki.Manager
{
	/// <summary>
	/// Gestionnaire de splash screens avec systeme de transition
	/// Gere completement l'affichage des credits et sequences d'images
	/// </summary>
	public partial class SplashScreenManager : Node
	{
		#region Private Fields
		private List<SplashScreenData> _splashScreens = new List<SplashScreenData>();
		private int _currentIndex = 0;
		private ColorRect _fadeOverlay;
		private ColorRect _backgroundRect;
		private TextureRect _imageDisplay;
		private Label _textDisplay;
		private Timer _displayTimer;
		private bool _isTransitioning = false;
		private float _fadeSpeed = 2.0f;
		
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
			GD.Print("SplashScreenManager: Debut de l'initialisation");
			
			var canvasLayer = new CanvasLayer();
			AddChild(canvasLayer);
			
			// Fond noir permanent pour les images
			_backgroundRect = new ColorRect
			{
				Color = new Color(0, 0, 0, 1),
				MouseFilter = Control.MouseFilterEnum.Ignore,
				Visible = false
			};
			canvasLayer.AddChild(_backgroundRect);
			_backgroundRect.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.FullRect);
			GD.Print("BackgroundRect cree");
			
			_imageDisplay = new TextureRect
			{
				ExpandMode = TextureRect.ExpandModeEnum.IgnoreSize,
				StretchMode = TextureRect.StretchModeEnum.KeepAspectCentered,
				Visible = false
			};
			canvasLayer.AddChild(_imageDisplay);
			_imageDisplay.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.FullRect);
			GD.Print($"ImageDisplay cree");

			_textDisplay = new Label
			{
				HorizontalAlignment = HorizontalAlignment.Center,
				VerticalAlignment = VerticalAlignment.Center,
				Visible = false
			};
			_textDisplay.AddThemeColorOverride("font_color", Colors.White);
			_textDisplay.AddThemeFontSizeOverride("font_size", 48);
			canvasLayer.AddChild(_textDisplay);
			_textDisplay.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.FullRect);
			GD.Print("TextDisplay cree");
			
			// Overlay de fade AU-DESSUS de tout (ajoute en dernier)
			_fadeOverlay = new ColorRect
			{
				Color = new Color(0, 0, 0, 1),
				MouseFilter = Control.MouseFilterEnum.Ignore
			};
			canvasLayer.AddChild(_fadeOverlay);
			_fadeOverlay.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.FullRect);
			GD.Print("FadeOverlay cree (au-dessus)");

			_displayTimer = new Timer();
			_displayTimer.OneShot = true;
			_displayTimer.Timeout += OnDisplayTimerTimeout;
			AddChild(_displayTimer);
			GD.Print("Timer cree");

			GD.Print("SplashScreenManager initialise avec succes");
		}
		#endregion

		#region Public API - Configuration
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
			GD.Print($"Splash screen texte ajoute: {text} ({duration}s)");
		}

		public void AddImageSplash(string imagePath, float duration = 3.0f)
		{
			var texture = GD.Load<Texture2D>(imagePath);
			if (texture == null)
			{
				GD.PrintErr($"Impossible de charger l'image: {imagePath}");
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
			GD.Print($"Splash screen image ajoute: {imagePath} ({duration}s)");
		}

		public void SetupCustomCredits()
		{
			Clear();		
			GD.Print("SetupCustomCredits: Debut");
			// Ajouter les images
			AddCreditImagesFromFolder(5.0f);		
			GD.Print($"Credits personnalises configures - Total: {GetSplashScreenCount()} ecrans");
		}

		private void TryAddImageIfExists(string imagePath, float duration)
		{
			if (ResourceLoader.Exists(imagePath))
			{
				AddImageSplash(imagePath, duration);
			}
		}

		public void SetFadeSpeed(float speed)
		{
			_fadeSpeed = Mathf.Max(0.1f, speed);
		}

		public void Clear()
		{
			_splashScreens.Clear();
			_currentIndex = 0;
			_totalSkips = 0;
			_isSequenceActive = false;
			GD.Print("Splash screens effaces");
		}
		#endregion

		#region Public API - Controle de sequence
		public void StartSequence()
		{
			if (_splashScreens.Count == 0)
			{
				GD.PrintErr("Aucun splash screen a afficher");
				EmitSignal(SignalName.AllSplashScreensCompleted);
				return;
			}

			_currentIndex = 0;
			_totalSkips = 0;
			_sequenceStartTime = DateTime.UtcNow;
			_isSequenceActive = true;
			
			GD.Print($"Demarrage de la sequence de {_splashScreens.Count} splash screens");
			EmitSignal(SignalName.SequenceStarted, _splashScreens.Count);
			
			ShowNextSplash();
		}

		public void Skip()
		{
			if (_isTransitioning || !_isSequenceActive)
				return;

			_displayTimer.Stop();
			_totalSkips++;
			
			GD.Print($"Skip vers le splash screen suivant (Total skips: {_totalSkips})");
			EmitSignal(SignalName.SplashScreenSkipped, _currentIndex);
			
			FadeOut();
		}

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

			GD.Print($"Toute la sequence a ete sautee (Total skips: {_totalSkips})");
			EmitSignal(SignalName.AllSplashScreensCompleted);
		}

		public void HandleInput(InputEvent @event)
		{
			if (!_isSequenceActive) return;

			if (@event is InputEventKey keyEvent && keyEvent.Pressed)
			{
				if (keyEvent.Keycode == Key.Space || keyEvent.Keycode == Key.Enter)
				{
					Skip();
				}
				else if (keyEvent.Keycode == Key.Escape)
				{
					SkipAll();
				}
			}
			
			if (@event is InputEventMouseButton mouseEvent && mouseEvent.Pressed)
			{
				Skip();
			}
		}
		#endregion

		#region Public API - Etat et statistiques
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
					SkipRate = elapsedTime > 0 ? Math.Round(_totalSkips / elapsedTime * 60, 2) : 0
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

		public int GetSplashScreenCount()
		{
			return _splashScreens.Count;
		}

		public int GetCurrentIndex()
		{
			return _currentIndex;
		}

		public int GetTotalSkips()
		{
			return _totalSkips;
		}

		public bool IsSequenceActive()
		{
			return _isSequenceActive;
		}

		private string FormatElapsedTime(double seconds)
		{
			int minutes = (int)(seconds / 60);
			int secs = (int)(seconds % 60);
			return $"{minutes:D2}:{secs:D2}";
		}
		#endregion

		#region Private - Logique d'affichage
		private void ShowNextSplash()
		{
			if (_currentIndex >= _splashScreens.Count)
			{
				_isSequenceActive = false;
				GD.Print("Tous les splash screens termines");
				
				var finalState = GetSplashScreenState();
				GD.Print($"Etat final: {System.Text.Json.JsonSerializer.Serialize(finalState)}");
				
				EmitSignal(SignalName.AllSplashScreensCompleted);
				return;
			}

			var splash = _splashScreens[_currentIndex];
			GD.Print($"Affichage du splash screen {_currentIndex + 1}/{_splashScreens.Count}: {splash.Text ?? splash.ImagePath}");

			_isTransitioning = true;
			FadeIn(splash);
		}

		private async void FadeIn(SplashScreenData splash)
		{
			GD.Print($"FadeIn: Debut pour type={splash.Type}");
			GD.Print($"  - FadeOverlay alpha initial: {_fadeOverlay.Color.A}");
			
			if (splash.Type == SplashScreenType.Text)
			{
				_textDisplay.Text = splash.Text;
				_textDisplay.AddThemeColorOverride("font_color", splash.TextColor);
				_textDisplay.AddThemeFontSizeOverride("font_size", splash.FontSize);
				_textDisplay.Visible = true;
				_imageDisplay.Visible = false;
				_backgroundRect.Visible = false;
				GD.Print($"FadeIn: Texte affiche - '{splash.Text}'");
			}
			else if (splash.Type == SplashScreenType.Image)
			{
				if (splash.Texture == null)
				{
					GD.PrintErr($"FadeIn: Texture est null pour {splash.ImagePath}");
					return;
				}
				
				GD.Print($"FadeIn: Configuration de l'image");
				GD.Print($"  - Chemin: {splash.ImagePath}");
				GD.Print($"  - Taille texture: {splash.Texture.GetSize()}");
				
				_imageDisplay.Texture = splash.Texture;
				_imageDisplay.Visible = true;
				_textDisplay.Visible = false;
				_backgroundRect.Visible = true;
				
				GD.Print($"FadeIn: Image configuree et visible=true");
			}

			GD.Print($"FadeIn: Debut du tween fade (1.0 -> 0.0 sur {1.0f / _fadeSpeed}s)");
			var tween = CreateTween();
			tween.TweenProperty(_fadeOverlay, "color:a", 0.0f, 1.0f / _fadeSpeed);
			await ToSignal(tween, Tween.SignalName.Finished);
			GD.Print($"FadeIn: Tween fade termine - alpha final: {_fadeOverlay.Color.A}");

			_isTransitioning = false;
			_displayTimer.Start(splash.Duration);
			GD.Print($"FadeIn: Timer demarre pour {splash.Duration}s");
		}

		private async void FadeOut()
		{
			_isTransitioning = true;
			GD.Print($"FadeOut: Debut - alpha initial: {_fadeOverlay.Color.A}");

			var tween = CreateTween();
			tween.TweenProperty(_fadeOverlay, "color:a", 1.0f, 1.0f / _fadeSpeed);
			GD.Print($"FadeOut: Tween demarre (0.0 -> 1.0 sur {1.0f / _fadeSpeed}s)");
			await ToSignal(tween, Tween.SignalName.Finished);
			GD.Print($"FadeOut: Tween termine - alpha final: {_fadeOverlay.Color.A}");

			_textDisplay.Visible = false;
			_imageDisplay.Visible = false;
			_backgroundRect.Visible = false;

			EmitSignal(SignalName.SplashScreenCompleted);

			_currentIndex++;
			ShowNextSplash();
		}

		private void OnDisplayTimerTimeout()
		{
			if (!_isTransitioning && _isSequenceActive)
			{
				FadeOut();
			}
		}
		#endregion

		public void AddCreditImagesFromFolder(float duration = 3.0f)
		{
			string folderPath = "res://Assets/Img/Credits";
			
			if (!DirAccess.DirExistsAbsolute(folderPath))
			{
				GD.PrintErr($"Dossier introuvable: {folderPath}");
				GD.Print("Tentative avec res://Img/Credits...");
				folderPath = "res://Img/Credits";
			}
			
			var dir = DirAccess.Open(folderPath);
			if (dir == null)
			{
				GD.PrintErr($"Impossible d'ouvrir le dossier: {folderPath}");
				return;
			}

			int imageCount = 0;
			dir.ListDirBegin();
			string fileName = dir.GetNext();
			
			while (fileName != "")
			{
				if (!dir.CurrentIsDir())
				{
					string lowerFileName = fileName.ToLower();
					if (lowerFileName.EndsWith(".png") || lowerFileName.EndsWith(".jpg") || 
					    lowerFileName.EndsWith(".jpeg") || lowerFileName.EndsWith(".webp"))
					{
						string imagePath = folderPath + "/" + fileName;
						AddImageSplash(imagePath, duration);
						imageCount++;
					}
				}
				fileName = dir.GetNext();
			}
			dir.ListDirEnd();
			
			GD.Print($"{imageCount} splash screens images ajoutes depuis {folderPath}");
		}
	}

	public enum SplashScreenType
	{
		Text,
		Image
	}

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
