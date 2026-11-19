using AkibaQuiz.Api.Admin;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.Sqlite;
using OrchardCore.Admin;
using OrchardCore.Media;
using System;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Security.Cryptography.Xml;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using YesSql.Services;
using static Azure.Core.HttpHeader;

namespace AkibaQuiz.Api.Controllers
{
    [Authorize(Roles = "Administrator")]
    public sealed class QuizStudioController : Controller
    {
        private readonly IQuestionService _questionService;
        private readonly IQcmService _qcmService;
        private readonly IGameService _gameService;
        private readonly IMediaCatalogService _mediaCatalogService;

        private readonly IMediaFileStore _mediaFileStore;

        private readonly IReferenceService _referenceService;

        public QuizStudioController(IQuestionService questionService, IQcmService qcmService, IGameService gameService, IReferenceService referenceService, IMediaCatalogService mediaCatalogService, IMediaFileStore mediaFileStore)
        {
            _questionService = questionService;
            _qcmService = qcmService;
            _referenceService = referenceService;
            _gameService = gameService;
            _mediaCatalogService = mediaCatalogService;
            _mediaFileStore = mediaFileStore;
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

            try
            {
                // Récupérer les associations déjà enregistrées
                // uniquement pour la question en cours de modification.
                var previousQuestion = input.Id.HasValue
                    ? await _questionService.GetByIdAsync(input.Id.Value, ct)
                    : null;

                if (input.Id.HasValue && previousQuestion is null)
                    return NotFound();

                // Transformer les sélections Orchard en IdMedia.
                var mediaAssociations = await ResolveMediaSelectionsAsync(
                    input.MediaAssociationsJson,
                    previousQuestion?.Medias ?? [],
                    ct);

                var request = new SaveQuestionAnswerRequest
                {
                    Question = input.Question,
                    Answer = input.Answer,
                    IdCategory = input.IdCategory,
                    TagIds = tagIds,

                    Medias = mediaAssociations
                };

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

            var previousQcm = input.Id.HasValue
                ? await _qcmService.GetByIdAsync(input.Id.Value, ct)
                : null;

            if (input.Id.HasValue && previousQcm is null)
                return NotFound();

            var mediaAssociations = await ResolveMediaSelectionsAsync(
                input.MediaAssociationsJson,
                previousQcm?.Medias ?? [],
                ct);

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
                Medias = mediaAssociations
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
                TypeQuestion = "QuestionAnswer",
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
                model.Revision = ComputeGameRevision(await _gameService.GetByIdAsync(id.Value, ct));

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
                    model.Rounds.Add(gRound);
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
            return View(model);
        }

        [Admin("AkibaQuiz/Studio/SaveGame")]
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> SaveGame([FromForm] GameSaveFormVm gameSave, CancellationToken ct)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);
            if (gameSave.Id is <= 0)
                return BadRequest(new { error = "Id invalide." });

            if (string.IsNullOrWhiteSpace(gameSave.Payload))
            {

                return BadRequest(new
                {
                    error = "Payload invalide.",
                    champsRecus = Request.Form.Keys.ToArray()
                });
            }

            SaveGameRequest? input;

            try
            {
                input = JsonSerializer.Deserialize<SaveGameRequest>(gameSave.Payload,
                    new JsonSerializerOptions(JsonSerializerDefaults.Web));
            }
            catch (JsonException)
            {
                return BadRequest(new { error = "Payload invalide." });
            }

            if (input is null)
            {
                return BadRequest(new
                {
                    error = "Aucune composition de Game reçue."
                });
            }

            var name = input?.Name?.Trim() ?? "";

            if (input.Name.Length < 2)
            {
                return BadRequest(new { error = "Le nom du jeu doit contenir au moins 2 caractères." });
            }

            if (input?.Rounds is null || input.Rounds.Count == 0)
                return BadRequest(new { error = "Le jeu doit contenir au moins un tour." });
            if (gameSave.Id.HasValue)
            {
                if (string.IsNullOrWhiteSpace(gameSave.Revision))
                    return BadRequest(new { error = "Revision invalide." });

                var existing = await _gameService.GetByIdAsync(gameSave.Id.Value, ct);
                if (existing is null)
                    return NotFound();


                if (!string.Equals(ComputeGameRevision(existing),
                    gameSave.Revision, StringComparison.OrdinalIgnoreCase))
                {
                    return Conflict(new { error = "Le jeu a été modifié par un autre utilisateur. Veuillez recharger la page et réessayer." });
                }
            }

            var validQuestions = (await _questionService.GetAllAsync(ct)).Select(q => q.Id).ToHashSet();
            var validQcms = (await _qcmService.GetAllAsync(ct)).Select(q => q.Id).ToHashSet();

            var request = new SaveGameRequest
            {
                Name = name
            };

            for (int i = 0; i < input.Rounds.Count; i++)
            {
                var round = input.Rounds[i];

                if (round is null ||
                    round.Position != i + 1 ||
                    round.Questions is null ||
                    round.Questions.Count == 0)
                {
                    return BadRequest(new { error = $"Le tour {i + 1} est invalide." });
                }

                var newRound = new SaveGameRoundRequest { Position = i + 1 };

                var seen = new HashSet<(string Type, long Id)>();

                for (int j = 0; j < round.Questions.Count; j++)
                {
                    var question = round.Questions[j];

                    if (question is null ||
                        question.Position != j + 1)
                    {
                        return BadRequest(new { error = $"La question {j + 1} du tour {i + 1} est invalide." });
                    }

                    bool isQa = question.IdQuestionAnswer is > 0;
                    bool isQcm = question.IdQCMQuestion is > 0;

                    if (isQa == isQcm ||
                        question.IdQuestionAnswer is <= 0 ||
                        question.IdQCMQuestion is <= 0)
                    {
                        return BadRequest(new { error = $"La question {j + 1} du tour {i + 1} doit être soit une question à réponse ouverte, soit une question QCM." });
                    }

                    string type = isQa ? "QuestionAnswer" : "QCM";

                    long id = isQa ? question.IdQuestionAnswer!.Value : question.IdQCMQuestion!.Value;

                    if (!seen.Add((type, id)))
                    {
                        return BadRequest(new { error = $"La question {j + 1} du tour {i + 1} est dupliquée." });
                    }

                    if (isQa && !validQuestions.Contains(id))
                    {
                        return BadRequest(new { error = $"La question {j + 1} du tour {i + 1} est invalide." });
                    }

                    if (isQcm && !validQcms.Contains(id))
                    {
                        return BadRequest(new { error = $"La question {j + 1} du tour {i + 1} est invalide." });
                    }

                    newRound.Questions.Add(
                        new SaveRoundQuestionRequest
                        {
                            Position = j + 1,
                            IdQuestionAnswer = isQa ? id : (long?)null,
                            IdQCMQuestion = isQcm ? id : (long?)null
                        });
                }
                request.Rounds.Add(newRound);
            }
            try
            {
                var saved = await _gameService.SaveAsync(
                            gameSave.Id,
                            request,
                            User.Identity?.Name ?? "Administrator",
                            ct);

                return Ok(new
                {
                    id = saved.Id,
                    redirectUrl = Url.Action(
                        "GameEditor",
                        "QuizStudio",
                        new
                        {
                            area = "AkibaQuiz.Api",
                            id = saved.Id
                        })
                });
            }
            catch (ApiValidationException ex)
            {
                return BadRequest(new { error = ex.Message });
            }
            catch (ApiConflictException ex)
            {
                return Conflict(new { error = ex.Message });
            }
            catch (KeyNotFoundException)
            {
                return NotFound(new
                {
                    error = "Le Game n'existe plus."
                });
            }
            catch (SqliteException ex) when (ex.SqliteErrorCode == 19)
            {
                return Conflict(new
                {
                    error = "Contrainte SQLite : une référence n'est plus valide."
                });
            }
        }


        #endregion

        private async Task<List<SaveMediaAssociationRequest>>
    ResolveMediaSelectionsAsync(
        string? json,
        IReadOnlyList<QuizMediaModel> existingMedias,
        CancellationToken ct)
        {
            if (string.IsNullOrWhiteSpace(json))
                throw new ApiValidationException(
                    "La liste des médias est absente.");

            List<MediaSelectionVm>? selected;

            try
            {
                selected = JsonSerializer.Deserialize<List<MediaSelectionVm>>(
                    json,
                    new JsonSerializerOptions(JsonSerializerDefaults.Web));
            }
            catch (JsonException)
            {
                throw new ApiValidationException(
                    "Le JSON des médias est invalide.");
            }

            if (selected is null || selected.Count > 30)
                throw new ApiValidationException(
                    "Liste de médias invalide (maximum 30 associations).");

            var allowedPhases = new HashSet<string>(
                StringComparer.Ordinal)
    {
        "BeforeQuestion",
        "DuringQuestion",
        "BeforeAnswer",
        "DuringAnswer",
        "AfterAnswer"
    };

            var previousIds = existingMedias
                .Select(m => m.IdMedia)
                .ToHashSet();

            // Première passe : vérifier toutes les entrées
            // avant de créer une référence dans Medias.
            var validated = new List<(MediaSelectionVm Item, string? Kind)>();

            foreach (var item in selected)
            {
                if (item is null)
                    throw new ApiValidationException(
                        "Association média invalide.");

                bool originalPhase = item.IdMedia is > 0 &&
                    existingMedias.Any(m =>
                        m.IdMedia == item.IdMedia &&
                        m.TypeDisplay == item.TypeDisplay);

                if (!allowedPhases.Contains(item.TypeDisplay) &&
                    !originalPhase)
                {
                    throw new ApiValidationException(
                        $"Phase média inconnue : {item.TypeDisplay}");
                }

                if (item.IdMedia.HasValue)
                {
                    if (item.IdMedia.Value <= 0 ||
                        !previousIds.Contains(item.IdMedia.Value))
                    {
                        throw new ApiValidationException(
                            "Référence média existante non autorisée.");
                    }

                    validated.Add((item, null));
                    continue;
                }

                var path = item.Path?.Trim() ?? "";

                // Accepter uniquement les chemins relatifs Orchard.
                if (string.IsNullOrWhiteSpace(path) ||
                    path.Length > 512 ||
                    path.Contains('\\') ||
                    path.Contains(':') ||
                    path.Contains('?') ||
                    path.Contains('#') ||
                    path.Split('/').Any(
                        part => part is "" or "." or ".."))
                {
                    throw new ApiValidationException(
                        "Chemin média Orchard invalide.");
                }

                string kind = Path.GetExtension(path)
                    .ToLowerInvariant() switch
                {
                    ".png" or ".jpg" or ".jpeg"
                        or ".gif" or ".webp" => "Image",

                    ".mp3" or ".ogg" or ".wav"
                        or ".m4a" => "Audio",

                    ".mp4" or ".webm" or ".mov" => "Video",

                    _ => throw new ApiValidationException(
                        "Format média non pris en charge.")
                };

                var file = await _mediaFileStore.GetFileInfoAsync(path);

                if (file is null || file.IsDirectory)
                    throw new ApiValidationException(
                        $"Fichier Orchard introuvable : {path}");

                item.Path = path;
                validated.Add((item, kind));
            }

            // Deuxième passe : résoudre les identifiants métier.
            var result = new List<SaveMediaAssociationRequest>();
            var seen = new HashSet<(long Id, string Phase)>();

            foreach (var (item, kind) in validated)
            {
                long idMedia = item.IdMedia ??
                    await _mediaCatalogService.ResolveOrCreateAsync(
                        item.Path!,
                        kind!,
                        ct);

                if (!seen.Add((idMedia, item.TypeDisplay)))
                {
                    throw new ApiValidationException(
                        "Le même média est associé deux fois " +
                        "à la même phase.");
                }

                result.Add(new SaveMediaAssociationRequest
                {
                    IdMedia = idMedia,
                    TypeDisplay = item.TypeDisplay
                });
            }

            return result;
        }



        private static string ComputeGameRevision(GameModel game)
        {
            var snapshot = new
            {
                game.Id,
                game.Name,
                Rounds = game.Rounds
                .OrderBy(r => r.Position)
                .ThenBy(r => r.Id)
                .Select(r => new
                {
                    r.Id,
                    r.Position,
                    Questions = r.Questions
                    .OrderBy(q => q.Position)
                    .ThenBy(q => q.Id)
                    .Select(q => new
                    {
                        q.Id,
                        q.Position,
                        q.IdQuestionAnswer,
                        q.IdQCMQuestion
                    })
                    .ToArray()
                })

            };
            var json = System.Text.Json.JsonSerializer.Serialize(snapshot);
            var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(json));

            return Convert.ToHexString(bytes);
        }
    }
}