using Satsuki.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Tools.Converters
{
    public static class SpawnPointDataConverter
    {
        public static SpawnPointData ConvertTo(SpawnPointDataResource resource)
        {
            return new SpawnPointData(
                resource.Index,
                new Godot.Vector3(
                    resource.Position.Item1,
                    resource.Position.Item2,
                    resource.Position.Item3),
                new Godot.Vector3(
                    resource.Rotation.Item1,
                    resource.Rotation.Item2,
                    resource.Rotation.Item3),
                resource.Type);
        }

        public static SpawnPointDataResource ConvertFrom(SpawnPointData data)
        {
            var resource = new SpawnPointDataResource
            {
                Index = data.Index,
                Position = Tuple.Create(data.Position.X, data.Position.Y, data.Position.Z),
                Rotation = Tuple.Create(data.Rotation.X, data.Rotation.Y, data.Rotation.Z),
                Type = data.Type
            };
            return resource;
        }
    }
}
