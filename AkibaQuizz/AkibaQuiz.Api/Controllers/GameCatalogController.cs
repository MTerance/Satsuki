using AkibaQuiz.Api.Mapping;
using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace AkibaQuiz.Api.Controllers;

[ApiController]
[Route("api/catalog/games")]
[TypeFilter(typeof(AdminApiKeyFilter))]
[TypeFilter(typeof(ApiExceptionFilter))]
public sealed class GameCatalogController(IGameService games) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> GetGames(CancellationToken ct)
        => Ok((await games.GetSummariesAsync(ct))
            .Select(QuizApiMapper.ToDto).ToList());
}
