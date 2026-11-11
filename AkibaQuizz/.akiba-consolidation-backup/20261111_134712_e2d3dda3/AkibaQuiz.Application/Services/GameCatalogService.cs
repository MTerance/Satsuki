
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Application.Catalog;

namespace AkibaQuiz.Application.Services
{
    public sealed class GameCatalogService : IGameCatalogService
    {
        private readonly IGameCatalogRepository _gameCatalogRepository;

        public GameCatalogService(IGameCatalogRepository gameCatalogRepository)
        {
            _gameCatalogRepository = gameCatalogRepository;
        }

        public Task<IReadOnlyList<GameSummaryDto>> GetGamesAsync(CancellationToken cancellationToken)
        {
            return _gameCatalogRepository.GetGamesAsync(cancellationToken);
        }
    }
}
