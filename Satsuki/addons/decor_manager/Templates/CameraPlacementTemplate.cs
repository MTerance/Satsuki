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

    #region Labels definition
    private Label _labelPositionCamera;
	private Label _labelRotationCamera;
	private Label _labelPositionTargetCamera;
	#endregion

	#region SpinBoxes definition
	private SpinBox _positionCameraX;
	private SpinBox _positionCameraY;
	private SpinBox _positionCameraZ;
	private SpinBox _rotationCameraX;
	private SpinBox _rotationCameraY;
	private SpinBox _rotationCameraZ;
	private SpinBox _positionTargetCameraX;
	private SpinBox _positionTargetCameraY;
	private SpinBox _positionTargetCameraZ;
	#endregion

	#region Nodes definition
	private Node3D _nodeCamera;
	private Node3D _nodeTargetCamera;
	#endregion

	#endregion

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		
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
        if (_nodeCamera != null && _positionCameraX != null)
		{
            _positionCameraX.Value = _nodeCamera.Position.X;
			_positionCameraY.Value = _nodeCamera.Position.Y;
			_positionCameraZ.Value = _nodeCamera.Position.Z;
			_rotationCameraX.Value = _nodeCamera.RotationDegrees.X;
			_rotationCameraY.Value = _nodeCamera.RotationDegrees.Y;
			_rotationCameraZ.Value = _nodeCamera.RotationDegrees.Z;
		}
	}

	private void UpdateTargetCameraNode()
	{
		if (_nodeTargetCamera != null && _positionTargetCameraX != null)
		{
            _positionTargetCameraX.Value = _nodeTargetCamera.Position.X;
			_positionTargetCameraY.Value = _nodeTargetCamera.Position.Y;
			_positionTargetCameraZ.Value = _nodeTargetCamera.Position.Z;
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

	private void InitLabels()
	{
        var posBox = FindChild("PositionBoxContainer", true, false);
        var rotBox = FindChild("RotationBoxContainer2", true, false);
        var targetBox = FindChild("TargetPositionBoxContainer", true, false);

        _labelPositionCamera = posBox?.FindChild("LabelPositionCamera", false, false) as Label;
        _labelRotationCamera = rotBox?.FindChild("LabelRotationCamera", false, false) as Label;
        _labelPositionTargetCamera = targetBox?.FindChild("LabelPositionTarget", false, false) as Label;

        if (_labelPositionCamera != null)
            _labelPositionCamera.MouseEntered += HandlePositionCameraLabelMouseEntered;
        if (_labelRotationCamera != null)
            _labelRotationCamera.MouseEntered += HandleRotationCameraLabelMouseEntered;
        if (_labelPositionTargetCamera != null)
            _labelPositionTargetCamera.MouseEntered += HandlePositionTargetCameraLabelMouseEntered;
    }

    private void HandlePositionTargetCameraLabelMouseEntered()
	{

	}

	private void HandleRotationCameraLabelMouseEntered()
	{

	}

	private void HandlePositionCameraLabelMouseEntered()
	{
		;
	}

	private void InitCameraPlacementTemplate()
	{
        _positionCameraX = FindChild("PositionCameraXSpinBox", true, false) as SpinBox;
        _positionCameraY = FindChild("PositionCameraYSpinBox", true, false) as SpinBox;
        _positionCameraZ = FindChild("PositionCameraZSpinBox", true, false) as SpinBox;
        _rotationCameraX = FindChild("RotationCameraXSpinBox", true, false) as SpinBox;
        _rotationCameraY = FindChild("RotationCameraYSpinBox", true, false) as SpinBox;
        _rotationCameraZ = FindChild("RotationCameraZSpinBox", true, false) as SpinBox;
        _positionTargetCameraX = FindChild("PositionCameraTargetXSpinBoxSpinBox", true, false) as SpinBox;
        _positionTargetCameraY = FindChild("PositionCameraTargetYSpinBoxSpinBox", true, false) as SpinBox;
        _positionTargetCameraZ = FindChild("PositionCameraTargetZSpinBoxSpinBox", true, false) as SpinBox;

        if (_positionCameraX != null) _positionCameraX.ValueChanged += OnSpinBoxUpdated;
        if (_positionCameraY != null) _positionCameraY.ValueChanged += OnSpinBoxUpdated;
        if (_positionCameraZ != null) _positionCameraZ.ValueChanged += OnSpinBoxUpdated;
        if (_rotationCameraX != null) _rotationCameraX.ValueChanged += OnSpinBoxUpdated;
        if (_rotationCameraY != null) _rotationCameraY.ValueChanged += OnSpinBoxUpdated;
        if (_rotationCameraZ != null) _rotationCameraZ.ValueChanged += OnSpinBoxUpdated;
        if (_positionTargetCameraX != null) _positionTargetCameraX.ValueChanged += OnSpinBoxUpdated;
        if (_positionTargetCameraY != null) _positionTargetCameraY.ValueChanged += OnSpinBoxUpdated;
        if (_positionTargetCameraZ != null) _positionTargetCameraZ.ValueChanged += OnSpinBoxUpdated;
    }

    private void OnSpinBoxUpdated(double value)
	{
		Vector3 newCameraPosition = new Vector3((float)_positionCameraX.Value, (float)_positionCameraY.Value, (float)_positionCameraZ.Value);
		Vector3 newTargetCameraPosition = new Vector3((float)_positionTargetCameraX.Value, (float)_positionTargetCameraY.Value, (float)_positionTargetCameraZ.Value);
		SetNodeCameraPosition(newCameraPosition);
		SetNodeTargetCameraPosition(newTargetCameraPosition);
	}

	//

	private void CleanupSpinBoxEvents()
	{
		if (_positionCameraX != null)
			_positionCameraX.ValueChanged -= OnSpinBoxUpdated;
		if (_positionCameraY != null)
			_positionCameraY.ValueChanged -= OnSpinBoxUpdated;
		if (_positionCameraZ != null)
			_positionCameraZ.ValueChanged -= OnSpinBoxUpdated;
		if (_positionTargetCameraX != null)
			_positionTargetCameraX.ValueChanged -= OnSpinBoxUpdated;
		if (_positionTargetCameraY != null)
			_positionTargetCameraY.ValueChanged -= OnSpinBoxUpdated;
		if (_positionTargetCameraZ != null)
			_positionTargetCameraZ.ValueChanged -= OnSpinBoxUpdated;
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
		CleanupSpinBoxEvents();
		CleanupNodes();
	}
}
#endif
