using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
    [GlobalClass]
    public partial class StageInfo : Resource
    {
        [Export]
        public Godot.Vector3 rectA { get; set; }
        [Export]
        public Godot.Vector3 rectB { get; set; }
        [Export]
        public Godot.Vector3 PositionZonePlayer { get; set; }
        [Export]
        public Godot.Vector3 RotationZonePlayer { get; set; }
        [Export]
        public float SizeZonePlayer { get; set; }
        [Export]
        public Godot.Vector3 PositionTargetMainCamera { get; set; }
        [Export]
        public Godot.Vector3 PositionMainCamera { get; set; }
        [Export]
        public CameraPlacement CameraPlacement { get; set; } = new CameraPlacement();


        public StageInfo()
        {
            rectA = Vector3.Zero;
            rectB = Vector3.Zero;
            PositionZonePlayer = Vector3.Zero;
            RotationZonePlayer = Vector3.Zero;
            SizeZonePlayer = 50f;
            PositionTargetMainCamera = Vector3.Zero;
            PositionMainCamera = Vector3.Zero;
        }
    }

    public class StageInfoResource
    {
        public Tuple<float, float, float> rectA { get; set; }
        public Tuple<float, float, float> rectB { get; set; }
        public Tuple<float, float, float> PositionZonePlayer { get; set; }
        public Tuple<float, float, float> RotationZonePlayer { get; set; }
        public float SizeZonePlayer { get; set; }
        public Tuple<float, float, float> PositionTargetMainCamera { get; set; }
        public Tuple<float, float, float> PositionMainCamera { get; set; }
        public CameraPlacementResource CameraPlacement { get; set; } = new CameraPlacementResource();

        public StageInfoResource()
        {
            rectA = Tuple.Create(0f, 0f, 0f);
            rectB = Tuple.Create(0f, 0f, 0f);
            PositionZonePlayer = Tuple.Create(0f, 0f, 0f);
            RotationZonePlayer = Tuple.Create(0f, 0f, 0f);
            SizeZonePlayer = 50f;
            PositionTargetMainCamera = Tuple.Create(0f, 0f, 0f);
            PositionMainCamera = Tuple.Create(0f, 0f, 0f);
        }
    }
}
