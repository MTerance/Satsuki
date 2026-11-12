using AkibaQuiz.Api.Admin;
using AkibaQuiz.Application.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using OrchardCore.Admin;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Controllers
{
    [Authorize(Roles = "Administrator")]
    public sealed class QuizStudioController : Controller
    {
        private readonly IQuestionService _questionService;
        private readonly IQcmService _qcmService;
        private readonly IGameService _gameService;

        public QuizStudioController(IQuestionService questionService, IQcmService qcmService, IGameService gameService)
        {
            _questionService = questionService;
            _qcmService = qcmService;
            _gameService = gameService;
        }

        [HttpGet]
        [Admin("AkibaQuiz/Studio/Index")]
        public async Task<IActionResult> Index(CancellationToken ct)
        {
            var questions = await _questionService.GetAllAsync(ct);
            var qcms = await _qcmService.GetAllAsync(ct);
            var games = await _gameService.GetAllAsync(ct);

            var model = new QuizStudioIndexVm
            {
                Questions = questions.Select(q => new QuestionRowVm
                {
                    Id = q.Id,
                    Question = q.Question,
                    Category = q.CategoryName ?? ""
                }).ToList(),
                Qcms = qcms.Select(q => new QcmRowVm
                {
                    Id = q.Id,
                    Question = q.Question,
                    AnswerCount = q.Answers.Count
                }).ToList(),
                Games = games.Select(g => new GameRowVm
                {
                    Id = g.Id,
                    Name = g.Name,
                    RoundCount = g.Rounds.Count,
                    QuestionCount = g.Rounds.Sum(r => r.Questions.Count)
                }).ToList()
            };
            return View(model);
        }
    }
}