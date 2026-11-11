using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Services;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Controllers
{
    [ApiController]
    [Route("api/catalog/games")]
    [TypeFilter(typeof(AdminApiKeyFilter))] // Auth TP local uniquement.
    [TypeFilter(typeof(ApiExceptionFilter))]
    public sealed class GameFullController(GameService service) : ControllerBase
    {
        [HttpGet("{id:long:min(1)}")]
        public async Task<IActionResult> Get(long id, CancellationToken ct)
        {
            var game = await service.GetFull(id, ct);
            return game is null ? NotFound() : Ok(game);
        }
    }
}
