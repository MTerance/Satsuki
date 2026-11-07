using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace AkibaQuiz.Contracts.Requests
{
    public sealed class SaveQuestionAnswerRequest
    {
        [Required, MinLength(3)]
        public string Question { get; set; } = "";

        [Required, MinLength(1)]
        public string Answer { get; set; } = "";

        [Range(1, long.MaxValue)]
        public long IdCategory { get; set; }

        public List<long> TagIds { get; set; } = [];
        public List<SaveMediaAssociationRequest> Medias { get; set; } = [];
    }

    public sealed class SaveQcmRequest
    {
        [Required, MinLength(3)]
        public string Question { get; set; } = "";

        [Range(1, long.MaxValue)]
        public long IdCategory { get; set; }

        public List<SaveQcmPropositionRequest> Answers { get; set; } = [];

        public List<long> TagIds { get; set; } = [];
        public List<SaveMediaAssociationRequest> Medias { get; set; } = [];
    }

    public sealed class SaveQcmPropositionRequest
    {
        [Required, MinLength(1)]
        public string Answer { get; set; } = "";

        public bool IsTrue { get; set; }
    }

    public sealed class SaveMediaAssociationRequest
    {
        [Range(1, long.MaxValue)]
        public long IdMedia { get; set; }

        [Required]
        public string TypeDisplay { get; set; } = "";
    }

    public sealed class SaveGameRequest
    {
        [Required, MinLength(2)]
        public string Name { get; set; } = "";

        public List<SaveGameRoundRequest> Rounds { get; set; } = [];
    }

    public sealed class SaveGameRoundRequest
    {
        public long Position { get; set; }

        public List<SaveRoundQuestionRequest> Questions { get; set; } = [];
    }

    public sealed class SaveRoundQuestionRequest
    {
        public long Position { get; set; }

        public long? IdQuestionAnswer { get; set; }
        public long? IdQCMQuestion { get; set; }
        public long? IdListQuestionsAnswers { get; set; }
    }
}
