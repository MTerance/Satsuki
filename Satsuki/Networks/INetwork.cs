using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Networks
{
    public interface INetwork
    {
        bool Start();
        bool Stop();
       // Task<bool> SendMessage(string message);
       // event Action<string, object> OnMessage;

    }
}
