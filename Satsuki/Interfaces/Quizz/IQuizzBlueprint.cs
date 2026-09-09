using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Interfaces.Quizz
{
    public interface IQuizzBlueprint
    {
        string TypeQuizz { get; set; }
        IQuizzModel Quizz { get; set; }
    }
}
