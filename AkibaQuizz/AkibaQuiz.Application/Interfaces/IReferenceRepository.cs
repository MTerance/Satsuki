using AkibaQuiz.Contracts;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Interfaces
{
    public interface IReferenceRepository 
    { 
        Task<List<CategoryDto>> Categories(CancellationToken ct);
        Task<List<TagDto>> Tags(CancellationToken ct);
    }
}
