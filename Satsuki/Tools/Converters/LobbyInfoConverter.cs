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
                PositionCamera = resource.PositionCamera,
                RotationCamera = resource.RotationCamera,
                PositionTargetCamera = resource.PositionTargetCamera,
                CameraPlacement = CameraPlacementConverter.ConvertTo(resource.CameraPlacement),
                SpawnPoints = new Godot.Collections.Array<SpawnPointData>(resource.SpawnPoints)
            };
            return lobbyInfo;
        }

        public static LobbyInfoResource ConvertFrom(LobbyInfo lobbyInfo)
        {
            var resource = new LobbyInfoResource
            {
                PositionCamera = lobbyInfo.PositionCamera,
                RotationCamera = lobbyInfo.RotationCamera,
                PositionTargetCamera = lobbyInfo.PositionTargetCamera,
                CameraPlacement = CameraPlacementConverter.ConvertFrom(lobbyInfo.CameraPlacement),
                SpawnPoints = new List<SpawnPointData>(lobbyInfo.SpawnPoints)
            };
            return resource;
        }
    }
}
