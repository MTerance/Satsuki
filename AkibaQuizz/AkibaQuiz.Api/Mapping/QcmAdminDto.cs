using AkibaQuiz.Contracts;

namespace AkibaQuiz.Api.Mapping;

/// <summary>
/// Compatibilite HTTP de /api/admin/qcm avec l'archive fournie.
/// N'exporte pas le modele metier directement depuis le controleur.
/// </summary>
public sealed record QcmAdminDto(
    long Id,
    string Question,
    DateTimeOffset? CreationDate,
    DateTimeOffset? LastUpdatedDate,
    long IdCategory,
    string CategoryName,
    string Author,
    List<PropositionDto> Answers,
    List<TagDto> Tags,
    List<MediaDto> Medias);
