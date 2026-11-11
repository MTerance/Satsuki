using AkibaQuiz.Contracts.Models;

namespace AkibaQuiz.Application.Interfaces;

public interface IReferenceService
{
    Task<IReadOnlyList<CategoryModel>> GetCategoriesAsync(CancellationToken ct);
    Task<IReadOnlyList<TagModel>> GetTagsAsync(CancellationToken ct);
}
