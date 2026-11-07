using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Infrastructure.Entities
{
    public sealed class QcmQuestionEntity
    {
        public long Id { get; set; }
        public string Question { get; set; }
        public string CreationDate { get; set; }
        public string LastUpdatedDate { get; set; }
        public string Author { get; set; }
        public long IdCategory { get; set; }
    }

    public sealed class QcmAnswerEntity
    {
        public long Id { get; set; }
        public string Answer { get; set; }
    }

    public sealed class  QcmQuizzEntity
    {
        public long Id { get; set; }
        public long IdQCMQuestion { get; set; }
        public long IdQCMAnswer { get; set; }

    }
}
