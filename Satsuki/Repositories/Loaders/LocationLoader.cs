using Godot;
using Satsuki.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Repositories.Loaders
{
    public class LocationLoader
    {
        public Node LoadStage(int id)
        {
            StageResource stage = new StageResource();
            stage.Load(id);
            var scene = GD.Load<PackedScene>(stage.ScenePath);
            return scene.Instantiate<Node3D>();
        }


    }
}
