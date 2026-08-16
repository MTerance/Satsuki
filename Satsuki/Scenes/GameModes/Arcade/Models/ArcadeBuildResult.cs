using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Scenes.GameModes.Arcade.Models
{
    public class ArcadeBuildResult
    {
        public Node Stage { get; set; }
        public Dictionary<int, Node3D> Players { get; set; } = new ();
        public Vector3 GameCameraPosition { get; set; }
        public Vector3 GameCameraRotation { get; set; }
    }
}
