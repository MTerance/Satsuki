using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Entities
{
    public sealed class CategoryEntity
    {
        public long Id { get; set; }
        public string Name { get; set; } = "";
    }

    public sealed class QuestionAnswerEntity
    {
        public long Id { get; set; }
        public string Question { get; set; } = "";
        public string Answer { get; set; } = "";
        public long IdCategory { get; set; }
        public string CreationDate { get; set; } = "";
        public string LastUpdateDate { get; set; } = "";
        public string Author { get; set; } = "";
    }

    public sealed class QcmQuestionEntity
    {
        public long Id { get; set; }
        public string Question { get; set; } = "";
        public string CreationDate { get; set; } = "";
        public string LastUpdatedTDate { get; set; } = "";
        public string Author { get; set; } = "";
        public long IdCategory { get; set; }
    }

    public sealed class QcmAnswerEntity
    {
        public long Id { get; set; }
        public string Answer { get; set; } = "";
    }

    public sealed class QcmQuizzEntity
    {
        public long Id { get; set; }
        public long IdQCMQuestion { get; set; }
        public long IdQCMAnswer { get; set; }
        public string IsTrue { get; set; } = "FALSE";
    }
}
