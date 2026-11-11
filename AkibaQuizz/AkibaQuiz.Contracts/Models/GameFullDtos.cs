using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Contracts.Models
{
    public sealed record GameFullDto(
        long Id,
        string Name,
        string Author,
        string? CreationDate,
        List<GameFullRoundDto> Rounds);

    public sealed record GameFullRoundDto(
        long Id,
        long Position,
        List<GameFullQuestionDto> Questions);

    public sealed record GameFullQuestionDto(
        long Id,
        long Position,
        string Type,
        long? IdQuestionAnswer,
        long? IdQCMQuestion,
        QuestionDto? QuestionAnswer,
        QcmDto? Qcm);
}
