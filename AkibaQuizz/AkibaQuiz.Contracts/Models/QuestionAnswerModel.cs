using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Models
{
    public sealed class QuestionAnswerModel
    {
        public long Id { get; set; }
        public string Question { get; set; } = string.Empty;
        public string Answer { get; set; } = string.Empty;
        public long IdCategory { get; set; }
        public string? CategoryName { get; set; }
        public string CreationDate { get; set; } = string.Empty;
        public string LastUpdateDate { get; set; } = string.Empty;
        public string Author { get; set; } = string.Empty;
        public List<TagModel> Tags { get; set; } = [];
        public List<QuizMediaModel> Medias { get; set; } = [];
    }
}
