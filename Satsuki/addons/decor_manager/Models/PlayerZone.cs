using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.addons.decor_manager.Models
{
    public partial class PlayerZone : Node3D
    {
        MeshInstance3D _zone;


        public override void _Ready()
        {
            CreateZone();
        }


        private void CreateZone()
        {
            var meshInstance = new MeshInstance3D();

            var quad = new QuadMesh
            {
                Size = new Vector2(6, 2)
            };

            meshInstance.Mesh = quad;
            meshInstance.RotationDegrees = new Vector3(-90, 0, 0);
            meshInstance.Position = new Vector3(0, 0.01f, 0);

            var material = new StandardMaterial3D
            {
                AlbedoColor = new Color(1, 0, 0, 0.5f),
            };
            meshInstance.MaterialOverride = material;
            _zone = meshInstance;
            AddChild(_zone);
        }
    }
}
