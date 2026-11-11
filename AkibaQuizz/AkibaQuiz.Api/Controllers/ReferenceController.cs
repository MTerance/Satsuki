using AkibaQuiz.Api.Mapping;
using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace AkibaQuiz.Api.Controllers;

[ApiController]
[Route("api/admin/references")]
[TypeFilter(typeof(AdminApiKeyFilter))]
public sealed class ReferencesController(IReferenceService references) : ControllerBase
{
    [HttpGet("categories")]
    public async Task<IActionResult> Categories(CancellationToken ct)
        => Ok((await references.GetCategoriesAsync(ct)).Select(QuizApiMapper.ToDto).ToList());

    [HttpGet("tags")]
    public async Task<IActionResult> Tags(CancellationToken ct)
        => Ok((await references.GetTagsAsync(ct)).Select(QuizApiMapper.ToDto).ToList());
}
