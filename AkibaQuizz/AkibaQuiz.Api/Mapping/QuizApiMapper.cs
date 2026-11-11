using AkibaQuiz.Contracts;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;

namespace AkibaQuiz.Api.Mapping;

/// <summary>
/// Seule l'API transforme les modèles métier en DTO HTTP.
/// Aucun repository ou service applicatif ne dépend de ces DTO.
/// </summary>
public static class QuizApiMapper
{
    public static CategoryDto ToDto(CategoryModel x) => new(x.Id, x.Name);
    public static TagDto ToDto(TagModel x) => new(x.Id, x.Name, x.Color);
    public static MediaDto ToDto(QuizMediaModel x) => new(
        x.Id, x.IdMedia, x.Filename, x.IdTypeMedia, x.TypeMediaName, x.TypeDisplay);
    public static PropositionDto ToDto(QcmPropositionModel x) => new(
        x.Id, x.IdQCMAnswer, x.Answer, x.IsTrue);

    public static QcmDto ToDto(QcmModel x) => new(
        x.Id, x.Question, x.IdCategory, x.CategoryName, x.Author,
        x.CreationDate?.ToString("O") ?? "",
        x.LastUpdatedDate?.ToString("O") ?? "",
        x.Answers.Select(a => ToDto(a)).ToList(),
        x.Tags.Select(t => ToDto(t)).ToList(),
        x.Medias.Select(m => ToDto(m)).ToList());

    // Préserve les noms JSON de QcmController dans l'archive fournie :
    // lastUpdatedDate, et non lastUpdatedTDate (utilisé par l'ancien QcmDto TP4.2).
    public static QcmAdminDto ToAdminDto(QcmModel x) => new(
        x.Id, x.Question, x.CreationDate, x.LastUpdatedDate,
        x.IdCategory, x.CategoryName, x.Author,
        x.Answers.Select(a => ToDto(a)).ToList(),
        x.Tags.Select(t => ToDto(t)).ToList(),
        x.Medias.Select(m => ToDto(m)).ToList());

    public static QuestionDto ToDto(QuestionAnswerModel x) => new(
        x.Id, x.Question, x.Answer, x.IdCategory, x.CategoryName,
        x.Author, x.CreationDate, x.LastUpdateDate,
        x.Tags.Select(t => ToDto(t)).ToList(), x.Medias.Select(m => ToDto(m)).ToList());

    public static GameDto ToDto(GameModel x) => new(
        x.Id, x.Name, x.Author, x.CreationDate,
        x.Rounds.OrderBy(r => r.Position).ThenBy(r => r.Id)
            .Select(r => new RoundDto(r.Id, r.Position,
                r.Questions.OrderBy(q => q.Position).ThenBy(q => q.Id)
                    .Select(q => new RoundQuestionDto(q.Id, q.Position,
                        q.IdQuestionAnswer, q.IdQCMQuestion, q.IdListQuestionsAnswers))
                    .ToList()))
            .ToList());

    public static GameSummaryDto ToDto(GameSummaryModel x)
        => new() { Id = x.Id, Name = x.Name, RoundCount = x.RoundCount,
                   QuestionCount = x.QuestionCount };

    public static GameFullDto ToDto(GameFullModel full)
        => new(full.Game.Id, full.Game.Name, full.Game.Author, full.Game.CreationDate,
            full.Rounds.Select(r => new GameFullRoundDto(r.Id, r.Position,
                r.Questions.Select(q => new GameFullQuestionDto(
                    q.Id, q.Position, q.Qcm is null ? "QuestionAnswer" : "QCM",
                    q.IdQuestionAnswer, q.IdQCMQuestion,
                    q.QuestionAnswer is null ? null : ToDto(q.QuestionAnswer),
                    q.Qcm is null ? null : ToDto(q.Qcm)))
                    .ToList())).ToList());

    public static SaveQuestionAnswerRequest ToRequest(QuestionWrite x)
    {
        if (x.TagIds is null || x.Medias is null || x.Medias.Any(m => m is null))
            throw new ApiValidationException("Listes de tags ou de médias invalides.");
        return new SaveQuestionAnswerRequest
        {
            Question = x.Question, Answer = x.Answer, IdCategory = x.IdCategory,
            TagIds = x.TagIds.ToList(),
            Medias = x.Medias.Select(m => new SaveMediaAssociationRequest
            {
                IdMedia = m.IdMedia, TypeDisplay = m.TypeDisplay
            }).ToList()
        };
    }

    public static SaveQcmRequest ToRequest(QcmWrite x)
    {
        if (x.TagIds is null || x.Medias is null || x.Answers is null ||
            x.Medias.Any(m => m is null) || x.Answers.Any(a => a is null))
            throw new ApiValidationException("Listes de réponses, tags ou médias invalides.");
        return new SaveQcmRequest
        {
            Question = x.Question, IdCategory = x.IdCategory,
            Answers = x.Answers.Select(a => new SaveQcmPropositionRequest
            {
                Answer = a.Answer, IsTrue = a.IsTrue
            }).ToList(),
            TagIds = x.TagIds.ToList(),
            Medias = x.Medias.Select(m => new SaveMediaAssociationRequest
            {
                IdMedia = m.IdMedia, TypeDisplay = m.TypeDisplay
            }).ToList()
        };
    }

    public static SaveGameRequest ToRequest(GameWrite x)
    {
        if (x.Rounds is null || x.Rounds.Any(r => r is null ||
            r.Questions is null || r.Questions.Any(q => q is null)))
            throw new ApiValidationException("Manches ou questions invalides.");
        return new SaveGameRequest
        {
            Name = x.Name,
            Rounds = x.Rounds.Select(r => new SaveGameRoundRequest
            {
                Position = r.Position,
                Questions = r.Questions.Select(q => new SaveRoundQuestionRequest
                {
                    Position = q.Position, IdQuestionAnswer = q.IdQuestionAnswer,
                    IdQCMQuestion = q.IdQCMQuestion,
                    IdListQuestionsAnswers = q.IdListQuestionsAnswers
                }).ToList()
            }).ToList()
        };
    }
}
