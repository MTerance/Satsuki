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

	#region textbox definition
	private LineEdit _zonePlayerPositionX;
	private LineEdit _zonePlayerPositionY;
	private LineEdit _zonePlayerPositionZ;
	private LineEdit _zonePlayerRotationX;
	private LineEdit _zonePlayerRotationY;
	private LineEdit _zonePlayerRotationZ;
	private LineEdit _zonePlayerSize;
	#endregion

	public override void _Ready()
	{
		InitializeLineEdits();
		// Initialise avec des valeurs par defaut (modifiables)
		InitializePlayerZone(Vector3.Zero, Vector3.Zero, 50.0f);
		// Connect lineedit change events to update the PlayerZone
		ConnectLineEditSignals();
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

	/// <summary>
	/// Récupère les LineEdit depuis le .tscn (nom des nodes doit correspondre).
	/// </summary>
	private void InitializeLineEdits()
	{
		_zonePlayerPositionX = FindChild("ZonePositionX", true, false) as LineEdit;
		checkIsLineEditValid(_zonePlayerPositionX);
		_zonePlayerPositionY = FindChild("ZonePositionY", true, false) as LineEdit;
		checkIsLineEditValid(_zonePlayerPositionY);	
		_zonePlayerPositionZ = FindChild("ZonePositionZ", true, false) as LineEdit;
		checkIsLineEditValid(_zonePlayerPositionZ);

		_zonePlayerRotationX = FindChild("ZoneRotationX", true, false) as LineEdit;
		checkIsLineEditValid(_zonePlayerRotationX);
        _zonePlayerRotationY = FindChild("ZoneRotationY", true, false) as LineEdit;
        checkIsLineEditValid(_zonePlayerRotationY);
        _zonePlayerRotationZ = FindChild("ZoneRotationZ", true, false) as LineEdit;
        checkIsLineEditValid(_zonePlayerRotationZ);
        _zonePlayerSize = FindChild("SizeZonePlayer", true, false) as LineEdit;
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
		if (_zonePlayerPositionX != null) _zonePlayerPositionX.TextChanged += OnLineEditChanged;
		if (_zonePlayerPositionY != null) _zonePlayerPositionY.TextChanged += OnLineEditChanged;
		if (_zonePlayerPositionZ != null) _zonePlayerPositionZ.TextChanged += OnLineEditChanged;
		if (_zonePlayerRotationX != null) _zonePlayerRotationX.TextChanged += OnLineEditChanged;
		if (_zonePlayerRotationY != null) _zonePlayerRotationY.TextChanged += OnLineEditChanged;
		if (_zonePlayerRotationZ != null) _zonePlayerRotationZ.TextChanged += OnLineEditChanged;
		if (_zonePlayerSize != null) _zonePlayerSize.TextChanged += OnLineEditChanged;

	}

	/// <summary>
	/// Déconnecte les signaux (appelé depuis _ExitTree si nécessaire).
	/// </summary>
	private void DisconnectLineEditSignals()
	{
		if (_zonePlayerPositionX != null) _zonePlayerPositionX.TextChanged -= OnLineEditChanged;
		if (_zonePlayerPositionY != null) _zonePlayerPositionY.TextChanged -= OnLineEditChanged;
		if (_zonePlayerPositionZ != null) _zonePlayerPositionZ.TextChanged -= OnLineEditChanged;
		if (_zonePlayerRotationX != null) _zonePlayerRotationX.TextChanged -= OnLineEditChanged;
		if (_zonePlayerRotationY != null) _zonePlayerRotationY.TextChanged -= OnLineEditChanged;
		if (_zonePlayerRotationZ != null) _zonePlayerRotationZ.TextChanged -= OnLineEditChanged;
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
			GD.Print(" positon X =  " + _zonePlayerPositionX.Text);
			GD.Print(" positon Y =  " + _zonePlayerPositionY.Text);
			GD.Print(" positon Z =  " + _zonePlayerPositionZ.Text);
			GD.Print(" rotation X =  " + _zonePlayerRotationX.Text);
			GD.Print(" rotation Y =  " + _zonePlayerRotationY.Text);
			GD.Print(" rotation Z =  " + _zonePlayerRotationZ.Text);
			float px = float.Parse(_zonePlayerPositionX.Text);
			float py = float.Parse(_zonePlayerPositionY.Text);
			float pz = float.Parse(_zonePlayerPositionZ.Text);

			float rx = float.Parse(_zonePlayerRotationX.Text);
			float ry = float.Parse(_zonePlayerRotationY.Text);
			float rz = float.Parse(_zonePlayerRotationZ.Text);

			float size = _zonePlayerSize != null ? float.Parse(_zonePlayerSize.Text) : PlayerZone.GetZoneSize();
			GD.Print($"PlayerZonePlacementContainer: PlayerZone mise a jour depuis UI - Pos({px},{py},{pz}) Rot({rx},{ry},{rz}) Size({size})");
			PlayerZone.Position = new Vector3(px, py, pz);
			PlayerZone.RotationDegrees = new Vector3(rx, ry, rz);
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

		if (_zonePlayerPositionX != null) _zonePlayerPositionX.Text = PlayerZone.Position.X.ToString("F2");
		if (_zonePlayerPositionY != null) _zonePlayerPositionY.Text = PlayerZone.Position.Y.ToString("F2");
		if (_zonePlayerPositionZ != null) _zonePlayerPositionZ.Text = PlayerZone.Position.Z.ToString("F2");

		if (_zonePlayerRotationX != null) _zonePlayerRotationX.Text = PlayerZone.RotationDegrees.X.ToString("F2");
		if (_zonePlayerRotationY != null) _zonePlayerRotationY.Text = PlayerZone.RotationDegrees.Y.ToString("F2");
		if (_zonePlayerRotationZ != null) _zonePlayerRotationZ.Text = PlayerZone.RotationDegrees.Z.ToString("F2");
	}

	public Vector3 GetPlayerZonePosition()
	{
		return PlayerZone != null ? PlayerZone.Position : Vector3.Zero;
	}

	public Vector3  GetPlayerZoneRotation()
	{
		return PlayerZone != null ? PlayerZone.RotationDegrees : Vector3.Zero;
	}

	public float GetPlayerZoneSize()
	{
		return PlayerZone != null ? PlayerZone.GetZoneSize() : 0.0f;
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
