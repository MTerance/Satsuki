using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Models
{
    public sealed class QcmQuestionModel
    {
        public long Id { get; set; }
        public string Question { get; set; } = string.Empty;
        public string CreationDate { get; set; } = string.Empty;
        public string LastUpdatedDate { get; set; } = string.Empty;
        public long IdCategory { get; set; }
        public string Author { get; set; } = string.Empty;
    }

    public sealed class QcmAnswerModel
    {
        public long Id { get; set; }
        public string Answer { get; set; } = string.Empty;
    }

    public sealed class  QcmQuizzModel
    {
        public long Id { get; set; }
        public long IdQCMQuestion { get; set; }
        public long IdQCMAnswer { get; set; }
        public string IsTrue { get; set; } = string.Empty;

    }
}
