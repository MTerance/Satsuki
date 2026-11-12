using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace AkibaQuiz.Api.Admin
{
    public sealed class GameRoundEditorVm
    {
        public long? Id { get; set; }
        public int Position { get; set; }
        public int QuestionCount { get; set; }
    }


    public class GameEditorVm
    {
        public long? Id { get; set; }

        [Required]
        [MinLength(1, ErrorMessage = "Le nom est obligatoire.")]
        public string Name { get; set; }
        public List<GameRoundEditorVm> Rounds { get; set; } = [];
    }
}
