using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Entities;
using AkibaQuiz.Contracts.Requests;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Data;
using System.Net.Http.Headers;

namespace AkibaQuiz.Application.Services
{
    public class QcmService(IQcmRepository repository) : IQcmService
    {
        public async Task<IReadOnlyList<QcmModel>> GetAllAsync(CancellationToken ct)
        {
            var questions = await repository.GetAllAsync(ct);
            var result = new List<QcmModel>();

            foreach (var question in questions)
            {
                result.Add(await BuildModelAsync(question,ct));
            }
            return result;
        }

        public async Task<QcmModel?> GetByIdAsync(long id, CancellationToken ct)
        {
            var question = await repository.GetQuestionAsync(id, ct);
            if (question == null)
                return null;
            return await BuildModelAsync(question, ct);
        }

        public async Task<QcmModel> CreateAsync(SaveQcmRequest request,string author, CancellationToken ct)
        {
            Validate(request);

            var id = await repository.CreateAsync(request, author, ct);
            return (await GetByIdAsync(id, ct))!;
        }

        public async Task<bool> UpdateAsync(long id, SaveQcmRequest request, CancellationToken ct)
        {
            Validate(request);
            return await repository.UpdateAsync(id, request, ct);
        }

        public async Task<bool> DeleteAsync(long id, CancellationToken ct)
        {
            return await repository.DeleteAsync(id, ct);
        }

        private async Task<QcmModel> BuildModelAsync(QcmQuestionEntity entity, CancellationToken ct)
        {
            var rows = await repository.GetAnswersAsync(entity.Id, ct);

            var model = new QcmModel
            {
                Id = entity.Id,
                Question = entity.Question,
                IdCategory = entity.IdCategory,
                Author = entity.Author,
                CreationDate = ParseDate(entity.CreationDate),
                LastUpdatedDate = ParseDate(entity.LastUpdatedTDate),
                Answers = rows.Select(x => new QcmPropositionModel
                {
                    Id = x.Id,
                    IdQCMAnswer = x.IdQCMAnswer,
                    Answer = x.Answer,
                    IsTrue = string.Equals(x.IsTrue, "true", StringComparison.OrdinalIgnoreCase),

                }).ToList()
            };
            return model;
        }

        private static DateTimeOffset? ParseDate(string? date)
        {
            if (string.IsNullOrEmpty(date))
                return null;
            if (DateTimeOffset.TryParse(date, out var result))
                return result;
            return null;
        }

        private static void Validate(SaveQcmRequest request)
        {
            if (string.IsNullOrEmpty(request.Question))
                throw new ArgumentException("Question cannot be null or empty.", nameof(request.Question));
            if (request.IdCategory <= 0)
                throw new ArgumentException("Invalid category", nameof(request.IdCategory));
            if (request.Answers == null || request.Answers.Count is < 2 or >8)
                throw new ArgumentException("At least two answers are required.", nameof(request.Answers));
            if (request.Answers.Any(x => string.IsNullOrEmpty(x.Answer)))
                throw new ArgumentException("Answer cannot be null or empty.", nameof(request.Answers));
            if (request.Answers.Count(x => x.IsTrue) < 1)
                throw new ArgumentException("At leastone answer must be marked as true.", nameof(request.Answers));
        }
    }
}
