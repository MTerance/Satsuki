using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;

namespace AkibaQuiz.Application.Interfaces;

public interface IGameService
{
    Task<IReadOnlyList<GameModel>> GetAllAsync(CancellationToken ct);
    Task<GameModel?> GetByIdAsync(long id, CancellationToken ct);
    Task<IReadOnlyList<GameSummaryModel>> GetSummariesAsync(CancellationToken ct);
    Task<GameFullModel?> GetFullAsync(long id, CancellationToken ct);
    Task<GameModel> SaveAsync(long? id, SaveGameRequest request, string author, CancellationToken ct);
    Task<bool> DeleteAsync(long id, CancellationToken ct);
}
