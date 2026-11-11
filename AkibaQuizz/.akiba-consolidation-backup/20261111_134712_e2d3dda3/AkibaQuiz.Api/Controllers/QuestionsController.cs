using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Services;
using AkibaQuiz.Contracts;
using AkibaQuiz.Contracts.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Controllers
{
    [ApiController]
    [Route("api/admin/questions-answers")]
    [IgnoreAntiforgeryToken]
    [TypeFilter(typeof(AdminApiKeyFilter))]
    [TypeFilter(typeof(ApiExceptionFilter))]
    public sealed class QuestionsAnswersController(QuestionService service) : ControllerBase
    {
        [HttpGet]
        public async Task<IActionResult> All(CancellationToken ct) => Ok(await service.All(ct));

        [HttpGet("{id:long}")]
        public async Task<IActionResult> Get(long id, CancellationToken ct)
        {
            var x = await service.Get(id, ct); return x is null ? NotFound() : Ok(x);
        }
        [HttpPost]
        public async Task<IActionResult> Create([FromBody] QuestionWrite input, CancellationToken ct)
        {
            var x = await service.Save(null, input, "TP4-Admin", ct);
            return CreatedAtAction(nameof(Get), new { id = x.Id }, x);
        }
        [HttpPut("{id:long}")]
        public async Task<IActionResult> Update(long id, [FromBody] QuestionWrite input, CancellationToken ct)
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
