using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Models
{
    public sealed class QuestionAnswerDto
    {
        public int Id { get; set; }
        public string Question { get; set; }
        public string Answer { get; set; }
        public int Points { get; set; } = 100; 
        public int TimeLimitSeconds { get; set; } = 30;
    }
}
