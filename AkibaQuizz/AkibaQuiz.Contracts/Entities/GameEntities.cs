using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Entities
{
    public sealed class GameEntity
    {
        public long Id { get; set; }
        public string Name { get; set; } = "";
        public string Author { get; set; } = "";
        public string? CreationDate { get; set; }
    }

    public sealed class GameRoundEntity
    {
        public long Id { get; set; }
        public long Position { get; set; }
        public long IdGame { get; set; }
    }

    public sealed class RoundQuestionEntity
    {
        public long Id { get; set; }
        public long Position { get; set; }
        public long IdGameRound { get; set; }

        public long? IdQuestionAnswer { get; set; }
        public long? IdQCMQuestion { get; set; }
        public long? IdListQuestionsAnswers { get; set; }
    }

    public sealed class GameModeEntity
    {
        public long Id { get; set; }
        public string Name { get; set; } = "";
        public string Tag { get; set; } = "";
        public string DateCreation { get; set; } = "";
        public string DateUpdated { get; set; } = "";
        public string Author { get; set; } = "";
    }
}