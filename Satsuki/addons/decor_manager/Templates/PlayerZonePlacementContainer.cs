using Godot;
using Satsuki.addons.decor_manager;
using Satsuki.addons.decor_manager.Models;
using System;

#if TOOLS
[Tool]
public partial class PlayerZonePlacementContainer : PanelContainer
{
	#region nodes definition
	private PlayerZone PlayerZone { get; set; }
	#endregion

	#region PanelComponent definition

	private Vector3dTextBox _positionZonePlayerTextBox;
	private Vector3dTextBox _rotationZonePlayerTextBox;
	
	#endregion

	#region textbox definition
	private LineEdit _zonePlayerSize;
	#endregion

	public override void _Ready()
	{
		InitializeLineEdits();
		// Initialise avec des valeurs par defaut (modifiables)
		// Connect lineedit change events to update the PlayerZone
		ConnectLineEditSignals();
		InitializePlayerZone(Vector3.Zero, Vector3.Zero, 50.0f);
	}

	/// <summary>
	/// Initialise la PlayerZone : configure centre, taille, et synchronise les LineEdits.
	/// </summary>
	public void InitializePlayerZone(Vector3 center, Vector3 rotation, float size)
	{
		if (PlayerZone == null)
		{
			PlayerZone = new PlayerZone();
			PlayerZone.Name = "PlayerZone";
		}
		// Configure la zone (implémentation coté PlayerZoneNode3d)
		PlayerZone.SetupPlayerZone(center, size);
		_zonePlayerSize.Text = size.ToString("F2");

		// Positionne le node et applique la rotation
		PlayerZone.Position = center;
		PlayerZone.RotationDegrees = rotation;

		// Met à jour l'UI avec les valeurs actuelles
		SceneManager.Instance.AddNodeToScene(PlayerZone);
		GD.Print("PlayerZonePlacementContainer: PlayerZone creee");
		UpdateLineEditsFromPlayerZone();
		GD.Print($"PlayerZonePlacementContainer: PlayerZone initialisee (center: {center}, size: {size})");
		GD.Print($"PlayerZonePlacementContainer: PlayerZone size actuelle: {PlayerZone.GetZoneSize()}");
	}

	public void Load(Vector3 position, Vector3 rotation, float size)
	{
		PlayerZone.Position = position;
		PlayerZone.RotationDegrees = rotation;
		PlayerZone.SetZoneSize(size);
		UpdateLineEditsFromPlayerZone();
	}

	/// <summary>
	/// Récupère les LineEdit depuis le .tscn (nom des nodes doit correspondre).
	/// </summary>
	private void InitializeLineEdits()
	{
		_positionZonePlayerTextBox = FindChild("PositionZoneBox", true, false) as Vector3dTextBox;
		_rotationZonePlayerTextBox = FindChild("RotationZoneBox", true, false) as Vector3dTextBox;
		_zonePlayerSize = FindChild("SizeZonePlayer", true, false) as LineEdit;
		_positionZonePlayerTextBox.Setup("Position\n Zone Player", Vector3.Zero);
		_rotationZonePlayerTextBox.Setup("Rotation\n Zone Player", Vector3.Zero);
		checkIsLineEditValid(_zonePlayerSize);
	}

	private bool checkIsLineEditValid(LineEdit lineEdit)
	{
		if (lineEdit == null)
		{
			GD.PrintErr($"PlayerZonePlacementContainer: LineEdit introuvable { lineEdit }");
			return false;
		}
		GD.Print($"PlayerZonePlacementContainer: LineEdit trouve {lineEdit.Name}");
		return true;
	}

	/// <summary>
	/// Connecte les signaux TextChanged des LineEdit à l'update.
	/// </summary>
	private void ConnectLineEditSignals()
	{
		_positionZonePlayerTextBox.ValueChanged += _positionZonePlayerTextBox_ValueChanged;
		_rotationZonePlayerTextBox.ValueChanged += _rotationZonePlayerTextBox_ValueChanged;
		if (_zonePlayerSize != null) _zonePlayerSize.TextChanged += OnLineEditChanged;
	}

	private void _rotationZonePlayerTextBox_ValueChanged(object sender, EventArgs e)
	{
		PlayerZone.RotationDegrees = _rotationZonePlayerTextBox.GetValue();
	}

	private void _positionZonePlayerTextBox_ValueChanged(object sender, EventArgs e)
	{
		PlayerZone.Position = _positionZonePlayerTextBox.GetValue();
	}

	/// <summary>
	/// Déconnecte les signaux (appelé depuis _ExitTree si nécessaire).
	/// </summary>
	private void DisconnectLineEditSignals()
	{

		_positionZonePlayerTextBox.ValueChanged -= _positionZonePlayerTextBox_ValueChanged;
		_rotationZonePlayerTextBox.ValueChanged -= _rotationZonePlayerTextBox_ValueChanged;
		if (_zonePlayerSize != null) _zonePlayerSize.TextChanged -= OnLineEditChanged;
	}

	private void OnLineEditChanged(string _)
	{
		UpdatePlayerZoneFromInputs();
	}

	/// <summary>
	/// Lit les LineEdits et applique la position/rotation à PlayerZone.
	/// Les valeurs invalides sont ignorées et loggées.
	/// </summary>
	private void UpdatePlayerZoneFromInputs()
	{
		if (PlayerZone == null)
		{
			GD.PrintErr("PlayerZonePlacementContainer: PlayerZone est null, impossible de mettre a jour");
			return;
		}
		try
		{
			PlayerZone.Position = _positionZonePlayerTextBox.GetValue();
			PlayerZone.RotationDegrees = _rotationZonePlayerTextBox.GetValue();
			float size = _zonePlayerSize != null ? float.Parse(_zonePlayerSize.Text) : PlayerZone.GetZoneSize();
			GD.Print($"PlayerZonePlacementContainer: PlayerZone mise a jour depuis UI - Pos({PlayerZone.Position.X},{PlayerZone.Position.Y},{PlayerZone.Position.Z}) Rot({PlayerZone.RotationDegrees.X},{PlayerZone.RotationDegrees.Y},{PlayerZone.RotationDegrees.Z}) Size({size})");

			PlayerZone.SetZoneSize(size);

			// Si PlayerZone expose un update visuel, lancez-le
			//PlayerZone.UpdatePlayerZone();


			GD.Print($"PlayerZonePlacementContainer: PlayerZone size actuelle: {PlayerZone.GetZoneSize()}");
		}
		catch (FormatException)
		{
			GD.PrintErr("PlayerZonePlacementContainer: valeur invalide dans un LineEdit (parse float)");
		}
	}

	/// <summary>
	/// Remplit les LineEdits avec les valeurs actuelles de PlayerZone.
	/// </summary>
	private void UpdateLineEditsFromPlayerZone()
	{
		if (PlayerZone == null) return;
		if (_positionZonePlayerTextBox != null)
			_positionZonePlayerTextBox.SetValue(PlayerZone.Position);
		if (_rotationZonePlayerTextBox != null)
			_rotationZonePlayerTextBox.SetValue(PlayerZone.RotationDegrees);
		if (_zonePlayerSize != null)
			_zonePlayerSize.Text = PlayerZone.GetZoneSize().ToString("F2");

	}

	public Vector3 GetPlayerZonePosition()
	{
		return _positionZonePlayerTextBox != null ? _positionZonePlayerTextBox.GetValue() : Vector3.Zero;
	}

	public Vector3  GetPlayerZoneRotation()
	{
		return _rotationZonePlayerTextBox != null ? _rotationZonePlayerTextBox.GetValue() : Vector3.Zero;
	}

	public float GetPlayerZoneSize()
	{
		return _zonePlayerSize != null ? float.Parse(_zonePlayerSize.Text) : 15.0f;
	}

	public override void _ExitTree()
	{
		DisconnectLineEditSignals();
		if (PlayerZone != null)
		{
			RemoveChild(PlayerZone);
			PlayerZone.QueueFree();
			PlayerZone = null;
		}
		base._ExitTree();
	}
}
#endif
