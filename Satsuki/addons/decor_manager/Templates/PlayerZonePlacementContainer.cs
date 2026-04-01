using Godot;
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
	#endregion

	public override void _Ready()
	{
		InitializeLineEdits();

		// Create and add PlayerZone node (its own _Ready will run after AddChild)
		if (PlayerZone == null)
		{
			PlayerZone = new PlayerZone();
			AddChild(PlayerZone);
			GD.Print("PlayerZonePlacementContainer: PlayerZone creee");
		}

		// Initialise avec des valeurs par defaut (modifiables)
		InitializePlayerZone(Vector3.Zero, 50.0f);

		// Connect lineedit change events to update the PlayerZone
		ConnectLineEditSignals();
	}

	/// <summary>
	/// Initialise la PlayerZone : configure centre, taille, et synchronise les LineEdits.
	/// </summary>
	public void InitializePlayerZone(Vector3 center, float size)
	{
		if (PlayerZone == null)
		{
			PlayerZone = new PlayerZone();
			AddChild(PlayerZone);
		}

		// Configure la zone (implémentation coté PlayerZoneNode3d)
		PlayerZone.SetupPlayerZone(center, size);

		// Positionne le node et remet la rotation à zéro si besoin
		PlayerZone.Position = center;
		PlayerZone.RotationDegrees = Vector3.Zero;

		// Met à jour l'UI avec les valeurs actuelles
		UpdateLineEditsFromPlayerZone();

		GD.Print($"PlayerZonePlacementContainer: PlayerZone initialisee (center: {center}, size: {size})");
	}

	/// <summary>
	/// Récupère les LineEdit depuis le .tscn (nom des nodes doit correspondre).
	/// </summary>
	private void InitializeLineEdits()
	{
		_zonePlayerPositionX = FindChild("ZonePlayerPositionX", true, false) as LineEdit;
		_zonePlayerPositionY = FindChild("ZonePlayerPositionY", true, false) as LineEdit;
		_zonePlayerPositionZ = FindChild("ZonePlayerPositionZ", true, false) as LineEdit;

		_zonePlayerRotationX = FindChild("ZonePlayerRotationX", true, false) as LineEdit;
		_zonePlayerRotationY = FindChild("ZonePlayerRotationY", true, false) as LineEdit;
		_zonePlayerRotationZ = FindChild("ZonePlayerRotationZ", true, false) as LineEdit;
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
		if (PlayerZone == null) return;

		try
		{
			float px = _zonePlayerPositionX != null ? float.Parse(_zonePlayerPositionX.Text) : PlayerZone.Position.X;
			float py = _zonePlayerPositionY != null ? float.Parse(_zonePlayerPositionY.Text) : PlayerZone.Position.Y;
			float pz = _zonePlayerPositionZ != null ? float.Parse(_zonePlayerPositionZ.Text) : PlayerZone.Position.Z;

			float rx = _zonePlayerRotationX != null ? float.Parse(_zonePlayerRotationX.Text) : PlayerZone.RotationDegrees.X;
			float ry = _zonePlayerRotationY != null ? float.Parse(_zonePlayerRotationY.Text) : PlayerZone.RotationDegrees.Y;
			float rz = _zonePlayerRotationZ != null ? float.Parse(_zonePlayerRotationZ.Text) : PlayerZone.RotationDegrees.Z;

			PlayerZone.Position = new Vector3(px, py, pz);
			PlayerZone.RotationDegrees = new Vector3(rx, ry, rz);

			// Si PlayerZone expose un update visuel, lancez-le
			//PlayerZone.UpdatePlayerZone();

			GD.Print($"PlayerZonePlacementContainer: PlayerZone mise a jour depuis UI - Pos({px},{py},{pz}) Rot({rx},{ry},{rz})");
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
