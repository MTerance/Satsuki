using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;

namespace AkibaQuiz.Application.Interfaces;

public interface IQuestionService
{
    Task<IReadOnlyList<QuestionAnswerModel>> GetAllAsync(CancellationToken ct);
    Task<QuestionAnswerModel?> GetByIdAsync(long id, CancellationToken ct);
    Task<QuestionAnswerModel> SaveAsync(long? id, SaveQuestionAnswerRequest request, string author, CancellationToken ct);
    Task<bool> DeleteAsync(long id, CancellationToken ct);
}
