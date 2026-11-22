using AkibaQuiz.Contracts.Models;

namespace AkibaQuiz.Application.Interfaces;

public interface IReferenceRepository
{
    Task<IReadOnlyList<CategoryModel>> GetCategoriesAsync(CancellationToken ct);
    Task<IReadOnlyList<TagModel>> GetTagsAsync(CancellationToken ct);

    Task<long?> CreateCategoryAsync(
        string name, CancellationToken ct);

    Task<bool> RenameCategoryAsync(
        long id, string name, CancellationToken ct);

    Task<bool> DeleteCategoryAsync(
        long id, CancellationToken ct);

    Task<long?> CreateTagAsync(
        string name, string? color, CancellationToken ct);

    Task<bool> UpdateTagAsync(
        long id, string name, string? color,
        CancellationToken ct);

    Task<bool> DeleteTagAsync(
        long id, CancellationToken ct);
}
