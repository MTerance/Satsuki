using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.addons.decor_manager.Tools
{
    public static class NodeBuilder
    {
        public static Sprite3D CreateSprite(string path, string nodeName, Vector3 scale, Vector3? position = null, Vector3? rotation = null)
        {
            Sprite3D sprite = new Sprite3D();
            sprite.Name = nodeName;
            sprite.Texture = GD.Load<Texture2D>(path);
            sprite.Scale = scale;
            sprite.Position = position ?? Vector3.Zero;
            sprite.RotationDegrees = rotation ?? Vector3.Zero;
            return sprite;
        }

        public static Label3D CreateLabel(string text, string nodeName, Vector3? position = null, Vector3? rotation = null, int fontSize = 24, bool noDepthTest = true)
        {
            Label3D label = new Label3D();
            label.Name = nodeName;
            label.Text = text;
            label.Position = position ?? Vector3.Zero;
            label.RotationDegrees = rotation ?? Vector3.Zero;
            label.FontSize = fontSize;
            label.NoDepthTest = noDepthTest;
            return label;
        }
    }
}
