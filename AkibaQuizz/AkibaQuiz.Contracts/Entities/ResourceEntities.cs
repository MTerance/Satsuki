using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Entities
{
    public sealed class MediaEntity
    {
        public long Id { get; set; }
        public string Filename { get; set; } = "";
        public long IdTypeMedia { get; set; }
    }

    public sealed class TypeMediaEntity
    {
        public long Id { get; set; }
        public string Name { get; set; } = "";
    }

    public sealed class MediaQuizzEntity
    {
        public long Id { get; set; }
        public long? IdQCMQuestion { get; set; }
        public long IdMedia { get; set; }
        public long? IdQuestionAnswer { get; set; }
        public string TypeDisplay { get; set; } = "";
    }

    public sealed class TagEntity
    {
        public long Id { get; set; }
        public string Name { get; set; } = "";
        public string? Color { get; set; }
    }

    public sealed class TagQuizzEntity
    {
        public long Id { get; set; }
        public long IdTag { get; set; }
        public long? IdQuestionAnswer { get; set; }
        public long? IdQCM { get; set; }
    }
}
