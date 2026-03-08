using Godot;
using Satsuki.addons.decor_manager.Tools;
using System;


#if TOOLS
[Tool]
public partial class CameraPlacementTemplate : Control
{
    #region properties

	private string _idTemplateCamera;
    private string _typeTemplateCamera = "default";

    #region SpinBoxes definition
    private SpinBox _positionCameraX;
	private SpinBox _positionCameraY;
	private SpinBox _positionCameraZ;
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
	}

	public void InitCameraPlacementTemplate(string idTemplateCamera, string typeTemplateCamera, Vector3 nodeCameraPosition, Vector3 nodeTargetCameraPosition)
	{
		_idTemplateCamera = idTemplateCamera;
		_typeTemplateCamera = typeTemplateCamera;
		InitCameraPlacementTemplate();
		CreateCameraNode();
		CreateCameraTargetNode();
		SetNodeCameraPosition(nodeCameraPosition);
		SetNodeTargetCameraPosition(nodeTargetCameraPosition);
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
    }

    private void SetNodeTargetCameraPosition(Vector3 nodeTargetCameraPosition)
    {
        _nodeTargetCamera.Position = nodeTargetCameraPosition;
    }

    private void SetNodeCameraPosition(Vector3 nodeCameraPosition)
    {
        _nodeCamera.Position = nodeCameraPosition;
    }

    private void InitCameraPlacementTemplate()
	{
        _positionCameraX = FindChild("PositionCameraX") as SpinBox;
		_positionCameraY = FindChild("PositionCameraY") as SpinBox;
		_positionCameraZ = FindChild("PositionCameraZ") as SpinBox;
		_positionTargetCameraX = FindChild("PositionTargetCameraX") as SpinBox;
		_positionTargetCameraY = FindChild("PositionTargetCameraY") as SpinBox;
		_positionTargetCameraZ = FindChild("PositionTargetCameraZ") as SpinBox;
		
        _positionCameraX.ValueChanged += OnSpinBoxUpdated;
        _positionCameraY.ValueChanged += OnSpinBoxUpdated;
        _positionCameraZ.ValueChanged += OnSpinBoxUpdated;
        _positionTargetCameraX.ValueChanged += OnSpinBoxUpdated;
        _positionTargetCameraY.ValueChanged += OnSpinBoxUpdated;
        _positionTargetCameraZ.ValueChanged += OnSpinBoxUpdated;
    }

    private void OnSpinBoxUpdated(double value)
    {
        Vector3 newCameraPosition = new Vector3((float)_positionCameraX.Value, (float)_positionCameraY.Value, (float)_positionCameraZ.Value);
        Vector3 newTargetCameraPosition = new Vector3((float)_positionTargetCameraX.Value, (float)_positionTargetCameraY.Value, (float)_positionTargetCameraZ.Value);
        SetNodeCameraPosition(newCameraPosition);
        SetNodeTargetCameraPosition(newTargetCameraPosition);
    }


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