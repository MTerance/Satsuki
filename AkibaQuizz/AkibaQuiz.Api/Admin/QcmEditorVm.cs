using AkibaQuiz.Contracts.Models;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace AkibaQuiz.Api.Admin
{
    public sealed class  QcmAnswerEditorVm
    {
        public string Answer { get; set; }
        public bool IsTrue { get; set; }
    }


    public sealed class QcmEditorVm
    {
        public long? Id { get; set; }

        [MinLength(1, ErrorMessage = "La question est obligatoire.")]
        public string Question { get; set; } = "";
        public List<QcmAnswerEditorVm> Answers { get; set; } = new();
        [Range(1, long.MaxValue, ErrorMessage = "La catégorie est obligatoire.")]
        public long IdCategory { get; set; }
        public List<long> TagIds { get; set; } = [];
        public IReadOnlyList<CategoryModel> Categories { get; set; } = [];
        public IReadOnlyList<TagModel> AvailablesTags { get; set; } = [];
        public IReadOnlyList<QuizMediaModel> ExistingMedias { get; set; } = [];
    }
}
