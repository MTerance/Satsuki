using Godot;
using Godot.Collections;
using Satsuki.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Scenes.Credits
{
    public partial class SplashScreenManager : Control
    {
        [Export] public string ImagePath { get; set; } = "res://images/splash.png";
        [Export] public float FadeInDuration { get; set; } = 1.0f;
        [Export] public float FadeOutDuration { get; set; } = 1.0f;
        [Export] public float DisplayDuration { get; set; } = 2.0f;

        [Export] public List<SplashScreenModel> SplashScreens = [];

        private TextureRect _imageDisplay;
        private ColorRect _background;
        private Tween _tween;

        [Signal] public delegate void SplashScreenFinishedEventHandler();

        public override void _Ready()
        {
            SetupUI();
            SetupSplashScreens();
            SetAnchorsAndOffsetsPreset(Control.LayoutPreset.FullRect);
            ZIndex = 100; // S'assurer qu'il est au-dessus de tout
        }


        private void SetupSplashScreens()
        {
            // recuperer la liste des ecrans a afficher

            SqliteDbManager.GetInstance.GetConnection();// getSplashScreens();

            foreach (var splashscreen in SplashScreens)
            {
                splashscreen.LoadTexture();
            }
        }


        private void SetupUI()
        {
            // Fond noir
            _background = new ColorRect();
            _background.Color = Colors.Black;
            _background.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.FullRect);
            AddChild(_background);

            // Image du splash screen
            _imageDisplay = new TextureRect();
            _imageDisplay.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.VcenterWide);
            _imageDisplay.ExpandMode = TextureRect.ExpandModeEnum.FitWidthProportional;
            _imageDisplay.StretchMode = TextureRect.StretchModeEnum.KeepAspectCentered;

            // Charger l'image
            if (ResourceLoader.Exists(ImagePath))
            {
                var texture = GD.Load<Texture2D>(ImagePath);
                _imageDisplay.Texture = texture;
            }
            else
            {
                GD.PrintErr($"Image splash screen non trouvée: {ImagePath}");
                // Image de secours (texte)
                var label = new Label();
                label.Text = "SATSUKI";
                label.AddThemeStyleboxOverride("normal", new StyleBoxEmpty());
                label.AddThemeColorOverride("font_color", Colors.White);
                label.AddThemeFontSizeOverride("font_size", 48);
                label.HorizontalAlignment = HorizontalAlignment.Center;
                label.VerticalAlignment = VerticalAlignment.Center;
                label.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.FullRect);
                _imageDisplay.AddChild(label);
            }

            AddChild(_imageDisplay);

            // Tween pour les animations
            _tween = new Tween();
            AddChild(_tween);

            // Commencer invisible
            Modulate = new Color(1, 1, 1, 0);
        }

        public async Task ShowSplashScreen()
        {
            Show();

            try
            {
                // Phase 1: Fade In
                await FadeIn();

                // Phase 2: Attendre
                await Task.Delay(TimeSpan.FromSeconds(DisplayDuration));

                // Phase 3: Fade Out
                await FadeOut();
            }
            catch (Exception ex)
            {
                GD.PrintErr($"Erreur splash screen: {ex.Message}");
            }
            finally
            {
                // Émettre le signal et se cacher
                EmitSignal(SignalName.SplashScreenFinished);
                Hide();
            }
        }

        private async Task FadeIn()
        {
            var tcs = new TaskCompletionSource<bool>();

            _tween.TweenProperty(this, "modulate:a", 1.0f, FadeInDuration);
            _tween.TweenCallback(Callable.From(() => tcs.SetResult(true))).SetDelay(FadeInDuration);

            await tcs.Task;
        }

        private async Task FadeOut()
        {
            var tcs = new TaskCompletionSource<bool>();

            _tween.TweenProperty(this, "modulate:a", 0.0f, FadeOutDuration);
            _tween.TweenCallback(Callable.From(() => tcs.SetResult(true))).SetDelay(FadeOutDuration);

            await tcs.Task;
        }

        public void SetImage(string imagePath)
        {
            ImagePath = imagePath;

            if (_imageDisplay != null && ResourceLoader.Exists(ImagePath))
            {
                var texture = GD.Load<Texture2D>(ImagePath);
                _imageDisplay.Texture = texture;
            }
        }

        public void SetDurations(float fadeIn, float display, float fadeOut)
        {
            FadeInDuration = fadeIn;
            DisplayDuration = display;
            FadeOutDuration = fadeOut;
        }

        // Version simplifiée avec une seule méthode
        public static async Task ShowSimpleSplash(Node parent, string imagePath, float totalDuration = 3.0f)
        {
            var splashManager = new SplashScreenManager();
            splashManager.ImagePath = imagePath;
            splashManager.FadeInDuration = totalDuration * 0.3f;
            splashManager.DisplayDuration = totalDuration * 0.4f;
            splashManager.FadeOutDuration = totalDuration * 0.3f;

            parent.AddChild(splashManager);

            await splashManager.ShowSplashScreen();

            splashManager.QueueFree();
        }
    }
}
