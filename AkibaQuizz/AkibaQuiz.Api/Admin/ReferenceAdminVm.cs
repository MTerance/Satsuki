using AkibaQuiz.Contracts.Models;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Admin
{
    public sealed class ReferenceAdminVm
    {
        public IReadOnlyList<CategoryModel> Categories { get; set; } = Array.Empty<CategoryModel>();
        public IReadOnlyList<TagModel> Tags { get; set; } = Array.Empty<TagModel>();
    }
}
