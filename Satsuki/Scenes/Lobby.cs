using Godot;
using Satsuki.Interfaces;
using Satsuki.Manager;
using Satsuki.Models;
using Satsuki.Repositories.Loaders;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json.Nodes;

public partial class Lobby : Node3D, IScene
{
    private Satsuki.Systems.ServerManager _serverManager;
    private string _lobbyPathScene;
    private CameraPlacement _cameraPlacement;
    private List<Spot> Spots = new List<Spot>();
    private Node lobbyLocation { get; set; }
    private Camera3D _camera;

    private void InitCameraPlacement()
    {
        _camera = GetNodeOrNull<Camera3D>("Camera3D");
        if (_camera == null)
        {
            _camera = new Camera3D();
            _camera.Position = _cameraPlacement.Position;
            // set target for camera to look at by getting cameraPlacement target value
            AddChild(_camera);
            GD.Print("Lobby: Camera3D created and added to the scene.");
        }
        else
        {
            _camera.Position = _cameraPlacement.Position;
            GD.Print("Lobby: Camera3D found and position set.");
        }
    }

    private void GetLobbyResource()
    {
        var lobbyInfo = GameInfoManager.Instance.GetGameInfo("Lobby");

        if (lobbyInfo != null && lobbyInfo.ContainsKey("IdStage"))
        {
            var idStage = ((int)lobbyInfo["IdStage"]);
            LocationLoader locationLoader = new LocationLoader();
            var stageResource = locationLoader.LoadStageRsc(idStage);
            lobbyLocation = locationLoader.LoadStage(stageResource);
            AddChild(lobbyLocation);
            LoadLobby(stageResource);
        }
        else
            GD.PrintErr("Lobby: Impossible de récupérer les informations du lobby.");
    }


    private void LoadLobby(StageResource stageResource)
    {
        _cameraPlacement = stageResource.LobbyInfo.CameraPlacement;

        var lobbyResource = stageResource.LobbyInfo;

        foreach (var spawn in lobbyResource.SpawnPoints)
        {
            var spot = new Spot
            {
                Position = spawn.Position,
                PlayerSpot = PlayerTypeSpot.Vacant,
                SpawnPoint = spawn
            };
            Spots.Add(spot);
        }
    }

    private void Init()
    {
        GetLobbyResource();
        InitCameraPlacement();
    }

    // Called when the node enters the scene tree for the first time.

    private void InitServerManager()
    {
        _serverManager = GetNodeOrNull<Satsuki.Systems.ServerManager>("/root/ServerManager");
        if (_serverManager != null)
        {
            _serverManager.SceneOrderReceived += OnSceneOrderReceived;
        }
        else
        {
            GD.PrintErr("Lobby: Impossible de récupérer le ServerManager.");
        }
    }

    public void InitLobby()
    {
        InitServerManager();
        Init();
    }

    public override void _Ready()
    {
        GD.Print("Lobby: Initialisation de la scène Lobby.");
        InitLobby();
        GD.Print($"LOG : Scene {GetSceneName()} initialisee a " + DateTime.Now.ToString("o"));
    }

    public override void _ExitTree()
    {
        if (_serverManager != null)
        {
            _serverManager.SceneOrderReceived -= OnSceneOrderReceived;
        }
        base._ExitTree();
    }


    private void ProcessMessage(string order,  string messageJson)
    {
        switch (order)
        {
            case "AddPlayer":
                AddPlayer();
                break;
            case "UpdatePlayer":
                UpdatePlayer();
                break;
            case "RetirePlayer":
                RetirePlayer();
                break;
            case "SetQuizzGame":
                SetQuizzGame();
                break;
            case "GoToGame":
                GoToGame();
                break;
            default:
                GD.PrintErr($"Lobby: Ordre scène inconnu '{order}'");
                break;
        }
    }


    private void OnSceneOrderReceived(string orderRequestJson)
    {
        if (Satsuki.Utils.ServerUtils.TryDeserializeOrderRequest(orderRequestJson, out var orderRequest))
        {
            ProcessMessage(orderRequest.Order, orderRequestJson);
            GD.Print($"Lobby: Ordre scène reçu '{orderRequest.Order}'");
        }
        else
        {
            GD.PrintErr($"Lobby: Impossible de désérialiser l'ordre scène: {orderRequestJson}");
        }
    }

    // Called every frame. 'delta' is the elapsed time since the previous frame.
    public override void _Process(double delta)
    {
    }

    public string GetSceneName()
    {
        return "Lobby";
    }

    public object GetSceneState()
    {
        return new
        {
            SceneInfo = new
            {
                SceneName = "Lobby",
                SceneType = "Lobby",
                Timestamp = DateTime.UtcNow
            },
            Spots = Spots.Select(spot => new
            {
                Position = spot.Position,
                PlayerSpot = spot.PlayerSpot.ToString()
            }).ToList()
        };
    }

    private void AddPlayer()
    {

    }

    private void UpdatePlayer()
    {

    }

    private void RetirePlayer()
    {

    }

    private void SetQuizzGame()
    {

    }

    private void GoToGame()
    {

    }

}
