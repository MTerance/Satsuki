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


    public async Task<GameFullModel?> GetFullAsync(
        long id,
        CancellationToken ct)
    {
        // ==========================================
        // 1. Validation de l'identifiant
        // ==========================================

        if (id <= 0)
        {
            throw new ApiValidationException(
                "Identifiant de Game invalide.");
        }

        ct.ThrowIfCancellationRequested();

        // ==========================================
        // 2. Chargement du Game
        // ==========================================

        var game = await repository.GetByIdAsync(id, ct);

        if (game is null)
            return null;

        // ==========================================
        // 3. Validation structurelle
        // ==========================================

        ValidateStoredGame(game);

        // ==========================================
        // 4. Initialisation des caches locaux
        // ==========================================

        var questionCache =
            new Dictionary<long, QuestionAnswerModel>();

        var qcmCache =
            new Dictionary<long, QcmModel>();

        var fullRounds =
            new List<GameFullRoundModel>();

        // ==========================================
        // 5. Construction des manches
        // ==========================================

        foreach (var round in game.Rounds
            .OrderBy(r => r.Position)
            .ThenBy(r => r.Id))
        {
            ct.ThrowIfCancellationRequested();

            var fullQuestions =
                new List<GameFullQuestionModel>();

            foreach (var entry in round.Questions
                .OrderBy(q => q.Position)
                .ThenBy(q => q.Id))
            {
                ct.ThrowIfCancellationRequested();

                QuestionAnswerModel? question = null;
                QcmModel? qcm = null;

                // ==================================
                // Chargement QuestionAnswer
                // ==================================

                if (entry.IdQuestionAnswer is long questionId)
                {
                    if (!questionCache.TryGetValue(
                        questionId,
                        out question))
                    {
                        question = await questions.GetByIdAsync(
                            questionId,
                            ct)
                            ?? throw new ApiConflictException(
                                $"QuestionAnswer #{questionId} " +
                                "introuvable.");

                        questionCache.Add(
                            questionId,
                            question);
                    }
                }

                // ==================================
                // Chargement QCM
                // ==================================

                else if (entry.IdQCMQuestion is long qcmId)
                {
                    if (!qcmCache.TryGetValue(qcmId, out qcm))
                    {
                        qcm = await qcms.GetByIdAsync(qcmId, ct)
                            ?? throw new ApiConflictException(
                                $"QCM #{qcmId} introuvable.");

                        qcmCache.Add(qcmId, qcm);
                    }
                }

                // ==================================
                // Construction de la question
                // ==================================

                fullQuestions.Add(new GameFullQuestionModel
                {
                    Id = entry.Id,

                    Position = entry.Position,

                    IdQuestionAnswer =
                        entry.IdQuestionAnswer,

                    IdQCMQuestion =
                        entry.IdQCMQuestion,

                    QuestionAnswer = question,

                    Qcm = qcm
                });
            }

            fullRounds.Add(new GameFullRoundModel
            {
                Id = round.Id,

                Position = round.Position,

                Questions = fullQuestions
            });
        }

        // ==========================================
        // 6. Construction du Game complet
        // ==========================================

        return new GameFullModel
        {
            Game = game,

            Rounds = fullRounds
        };
    }

    public async Task<GameModel> SaveAsync(
        long? id,
        SaveGameRequest value,
        string author,
        CancellationToken ct)
    {
        if (id is <= 0)
        {
            throw new ApiValidationException(
                "Identifiant de Game invalide.");
        }

        ValidateGame(value);

        var key = await repository.SaveAsync(
            id,
            value,
            author,
            ct);

        return await repository.GetByIdAsync(key, ct)
            ?? throw new InvalidOperationException(
                $"Game #{key} non relu apres enregistrement.");
    }


    public Task<bool> DeleteAsync(long id, CancellationToken ct) => repository.DeleteAsync(id, ct);

    private static void ValidateStoredGame(GameModel game)
    {
        var request = new SaveGameRequest
        {
            Name = game.Name,

            Rounds = game.Rounds
                .OrderBy(r => r.Position)
                .ThenBy(r => r.Id)
                .Select(round => new SaveGameRoundRequest
                {
                    Position = round.Position,

                    Questions = round.Questions
                        .OrderBy(q => q.Position)
                        .ThenBy(q => q.Id)
                        .Select(question =>
                            new SaveRoundQuestionRequest
                            {
                                Position = question.Position,

                                IdQuestionAnswer =
                                    question.IdQuestionAnswer,

                                IdQCMQuestion =
                                    question.IdQCMQuestion,

                                IdListQuestionsAnswers =
                                    question.IdListQuestionsAnswers
                            })
                        .ToList()
                })
                .ToList()
        };

        try
        {
            ValidateGame(request);
        }
        catch (ApiValidationException ex)
        {
            throw new ApiConflictException(
                $"Le Game #{game.Id} contient une " +
                $"structure invalide : {ex.Message}");
        }
    }



    private static void ValidateGame(SaveGameRequest value)
    {
        ArgumentNullException.ThrowIfNull(value);

        // ========================================
        // Validation du Game
        // ========================================

        if (string.IsNullOrWhiteSpace(value.Name) ||
            value.Name.Trim().Length < 2)
        {
            throw new ApiValidationException(
                "Le nom du Game doit contenir au moins deux caractères.");
        }

        if (value.Rounds is null || value.Rounds.Count == 0)
        {
            throw new ApiValidationException(
                "Le Game doit contenir au moins une manche.");
        }

        // ========================================
        // Validation des manches
        // ========================================

        for (int i = 0; i < value.Rounds.Count; i++)
        {
            var round = value.Rounds[i];

            long expectedRoundPosition = i + 1L;

            if (round is null)
            {
                throw new ApiValidationException(
                    $"La manche {expectedRoundPosition} est invalide.");
            }

            if (round.Position != expectedRoundPosition)
            {
                throw new ApiValidationException(
                    $"Position de manche invalide. " +
                    $"Attendue : {expectedRoundPosition}, " +
                    $"reçue : {round.Position}.");
            }

            if (round.Questions is null ||
                round.Questions.Count == 0)
            {
                throw new ApiValidationException(
                    $"La manche {round.Position} doit contenir " +
                    "au moins une question.");
            }

            var references = new HashSet<(string Type, long Id)>();

            // ========================================
            // Validation des questions
            // ========================================

            for (int j = 0; j < round.Questions.Count; j++)
            {
                var question = round.Questions[j];

                long expectedQuestionPosition = j + 1L;

                if (question is null)
                {
                    throw new ApiValidationException(
                        $"La question {expectedQuestionPosition} " +
                        $"de la manche {round.Position} est invalide.");
                }

                if (question.Position != expectedQuestionPosition)
                {
                    throw new ApiValidationException(
                        $"Position de question invalide dans " +
                        $"la manche {round.Position}. " +
                        $"Attendue : {expectedQuestionPosition}, " +
                        $"reçue : {question.Position}.");
                }

                // ========================================
                // Exclusivité des références QA / QCM
                // ========================================

                var validQA = question.IdQuestionAnswer is > 0;
                var validQcm = question.IdQCMQuestion is > 0;

                if (question.IdListQuestionsAnswers.HasValue ||
                    validQA == validQcm ||
                    (question.IdQuestionAnswer.HasValue && !validQA) ||
                    (question.IdQCMQuestion.HasValue && !validQcm))
                {
                    throw new ApiValidationException(
                        $"Référence invalide pour la question " +
                        $"{question.Position} de la manche " +
                        $"{round.Position}. " +
                        "Utiliser exactement une référence " +
                        "QuestionAnswer ou QCM.");
                }

                // ========================================
                // Détection des doublons
                // ========================================

                var reference = validQA
                    ? ("QA", question.IdQuestionAnswer!.Value)
                    : ("QCM", question.IdQCMQuestion!.Value);

                if (!references.Add(reference))
                {
                    throw new ApiValidationException(
                        $"La question {reference.Item1} " +
                        $"#{reference.Item2} est présente plusieurs fois " +
                        $"dans la manche {round.Position}.");
                }
            }
        }
    }
}