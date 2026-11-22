using AkibaQuiz.Contracts.Models;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Admin
{
    public sealed class QuestionEditorVm
    {
        public long? Id { get; set; }
        public string Question { get; set; } = "";
        public string Answer { get; set; } = "";
        public long IdCategory { get; set; }
        public List<long> TagsIds { get; set; } = new List<long>();

        public IReadOnlyList<CategoryModel> Categories { get; set; } = new List<CategoryModel>();
        public IReadOnlyList<TagModel> AvailablesTags { get; set; } = new List<TagModel>();
        public IReadOnlyList<QuizMediaModel> ExistingMedia { get; set; } = new List<QuizMediaModel>();

        public string? MediaAssociationsJson { get; set; }

    }
}
