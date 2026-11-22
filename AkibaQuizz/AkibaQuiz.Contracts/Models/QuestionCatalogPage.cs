using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Models
{
    public sealed class QuestionCatalogItem
    {
        public long Id { get; set; }

        public string Type { get; set; } = "";

        public string Question { get; set; } = "";

        public long IdCategory { get; set; }

        public string CategoryName { get; set; } = "";

        public int AnswerCount { get; set; }
    }

    public sealed class QuestionCatalogPage
    {
        public List<QuestionCatalogItem> Items { get; set; } = [];

        public long TotalCount { get; set; }

        public int Page { get; set; }

        public int PageSize { get; set; }

        public long TotalPages =>
            PageSize <= 0
                ? 0
                : (TotalCount + PageSize - 1) / PageSize;
    }
}
