using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Text;
using AkibaQuiz.Contracts.Models;
using Microsoft.AspNetCore.Mvc;

namespace AkibaQuiz.Api.Controllers
{
    [ApiController]
    [Route("api/questions")]
    public sealed class QuestionsController : ControllerBase
    {
        private static readonly ConcurrentDictionary<int,QuestionAnswerDto> _questions = new ();

        private static int _nextId;

        [HttpGet]
        public ActionResult<IEnumerable<QuestionAnswerDto>> GetAll()
        {
            return Ok(_questions.Values.OrderBy(q => q.Id));
        }

        [HttpGet("{id:int}")]
        public ActionResult<QuestionAnswerDto> GetById(int id)
        {
            if (_questions.TryGetValue(id, out var question))
            {
                return Ok(question);
            }
            return NotFound();
        }

        [HttpPost]
        public ActionResult<QuestionAnswerDto> Create([FromBody] CreateQuestionRequest request)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var id = System.Threading.Interlocked.Increment(ref _nextId);

            var question = new QuestionAnswerDto
            {
                Id = id,
                Question = request.Question,
                Answer = request.Answer,
                Points = request.Points,
                TimeLimitSeconds = request.TimeLimitSeconds
            };
            _questions[id] = question;
            return CreatedAtAction(nameof(GetById), new { id }, question);
        }
    }
}
