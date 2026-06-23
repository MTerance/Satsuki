using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models.Resources
{
    [GlobalClass]
    public partial class GameConfig : Resource
    {
        [Export]
        public StageResource Lobby { get; set; }
         
    }
}
