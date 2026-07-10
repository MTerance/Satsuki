using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
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

    public class LobbyInfoResource
    {
        public Tuple<float, float, float> PositionCamera { get; set; }
        public Tuple<float, float, float> RotationCamera { get; set; }
        public Tuple<float, float, float> PositionTargetCamera { get; set; }
        public CameraPlacementResource CameraPlacement { get; set; } = new CameraPlacementResource();
        public List<SpawnPointData> SpawnPoints { get; set; }
        public LobbyInfoResource()
        {
            SpawnPoints = new List<SpawnPointData>();
            PositionCamera = Tuple.Create(0f, 0f, 0f);
            RotationCamera = Tuple.Create(0f, 0f, 0f);
            PositionTargetCamera = Tuple.Create(0f, 0f, 0f);
        }
    }
}