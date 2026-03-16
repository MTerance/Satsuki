using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
    [GlobalClass]
    public partial class LobbyInfo : Resource
    {
        [Export]
        public Godot.Vector3 PositionCamera { get; set; }
        [Export]
        public Godot.Vector3 RotationCamera { get; set; }
        [Export]
        public Godot.Vector3 PositionTargetCamera { get; set; }
        [Export]
        public CameraPlacement CameraPlacement { get; set; } = new CameraPlacement();
        [Export]
        public Godot.Collections.Array<SpawnPointData> SpawnPoints { get; set; }
        public LobbyInfo()
        {
            SpawnPoints = new Godot.Collections.Array<SpawnPointData>();
            PositionCamera = Vector3.Zero;
            RotationCamera = Vector3.Zero;
            PositionTargetCamera = Vector3.Zero;
        }
    }
}