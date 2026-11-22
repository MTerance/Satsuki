using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Models
{
    public sealed class QuestionLabelModel
    {
        public long Id { get; set; }
        public string Type { get; set; } = "";
        public string Question { get; set; } = "";

    }
}
