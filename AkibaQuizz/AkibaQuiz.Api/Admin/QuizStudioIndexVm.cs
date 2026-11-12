using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Admin
{
    public sealed class QuizStudioIndexVm
    {
        public List<QuestionRowVm> Questions { get; set; } = new();

        public List<QcmRowVm> Qcms { get; set; } = new();

        public List<GameRowVm> Games { get; set; } = new();
    }

    public sealed class QuestionRowVm
    {
        public long Id { get; set; }
        public string Question { get; set; } = "";
        public string Category { get; set; } = "";
    }

    public sealed class QcmRowVm
    {
        public long Id { get; set; }
        public string Question { get; set; } = "";
        public int AnswerCount { get; set; }
    }

    public sealed class GameRowVm
    {
        public long Id { get; set; }
        public string Name { get; set; } = "";
        public int RoundCount { get; set; }
        public int QuestionCount { get; set; }
    }
}
