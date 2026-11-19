using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Admin
{
    public sealed class MediaSelectionVm
    {
        public long? IdMedia { get; set; }

        public string? Path { get; set; }

        public string? Filename { get; set; }

        public string TypeDisplay { get; set; } = "DuringQuestion";

    }
}
