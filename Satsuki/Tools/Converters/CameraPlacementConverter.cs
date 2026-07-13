using Satsuki.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Tools.Converters
{
    public static class CameraPlacementConverter
    {

        public static CameraPlacement ConvertTo(CameraPlacementResource resource)
        {
            return new CameraPlacement(
                resource.Index,
                resource.TypeTemplateCamera,
                new Godot.Vector3(
                    resource.Position.Item1,
                    resource.Position.Item2,
                    resource.Position.Item3),
                new Godot.Vector3(
                    resource.Rotation.Item1,
                    resource.Rotation.Item2,
                    resource.Rotation.Item3),
                new Godot.Vector3(
                    resource.Target.Item1,
                    resource.Target.Item2,
                    resource.Target.Item3));
        }

        public static CameraPlacementResource ConvertFrom(CameraPlacement placement)
        {
            var resource = new CameraPlacementResource
            {
                Index = placement.Index,
                TypeTemplateCamera = placement.TypeTemplateCamera,
                Position = Tuple.Create(placement.Position.X, placement.Position.Y, placement.Position.Z),
                Rotation = Tuple.Create(placement.Rotation.X, placement.Rotation.Y, placement.Rotation.Z),
                Target = Tuple.Create(placement.Target.X, placement.Target.Y, placement.Target.Z)
            };
            return resource;
        }
    }
}
