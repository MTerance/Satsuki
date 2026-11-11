using AkibaQuiz.Contracts;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Interfaces
{
    public interface IQuestionRepository
    { 
        Task<List<QuestionDto>> All(CancellationToken ct);
        Task<QuestionDto?> Get(long id, CancellationToken ct);
        Task<long> Save(long? id, QuestionWrite value, string author, CancellationToken ct);
        Task<bool> Delete(long id, CancellationToken ct);
    }
}
