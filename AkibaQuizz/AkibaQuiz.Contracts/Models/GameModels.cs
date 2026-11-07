using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Models
{
    public sealed class GameModel
    {
        public long Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Author { get; set; } = string.Empty;
        public string? CreationDate { get; set; } = string.Empty;
    }

    public sealed class GameRoundModel
    {
        public long Id { get; set; }
        public long IdGame { get; set; }
        public int Position { get; set; }
    }

    public sealed class RoundQuestionModel
    {
        public long Id { get; set; }
        public long IdGameRound { get; set; }
        public long? IdQuestionAnswer { get; set; }
        public long? IdQCMQuestion { get; set; }
        public long? IdListQuestionsAnswers { get; set; }
        public long Position { get; set; }
    }
}
