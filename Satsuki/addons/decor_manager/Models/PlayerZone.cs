using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

#if TOOLS
namespace Satsuki.addons.decor_manager.Models
{
	[Tool]
	public partial class PlayerZone : Node3D
	{

		private MeshInstance3D _zone;
		public override void _Ready()
		{
			
		}

		public void SetupPlayerZone(Vector3 center, float size)
		{
			GD.Print("PlayerZone: SetupPlayerZone called with center=" + center + " size=" + size);
			CreateZone(center, size);
			// Met à jour la position et la taille de la zone
			this.Position = center;
			_zone.Position = new Vector3(0, 0.01f, 0);
		}

		public void SetZoneSize(float size)
		{
			if (_zone != null && IsInstanceValid(_zone))
			{
				var quadMesh = _zone.Mesh as QuadMesh;
				if (quadMesh != null)
				{
					quadMesh.Size = new Vector2(size, size / 2);
				}
			}
		}

		public float GetZoneSize()
		{
			if (_zone != null && IsInstanceValid(_zone))
			{
				var quadMesh = _zone.Mesh as QuadMesh;
				if (quadMesh != null)
				{
					return quadMesh.Size.X; // Assuming the size is uniform, return the X size
				}
			}
			return 0f; // Return 0 if the zone or mesh is not valid
		}

		private void CreateZone(Vector3 center, float size)
		{
			GD.Print("PlayerZone: CreateZone called");
			var existing = GetNodeOrNull<MeshInstance3D>($"PlayerZone_Mesh");
			if (existing != null && IsInstanceValid(existing))
			{
				GD.Print("PlayerZone: Removing existing zone mesh");
				//SceneManager.Instance.RemoveNodeFromScene(existing);
				//RemoveChild(existing);
				//existing.QueueFree();
			}

			var meshInstance = new MeshInstance3D();
			meshInstance.Name = $"PlayerZone_Mesh";
			var quad = new QuadMesh
			{
				Size = new Vector2(size, size / 2)
			};

			meshInstance.Mesh = quad;
			meshInstance.RotationDegrees = new Vector3(-90, 0, 0);
			meshInstance.Position = new Vector3(0, 0.01f, 0);

			var material = new StandardMaterial3D
			{
				AlbedoColor = new Color(0.5f, 0.5f, 1, 0.7f),
				Transparency = BaseMaterial3D.TransparencyEnum.Alpha,
				ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
				CullMode = BaseMaterial3D.CullModeEnum.Disabled
			};
			meshInstance.MaterialOverride = material;
			meshInstance.Visible = true;
			_zone = meshInstance;
			_zone.Name = "PlayerZoneForMainScene";
			AddChild(_zone);
			if (Owner != null)
			{
				_zone.Owner = Owner;
			}
		}

		public override void _ExitTree()
		{
			if (_zone != null && IsInstanceValid(_zone) && IsAncestorOf(_zone))
			{
				RemoveChild(_zone);
				_zone.QueueFree();
				_zone = null;
			}
		}
	}
}
#endif
