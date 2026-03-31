using Godot;
using System;

#if TOOLS
[Tool]
public partial class PlayerZoneNode3d : Node3D
{
	[Export]
	public Vector3 Center { get; private set; } = new Vector3(0, 1, 0);

	[Export]
	public float Size { get; private set; } = 10.0f;

	[Export]
	public Color ZoneColor { get; set; } = new Color(0, 1, 0, 0.25f);

	private MeshInstance3D _meshInstance;

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		EnsureMeshInstance();
		UpdateVisual();
		GD.Print("PlayerZoneNode3D ready");
	}

	public override void _Process(double delta)
	{
		// Optionnel: logique runtime
	}

	private void EnsureMeshInstance()
	{
		if (_meshInstance != null && IsInstanceValid(_meshInstance))
			return;

		_meshInstance = GetNodeOrNull<MeshInstance3D>("PlayerZone_MeshInstance");
		if (_meshInstance == null)
		{
			_meshInstance = new MeshInstance3D { Name = "PlayerZone_MeshInstance" };
			AddChild(_meshInstance);
		}
	}

	private BoxMesh CreateBoxMesh(float size)
	{
		var box = new BoxMesh();
		// width = size, depth = size, height = thin
		box.Size = new Vector3(size, Math.Max(0.1f, size * 0.05f), size);
		return box;
	}

	private StandardMaterial3D CreateMaterial(Color color)
	{
		var mat = new StandardMaterial3D();
		mat.AlbedoColor = color;
		mat.AlbedoTexture = null;
		mat.Set("flags_transparent", true); // sécurité pour certaines versions
		return mat;
	}

	/// <summary>
	/// Configure le centre et la taille de la zone.
	/// </summary>
	public void SetupPlayerZone(Vector3 center, float size)
	{
		Center = center;
		Size = Math.Max(0.01f, size);
		EnsureMeshInstance();
		UpdateVisual();
	}

	/// <summary>
	/// Crée/Met à jour le mesh visible (Box) en fonction de Size et ZoneColor.
	/// </summary>
	public void SetupBoxMesh()
	{
		EnsureMeshInstance();
		_meshInstance.Mesh = CreateBoxMesh(Size);
		_meshInstance.MaterialOverride = CreateMaterial(ZoneColor);
		_meshInstance.Position = Vector3.Zero;
		_meshInstance.RotationDegrees = Vector3.Zero;
	}

	/// <summary>
	/// Appelé lorsqu'on veut forcer la mise à jour visuelle.
	/// </summary>
	public void UpdatePlayerZone()
	{
		EnsureMeshInstance();
		SetupBoxMesh();
		// Positionner le node au centre défini
		this.Position = Center;
	}

	private void UpdateVisual()
	{
		EnsureMeshInstance();
		_meshInstance.Mesh = CreateBoxMesh(Size);
		_meshInstance.MaterialOverride = CreateMaterial(ZoneColor);
		this.Position = Center;
		_meshInstance.Position = Vector3.Zero;
	}
}
#endif