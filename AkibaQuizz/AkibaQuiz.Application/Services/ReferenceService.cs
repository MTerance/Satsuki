
using System.Text.RegularExpressions;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts;
using AkibaQuiz.Contracts.Models;

namespace AkibaQuiz.Application.Services;

public sealed class ReferenceService(
    IReferenceRepository repository) : IReferenceService
{
    public Task<IReadOnlyList<CategoryModel>> GetCategoriesAsync(
        CancellationToken ct)
        => repository.GetCategoriesAsync(ct);

    public Task<IReadOnlyList<TagModel>> GetTagsAsync(
        CancellationToken ct)
        => repository.GetTagsAsync(ct);

    public async Task<long> CreateCategoryAsync(
        string name, CancellationToken ct)
    {
        name = ValidateName(name);

        var id = await repository.CreateCategoryAsync(name, ct);

        return id ?? throw new ApiConflictException(
            "Cette catégorie existe déjà.");
    }

    public async Task RenameCategoryAsync(
        long id, string name, CancellationToken ct)
    {
        ValidateId(id);
        name = ValidateName(name);

        var categories = await repository.GetCategoriesAsync(ct);

        if (!categories.Any(c => c.Id == id))
            throw new KeyNotFoundException(
                "Catégorie introuvable.");

        if (!await repository.RenameCategoryAsync(id, name, ct))
            throw new ApiConflictException(
                "Ce nom de catégorie est déjà utilisé.");
    }

    public async Task DeleteCategoryAsync(
        long id, CancellationToken ct)
    {
        ValidateId(id);

        var categories = await repository.GetCategoriesAsync(ct);

        if (!categories.Any(c => c.Id == id))
            throw new KeyNotFoundException(
                "Catégorie introuvable.");

        if (!await repository.DeleteCategoryAsync(id, ct))
            throw new ApiConflictException(
                "Cette catégorie est utilisée ou " +
                "a été modifiée entre-temps.");
    }

    public async Task<long> CreateTagAsync(
        string name, string? color, CancellationToken ct)
    {
        name = ValidateName(name);
        color = ValidateColor(color);

        var id = await repository.CreateTagAsync(
            name, color, ct);

        return id ?? throw new ApiConflictException(
            "Ce tag existe déjà.");
    }

    public async Task UpdateTagAsync(
        long id, string name, string? color,
        CancellationToken ct)
    {
        ValidateId(id);
        name = ValidateName(name);
        color = ValidateColor(color);

        var tags = await repository.GetTagsAsync(ct);

        if (!tags.Any(t => t.Id == id))
            throw new KeyNotFoundException(
                "Tag introuvable.");

        if (!await repository.UpdateTagAsync(
            id, name, color, ct))
        {
            throw new ApiConflictException(
                "Ce nom de tag est déjà utilisé.");
        }
    }

    public async Task DeleteTagAsync(
        long id, CancellationToken ct)
    {
        ValidateId(id);

        var tags = await repository.GetTagsAsync(ct);

        if (!tags.Any(t => t.Id == id))
            throw new KeyNotFoundException(
                "Tag introuvable.");

        if (!await repository.DeleteTagAsync(id, ct))
            throw new ApiConflictException(
                "Ce tag est utilisé ou " +
                "a été modifié entre-temps.");
    }

    private static void ValidateId(long id)
    {
        if (id <= 0)
            throw new ApiValidationException(
                "Identifiant invalide.");
    }

    private static string ValidateName(string? name)
    {
        name = name?.Trim() ?? "";

        if (name.Length < 2 || name.Length > 80)
            throw new ApiValidationException(
                "Le nom doit contenir entre 2 et 80 caractères.");

        return name;
    }

    private static string? ValidateColor(string? color)
    {
        if (string.IsNullOrWhiteSpace(color))
            return null;

        color = color.Trim().ToUpperInvariant();

        if (!Regex.IsMatch(
            color,
            @"^#[0-9A-F]{6}$",
            RegexOptions.CultureInvariant))
        {
            throw new ApiValidationException(
                "La couleur doit être au format #RRGGBB.");
        }

        return color;
    }
}
