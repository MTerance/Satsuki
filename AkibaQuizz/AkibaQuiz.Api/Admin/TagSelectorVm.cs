using System;
using System.Collections.Generic;
using System.Text;
using AkibaQuiz.Contracts.Models;

namespace AkibaQuiz.Api.Admin
{
    public sealed class TagSelectorVm
    {
        public IReadOnlyList<TagModel> AvailableTags { get; set; } = Array.Empty<TagModel>();
        public IReadOnlyCollection<long> SelectedIds { get; set; } = Array.Empty<long>();
        public string FieldName { get; set; } = "TagIds";
        public string SearchId { get; init; } = "akiba-text-search";
    }
}
