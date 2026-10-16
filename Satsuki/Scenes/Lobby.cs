using Godot;
using Satsuki.Interfaces;
using Satsuki.Manager;
using Satsuki.Models;
using Satsuki.Repositories.Loaders;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Nodes;

public partial class Lobby : Node3D, IScene
{
	private Satsuki.Systems.ServerManager _serverManager;
	private string _lobbyPathScene;
	private CameraPlacement _cameraPlacement;
	private List<Spot> _spots = new List<Spot>();


	public class PlayerProfile
	{
		public Guid Id { get; set; }
		public string Name { get; set; }
		public string Gender { get; set; }
		public int IdSpot { get; set; }
		public string Color { get; set; }
	}


	private List<PlayerProfile> _players = new List<PlayerProfile>();
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
				Id = spawn.Index,
				Position = spawn.Position,
				PlayerSpot = PlayerTypeSpot.Vacant,
				SpawnPoint = spawn
			};
			_spots.Add(spot);
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
				var newProfile = JsonSerializer.Deserialize<PlayerProfile>(messageJson);
				AddPlayer(newProfile);
				break;
			case "UpdatePlayer":
				var updatedProfile = JsonSerializer.Deserialize<PlayerProfile>(messageJson);
				UpdatePlayer(updatedProfile);    
				break;
			case "RetirePlayer":
				var retiredProfile = JsonSerializer.Deserialize<PlayerProfile>(messageJson);
				RetirePlayer(retiredProfile.Id);
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

	public override void _Input(InputEvent @event)
	{
		if (@event is InputEventKey keyEvent && keyEvent.Pressed)
		{
			if (keyEvent.Keycode == Key.Space || keyEvent.Keycode == Key.Enter)
			{
				// debug.
				// add  a cube a the position 000
				var cube = new MeshInstance3D();
				cube.Mesh = new BoxMesh();
				cube.Scale = new Vector3(5, 5, 5);
				cube.Position = _spots[Random.Shared.Next(0,_spots.Count)].Position;
				GD.Print($"Lobby: Adding a cube at position {cube.Position.X},{cube.Position.Y}, {cube.Position.Z}.");
				AddChild(cube);
			}
		}
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
			Spots = _spots.Select(spot => new
			{
				Position = spot.Position,
				PlayerSpot = spot.PlayerSpot.ToString()
			}).ToList()
		};
	}

	private void AddPlayer(PlayerProfile player)
	{
		if (!_spots.Exists(x => x.PlayerSpot == PlayerTypeSpot.Vacant))
		{
			GD.PrintErr("Lobby: Impossible d'ajouter un joueur, tous les spots sont occupés.");
			return;
		}
		var spot = _spots.First(x => x.PlayerSpot == PlayerTypeSpot.Vacant);
		var character = new PlayerLoader().LoadPlayerMesh();
		character.Position = spot.Position;
		character.Name = $"Player_{player.Id}";
		GD.Print($"Lobby: Player {player.Id} mesh loaded and positioned at {character.Position.X},{character.Position.Y},{character.Position.Z}.");
        (character as Character)?.SetAnimation(CharacterAnimation.Idle);
		GD.Print($"Lobby: Adding player {player.Id} to spot {spot.Id} at position {spot.Position}.");
		lobbyLocation.AddChild(character);

		GD.Print($"Lobby: Player {player.Id} added to the scene at position {character.Position.X},{character.Position.Y},{character.Position.Z}.");
		spot.PlayerSpot = PlayerTypeSpot.Occupied;
		GD.Print($"Lobby: Player added to spot {spot.Id}. Spot is now occupied.");
		GD.Print($"Lobby : nb of available spots {_spots.Count(x => x.PlayerSpot == PlayerTypeSpot.Vacant)}");
		_players.Add(player);
		var message = JsonSerializer.Serialize(new
		{
			Order = "PlayerAdded",
			Player = JsonSerializer.Serialize(player)
		});
		_ = _serverManager.BroadcastMessageToAllClients(message);
	}

	private void UpdatePlayer(PlayerProfile player)
	{
		var oldPlayer = _players.FirstOrDefault(p => p.Id == player.Id);
		if (oldPlayer != null)
		{
			oldPlayer.Name = player.Name;
			oldPlayer.Gender = player.Gender;
			oldPlayer.Color = player.Color;
			GD.Print($"Lobby: Player {player.Id} updated.");
		}
		else
		{
			GD.PrintErr($"Lobby: Player {player.Id} not found for update.");
		}
		_ = _serverManager.BroadcastMessageToAllClients(JsonSerializer.Serialize(new
		{
			Order = "PlayerUpdated",
			Player = JsonSerializer.Serialize(player)
		}));

	}

	private void RetirePlayer(Guid idPlayer)
	{
		var nodePlayer = lobbyLocation.GetNodeOrNull<Node3D>($"Player_{idPlayer}");
		if (nodePlayer != null)
		{
			var idSpot = _players.FirstOrDefault(p => p.Id == idPlayer).IdSpot; // Mark the spot as vacant
			_spots.FirstOrDefault(s => s.Id == idSpot).PlayerSpot = PlayerTypeSpot.Vacant;
			_players.RemoveAll(p => p.Id == idPlayer);
			lobbyLocation.RemoveChild(nodePlayer);
			GD.Print($"Lobby: Player_{idPlayer} removed from the lobby.");
			_ = _serverManager.BroadcastMessageToAllClients(JsonSerializer.Serialize(new
			{
				Order = "PlayerRetired",
				PlayerId = idPlayer
			}));
		}
	}

	private void SetQuizzGame()
	{

	}

	private void GoToGame()
	{

	}

}
