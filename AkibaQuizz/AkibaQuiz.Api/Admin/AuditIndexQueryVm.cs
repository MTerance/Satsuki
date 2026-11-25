using AkibaQuiz.Application.Auditing;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Admin
{
    public sealed class AuditIndexQueryVm
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

        public AuditFilter ToFilter() => new()
        {
            EntityType = EntityType,
            EntityId = EntityId,
            Action = Action,
            ActorType = ActorType,
            ActorId = ActorId,
            CorrelationId = CorrelationId,
            DateFrom = DateFrom,
            DateTo = DateTo,
            Page = Page,
            PageSize = PageSize
        };
    }

    public sealed class QuizAuditIndexVm
    {
        public AuditIndexQueryVm Filters { get; init; }
            = new();

        public AuditPage Results { get; init; }
            = new();
    }
}
