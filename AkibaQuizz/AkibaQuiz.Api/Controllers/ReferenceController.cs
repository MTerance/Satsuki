
using AkibaQuiz.Api.Mapping;
using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace AkibaQuiz.Api.Controllers;

[ApiController]
[Route("api/admin/references")]
[TypeFilter(typeof(AdminApiKeyFilter))]
[TypeFilter(typeof(ApiExceptionFilter))]
public sealed class ReferencesController(
    IReferenceService references) : ControllerBase
{
    [HttpGet("categories")]
    public async Task<IActionResult> Categories(
        CancellationToken ct)
    {
        var categories =
            await references.GetCategoriesAsync(ct);

        return Ok(
            categories
                .Select(QuizApiMapper.ToDto)
                .ToList());
    }

    [HttpGet("tags")]
    public async Task<IActionResult> Tags(
        CancellationToken ct)
    {
        var tags =
            await references.GetTagsAsync(ct);

        return Ok(
            tags
                .Select(QuizApiMapper.ToDto)
                .ToList());
    }
}
