using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Satsuki.Interfaces.Models;
using Satsuki.Interfaces.Quizz;

namespace Satsuki.Models
{
    public class GameRecord : IGameRecord
    {
        public GameRecord() { }        
        public int Id { get; set; }
        public string GameInstanceName { get; set; }
        public int IdStage { get; set;  }
        public List<PlayerInfo> Players { get; set; }
        public List<IQuizzModel> Quizzs { get; set; } = new List<IQuizzModel>();
    }
}
