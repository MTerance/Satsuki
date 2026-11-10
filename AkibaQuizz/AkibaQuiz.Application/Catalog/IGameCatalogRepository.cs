using AkibaQuiz.Contracts.Models;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Catalog
{
    public interface IGameCatalogRepository
    {
        Task<IReadOnlyList<GameSummaryDto>> GetGamesAsync(CancellationToken ct);
    }
}
