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
                PositionTargetMainCamera = new Godot.Vector3(resource.PositionTargetMainCamera.Item1, resource.PositionTargetMainCamera.Item2, resource.PositionTargetMainCamera.Item3),
                PositionMainCamera = new Godot.Vector3(resource.PositionMainCamera.Item1, resource.PositionMainCamera.Item2, resource.PositionMainCamera.Item3),
                CameraPlacement = resource.CameraPlacement != null ? CameraPlacementConverter.ConvertTo(resource.CameraPlacement) : null,
                PositionZonePlayer = resource.PositionZonePlayer != null ? new Godot.Vector3(resource.PositionZonePlayer.Item1, resource.PositionZonePlayer.Item2, resource.PositionZonePlayer.Item3) : Godot.Vector3.Zero,
                RotationZonePlayer = resource.RotationZonePlayer != null ? new Godot.Vector3(resource.RotationZonePlayer.Item1, resource.RotationZonePlayer.Item2, resource.RotationZonePlayer.Item3) : Godot.Vector3.Zero,
                SizeZonePlayer = resource.SizeZonePlayer != 0.0f ? resource.SizeZonePlayer : 15.0f
            };
            return stageInfo;
        }

        public static StageInfoResource ConvertFrom(StageInfo stageInfo)
        {
            var resource = new StageInfoResource
            {
                PositionTargetMainCamera = Tuple.Create(stageInfo.PositionTargetMainCamera.X, stageInfo.PositionTargetMainCamera.Y, stageInfo.PositionTargetMainCamera.Z),
                PositionMainCamera = Tuple.Create(stageInfo.PositionMainCamera.X, stageInfo.PositionMainCamera.Y, stageInfo.PositionMainCamera.Z),
                CameraPlacement = stageInfo.CameraPlacement != null ? CameraPlacementConverter.ConvertFrom(stageInfo.CameraPlacement) : null,
                PositionZonePlayer = Tuple.Create(stageInfo.PositionZonePlayer.X, stageInfo.PositionZonePlayer.Y, stageInfo.PositionZonePlayer.Z),
                RotationZonePlayer = Tuple.Create(stageInfo.RotationZonePlayer.X, stageInfo.RotationZonePlayer.Y, stageInfo.RotationZonePlayer.Z),
                SizeZonePlayer = stageInfo.SizeZonePlayer
            };
            return resource;
        }
    }
}
