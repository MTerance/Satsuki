using Godot;
using Microsoft.VisualBasic.FileIO;
using Satsuki.Models;
using System;

#if TOOLS
[Tool]
#endif
public partial class PlayerSpawnTemplate : Control
{

	private Button _deleteButton;
	private OptionButton _spawnPointTypeOption;
	private Label IdSpawnDataLabel;
	private Node3D _spawnPointNode;
	//
	private LineEdit _positionXLineEdit;
	private LineEdit _positionYLineEdit;
	private LineEdit _positionZLineEdit;

	private LineEdit _rotationXLineEdit;
	private LineEdit _rotationYLineEdit;
	private LineEdit _rotationZLineEdit;

	//
	Vector3 _lastPosition;
	Vector3 _lastRotation;

	private bool _isInitialized = false;

	[Signal]
	public delegate void onSpawnPointPositionChangedEventHandler(string nodeName, Vector3 newPosition,Vector3 newRotation);
	[Signal]
	public delegate void OnSpawnPointTypeChangedEventHandler(int index, int type);
	[Signal]
	public delegate void OnDeleteSpawnPointEventHandler(string nodeName);


	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		InitializeControls();
	}

	private void InitializeControls()
	{
		if (_isInitialized)
			return;
		_deleteButton = FindChild("DeleteButton") as Button;
		if (_deleteButton != null)
			_deleteButton.Pressed += OnDeleteButtonPressed;
		_spawnPointTypeOption = FindChild("SpawnPointTypeOption") as OptionButton;
		if (_spawnPointTypeOption != null)
			_spawnPointTypeOption.ItemSelected += OnSpawnPointTypeSelected;
		InitPositionAndRotationLineEdits();
		_lastPosition = new Vector3(0, 0, 0);
		_lastRotation = new Vector3(0, 0, 0);
		_isInitialized = true;
	}

	private void InitPositionAndRotationLineEdits()
	{
		_positionXLineEdit = FindChild("positionX") as LineEdit;
		_positionYLineEdit = FindChild("positionY") as LineEdit;
		_positionZLineEdit = FindChild("positionZ") as LineEdit;

		_rotationXLineEdit = FindChild("rotationX") as LineEdit;
		_rotationYLineEdit = FindChild("rotationY") as LineEdit;
		_rotationZLineEdit = FindChild("rotationZ") as LineEdit;
	}


	private void OnSpawnPointTypeSelected(long index)
	{
		var selectedText = _spawnPointTypeOption.GetItemText((int)index);

		SpawnPointType spawnPointType = (SpawnPointType)index;

		var id = int.Parse(IdSpawnDataLabel.Text);
		
		GD.Print($"SpawnPointType {IdSpawnDataLabel.Text } selected: {selectedText}");
		EmitSignal(SignalName.OnSpawnPointTypeChanged, int.Parse(IdSpawnDataLabel.Text), (int)spawnPointType);
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
		if (_spawnPointNode != null &&
			(_spawnPointNode.Position != _lastPosition ||
			_spawnPointNode.RotationDegrees != _lastRotation))
		{
			UpdateLastPositionAndRotation();
			SetLineEditsFromSpawnPointNode();
			GD.Print($"Spawn point {IdSpawnDataLabel.Text} position or rotation changed: Position={_spawnPointNode.Position}, Rotation={_spawnPointNode.RotationDegrees}");
			EmitSignal(SignalName.onSpawnPointPositionChanged,
				_spawnPointNode.Name, _spawnPointNode.Position, _spawnPointNode.RotationDegrees);
		}
	}



	private void UpdateLastPositionAndRotation()
	{
		_lastPosition = _spawnPointNode.Position;
		_lastRotation = _spawnPointNode.RotationDegrees;
	}

	private void SetLineEditsFromSpawnPointNode()
	{
		if (_spawnPointNode == null)
			return;
		if (_positionXLineEdit == null)
			return;
		_positionXLineEdit.Text = _spawnPointNode.Position.X.ToString();
		_positionYLineEdit.Text = _spawnPointNode.Position.Y.ToString();
		_positionZLineEdit.Text = _spawnPointNode.Position.Z.ToString();
		_rotationXLineEdit.Text = _spawnPointNode.RotationDegrees.X.ToString();
		_rotationYLineEdit.Text = _spawnPointNode.RotationDegrees.Y.ToString();
		_rotationZLineEdit.Text = _spawnPointNode.RotationDegrees.Z.ToString();
	}

	public void InitPlayerSpawnTemplate(SpawnPointData spawnPoint)
	{
		IdSpawnDataLabel = FindChild("IdSpawnPoint") as Label;
		IdSpawnDataLabel.Text = spawnPoint.Index.ToString();
		_deleteButton = FindChild("DeleteButton") as Button;
		_deleteButton.Pressed += OnDeleteButtonPressed;
		InitPositionAndRotationLineEdits();
	}

	public void SetSpawnPointNode(Node3D spawnPointNode)
	{
		_spawnPointNode = spawnPointNode;
		if (_spawnPointNode == null)
			return;
		UpdateLastPositionAndRotation();
		SetLineEditsFromSpawnPointNode();
	}

	private void DeleteSpawnPoint()
	{
		var parent = GetParent() as VBoxContainer;
		if (parent != null)
		{
			parent.RemoveChild(this);
			EmitSignal(SignalName.OnDeleteSpawnPoint, _spawnPointNode.Name);
			this.QueueFree();
		}
	}

	public void OnDeleteButtonPressed()
	{
		DeleteSpawnPoint();
	}

}
