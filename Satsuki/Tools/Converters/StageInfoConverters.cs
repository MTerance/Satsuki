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
                rectA = resource.rectA,
                rectB = resource.rectB,
                PositionTargetMainCamera = resource.PositionTargetMainCamera,
                PositionMainCamera = resource.PositionMainCamera
            };
            return stageInfo;
        }

        public static StageInfoResource ConvertFrom(StageInfo stageInfo)
        {
            var resource = new StageInfoResource
            {
                rectA = stageInfo.rectA,
                rectB = stageInfo.rectB,
                PositionTargetMainCamera = stageInfo.PositionTargetMainCamera,
                PositionMainCamera = stageInfo.PositionMainCamera
            };
            return resource;
        }
    }
}
