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
        MeshInstance3D _zone;


        public override void _Ready()
        {
            CreateZone();
        }

        public void SetupPlayerZone(Vector3 center, float size)
        {
            GD.Print("PlayerZone: SetupPlayerZone called with center=" + center + " size=" + size);

            if (_zone == null || !IsInstanceValid(_zone))
            {
                CreateZone();
            }
            // Met à jour la position et la taille de la zone
            this.Position = center;
            _zone.Position = new Vector3(0, 0.01f, 0);
            if (_zone.Mesh is QuadMesh quadMesh)
            {
                quadMesh.Size = new Vector2(size, size/2);
            }
        }

        private void CreateZone()
        {
            GD.Print("PlayerZone: CreateZone called");
            var existing = GetNodeOrNull<MeshInstance3D>("PlayerZone_Mesh");
            if (existing != null && IsInstanceValid(existing))
            {
                existing.QueueFree();
            }

            var meshInstance = new MeshInstance3D();
            meshInstance.Name = "PlayerZone_Mesh";
            var quad = new QuadMesh
            {
                Size = new Vector2(6f, 2f)
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
            AddChild(_zone);
        }

        public override void _ExitTree()
        {
            if (_zone != null && IsInstanceValid(_zone))
            {
                _zone.QueueFree();
                _zone = null;
            }
        }
    }
}
#endif
