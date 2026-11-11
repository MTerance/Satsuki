using Microsoft.AspNetCore.Mvc;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Api.Security;

namespace AkibaQuiz.Api.Controllers
{

    [ApiController]
    [Route("api/catalog/games")]
    [TypeFilter(typeof(AdminApiKeyFilter))]
    public class GameCatalogController : ControllerBase
    {
        private readonly IGameCatalogService _gameCatalogService;

        public GameCatalogController(IGameCatalogService gameCatalogService)
        {
            _gameCatalogService = gameCatalogService;
        }

        [HttpGet]
        public async Task<IActionResult> GetGames(CancellationToken cancellationToken)
        {
            var games = await _gameCatalogService.GetGamesAsync(cancellationToken);
            return Ok(games);
        }
    }
}
