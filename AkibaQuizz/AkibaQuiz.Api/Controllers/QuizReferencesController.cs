using AkibaQuiz.Api.Admin;
using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Application.Services;
using AkibaQuiz.Contracts;
using GraphQL;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using OrchardCore.Admin;
using System;
using System.Collections.Generic;
using System.ComponentModel.Design;
using System.Security.Cryptography.Xml;
using System.Text;

namespace AkibaQuiz.Api.Controllers
{

    [Microsoft.AspNetCore.Authorization.Authorize]
    public sealed class QuizReferencesController : Controller
    {
        private readonly Application.Interfaces.IReferenceService _referenceService;
        private readonly IAuthorizationService _authorizationService;

        public QuizReferencesController(Application.Interfaces.IReferenceService referenceService, IAuthorizationService authorizationService)
        {
            _referenceService = referenceService;
            _authorizationService = authorizationService;
        }

        [HttpGet]
        [Admin("AkibaQuiz/Studio/References")]
        public async Task<IActionResult> Index(CancellationToken ct)
        {
            if (!await _authorizationService.AuthorizeAsync(
                User,QuizPermissions.ManageQuizReferences))
            {
                return Forbid();
            }

            var model = new ReferenceAdminVm
            {
                Categories = await _referenceService.GetCategoriesAsync(ct),
                Tags = await _referenceService.GetTagsAsync(ct)
            };
            return View(model);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        [Admin("AkibaQuiz/Studio/CreateCategory")]
        public Task<IActionResult> CreateCategory(string name, CancellationToken ct)
        {
            return Execute(
                async () =>
                {
                    await _referenceService.CreateCategoryAsync(name, ct);
                },
                "Catégorie créée.");
        }


        [HttpPost]
        [ValidateAntiForgeryToken]
        [Admin("AkibaQuiz/Studio/RenameCategory")]
        public async Task<IActionResult> RenameCategory(long id, string name, CancellationToken ct)
        {
            await _referenceService.RenameCategoryAsync(id, name, ct);
            return Ok();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        [Admin("AkibaQuiz/Studio/DeleteCategory")]
        public Task<IActionResult> DeleteCategory(
        long id, CancellationToken ct)
        {
            return Execute(
                () => _referenceService.DeleteCategoryAsync(id, ct),
                "Catégorie supprimée.");
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        [Admin("AkibaQuiz/Studio/CreateTag")]
        public Task<IActionResult> CreateTag(
      string name, string? color,
      CancellationToken ct)
        {
            return Execute(
                async () =>
                    await _referenceService.CreateTagAsync(
                        name, color, ct),
                "Tag créé.");
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        [Admin("AkibaQuiz/Studio/UpdateTag")]
        public Task<IActionResult> UpdateTag(
            long id, string name, string? color,
            CancellationToken ct)
        {
            return Execute(
                () => _referenceService.UpdateTagAsync(
                    id, name, color, ct),
                "Tag modifié.");
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        [Admin("AkibaQuiz/Studio/DeleteTag")]
        public Task<IActionResult> DeleteTag(
            long id, CancellationToken ct)
        {
            return Execute(
                () => _referenceService.DeleteTagAsync(id, ct),
                "Tag supprimé.");
        }

        private async Task<IActionResult> Execute(
       Func<Task> operation,
       string successMessage)
        {
            try
            {
                await operation();
                TempData["ReferenceNotice"] = successMessage;
            }
            catch (ApiValidationException ex)
            {
                TempData["ReferenceError"] = ex.Message;
            }
            catch (ApiConflictException ex)
            {
                TempData["ReferenceError"] = ex.Message;
            }
            catch (KeyNotFoundException ex)
            {
                TempData["ReferenceError"] = ex.Message;
            }

            return RedirectToAction(
                nameof(Index),
                "QuizReferences",
                new { area = "AkibaQuiz.Api" });
        }

    }
}
