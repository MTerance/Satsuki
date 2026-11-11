using AkibaQuiz.Contracts.Models;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Interfaces
{
    public interface IGameCatalogService
    {
        Task<IReadOnlyList<GameSummaryDto>> GetGamesAsync(CancellationToken cancellationToken);
    }
}
