using AkibaQuiz.Contracts;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;
using AkibaQuiz.Application.Interfaces;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Services
{
    public sealed class QuestionCatalogService : IQuestionCatalogService
    {
        private readonly IQuestionCatalogRepository _repository;
        public QuestionCatalogService(IQuestionCatalogRepository repository)
        {
            _repository = repository;
        }

        public Task<QuestionCatalogPage> SearchAsync(
       QuestionCatalogQuery query,
       CancellationToken ct)
        {
            ArgumentNullException.ThrowIfNull(query);

            query.Kind = string.IsNullOrWhiteSpace(query.Kind)
                ? "All"
                : query.Kind.Trim();

            if (query.Kind is not
                ("All" or "QuestionAnswer" or "QCM"))
            {
                throw new ApiValidationException(
                    "Type de question invalide.");
            }

            if (query.Page < 1)
                throw new ApiValidationException(
                    "Le numéro de page doit être supérieur à zéro.");

            if (query.PageSize is < 1 or > 100)
                throw new ApiValidationException(
                    "La taille de page doit être comprise entre 1 et 100.");

            if (query.CategoryId is <= 0)
                throw new ApiValidationException(
                    "Identifiant de catégorie invalide.");

            if (query.TagId is <= 0)
                throw new ApiValidationException(
                    "Identifiant de tag invalide.");

            query.Text = query.Text?.Trim();

            if (query.Text?.Length > 160)
                throw new ApiValidationException(
                    "La recherche ne peut pas dépasser 160 caractères.");

            if (string.IsNullOrEmpty(query.Text))
                query.Text = null;

            return _repository.SearchAsync(query, ct);
        }

        public Task<IReadOnlyList<QuestionLabelModel>>
    GetLabelsByIdsAsync(
        IEnumerable<long> questionIds,
        IEnumerable<long> qcmIds,
        CancellationToken ct)
        {
            return _repository.GetLabelsByIdsAsync(
                questionIds,
                qcmIds,
                ct);
        }
    }
}
