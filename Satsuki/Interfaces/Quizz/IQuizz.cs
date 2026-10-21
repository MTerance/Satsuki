using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Interfaces.Quizz
{
    public interface IQuizz
    {
        string      GetQuizzTypeName();
        string      GetQuizzState();
        void        SetQuizzContent(IQuizzModel model);
    }
}
