using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{

    public class DecorConfiguration
    {
        public string ScenePath { get; set; }
        public string SceneName { get; set; }
        public List<SpawnPointData> SpawnPoints { get; set; }
        public List<MenuRenderSurfaceData> MenuRenderSurfaces { get; set; }
        public DateTime SavedAt { get; set; }
    }
}
