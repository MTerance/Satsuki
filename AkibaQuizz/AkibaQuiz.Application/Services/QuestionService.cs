using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Services
{
    public sealed class QuestionService(IQuestionRepository repo)
    {
        public Task<List<QuestionDto>> All(CancellationToken ct) => repo.All(ct);
        public Task<QuestionDto?> Get(long id, CancellationToken ct) => repo.Get(id, ct);
        public async Task<QuestionDto> Save(long? id, QuestionWrite value, string author, CancellationToken ct)
        {
            if (string.IsNullOrWhiteSpace(value.Question) || string.IsNullOrWhiteSpace(value.Answer) || value.IdCategory <= 0 || value.TagIds is null || value.Medias is null)
                throw new ApiValidationException("Question, réponse, catégorie et listes obligatoires.");
            var key = await repo.Save(id, value, author, ct);
            return (await repo.Get(key, ct))!;
        }
        public Task<bool> Delete(long id, CancellationToken ct) => repo.Delete(id, ct);
    }
}
