using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;

namespace AkibaQuiz.Application.Services;

public sealed class QuestionService(IQuestionRepository repository) : IQuestionService
{
    public Task<IReadOnlyList<QuestionAnswerModel>> GetAllAsync(CancellationToken ct)
        => repository.GetAllAsync(ct);

    public Task<QuestionAnswerModel?> GetByIdAsync(long id, CancellationToken ct)
        => repository.GetByIdAsync(id, ct);

    public async Task<QuestionAnswerModel> SaveAsync(long? id, SaveQuestionAnswerRequest value, string author, CancellationToken ct)
    {
        ArgumentNullException.ThrowIfNull(value);
        if (string.IsNullOrWhiteSpace(value.Question) || string.IsNullOrWhiteSpace(value.Answer)
            || value.IdCategory <= 0 || value.TagIds is null || value.Medias is null)
            throw new ApiValidationException("Question, réponse, catégorie et listes obligatoires.");

        var key = await repository.SaveAsync(id, value, author, ct);
        return await repository.GetByIdAsync(key, ct)
            ?? throw new InvalidOperationException($"QuestionAnswer #{key} non relu après enregistrement.");
    }

    public Task<bool> DeleteAsync(long id, CancellationToken ct) => repository.DeleteAsync(id, ct);
}
