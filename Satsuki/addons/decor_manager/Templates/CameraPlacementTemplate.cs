using Godot;
using Satsuki.addons.decor_manager;
using Satsuki.addons.decor_manager.Tools;
using Satsuki.Models;
using System;


#if TOOLS
[Tool]
public partial class CameraPlacementTemplate : PanelContainer
{
	#region properties

	private string _idTemplateCamera;
	private string _typeTemplateCamera = "default";


	#region Vector3D TextBox

	private Vector3dTextBox _positionCameraTextBox;
	private Vector3dTextBox _rotationCameraTextBox;
	private Vector3dTextBox _targetCameraTextBox;

	#endregion

	#region Nodes definition
	private Node3D _nodeCamera;
	private Node3D _nodeTargetCamera;
	#endregion

	#endregion

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		_positionCameraTextBox = FindChild("PositionBox", true, false) as Vector3dTextBox;
		_rotationCameraTextBox = FindChild("RotationBox", true, false) as Vector3dTextBox;
		_targetCameraTextBox = FindChild("TargetBox", true, false) as Vector3dTextBox;

		if (_positionCameraTextBox != null)
			_positionCameraTextBox.Setup("Position Camera", Vector3.Zero);
		if (_rotationCameraTextBox != null)
			_rotationCameraTextBox.Setup("Rotation Camera", Vector3.Zero);
		if (_targetCameraTextBox != null)
			_targetCameraTextBox.Setup("Target Camera", Vector3.Zero);
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
		SyncMarkers();
	}

	private void SyncMarkers()
	{
		UpdateCameraPositionUI();
		UpdateTargetCameraNode();
	}

	private void UpdateCameraPositionUI()
	{
		if (_nodeCamera != null &&
			_positionCameraTextBox != null &&
			_rotationCameraTextBox != null)
		{
			_positionCameraTextBox?.SetValue(_nodeCamera.Position);
			_rotationCameraTextBox?.SetValue(_nodeCamera.RotationDegrees);           
		}
	}

	private void UpdateTargetCameraNode()
	{
		if (_nodeTargetCamera != null && _targetCameraTextBox != null)
		{
			_targetCameraTextBox?.SetValue(_nodeTargetCamera.Position);
		}
	}

	public void Init(string typeTemplateCamera)
	{
		_typeTemplateCamera = typeTemplateCamera;
		_idTemplateCamera = Satsuki.addons.decor_manager.Tools.Tool.GenerateStageId().ToString();
		InitCameraPlacementTemplate();
		InitLabels();
		CreateCameraNode();
		CreateCameraTargetNode();
	}

	public void UpdateCameraPlacementInfo(CameraPlacement cameraPlacement)
	{
		cameraPlacement.Position = _nodeCamera.Position;
		cameraPlacement.Rotation = _nodeCamera.RotationDegrees;
		cameraPlacement.Target = _nodeTargetCamera.Position;
	}


	public void GetCameraPlacementInfo(out CameraPlacement cameraPlacement)
	{
		cameraPlacement = new CameraPlacement();
		cameraPlacement.Position = _nodeCamera != null ? _nodeCamera.Position : Vector3.Zero;
		cameraPlacement.Rotation = _nodeCamera != null ? _nodeCamera.RotationDegrees : Vector3.Zero;
		cameraPlacement.Target = _nodeTargetCamera != null ? _nodeTargetCamera.Position : Vector3.Zero;
		cameraPlacement.TypeTemplateCamera = _typeTemplateCamera;
		cameraPlacement.Index = int.TryParse(_idTemplateCamera, out int index) ? index : 0;
	}

	public void GetPositionAndRotation(out Vector3 position, out Vector3 rotation)
	{
		position = _nodeCamera != null ? _nodeCamera.Position : Vector3.Zero;
		rotation = _nodeCamera != null ? _nodeCamera.RotationDegrees : Vector3.Zero;
	}


	public void GetPositionTarget(out Vector3 positionTarget)
	{
		positionTarget = _nodeTargetCamera != null ? _nodeTargetCamera.Position : Vector3.Zero;
	}

	public void Load(CameraPlacement camera)
	{
		if (camera.Index == 0)
			camera.Index = Satsuki.addons.decor_manager.Tools.Tool.GenerateStageId();
		_idTemplateCamera = camera.Index.ToString();
		_typeTemplateCamera = camera.TypeTemplateCamera;
		SetNodeCameraPosition(camera.Position);
		SetNodeCameraRotation(camera.Rotation);
		SetNodeTargetCameraPosition(camera.Target);
		UpdateCameraNode();
	}

	private void UpdateCameraNode()
	{
		if (_nodeCamera == null)
			return;
		_nodeCamera.Name = $"Camera_{_typeTemplateCamera}_{_idTemplateCamera}";

	}

	private void CreateCameraNode()
	{
		if (_nodeCamera == null)
			_nodeCamera = new Node3D();
		Sprite3D sprite = NodeBuilder.CreateSprite("res://addons/decor_manager/Icons/blue-camera-video.png", $"CameraSprite_{_typeTemplateCamera}_{_idTemplateCamera}", new Vector3(0.5f, 0.5f, 0.5f));
		Label3D label = NodeBuilder.CreateLabel($"Camera {_idTemplateCamera}", $"LabelCamera_{_typeTemplateCamera}_{_idTemplateCamera}", new Vector3(0, 0.75f, 0), new Vector3(-90, 0, 0), 24, true);
		_nodeCamera.AddChild(sprite);
		_nodeCamera.AddChild(label);
		_nodeCamera.Name = $"Camera_{_typeTemplateCamera}_{_idTemplateCamera}";
		_nodeCamera.Position = Vector3.Zero;
		SceneManager.Instance.AddNodeToScene(_nodeCamera);

	}

	private void CreateCameraTargetNode()
	{
		if (_nodeTargetCamera == null)
			_nodeTargetCamera = new Node3D();
		Sprite3D sprite = NodeBuilder.CreateSprite("res://addons/decor_manager/Icons/blue-target.png", $"CameraTargetSprite_{_typeTemplateCamera}_{_idTemplateCamera}", new Vector3(0.5f, 0.5f, 0.5f));
		Label3D label = NodeBuilder.CreateLabel($"Camera Target {_idTemplateCamera}", $"LabelCameraTarget_{_typeTemplateCamera}_{_idTemplateCamera}", new Vector3(0, 0.75f, 0), new Vector3(-90, 0, 0), 24, true);
		_nodeTargetCamera.AddChild(sprite);
		_nodeTargetCamera.AddChild(label);
		_nodeTargetCamera.Name = $"CameraTarget_{_typeTemplateCamera}_{_idTemplateCamera}";
		_nodeTargetCamera.Position = Vector3.Zero;
		_nodeTargetCamera.RotationDegrees = new Vector3(-90, 0, 90);
		SceneManager.Instance.AddNodeToScene(_nodeTargetCamera);
	}

	private void SetNodeTargetCameraPosition(Vector3 nodeTargetCameraPosition)
	{
		if (_nodeTargetCamera != null)
			_nodeTargetCamera.Position = nodeTargetCameraPosition;
	}

	private void SetNodeCameraPosition(Vector3 nodeCameraPosition)
	{
		if (_nodeCamera != null)
			_nodeCamera.Position = nodeCameraPosition;
	}

    private void SetNodeCameraRotation(Vector3 nodeCameraRotation)
    {
        if (_nodeCamera != null)
            _nodeCamera.RotationDegrees = nodeCameraRotation;
    }

    private void InitLabels()
	{
		_positionCameraTextBox.Setup("Position Camera", Vector3.Zero);
		_rotationCameraTextBox.Setup("Rotation Camera", Vector3.Zero);
		_targetCameraTextBox.Setup("Target Camera", Vector3.Zero);

	}

	private void InitCameraPlacementTemplate()
	{
		_rotationCameraTextBox = FindChild("RotationBox", true, false) as Vector3dTextBox;
		_positionCameraTextBox = FindChild("PositionBox", true, false) as Vector3dTextBox;
		_targetCameraTextBox = FindChild("TargetBox", true, false) as Vector3dTextBox;

		if (_positionCameraTextBox != null) _positionCameraTextBox.ValueChanged += OnVector3TextBoxUpdated;
		else GD.PrintErr("PositionBox not found in CameraPlacementTemplate");
		if (_rotationCameraTextBox != null) _rotationCameraTextBox.ValueChanged += OnVector3TextBoxUpdated;
		else GD.PrintErr("RotationBox not found in CameraPlacementTemplate");
		if (_targetCameraTextBox != null) _targetCameraTextBox.ValueChanged += OnVector3TextBoxUpdated;
		else GD.PrintErr("TargetBox not found in CameraPlacementTemplate");
	}

	private void OnVector3TextBoxUpdated(object sender, EventArgs e)
	{
		Vector3 newCameraPosition = _positionCameraTextBox.GetValue();
		Vector3 newTargetCameraPosition = _targetCameraTextBox.GetValue();
		SetNodeCameraPosition(newCameraPosition);
		SetNodeTargetCameraPosition(newTargetCameraPosition);
	}

	//

	private void CleanupTextBoxEvents()
	{
		if (_positionCameraTextBox != null)
			_positionCameraTextBox.ValueChanged -= OnVector3TextBoxUpdated;
		if (_rotationCameraTextBox != null)
			_rotationCameraTextBox.ValueChanged -= OnVector3TextBoxUpdated;
		if (_targetCameraTextBox != null)
			_targetCameraTextBox.ValueChanged -= OnVector3TextBoxUpdated;
	}

	private void CleanupNodes()
	{
		if (_nodeCamera != null)
		{
			_nodeCamera.QueueFree();
			_nodeCamera = null;
		}
		if (_nodeTargetCamera != null)
		{
			_nodeTargetCamera.QueueFree();
			_nodeTargetCamera = null;
		}
	}

	private void Cleanup()
	{
		CleanupTextBoxEvents();
		CleanupNodes();
	}
}
#endif
