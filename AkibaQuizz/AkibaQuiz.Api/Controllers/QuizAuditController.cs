using AkibaQuiz.Api.Admin;
using AkibaQuiz.Api.Security;
using AkibaQuiz.Application.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using OrchardCore.Admin;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Controllers
{
    [Authorize]
    public sealed class QuizAuditController(
        IAuditEventReader auditEventReader,
        IAuthorizationService authorization)
        : Controller
    {
        [HttpGet]
        [Admin(
            "AkibaQuiz/Studio/Audit",
            "AkibaQuizAuditIndex")]
        public async Task<IActionResult> Index(
            [FromQuery] AuditIndexQueryVm query,
            CancellationToken ct)
        {
            // 1. Autorisation Orchard côté serveur.
            if (!await authorization.AuthorizeAsync(
                User,
                QuizPermissions.ViewQuizAudit))
            {
                return Forbid();
            }

            // 2. Vérifier le model binding HTTP.
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            // 3. Valider la pagination.
            if (query.Page < 1 ||
                query.PageSize is < 1 or > 100)
            {
                return BadRequest("Pagination invalide.");
            }

            // 4. Vérifier les valeurs des filtres.
            if (!string.IsNullOrEmpty(query.EntityType) &&
                query.EntityType is not
                    ("QuestionAnswer" or "QCM" or
                     "Game" or "Category" or "Tag"))
            {
                return BadRequest(
                    "Type d'entité invalide.");
            }

            if (!string.IsNullOrEmpty(query.Action) &&
                query.Action is not
                    ("Create" or "Update" or "Delete"))
            {
                return BadRequest("Action invalide.");
            }

            if (!string.IsNullOrEmpty(query.ActorType) &&
                query.ActorType is not
                    ("OrchardUser" or "AdminApi" or "System"))
            {
                return BadRequest(
                    "Type d'auteur invalide.");
            }

            if (query.EntityId is <= 0)
            {
                return BadRequest(
                    "Identifiant d'entité invalide.");
            }

            if (query.ActorId?.Length > 128 ||
                query.CorrelationId?.Length > 128)
            {
                return BadRequest(
                    "Critère de recherche trop long.");
            }

            // 5. Contrôler la période.
            if (query.DateFrom > query.DateTo ||
                query.DateTo == DateOnly.MaxValue)
            {
                return BadRequest("Période invalide.");
            }

            // 6. Convertir les paramètres HTTP
            // en critères de lecture Application.
            var filter = query.ToFilter();

            var page = await auditEventReader.SearchAsync(
                filter,
                ct);

            // 7. Corriger une page devenue hors limites.
            if (page.TotalPages > 0 &&
                query.Page > page.TotalPages)
            {
                query.Page = (int)page.TotalPages;

                page = await auditEventReader.SearchAsync(
                    query.ToFilter(),
                    ct);
            }
            else if (page.TotalPages == 0 && query.Page != 1)
            {
                query.Page = 1;

                page = await auditEventReader.SearchAsync(
                    query.ToFilter(),
                    ct);
            }

            // 8. Construire le ViewModel Razor.
            return View(new QuizAuditIndexVm
            {
                Filters = query,
                Results = page
            });
        }
    }
}
