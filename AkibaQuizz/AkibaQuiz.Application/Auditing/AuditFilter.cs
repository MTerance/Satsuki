using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Auditing
{
    public sealed record AuditFilter
    {
        public string? EntityType { get; init; }
        public long? EntityId { get; init; }

        public string? Action { get; init; }

        public string? ActorType { get; init; }
        public string? ActorId { get; init; }

        public string? CorrelationId { get; init; }

        public DateOnly? DateFrom { get; init; }
        public DateOnly? DateTo { get; init; }

        public int Page { get; init; } = 1;
        public int PageSize { get; init; } = 25;
    }
}
