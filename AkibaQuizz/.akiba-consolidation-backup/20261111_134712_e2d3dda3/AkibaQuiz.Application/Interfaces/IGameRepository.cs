using AkibaQuiz.Contracts;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Interfaces
{
    public interface IGameRepository
    {
        Task<List<GameDto>> All(CancellationToken ct);

        Task<GameDto?> Get(long id, CancellationToken ct);

        Task<long> Save(
            long? id,
            GameWrite value,
            string author,
            CancellationToken ct);

        Task<bool> Delete(
            long id,
            CancellationToken ct);
    }
}
