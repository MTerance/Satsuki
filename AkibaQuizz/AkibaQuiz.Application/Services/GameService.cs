using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Services
{
    public sealed class GameService(IGameRepository repo)
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
    }
}
