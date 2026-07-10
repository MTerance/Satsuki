using Godot;
using Satsuki.addons.decor_manager.Tools;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
    [GlobalClass]
    public partial class CameraPlacement : Resource
    {
        [Export]
        public int Index;
        [Export]
        public string TypeTemplateCamera;
        [Export]
        public Vector3 Position;
        [Export]
        public Vector3 Rotation;
        [Export]
        public Vector3 Target;

        public CameraPlacement()
        {
            Index = Tool.GenerateStageId();
            TypeTemplateCamera = string.Empty;
            Position = Vector3.Zero;
            Rotation = Vector3.Zero;
            Target = Vector3.Zero;
        }

        public CameraPlacement(int index, string typeTemplateCamera, Vector3 position, Vector3 rotation, Vector3 target)
        {
            Index = index;
            TypeTemplateCamera = typeTemplateCamera;
            Position = position;
            Rotation = rotation;
            Target = target;
        }
    }

    public class CameraPlacementResource
    {
        public int Index { get; set; }
        public string TypeTemplateCamera { get; set; }
        public Tuple<float,float,float> Position { get; set; }
        public Tuple<float, float, float> Rotation { get; set; }
        public Tuple<float, float, float> Target { get; set; }
        public CameraPlacementResource()
        {
            Index = 0;
            TypeTemplateCamera = string.Empty;
            Position = Tuple.Create(0f, 0f, 0f);
            Rotation = Tuple.Create(0f, 0f, 0f);
            Target = Tuple.Create(0f, 0f, 0f);
        }
        public CameraPlacementResource(int index, string typeTemplateCamera, Vector3 position, Vector3 rotation, Vector3 target)
        {
            Index = index;
            TypeTemplateCamera = typeTemplateCamera;
            Position = Tuple.Create(position.X, position.Y, position.Z);
            Rotation = Tuple.Create(rotation.X, rotation.Y, rotation.Z);
            Target = Tuple.Create(target.X, target.Y, target.Z);
        }
    }
}
