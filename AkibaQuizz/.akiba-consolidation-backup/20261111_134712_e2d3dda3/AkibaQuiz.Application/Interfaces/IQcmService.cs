using AkibaQuiz.Contracts.Requests;
using AkibaQuiz.Contracts.Models;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace AkibaQuiz.Application.Interfaces
{
    public interface IQcmService
    {
        Task<IReadOnlyList<QcmModel>> GetAllAsync(CancellationToken ct);
        Task<QcmModel?> GetByIdAsync(long id, CancellationToken ct);
        Task<QcmModel> CreateAsync(SaveQcmRequest request, string author, CancellationToken ct);
        Task<bool> UpdateAsync(long id, SaveQcmRequest request, CancellationToken ct);
        Task<bool> DeleteAsync(long id, CancellationToken ct);
    }
}
