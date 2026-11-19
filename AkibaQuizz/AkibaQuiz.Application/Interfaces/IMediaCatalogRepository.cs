using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Interfaces
{
    public interface IMediaCatalogRepository
    {
        Task<long> ResolveOrCreateAsync(string orchardPath, string mediaType, CancellationToken cancellationToken);
    }
}
