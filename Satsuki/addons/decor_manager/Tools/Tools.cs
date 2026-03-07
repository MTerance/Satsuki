using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.addons.decor_manager.Tools
{
    public static class Tool
    {
        public static int GenerateStageId()
        {
            return (int)(DateTime.UtcNow.Ticks % int.MaxValue);
        }
    }
}
