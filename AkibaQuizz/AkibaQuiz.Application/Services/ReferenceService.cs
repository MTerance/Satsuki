using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts.Models;

namespace AkibaQuiz.Application.Services;

public sealed class ReferenceService(IReferenceRepository repository) : IReferenceService
{
    public Task<IReadOnlyList<CategoryModel>> GetCategoriesAsync(CancellationToken ct)
        => repository.GetCategoriesAsync(ct);

    public Task<IReadOnlyList<TagModel>> GetTagsAsync(CancellationToken ct)
        => repository.GetTagsAsync(ct);
}
