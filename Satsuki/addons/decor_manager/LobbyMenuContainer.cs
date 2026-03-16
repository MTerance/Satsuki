using Godot;
using Godot.NativeInterop;
using Satsuki.addons.decor_manager;
using Satsuki.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;

#if TOOLS
[Tool]


public partial class LobbyMenuContainer : VBoxContainer
{

	private readonly List<SpawnPointData> _spawnPoints = new List<SpawnPointData>();

	private readonly System.Collections.Generic.Dictionary<SpawnPointData, Control> _spawnPointToUIControl = new();

	private readonly System.Collections.Generic.Dictionary<Node3D, SpawnPointData> _nodeToSpawnPoint = new();

	//

	CameraPlacementTemplate _cameraPlacementPanel;

	//
	private Button _addSpawnPointButton;

	[Signal]
	public delegate void SpawnPointCreatedEventHandler(Node3D node);

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		CreateSpawnPointPanel();
		CreateCameraPlacementPanel();
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
		SyncSelectedMarkers();
	}

	public override void _ExitTree()
	{
		Cleanup();
	}

	private void CreateCameraPlacementPanel()
	{
		_cameraPlacementPanel = FindChild("CameraPlacementContainer", true, false) as CameraPlacementTemplate;
		if (_cameraPlacementPanel != null)
			_cameraPlacementPanel.Init("lobby");
	}


	public LobbyInfo GetLobbyInfo()
	{
		Godot.Collections.Array<SpawnPointData> spawnPointsArray = new Godot.Collections.Array<SpawnPointData>();
		foreach (var spawn in _spawnPoints)
		{
			spawnPointsArray.Add(spawn);
		}

		CameraPlacement cameraPlacement = null;

        _cameraPlacementPanel.GetCameraPlacementInfo(out cameraPlacement);

        return new LobbyInfo
		{
			SpawnPoints = spawnPointsArray,			
			CameraPlacement = cameraPlacement,
        };
	}

	private void LoadCameraPlacement(CameraPlacement camera)
	{
		if (camera.TypeTemplateCamera == string.Empty)
			camera.TypeTemplateCamera = "Lobby";
		_cameraPlacementPanel.Load(camera);
	}


	public void LoadLobbyInfo(LobbyInfo lobbyInfo)
	{
		ClearSpawnPoints();
		foreach (var spawnPoint in lobbyInfo.SpawnPoints)
		{
			LoadSpawnPoint(spawnPoint);
		}
		LoadCameraPlacement(lobbyInfo.CameraPlacement);
	}

	public void SetLobbyInfo(LobbyInfo lobbyInfo)
	{
		LoadLobbyInfo(lobbyInfo);
	}

	private void Cleanup()
	{
		if (_addSpawnPointButton != null)
		{
			_addSpawnPointButton.Pressed -= OnSpawnPointButtonPressed;
			_addSpawnPointButton = null;
		}
	}

	private void CreateSpawnPointPanel()
	{
		_addSpawnPointButton = FindChild("AddPlayerSpawnButton", true, false) as Button;
		if (_addSpawnPointButton != null &&
			!_addSpawnPointButton.IsConnected(Button.SignalName.Pressed, Callable.From(OnSpawnPointButtonPressed)))
		{
			_addSpawnPointButton.Pressed += OnSpawnPointButtonPressed;
		}
		else
			GD.PrintErr("LobbyMenuContainer: AddSpawnPointButton trouve");
	}

	public void ClearSpawnPoints()
	{
		foreach (var kvp in _nodeToSpawnPoint)
		{
			ClearSpawn(kvp);
		}
		_spawnPoints.Clear();
		_nodeToSpawnPoint.Clear();
		_spawnPointToUIControl.Clear();
	}

	private void ClearSpawn(KeyValuePair<Node3D, SpawnPointData> kvp)
	{
		var node = kvp.Key;
		var spawnPoint = kvp.Value;
		if (node != null)
		{
			node.QueueFree();
			DeleteSpawnPoint(spawnPoint);
			SceneManager.Instance.RemoveNodeFromScene(node);
			_nodeToSpawnPoint.Remove(node);
		}
	}

	private void DeleteSpawnPoint(SpawnPointData spawnPoint)
	{
		_spawnPoints.Remove(spawnPoint);

		if (_spawnPointToUIControl.TryGetValue(spawnPoint, out var uiControl))
		{
			uiControl.QueueFree();
			_spawnPointToUIControl.Remove(spawnPoint);
		}
	}

	private void OnSpawnPointDeleted(string nodename)
	{
		GD.Print($"OnSpawnPointDeleted: Suppression du spawn point {nodename}");

		_nodeToSpawnPoint.TryGetValue(_nodeToSpawnPoint.Keys.FirstOrDefault(k => k.Name == nodename), out var spawnPoint);
		if (spawnPoint != null)
		{
			var kvp = _nodeToSpawnPoint.FirstOrDefault(k => k.Value == spawnPoint);
			ClearSpawn(kvp);
		}
	}

	private void BuildSpawnPointControl(SpawnPointData spawnPoint,Control control)
	{
		var playerSpawnTemplate = control as PlayerSpawnTemplate;
		playerSpawnTemplate.InitPlayerSpawnTemplate(spawnPoint);
		playerSpawnTemplate.OnSpawnPointTypeChanged += OnSpawnPointTypeChanged;
		playerSpawnTemplate.onSpawnPointPositionChanged += OnSpawnPointPositionChanged;
		playerSpawnTemplate.OnDeleteSpawnPoint += OnSpawnPointDeleted;
	}

	private void LoadSpawnPoint(SpawnPointData spawnPoint)
	{
		_spawnPoints.Add(spawnPoint);

		var spawnPointControlPath = "res://addons/decor_manager/Scenes/player_spawn_container.tscn";
		var controlScene = GetModel(spawnPointControlPath);

		Control control = controlScene.Instantiate<Control>();
		var container = FindChild("PlayersSpawnsContainer", true, false) as VBoxContainer;

		if (container != null)
		{
			GD.Print("AddNewSpawnPoint: Ajout du spawn point dans la liste");

			BuildSpawnPointControl(spawnPoint, control);

			_spawnPointToUIControl[spawnPoint] = control;
			var node = new Node3D();
			node.Name = $"gizmo_inter_SpawnPoint_{spawnPoint.Index}";
			node.AddChild(CreateLabelForPointMarker(spawnPoint));
			node.AddChild(CreateSpawnPointMarker(spawnPoint));
			if (node != null)
			{
				_nodeToSpawnPoint[node] = spawnPoint;
				((PlayerSpawnTemplate)control).SetSpawnPointNode(node);
				container.AddChild(control);
				EmitSignal(SignalName.SpawnPointCreated, node);
				GD.Print("AddNewSpawnPoint: Spawn point ajoute dans la liste");
			}
			else
			{
				GD.PrintErr("AddNewSpawnPoint: Erreur lors de la creation du node pour le spawn point");
			}
		}
		else
			GD.PrintErr("AddNewSpawnPoint: Container pour les spawn points introuvable");
	}

	private PackedScene GetModel(string path)
	{
		if (!ResourceLoader.Exists(path))
		{
			GD.PrintErr("GetModel: Resource introuvable a l'adresse " + path);
			return null;
		}

		PackedScene controlScene = GD.Load<PackedScene>(path);
		return controlScene;
	}

	private void AddNewSpawnPoint()
	{
		GD.Print("AddNewSpawnPoint: Begin");
		var spawnPoint = new SpawnPointData(Satsuki.addons.decor_manager.Tools.Tool.GenerateStageId(), Vector3.Zero, Vector3.Zero, SpawnPointType.Standard_Idle);
		LoadSpawnPoint(spawnPoint);
	}

	private void OnSpawnPointPositionChanged(string nodeName, Vector3 newPosition, Vector3 newRotation)
	{
		var tmpSbstrNameId = nodeName.Split('_');
		var id = int.Parse(tmpSbstrNameId.Last());
		GD.Print($"OnSpawnPointPositionChanged: Position a changer pour {id}\n New Pos: {newPosition}, New Rot: {newRotation}");

		var node = _nodeToSpawnPoint.FirstOrDefault(kvp => kvp.Value.Index == id).Key;
		if (node != null &&
			_nodeToSpawnPoint.TryGetValue(node, out var spawnPoint))
		{
			UpdateLabelForPointMarker(node);
			GD.Print($"OnSpawnPointPositionChanged: Position changee pour {nodeName}\n Old Pos : {node.Position} - Old Rot : {node.RotationDegrees}\n New Pos: {newPosition}, New Rot: {newRotation}");
		}
	}

	private void OnSpawnPointButtonPressed()
	{
		AddNewSpawnPoint();
	}

	public List<SpawnPointData> GetSpawnsPoints()
	{
		return _spawnPoints;
	}


	private Label3D CreateLabelForPointMarker(SpawnPointData spawnPoint)
	{
		var label = new Label3D();
		var labelText = $"SpawnPoint_{spawnPoint.Index}\nPos: {spawnPoint.Position}\nRot: {spawnPoint.Rotation}\n Type: {spawnPoint.Type}";
		label.Text = labelText;
		label.Position = spawnPoint.Position + new Vector3(0, 1.5f, 0); // Positionner le label au-dessus du marqueur
		label.FontSize = 24;
		label.NoDepthTest = true;

		return label;
	}

	private void UpdateLabelForPointMarker(Node3D node)
	{
		GD.Print($"[LobbyMenuContainer] UpdateLabelForPointMarker called for node: {node?.Name}");

		if (_nodeToSpawnPoint.TryGetValue(node, out var spawnPoint))
		{
			Label3D label = null;
			for (int i = 0; i < node.GetChildCount(); i++)
			{
				if (node.GetChild(i) is Label3D foundLabel)
				{
					label = foundLabel;
					break;
				}
			}

			if (label != null)
			{
				label.Text = $"SpawnPoint_{spawnPoint.Index}\nPos: {node.Position}\nRot: {node.RotationDegrees}\n Type: {spawnPoint.Type}";
				GD.Print($"Label updated for SpawnPoint_{spawnPoint.Index}");
			}
		}
	}

	private Sprite3D CreateSpawnPointMarker(SpawnPointData spawnPoint)
	{
		Sprite3D marker = new Sprite3D();
		marker.Name = $"SpawnPoint_{spawnPoint.Index}";
		marker.Texture = GD.Load<Texture2D>("res://addons/decor_manager/Icons/blue-user.png");
		marker.Scale = new Vector3(0.5f, 0.5f, 0.5f);
		marker.Position = spawnPoint.Position;
		marker.RotationDegrees = new Vector3(90, 90, 90);

		return marker;
	}

	private void UpdateSpawnPointFromMarker(Node3D node)
	{
		if (_nodeToSpawnPoint.TryGetValue(node, out var spawnPoint))
		{
			spawnPoint.Position = node.Position;
			spawnPoint.Rotation = node.RotationDegrees;
		}
	}


	private void SyncSelectedMarkers()
	{
		foreach (var kvp in _nodeToSpawnPoint)
		{
			var node = kvp.Key;
			var spawnPoint = kvp.Value;

			// Verifier si la position ou rotation a change
			if (node.Position != spawnPoint.Position
				|| node.RotationDegrees != spawnPoint.Rotation)
			{
				UpdateSpawnPointFromMarker(node);
			}
		}
	}

	private void OnSpawnPointTypeChanged(int id, int type)
	{
		var node = _nodeToSpawnPoint.FirstOrDefault(kvp => kvp.Value.Index == id).Key;
		if (node != null &&
			_nodeToSpawnPoint.TryGetValue(node, out var spawnPoint))
		{
			spawnPoint.Type = (SpawnPointType)type;
			UpdateLabelForPointMarker(node);
			GD.Print($"Spawn point {spawnPoint.Index} type changed to {type}");
		}
	}
#endif
}
