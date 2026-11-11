using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;

namespace AkibaQuiz.Application.Interfaces;

public interface IQuestionRepository
{
    Task<IReadOnlyList<QuestionAnswerModel>> GetAllAsync(CancellationToken ct);
    Task<QuestionAnswerModel?> GetByIdAsync(long id, CancellationToken ct);
    Task<long> SaveAsync(long? id, SaveQuestionAnswerRequest request, string author, CancellationToken ct);
    Task<bool> DeleteAsync(long id, CancellationToken ct);
}
