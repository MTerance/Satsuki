using Godot;
using Satsuki.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static Godot.WebSocketPeer;

namespace Satsuki.Repositories.Loaders
{
    public class LocationLoader
    {
        public StageResource LoadStageRsc(int id)
        {
            StageResource stage = new StageResource();
            stage.Load(id);
            return stage;
        }

        public Node LoadStage(StageResource rsc)
        {
            var scene = GD.Load<PackedScene>(rsc.ScenePath);
            return scene.Instantiate<Node3D>();
        }

    }
}