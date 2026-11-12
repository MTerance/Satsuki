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
        public List<long> TagsId { get; set; } = [];

        public IReadOnlyList<CategoryModel> Categories { get; set; } = [];
        public IReadOnlyList<TagModel> AvailablesTags { get; set; } = [];
        public IReadOnlyList<QuizMediaModel> ExistingMedia { get; set; } = [];

    }
}
