using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
    public class PlayerInfo
    {
        public int Id { get; set;  }
        public string Name { get; set; }
        public Tuple<int,int,int> RGBColor { get; set; }
    }
}