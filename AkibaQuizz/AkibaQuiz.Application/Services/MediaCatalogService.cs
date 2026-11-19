using AkibaQuiz.Application.Interfaces;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Services
{
    public sealed class MediaCatalogService : IMediaCatalogService
    {
        private readonly IMediaCatalogRepository _repository;

        public MediaCatalogService(IMediaCatalogRepository repository)
        {
            _repository = repository;
        }

        public async Task<long> ResolveOrCreateAsync(string orchardPath, string mediaType, CancellationToken cancellationToken)
        {
            return await _repository.ResolveOrCreateAsync(orchardPath, mediaType, cancellationToken);
        }
    }
}
