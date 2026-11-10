using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts.Requests;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace AkibaQuiz.Api.Controllers
{
    [ApiController]
    [Route("api/admin/qcm")]
    [IgnoreAntiforgeryToken]
    [TypeFilter(typeof(AdminApiKeyFilter))]
    [TypeFilter(typeof(ApiExceptionFilter))]
    public class QcmController : ControllerBase
    {
        private readonly IQcmService qcmService;

        public QcmController(IQcmService qcmService)
        {
            this.qcmService = qcmService;
        }

        [HttpGet]
        public async Task<IActionResult> GetAll(CancellationToken ct)
        {
            var result = await qcmService.GetAllAsync(ct);
            return Ok(result);
        }
        
        [HttpGet("{id:long}")]
        public async Task<IActionResult> GetById(long id, CancellationToken ct)
        {
            var result = await qcmService.GetByIdAsync(id, ct);
            if (result == null)
                return NotFound();
            return Ok(result);
        }

        [HttpPost]
        public async Task<IActionResult> Create([FromBody] SaveQcmRequest request, CancellationToken ct)
        {
            var result = await qcmService.CreateAsync(request, User.Identity?.Name ?? "anonymous", ct);
            return CreatedAtAction(nameof(GetById), new { id = result.Id }, result);
        }

        [HttpPut("{id:long}")]
        public async Task<IActionResult> Update(long id, [FromBody] SaveQcmRequest request, CancellationToken ct)
        {
            var success = await qcmService.UpdateAsync(id, request, ct);
            if (!success)
                return NotFound();
            return NoContent();
        }

        [HttpDelete("{id:long}")]
        public async Task<IActionResult> Delete(long id, CancellationToken ct)
        {
            var success = await qcmService.DeleteAsync(id, ct);
            if (!success)
                return NotFound();
            return NoContent();
        }
    }
}
