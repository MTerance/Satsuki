using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Models
{
    public sealed class GameSummaryDto
    {
        public long Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public int RoundCount { get; set; }
        public int QuestionCount { get; set; }
    }
}
