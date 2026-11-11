using AkibaQuiz.Api.Mapping;
using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts;
using Microsoft.AspNetCore.Mvc;

namespace AkibaQuiz.Api.Controllers;

[ApiController]
[Route("api/admin/questions-answers")]
[IgnoreAntiforgeryToken]
[TypeFilter(typeof(AdminApiKeyFilter))]
[TypeFilter(typeof(ApiExceptionFilter))]
public sealed class QuestionsAnswersController(IQuestionService service) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> All(CancellationToken ct)
        => Ok((await service.GetAllAsync(ct)).Select(QuizApiMapper.ToDto).ToList());

    [HttpGet("{id:long}")]
    public async Task<IActionResult> Get(long id, CancellationToken ct)
    {
        var item = await service.GetByIdAsync(id, ct);
        return item is null ? NotFound() : Ok(QuizApiMapper.ToDto(item));
    }

    [HttpPost]
    public async Task<IActionResult> Create([FromBody] QuestionWrite input, CancellationToken ct)
    {
        var model = await service.SaveAsync(null, QuizApiMapper.ToRequest(input), "TP4-Admin", ct);
        var dto = QuizApiMapper.ToDto(model);
        return CreatedAtAction(nameof(Get), new { id = dto.Id }, dto);
    }

    [HttpPut("{id:long}")]
    public async Task<IActionResult> Update(long id, [FromBody] QuestionWrite input, CancellationToken ct)
    {
        await service.SaveAsync(id, QuizApiMapper.ToRequest(input), "TP4-Admin", ct);
        return NoContent();
    }

    [HttpDelete("{id:long}")]
    public async Task<IActionResult> Delete(long id, CancellationToken ct)
        => await service.DeleteAsync(id, ct) ? NoContent() : NotFound();
}
