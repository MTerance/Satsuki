using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Services
{
    public sealed class GameService(IGameRepository repo, QuestionService questionService, QcmService qcmService)
    {
        public Task<List<GameDto>> All(CancellationToken ct) => repo.All(ct);
        public Task<GameDto?> Get(long id, CancellationToken ct) => repo.Get(id, ct);
        public async Task<GameDto> Save(long? id, GameWrite value, string author, CancellationToken ct)
        {
            if (string.IsNullOrWhiteSpace(value.Name) 
                || value.Rounds is null) 
                throw new ApiValidationException("Nom et manches obligatoires.");
            if (value.Rounds.Any(r => r is null || r.Position < 0 ||r.Questions is null) ||
            value.Rounds.Select(r => r.Position).Distinct().Count() != value.Rounds.Count) 
                throw new ApiValidationException("Positions de manches invalides ou dupliquées.");
            foreach (var r in value.Rounds)
            {
                if (r.Questions.Any(q => q is null || q.Position < 0) || r.Questions.Select(q => q.Position).Distinct().Count() != r.Questions.Count)
                    throw new ApiValidationException("Positions de questions invalides ou dupliquées.");
                foreach (var q in r.Questions) if ((q.IdQuestionAnswer.HasValue ? 1 : 0) + (q.IdQCMQuestion.HasValue ? 1 : 0) + (q.IdListQuestionsAnswers.HasValue ? 1 : 0) != 1 || q.IdListQuestionsAnswers.HasValue)
                    throw new ApiValidationException("Utiliser exactement une référence QuestionAnswer ou QCM. IdListQuestionsAnswers n'est pas pris en charge.");
            }
            var key = await repo.Save(id, value, author, ct); 
            return (await repo.Get(key, ct))!;
        }
        public Task<bool> Delete(long id, CancellationToken ct) => repo.Delete(id, ct);

        /// <summary>
        /// Charge la definition complete d'un Game destinee a Ciel (regie).
        /// Reutilise les repositories existants et ne change pas le CRUD TP4.
        /// </summary>
        public async Task<GameFullDto?> GetFull(long id, CancellationToken ct)
        {
            if (id <= 0)
                return null;

            var game = await repo.Get(id, ct);
            if (game is null)
                return null;

            // Un QCM / QuestionAnswer peut apparaitre dans plusieurs manches :
            // le charger une seule fois pendant cette requete.
            var questions = new Dictionary<long, QuestionDto>();
            var qcms = new Dictionary<long, QcmDto>();
            var rounds = new List<GameFullRoundDto>();

            foreach (var round in game.Rounds.OrderBy(r => r.Position).ThenBy(r => r.Id))
            {
                var entries = new List<GameFullQuestionDto>();

                foreach (var reference in round.Questions.OrderBy(q => q.Position).ThenBy(q => q.Id))
                {
                    bool hasQa = reference.IdQuestionAnswer.HasValue;
                    bool hasQcm = reference.IdQCMQuestion.HasValue;

                    if (reference.IdListQuestionsAnswers.HasValue ||
                        hasQa == hasQcm ||
                        (hasQa && reference.IdQuestionAnswer!.Value <= 0) ||
                        (hasQcm && reference.IdQCMQuestion!.Value <= 0))
                    {
                        throw new ApiConflictException(
                            $"Reference de question incorrecte : RoundQuestions #{reference.Id}.");
                    }

                    if (hasQa)
                    {
                        long questionId = reference.IdQuestionAnswer!.Value;
                        if (!questions.TryGetValue(questionId, out var question))
                        {
                            question = await questionService.Get(questionId, ct)
                                ?? throw new ApiConflictException(
                                    $"QuestionAnswer #{questionId} introuvable.");
                            questions.Add(questionId, question);
                        }

                        entries.Add(new GameFullQuestionDto(
                            reference.Id, reference.Position, "QuestionAnswer",
                            questionId, null, question, null));
                    }
                    else
                    {
                        long qcmId = reference.IdQCMQuestion!.Value;
                        if (!qcms.TryGetValue(qcmId, out var qcm))
                        {
                            qcm = await qcmService.GetByIdAsync(qcmId, ct)
                                ?? throw new ApiConflictException(
                                    $"QCM #{qcmId} introuvable.");
                            qcms.Add(qcmId, qcm);
                        }

                        entries.Add(new GameFullQuestionDto(
                            reference.Id, reference.Position, "QCM",
                            null, qcmId, null, qcm));
                    }
                }

                rounds.Add(new GameFullRoundDto(round.Id, round.Position, entries));
            }

            return new GameFullDto(
                game.Id, game.Name, game.Author, game.CreationDate, rounds);
        }

    }
}
