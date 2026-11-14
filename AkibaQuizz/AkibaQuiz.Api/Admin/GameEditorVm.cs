using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace AkibaQuiz.Api.Admin
{

    public sealed class GameQuestionBankItemVm
    {
        public long Id { get; set; }
        public string TypeQuestion { get; set; } = "";
        public string Label { get; set; } = "";
    }

    public sealed class GameQuestionEditorVm
    {
        public long Id { get; set; }
        public long Position { get; set; }
        public string TypeQuestion { get; set; } = "";
        public long? QuestionId { get; set; }
        public long? QcmQuestionId { get; set; }
        public string Label { get; set; } = "";
    }

    public sealed class GameRoundEditorVm
    {
        public long? Id { get; set; }
        public int Position { get; set; }
        public int QuestionCount { get; set; }
        public List<GameQuestionEditorVm> Questions { get; set; } = [];
    }


    public sealed class GameEditorVm
    {
        public long? Id { get; set; }
        [Required]
        [MinLength(1, ErrorMessage = "Le nom est obligatoire.")]
        public string Name { get; set; } = "";
        public List<GameRoundEditorVm> Rounds { get; set; } = [];
        public List<GameQuestionBankItemVm> QuestionBank { get; set; } = [];
    }
}
