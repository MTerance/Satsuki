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
public sealed class QcmController(IQcmService service) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> GetAll(CancellationToken ct)
        => Ok((await service.GetAllAsync(ct)).Select(QuizApiMapper.ToAdminDto).ToList());

    [HttpGet("{id:long}")]
    public async Task<IActionResult> GetById(long id, CancellationToken ct)
    {
        var item = await service.GetByIdAsync(id, ct);
        return item is null ? NotFound() : Ok(QuizApiMapper.ToAdminDto(item));
    }

    // Le endpoint courant prend SaveQcmRequest, pas QcmWrite.
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] SaveQcmRequest input, CancellationToken ct)
    {
        var model = await service.SaveAsync(null, input, User.Identity?.Name ?? "anonymous", ct);
        var dto = QuizApiMapper.ToAdminDto(model);
        return CreatedAtAction(nameof(GetById), new { id = dto.Id }, dto);
    }

    [HttpPut("{id:long}")]
    public async Task<IActionResult> Update(long id, [FromBody] SaveQcmRequest input, CancellationToken ct)
    {
        await service.SaveAsync(id, input, User.Identity?.Name ?? "anonymous", ct);
        return NoContent();
    }

    [HttpDelete("{id:long}")]
    public async Task<IActionResult> Delete(long id, CancellationToken ct)
        => await service.DeleteAsync(id, ct) ? NoContent() : NotFound();
}
