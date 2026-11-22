using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts.Requests;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Controllers
{
    [ApiController]
    [Route("api/admin/question-catalog")]
    [TypeFilter(typeof(AdminApiKeyFilter))]
    [TypeFilter(typeof(ApiExceptionFilter))]
    public sealed class QuestionCatalogController(
        IQuestionCatalogService catalog)
        : ControllerBase
    {
        [HttpGet]
        public async Task<IActionResult> Search(
            [FromQuery] QuestionCatalogQuery query,
            CancellationToken ct)
        {
            var result = await catalog.SearchAsync(
                query, ct);

            return Ok(result);
        }
    }
}
