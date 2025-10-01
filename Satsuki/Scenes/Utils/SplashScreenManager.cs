using Godot;
using Godot.Collections;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

public partial class SplashScreenManager : Control
{
    [Export] public Array<TextureRect> 	SplashScreenList = new Array<TextureRect>{};
    [Export] public float FadeInDuration { get; set; } = 1.0f;
    [Export] public float DisplayDuration { get; set; } = 2.0f;
    [Export] public float FadeOutDuration { get; set; } = 1.0f;

    private ColorRect _background;
    private Tween _tween;

    [Signal] public delegate void FadeInStartedEventHandler();
    [Signal] public delegate void FadeInFinishedEventHandler();
    [Signal] public delegate void FadeOutStartedEventHandler();
    [Signal] public delegate void FadeOutFinishedEventHandler();


    public override async void _Ready()
    {

    }

    public override async void _Draw()
    {

    }




    // Puis les émettre aux bons moments dans les méthodes
    private async Task FadeIn()
    {
        EmitSignal(SignalName.FadeInStarted);

        var tcs = new TaskCompletionSource<bool>();

        _tween.TweenProperty(this, "modulate:a", 1.0f, FadeInDuration);
        _tween.TweenCallback(Callable.From(() => {
            EmitSignal(SignalName.FadeInFinished);
            tcs.SetResult(true);
        })).SetDelay(FadeInDuration);

        await tcs.Task;
    }

}
