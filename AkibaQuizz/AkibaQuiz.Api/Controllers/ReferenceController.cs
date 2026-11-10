using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Controllers
{
    [ApiController]
    [Route("api/admin/references")]
    [TypeFilter(typeof(AdminApiKeyFilter))]
    public sealed class ReferencesController(IReferenceRepository repo) : ControllerBase
    {
        [HttpGet("categories")] 
        public async Task<IActionResult> Categories(CancellationToken ct) => Ok(await repo.Categories(ct));
        [HttpGet("tags")] 
        public async Task<IActionResult> Tags(CancellationToken ct) => Ok(await repo.Tags(ct));
    }

}
