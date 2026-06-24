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
        public Godot.Vector3  rectA { get; set; }
        [Export]
        public Godot.Vector3 rectB { get; set; }
        [Export]
        public Godot.Vector3 PositionTargetMainCamera { get; set; }
        [Export]
        public Godot.Vector3 PositionMainCamera { get; set; }

        public StageInfo()
        {
            rectA = Vector3.Zero;
            rectB = Vector3.Zero;
            PositionTargetMainCamera = Vector3.Zero;
            PositionMainCamera = Vector3.Zero;
        }
    }
}
