using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Repositories.Loaders
{
    public class PlayerLoader
    {
        public Node3D LoadPlayerMesh()
        {
            var node = GD.Load<PackedScene>("res://Scenes/Characters/Character.tscn");
            return node.Instantiate<Node3D>();
        }
    }
}
