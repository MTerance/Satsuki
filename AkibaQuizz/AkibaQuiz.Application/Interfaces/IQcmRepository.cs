using AkibaQuiz.Contracts.Entities;
using AkibaQuiz.Contracts.Requests;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Interfaces
{
    public sealed class QcmAnswerRow
    {
        public long Id { get; set; }
        public long IdQCMAnswer { get; set; }
        public string Answer { get; set; } = "";
        public string IsTrue { get; set; } = "FALSE";
    }


    public interface IQcmRepository
    {
        Task<IReadOnlyList<QcmQuestionEntity>> GetAllAsync(CancellationToken ct = default);

        Task<QcmQuestionEntity?> GetQuestionAsync(long id, CancellationToken ct = default);

        
        Task<IReadOnlyList<QcmAnswerRow>> GetAnswersAsync(long id, CancellationToken ct = default);
        

        Task<long> CreateAsync(
            SaveQcmRequest request,
            string author,
            CancellationToken ct = default);

        Task<bool> UpdateAsync(
            long id,
            SaveQcmRequest request,
            CancellationToken ct = default);

        Task<bool> DeleteAsync(
            long id, CancellationToken ct = default);
    }
}
