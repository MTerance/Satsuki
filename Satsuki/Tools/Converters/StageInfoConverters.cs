using Satsuki.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Tools.Converters
{
    public static class StageInfoConverter
    {
        public static StageInfo ConvertTo(StageInfoResource resource)
        {
            var stageInfo = new StageInfo
            {
                rectA = new Godot.Vector3(resource.rectA.Item1, resource.rectA.Item2, resource.rectA.Item3),
                rectB = new Godot.Vector3(resource.rectB.Item1, resource.rectB.Item2, resource.rectB.Item3),
                PositionTargetMainCamera = new Godot.Vector3(resource.PositionTargetMainCamera.Item1, resource.PositionTargetMainCamera.Item2, resource.PositionTargetMainCamera.Item3),
                PositionMainCamera = new Godot.Vector3(resource.PositionMainCamera.Item1, resource.PositionMainCamera.Item2, resource.PositionMainCamera.Item3)
            };
            return stageInfo;
        }

        public static StageInfoResource ConvertFrom(StageInfo stageInfo)
        {
            var resource = new StageInfoResource
            {
                rectA = Tuple.Create(stageInfo.rectA.X, stageInfo.rectA.Y, stageInfo.rectA.Z),
                rectB = Tuple.Create(stageInfo.rectB.X, stageInfo.rectB.Y, stageInfo.rectB.Z),
                PositionTargetMainCamera = Tuple.Create(stageInfo.PositionTargetMainCamera.X, stageInfo.PositionTargetMainCamera.Y, stageInfo.PositionTargetMainCamera.Z),
                PositionMainCamera = Tuple.Create(stageInfo.PositionMainCamera.X, stageInfo.PositionMainCamera.Y, stageInfo.PositionMainCamera.Z)
            };
            return resource;
        }
    }
}
