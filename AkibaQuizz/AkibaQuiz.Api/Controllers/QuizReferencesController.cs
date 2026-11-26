
using AkibaQuiz.Api.Admin;
using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Application.Services;
using AkibaQuiz.Contracts;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using OrchardCore.Admin;

namespace AkibaQuiz.Api.Controllers
{
    [Authorize]
    public sealed class QuizReferencesController : Controller
    {
        private readonly IReferenceService _referenceService;
        private readonly IAuthorizationService _authorizationService;

        public QuizReferencesController(
            IReferenceService referenceService,
            IAuthorizationService authorizationService)
        {
            _referenceService = referenceService;
            _authorizationService = authorizationService;
        }

        #region Catalogue

        [HttpGet]
        [Admin("AkibaQuiz/Studio/References")]
        public async Task<IActionResult> Index(
            CancellationToken ct)
        {
            if (!await CanManageReferencesAsync())
            {
                return Forbid();
            }

            var model = new ReferenceAdminVm
            {
                Categories =
                    await _referenceService.GetCategoriesAsync(ct),

                Tags =
                    await _referenceService.GetTagsAsync(ct)
            };

            return View(model);
        }

        #endregion

        #region Categories

        [HttpPost]
        [ValidateAntiForgeryToken]
        [Admin("AkibaQuiz/Studio/CreateCategory")]
        public async Task<IActionResult> CreateCategory(
            string name,
            CancellationToken ct)
        {
            if (!await CanManageReferencesAsync())
            {
                return Forbid();
            }

            return await Execute(
                async () =>
                {
                    await _referenceService
                        .CreateCategoryAsync(name, ct);
                },
                "Catégorie créée.");
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        [Admin("AkibaQuiz/Studio/RenameCategory")]
        public async Task<IActionResult> RenameCategory(
            long id,
            string name,
            CancellationToken ct)
        {
            if (!await CanManageReferencesAsync())
            {
                return Forbid();
            }

            await _referenceService
                .RenameCategoryAsync(id, name, ct);

            return Ok();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        [Admin("AkibaQuiz/Studio/DeleteCategory")]
        public async Task<IActionResult> DeleteCategory(
            long id,
            CancellationToken ct)
        {
            if (!await CanManageReferencesAsync())
            {
                return Forbid();
            }

            return await Execute(
                () => _referenceService
                    .DeleteCategoryAsync(id, ct),

                "Catégorie supprimée.");
        }

        #endregion

        #region Tags

        [HttpPost]
        [ValidateAntiForgeryToken]
        [Admin("AkibaQuiz/Studio/CreateTag")]
        public async Task<IActionResult> CreateTag(
            string name,
            string? color,
            CancellationToken ct)
        {
            if (!await CanManageReferencesAsync())
            {
                return Forbid();
            }

            return await Execute(
                async () =>
                    await _referenceService
                        .CreateTagAsync(name, color, ct),

                "Tag créé.");
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        [Admin("AkibaQuiz/Studio/UpdateTag")]
        public async Task<IActionResult> UpdateTag(
            long id,
            string name,
            string? color,
            CancellationToken ct)
        {
            if (!await CanManageReferencesAsync())
            {
                return Forbid();
            }

            return await Execute(
                () => _referenceService
                    .UpdateTagAsync(id, name, color, ct),

                "Tag modifié.");
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        [Admin("AkibaQuiz/Studio/DeleteTag")]
        public async Task<IActionResult> DeleteTag(
            long id,
            CancellationToken ct)
        {
            if (!await CanManageReferencesAsync())
            {
                return Forbid();
            }

            return await Execute(
                () => _referenceService
                    .DeleteTagAsync(id, ct),

                "Tag supprimé.");
        }

        #endregion

        #region Authorization

        private Task<bool> CanManageReferencesAsync()
        {
            return _authorizationService.AuthorizeAsync(
                User,
                QuizPermissions.ManageQuizReferences);
        }

        #endregion

        #region Helpers

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

        #endregion
    }
}
