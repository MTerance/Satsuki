using System.Collections.Generic;
using Satsuki.Interfaces.Models;
using Satsuki.Interfaces.Quizz;
using Satsuki.Models;

namespace Satsuki.Scenes.GameModes.Arcade.Models
{
    public class ArcadeGameRecord : IGameRecord
    {
        public int Id { get; set; }
        public string GameInstanceName { get; set; }
        public string GameName { get; set; }
        public int IdStage { get; set; }
        public List<PlayerInfo> Players { get; set; }        
        public List<IQuizzModel> Quizzs { get; set; } = new List<IQuizzModel>();
    }
}
