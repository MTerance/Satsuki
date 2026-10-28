using Godot;
using Satsuki.Models;
using System;
using static Lobby;

public partial class LobbyMenuScreen : Node2D
{

    public Sprite2D Background { get; set; }
    public Sprite2D Logo { get; set; }

    public Label LocationName { get; set; }

    public Label GameSessionName { get; set; }


    public override void _Ready()
    {
        Background = GetNode<Sprite2D>("BgdGameImg");
        Logo = GetNode<Sprite2D>("LogoGameImg");
        LocationName = GetNode<Label>("GameSessionLocationLabel");
        GameSessionName = GetNode<Label>("GameSessionNameLabel");
    }


    public void SetMenuScreenContent(LobbyScreenContent lobbyScreenContent)
    {
        LocationName.Text = lobbyScreenContent.LocationName;
        GameSessionName.Text = lobbyScreenContent.GameSessionName;
        Background.Texture = GD.Load<Texture2D>(lobbyScreenContent.BackgroundImgPath);
        Logo.Texture = GD.Load<Texture2D>(lobbyScreenContent.LogoImgPath);
    }

}
