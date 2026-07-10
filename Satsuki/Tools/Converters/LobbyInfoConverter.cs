using Satsuki.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Tools.Converters
{
    public static class LobbyInfoConverter
    {
        public static LobbyInfo ConvertTo(LobbyInfoResource resource)
        {
            var lobbyInfo = new LobbyInfo
            {
                PositionCamera = new Godot.Vector3(resource.PositionCamera.Item1, resource.PositionCamera.Item2, resource.PositionCamera.Item3),
                RotationCamera = new Godot.Vector3(resource.RotationCamera.Item1, resource.RotationCamera.Item2, resource.RotationCamera.Item3),
                PositionTargetCamera = new Godot.Vector3(resource.PositionTargetCamera.Item1, resource.PositionTargetCamera.Item2, resource.PositionTargetCamera.Item3),
                CameraPlacement = CameraPlacementConverter.ConvertTo(resource.CameraPlacement),
                SpawnPoints = new Godot.Collections.Array<SpawnPointData>(resource.SpawnPoints)
            };
            return lobbyInfo;
        }

        public static LobbyInfoResource ConvertFrom(LobbyInfo lobbyInfo)
        {
            var resource = new LobbyInfoResource
            {
                PositionCamera = Tuple.Create(lobbyInfo.PositionCamera.X, lobbyInfo.PositionCamera.Y, lobbyInfo.PositionCamera.Z),
                RotationCamera = Tuple.Create(lobbyInfo.RotationCamera.X, lobbyInfo.RotationCamera.Y, lobbyInfo.RotationCamera.Z),
                PositionTargetCamera = Tuple.Create(lobbyInfo.PositionTargetCamera.X, lobbyInfo.PositionTargetCamera.Y, lobbyInfo.PositionTargetCamera.Z),
                CameraPlacement = CameraPlacementConverter.ConvertFrom(lobbyInfo.CameraPlacement),
                SpawnPoints = new List<SpawnPointData>(lobbyInfo.SpawnPoints)
            };
            return resource;
        }
    }
}
