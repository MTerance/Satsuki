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
            return new CameraPlacement(resource.Index, resource.TypeTemplateCamera, resource.Position, resource.Rotation, resource.Target);
        }

        public static CameraPlacementResource ConvertFrom(CameraPlacement placement)
        {
            return new CameraPlacementResource(placement.Index, placement.TypeTemplateCamera, placement.Position, placement.Rotation, placement.Target);
        }
    }
}
