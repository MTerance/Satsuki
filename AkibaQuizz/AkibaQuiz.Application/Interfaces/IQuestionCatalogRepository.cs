using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Interfaces
{
    public interface IQuestionCatalogRepository
    {
        Task<QuestionCatalogPage> SearchAsync(QuestionCatalogQuery query,
            CancellationToken ct);
        Task<IReadOnlyList<QuestionLabelModel>> GetLabelsByIdsAsync(IEnumerable<long> questionIds,
            IEnumerable<long> qcmIds,
            CancellationToken ct);
    }
}
