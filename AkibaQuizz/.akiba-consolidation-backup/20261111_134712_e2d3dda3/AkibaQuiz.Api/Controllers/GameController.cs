using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Services;
using AkibaQuiz.Contracts;
using Microsoft.AspNetCore.Mvc;

namespace AkibaQuiz.Api.Controllers
{
    [ApiController]
    [Route("api/admin/games")]
    [IgnoreAntiforgeryToken]
    [TypeFilter(typeof(AdminApiKeyFilter))]
    [TypeFilter(typeof(ApiExceptionFilter))]
    public sealed class GamesController(GameService service) : ControllerBase
    {
        [HttpGet] 
        public async Task<IActionResult> All(CancellationToken ct) => Ok(await service.All(ct));
        
        [HttpGet("{id:long}")] 
        public async Task<IActionResult> Get(long id, CancellationToken ct) 
        {
            var x = await service.Get(id, ct);
            return x is null ? NotFound() : Ok(x); 
        }
        [HttpPost] 
        public async Task<IActionResult> Create([FromBody] GameWrite input, CancellationToken ct) 
        {
            var x = await service.Save(null, input, "TP4-Admin", ct);
            return CreatedAtAction(nameof(Get), new { id = x.Id }, x); 
        }
        [HttpPut("{id:long}")]
        public async Task<IActionResult> Update(long id, [FromBody] GameWrite input, CancellationToken ct) 
        { 
            await service.Save(id, input, "TP4-Admin", ct);
            return NoContent();
        }
        [HttpDelete("{id:long}")] 
        public async Task<IActionResult> Delete(long id, CancellationToken ct) 
        {
            return await service.Delete(id, ct) ? NoContent() : NotFound();
        }
    }
}
