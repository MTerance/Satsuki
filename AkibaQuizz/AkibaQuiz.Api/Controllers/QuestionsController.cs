
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
public sealed class QuestionsAnswersController(
    IQuestionService service,
    IAuditActorProvider auditActorProvider)
    : ControllerBase
{
    #region Lecture

    [HttpGet]
    public async Task<IActionResult> All(
        CancellationToken ct)
    {
        var items = await service.GetAllAsync(ct);

        return Ok(
            items.Select(QuizApiMapper.ToDto).ToList());
    }

    [HttpGet("{id:long}")]
    public async Task<IActionResult> Get(
        long id,
        CancellationToken ct)
    {
        if (id <= 0)
        {
            return BadRequest(new
            {
                error = "Identifiant de question invalide."
            });
        }

        var item = await service.GetByIdAsync(id, ct);

        return item is null
            ? NotFound()
            : Ok(QuizApiMapper.ToDto(item));
    }

    #endregion

    #region Creation

    [HttpPost]
    public async Task<IActionResult> Create(
        [FromBody] QuestionWrite input,
        CancellationToken ct)
    {
        var actor = auditActorProvider.GetCurrent();

        var request = QuizApiMapper.ToRequest(input);

        var model = await service.SaveAsync(
            null,
            request,
            actor.ActorId,
            ct);

        var dto = QuizApiMapper.ToDto(model);

        return CreatedAtAction(
            nameof(Get),
            new { id = dto.Id },
            dto);
    }

    #endregion

    #region Modification

    [HttpPut("{id:long}")]
    public async Task<IActionResult> Update(
        long id,
        [FromBody] QuestionWrite input,
        CancellationToken ct)
    {
        if (id <= 0)
        {
            return BadRequest(new
            {
                error = "Identifiant de question invalide."
            });
        }

        var actor = auditActorProvider.GetCurrent();

        var request = QuizApiMapper.ToRequest(input);

        await service.SaveAsync(
            id,
            request,
            actor.ActorId,
            ct);

        return NoContent();
    }

    #endregion

    #region Suppression

    [HttpDelete("{id:long}")]
    public async Task<IActionResult> Delete(
        long id,
        CancellationToken ct)
    {
        if (id <= 0)
        {
            return BadRequest(new
            {
                error = "Identifiant de question invalide."
            });
        }

        var deleted = await service.DeleteAsync(id, ct);

        return deleted
            ? NoContent()
            : NotFound();
    }

    #endregion
}