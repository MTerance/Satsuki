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
        public Node LoadPlayerMesh()
        {
            var node = GD.Load<PackedScene>("res://Assets/Models/Player/Player.tscn");
            return node.Instantiate<Node3D>();
        }
    }
}
