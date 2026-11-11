using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;

namespace AkibaQuiz.Application.Services;

// Orchestration de cas d'utilisation. Ne dépend pas d'Infrastructure ni d'un DTO HTTP.
public sealed class GameService(
    IGameRepository repository,
    IQuestionService questions,
    IQcmService qcms) : IGameService
{
    public Task<IReadOnlyList<GameModel>> GetAllAsync(CancellationToken ct)
        => repository.GetAllAsync(ct);

    public Task<GameModel?> GetByIdAsync(long id, CancellationToken ct)
        => repository.GetByIdAsync(id, ct);

    public Task<IReadOnlyList<GameSummaryModel>> GetSummariesAsync(CancellationToken ct)
        => repository.GetSummariesAsync(ct);

    public async Task<GameFullModel?> GetFullAsync(long id, CancellationToken ct)
    {
        var game = await repository.GetByIdAsync(id, ct);
        if (game is null) return null;

        // Une même question peut apparaître dans plusieurs manches : un seul chargement par ID.
        var questionCache = new Dictionary<long, QuestionAnswerModel>();
        var qcmCache = new Dictionary<long, QcmModel>();
        var fullRounds = new List<GameFullRoundModel>();

        foreach (var round in game.Rounds.OrderBy(r => r.Position).ThenBy(r => r.Id))
        {
            var fullQuestions = new List<GameFullQuestionModel>();
            foreach (var entry in round.Questions.OrderBy(q => q.Position).ThenBy(q => q.Id))
            {
                bool hasQuestion = entry.IdQuestionAnswer is > 0;
                bool hasQcm = entry.IdQCMQuestion is > 0;
                if (entry.IdListQuestionsAnswers.HasValue || hasQuestion == hasQcm
                    || (entry.IdQuestionAnswer.HasValue && !hasQuestion)
                    || (entry.IdQCMQuestion.HasValue && !hasQcm))
                    throw new ApiConflictException($"Référence invalide dans RoundQuestions #{entry.Id}.");

                QuestionAnswerModel? question = null;
                QcmModel? qcm = null;
                if (entry.IdQuestionAnswer is long questionId)
                {
                    if (!questionCache.TryGetValue(questionId, out question))
                    {
                        question = await questions.GetByIdAsync(questionId, ct)
                            ?? throw new ApiConflictException($"QuestionAnswer #{questionId} introuvable.");
                        questionCache.Add(questionId, question);
                    }
                }
                else if (entry.IdQCMQuestion is long qcmId)
                {
                    if (!qcmCache.TryGetValue(qcmId, out qcm))
                    {
                        qcm = await qcms.GetByIdAsync(qcmId, ct)
                            ?? throw new ApiConflictException($"QCM #{qcmId} introuvable.");
                        qcmCache.Add(qcmId, qcm);
                    }
                }
                fullQuestions.Add(new GameFullQuestionModel
                {
                    Id = entry.Id, Position = entry.Position,
                    IdQuestionAnswer = entry.IdQuestionAnswer,
                    IdQCMQuestion = entry.IdQCMQuestion,
                    QuestionAnswer = question, Qcm = qcm
                });
            }
            fullRounds.Add(new GameFullRoundModel
            {
                Id = round.Id, Position = round.Position, Questions = fullQuestions
            });
        }
        return new GameFullModel { Game = game, Rounds = fullRounds };
    }

    public async Task<GameModel> SaveAsync(long? id, SaveGameRequest value, string author, CancellationToken ct)
    {
        ArgumentNullException.ThrowIfNull(value);
        if (string.IsNullOrWhiteSpace(value.Name) || value.Rounds is null)
            throw new ApiValidationException("Nom et manches obligatoires.");
        if (value.Rounds.Any(r => r is null || r.Position < 0 || r.Questions is null)
            || value.Rounds.Select(r => r.Position).Distinct().Count() != value.Rounds.Count)
            throw new ApiValidationException("Positions de manches invalides ou dupliquées.");
        foreach (var round in value.Rounds)
        {
            if (round.Questions.Any(q => q is null || q.Position < 0)
                || round.Questions.Select(q => q.Position).Distinct().Count() != round.Questions.Count)
                throw new ApiValidationException("Positions de questions invalides ou dupliquées.");
            foreach (var question in round.Questions)
            {
                var validQA = question.IdQuestionAnswer is > 0;
                var validQcm = question.IdQCMQuestion is > 0;
                if (question.IdListQuestionsAnswers.HasValue || validQA == validQcm
                    || (question.IdQuestionAnswer.HasValue && !validQA)
                    || (question.IdQCMQuestion.HasValue && !validQcm))
                    throw new ApiValidationException("Utiliser exactement une référence QuestionAnswer ou QCM. IdListQuestionsAnswers n'est pas pris en charge.");
            }
        }
        var key = await repository.SaveAsync(id, value, author, ct);
        return await repository.GetByIdAsync(key, ct)
            ?? throw new InvalidOperationException($"Game #{key} non relu après enregistrement.");
    }

    public Task<bool> DeleteAsync(long id, CancellationToken ct) => repository.DeleteAsync(id, ct);
}
