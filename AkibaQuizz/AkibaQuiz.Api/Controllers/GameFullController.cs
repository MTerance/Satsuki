using AkibaQuiz.Api.Mapping;
using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace AkibaQuiz.Api.Controllers;

[ApiController]
[Route("api/catalog/games")]
[TypeFilter(typeof(AdminApiKeyFilter))]
[TypeFilter(typeof(ApiExceptionFilter))]
public sealed class GameFullController(IGameService service) : ControllerBase
{
    [HttpGet("{id:long:min(1)}")]
    public async Task<IActionResult> Get(long id, CancellationToken ct)
    {
        var full = await service.GetFullAsync(id, ct);
        return full is null ? NotFound() : Ok(QuizApiMapper.ToDto(full));
    }
}
