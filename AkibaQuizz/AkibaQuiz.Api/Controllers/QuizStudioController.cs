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
using YesSql.Services;

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

        #region Question Editor

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
        #endregion

        #region QCM Editor

        [Admin("AkibaQuiz/Studio/QcmEditor")]
        [HttpGet]
        public async Task<IActionResult> QcmEditor(long? id, CancellationToken ct)
        {
            var tags = await _referenceService.GetTagsAsync(ct);
            var categories = await _referenceService.GetCategoriesAsync(ct);
            var model = new QcmEditorVm();

            if (id.HasValue)
            {
                var qcm = await _qcmService.GetByIdAsync(id.Value, ct);
                if (qcm == null)
                {
                    return NotFound();
                }
                model = new QcmEditorVm
                {
                    Id = qcm.Id,
                    Question = qcm.Question,
                    Answers = qcm.Answers.Select(a => new QcmAnswerEditorVm
                    {
                        Answer = a.Answer,
                        IsTrue = a.IsTrue
                    }).ToList(),
                    IdCategory = qcm.IdCategory,
                    TagIds = qcm.Tags.Select(t => t.Id).ToList(),
                    AvailablesTags = tags,
                    ExistingMedias = qcm.Medias
                };
            }
            await FillQcmReferenceAsync(model, ct);
            return View(model);
        }

        [Admin("AkibaQuiz/Studio/SaveQcm")]
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> SaveQcm(QcmEditorVm input, CancellationToken ct)
        {
            input.Question = input.Question?.Trim() ?? "";
            if (string.IsNullOrWhiteSpace(input.Question) ||
                input.Question.Length < 3)
            {
                ModelState.AddModelError(
                    nameof(input.Question),
                    "L'énoncé doit contenir au moins 3 caractères.");
            }
            if (input.Answers.Count < 2)
            {
                ModelState.AddModelError(
                    nameof(input.Answers),
                    "Au moins deux réponses sont requises.");
            }
            if (!input.Answers.Any(a => a.IsTrue))
            {
                ModelState.AddModelError(
                    nameof(input.Answers),
                    "Au moins une réponse correcte est requise.");
            }
            await FillQcmReferenceAsync(input, ct);
            if (!ModelState.IsValid)
                return View("QcmEditor", input);
            var request = new SaveQcmRequest
            {
                Question = input.Question,
                Answers = input.Answers.Select(a => new SaveQcmPropositionRequest
                {
                    Answer = a.Answer,
                    IsTrue = a.IsTrue
                }).ToList(),
                IdCategory = input.IdCategory,
                TagIds = input.TagIds.Distinct().ToList(),
                Medias = input.ExistingMedias.Select(m => new SaveMediaAssociationRequest
                {
                    IdMedia = m.IdMedia,
                    TypeDisplay = m.TypeDisplay
                }).ToList()
            };
            try
            {
                await _qcmService.SaveAsync(
                    input.Id,
                    request,
                    User.Identity?.Name ?? "Administrator",
                    ct);
                TempData["Notice"] = "QCM enregistré.";
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
            return View("QcmEditor", input);
        }

        private async Task FillQcmReferenceAsync(QcmEditorVm model, CancellationToken ct)
        {
            model.AvailablesTags = await _referenceService.GetTagsAsync(ct);
            model.Categories = await _referenceService.GetCategoriesAsync(ct);

            while (model.Answers.Count < 4)
            {
                model.Answers.Add(new QcmAnswerEditorVm());
            }
        }

        #endregion

        #region Game Editor


        [Admin("AkibaQuiz/Studio/GameEditor")]
        [HttpGet]
        public async Task<IActionResult> GameEditor(long? id, CancellationToken ct)
        {
            var model = new GameEditorVm();

            var questions = await _questionService.GetAllAsync(ct);
            var qcms = await _qcmService.GetAllAsync(ct);

            model.QuestionBank = questions.Select(q => new GameQuestionBankItemVm
            {
                Id = q.Id,
                TypeQuestion = "Question",
                Label = q.Question
            }).Concat(qcms.Select(q => new GameQuestionBankItemVm
            {
                Id = q.Id,
                TypeQuestion = "QCM",
                Label = q.Question
            }))
            .OrderBy(q => q.TypeQuestion)
            .ThenBy(q => q.Label)
            .ToList();

            var questionById = questions.ToDictionary(q => q.Id);
            var qcmById = qcms.ToDictionary(q => q.Id);

            if (id.HasValue)
            {
                var full = await _gameService.GetFullAsync(id.Value, ct);

                if (full is null)
                    return NotFound();

                model.Id = full.Game.Id;
                model.Name = full.Game.Name;

                foreach (var round in full.Rounds.OrderBy(r => r.Position).ThenBy(r => r.Id))
                {
                    var gRound = new GameRoundEditorVm
                    {
                        Id = round.Id,
                        Position = model.Rounds.Count + 1
                    };

                    foreach (var entry in round.Questions
                        .OrderBy(q => q.Position)
                        .ThenBy(q => q.Id))
                    {
                        bool isQuestion = entry.IdQuestionAnswer is > 0;
                        bool isQcm = entry.IdQCMQuestion is > 0;
                        if ((!isQuestion && !isQcm) || (isQuestion && isQcm))
                        {
                            return Conflict($"Type de question inconnu : {entry.Id}");
                        }
                        string type;
                        long questionId;
                        string label;

                        if (isQuestion)
                        {
                            questionId = entry.IdQuestionAnswer!.Value;
                            if (!questionById.TryGetValue(questionId, out var q))
                            {
                                return Conflict(
                                    $"QuestionAnswer #{questionId} introuvable.");
                            }
                            type = "QuestionAnswer";
                            label = q.Question;
                        }
                        else
                        {
                            questionId = entry.IdQCMQuestion!.Value;
                            if (!qcmById.TryGetValue(questionId, out var q))
                            {
                                return Conflict(
                                    $"QCM #{questionId} introuvable.");
                            }
                            type = "QCM";
                            label = q.Question;
                        }
                        gRound.Questions.Add(new GameQuestionEditorVm
                        {
                            Id = entry.Id,
                            Position = entry.Position,
                            TypeQuestion = type,
                            QuestionId = isQuestion ? questionId : (long?)null,
                            QcmQuestionId = isQcm ? questionId : (long?)null,
                            Label = label
                        });
                    }
                }
            }
            if (model.Rounds.Count == 0)
            {
                model.Rounds.Add(new GameRoundEditorVm
                {
                    Position = 1,
                    QuestionCount = 0
                });
            }
            Console.WriteLine(
                $"GameEditor : Game={model.Id}, " +
                $"Manches={model.Rounds.Count}, " +
                $"Questions={model.Rounds.Sum(r => r.Questions.Count)}");
            return View(model);
        }
        #endregion
    }
}