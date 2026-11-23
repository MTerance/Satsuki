using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Auditing
{
    public sealed record AuditActor(
        string ActorType,
        string ActorId,
        string? CorrelationId
    );
}
