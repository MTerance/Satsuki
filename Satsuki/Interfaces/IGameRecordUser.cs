using Satsuki.Interfaces.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Interfaces
{
    public interface IGameRecordUser
    {
        IGameRecord LoadCurrentGameRecord();
        void SetGameRecord(IGameRecord gameRecord);
    }
}
