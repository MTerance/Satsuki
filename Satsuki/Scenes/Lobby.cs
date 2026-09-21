using Godot;
using Satsuki.Models;
using System;
using System.Collections.Generic;

public partial class Lobby : Node3D
{
	private string _lobbyPathScene;
	private CameraPlacement _cameraPlacement;
	private List<Spot> Spots = new List<Spot>();

	private void LoadLobby(StageResource stageResource)
	{
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

	private Satsuki.Systems.ServerManager _serverManager;

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		_serverManager = GetNodeOrNull<Satsuki.Systems.ServerManager>("/root/ServerManager");
		if (_serverManager != null)
		{
			_serverManager.SceneOrderReceived += OnSceneOrderReceived;
		}
	}

	public override void _ExitTree()
	{
		if (_serverManager != null)
		{
			_serverManager.SceneOrderReceived -= OnSceneOrderReceived;
		}
		base._ExitTree();
	}

	private void OnSceneOrderReceived(string orderRequestJson)
	{
		if (Satsuki.Utils.ServerUtils.TryDeserializeOrderRequest(orderRequestJson, out var orderRequest))
		{
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
}
