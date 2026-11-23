using AkibaQuiz.Application.Auditing;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Application.Interfaces
{
    public interface IAuditActorProvider
    {
        AuditActor GetCurrent();
    }
}
