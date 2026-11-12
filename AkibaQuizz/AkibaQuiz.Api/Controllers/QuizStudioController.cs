using AkibaQuiz.Api.Admin;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts;
using AkibaQuiz.Contracts.Requests;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using OrchardCore.Admin;
using System;
using System.Collections.Generic;
using System.Security.Cryptography.Xml;
using System.Text;

namespace AkibaQuiz.Api.Controllers
{
    [Authorize(Roles = "Administrator")]
    public sealed class QuizStudioController : Controller
    {
        private readonly IQuestionService _questionService;
        private readonly IQcmService _qcmService;
        private readonly IGameService _gameService;

        private readonly IReferenceService _referenceService;

        public QuizStudioController(IQuestionService questionService, IQcmService qcmService, IGameService gameService, IReferenceService referenceService)
        {
            _questionService = questionService;
            _qcmService = qcmService;
            _referenceService = referenceService;
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

        [HttpGet]
        [Admin("AkibaQuiz/Studio/QuestionEditor")]
        public async Task<IActionResult> QuestionEditor(long? id, CancellationToken ct)
        {
            var categories = await _referenceService.GetCategoriesAsync(ct);
            var tags = await _referenceService.GetTagsAsync(ct);
            if (id.HasValue)
            {
                var question = await _questionService.GetByIdAsync(id.Value, ct);
                if (question == null)
                {
                    return NotFound();
                }
                var model = new QuestionEditorVm
                {
                    Id = question.Id,
                    Question = question.Question,
                    Answer = question.Answer,
                    IdCategory = question.IdCategory,
                    TagsId = question.Tags.Select(t => t.Id).ToList(),
                    Categories = categories,
                    AvailablesTags = tags,
                    ExistingMedia = question.Medias
                };
                return View(model);
            }
            else
            {
                var model = new QuestionEditorVm
                {
                    Categories = categories,
                    AvailablesTags = tags
                };
                return View(model);
            }
        }

        [Admin("AkibaQuiz/Studio/SaveQuestion")]
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> SaveQuestion(QuestionEditorVm input, CancellationToken ct)
        {
            input.Question = input.Question?.Trim() ?? "";
            input.Answer = input.Answer?.Trim() ?? "";

            if (string.IsNullOrWhiteSpace(input.Question) ||
                input.Question.Length < 3)
            {
                ModelState.AddModelError(
                    nameof(input.Question),
                    "L'énoncé doit contenir au moins 3 caractères.");
            }

            if (string.IsNullOrWhiteSpace(input.Answer))
            {
                ModelState.AddModelError(
                    nameof(input.Answer),
                    "La réponse est obligatoire.");
            }

            if (input.Id is <= 0)
                return BadRequest();

            input.Categories = await _referenceService
                .GetCategoriesAsync(ct);

            input.AvailablesTags = await _referenceService
                .GetTagsAsync(ct);

            if (!input.Categories.Any(c => c.Id == input.IdCategory))
            {
                ModelState.AddModelError(
                    nameof(input.IdCategory),
                    "Catégorie inexistante.");
            }

            var tagIds = (input.TagsId ?? [])
                .Distinct()
                .ToList();

            if (tagIds.Any(id =>
                !input.AvailablesTags.Any(t => t.Id == id)))
            {
                ModelState.AddModelError(
                    nameof(input.TagsId),
                    "Un ou plusieurs tags sont invalides.");
            }

            var existing = input.Id.HasValue
                ? await _questionService.GetByIdAsync(input.Id.Value, ct)
                : null;

            if (input.Id.HasValue && existing is null)
                return NotFound();

            input.ExistingMedia = existing?.Medias ?? [];

            if (!ModelState.IsValid)
                return View("QuestionEditor", input);

            var request = new SaveQuestionAnswerRequest
            {
                Question = input.Question,
                Answer = input.Answer,
                IdCategory = input.IdCategory,
                TagIds = tagIds,

                Medias = input.ExistingMedia
                    .Select(m => new SaveMediaAssociationRequest
                    {
                        IdMedia = m.IdMedia,
                        TypeDisplay = m.TypeDisplay
                    })
                    .ToList()
            };

            try
            {
                await _questionService.SaveAsync(
                    input.Id,
                    request,
                    User.Identity?.Name ?? "Administrator",
                    ct);

                TempData["Notice"] = "Question enregistrée.";

                return RedirectToAction(nameof(Index));
            }
            catch (ApiValidationException ex)
            {
                ModelState.AddModelError("", ex.Message);
            }
            catch (ApiConflictException ex)
            {
                ModelState.AddModelError("", ex.Message);
            }

            return View("QuestionEditor", input);
        }
    }
}