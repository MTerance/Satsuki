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
}
