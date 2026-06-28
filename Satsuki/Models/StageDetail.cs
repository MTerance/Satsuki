using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
    [GlobalClass]
    public partial class StageDetail : Resource
    {
        [Export]
        public int Id { get; set; }
        [Export]
        public string Name { get; set; }
        [Export]
        public bool hasLobbyInformation { get; set; }
        [Export]
        public bool hasStageInformation { get; set; }

        public StageDetail()
        {
            Id = 0;
            Name = string.Empty;
            hasLobbyInformation = false;
            hasStageInformation = false;
        }
    }
}
