using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Models
{
    public sealed class TagModel
    {
        public long Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string? Color { get; set; }
    }

    public sealed class QuizMediaModel
    {
        public long Id { get; set; }
        public long IdMedia { get; set; }
        public string Filename { get; set; } = string.Empty;
        public long IdTypeMedia { get; set; }
        public string TypeMediaName { get; set; } = string.Empty;
        public string TypeDisplay { get; set; } = string.Empty;
    }

    public sealed class QcmPropositionModel
    {
        public long Id { get; set; }
        public long IdQCMAnswer { get; set; }
        public string Answer { get; set; } = string.Empty;
        public bool IsTrue { get; set; }
    }

    public sealed class QcmModel
    {
        public long Id { get; set; }
        public string Question { get; set; } = string.Empty;
        public DateTimeOffset CreationDate { get; set; }
        public DateTimeOffset LastUpdatedDate { get; set; }        
        public long IdCategory { get; set; }
        public string CategoryName { get; set; } = string.Empty;        
        public string Author { get; set; } = string.Empty;
        public List<QcmPropositionModel> Answers { get; set; } = [];
        public List<TagModel> Tags { get; set; } = [];
        public List <QuizMediaModel> Medias { get; set; } = [];
    }
}
