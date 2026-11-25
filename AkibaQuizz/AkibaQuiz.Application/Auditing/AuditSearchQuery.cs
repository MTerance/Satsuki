using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Auditing
{
    public sealed class AuditSearchQuery
    {
        public string? EntityType { get; set; }
        public long? EntityId { get; set; }
        public string? Action { get; set; }
        public string? ActorType { get; set; }
        public string? ActorId { get; set; }
        public string? CorrelationId { get; set; }
        public DateOnly? DateFrom { get; set; }
        public DateOnly? DateTo { get; set; }

        public int Page { get; set; } = 1;
        public int PageSize { get; set; } = 25;
    }

    public sealed class AuditEventRow
    {
        public long Id { get; set; }
        public string OccurredAtUtc { get; set; } = "";
        public string EntityType { get; set; } = "";
        public long EntityId { get; set; }
        public string Action { get; set; } = "";
        public string ActorType { get; set; } = "";
        public string ActorId { get; set; } = "";

        public string? CorrelationId { get; set; }
        public string? DetailsJson { get; set; }
    }

    public sealed class AuditPage
    {
        public IReadOnlyList<AuditEventRow> Items { get; init; }
            = [];
        public long TotalCount { get; init; }
        public int Page { get; init; }
        public int PageSize { get; init; }
        public long TotalPages =>
            PageSize <= 0
                ? 0
                : (TotalCount + PageSize - 1) / PageSize;
    }
}
