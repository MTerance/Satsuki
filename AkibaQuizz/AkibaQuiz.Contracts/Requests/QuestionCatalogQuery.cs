using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Requests
{
    public sealed class QuestionCatalogQuery
    {
        public string? Text { get; set; }

        // All, QuestionAnswer ou QCM
        public string Kind { get; set; } = "All";

        public long? CategoryId { get; set; }

        public long? TagId { get; set; }

        public int Page { get; set; } = 1;

        public int PageSize { get; set; } = 25;
    }
}
