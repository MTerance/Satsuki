using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
    public struct OrderRequest
    {
        public string ClientId { get; set; }
        public string Target { get; set; }
        public string Order { get; set; }
        public string JsonData { get; set; }
    }
}
