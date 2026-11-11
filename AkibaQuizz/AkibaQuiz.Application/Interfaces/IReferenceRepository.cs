using AkibaQuiz.Contracts.Models;

namespace AkibaQuiz.Application.Interfaces;

public interface IReferenceRepository
{
    Task<IReadOnlyList<CategoryModel>> GetCategoriesAsync(CancellationToken ct);
    Task<IReadOnlyList<TagModel>> GetTagsAsync(CancellationToken ct);
}
