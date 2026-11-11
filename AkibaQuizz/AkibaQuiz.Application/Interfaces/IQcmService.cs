using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;

namespace AkibaQuiz.Application.Interfaces;

public interface IQcmService
{
    Task<IReadOnlyList<QcmModel>> GetAllAsync(CancellationToken ct);
    Task<QcmModel?> GetByIdAsync(long id, CancellationToken ct);
    Task<QcmModel> SaveAsync(long? id, SaveQcmRequest request, string author, CancellationToken ct);
    Task<bool> DeleteAsync(long id, CancellationToken ct);
}
