using System;
using System.Collections.Generic;
using System.Text;
using System.ComponentModel.DataAnnotations;

namespace AkibaQuiz.Contracts.Models
{
    /*
    public sealed class SaveQcmMediaRequest
    {
        public long IdMedia { get; set; }

        [Required]
        public string TypeDisplay { get; set; } = string.Empty;
    }

    public sealed class SaveQcmPropositionRequest
    {
        public long? IdQCMAnswer { get; set; }
        [Required]
        [MinLength(1)]
        public string Answer { get; set; } = string.Empty;
        public bool IsTrue { get; set; }
    }

    public sealed class SaveQcmRequest
    {
        [Required]
        [MinLength(3)]
        public string Question { get; set; } = string.Empty;

        [Range(1, long.MaxValue)]
        public long IdCategory { get; set; }

        public List<SaveQcmPropositionRequest> Answers { get; set; } = [];

        public List<long> TagIds { get; set; } = [];

        public List<SaveQcmMediaRequest> Medias { get; set; } = [];
    }
    */
}
