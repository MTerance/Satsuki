using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;

namespace AkibaQuiz.Application.Services;

public sealed class QcmService(IQcmRepository repository) : IQcmService
{
    public Task<IReadOnlyList<QcmModel>> GetAllAsync(CancellationToken ct)
        => repository.GetAllAsync(ct);

    public Task<QcmModel?> GetByIdAsync(long id, CancellationToken ct)
        => repository.GetByIdAsync(id, ct);

    public async Task<QcmModel> SaveAsync(long? id, SaveQcmRequest value, string author, CancellationToken ct)
    {
        ArgumentNullException.ThrowIfNull(value);
        if (string.IsNullOrWhiteSpace(value.Question) || value.IdCategory <= 0
            || value.Answers is null || value.Answers.Count is < 2 or > 8
            || value.Answers.Any(a => a is null || string.IsNullOrWhiteSpace(a.Answer))
            || !value.Answers.Any(a => a.IsTrue)
            || value.TagIds is null || value.Medias is null)
            throw new ApiValidationException("QCM invalide : 2 à 8 propositions et au moins une bonne réponse.");

        var key = await repository.SaveAsync(id, value, author, ct);
        return await repository.GetByIdAsync(key, ct)
            ?? throw new InvalidOperationException($"QCM #{key} non relu après enregistrement.");
    }

    public Task<bool> DeleteAsync(long id, CancellationToken ct) => repository.DeleteAsync(id, ct);
}
