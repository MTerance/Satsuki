
using AkibaQuiz.Api.Mapping;
using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts.Requests;
using Microsoft.AspNetCore.Mvc;

namespace AkibaQuiz.Api.Controllers;

[ApiController]
[Route("api/admin/qcm")]
[IgnoreAntiforgeryToken]
[TypeFilter(typeof(AdminApiKeyFilter))]
[TypeFilter(typeof(ApiExceptionFilter))]
public sealed class QcmController(
    IQcmService service,
    IAuditActorProvider auditActorProvider)
    : ControllerBase
{
    #region Lecture

    [HttpGet]
    public async Task<IActionResult> GetAll(
        CancellationToken ct)
    {
        var items = await service.GetAllAsync(ct);

        return Ok(
            items.Select(QuizApiMapper.ToAdminDto).ToList());
    }

    [HttpGet("{id:long}")]
    public async Task<IActionResult> GetById(
        long id,
        CancellationToken ct)
    {
        if (id <= 0)
        {
            return BadRequest(new
            {
                error = "Identifiant de QCM invalide."
            });
        }

        var item = await service.GetByIdAsync(id, ct);

        return item is null
            ? NotFound()
            : Ok(QuizApiMapper.ToAdminDto(item));
    }

    #endregion

    #region Creation

    [HttpPost]
    public async Task<IActionResult> Create(
        [FromBody] SaveQcmRequest input,
        CancellationToken ct)
    {
        var actor = auditActorProvider.GetCurrent();

        var model = await service.SaveAsync(
            null,
            input,
            actor.ActorId,
            ct);

        var dto = QuizApiMapper.ToAdminDto(model);

        return CreatedAtAction(
            nameof(GetById),
            new { id = dto.Id },
            dto);
    }

    #endregion

    #region Modification

    [HttpPut("{id:long}")]
    public async Task<IActionResult> Update(
        long id,
        [FromBody] SaveQcmRequest input,
        CancellationToken ct)
    {
        if (id <= 0)
        {
            return BadRequest(new
            {
                error = "Identifiant de QCM invalide."
            });
        }

        var actor = auditActorProvider.GetCurrent();

        await service.SaveAsync(
            id,
            input,
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
                error = "Identifiant de QCM invalide."
            });
        }

        var deleted = await service.DeleteAsync(id, ct);

        return deleted
            ? NoContent()
            : NotFound();
    }

    #endregion
}