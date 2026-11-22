using AkibaQuiz.Contracts.Models;

namespace AkibaQuiz.Application.Interfaces;

public interface IReferenceService
{
    Task<IReadOnlyList<CategoryModel>> GetCategoriesAsync(CancellationToken ct);
    Task<IReadOnlyList<TagModel>> GetTagsAsync(CancellationToken ct);
    Task<long> CreateCategoryAsync(string name, CancellationToken ct);

    Task RenameCategoryAsync(long id, string name, CancellationToken ct);
    Task DeleteCategoryAsync(
        long id, CancellationToken ct);

    Task<long> CreateTagAsync(
        string name, string? color, CancellationToken ct);

    Task UpdateTagAsync(
        long id, string name, string? color,
        CancellationToken ct);

    Task DeleteTagAsync(
        long id, CancellationToken ct);
}
