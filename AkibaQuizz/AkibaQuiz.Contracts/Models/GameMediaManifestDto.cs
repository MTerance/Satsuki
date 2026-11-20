using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Models
{
    public sealed record GameMediaItemDto(
        long IdMedia,
        string Filename,
        string TypeMediaName,
        string? Url,
        bool Available
    );

    public sealed record GameMediaManifestDto(
        long GameId,
        List<GameMediaItemDto> Medias
    );
}
